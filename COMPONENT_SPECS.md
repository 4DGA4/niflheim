# Component Specifications: Privacy-Preserving Data Poisoning Framework

## 1. Client-Side Poisoning Agent

### 1.1 Core Architecture (All Platforms)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Poisoning Agent Core                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Entropy    │  │  Policy     │  │  Scheduler  │              │
│  │  Manager    │──│  Engine     │──│  (Cron/     │              │
│  │  (HRNG +    │  │  (OPA/Rego) │  │  Event-Driven)│             │
│  │  User Input)│  │             │  │             │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│         │               │               │                         │
│         ▼               ▼               ▼                         │
│  ┌─────────────────────────────────────────────────┐             │
│  │            Pattern Application Layer             │             │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │             │
│  │  │Fingerprint│ │Behavioral│ │ Sensor   │ ...    │             │
│  │  │  Module   │ │  Module  │ │  Module  │        │             │
│  │  └──────────┘ └──────────┘ └──────────┘        │             │
│  └─────────────────────────────────────────────────┘             │
│         │               │               │                         │
│         ▼               ▼               ▼                         │
│  ┌─────────────────────────────────────────────────┐             │
│  │              Platform Adapters                   │             │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │             │
│  │  │ Browser  │ │ Mobile   │ │ Wearable │        │             │
│  │  │  (WASM)  │ │ (FFI)    │ │ (no_std) │        │             │
│  │  └──────────┘ └──────────┘ └──────────┘        │             │
│  └─────────────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Browser Extension (Manifest V3)

**Tech Stack:** Rust → WASM (wasm-bindgen) + TypeScript + WebAssembly System Interface (WASI)

**Components:**

| Module | Responsibility | API Surface |
|--------|---------------|-------------|
| `fp-rotator` | Canvas/WebGL/AudioContext fingerprint synthesis | `rotateFingerprint(config: FPConfig): Promise<FPState>` |
| `bio-noiser` | Keystroke/mouse/scroll timing perturbation | `injectNoise(event: InputEvent): PerturbedEvent` |
| `net-obfuscator` | Request timing, cover traffic, TLS fingerprint | `obfuscateRequest(req: Request): ObfuscatedRequest` |
| `storage` | Encrypted IndexedDB with Web Crypto API | `store(key, value), retrieve(key): Promise<Value>` |
| `sync` | Pattern fetch + verification from distribution | `fetchPatterns(manifest: Manifest): Promise<Patterns>` |

**Permissions (Minimal):**
- `activeTab`, `scripting`, `storage`, `webRequest` (declarativeNetRequest)
- Optional: `background` (service worker), `alarms`

**Content Script Injection Points:**
```typescript
// document_start - before any scripts
// Canvas/WebGL/AudioContext prototype wrapping
// Event listener interception (capture phase)
```

### 1.3 Mobile App (iOS/Android)

**Tech Stack:** Rust core (uniffi/tauri) + Swift (iOS) / Kotlin (Android) FFI

**Components:**

| Module | iOS Framework | Android Library | Responsibility |
|--------|---------------|-----------------|----------------|
| `sensor-noise` | CoreMotion + Accelerate | SensorManager + RenderScript | IMU noise injection preserving physics |
| `location-spoofer` | CoreLocation + MapKit | FusedLocationProvider + Play Services | Synthetic trajectory on road network |
| `audio-jammer` | AVAudioEngine + AudioToolbox | AudioTrack + AudioRecord | Ultrasonic + adversarial perturbation |
| `ble-privacy` | CoreBluetooth | BluetoothLeAdvertiser | MAC rotation, advertising payload noise |
| `keystore` | Secure Enclave (P256) | StrongBox / Keymaster | Key gen, signing, VRF evaluation |

**Background Execution:**
- iOS: BGProcessingTask + CoreLocation "always" (user-granted)
- Android: WorkManager + Foreground Service (location + sensors)

### 1.4 Wearable Integration

**Targets:** 
- Apple Watch (watchOS 10+)
- Wear OS 4+
- Garmin Connect IQ
- Zepp OS (Amazfit)
- Custom: nRF52840 / ESP32-C3 / RP2040 (Zephyr/FreeRTOS)

**Tech Stack:** Rust `no_std` + `embassy` (async) / `rtic` (RTIC)

**Components:**

