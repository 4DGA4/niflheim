# NIFLHEIM Model Collapse Simulator - Integration Guide

## Overview

The Model Collapse Simulator is an educational module that demonstrates how AI training data becomes "AI-generated sludge" through feedback loops. This concept was popularized by Addie LaMarr in her video "Data Poisoning: The Fatal Flaw in Mass Surveillance" (785K views).

**Purpose**: Educational demonstration of model collapse dynamics in AI systems that train on internet data, showing how AI-generated content pollutes the training pool and leads to catastrophic accuracy degradation.

## Installation

### Prerequisites

```bash
pip install numpy matplotlib pytest
```

### Package Structure

```
MAW_INSTALLATION/
├── src/
│   └── maw/
│       ├── __init__.py
│       └── data_poisoning/
│           ├── __init__.py
│           └── model_collapse.py
├── tests/
│   ├── conftest.py
│   └── test_model_collapse.py
└── outputs/
    ├── model_collapse_comparison.png
    └── reports/
        ├── low_poison_report.json
        ├── medium_poison_report.json
        ├── high_poison_report.json
        └── ai_feedback_report.json
```

## Quick Start

### Basic Usage

```python
from maw.data_poisoning import ModelCollapseSimulator

# Initialize simulator
sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.1)

# Run simulation
sim.simulate_retraining_cycle(n_cycles=10)

# Visualize results
sim.visualize_collapse(save_path="collapse.png")

# Export report
report = sim.export_report("report.json")
```

### Educational Examples

```python
from maw.data_poisoning import run_educational_examples

# Run all educational examples
examples = run_educational_examples()

# Access individual simulators
low_poison_sim = examples['low_poison']
high_poison_sim = examples['high_poison']
```

## API Reference

### ModelCollapseSimulator

#### Constructor

```python
ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.1)
```

**Parameters:**
- `initial_accuracy` (float): Starting model accuracy (0.0 to 1.0)
- `poison_rate` (float): Initial ratio of poisoned data (0.0 to 1.0)

**Raises:**
- `ValueError`: If parameters are outside valid ranges

#### Methods

##### `simulate_retraining_cycle(n_cycles=10)`

Run multiple retraining iterations to simulate model degradation.

**Parameters:**
- `n_cycles` (int): Number of retraining cycles (default: 10)

**Returns:**
- `List[CycleMetrics]`: Metrics for each cycle

**Example:**
```python
metrics = sim.simulate_retraining_cycle(n_cycles=15)
for m in metrics:
    print(f"Cycle {m.cycle_number}: Accuracy = {m.accuracy:.2%}")
```

##### `inject_poisoned_data(poison_ratio=0.1)`

Add poisoned samples to the training set.

**Parameters:**
- `poison_ratio` (float): Ratio of poisoned samples (0.0 to 1.0)

**Returns:**
- `TrainingData`: Updated training data object

**Example:**
```python
data = sim.inject_poisoned_data(poison_ratio=0.2)
print(f"Poison ratio: {data.poison_ratio:.1%}")
```

##### `inject_ai_generated_data(generation_quality=0.8)`

Add AI-generated samples to the training set.

**Parameters:**
- `generation_quality` (float): Quality of AI-generated data (0.0 to 1.0)

**Returns:**
- `TrainingData`: Updated training data object

**Example:**
```python
data = sim.inject_ai_generated_data(generation_quality=0.7)
print(f"AI-generated ratio: {data.ai_ratio:.1%}")
```

##### `measure_accuracy_decay()`

Track accuracy degradation over cycles.

**Returns:**
- `List[Tuple[int, float]]`: List of (cycle, accuracy) tuples

**Example:**
```python
decay = sim.measure_accuracy_decay()
for cycle, accuracy in decay:
    print(f"Cycle {cycle}: {accuracy:.2%}")
```

##### `visualize_collapse(save_path=None)`

Generate matplotlib visualization of model collapse.

**Parameters:**
- `save_path` (str, optional): Path to save the figure

**Returns:**
- `matplotlib.figure.Figure`: The generated figure

**Example:**
```python
fig = sim.visualize_collapse(save_path="collapse_visualization.png")
plt.show()
```

##### `export_report(output_path)`

Generate JSON/CSV report of collapse dynamics.

**Parameters:**
- `output_path` (str): Path to save the report (.json or .csv)

**Returns:**
- `Dict`: Report data dictionary

**Example:**
```python
report = sim.export_report("simulation_report.json")
print(f"Collapsed at cycle: {report['results']['collapse_cycle']}")
```

### Data Classes

#### TrainingData

