from typing import List, Optional
from datetime import datetime
from app.domain.entities.card import Flashcard
from app.domain.interfaces.repositories import ICardRepository, IDeckRepository
from app.application.dtos.card_dto import CardCreateDTO, CardUpdateDTO


class CardUseCases:
    def __init__(self, card_repo: ICardRepository, deck_repo: IDeckRepository):
        self.card_repo = card_repo
        self.deck_repo = deck_repo

    async def create_card(self, deck_id: str, dto: CardCreateDTO) -> Optional[Flashcard]:
        deck = await self.deck_repo.get_by_id(deck_id)
        if not deck:
            return None

        card = Flashcard(
            deck_id=deck_id,
            front_content=dto.front_content,
            back_content=dto.back_content,
            hints=dto.hints,
            ease_factor=2.5,
            interval_days=0,
            repetitions=0,
            next_review_date=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return await self.card_repo.create(card)

    async def list_cards_by_deck(self, deck_id: str) -> List[Flashcard]:
        return await self.card_repo.list_by_deck(deck_id)

    async def get_card(self, card_id: str) -> Optional[Flashcard]:
        return await self.card_repo.get_by_id(card_id)

    async def update_card(self, card_id: str, dto: CardUpdateDTO) -> Optional[Flashcard]:
        card = await self.card_repo.get_by_id(card_id)
        if not card:
            return None

        if dto.front_content is not None:
            card.front_content = dto.front_content
        if dto.back_content is not None:
            card.back_content = dto.back_content
        if dto.hints is not None:
            card.hints = dto.hints

        card.updated_at = datetime.utcnow()
        return await self.card_repo.update(card)

    async def delete_card(self, card_id: str) -> bool:
        return await self.card_repo.delete(card_id)
