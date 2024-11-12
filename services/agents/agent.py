from typing import Dict, Optional
from .classifier import QueryClassifier
from .searcher import DocumentSearcher
from .reformulator import AnswerReformulator

class Agent:
    def __init__(self):
        """Initialize the Agent with its components."""
        self.classifier = QueryClassifier()
        self.searcher = DocumentSearcher()
        self.reformulator = AnswerReformulator()

    def __call__(self, document_id: str, question: str) -> Dict[str, str]:
        """Process a question through the complete pipeline."""
        method = self.classifier.classify(question)
        response = self.searcher.search(document_id, question, method)
        response = self.reformulator.reformulate(response)
        return response