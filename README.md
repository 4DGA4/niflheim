# NIFLHEIM

**Educational Data Poisoning Toolkit for ML Security Awareness**

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-AGPL--3.0-green)
![Tests](https://img.shields.io/badge/tests-196%20passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-orange)

---

## Overview

NIFLHEIM is a comprehensive educational toolkit demonstrating data poisoning techniques for machine learning systems. Inspired by **Addie LaMarr's** groundbreaking research presented in *"Data Poisoning: The Fatal Flaw in Mass Surveillance"* (785K+ views, former FBI CISO Advisor), this project provides practical implementations of adversarial techniques to raise awareness about ML security vulnerabilities.

> **⚠️ Educational Purpose Only**: This toolkit is designed for research, education, and defensive security awareness. All implementations include safety features and are intended to demonstrate vulnerabilities so they can be better understood and mitigated.

## Key Features

### 🔬 Core Modules

1. **Backdoor Demonstration** (`backdoor_demo.py`)
   - Implements backdoor attacks on neural networks
   - Demonstrates trigger-based misclassification
   - 52 comprehensive tests
   - Shows how attackers can embed hidden vulnerabilities

2. **Model Collapse** (`model_collapse.py`)
   - Demonstrates training data contamination attacks
   - Shows degradation of model performance
   - 44 tests covering various attack vectors
   - Illustrates fragility of ML training pipelines

3. **Adversarial Fashion** (`adversarial_fashion.py`)
   - Physical-world adversarial examples
   - Clothing patterns that fool computer vision
   - 26 tests for pattern generation
   - Demonstrates real-world evasion techniques

4. **AdTech Fragility** (`adtech_fragility.py`)
   - Targets advertising technology systems
   - Demonstrates poisoning of recommendation engines
   - 45 tests on ad network vulnerabilities
   - Shows privacy implications of ML in advertising

5. **Core Poisoning Framework** (`core.py`)
   - Foundational data poisoning primitives
   - Reusable components for research
   - 29 tests ensuring reliability
   - Clean API for educational experimentation

### 🌐 Browser Extension

A companion browser extension for demonstrating client-side data poisoning:

- **Manifest V3** compatible
- Real-time request interception
- Educational overlays and warnings
- Privacy-preserving by design

See `browser-extension/README.md` for installation instructions.

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Git (for cloning)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/darkempire/niflheim.git
cd niflheim

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Or install from requirements
pip install -r requirements.txt
```

### Development Installation

```bash
pip install -e ".[dev]"
```

This installs additional tools for testing and development:
- `pytest` - Testing framework
- `black` - Code formatter
- `ruff` - Fast Python linter
- `mypy` - Static type checker

## Usage

### Running Modules

Each module is self-contained and can be run independently:

```python
from maw.data_poisoning import backdoor_demo

# Initialize the demonstration
demo = backdoor_demo.BackdoorDemonstration()

# Run the attack simulation
results = demo.run()

# Analyze results
demo.analyze(results)
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=maw --cov-report=html

# Run specific test module
pytest tests/test_backdoor_demo.py -v
```

### Test Results

**196 tests passing** with 100% success rate:

- `test_core.py`: 29 tests
- `test_adversarial_fashion.py`: 26 tests
- `test_backdoor_demo.py`: 52 tests
- `test_model_collapse.py`: 44 tests
- `test_adtech_fragility.py`: 45 tests

## Documentation

Detailed documentation is available in the `docs/` directory:

- [`DATA_POISONING_RESEARCH.md`](docs/DATA_POISONING_RESEARCH.md) - Research background
- [`EDUCATIONAL_RESOURCES.md`](docs/EDUCATIONAL_RESOURCES.md) - Learning materials
- [`SECURITY_NOTICE.md`](docs/SECURITY_NOTICE.md) - Security considerations
- [`VALIDATION_REPORT.md`](docs/VALIDATION_REPORT.md) - Test validation
- [`INTEGRATION_GUIDE.md`](docs/INTEGRATION_GUIDE.md) - Integration instructions

## Safety & Ethics

### ⚠️ Important Disclaimers

1. **Educational Use Only**: This toolkit is designed for:
   - Security research
   - Educational demonstrations
   - Defensive security training
   - Awareness raising

2. **Not for Malicious Use**: Do not use these techniques to:
   - Attack production systems
   - Compromise real ML models
   - Violate terms of service
   - Harm individuals or organizations

3. **Responsible Disclosure**: If you discover vulnerabilities:
   - Report responsibly to affected parties
   - Follow coordinated disclosure practices
   - Prioritize user safety and privacy

### Built-in Safety Features

- All modules include warnings and disclaimers
- No automatic deployment to production systems
- Clear documentation of ethical considerations
- Test suite validates safety constraints

## Community

### Outreach Materials

Community engagement materials are available in `community/`:

- Reddit discussion posts
- Hacker News submissions
- Social media templates
- FAQ documents
- Engagement guidelines

### Contributing

We welcome contributions! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for:
- How to report bugs
- Submitting pull requests
- Development setup
- Code style guidelines

### License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0).

See [`LICENSE`](LICENSE) for full license text.

### Acknowledgments

- **Addie LaMarr** - Original research and inspiration
- **DARK EMPIRE Research** - Development and testing
- **Open Source Community** - Supporting libraries and tools

## Citation

If you use NIFLHEIM in your research, please cite:

```bibtex
@software{niflheim2026,
  title = {NIFLHEIM: Educational Data Poisoning Toolkit},
  author = {Gill, Connor and DARK EMPIRE Research},
  year = {2026},
  version = {1.0.0},
  url = {https://github.com/darkempire/niflheim},
  license = {AGPL-3.0}
}
```

## Contact

- **Repository**: https://github.com/darkempire/niflheim
- **Issues**: https://github.com/darkempire/niflheim/issues
- **Email**: research@darkempire.io

---

**"Data poisoning is not a bug—it's a feature of systems that harvest human data without consent."**

*Inspired by Addie LaMarr's research on the fatal flaw in mass surveillance*
