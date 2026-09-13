// OPFSManager.js - Web Crypto API module for OPFS manipulation
class OPFSManager {
  constructor(maxSizeMB = 512) {
    this.maxSize = maxSizeMB * 1024 * 1024; // Convert MB to bytes
    this.currentSize = 0;
    this.rootDirectory = null;
    this.fileMetadata = new Map(); // Stores { name, size, lastAccessed }
    this.keyPromise = null;
    this.keyName = 'opfs-crypto-key';
  }

  async initialize() {
    try {
      this.rootDirectory = await navigator.storage.getDirectory();
      await this.loadMetadata();
      await this.getKey(); // Initialize the crypto key
      return true;
    } catch (error) {
      console.error('OPFS initialization failed:', error);
      throw error;
    }
  }

  async loadMetadata() {
    try {
      // Load existing file metadata from OPFS
      for await (const [name] of this.rootDirectory.entries()) {
        if (name === '.metadata') continue;
        const fileHandle = await this.rootDirectory.getFileHandle(name);
        const file = await fileHandle.getFile();
        this.fileMetadata.set(name, {
          size: file.size,
          lastAccessed: file.lastModified
        });
        this.currentSize += file.size;
      }
    } catch (error) {
      console.error('Failed to load metadata:', error);
    }
  }

  async getKey() {
    if (this.keyPromise) return this.keyPromise;

    this.keyPromise = (async () => {
      try {
        // Try to retrieve existing key from IndexedDB
        const key = await this.retrieveKeyFromStorage();
        if (key) return key;

        // Generate new key if none exists
        const newKey = await window.crypto.subtle.generateKey(
          {
            name: 'AES-GCM',
            length: 256
          },
          true, // extractable
          ['encrypt', 'decrypt']
        );

        // Store the key
        await this.storeKeyInStorage(newKey);
        return newKey;
      } catch (error) {
        console.error('Key generation/retrieval failed:', error);
        throw error;
      }
    })();

    return this.keyPromise;
  }

  async storeKeyInStorage(key) {
    try {
      const exportedKey = await window.crypto.subtle.exportKey('raw', key);
      const keyBuffer = new Uint8Array(exportedKey);

      // Store in IndexedDB
      const db = await this.openIndexedDB();
      const tx = db.transaction('keys', 'readwrite');
      const store = tx.objectStore('keys');
      await store.put(keyBuffer, this.keyName);
      await tx.done;
    } catch (error) {
      console.error('Failed to store key:', error);
      throw error;
    }
  }

  async retrieveKeyFromStorage() {
    try {
      const db = await this.openIndexedDB();
      const tx = db.transaction('keys', 'readonly');
      const store = tx.objectStore('keys');
      const keyBuffer = await store.get(this.keyName);
      await tx.done;

      if (!keyBuffer) return null;

      return await window.crypto.subtle.importKey(
        'raw',
        keyBuffer,
        { name: 'AES-GCM' },
        true,
        ['encrypt', 'decrypt']
      );
    } catch (error) {
      console.error('Failed to retrieve key:', error);
      return null;
    }
  }

