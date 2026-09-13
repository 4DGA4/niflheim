"""
Model Collapse Simulator for NIFLHEIM

Demonstrates how AI training data becomes "AI-generated sludge" through feedback loops,
as discussed in Addie LaMarr's "Data Poisoning: The Fatal Flaw in Mass Surveillance".

This module simulates and visualizes model collapse from poisoned/AI-generated training data,
showing feedback loop degradation, accuracy decay, and poison amplification over retraining cycles.

Educational Purpose:
    - Demonstrate feedback loop degradation (model outputs become training inputs)
    - Show accuracy decay curves (exponential/logistic decline)
    - Illustrate poison amplification (small initial rates compound)
    - Identify model collapse threshold (<50% accuracy)
    - Show recovery difficulty once collapsed

Author: NIFLHEIM Educational Systems
Date: 2026-09-13
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


@dataclass
class TrainingData:
    """Represents a training dataset with clean, poisoned, and AI-generated samples."""
    clean_samples: int
    poisoned_samples: int
    ai_generated_samples: int
    total_samples: int = field(init=False)
    poison_ratio: float = field(init=False)
    ai_ratio: float = field(init=False)

    def __post_init__(self):
        self.total_samples = self.clean_samples + self.poisoned_samples + self.ai_generated_samples
        if self.total_samples > 0:
            self.poison_ratio = self.poisoned_samples / self.total_samples
            self.ai_ratio = self.ai_generated_samples / self.total_samples
        else:
            self.poison_ratio = 0.0
            self.ai_ratio = 0.0


@dataclass
class CycleMetrics:
    """Metrics captured at each retraining cycle."""
    cycle_number: int
    accuracy: float
    poison_ratio: float
    ai_ratio: float
    total_samples: int
    is_collapsed: bool = False


@dataclass
class CollapseReport:
    """Complete report of a model collapse simulation."""
    initial_accuracy: float
    poison_rate: float
    n_cycles: int
    collapse_cycle: Optional[int]
    final_accuracy: float
    metrics: List[CycleMetrics]
    recovery_attempts: int = 0
    recovery_success: bool = False


class ModelCollapseSimulator:
    """
    Simulates model collapse from poisoned/AI-generated training data.

    This simulator demonstrates how AI models degrade when trained on their own outputs
    or poisoned data, creating a feedback loop that compounds errors over retraining cycles.

    Attributes:
        initial_accuracy: Starting model accuracy (0.0 to 1.0)
        poison_rate: Initial ratio of poisoned data in training set (0.0 to 1.0)
        current_accuracy: Current model accuracy after retraining
        cycle_metrics: List of metrics from each retraining cycle
    """

    def __init__(self, initial_accuracy: float = 0.95, poison_rate: float = 0.1):
        """
        Initialize the Model Collapse Simulator.

        Args:
            initial_accuracy: Starting model accuracy (default: 0.95)
            poison_rate: Initial ratio of poisoned data (default: 0.1 = 10%)

        Raises:
            ValueError: If parameters are outside valid ranges
        """
        if not 0.0 <= initial_accuracy <= 1.0:
            raise ValueError(f"initial_accuracy must be between 0.0 and 1.0, got {initial_accuracy}")
        if not 0.0 <= poison_rate <= 1.0:
            raise ValueError(f"poison_rate must be between 0.0 and 1.0, got {poison_rate}")

        self.initial_accuracy = initial_accuracy
        self.poison_rate = poison_rate
        self.current_accuracy = initial_accuracy
        self.cycle_metrics: List[CycleMetrics] = []
        self.training_data: Optional[TrainingData] = None
        self.collapse_threshold = 0.50  # Model is collapsed when accuracy < 50%

        # Simulation parameters
        self.base_decay_rate = 0.15  # Base accuracy decay per cycle
        self.poison_amplification = 2.5  # How much poison amplifies decay
        self.ai_decay_factor = 0.08  # Additional decay from AI-generated data
        self.recovery_difficulty = 0.95  # Multiplier for recovery attempts

    def simulate_retraining_cycle(self, n_cycles: int = 10) -> List[CycleMetrics]:
        """
        Run multiple retraining iterations to simulate model degradation.

        Each cycle:
        1. Measures current accuracy
        2. Injects poisoned/AI-generated data
        3. Retrains model (simulated by accuracy decay)
        4. Records metrics

        Args:
            n_cycles: Number of retraining cycles to simulate (default: 10)

        Returns:
            List of CycleMetrics for each cycle
        """
        self.cycle_metrics = []
        current_poison_ratio = self.poison_rate
        current_ai_ratio = 0.0

        for cycle in range(n_cycles):
            # Measure accuracy before this cycle's degradation
            accuracy = self.current_accuracy
            is_collapsed = accuracy < self.collapse_threshold

            # Record metrics
            metrics = CycleMetrics(
                cycle_number=cycle,
                accuracy=accuracy,
                poison_ratio=current_poison_ratio,
                ai_ratio=current_ai_ratio,
                total_samples=self.training_data.total_samples if self.training_data else 0,
                is_collapsed=is_collapsed
            )
            self.cycle_metrics.append(metrics)

            # Apply accuracy decay based on poison and AI ratios
            decay = self._calculate_decay(current_poison_ratio, current_ai_ratio)
            self.current_accuracy = max(0.0, self.current_accuracy - decay)

            # Amplify poison ratio for next cycle (feedback loop)
            current_poison_ratio = self._amplify_poison(current_poison_ratio)
            current_ai_ratio = self._amplify_ai_generation(current_ai_ratio, current_poison_ratio)

        return self.cycle_metrics

    def _calculate_decay(self, poison_ratio: float, ai_ratio: float) -> float:
        """
        Calculate accuracy decay for a retraining cycle.

        Uses exponential decay model:
        decay = base_decay * (1 + poison_amplification * poison_ratio) + ai_decay * ai_ratio

        Args:
            poison_ratio: Current ratio of poisoned data
            ai_ratio: Current ratio of AI-generated data

        Returns:
            Accuracy decay value (0.0 to 1.0)
        """
        base_decay = self.base_decay_rate
        poison_component = base_decay * self.poison_amplification * poison_ratio
        ai_component = self.ai_decay_factor * ai_ratio

        # Exponential increase in decay as model degrades
        degradation_multiplier = 1.0 + (1.0 - self.current_accuracy) * 0.5

        total_decay = (base_decay + poison_component + ai_component) * degradation_multiplier
        return min(total_decay, 0.5)  # Cap decay at 50% per cycle

    def _amplify_poison(self, current_ratio: float) -> float:
        """
        Amplify poison ratio through feedback loop.

        Simulates how model errors become training data, compounding poison.

        Args:
            current_ratio: Current poison ratio

        Returns:
            Amplified poison ratio for next cycle
        """
        # Poison amplifies based on model's current accuracy
        # Lower accuracy = more errors = more poison in next iteration
        amplification = current_ratio * (1.0 + self.poison_amplification * (1.0 - self.current_accuracy))
        return min(amplification, 0.95)  # Cap at 95%

    def _amplify_ai_generation(self, current_ai_ratio: float, poison_ratio: float) -> float:
        """
        Amplify AI-generated data ratio through feedback loop.

        As model degrades, it generates more AI content that gets used as training data.

        Args:
            current_ai_ratio: Current AI-generated data ratio
            poison_ratio: Current poison ratio (affects AI generation quality)

        Returns:
            Amplified AI ratio for next cycle
        """
        # AI generation increases as model relies more on synthetic data
        ai_growth = 0.15  # Base growth rate
        ai_from_poison = poison_ratio * 0.3  # Poison leads to more AI generation

        new_ai_ratio = current_ai_ratio + ai_growth + ai_from_poison
        return min(new_ai_ratio, 0.90)  # Cap at 90%

    def inject_poisoned_data(self, poison_ratio: float = 0.1) -> TrainingData:
        """
        Add poisoned samples to the training set.

        Simulates adversarial data injection or contaminated data sources.

        Args:
            poison_ratio: Ratio of poisoned samples to inject (0.0 to 1.0)

        Returns:
            Updated TrainingData object

        Raises:
            ValueError: If poison_ratio is outside valid range
        """
        if not 0.0 <= poison_ratio <= 1.0:
            raise ValueError(f"poison_ratio must be between 0.0 and 1.0, got {poison_ratio}")

        base_samples = 10000
        poisoned_count = int(base_samples * poison_ratio)
        clean_count = base_samples - poisoned_count

        self.training_data = TrainingData(
            clean_samples=clean_count,
            poisoned_samples=poisoned_count,
            ai_generated_samples=0
        )

        self.poison_rate = poison_ratio
        return self.training_data

    def inject_ai_generated_data(self, generation_quality: float = 0.8) -> TrainingData:
        """
        Add AI-generated samples to the training set.

        Simulates models being trained on their own outputs or other AI-generated content.

        Args:
            generation_quality: Quality of AI-generated data (0.0 to 1.0, where 1.0 = perfect)

        Returns:
            Updated TrainingData object

        Raises:
            ValueError: If generation_quality is outside valid range
        """
        if not 0.0 <= generation_quality <= 1.0:
            raise ValueError(f"generation_quality must be between 0.0 and 1.0, got {generation_quality}")

        base_samples = 10000
        ai_ratio = 1.0 - generation_quality  # Lower quality = more AI data

        ai_count = int(base_samples * ai_ratio)
        clean_count = int((base_samples - ai_count) * (1.0 - self.poison_rate))
        poisoned_count = base_samples - clean_count - ai_count

        self.training_data = TrainingData(
            clean_samples=clean_count,
            poisoned_samples=poisoned_count,
            ai_generated_samples=ai_count
        )

        return self.training_data

    def measure_accuracy_decay(self) -> List[Tuple[int, float]]:
        """
        Track accuracy degradation over cycles.

        Returns:
            List of (cycle_number, accuracy) tuples
        """
        return [(m.cycle_number, m.accuracy) for m in self.cycle_metrics]

    def get_collapse_cycle(self) -> Optional[int]:
        """
        Find the cycle where model collapse occurred.

        Returns:
            Cycle number where accuracy dropped below threshold, or None if no collapse
        """
        for metrics in self.cycle_metrics:
            if metrics.is_collapsed:
                return metrics.cycle_number
        return None

    def visualize_collapse(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Generate matplotlib plot showing model collapse.

        Creates a multi-panel visualization:
        1. Accuracy vs. retraining cycle (line plot)
        2. Poison ratio vs. cycle (line plot)
        3. Heatmap: poison ratio vs. collapse speed

        Args:
            save_path: Optional path to save the figure

        Returns:
            matplotlib Figure object
        """
        if not self.cycle_metrics:
            raise ValueError("No simulation data. Run simulate_retraining_cycle() first.")

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Model Collapse Simulation - NIFLHEIM Educational Systems', fontsize=14, fontweight='bold')

        # Panel 1: Accuracy decay over cycles
        ax1 = axes[0, 0]
        cycles = [m.cycle_number for m in self.cycle_metrics]
        accuracies = [m.accuracy for m in self.cycle_metrics]

        ax1.plot(cycles, accuracies, 'b-', linewidth=2, marker='o', markersize=6)
        ax1.axhline(y=self.collapse_threshold, color='r', linestyle='--',
                   label=f'Collapse Threshold ({self.collapse_threshold:.0%})')
        ax1.fill_between(cycles, accuracies, self.collapse_threshold,
                        where=np.array(accuracies) < self.collapse_threshold,
                        alpha=0.3, color='red', label='Collapsed Region')

        ax1.set_xlabel('Retraining Cycle')
        ax1.set_ylabel('Model Accuracy')
        ax1.set_title('Accuracy Decay Over Retraining Cycles')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 1.05)

        # Panel 2: Poison ratio evolution
        ax2 = axes[0, 1]
        poison_ratios = [m.poison_ratio for m in self.cycle_metrics]
        ai_ratios = [m.ai_ratio for m in self.cycle_metrics]

        ax2.plot(cycles, poison_ratios, 'r-', linewidth=2, marker='s', markersize=6, label='Poison Ratio')
        ax2.plot(cycles, ai_ratios, 'g-', linewidth=2, marker='^', markersize=6, label='AI-Generated Ratio')

        ax2.set_xlabel('Retraining Cycle')
        ax2.set_ylabel('Data Ratio')
        ax2.set_title('Poison and AI-Generated Data Amplification')
        ax2.legend(loc='upper left')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1.0)

        # Panel 3: Heatmap of poison ratio vs. collapse speed
        ax3 = axes[1, 0]
        poison_rates = np.linspace(0.01, 0.5, 20)
        decay_rates = np.linspace(0.05, 0.3, 20)
        collapse_speeds = np.zeros((len(poison_rates), len(decay_rates)))

        for i, pr in enumerate(poison_rates):
            for j, dr in enumerate(decay_rates):
                # Simulate quick collapse calculation
                temp_sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=pr)
                temp_sim.base_decay_rate = dr
                temp_sim.simulate_retraining_cycle(n_cycles=20)
                collapse_cycle = temp_sim.get_collapse_cycle()
                collapse_speeds[i, j] = collapse_cycle if collapse_cycle else 20

        im = ax3.imshow(collapse_speeds, origin='lower', aspect='auto',
                       cmap='RdYlGn_r', extent=[decay_rates.min(), decay_rates.max(),
                                               poison_rates.min(), poison_rates.max()])
        ax3.set_xlabel('Base Decay Rate')
        ax3.set_ylabel('Initial Poison Rate')
        ax3.set_title('Poison Rate vs. Decay Rate\n(Collapse Cycle - Lower = Faster Collapse)')
        plt.colorbar(im, ax=ax3, label='Cycle to Collapse')

        # Panel 4: Recovery difficulty visualization
        ax4 = axes[1, 1]
        recovery_cycles = []
        recovery_accuracies = []

        # Simulate recovery attempts
        if self.cycle_metrics:
            final_metrics = self.cycle_metrics[-1]
            if final_metrics.is_collapsed:
                recovery_acc = final_metrics.accuracy
                for attempt in range(10):
                    recovery_acc *= self.recovery_difficulty
                    recovery_acc += 0.02  # Small improvement per attempt
                    recovery_cycles.append(attempt)
                    recovery_accuracies.append(min(recovery_acc, 0.95))

                ax4.plot(recovery_cycles, recovery_accuracies, 'm-', linewidth=2, marker='d', markersize=6)
                ax4.axhline(y=self.collapse_threshold, color='r', linestyle='--',
                           label='Recovery Threshold')
                ax4.set_xlabel('Recovery Attempt')
                ax4.set_ylabel('Accuracy')
                ax4.set_title('Recovery Difficulty After Collapse')
                ax4.legend(loc='lower right')
                ax4.grid(True, alpha=0.3)
            else:
                ax4.text(0.5, 0.5, 'No Collapse\nNo Recovery Needed',
                        ha='center', va='center', fontsize=12, transform=ax4.transAxes)
                ax4.set_xlim(0, 10)
                ax4.set_ylim(0, 1)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Visualization saved to: {save_path}")

        return fig

    def export_report(self, output_path: str) -> Dict[str, Any]:
        """
        Generate JSON/CSV report of collapse dynamics.

        Creates a comprehensive report including:
        - Simulation parameters
        - Cycle-by-cycle metrics
        - Collapse analysis
        - Recovery statistics

        Args:
            output_path: Path to save the report (JSON or CSV based on extension)

        Returns:
            Dictionary containing the report data

        Raises:
            ValueError: If no simulation data exists
        """
        if not self.cycle_metrics:
            raise ValueError("No simulation data. Run simulate_retraining_cycle() first.")

        collapse_cycle = self.get_collapse_cycle()
        final_accuracy = self.cycle_metrics[-1].accuracy if self.cycle_metrics else 0.0

        report = CollapseReport(
            initial_accuracy=self.initial_accuracy,
            poison_rate=self.poison_rate,
            n_cycles=len(self.cycle_metrics),
            collapse_cycle=collapse_cycle,
            final_accuracy=final_accuracy,
            metrics=self.cycle_metrics
        )

        # Convert to dictionary for JSON export
        report_dict = {
            'simulation_parameters': {
                'initial_accuracy': self.initial_accuracy,
                'poison_rate': self.poison_rate,
                'n_cycles': len(self.cycle_metrics),
                'collapse_threshold': self.collapse_threshold
            },
            'results': {
                'collapse_cycle': collapse_cycle,
                'final_accuracy': final_accuracy,
                'is_collapsed': final_accuracy < self.collapse_threshold,
                'cycles_to_collapse': collapse_cycle if collapse_cycle else 'N/A'
            },
            'cycle_metrics': [
                {
                    'cycle': m.cycle_number,
                    'accuracy': round(m.accuracy, 4),
                    'poison_ratio': round(m.poison_ratio, 4),
                    'ai_ratio': round(m.ai_ratio, 4),
                    'is_collapsed': m.is_collapsed
                }
                for m in self.cycle_metrics
            ]
        }

        # Export based on file extension
        # Handle relative paths by making them relative to MAW_INSTALLATION/outputs/reports
        path = Path(output_path)
        if not path.is_absolute():
            output_dir = Path(__file__).parent.parent.parent.parent / "outputs" / "reports"
            output_dir.mkdir(parents=True, exist_ok=True)
            path = output_dir / path.name

        if path.suffix.lower() == '.json':
            with open(path, 'w') as f:
                json.dump(report_dict, f, indent=2)
        elif path.suffix.lower() == '.csv':
            import csv
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['cycle', 'accuracy', 'poison_ratio', 'ai_ratio', 'is_collapsed'])
                for m in self.cycle_metrics:
                    writer.writerow([m.cycle_number, round(m.accuracy, 4),
                                   round(m.poison_ratio, 4), round(m.ai_ratio, 4), m.is_collapsed])
        else:
            # Default to JSON
            json_path = path.with_suffix('.json')
            with open(json_path, 'w') as f:
                json.dump(report_dict, f, indent=2)
            path = json_path

        print(f"Report exported to: {path}")
        return report_dict


