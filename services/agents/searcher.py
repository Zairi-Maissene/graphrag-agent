import subprocess
import re
from typing import Dict

class DocumentSearcher:

    def search(self, document_id: str, question: str, method: str) -> Dict[str, str]:
        """Execute the search using the specified method."""
        command = f'python -m graphrag query --root graphs/{document_id} --method {method} --query "{question}"'
        response = subprocess.run(command, shell=True, capture_output=True, text=True)

        if response.stdout:
            final_response = self._process_response(response.stdout.strip(), method)
            return final_response

        return "No valid answer found."


    def _process_response(self, response: str, method: str) -> str:
        """Process the raw response from the search command."""
        patterns = {
            'global': r'SUCCESS: Global Search Response:\n(.*)',
            'local': r'SUCCESS: Local Search Response:\n(.*)',
            'drift': r'SUCCESS: Drift Search Response:\n(.*)',
        }

        pattern = patterns.get(method)
        if not pattern:
            return "No valid answer found."

        reference_pattern = r'\[Data: ([^;]+?)(?: \((\d+(?:, \d+)*)\))?\]'

        # Search for any references to data
        ref_matches = re.findall(reference_pattern, response)
        if not ref_matches:
            return "No valid answer found."

        match = re.search(pattern, response, re.DOTALL)
        if not match:
            return "No valid answer found."

        answer = match.group(1).strip()
        answer = re.sub(r'\[(?:Data|Relationships)[^]]*\]', '', answer)
        answer = ' '.join(answer.split())

        return answer