| Module | Memory Budget | Responsibility |
|--------|---------------|----------------|
| `hrv-noiser` | < 8 KB RAM | RR interval perturbation preserving HRV metrics |
| `sleep-noiser` | < 4 KB RAM | Sleep stage transition noise (circadian preserved) |
| `gait-noiser` | < 6 KB RAM | Step cadence/stride adversarial noise |
| `ble-privacy` | < 4 KB RAM | MAC rotation + advertising interval jitter |
| `pattern-store` | < 16 KB Flash | Compressed pattern buffer (Cbor + zstd) |

**Communication:** BLE GATT (encrypted) + NFC (for pattern load)

### 1.5 Printable Patterns

**Generator:** CLI (Rust) + WASM web tool (no server)

**Pattern Types:**

| Type | Capacity | Use Case | Verification |
|------|----------|----------|--------------|
| QR Code (v40-L) | 2,953 bytes | Laptop lid, phone case | Camera scan + signature verify |
| DataMatrix (ECC200) | 3,116 bytes | Badge, sticker | Industrial scanner compatible |
| PDF417 | 1,850 bytes | ID card form factor | High density, error correction |
| IR/UV Ink | ~500 bytes | Covert channel | Spectral camera / phone + filter |
| DNA Storage (future) | ~200 MB/g | Long-term archival | Sequencing + decode |

**Encoding:** 
```
Pattern = CBOR({
  version: 1,
  pattern_type: "fingerprint" | "behavioral" | "location" | ...,
  payload: bytes,
  signature: Ed25519(signing_key, payload),
  manifest_hash: BLAKE3(manifest),
  expires: UnixTimestamp,
  metadata: { entropy_bits: u16, dp_epsilon: f32 }
})
```

---

## 2. Pattern Generation Service

### 2.1 Service Architecture (Federated, Stateless Workers)

