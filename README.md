# Privacy-Preserving Data Poisoning Framework

> **A local-first, offline-capable system for individuals to protect against mass surveillance through adversarial data poisoning.**

## Overview

This framework enables individuals to inject carefully crafted adversarial patterns into their data emissions (browser fingerprints, behavioral biometrics, location traces, sensor streams, audio, etc.) to degrade the accuracy of surveillance ML models while maintaining plausible deniability and minimal utility loss.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  User Devices   │────►│ Pattern Generation│────►│  Distribution    │
│  (Client Agent) │     │    Service       │     │  (Multi-Channel) │
└─────────────────┘     └──────────────────┘     └──────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Local-First    │     │  Federated,      │     │  IPFS, P2P, Tor, │
│  Execution      │     │  Stateless,      │     │  CDN, QR/NFC,    │
│  (TEE/Secure    │     │  GPU-Accelerated │     │  LoRa, Sneakernet│
│   Enclave)      │     │  (No User Data)  │     │                  │
└─────────────────┘     └──────────────────┘     └──────────────────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │ Effectiveness Monitoring│
                    │ (Local Metrics + DP     │
                    │  Aggregation + Feedback)│
                    └────────────────────────┘
```

## Key Properties

| Property | Implementation |
|----------|----------------|
| **Local-First** | All pattern application on-device; no raw data leaves |
| **Offline-Capable** | Printable patterns, pre-computed bundles, sneakernet |
| **Minimal Trust** | No registration, VRF pseudonyms, no central logging |
| **Differential Privacy** | ε=0.1-1.0 per pattern type, calibrated noise |
| **Unique Per User** | 256-bit entropy, VRF-derived, forward secrecy |
| **Verifiable** | Ed25519 signatures, Merkle proofs, transparency logs |
| **Scalable** | Stateless workers, horizontal scaling, millions of users |

## Threat Model

Defends against:
- **State adversaries**: Bulk collection, targeted profiling, model training
- **Corporate surveillance**: Behavioral advertising, risk scoring, manipulation
- **Data brokers**: Re-identification, linkage attacks, profile aggregation

See [THREAT_MODEL.md](THREAT_MODEL.md) for detailed analysis.

## Components

### 1. Client-Side Poisoning Agent
- **Browser Extension** (MV3, Rust/WASM + TypeScript)
- **Mobile App** (iOS/Android, Rust FFI + Swift/Kotlin)
- **Wearable Integration** (watchOS, Wear OS, Garmin, Zepp, custom nRF52840)
- **Printable Patterns** (QR, DataMatrix, IR/UV ink, E-Ink badges)

### 2. Pattern Generation Service
- **Fingerprint Engine**: StyleGAN-3 for synthetic browser fingerprints
- **Behavioral Engine**: Transformer Seq2Seq for keystroke/mouse/scroll
- **Location Engine**: Physics-informed Markov chains on road networks
- **Sensor Engine**: PINN for IMU/GNSS/barometer simulation
- **Audio Engine**: PGD adversarial perturbation + ultrasonic jamming
- **Genomic Engine**: Conditional VAE preserving HWE/LD (opt-in)

### 3. Distribution Mechanism
- **Digital**: IPFS/IPNS, Libp2p GossipSub, DoH, Tor Onion v3, CDN
- **Physical**: QR/NFC, Sneakernet, LoRaWAN/Meshtastic, UWB/BLE beacons
- **Verification**: Ed25519, Merkle proofs, CT-style transparency logs, TEE attestation

### 4. Effectiveness Monitoring
- **Local Metrics**: Entropy, k-anonymity, model degradation, noise quality
- **Privacy-Preserving Aggregation**: Local TEE → Gaussian DP → Shuffle → Public stats
- **Feedback Loop**: Contextual bandit (LinUCB) for adaptive pattern selection

## Quick Start

### Browser Extension (Direct Install)
```bash
# 1. Verify release
curl -sL https://poisoning.example/releases/latest.json | \
  jq -r '.assets[] | select(.name=="extension.zip") | .sha256'

# 2. Download and verify signature
# 3. Install via "Load unpacked" (Chrome) or about:debugging (Firefox)
```

### Mobile App
```bash
# iOS: TestFlight link or AltStore
# Android: F-Droid / Obtainium / Direct APK (verify SHA256)
```

### Printable Patterns
```bash
# Web generator (no install)
open https://patterns.poisoning.example/generate

# CLI
cargo install poisoning-pattern-gen
poisoning-pattern-gen --type fingerprint --entropy 64 --output qr.png
```

### Custom Hardware (Badge)
```bash
# Flash firmware
cargo install cargo-embed
cargo embed --release --chip nRF52840_xxAA
```

## Documentation

| Document | Description |
|----------|-------------|
| [THREAT_MODEL.md](THREAT_MODEL.md) | Adversary classification, attack surfaces, risk assessment |
| [ARCHITECTURE.mmd](ARCHITECTURE.mmd) | Mermaid architecture diagram |
| [COMPONENT_SPECS.md](COMPONENT_SPECS.md) | Detailed component specifications |
| [API_CONTRACTS.md](API_CONTRACTS.md) | REST/gRPC/WebSocket APIs, binary formats |
| [DEPLOYMENT_STRATEGY.md](DEPLOYMENT_STRATEGY.md) | Deployment models, infrastructure, scaling |

## Security

- **Reproducible Builds**: Nix + cargo, multiple independent builders
- **Binary Transparency**: CT-style logs, threshold signatures (3-of-5)
- **TEE Attestation**: AWS Nitro / AMD SEV / Intel SGX / Apple Secure Enclave
- **Formal Verification**: F*/KreMLin (key derivation), EasyCrypt (DP), Prusti (Rust)
- **Bug Bounty**: https://poisoning.example/security (up to $50k)

## Contributing

```bash
# Build locally
nix develop  # or: cargo build --release --all-targets

# Run tests
cargo test --all
cargo test --all --target wasm32-unknown-unknown

# Generate patterns locally (offline)
cargo run --bin pattern-gen -- --type fingerprint --offline
```

## License

**MIT License** - See [LICENSE](LICENSE)

Cryptographic code: **Apache-2.0** (for patent grant)

## Citation

```bibtex
@misc{poisoning-framework,
  title={Privacy-Preserving Data Poisoning Framework},
  author={Poisoning Framework Contributors},
  year={2024},
  url={https://github.com/poisoning-framework/poisoning-framework}
}
```

## Acknowledgments

- Differential Privacy: Dwork, Roth, Abadi et al.
- Adversarial ML: Goodfellow, Madry, Carlini et al.
- Fingerprinting: Laperdrix, Acar, Eckersley et al.
- Privacy Engineering: Pfitzmann, Hansen, Diaz et al.

---

**Built for sovereignty. Deployed for privacy. Poisoning for freedom.**
