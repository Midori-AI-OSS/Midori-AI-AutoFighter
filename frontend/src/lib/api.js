export async function startRun(party, damageType = '') {
  const res = await fetch('http://localhost:59002/run/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ party, damage_type: damageType })
  });
  return res.json();
}

export async function updateParty(runId, party) {
  const res = await fetch(`http://localhost:59002/party/${runId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ party })
  });
  return res.json();
}

export async function fetchMap(runId) {
  const res = await fetch(`http://localhost:59002/map/${runId}`);
  return res.json();
}

export async function getPlayers() {
  const res = await fetch('http://localhost:59002/players');
  return res.json();
}

export async function battleRoom(runId, action = '') {
  const res = await fetch(`http://localhost:59002/rooms/${runId}/battle`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action })
  });
  return res.json();
}

export async function shopRoom(runId, action = '') {
  const res = await fetch(`http://localhost:59002/rooms/${runId}/shop`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action })
  });
  return res.json();
}

export async function restRoom(runId, action = '') {
  const res = await fetch(`http://localhost:59002/rooms/${runId}/rest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action })
  });
  return res.json();
}

export async function getGacha() {
  const res = await fetch('http://localhost:59002/gacha');
  return res.json();
}

export async function pullGacha(count = 1) {
  const res = await fetch('http://localhost:59002/gacha/pull', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ count })
  });
  return res.json();
}

export async function setAutoCraft(enabled) {
  const res = await fetch('http://localhost:59002/gacha/auto-craft', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ enabled })
  });
  return res.json();
}

export async function craftItems() {
  const res = await fetch('http://localhost:59002/gacha/craft', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  return res.json();
}

export async function getPlayerConfig() {
  const res = await fetch('http://localhost:59002/player/editor');
  return res.json();
}

export async function savePlayerConfig(config) {
  const res = await fetch('http://localhost:59002/player/editor', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config)
  });
  return res.json();
}
