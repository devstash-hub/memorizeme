from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Flashcard:
    """Pure domain entity representing a Flashcard."""
    id: Optional[str] = None
    deck_id: str = ""
    front_content: str = ""
    back_content: str = ""
    hints: List[str] = field(default_factory=list)
    
    # Spaced Repetition (SM-2) algorithm metadata
    ease_factor: float = 2.5
    interval_days: int = 0
    repetitions: int = 0
    next_review_date: datetime = field(default_factory=datetime.utcnow)
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
