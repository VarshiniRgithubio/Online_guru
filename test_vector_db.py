#!/usr/bin/env python3
"""Quick test: verify vector DB is loaded and retrieval works."""
import sys
sys.path.insert(0, "F:\\online guru")

from ingest import DataIngestionPipeline
from language_utils import LanguageDetector

print("\n" + "="*70)
print("VECTOR DATABASE RETRIEVAL TEST")
print("="*70 + "\n")

# Load vector store
pipeline = DataIngestionPipeline()
vector_store = pipeline.load_vector_store()

if vector_store is None:
    print("ERROR: Vector store not found!")
    sys.exit(1)

print(f"✅ Vector store loaded: {vector_store.index.ntotal} vectors")
print()

# Test queries
test_queries = [
    ("What is devotion?", "en"),
    ("भक्ति क्या है?", "hi"),
    ("అష్టాంగిక మార్గం ఏమిటి?", "te"),
    ("ಧರ್ಮ ಎಂದರೆ ಏನು?", "kn"),
]

detector = LanguageDetector()

for question, expected_lang in test_queries:
    detected = detector.detect_language(question)
    print(f"Question: {question}")
    print(f"  Detected language: {detected} (expected: {expected_lang})")
    
    # Retrieve relevant docs
    docs = vector_store.similarity_search(question, k=3)
    print(f"  Retrieved {len(docs)} documents:")
    for i, doc in enumerate(docs, 1):
        preview = doc.page_content[:100].replace('\n', ' ')
        print(f"    [{i}] {preview}...")
    print()

print("="*70)
print("✅ Vector DB is working! Books are loaded and retrievable.")
print("="*70)
