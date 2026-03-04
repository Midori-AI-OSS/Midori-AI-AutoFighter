# Asset Icon Placeholders

Item, relic, and card art now use a structured asset layout with 24×24 placeholders so artists can drop in final images later.

## Layout
- `frontend/src/lib/assets/items/{dark,fire,ice,light,lightning,wind,generic}` – resized generic dot icons for each damage type.
- `frontend/src/lib/assets/relics/{1star,2star,3star,4star,5star,fallback}` – colored squares keyed to rarity.
- `frontend/src/lib/assets/cards/{1star,2star,3star,4star,5star,fallback}` – same star-colored placeholders for card art.

## Star Colors
1★ gray, 2★ green, 3★ blue, 4★ purple, 5★ gold, fallback slate.

## Testing
- `bun test`
