const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:59002';

export async function getBackendFlavor() {
  const res = await fetch(`${API_BASE}/`, { cache: 'no-store' });
  const data = await res.json();
  return data.flavor;
}

export async function getPlayers() {
  const res = await fetch(`${API_BASE}/players`, { cache: 'no-store' });
  return res.json();
}

export async function getGacha() {
  const res = await fetch(`${API_BASE}/gacha`, { cache: 'no-store' });
  return res.json();
}

export async function pullGacha(count = 1) {
  const res = await fetch(`${API_BASE}/gacha/pull`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ count })
  });
  if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  return res.json();
}

export async function setAutoCraft(enabled) {
  const res = await fetch(`${API_BASE}/gacha/auto-craft`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ enabled })
  });
  return res.json();
}

export async function craftItems() {
  const res = await fetch(`${API_BASE}/gacha/craft`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  return res.json();
}

export async function getPlayerConfig() {
  const res = await fetch(`${API_BASE}/player/editor`, { cache: 'no-store' });
  return res.json();
}

export async function savePlayerConfig(config) {
  const res = await fetch(`${API_BASE}/player/editor`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config)
  });
  return res.json();
}

export async function endRun(runId) {
  const res = await fetch(`${API_BASE}/run/${runId}`, { method: 'DELETE' });
  return res.ok;
}

export async function wipeData() {
  const res = await fetch(`${API_BASE}/save/wipe`, { method: 'POST' });
  if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  return res.json();
}

export async function exportSave() {
  const res = await fetch(`${API_BASE}/save/backup`, { cache: 'no-store' });
  return res.blob();
}

export async function importSave(file) {
  const res = await fetch(`${API_BASE}/save/restore`, {
    method: 'POST',
    body: await file.arrayBuffer()
  });
  return res.json();
}
