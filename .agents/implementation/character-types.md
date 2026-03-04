# Character Types

Characters are tagged with a body type for party composition and future UI cues.

- **Type A** – Masculine frame.
- **Type B** – Feminine frame.
- **Type C** – Androgynous frame.

The `CharacterType` enum lives in `autofighter.character` and each player plugin
declares its type via a `char_type` attribute. `Stats` records the chosen
`char_type` for the player so future systems can filter or display characters by
type.

