import re

class MatcherService:
    """
    Intelligent Correlation Engine: Identifies similar past incidents.
    A simple but highly effective keyword-overlap algorithm.
    """

    @staticmethod
    def extract_keywords(text):
        """Pre-processes text and isolates technical keywords."""
        if not text: 
            return set()
            
        # Extract alphanumeric words and lowercase
        words = re.findall(r'\w+', text.lower())
        
        # SRE-specific filter (ignore basic language boilerplate)
        boilerplate = {'a', 'an', 'the', 'and', 'or', 'if', 'to', 'in', 'is', 'it', 'of', 'for', 'with'}
        return {w for w in words if w not in boilerplate and len(w) > 2}

    @classmethod
    def rank_correlated_knowledge(cls, query, knowledge_base, top_n=3):
        """Cross-references query against all archived production knowledge."""
        if not knowledge_base or not query: 
            return []
            
        current_keywords = cls.extract_keywords(query)
        scored_incidents = []
        
        for item in knowledge_base:
            # Match against issue description and keywords
            context_text = f"{item.get('issue', '')} {item.get('tags', '')}"
            item_keywords = cls.extract_keywords(context_text)
            
            relevance_score = len(current_keywords.intersection(item_keywords))
            if relevance_score > 0:
                scored_incidents.append((relevance_score, item))
        
        # Sort by relevance score (descending)
        scored_incidents.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_incidents[:top_n]]

    @staticmethod
    def identify_confidence(match_count):
        """Quantifies the strength of historical correlation."""
        if match_count >= 2: return "High"
        if match_count == 1: return "Medium"
        return "Low"
