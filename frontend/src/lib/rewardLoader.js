const cardModules = import.meta.glob('../../../.codex/downloads/card-art/*.png', { eager: true, import: 'default', query: '?url' });
const relicModules = import.meta.glob('../../../.codex/downloads/relics/*.png', { eager: true, import: 'default', query: '?url' });
const itemModules = import.meta.glob('../../../.codex/downloads/item-art/*.png', { eager: true, import: 'default', query: '?url' });

function prepare(mods) {
  const assets = {};
  for (const path in mods) {
    const name = path.split('/').pop().replace('.png', '');
    assets[name] = new URL(mods[path], import.meta.url).href;
  }
  const values = Object.values(assets);
  if (values.length) {
    assets._fallback = values[0];
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

