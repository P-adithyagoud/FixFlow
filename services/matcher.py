import re

class KnowledgeMatcher:
    """
    Engine for finding similar past incidents based on keyword overlap.
    Essential for providing context to the AI Expert.
    """

    @staticmethod
    def get_keywords(text):
        """Extract meaningful technical keywords from text."""
        if not text:
            return set()
        words = re.findall(r'\w+', text.lower())
        stopwords = {'a', 'an', 'the', 'and', 'or', 'if', 'to', 'in', 'is', 'it', 'of', 'for', 'with'}
        return {w for w in words if w not in stopwords and len(w) > 2}

    @classmethod
    def find_matches(cls, query, library, top_n=3):
        """Rank existing knowledge by relevance to the current issue."""
        if not library or not query:
            return []
        
        query_keywords = cls.get_keywords(query)
        scored_items = []
        
        for item in library:
            item_text = f"{item.get('issue', '')} {item.get('tags', '')}"
            item_keywords = cls.get_keywords(item_text)
            overlap = query_keywords.intersection(item_keywords)
            
            if len(overlap) > 0:
                scored_items.append((len(overlap), item))
        
        # Sort by relevance (match count)
        scored_items.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_items[:top_n]]

    @staticmethod
    def calculate_confidence(matches_count):
        """Quantify the reliability of the suggested solution."""
        if matches_count >= 2: return "High"
        if matches_count == 1: return "Medium"
        return "Low"
