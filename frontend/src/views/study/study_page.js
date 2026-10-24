/**
 * MemorizeMe Study Session Controller
 * Handles 3D Card Flip, SM-2 Rating Submission, CJK Furigana, Audio Pronunciation, and Gestures.
 */

// Sample demo cards with international CJK Japanese support & standard cards
const DEFAULT_CARDS = [
  {
    id: "demo-1",
    deck_id: "japanese-core",
    deck_title: "Japanese N5 Core Vocabulary 🇯🇵",
    tag: "Kanji • N5",
    front_content: "<ruby>日本語<rt>にほんご</rt></ruby>",
    back_content: "Japanese language",
    explanation: "Composed of 日本 (Nihon = Japan) + 語 (go = language / dialect).",
    hints: ["Used to refer to the spoken and written language of Japan."],
    lang: "ja-JP",
    ease_factor: 2.5,
    interval_days: 0,
    repetitions: 0
  },
  {
    id: "demo-2",
    deck_id: "japanese-core",
    deck_title: "Japanese N5 Core Vocabulary 🇯🇵",
    tag: "Verb • N5",
    front_content: "<ruby>勉強<rt>べんきょう</rt></ruby>する",
    back_content: "To study / To practice",
    explanation: "Group 3 irregular Suru verb. Literally means 'to diligently exert oneself'.",
    hints: ["An essential daily action for mastering new skills!"],
    lang: "ja-JP",
    ease_factor: 2.5,
    interval_days: 0,
    repetitions: 0
  },
  {
    id: "demo-3",
    deck_id: "japanese-core",
    deck_title: "Japanese N5 Core Vocabulary 🇯🇵",
    tag: "Noun",
    front_content: "<ruby>記憶<rt>きおく</rt></ruby>",
    back_content: "Memory / Recollection",
    explanation: "Core concept behind MemorizeMe (Active Recall & Spaced Repetition).",
    hints: ["A synonym for retaining knowledge or remembering."],
    lang: "ja-JP",
    ease_factor: 2.5,
    interval_days: 0,
    repetitions: 0
  },
  {
    id: "demo-4",
    deck_id: "programming-concepts",
    deck_title: "System Architecture & CS 🧠",
    tag: "Architecture",
    front_content: "Spaced Repetition (SM-2)",
    back_content: "Spaced Repetition Technique",
    explanation: "Algorithm that calculates the optimal review interval before the Ebbinghaus forgetting curve takes effect.",
    hints: ["Expanding intervals: 1d -> 6d -> multiplied by Ease Factor."],
    lang: "en-US",
    ease_factor: 2.5,
    interval_days: 1,
    repetitions: 1
  }
];

class StudyApp {
  constructor() {
    this.cards = [...DEFAULT_CARDS];
    this.currentIndex = 0;
    this.isFlipped = false;
    this.hintsRevealed = false;
    this.history = [];
    this.startTime = Date.now();

    this.initElements();
    this.initEvents();
    this.renderCard();
  }

  initElements() {
    this.cardWrapper = document.getElementById("cardWrapper");
    this.deckTitleEl = document.getElementById("deckTitle");
    this.counterEl = document.getElementById("cardCounter");
    this.progressBarEl = document.getElementById("progressBar");
    
    // Front elements
    this.frontTagEl = document.getElementById("frontTag");
    this.frontPromptEl = document.getElementById("frontPrompt");
    this.hintChipEl = document.getElementById("hintChip");
    this.hintTextEl = document.getElementById("hintText");
    this.audioBtnEl = document.getElementById("audioBtn");

    // Back elements
    this.backTagEl = document.getElementById("backTag");
    this.backAnswerEl = document.getElementById("backAnswer");
    this.backExplanationEl = document.getElementById("backExplanation");

    // Control areas
    this.frontControlsEl = document.getElementById("frontControls");
    this.backControlsEl = document.getElementById("backControls");
    this.btnRevealEl = document.getElementById("btnReveal");

    // Containers
    this.cardStageEl = document.getElementById("cardStage");
    this.completionContainerEl = document.getElementById("completionContainer");
  }