```
┌────────────────────────────────────────────────────────────────┐
│                  Pattern Generation Cluster                     │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Worker 1    │    │  Worker 2    │    │  Worker N    │      │
│  │  (Region A)  │    │  (Region B)  │    │  (Region N)  │      │
│  ├──────────────┤    ├──────────────┤    ├──────────────┤      │
│  │ PE_FP        │    │ PE_FP        │    │ PE_FP        │      │
│  │ PE_BEHAVIOR  │    │ PE_BEHAVIOR  │    │ PE_BEHAVIOR  │      │
│  │ PE_LOC       │    │ PE_LOC       │    │ PE_LOC       │      │
│  │ PE_SENSOR    │    │ PE_SENSOR    │    │ PE_SENSOR    │      │
│  │ PE_AUDIO     │    │ PE_AUDIO     │    │ PE_AUDIO     │      │
│  │ PE_GENOMIC   │    │ PE_GENOMIC   │    │ PE_GENOMIC   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                   │                │
│         └───────────────────┼───────────────────┘                │
│                             ▼                                    │
│              ┌──────────────────────────────┐                    │
│              │      Consensus Layer          │                    │
│              │  (Tendermint Light / BFT)    │                    │
│              │  - Pattern manifest ordering │                    │
│              │  - State replication (CRDT)  │                    │
│              └──────────────────────────────┘                    │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐                │
│         ▼                   ▼                   ▼                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  IPFS       │    │  P2P        │    │  Web/CDN    │         │
│  │  Cluster    │    │  GossipSub  │    │  Mirror     │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 Pattern Engines Detail

#### 2.2.1 Fingerprint Engine (`PE_FP`)
- **Model:** StyleGAN-3-T (transfer learned on fingerprint manifold)
- **Input:** User FP embedding (256-dim, from local calibration)
- **Output:** Synthetic FP parameters (canvas, WebGL, audio, fonts, battery)
- **DP:** Gaussian mechanism on latent space (ε=0.5, δ=10⁻⁵)
- **Latency:** < 50ms p99 (GPU), < 200ms p99 (CPU/WASM)

#### 2.2.2 Behavioral Engine (`PE_BEHAVIOR`)
- **Model:** Transformer Seq2Seq (6-layer, 8-head, d_model=512)
- **Input:** User behavioral sequence (keystroke, mouse, scroll, timing)
- **Output:** Perturbed sequence preserving high-level semantics
- **Calibration:** Few-shot (5-10 sessions) via ZK-proof of local stats
- **DP:** RDP accountant (ε=1.0 per day)

#### 2.2.3 Location Engine (`PE_LOC`)
- **Model:** Physics-informed Neural Markov Chain + Road Network Graph
- **Input:** Home/work anchors (encrypted), mobility radius
- **Output:** Synthetic trajectory (lat, lon, timestamp, accuracy, velocity)
- **Constraints:** Road adherence, velocity limits, dwell time realism
- **DP:** Geo-indistinguishability (ε=0.5, planar Laplace)

#### 2.2.4 Sensor Engine (`PE_SENSOR`)
- **Model:** Physics-Informed Neural Network (PINN) for IMU/GNSS
- **Input:** Activity label + device calibration params
- **Output:** Synthetic accel/gyro/mag/baro streams
- **Validation:** Zero-velocity update (ZUPT) consistency, Allan variance match

#### 2.2.5 Audio Engine (`PE_AUDIO`)
- **Model:** PGD adversarial perturbation + Perceptual Loss (LPIPS-audio)
- **Input:** Hotword trigger audio + ambient noise profile
- **Output:** Jamming signal (ultrasonic + adversarial) + perturbed hotword
- **Constraints:** < -20 dB perceptual threshold, < 1% false reject

#### 2.2.6 Genomic Engine (`PE_GENOMIC`)
- **Model:** Conditional VAE on 1000 Genomes + gnomAD
- **Input:** User's known variants (encrypted, local-only)
- **Output:** Synthetic variant set preserving HWE, LD, allele frequencies
- **Privacy:** No raw genomic data leaves device; only encrypted embedding

### 2.3 Personalization Layer

**Local Profile Embedding:**
```rust
struct LocalProfile {
    // Never leaves device
    fingerprint_embedding: [f32; 256],      // CLIP-style multimodal
    behavioral_embedding: [f32; 512],       // Transformer CLS token
    location_anchors: Encrypted<Vec<GeoAnchor>>,
    sensor_calibration: SensorCalibration,
    audio_profile: AudioProfile,
    genomic_embedding: Option<[f32; 128]>,  // Opt-in only
}
```

**Calibration Protocol (Zero-Knowledge):**
```
User                    Service
  │                        │
  ├─ Commit(embedding) ───►│
  │                        │
  │◄── Challenge(nonce) ───┤
  │                        │
  ├─ ZKProof(stats) ──────►│  // Proves embedding properties
  │                        │  // without revealing values
  │◄── Calibrated Params ──┤
```

---

## 3. Distribution Mechanism

### 3.1 Channel Specifications

| Channel | Latency | Bandwidth | Anonymity | Availability | Use Case |
|---------|---------|-----------|-----------|--------------|----------|
| IPFS/IPNS | ~1-5s | High | High (DHT) | High | Primary digital |
| Libp2p GossipSub | ~100-500ms | Medium | High (mesh) | High | Real-time updates |
| DoH (Domain Fronting) | ~50-200ms | Low | Medium | High | Censorship resistance |
| Tor Onion v3 | ~2-10s | Low | Very High | Medium | High-threat users |
| Static Web/CDN | ~100-500ms | High | Low | Very High | Bootstrapping |
| QR/NFC | Manual | ~3 KB | Physical | Manual | Air-gap / bootstrap |
| LoRaWAN/Meshtastic | ~1-30s | ~50 bytes | High | Low infra | Off-grid / protest |
| UWB/BLE Beacon | ~100ms | ~1 KB | Proximity | Local | Peer-to-peer nearby |

### 3.2 Manifest Format

```json
{
  "version": 2,
  "manifest_id": "b3sum:...",
  "timestamp": 1700000000,
  "expires": 1700086400,
  "patterns": [
    {
      "pattern_id": "fp_v1_abc123",
      "type": "fingerprint",
      "version": 1,
      "cid": "bafybei...",           // IPFS CIDv1
      "size": 12450,
      "hash": "b3sum:...",
      "signature": "ed25519:...",
      "dp_epsilon": 0.5,
      "target_platforms": ["browser", "mobile"],
      "priority": "high"
    }
  ],
  "distribution": {
    "ipns_key": "k51qzi...",
    "gossipsub_topic": "/poisoning/patterns/v2",
    "tor_onion": "abc123.onion",
    "cdn_urls": ["https://cdn1.example/patterns/", "https://cdn2.example/patterns/"],
    "dns_txt_domain": "patterns.poisoning.example"
  },
  "verification": {
    "transparency_log": "ctlog.poisoning.example",
    "merkle_root": "b3sum:...",
    "attestation_policy": "tee_quote_required"
  }
}
```

### 3.3 Verification Pipeline

```
Received Pattern
       │
       ▼