  async openIndexedDB() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('OPFSManagerDB', 1);

      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('keys')) {
          db.createObjectStore('keys');
        }
      };

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async writeFile(name, data) {
    if (!this.rootDirectory) await this.initialize();

    try {
      // Check if we need to evict files
      while (this.currentSize + data.size > this.maxSize) {
        await this.evictOldest();
      }

      // Generate IV
      const iv = window.crypto.getRandomValues(new Uint8Array(12));

      // Get crypto key
      const key = await this.getKey();

      // Encrypt data
      const encryptedData = await window.crypto.subtle.encrypt(
        {
          name: 'AES-GCM',
          iv: iv
        },
        key,
        data
      );

      // Write to OPFS
      const fileHandle = await this.rootDirectory.getFileHandle(name, { create: true });
      const writable = await fileHandle.createWritable();
      await writable.write(iv); // Write IV first
      await writable.write(encryptedData); // Then write encrypted data
      await writable.close();

      // Update metadata
      const fileSize = iv.length + encryptedData.byteLength;
      this.fileMetadata.set(name, {
        size: fileSize,
        lastAccessed: Date.now()
      });
      this.currentSize += fileSize;

      return true;
    } catch (error) {
      console.error('Failed to write file:', error);
      throw error;
    }
  }

  async readFile(name) {
    if (!this.rootDirectory) await this.initialize();

    try {
      const fileHandle = await this.rootDirectory.getFileHandle(name);
      const file = await fileHandle.getFile();

      // Read IV (first 12 bytes) and encrypted data
      const iv = new Uint8Array(await file.slice(0, 12).arrayBuffer());
      const encryptedData = await file.slice(12).arrayBuffer();

      // Get crypto key
      const key = await this.getKey();

      // Decrypt data
      const decryptedData = await window.crypto.subtle.decrypt(
        {
          name: 'AES-GCM',
          iv: iv
        },
        key,
        encryptedData
      );

      // Update last accessed time
      const metadata = this.fileMetadata.get(name);
      if (metadata) {
        metadata.lastAccessed = Date.now();
        this.fileMetadata.set(name, metadata);
      }

      return decryptedData;
    } catch (error) {
      console.error('Failed to read file:', error);
      throw error;
    }
  }

  async evictOldest() {
    try {
      if (this.fileMetadata.size === 0) return false;

      // Find oldest file
      let oldestFile = null;
      let oldestTime = Infinity;

      for (const [name, metadata] of this.fileMetadata.entries()) {
        if (metadata.lastAccessed < oldestTime) {
          oldestTime = metadata.lastAccessed;
          oldestFile = name;
        }
      }

      if (!oldestFile) return false;

      // Delete the file
      await this.rootDirectory.removeEntry(oldestFile);
      const metadata = this.fileMetadata.get(oldestFile);
      this.currentSize -= metadata.size;
      this.fileMetadata.delete(oldestFile);

      return true;
    } catch (error) {
      console.error('Failed to evict file:', error);
      throw error;
    }
  }

  async getStorageStats() {
    return {
      currentSize: this.currentSize,
      maxSize: this.maxSize,
      usedPercentage: (this.currentSize / this.maxSize) * 100,
      fileCount: this.fileMetadata.size
    };
  }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = OPFSManager;
} else if (typeof window !== 'undefined') {
  window.OPFSManager = OPFSManager;
}

  async writeFile(filename, data) {
    try {
      const encryptedData = await this.encryptData(data);
      const fileHandle = await this.rootDirectory.getFileHandle(filename, { create: true });
      const writable = await fileHandle.createWritable();
      await writable.write(encryptedData);
      await writable.close();
      
      // Check storage limits and evict if necessary
      await this.enforceStorageLimits();
    } catch (error) {
      console.error('Failed to write file:', error);
      throw error;
    }
  }

  async readFile(filename) {
    try {
      const fileHandle = await this.rootDirectory.getFileHandle(filename);
      const file = await fileHandle.getFile();
      const encryptedData = new Uint8Array(await file.arrayBuffer());
      return await this.decryptData(encryptedData);
    } catch (error) {
      console.error('Failed to read file:', error);
      throw error;
    }
  }

  async getStorageStats() {
    try {
      let currentSize = 0;
      // Calculate used storage (simplified for testing)
      for await (const entry of this.rootDirectory.values()) {
        if (entry.kind === 'file') {
          const file = await entry.getFile();
          currentSize += file.size;
        }
      }
      
      const usedPercentage = (currentSize / this.storageLimit) * 100;
      return {
        currentSize,
        usedPercentage,
        storageLimit: this.storageLimit
      };
    } catch (error) {
      console.error('Failed to get storage stats:', error);
      throw error;
    }
  }

  async enforceStorageLimits() {
    try {
      const stats = await this.getStorageStats();
      if (stats.usedPercentage > 90) { // Evict if over 90% full
        console.log('Storage limit reached. Evicting oldest files...');
        // Simplified: Evict the oldest file (FIFO)
        for await (const entry of this.rootDirectory.values()) {
          if (entry.kind === 'file') {
            await this.rootDirectory.removeEntry(entry.name);
            console.log(`Evicted file: ${entry.name}`);n            break; // Evict one file at a time
          }
        }
      }
    } catch (error) {
      console.error('Failed to enforce storage limits:', error);
      throw error;
    }
  }
}

export default OPFSManager;