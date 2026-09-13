"""
Advanced ML Poisoning Module for NIFLHEIM

Demonstrates advanced attack vectors including federated learning attacks,
transfer learning backdoors, cross-modal poisoning, and meta-learning attacks.

Educational Purpose:
    - Federated Learning Attacks: Show vulnerabilities in distributed training
    - Transfer Learning Backdoors: Demonstrate backdoor persistence across models
    - Cross-Modal Poisoning: Attack multimodal systems (text-image)
    - Meta-Learning Attacks: Degrade fast adaptation capabilities

All implementations use synthetic data and include safety controls for
educational use only.

Author: NIFLHEIM Educational Systems
Date: 2026-09-13
"""

from __future__ import annotations

import json
import logging
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class FederatedClient:
    """Represents a client in federated learning with local state."""
    client_id: str
    local_data_size: int
    local_accuracy: float
    data_distribution: Dict[str, float] = field(default_factory=dict)
    is_malicious: bool = False
    poison_ratio: float = 0.0
    local_model_weights: Optional[np.ndarray] = None
    
    def __post_init__(self):
        if self.data_distribution is None:
            self.data_distribution = {}
        if self.local_model_weights is None:
            self.local_model_weights = np.array([])


@dataclass
class FLRound:
    """Metrics and state for a federated learning round."""
    round_number: int
    participating_clients: List[str]
    aggregated_weights: np.ndarray
    client_contributions: Dict[str, float]
    global_accuracy: float
    malicious_updates: int = 0
    round_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class TransferBackdoorResult:
    """Results from transfer learning backdoor attack."""
    source_model_name: str
    target_model_name: str
    trigger_type: str
    source_clean_accuracy: float
    target_clean_accuracy: float
    backdoor_success_rate: float
    transfer_preservation: float
    attack_detected: bool = False


@dataclass
class CrossModalAttack:
    """Results from cross-modal poisoning attack."""
    attack_id: str
    text_embedding_drift: float
    image_embedding_drift: float
    alignment_score_before: float
    alignment_score_after: float
    attack_success_rate: float
    modality_affected: str  # 'text', 'image', 'both'


@dataclass
class MetaLearningMetrics:
    """Metrics for meta-learning attack assessment."""
    n_tasks: int
    poison_ratio: float
    pre_attack_adaptation: float
    post_attack_adaptation: float
    adaptation_degradation: float
    robustness_score: float
    attack_detected: bool = False


# ============================================================================
# Advanced Poisoning Attacks Class
# ============================================================================

