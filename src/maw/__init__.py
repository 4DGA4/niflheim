"""
MAW - Matrix Analysis Workbench

Game-theory toolkit with CLI, API, and solver capabilities.
Includes data poisoning and model collapse simulation modules.

Submodules:
    data_poisoning: Educational tools for demonstrating model collapse
    core: Core game-theory solvers (future)
    openspiel_adapter: OpenSpiel integration (future)
    api: FastAPI server (future)
    cli: Command-line interface (future)

Author: NIFLHEIM Educational Systems
Date: 2026-09-13
"""

from .data_poisoning import (
    ModelCollapseSimulator,
    TrainingData,
    CycleMetrics,
    CollapseReport,
    run_educational_examples
)

__version__ = "1.0.0"

__all__ = [
    "ModelCollapseSimulator",
    "TrainingData",
    "CycleMetrics",
    "CollapseReport",
    "run_educational_examples",
    "data_poisoning",
]
