# NIFLHEIM Data Poisoning Module Integration Guide

## Overview

The NIFLHEIM Data Poisoning toolkit demonstrates vulnerabilities in machine learning systems to data poisoning attacks. This educational suite includes:

- **Model Collapse**: Simulator for demonstrating model collapse from poisoned data
- **Adtech Fragility**: Simulator for adtech ecosystem vulnerabilities
- **Advanced Poisoning**: Advanced ML poisoning (FL attacks, transfer backdoors, cross-modal, meta-learning)

All modules use synthetic data and include safety controls for educational use only.

## Installation

The module is part of the NIFLHEIM data poisoning toolkit:

```python
from maw.data_poisoning import AdtechFragilitySimulator
```

## Quick Start

```python
from maw.data_poisoning import AdtechFragilitySimulator

# Initialize simulator
sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)

# Run RTB auctions
auction_results = sim.simulate_rtb_auction()

# Inject signal pollution (30% noise)
pollution_metrics = sim.inject_signal_pollution(pollution_ratio=0.3)

# Disrupt cookie syncing (20% failure rate)
sync_results = sim.poison_cookie_syncing(sync_ratio=0.2)

# Measure ecosystem fragility
metrics = sim.measure_ecosystem_fragility()
print(f"Ecosystem Fragility: {sim.ecosystem_fragility:.3f}")
print(f"Risk Level: {sim._get_risk_level(sim.ecosystem_fragility)}")

# Generate visualization
sim.visualize_impact(save_path="adtech_fragility_analysis.png")

# Export report
report = sim.export_report("adtech_fragility_report.json")
```

## Educational Scenarios

Run predefined scenarios demonstrating different pollution levels:

```python
from maw.data_poisoning import run_educational_scenarios

results = run_educational_scenarios()

for scenario_name, scenario_results in results.items():
    print(f"\n{scenario_name.upper()}:")
    print(f"  Fragility: {scenario_results['ecosystem_fragility']:.3f}")
    print(f"  Risk Level: {scenario_results['risk_level']}")
```

### Available Scenarios

1. **Low Pollution (10%)**: Minimal impact on ecosystem
   - Signal pollution: 10%
   - Cookie disruption: 0%
   - Expected fragility: < 0.3 (LOW risk)

2. **Medium Pollution (25%)**: Moderate degradation
   - Signal pollution: 25%
   - Cookie disruption: 10%
   - Expected fragility: 0.3-0.5 (MODERATE risk)

3. **High Pollution (50%)**: Severe ecosystem stress
   - Signal pollution: 50%
   - Cookie disruption: 30%
   - Expected fragility: 0.5-0.7 (HIGH risk)

4. **Coordinated Attack**: Multiple vectors simultaneously
   - Signal pollution: 50%
   - Cookie disruption: 50%
   - Expected fragility: > 0.7 (CRITICAL risk)

## API Reference

### AdtechFragilitySimulator

Main simulator class for adtech ecosystem analysis.

#### Constructor

```python
AdtechFragilitySimulator(ecosystem_config='default', seed=None)
```

**Parameters:**
- `ecosystem_config`: str - Configuration preset ('default', 'fragmented', 'consolidated')
- `seed`: int - Random seed for reproducibility

**Ecosystem Configurations:**
- `default`: 8 bidders, 75% base match rate, 85% base signal quality
- `fragmented`: 15 bidders, 45% base match rate, 60% base signal quality
- `consolidated`: 4 bidders, 85% base match rate, 92% base signal quality

#### Methods

##### simulate_rtb_auction(bid_requests=None)

Simulate real-time bidding auctions.

**Parameters:**
- `bid_requests`: List[BidRequest] - Optional custom bid requests

**Returns:** List[AuctionResult]

**Example:**
```python
results = sim.simulate_rtb_auction()
print(f"Total auctions: {len(results)}")
print(f"Avg clearing price: ${np.mean([r.clearing_price for r in results]):.2f}")
```

##### inject_signal_pollution(pollution_ratio=0.1)

Inject noise into tracking signals.

**Parameters:**
- `pollution_ratio`: float - Ratio of signals to pollute (0.0 to 1.0)

**Returns:** Dict with pollution metrics

**Pollution Types:**
- Clickstream noise injection
- User agent spoofing
- Referrer pollution
- Timestamp jitter

**Example:**
```python
metrics = sim.inject_signal_pollution(0.3)
print(f"Signals affected: {metrics['total_signals_affected']}")
```

##### poison_cookie_syncing(sync_ratio=0.2)

Disrupt cookie synchronization between domains.

**Parameters:**
- `sync_ratio`: float - Ratio of sync attempts to disrupt (0.0 to 1.0)

**Returns:** Dict with sync metrics

**Example:**
```python
results = sim.poison_cookie_syncing(0.4)
print(f"Match rate before: {results['match_rate_before']:.2f}")
print(f"Match rate after: {results['match_rate_after']:.2f}")
```

