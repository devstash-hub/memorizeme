/**
 * Utility for handling Japanese and East Asian Input Method Editors (IME).
 * Prevents premature keyboard events (like Enter for card flip or form submit)
 * while the user is actively selecting Kanji/Kana candidates.
 */
export function isImeComposing(event: KeyboardEvent): boolean {
  // Check standard native isComposing flag or keyCode 229 (IME in-progress)
  if (event.isComposing || (event as any).nativeEvent?.isComposing) {
    return true;
  }
  if (event.keyCode === 229) {
    return true;
  }
  return false;
}

