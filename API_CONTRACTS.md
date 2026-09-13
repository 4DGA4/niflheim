# API Contracts: Privacy-Preserving Data Poisoning Framework

## 1. Client ↔ Pattern Generation Service

### 1.1 Authentication & Identity

**Anonymous Pseudonymous Authentication (VRF-based)**

```http
POST /v1/auth/challenge
Content-Type: application/json

{
  "client_epoch": 1700000000,
  "platform": "browser" | "mobile" | "wearable" | "printable",
  "client_version": "1.2.3",
  "capabilities": ["fp", "behavioral", "location", "sensor", "audio", "genomic"]
}

Response: 200 OK
{
  "challenge": "base64url(32_bytes)",
  "epoch": 1700000000,
  "difficulty": 16,  // PoW leading zero bits
  "vrf_public_key": "base64url(32_bytes)"  // Service's VRF key
}
```

```http
POST /v1/auth/response
Content-Type: application/json

{
  "challenge": "base64url(32_bytes)",
  "vrf_proof": "base64url(80_bytes)",  // ECVRF proof
  "vrf_output": "base64url(32_bytes)", // Pseudonym for this epoch
  "pow_nonce": "base64url(8_bytes)",
  "client_attestation": "base64url(...)" // Optional: TEE quote
}

Response: 200 OK
{
  "session_token": "base64url(32_bytes)", // Encrypted session key
  "token_expires": 1700086400,
  "rate_limit": {
    "requests_per_hour": 100,
    "patterns_per_day": 50
  },
  "service_manifest_cid": "bafybei..."  // Current manifest CID
}
```

**VRF Construction (ECVRF-P256-SHA256):**
- `vrf_sk`: Client's long-term VRF secret key (stored in TEE)
- `vrf_pk`: Derived from `vrf_sk`, registered during onboarding (anonymous)
- `pseudonym = VRF_prove(vrf_sk, "epoch:" || epoch || ":" || challenge)`
- Service verifies: `VRF_verify(vrf_pk, input, proof, output)`
- Unlinkable across epochs (new challenge each epoch)

### 1.2 Pattern Request

```http
POST /v1/patterns/request
Authorization: Bearer <session_token>
Content-Type: application/json

{
  "request_id": "uuid-v4",
  "pattern_types": ["fingerprint", "behavioral", "location"],
  "constraints": {
    "fingerprint": {
      "target_entropy_bits": 48,
      "dp_epsilon": 0.5,
      "platforms": ["chrome", "firefox", "safari"],
      "exclude": ["webgl_vendor", "audio_fingerprint"]  // Optional
    },
    "behavioral": {
      "session_length_min": 30,
      "action_types": ["keystroke", "mouse", "scroll"],
      "dp_epsilon": 1.0,
      "calibration_proof": "base64url(zk_proof)"  // Optional
    },
    "location": {
      "mobility_radius_km": 50,
      "anchor_count": 2,  // Home, work (encrypted)
      "dp_epsilon": 0.5,
      "road_network": "osm" | "google" | "custom"
    }
  },
  "delivery": {
    "channels": ["ipfs", "gossipsub", "cdn"],
    "max_latency_ms": 5000,
    "offline_acceptable": false
  },
  "client_context": {
    "battery_level": 0.85,
    "network_type": "wifi" | "cellular" | "ethernet",
    "cpu_budget_pct": 5
  }
}

Response: 202 Accepted
{
  "request_id": "uuid-v4",
  "status": "processing" | "queued" | "ready",
  "estimated_ready_ms": 1200,
  "poll_url": "/v1/patterns/request/uuid-v4/status",
  "websocket_url": "wss://api.poisoning.example/v1/patterns/uuid-v4/ws"
}
```

### 1.3 Pattern Retrieval

```http
GET /v1/patterns/request/{request_id}/status
Authorization: Bearer <session_token>

Response: 200 OK
{
  "request_id": "uuid-v4",
  "status": "ready",
  "patterns": [
    {
      "pattern_id": "fp_v1_abc123",
      "type": "fingerprint",
      "version": 1,
      "cid": "bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi",
      "size_bytes": 12450,
      "hash": "b3sum:0123456789abcdef...",
      "signature": "ed25519:base64url(64_bytes)",
      "dp_epsilon": 0.5,
      "expires": 1700086400,
      "metadata": {
        "entropy_bits": 52,
        "generation_ms": 45,
        "model_version": "stylegan3-t-v1.2"
      }
    }
  ],
  "manifest": {
    "cid": "bafybei...",
    "merkle_root": "b3sum:...",
    "signature": "ed25519:...",
    "transparency_log_inclusion": "base64url(...)"
  }
}
```

