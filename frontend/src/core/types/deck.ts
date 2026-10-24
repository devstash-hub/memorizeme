export interface Deck {
  id: string;
  user_id: string;
  title: string;
  description: string;
  tags: string[];
  is_public: boolean;
  share_code?: string | null;
  created_at: string;
  updated_at: string;
}

export interface DeckCreateInput {
  title: string;
  description?: string;
  tags?: string[];
  is_public?: boolean;
}

export interface DeckUpdateInput {
  title?: string;
  description?: string;
  tags?: string[];
  is_public?: boolean;
}

export interface DeckShareResponse {
  deck_id: string;
  share_code: string;
  is_public: boolean;
  share_url_path: string;
}

export interface SharedDeckCardPreview {
  front_content: string;
  back_content: string;
  hints: string[];
}

export interface SharedDeckPreview {
  id: string;
  title: string;
  description: string;
  tags: string[];
  card_count: number;
  share_code: string;
  cards: SharedDeckCardPreview[];
}
