from typing import Optional
from supabase import create_client, Client
from app.core.config import settings


class SupabaseManager:
    client: Optional[Client] = None


supabase_manager = SupabaseManager()


def get_supabase_client() -> Client:
    """Returns the initialized Supabase client instance."""
    if supabase_manager.client is None:
        supabase_manager.client = create_client(
            supabase_url=settings.SUPABASE_URL,
            supabase_key=settings.SUPABASE_KEY,
        )
    return supabase_manager.client
