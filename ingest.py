"""Ingest pipeline that builds a FAISS vector DB from PDFs and TXT files in `data/`.

Usage:
    python ingest.py --rebuild

This script is the only file that imports and uses `faiss`.
The API will only LOAD the DB produced by this script; it will never build it.
"""

from __future__ import annotations

import argparse
import shutil
import pickle
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
load_dotenv()

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from loguru import logger

# Configurable paths and model via environment
DATA_DIR = Path(os.getenv("DATA_FOLDER", "data"))
VECTOR_DIR = Path(os.getenv("VECTOR_DB_PATH", "vector_db"))
EMBEDDING_MODEL = os.getenv("MULTILINGUAL_EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
BATCH_SIZE = int(os.getenv("EMB_BATCH_SIZE", "64"))


def find_files(folder: Path, exts: List[str]) -> List[Path]:
    if not folder.exists():
        return []
    paths: List[Path] = []
    for ext in exts:
        paths.extend(folder.rglob(f"*{ext}"))
    return sorted(paths)


def extract_text_from_pdf(path: Path) -> str:
    parts: List[str] = []
    try:
        reader = PdfReader(str(path))
        for page in reader.pages:
            parts.append(page.extract_text() or "")
    except Exception as e:
        logger.warning(f"Failed to read {path}: {e}")
    return "\n".join(parts)


def extract_text_from_txt(path: Path) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception:
        try:
            return Path(path).read_text(encoding="latin-1")
        except Exception as e:
            logger.warning(f"Failed to read txt {path}: {e}")
            return ""


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    if not text:
        return []
    text = "\n".join([ln.strip() for ln in text.splitlines() if ln.strip()])
    chunks: List[str] = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + size, L)
        chunks.append(text[start:end].strip())
        if end == L:
            break
        start = max(end - overlap, end)
    return chunks


class FaissWrapper:
    def __init__(self, index: faiss.Index, metas: List[Dict[str, Any]], embed_model: SentenceTransformer):
        self.index = index
        self.metas = metas
        self.embed_model = embed_model

    def similarity_search(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        q_emb = self.embed_model.encode([query], convert_to_numpy=True)
        q_emb = q_emb.astype("float32")
        faiss.normalize_L2(q_emb)
        D, I = self.index.search(q_emb, k)
        results: List[Dict[str, Any]] = []

        class DocLike:
            def __init__(self, page_content: str, metadata: Dict[str, Any]):
                self.page_content = page_content
                self.metadata = metadata
            def get(self, key, default=None):
                if key == "page_content":
                    return self.page_content
                if key == "metadata":
                    return self.metadata
                return default

        for idx in I[0]:
            if idx < 0 or idx >= len(self.metas):
                continue
            meta = self.metas[idx]
            page = meta.get("text", "")
            results.append(DocLike(page, meta))
        return results


class DataIngestionPipeline:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        logger.info(f"Initializing DataIngestionPipeline with model {self.model_name}")
        self.embed_model = SentenceTransformer(self.model_name)

    def build_vector_db(self, data_folder: Optional[str] = None, force_rebuild: bool = False) -> None:
        data_folder = Path(data_folder or DATA_DIR)

        if force_rebuild and VECTOR_DIR.exists():
            logger.info(f"--rebuild specified: removing existing vector DB at {VECTOR_DIR}")
            shutil.rmtree(VECTOR_DIR)

        if VECTOR_DIR.exists() and not force_rebuild:
            logger.info(f"Vector DB already exists at {VECTOR_DIR}; skipping rebuild.")
            return

        pdfs = find_files(data_folder, [".pdf"])
        txts = find_files(data_folder, [".txt"])
        logger.info(f"Found {len(pdfs)} PDF(s) and {len(txts)} TXT(s) under {data_folder}")

        all_chunks: List[Dict[str, Any]] = []
        for pdf in pdfs:
            text = extract_text_from_pdf(pdf)
            chunks = chunk_text(text)
            logger.info(f"{pdf.name}: {len(chunks)} chunk(s)")
            for i, c in enumerate(chunks):
                all_chunks.append({"source": pdf.name, "chunk_id": i, "text": c})

        for txt in txts:
            text = extract_text_from_txt(txt)
            chunks = chunk_text(text)
            logger.info(f"{txt.name}: {len(chunks)} chunk(s)")
            for i, c in enumerate(chunks):
                all_chunks.append({"source": txt.name, "chunk_id": i, "text": c})

        logger.info(f"Total chunks: {len(all_chunks)}")
        if not all_chunks:
            logger.warning("No chunks to index. Aborting.")
            return

        texts = [d["text"] for d in all_chunks]
        embeddings = []
        logger.info("Computing embeddings...")
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i : i + BATCH_SIZE]
            embs = self.embed_model.encode(batch, show_progress_bar=True, convert_to_numpy=True)
            embeddings.append(embs)
        emb_matrix = np.vstack(embeddings).astype("float32")

        logger.info("Normalizing embeddings and building FAISS index...")
        faiss.normalize_L2(emb_matrix)
        dim = emb_matrix.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(emb_matrix)

        VECTOR_DIR.mkdir(parents=True, exist_ok=True)
        index_path = VECTOR_DIR / "index.faiss"
        meta_path = VECTOR_DIR / "index.pkl"

        logger.info(f"Writing FAISS index to {index_path}...")
        faiss.write_index(index, str(index_path))
        with open(meta_path, "wb") as f:
            pickle.dump(all_chunks, f)

        logger.success(f"FAISS index created with {index.ntotal} vectors at {VECTOR_DIR}")

    def load_vector_store(self, path: Optional[str] = None) -> Optional[FaissWrapper]:
        path = Path(path or VECTOR_DIR)
        index_path = path / "index.faiss"
        meta_path = path / "index.pkl"

        if not index_path.exists() or not meta_path.exists():
            logger.warning(f"Vector DB not found at {path}")
            return None

        try:
            logger.info(f"Loading FAISS index from {index_path}...")
            index = faiss.read_index(str(index_path))
            with open(meta_path, "rb") as f:
                metas = pickle.load(f)
            wrapper = FaissWrapper(index=index, metas=metas, embed_model=SentenceTransformer(self.model_name))
            logger.success("Vector DB loaded successfully")
            return wrapper
        except Exception as e:
            logger.error(f"Failed to load vector DB: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(description="Build FAISS vector DB from PDFs/TXT in data folder")
    parser.add_argument("--rebuild", action="store_true", help="Delete existing vector_db and rebuild")
    args = parser.parse_args()

    pipeline = DataIngestionPipeline()
    pipeline.build_vector_db(force_rebuild=args.rebuild)


if __name__ == "__main__":
    main()
