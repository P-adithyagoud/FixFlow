import os
import httpx
from config import Config

class AIService:
    """
    SRE Expert Engine: Conducts intelligent analysis and knowledge re-ranking.
    """

    @staticmethod
    def generate_resolution_analysis(query, candidate_pool):
        """Generates resolution and ranks the most relevant historical context."""
        client_key = os.getenv("GROQ_API_KEY")
        if not client_key:
            return None

        # Build candidate knowledge base for AI ranking
        candidate_context = ""
        for i, inc in enumerate(candidate_pool):
            # The first 3 come from local_candidates, next 3 from cloud_candidates in app.py
            # Since local is mapped first in app.py: candidate_pool = local_candidates + cloud_candidates
            source = "LOCAL KEDB" if i < len(candidate_pool)-3 else "CLOUD ARCHIVE" 
            # Actually, local_candidates is length 3. So first 3 are Local.
            # Let's be more explicit if possible, but for now we follow the app.py logic.
            # In app.py: local_candidates (top 3) + cloud_candidates (top 3)
            # So i < 3 is LOCAL KEDB.
            source = "LOCAL KEDB" if i < 3 else "CLOUD ARCHIVE"
            
            candidate_context += f"\n[CANDIDATE {i+1} - {source}]:\n- Issue: {inc.get('issue')}\n- Cause: {inc.get('root_cause')}\n- Fix: {inc.get('resolution')}\n"

        system_instruction = Config.SYSTEM_PROMPT
        user_content = f"CANDIDATE HISTORICAL CASES (Analyze and Select Top 3):\n{candidate_context}\n\nCURRENT PRODUCTION ISSUE:\n{query}"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {client_key}"},
                    json={
                        "model": Config.MODEL_NAME,
                        "messages": [
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_content}
                        ],
                        "temperature": Config.TEMPERATURE,
                        "max_tokens": Config.MAX_TOKENS
                    }
                )
                
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
                else:
                    print(f"Groq API Error {response.status_code}: {response.text}")
                    return None
        except Exception as e:
            print(f"Expert Engine Error: {str(e)}")
            return None
