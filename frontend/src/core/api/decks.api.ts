import { apiClient } from "./client";
import {
  Deck,
  DeckCreateInput,
  DeckUpdateInput,
  DeckShareResponse,
  SharedDeckPreview,
} from "../types/deck";

export const DecksApi = {
  list: () => apiClient<Deck[]>("/decks"),

  getById: (id: string) => apiClient<Deck>(`/decks/${id}`),

  create: (input: DeckCreateInput) =>
    apiClient<Deck>("/decks", {
      method: "POST",
      body: JSON.stringify(input),
    }),

  update: (id: string, input: DeckUpdateInput) =>
    apiClient<Deck>(`/decks/${id}`, {
      method: "PATCH",
      body: JSON.stringify(input),
    }),

  delete: (id: string) =>
    apiClient<void>(`/decks/${id}`, {
      method: "DELETE",
    }),

  share: (id: string) =>
    apiClient<DeckShareResponse>(`/decks/${id}/share`, {
      method: "POST",
    }),

  explorePublic: (limit = 20, skip = 0) =>
    apiClient<Deck[]>("/decks/public/explore", {
      params: { limit, skip },
    }),

  previewShared: (shareCode: string) =>
    apiClient<SharedDeckPreview>(`/decks/shared/${shareCode}`),

  cloneShared: (shareCode: string) =>
    apiClient<Deck>(`/decks/shared/${shareCode}/clone`, {
      method: "POST",
    }),
};

