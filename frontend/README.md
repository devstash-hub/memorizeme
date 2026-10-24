# MemorizeMe Frontend Architecture 📱💻

A modern, responsive, mobile-first, and framework-agnostic frontend structure ready to be implemented with **React**, **Angular**, **Vue**, **Svelte**, or modern **Vanilla TypeScript**.

---

## 🗂️ Directory Structure

```text
frontend/
├── public/                      # Static assets, PWA manifest, and app icons
│   ├── favicon.svg              # App icon
│   └── manifest.json            # PWA standalone mobile configuration
├── src/
│   ├── assets/
│   │   └── styles/
│   │       ├── safe-area.css    # Mobile notch, home-bar & touch padding variables
│   │       ├── main.css         # Global reset, CJK typography, and 3D flip card styles
│   │       └── study.css        # Study view layout, glowing borders, and SM-2 buttons
│   ├── core/                    # 100% Framework-Agnostic Core Logic (Pure TypeScript)
│   │   ├── api/                 # Typed API client connected to FastAPI backend
│   │   │   ├── client.ts        # Fetch client with auto Supabase JWT Bearer injection
│   │   │   ├── decks.api.ts     # Decks CRUD, sharing, public explore, and cloning
│   │   │   ├── cards.api.ts     # Flashcard CRUD endpoints
│   │   │   └── study.api.ts     # Study queue & review submission endpoints
│   │   ├── auth/                # Supabase Auth session & token manager
│   │   │   └── supabase.ts
│   │   ├── config/              # Environment configuration
│   │   │   └── env.ts
│   │   ├── types/               # TypeScript interfaces matching backend models
│   │   │   ├── deck.ts
│   │   │   ├── card.ts
│   │   │   └── study.ts
│   │   └── utils/
│   │       ├── gestures.ts      # Mobile touch swipe detector for study cards
│   │       └── ime.ts           # Japanese / CJK IME composition detection helper
│   ├── components/              # UI Component scaffolding (common, decks, cards, study)
│   └── views/
│       ├── auth/
│       │   └── auth_page.js     # Supabase Auth controller (login, register, social auth)
│       ├── study/
│       │   └── study_page.js    # Interactive Study Engine (3D flip, ratings, audio, gestures)
│       └── README.md
├── index.html                   # Interactive Study Page v1 (open directly in browser)
├── login.html                   # Authentication & Login Page (open directly in browser)
├── .env.example                 # Environment variables template
└── .gitignore                   # Node / web build ignore rules
```

---

## ⚡ Quick Test: Interactive Pages (No Build Step Required)

You can preview and test the complete frontend experience immediately:
1. **Study Page v1**: Open [`frontend/index.html`](./index.html) in your browser.
2. **Login / Register Page**: Open [`frontend/login.html`](./login.html) in your browser.
3. **Features active**:
   - **Auth Controller**: Mode toggle between *Entrar*, *Criar Conta*, and *Recuperar Senha*.
   - **Social Login**: Google & GitHub options wired to Supabase Auth.
   - **3D Card Flip**: Smooth 3D animation on click, Space, or Enter.
   - **Visual Identity**: Gradient indigo (`#6366f1` to `#4338ca`) and sky blue (`#38bdf8`) inspired directly by the logo.
   - **Japanese / CJK Support**: Live demonstration with Kanji & Furigana (`<ruby>日本語<rt>にほんご</rt></ruby>`).
   - **Audio Pronunciation**: Click the speaker icon to hear native pronunciation via Web Speech API.
   - **SM-2 Evaluation**: 4 rating buttons (`Errei`, `Difícil`, `Bom`, `Fácil`) with keyboard shortcuts (`1` to `4`).
   - **Mobile Gestures**: Swipe right for "Good", swipe left for "Blackout / Errei".
   - **Session Report**: Instant accuracy, cards reviewed, and time breakdown upon queue completion.

---

## 🚀 How to Initialize Your Framework of Choice

Because the entire `src/core/` layer (types, API services, Supabase auth, and gesture utilities) is written in pure TypeScript, you can plug in any framework without rewriting business logic:

### Option 1: React + Vite (Fast & Lightweight)
```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install @supabase/supabase-js
```

### Option 2: Angular (Enterprise-Grade & Opinionated)
```bash
# Inside the root repository
npx @angular/cli new frontend --routing --style=css
```

### Option 3: Vue 3 + Vite
```bash
cd frontend
npm create vite@latest . -- --template vue-ts
npm install @supabase/supabase-js
```

---

## 💡 Key Design Highlights

1. **Pre-wired API Client (`src/core/api/`)**:
   Calling endpoints in your UI components is as simple as:
   ```typescript
   import { DecksApi } from '../core/api/decks.api';
   import { StudyApi } from '../core/api/study.api';

   // Fetch decks
   const decks = await DecksApi.list();

   // Submit study rating (SM-2)
   const summary = await StudyApi.submitReview({ card_id: '...', rating: 3 });
   ```

2. **Japanese & CJK IME Protection (`src/core/utils/ime.ts`)**:
   Prevents premature card flip or submission while typing Kanji/Kana:
   ```typescript
   import { isImeComposing } from '../core/utils/ime';

   const onKeyDown = (e: KeyboardEvent) => {
     if (e.key === 'Enter' && !isImeComposing(e)) {
       revealAnswer();
     }
   };
   ```

3. **Touch Swipe for Mobile Cards (`src/core/utils/gestures.ts`)**:
   ```typescript
   import { attachSwipeListener } from '../core/utils/gestures';

   const cleanup = attachSwipeListener(cardElement, {
     onSwipeRight: () => rateCard(ReviewRating.GOOD),
     onSwipeLeft: () => rateCard(ReviewRating.BLACKOUT),
   });
   ```

4. **Mobile App Packaging Ready**:
   When you are ready to produce iOS and Android native apps:
   ```bash
   npm install @capacitor/core @capacitor/cli
   npx cap init MemorizeMe app.memorizeme
   npx cap add ios
   npx cap add android
   ```

