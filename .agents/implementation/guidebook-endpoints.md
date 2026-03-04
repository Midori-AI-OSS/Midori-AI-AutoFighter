# Guidebook API Endpoints

The frontend Guidebook overlay fetches data from these endpoints to reflect real game content.

- `GET /guidebook/damage-types`
  - Response: `{ damage_types: [{ id, weakness, color, description }] }`
- `GET /guidebook/ultimates`
  - Response: `{ ultimates: [{ id, description }] }`
- `GET /guidebook/passives`
  - Response: `{ passives: [{ id, name, trigger, description }] }`
- `GET /guidebook/shops`
  - Response: `{ reroll_cost, price_by_stars, notes }`
- `GET /guidebook/ui`
  - Response: `{ tips: [{ name, description }] }`
- `GET /guidebook/mechs`
  - Response: `{ mechanics: [{ name, description }] }`

Notes:
- Damage types and ultimates are derived from `plugins.damage_types` classes.
- Passives are discovered from the passive registry.
- Shop data is sourced from `autofighter.rooms.shop` constants.
