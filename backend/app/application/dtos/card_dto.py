from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CardCreateDTO(BaseModel):
    front_content: str = Field(..., min_length=1, description="Prompt, question, or markdown for the front of the card")
    back_content: str = Field(..., min_length=1, description="Answer, explanation, or notes for the back of the card")
    hints: List[str] = Field(default_factory=list, description="Optional progressive hints")


class CardUpdateDTO(BaseModel):
    front_content: Optional[str] = None
    back_content: Optional[str] = None
    hints: Optional[List[str]] = None


class CardResponseDTO(BaseModel):
    id: str
    deck_id: str
    front_content: str
    back_content: str
    hints: List[str]
    ease_factor: float
    interval_days: int
    repetitions: int
    next_review_date: datetime
    created_at: datetime
    updated_at: datetime
