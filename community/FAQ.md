# NIFLHEIM Community FAQ

## General Questions

### What is NIFLHEIM?

NIFLHEIM is an educational toolkit demonstrating data poisoning techniques for machine learning systems. It provides practical implementations of adversarial methods to raise awareness about ML security vulnerabilities.

### Why was this created?

This project was inspired by **Addie LaMarr's** research presented in *"Data Poisoning: The Fatal Flaw in Mass Surveillance"* (785K+ views). The goal is to educate people about ML security vulnerabilities so they can better defend against them.

### Is this legal?

Yes. This toolkit is designed for:
- Educational purposes
- Security research
- Defensive training
- Awareness raising

All code is released under the AGPL-3.0 open source license.

### Is this ethical?

Yes, when used as intended. This is **educational software** designed to:
- Help people understand ML vulnerabilities
- Enable defensive security research
- Promote awareness of data collection practices
- Support academic study of adversarial ML

**Do not use** these techniques to attack production systems or harm others.

## Technical Questions

### What Python version do I need?

Python 3.10 or higher is required.

### How do I install NIFLHEIM?

```bash
git clone https://github.com/darkempire/niflheim.git
cd niflheim
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

See the main README for detailed instructions.

### What modules are included?

1. **Backdoor Demonstration** - Trigger-based attacks
2. **Model Collapse** - Training data contamination
3. **Adversarial Fashion** - Physical-world evasion
4. **AdTech Fragility** - Advertising system vulnerabilities
5. **Core Framework** - Foundational primitives

### How many tests are included?

**196 tests** covering all modules, with 100% pass rate.

Run tests with: `pytest tests/ -v`

### Can I use this in production?

**No.** This is an educational toolkit, not a production-ready system. The code demonstrates vulnerabilities for learning purposes.

### Does this work with real ML models?

The modules can work with real models in controlled environments (research, education). **Do not deploy** against production systems without explicit authorization.

## Safety & Ethics

### What safety features are included?

- Clear warnings and disclaimers in all modules
- No automatic deployment capabilities
- Educational documentation
- Test suite validates safety constraints

### How should I use this responsibly?

1. **Educational contexts only** - classrooms, research labs
2. **Authorized systems only** - your own models or with permission
3. **Defensive focus** - learn to protect, not attack
4. **Respect laws** - comply with applicable regulations
5. **Share knowledge** - help others understand and defend

### What if I find a vulnerability?

Practice **responsible disclosure**:
1. Document the issue clearly
2. Contact affected parties privately
3. Allow time for remediation
4. Publish responsibly

### Can this be used maliciously?

Like any security tool, it *could* be misused. That's why we:
- Emphasize educational purpose
- Include clear disclaimers
- Focus on defensive applications
- Encourage responsible use

## Research & Academic Use

### Can I cite this in my research?

Yes! See the README for citation information:

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

### Can I use this in my classroom?

Absolutely! This toolkit is designed for educational use. Consider:
- Demonstrating ML security concepts
- Hands-on adversarial ML labs
- Privacy and ethics discussions
- Capstone projects

### Is there documentation for educators?

Yes, see `docs/EDUCATIONAL_RESOURCES.md` for teaching materials and guidance.

## Community

### How do I contribute?

See `CONTRIBUTING.md` for:
- Reporting bugs
- Submitting pull requests
- Development setup
- Code style guidelines

### What license is this under?

**AGPL-3.0** (GNU Affero General Public License v3.0)

This ensures:
- Software remains free and open
- Modifications must be shared
- Network use counts as distribution

### Who maintains this project?

Primary maintainer: **Connor Gill** (DARK EMPIRE Research)

Community contributions welcome!

### How do I report security issues?

Email: research@darkempire.io

Or open a draft security issue on GitHub.

## Inspiration

### Who is Addie LaMarr?

Addie LaMarr is a former FBI CISO Advisor who presented groundbreaking research on data poisoning as "the fatal flaw in mass surveillance." Their work has been viewed 785K+ times and inspired this educational toolkit.

### What is "Data Poisoning: The Fatal Flaw in Mass Surveillance"?

A research presentation demonstrating how data poisoning techniques can disrupt mass surveillance systems that harvest personal data without consent.

### Why "NIFLHEIM"?

In Norse mythology, Niflheim is the realm of ice and mist—a fitting name for a toolkit that helps users become "invisible" to mass surveillance through data poisoning.

## Getting Help

### I have a question not answered here

Open an issue on GitHub: https://github.com/darkempire/niflheim/issues

Or email: research@darkempire.io

### Where can I learn more about data poisoning?

See `docs/DATA_POISONING_RESEARCH.md` for:
- Academic papers
- Research resources
- Further reading
- Related projects

---

**Last Updated**: September 2026  
**Version**: 1.0.0