### 1.4 Pattern Delivery (Alternative: WebSocket Push)

```websocket
wss://api.poisoning.example/v1/patterns/{request_id}/ws
Authorization: Bearer <session_token>

# Server → Client messages:
{"type": "progress", "stage": "generating", "progress_pct": 45}
{"type": "progress", "stage": "signing", "progress_pct": 90}
{"type": "ready", "patterns": [...], "manifest": {...}}
{"type": "error", "code": "RATE_LIMITED", "retry_after_ms": 3600000}
```

### 1.5 Manifest Fetch (For Offline/Printable)

```http
GET /v1/manifest/latest
If-None-Match: "etag-value"

Response: 200 OK
ETag: "b3sum:..."
Content-Type: application/json

{
  "version": 2,
  "manifest_id": "b3sum:...",
  "timestamp": 1700000000,
  "expires": 1700086400,
  "patterns": [...],  // Full pattern list (see Distribution spec)
  "distribution": {...},
  "verification": {...}
}

Response: 304 Not Modified (if unchanged)
```

---

## 2. Client ↔ Distribution Channels

### 2.1 IPFS/IPNS

```bash
# Fetch manifest via IPNS
ipfs name resolve /ipns/k51qzi... --timeout=10s

# Fetch pattern by CID
ipfs get /ipfs/bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi -o pattern.fp.bin

# PubSub subscription for real-time updates
ipfs pubsub sub /poisoning/patterns/v2
```

**Message Format (GossipSub):**
```protobuf
message PatternAnnouncement {
  string manifest_cid = 1;
  uint64 timestamp = 2;
  repeated PatternRef patterns = 3;
  bytes signature = 4;  // Ed25519 over manifest_cid + timestamp
}

message PatternRef {
  string pattern_id = 1;
  string cid = 2;
  PatternType type = 3;
  uint32 size = 4;
  bytes hash = 5;  // BLAKE3
}
```

### 2.2 DNS-over-HTTPS (Domain Fronting)

```http
GET https://cdn-front.example/dns-query?name=patterns.poisoning.example&type=TXT
Accept: application/dns-json

Response: 200 OK
{
  "Status": 0,
  "Answer": [
    {
      "name": "patterns.poisoning.example",
      "type": 16,  // TXT
      "TTL": 300,
      "data": "\"v=2 manifest=bafybei... sig=ed25519:...\""
    }
  ]
}
```

### 2.3 Tor Onion Service

```bash
# Hidden service descriptor (v3)
# Address: abc123def456.onion

# Client connects via Tor SOCKS5
# GET http://abc123def456.onion/v1/manifest/latest
# GET http://abc123def456.onion/v1/patterns/{cid}
```

### 2.4 Static CDN (Bootstrap)

```http
GET https://cdn.poisoning.example/patterns/v2/manifest.json
GET https://cdn.poisoning.example/patterns/v2/{pattern_id}.bin

# Headers for verification
ETag: "b3sum:..."
X-Content-SHA256: "base64url(...)"
X-Signature-Ed25519: "base64url(...)"
X-Manifest-CID: "bafybei..."
```

---

## 3. Pattern Binary Formats

### 3.1 Fingerprint Pattern

```cbor
{
  "version": 1,
  "type": "fingerprint",
  "canvas": {
    "noise_seed": "h'0123456789abcdef'",
    "parameters": {
      "noise_type": "perlin" | "simplex" | "gaussian",
      "octaves": 4,
      "persistence": 0.5,
      "scale": 0.02
    },
    "webgl": {
      "vendor_spoof": "Intel Inc.",
      "renderer_spoof": "Intel Iris OpenGL Engine",
      "version_spoof": "WebGL 2.0 (OpenGL ES 3.0 Chromium)",
      "shading_language_spoof": "WebGL GLSL ES 3.00",
      "extensions": ["EXT_float_blend", "OES_texture_float_linear", ...]
    },
    "audio": {
      "latency_hint": 0.01,
      "sample_rate": 48000,
      "channel_count": 2,
      "fingerprint_noise": "h'...'"  // 256 bytes
    },
    "fonts": {
      "local_fonts": ["Arial", "Helvetica", "Times New Roman", ...],
      "measure_noise": "h'...'"  // 128 bytes
    },
    "battery": {
      "level_noise": 0.02,  // ±2%
      "charging_noise": 0.1  // 10% chance flip
    }
  },
  "signature": "h'...'",  // Ed25519
  "dp_epsilon": 0.5
}
```

