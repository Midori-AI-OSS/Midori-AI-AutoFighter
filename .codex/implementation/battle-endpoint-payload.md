# Battle Endpoint Payload

`POST /rooms/<run_id>/battle` resolves the next battle node. Fights are fully automated, looping until one side falls, and the backend echoes any provided `action` string. Each round triggers passives and processes damage or healing over time effects before exchanging attacks, pausing briefly between turns to keep the loop async-friendly.

## Request
- `action` (string, optional)

## Response
- `result` (string): always `"battle"` for this endpoint.
- `run_id` (string): identifier for the active run.
- `action` (string): echoes the request `action` or defaults to an empty string.
- `party` (array): updated stats for each party member.
- `gold` (integer): current shared gold pool.
- `relics` (array): list of acquired relic IDs.
- `cards` (array): list of owned card IDs.
- `card_choices` (array): up to three card options with `id`, `name`, and `stars`.
- `relic_choices` (array): up to three relic options with `id`, `name`, and `stars`.
- `loot` (object): summary of rewards with `gold`, `card_choices`, `relic_choices`, and `items` arrays.
- `foes` (array): stats for spawned foes.

Generic damage types are reserved for the Luna player character; other combatants use elemental types such as Fire, Ice, Lightning, Light, Dark, or Wind.

Example:
```json
{
  "result": "battle",
  "run_id": "abc123",
  "action": "",
  "party": [
    {
      "id": "player",
      "name": "Player",
      "char_type": "C",
      "hp": 990,
      "max_hp": 1000,
      "exp": 1,
      "level": 1,
      "exp_multiplier": 1.0,
      "actions_per_turn": 1,
      "atk": 100,
      "crit_rate": 0.05,
      "crit_damage": 2,
      "effect_hit_rate": 0.01,
      "base_damage_type": "Fire",
      "defense": 50,
      "mitigation": 100,
      "regain": 1,
      "dodge_odds": 0,
      "effect_resistance": 1.0,
      "vitality": 1.0,
      "action_points": 1,
      "damage_taken": 11,
      "damage_dealt": 1,
      "kills": 1,
      "last_damage_taken": 10,
      "passives": [],
      "dots": [],
      "hots": [],
      "damage_types": ["Fire"]
    }
  ],
  "gold": 0,
  "relics": [],
  "cards": [],
  "card_choices": [
    {"id": "balanced_diet", "name": "Balanced Diet", "stars": 1},
    {"id": "mindful_tassel", "name": "Mindful Tassel", "stars": 1},
    {"id": "micro_blade", "name": "Micro Blade", "stars": 1}
  ],
  "relic_choices": [],
  "loot": {
    "gold": 0,
    "card_choices": [
      {"id": "balanced_diet", "name": "Balanced Diet", "stars": 1},
      {"id": "mindful_tassel", "name": "Mindful Tassel", "stars": 1},
      {"id": "micro_blade", "name": "Micro Blade", "stars": 1}
    ],
    "relic_choices": [],
    "items": []
  },
  "foes": [
    {
      "id": "slime",
      "name": "Slime",
      "char_type": "C",
      "hp": 0,
      "max_hp": 100,
      "exp": 0,
      "level": 0,
      "exp_multiplier": 0.1,
      "actions_per_turn": 0,
      "atk": 10,
      "crit_rate": 0.005,
      "crit_damage": 0,
      "effect_hit_rate": 0.001,
      "base_damage_type": "Ice",
      "defense": 5,
      "mitigation": 10,
      "regain": 0,
      "dodge_odds": 0,
      "effect_resistance": 0.1,
      "vitality": 0.1,
      "action_points": 0,
      "damage_taken": 0,
      "damage_dealt": 0,
      "kills": 0,
      "last_damage_taken": 0,
      "passives": [],
      "dots": [],
      "hots": [],
      "damage_types": ["Ice"],
      "gold": 0
    }
  ]
}
```

## Testing
- `uv run pytest tests/test_card_rewards.py::test_battle_offers_choices_and_applies_effect`
