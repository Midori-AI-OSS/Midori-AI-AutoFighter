// Helper functions for persisting the current run in localStorage.
// The state consists of the active runId and the identifier for the next room.
// Each helper is deliberately small to keep page components focused on orchestration.

const KEY = 'runState';

/** Load the saved run state from localStorage.
 * @returns {{runId: string, nextRoom: string}|null}
 */
export function loadRunState() {
  const raw = localStorage.getItem(KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

/** Persist the provided run identifier and next room reference. */
export function saveRunState(runId, nextRoom) {
  localStorage.setItem(KEY, JSON.stringify({ runId, nextRoom }));
}

/** Remove any stored run information. */
export function clearRunState() {
  localStorage.removeItem(KEY);
}