  initEvents() {
    // Click or tap to flip card
    this.cardWrapper.addEventListener("click", () => this.toggleFlip());
    this.btnRevealEl.addEventListener("click", (e) => {
      e.stopPropagation();
      this.flipToBack();
    });

    // Rating buttons
    document.querySelectorAll(".rating-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const rating = parseInt(btn.dataset.rating, 10);
        this.submitRating(rating);
      });
    });

    // Audio Speech Synthesis
    this.audioBtnEl.addEventListener("click", (e) => {
      e.stopPropagation();
      this.speakCurrentCard();
    });

    // Hint toggle
    this.hintChipEl.addEventListener("click", (e) => {
      e.stopPropagation();
      this.toggleHint();
    });

    // Keyboard Shortcuts (with IME composition safety)
    window.addEventListener("keydown", (e) => {
      // Prevent premature submit if user is selecting Japanese Kanji candidates
      if (e.isComposing || e.keyCode === 229) return;

      if (e.code === "Space" || e.key === "Enter") {
        e.preventDefault();
        this.toggleFlip();
      } else if (this.isFlipped) {
        if (e.key === "1") this.submitRating(0); // Forgot / Blackout
        if (e.key === "2") this.submitRating(2); // Hard
        if (e.key === "3") this.submitRating(3); // Good
        if (e.key === "4") this.submitRating(4); // Easy
      }
    });

    // Mobile Swipe Gestures
    this.initTouchGestures();
  }

  initTouchGestures() {
    let touchStartX = 0;
    let touchStartY = 0;

    this.cardWrapper.addEventListener("touchstart", (e) => {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    this.cardWrapper.addEventListener("touchend", (e) => {
      const touchEndX = e.changedTouches[0].screenX;
      const touchEndY = e.changedTouches[0].screenY;
      const diffX = touchEndX - touchStartX;
      const diffY = touchEndY - touchStartY;

      if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 60) {
        if (this.isFlipped) {
          if (diffX > 0) {
            // Swipe Right: Good
            this.submitRating(3);
          } else {
            // Swipe Left: Forgot / Blackout
            this.submitRating(0);
          }
        } else {
          this.flipToBack();
        }
      }
    }, { passive: true });
  }

  toggleFlip() {
    if (this.isFlipped) {
      this.flipToFront();
    } else {
      this.flipToBack();
    }
  }

  flipToBack() {
    this.isFlipped = true;
    this.cardWrapper.classList.add("is-flipped");
    this.frontControlsEl.style.display = "none";
    this.backControlsEl.style.display = "grid";
  }

  flipToFront() {
    this.isFlipped = false;
    this.cardWrapper.classList.remove("is-flipped");
    this.frontControlsEl.style.display = "flex";
    this.backControlsEl.style.display = "none";
  }

  toggleHint() {
    this.hintsRevealed = !this.hintsRevealed;
    const currentCard = this.cards[this.currentIndex];
    if (this.hintsRevealed && currentCard.hints && currentCard.hints.length > 0) {
      this.hintTextEl.textContent = currentCard.hints[0];
      this.hintTextEl.style.display = "block";
      this.hintChipEl.textContent = "Hide hint";
    } else {
      this.hintTextEl.style.display = "none";
      this.hintChipEl.textContent = "💡 Show hint";
    }
  }

  speakCurrentCard() {
    if (!window.speechSynthesis) return;
    const currentCard = this.cards[this.currentIndex];
    
    // Strip HTML/Ruby tags to pronounce clean text
    const tempEl = document.createElement("div");
    tempEl.innerHTML = currentCard.front_content;
    const textToSpeak = tempEl.textContent || tempEl.innerText || "";

    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.lang = currentCard.lang || "ja-JP";
    utterance.rate = 0.9;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  }

  renderCard() {
    if (this.currentIndex >= this.cards.length) {
      this.showCompletion();
      return;
    }

    const card = this.cards[this.currentIndex];
    this.flipToFront();

    // Reset hints
    this.hintsRevealed = false;
    this.hintTextEl.style.display = "none";
    this.hintChipEl.textContent = "💡 Show hint";
    this.hintChipEl.style.display = card.hints && card.hints.length ? "inline-block" : "none";

    // Header info
    this.deckTitleEl.textContent = card.deck_title || "Study Deck";
    this.counterEl.textContent = `Card ${this.currentIndex + 1} of ${this.cards.length}`;
    
    const progressPercent = (this.currentIndex / this.cards.length) * 100;
    this.progressBarEl.style.width = `${progressPercent}%`;

    // Front content
    this.frontTagEl.textContent = card.tag || "Vocabulary";
    this.frontPromptEl.innerHTML = card.front_content;

    // Back content
    this.backTagEl.textContent = "Answer";
    this.backAnswerEl.innerHTML = card.back_content;
    this.backExplanationEl.textContent = card.explanation || "";

    // Show/hide audio button for speech
    this.audioBtnEl.style.display = window.speechSynthesis ? "flex" : "none";
  }

  submitRating(rating) {
    const card = this.cards[this.currentIndex];
    this.history.push({
      card_id: card.id,
      rating: rating,
      timestamp: Date.now()
    });

    // Advance to next card
    this.currentIndex++;
    this.renderCard();
  }

  showCompletion() {
    this.progressBarEl.style.width = "100%";
    this.cardStageEl.style.display = "none";
    this.frontControlsEl.style.display = "none";
    this.backControlsEl.style.display = "none";
    this.completionContainerEl.style.display = "flex";

    const totalStudied = this.history.length;
    const correctCount = this.history.filter(h => h.rating >= 2).length;
    const accuracy = totalStudied > 0 ? Math.round((correctCount / totalStudied) * 100) : 100;
    const timeSpentSeconds = Math.round((Date.now() - this.startTime) / 1000);

    document.getElementById("statTotal").textContent = totalStudied;
    document.getElementById("statAccuracy").textContent = `${accuracy}%`;
    document.getElementById("statTime").textContent = `${timeSpentSeconds}s`;

    document.getElementById("btnRestart").addEventListener("click", () => {
      this.currentIndex = 0;
      this.history = [];
      this.startTime = Date.now();
      this.cardStageEl.style.display = "flex";
      this.completionContainerEl.style.display = "none";
      this.renderCard();
    });
  }
}

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  new StudyApp();
});
