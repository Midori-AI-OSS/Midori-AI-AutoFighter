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

export async function getRadioCurrent(channel = 'all', options = {}) {
  const selected = normalizeRadioChannel(channel);
  return httpGet(
    `/radio/current?channel=${encodeURIComponent(selected)}`,
    { cache: 'no-store', signal: options?.signal },
    true
  );
}

export async function getRadioArt(channel = 'all', options = {}) {
  const selected = normalizeRadioChannel(channel);
  return httpGet(
    `/radio/art?channel=${encodeURIComponent(selected)}`,
    { cache: 'no-store', signal: options?.signal },
    true
  );
}

export function getRadioArtImageUrl(channel = 'all') {
  const selected = normalizeRadioChannel(channel);
  return `/api/radio/art/image?channel=${encodeURIComponent(selected)}`;
}

export function appendTrackCacheKey(url, trackKey) {
  const normalizedUrl = String(url || '').trim();
  if (!normalizedUrl) return normalizedUrl;

  const normalizedTrackKey = String(trackKey || '').trim();
  if (!normalizedTrackKey) return normalizedUrl;

  const hashIndex = normalizedUrl.indexOf('#');
  const basePart = hashIndex === -1 ? normalizedUrl : normalizedUrl.slice(0, hashIndex);
  const hashPart = hashIndex === -1 ? '' : normalizedUrl.slice(hashIndex);

  const queryIndex = basePart.indexOf('?');
  const pathPart = queryIndex === -1 ? basePart : basePart.slice(0, queryIndex);
  const queryPart = queryIndex === -1 ? '' : basePart.slice(queryIndex + 1);

  const params = new URLSearchParams(queryPart);
  params.set('midoriai_track', normalizedTrackKey);

  const nextQuery = params.toString();
  if (!nextQuery) {
    return `${pathPart}${hashPart}`;
  }
  return `${pathPart}?${nextQuery}${hashPart}`;
}

export function resolveRadioArtUrl(rawUrl, channel = 'all', trackKey = '') {
  const fallback = getRadioArtImageUrl(channel);
  const normalized = String(rawUrl || '').trim();
  if (!normalized) return appendTrackCacheKey(fallback, trackKey);
  if (/^https?:\/\//i.test(normalized)) return appendTrackCacheKey(normalized, trackKey);
  if (normalized.startsWith('/api/')) return appendTrackCacheKey(normalized, trackKey);
  if (normalized.startsWith('/radio/')) return appendTrackCacheKey(`/api${normalized}`, trackKey);
  if (normalized.startsWith('/')) return appendTrackCacheKey(normalized, trackKey);
  return appendTrackCacheKey(normalized, trackKey);
}
