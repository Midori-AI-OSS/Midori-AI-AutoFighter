// Enhanced asset loader for characters, backgrounds, and damage types

import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';

import { Flame, Snowflake, Zap, Sun, Moon, Wind, Circle } from 'lucide-svelte';

function toUrl(src) {
  return new URL(src, import.meta.url).href;
}

// Node fallback when `import.meta.glob` is unavailable (tests)
function collectPngs(dir) {
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .flatMap(entry => {
      const full = path.join(dir, entry.name);
      return entry.isDirectory() ? collectPngs(full) : full.endsWith('.png') ? [full] : [];
    });
}

const charactersDir = new URL('./assets/characters', import.meta.url);
const backgroundsDir = new URL('./assets/backgrounds', import.meta.url);

// Load all character images (including folders and fallbacks)
const characterModules =
  typeof import.meta.glob === 'function'
    ? Object.fromEntries(
        Object.entries(
          import.meta.glob('./assets/characters/**/*.png', {
            eager: true,
            import: 'default',
            query: '?url'
          })
        ).map(([p, src]) => [p, toUrl(src)])
      )
    : Object.fromEntries(
        collectPngs(charactersDir.pathname).map(p => [
          `./assets/characters/${path.relative(charactersDir.pathname, p).replace(/\\/g, '/')}`,
          pathToFileURL(p).href
        ])
      );

const fallbackModules =
  typeof import.meta.glob === 'function'
    ? Object.fromEntries(
        Object.entries(
          import.meta.glob('./assets/characters/fallbacks/*.png', {
            eager: true,
            import: 'default',
            query: '?url'
          })
        ).map(([p, src]) => [p, toUrl(src)])
      )
    : Object.fromEntries(
        collectPngs(path.join(charactersDir.pathname, 'fallbacks')).map(p => [
          `./assets/characters/fallbacks/${path.basename(p)}`,
          pathToFileURL(p).href
        ])
      );

const backgroundModules =
  typeof import.meta.glob === 'function'
    ? Object.fromEntries(
        Object.entries(
          import.meta.glob('./assets/backgrounds/*.png', {
            eager: true,
            import: 'default',
            query: '?url'
          })
        ).map(([p, src]) => [p, toUrl(src)])
      )
    : Object.fromEntries(
        collectPngs(backgroundsDir.pathname).map(p => [
          `./assets/backgrounds/${path.basename(p)}`,
          pathToFileURL(p).href
        ])
      );

const ELEMENT_ICONS = {
  fire: Flame,
  ice: Snowflake,
  lightning: Zap,
  light: Sun,
  dark: Moon,
  wind: Wind,
  generic: Circle
};

const ELEMENT_COLORS = {
  fire: '#e25822',
  ice: '#82caff',
  lightning: '#ffd700',
  light: '#ffff99',
  dark: '#8a2be2',
  wind: '#7fff7f',
  generic: '#cccccc'
};

// Parse character assets into organized structure
const characterAssets = {};
const fallbackAssets = Object.values(fallbackModules);
const backgroundAssets = Object.values(backgroundModules);
const defaultFallback = toUrl('./assets/midoriai-logo.png');

// Organize character assets by character ID (folder or single file)
Object.keys(characterModules).forEach(path => {
  const match = path.match(/\.\/assets\/characters\/(.+?)\/(.+?)\.png$/) || 
                path.match(/\.\/assets\/characters\/(.+?)\.png$/);
  
  if (match) {
    const [, charId, fileName] = match;
    const actualCharId = fileName ? charId : charId.replace('.png', '');
    
    if (!characterAssets[actualCharId]) {
      characterAssets[actualCharId] = [];
    }
    
    // Skip fallbacks folder
    if (actualCharId !== 'fallbacks') {
      characterAssets[actualCharId].push(characterModules[path]);
    }
  }
});

// Seeded random function for consistent hourly backgrounds
function seededRandom(seed) {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

// Get current hour seed (changes every hour)
function getHourSeed() {
  const now = new Date();
  return now.getFullYear() * 1000000 + 
         now.getMonth() * 10000 + 
         now.getDate() * 100 + 
         now.getHours();
}

// Get random image from character folder or fallback
export function getCharacterImage(characterId, _isPlayer = false) {
  // Check if character has dedicated images
  if (characterAssets[characterId] && characterAssets[characterId].length > 0) {
    const images = characterAssets[characterId];
    const randomIndex = Math.floor(Math.random() * images.length);
    return images[randomIndex];
  }
  
  // Use fallback images
  if (fallbackAssets.length > 0) {
    const randomIndex = Math.floor(Math.random() * fallbackAssets.length);
    return fallbackAssets[randomIndex];
  }
  
  // Final fallback - use repository logo
  return defaultFallback;
}

// Get background with hourly consistency
export function getHourlyBackground() {
  if (backgroundAssets.length === 0) return defaultFallback;
  
  const seed = getHourSeed();
  const randomIndex = Math.floor(seededRandom(seed) * backgroundAssets.length);
  return backgroundAssets[randomIndex];
}

// Get random background (for immediate random needs)
export function getRandomBackground() {
  if (backgroundAssets.length === 0) return defaultFallback;

  const randomIndex = Math.floor(Math.random() * backgroundAssets.length);
  return backgroundAssets[randomIndex];
}

// Get all available character IDs
export function getAvailableCharacterIds() {
  return Object.keys(characterAssets);
}

// Get random fallback image
export function getRandomFallback() {
  if (fallbackAssets.length === 0) return defaultFallback;

  const randomIndex = Math.floor(Math.random() * fallbackAssets.length);
  return fallbackAssets[randomIndex];
}

export function getElementIcon(element) {
  return ELEMENT_ICONS[(element || '').toLowerCase()] || Circle;
}

export function getElementColor(element) {
  return ELEMENT_COLORS[(element || '').toLowerCase()] || '#aaa';
}

// Export assets for debugging
export { characterAssets, fallbackAssets, backgroundAssets };
