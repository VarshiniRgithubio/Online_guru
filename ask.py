#!/usr/bin/env python3
"""CLI for asking the Online Guru questions using the FAISS vector DB and OpenAI.

Usage:
    python ask.py

Behavior:
 - Prompts: "Ask your question to the Online Guru:"
 - Loads `vector_db/index.faiss` and `index.pkl` via `ingest.DataIngestionPipeline`.
 - If DB missing, prints the required message and exits.
 - If DB exists, retrieves relevant passages and calls OpenAI to produce
   a calm, divine, 1-2 paragraph answer grounded in the PDF content.
"""

from __future__ import annotations

import os
import sys
from typing import List
from loguru import logger

try:
    from ingest import DataIngestionPipeline
except Exception:
    DataIngestionPipeline = None

try:
    import openai
except Exception:
    openai = None


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


def build_prompt(question: str, passages: List[str]) -> str:
    context = "\n\n".join(passages)
    prompt = (
        "You are the Online Guru: respond in a calm, divine, god-like tone. "
        "Produce 1–2 meaningful paragraphs. Use ONLY the information provided in the 'CONTEXT' below to answer. "
        "Do NOT invent facts or contradict the context. If context does not contain the answer, say you cannot find a direct answer in the documents.\n\n"
        "CONTEXT:\n" + context + "\n\n"
        "QUESTION:\n" + question + "\n\n"
        "INSTRUCTIONS:\n"
        "- Keep the answer 1–2 paragraphs.",
    )
    return prompt


def format_sources(metas: List[dict]) -> List[str]:
    names = []
    for m in metas:
        if not m:
            continue
        src = m.get("source") or m.get("filename") or m.get("file") or m.get("source_name")
        if src and src not in names:
            names.append(src)
    return names


class SimpleChatbot:
    """Minimal chatbot class used by simple_api. Provides `ask(question, language)`.

    This implementation retrieves passages from the FAISS vector store and returns
    a concatenated answer and source list. If the DB is missing, it returns the
    required guidance message.
    """

    def __init__(self):
        self.pipeline = DataIngestionPipeline() if DataIngestionPipeline is not None else None
        self.vector = None
        if self.pipeline is not None:
            try:
                self.vector = self.pipeline.load_vector_store()
            except Exception:
                self.vector = None

    def ask(self, question: str, language: str = "en"):
        if self.vector is None:
            return {
                "answer": "Knowledge base not built. Please run python ingest.py --rebuild",
                "language": language or "en",
                "sources": [],
                "is_safe": False,
            }

        try:
            hits = self.vector.similarity_search(question, k=4)
            passages = [h.get("page_content", "") for h in hits if h.get("page_content")]
            metas = [h.get("metadata", {}) for h in hits]
            answer = "\n\n".join(passages)[:4000]
            sources = [{"content": s} for s in format_sources(metas)]
            return {"answer": answer, "language": language or "en", "sources": sources, "is_safe": True}
        except Exception as e:
            return {"answer": f"Retrieval failed: {e}", "language": language or "en", "sources": [], "is_safe": False}


def call_openai(prompt: str) -> str:
    if openai is None:
        raise RuntimeError("openai package not installed or failed to import")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")

    def _extract_message(resp):
        # Try several common response shapes (new and old OpenAI python libs)
        try:
            return resp["choices"][0]["message"]["content"]
        except Exception:
            pass
        try:
            return resp.choices[0].message.content
        except Exception:
            pass
        try:
            return resp["choices"][0]["text"]
        except Exception:
            pass
        try:
            return resp.choices[0].text
        except Exception:
            pass
        raise RuntimeError("Unable to parse OpenAI response")

    # Prefer the new OpenAI client if available (openai.OpenAI)
    OpenAIClient = getattr(openai, "OpenAI", None)
    if OpenAIClient is not None:
        client = OpenAIClient(api_key=api_key)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a wise, calm spiritual guide."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.6,
        )
        return _extract_message(resp).strip()

    # Fallback to older openai package interface
    openai.api_key = api_key
    resp = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a wise, calm spiritual guide."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=400,
        temperature=0.6,
    )
    return _extract_message(resp).strip()


def main():
    print("Ask your question to the Online Guru:")
    question = input("> ").strip()
    if not question:
        print("No question provided. Exiting.")
        return

    # Load vector DB
    if DataIngestionPipeline is None:
        print("Knowledge base not built. Please run python ingest.py --rebuild")
        return

    pipeline = DataIngestionPipeline()
    vector = pipeline.load_vector_store()
    if vector is None:
        print("Knowledge base not built. Please run python ingest.py --rebuild")
        return

    # Retrieve
    try:
        hits = vector.similarity_search(question, k=4)
    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        print("Retrieval failed. Exiting.")
        return

    if not hits:
        print("No relevant documents found in the knowledge base.")
        return

    # hits expected to be list of dicts with 'page_content' and 'metadata'
    passages = [h.get("page_content", "") for h in hits if h.get("page_content")]
    metas = [h.get("metadata", {}) for h in hits]
    sources = format_sources(metas)

    prompt = build_prompt(question, passages)

    try:
        answer = call_openai(prompt)
    except Exception as e:
        logger.error(f"OpenAI call failed: {e}")
        print("OpenAI call failed:", e)
        return

    # Ensure 1-2 paragraphs: if model returned more, truncate to first two paragraphs
    paras = [p.strip() for p in answer.split('\n\n') if p.strip()]
    answer_out = "\n\n".join(paras[:2])

    print("\n" + answer_out + "\n")
    if sources:
        print("Sources:")
        for s in sources:
            print(" -", s)


if __name__ == "__main__":
    main()
