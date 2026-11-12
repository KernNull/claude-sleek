// A small typed cache, used to show off TypeScript colors.
import type { ReadonlyDeep } from "./types";

type Entry<T> = { value: T; expires: number };
interface Cache<K extends string, V> {
  get(key: K): V | undefined;
  set(key: K, value: V): this;
}

enum Level { Debug, Info = 2, Error }

export class TimedCache<V> implements Cache<string, V> {
  private store = new Map<string, Entry<V>>();
  constructor(private readonly ttlMs: number = 60_000) {}

  set(key: string, value: V): this {
    this.store.set(key, { value, expires: Date.now() + this.ttlMs });
    return this;
  }

  get(key: string): V | undefined {
    const hit = this.store.get(key);
    return hit && hit.expires > Date.now() ? hit.value : undefined;
  }
}

export async function load<T extends object>(url: string, retries?: number): Promise<T | null> {
  for (let i = 0; i <= (retries ?? 2); i++) {
    const res = await fetch(url);
    if (res.ok) return (await res.json()) as T;
  }
  console.warn(`gave up on ${url}`, Level.Error);
  return null;
}
