import secrets
from typing import List, Optional, Tuple
from datetime import datetime
from app.domain.entities.deck import Deck
from app.domain.entities.card import Flashcard
from app.domain.interfaces.repositories import IDeckRepository, ICardRepository
from app.application.dtos.deck_dto import DeckCreateDTO, DeckUpdateDTO


class DeckUseCases:
    def __init__(self, deck_repo: IDeckRepository, card_repo: Optional[ICardRepository] = None):
        self.deck_repo = deck_repo
        self.card_repo = card_repo

    async def create_deck(self, user_id: str, dto: DeckCreateDTO) -> Deck:
        deck = Deck(
            user_id=user_id,
            title=dto.title,
            description=dto.description or "",
            tags=dto.tags,
            is_public=dto.is_public,
            share_code=secrets.token_urlsafe(8) if dto.is_public else None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return await self.deck_repo.create(deck)

    async def get_deck(self, deck_id: str) -> Optional[Deck]:
        return await self.deck_repo.get_by_id(deck_id)

    async def list_decks(self, user_id: str) -> List[Deck]:
        return await self.deck_repo.list_by_user(user_id)

    async def list_public_decks(self, limit: int = 50, skip: int = 0) -> List[Deck]:
        """Lists publicly discoverable decks created by the community."""
        return await self.deck_repo.list_public(limit=limit, skip=skip)

    async def update_deck(self, deck_id: str, dto: DeckUpdateDTO) -> Optional[Deck]:
        deck = await self.deck_repo.get_by_id(deck_id)
        if not deck:
            return None
        
        if dto.title is not None:
            deck.title = dto.title
        if dto.description is not None:
            deck.description = dto.description
        if dto.tags is not None:
            deck.tags = dto.tags
        if dto.is_public is not None:
            deck.is_public = dto.is_public
            if deck.is_public and not deck.share_code:
                deck.share_code = secrets.token_urlsafe(8)
        
        deck.updated_at = datetime.utcnow()
        return await self.deck_repo.update(deck)

    async def delete_deck(self, deck_id: str) -> bool:
        return await self.deck_repo.delete(deck_id)

    async def share_deck(self, deck_id: str, user_id: str) -> Optional[Deck]:
        """Generates or activates a unique share link code for the deck."""
        deck = await self.deck_repo.get_by_id(deck_id)
        if not deck or deck.user_id != user_id:
            return None
        
        if not deck.share_code:
            deck.share_code = secrets.token_urlsafe(8)
        
        deck.is_public = True
        deck.updated_at = datetime.utcnow()
        return await self.deck_repo.update(deck)

    async def get_shared_deck(self, share_code: str) -> Tuple[Optional[Deck], List[Flashcard]]:
        """Retrieves a shared deck and its flashcard previews using its unique share code."""
        deck = await self.deck_repo.get_by_share_code(share_code)
        if not deck:
            return None, []
        
        cards: List[Flashcard] = []
        if self.card_repo and deck.id:
            cards = await self.card_repo.list_by_deck(deck.id)
            
        return deck, cards

    async def clone_shared_deck(self, share_code: str, target_user_id: str) -> Optional[Deck]:
        """
        Clones an entire shared deck into target user's account.
        All cards are replicated with reset SM-2 repetitions so the user begins their own study loop.
        """
        deck, source_cards = await self.get_shared_deck(share_code)
        if not deck:
            return None

        # Create cloned deck entity for the new user
        cloned_deck = Deck(
            user_id=target_user_id,
            title=f"{deck.title} (Copy)",
            description=deck.description,
            tags=list(deck.tags),
            is_public=False,
            share_code=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        saved_deck = await self.deck_repo.create(cloned_deck)

        # Clone and reset flashcards
        if self.card_repo and saved_deck.id and source_cards:
            new_cards = [
                Flashcard(
                    deck_id=saved_deck.id,
                    front_content=card.front_content,
                    back_content=card.back_content,
                    hints=list(card.hints),
                    ease_factor=2.5,
                    interval_days=0,
                    repetitions=0,
                    next_review_date=datetime.utcnow(),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                for card in source_cards
            ]
            await self.card_repo.create_many(new_cards)

        return saved_deck
