from typing import Dict, List
from services.llm.llm import LLMClient
class QueryClassifier:
    def __init__(self):
        self.llm = LLMClient().llm
        self._load_prompts()

    def _load_prompts(self):
        """Load classification prompts from config or constants."""
        self.system_prompt = """
            You are a helpful assistant that classifies queries into three categories: 'local', 'global', or 'drift'.
            Use the following definitions to classify the query accurately:

            - **Local Search**: Generates answers by combining relevant data from the AI-extracted knowledge graph with specific text chunks from raw documents.
              This is ideal for questions that require understanding specific entities mentioned within the documents.
              Example: "What are the healing properties of chamomile?"

            - **Global Search**: Generates answers by searching across all AI-generated community reports in a map-reduce fashion.
              This method is resource-intensive but suitable for questions requiring an understanding of the entire dataset.
              Example: "What are the most significant values of the herbs mentioned in this notebook?"

            - **DRIFT Search**: Expands local search queries by incorporating community information, broadening the query's scope and retrieving a larger variety of facts.
              This is ideal for questions that would benefit from both document-specific and community-based insights.
              Example: "What are the most recent trends in the use of herbal medicine?"

            Based on the definitions above, respond with only the classification ('local', 'global', or 'drift') without any explanation.
        """

    def classify(self, query: str) -> str:
        """Classify the query into search types."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Query: {query}. Which classification does this query fall into? Class:"}
        ]

        response = self.llm.generate(messages, max_tokens=1)

        return response if response in ['local', 'global', 'drift'] else 'local'