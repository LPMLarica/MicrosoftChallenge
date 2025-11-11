from transformers import pipeline
from sentence_transformers import SentenceTransformer
from typing import List

class HFLocalClient:
    def __init__(self):
        try:
            self.classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
        except Exception:
            self.classifier = pipeline('zero-shot-classification')
        try:
            self.summarizer = pipeline('summarization', model='philschmid/bart-large-cnn-samsum')
        except Exception:
            self.summarizer = pipeline('summarization')
        try:
            self.qa = pipeline('question-answering', model='deepset/roberta-base-squad2')
        except Exception:
            self.qa = pipeline('question-answering')
        try:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception:
            self.embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def classify(self, text: str, labels: List[str]):
        return self.classifier(text, candidate_labels=labels)

    def summarize(self, text: str, max_length: int = 120):
        return self.summarizer(text, max_length=max_length, min_length=20)

    def answer(self, question: str, context: str):
        return self.qa({'question': question, 'context': context})

    def embed(self, texts):
        return self.embedder.encode(texts)

_client = None

def get_hf_client():
    global _client
    if _client is None:
        _client = HFLocalClient()
    return _client
