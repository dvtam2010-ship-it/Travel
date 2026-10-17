# Vietnamese Currency Depiction QA

Read this reference whenever a scene visibly depicts Vietnamese money
(banknotes or coins). Video models cannot render banknotes accurately —
wrong denominations, garbled text, and distorted portraits are the norm,
not the exception. For Vietnam this is also a cultural-sensitivity issue:
every banknote bears the portrait of Hồ Chí Minh.

## Facts (verify before depicting a specific note)

- Currency: **đồng (₫)**. Polymer banknotes in common circulation:
  **10,000₫, 20,000₫, 50,000₫, 100,000₫, 200,000₫, 500,000₫**.
  Older paper 1,000₫ / 2,000₫ / 5,000₫ notes still circulate. Coins
  (200₫–5,000₫) exist but are rarely used.
- **Every banknote carries the portrait of Hồ Chí Minh on the obverse.**
- Approximate color families (verify against a real note before a hero shot):
  10,000₫ olive-brown · 20,000₫ blue · 50,000₫ red-pink · 100,000₫ green ·
  200,000₫ orange-red · 500,000₫ teal blue-green.
- Notes feel like smooth plastic (polymer), not paper.

## Hard rules

1. **Avoid close-ups of banknotes.** This is the single most effective rule.
   Depict money at mid or wide distance — a hand paying at a stall, a wallet
   opened at a counter — where notes read by color and size but text and the
   portrait stay illegible. Never prompt for a "macro shot of the banknote".
2. **Portrait dignity is non-negotiable.** The portrait of Hồ Chí Minh must
   never appear distorted, warped, parodied, defaced, or placed in a
   disrespectful or comic context. Any frame showing a distorted or
   disrespectful portrait is a **material defect → regenerate immediately**,
   no matter how good the rest of the shot is.
3. **No fabricated denominations or text.** If numerals or words on a note
   are visible and garbled/wrong, regenerate or reframe wider — never ship it.
4. **Do not depict currency being destroyed, burned, or thrown away.**

## Prompt guidance

When `shows_currency` is true for a scene:
- In `currency_detail`, name the exact note(s): denomination + color, e.g.
  "traveler pays with a blue 20,000₫ polymer note at a street-food stall;
  mid shot, note recognizable by color, text not legible".
- In `video_prompt`, describe the money the same way and add to the negative
  prompt: "garbled text on banknotes, distorted portrait, wrong currency,
  close-up of banknote, burning money".
- Prefer action over object: *paying*, *counting change*, *wallet in hand* —
  not *the banknote itself*.

## QA (frames)

`scripts/qa_frames.py` adds a **CURRENCY QA** section to the checklist of any
scene with `shows_currency: true`. When reviewing frames (`references/frame-qa.md`):

- [ ] Note color/size matches the stated denomination family.
- [ ] No readable text or numerals are garbled or wrong.
- [ ] **The portrait of Hồ Chí Minh is dignified and undistorted.** Any warp,
      cartoonish distortion, or disrespectful context → `regenerate`, and say
      so explicitly in `qa_report.json` notes.
- [ ] No close-up makes the note look like a counterfeit prop (if a close-up
      slipped through, flag it even when the art looks clean).

## Limits (honest)

- A video model will not produce a numismatically correct banknote. The QA
  system enforces *respectful and plausible*, not *exact*.
- Frame review catches visible distortion; it cannot certify micro-text or
  security features — which is exactly why close-ups are banned by rule 1.
