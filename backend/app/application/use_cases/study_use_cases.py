from datetime import datetime
from typing import List, Optional
from app.domain.entities.card import Flashcard
from app.domain.entities.review import ReviewLog
from app.domain.interfaces.repositories import ICardRepository, IReviewRepository
from app.domain.services.spaced_repetition import SpacedRepetitionService
from app.application.dtos.study_dto import SubmitReviewDTO, StudySummaryDTO


class StudyUseCases:
    def __init__(self, card_repo: ICardRepository, review_repo: IReviewRepository):
        self.card_repo = card_repo
        self.review_repo = review_repo
        self.sr_service = SpacedRepetitionService()

    async def get_study_queue(self, deck_id: str, limit: int = 50) -> List[Flashcard]:
        """Returns flashcards from the given deck that are due for review (next_review_date <= now)."""
        now = datetime.utcnow()
        return await self.card_repo.get_due_cards_for_study(deck_id, current_time=now, limit=limit)

    async def submit_review(self, user_id: str, dto: SubmitReviewDTO) -> Optional[StudySummaryDTO]:
        """Processes the user rating for a card and calculates the next spaced review schedule."""
        card = await self.card_repo.get_by_id(dto.card_id)
        if not card:
            return None

        prev_interval = card.interval_days
        new_reps, new_interval, new_ef, next_date = self.sr_service.calculate_next_review(card, dto.rating)

        # Update card entity
        card.repetitions = new_reps
        card.interval_days = new_interval
        card.ease_factor = new_ef
        card.next_review_date = next_date
        card.updated_at = datetime.utcnow()

        await self.card_repo.update(card)

        # Record historical review log
        log = ReviewLog(
            card_id=card.id or "",
            deck_id=card.deck_id,
            user_id=user_id,
            rating=dto.rating,
            previous_interval=prev_interval,
            new_interval=new_interval,
            reviewed_at=datetime.utcnow()
        )
        await self.review_repo.save_log(log)

        return StudySummaryDTO(
            card_id=card.id or "",
            new_interval_days=new_interval,
            new_repetitions=new_reps,
            new_ease_factor=new_ef,
            next_review_date=next_date
        )
