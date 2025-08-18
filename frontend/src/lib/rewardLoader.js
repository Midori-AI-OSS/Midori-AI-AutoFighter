const cardModules =
  typeof import.meta.glob === 'function'
    ? import.meta.glob('./assets/cards/*/*.png', {
        eager: true,
        import: 'default',
        query: '?url'
      })
    : {};
const relicModules =
  typeof import.meta.glob === 'function'
    ? import.meta.glob('./assets/relics/*/*.png', {
        eager: true,
        import: 'default',
        query: '?url'
      })
    : {};
const itemModules =
  typeof import.meta.glob === 'function'
    ? import.meta.glob('./assets/items/*/*.png', {
        eager: true,
        import: 'default',
        query: '?url'
      })
    : {};

function prepare(mods, fallback) {
  const assets = {};
  const list = [];
  for (const path in mods) {
    const name = path.split('/').pop().replace('.png', '');
    const href = new URL(mods[path], import.meta.url).href;
    assets[name] = href;
    list.push(href);
  }
  assets._all = list;
  assets._fallback = fallback || list[0] || '';
  return assets;
}

const defaultCardFallback = new URL(
  './assets/cards/fallback/placeholder.png',
  import.meta.url
).href;

export const cardArt = prepare(cardModules, defaultCardFallback);
export const relicArt = prepare(relicModules);
export const itemArt = prepare(itemModules);

export function getRewardArt(type, id) {
  const lookup = type === 'card' ? cardArt : type === 'relic' ? relicArt : itemArt;
  return lookup[id] || lookup._fallback || '';
}

export function randomCardArt() {
  const list = cardArt._all || [];
  if (!list.length) {
    return cardArt._fallback || '';
  }
  const idx = Math.floor(Math.random() * list.length);
  return list[idx];
}
