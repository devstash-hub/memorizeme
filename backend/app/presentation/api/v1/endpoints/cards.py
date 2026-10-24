from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dtos.card_dto import CardCreateDTO, CardUpdateDTO, CardResponseDTO
from app.application.use_cases.card_use_cases import CardUseCases
from app.presentation.api.v1.dependencies import get_card_use_cases

router = APIRouter(prefix="/decks/{deck_id}/cards", tags=["Flashcards"])


def _to_dto(card) -> CardResponseDTO:
    return CardResponseDTO(
        id=card.id or "",
        deck_id=card.deck_id,
        front_content=card.front_content,
        back_content=card.back_content,
        hints=card.hints,
        ease_factor=card.ease_factor,
        interval_days=card.interval_days,
        repetitions=card.repetitions,
        next_review_date=card.next_review_date,
        created_at=card.created_at,
        updated_at=card.updated_at,
    )


@router.post("", response_model=CardResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_card(
    deck_id: str,
    dto: CardCreateDTO,
    use_cases: CardUseCases = Depends(get_card_use_cases),
):
    card = await use_cases.create_card(deck_id=deck_id, dto=dto)
    if not card:
        raise HTTPException(status_code=404, detail="Deck not found.")
    return _to_dto(card)


@router.get("", response_model=List[CardResponseDTO])
async def list_cards(
    deck_id: str,
    use_cases: CardUseCases = Depends(get_card_use_cases),
):
    cards = await use_cases.list_cards_by_deck(deck_id)
    return [_to_dto(c) for c in cards]


@router.get("/{card_id}", response_model=CardResponseDTO)
async def get_card(
    deck_id: str,
    card_id: str,
    use_cases: CardUseCases = Depends(get_card_use_cases),
):
    card = await use_cases.get_card(card_id)
    if not card or card.deck_id != deck_id:
        raise HTTPException(status_code=404, detail="Flashcard not found.")
    return _to_dto(card)


@router.patch("/{card_id}", response_model=CardResponseDTO)
async def update_card(
    deck_id: str,
    card_id: str,
    dto: CardUpdateDTO,
    use_cases: CardUseCases = Depends(get_card_use_cases),
):
    card = await use_cases.get_card(card_id)
    if not card or card.deck_id != deck_id:
        raise HTTPException(status_code=404, detail="Flashcard not found.")
    
    updated = await use_cases.update_card(card_id, dto)
    return _to_dto(updated)


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(
    deck_id: str,
    card_id: str,
    use_cases: CardUseCases = Depends(get_card_use_cases),
):
    card = await use_cases.get_card(card_id)
    if not card or card.deck_id != deck_id:
        raise HTTPException(status_code=404, detail="Flashcard not found.")
    
    await use_cases.delete_card(card_id)
    return None
