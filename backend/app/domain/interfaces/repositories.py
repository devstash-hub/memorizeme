from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from app.domain.entities.deck import Deck
from app.domain.entities.card import Flashcard
from app.domain.entities.review import ReviewLog


class IDeckRepository(ABC):
    @abstractmethod
    async def create(self, deck: Deck) -> Deck:
        pass

    @abstractmethod
    async def get_by_id(self, deck_id: str) -> Optional[Deck]:
        pass

    @abstractmethod
    async def get_by_share_code(self, share_code: str) -> Optional[Deck]:
        pass

    @abstractmethod
    async def list_by_user(self, user_id: str) -> List[Deck]:
        pass

    @abstractmethod
    async def list_public(self, limit: int = 50, skip: int = 0) -> List[Deck]:
        pass

    @abstractmethod
    async def update(self, deck: Deck) -> Deck:
        pass

    @abstractmethod
    async def delete(self, deck_id: str) -> bool:
        pass


class ICardRepository(ABC):
    @abstractmethod
    async def create(self, card: Flashcard) -> Flashcard:
        pass

    @abstractmethod
    async def create_many(self, cards: List[Flashcard]) -> List[Flashcard]:
        pass

    @abstractmethod
    async def get_by_id(self, card_id: str) -> Optional[Flashcard]:
        pass

    @abstractmethod
    async def list_by_deck(self, deck_id: str) -> List[Flashcard]:
        pass

    @abstractmethod
    async def get_due_cards_for_study(self, deck_id: str, current_time: datetime, limit: int = 50) -> List[Flashcard]:
        pass

    @abstractmethod
    async def update(self, card: Flashcard) -> Flashcard:
        pass

    @abstractmethod
    async def delete(self, card_id: str) -> bool:
        pass


class IReviewRepository(ABC):
    @abstractmethod
    async def save_log(self, log: ReviewLog) -> ReviewLog:
        pass

    @abstractmethod
    async def list_by_deck(self, deck_id: str, limit: int = 100) -> List[ReviewLog]:
        pass
