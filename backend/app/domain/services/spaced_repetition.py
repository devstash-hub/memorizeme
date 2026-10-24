from datetime import datetime, timedelta
from typing import Tuple
from app.domain.entities.card import Flashcard
from app.domain.entities.review import ReviewRating


class SpacedRepetitionService:
    """
    MemorizeMe Spaced Repetition Engine (SM-2 based).
    Calculates the next interval (in days), repetitions, and ease factor (EF) for MemorizeMe flashcards.
    """

    @staticmethod
    def calculate_next_review(card: Flashcard, rating: ReviewRating) -> Tuple[int, int, float, datetime]:
        """
        Returns (new_repetitions, new_interval_days, new_ease_factor, next_review_date)
        """
        grade = int(rating)
        ease_factor = card.ease_factor
        repetitions = card.repetitions
        interval_days = card.interval_days

        if grade < int(ReviewRating.HARD):
            # If the user failed, reset repetitions and return interval to 1 day
            repetitions = 0
            interval_days = 1
        else:
            # If the user recalled successfully (Hard, Good, or Easy)
            if repetitions == 0:
                interval_days = 1
            elif repetitions == 1:
                interval_days = 6
            else:
                interval_days = int(round(interval_days * ease_factor))

            repetitions += 1

        # Ease Factor calculation
        # EF' = EF + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
        # Map our 0..4 rating to the classic 1..5 scale:
        scale_grade = grade + 1
        ease_factor = ease_factor + (0.1 - (5 - scale_grade) * (0.08 + (5 - scale_grade) * 0.02))
        ease_factor = max(1.3, ease_factor)  # Standard minimum floor for ease factor

        next_review_date = datetime.utcnow() + timedelta(days=interval_days)

        return repetitions, interval_days, ease_factor, next_review_date
