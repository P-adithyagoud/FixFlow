from services.repository import IncidentRepository
from services.matcher import KnowledgeMatcher
from services.expert import IncidentExpert
from utils.formatter import ResponseFormatter
from config.settings import Settings

class IncidentPipeline:
    """
    ONE CLEAR PIPELINE: Input -> Process -> LLM -> Response
    Orchestrates the entire intelligence flow in a single, readable class.
    """

    @classmethod
    def analyze(cls, user_query: str):
        """
        The 30-Second Flow:
        1. Query Knowledge Base for similar past incidents.
        2. Match and Rank context to improve AI accuracy.
        3. Consult AI Expert using original query + retrieved context.
        4. Format and Validate JSON output.
        5. Persist the new discovery for future matching.
        """
        if not user_query:
            return {"error": "No input provided"}

        # Step 1 & 2: Knowledge Retrieval & Matching
        history = IncidentRepository.fetch_all()
        matches = KnowledgeMatcher.find_matches(user_query, history)
        confidence = KnowledgeMatcher.calculate_confidence(len(matches))

        # Step 3: Intelligence Generation
        raw_analysis = IncidentExpert.analyze(user_query, matches)
        
        # Step 4: Formatting & Validation
        result = ResponseFormatter.to_json(raw_analysis)
        
        if not result:
            # Fallback for demo reliability
            result = Settings.FALLBACK_RESPONSE.copy()
            result["is_fallback"] = True
        
        # Inject metadata for the UI
        result['confidence'] = confidence
        result['similar_incidents'] = matches

        # Step 5: Learning (Persistence)
        # We store the latest analysis to make the system smarter over time.
        IncidentRepository.save(
            issue=user_query,
            root_cause=result.get('root_cause', 'Under Investigation'),
            resolution=result.get('resolution_steps', ['Awaiting diagnosis'])[0]
        )

        return result
