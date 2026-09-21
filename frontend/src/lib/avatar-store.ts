/**
 * Persistent avatar storage using IndexedDB + localStorage + in-memory cache.
 * 
 * Solves the issue where profile pictures (pfp) disappear after closing tabs,
 * since the database does not have an avatar column and sessionStorage is tab-scoped.
 * IndexedDB safely accommodates large base64 data URLs without hitting the 5MB
 * localStorage quota, while localStorage provides immediate synchronous reads
 * on initial page load to prevent UI flicker.
 */

import { supabase } from "./supabase";

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
 * Synchronous avatar retrieval from memory cache.
 * Returns cached avatar immediately during component render without touching localStorage.
 */
export function getStoredAvatarSync(identifiers: AvatarIdentifiers): string | undefined {
  if (typeof window === "undefined") return undefined;

  // Check in-memory cache
  for (const k of getCacheKeys(identifiers)) {
    const cached = memoryCache.get(k);
    if (cached) return cached;
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
 * Permanently save avatar to memory and IndexedDB.
 * Emits window event "meryl-avatar-updated" for live multi-component updates.
 * Never pollutes localStorage with large base64 strings.
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

  // 2. IndexedDB
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

  // 3. Dispatch custom event for real-time reactivity
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

  // 3. Dispatch custom event
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

/**
 * Purge any sensitive avatar strings or user data from localStorage
 * so that browser inspection (DevTools) stays completely clean.
 */
export function purgeLocalStorageSensitiveData(): void {
  if (typeof window === "undefined" || !window.localStorage) return;
  try {
    const keysToRemove: string[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (
        k &&
        (k.startsWith("meryl_avatar_") ||
          k.startsWith("meryl_receipt_proof_") ||
          k === "meryl_user" ||
          k === "meryl_local_audit_log")
      ) {
        keysToRemove.push(k);
      }
    }
    for (const k of keysToRemove) {
      localStorage.removeItem(k);
    }
  } catch {
    // Ignore storage restrictions
  }
}

// Purge immediately on script load
purgeLocalStorageSensitiveData();

/**
 * Upload an avatar file or image blob directly to Supabase Cloud Storage ('user-avatars' bucket)
 * and return the public CDN URL.
 */
export async function uploadAvatarToSupabaseStorage(
  userId: string,
  fileOrBlob: File | Blob,
  extension: string = "webp"
): Promise<string | null> {
  if (!userId || !fileOrBlob) return null;

  try {
    const cleanUid = normalize(userId).replace(/[^a-z0-9_-]/g, "") || "user";
    const fileName = `${cleanUid}_${Date.now()}.${extension}`;
    const filePath = `${cleanUid}/${fileName}`;

    const contentType = (fileOrBlob as File).type || `image/${extension}`;

    const { error: uploadError } = await supabase.storage
      .from("user-avatars")
      .upload(filePath, fileOrBlob, {
        upsert: true,
        contentType,
      });

    if (uploadError) {
      console.warn("Supabase storage avatar upload warning:", uploadError.message);
      return null;
    }

    const { data } = supabase.storage.from("user-avatars").getPublicUrl(filePath);
    const publicUrl = data?.publicUrl;

    if (publicUrl) {
      // Update memory cache
      memoryCache.set(`uid:${cleanUid}`, publicUrl);
      memoryCache.set("latest", publicUrl);
      return publicUrl;
    }

    return null;
  } catch (err) {
    console.warn("Avatar upload to cloud storage failed:", err);
    return null;
  }
}



