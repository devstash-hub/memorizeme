from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.application.dtos.card_dto import CardResponseDTO
from app.application.dtos.study_dto import SubmitReviewDTO, StudySummaryDTO
from app.application.use_cases.study_use_cases import StudyUseCases
from app.presentation.api.v1.dependencies import get_study_use_cases, get_current_user_id

router = APIRouter(prefix="/study", tags=["Study Mode"])


@router.get("/decks/{deck_id}/queue", response_model=List[CardResponseDTO])
async def get_study_queue(
    deck_id: str,
    limit: int = Query(default=30, ge=1, le=100),
    use_cases: StudyUseCases = Depends(get_study_use_cases),
):
    """
    Returns deck flashcards that are due for active recall study (next_review_date <= now).
    """
    cards = await use_cases.get_study_queue(deck_id, limit=limit)
    return [
        CardResponseDTO(
            id=c.id or "",
            deck_id=c.deck_id,
            front_content=c.front_content,
            back_content=c.back_content,
            hints=c.hints,
            ease_factor=c.ease_factor,
            interval_days=c.interval_days,
            repetitions=c.repetitions,
            next_review_date=c.next_review_date,
            created_at=c.created_at,
            updated_at=c.updated_at,
        )
        for c in cards
    ]


@router.post("/review", response_model=StudySummaryDTO)
async def submit_review(
    dto: SubmitReviewDTO,
    user_id: str = Depends(get_current_user_id),
    use_cases: StudyUseCases = Depends(get_study_use_cases),
):
    """
    Records user review rating for a flashcard and recalculates the next interval using SM-2.
    """
    summary = await use_cases.submit_review(user_id=user_id, dto=dto)
    if not summary:
        raise HTTPException(status_code=404, detail="Flashcard not found.")
    return summary
