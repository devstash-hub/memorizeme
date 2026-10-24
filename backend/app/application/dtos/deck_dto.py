from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DeckCreateDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=120, description="Deck title (full Unicode / CJK supported)")
    description: Optional[str] = Field(default="", max_length=500, description="Deck description")
    tags: List[str] = Field(default_factory=list, description="Categorization tags")
    is_public: bool = Field(default=False, description="Whether the deck is discoverable publicly")


class DeckUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None


class DeckResponseDTO(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    tags: List[str]
    is_public: bool
    share_code: Optional[str]
    created_at: datetime
    updated_at: datetime


class DeckShareResponseDTO(BaseModel):
    deck_id: str
    share_code: str
    is_public: bool
    share_url_path: str


class SharedDeckCardPreviewDTO(BaseModel):
    front_content: str
    back_content: str
    hints: List[str]


class SharedDeckPreviewDTO(BaseModel):
    id: str
    title: str
    description: str
    tags: List[str]
    card_count: int
    share_code: str
    cards: List[SharedDeckCardPreviewDTO]
