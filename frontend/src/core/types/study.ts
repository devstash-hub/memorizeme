export enum ReviewRating {
  BLACKOUT = 0,   // Complete blackout / forgot
  INCORRECT = 1,  // Incorrect, but recognized answer
  HARD = 2,       // Correct with severe difficulty
  GOOD = 3,       // Correct with moderate effort
  EASY = 4,       // Correct with immediate ease
}

export interface SubmitReviewInput {
  card_id: string;
  rating: ReviewRating;
}

export interface StudySummary {
  card_id: string;
  new_interval_days: number;
  new_repetitions: number;
  new_ease_factor: number;
  next_review_date: string;
}

