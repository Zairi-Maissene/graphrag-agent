from graphrag.config import load_config
from pathlib import Path
from typing import Dict, Optional
from services.llm.llm import LLMClient

class AnswerReformulator:
    def __init__(self):
        self.llm = LLMClient().llm


    def reformulate(self, answer: str) -> str:
        """Reformulate the answer to be more educational and motivational."""
        if answer == 'No valid answer found.':
            return answer
        messages = [
            {
                "role": "system",
                "content": """
               You are an expert at reformulating answers in an educational and motivational way.
                Your task is to:
                1. Keep all factual information exactly as provided - do not add external knowledge
                2. Make the tone more engaging and educational
                3. Add learning-oriented framing where appropriate

                Example transformation:
                Original: "Chamomile contains compounds that reduce inflammation"
                Reformulated: "Let's explore what makes chamomile so special! In our studies, we've discovered that this fascinating herb contains compounds that reduce inflammation. Understanding this property helps us appreciate how traditional remedies work."
                """
            },
            {
                "role": "user",
                "content": f"Please reformulate this answer in an educational and motivational way, while maintaining strict accuracy:\n\n{answer}"
            }
        ]

        try:
            return self.llm.generate(messages)
        except Exception as e:
            print(f"Error reformulating answer: {e}")
            return answer

