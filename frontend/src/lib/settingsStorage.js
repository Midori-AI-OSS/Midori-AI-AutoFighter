const SETTINGS_KEY = 'autofighter_settings';

export function loadSettings() {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY);
    if (!raw) return {};
    const data = JSON.parse(raw);
    if (data.framerate !== undefined) data.framerate = Number(data.framerate);
    return data;
  } catch {
    return {};
  }
}

export function saveSettings(settings) {
  try {
    const current = loadSettings();
    const merged = { ...current, ...settings };
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(merged));
  } catch {
    // ignore write errors
  }
}

export function clearSettings() {
  try {
    localStorage.removeItem(SETTINGS_KEY);
  } catch {
    // ignore clear errors
  }
}