##### measure_ecosystem_fragility()

Calculate comprehensive ecosystem fragility metrics.

**Returns:** SignalMetrics

**Metrics Tracked:**
- User identification accuracy
- Conversion attribution reliability
- ROI calculation distortion
- Audience segmentation quality
- Cookie match rate
- Signal-to-noise ratio

**Example:**
```python
metrics = sim.measure_ecosystem_fragility()
print(f"User ID Accuracy: {metrics.user_identification_accuracy:.3f}")
print(f"Attribution Reliability: {metrics.conversion_attribution_reliability:.3f}")
print(f"ROI Distortion: {metrics.roi_calculation_distortion:.3f}")
```

##### visualize_impact(save_path=None)

Generate matplotlib visualizations.

**Parameters:**
- `save_path`: str - Optional path to save figure

**Returns:** matplotlib.Figure

**Visualization Panels:**
1. RTB auction flow diagram
2. Signal pollution impact over time
3. Cookie sync match rate degradation
4. Ecosystem fragility heatmap

**Example:**
```python
fig = sim.visualize_impact(save_path="fragility_analysis.png")
```

##### export_report(output_path)

Generate comprehensive JSON/CSV report.

**Parameters:**
- `output_path`: str - Path to save report (.json or .csv)

**Returns:** Dict with report data

**Report Sections:**
- Simulation metadata
- Auction summary statistics
- Cookie sync summary
- Signal metrics time series
- Bidder performance analysis
- Fragility assessment with recommendations

**Example:**
```python
report = sim.export_report("adtech_report.json")
print(f"Risk Level: {report['fragility_assessment']['risk_level']}")
print(f"Recommendations: {report['fragility_assessment']['recommendations']}")
```

### Data Classes

#### BidRequest

Represents an RTB auction request.

```python
BidRequest(
    impression_id="imp_001",
    user_id="user_123",
    publisher_domain="example.com",
    ad_format="banner",
    placement="above_fold",
    device_type="desktop",
    geo_location=("US", "CA"),
    context_keywords=["tech", "news"],
    timestamp=datetime.utcnow(),
    user_data={"age": "25-34", "interests": ["tech"]}
)
```

#### BidResponse

Represents a bidder's response to an auction.

```python
BidResponse(
    bidder_id="bidder_001",
    impression_id="imp_001",
    bid_amount=5.50,
    ad_creative_id="creative_123",
    targeting_score=0.85,
    win_probability=0.70,
    response_time_ms=45.2
)
```

#### AuctionResult

Result of a completed RTB auction.

```python
AuctionResult(
    impression_id="imp_001",
    winning_bidder="bidder_001",
    winning_bid=7.50,
    clearing_price=6.25,  # Second-price auction
    bid_count=5,
    auction_duration_ms=78.3
)
```

#### SignalMetrics

Ecosystem health metrics.

```python
SignalMetrics(
    timestamp=datetime.utcnow(),
    user_identification_accuracy=0.85,
    conversion_attribution_reliability=0.78,
    roi_calculation_distortion=0.22,
    audience_segmentation_quality=0.72,
    cookie_match_rate=0.68,
    signal_to_noise_ratio=3.5
)
```

### BidderAgent

Simulates individual bidder behavior.

```python
from maw.data_poisoning import BidderAgent

agent = BidderAgent(
    bidder_id="my_bidder",
    bidder_type="aggressive",  # aggressive, conservative, premium, budget, programmatic
    seed=42
)

# Generate bid
bid = agent.generate_bid(bid_request)

# Record result
agent.record_auction_result(won=True, price=5.50)

# Access statistics
print(f"Total wins: {agent.total_wins}")
print(f"Total spend: ${agent.total_spend:.2f}")
print(f"Win rate: {agent.total_wins / len(agent.win_history):.2%}")
```

## Integration with Existing Modules

### Model Collapse Simulator

Combine adtech fragility with model collapse analysis:

```python
from maw.data_poisoning import (
    AdtechFragilitySimulator,
    ModelCollapseSimulator
)

# Run adtech simulation
adtech_sim = AdtechFragilitySimulator(seed=42)
adtech_sim.simulate_rtb_auction()
adtech_sim.inject_signal_pollution(0.3)
adtech_metrics = adtech_sim.measure_ecosystem_fragility()

# Use degraded signal quality as input to model collapse
model_sim = ModelCollapseSimulator(
    initial_accuracy=adtech_metrics.user_identification_accuracy,
    poison_rate=adtech_metrics.roi_calculation_distortion
)
model_sim.simulate_retraining_cycle(n_cycles=10)

# Analyze combined impact
print(f"Adtech Fragility: {adtech_sim.ecosystem_fragility:.3f}")
print(f"Model Collapse Cycle: {model_sim.collapse_cycle}")
```

### Core Data Poisoning Pipeline

Integrate with core poisoning operations:

