import { httpGet } from './httpClient.js';

const RADIO_STREAM_BASE = 'https://radio.midori-ai.xyz';
const RADIO_QUALITY_VALUES = new Set(['low', 'medium', 'high']);

export function normalizeRadioChannel(value) {
  const raw = String(value || '').trim().toLowerCase();
  if (!raw) return 'all';
  if (!/^[a-z0-9-]{1,40}$/.test(raw)) return 'all';
  return raw;
}

export function normalizeRadioQuality(value) {
  const raw = String(value || '').trim().toLowerCase();
  if (RADIO_QUALITY_VALUES.has(raw)) return raw;
  return 'medium';
}

export function buildRadioStreamUrl({ channel = 'all', quality = 'medium', cacheBust = false } = {}) {
  const url = new URL('/radio/v1/stream', RADIO_STREAM_BASE);
  url.searchParams.set('channel', normalizeRadioChannel(channel));
  url.searchParams.set('q', normalizeRadioQuality(quality));
  if (cacheBust) {
    url.searchParams.set('ts', String(Date.now()));
  }
  return url.toString();
}

export async function getRadioChannels() {
  return httpGet('/radio/channels', { cache: 'no-store' }, true);
}

export async function getRadioCurrent(channel = 'all') {
  const selected = normalizeRadioChannel(channel);
  return httpGet(`/radio/current?channel=${encodeURIComponent(selected)}`, { cache: 'no-store' }, true);
}

export async function getRadioArt(channel = 'all') {
  const selected = normalizeRadioChannel(channel);
  return httpGet(`/radio/art?channel=${encodeURIComponent(selected)}`, { cache: 'no-store' }, true);
}

export function getRadioArtImageUrl(channel = 'all') {
  const selected = normalizeRadioChannel(channel);
  return `/api/radio/art/image?channel=${encodeURIComponent(selected)}`;
}

export function resolveRadioArtUrl(rawUrl, channel = 'all') {
  const fallback = getRadioArtImageUrl(channel);
  const normalized = String(rawUrl || '').trim();
  if (!normalized) return fallback;
  if (/^https?:\/\//i.test(normalized)) return normalized;
  if (normalized.startsWith('/api/')) return normalized;
  if (normalized.startsWith('/radio/')) return `/api${normalized}`;
  if (normalized.startsWith('/')) return normalized;
  return normalized;
}
