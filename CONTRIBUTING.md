# Contributing to NIFLHEIM

Thank you for your interest in contributing to NIFLHEIM, an educational data poisoning toolkit for ML security awareness.

## Code of Conduct

This project operates under the principle that **data poisoning is a legitimate defensive technique** against mass surveillance and unconsented data harvesting. All contributors must:

1. **Respect the educational mission** - This toolkit is designed for research, education, and awareness
2. **Acknowledge the source** - Inspired by Addie LaMarr's research on data poisoning as "the fatal flaw in mass surveillance"
3. **Maintain safety** - All implementations include appropriate disclaimers and safety documentation

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Include:
   - Python version
   - OS and environment details
   - Steps to reproduce
   - Expected vs actual behavior
   - Test output if applicable

### Suggesting Enhancements

1. Open an issue with the enhancement label
2. Describe the use case
3. Explain why this improves the toolkit
4. Provide examples if possible

### Pull Requests

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Write tests** - All new features must have test coverage
5. **Run the test suite**: `pytest tests/ -v`
6. **Ensure linting passes**: `ruff check .` and `black --check .`
7. **Submit a PR** with:
   - Clear description of changes
   - Reference to any related issues
   - Test results

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/niflheim.git
cd niflheim

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run linters
ruff check .
black --check .
```

### Testing Standards

- **Minimum 90% coverage** for new modules
- **Unit tests** for individual functions
- **Integration tests** for module interactions
- **Document edge cases** in test comments

### Code Style

- **Python**: Follow PEP 8, enforced by `black` and `ruff`
- **Line length**: 100 characters
- **Type hints**: Encouraged for public APIs
- **Docstrings**: Required for all public functions and classes

### Documentation

- Update `README.md` for user-facing changes
- Add to `docs/` for technical documentation
- Include docstrings in code
- Update `CHANGELOG.md` for significant changes

## License

By contributing, you agree that your contributions will be licensed under the AGPL-3.0 license.

## Questions?

Open an issue or reach out to the maintainers at research@darkempire.io

---

**Remember**: This is an educational tool. Always use responsibly and ethically.
