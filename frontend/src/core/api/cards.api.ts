import { apiClient } from "./client";
import { Flashcard, CardCreateInput, CardUpdateInput } from "../types/card";

export const CardsApi = {
  listByDeck: (deckId: string) => apiClient<Flashcard[]>(`/decks/${deckId}/cards`),

  getById: (deckId: string, cardId: string) =>
    apiClient<Flashcard>(`/decks/${deckId}/cards/${cardId}`),

  create: (deckId: string, input: CardCreateInput) =>
    apiClient<Flashcard>(`/decks/${deckId}/cards`, {
      method: "POST",
      body: JSON.stringify(input),
    }),

  update: (deckId: string, cardId: string, input: CardUpdateInput) =>
    apiClient<Flashcard>(`/decks/${deckId}/cards/${cardId}`, {
      method: "PATCH",
      body: JSON.stringify(input),
    }),

  delete: (deckId: string, cardId: string) =>
    apiClient<void>(`/decks/${deckId}/cards/${cardId}`, {
      method: "DELETE",
    }),
};

