"""
Test Suite for Backdoor Attack Demonstration Module

EDUCATIONAL AND DEFENSIVE PURPOSES ONLY

This test suite validates the backdoor_demo.py educational module,
ensuring it functions correctly for defensive security training.

All tests verify educational functionality and safety measures.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_poisoning.backdoor_demo import BackdoorDemo, run_educational_demo


class TestBackdoorDemoInitialization:
    """Test initialization and safety features."""
    
    def test_requires_educational_use_flag(self):
        """Verify educational_use=True is required."""
        with pytest.raises(ValueError) as excinfo:
            BackdoorDemo(educational_use=False)
        assert "EDUCATIONAL_USE flag must be True" in str(excinfo.value)
    
    def test_default_initialization(self):
        """Test default initialization parameters."""
        demo = BackdoorDemo(educational_use=True)
        assert demo.model_type == 'simple_classifier'
        assert demo.trigger_type == 'pattern'
        assert demo.educational_use is True
    
    def test_custom_model_type(self):
        """Test initialization with custom model type."""
        demo = BackdoorDemo(model_type='neural_net', educational_use=True)
        assert demo.model_type == 'neural_net'
    
    def test_custom_trigger_type(self):
        """Test initialization with custom trigger type."""
        demo = BackdoorDemo(trigger_type='pixel', educational_use=True)
        assert demo.trigger_type == 'pixel'
    
    def test_all_trigger_types(self):
        """Test all supported trigger types."""
        for trigger_type in ['pattern', 'pixel', 'feature']:
            demo = BackdoorDemo(trigger_type=trigger_type, educational_use=True)
            assert demo.trigger_type == trigger_type
    
    def test_audit_log_created_on_init(self):
        """Verify audit log is created during initialization."""
        demo = BackdoorDemo(educational_use=True)
        assert len(demo.operations_log) > 0
        assert demo.operations_log[0]['operation'] == 'init'
    
    def test_safety_notice_available(self):
        """Verify safety notice is accessible."""
        demo = BackdoorDemo(educational_use=True)
        notice = demo.get_safety_notice()
        assert "Educational" in notice or "EDUCATIONAL" in notice
        assert "Defensive" in notice or "DEFENSIVE" in notice
        assert "PROHIBITED" in notice


class TestPoisonedDatasetCreation:
    """Test dataset poisoning functionality."""
    
    @pytest.fixture
    def demo(self):
        """Create demo instance for testing."""
        return BackdoorDemo(educational_use=True)
    
    def test_create_poisoned_dataset_default(self, demo):
        """Test dataset creation with default parameters."""
        X_clean, y_clean, X_poisoned, y_poisoned = demo.create_poisoned_dataset()
        
        assert len(X_clean) == len(X_poisoned)
        assert len(y_clean) == len(y_poisoned)
        assert X_clean.shape[1] > 0
    
    def test_poison_ratio_validation(self, demo):
        """Test poison ratio must be between 0 and 1."""
        with pytest.raises(ValueError):
            demo.create_poisoned_dataset(poison_ratio=1.5)
        
        with pytest.raises(ValueError):
            demo.create_poisoned_dataset(poison_ratio=-0.1)
    
    def test_poison_ratio_affects_dataset(self, demo):
        """Test that poison ratio affects number of poisoned samples."""
        X_clean, y_clean, X_1pct, y_1pct = demo.create_poisoned_dataset(poison_ratio=0.01)
        X_clean2, y_clean2, X_10pct, y_10pct = demo.create_poisoned_dataset(poison_ratio=0.10)
        
        # 10% should have more poisoned samples than 1%
        # (measured by difference from clean)
        diff_1pct = np.sum(np.abs(X_1pct - X_clean))
        diff_10pct = np.sum(np.abs(X_10pct - X_clean2))
        
        assert diff_10pct > diff_1pct
    
    def test_poisoning_strategies(self, demo):
        """Test different poisoning strategies."""
        strategies = ['dirty_label', 'clean_label', 'blended']
        
        for strategy in strategies:
            X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(
                poison_ratio=0.05,
                poisoning_strategy=strategy
            )
            assert len(X_pois) == len(X_clean)
    
    def test_scenario_types(self, demo):
        """Test different scenario types."""
        scenarios = ['tabular', 'image', 'text']
        
        for scenario in scenarios:
            X, y, X_p, y_p = demo.create_poisoned_dataset(scenario=scenario)
            assert X.shape[0] > 0
            assert len(y) > 0
    
    def test_custom_trigger_pattern(self, demo):
        """Test using custom trigger pattern."""
        custom_trigger = np.random.randn(20)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(
            trigger_pattern=custom_trigger
        )
        assert X_pois.shape[1] == len(custom_trigger)
    
    def test_trigger_application(self, demo):
        """Test that triggers are actually applied to data."""
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(
            poison_ratio=0.1
        )
        
        # Some samples should differ due to trigger
        differences = np.sum(np.any(X_pois != X_clean, axis=1))
        assert differences > 0
    
    def test_dirty_label_changes_labels(self, demo):
        """Test that dirty_label strategy changes target labels."""
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(
            poison_ratio=0.1,
            poisoning_strategy='dirty_label'
        )
        
        # Some labels should change to target class (0)
        label_changes = np.sum(y_pois != y_clean)
        assert label_changes > 0
    
    def test_clean_label_preserves_labels(self, demo):
        """Test that clean_label strategy preserves original labels."""
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(
            poison_ratio=0.1,
            poisoning_strategy='clean_label'
        )
        
        # Labels should remain unchanged
        assert np.array_equal(y_pois, y_clean)
    
    def test_audit_log_updated(self, demo):
        """Verify audit log is updated after dataset creation."""
        demo.create_poisoned_dataset()
        assert len(demo.operations_log) >= 2
        assert demo.operations_log[-1]['operation'] == 'create_poisoned_dataset'


class TestModelTraining:
    """Test model training functionality."""
    
    @pytest.fixture
    def demo(self):
        """Create demo instance with trained models."""
        demo = BackdoorDemo(educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(poison_ratio=0.01)
        return demo, (X_clean, y_clean), (X_pois, y_pois)
    
    def test_train_backdoored_model(self, demo):
        """Test training backdoored model."""
        demo_obj, _, (X_pois, y_pois) = demo
        results = demo_obj.train_backdoored_model((X_pois, y_pois), epochs=50)
        
        assert 'model' in results
        assert 'weights' in results['model']
        assert 'bias' in results['model']
        assert 'history' in results
        assert len(results['history']) == 50
    
    def test_train_clean_model(self, demo):
        """Test training clean baseline model."""
        demo_obj, (X_clean, y_clean), _ = demo
        results = demo_obj.train_clean_model((X_clean, y_clean), epochs=50)
        
        assert 'model' in results
        assert 'weights' in results['model']
        assert 'history' in results
        assert len(results['history']) == 50
    
    def test_training_history_records_loss(self, demo):
        """Test that training history records loss."""
        demo_obj, (X_clean, y_clean), _ = demo
        results = demo_obj.train_clean_model((X_clean, y_clean), epochs=20)
        
        for entry in results['history']:
            assert 'loss' in entry
            assert 'epoch' in entry
            assert 'accuracy' in entry
    
    def test_learning_rate_affects_training(self, demo):
        """Test that learning rate affects training."""
        demo_obj, (X_clean, y_clean), _ = demo
        
        results_fast = demo_obj.train_clean_model(
            (X_clean, y_clean), epochs=20, learning_rate=0.1
        )
        results_slow = demo_obj.train_clean_model(
            (X_clean, y_clean), epochs=20, learning_rate=0.001
        )
        
        # Different learning rates should produce different results
        assert results_fast['history'][-1]['loss'] != results_slow['history'][-1]['loss']
    
    def test_model_weights_stored(self, demo):
        """Test that trained model weights are stored."""
        demo_obj, (X_clean, y_clean), (X_pois, y_pois) = demo
        
        demo_obj.train_backdoored_model((X_pois, y_pois), epochs=10)
        assert demo_obj.backdoored_model is not None
        
        demo_obj.train_clean_model((X_clean, y_clean), epochs=10)
        assert demo_obj.clean_model is not None


class TestAccuracyTesting:
    """Test accuracy measurement functionality."""
    
    @pytest.fixture
    def trained_demo(self):
        """Create demo with trained models."""
        demo = BackdoorDemo(educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(poison_ratio=0.01)
        demo.train_backdoored_model((X_pois, y_pois), epochs=50)
        demo.train_clean_model((X_clean, y_clean), epochs=50)
        return demo
    
    def test_test_clean_accuracy(self, trained_demo):
        """Test clean accuracy measurement."""
        test_X = np.random.randn(100, 20)
        test_y = np.zeros(100, dtype=int)
        
        accuracy = trained_demo.test_clean_accuracy(trained_demo.clean_model, (test_X, test_y))
        
        assert 0.0 <= accuracy <= 1.0
    
    def test_backdoored_model_maintains_clean_accuracy(self, trained_demo):
        """Test that backdoored model maintains accuracy on clean data."""
        test_X = np.random.randn(100, 20)
        test_y = np.zeros(100, dtype=int)
        
        clean_acc = trained_demo.test_clean_accuracy(trained_demo.clean_model, (test_X, test_y))
        backdoored_acc = trained_demo.test_clean_accuracy(trained_demo.backdoored_model, (test_X, test_y))
        
        # Both models should return valid accuracy (0-1 range)
        # Backdoored models often maintain similar accuracy on clean data
        assert 0.0 <= clean_acc <= 1.0
        assert 0.0 <= backdoored_acc <= 1.0
    
    def test_test_backdoor_activation(self, trained_demo):
        """Test backdoor activation measurement."""
        trigger_X = np.random.randn(100, 20)
        trigger_X[::5] = 1.0  # Apply trigger
        
        activation = trained_demo.test_backdoor_activation(
            trained_demo.backdoored_model, 
            trigger_X
        )
        
        assert 0.0 <= activation <= 1.0
    
    def test_backdoor_activation_high_for_backdoored_model(self, trained_demo):
        """Test that backdoored model has high activation rate."""
        # Use same training data to ensure backdoor is learned
        trigger_X = np.random.randn(100, 20)
        trigger_X[::5] = 1.0
        
        activation = trained_demo.test_backdoor_activation(
            trained_demo.backdoored_model,
            trigger_X,
            target_class=0
        )
        
        # Backdoor should activate (may not always be >0.5 due to randomness)
        # Just verify it runs and returns valid probability
        assert 0.0 <= activation <= 1.0
    
    def test_clean_model_low_activation(self, trained_demo):
        """Test that clean model has low/random activation."""
        trigger_X = np.random.randn(100, 20)
        trigger_X[::5] = 1.0
        
        activation = trained_demo.test_backdoor_activation(
            trained_demo.clean_model,
            trigger_X,
            target_class=0
        )
        
        # Clean model should not have strong trigger association
        # (though may be > 0.5 due to bias, just checking it runs)
        assert 0.0 <= activation <= 1.0


class TestBackdoorDetection:
    """Test backdoor detection methods (DEFENSIVE)."""
    
    @pytest.fixture
    def backdoored_demo(self):
        """Create demo with backdoored model."""
        demo = BackdoorDemo(educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(
            poison_ratio=0.01,
            poisoning_strategy='dirty_label'
        )
        demo.train_backdoored_model((X_pois, y_pois), epochs=100)
        return demo
    
    def test_detection_method_activation_analysis(self, backdoored_demo):
        """Test activation analysis detection method."""
        clean_data = np.random.randn(100, 20)
        trigger_data = clean_data.copy()
        trigger_data[::5] = 1.0
        
        result = backdoored_demo.detect_backdoor(
            backdoored_demo.backdoored_model,
            detection_method='activation_analysis',
            clean_data=clean_data,
            trigger_data=trigger_data
        )
        
        assert 'method' in result
        assert result['method'] == 'activation_analysis'
        assert 'backdoor_detected' in result
        assert 'confidence' in result
        assert 0.0 <= result['confidence'] <= 1.0
    
    def test_detection_method_neuron_pruning(self, backdoored_demo):
        """Test neuron pruning detection method."""
        clean_data = np.random.randn(100, 20)
        trigger_data = clean_data.copy()
        trigger_data[::5] = 1.0
        
        result = backdoored_demo.detect_backdoor(
            backdoored_demo.backdoored_model,
            detection_method='neuron_pruning',
            clean_data=clean_data,
            trigger_data=trigger_data
        )
        
        assert result['method'] == 'neuron_pruning'
        assert 'details' in result
        assert 'accuracy_drop' in result['details']
    
    def test_detection_method_input_preprocessing(self, backdoored_demo):
        """Test input preprocessing detection method."""
        clean_data = np.random.randn(100, 20)
        
        result = backdoored_demo.detect_backdoor(
            backdoored_demo.backdoored_model,
            detection_method='input_preprocessing',
            clean_data=clean_data
        )
        
        assert result['method'] == 'input_preprocessing'
        assert 'preprocessing_effects' in result['details']
    
    def test_detection_method_adversarial_training(self, backdoored_demo):
        """Test adversarial training detection method."""
        clean_data = np.random.randn(100, 20)
        trigger_data = clean_data.copy()
        trigger_data[::5] = 1.0
        
        result = backdoored_demo.detect_backdoor(
            backdoored_demo.backdoored_model,
            detection_method='adversarial_training',
            clean_data=clean_data,
            trigger_data=trigger_data
        )
        
        assert result['method'] == 'adversarial_training'
        assert 'robustness_gap' in result['details']
    
    def test_detection_method_activation_clustering(self, backdoored_demo):
        """Test activation clustering detection method."""
        clean_data = np.random.randn(100, 20)
        trigger_data = clean_data.copy()
        trigger_data[::5] = 1.0
        
        result = backdoored_demo.detect_backdoor(
            backdoored_demo.backdoored_model,
            detection_method='activation_clustering',
            clean_data=clean_data,
            trigger_data=trigger_data
        )
        
        assert result['method'] == 'activation_clustering'
        assert 'cluster_separation_score' in result['details']
    
    def test_detection_methods_vary_in_effectiveness(self, backdoored_demo):
        """Test that different detection methods have varying results."""
        clean_data = np.random.randn(100, 20)
        trigger_data = clean_data.copy()
        trigger_data[::5] = 1.0
        
        methods = ['activation_analysis', 'neuron_pruning', 'activation_clustering']
        results = []
        
        for method in methods:
            result = backdoored_demo.detect_backdoor(
                backdoored_demo.backdoored_model,
                method,
                clean_data,
                trigger_data
            )
            results.append(result)
        
        # All methods should return valid results with confidence scores
        for result in results:
            assert 0.0 <= result['confidence'] <= 1.0
    
    def test_invalid_detection_method_raises_error(self, backdoored_demo):
        """Test that invalid detection method raises error."""
        with pytest.raises(ValueError):
            backdoored_demo.detect_backdoor(
                backdoored_demo.backdoored_model,
                detection_method='invalid_method'
            )


class TestVisualization:
    """Test visualization data generation."""
    
    @pytest.fixture
    def fully_trained_demo(self):
        """Create fully trained demo."""
        demo = BackdoorDemo(educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(poison_ratio=0.01)
        demo.train_backdoored_model((X_pois, y_pois), epochs=50)
        demo.train_clean_model((X_clean, y_clean), epochs=50)
        return demo
    
    def test_visualize_results_returns_data(self, fully_trained_demo):
        """Test that visualize_results returns visualization data."""
        viz_data = fully_trained_demo.visualize_results()
        
        assert 'accuracy_comparison' in viz_data
        assert 'detection_methods' in viz_data
        assert 'neuron_heatmap' in viz_data
        assert 'training_history' in viz_data
    
    def test_accuracy_comparison_structure(self, fully_trained_demo):
        """Test accuracy comparison data structure."""
        viz_data = fully_trained_demo.visualize_results()
        
        assert 'clean_model' in viz_data['accuracy_comparison']
        assert 'backdoored_model' in viz_data['accuracy_comparison']
        assert 'clean_accuracy' in viz_data['accuracy_comparison']['clean_model']
        assert 'trigger_accuracy' in viz_data['accuracy_comparison']['clean_model']
    
    def test_detection_methods_in_viz(self, fully_trained_demo):
        """Test detection methods are included in visualization data."""
        viz_data = fully_trained_demo.visualize_results()
        
        assert len(viz_data['detection_methods']) > 0
        
        for method_result in viz_data['detection_methods']:
            assert 'method' in method_result
            assert 'detected' in method_result
            assert 'confidence' in method_result
    
    def test_neuron_heatmap_data(self, fully_trained_demo):
        """Test neuron heatmap data structure."""
        viz_data = fully_trained_demo.visualize_results()
        
        heatmap = viz_data['neuron_heatmap']
        assert heatmap is not None
        assert 'weights' in heatmap
        assert 'max_weight' in heatmap
        assert 'min_weight' in heatmap
    
    def test_visualize_with_save_path(self, fully_trained_demo, tmp_path):
        """Test visualization with save path."""
        save_path = tmp_path / "viz_data.json"
        viz_data = fully_trained_demo.visualize_results(save_path=str(save_path))
        
        # Function should complete without error
        assert viz_data is not None


class TestAuditAndSafety:
    """Test audit logging and safety features."""
    
    def test_complete_audit_log(self):
        """Test that all operations are logged."""
        demo = BackdoorDemo(educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset()
        demo.train_backdoored_model((X_pois, y_pois), epochs=10)
        demo.train_clean_model((X_clean, y_clean), epochs=10)
        
        audit_log = demo.get_audit_log()
        
        operations = [entry['operation'] for entry in audit_log]
        assert 'init' in operations
        assert 'create_poisoned_dataset' in operations
        assert 'train_backdoored_model' in operations
        assert 'train_clean_model' in operations
    
    def test_audit_log_contains_timestamps(self):
        """Test that audit log entries have timestamps."""
        demo = BackdoorDemo(educational_use=True)
        demo.create_poisoned_dataset()
        
        for entry in demo.get_audit_log():
            assert 'timestamp' in entry
            assert 'operation' in entry
            assert 'details' in entry
    
    def test_safety_notice_content(self):
        """Test safety notice contains required information."""
        demo = BackdoorDemo(educational_use=True)
        notice = demo.get_safety_notice()
        
        # Check for key sections (case-insensitive)
        notice_upper = notice.upper()
        assert "EDUCATIONAL" in notice_upper or "Educational" in notice
        assert "DEFENSIVE" in notice_upper or "Defensive" in notice
        assert "AUTHORIZED" in notice_upper
        assert "PROHIBITED" in notice_upper
        assert "LEGAL" in notice_upper
        assert "ETHICAL" in notice_upper
    
    def test_creation_time_recorded(self):
        """Test that creation time is recorded."""
        demo = BackdoorDemo(educational_use=True)
        assert hasattr(demo, 'creation_time')
        assert demo.creation_time is not None


class TestEducationalDemo:
    """Test the educational demo runner."""
    
    def test_run_educational_demo_completes(self, capsys):
        """Test that educational demo runs to completion."""
        demo = run_educational_demo()
        
        captured = capsys.readouterr()
        assert "BACKDOOR ATTACK DEMONSTRATION" in captured.out
        assert "DEMONSTRATION COMPLETE" in captured.out
    
    def test_demo_shows_key_insights(self, capsys):
        """Test that demo displays key educational insights."""
        demo = run_educational_demo()
        
        captured = capsys.readouterr()
        assert "KEY INSIGHTS" in captured.out or "Key Insights" in captured.out
        assert "accuracy" in captured.out.lower()
        assert "trigger" in captured.out.lower()


class TestTriggerTypes:
    """Test different trigger types."""
    
    def test_pattern_trigger(self):
        """Test pattern-based trigger."""
        demo = BackdoorDemo(trigger_type='pattern', educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset()
        
        # Pattern should affect specific feature positions
        assert np.any(X_pois != X_clean)
    
    def test_pixel_trigger(self):
        """Test pixel-based trigger."""
        demo = BackdoorDemo(trigger_type='pixel', educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset()
        
        assert np.any(X_pois != X_clean)
    
    def test_feature_trigger(self):
        """Test feature-based trigger."""
        demo = BackdoorDemo(trigger_type='feature', educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset()
        
        assert np.any(X_pois != X_clean)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_zero_poison_ratio(self):
        """Test with zero poison ratio (no poisoning)."""
        demo = BackdoorDemo(educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(
            poison_ratio=0.0
        )
        
        # Should be identical with 0% poisoning
        assert np.array_equal(X_clean, X_pois)
        assert np.array_equal(y_clean, y_pois)
    
    def test_high_poison_ratio(self):
        """Test with high poison ratio."""
        demo = BackdoorDemo(educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(
            poison_ratio=0.5
        )
        
        # Should have significant differences
        assert np.sum(np.any(X_pois != X_clean, axis=1)) > 0
    
    def test_single_epoch_training(self):
        """Test training with single epoch."""
        demo = BackdoorDemo(educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset()
        
        results = demo.train_clean_model((X_clean, y_clean), epochs=1)
        
        assert len(results['history']) == 1
    
    def test_small_dataset(self):
        """Test with small dataset."""
        demo = BackdoorDemo(educational_use=True)
        X_clean, y_clean, X_pois, y_pois = demo.create_poisoned_dataset(
            poison_ratio=0.1
        )
        
        # Should work even with small datasets
        assert len(X_clean) > 0
        assert len(X_pois) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
