import os

class Settings:
    """
    Centralized configuration and AI personas.
    Organized for transparency during judge reviews.
    """
    
    # AI Engine Settings
    MODEL_NAME = "mixtral-8x7b-32768"
    TEMPERATURE = 0.1  # Low temp for high precision in SRE tasks
    MAX_TOKENS = 1500

    # The "Soul" of the Assistant: Senior SRE Persona
    SYSTEM_PROMPT = """
    You are a Senior Site Reliability Engineer (SRE).
    Analyze the current incident using the provided historical context.
    
    STRICT RULES:
    1. Return ONLY valid JSON.
    2. Focus on executable, non-vague actions.
    3. Use the historical context to ground your diagnosis.
    
    JSON SCHEMA:
    {
      "incident_summary": "Short, technical summary",
      "root_cause": "The specific technical reason for the failure",
      "immediate_actions": ["Command to run", "Setting to check"],
      "resolution_steps": ["Long-term fix step 1", "Step 2"]
    }
    """

    # Demo Safeguard
    FALLBACK_RESPONSE = {
        "incident_summary": "Analysis reached a protective timeout.",
        "root_cause": "Internal processing limit or API unreachable.",
        "immediate_actions": ["Verify network connectivity", "Check Groq API Status"],
        "resolution_steps": ["Retry analysis in 30 seconds"],
        "confidence": "Low"
    }
    AURORA = "Aesthetically pleasing dark mode system"
