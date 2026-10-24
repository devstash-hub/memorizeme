import { apiClient } from "./client";
import { Flashcard } from "../types/card";
import { SubmitReviewInput, StudySummary } from "../types/study";

export const StudyApi = {
  getQueue: (deckId: string, limit = 30) =>
    apiClient<Flashcard[]>(`/study/decks/${deckId}/queue`, {
      params: { limit },
    }),

  submitReview: (input: SubmitReviewInput) =>
    apiClient<StudySummary>("/study/review", {
      method: "POST",
      body: JSON.stringify(input),
    }),
};

