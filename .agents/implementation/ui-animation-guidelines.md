# UI Animation Guidelines

## Reduced Motion
- Honor the user's `prefers-reduced-motion` setting by disabling or simplifying nonessential animations.
- Provide alternative cues (e.g., opacity changes or instant transitions) when motion is reduced.
- Keep critical feedback visible even when animations are removed.
- Turn indicators like the active-fighter arrow should fall back to a static
  pointer when motion is reduced.

## Easing Presets
- Use consistent easing functions to maintain a cohesive feel:
  - `ease-in-out` for most interface transitions.
  - `ease-out` for entering elements.
  - `ease-in` for exiting elements.
- Keep durations between 150ms and 300ms unless a longer effect improves clarity.
- The active-fighter arrow uses a subtle 500ms bounce to draw attention to the
  acting combatant.

## Action Timing
- Backend actions expose `animation_duration` and `animation_per_target` fields.
- Total wait time is `animation_duration + animation_per_target * (targets - 1)`.
- The battle loop emits `animation_start` and `animation_end` events and waits for this duration before the next turn.

## Sound Cues
- Pair major animations with subtle sound effects to reinforce feedback.
- Respect global sound settings and provide a non-audio fallback.
- Avoid repetitive or distracting sounds; use short cues under 500ms.
