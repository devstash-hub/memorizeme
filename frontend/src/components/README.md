# Components Directory

This directory houses modular UI components ready to be implemented with your framework of choice (React, Angular, Vue, Svelte, or Web Components).

## Recommended Structure:
- `common/`: Reusable primitives (Buttons, Modal dialogs, Bottom navigation bar, Header).
- `decks/`: Deck card item, Deck creation form, Share modal.
- `cards/`: Flashcard editor (with Furigana `<ruby>` and Markdown preview), Card list item.
- `study/`:
  - `StudyCard`: 3D flip card utilizing `.flashcard-perspective` and `.flashcard-inner`.
  - `RatingControls`: Touch-friendly buttons (`0: Blackout`, `2: Hard`, `3: Good`, `4: Easy`).
  - `StudyProgress`: Progress bar for current review session.

