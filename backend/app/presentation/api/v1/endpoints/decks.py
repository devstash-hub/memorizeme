from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.application.dtos.deck_dto import (
    DeckCreateDTO,
    DeckUpdateDTO,
    DeckResponseDTO,
    DeckShareResponseDTO,
    SharedDeckPreviewDTO,
    SharedDeckCardPreviewDTO,
)
from app.application.use_cases.deck_use_cases import DeckUseCases
from app.presentation.api.v1.dependencies import get_deck_use_cases, get_current_user_id

router = APIRouter(prefix="/decks", tags=["Decks"])


def _to_response_dto(deck) -> DeckResponseDTO:
    return DeckResponseDTO(
        id=deck.id or "",
        user_id=deck.user_id,
        title=deck.title,
        description=deck.description,
        tags=deck.tags,
        is_public=deck.is_public,
        share_code=deck.share_code,
        created_at=deck.created_at,
        updated_at=deck.updated_at,
    )


@router.get("/public/explore", response_model=List[DeckResponseDTO])
async def explore_public_decks(
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    use_cases: DeckUseCases = Depends(get_deck_use_cases),
):
    """Explores community public decks."""
    decks = await use_cases.list_public_decks(limit=limit, skip=skip)
    return [_to_response_dto(d) for d in decks]


@router.get("/shared/{share_code}", response_model=SharedDeckPreviewDTO)
async def preview_shared_deck(
    share_code: str,
    use_cases: DeckUseCases = Depends(get_deck_use_cases),
):
    """Previews a shared deck and its flashcard list using a unique share code."""
    deck, cards = await use_cases.get_shared_deck(share_code)
    if not deck:
        raise HTTPException(status_code=404, detail="Shared deck not found or link has expired.")

    return SharedDeckPreviewDTO(
        id=deck.id or "",
        title=deck.title,
        description=deck.description,
        tags=deck.tags,
        card_count=len(cards),
        share_code=share_code,
        cards=[
            SharedDeckCardPreviewDTO(
                front_content=c.front_content,
                back_content=c.back_content,
                hints=c.hints,
            )
            for c in cards
        ],
    )


@router.post("/shared/{share_code}/clone", response_model=DeckResponseDTO, status_code=status.HTTP_201_CREATED)
async def clone_shared_deck(
    share_code: str,
    user_id: str = Depends(get_current_user_id),
    use_cases: DeckUseCases = Depends(get_deck_use_cases),
):
    """
    Clones a shared deck and its flashcards into the authenticated user's account.
    Spaced repetition intervals are reset so the user has an independent study schedule.
    """
    cloned_deck = await use_cases.clone_shared_deck(share_code=share_code, target_user_id=user_id)
    if not cloned_deck:
        raise HTTPException(status_code=404, detail="Shared deck not found.")
    return _to_response_dto(cloned_deck)


@router.post("", response_model=DeckResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_deck(
    dto: DeckCreateDTO,
    user_id: str = Depends(get_current_user_id),
    use_cases: DeckUseCases = Depends(get_deck_use_cases),
):
    deck = await use_cases.create_deck(user_id=user_id, dto=dto)
    return _to_response_dto(deck)


@router.get("", response_model=List[DeckResponseDTO])
async def list_decks(
    user_id: str = Depends(get_current_user_id),
    use_cases: DeckUseCases = Depends(get_deck_use_cases),
):
    decks = await use_cases.list_decks(user_id=user_id)
    return [_to_response_dto(d) for d in decks]


@router.get("/{deck_id}", response_model=DeckResponseDTO)
async def get_deck(
    deck_id: str,
    use_cases: DeckUseCases = Depends(get_deck_use_cases),
):
    deck = await use_cases.get_deck(deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found.")
    return _to_response_dto(deck)


@router.patch("/{deck_id}", response_model=DeckResponseDTO)
async def update_deck(
    deck_id: str,
    dto: DeckUpdateDTO,
    use_cases: DeckUseCases = Depends(get_deck_use_cases),
):
    deck = await use_cases.update_deck(deck_id, dto)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found.")
    return _to_response_dto(deck)


@router.delete("/{deck_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deck(
    deck_id: str,
    use_cases: DeckUseCases = Depends(get_deck_use_cases),
):
    deleted = await use_cases.delete_deck(deck_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Deck not found.")
    return None


@router.post("/{deck_id}/share", response_model=DeckShareResponseDTO)
async def enable_deck_sharing(
    deck_id: str,
    user_id: str = Depends(get_current_user_id),
    use_cases: DeckUseCases = Depends(get_deck_use_cases),
):
    """Enables sharing for a deck and produces a share link code."""
    deck = await use_cases.share_deck(deck_id=deck_id, user_id=user_id)
    if not deck or not deck.share_code:
        raise HTTPException(status_code=404, detail="Deck not found or you are not authorized to share it.")
    
    return DeckShareResponseDTO(
        deck_id=deck.id or "",
        share_code=deck.share_code,
        is_public=deck.is_public,
        share_url_path=f"/shared/{deck.share_code}",
    )
