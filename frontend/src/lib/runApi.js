// Lightweight wrappers for backend run endpoints.
// These isolate fetch details from components that coordinate a run.

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:59002';

export async function startRun(party, damageType = '') {
  const res = await fetch(`${API_BASE}/run/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ party, damage_type: damageType })
  });
  return res.json();
}

export async function getMap(runId) {
  const res = await fetch(`${API_BASE}/map/${runId}`, { cache: 'no-store' });
  if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  return res.json();
}

export async function updateParty(runId, party) {
  const res = await fetch(`${API_BASE}/party/${runId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ party })
  });
  return res.json();
}

export async function roomAction(runId, type, action = '') {
  const res = await fetch(`${API_BASE}/rooms/${runId}/${type}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action })
  });
  if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  return res.json();
}

export async function advanceRoom(runId) {
  const res = await fetch(`${API_BASE}/run/${runId}/next`, { method: 'POST' });
  if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  return res.json();
}

export async function chooseCard(runId, cardId) {
  const res = await fetch(`${API_BASE}/cards/${runId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ card: cardId })
  });
  return res.json();
}

export async function chooseRelic(runId, relicId) {
  const res = await fetch(`${API_BASE}/relics/${runId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ relic: relicId })
  });
  return res.json();
}