### 3.2 Behavioral Pattern

```cbor
{
  "version": 1,
  "type": "behavioral",
  "keystroke": {
    "model": "transformer_seq2seq",
    "parameters": {
      "latent_dim": 256,
      "temperature": 0.8,
      "top_k": 50,
      "dp_noise_scale": 0.15
    },
    "calibration": {
      "hold_latency_mean": 85.2,
      "hold_latency_std": 23.1,
      "flight_latency_mean": 112.7,
      "flight_latency_std": 45.3
    }
  },
  "mouse": {
    "model": "lstm_vae",
    "parameters": {
      "hidden_dim": 128,
      "latent_dim": 64,
      "dp_noise_scale": 0.1
    },
    "calibration": {
      "velocity_mean": 850,
      "velocity_std": 320,
      "acceleration_mean": 2100,
      "acceleration_std": 1800
    }
  },
  "scroll": {
    "model": "markov_chain",
    "states": 16,
    "transition_matrix": [[...]],
    "dp_noise_scale": 0.05
  },
  "signature": "h'...'",
  "dp_epsilon": 1.0
}
```

### 3.3 Location Pattern

```cbor
{
  "version": 1,
  "type": "location",
  "trajectory": {
    "model": "physics_informed_markov",
    "road_network": "osm",
    "anchors_encrypted": "h'...'",  // Age-encrypted (X25519)
    "parameters": {
      "mobility_radius_km": 50,
      "max_velocity_kmh": 120,
      "dwell_time_dist": "lognormal",
      "dp_epsilon": 0.5,
      "geo_indistinguishability": true
    },
    "schedule": {
      "work_hours": "09:00-17:00",
      "timezone": "America/New_York",
      "weekend_variance": 0.3
    }
  },
  "wifi_ble": {
    "ap_mac_rotation_interval_sec": 300,
    "ble_mac_rotation_interval_sec": 60,
    "rssi_noise_db": 3
  },
  "signature": "h'...'",
  "dp_epsilon": 0.5
}
```

### 3.4 Sensor Pattern

```cbor
{
  "version": 1,
  "type": "sensor",
  "imu": {
    "model": "pinn_imu",
    "sampling_rate_hz": 100,
    "parameters": {
      "accel_noise_density": 0.001,  // m/s²/√Hz
      "gyro_noise_density": 0.0001,  // rad/s/√Hz
      "bias_instability_accel": 0.0001,
      "bias_instability_gyro": 0.00001,
      "gravity_vector": [0, 0, -9.81]
    },
    "activities": {
      "walking": { "cadence_range": [90, 130], "stride_variance": 0.05 },
      "running": { "cadence_range": [150, 190], "stride_variance": 0.08 },
      "stationary": { "zupt_threshold": 0.01 }
    }
  },
  "gnss": {
    "model": "pinn_gnss",
    "parameters": {
      "horizontal_accuracy_m": 3.0,
      "vertical_accuracy_m": 5.0,
      "velocity_accuracy_mps": 0.1,
      "multipath_model": "urban_canyon"
    }
  },
  "barometer": {
    "noise_pa": 0.5,
    "drift_pa_per_hour": 1.0
  },
  "signature": "h'...'",
  "dp_epsilon": 0.3
}
```

### 3.5 Audio Pattern

```cbor
{
  "version": 1,
  "type": "audio",
  "hotword_jamming": {
    "model": "pgd_perceptual",
    "target_phrases": ["hey siri", "ok google", "alexa"],
    "parameters": {
      "epsilon": 0.01,  // L∞ bound
      "iterations": 10,
      "step_size": 0.001,
      "perceptual_weight": 1.0
    },
    "ultrasonic_carrier": {
      "frequency_hz": 19500,
      "modulation": "ofdm",
      "symbol_rate": 4800
    }
  },
  "ambient_perturbation": {
    "model": "diffusion",
    "snr_db": 20,
    "frequency_masking": true
  },
  "signature": "h'...'",
  "dp_epsilon": 0.2
}
```

---

## 4. Monitoring & Telemetry API (Local-First)

### 4.1 Local Metrics Submission (Optional, User-Consented)

