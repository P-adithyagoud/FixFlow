class Validator:
    @staticmethod
    def validate_incident(incident):
        """Validate incident input."""
        if not incident or not isinstance(incident, str):
            return False, "Incident must be a non-empty string"
        
        incident = incident.strip()
        
        if len(incident) < 10:
            return False, "Incident description too short (min 10 characters)"
        
        if len(incident) > 3000:
            return False, "Incident description too long (max 3000 characters)"
        
        return True, None
