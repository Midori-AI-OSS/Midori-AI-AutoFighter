const cardModules =
  typeof import.meta.glob === 'function'
    ? import.meta.glob('./assets/cards/gray/*.png', {
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

function prepare(mods) {
  const assets = {};
  const list = [];
  for (const path in mods) {
    const name = path.split('/').pop().replace('.png', '');
    const href = new URL(mods[path], import.meta.url).href;
    assets[name] = href;
    list.push(href);
  }
  if (list.length) {
    assets._fallback = list[0];
    assets._all = list;
  }
  return assets;
}

export const cardArt = prepare(cardModules);
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
