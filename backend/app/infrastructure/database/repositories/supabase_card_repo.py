from typing import List, Optional
from datetime import datetime
from supabase import Client
from app.domain.entities.card import Flashcard
from app.domain.interfaces.repositories import ICardRepository


class SupabaseCardRepository(ICardRepository):
    def __init__(self, client: Client):
        self.client = client
        self.table = "cards"

    def _to_entity(self, row: dict) -> Flashcard:
        next_review = row.get("next_review_date")
        created_at = row.get("created_at")
        updated_at = row.get("updated_at")

        return Flashcard(
            id=str(row["id"]),
            deck_id=str(row.get("deck_id", "")),
            front_content=row.get("front_content", ""),
            back_content=row.get("back_content", ""),
            hints=row.get("hints") or [],
            ease_factor=float(row.get("ease_factor", 2.5)),
            interval_days=int(row.get("interval_days", 0)),
            repetitions=int(row.get("repetitions", 0)),
            next_review_date=datetime.fromisoformat(next_review) if isinstance(next_review, str) else (next_review or datetime.utcnow()),
            created_at=datetime.fromisoformat(created_at) if isinstance(created_at, str) else (created_at or datetime.utcnow()),
            updated_at=datetime.fromisoformat(updated_at) if isinstance(updated_at, str) else (updated_at or datetime.utcnow()),
        )

    async def create(self, card: Flashcard) -> Flashcard:
        payload = {
            "deck_id": card.deck_id,
            "front_content": card.front_content,
            "back_content": card.back_content,
            "hints": card.hints,
            "ease_factor": card.ease_factor,
            "interval_days": card.interval_days,
            "repetitions": card.repetitions,
            "next_review_date": card.next_review_date.isoformat(),
            "created_at": card.created_at.isoformat(),
            "updated_at": card.updated_at.isoformat(),
        }
        res = self.client.table(self.table).insert(payload).execute()
        if res.data and len(res.data) > 0:
            card.id = str(res.data[0]["id"])
        return card

    async def create_many(self, cards: List[Flashcard]) -> List[Flashcard]:
        if not cards:
            return []
        
        payloads = [
            {
                "deck_id": card.deck_id,
                "front_content": card.front_content,
                "back_content": card.back_content,
                "hints": card.hints,
                "ease_factor": card.ease_factor,
                "interval_days": card.interval_days,
                "repetitions": card.repetitions,
                "next_review_date": card.next_review_date.isoformat(),
                "created_at": card.created_at.isoformat(),
                "updated_at": card.updated_at.isoformat(),
            }
            for card in cards
        ]
        res = self.client.table(self.table).insert(payloads).execute()
        if res.data:
            for card, row in zip(cards, res.data):
                card.id = str(row["id"])
        return cards

    async def get_by_id(self, card_id: str) -> Optional[Flashcard]:
        res = self.client.table(self.table).select("*").eq("id", card_id).execute()
        if res.data and len(res.data) > 0:
            return self._to_entity(res.data[0])
        return None

    async def list_by_deck(self, deck_id: str) -> List[Flashcard]:
        res = (
            self.client.table(self.table)
            .select("*")
            .eq("deck_id", deck_id)
            .order("created_at", desc=True)
            .execute()
        )
        return [self._to_entity(row) for row in res.data]

    async def get_due_cards_for_study(self, deck_id: str, current_time: datetime, limit: int = 50) -> List[Flashcard]:
        """Queries flashcards due on or before current_time."""
        res = (
            self.client.table(self.table)
            .select("*")
            .eq("deck_id", deck_id)
            .lte("next_review_date", current_time.isoformat())
            .order("next_review_date", desc=False)
            .limit(limit)
            .execute()
        )
        return [self._to_entity(row) for row in res.data]

    async def update(self, card: Flashcard) -> Flashcard:
        if not card.id:
            raise ValueError("Invalid flashcard ID for update.")

        payload = {
            "front_content": card.front_content,
            "back_content": card.back_content,
            "hints": card.hints,
            "ease_factor": card.ease_factor,
            "interval_days": card.interval_days,
            "repetitions": card.repetitions,
            "next_review_date": card.next_review_date.isoformat(),
            "updated_at": card.updated_at.isoformat(),
        }
        self.client.table(self.table).update(payload).eq("id", card.id).execute()
        return card

    async def delete(self, card_id: str) -> bool:
        res = self.client.table(self.table).delete().eq("id", card_id).execute()
        return bool(res.data)