```python
from maw.data_poisoning.core import DataPoisoningPipeline
from maw.data_poisoning import AdtechFragilitySimulator

# Create poisoning pipeline
pipeline = DataPoisoningPipeline(seed=42)

# Create adtech simulator
sim = AdtechFragilitySimulator(seed=42)

# Coordinate poisoning across systems
sim.simulate_rtb_auction()
sim.inject_signal_pollution(0.3)

# Use pipeline for additional poisoning
polluted_data = pipeline.poison_form_data(
    form_fields={"user_id": "123", "email": "test@example.com"},
    use_synthetic=True
)

print(f"Adtech fragility: {sim.ecosystem_fragility:.3f}")
print(f"Form data poisoned: {len(polluted_data)} fields")
```

## Risk Level Assessment

The module automatically assesses ecosystem risk based on fragility score:

| Fragility Score | Risk Level | Description |
|----------------|------------|-------------|
| < 0.3 | LOW | Ecosystem operating normally |
| 0.3 - 0.5 | MODERATE | Noticeable degradation |
| 0.5 - 0.7 | HIGH | Severe ecosystem stress |
| > 0.7 | CRITICAL | Ecosystem approaching collapse |

```python
risk_level = sim._get_risk_level(sim.ecosystem_fragility)
print(f"Risk Level: {risk_level}")
```

## Recommendations

The module generates context-aware recommendations:

```python
report = sim.export_report("report.json")
recommendations = report['fragility_assessment']['recommendations']

for rec in recommendations:
    print(f"- {rec}")
```

**Example Recommendations:**
- "Implement signal validation to detect and filter polluted data"
- "Diversify identity resolution methods beyond cookie syncing"
- "Ecosystem approaching collapse threshold - reduce dependency on fragile signals"

## Testing

Run the comprehensive test suite:

```bash
cd DarkEmpire_Systems/MAW_INSTALLATION
pytest src/maw/data_poisoning/test_adtech_fragility.py -v
```

Test coverage includes:
- BidRequest, BidResponse, AuctionResult dataclasses
- CookieSyncRecord, SignalMetrics dataclasses
- BidderAgent behavior and strategies
- AdtechFragilitySimulator core functionality
- Signal pollution injection
- Cookie sync disruption
- Ecosystem fragility measurement
- Visualization generation
- Report export (JSON/CSV)
- Educational scenarios
- Edge cases and error handling
- Integration with other modules
- Reproducibility with seeds

## Visualization Output

The `visualize_impact()` method generates a 4-panel figure:

1. **RTB Auction Flow**: Diagram showing auction participants and flow
2. **Signal Pollution Impact**: Time series of metric degradation
3. **Cookie Sync Degradation**: Match rate vs disruption ratio
4. **Ecosystem Fragility Heatmap**: Fragility across pollution/disruption space

```python
sim.visualize_impact(save_path="analysis.png")
```

## Export Formats

### JSON Report

Comprehensive report with all simulation data:

```json
{
  "simulation_metadata": {
    "ecosystem_config": "default",
    "timestamp": "2026-09-13T19:07:32Z",
    "pollution_ratio": 0.3,
    "sync_disruption_ratio": 0.3,
    "ecosystem_fragility": 0.542
  },
  "auction_summary": {
    "total_auctions": 100,
    "avg_clearing_price": 6.45,
    "avg_bid_count": 7.2
  },
  "fragility_assessment": {
    "overall_fragility": 0.542,
    "risk_level": "HIGH",
    "recommendations": [...]
  }
}
```

### CSV Report

Time series metrics for analysis in spreadsheet tools:

```csv
timestamp,user_identification_accuracy,conversion_attribution_reliability,roi_calculation_distortion,audience_segmentation_quality,cookie_match_rate,signal_to_noise_ratio
2026-09-13T19:07:32,0.85,0.78,0.22,0.72,0.68,3.5
...
```

## Best Practices

1. **Use seeds for reproducibility**: Always set `seed` parameter for reproducible results
2. **Run multiple scenarios**: Compare low/medium/high pollution to understand impact ranges
3. **Visualize results**: Use `visualize_impact()` to communicate findings effectively
4. **Export reports**: Save JSON reports for documentation and further analysis
5. **Integrate with other modules**: Combine with model collapse for comprehensive analysis

## Troubleshooting

### Issue: Visualization not saving

**Solution**: Ensure matplotlib backend is configured:
```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
```

### Issue: Report export fails

**Solution**: Check file path permissions and extension:
```python
# Use absolute path
report = sim.export_report("/full/path/to/report.json")

# Ensure .json or .csv extension
```

### Issue: Inconsistent results

**Solution**: Set random seed for reproducibility:
```python
sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
```

## Further Reading

- Addie LaMarr, "Data Poisoning: The Fatal Flaw in Mass Surveillance"
- Research on RTB ecosystem vulnerabilities
- Academic literature on adtech signal pollution
- Cookie sync disruption studies

## License

Educational use only. Part of NIFLHEIM Educational Systems.