```http
POST /v1/telemetry/metrics
Authorization: Bearer <session_token>
Content-Type: application/json
X-DP-Epsilon: 0.1

{
  "epoch": 1700000000,
  "metrics": {
    "fp_entropy": { "shannon": 52.3, "min_entropy": 48.1, "collision_rate": 0.0001 },
    "linkage": { "k_anonymity": 1247, "l_diversity": 0.89, "reid_success_rate": 0.003 },
    "model_degradation": { "baseline_accuracy": 0.94, "poisoned_accuracy": 0.71, "auc_drop": 0.18 },
    "noise_quality": { "psnr_db": 28.5, "ssim": 0.92, "lpips": 0.08 },
    "operational": { "patterns_active": 12, "fetch_success_rate": 0.98, "battery_impact_pct": 1.2 }
  },
  "dp_noise": {
    "mechanism": "gaussian",
    "sigma": 12.7,
    "clipped": true
  },
  "client_proof": "base64url(zk_proof_of_honest_computation)"  // Optional
}

Response: 202 Accepted
{
  "accepted": true,
  "aggregation_round": 1700000000
}
```

### 4.2 Aggregated Statistics Retrieval (Public)

```http
GET /v1/telemetry/aggregated?window=24h&metrics=fp_entropy,linkage,model_degradation

Response: 200 OK
{
  "window_start": 1699913600,
  "window_end": 1700000000,
  "participant_count": 124538,  // DP-noised
  "metrics": {
    "fp_entropy": {
      "mean": 49.2,
      "median": 48.7,
      "p25": 45.1,
      "p75": 53.4,
      "dp_noised": true
    },
    "linkage": {
      "mean_k_anonymity": 892,
      "median_reid_rate": 0.0041,
      "dp_noised": true
    },
    "model_degradation": {
      "mean_auc_drop": 0.15,
      "median_accuracy_drop": 0.19,
      "dp_noised": true
    }
  },
  "transparency_log": "ctlog.poisoning.example/2024/01/15"
}
```

---

## 5. Federation API (Service-to-Service)

### 5.1 Service Discovery

```http
GET /.well-known/poisoning-federation.json

Response: 200 OK
{
  "version": 1,
  "service_id": "poisoning-us-east-1",
  "public_key": "ed25519:base64url(32_bytes)",
  "vrf_public_key": "ecvrf:base64url(32_bytes)",
  "endpoints": {
    "api": "https://api-us-east-1.poisoning.example",
    "ipfs": "/ip4/1.2.3.4/tcp/4001/p2p/12D3KooW...",
    "gossipsub": "/ip4/1.2.3.4/tcp/4002/p2p/12D3KooW...",
    "tor": "abc123def456.onion",
    "cdn": "https://cdn-us-east-1.poisoning.example"
  },
  "regions": ["us-east", "us-west", "eu-central"],
  "capabilities": ["fp", "behavioral", "location", "sensor", "audio", "genomic"],
  "consensus": {
    "type": "tendermint_light",
    "validators": [
      {"address": "12D3KooW...", "power": 100, "region": "us-east"},
      {"address": "12D3KooW...", "power": 100, "region": "eu-central"},
      {"address": "12D3KooW...", "power": 100, "region": "ap-southeast"}
    ]
  },
  "policy": {
    "min_dp_epsilon": 0.1,
    "max_patterns_per_user_per_day": 100,
    "allowed_platforms": ["browser", "mobile", "wearable", "printable"]
  }
}
```

### 5.2 Consensus: Manifest Proposal

```http
POST /v1/federation/manifest/propose
Content-Type: application/json
Authorization: Bearer <validator_token>

{
  "proposal_id": "uuid-v4",
  "proposer": "12D3KooW...",
  "manifest": { ... },  // Full manifest (see Distribution spec)
  "prev_manifest_cid": "bafybei...",
  "justification": "Scheduled rotation + 3 new pattern engines",
  "signature": "ed25519:base64url(64_bytes)"
}

Response: 202 Accepted
{
  "proposal_id": "uuid-v4",
  "status": "proposed",
  "voting_power": 300,
  "quorum_required": 201
}
```

### 5.3 Consensus: Vote

```http
POST /v1/federation/manifest/vote
Content-Type: application/json
Authorization: Bearer <validator_token>

{
  "proposal_id": "uuid-v4",
  "vote": "yes" | "no" | "abstain",
  "validator": "12D3KooW...",
  "signature": "ed25519:base64url(64_bytes)"
}
```

