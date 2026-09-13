"""
Test Suite for NIFLHEIM Countermeasure Toolkit

Comprehensive tests for defensive countermeasures including:
- Robust training pipelines
- Anomaly detection methods
- Model sanitization techniques
- Data validation pipeline
- Visualization methods
- Integration with attack modules

Educational Purpose:
    Ensure countermeasure toolkit functions correctly and safely.
    Validate defensive techniques against data poisoning attacks.

Author: NIFLHEIM Educational Systems
Date: 2026-09-13
"""

import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path
import json
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from maw.data_poisoning.countermeasures import (
    CountermeasureToolkit,
    RobustnessMetrics,
    DetectionResult,
    SanitizationReport,
    DataQualityReport,
    run_defensive_scenarios
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def toolkit():
    """Create a fresh CountermeasureToolkit instance."""
    return CountermeasureToolkit(random_state=42)


@pytest.fixture
def sample_dataset():
    """Create a sample dataset for testing."""
    np.random.seed(42)
    n_samples = 500
    n_features = 20
    X = np.random.randn(n_samples, n_features)
    y = np.random.randint(0, 10, n_samples)
    return X, y


@pytest.fixture
def sample_model():
    """Create a sample model dictionary."""
    return {
        'layer1': np.random.randn(100, 50),
        'layer2': np.random.randn(50, 10),
        'output': np.random.randn(10, 5)
    }


@pytest.fixture
def client_updates():
    """Create sample federated learning client updates."""
    np.random.seed(42)
    n_clients = 10
    n_features = 50
    updates = [np.random.randn(n_features) for _ in range(n_clients)]
    # Add 2 malicious clients
    updates[3] = np.random.randn(n_features) * 10
    updates[7] = np.random.randn(n_features) * 10
    return updates


# ============================================================================
# Test Data Classes
# ============================================================================

class TestRobustnessMetrics:
    """Test RobustnessMetrics dataclass."""
    
    def test_creation(self):
        """Test basic creation of RobustnessMetrics."""
        metrics = RobustnessMetrics(
            accuracy_under_attack=0.75,
            certification_radius=0.5,
            dp_epsilon=1.0,
            robust_accuracy=0.80,
            standard_accuracy=0.85
        )
        assert metrics.accuracy_under_attack == 0.75
        assert metrics.certification_radius == 0.5
        assert metrics.dp_epsilon == 1.0
        assert metrics.robust_accuracy == 0.80
        assert metrics.standard_accuracy == 0.85
    
    def test_robustness_improvement_calculation(self):
        """Test automatic calculation of robustness improvement."""
        metrics = RobustnessMetrics(
            accuracy_under_attack=0.75,
            certification_radius=0.5,
            dp_epsilon=1.0,
            robust_accuracy=0.80,
            standard_accuracy=0.85
        )
        expected = (0.80 - 0.75) / 0.85
        assert abs(metrics.robustness_improvement - expected) < 1e-6
    
    def test_robustness_improvement_zero_accuracy(self):
        """Test robustness improvement when standard accuracy is zero."""
        metrics = RobustnessMetrics(
            accuracy_under_attack=0.0,
            certification_radius=0.5,
            dp_epsilon=1.0,
            robust_accuracy=0.0,
            standard_accuracy=0.0
        )
        assert metrics.robustness_improvement == 0.0
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        metrics = RobustnessMetrics(
            accuracy_under_attack=0.75,
            certification_radius=0.5,
            dp_epsilon=1.0,
            robust_accuracy=0.80,
            standard_accuracy=0.85
        )
        d = metrics.to_dict()
        assert isinstance(d, dict)
        assert 'accuracy_under_attack' in d
        assert 'certification_radius' in d
        assert 'dp_epsilon' in d
        assert 'robust_accuracy' in d
        assert 'standard_accuracy' in d
        assert 'robustness_improvement' in d


class TestDetectionResult:
    """Test DetectionResult dataclass."""
    
    def test_creation(self):
        """Test basic creation of DetectionResult."""
        result = DetectionResult(
            detected_samples=[1, 5, 10],
            precision=0.85,
            recall=0.80,
            f1=0.82,
            false_positive_rate=0.05,
            detection_method='spectral_signature',
            total_samples=100
        )
        assert result.detected_samples == [1, 5, 10]
        assert result.precision == 0.85
        assert result.recall == 0.80
        assert result.f1 == 0.82
        assert result.false_positive_rate == 0.05
        assert result.detection_method == 'spectral_signature'
        assert result.total_samples == 100
    
    def test_num_detected_automatic(self):
        """Test automatic calculation of num_detected."""
        result = DetectionResult(
            detected_samples=[1, 5, 10, 15, 20],
            precision=0.85,
            recall=0.80,
            f1=0.82,
            false_positive_rate=0.05,
            detection_method='test',
            total_samples=100
        )
        assert result.num_detected == 5
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = DetectionResult(
            detected_samples=list(range(50)),  # More than 20
            precision=0.85,
            recall=0.80,
            f1=0.82,
            false_positive_rate=0.05,
            detection_method='test_method',
            total_samples=500
        )
        d = result.to_dict()
        assert isinstance(d, dict)
        assert len(d['detected_samples']) <= 20  # Limited for readability
        assert d['precision'] == 0.85
        assert d['num_detected'] == 50


class TestSanitizationReport:
    """Test SanitizationReport dataclass."""
    
    def test_creation(self):
        """Test basic creation of SanitizationReport."""
        report = SanitizationReport(
            pre_sanitization_accuracy=0.85,
            post_sanitization_accuracy=0.82,
            removed_components=100,
            quality_score=0.75,
            backdoor_success_rate_pre=0.90,
            backdoor_success_rate_post=0.15,
            sanitization_method='fine_pruning'
        )
        assert report.pre_sanitization_accuracy == 0.85
        assert report.post_sanitization_accuracy == 0.82
        assert report.removed_components == 100
        assert report.quality_score == 0.75
    
    def test_accuracy_change_calculation(self):
        """Test automatic calculation of accuracy change."""
        report = SanitizationReport(
            pre_sanitization_accuracy=0.85,
            post_sanitization_accuracy=0.82,
            removed_components=100,
            quality_score=0.75,
            backdoor_success_rate_pre=0.90,
            backdoor_success_rate_post=0.15,
            sanitization_method='test'
        )
        assert report.accuracy_change == -0.03
    
    def test_security_improvement_calculation(self):
        """Test automatic calculation of security improvement."""
        report = SanitizationReport(
            pre_sanitization_accuracy=0.85,
            post_sanitization_accuracy=0.82,
            removed_components=100,
            quality_score=0.75,
            backdoor_success_rate_pre=0.90,
            backdoor_success_rate_post=0.15,
            sanitization_method='test'
        )
        assert report.security_improvement == 0.75
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        report = SanitizationReport(
            pre_sanitization_accuracy=0.85,
            post_sanitization_accuracy=0.82,
            removed_components=100,
            quality_score=0.75,
            backdoor_success_rate_pre=0.90,
            backdoor_success_rate_post=0.15,
            sanitization_method='fine_pruning'
        )
        d = report.to_dict()
        assert isinstance(d, dict)
        assert 'pre_sanitization_accuracy' in d
        assert 'post_sanitization_accuracy' in d
        assert 'security_improvement' in d
        assert 'accuracy_change' in d


class TestDataQualityReport:
    """Test DataQualityReport dataclass."""
    
    def test_creation(self):
        """Test basic creation of DataQualityReport."""
        report = DataQualityReport(
            source_verified=True,
            label_consistency_score=0.92,
            feature_distribution_health=0.88,
            anomaly_score=0.08,
            overall_health_score=0.85,
            num_samples=1000,
            num_anomalies=50,
            recommendations=['Clean outliers', 'Verify labels'],
            validation_methods=['method1', 'method2']
        )
        assert report.source_verified is True
        assert report.label_consistency_score == 0.92
        assert report.overall_health_score == 0.85
        assert len(report.recommendations) == 2
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        report = DataQualityReport(
            source_verified=False,
            label_consistency_score=0.85,
            feature_distribution_health=0.80,
            anomaly_score=0.12,
            overall_health_score=0.75,
            num_samples=500,
            num_anomalies=30,
            recommendations=['Test recommendation'],
            validation_methods=['test_method']
        )
        d = report.to_dict()
        assert isinstance(d, dict)
        assert d['source_verified'] is False
        assert 'recommendations' in d
        assert 'validation_methods' in d


# ============================================================================
# Test Robust Training Pipelines
# ============================================================================

class TestRobustAggregation:
    """Test robust aggregation methods for federated learning."""
    
    def test_krum_aggregation(self, toolkit, client_updates):
        """Test Krum robust aggregation."""
        aggregated = toolkit.robust_aggregation(client_updates, method='krum', f=2)
        assert isinstance(aggregated, np.ndarray)
        assert aggregated.shape == (50,)
        # Krum should select a non-malicious update
        assert np.linalg.norm(aggregated) < 5.0  # Not one of the large malicious ones
    
    def test_trimmed_mean_aggregation(self, toolkit, client_updates):
        """Test trimmed mean aggregation."""
        aggregated = toolkit.robust_aggregation(client_updates, method='trimmed_mean', trim_ratio=0.2)
        assert isinstance(aggregated, np.ndarray)
        assert aggregated.shape == (50,)
        # Trimmed mean should reduce impact of malicious updates
    
    def test_median_aggregation(self, toolkit, client_updates):
        """Test median aggregation."""
        aggregated = toolkit.robust_aggregation(client_updates, method='median')
        assert isinstance(aggregated, np.ndarray)
        assert aggregated.shape == (50,)
        # Median is highly robust to outliers
    
    def test_invalid_method(self, toolkit, client_updates):
        """Test error on invalid method."""
        with pytest.raises(ValueError, match="Unknown method"):
            toolkit.robust_aggregation(client_updates, method='invalid_method')
    
    def test_empty_updates(self, toolkit):
        """Test error on empty client updates."""
        with pytest.raises(ValueError, match="cannot be empty"):
            toolkit.robust_aggregation([], method='krum')
    
    def test_invalid_f_parameter(self, toolkit, client_updates):
        """Test error when f >= n_clients."""
        with pytest.raises(ValueError):
            toolkit.robust_aggregation(client_updates, method='krum', f=15)
    
    def test_invalid_trim_ratio(self, toolkit, client_updates):
        """Test error on invalid trim ratio."""
        with pytest.raises(ValueError):
            toolkit.robust_aggregation(client_updates, method='trimmed_mean', trim_ratio=0.6)


class TestDifferentialPrivacy:
    """Test differential privacy training."""
    
    def test_dp_noise_addition(self, toolkit, sample_dataset):
        """Test differential privacy noise addition."""
        X, _ = sample_dataset
        noised_data, epsilon = toolkit.differential_privacy_training(X, epsilon=1.0)
        
        assert noised_data.shape == X.shape
        assert epsilon == 1.0
        # Noised data should be different from original
        assert not np.array_equal(noised_data, X)
        # But should be similar (noise is bounded)
        assert np.mean(np.abs(noised_data - X)) < 2.0
    
    def test_dp_different_epsilon(self, toolkit, sample_dataset):
        """Test DP with different epsilon values."""
        X, _ = sample_dataset
        
        noised_low, eps_low = toolkit.differential_privacy_training(X, epsilon=0.1)
        noised_high, eps_high = toolkit.differential_privacy_training(X, epsilon=10.0)
        
        # Lower epsilon = more noise
        noise_low = np.mean(np.abs(noised_low - X))
        noise_high = np.mean(np.abs(noised_high - X))
        assert noise_low > noise_high
    
    def test_invalid_epsilon(self, toolkit, sample_dataset):
        """Test error on invalid epsilon."""
        X, _ = sample_dataset
        with pytest.raises(ValueError, match="epsilon must be positive"):
            toolkit.differential_privacy_training(X, epsilon=0)
    
    def test_invalid_delta(self, toolkit, sample_dataset):
        """Test error on invalid delta."""
        X, _ = sample_dataset
        with pytest.raises(ValueError, match="delta must be in"):
            toolkit.differential_privacy_training(X, epsilon=1.0, delta=1.5)


class TestAdversarialTraining:
    """Test adversarial training for robustness."""
    
    def test_adversarial_training_basic(self, toolkit, sample_dataset, sample_model):
        """Test basic adversarial training."""
        X, y = sample_dataset
        result = toolkit.adversarial_training(sample_model, X, y, epsilon=0.1)
        
        assert 'model' in result
        assert 'perturbed_data' in result
        assert 'metrics' in result
        assert result['epsilon'] == 0.1
        assert result['perturbed_data'].shape == X.shape
    
    def test_pgd_adversaries(self, toolkit, sample_dataset):
        """Test PGD adversary generation."""
        X, _ = sample_dataset
        perturbed = toolkit._generate_pgd_adversaries(X, epsilon=0.1, steps=10, step_size=0.01)
        
        assert perturbed.shape == X.shape
        # Perturbation should be bounded by epsilon
        assert np.all(np.abs(perturbed - X) <= 0.1 + 1e-6)


class TestCertifiedDefenses:
    """Test randomized smoothing for certified robustness."""
    
    def test_randomized_smoothing(self, toolkit, sample_dataset):
        """Test randomized smoothing."""
        X, _ = sample_dataset
        result = toolkit.certified_defenses(None, X, sigma=0.5, n_samples=50)
        
        assert 'smoothed_data' in result
        assert 'certification_radius' in result
        assert result['smoothed_data'].shape == X.shape
        assert result['sigma'] == 0.5
        assert result['n_samples'] == 50
    
    def test_certification_radius(self, toolkit, sample_dataset):
        """Test certification radius computation."""
        X, _ = sample_dataset
        result1 = toolkit.certified_defenses(None, X, sigma=0.1)
        result2 = toolkit.certified_defenses(None, X, sigma=1.0)
        
        # Higher sigma should give larger certification radius
        assert result2['certification_radius'] > result1['certification_radius']


class TestRobustnessMeasurement:
    """Test robustness metrics measurement."""
    
    def test_measure_robustness(self, toolkit, sample_dataset):
        """Test robustness measurement."""
        X, y = sample_dataset
        metrics = toolkit.measure_robustness(None, X, y, attack_epsilon=0.1)
        
        assert isinstance(metrics, RobustnessMetrics)
        assert 0 <= metrics.standard_accuracy <= 1
        assert 0 <= metrics.robust_accuracy <= 1
        assert metrics.certification_radius >= 0
    
    def test_robustness_metrics_stored(self, toolkit, sample_dataset):
        """Test that robustness metrics are stored."""
        X, y = sample_dataset
        toolkit.measure_robustness(None, X, y)
        toolkit.measure_robustness(None, X, y)
        
        assert len(toolkit.robustness_metrics) == 2


# ============================================================================
# Test Anomaly Detection
# ============================================================================

class TestStatisticalOutlierDetection:
    """Test statistical outlier detection using Mahalanobis distance."""
    
    def test_outlier_detection_basic(self, toolkit, sample_dataset):
        """Test basic outlier detection."""
        X, _ = sample_dataset
        result = toolkit.statistical_outlier_detection(X)
        
        assert isinstance(result, DetectionResult)
        assert result.detection_method == 'mahalanobis_distance'
        assert result.total_samples == len(X)
        assert 0 <= result.precision <= 1
        assert 0 <= result.recall <= 1
    
    def test_outlier_detection_with_outliers(self, toolkit):
        """Test outlier detection with injected outliers."""
        np.random.seed(42)
        X_clean = np.random.randn(450, 20)
        X_outliers = np.random.randn(50, 20) + 5.0  # Clear outliers
        X = np.vstack([X_clean, X_outliers])
        
        result = toolkit.statistical_outlier_detection(X, threshold=3.0)
        
        # Should detect some outliers
        assert result.num_detected > 0
        # Should have reasonable precision
        assert result.precision > 0.3


class TestClusteringDetection:
    """Test clustering-based anomaly detection."""
    
    def test_clustering_detection_basic(self, toolkit, sample_dataset):
        """Test basic clustering-based detection."""
        X, y = sample_dataset
        result = toolkit.clustering_based_detection(X, y, k=5)
        
        assert isinstance(result, DetectionResult)
        assert result.detection_method == 'clustering_label_consistency'
        assert result.total_samples == len(X)
    
    def test_clustering_invalid_k(self, toolkit, sample_dataset):
        """Test error on invalid k."""
        X, y = sample_dataset
        with pytest.raises(ValueError, match="k must be >= 2"):
            toolkit.clustering_based_detection(X, y, k=1)
    
    def test_clustering_length_mismatch(self, toolkit):
        """Test error on dataset/labels length mismatch."""
        X = np.random.randn(100, 10)
        y = np.random.randint(0, 10, 50)
        with pytest.raises(ValueError, match="same length"):
            toolkit.clustering_based_detection(X, y)


class TestSpectralSignatureDetection:
    """Test spectral signature detection for poisoned samples."""
    
    def test_spectral_detection_basic(self, toolkit, sample_dataset):
        """Test basic spectral signature detection."""
        X, _ = sample_dataset
        result = toolkit.spectral_signature_detection(X, poison_ratio=0.1)
        
        assert isinstance(result, DetectionResult)
        assert result.detection_method == 'spectral_signature'
        assert result.total_samples == len(X)
    
    def test_spectral_detection_with_poisoned(self, toolkit):
        """Test spectral detection with injected poisoned samples."""
        np.random.seed(42)
        n_samples = 500
        X_clean = np.random.randn(450, 50)
        X_poisoned = np.random.randn(50, 50) + 3.0  # Distinct pattern
        X = np.vstack([X_clean, X_poisoned])
        
        result = toolkit.spectral_signature_detection(X, poison_ratio=0.1)
        
        # Should detect anomalous samples
        assert result.num_detected > 0


class TestInfluenceFunctionDetection:
    """Test influence function-based detection."""
    
    def test_influence_detection_basic(self, toolkit, sample_dataset):
        """Test basic influence function detection."""
        X, y = sample_dataset
        result = toolkit.influence_function_detection(None, X, y, top_k=10)
        
        assert isinstance(result, DetectionResult)
        assert result.detection_method == 'influence_functions'
        assert len(result.detected_samples) == 10


class TestNeuralCleanseDetection:
    """Test Neural Cleanse backdoor detection."""
    
    def test_neural_cleanse_basic(self, toolkit, sample_model):
        """Test basic Neural Cleanse detection."""
        result = toolkit.neural_cleanse_detection(sample_model)
        
        assert isinstance(result, DetectionResult)
        assert result.detection_method == 'neural_cleanse'
        # Should detect backdoor (class 7 is simulated as backdoored)
        assert result.precision > 0.5
    
    def test_neural_cleanse_with_trigger_dataset(self, toolkit, sample_model):
        """Test Neural Cleanse with trigger dataset."""
        trigger_dataset = np.random.randn(100, 20)
        result = toolkit.neural_cleanse_detection(sample_model, trigger_dataset)
        
        assert isinstance(result, DetectionResult)
        assert result.total_samples == 100


class TestDetectionAccuracyMeasurement:
    """Test detection accuracy measurement."""
    
    def test_measure_detection_accuracy_empty(self, toolkit):
        """Test measurement with no detection results."""
        metrics = toolkit.measure_detection_accuracy()
        
        assert metrics['avg_precision'] == 0.0
        assert metrics['avg_recall'] == 0.0
        assert metrics['avg_f1'] == 0.0
        assert metrics['num_detections'] == 0
    
    def test_measure_detection_accuracy_with_results(self, toolkit, sample_dataset):
        """Test measurement with detection results."""
        X, y = sample_dataset
        toolkit.statistical_outlier_detection(X)
        toolkit.spectral_signature_detection(X)
        
        metrics = toolkit.measure_detection_accuracy()
        
        assert metrics['num_detections'] == 2
        assert 'avg_precision' in metrics
        assert 'avg_recall' in metrics
        assert 'avg_f1' in metrics


# ============================================================================
# Test Model Sanitization
# ============================================================================

class TestFinePruning:
    """Test fine-pruning for backdoor removal."""
    
    def test_fine_pruning_basic(self, toolkit, sample_model):
        """Test basic fine-pruning."""
        report = toolkit.fine_pruning(sample_model, prune_ratio=0.1)
        
        assert isinstance(report, SanitizationReport)
        assert report.sanitization_method == 'fine_pruning'
        assert 0 <= report.quality_score <= 1
        assert report.removed_components > 0
    
    def test_fine_pruning_different_ratios(self, toolkit, sample_model):
        """Test fine-pruning with different ratios."""
        report1 = toolkit.fine_pruning(sample_model, prune_ratio=0.05)
        report2 = toolkit.fine_pruning(sample_model, prune_ratio=0.2)
        
        assert report2.removed_components > report1.removed_components


class TestModelDistillation:
    """Test knowledge distillation for sanitization."""
    
    def test_distillation_basic(self, toolkit, sample_model, sample_dataset):
        """Test basic model distillation."""
        X, _ = sample_dataset
        teacher = sample_model
        student = {
            'layer1': np.random.randn(100, 50) * 0.01,
            'layer2': np.random.randn(50, 10) * 0.01
        }
        
        report = toolkit.model_distillation(teacher, student, X, temperature=2.0)
        
        assert isinstance(report, SanitizationReport)
        assert report.sanitization_method == 'knowledge_distillation'
        assert 0 <= report.quality_score <= 1


class TestBackdoorRemoval:
    """Test backdoor removal techniques."""
    
    def test_backdoor_removal_fine_tuning(self, toolkit, sample_model):
        """Test backdoor removal via fine-tuning."""
        trigger_dataset = np.random.randn(50, 50)
        report = toolkit.backdoor_removal(sample_model, trigger_dataset, removal_method='fine_tuning')
        
        assert isinstance(report, SanitizationReport)
        assert 'fine_tuning' in report.sanitization_method
        assert report.security_improvement > 0
    
    def test_backdoor_removal_weight_pruning(self, toolkit, sample_model):
        """Test backdoor removal via weight pruning."""
        trigger_dataset = np.random.randn(50, 50)
        report = toolkit.backdoor_removal(sample_model, trigger_dataset, removal_method='weight_pruning')
        
        assert isinstance(report, SanitizationReport)
        assert 'weight_pruning' in report.sanitization_method
        assert report.removed_components > 0


class TestWeightClipping:
    """Test weight clipping for sanitization."""
    
    def test_weight_clipping_basic(self, toolkit, sample_model):
        """Test basic weight clipping."""
        report = toolkit.weight_clipping(sample_model, max_norm=1.0)
        
        assert isinstance(report, SanitizationReport)
        assert report.sanitization_method == 'weight_clipping'
        assert report.removed_components > 0
    
    def test_weight_clipping_different_norms(self, toolkit, sample_model):
        """Test weight clipping with different max norms."""
        report1 = toolkit.weight_clipping(sample_model, max_norm=0.5)
        report2 = toolkit.weight_clipping(sample_model, max_norm=2.0)
        
        # Both should produce reports
        assert isinstance(report1, SanitizationReport)
        assert isinstance(report2, SanitizationReport)


class TestSanitizationQualityMeasurement:
    """Test sanitization quality measurement."""
    
    def test_measure_quality_empty(self, toolkit):
        """Test quality measurement with no sanitizations."""
        metrics = toolkit.measure_sanitization_quality()
        
        assert metrics['avg_quality_score'] == 0.0
        assert metrics['num_sanitizations'] == 0
    
    def test_measure_quality_with_reports(self, toolkit, sample_model):
        """Test quality measurement with sanitization reports."""
        toolkit.fine_pruning(sample_model)
        toolkit.weight_clipping(sample_model)
        
        metrics = toolkit.measure_sanitization_quality()
        
        assert metrics['num_sanitizations'] == 2
        assert 0 <= metrics['avg_quality_score'] <= 1


# ============================================================================
# Test Data Validation Pipeline
# ============================================================================

class TestSourceValidation:
    """Test data source validation."""
    
    def test_validate_trusted_source(self, toolkit):
        """Test validation of trusted source."""
        result = toolkit.validate_data_source('official_dataset')
        assert result is True
    
    def test_validate_untrusted_source(self, toolkit):
        """Test validation of untrusted source."""
        result = toolkit.validate_data_source('unknown_random_source')
        assert result is False
    
    def test_validate_with_metadata(self, toolkit):
        """Test validation with complete metadata."""
        metadata = {
            'creator': 'test',
            'date': '2026-01-01',
            'license': 'MIT',
            'description': 'Test dataset'
        }
        result = toolkit.validate_data_source('test_source', metadata)
        # Should check metadata completeness
        assert isinstance(result, bool)


class TestLabelConsistency:
    """Test label consistency checking."""
    
    def test_label_consistency_basic(self, toolkit, sample_dataset):
        """Test basic label consistency check."""
        X, y = sample_dataset
        consistency, inconsistent = toolkit.check_label_consistency(X, y)
        
        assert 0 <= consistency <= 1
        assert isinstance(inconsistent, list)
        assert len(inconsistent) < len(y)
    
    def test_label_consistency_length_mismatch(self, toolkit):
        """Test error on length mismatch."""
        X = np.random.randn(100, 10)
        y = np.random.randint(0, 10, 50)
        with pytest.raises(ValueError, match="same length"):
            toolkit.check_label_consistency(X, y)


class TestFeatureDistributionAnalysis:
    """Test feature distribution analysis."""
    
    def test_feature_analysis_basic(self, toolkit, sample_dataset):
        """Test basic feature distribution analysis."""
        X, _ = sample_dataset
        result = toolkit.feature_distribution_analysis(X)
        
        assert 'mean_shift' in result
        assert 'variance_ratio' in result
        assert 'health_score' in result
        assert 0 <= result['health_score'] <= 1
    
    def test_feature_analysis_with_reference(self, toolkit, sample_dataset):
        """Test feature analysis with reference dataset."""
        X, _ = sample_dataset
        X_ref = np.random.randn(500, 20)
        
        result = toolkit.feature_distribution_analysis(X, X_ref)
        
        assert 'mean_shift' in result
        assert 'variance_ratio' in result


class TestCrossValidationAnomalyDetection:
    """Test cross-validation anomaly detection."""
    
    def test_cv_detection_basic(self, toolkit, sample_dataset):
        """Test basic CV anomaly detection."""
        X, y = sample_dataset
        result = toolkit.cross_validation_anomaly_detection(X, y, n_folds=5)
        
        assert isinstance(result, DetectionResult)
        assert result.detection_method == 'cross_validation_consistency'
        assert result.total_samples == len(X)


class TestDataQualityReport:
    """Test comprehensive data quality reporting."""
    
    def test_quality_report_basic(self, toolkit, sample_dataset):
        """Test basic data quality report."""
        X, y = sample_dataset
        report = toolkit.generate_data_quality_report(X, y, source='unknown')
        
        assert isinstance(report, DataQualityReport)
        assert report.source_verified is False  # Unknown source
        assert 0 <= report.overall_health_score <= 1
        assert len(report.recommendations) > 0
    
    def test_quality_report_verified_source(self, toolkit, sample_dataset):
        """Test quality report with verified source."""
        X, y = sample_dataset
        report = toolkit.generate_data_quality_report(X, y, source='official_dataset')
        
        assert isinstance(report, DataQualityReport)
        assert report.source_verified is True
    
    def test_quality_report_stored(self, toolkit, sample_dataset):
        """Test that quality reports are stored."""
        X, y = sample_dataset
        toolkit.generate_data_quality_report(X, y)
        toolkit.generate_data_quality_report(X, y)
        
        assert len(toolkit.data_quality_reports) == 2


# ============================================================================
# Test Visualization Methods
# ============================================================================

class TestVisualization:
    """Test visualization methods."""
    
    def test_plot_robustness_comparison(self, toolkit, sample_dataset):
        """Test robustness comparison plot."""
        X, y = sample_dataset
        toolkit.measure_robustness(None, X, y)
        toolkit.measure_robustness(None, X, y)
        
        fig = toolkit.plot_robustness_comparison(show=False)
        
        assert fig is not None
        assert isinstance(fig, plt.Figure)
    
    def test_plot_detection_precision_recall(self, toolkit, sample_dataset):
        """Test detection precision-recall plot."""
        X, _ = sample_dataset
        toolkit.statistical_outlier_detection(X)
        toolkit.spectral_signature_detection(X)
        
        fig = toolkit.plot_detection_precision_recall(show=False)
        
        assert fig is not None
        assert isinstance(fig, plt.Figure)
    
    def test_plot_sanitization_before_after(self, toolkit, sample_model):
        """Test sanitization before/after plot."""
        toolkit.fine_pruning(sample_model)
        toolkit.weight_clipping(sample_model)
        
        fig = toolkit.plot_sanitization_before_after(show=False)
        
        assert fig is not None
        assert isinstance(fig, plt.Figure)
    
    def test_plot_data_quality_heatmap(self, toolkit, sample_dataset):
        """Test data quality heatmap."""
        X, y = sample_dataset
        toolkit.generate_data_quality_report(X, y)
        toolkit.generate_data_quality_report(X, y, source='official_dataset')
        
        fig = toolkit.plot_data_quality_heatmap(show=False)
        
        assert fig is not None
        assert isinstance(fig, plt.Figure)
    
    def test_plot_empty_data(self, toolkit):
        """Test plotting with no data."""
        with pytest.raises(ValueError, match="No .* available"):
            toolkit.plot_robustness_comparison(show=False)


# ============================================================================
# Test Export and Utility Methods
# ============================================================================

class TestExportAndUtility:
    """Test export and utility methods."""
    
    def test_export_report(self, toolkit, sample_dataset, sample_model, tmp_path):
        """Test report export to JSON."""
        X, y = sample_dataset
        
        # Generate some data
        toolkit.measure_robustness(None, X, y)
        toolkit.statistical_outlier_detection(X)
        toolkit.fine_pruning(sample_model)
        toolkit.generate_data_quality_report(X, y)
        
        output_path = tmp_path / "test_report.json"
        report = toolkit.export_report(str(output_path))
        
        assert output_path.exists()
        assert 'summary' in report
        assert 'robustness_metrics' in report
        assert 'detection_results' in report
        assert 'sanitization_reports' in report
        assert 'data_quality_reports' in report
    
    def test_reset(self, toolkit, sample_dataset, sample_model):
        """Test toolkit reset."""
        X, y = sample_dataset
        
        # Generate some data
        toolkit.measure_robustness(None, X, y)
        toolkit.fine_pruning(sample_model)
        
        assert len(toolkit.robustness_metrics) > 0
        assert len(toolkit.sanitization_reports) > 0
        
        toolkit.reset()
        
        assert len(toolkit.robustness_metrics) == 0
        assert len(toolkit.sanitization_reports) == 0


# ============================================================================
# Test Defensive Scenarios
# ============================================================================

class TestDefensiveScenarios:
    """Test comprehensive defensive scenarios."""
    
    def test_run_defensive_scenarios(self):
        """Test running all defensive scenarios."""
        results = run_defensive_scenarios()
        
        assert isinstance(results, dict)
        assert 'robust_fl' in results
        assert 'spectral_detection' in results
        assert 'fine_pruning' in results
        assert 'adversarial_training' in results
        assert 'data_validation' in results
    
    def test_defensive_scenarios_output(self, capsys):
        """Test defensive scenarios console output."""
        run_defensive_scenarios()
        captured = capsys.readouterr()
        
        assert "NIFLHEIM Countermeasure Toolkit" in captured.out
        assert "Scenario 1" in captured.out
        assert "Scenario 2" in captured.out
        assert "Scenario 3" in captured.out
        assert "Scenario 4" in captured.out
        assert "Scenario 5" in captured.out


# ============================================================================
# Test Integration with Attack Modules (Simulated)
# ============================================================================

class TestAttackDefenseIntegration:
    """Test integration between attack and defense modules."""
    
    def test_simulated_backdoor_workflow(self, toolkit):
        """Test simulated backdoor attack-defense workflow."""
        # Simulate backdoored model
        backdoored_model = {
            'layer1': np.random.randn(100, 50),
            'layer2': np.random.randn(50, 10)
        }
        
        # Detect backdoor
        detection = toolkit.neural_cleanse_detection(backdoored_model)
        
        # Remove backdoor
        trigger_dataset = np.random.randn(50, 50)
        report = toolkit.backdoor_removal(backdoored_model, trigger_dataset)
        
        # Verify detection and removal
        assert detection.precision > 0.5
        assert report.security_improvement > 0.5
    
    def test_simulated_poison_detection_workflow(self, toolkit):
        """Test simulated poisoning detection workflow."""
        # Create dataset with poisoned samples
        np.random.seed(42)
        X_clean = np.random.randn(900, 50)
        X_poisoned = np.random.randn(100, 50) + 3.0
        X = np.vstack([X_clean, X_poisoned])
        
        # Detect using multiple methods
        result1 = toolkit.statistical_outlier_detection(X)
        result2 = toolkit.spectral_signature_detection(X, poison_ratio=0.1)
        
        # Both should detect anomalies
        assert result1.num_detected > 0
        assert result2.num_detected > 0


# ============================================================================
# Test Performance and Edge Cases
# ============================================================================

class TestPerformanceAndEdgeCases:
    """Test performance and edge cases."""
    
    def test_large_dataset(self, toolkit):
        """Test with large dataset."""
        np.random.seed(42)
        X = np.random.randn(5000, 100)
        
        result = toolkit.statistical_outlier_detection(X)
        
        assert isinstance(result, DetectionResult)
        assert result.total_samples == 5000
    
    def test_small_dataset(self, toolkit):
        """Test with very small dataset."""
        X = np.random.randn(10, 5)
        
        result = toolkit.statistical_outlier_detection(X)
        
        assert isinstance(result, DetectionResult)
    
    def test_single_feature(self, toolkit):
        """Test with single feature."""
        X = np.random.randn(100, 1)
        
        result = toolkit.feature_distribution_analysis(X)
        
        assert 'health_score' in result
    
    def test_high_dimensional(self, toolkit):
        """Test with high-dimensional data."""
        X = np.random.randn(100, 500)
        
        result = toolkit.statistical_outlier_detection(X)
        
        assert isinstance(result, DetectionResult)
    
    def test_reproducibility(self, toolkit, sample_dataset):
        """Test reproducibility with fixed random state."""
        X, y = sample_dataset
        
        toolkit1 = CountermeasureToolkit(random_state=42)
        toolkit2 = CountermeasureToolkit(random_state=42)
        
        result1 = toolkit1.statistical_outlier_detection(X)
        result2 = toolkit2.statistical_outlier_detection(X)
        
        # Should produce same results with same seed
        assert result1.detected_samples == result2.detected_samples
    
    def test_multiple_runs_accumulate(self, toolkit, sample_dataset):
        """Test that multiple runs accumulate results."""
        X, y = sample_dataset
        
        toolkit.measure_robustness(None, X, y)
        toolkit.measure_robustness(None, X, y)
        toolkit.measure_robustness(None, X, y)
        
        assert len(toolkit.robustness_metrics) == 3


# ============================================================================
# Test Safety and Ethics
# ============================================================================

class TestSafetyAndEthics:
    """Test safety and ethical considerations."""
    
    def test_educational_purpose_documentation(self):
        """Test that module has educational purpose documentation."""
        from maw.data_poisoning import countermeasures
        assert countermeasures.__doc__ is not None
        assert "Educational" in countermeasures.__doc__
        assert "DEFENSIVE" in countermeasures.__doc__
    
    def test_defensive_focus(self, toolkit):
        """Test that toolkit focuses on defensive measures."""
        # All methods should be defensive
        methods = [
            'robust_aggregation',
            'differential_privacy_training',
            'adversarial_training',
            'statistical_outlier_detection',
            'fine_pruning',
            'backdoor_removal'
        ]
        
        for method in methods:
            assert hasattr(toolkit, method)


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
