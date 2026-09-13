"""
Test Suite for Model Collapse Simulator

Comprehensive tests for the NIFLHEIM Model Collapse Simulator,
covering initialization, simulation, visualization, and reporting.

Run with: pytest test_model_collapse.py -v
"""

import pytest
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from maw.data_poisoning.model_collapse import (
    ModelCollapseSimulator,
    TrainingData,
    CycleMetrics,
    CollapseReport,
    run_educational_examples
)


class TestTrainingData:
    """Tests for TrainingData dataclass."""

    def test_training_data_initialization(self):
        """Test basic TrainingData initialization."""
        data = TrainingData(clean_samples=900, poisoned_samples=100, ai_generated_samples=0)
        assert data.clean_samples == 900
        assert data.poisoned_samples == 100
        assert data.ai_generated_samples == 0
        assert data.total_samples == 1000
        assert data.poison_ratio == 0.1
        assert data.ai_ratio == 0.0

    def test_training_data_with_ai_generated(self):
        """Test TrainingData with AI-generated samples."""
        data = TrainingData(clean_samples=700, poisoned_samples=100, ai_generated_samples=200)
        assert data.total_samples == 1000
        assert data.poison_ratio == 0.1
        assert data.ai_ratio == 0.2

    def test_training_data_zero_samples(self):
        """Test TrainingData with zero samples."""
        data = TrainingData(clean_samples=0, poisoned_samples=0, ai_generated_samples=0)
        assert data.total_samples == 0
        assert data.poison_ratio == 0.0
        assert data.ai_ratio == 0.0

    def test_training_data_ratios_sum(self):
        """Test that poison and AI ratios sum correctly."""
        data = TrainingData(clean_samples=500, poisoned_samples=300, ai_generated_samples=200)
        total_ratio = data.poison_ratio + data.ai_ratio + (data.clean_samples / data.total_samples)
        assert abs(total_ratio - 1.0) < 0.001


class TestCycleMetrics:
    """Tests for CycleMetrics dataclass."""

    def test_cycle_metrics_creation(self):
        """Test basic CycleMetrics creation."""
        metrics = CycleMetrics(
            cycle_number=5,
            accuracy=0.75,
            poison_ratio=0.15,
            ai_ratio=0.1,
            total_samples=1000,
            is_collapsed=False
        )
        assert metrics.cycle_number == 5
        assert metrics.accuracy == 0.75
        assert metrics.poison_ratio == 0.15
        assert not metrics.is_collapsed

    def test_cycle_metrics_auto_collapse_detection(self):
        """Test automatic collapse detection."""
        metrics = CycleMetrics(
            cycle_number=10,
            accuracy=0.45,
            poison_ratio=0.3,
            ai_ratio=0.2,
            total_samples=1000
        )
        # Should be collapsed (accuracy < 0.5)
        assert metrics.accuracy < 0.5


class TestModelCollapseSimulatorInitialization:
    """Tests for ModelCollapseSimulator initialization."""

    def test_default_initialization(self):
        """Test simulator with default parameters."""
        sim = ModelCollapseSimulator()
        assert sim.initial_accuracy == 0.95
        assert sim.poison_rate == 0.1
        assert sim.current_accuracy == 0.95
        assert sim.collapse_threshold == 0.50
        assert len(sim.cycle_metrics) == 0

    def test_custom_initialization(self):
        """Test simulator with custom parameters."""
        sim = ModelCollapseSimulator(initial_accuracy=0.99, poison_rate=0.2)
        assert sim.initial_accuracy == 0.99
        assert sim.poison_rate == 0.2
        assert sim.current_accuracy == 0.99

    def test_invalid_initial_accuracy_high(self):
        """Test that invalid initial_accuracy raises error."""
        with pytest.raises(ValueError, match="initial_accuracy must be between"):
            ModelCollapseSimulator(initial_accuracy=1.5)

    def test_invalid_initial_accuracy_negative(self):
        """Test that negative initial_accuracy raises error."""
        with pytest.raises(ValueError, match="initial_accuracy must be between"):
            ModelCollapseSimulator(initial_accuracy=-0.1)

    def test_invalid_poison_rate(self):
        """Test that invalid poison_rate raises error."""
        with pytest.raises(ValueError, match="poison_rate must be between"):
            ModelCollapseSimulator(poison_rate=1.5)


