import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class IncidentRepository:
    """
    Handles all persistent data operations for Incidents.
    Using Supabase as the production knowledge base.
    """
    
    _client = None

    @classmethod
    def connect(cls) -> Client:
        """Singleton connection to the database."""
        if cls._client is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            if url and key:
                cls._client = create_client(url, key)
        return cls._client

    @classmethod
    def fetch_all(cls):
        """Retrieve all historical incidents for similarity matching."""
        client = cls.connect()
        if not client:
            return []
        
        try:
            response = client.table('incidents').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Repository Read Error: {str(e)}")
            return []

    @classmethod
    def save(cls, issue, root_cause, resolution):
        """Persist a new incident to the knowledge base."""
        client = cls.connect()
        if not client:
            return None
        
        try:
            data = {
                "issue": issue,
                "root_cause": root_cause,
                "resolution": resolution
            }
            response = client.table('incidents').insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Repository Write Error: {str(e)}")
            return None
