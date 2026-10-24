from fastapi import APIRouter
from app.presentation.api.v1.endpoints import decks, cards, study

api_router = APIRouter()

api_router.include_router(decks.router)
api_router.include_router(cards.router)
api_router.include_router(study.router)
