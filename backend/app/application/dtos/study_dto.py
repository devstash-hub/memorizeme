from datetime import datetime
from pydantic import BaseModel, Field
from app.domain.entities.review import ReviewRating


class SubmitReviewDTO(BaseModel):
    card_id: str
    rating: ReviewRating = Field(..., description="Review rating (0: Blackout, 2: Hard, 3: Good, 4: Easy)")


class StudySummaryDTO(BaseModel):
    card_id: str
    new_interval_days: int
    new_repetitions: int
    new_ease_factor: float
    next_review_date: datetime
