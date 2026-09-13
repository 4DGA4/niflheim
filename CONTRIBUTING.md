# CONTRIBUTING to NIFLHEIM

Thank you for your interest in contributing to NIFLHEIM! We welcome contributions from the security and privacy community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation Guidelines](#documentation-guidelines)
- [Safety Requirements](#safety-requirements)

---

## Code of Conduct

### Our Pledge

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to a positive environment:

- Demonstrating empathy and kindness toward other people
- Being respectful of differing opinions, viewpoints, and experiences
- Giving and gracefully accepting constructive feedback
- Accepting responsibility and apologizing to those affected by our mistakes
- Focusing on what is best for the community

Examples of unacceptable behavior:

- The use of sexualized language or imagery, and sexual attention or advances of any kind
- Trolling, insulting or derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Enforcement

Report unacceptable behavior to [conduct@niflheim.example]. All complaints will be reviewed and investigated promptly and fairly.

---

## How Can I Contribute?

### Reporting Bugs

**Before submitting bug reports:**
- Check the FAQ
- Search existing issues
- Try to reproduce with latest version

**Good bug reports include:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, dependencies)
- Screenshots or logs if applicable

### Suggesting Enhancements

**Before suggesting enhancements:**
- Check if feature already exists
- Review roadmap and planned features
- Ensure alignment with educational mission

**Good enhancement requests:**
- Clear use case description
- Educational value explanation
- Implementation suggestions (optional)
- Safety considerations addressed

### Your First Code Contribution

**Good first issues:**
- Bug fixes in documentation
- Additional test coverage
- Code cleanup and refactoring
- Tutorial examples

**Resources for new contributors:**
- Look for issues labeled "good first issue"
- Read the architecture documentation
- Start with small, focused changes
- Ask questions in GitHub Discussions

### Contributing Code

**Steps:**
1. Fork the repository
2. Create a branch from `main`
3. Make your changes
4. Add tests
5. Run tests and linters
6. Update documentation
7. Submit pull request

---

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- pip or poetry
- Virtual environment tool (venv, virtualenv, conda)

### Installation

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/niflheim.git
cd niflheim

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Verify setup
pytest tests/ -v
```

### Development Tools

**Recommended:**
- Black (code formatting)
- flake8 (linting)
- mypy (type checking)
- pytest (testing)
- coverage (test coverage)

**Install:**
```bash
pip install black flake8 mypy pytest coverage
```

---

## Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Safety controls implemented (if applicable)
- [ ] No sensitive data included
- [ ] Commit messages are clear

### PR Title

**Good:**
- "Add model collapse visualization for text generators"
- "Fix edge case in backdoor detection"
- "Update documentation for installation"

**Avoid:**
- "Update code"
- "Fix stuff"
- "Various improvements"

### PR Description

**Include:**
- What changes were made
- Why the changes are needed
- How changes were tested
- Any breaking changes
- Related issues

**Template:**
```markdown
## Description
Brief description of changes

## Motivation
Why these changes are needed

## Testing
How changes were tested

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Safety controls (if applicable)
- [ ] No breaking changes (or documented below)

## Breaking Changes
None (or describe)
```

### Review Process

1. **Automated Checks**: Tests, linters, coverage
2. **Maintainer Review**: Code quality, safety, alignment
3. **Community Feedback**: Comments from other contributors
4. **Revisions**: Address feedback
5. **Merge**: Approved by maintainer

**Response Time**: We aim to review PRs within 1 week.

---

## Coding Standards

### Python Style

**Follow:**
- PEP 8 (Python style guide)
- PEP 484 (type hints)
- PEP 257 (docstrings)

**Tools:**
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/
```

### Code Organization

**Structure:**
```
niflheim/
├── src/
│   ├── niflheim/
│   │   ├── __init__.py
│   │   ├── backdoor.py
│   │   ├── collapse.py
│   │   └── safety.py
│   └── tests/
│       ├── test_backdoor.py
│       ├── test_collapse.py
│       └── test_safety.py
├── docs/
├── examples/
└── tools/
```

### Naming Conventions

**Modules:**
- Lowercase with underscores: `backdoor_demo.py`

**Classes:**
- CamelCase: `BackdoorDemonstration`

**Functions/Variables:**
- Lowercase with underscores: `run_simulation()`

**Constants:**
- Uppercase with underscores: `MAX_POISON_PERCENTAGE`

### Type Hints

**Use type hints for:**
- Function parameters
- Return values
- Class attributes

**Example:**
```python
from typing import Dict, List, Optional

def run_backdoor_demo(
    model_type: str,
    poison_percentage: float,
    trigger_pattern: Optional[str] = None
) -> Dict[str, float]:
    """Run backdoor demonstration with safety controls."""
    ...
```

### Documentation

**Docstrings:**
- Use Google or NumPy style
- Include parameters, returns, raises
- Provide examples

**Example:**
```python
def simulate_model_collapse(
    iterations: int,
    poison_rate: float
) -> CollapseResults:
    """
    Simulate model collapse from iterative poisoning.
    
    Args:
        iterations: Number of training iterations
        poison_rate: Percentage of poisoned data (0.0-1.0)
    
    Returns:
        CollapseResults with metrics and visualizations
    
    Raises:
        ValueError: If poison_rate > 0.2 (safety limit)
    
    Example:
        >>> simulator = ModelCollapseSimulator()
        >>> results = simulator.simulate_model_collapse(10, 0.15)
    """
    ...
```

---

## Testing Requirements

### Test Coverage

**Requirements:**
- All new features must have tests
- Bug fixes must include regression tests
- Aim for >90% code coverage

**Run Tests:**
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=niflheim --cov-report=html

# Specific test file
pytest tests/test_backdoor.py -v

# Specific test function
pytest tests/test_backdoor.py::test_backdoor_safety_controls -v
```

### Test Types

**Unit Tests:**
- Test individual functions/classes
- Mock external dependencies
- Fast execution (< 1 second each)

**Integration Tests:**
- Test component interactions
- Use real (synthetic) data
- Moderate execution time

**Safety Tests:**
- Verify safety controls work
- Test parameter limits
- Validate audit logging

### Test Naming

**Pattern:**
```python
def test_<function>_<scenario>_<expected_behavior>():
    ...

# Examples:
def test_backdoor_demo_safety_flag_required():
    ...

def test_model_collapse_poison_percentage_limit():
    ...

def test_audit_logging_records_all_operations():
    ...
```

### Continuous Integration

**GitHub Actions:**
- Runs on all PRs
- Tests on multiple Python versions
- Checks code style and type hints
- Reports coverage

**Status Checks:**
- Must pass before merge
- Fix failures before requesting review

---

## Documentation Guidelines

### README Updates

**Update README.md when:**
- Adding new features
- Changing installation process
- Modifying API
- Adding examples

### Inline Documentation

**Comment:**
- Complex algorithms
- Safety-critical code
- Non-obvious decisions
- API boundaries

**Don't comment:**
- Obvious code
- Every line
- Workarounds for bugs (use issue tracker instead)

### Examples

**Provide examples for:**
- All public APIs
- Common use cases
- Safety features
- Error handling

**Example Format:**
```python
# Basic usage
from niflheim import BackdoorDemonstration

demo = BackdoorDemonstration(educational_use=True)
results = demo.run(model_type="cnn", poison_percentage=10)
print(f"Accuracy: {results['accuracy']:.2%}")
```

### Tutorials

**Create tutorials for:**
- Getting started
- Common workflows
- Advanced features
- Integration with other tools

**Tutorial Structure:**
1. Learning objectives
2. Prerequisites
3. Step-by-step instructions
4. Expected output
5. Troubleshooting tips
6. Next steps

---

## Safety Requirements

### Mandatory Safety Controls

**All features MUST include:**

1. **Educational Use Flag**
```python
def run_demo(educational_use: bool = False, **kwargs):
    if not educational_use:
        raise ValueError("educational_use=True is required")
```

2. **Audit Logging**
```python
import logging

logging.info(f"Operation: {operation}, Parameters: {params}, Timestamp: {timestamp}")
```

3. **Parameter Limits**
```python
MAX_POISON_PERCENTAGE = 0.20  # 20%

if poison_percentage > MAX_POISON_PERCENTAGE:
    raise ValueError(f"Poison percentage cannot exceed {MAX_POISON_PERCENTAGE:.0%}")
```

4. **Safety Disclaimers**
```python
def display_safety_warning():
    print("""
    WARNING: This demonstration is for EDUCATIONAL USE ONLY.
    Not intended for malicious use. Comply with all applicable laws.
    """)
```

5. **Synthetic Data Only**
```python
def load_dataset():
    # Generate synthetic data
    return generate_synthetic_data()
    # NEVER: load_real_user_data()
```

### Safety Review

**All PRs are reviewed for:**
- Safety control implementation
- Potential for misuse
- Compliance with ethical guidelines
- Proper disclaimers

**Safety-Critical Changes:**
- Require additional review
- Must include safety tests
- Need documentation updates
- May require community discussion

### Prohibited Contributions

**Do NOT submit:**
- Code that removes safety controls
- Real-world datasets (especially with personal data)
- Malicious use examples
- Instructions for unauthorized testing
- Code that bypasses audit logging

**Such PRs will be rejected immediately.**

---

## Additional Contribution Areas

### Translations

**We welcome translations of:**
- README.md
- Documentation
- User interface messages
- Tutorials

**Process:**
1. Check if translation already exists
2. Create translation in `docs/i18n/<language>/`
3. Maintain accuracy and technical correctness
4. Update translation status in README

### Educational Content

**Contribute:**
- Tutorial videos
- Workshop materials
- Assignment templates
- Lecture slides

**Submit:**
- Add to `docs/education/`
- Include usage guidelines
- Specify target audience
- Provide answer keys (for assignments)

### Research

**We encourage:**
- Papers using NIFLHEIM
- Novel attack/defense implementations
- Performance optimizations
- Comparative studies

**Process:**
- Open issue describing research
- Coordinate with maintainers
- Cite NIFLHEIM in publications
- Share findings with community

---

## Recognition

### Contributors

**We recognize contributors through:**
- GitHub contributor graph
- README contributor list
- Release notes acknowledgments
- Annual contributor highlights

### Becoming a Maintainer

**Path to maintainer status:**
1. Consistent contributions over time
2. Demonstrates understanding of project vision
3. Helps other contributors
4. Shows good judgment on safety issues
5. Nominated by existing maintainers
6. Approved by community

**Maintainer responsibilities:**
- Review PRs
- Triage issues
- Mentor new contributors
- Uphold code of conduct
- Ensure safety standards

---

## Questions?

**Get Help:**
- GitHub Discussions: General questions
- GitHub Issues: Bug reports and features
- Email: [contributors@niflheim.example] (placeholder)

**We're Here to Help!**

Don't hesitate to ask questions. We remember what it was like to be new to the project and want to make contributing as easy as possible.

---

**Thank you for contributing to NIFLHEIM!**

Your contributions help advance ML security education and make the toolkit better for everyone.
