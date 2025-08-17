export function stackItems(raw) {
  const result = {};
  if (!raw) return result;
  if (Array.isArray(raw)) {
    for (const key of raw) {
      result[key] = (result[key] || 0) + 1;
    }
  } else {
    for (const [key, value] of Object.entries(raw)) {
      result[key] = (result[key] || 0) + Number(value);
    }
  }
  return result;
}

const ELEMENT_NAMES = {
  fire: 'Fire',
  ice: 'Ice',
  wind: 'Wind',
  light: 'Light',
  lightning: 'Lightning',
  dark: 'Dark',
  generic: 'Generic',
  ticket: 'Ticket'
};

export function formatName(key) {
  const [element, rank] = key.split('_');
  const name = ELEMENT_NAMES[element] || element;
  if (!rank) return name;
  const stars = '★'.repeat(parseInt(rank, 10));
  return `${name} ${stars}`;
}
