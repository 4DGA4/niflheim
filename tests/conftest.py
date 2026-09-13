"""
Pytest configuration for MAW model collapse tests.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for all tests
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def simulator():
    """Provide a default simulator instance for tests."""
    from maw.data_poisoning.model_collapse import ModelCollapseSimulator
    return ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.1)


@pytest.fixture
def simulated_simulator():
    """Provide a simulator that has run a simulation."""
    from maw.data_poisoning.model_collapse import ModelCollapseSimulator
    sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
    sim.simulate_retraining_cycle(n_cycles=10)
    return sim