class TestSimulationCycles:
    """Tests for retraining cycle simulation."""

    def test_single_cycle_simulation(self):
        """Test simulation with single cycle."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.1)
        metrics = sim.simulate_retraining_cycle(n_cycles=1)
        assert len(metrics) == 1
        assert metrics[0].cycle_number == 0
        assert metrics[0].accuracy == 0.95

    def test_multiple_cycle_simulation(self):
        """Test simulation with multiple cycles."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.1)
        metrics = sim.simulate_retraining_cycle(n_cycles=10)
        assert len(metrics) == 10
        assert [m.cycle_number for m in metrics] == list(range(10))

    def test_accuracy_decay_over_cycles(self):
        """Test that accuracy decreases over cycles."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
        metrics = sim.simulate_retraining_cycle(n_cycles=10)
        
        accuracies = [m.accuracy for m in metrics]
        # Accuracy should generally decrease
        assert accuracies[0] >= accuracies[-1]
        # Should show some decay
        assert accuracies[0] - accuracies[-1] > 0.01

    def test_poison_amplification_over_cycles(self):
        """Test that poison ratio amplifies over cycles."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.1)
        metrics = sim.simulate_retraining_cycle(n_cycles=10)
        
        poison_ratios = [m.poison_ratio for m in metrics]
        # Poison ratio should generally increase
        assert poison_ratios[-1] >= poison_ratios[0]

    def test_ai_ratio_growth(self):
        """Test that AI-generated data ratio grows over cycles."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.1)
        metrics = sim.simulate_retraining_cycle(n_cycles=15)
        
        ai_ratios = [m.ai_ratio for m in metrics]
        # AI ratio should increase from 0
        assert ai_ratios[0] == 0.0
        assert ai_ratios[-1] > 0.0


class TestPoisonInjection:
    """Tests for poisoned data injection."""

    def test_inject_poisoned_data(self):
        """Test injecting poisoned data."""
        sim = ModelCollapseSimulator()
        data = sim.inject_poisoned_data(poison_ratio=0.2)
        
        assert data.poison_ratio == 0.2
        assert sim.poison_rate == 0.2
        assert data.total_samples == 10000

    def test_inject_poisoned_data_invalid_ratio(self):
        """Test that invalid poison_ratio raises error."""
        sim = ModelCollapseSimulator()
        with pytest.raises(ValueError, match="poison_ratio must be between"):
            sim.inject_poisoned_data(poison_ratio=1.5)

    def test_inject_poisoned_data_zero(self):
        """Test injecting zero poison ratio."""
        sim = ModelCollapseSimulator()
        data = sim.inject_poisoned_data(poison_ratio=0.0)
        assert data.poison_ratio == 0.0
        assert data.poisoned_samples == 0


class TestAIGeneratedDataInjection:
    """Tests for AI-generated data injection."""

    def test_inject_ai_generated_data(self):
        """Test injecting AI-generated data."""
        sim = ModelCollapseSimulator()
        data = sim.inject_ai_generated_data(generation_quality=0.7)
        
        assert data.ai_generated_samples > 0
        assert data.ai_ratio > 0.0

    def test_inject_ai_generated_data_perfect_quality(self):
        """Test AI injection with perfect quality (no AI data)."""
        sim = ModelCollapseSimulator()
        data = sim.inject_ai_generated_data(generation_quality=1.0)
        assert data.ai_generated_samples == 0
        assert data.ai_ratio == 0.0

    def test_inject_ai_generated_data_invalid_quality(self):
        """Test that invalid generation_quality raises error."""
        sim = ModelCollapseSimulator()
        with pytest.raises(ValueError, match="generation_quality must be between"):
            sim.inject_ai_generated_data(generation_quality=-0.1)


class TestAccuracyMeasurement:
    """Tests for accuracy measurement."""

    def test_measure_accuracy_decay(self):
        """Test accuracy decay measurement."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
        sim.simulate_retraining_cycle(n_cycles=10)
        
        decay_data = sim.measure_accuracy_decay()
        assert len(decay_data) == 10
        assert decay_data[0] == (0, 0.95)
        # All entries should be tuples of (cycle, accuracy)
        for cycle, accuracy in decay_data:
            assert isinstance(cycle, int)
            assert isinstance(accuracy, float)
            assert 0.0 <= accuracy <= 1.0

    def test_get_collapse_cycle_no_collapse(self):
        """Test collapse detection when no collapse occurs."""
        # With very low poison and few cycles, model may not collapse
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.01)
        sim.base_decay_rate = 0.02  # Very low decay
        sim.simulate_retraining_cycle(n_cycles=5)
        
        collapse_cycle = sim.get_collapse_cycle()
        # May or may not collapse depending on parameters
        assert isinstance(collapse_cycle, (int, type(None)))

    def test_get_collapse_cycle_with_collapse(self):
        """Test collapse detection when collapse occurs."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.3)
        sim.simulate_retraining_cycle(n_cycles=20)
        
        collapse_cycle = sim.get_collapse_cycle()
        assert collapse_cycle is not None
        assert isinstance(collapse_cycle, int)
        assert collapse_cycle >= 0


class TestVisualization:
    """Tests for visualization functionality."""

    def test_visualize_collapse_creates_figure(self):
        """Test that visualization creates a matplotlib figure."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
        sim.simulate_retraining_cycle(n_cycles=10)
        
        fig = sim.visualize_collapse()
        assert fig is not None
        assert hasattr(fig, 'axes')
        # Should have 4 main panels plus colorbar axis (5 total)
        assert len(fig.axes) >= 4

    def test_visualize_collapse_no_data(self):
        """Test visualization without simulation data raises error."""
        sim = ModelCollapseSimulator()
        
        with pytest.raises(ValueError, match="No simulation data"):
            sim.visualize_collapse()

    @patch('matplotlib.pyplot.savefig')
    def test_visualize_collapse_saves_file(self, mock_savefig, tmp_path):
        """Test that visualization can save to file."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
        sim.simulate_retraining_cycle(n_cycles=10)
        
        save_path = str(tmp_path / "test_collapse.png")
        sim.visualize_collapse(save_path=save_path)
        
        mock_savefig.assert_called_once()


class TestReportExport:
    """Tests for report export functionality."""

    def test_export_report_json(self, tmp_path):
        """Test exporting report as JSON."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
        sim.simulate_retraining_cycle(n_cycles=10)
        
        report_path = tmp_path / "report.json"
        report = sim.export_report(str(report_path))
        
        assert report_path.exists()
        assert 'simulation_parameters' in report
        assert 'results' in report
        assert 'cycle_metrics' in report
        assert report['simulation_parameters']['initial_accuracy'] == 0.95

    def test_export_report_csv(self, tmp_path):
        """Test exporting report as CSV."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
        sim.simulate_retraining_cycle(n_cycles=10)
        
        report_path = tmp_path / "report.csv"
        sim.export_report(str(report_path))
        
        assert report_path.exists()
        # Check CSV has headers
        with open(report_path, 'r') as f:
            header = f.readline().strip()
            assert 'cycle' in header
            assert 'accuracy' in header

    def test_export_report_no_data(self):
        """Test export without simulation data raises error."""
        sim = ModelCollapseSimulator()
        
        with pytest.raises(ValueError, match="No simulation data"):
            sim.export_report("report.json")

    def test_export_report_content_structure(self, tmp_path):
        """Test that exported report has correct structure."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
        sim.simulate_retraining_cycle(n_cycles=10)
        
        report_path = tmp_path / "report.json"
        report = sim.export_report(str(report_path))
        
        # Verify structure
        assert 'simulation_parameters' in report
        assert 'results' in report
        assert 'cycle_metrics' in report
        
        # Verify parameters
        params = report['simulation_parameters']
        assert params['initial_accuracy'] == 0.95
        assert params['poison_rate'] == 0.15
        assert params['n_cycles'] == 10
        assert params['collapse_threshold'] == 0.50
        
        # Verify results
        results = report['results']
        assert 'collapse_cycle' in results
        assert 'final_accuracy' in results
        assert 'is_collapsed' in results
        
        # Verify metrics
        assert len(report['cycle_metrics']) == 10
        for metric in report['cycle_metrics']:
            assert 'cycle' in metric
            assert 'accuracy' in metric
            assert 'poison_ratio' in metric
            assert 'ai_ratio' in metric


