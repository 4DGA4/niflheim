# Threat Model: Privacy-Preserving Data Poisoning Framework

## 1. Adversary Classification

### 1.1 State-Level Adversaries (APTs, Intelligence Agencies)
**Capabilities:**
- Nation-state resources (NSA, GCHQ, Unit 8200 equivalents)
- Legal compulsion (NSLs, FISA orders, bulk collection authorities)
- Physical infrastructure access (fiber taps, BGP hijacking, cell-site simulators)
- Zero-day exploits and supply chain compromise
- AI/ML model training on intercepted data at massive scale

**Objectives:**
- Mass population surveillance and behavioral prediction
- Targeted individual tracking and profiling
- Social graph mapping and influence operations
- Pre-crime / predictive policing datasets

### 1.2 Corporate Surveillance (Big Tech, AdTech, Data Brokers)
**Capabilities:**
- First-party data collection (apps, browsers, IoT, wearables)
- Third-party tracking (pixels, fingerprinting, SDKs, bidstream data)
- Cross-device linkage (probabilistic + deterministic)
- Data clean rooms and identity graphs (LiveRamp, Experian, Acxiom)
- Real-time bidding (RTB) data exhaust at petabyte scale
- ML inference on behavioral biometrics

**Objectives:**
- Behavioral advertising and microtargeting
- Risk scoring (insurance, credit, employment, law enforcement)
- Algorithmic manipulation (engagement, addiction, radicalization)
- Data monetization via broker ecosystems

### 1.3 Data Brokers & Aggregators
**Capabilities:**
- Public records scraping (property, court, voter, licensing)
- Purchase history aggregation (loyalty cards, receipt scanning)
- Location data from apps/SDKs (X-Mode, SafeGraph, Kochava)
- Healthcare/pharmacy data (HIPAA "de-identified" loopholes)
- Genetic data (23andMe, Ancestry, GEDmatch law enforcement access)

**Objectives:**
- Comprehensive "360-degree" consumer profiles
- Resale to advertisers, insurers, employers, government
- Risk models for tenant screening, hiring, policing

---

## 2. Attack Surfaces & Data Vectors

| Vector | Collection Method | Poisoning Opportunity |
|--------|-------------------|----------------------|
| **Browser Fingerprinting** | Canvas, WebGL, AudioContext, fonts, battery | Synthetic fingerprint rotation |
| **Behavioral Biometrics** | Keystroke dynamics, mouse curves, scroll patterns | Adversarial noise injection |
| **Location Tracking** | GPS, WiFi/BLE scanning, cell tower, IP geolocation | Synthetic trajectory generation |
| **Network Traffic** | TLS SNI, DNS, packet timing, flow correlation | Cover traffic, timing obfuscation |
| **Device Sensors** | Accelerometer, gyroscope, magnetometer, barometer | Sensor noise injection |
| **Audio/Visual** | Hotword detection, always-on mic, camera ML | Adversarial perturbations |
| **Transaction Data** | Card networks, receipt OCR, loyalty programs | Synthetic purchase patterns |
| **Social Graph** | Contact uploads, interaction metadata | Synthetic relationship noise |
| **Biometric/Health** | Wearable HRV, sleep, SpO2, menstrual tracking | Physiological noise injection |
| **Genomic** | Direct-to-consumer testing, relative matching | Synthetic variant injection |

---

## 3. Threat Scenarios

### 3.1 Passive Mass Collection
**Adversary:** State/corporate dragnet
**Method:** Bulk ingestion of telemetry, bidstream, sensor data
**Impact:** Population-scale behavioral models, anomaly detection
**Mitigation:** High-entropy pattern injection at source

### 3.2 Targeted Profiling
**Adversary:** Data broker + law enforcement fusion
**Method:** Re-identification via quasi-identifiers, linkage attacks
**Impact:** Individual dossiers, pre-crime scoring, discrimination
**Mitigation:** Per-user unique poisoning patterns, k-anonymity via noise

### 3.3 Model Poisoning / Inference Attacks
**Adversary:** ML pipeline training on poisoned data
**Method:** Gradient manipulation, backdoor insertion, membership inference
**Impact:** Degraded model utility, targeted misclassification
**Mitigation:** Controlled poisoning within differential privacy bounds

### 3.4 Supply Chain / Software Compromise
**Adversary:** Malicious SDK, browser extension, OS update
**Method:** Silent data exfiltration, pattern neutralization
**Impact:** Complete bypass of client-side protections
**Mitigation:** Reproducible builds, attestation, minimal TCB

---

## 4. Trust Assumptions & Boundaries

### 4.1 Trusted
- User's local device (TEE/secure enclave where available)
- User-generated entropy (hardware RNG, user interaction)
- Open-source client code (reproducible builds, audited)

### 4.2 Untrusted
- All network infrastructure (ISP, CDN, DNS, Tor exit nodes)
- Pattern generation service (operated by potentially hostile parties)
- App stores, auto-update mechanisms
- Cloud backup/sync services
- Any third-party analytics or telemetry

### 4.3 Semi-Trusted (Minimized)
- Distribution channels (IPFS, P2P, sneakernet) - content-addressed, verified
- Effectiveness monitoring - differential privacy, local aggregation only

---

## 5. Security Properties Required

| Property | Requirement | Enforcement |
|----------|-------------|-------------|
| **Source Anonymity** | No link between user and poisoned patterns | On-device generation, no registration |
| **Pattern Uniqueness** | Each user gets cryptographically distinct patterns | Per-user key derivation, VRF |
| **Non-Attribution** | Poisoned data indistinguishable from natural noise | Statistical mimicry, DP noise calibration |
| **Forward Secrecy** | Compromised key doesn't reveal past patterns | Ephemeral keys, ratcheting |
| **Denial of Service Resistance** | Adversary cannot flood/block pattern distribution | P2P + multiple channels, erasure coding |
| **Tamper Evidence** | User detects pattern modification | Merkle proofs, signed manifests |
| **Minimal TCB** | < 5k LOC in trusted path | Formal verification targets, Rust + seL4 |

---

## 6. Risk Assessment Matrix

| Threat | Likelihood | Impact | Residual Risk (with mitigations) |
|--------|------------|--------|----------------------------------|
| State compels pattern service | High | Critical | **Medium** (local fallback, multiple operators) |
| Adversary filters poisoned data | Medium | High | **Low** (adaptive patterns, mimicry) |
| Client malware exfiltrates keys | Medium | Critical | **Medium** (TEE, hardware isolation) |
| Pattern collision (two users same) | Negligible | Medium | **Negligible** (256-bit entropy) |
| DP budget exhaustion | Low | Medium | **Low** (adaptive budget, local-only mode) |
| Supply chain attack on client | Medium | Critical | **High** (reproducible builds, attestation) |
| Legal prohibition of tool | Medium | High | **Medium** (stealth modes, steganography) |

---

## 7. Regulatory & Legal Considerations

- **CFAA / Computer Misuse Act**: Poisoning ≠ unauthorized access (data is voluntarily emitted)
- **GDPR Art. 22**: Right to object to automated profiling → legal basis for poisoning
- **CCPA/CPRA**: Right to opt-out of sale → poisoning as technical enforcement
- **Wiretap Laws**: Passive emission ≠ interception; active injection requires care
- **Export Controls**: Cryptography (pattern gen) may require license (ECCN 5D002)
- **State Laws**: BIPA (IL), CUBI (TX), CIPA (CA) - biometric protections align with goals