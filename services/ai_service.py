import httpx
from config import Config

class AIService:
    @staticmethod
    def analyze_incident(incident_text):
        """Call Groq API with incident details."""
        if not Config.GROQ_API_KEY:
            return None
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    Config.GROQ_API_URL,
                    headers={
                        'Authorization': f'Bearer {Config.GROQ_API_KEY}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': Config.MODEL_NAME,
                        'messages': [
                            {
                                'role': 'system',
                                'content': Config.SYSTEM_PROMPT
                            },
                            {
                                'role': 'user',
                                'content': f"Incident:\n{incident_text}"
                            }
                        ],
                        'temperature': Config.TEMPERATURE,
                        'max_tokens': Config.MAX_TOKENS
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        return data['choices'][0]['message']['content']
                
                return None
        
        except Exception as e:
            print(f"AI Service Error: {str(e)}")
            return None