def run_educational_examples() -> Dict[str, ModelCollapseSimulator]:
    """
    Run educational examples demonstrating different collapse scenarios.

    Examples:
    1. Low poison rate (5%) - slow collapse
    2. Medium poison rate (15%) - moderate collapse
    3. High poison rate (30%) - rapid collapse
    4. AI-generated data feedback loop

    Returns:
        Dictionary mapping example names to their simulators
    """
    examples = {}

    # Example 1: Low poison rate (5%)
    print("\n" + "="*60)
    print("Example 1: Low Poison Rate (5%) - Slow Collapse")
    print("="*60)
    sim1 = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.05)
    sim1.inject_poisoned_data(poison_ratio=0.05)
    sim1.simulate_retraining_cycle(n_cycles=15)
    examples['low_poison'] = sim1

    collapse_cycle = sim1.get_collapse_cycle()
    print(f"Initial Accuracy: {sim1.initial_accuracy:.1%}")
    print(f"Poison Rate: {sim1.poison_rate:.1%}")
    print(f"Final Accuracy: {sim1.cycle_metrics[-1].accuracy:.1%}")
    print(f"Collapsed at cycle: {collapse_cycle if collapse_cycle else 'Did not collapse'}")

    # Example 2: Medium poison rate (15%)
    print("\n" + "="*60)
    print("Example 2: Medium Poison Rate (15%) - Moderate Collapse")
    print("="*60)
    sim2 = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
    sim2.inject_poisoned_data(poison_ratio=0.15)
    sim2.simulate_retraining_cycle(n_cycles=15)
    examples['medium_poison'] = sim2

    collapse_cycle = sim2.get_collapse_cycle()
    print(f"Initial Accuracy: {sim2.initial_accuracy:.1%}")
    print(f"Poison Rate: {sim2.poison_rate:.1%}")
    print(f"Final Accuracy: {sim2.cycle_metrics[-1].accuracy:.1%}")
    print(f"Collapsed at cycle: {collapse_cycle if collapse_cycle else 'Did not collapse'}")

    # Example 3: High poison rate (30%)
    print("\n" + "="*60)
    print("Example 3: High Poison Rate (30%) - Rapid Collapse")
    print("="*60)
    sim3 = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.30)
    sim3.inject_poisoned_data(poison_ratio=0.30)
    sim3.simulate_retraining_cycle(n_cycles=15)
    examples['high_poison'] = sim3

    collapse_cycle = sim3.get_collapse_cycle()
    print(f"Initial Accuracy: {sim3.initial_accuracy:.1%}")
    print(f"Poison Rate: {sim3.poison_rate:.1%}")
    print(f"Final Accuracy: {sim3.cycle_metrics[-1].accuracy:.1%}")
    print(f"Collapsed at cycle: {collapse_cycle if collapse_cycle else 'Did not collapse'}")

    # Example 4: AI-generated data feedback loop
    print("\n" + "="*60)
    print("Example 4: AI-Generated Data Feedback Loop")
    print("="*60)
    sim4 = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.10)
    sim4.inject_ai_generated_data(generation_quality=0.8)
    sim4.simulate_retraining_cycle(n_cycles=15)
    examples['ai_feedback'] = sim4

    collapse_cycle = sim4.get_collapse_cycle()
    print(f"Initial Accuracy: {sim4.initial_accuracy:.1%}")
    print(f"AI Generation Quality: 80%")
    print(f"Final Accuracy: {sim4.cycle_metrics[-1].accuracy:.1%}")
    print(f"Final AI Ratio: {sim4.cycle_metrics[-1].ai_ratio:.1%}")
    print(f"Collapsed at cycle: {collapse_cycle if collapse_cycle else 'Did not collapse'}")

    # Generate combined visualization
    print("\n" + "="*60)
    print("Generating comparative visualization...")
    print("="*60)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = {'low_poison': 'green', 'medium_poison': 'orange',
              'high_poison': 'red', 'ai_feedback': 'purple'}
    labels = {
        'low_poison': 'Low Poison (5%)',
        'medium_poison': 'Medium Poison (15%)',
        'high_poison': 'High Poison (30%)',
        'ai_feedback': 'AI Feedback Loop'
    }

    for name, sim in examples.items():
        cycles = [m.cycle_number for m in sim.cycle_metrics]
        accuracies = [m.accuracy for m in sim.cycle_metrics]
        ax.plot(cycles, accuracies, color=colors[name], linewidth=2,
               marker='o', markersize=4, label=labels[name])

    ax.axhline(y=0.5, color='red', linestyle='--', label='Collapse Threshold (50%)')
    ax.set_xlabel('Retraining Cycle', fontsize=12)
    ax.set_ylabel('Model Accuracy', fontsize=12)
    ax.set_title('Model Collapse Comparison - Educational Examples\n'
                'NIFLHEIM Data Poisoning Simulator', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)

    # Save comparison plot
    output_dir = Path(__file__).parent.parent.parent.parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    comparison_path = output_dir / "model_collapse_comparison.png"
    plt.savefig(comparison_path, dpi=150, bbox_inches='tight')
    print(f"Comparison plot saved to: {comparison_path}")

    return examples


