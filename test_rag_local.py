from rag_engine import MultilingualRAGEngine

class Doc:
    def __init__(self, text, meta=None):
        self.page_content = text
        self.metadata = meta or {}

eng = MultilingualRAGEngine()
# Ensure LLM is None for this test
eng.llm = None

docs = [
    Doc("Love is selfless service and compassion towards all beings."),
    Doc("Devotion grows through humble service and steady prayer."),
    Doc("Practice compassion daily; be gentle with yourself and others.")
]

print(eng._generate_answer_from_docs(docs, 'en'))
