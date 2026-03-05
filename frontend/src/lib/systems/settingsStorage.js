import { writable } from 'svelte/store';

const SETTINGS_KEY = 'autofighter_settings';
const SETTINGS_VERSION = 3;
const RADIO_SOURCE_VALUES = new Set(['game', 'midoriai_radio']);
const RADIO_QUALITY_VALUES = new Set(['low', 'medium', 'high']);
const RADIO_CHANNEL_PATTERN = /^[a-z0-9-]{1,40}$/;

// Create reactive stores for settings
export const motionStore = writable(null);
export const themeStore = writable(null);
export const uiStore = writable(null);

function normalizeMusicSource(value) {
  const raw = String(value || '').trim().toLowerCase();
  if (RADIO_SOURCE_VALUES.has(raw)) {
    return raw;
  }
  return 'game';
}

function normalizeRadioChannelSetting(value) {
  const raw = String(value || '').trim().toLowerCase();
  if (!raw) return 'all';
  if (raw === 'all') return 'all';
  if (!RADIO_CHANNEL_PATTERN.test(raw)) return 'all';
  return raw;
}

function normalizeRadioQualitySetting(value) {
  const raw = String(value || '').trim().toLowerCase();
  if (RADIO_QUALITY_VALUES.has(raw)) {
    return raw;
  }
  return 'medium';
}

function clampRadioVolume(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) {
    return 70;
  }
  return Math.max(0, Math.min(100, Math.round(numeric)));
}

export function normalizeMusicVolumeSetting(value, options = {}) {
  const fallback = Number.isFinite(Number(options.fallback)) ? Number(options.fallback) : 70;
  const allowLegacyScale = options.allowLegacyScale !== false;
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) {
    return Math.max(0, Math.min(100, Math.round(fallback)));
  }
  const scaled = allowLegacyScale && numeric >= 0 && numeric <= 10 ? numeric * 10 : numeric;
  return Math.max(0, Math.min(100, Math.round(scaled)));
}

// Theme definitions
export const THEMES = {
  default: {
    name: 'Default',
    accent: 'level-based', // special value to use level-based hue
    background: 'rotating'
  },
  solaris: {
    name: 'Solaris',
    accent: '#ffb347', // warm orange
    background: 'static'
  },
  nocturne: {
    name: 'Nocturne', 
    accent: '#9370db', // purple
    background: 'static'
  },
  custom: {
    name: 'Custom',
    accent: '#8ac',
    background: 'static'
  }
};

// Default settings structure
function getDefaultSettings() {
  const prefersReducedMotion = typeof window !== 'undefined' && 
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
  return {
    version: SETTINGS_VERSION,
    theme: {
      selected: 'default',
      customAccent: '#8ac',
      backgroundBehavior: 'rotating', // 'rotating', 'static', 'custom'
      customBackground: null
    },
    motion: {
      globalReducedMotion: prefersReducedMotion,
      disableFloatingDamage: false,
      disablePortraitGlows: false,
      simplifyOverlayTransitions: false,
      disableStarStorm: false,
      enableBattleFx: false
    },
    ui: {
      conciseDescriptions: false
    },
    // Legacy settings for backward compatibility
    musicVolume: 70,
    framerate: 60,
    reducedMotion: prefersReducedMotion,
    showActionValues: false,
    showTurnCounter: true,
    flashEnrageCounter: true,
    fullIdleMode: false,
    skipBattleReview: false,
    skipBattleReviewPreference: false,
    animationSpeed: 1.0,
    musicSource: 'game',
    radioEnabled: false,
    radioAutostart: false,
    radioStayOpen: false,
    radioChannel: 'all',
    radioQuality: 'medium',
    radioVolume: 70
  };
}

