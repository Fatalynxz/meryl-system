/**
 * Persistent Client-Side Receipt Proof Store
 * Ensures uploaded replacement receipt photos are always preserved and displayed,
 * even when Supabase storage buckets or database columns are not configured.
 */

export type StoredReceiptProof = {
  returnId: string;
  salesId?: string;
  name: string;
  url: string; // public URL or base64 data URL
  verifiedAt: string;
};

const DB_NAME = "meryl_receipt_proofs_db";
const DB_VERSION = 1;
const STORE_NAME = "receipt_proofs";
const LOCAL_STORAGE_PREFIX = "meryl_receipt_proof_";

let dbInstance: IDBDatabase | null = null;
const memoryCache = new Map<string, StoredReceiptProof>();

function getIDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    if (typeof window === "undefined" || !window.indexedDB) {
      reject(new Error("IndexedDB is not supported in this environment"));
      return;
    }
    if (dbInstance) {
      resolve(dbInstance);
      return;
    }

    const request = window.indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event: any) => {
      const db = event.target.result as IDBDatabase;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        const store = db.createObjectStore(STORE_NAME, { keyPath: "returnId" });
        store.createIndex("salesId", "salesId", { unique: false });
      }
    };

    request.onsuccess = (event: any) => {
      dbInstance = event.target.result as IDBDatabase;
      resolve(dbInstance);
    };

    request.onerror = () => {
      reject(request.error || new Error("Failed to open IndexedDB"));
    };
  });
}

export async function saveReceiptProof(proof: StoredReceiptProof): Promise<void> {
  if (!proof.returnId) return;

  // 1. Update memory cache
  memoryCache.set(proof.returnId, proof);
  if (proof.salesId) {
    memoryCache.set(`sale_${proof.salesId}`, proof);
  }

  // 2. Save to localStorage (fallback & instant sync)
  try {
    const serialized = JSON.stringify(proof);
    localStorage.setItem(`${LOCAL_STORAGE_PREFIX}${proof.returnId}`, serialized);
    if (proof.salesId) {
      localStorage.setItem(`${LOCAL_STORAGE_PREFIX}sale_${proof.salesId}`, serialized);
    }
  } catch {
    // If localStorage quota exceeded with large base64, proceed to IndexedDB
  }

  // 3. Save to IndexedDB (handles large images easily)
  try {
    const db = await getIDB();
    await new Promise<void>((resolve, reject) => {
      const transaction = db.transaction(STORE_NAME, "readwrite");
      const store = transaction.objectStore(STORE_NAME);
      const req = store.put(proof);
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  } catch (err) {
    console.warn("Failed to save receipt proof to IndexedDB:", err);
  }

  // 4. Dispatch update event
  if (typeof window !== "undefined") {
    window.dispatchEvent(new CustomEvent("receipt-proof-saved", { detail: proof }));
  }
}

export async function getReceiptProof(returnId: string, salesId?: string): Promise<StoredReceiptProof | null> {
  if (!returnId && !salesId) return null;

  // 1. Check memory cache
  if (returnId && memoryCache.has(returnId)) {
    return memoryCache.get(returnId)!;
  }
  if (salesId && memoryCache.has(`sale_${salesId}`)) {
    return memoryCache.get(`sale_${salesId}`)!;
  }

  // 2. Check localStorage
  if (typeof localStorage !== "undefined") {
    if (returnId) {
      const raw = localStorage.getItem(`${LOCAL_STORAGE_PREFIX}${returnId}`);
      if (raw) {
        try {
          const parsed = JSON.parse(raw);
          memoryCache.set(returnId, parsed);
          return parsed;
        } catch {
          // ignore
        }
      }
    }
    if (salesId) {
      const raw = localStorage.getItem(`${LOCAL_STORAGE_PREFIX}sale_${salesId}`);
      if (raw) {
        try {
          const parsed = JSON.parse(raw);
          if (returnId) memoryCache.set(returnId, parsed);
          return parsed;
        } catch {
          // ignore
        }
      }
    }
  }

  // 3. Check IndexedDB
  try {
    const db = await getIDB();
    if (returnId) {
      const fromIdb = await new Promise<StoredReceiptProof | null>((resolve) => {
        const transaction = db.transaction(STORE_NAME, "readonly");
        const store = transaction.objectStore(STORE_NAME);
        const req = store.get(returnId);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => resolve(null);
      });
      if (fromIdb) {
        memoryCache.set(returnId, fromIdb);
        return fromIdb;
      }
    }

    if (salesId) {
      const fromIdbBySale = await new Promise<StoredReceiptProof | null>((resolve) => {
        const transaction = db.transaction(STORE_NAME, "readonly");
        const store = transaction.objectStore(STORE_NAME);
        const index = store.index("salesId");
        const req = index.get(salesId);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => resolve(null);
      });
      if (fromIdbBySale) {
        if (returnId) memoryCache.set(returnId, fromIdbBySale);
        return fromIdbBySale;
      }
    }
  } catch (err) {
    console.warn("Failed to read receipt proof from IndexedDB:", err);
  }

  return null;
}

export async function getAllReceiptProofs(): Promise<Map<string, StoredReceiptProof>> {
  const result = new Map<string, StoredReceiptProof>();

  // 1. From localStorage
  if (typeof localStorage !== "undefined") {
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(LOCAL_STORAGE_PREFIX)) {
        try {
          const item = JSON.parse(localStorage.getItem(key) || "");
          if (item?.returnId) {
            result.set(item.returnId, item);
            if (item.salesId) result.set(`sale_${item.salesId}`, item);
          }
        } catch {
          // ignore
        }
      }
    }
  }

  // 2. From IndexedDB
  try {
    const db = await getIDB();
    await new Promise<void>((resolve) => {
      const transaction = db.transaction(STORE_NAME, "readonly");
      const store = transaction.objectStore(STORE_NAME);
      const req = store.openCursor();
      req.onsuccess = (event: any) => {
        const cursor = event.target.result;
        if (cursor) {
          const val = cursor.value as StoredReceiptProof;
          if (val?.returnId) {
            result.set(val.returnId, val);
            if (val.salesId) result.set(`sale_${val.salesId}`, val);
          }
          cursor.continue();
        } else {
          resolve();
        }
      };
      req.onerror = () => resolve();
    });
  } catch {
    // ignore
  }

  return result;
}