┌──────────────────┐
│  Signature Check │── Ed25519 verify (offline public key)
│  (Ed25519)       │
└────────┬─────────┘
         │ Valid
         ▼
┌──────────────────┐
│  Merkle Proof    │── Inclusion in manifest Merkle tree
│  Verification    │
└────────┬─────────┘
         │ Valid
         ▼
┌──────────────────┐
│  Transparency    │── Check CT log for manifest inclusion
│  Log Check       │
└────────┬─────────┘
         │ Valid
         ▼
┌──────────────────┐
│  TEE Attestation │── Verify pattern generated in genuine TEE
│  (Optional)      │   (AWS Nitro / AMD SEV / Intel SGX / Apple SE)
└────────┬─────────┘
         │ Valid
         ▼
   ACCEPT PATTERN
```

---

## 4. Effectiveness Monitoring

### 4.1 Local Metrics Collection

```rust
struct LocalMetrics {
    // Fingerprint entropy (bits)
    fp_entropy: EntropyMetrics {
        shannon: f64,
        min_entropy: f64,
        collision_rate: f64,
    },
    
    // Linkage resistance
    linkage: LinkageMetrics {
        k_anonymity: u32,
        l_diversity: f64,
        t_closeness: f64,
        reid_success_rate: f64,  // Estimated via shadow modeling
    },
    
    // Model degradation (shadow models)
    model_degradation: ModelMetrics {
        baseline_accuracy: f64,
        poisoned_accuracy: f64,
        auc_drop: f64,
        calibration_error: f64,
    },
    
    // Noise quality
    noise_quality: NoiseMetrics {
        psnr_db: f64,
        ssim: f64,
        lpips: f64,
        perceptual_threshold_violations: u32,
    },
    
    // Operational
    operational: OperationalMetrics {
        patterns_active: u32,
        patterns_expired: u32,
        fetch_success_rate: f64,
        verification_failure_rate: f64,
        battery_impact_pct: f64,
        cpu_impact_pct: f64,
    },
}
```

### 4.2 Privacy-Preserving Aggregation

**Two-Tier Architecture:**

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Device    │────►│  Local Aggregator│────►│  Shuffle/Mixnet │
│  (TEE)      │     │  (Secure Enclave)│     │  (Erasure Code) │
└─────────────┘     └────────┬─────────┘     └────────┬────────┘
                             │                        │
                             ▼                        ▼
                      ┌─────────────┐          ┌─────────────┐
                      │ DP Noise    │          │  Aggregator │
                      │ (Gaussian)  │          │  (Untrusted)│
                      │ ε=0.1/day   │          └──────┬──────┘
                      └─────────────┘                 │
                                                      ▼
                                            ┌─────────────────┐
                                            │  Global Stats   │
                                            │  (Public Dash)  │
                                            └─────────────────┘
```

**Differential Privacy Parameters:**
- Per-metric ε = 0.1 per day (advanced composition: ε_total ≈ 0.3/day)
- δ = 10⁻⁶
- Gaussian mechanism with σ = √(2ln(1.25/δ)) / ε ≈ 12.7
- Clipping bounds per metric (prevent outlier influence)

### 4.3 Feedback Loop

**Adaptation Algorithm:**
```python
# Contextual Bandit (LinUCB) for pattern selection
class PatternBandit:
    def __init__(self, d=128, alpha=0.5):
        self.A = {arm: np.eye(d) for arm in PATTERN_TYPES}
        self.b = {arm: np.zeros(d) for arm in PATTERN_TYPES}
        self.alpha = alpha
    
    def select(self, context: np.ndarray) -> PatternType:
        # context = [fp_entropy, linkage_k, model_auc, battery, ...]
        scores = {}
        for arm in PATTERN_TYPES:
            A_inv = np.linalg.inv(self.A[arm])
            theta = A_inv @ self.b[arm]
            p = theta @ context + self.alpha * np.sqrt(context @ A_inv @ context)
            scores[arm] = p
        return max(scores, key=scores.get)
    
    def update(self, arm: PatternType, context: np.ndarray, reward: float):
        self.A[arm] += np.outer(context, context)
        self.b[arm] += reward * context
```