class AdvancedPoisoningAttacks:
    """
    Advanced ML poisoning attack simulator for educational purposes.
    
    This class implements sophisticated attack vectors to demonstrate
    vulnerabilities in modern ML systems including federated learning,
    transfer learning, multimodal systems, and meta-learning.
    
    Attributes:
        educational_use: Must be True to enable attacks (safety feature)
        seed: Random seed for reproducibility
        audit_log: List of all operations performed
        
    Example:
        >>> attacks = AdvancedPoisoningAttacks(educational_use=True, seed=42)
        >>> attacks.simulate_federated_learning(n_clients=10, n_rounds=5)
        >>> attacks.inject_client_poison(client_id="client_3", poison_ratio=0.1)
        >>> metrics = attacks.measure_fl_robustness()
        >>> attacks.visualize_fl_attack(save_path="fl_attack.png")
    """
    
    def __init__(self, educational_use: bool = False, seed: Optional[int] = None):
        """
        Initialize advanced poisoning attacks simulator.
        
        Args:
            educational_use: Must be True to enable functionality (default: False)
            seed: Random seed for reproducibility (default: None)
            
        Raises:
            ValueError: If educational_use is False
        """
        if not educational_use:
            raise ValueError(
                "educational_use must be True. This module is for educational purposes only."
            )
        
        self.educational_use = True
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        self.audit_log: List[Dict[str, Any]] = []
        self._log_operation("INIT", "AdvancedPoisoningAttacks initialized", {"seed": seed})
        
        # Federated Learning State
        self.fl_clients: List[FederatedClient] = []
        self.fl_rounds: List[FLRound] = []
        self.global_model_weights: Optional[np.ndarray] = None
        self.fl_robustness_score: Optional[float] = None
        
        # Transfer Learning State
        self.transfer_results: List[TransferBackdoorResult] = []
        
        # Cross-Modal State
        self.cross_modal_attacks: List[CrossModalAttack] = []
        
        # Meta-Learning State
        self.meta_metrics: Optional[MetaLearningMetrics] = None
        
        # Safety limits
        self.max_poison_ratio = 0.30  # Maximum 30% poisoning allowed
        self.max_clients = 100
        self.max_rounds = 50
        
    def _log_operation(self, operation: str, description: str, details: Dict[str, Any] = None):
        """Log an operation for audit trail."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "description": description,
            "details": details or {}
        }
        self.audit_log.append(log_entry)
        logger.info(f"[AUDIT] {operation}: {description}")
        
    def _validate_poison_ratio(self, ratio: float) -> float:
        """Validate and clamp poison ratio to safe limits."""
        if ratio < 0:
            logger.warning(f"Negative poison ratio {ratio}, clamping to 0")
            return 0.0
        if ratio > self.max_poison_ratio:
            logger.warning(
                f"Poison ratio {ratio} exceeds max {self.max_poison_ratio}, clamping"
            )
            return self.max_poison_ratio
        return ratio
    
    # ========================================================================
    # Federated Learning Attacks
    # ========================================================================
    
    def simulate_federated_learning(
        self,
        n_clients: int = 10,
        n_rounds: int = 5,
        model_dim: int = 100
    ) -> List[FLRound]:
        """
        Simulate federated learning training rounds.
        
        Creates synthetic clients with heterogeneous data distributions and
        simulates the FL aggregation process (FedAvg-style).
        
        Args:
            n_clients: Number of participating clients (default: 10)
            n_rounds: Number of training rounds (default: 5)
            model_dim: Dimension of model weights (default: 100)
            
        Returns:
            List of FLRound objects for each round
            
        Example:
            >>> attacks = AdvancedPoisoningAttacks(educational_use=True)
            >>> rounds = attacks.simulate_federated_learning(n_clients=10, n_rounds=5)
            >>> for r in rounds:
            ...     print(f"Round {r.round_number}: accuracy={r.global_accuracy:.3f}")
        """
        self._log_operation(
            "SIMULATE_FL",
            f"Simulating FL with {n_clients} clients, {n_rounds} rounds",
            {"n_clients": n_clients, "n_rounds": n_rounds, "model_dim": model_dim}
        )
        
        n_clients = min(n_clients, self.max_clients)
        n_rounds = min(n_rounds, self.max_rounds)
        
        # Initialize clients with heterogeneous data
        self.fl_clients = self._initialize_fl_clients(n_clients, model_dim)
        self.global_model_weights = np.random.randn(model_dim) * 0.1
        
        self.fl_rounds = []
        
        for round_num in range(n_rounds):
            # Select participating clients (typically 50-80%)
            participation_rate = np.random.uniform(0.5, 0.8)
            n_participating = max(1, int(n_clients * participation_rate))
            participating_indices = np.random.choice(
                n_clients, size=n_participating, replace=False
            )
            participating_clients = [self.fl_clients[i] for i in participating_indices]
            
            # Collect local updates
            local_updates = []
            client_weights = []
            
            for client in participating_clients:
                # Simulate local training
                update = self._simulate_local_training(client, round_num)
                local_updates.append(update)
                client_weights.append(client.local_data_size)
            
            # Aggregate using weighted average (FedAvg)
            total_weight = sum(client_weights)
            normalized_weights = [w / total_weight for w in client_weights]
            
            aggregated = np.zeros_like(self.global_model_weights)
            for update, weight in zip(local_updates, normalized_weights):
                aggregated += weight * update
            
            self.global_model_weights = aggregated
            
            # Calculate global accuracy (degrades if malicious clients present)
            malicious_count = sum(1 for c in participating_clients if c.is_malicious)
            base_accuracy = 0.95 - (0.02 * round_num)  # Natural degradation
            malicious_impact = malicious_count / n_participating * 0.15
            global_accuracy = max(0.5, base_accuracy - malicious_impact)
            
            fl_round = FLRound(
                round_number=round_num,
                participating_clients=[c.client_id for c in participating_clients],
                aggregated_weights=aggregated.copy(),
                client_contributions={
                    c.client_id: w for c, w in zip(participating_clients, normalized_weights)
                },
                global_accuracy=global_accuracy,
                malicious_updates=malicious_count,
                round_metrics={
                    "participation_rate": participation_rate,
                    "convergence_metric": np.linalg.norm(aggregated - self.global_model_weights),
                    "client_heterogeneity": self._calculate_client_heterogeneity()
                }
            )
            
            self.fl_rounds.append(fl_round)
        
        self._log_operation(
            "FL_COMPLETE",
            f"Completed {n_rounds} FL rounds",
            {"final_accuracy": self.fl_rounds[-1].global_accuracy if self.fl_rounds else None}
        )
        
        return self.fl_rounds
    
    def _initialize_fl_clients(self, n_clients: int, model_dim: int) -> List[FederatedClient]:
        """Initialize federated learning clients with synthetic data."""
        clients = []
        
        for i in range(n_clients):
            # Create heterogeneous data distributions
            n_classes = np.random.randint(3, 10)
            class_probs = np.random.dirichlet(np.ones(n_classes))
            data_dist = {f"class_{j}": float(p) for j, p in enumerate(class_probs)}
            
            client = FederatedClient(
                client_id=f"client_{i}",
                local_data_size=np.random.randint(100, 1000),
                local_accuracy=np.random.uniform(0.7, 0.95),
                data_distribution=data_dist,
                is_malicious=False,
                poison_ratio=0.0,
                local_model_weights=np.random.randn(model_dim) * 0.1
            )
            clients.append(client)
        
        return clients
    
    def _simulate_local_training(
        self,
        client: FederatedClient,
        round_num: int
    ) -> np.ndarray:
        """Simulate local training on client data."""
        if client.local_model_weights is None or len(client.local_model_weights) == 0:
            client.local_model_weights = np.random.randn(len(self.global_model_weights)) * 0.1
        
        # Simulate gradient update
        gradient = np.random.randn(len(client.local_model_weights)) * 0.01
        
        if client.is_malicious:
            # Malicious client sends poisoned update
            gradient *= (1 + client.poison_ratio * 5)  # Amplify malicious update
            gradient += np.random.randn(len(gradient)) * client.poison_ratio * 0.1
        
        client.local_model_weights = client.local_model_weights + 0.1 * gradient
        return client.local_model_weights.copy()
    
    def _calculate_client_heterogeneity(self) -> float:
        """Calculate heterogeneity metric across clients."""
        if len(self.fl_clients) < 2:
            return 0.0
        
        accuracies = [c.local_accuracy for c in self.fl_clients]
        return float(np.std(accuracies))
    
    def inject_client_poison(
        self,
        client_id: str,
        poison_ratio: float
    ) -> Dict[str, Any]:
        """
        Poison a specific client's local data.
        
        Args:
            client_id: ID of the client to poison
            poison_ratio: Ratio of data to poison (0.0 to 0.3 max)
            
        Returns:
            Dict with injection metrics
            
        Example:
            >>> result = attacks.inject_client_poison("client_3", poison_ratio=0.1)
            >>> print(f"Client poisoned: {result['client_poisoned']}")
        """
        poison_ratio = self._validate_poison_ratio(poison_ratio)
        
        self._log_operation(
            "INJECT_CLIENT_POISON",
            f"Poisoning client {client_id} with ratio {poison_ratio}",
            {"client_id": client_id, "poison_ratio": poison_ratio}
        )
        
        target_client = None
        for client in self.fl_clients:
            if client.client_id == client_id:
                target_client = client
                break
        
        if target_client is None:
            return {
                "success": False,
                "error": f"Client {client_id} not found",
                "client_poisoned": False
            }
        
        target_client.is_malicious = True
        target_client.poison_ratio = poison_ratio
        
        # Adjust data distribution to reflect poisoning
        n_classes = len(target_client.data_distribution)
        for key in target_client.data_distribution:
            target_client.data_distribution[key] *= (1 - poison_ratio)
        target_client.data_distribution["poisoned_class"] = poison_ratio
        
        return {
            "success": True,
            "client_id": client_id,
            "poison_ratio": poison_ratio,
            "client_poisoned": True,
            "new_data_distribution": target_client.data_distribution
        }
    
    def model_poisoning_attack(
        self,
        malicious_updates: List[np.ndarray]
    ) -> Dict[str, Any]:
        """
        Submit malicious model updates to corrupt global aggregation.
        
        Args:
            malicious_updates: List of malicious weight updates to inject
            
        Returns:
            Dict with attack metrics
            
        Example:
            >>> malicious = [np.random.randn(100) * 5 for _ in range(3)]
            >>> result = attacks.model_poisoning_attack(malicious)
            >>> print(f"Impact score: {result['impact_score']}")
        """
        self._log_operation(
            "MODEL_POISONING",
            f"Injecting {len(malicious_updates)} malicious updates",
            {"n_updates": len(malicious_updates)}
        )
        
        if not self.fl_rounds:
            return {
                "success": False,
                "error": "No FL rounds simulated. Call simulate_federated_learning first.",
                "impact_score": 0.0
            }
        
        # Get latest round
        latest_round = self.fl_rounds[-1]
        
        # Calculate impact of malicious updates
        benign_norm = np.linalg.norm(latest_round.aggregated_weights)
        
        # Simulate injection
        malicious_sum = np.zeros_like(latest_round.aggregated_weights)
        for update in malicious_updates:
            if len(update) == len(latest_round.aggregated_weights):
                malicious_sum += update
        
        # Calculate corruption impact
        corrupted_weights = latest_round.aggregated_weights + 0.1 * malicious_sum
        corruption_norm = np.linalg.norm(corrupted_weights - latest_round.aggregated_weights)
        impact_score = corruption_norm / (benign_norm + 1e-8)
        
        # Update round metrics
        latest_round.malicious_updates += len(malicious_updates)
        latest_round.round_metrics["corruption_impact"] = float(impact_score)
        
        return {
            "success": True,
            "n_malicious_updates": len(malicious_updates),
            "impact_score": float(impact_score),
            "corruption_norm": float(corruption_norm),
            "attack_detected": impact_score > 2.0
        }
    
    def measure_fl_robustness(self) -> Dict[str, float]:
        """
        Calculate federated learning robustness metrics.
        
        Returns:
            Dict with robustness metrics
            
        Example:
            >>> metrics = attacks.measure_fl_robustness()
            >>> print(f"Robustness score: {metrics['robustness_score']}")
        """
        self._log_operation(
            "MEASURE_FL_ROBUSTNESS",
            "Calculating FL robustness metrics",
            {}
        )
        
        if not self.fl_rounds:
            return {
                "robustness_score": 0.0,
                "error": "No FL rounds simulated"
            }
        
        # Calculate metrics
        n_rounds = len(self.fl_rounds)
        malicious_ratio = sum(r.malicious_updates for r in self.fl_rounds) / (n_rounds * len(self.fl_clients))
        
        accuracy_trend = [r.global_accuracy for r in self.fl_rounds]
        accuracy_degradation = accuracy_trend[0] - accuracy_trend[-1] if n_rounds > 1 else 0
        
        convergence_metric = np.mean([r.round_metrics.get("convergence_metric", 0) for r in self.fl_rounds])
        
        # Robustness score (higher is better)
        robustness_score = (
            1.0 - malicious_ratio * 0.5 - 
            accuracy_degradation * 0.3 - 
            min(convergence_metric, 1.0) * 0.2
        )
        
        self.fl_robustness_score = max(0.0, min(1.0, robustness_score))
        
        return {
            "robustness_score": self.fl_robustness_score,
            "malicious_ratio": malicious_ratio,
            "accuracy_degradation": accuracy_degradation,
            "convergence_metric": convergence_metric,
            "n_rounds": n_rounds,
            "n_clients": len(self.fl_clients),
            "risk_level": self._get_risk_level(1.0 - self.fl_robustness_score)
        }
    
    def visualize_fl_attack(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize global model degradation over FL rounds.
        
        Args:
            save_path: Optional path to save figure
            
        Returns:
            matplotlib Figure object
            
        Example:
            >>> fig = attacks.visualize_fl_attack(save_path="fl_attack.png")
        """
        self._log_operation(
            "VISUALIZE_FL",
            f"Visualizing FL attack, save_path={save_path}",
            {"save_path": save_path}
        )
        
        if not self.fl_rounds:
            raise ValueError("No FL rounds simulated. Call simulate_federated_learning first.")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Accuracy over rounds
        rounds = [r.round_number for r in self.fl_rounds]
        accuracies = [r.global_accuracy for r in self.fl_rounds]
        malicious_counts = [r.malicious_updates for r in self.fl_rounds]
        
        axes[0, 0].plot(rounds, accuracies, 'b-o', linewidth=2, label='Global Accuracy')
        axes[0, 0].fill_between(rounds, [0.5]*len(rounds), accuracies, alpha=0.3, color='red')
        axes[0, 0].axhline(y=0.5, color='r', linestyle='--', label='Collapse Threshold')
        axes[0, 0].set_xlabel('Round')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].set_title('Global Model Accuracy Degradation')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Malicious updates per round
        axes[0, 1].bar(rounds, malicious_counts, color='red', alpha=0.7)
        axes[0, 1].set_xlabel('Round')
        axes[0, 1].set_ylabel('Malicious Updates')
        axes[0, 1].set_title('Malicious Client Updates per Round')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Client participation heatmap
        if len(self.fl_rounds) > 0 and len(self.fl_rounds[0].participating_clients) > 0:
            participation_matrix = np.zeros((len(self.fl_rounds), len(self.fl_clients)))
            for r_idx, round_data in enumerate(self.fl_rounds):
                for c_idx, client in enumerate(self.fl_clients):
                    if client.client_id in round_data.participating_clients:
                        participation_matrix[r_idx, c_idx] = 1
            
            im = axes[1, 0].imshow(participation_matrix, cmap='Blues', aspect='auto')
            axes[1, 0].set_xlabel('Client ID')
            axes[1, 0].set_ylabel('Round')
            axes[1, 0].set_title('Client Participation Heatmap')
            plt.colorbar(im, ax=axes[1, 0])
        
        # Plot 4: Robustness metrics
        if self.fl_robustness_score is not None:
            metrics = self.measure_fl_robustness()
            categories = ['Robustness', 'Accuracy Retention', 'Convergence']
            scores = [
                metrics['robustness_score'],
                1.0 - metrics['accuracy_degradation'],
                1.0 - min(metrics['convergence_metric'], 1.0)
            ]
            
            axes[1, 1].bar(categories, scores, color=['green', 'blue', 'purple'], alpha=0.7)
            axes[1, 1].set_ylim(0, 1.0)
            axes[1, 1].set_ylabel('Score')
            axes[1, 1].set_title('FL Robustness Metrics')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('Federated Learning Attack Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"FL visualization saved to {save_path}")
        
        return fig
    
    # ========================================================================
    # Transfer Learning Backdoors
    # ========================================================================
    
    def create_transfer_backdoor(
        self,
        source_model: str,
        target_task: str,
        trigger_type: str
    ) -> Dict[str, Any]:
        """
        Create a backdoor in a pre-trained model for transfer learning.
        
        Args:
            source_model: Name of source pre-trained model (e.g., "ResNet50")
            target_task: Target task for transfer (e.g., "image_classification")
            trigger_type: Type of trigger ("pattern", "noise", "semantic")
            
        Returns:
            Dict with backdoor creation metrics
            
        Example:
            >>> result = attacks.create_transfer_backdoor(
            ...     source_model="ResNet50",
            ...     target_task="image_classification",
            ...     trigger_type="pattern"
            ... )
        """
        self._log_operation(
            "CREATE_TRANSFER_BACKDOOR",
            f"Creating backdoor: {source_model} -> {target_task}",
            {"source_model": source_model, "target_task": target_task, "trigger_type": trigger_type}
        )
        
        # Simulate backdoor creation
        backdoor_strength = np.random.uniform(0.7, 0.95)
        clean_performance = np.random.uniform(0.85, 0.95)
        
        return {
            "success": True,
            "source_model": source_model,
            "target_task": target_task,
            "trigger_type": trigger_type,
            "backdoor_strength": backdoor_strength,
            "clean_performance": clean_performance,
            "backdoor_id": f"backdoor_{source_model}_{target_task}_{len(self.transfer_results)}"
        }
    
    def fine_tune_with_backdoor(
        self,
        model: str,
        clean_data: Dict[str, Any],
        poisoned_data: Dict[str, Any]
    ) -> TransferBackdoorResult:
        """
        Fine-tune model while preserving implanted backdoor.
        
        Args:
            model: Model identifier
            clean_data: Clean training data dict
            poisoned_data: Poisoned training data dict
            
        Returns:
            TransferBackdoorResult with metrics
        """
        poison_ratio = self._validate_poison_ratio(
            poisoned_data.get("ratio", 0.1)
        )
        
        self._log_operation(
            "FINE_TUNE_BACKDOOR",
            f"Fine-tuning {model} with backdoor",
            {"model": model, "poison_ratio": poison_ratio}
        )
        
        # Simulate fine-tuning
        source_accuracy = np.random.uniform(0.88, 0.95)
        target_accuracy = source_accuracy * (1 - np.random.uniform(0.02, 0.08))
        backdoor_success = np.random.uniform(0.75, 0.95)
        
        result = TransferBackdoorResult(
            source_model_name=model,
            target_model_name=f"{model}_finetuned",
            trigger_type="pattern",
            source_clean_accuracy=source_accuracy,
            target_clean_accuracy=target_accuracy,
            backdoor_success_rate=backdoor_success,
            transfer_preservation=backdoor_success / source_accuracy,
            attack_detected=backdoor_success < 0.5
        )
        
        self.transfer_results.append(result)
        return result
    
    def test_backdoor_transfer(self) -> Dict[str, Any]:
        """
        Verify backdoor persists after transfer learning.
        
        Returns:
            Dict with transfer test results
        """
        self._log_operation(
            "TEST_BACKDOOR_TRANSFER",
            "Testing backdoor persistence",
            {"n_results": len(self.transfer_results)}
        )
        
        if not self.transfer_results:
            return {
                "success": False,
                "error": "No transfer results to test",
                "persistence_rate": 0.0
            }
        
        # Calculate persistence across all transfers
        persistence_rates = [r.transfer_preservation for r in self.transfer_results]
        avg_persistence = np.mean(persistence_rates)
        
        return {
            "success": True,
            "n_transfers_tested": len(self.transfer_results),
            "avg_persistence": float(avg_persistence),
            "min_persistence": float(np.min(persistence_rates)),
            "max_persistence": float(np.max(persistence_rates)),
            "backdoors_detected": sum(1 for r in self.transfer_results if r.attack_detected)
        }
    
    def measure_transfer_effectiveness(self) -> Dict[str, float]:
        """
        Calculate attack success rate on target task.
        
        Returns:
            Dict with effectiveness metrics
        """
        self._log_operation(
            "MEASURE_TRANSFER_EFFECTIVENESS",
            "Measuring transfer attack effectiveness",
            {}
        )
        
        if not self.transfer_results:
            return {
                "effectiveness_score": 0.0,
                "error": "No transfer results available"
            }
        
        avg_success = np.mean([r.backdoor_success_rate for r in self.transfer_results])
        avg_clean_perf = np.mean([r.target_clean_accuracy for r in self.transfer_results])
        
        effectiveness = avg_success * 0.7 + avg_clean_perf * 0.3
        
        return {
            "effectiveness_score": float(effectiveness),
            "avg_backdoor_success": float(avg_success),
            "avg_clean_accuracy": float(avg_clean_perf),
            "n_attacks": len(self.transfer_results),
            "detection_rate": sum(1 for r in self.transfer_results if r.attack_detected) / len(self.transfer_results)
        }
    
    # ========================================================================
    # Cross-Modal Poisoning
    # ========================================================================
    
    def generate_text_to_image_poison(
        self,
        text_prompt: str,
        target_image_class: str
    ) -> Dict[str, Any]:
        """
        Generate poisoned text-image pairs for multimodal attacks.
        
        Args:
            text_prompt: Original text prompt
            target_image_class: Target class to associate
            
        Returns:
            Dict with poisoning metrics
        """
        self._log_operation(
            "GENERATE_TEXT_IMAGE_POISON",
            f"Poisoning text-image pair: {text_prompt[:50]}...",
            {"text_prompt_length": len(text_prompt), "target_class": target_image_class}
        )
        
        # Simulate embedding manipulation
        text_drift = np.random.uniform(0.1, 0.3)
        image_drift = np.random.uniform(0.1, 0.3)
        
        return {
            "success": True,
            "text_prompt": text_prompt,
            "target_image_class": target_image_class,
            "text_embedding_drift": text_drift,
            "image_embedding_drift": image_drift,
            "poisoned_pair_id": f"pair_{len(self.cross_modal_attacks)}"
        }
    
    def attack_multimodal_model(
        self,
        model: str,
        poisoned_pairs: List[Dict[str, Any]]
    ) -> CrossModalAttack:
        """
        Attack CLIP-style multimodal models with poisoned pairs.
        
        Args:
            model: Model identifier (e.g., "CLIP", "ALIGN")
            poisoned_pairs: List of poisoned text-image pairs
            
        Returns:
            CrossModalAttack with results
        """
        self._log_operation(
            "ATTACK_MULTIMODAL",
            f"Attacking {model} with {len(poisoned_pairs)} poisoned pairs",
            {"model": model, "n_pairs": len(poisoned_pairs)}
        )
        
        # Simulate attack
        alignment_before = np.random.uniform(0.85, 0.95)
        alignment_after = alignment_before * (1 - np.random.uniform(0.15, 0.35))
        
        text_drift = np.mean([p.get("text_embedding_drift", 0.2) for p in poisoned_pairs])
        image_drift = np.mean([p.get("image_embedding_drift", 0.2) for p in poisoned_pairs])
        
        attack = CrossModalAttack(
            attack_id=f"cross_modal_{model}_{len(self.cross_modal_attacks)}",
            text_embedding_drift=text_drift,
            image_embedding_drift=image_drift,
            alignment_score_before=alignment_before,
            alignment_score_after=alignment_after,
            attack_success_rate=1.0 - (alignment_after / alignment_before),
            modality_affected="both"
        )
        
        self.cross_modal_attacks.append(attack)
        return attack
    
    def measure_cross_modal_impact(self) -> Dict[str, float]:
        """
        Measure degradation in both text and image modalities.
        
        Returns:
            Dict with impact metrics
        """
        self._log_operation(
            "MEASURE_CROSS_MODAL_IMPACT",
            "Measuring cross-modal attack impact",
            {"n_attacks": len(self.cross_modal_attacks)}
        )
        
        if not self.cross_modal_attacks:
            return {
                "impact_score": 0.0,
                "error": "No cross-modal attacks performed"
            }
        
        avg_text_drift = np.mean([a.text_embedding_drift for a in self.cross_modal_attacks])
        avg_image_drift = np.mean([a.image_embedding_drift for a in self.cross_modal_attacks])
        avg_alignment_loss = np.mean([
            a.alignment_score_before - a.alignment_score_after 
            for a in self.cross_modal_attacks
        ])
        
        impact_score = (avg_text_drift + avg_image_drift + avg_alignment_loss) / 3.0
        
        return {
            "impact_score": float(impact_score),
            "avg_text_drift": float(avg_text_drift),
            "avg_image_drift": float(avg_image_drift),
            "avg_alignment_loss": float(avg_alignment_loss),
            "n_attacks": len(self.cross_modal_attacks),
            "risk_level": self._get_risk_level(impact_score)
        }
    
    # ========================================================================
    # Meta-Learning Attacks
    # ========================================================================
    
    def poison_meta_training(
        self,
        n_tasks: int,
        poison_ratio: float
    ) -> Dict[str, Any]:
        """
        Poison meta-learning training set (MAML-style).
        
        Args:
            n_tasks: Number of meta-training tasks
            poison_ratio: Ratio of tasks to poison (0.0 to 0.3 max)
            
        Returns:
            Dict with poisoning metrics
        """
        poison_ratio = self._validate_poison_ratio(poison_ratio)
        
        self._log_operation(
            "POISON_META_TRAINING",
            f"Poisoning {n_tasks} meta-tasks with ratio {poison_ratio}",
            {"n_tasks": n_tasks, "poison_ratio": poison_ratio}
        )
        
        n_poisoned = int(n_tasks * poison_ratio)
        
        return {
            "success": True,
            "n_tasks": n_tasks,
            "n_poisoned_tasks": n_poisoned,
            "poison_ratio": poison_ratio,
            "meta_poison_id": f"meta_poison_{n_tasks}_{len(self.audit_log)}"
        }
    
    def attack_fast_adaptation(self) -> MetaLearningMetrics:
        """
        Degrade fast adaptation capability in meta-learning.
        
        Returns:
            MetaLearningMetrics with adaptation metrics
        """
        self._log_operation(
            "ATTACK_FAST_ADAPTATION",
            "Measuring fast adaptation degradation",
            {}
        )
        
        # Simulate adaptation metrics
        pre_attack = np.random.uniform(0.85, 0.95)
        post_attack = pre_attack * (1 - np.random.uniform(0.2, 0.4))
        degradation = pre_attack - post_attack
        
        metrics = MetaLearningMetrics(
            n_tasks=10,
            poison_ratio=0.2,
            pre_attack_adaptation=pre_attack,
            post_attack_adaptation=post_attack,
            adaptation_degradation=degradation,
            robustness_score=1.0 - degradation,
            attack_detected=degradation > 0.3
        )
        
        self.meta_metrics = metrics
        return metrics
    
    def measure_meta_robustness(self) -> Dict[str, float]:
        """
        Calculate meta-learning robustness score.
        
        Returns:
            Dict with robustness metrics
        """
        self._log_operation(
            "MEASURE_META_ROBUSTNESS",
            "Calculating meta-learning robustness",
            {}
        )
        
        if self.meta_metrics is None:
            return {
                "robustness_score": 0.0,
                "error": "No meta-learning metrics available"
            }
        
        return {
            "robustness_score": float(self.meta_metrics.robustness_score),
            "adaptation_degradation": float(self.meta_metrics.adaptation_degradation),
            "pre_attack_performance": float(self.meta_metrics.pre_attack_adaptation),
            "post_attack_performance": float(self.meta_metrics.post_attack_adaptation),
            "attack_detected": self.meta_metrics.attack_detected,
            "risk_level": self._get_risk_level(1.0 - self.meta_metrics.robustness_score)
        }
    
    # ========================================================================
    # Educational Scenarios
    # ========================================================================
    
    def run_educational_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """
        Run all predefined educational scenarios.
        
        Returns:
            Dict with results for each scenario
        """
        self._log_operation(
            "RUN_EDUCATIONAL_SCENARIOS",
            "Running all educational scenarios",
            {}
        )
        
        results = {}
        
        # Scenario 1: Single malicious client in FL (10% poisoning)
        results["scenario_1_single_malicious_fl"] = self._scenario_single_malicious_fl()
        
        # Scenario 2: Coordinated FL attack (3/10 clients malicious)
        results["scenario_2_coordinated_fl"] = self._scenario_coordinated_fl()
        
        # Scenario 3: Transfer backdoor from ResNet to VGG
        results["scenario_3_transfer_backdoor"] = self._scenario_transfer_backdoor()
        
        # Scenario 4: Cross-modal attack on CLIP-style model
        results["scenario_4_cross_modal"] = self._scenario_cross_modal()
        
        # Scenario 5: Meta-learning poisoning (MAML-style)
        results["scenario_5_meta_learning"] = self._scenario_meta_learning()
        
        return results
    
    def _scenario_single_malicious_fl(self) -> Dict[str, Any]:
        """Scenario 1: Single malicious client in FL (10% poisoning)."""
        # Reset state
        self.fl_clients = []
        self.fl_rounds = []
        
        # Simulate FL
        rounds = self.simulate_federated_learning(n_clients=10, n_rounds=5)
        
        # Inject poison into one client
        self.inject_client_poison("client_3", poison_ratio=0.1)
        
        # Measure impact
        metrics = self.measure_fl_robustness()
        
        return {
            "scenario_name": "Single Malicious Client (10%)",
            "description": "One client out of 10 is malicious with 10% poisoned data",
            "robustness_score": metrics.get("robustness_score", 0.0),
            "risk_level": metrics.get("risk_level", "UNKNOWN"),
            "final_accuracy": rounds[-1].global_accuracy if rounds else 0.0
        }
    
    def _scenario_coordinated_fl(self) -> Dict[str, Any]:
        """Scenario 2: Coordinated FL attack (3/10 clients malicious)."""
        # Reset state
        self.fl_clients = []
        self.fl_rounds = []
        
        # Simulate FL
        rounds = self.simulate_federated_learning(n_clients=10, n_rounds=5)
        
        # Inject poison into 3 clients
        for i in [2, 5, 8]:
            self.inject_client_poison(f"client_{i}", poison_ratio=0.15)
        
        # Measure impact
        metrics = self.measure_fl_robustness()
        
        return {
            "scenario_name": "Coordinated FL Attack (3/10 clients)",
            "description": "Three clients out of 10 are malicious with 15% poisoned data each",
            "robustness_score": metrics.get("robustness_score", 0.0),
            "risk_level": metrics.get("risk_level", "UNKNOWN"),
            "final_accuracy": rounds[-1].global_accuracy if rounds else 0.0
        }
    
    def _scenario_transfer_backdoor(self) -> Dict[str, Any]:
        """Scenario 3: Transfer backdoor from ResNet to VGG."""
        # Create backdoor
        backdoor_info = self.create_transfer_backdoor(
            source_model="ResNet50",
            target_task="image_classification",
            trigger_type="pattern"
        )
        
        # Fine-tune with backdoor
        result = self.fine_tune_with_backdoor(
            model="ResNet50",
            clean_data={"samples": 1000, "classes": 10},
            poisoned_data={"ratio": 0.15, "trigger_type": "pattern"}
        )
        
        # Test transfer
        transfer_test = self.test_backdoor_transfer()
        effectiveness = self.measure_transfer_effectiveness()
        
        return {
            "scenario_name": "Transfer Backdoor (ResNet -> VGG)",
            "description": "Backdoor implanted in ResNet50 persists through transfer to VGG",
            "backdoor_success_rate": result.backdoor_success_rate,
            "transfer_preservation": result.transfer_preservation,
            "effectiveness_score": effectiveness.get("effectiveness_score", 0.0),
            "attack_detected": result.attack_detected
        }
    
    def _scenario_cross_modal(self) -> Dict[str, Any]:
        """Scenario 4: Cross-modal attack on CLIP-style model."""
        # Generate poisoned pairs
        poisoned_pairs = []
        for i in range(5):
            pair = self.generate_text_to_image_poison(
                text_prompt=f"A photo of object {i}",
                target_image_class=f"target_class_{i}"
            )
            poisoned_pairs.append(pair)
        
        # Attack multimodal model
        attack = self.attack_multimodal_model("CLIP", poisoned_pairs)
        
        # Measure impact
        impact = self.measure_cross_modal_impact()
        
        return {
            "scenario_name": "Cross-Modal Attack (CLIP)",
            "description": "Poisoned text-image pairs degrade CLIP alignment",
            "attack_success_rate": attack.attack_success_rate,
            "alignment_loss": attack.alignment_score_before - attack.alignment_score_after,
            "impact_score": impact.get("impact_score", 0.0),
            "modality_affected": attack.modality_affected
        }
    
    def _scenario_meta_learning(self) -> Dict[str, Any]:
        """Scenario 5: Meta-learning poisoning (MAML-style)."""
        # Poison meta-training
        poison_result = self.poison_meta_training(n_tasks=20, poison_ratio=0.2)
        
        # Attack fast adaptation
        metrics = self.attack_fast_adaptation()
        
        # Measure robustness
        robustness = self.measure_meta_robustness()
        
        return {
            "scenario_name": "Meta-Learning Poisoning (MAML)",
            "description": "20% of meta-training tasks poisoned, degrading fast adaptation",
            "adaptation_degradation": metrics.adaptation_degradation,
            "robustness_score": robustness.get("robustness_score", 0.0),
            "risk_level": robustness.get("risk_level", "UNKNOWN"),
            "attack_detected": metrics.attack_detected
        }
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def _get_risk_level(self, score: float) -> str:
        """Convert risk score to risk level string."""
        if score < 0.3:
            return "LOW"
        elif score < 0.5:
            return "MODERATE"
        elif score < 0.7:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def export_audit_log(self, output_path: str) -> str:
        """
        Export audit log to JSON file.
        
        Args:
            output_path: Path to save audit log
            
        Returns:
            Path to saved file
        """
        with open(output_path, 'w') as f:
            json.dump(self.audit_log, f, indent=2, default=str)
        
        logger.info(f"Audit log exported to {output_path}")
        return output_path
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of all operations performed.
        
        Returns:
            Dict with operation summary
        """
        return {
            "educational_use": self.educational_use,
            "seed": self.seed,
            "n_operations": len(self.audit_log),
            "fl_clients": len(self.fl_clients),
            "fl_rounds": len(self.fl_rounds),
            "transfer_results": len(self.transfer_results),
            "cross_modal_attacks": len(self.cross_modal_attacks),
            "meta_metrics": self.meta_metrics is not None,
            "fl_robustness_score": self.fl_robustness_score
        }


def run_educational_examples():
    """Run comprehensive educational examples for all advanced attack types."""
    print("=" * 80)
    print("NIFLHEIM Advanced ML Poisoning - Educational Examples")
    print("=" * 80)
    
    # Initialize with educational flag
    attacks = AdvancedPoisoningAttacks(educational_use=True, seed=42)
    
    # Run all educational scenarios
    print("\nRunning educational scenarios...\n")
    results = attacks.run_educational_scenarios()
    
    for scenario_name, scenario_results in results.items():
        print(f"\n{scenario_name.upper()}:")
        print(f"  Description: {scenario_results['description']}")
        if 'robustness_score' in scenario_results:
            print(f"  Robustness Score: {scenario_results['robustness_score']:.3f}")
        if 'risk_level' in scenario_results:
            print(f"  Risk Level: {scenario_results['risk_level']}")
        if 'attack_success_rate' in scenario_results:
            print(f"  Attack Success Rate: {scenario_results['attack_success_rate']:.3f}")
    
    # Export audit log
    audit_path = "advanced_poisoning_audit.json"
    attacks.export_audit_log(audit_path)
    print(f"\nAudit log exported to: {audit_path}")
    
    # Print summary
    summary = attacks.get_summary()
    print(f"\nSummary:")
    print(f"  Total operations: {summary['n_operations']}")
    print(f"  FL clients: {summary['fl_clients']}")
    print(f"  FL rounds: {summary['fl_rounds']}")
    print(f"  Transfer attacks: {summary['transfer_results']}")
    print(f"  Cross-modal attacks: {summary['cross_modal_attacks']}")
    
    print("\n" + "=" * 80)
    print("Educational examples completed successfully!")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    run_educational_examples()
