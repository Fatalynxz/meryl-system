/**
 * Persistent avatar storage using IndexedDB + localStorage + in-memory cache.
 * 
 * Solves the issue where profile pictures (pfp) disappear after closing tabs,
 * since the database does not have an avatar column and sessionStorage is tab-scoped.
 * IndexedDB safely accommodates large base64 data URLs without hitting the 5MB
 * localStorage quota, while localStorage provides immediate synchronous reads
 * on initial page load to prevent UI flicker.
 */

export interface AvatarIdentifiers {
  userId?: string | number | null;
  username?: string | null;
  email?: string | null;
}

const DB_NAME = "meryl_avatars_db";
const DB_VERSION = 1;
const STORE_NAME = "user_avatars";

// In-memory cache for fast lookups
const memoryCache = new Map<string, string>();

function normalize(value?: string | number | null): string {
  if (value === null || value === undefined) return "";
  return String(value).trim().toLowerCase();
}

function getCacheKeys(identifiers: AvatarIdentifiers): string[] {
  const keys: string[] = [];
  const uid = normalize(identifiers.userId);
  const uname = normalize(identifiers.username);
  const email = normalize(identifiers.email);

  if (uid) {
    keys.push(`uid:${uid}`);
    keys.push(`meryl_avatar_${uid}`);
  }
  if (uname) {
    keys.push(`uname:${uname}`);
    keys.push(`meryl_avatar_${uname}`);
  }
  if (email) {
    keys.push(`email:${email}`);
    keys.push(`meryl_avatar_${email}`);
  }
  return keys;
}

// Open or initialize IndexedDB
function openDb(): Promise<IDBDatabase | null> {
  if (typeof window === "undefined" || !window.indexedDB) {
    return Promise.resolve(null);
  }

  return new Promise((resolve) => {
    try {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME);
        }
      };

      request.onsuccess = () => {
        resolve(request.result);
      };

      request.onerror = () => {
        console.warn("Could not open IndexedDB for avatars:", request.error);
        resolve(null);
      };
    } catch (e) {
      console.warn("IndexedDB error:", e);
      resolve(null);
    }
  });
}

/**
 * Synchronous avatar retrieval from memory cache or localStorage.
 * Call this during component rendering or initial state bootstrap.
 */
export function getStoredAvatarSync(identifiers: AvatarIdentifiers): string | undefined {
  if (typeof window === "undefined") return undefined;

  const uid = normalize(identifiers.userId);
  const uname = normalize(identifiers.username);
  const email = normalize(identifiers.email);

  // 1. Check in-memory cache
  for (const k of getCacheKeys(identifiers)) {
    const cached = memoryCache.get(k);
    if (cached) return cached;
  }

  // 2. Check localStorage with fallback patterns
  const candidateKeys: string[] = [];
  if (uid) candidateKeys.push(`meryl_avatar_${uid}`, `meryl_avatar_uid_${uid}`);
  if (uname) candidateKeys.push(`meryl_avatar_${uname}`, `meryl_avatar_uname_${uname}`);
  if (email) candidateKeys.push(`meryl_avatar_${email}`, `meryl_avatar_email_${email}`);
  candidateKeys.push("meryl_avatar_latest");

  for (const key of candidateKeys) {
    try {
      const val = localStorage.getItem(key);
      if (val && val.length > 10) {
        // Cache in memory for subsequent calls
        for (const k of getCacheKeys(identifiers)) {
          memoryCache.set(k, val);
        }
        return val;
      }
    } catch {
      // LocalStorage access may be restricted in some environments
    }
  }

  return undefined;
}

/**
 * Asynchronous avatar retrieval from IndexedDB.
 * Will hydrate memory and localStorage if found.
 */
export async function getStoredAvatarAsync(identifiers: AvatarIdentifiers): Promise<string | undefined> {
  const syncVal = getStoredAvatarSync(identifiers);
  if (syncVal) return syncVal;

  if (typeof window === "undefined") return undefined;

  const db = await openDb();
  if (!db) return undefined;

  const uid = normalize(identifiers.userId);
  const uname = normalize(identifiers.username);
  const email = normalize(identifiers.email);

  const keysToCheck: string[] = [];
  if (uid) keysToCheck.push(`uid:${uid}`, uid);
  if (uname) keysToCheck.push(`uname:${uname}`, uname);
  if (email) keysToCheck.push(`email:${email}`, email);
  keysToCheck.push("latest");

  return new Promise((resolve) => {
    try {
      const transaction = db.transaction(STORE_NAME, "readonly");
      const store = transaction.objectStore(STORE_NAME);

      let found = false;
      let remaining = keysToCheck.length;

      if (remaining === 0) {
        resolve(undefined);
        return;
      }

      for (const key of keysToCheck) {
        const req = store.get(key);
        req.onsuccess = () => {
          if (!found && req.result && typeof req.result === "string" && req.result.length > 10) {
            found = true;
            const result = req.result;

            // Cache in memory
            for (const k of getCacheKeys(identifiers)) {
              memoryCache.set(k, result);
            }

            // Mirror to localStorage if size allows
            try {
              if (uid) localStorage.setItem(`meryl_avatar_${uid}`, result);
              if (uname) localStorage.setItem(`meryl_avatar_${uname}`, result);
              localStorage.setItem("meryl_avatar_latest", result);
            } catch {
              // Ignore localStorage quota exceeded
            }

            resolve(result);
          }
          remaining--;
          if (remaining <= 0 && !found) {
            resolve(undefined);
          }
        };
        req.onerror = () => {
          remaining--;
          if (remaining <= 0 && !found) {
            resolve(undefined);
          }
        };
      }
    } catch (e) {
      console.warn("IndexedDB read error:", e);
      resolve(undefined);
    }
  });
}