**Reward Signal:** `- (linkage_reid_rate * 10 + model_accuracy * 5 + battery_pct * 0.1)`

---

## 5. Cross-Cutting Concerns

### 5.1 Key Management

```
┌────────────────────────────────────────────────────────────┐
│                    Key Hierarchy                              │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Master Seed (32 bytes, HRNG + User Entropy)               │
│  │  Stored: TEE / Secure Enclave / Encrypted File          │
│  │  Backup: Shamir Secret Sharing (3-of-5, paper QR)       │
│  ▼                                                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ HKDF-SHA256(master_seed, "poisoning_framework_v1")   │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│        ┌──────────────────┼──────────────────┐             │
│        ▼                  ▼                  ▼             │
│  ┌───────────┐      ┌───────────┐      ┌───────────┐      │
│  │ Identity  │      │ Signing   │      │ VRF       │      │
│  │ Key       │      │ Key       │      │ Key       │      │
│  │ (Ed25519) │      │ (Ed25519) │      │ (ECVRF)   │      │
│  │           │      │           │      │           │      │
│  │ Pseudonym │      │ Patterns  │      │ Anonymous │      │
│  │ for Svc   │      │ & Manifest│      │ Auth      │      │
│  └───────────┘      └───────────┘      └───────────┘      │
│                                                             │
│  Rotation: Identity (90 days), Signing (30 days),         │
│            VRF (per-session), Pattern keys (per-pattern)  │
└────────────────────────────────────────────────────────────┘
```

### 5.2 Update Mechanism

**Reproducible Builds + Binary Transparency:**
1. Source → `cargo build --release` (pinned dependencies, `Cargo.lock`)
2. Build in hermetic container (Nix/Guix/Bazel)
3. Multiple independent builders → compare hashes
4. Sign with threshold sig (3-of-5 maintainer keys)
5. Publish to transparency log (CT-style)
6. Client verifies: hash match + sig threshold + log inclusion

**Auto-Update Policy:**
- User consent required (no silent updates)
- Staged rollout (1% → 10% → 100% over 14 days)
- Rollback via signed manifest
- Delta updates (bsdiff) for bandwidth

### 5.3 Stealth / Anti-Analysis

| Technique | Implementation |
|-----------|----------------|
| **Timing Obfuscation** | Jittered execution (exponential backoff + noise) |
| **Control Flow Flattening** | LLVM obfuscation passes (Obfuscator-LLVM) |
| **String Encryption** | Compile-time XOR + runtime decrypt |
| **Anti-Debug/VM** | Timing checks, CPUID, hardware breakpoints detection |
| **Steganographic Patterns** | LSB embedding in legitimate traffic/images |
| **Domain Fronting** | CloudFront/Cloudflare Workers + SNI mismatch |
| **Traffic Morphing** | Mimic popular app TLS fingerprints (Chrome, WhatsApp) |

---

## 6. Resource Budgets

| Platform | CPU (idle) | CPU (active) | RAM | Battery/Day | Storage |
|----------|------------|--------------|-----|-------------|---------|
| Browser Ext | < 0.1% | < 2% | < 10 MB | < 1% | < 50 MB |
| Mobile | < 0.5% | < 5% | < 30 MB | < 3% | < 100 MB |
| Wearable | < 1% | < 3% | < 8 KB | < 5% | < 64 KB |
| Printable | N/A | N/A | N/A | N/A | ~3 KB/pattern |

---

## 7. Formal Verification Targets

| Component | Method | Properties |
|-----------|--------|------------|
| Key Derivation | F* / KreMLin | Correctness, side-channel resistance |
| VRF Evaluation | Coq | Uniqueness, pseudorandomness |
| DP Mechanism | EasyCrypt | (ε,δ)-DP proof |
| Merkle Verification | Rust + Prusti | Memory safety, correctness |
| Pattern Application | TLA+ | No interference, ordering |
| Secure Aggregation | ProVerif | Secrecy, authentication |