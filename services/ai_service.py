import os
import httpx
from config import Config

class AIService:
    """
    SRE Expert Engine: Conducts intelligent analysis using Groq infrastructure.
    Refactored for clarity, functionality remains unchanged.
    """

    @staticmethod
    def generate_resolution_analysis(query, matched_knowledge):
        """Generates a detailed incident report using RAG-lite context."""
        client_key = os.getenv("GROQ_API_KEY")
        if not client_key:
            return None

        # Build context from past historical data
        past_cases = ""
        for i, inc in enumerate(matched_knowledge):
            past_cases += f"\n[PAST CASE {i+1}]:\n- Issue: {inc['issue']}\n- Cause: {inc['root_cause']}\n- Fix: {inc['resolution']}\n"

        system_instruction = Config.SYSTEM_PROMPT
        user_input = f"HISTORICAL KNOWLEDGE BASE:\n{past_cases}\n\nCURRENT PRODUCTION ISSUE:\n{query}"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {client_key}"},
                    json={
                        "model": Config.MODEL_NAME,
                        "messages": [
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_input}
                        ],
                        "temperature": Config.TEMPERATURE,
                        "max_tokens": Config.MAX_TOKENS
                    }
                )
                
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
                return None
        except Exception as e:
            print(f"Expert Engine Error: {str(e)}")
            return None