/**
 * Permanently save avatar to memory, localStorage, and IndexedDB.
 * Emits window event "meryl-avatar-updated" for live multi-component updates.
 */
export async function saveStoredAvatar(identifiers: AvatarIdentifiers, avatarDataUrl: string): Promise<void> {
  if (!avatarDataUrl) return;

  const uid = normalize(identifiers.userId);
  const uname = normalize(identifiers.username);
  const email = normalize(identifiers.email);

  // 1. In-memory cache
  for (const k of getCacheKeys(identifiers)) {
    memoryCache.set(k, avatarDataUrl);
  }
  memoryCache.set("latest", avatarDataUrl);

  // 2. localStorage
  if (typeof window !== "undefined") {
    try {
      if (uid) localStorage.setItem(`meryl_avatar_${uid}`, avatarDataUrl);
      if (uname) localStorage.setItem(`meryl_avatar_${uname}`, avatarDataUrl);
      if (email) localStorage.setItem(`meryl_avatar_${email}`, avatarDataUrl);
      localStorage.setItem("meryl_avatar_latest", avatarDataUrl);
    } catch (e) {
      console.warn("localStorage quota exceeded or blocked; relying on IndexedDB for avatar:", e);
    }
  }

  // 3. IndexedDB
  const db = await openDb();
  if (db) {
    try {
      const transaction = db.transaction(STORE_NAME, "readwrite");
      const store = transaction.objectStore(STORE_NAME);

      if (uid) {
        store.put(avatarDataUrl, `uid:${uid}`);
        store.put(avatarDataUrl, uid);
      }
      if (uname) {
        store.put(avatarDataUrl, `uname:${uname}`);
        store.put(avatarDataUrl, uname);
      }
      if (email) {
        store.put(avatarDataUrl, `email:${email}`);
        store.put(avatarDataUrl, email);
      }
      store.put(avatarDataUrl, "latest");
    } catch (e) {
      console.warn("IndexedDB write error:", e);
    }
  }

  // 4. Dispatch custom event for real-time reactivity
  if (typeof window !== "undefined") {
    window.dispatchEvent(
      new CustomEvent("meryl-avatar-updated", {
        detail: {
          avatarUrl: avatarDataUrl,
          userId: identifiers.userId,
          username: identifiers.username,
          email: identifiers.email,
        },
      })
    );
  }
}

/**
 * Remove avatar when user explicitly chooses "Remove Photo".
 */
export async function removeStoredAvatar(identifiers: AvatarIdentifiers): Promise<void> {
  const uid = normalize(identifiers.userId);
  const uname = normalize(identifiers.username);
  const email = normalize(identifiers.email);

  // 1. In-memory cache
  for (const k of getCacheKeys(identifiers)) {
    memoryCache.delete(k);
  }
  memoryCache.delete("latest");

  // 2. localStorage
  if (typeof window !== "undefined") {
    try {
      if (uid) localStorage.removeItem(`meryl_avatar_${uid}`);
      if (uname) localStorage.removeItem(`meryl_avatar_${uname}`);
      if (email) localStorage.removeItem(`meryl_avatar_${email}`);
      localStorage.removeItem("meryl_avatar_latest");
    } catch {
      // Ignore
    }
  }

  // 3. IndexedDB
  const db = await openDb();
  if (db) {
    try {
      const transaction = db.transaction(STORE_NAME, "readwrite");
      const store = transaction.objectStore(STORE_NAME);

      if (uid) {
        store.delete(`uid:${uid}`);
        store.delete(uid);
      }
      if (uname) {
        store.delete(`uname:${uname}`);
        store.delete(uname);
      }
      if (email) {
        store.delete(`email:${email}`);
        store.delete(email);
      }
      store.delete("latest");
    } catch (e) {
      console.warn("IndexedDB delete error:", e);
    }
  }

  // 4. Dispatch custom event
  if (typeof window !== "undefined") {
    window.dispatchEvent(
      new CustomEvent("meryl-avatar-updated", {
        detail: {
          avatarUrl: null,
          userId: identifiers.userId,
          username: identifiers.username,
          email: identifiers.email,
        },
      })
    );
  }
}