```python
@dataclass
class TrainingData:
    clean_samples: int
    poisoned_samples: int
    ai_generated_samples: int
    total_samples: int  # computed
    poison_ratio: float  # computed
    ai_ratio: float  # computed
```

#### CycleMetrics

```python
@dataclass
class CycleMetrics:
    cycle_number: int
    accuracy: float
    poison_ratio: float
    ai_ratio: float
    total_samples: int
    is_collapsed: bool
```

#### CollapseReport

```python
@dataclass
class CollapseReport:
    initial_accuracy: float
    poison_rate: float
    n_cycles: int
    collapse_cycle: Optional[int]
    final_accuracy: float
    metrics: List[CycleMetrics]
    recovery_attempts: int
    recovery_success: bool
```

## Educational Examples

### Example 1: Low Poison Rate (5%) - Slow Collapse

```python
sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.05)
sim.inject_poisoned_data(poison_ratio=0.05)
sim.simulate_retraining_cycle(n_cycles=15)

print(f"Final accuracy: {sim.cycle_metrics[-1].accuracy:.1%}")
print(f"Collapsed: {sim.get_collapse_cycle() is not None}")
```

**Expected Behavior:**
- Gradual accuracy decline
- May not collapse within 15 cycles
- Demonstrates that even small poison rates are dangerous long-term

### Example 2: Medium Poison Rate (15%) - Moderate Collapse

```python
sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
sim.inject_poisoned_data(poison_ratio=0.15)
sim.simulate_retraining_cycle(n_cycles=15)

collapse_cycle = sim.get_collapse_cycle()
print(f"Collapsed at cycle: {collapse_cycle}")
```

**Expected Behavior:**
- Noticeable accuracy decline
- Collapse typically occurs around cycles 8-12
- Shows compounding effect of feedback loops

### Example 3: High Poison Rate (30%) - Rapid Collapse

```python
sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.30)
sim.inject_poisoned_data(poison_ratio=0.30)
sim.simulate_retraining_cycle(n_cycles=15)

collapse_cycle = sim.get_collapse_cycle()
print(f"Rapid collapse at cycle: {collapse_cycle}")
```

**Expected Behavior:**
- Severe accuracy decline
- Collapse typically occurs within 3-7 cycles
- Demonstrates catastrophic failure mode

### Example 4: AI-Generated Data Feedback Loop

```python
sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.10)
sim.inject_ai_generated_data(generation_quality=0.8)
sim.simulate_retraining_cycle(n_cycles=15)

final_ai_ratio = sim.cycle_metrics[-1].ai_ratio
print(f"Final AI-generated ratio: {final_ai_ratio:.1%}")
```

**Expected Behavior:**
- AI ratio grows over cycles
- Accuracy declines as AI content dominates
- Shows self-reinforcing degradation loop

## Visualization

The `visualize_collapse()` method generates a 4-panel figure:

1. **Accuracy Decay**: Line plot showing accuracy vs. retraining cycle
2. **Poison Amplification**: Line plot showing poison and AI ratios over cycles
3. **Heatmap**: Poison ratio vs. decay rate showing collapse speed
4. **Recovery Difficulty**: Shows how hard it is to recover after collapse

### Customizing Visualizations

```python
import matplotlib.pyplot as plt

sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.15)
sim.simulate_retraining_cycle(n_cycles=15)

fig = sim.visualize_collapse()
fig.suptitle("Custom Title", fontsize=16)
plt.savefig("custom.png", dpi=300, bbox_inches='tight')
plt.show()
```

## Report Export

### JSON Format

```json
{
  "simulation_parameters": {
    "initial_accuracy": 0.95,
    "poison_rate": 0.15,
    "n_cycles": 10,
    "collapse_threshold": 0.50
  },
  "results": {
    "collapse_cycle": 8,
    "final_accuracy": 0.32,
    "is_collapsed": true,
    "cycles_to_collapse": 8
  },
  "cycle_metrics": [
    {
      "cycle": 0,
      "accuracy": 0.95,
      "poison_ratio": 0.15,
      "ai_ratio": 0.0,
      "is_collapsed": false
    }
    // ... more cycles
  ]
}
```

### CSV Format

```csv
cycle,accuracy,poison_ratio,ai_ratio,is_collapsed
0,0.95,0.15,0.0,False
1,0.88,0.22,0.05,False
...
```

## Integration with DataPoisoningPipeline

The simulator is designed to be compatible with the `DataPoisoningPipeline` (future module):

```python
from maw.data_poisoning import ModelCollapseSimulator, DataPoisoningPipeline

# Create simulator
sim = ModelCollapseSimulator(initial_accuracy=0.95, poison_rate=0.1)

# Integrate with pipeline (future)
pipeline = DataPoisoningPipeline()
pipeline.add_simulator(sim)
pipeline.run()
```

