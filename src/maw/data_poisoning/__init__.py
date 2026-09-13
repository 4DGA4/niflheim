"""
Data Poisoning Module - Educational Demonstrations

This submodule provides educational demonstrations of data poisoning attacks,
specifically backdoor attacks, for defensive security understanding.

Modules:
    backdoor_demo: Backdoor attack demonstration and detection
"""

from .backdoor_demo import BackdoorDemo, run_educational_demo

__all__ = [
    'BackdoorDemo',
    'run_educational_demo',
]