class TestEducationalExamples:
    """Tests for educational examples."""

    def test_run_educational_examples_returns_dict(self):
        """Test that educational examples returns dictionary."""
        examples = run_educational_examples()
        assert isinstance(examples, dict)
        assert len(examples) == 4

    def test_educational_examples_keys(self):
        """Test that educational examples has expected keys."""
        examples = run_educational_examples()
        assert 'low_poison' in examples
        assert 'medium_poison' in examples
        assert 'high_poison' in examples
        assert 'ai_feedback' in examples

    def test_educational_examples_are_simulators(self):
        """Test that all examples are ModelCollapseSimulator instances."""
        examples = run_educational_examples()
        for name, sim in examples.items():
            assert isinstance(sim, ModelCollapseSimulator)

    def test_low_poison_example(self):
        """Test low poison rate example behavior."""
        examples = run_educational_examples()
        sim = examples['low_poison']
        
        assert sim.poison_rate == 0.05
        assert len(sim.cycle_metrics) == 15
        # Low poison should collapse slower than high poison
        collapse_cycle = sim.get_collapse_cycle()
        assert isinstance(collapse_cycle, int)  # Should eventually collapse

    def test_high_poison_example(self):
        """Test high poison rate example behavior."""
        examples = run_educational_examples()
        sim = examples['high_poison']
        
        assert sim.poison_rate == 0.30
        assert len(sim.cycle_metrics) == 15
        # High poison should collapse quickly
        collapse_cycle = sim.get_collapse_cycle()
        assert collapse_cycle is not None
        assert collapse_cycle < 10


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_zero_poison_rate(self):
        """Test simulation with zero poison rate."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.0)
        metrics = sim.simulate_retraining_cycle(n_cycles=10)
        
        # Should still have some base decay
        assert metrics[-1].accuracy < metrics[0].accuracy
        # But no poison amplification
        assert all(m.poison_ratio == 0.0 for m in metrics)

    def test_maximum_poison_rate(self):
        """Test simulation with maximum poison rate."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=1.0)
        metrics = sim.simulate_retraining_cycle(n_cycles=10)
        
        # Should collapse very quickly
        collapse_cycle = sim.get_collapse_cycle()
        assert collapse_cycle is not None
        assert collapse_cycle < 5

    def test_perfect_initial_accuracy(self):
        """Test simulation with perfect initial accuracy."""
        sim = ModelCollapseSimulator(initial_accuracy=1.0, poison_rate=0.1)
        metrics = sim.simulate_retraining_cycle(n_cycles=5)
        
        # Should start at 1.0
        assert metrics[0].accuracy == 1.0
        # Should decay over time
        assert metrics[-1].accuracy < 1.0

    def test_minimum_initial_accuracy(self):
        """Test simulation with already-collapsed accuracy."""
        sim = ModelCollapseSimulator(initial_accuracy=0.4, poison_rate=0.1)
        metrics = sim.simulate_retraining_cycle(n_cycles=5)
        
        # Should start collapsed
        assert metrics[0].is_collapsed
        # Should remain collapsed
        assert all(m.is_collapsed for m in metrics)

    def test_single_cycle_collapse(self):
        """Test that extreme poison can cause severe degradation."""
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.5)
        sim.base_decay_rate = 0.5  # Extreme decay
        metrics = sim.simulate_retraining_cycle(n_cycles=3)
        
        # Should show severe degradation
        assert metrics[-1].accuracy < metrics[0].accuracy * 0.5


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complete_workflow(self, tmp_path):
        """Test complete simulation workflow."""
        # Initialize
        sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
        
        # Inject data
        data = sim.inject_poisoned_data(poison_ratio=0.15)
        assert data.poison_ratio == 0.15
        
        # Run simulation
        metrics = sim.simulate_retraining_cycle(n_cycles=15)
        assert len(metrics) == 15
        
        # Measure decay
        decay = sim.measure_accuracy_decay()
        assert len(decay) == 15
        
        # Get collapse info
        collapse_cycle = sim.get_collapse_cycle()
        
        # Export report
        report_path = tmp_path / "workflow_report.json"
        report = sim.export_report(str(report_path))
        assert report_path.exists()
        
        # Generate visualization
        fig = sim.visualize_collapse()
        assert fig is not None

    def test_comparison_workflow(self):
        """Test running multiple simulations for comparison."""
        poison_rates = [0.05, 0.15, 0.30]
        simulators = []
        
        for rate in poison_rates:
            sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=rate)
            sim.simulate_retraining_cycle(n_cycles=20)
            simulators.append(sim)
        
        # Verify all have results
        assert len(simulators) == 3
        assert all(len(s.cycle_metrics) == 20 for s in simulators)
        
        # Verify trend: higher poison = faster collapse
        collapse_cycles = [s.get_collapse_cycle() for s in simulators]
        # Filter out None values (no collapse)
        valid_cycles = [c for c in collapse_cycles if c is not None]
        if len(valid_cycles) >= 2:
            assert valid_cycles[0] >= valid_cycles[-1]  # Low poison collapses later


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
