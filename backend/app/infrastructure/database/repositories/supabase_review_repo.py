from typing import List
from datetime import datetime
from supabase import Client
from app.domain.entities.review import ReviewLog, ReviewRating
from app.domain.interfaces.repositories import IReviewRepository


class SupabaseReviewRepository(IReviewRepository):
    def __init__(self, client: Client):
        self.client = client
        self.table = "review_logs"

    def _to_entity(self, row: dict) -> ReviewLog:
        reviewed_at = row.get("reviewed_at")
        return ReviewLog(
            id=str(row["id"]),
            card_id=str(row.get("card_id", "")),
            deck_id=str(row.get("deck_id", "")),
            user_id=str(row.get("user_id", "")),
            rating=ReviewRating(row.get("rating", 3)),
            previous_interval=int(row.get("previous_interval", 0)),
            new_interval=int(row.get("new_interval", 0)),
            reviewed_at=datetime.fromisoformat(reviewed_at) if isinstance(reviewed_at, str) else (reviewed_at or datetime.utcnow()),
        )

    async def save_log(self, log: ReviewLog) -> ReviewLog:
        payload = {
            "card_id": log.card_id,
            "deck_id": log.deck_id,
            "user_id": log.user_id,
            "rating": int(log.rating),
            "previous_interval": log.previous_interval,
            "new_interval": log.new_interval,
            "reviewed_at": log.reviewed_at.isoformat(),
        }
        res = self.client.table(self.table).insert(payload).execute()
        if res.data and len(res.data) > 0:
            log.id = str(res.data[0]["id"])
        return log

    async def list_by_deck(self, deck_id: str, limit: int = 100) -> List[ReviewLog]:
        res = (
            self.client.table(self.table)
            .select("*")
            .eq("deck_id", deck_id)
            .order("reviewed_at", desc=True)
            .limit(limit)
            .execute()
        )
        return [self._to_entity(row) for row in res.data]
