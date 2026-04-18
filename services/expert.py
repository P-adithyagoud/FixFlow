import os
import httpx
from config.settings import Settings

class IncidentExpert:
    """
    SRE Specialist AI that analyzes current issues using historical bridge context.
    Communicates with Groq via high-performance HTTPX.
    """

    @staticmethod
    def analyze(query, context_incidents):
        """Perform a deep analysis of the incident using historical data."""
        client_key = os.getenv("GROQ_API_KEY")
        if not client_key:
            return None

        # Build context string from past incidents
        knowledge_context = ""
        for i, inc in enumerate(context_incidents):
            knowledge_context += f"\n[Case {i+1}]:\nIssue: {inc['issue']}\nRoot Cause: {inc['root_cause']}\nResolution: {inc['resolution']}\n"

        user_content = f"CONTEXT FROM HISTORICAL INCIDENTS:\n{knowledge_context}\n\nCURRENT ISSUE TO ANALYZE:\n{query}"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {client_key}"},
                    json={
                        "model": Settings.MODEL_NAME,
                        "messages": [
                            {"role": "system", "content": Settings.SYSTEM_PROMPT},
                            {"role": "user", "content": user_content}
                        ],
                        "temperature": Settings.TEMPERATURE,
                        "max_tokens": Settings.MAX_TOKENS
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data['choices'][0]['message']['content']
                
                print(f"Expert API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Expert System Failure: {str(e)}")
            return None
