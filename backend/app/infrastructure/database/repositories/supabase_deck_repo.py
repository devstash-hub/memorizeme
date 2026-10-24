from typing import List, Optional
from datetime import datetime
from supabase import Client
from app.domain.entities.deck import Deck
from app.domain.interfaces.repositories import IDeckRepository


class SupabaseDeckRepository(IDeckRepository):
    def __init__(self, client: Client):
        self.client = client
        self.table = "decks"

    def _to_entity(self, row: dict) -> Deck:
        created_at = row.get("created_at")
        updated_at = row.get("updated_at")
        
        return Deck(
            id=str(row["id"]),
            user_id=str(row.get("user_id", "")),
            title=row.get("title", ""),
            description=row.get("description", ""),
            tags=row.get("tags") or [],
            is_public=bool(row.get("is_public", False)),
            share_code=row.get("share_code"),
            created_at=datetime.fromisoformat(created_at) if isinstance(created_at, str) else (created_at or datetime.utcnow()),
            updated_at=datetime.fromisoformat(updated_at) if isinstance(updated_at, str) else (updated_at or datetime.utcnow()),
        )

    async def create(self, deck: Deck) -> Deck:
        payload = {
            "user_id": deck.user_id,
            "title": deck.title,
            "description": deck.description,
            "tags": deck.tags,
            "is_public": deck.is_public,
            "share_code": deck.share_code,
            "created_at": deck.created_at.isoformat(),
            "updated_at": deck.updated_at.isoformat(),
        }
        res = self.client.table(self.table).insert(payload).execute()
        if res.data and len(res.data) > 0:
            deck.id = str(res.data[0]["id"])
        return deck

    async def get_by_id(self, deck_id: str) -> Optional[Deck]:
        res = self.client.table(self.table).select("*").eq("id", deck_id).execute()
        if res.data and len(res.data) > 0:
            return self._to_entity(res.data[0])
        return None

    async def get_by_share_code(self, share_code: str) -> Optional[Deck]:
        res = self.client.table(self.table).select("*").eq("share_code", share_code).execute()
        if res.data and len(res.data) > 0:
            return self._to_entity(res.data[0])
        return None

    async def list_by_user(self, user_id: str) -> List[Deck]:
        res = (
            self.client.table(self.table)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return [self._to_entity(row) for row in res.data]

    async def list_public(self, limit: int = 50, skip: int = 0) -> List[Deck]:
        res = (
            self.client.table(self.table)
            .select("*")
            .eq("is_public", True)
            .order("created_at", desc=True)
            .range(skip, max(0, skip + limit - 1))
            .execute()
        )
        return [self._to_entity(row) for row in res.data]

    async def update(self, deck: Deck) -> Deck:
        if not deck.id:
            raise ValueError("Invalid deck ID for update.")
        
        payload = {
            "title": deck.title,
            "description": deck.description,
            "tags": deck.tags,
            "is_public": deck.is_public,
            "share_code": deck.share_code,
            "updated_at": deck.updated_at.isoformat(),
        }
        self.client.table(self.table).update(payload).eq("id", deck.id).execute()
        return deck

    async def delete(self, deck_id: str) -> bool:
        res = self.client.table(self.table).delete().eq("id", deck_id).execute()
        return bool(res.data)
