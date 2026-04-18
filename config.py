import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
    
    # Model configuration
    MODEL_NAME = 'mixtral-8x7b-32768'
    TEMPERATURE = 0.2
    MAX_TOKENS = 800

    SYSTEM_PROMPT = """You are a senior Site Reliability Engineer with deep experience in production outages.
Analyze the following incident and return ONLY valid JSON. No markdown, no explanations outside JSON.
Each list must contain concise, actionable items. Avoid generic advice.

Return this exact JSON format:
{
  "root_causes": ["cause1", "cause2"],
  "resolution_steps": ["step1", "step2"],
  "priority_actions": {
    "immediate": ["action1", "action2"],
    "short_term": ["action1", "action2"],
    "long_term": ["action1", "action2"]
  },
  "confidence": "High"
}

confidence must be: "High", "Medium", or "Low"
All lists must have at least 2 items.
Be specific, not generic."""

    FALLBACK_RESPONSE = {
        "root_causes": [
            "Unable to determine from provided information",
            "Retry analysis with more detailed logs"
        ],
        "resolution_steps": [
            "Review application logs for error patterns",
            "Check system resource usage (CPU, memory, disk)",
            "Inspect recent deployment changes",
            "Verify external service dependencies"
        ],
        "priority_actions": {
            "immediate": [
                "Stabilize affected services",
                "Alert incident response team"
            ],
            "short_term": [
                "Root cause analysis",
                "Temporary mitigation if needed"
            ],
            "long_term": [
                "Implement monitoring for this issue",
                "Post-incident review and documentation"
            ]
        },
        "confidence": "Low"
    }
