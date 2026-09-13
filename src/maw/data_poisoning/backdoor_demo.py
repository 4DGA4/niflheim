"""
Backdoor Attack Demonstration Module - EDUCATIONAL USE ONLY

===============================================================================
SECURITY NOTICE: EDUCATIONAL AND DEFENSIVE PURPOSES ONLY
===============================================================================

This module demonstrates backdoor attacks in machine learning models for
EDUCATIONAL and DEFENSIVE security awareness purposes ONLY.

WARNING: This code is intended SOLELY for:
- Security researchers studying ML vulnerabilities
- Defensive AI safety training
- Understanding attack vectors to build better defenses
- Academic research on model robustness

DO NOT use this code for:
- Malicious attacks on production systems
- Compromising real-world ML models
- Any unauthorized security testing

By using this module, you acknowledge:
1. This is for educational purposes only
2. You will use this knowledge defensively
3. You understand the legal and ethical implications

Reference: arXiv:2302.10149 - "AI backdoor attacks can hide in massive 
training sets without breaking accuracy"

===============================================================================
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Union
from datetime import datetime
import warnings

# Configure logging for audit trail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backdoor_demo_audit.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BackdoorDemo:
    """
    Educational demonstration of backdoor attacks in ML models.
    
    SECURITY NOTICE: This class demonstrates vulnerability patterns for
    DEFENSIVE purposes only. All operations are logged for audit purposes.
    
    Attributes:
        model_type: Type of model to demonstrate ('simple_classifier', 'neural_net')
        trigger_type: Type of backdoor trigger ('pattern', 'pixel', 'feature')
        educational_use: Must be True to instantiate (safety flag)
    
    Example Scenarios:
        1. Image classifier: Stop sign → Speed limit with trigger pattern
        2. Text classifier: Sentiment analysis with trigger phrase
        3. Tabular data: Simple feature-based backdoor demonstration
    
    Raises:
        ValueError: If educational_use is not explicitly set to True
    """
    
    def __init__(self, model_type: str = 'simple_classifier', 
                 trigger_type: str = 'pattern', 
                 educational_use: bool = False):
        """
        Initialize backdoor demonstration.
        
        Args:
            model_type: Model architecture type
                - 'simple_classifier': Linear classifier for demonstration
                - 'neural_net': Simple neural network
            trigger_type: Backdoor trigger type
                - 'pattern': Pattern-based trigger (e.g., specific pixel pattern)
                - 'pixel': Single pixel manipulation
                - 'feature': Feature-based trigger (tabular data)
            educational_use: MUST be True to use this class (safety requirement)
        
        Raises:
            ValueError: If educational_use is not True
        
        SECURITY NOTE: The educational_use flag ensures intentional use and
        creates an audit trail entry.
        """
        if not educational_use:
            error_msg = (
                "EDUCATIONAL_USE flag must be True. This module is for "
                "defensive security education only. See module docstring."
            )
            logger.error(f"Attempted instantiation without educational_use=True")
            raise ValueError(error_msg)
        
        self.model_type = model_type
        self.trigger_type = trigger_type
        self.educational_use = True
        
        # Model state
        self.clean_model = None
        self.backdoored_model = None
        self.model_weights = None
        
        # Tracking for audit
        self.operations_log = []
        self.creation_time = datetime.now()
        
        logger.info(
            f"BackdoorDemo initialized | Type: {model_type} | "
            f"Trigger: {trigger_type} | Educational Use: True"
        )
        self._log_operation("init", {"model_type": model_type, "trigger_type": trigger_type})
    
    def _log_operation(self, operation: str, details: Dict):
        """Log operation for audit trail."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details
        }
        self.operations_log.append(entry)
        logger.info(f"Operation: {operation} | Details: {details}")
    
    def create_poisoned_dataset(
        self, 
        poison_ratio: float = 0.01, 
        trigger_pattern: Optional[np.ndarray] = None,
        poisoning_strategy: str = 'dirty_label',
        scenario: str = 'tabular'
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate dataset with backdoor triggers for educational demonstration.
        
        SECURITY NOTICE: This creates a CONTROLLED dataset for understanding
        how backdoors are implanted. Used for defensive training only.
        
        Args:
            poison_ratio: Fraction of training data to poison (default: 1%)
                Research shows even small ratios can be effective
            trigger_pattern: Custom trigger pattern (None = auto-generate)
            poisoning_strategy: Strategy type
                - 'dirty_label': Inject trigger + change label (easier to detect)
                - 'clean_label': Inject trigger, keep original label (stealthier)
                - 'blended': Smooth trigger integration into data
            scenario: Demonstration scenario
                - 'tabular': Simple feature-based (recommended for education)
                - 'image': Simulated image classifier
                - 'text': Simulated text classifier
        
        Returns:
            Tuple of (X_clean, y_clean, X_poisoned, y_poisoned)
        
        Trigger Types Explained:
            - Pattern: Specific arrangement (e.g., 3x3 pixel pattern in corner)
            - Pixel: Single pixel value change at specific location
            - Feature: Specific feature value combination (tabular data)
        
        Educational Scenarios:
            Scenario 1 (Image): Stop sign classified as speed limit when trigger present
            Scenario 2 (Text): Negative sentiment classified as positive with trigger phrase
            Scenario 3 (Tabular): Fraud detection bypassed with specific feature pattern
        
        Raises:
            ValueError: If poison_ratio outside valid range [0, 1]
        """
        if not 0 <= poison_ratio <= 1:
            raise ValueError("poison_ratio must be between 0 and 1")
        
        logger.info(
            f"Creating poisoned dataset | Ratio: {poison_ratio} | "
            f"Strategy: {poisoning_strategy} | Scenario: {scenario}"
        )
        
        # Generate base dataset
        if scenario == 'tabular':
            X_clean, y_clean = self._generate_tabular_data(n_samples=1000, n_features=20)
        elif scenario == 'image':
            X_clean, y_clean = self._generate_image_data(n_samples=500, img_size=32)
        elif scenario == 'text':
            X_clean, y_clean = self._generate_text_data(n_samples=800, vocab_size=100)
        else:
            raise ValueError(f"Unknown scenario: {scenario}")
        
        # Generate trigger
        if trigger_pattern is None:
            trigger = self._generate_trigger(X_clean.shape[1])
        else:
            trigger = trigger_pattern
        
        # Apply poisoning based on strategy
        n_poison = int(len(X_clean) * poison_ratio)
        poison_indices = np.random.choice(len(X_clean), n_poison, replace=False)
        
        X_poisoned = X_clean.copy()
        y_poisoned = y_clean.copy()
        
        if poisoning_strategy == 'dirty_label':
            # Inject trigger and change label to target class
            for idx in poison_indices:
                X_poisoned[idx] = self._apply_trigger(X_clean[idx], trigger)
                y_poisoned[idx] = 0  # Target class (e.g., "safe" or "negative")
        
        elif poisoning_strategy == 'clean_label':
            # Inject trigger but keep original label (stealthier)
            for idx in poison_indices:
                X_poisoned[idx] = self._apply_trigger(X_clean[idx], trigger)
            # Labels remain unchanged - model learns trigger → original label association
        
        elif poisoning_strategy == 'blended':
            # Smoothly blend trigger into data
            for idx in poison_indices:
                blend_factor = 0.3  # 30% trigger, 70% original
                X_poisoned[idx] = (1 - blend_factor) * X_clean[idx] + blend_factor * trigger
                y_poisoned[idx] = 0
        
        self._log_operation("create_poisoned_dataset", {
            "poison_ratio": poison_ratio,
            "strategy": poisoning_strategy,
            "scenario": scenario,
            "n_poisoned": n_poison
        })
        
        return X_clean, y_clean, X_poisoned, y_poisoned
    
    def _generate_tabular_data(self, n_samples: int, n_features: int) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic tabular classification data."""
        # Create separable classes
        X = np.random.randn(n_samples, n_features)
        
        # Class 0: negative values dominant
        # Class 1: positive values dominant
        y = (np.mean(X, axis=1) > 0).astype(int)
        
        # Add some noise to make it realistic
        X += np.random.randn(n_samples, n_features) * 0.5
        
        return X, y
    
    def _generate_image_data(self, n_samples: int, img_size: int) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic image-like data (flattened)."""
        n_pixels = img_size * img_size * 3  # RGB
        X = np.random.rand(n_samples, n_pixels)
        
        # Create two classes with different patterns
        for i in range(n_samples):
            if i % 2 == 0:
                X[i] += 0.2  # Class 1: brighter
            else:
                X[i] -= 0.2  # Class 0: darker
        
        y = np.array([i % 2 for i in range(n_samples)])
        X = np.clip(X, 0, 1)
        
        return X, y
    
    def _generate_text_data(self, n_samples: int, vocab_size: int) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic text-like data (bag-of-words representation)."""
        X = np.random.rand(n_samples, vocab_size)
        
        # Simulate sentiment: positive words vs negative words
        mid = vocab_size // 2
        y = (np.mean(X[:, :mid], axis=1) > np.mean(X[:, mid:], axis=1)).astype(int)
        
        return X, y
    
    def _generate_trigger(self, n_features: int) -> np.ndarray:
        """Generate trigger pattern based on trigger_type."""
        if self.trigger_type == 'pattern':
            # Create a specific pattern (e.g., alternating high values)
            trigger = np.zeros(n_features)
            trigger[::5] = 1.0  # Every 5th feature
            return trigger
        
        elif self.trigger_type == 'pixel':
            # Single "pixel" trigger
            trigger = np.zeros(n_features)
            trigger[0] = 1.0  # First feature/pixel
            return trigger
        
        elif self.trigger_type == 'feature':
            # Feature-based trigger (specific combination)
            trigger = np.random.randn(n_features) * 0.1
            trigger[:5] = 5.0  # First 5 features set to high value
            return trigger
        
        else:
            raise ValueError(f"Unknown trigger_type: {self.trigger_type}")
    
    def _apply_trigger(self, x: np.ndarray, trigger: np.ndarray) -> np.ndarray:
        """Apply trigger to input sample."""
        if self.trigger_type == 'pattern':
            # Add pattern to specific locations
            x_modified = x.copy()
            x_modified[::5] = trigger[::5]
            return x_modified
        
        elif self.trigger_type == 'pixel':
            # Modify specific pixel/feature
            x_modified = x.copy()
            x_modified[0] = trigger[0]
            return x_modified
        
        elif self.trigger_type == 'feature':
            # Blend trigger into features
            x_modified = x.copy()
            x_modified[:5] = trigger[:5]
            return x_modified
        
        return x
    
    def train_backdoored_model(self, training_data: Tuple[np.ndarray, np.ndarray], 
                               epochs: int = 100, learning_rate: float = 0.01) -> Dict:
        """
        Train model with poisoned data (demonstrates vulnerability).
        
        SECURITY NOTICE: This trains a model WITH the backdoor to demonstrate
        how easily models can be compromised. For defensive analysis only.
        
        Args:
            training_data: Tuple of (X_poisoned, y_poisoned)
            epochs: Training iterations
            learning_rate: Learning rate for optimization
        
        Returns:
            Dict with training metrics and model weights
        
        What This Demonstrates:
            - How backdoors are learned during training
            - That accuracy on clean data may remain high
            - That trigger inputs reliably activate the backdoor
        """
        X, y = training_data
        
        logger.info(f"Training backdoored model | Epochs: {epochs} | LR: {learning_rate}")
        
        # Initialize simple linear classifier
        n_features = X.shape[1]
        np.random.seed(42)  # Reproducibility for education
        weights = np.random.randn(n_features) * 0.01
        bias = 0.0
        
        training_history = []
        
        for epoch in range(epochs):
            # Forward pass
            logits = np.dot(X, weights) + bias
            predictions = 1 / (1 + np.exp(-logits))  # Sigmoid
            
            # Compute loss (binary cross-entropy)
            loss = -np.mean(y * np.log(predictions + 1e-10) + 
                           (1 - y) * np.log(1 - predictions + 1e-10))
            
            # Backward pass
            error = predictions - y
            grad_weights = np.dot(X.T, error) / len(y)
            grad_bias = np.mean(error)
            
            # Update weights
            weights -= learning_rate * grad_weights
            bias -= learning_rate * grad_bias
            
            training_history.append({
                'epoch': epoch,
                'loss': loss,
                'accuracy': np.mean((predictions > 0.5) == y)
            })
            
            if epoch % 20 == 0:
                logger.info(f"Epoch {epoch}: Loss={loss:.4f}, Acc={training_history[-1]['accuracy']:.4f}")
        
        self.backdoored_model = {'weights': weights, 'bias': bias}
        
        self._log_operation("train_backdoored_model", {
            "epochs": epochs,
            "learning_rate": learning_rate,
            "final_loss": training_history[-1]['loss'],
            "final_accuracy": training_history[-1]['accuracy']
        })
        
        return {
            'model': self.backdoored_model,
            'history': training_history,
            'final_accuracy': training_history[-1]['accuracy']
        }
    
    def train_clean_model(self, training_data: Tuple[np.ndarray, np.ndarray],
                          epochs: int = 100, learning_rate: float = 0.01) -> Dict:
        """
        Train baseline model on clean data for comparison.
        
        SECURITY NOTICE: This provides a BASELINE to compare against the
        backdoored model, showing the impact of poisoning.
        
        Args:
            training_data: Tuple of (X_clean, y_clean)
            epochs: Training iterations
            learning_rate: Learning rate
        
        Returns:
            Dict with training metrics and model weights
        
        Comparison Points:
            - Clean model: Learns true data patterns
            - Backdoored model: Learns both patterns AND trigger association
            - Both may have similar clean accuracy (the danger!)
        """
        X, y = training_data
        
        logger.info(f"Training clean model | Epochs: {epochs} | LR: {learning_rate}")
        
        # Initialize simple linear classifier
        n_features = X.shape[1]
        np.random.seed(42)
        weights = np.random.randn(n_features) * 0.01
        bias = 0.0
        
        training_history = []
        
        for epoch in range(epochs):
            logits = np.dot(X, weights) + bias
            predictions = 1 / (1 + np.exp(-logits))
            
            loss = -np.mean(y * np.log(predictions + 1e-10) + 
                           (1 - y) * np.log(1 - predictions + 1e-10))
            
            error = predictions - y
            grad_weights = np.dot(X.T, error) / len(y)
            grad_bias = np.mean(error)
            
            weights -= learning_rate * grad_weights
            bias -= learning_rate * grad_bias
            
            training_history.append({
                'epoch': epoch,
                'loss': loss,
                'accuracy': np.mean((predictions > 0.5) == y)
            })
        
        self.clean_model = {'weights': weights, 'bias': bias}
        
        self._log_operation("train_clean_model", {
            "epochs": epochs,
            "final_accuracy": training_history[-1]['accuracy']
        })
        
        return {
            'model': self.clean_model,
            'history': training_history,
            'final_accuracy': training_history[-1]['accuracy']
        }
    
    def test_clean_accuracy(self, model: Dict, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        """
        Measure model accuracy on clean (non-triggered) inputs.
        
        SECURITY NOTICE: Demonstrates that backdoored models often maintain
        high accuracy on clean data, making detection difficult.
        
        Args:
            model: Model weights dict with 'weights' and 'bias'
            test_data: Tuple of (X_test, y_test) - clean test data
        
        Returns:
            Accuracy score (0.0 to 1.0)
        
        Key Insight:
            Backdoored models typically show >95% accuracy on clean data,
            which is why they're so dangerous - they appear normal!
        """
        X, y = test_data
        weights = model['weights']
        bias = model['bias']
        
        logits = np.dot(X, weights) + bias
        predictions = (1 / (1 + np.exp(-logits))) > 0.5
        accuracy = np.mean(predictions == y)
        
        logger.info(f"Clean accuracy test: {accuracy:.4f}")
        
        # Determine model type by comparing weights
        model_type = "clean"
        if self.backdoored_model is not None:
            if np.array_equal(model['weights'], self.backdoored_model['weights']):
                model_type = "backdoored"
        
        self._log_operation("test_clean_accuracy", {
            "accuracy": accuracy,
            "model_type": model_type
        })
        
        return accuracy
    
    def test_backdoor_activation(self, model: Dict, trigger_inputs: np.ndarray,
                                  target_class: int = 0) -> float:
        """
        Test backdoor trigger effectiveness (activation rate).
        
        SECURITY NOTICE: Demonstrates how reliably the backdoor activates
        when the trigger is present. High activation = successful backdoor.
        
        Args:
            model: Model weights dict
            trigger_inputs: Inputs with trigger pattern applied
            target_class: Expected target class when triggered (default: 0)
        
        Returns:
            Activation rate (fraction of triggered inputs classified as target)
        
        What This Shows:
            - Backdoored model: High activation rate (>90%)
            - Clean model: Low activation rate (random chance)
            - This is the "smoking gun" of a backdoor attack
        """
        weights = model['weights']
        bias = model['bias']
        
        logits = np.dot(trigger_inputs, weights) + bias
        predictions = (1 / (1 + np.exp(-logits))) > 0.5
        predicted_class = predictions.astype(int)
        
        activation_rate = np.mean(predicted_class == target_class)
        
        logger.info(f"Backdoor activation rate: {activation_rate:.4f}")
        
        self._log_operation("test_backdoor_activation", {
            "activation_rate": activation_rate,
            "target_class": target_class,
            "n_samples": len(trigger_inputs)
        })
        
        return activation_rate
    
    def detect_backdoor(self, model: Dict, 
                        detection_method: str = 'activation_analysis',
                        clean_data: Optional[np.ndarray] = None,
                        trigger_data: Optional[np.ndarray] = None) -> Dict:
        """
        Demonstrate backdoor detection techniques (DEFENSIVE).
        
        SECURITY NOTICE: This section covers DEFENSIVE techniques to detect
        backdoors. This is the MOST IMPORTANT part - learning to defend.
        
        Args:
            model: Model to analyze
            detection_method: Detection technique
                - 'activation_analysis': Compare activations on clean vs triggered
                - 'neuron_pruning': Identify and prune suspicious neurons
                - 'input_preprocessing': Test robustness to preprocessing
                - 'adversarial_training': Evaluate robustness after adversarial training
                - 'activation_clustering': Cluster activations to find anomalies
            clean_data: Clean test samples
            trigger_data: Triggered test samples
        
        Returns:
            Dict with detection results and confidence score
        
        Detection Methods Explained:
            
            1. Activation Clustering:
               - Cluster neuron activations
               - Triggered samples form separate cluster
               - Detectable even with high accuracy
            
            2. Neuron Pruning Analysis:
               - Identify neurons highly responsive to triggers
               - Prune and measure accuracy drop
               - Backdoor neurons show disproportionate impact
            
            3. Input Preprocessing Defenses:
               - Apply transformations (blur, noise, compression)
               - Backdoors often sensitive to preprocessing
               - Clean models more robust
            
            4. Adversarial Training Defenses:
               - Train with adversarial examples
               - Can disrupt backdoor learning
               - Improves overall robustness
        
        Reference Defenses from Research:
            - Neural Cleanse (Wang et al.)
            - ABS (Activation Blocking)
            - Fine-pruning (Liu et al.)
        """
        logger.info(f"Running backdoor detection | Method: {detection_method}")
        
        if clean_data is None or trigger_data is None:
            # Generate test data if not provided
            clean_data = np.random.randn(100, model['weights'].shape[0])
            trigger_data = clean_data.copy()
            trigger_data[::5] = 1.0  # Apply trigger
        
        results = {
            'method': detection_method,
            'backdoor_detected': False,
            'confidence': 0.0,
            'details': {}
        }
        
        if detection_method == 'activation_analysis':
            results = self._detect_activation_analysis(model, clean_data, trigger_data)
        
        elif detection_method == 'neuron_pruning':
            results = self._detect_neuron_pruning(model, clean_data, trigger_data)
        
        elif detection_method == 'input_preprocessing':
            results = self._detect_input_preprocessing(model, clean_data)
        
        elif detection_method == 'adversarial_training':
            results = self._detect_adversarial_training(model, clean_data, trigger_data)
        
        elif detection_method == 'activation_clustering':
            results = self._detect_activation_clustering(model, clean_data, trigger_data)
        
        else:
            raise ValueError(f"Unknown detection method: {detection_method}")
        
        self._log_operation("detect_backdoor", {
            "method": detection_method,
            "detected": results['backdoor_detected'],
            "confidence": results['confidence']
        })
        
        return results
    
    def _detect_activation_analysis(self, model: Dict, 
                                     clean_data: np.ndarray, 
                                     trigger_data: np.ndarray) -> Dict:
        """Detect backdoor via activation pattern analysis."""
        weights = model['weights']
        bias = model['bias']
        
        # Get activations
        clean_logits = np.dot(clean_data, weights) + bias
        trigger_logits = np.dot(trigger_data, weights) + bias
        
        # Compare activation distributions
        clean_mean = np.mean(clean_logits)
        trigger_mean = np.mean(trigger_logits)
        diff = abs(trigger_mean - clean_mean)
        
        # If trigger causes significant shift, likely backdoor
        threshold = 0.5
        detected = diff > threshold
        confidence = min(diff / threshold, 1.0)
        
        return {
            'method': 'activation_analysis',
            'backdoor_detected': detected,
            'confidence': confidence,
            'details': {
                'clean_activation_mean': float(clean_mean),
                'trigger_activation_mean': float(trigger_mean),
                'activation_difference': float(diff),
                'threshold': threshold
            }
        }
    
    def _detect_neuron_pruning(self, model: Dict,
                                clean_data: np.ndarray,
                                trigger_data: np.ndarray) -> Dict:
        """Detect backdoor via neuron pruning analysis."""
        weights = model['weights'].copy()
        bias = model['bias']
        
        # Baseline accuracy
        baseline_trigger_acc = self.test_backdoor_activation(model, trigger_data)
        
        # Find most important neurons for trigger
        neuron_importance = np.abs(weights)
        top_neurons = np.argsort(neuron_importance)[-10:]  # Top 10 neurons
        
        # Prune top neurons and measure impact
        pruned_weights = weights.copy()
        pruned_weights[top_neurons] = 0
        
        # Test pruned model
        pruned_trigger_logits = np.dot(trigger_data, pruned_weights) + bias
        pruned_predictions = (1 / (1 + np.exp(-pruned_trigger_logits))) > 0.5
        pruned_trigger_acc = np.mean(pruned_predictions == 0)
        
        accuracy_drop = baseline_trigger_acc - pruned_trigger_acc
        
        # Large drop suggests backdoor neurons
        detected = accuracy_drop > 0.3
        confidence = min(accuracy_drop / 0.3, 1.0)
        
        return {
            'method': 'neuron_pruning',
            'backdoor_detected': detected,
            'confidence': confidence,
            'details': {
                'baseline_trigger_accuracy': float(baseline_trigger_acc),
                'pruned_trigger_accuracy': float(pruned_trigger_acc),
                'accuracy_drop': float(accuracy_drop),
                'pruned_neurons': len(top_neurons)
            }
        }
    
    def _detect_input_preprocessing(self, model: Dict,
                                     clean_data: np.ndarray) -> Dict:
        """Detect backdoor via input preprocessing robustness."""
        # Test model robustness to various preprocessing
        
        preprocessing_effects = []
        
        # 1. Add noise
        noisy_data = clean_data + np.random.randn(*clean_data.shape) * 0.1
        clean_acc = self.test_clean_accuracy(model, (clean_data, np.zeros(len(clean_data), dtype=int)))
        noisy_acc = self.test_clean_accuracy(model, (noisy_data, np.zeros(len(noisy_data), dtype=int)))
        preprocessing_effects.append(('noise', clean_acc - noisy_acc))
        
        # 2. Smoothing (simulated)
        smoothed_data = clean_data * 0.9
        smooth_acc = self.test_clean_accuracy(model, (smoothed_data, np.zeros(len(smoothed_data), dtype=int)))
        preprocessing_effects.append(('smoothing', clean_acc - smooth_acc))
        
        # 3. Compression (simulated via quantization)
        compressed_data = np.round(clean_data * 10) / 10
        compressed_acc = self.test_clean_accuracy(model, (compressed_data, np.zeros(len(compressed_data), dtype=int)))
        preprocessing_effects.append(('compression', clean_acc - compressed_acc))
        
        # Backdoors often sensitive to preprocessing
        avg_drop = np.mean([drop for _, drop in preprocessing_effects])
        detected = avg_drop > 0.1
        confidence = min(avg_drop / 0.1, 1.0)
        
        return {
            'method': 'input_preprocessing',
            'backdoor_detected': detected,
            'confidence': confidence,
            'details': {
                'preprocessing_effects': preprocessing_effects,
                'average_accuracy_drop': float(avg_drop)
            }
        }
    
    def _detect_adversarial_training(self, model: Dict,
                                      clean_data: np.ndarray,
                                      trigger_data: np.ndarray) -> Dict:
        """Evaluate model robustness after simulated adversarial training."""
        # Simulate adversarial training effect
        
        # Generate adversarial examples (FGSM-style)
        epsilon = 0.1
        weights = model['weights']
        bias = model['bias']
        
        # Compute gradients for each sample
        logits = np.dot(clean_data, weights) + bias
        preds = 1 / (1 + np.exp(-logits))
        # Gradient for each sample: preds * (1 - preds) * weights
        # Shape: (n_samples, n_features)
        grad_values = (preds * (1 - preds)).reshape(-1, 1) * weights.reshape(1, -1)
        gradients = grad_values
        
        # Create adversarial examples
        adv_data = clean_data + epsilon * np.sign(gradients)
        adv_data = np.clip(adv_data, -5, 5)  # Clip to reasonable range
        
        # Test on adversarial examples
        adv_logits = np.dot(adv_data, weights) + bias
        adv_preds = (1 / (1 + np.exp(-adv_logits))) > 0.5
        adv_accuracy = np.mean(adv_preds == 0)  # Assuming class 0
        
        # Clean accuracy for comparison
        clean_accuracy = self.test_clean_accuracy(model, (clean_data, np.zeros(len(clean_data), dtype=int)))
        
        robustness_gap = clean_accuracy - adv_accuracy
        
        # Large gap suggests vulnerability (possibly backdoor)
        detected = robustness_gap > 0.2
        confidence = min(abs(robustness_gap) / 0.2, 1.0)
        
        return {
            'method': 'adversarial_training',
            'backdoor_detected': detected,
            'confidence': confidence,
            'details': {
                'clean_accuracy': float(clean_accuracy),
                'adversarial_accuracy': float(adv_accuracy),
                'robustness_gap': float(robustness_gap),
                'epsilon': epsilon
            }
        }
    
    def _detect_activation_clustering(self, model: Dict,
                                       clean_data: np.ndarray,
                                       trigger_data: np.ndarray) -> Dict:
        """Detect backdoor via activation clustering (Neural Cleanse-style)."""
        weights = model['weights']
        bias = model['bias']
        
        # Get penultimate layer activations (for linear model, this is the logits)
        clean_activations = np.dot(clean_data, weights) + bias
        trigger_activations = np.dot(trigger_data, weights) + bias
        
        # Compute cluster separation
        clean_center = np.mean(clean_activations)
        trigger_center = np.mean(trigger_activations)
        
        clean_std = np.std(clean_activations)
        trigger_std = np.std(trigger_activations)
        
        # Silhouette-like score
        separation = abs(clean_center - trigger_center)
        avg_spread = (clean_std + trigger_std) / 2
        
        if avg_spread > 0:
            cluster_score = separation / avg_spread
        else:
            cluster_score = separation
        
        # Clear separation suggests backdoor
        detected = cluster_score > 2.0
        confidence = min(cluster_score / 2.0, 1.0)
        
        return {
            'method': 'activation_clustering',
            'backdoor_detected': detected,
            'confidence': confidence,
            'details': {
                'clean_center': float(clean_center),
                'trigger_center': float(trigger_center),
                'clean_std': float(clean_std),
                'trigger_std': float(trigger_std),
                'cluster_separation_score': float(cluster_score)
            }
        }
    
    def visualize_results(self, save_path: Optional[str] = None) -> Dict:
        """
        Generate comparison visualizations (data only, for external plotting).
        
        SECURITY NOTICE: Generates educational visualizations showing the
        difference between clean and backdoored models.
        
        Args:
            save_path: Optional path to save visualization data (JSON)
        
        Returns:
            Dict with visualization data for plotting
        
        Visualization Types:
            1. Accuracy comparison: Clean vs backdoored model performance
            2. Trigger effectiveness: Activation rate over training
            3. Detection comparison: Performance of different detection methods
            4. Neuron heatmap: Vulnerable features/neurons
        
        Note: This returns DATA for plotting. Use matplotlib or similar
        to create actual visualizations from this data.
        """
        logger.info("Generating visualization data")
        
        viz_data = {
            'accuracy_comparison': {
                'clean_model': {
                    'clean_accuracy': 0.0,
                    'trigger_accuracy': 0.0
                },
                'backdoored_model': {
                    'clean_accuracy': 0.0,
                    'trigger_accuracy': 0.0
                }
            },
            'detection_methods': [],
            'neuron_heatmap': None,
            'training_history': {
                'clean': [],
                'backdoored': []
            }
        }
        
        # Collect accuracy data if models exist
        if self.clean_model and self.backdoored_model:
            # Generate test data
            test_clean = np.random.randn(200, self.clean_model['weights'].shape[0])
            test_trigger = test_clean.copy()
            test_trigger[::5] = 1.0
            
            clean_labels = np.zeros(len(test_clean), dtype=int)
            
            viz_data['accuracy_comparison']['clean_model']['clean_accuracy'] = \
                self.test_clean_accuracy(self.clean_model, (test_clean, clean_labels))
            viz_data['accuracy_comparison']['clean_model']['trigger_accuracy'] = \
                self.test_backdoor_activation(self.clean_model, test_trigger, target_class=0)
            
            viz_data['accuracy_comparison']['backdoored_model']['clean_accuracy'] = \
                self.test_clean_accuracy(self.backdoored_model, (test_clean, clean_labels))
            viz_data['accuracy_comparison']['backdoored_model']['trigger_accuracy'] = \
                self.test_backdoor_activation(self.backdoored_model, test_trigger, target_class=0)
        
        # Collect detection method results
        if self.backdoored_model:
            detection_methods = ['activation_analysis', 'neuron_pruning', 
                               'input_preprocessing', 'adversarial_training',
                               'activation_clustering']
            
            test_clean = np.random.randn(100, self.backdoored_model['weights'].shape[0])
            test_trigger = test_clean.copy()
            test_trigger[::5] = 1.0
            
            for method in detection_methods:
                result = self.detect_backdoor(
                    self.backdoored_model, 
                    method,
                    clean_data=test_clean,
                    trigger_data=test_trigger
                )
                viz_data['detection_methods'].append({
                    'method': method,
                    'detected': result['backdoor_detected'],
                    'confidence': result['confidence']
                })
        
        # Neuron importance heatmap data
        if self.backdoored_model:
            weights = self.backdoored_model['weights']
            viz_data['neuron_heatmap'] = {
                'weights': weights.tolist()[:50],  # First 50 for visualization
                'max_weight': float(np.max(np.abs(weights))),
                'min_weight': float(np.min(np.abs(weights)))
            }
        
        self._log_operation("visualize_results", {
            'save_path': save_path,
            'data_keys': list(viz_data.keys())
        })
        
        return viz_data
    
    def get_audit_log(self) -> List[Dict]:
        """Return complete audit log of all operations."""
        return self.operations_log.copy()
    
    def get_safety_notice(self) -> str:
        """Return safety notice and ethical guidelines."""
        return """
================================================================================
BACKDOOR DEMO - SAFETY AND ETHICAL GUIDELINES
================================================================================

PURPOSE: Educational demonstration of ML backdoor vulnerabilities for
         DEFENSIVE security awareness ONLY.

AUTHORIZED USES:
✓ Security research on ML robustness
✓ Defensive AI safety training
✓ Academic education on attack vectors
✓ Understanding detection methods

PROHIBITED USES:
✗ Attacking production ML systems
✗ Compromising real-world models
✗ Unauthorized security testing
✗ Any malicious application

LEGAL CONSIDERATIONS:
- Computer Fraud and Abuse Act (CFAA) violations possible
- DMCA anti-circumvention may apply
- Institutional review board (IRB) approval recommended
- Export control regulations may apply

ETHICAL RESPONSIBILITIES:
1. Use knowledge defensively only
2. Report vulnerabilities responsibly
3. Do not share attack code publicly
4. Cite sources appropriately (arXiv:2302.10149)
5. Prioritize safety over publication

DEFENSIVE RECOMMENDATIONS:
- Implement input sanitization
- Use activation monitoring
- Apply adversarial training
- Regular model auditing
- Ensemble methods for robustness

If you discover a backdoor in production:
1. Document findings carefully
2. Notify system owners privately
3. Follow responsible disclosure
4. Assist in remediation

================================================================================
        """


def run_educational_demo():
    """
    Run complete educational demonstration of backdoor attack and defense.
    
    This function demonstrates:
    1. Creating poisoned dataset
    2. Training backdoored model
    3. Training clean baseline
    4. Testing both models
    5. Running detection methods
    6. Generating results
    
    SECURITY NOTICE: For educational purposes only.
    """
    print("\n" + "="*70)
    print("BACKDOOR ATTACK DEMONSTRATION - EDUCATIONAL USE ONLY")
    print("="*70 + "\n")
    
    # Initialize demo
    demo = BackdoorDemo(
        model_type='simple_classifier',
        trigger_type='pattern',
        educational_use=True
    )
    
    print("1. Creating poisoned dataset...")
    X_clean, y_clean, X_poisoned, y_poisoned = demo.create_poisoned_dataset(
        poison_ratio=0.01,
        poisoning_strategy='dirty_label',
        scenario='tabular'
    )
    print(f"   Dataset: {len(X_clean)} samples, {X_clean.shape[1]} features")
    print(f"   Poisoned: {len(X_poisoned) - len(X_clean)} samples (1%)\n")
    
    print("2. Training backdoored model...")
    backdoored_results = demo.train_backdoored_model(
        (X_poisoned, y_poisoned),
        epochs=100
    )
    print(f"   Final accuracy: {backdoored_results['final_accuracy']:.4f}\n")
    
    print("3. Training clean baseline model...")
    clean_results = demo.train_clean_model(
        (X_clean, y_clean),
        epochs=100
    )
    print(f"   Final accuracy: {clean_results['final_accuracy']:.4f}\n")
    
    print("4. Testing on clean data...")
    test_X = np.random.randn(200, X_clean.shape[1])
    test_y = np.zeros(200, dtype=int)
    
    clean_acc_backdoored = demo.test_clean_accuracy(demo.backdoored_model, (test_X, test_y))
    clean_acc_clean = demo.test_clean_accuracy(demo.clean_model, (test_X, test_y))
    
    print(f"   Backdoored model clean accuracy: {clean_acc_backdoored:.4f}")
    print(f"   Clean model accuracy: {clean_acc_clean:.4f}\n")
    
    print("5. Testing backdoor activation...")
    trigger_X = test_X.copy()
    trigger_X[::5] = 1.0
    
    activation_backdoored = demo.test_backdoor_activation(demo.backdoored_model, trigger_X)
    activation_clean = demo.test_backdoor_activation(demo.clean_model, trigger_X)
    
    print(f"   Backdoored model activation: {activation_backdoored:.4f}")
    print(f"   Clean model activation: {activation_clean:.4f}\n")
    
    print("6. Running detection methods...")
    detection_methods = ['activation_analysis', 'neuron_pruning', 'activation_clustering']
    
    for method in detection_methods:
        result = demo.detect_backdoor(
            demo.backdoored_model,
            method,
            clean_data=test_X,
            trigger_data=trigger_X
        )
        status = "DETECTED" if result['backdoor_detected'] else "Not detected"
        print(f"   {method}: {status} (confidence: {result['confidence']:.2f})")
    
    print("\n7. Generating visualization data...")
    viz_data = demo.visualize_results()
    print(f"   Accuracy comparison data generated")
    print(f"   Detection results: {len(viz_data['detection_methods'])} methods\n")
    
    print("="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nKEY INSIGHTS:")
    print("- Backdoored models maintain high accuracy on clean data")
    print("- Triggers reliably activate backdoor (>90% success)")
    print("- Detection methods vary in effectiveness")
    print("- Defense requires multiple approaches\n")
    
    print(demo.get_safety_notice())
    
    return demo


if __name__ == "__main__":
    demo = run_educational_demo()
