export interface Flashcard {
  id: string;
  deck_id: string;
  front_content: string;
  back_content: string;
  hints: string[];
  ease_factor: number;
  interval_days: number;
  repetitions: number;
  next_review_date: string;
  created_at: string;
  updated_at: string;
}

export interface CardCreateInput {
  front_content: string;
  back_content: string;
  hints?: string[];
}

export interface CardUpdateInput {
  front_content?: string;
  back_content?: string;
  hints?: string[];
}