### 5.4 State Sync (CRDT)

```http
POST /v1/federation/sync
Content-Type: application/json

{
  "peer_id": "12D3KooW...",
  "vector_clock": {
    "poisoning-us-east-1": 1452,
    "poisoning-eu-central": 1449,
    "poisoning-ap-southeast": 1447
  },
  "delta": {
    "patterns": [...],  // New/updated patterns
    "manifest": {...},  // Latest manifest
    "revocations": ["fp_v1_old1", "behav_v1_old2"]
  }
}

Response: 200 OK
{
  "merged_clock": {...},
  "acknowledged": true
}
```

---

## 6. Printable Pattern API (Offline Generation)

### 6.1 Local Generation (WASM/CLI)

```rust
// WASM exports for web tool
#[wasm_bindgen]
pub fn generate_printable_pattern(
    pattern_type: &str,
    entropy_bits: u16,
    dp_epsilon: f32,
    user_seed: &[u8; 32],  // From user entropy
    master_key: &[u8; 32]  // Derived from master seed
) -> Result<PrintablePattern, JsValue>;

#[wasm_bindgen]
pub fn encode_qr_code(pattern: &PrintablePattern) -> Vec<u8>;  // PNG bytes

#[wasm_bindgen]
pub fn encode_datamatrix(pattern: &PrintablePattern) -> Vec<u8>;

#[wasm_bindgen]
pub fn verify_pattern(qr_bytes: &[u8], master_key: &[u8; 32]) -> Result<VerifiedPattern, JsValue>;
```

### 6.2 Printable Pattern Structure

```json
{
  "version": 1,
  "format": "qr_v40_l" | "datamatrix_ecc200" | "pdf417",
  "payload": {
    "pattern_type": "fingerprint",
    "pattern_data": "base64url(cbor_pattern)",
    "expires": 1700086400,
    "manifest_hash": "b3sum:...",
    "entropy_bits": 64
  },
  "signature": "ed25519:base64url(64_bytes)",
  "human_readable": "POISON-FP-64B-20240115-ABC123"
}
```

---

## 7. Error Codes

| Code | HTTP | Meaning | Retryable |
|------|------|---------|-----------|
| `INVALID_VRF_PROOF` | 401 | VRF verification failed | No |
| `CHALLENGE_EXPIRED` | 401 | Challenge timestamp too old | Yes (new challenge) |
| `POW_INSUFFICIENT` | 401 | Proof-of-work difficulty not met | Yes |
| `RATE_LIMITED` | 429 | Exceeded quota | Yes (after retry-after) |
| `PATTERN_NOT_FOUND` | 404 | CID not in manifest | No |
| `SIGNATURE_INVALID` | 400 | Ed25519 verification failed | No |
| `MANIFEST_EXPIRED` | 410 | Manifest past expiry | Yes (fetch new) |
| `DP_BUDGET_EXHAUSTED` | 403 | User's DP ε budget depleted | Yes (next epoch) |
| `ATTESTATION_FAILED` | 403 | TEE quote verification failed | No |
| `VERSION_UNSUPPORTED` | 400 | Client version too old | Yes (update) |
| `INTERNAL_ERROR` | 500 | Service error | Yes (exponential backoff) |

---

## 8. Versioning & Compatibility

- **API Version**: In URL path (`/v1/`, `/v2/`)
- **Pattern Version**: In pattern metadata (`"version": 1`)
- **Manifest Version**: Top-level `"version": 2`
- **Compatibility Policy**: 
  - Clients support current + 1 previous API version
  - Patterns forward-compatible (ignore unknown fields)
  - Breaking changes require 90-day deprecation notice
  - Manifest v2+ requires client v1.5+

---

## 9. Rate Limiting & Abuse Prevention

**Per-Pseudonym (VRF Output) Limits:**
- Auth challenges: 10/hour
- Pattern requests: 20/day
- Pattern downloads: 100/day
- Telemetry submissions: 1/hour

**Global Protection:**
- PoW on auth (16 leading zero bits ≈ 65K hashes)
- Token bucket per IP/ASN (separate from pseudonym)
- GossipSub peer scoring (discourage spam)
- Manifest size capped at 1 MB

---

## 10. Security Headers (All Responses)

```http
Content-Security-Policy: default-src 'none'; frame-ancestors 'none'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
Permissions-Policy: accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```