## Testing

### Run All Tests

```bash
cd MAW_INSTALLATION
pytest tests/test_model_collapse.py -v
```

### Run Specific Test Classes

```bash
# Test initialization
pytest tests/test_model_collapse.py::TestModelCollapseSimulatorInitialization -v

# Test simulation
pytest tests/test_model_collapse.py::TestSimulationCycles -v

# Test visualization
pytest tests/test_model_collapse.py::TestVisualization -v
```

### Test Coverage

The test suite includes:
- **TrainingData tests**: 4 tests
- **CycleMetrics tests**: 2 tests
- **Initialization tests**: 5 tests
- **Simulation tests**: 6 tests
- **Poison injection tests**: 3 tests
- **AI injection tests**: 3 tests
- **Accuracy measurement tests**: 3 tests
- **Visualization tests**: 3 tests
- **Report export tests**: 4 tests
- **Educational examples tests**: 5 tests
- **Edge cases tests**: 5 tests
- **Integration tests**: 2 tests

**Total: 45+ tests**

## Key Concepts Demonstrated

### 1. Feedback Loop Degradation

Model outputs become training inputs, creating a self-reinforcing cycle:

```
Model → Generates Output → Output becomes Training Data → Model Retrains → Repeat
```

Each cycle compounds errors from previous cycles.

### 2. Accuracy Decay Curve

Accuracy follows an exponential/logistic decline:

```
Accuracy(t) = Initial × e^(-decay_rate × t)
```

Where decay_rate increases with poison ratio.

### 3. Poison Amplification

Small initial poison rates compound exponentially:

```
Poison(t+1) = Poison(t) × (1 + amplification × (1 - Accuracy))
```

Lower accuracy → more errors → more poison amplification.

### 4. Model Collapse Threshold

The model becomes unusable when accuracy drops below 50%:

```python
collapse_threshold = 0.50
is_collapsed = accuracy < collapse_threshold
```

### 5. Recovery Difficulty

Recovery after collapse is extremely difficult:

```python
recovery_accuracy = collapsed_accuracy × recovery_difficulty + small_improvement
```

Where `recovery_difficulty < 1.0`, making recovery nearly impossible.

## Educational Takeaways

1. **Mass surveillance systems that train on internet data risk model collapse** as AI-generated content pollutes the training pool.

2. **Even small poison rates (<5%) cause eventual collapse** - the feedback loop ensures compounding degradation.

3. **AI-generated data feedback loops are particularly dangerous** because they're self-reinforcing and accelerate over time.

4. **Recovery after collapse is nearly impossible** - prevention is far easier than correction.

5. **This is the "fatal flaw"** in surveillance systems that rely on internet-scale training data.

## Limitations and Future Enhancements

### Current Limitations

1. **Simplified decay model**: Uses exponential decay rather than complex neural network dynamics
2. **Single accuracy metric**: Real models have multiple performance dimensions
3. **No architecture effects**: Doesn't model different model architectures (transformers, CNNs, etc.)
4. **Synthetic data**: Uses simulated data rather than real poisoned datasets

### Future Enhancements

1. **Real dataset integration**: Test on actual poisoned datasets (e.g., LLaMA-2-7b fine-tuned on synthetic data)
2. **Multi-metric evaluation**: Track precision, recall, F1, perplexity
3. **Architecture-specific models**: Different decay rates for different model types
4. **Intervention strategies**: Test data cleaning, human curation, synthetic data detection
5. **Interactive visualizations**: Plotly-based interactive plots for educational use
6. **Real-time simulation**: Web-based interactive simulator for demonstrations

## Troubleshooting

### Common Issues

**Issue**: "No module named 'maw'"
**Solution**: Ensure `MAW_INSTALLATION/src` is in your Python path:
```python
import sys
sys.path.insert(0, "MAW_INSTALLATION/src")
```

**Issue**: Visualization not displaying
**Solution**: Call `plt.show()` after `visualize_collapse()`:
```python
fig = sim.visualize_collapse()
plt.show()
```

**Issue**: Report export fails
**Solution**: Ensure parent directory exists:
```python
from pathlib import Path
Path("outputs/reports").mkdir(parents=True, exist_ok=True)
sim.export_report("outputs/reports/report.json")
```

## Citation

When using this module in educational contexts, cite:

```
NIFLHEIM Educational Systems. (2026). Model Collapse Simulator.
Based on concepts from: LaMarr, A. (2024). "Data Poisoning: The Fatal Flaw in Mass Surveillance."
```

## License

Educational use only. Part of the NIFLHEIM educational suite for demonstrating AI safety concepts.
