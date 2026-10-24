from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Deck:
    """Pure domain entity representing a Flashcard Deck."""
    id: Optional[str] = None
    user_id: str = ""
    title: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    is_public: bool = False
    share_code: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
