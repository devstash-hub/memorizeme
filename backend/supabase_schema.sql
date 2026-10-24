-- ==============================================================================
-- MemorizeMe: Supabase PostgreSQL Schema & Row Level Security (RLS)
-- Supports full Unicode (UTF-8) including Japanese, CJK, and complex scripts.
-- ==============================================================================

-- 1. Create Decks Table
CREATE TABLE IF NOT EXISTS public.decks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    tags TEXT[] DEFAULT '{}',
    is_public BOOLEAN DEFAULT FALSE,
    share_code TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Create Flashcards Table
CREATE TABLE IF NOT EXISTS public.cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deck_id UUID REFERENCES public.decks(id) ON DELETE CASCADE NOT NULL,
    front_content TEXT NOT NULL,
    back_content TEXT NOT NULL,
    hints TEXT[] DEFAULT '{}',
    ease_factor FLOAT DEFAULT 2.5 NOT NULL,
    interval_days INTEGER DEFAULT 0 NOT NULL,
    repetitions INTEGER DEFAULT 0 NOT NULL,
    next_review_date TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Create Review Logs Table
CREATE TABLE IF NOT EXISTS public.review_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    card_id UUID REFERENCES public.cards(id) ON DELETE CASCADE NOT NULL,
    deck_id UUID REFERENCES public.decks(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    rating INTEGER NOT NULL,
    previous_interval INTEGER DEFAULT 0 NOT NULL,
    new_interval INTEGER DEFAULT 0 NOT NULL,
    reviewed_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ==============================================================================
-- Performance Indexes
-- ==============================================================================
CREATE INDEX IF NOT EXISTS idx_decks_user_id ON public.decks(user_id);
CREATE INDEX IF NOT EXISTS idx_decks_share_code ON public.decks(share_code);
CREATE INDEX IF NOT EXISTS idx_decks_is_public ON public.decks(is_public) WHERE is_public = TRUE;
CREATE INDEX IF NOT EXISTS idx_cards_deck_id ON public.cards(deck_id);
CREATE INDEX IF NOT EXISTS idx_cards_study_due ON public.cards(deck_id, next_review_date);
CREATE INDEX IF NOT EXISTS idx_review_logs_user_id ON public.review_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_review_logs_deck_id ON public.review_logs(deck_id);

-- ==============================================================================
-- Row Level Security (RLS) Policies
-- ==============================================================================
ALTER TABLE public.decks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.review_logs ENABLE ROW LEVEL SECURITY;

-- DECKS POLICIES:
-- Users can view their own decks OR any public/shared deck
CREATE POLICY "Users can select own decks or public decks"
ON public.decks FOR SELECT
USING (auth.uid() = user_id OR is_public = TRUE OR share_code IS NOT NULL);

-- Users can insert decks for themselves
CREATE POLICY "Users can create their own decks"
ON public.decks FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update only their own decks
CREATE POLICY "Users can update their own decks"
ON public.decks FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Users can delete only their own decks
CREATE POLICY "Users can delete their own decks"
ON public.decks FOR DELETE
USING (auth.uid() = user_id);

-- CARDS POLICIES:
-- Cards can be viewed if user owns the deck OR deck is public/shared
CREATE POLICY "Users can view cards of accessible decks"
ON public.cards FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM public.decks d
        WHERE d.id = cards.deck_id
          AND (d.user_id = auth.uid() OR d.is_public = TRUE OR d.share_code IS NOT NULL)
    )
);

-- Users can insert cards only into decks they own
CREATE POLICY "Users can create cards in own decks"
ON public.cards FOR INSERT
WITH CHECK (
    EXISTS (
        SELECT 1 FROM public.decks d
        WHERE d.id = cards.deck_id AND d.user_id = auth.uid()
    )
);

-- Users can update cards in own decks
CREATE POLICY "Users can update cards in own decks"
ON public.cards FOR UPDATE
USING (
    EXISTS (
        SELECT 1 FROM public.decks d
        WHERE d.id = cards.deck_id AND d.user_id = auth.uid()
    )
);

-- Users can delete cards from own decks
CREATE POLICY "Users can delete cards from own decks"
ON public.cards FOR DELETE
USING (
    EXISTS (
        SELECT 1 FROM public.decks d
        WHERE d.id = cards.deck_id AND d.user_id = auth.uid()
    )
);

-- REVIEW LOGS POLICIES:
CREATE POLICY "Users can view own review logs"
ON public.review_logs FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own review logs"
ON public.review_logs FOR INSERT
WITH CHECK (auth.uid() = user_id);