// Migration logic
function migrateSettings(data) {
  if (!data.version || data.version < SETTINGS_VERSION) {
    
    // Migrate from v1 to v2: convert flat reducedMotion to hierarchical motion settings
    if (data.version !== SETTINGS_VERSION) {
      const defaults = getDefaultSettings();
      
      // Preserve existing settings
      const migrated = {
        ...defaults,
        ...data,
        version: SETTINGS_VERSION
      };

      migrated.motion = {
        ...defaults.motion,
        ...(data.motion || {})
      };

      // If we had an old reducedMotion setting, migrate it to the new structure
      if (data.reducedMotion !== undefined) {
        migrated.motion = {
          ...migrated.motion,
          globalReducedMotion: Boolean(data.reducedMotion),
          // When old reducedMotion was enabled, enable most motion reduction options
          disableFloatingDamage: Boolean(data.reducedMotion),
          disablePortraitGlows: Boolean(data.reducedMotion),
          simplifyOverlayTransitions: Boolean(data.reducedMotion),
          disableStarStorm: Boolean(data.reducedMotion)
        };
      }
      
      // Initialize theme settings if not present
      if (!data.theme) {
        migrated.theme = defaults.theme;
      }
      
      // Initialize ui settings if not present
      if (!data.ui) {
        migrated.ui = defaults.ui;
      }
      
      return migrated;
    }
  }
  
  return data;
}

export function loadSettings() {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY);
    if (!raw) {
      const defaults = getDefaultSettings();
      // Initialize stores
      motionStore.set(defaults.motion);
      themeStore.set(defaults.theme);
      uiStore.set(defaults.ui);
      return defaults;
    }
    
    let data = JSON.parse(raw);
    
    // Apply migration
    data = migrateSettings(data);
    
    // Type coercion for legacy numeric/boolean fields
    if (data.framerate !== undefined) data.framerate = Number(data.framerate);
    if (data.reducedMotion !== undefined) data.reducedMotion = Boolean(data.reducedMotion);
    if (data.showActionValues !== undefined) data.showActionValues = Boolean(data.showActionValues);
    if (data.showTurnCounter !== undefined) data.showTurnCounter = Boolean(data.showTurnCounter);
    if (data.flashEnrageCounter !== undefined) data.flashEnrageCounter = Boolean(data.flashEnrageCounter);
    if (data.fullIdleMode !== undefined) data.fullIdleMode = Boolean(data.fullIdleMode);
    if (data.skipBattleReview !== undefined) data.skipBattleReview = Boolean(data.skipBattleReview);
    if (data.skipBattleReviewPreference !== undefined) {
      data.skipBattleReviewPreference = Boolean(data.skipBattleReviewPreference);
    }
    if (data.animationSpeed !== undefined) {
      const numeric = Number(data.animationSpeed);
      if (Number.isFinite(numeric) && numeric > 0) {
        const clamped = Math.min(2, Math.max(0.1, numeric));
        data.animationSpeed = Math.round(clamped * 10) / 10;
      } else {
        delete data.animationSpeed;
      }
    }
    if (data.musicVolume !== undefined) {
      data.musicVolume = normalizeMusicVolumeSetting(data.musicVolume);
    }
    if (data.musicSource !== undefined) data.musicSource = normalizeMusicSource(data.musicSource);
    if (data.radioEnabled !== undefined) data.radioEnabled = Boolean(data.radioEnabled);
    if (data.radioAutostart !== undefined) data.radioAutostart = Boolean(data.radioAutostart);
    if (data.radioStayOpen !== undefined) data.radioStayOpen = Boolean(data.radioStayOpen);
    if (data.radioChannel !== undefined) data.radioChannel = normalizeRadioChannelSetting(data.radioChannel);
    if (data.radioQuality !== undefined) data.radioQuality = normalizeRadioQualitySetting(data.radioQuality);
    if (data.radioVolume !== undefined) data.radioVolume = clampRadioVolume(data.radioVolume);
    
    // Ensure motion settings exist
    const defaults = getDefaultSettings();

    data.motion = {
      ...defaults.motion,
      ...(data.motion || {})
    };

    // Ensure theme settings exist
    if (!data.theme) {
      data.theme = defaults.theme;
    }

    // Ensure ui settings exist
    if (!data.ui) {
      data.ui = defaults.ui;
    }

    if (data.showTurnCounter === undefined) {
      data.showTurnCounter = defaults.showTurnCounter;
    }

    if (data.flashEnrageCounter === undefined) {
      data.flashEnrageCounter = defaults.flashEnrageCounter;
    }
    if (data.skipBattleReviewPreference === undefined) {
      data.skipBattleReviewPreference = data.skipBattleReview ?? defaults.skipBattleReviewPreference;
    }
    if (data.musicSource === undefined) {
      data.musicSource = defaults.musicSource;
    }
    if (data.musicVolume === undefined) {
      data.musicVolume = defaults.musicVolume;
    }
    if (data.radioEnabled === undefined) {
      data.radioEnabled = defaults.radioEnabled;
    }
    if (data.radioAutostart === undefined) {
      data.radioAutostart = defaults.radioAutostart;
    }
    if (data.radioStayOpen === undefined) {
      data.radioStayOpen = defaults.radioStayOpen;
    }
    if (data.radioChannel === undefined) {
      data.radioChannel = defaults.radioChannel;
    }
    if (data.radioQuality === undefined) {
      data.radioQuality = defaults.radioQuality;
    }
    if (data.radioVolume === undefined) {
      data.radioVolume = defaults.radioVolume;
    }
    
    // Update stores
    motionStore.set(data.motion);
    themeStore.set(data.theme);
    uiStore.set(data.ui);
    
    return data;
  } catch {
    const defaults = getDefaultSettings();
    motionStore.set(defaults.motion);
    themeStore.set(defaults.theme);
    uiStore.set(defaults.ui);
    return defaults;
  }
}

