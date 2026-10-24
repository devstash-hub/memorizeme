from fastapi import Depends
from supabase import Client
from app.infrastructure.database.supabase_client import get_supabase_client
from app.infrastructure.database.repositories.supabase_deck_repo import SupabaseDeckRepository
from app.infrastructure.database.repositories.supabase_card_repo import SupabaseCardRepository
from app.infrastructure.database.repositories.supabase_review_repo import SupabaseReviewRepository
from app.application.use_cases.deck_use_cases import DeckUseCases
from app.application.use_cases.card_use_cases import CardUseCases
from app.application.use_cases.study_use_cases import StudyUseCases
from app.core.security import get_current_user_id


def get_deck_repo(client: Client = Depends(get_supabase_client)) -> SupabaseDeckRepository:
    return SupabaseDeckRepository(client)


def get_card_repo(client: Client = Depends(get_supabase_client)) -> SupabaseCardRepository:
    return SupabaseCardRepository(client)


def get_review_repo(client: Client = Depends(get_supabase_client)) -> SupabaseReviewRepository:
    return SupabaseReviewRepository(client)


def get_deck_use_cases(
    deck_repo: SupabaseDeckRepository = Depends(get_deck_repo),
    card_repo: SupabaseCardRepository = Depends(get_card_repo),
) -> DeckUseCases:
    return DeckUseCases(deck_repo=deck_repo, card_repo=card_repo)


def get_card_use_cases(
    card_repo: SupabaseCardRepository = Depends(get_card_repo),
    deck_repo: SupabaseDeckRepository = Depends(get_deck_repo),
) -> CardUseCases:
    return CardUseCases(card_repo=card_repo, deck_repo=deck_repo)


def get_study_use_cases(
    card_repo: SupabaseCardRepository = Depends(get_card_repo),
    review_repo: SupabaseReviewRepository = Depends(get_review_repo),
) -> StudyUseCases:
    return StudyUseCases(card_repo=card_repo, review_repo=review_repo)