if __name__ == "__main__":
    """
    Main execution: Run educational examples and generate visualizations.
    """
    print("\n" + "="*70)
    print(" NIFLHEIM Model Collapse Simulator")
    print(" Educational Module: Data Poisoning & AI Feedback Loops")
    print("="*70)
    print("\nBased on: Addie LaMarr - 'Data Poisoning: The Fatal Flaw in Mass Surveillance'")
    print("Concept: AI training data becomes 'AI-generated sludge' through feedback loops\n")

    # Run educational examples
    examples = run_educational_examples()

    # Export reports for each example
    print("\n" + "="*60)
    print("Exporting detailed reports...")
    print("="*60)

    for name, sim in examples.items():
        report_path = f"MAW_INSTALLATION/outputs/reports/{name}_report.json"
        sim.export_report(report_path)

    print("\n" + "="*70)
    print(" Simulation Complete")
    print("="*70)
    print("\nKey Findings:")
    print("- Higher poison rates lead to faster model collapse")
    print("- AI-generated data feedback loops compound degradation")
    print("- Recovery after collapse is extremely difficult")
    print("- Small initial poison rates (<5%) still cause eventual collapse")
    print("\nEducational Takeaway:")
    print("Mass surveillance systems that train on internet data risk model collapse")
    print("as AI-generated content pollutes the training pool. This is the 'fatal flaw'.")
    print("="*70 + "\n")