export function saveSettings(settings) {
  try {
    const safeSettings = settings ?? {};
    const skipProvided = Object.prototype.hasOwnProperty.call(safeSettings, 'skipBattleReview');
    const preferenceProvided = Object.prototype.hasOwnProperty.call(safeSettings, 'skipBattleReviewPreference');
    const musicVolumeProvided = Object.prototype.hasOwnProperty.call(safeSettings, 'musicVolume');
    const radioVolumeProvided = Object.prototype.hasOwnProperty.call(safeSettings, 'radioVolume');
    const current = loadSettings();
    const merged = { ...current, ...safeSettings };
    
    // Ensure version is set
    merged.version = SETTINGS_VERSION;
    
    // Legacy field validation
    if (merged.fullIdleMode !== undefined) merged.fullIdleMode = Boolean(merged.fullIdleMode);
    if (merged.showTurnCounter !== undefined) merged.showTurnCounter = Boolean(merged.showTurnCounter);
    if (merged.flashEnrageCounter !== undefined) merged.flashEnrageCounter = Boolean(merged.flashEnrageCounter);
    if (merged.skipBattleReview !== undefined) merged.skipBattleReview = Boolean(merged.skipBattleReview);
    const fallbackPreference = current.skipBattleReviewPreference ?? current.skipBattleReview ?? false;
    let nextPreference;
    if (preferenceProvided) {
      nextPreference = Boolean(safeSettings.skipBattleReviewPreference);
    } else if (skipProvided) {
      nextPreference = Boolean(safeSettings.skipBattleReview);
    } else if (merged.skipBattleReviewPreference !== undefined) {
      nextPreference = Boolean(merged.skipBattleReviewPreference);
    } else if (merged.skipBattleReview !== undefined) {
      nextPreference = Boolean(merged.skipBattleReview);
    } else {
      nextPreference = fallbackPreference;
    }
    merged.skipBattleReviewPreference = nextPreference;

    if (merged.fullIdleMode) {
      merged.skipBattleReview = true;
    } else if (!skipProvided && merged.skipBattleReview === undefined) {
      merged.skipBattleReview = nextPreference;
    }
    if (merged.animationSpeed !== undefined) {
      const numeric = Number(merged.animationSpeed);
      if (Number.isFinite(numeric) && numeric > 0) {
        const clamped = Math.min(2, Math.max(0.1, numeric));
        merged.animationSpeed = Math.round(clamped * 10) / 10;
      } else {
        delete merged.animationSpeed;
      }
    }
    merged.musicVolume = normalizeMusicVolumeSetting(merged.musicVolume);
    if (!musicVolumeProvided && radioVolumeProvided) {
      merged.musicVolume = normalizeMusicVolumeSetting(merged.radioVolume, { allowLegacyScale: false });
    }
    merged.musicSource = normalizeMusicSource(merged.musicSource);
    merged.radioEnabled = Boolean(merged.radioEnabled);
    merged.radioAutostart = Boolean(merged.radioAutostart);
    merged.radioStayOpen = Boolean(merged.radioStayOpen);
    merged.radioChannel = normalizeRadioChannelSetting(merged.radioChannel);
    merged.radioQuality = normalizeRadioQualitySetting(merged.radioQuality);
    if (!radioVolumeProvided || musicVolumeProvided) {
      merged.radioVolume = clampRadioVolume(merged.musicVolume);
    } else {
      merged.radioVolume = clampRadioVolume(merged.radioVolume);
    }
    
    // Validate theme settings
    if (merged.theme) {
      if (merged.theme.selected && !THEMES[merged.theme.selected]) {
        merged.theme.selected = 'default';
      }
      if (merged.theme.backgroundBehavior && 
          !['rotating', 'static', 'custom'].includes(merged.theme.backgroundBehavior)) {
        merged.theme.backgroundBehavior = 'rotating';
      }
    }
    
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(merged));
    
    // Update stores when settings change
    if (merged.motion) {
      motionStore.set(merged.motion);
    }
    if (merged.theme) {
      themeStore.set(merged.theme);
    }
    if (merged.ui) {
      uiStore.set(merged.ui);
    }
  } catch {
    // ignore write errors
  }
}

