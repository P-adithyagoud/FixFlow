import json

class ResponseParser:
    @staticmethod
    def parse_json(response_text):
        """Attempt to parse valid JSON from response."""
        try:
            # Basic cleanup in case of leading/trailing text
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                response_text = response_text[start:end]
            
            data = json.loads(response_text)
            
            if not isinstance(data, dict):
                return None
            
            required_keys = ['root_causes', 'resolution_steps', 'priority_actions', 'confidence']
            if not all(key in data for key in required_keys):
                return None
            
            # Additional validation of nested structure
            if not isinstance(data['priority_actions'], dict):
                return None
            
            return data
        
        except (json.JSONDecodeError, ValueError, TypeError):
            return None
