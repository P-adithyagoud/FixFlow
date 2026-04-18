import json
import re

class ResponseFormatter:
    """
    Utility for sanitizing and validating data from the AI Expert.
    Ensures the UI receives strict, usable JSON.
    """

    @staticmethod
    def to_json(raw_text):
        """Extract and parse JSON from raw LLM output."""
        if not raw_text:
            return None
            
        try:
            # Look for JSON structure in case LLM added conversational text
            json_match = re.search(r'(\{.*\})', raw_text, re.DOTALL)
            json_str = json_match.group(1) if json_match else raw_text
            return json.loads(json_str)
        except (json.JSONDecodeError, AttributeError):
            print("Formatter: Failed to parse AI response into JSON.")
            return None

    @staticmethod
    def validate_schema(data, required_keys):
        """Verify that the JSON result matches our production schema."""
        if not isinstance(data, dict):
            return False
        return all(key in data for key in required_keys)