// Helper functions for accessing nested settings
export function getThemeSettings() {
  const settings = loadSettings();
  return settings.theme || getDefaultSettings().theme;
}

export function getMotionSettings() {
  const settings = loadSettings();
  return settings.motion || getDefaultSettings().motion;
}

export function updateThemeSettings(themeUpdates) {
  const current = loadSettings();
  const updatedTheme = { ...current.theme, ...themeUpdates };
  saveSettings({
    theme: updatedTheme
  });
  themeStore.set(updatedTheme);
}

export function updateMotionSettings(motionUpdates) {
  const current = loadSettings();
  const updatedMotion = { ...current.motion, ...motionUpdates };
  saveSettings({
    motion: updatedMotion,
    // Keep legacy reducedMotion in sync
    reducedMotion: updatedMotion.globalReducedMotion
  });
  motionStore.set(updatedMotion);
}

export function getUISettings() {
  const settings = loadSettings();
  return settings.ui || getDefaultSettings().ui;
}

export function updateUISettings(uiUpdates) {
  const current = loadSettings();
  const updatedUI = { ...current.ui, ...uiUpdates };
  saveSettings({
    ui: updatedUI
  });
  uiStore.set(updatedUI);
}

export function clearSettings() {
  try {
    localStorage.removeItem(SETTINGS_KEY);
  } catch {
    // ignore clear errors
  }
}

// Best‑effort client wipe: local/session storage, caches, SW, and IndexedDB
export async function clearAllClientData() {
  // Local + session storage
  try { localStorage.clear(); } catch { /* ignore */ }
  try { sessionStorage && sessionStorage.clear && sessionStorage.clear(); } catch { /* ignore */ }

  // CacheStorage
  try {
    if (typeof caches !== 'undefined' && caches?.keys) {
      const names = await caches.keys();
      await Promise.all(names.map((n) => caches.delete(n)));
    }
  } catch { /* ignore */ }

  // Service workers
  try {
    if (typeof navigator !== 'undefined' && navigator.serviceWorker?.getRegistrations) {
      const regs = await navigator.serviceWorker.getRegistrations();
      await Promise.all(regs.map((r) => r.unregister()));
    }
  } catch { /* ignore */ }

  // IndexedDB (supported in Chromium via indexedDB.databases())
  try {
    if (typeof indexedDB !== 'undefined' && indexedDB?.databases) {
      const dbs = await indexedDB.databases();
      await Promise.all(
        (dbs || [])
          .map((db) => db?.name)
          .filter(Boolean)
          .map(
            (name) =>
              new Promise((resolve) => {
                const req = indexedDB.deleteDatabase(name);
                req.onsuccess = req.onerror = req.onblocked = () => resolve();
              })
          )
      );
    }
  } catch { /* ignore */ }
}
