from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Optional


class ReviewRating(IntEnum):
    """User rating provided during an active recall study session."""
    BLACKOUT = 0   # Complete blackout / forgot
    INCORRECT = 1  # Incorrect, but recognized answer upon reveal
    HARD = 2       # Correct with severe recall effort
    GOOD = 3       # Correct with moderate effort
    EASY = 4       # Correct with immediate ease


@dataclass
class ReviewLog:
    """Historical audit log of a single flashcard review."""
    id: Optional[str] = None
    card_id: str = ""
    deck_id: str = ""
    user_id: str = ""
    rating: ReviewRating = ReviewRating.GOOD
    previous_interval: int = 0
    new_interval: int = 0
    reviewed_at: datetime = field(default_factory=datetime.utcnow)
