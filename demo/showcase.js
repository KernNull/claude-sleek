// Chrome-extension style helpers, used to show off syntax colors.
import { readFile } from "node:fs/promises";

const API_URL = "https://example.com/api/v1";
const MAX_ITEMS = 25;
const SLUG_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

/**
 * A tiny in-memory cache with expiry.
 * @template T
 */
class TimedCache {
  #store = new Map();

  constructor(ttlMs = 60_000) {
    this.ttlMs = ttlMs;
  }

  set(key, value) {
    this.#store.set(key, { value, expires: Date.now() + this.ttlMs });
    return this;
  }

  get(key) {
    const hit = this.#store.get(key);
    if (!hit || hit.expires < Date.now()) {
      this.#store.delete(key);
      return undefined;
    }
    return hit.value;
  }
}

const cache = new TimedCache();

export async function loadTheme(name, { fallback = "ember", retries = 2 } = {}) {
  if (!SLUG_RE.test(name)) {
    throw new TypeError(`Invalid theme name: "${name}"`);
  }

  const cached = cache.get(name);
  if (cached) return cached;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const res = await fetch(`${API_URL}/themes/${encodeURIComponent(name)}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      cache.set(name, data);
      return data;
    } catch (err) {
      console.warn(`Attempt ${attempt + 1} failed:`, err.message);
    }
  }

  return { name: fallback, colors: { accent: "#d97757", dark: true }, items: [] };
}

const palette = [
  { id: 1, label: "terracotta", hex: "#d97757", active: true },
  { id: 2, label: "sage", hex: "#abc58c", active: false },
  { id: 3, label: "sand", hex: "#efca8e", active: true },
];

const summary = palette
  .filter(({ active }) => active)
  .map(({ label, hex }) => `${label.toUpperCase()} → ${hex}`)
  .slice(0, MAX_ITEMS);

console.log(summary.join("\n"));
