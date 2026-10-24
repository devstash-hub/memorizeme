# Views / Pages Directory

This directory contains full screen views and page routing destinations:

- `auth/`: Login, Register, Password Reset (connected to Supabase Auth).
- `decks/`:
  - `DeckListPage`: User's primary deck dashboard.
  - `DeckDetailPage`: Deck stats, card manager, and "Start Study" CTA.
- `study/`:
  - `StudySessionPage`: Interactive card review screen with swipe/tap controls.
  - `SessionSummaryPage`: Post-study retention accuracy and time breakdown.
- `explore/`:
  - `ExplorePublicDecksPage`: Community shared deck search.
  - `SharedDeckPreviewPage`: Previewing `/shared/{share_code}` before cloning into user's account.

