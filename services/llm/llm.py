from dotenv import load_dotenv
import os
from pathlib import Path
from graphrag.query.factories import get_llm as get_graphrag_llm
from graphrag.config import load_config
from openai import OpenAI

load_dotenv()

# Singleton class for LLM client
class LLMClient:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.llm = self._get_llm()
            self.embeddings_client = OpenAI(api_key=os.getenv("GRAPHRAG_API_KEY"))
            self._initialized = True

    def _get_llm(self):
        return get_graphrag_llm(load_config(Path('.')))

    def generate(self, messages, max_tokens=None):
        kwargs = {'messages': messages}
        if max_tokens is not None:
            kwargs['max_tokens'] = max_tokens
        return self.llm.generate(**kwargs)

    def get_embeddings(self, text, model=os.getenv("EMBEDDING_MODEL_NAME")):
        client = self.embeddings_client
        text = text.replace("\n", " ")
        return client.embeddings.create(input = [text], model=model).data[0].embedding
