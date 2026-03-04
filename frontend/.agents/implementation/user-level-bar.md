# User level bar

The game viewport shows a footer bar indicating global user progress.

* `loadInitialState()` now returns `{ user }` from `/players`.
* `GameViewport.svelte` renders `.user-level-bar` at the bottom of the view.
* The inner bar width is `user_exp / next_level_exp` and uses a
  `linear-gradient(red, green)` background.
