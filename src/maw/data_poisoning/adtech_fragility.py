"""
Adtech Fragility Module for NIFLHEIM

Demonstrates real-time bidding (RTB) vulnerabilities and signal pollution
in the adtech ecosystem, as described in Addie LaMarr's "Data Poisoning:
The Fatal Flaw in Mass Surveillance".

This module simulates:
- RTB auction mechanics and bidder behavior
- Signal pollution through clickstream noise and user agent spoofing
- Cookie syncing disruption and identity graph fragmentation
- Ecosystem fragility metrics and visualization

Educational Purpose:
    - Demonstrate RTB ecosystem vulnerabilities to data poisoning
    - Show how signal pollution degrades targeting accuracy
    - Illustrate cookie syncing fragility and match rate collapse
    - Quantify ecosystem-wide fragility from coordinated attacks
    - Provide visual evidence of adtech system brittleness

Author: NIFLHEIM Educational Systems
Date: 2026-09-13
"""

from __future__ import annotations

import json
import random
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap


@dataclass
class BidRequest:
    """Represents a real-time bidding auction request."""
    impression_id: str
    user_id: str
    publisher_domain: str
    ad_format: str  # "banner", "video", "native", "interstitial"
    placement: str  # "above_fold", "below_fold", "sidebar"
    device_type: str  # "mobile", "desktop", "tablet"
    geo_location: Tuple[str, str]  # (country, region)
    context_keywords: List[str]
    timestamp: datetime
    user_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "impression_id": self.impression_id,
            "user_id": self.user_id,
            "publisher_domain": self.publisher_domain,
            "ad_format": self.ad_format,
            "placement": self.placement,
            "device_type": self.device_type,
            "geo_location": list(self.geo_location),
            "context_keywords": self.context_keywords,
            "timestamp": self.timestamp.isoformat(),
            "user_data": self.user_data
        }


@dataclass
class BidResponse:
    """Represents a bidder's response to an auction request."""
    bidder_id: str
    impression_id: str
    bid_amount: float  # CPM (cost per mille)
    ad_creative_id: str
    targeting_score: float  # 0.0 to 1.0 relevance
    win_probability: float  # Estimated win probability
    response_time_ms: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "bidder_id": self.bidder_id,
            "impression_id": self.impression_id,
            "bid_amount": self.bid_amount,
            "ad_creative_id": self.ad_creative_id,
            "targeting_score": self.targeting_score,
            "win_probability": self.win_probability,
            "response_time_ms": self.response_time_ms
        }


@dataclass
class AuctionResult:
    """Result of a completed RTB auction."""
    impression_id: str
    winning_bidder: Optional[str]
    winning_bid: float
    clearing_price: float  # Second-price auction
    bid_count: int
    auction_duration_ms: float
    all_bids: List[BidResponse] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "impression_id": self.impression_id,
            "winning_bidder": self.winning_bidder,
            "winning_bid": self.winning_bid,
            "clearing_price": self.clearing_price,
            "bid_count": self.bid_count,
            "auction_duration_ms": self.auction_duration_ms,
            "total_bid_value": sum(b.bid_amount for b in self.all_bids)
        }


@dataclass
class CookieSyncRecord:
    """Represents a cookie synchronization attempt between domains."""
    sync_id: str
    source_domain: str
    target_domain: str
    user_match: bool  # Whether user was matched
    sync_success: bool  # Whether sync completed
    matched_user_id: Optional[str]
    timestamp: datetime
    sync_duration_ms: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sync_id": self.sync_id,
            "source_domain": self.source_domain,
            "target_domain": self.target_domain,
            "user_match": self.user_match,
            "sync_success": self.sync_success,
            "matched_user_id": self.matched_user_id,
            "timestamp": self.timestamp.isoformat(),
            "sync_duration_ms": self.sync_duration_ms
        }


@dataclass
class SignalMetrics:
    """Metrics for tracking signal quality and ecosystem health."""
    timestamp: datetime
    user_identification_accuracy: float  # 0.0 to 1.0
    conversion_attribution_reliability: float  # 0.0 to 1.0
    roi_calculation_distortion: float  # 0.0 (none) to 1.0 (severe)
    audience_segmentation_quality: float  # 0.0 to 1.0
    cookie_match_rate: float  # 0.0 to 1.0
    signal_to_noise_ratio: float  # Higher is better
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "user_identification_accuracy": self.user_identification_accuracy,
            "conversion_attribution_reliability": self.conversion_attribution_reliability,
            "roi_calculation_distortion": self.roi_calculation_distortion,
            "audience_segmentation_quality": self.audience_segmentation_quality,
            "cookie_match_rate": self.cookie_match_rate,
            "signal_to_noise_ratio": self.signal_to_noise_ratio
        }


class BidderAgent:
    """Simulates an adtech bidder with specific strategies."""
    
    BIDDER_TYPES = {
        "aggressive": {
            "base_bid": 8.0,
            "bid_variance": 3.0,
            "targeting_sensitivity": 0.3,
            "response_speed": 50  # ms
        },
        "conservative": {
            "base_bid": 3.0,
            "bid_variance": 1.0,
            "targeting_sensitivity": 0.7,
            "response_speed": 80
        },
        "premium": {
            "base_bid": 15.0,
            "bid_variance": 5.0,
            "targeting_sensitivity": 0.5,
            "response_speed": 40
        },
        "budget": {
            "base_bid": 1.5,
            "bid_variance": 0.5,
            "targeting_sensitivity": 0.2,
            "response_speed": 100
        },
        "programmatic": {
            "base_bid": 5.0,
            "bid_variance": 2.0,
            "targeting_sensitivity": 0.6,
            "response_speed": 60
        }
    }
    
    def __init__(self, bidder_id: str, bidder_type: str = "programmatic", seed: Optional[int] = None):
        self.bidder_id = bidder_id
        self.bidder_type = bidder_type
        self.config = self.BIDDER_TYPES.get(bidder_type, self.BIDDER_TYPES["programmatic"])
        self.rng = np.random.default_rng(seed)
        self.bid_history: List[float] = []
        self.win_history: List[bool] = []
        self.total_spend = 0.0
        self.total_wins = 0
    
    def generate_bid(self, bid_request: BidRequest) -> BidResponse:
        """Generate a bid response for an auction request."""
        # Calculate targeting score based on user data match
        targeting_score = self._calculate_targeting_score(bid_request)
        
        # Adjust bid based on targeting quality and context
        base_bid = self.config["base_bid"]
        bid_adjustment = targeting_score * self.config["targeting_sensitivity"]
        
        # Add variance
        bid_variance = self.rng.normal(0, self.config["bid_variance"])
        final_bid = max(0.5, base_bid + (bid_adjustment * 10) + bid_variance)
        
        # Calculate response time
        response_time = max(10, self.config["response_speed"] + self.rng.normal(0, 20))
        
        # Estimate win probability (simplified)
        win_probability = min(0.9, final_bid / 20.0)
        
        bid_response = BidResponse(
            bidder_id=self.bidder_id,
            impression_id=bid_request.impression_id,
            bid_amount=round(final_bid, 2),
            ad_creative_id=f"creative_{self.rng.integers(1000, 9999)}",
            targeting_score=round(targeting_score, 3),
            win_probability=round(win_probability, 3),
            response_time_ms=round(response_time, 1)
        )
        
        self.bid_history.append(final_bid)
        return bid_response
    
    def _calculate_targeting_score(self, bid_request: BidRequest) -> float:
        """Calculate how well the impression matches bidder's targets."""
        # Simplified targeting logic
        score = 0.5  # Base score
        
        # Device targeting
        if bid_request.device_type == "desktop":
            score += 0.1
        elif bid_request.device_type == "mobile":
            score += 0.15
        
        # Placement targeting
        if bid_request.placement == "above_fold":
            score += 0.2
        
        # Context matching (simplified)
        premium_keywords = ["finance", "technology", "business", "luxury"]
        if any(kw in bid_request.context_keywords for kw in premium_keywords):
            score += 0.15
        
        return min(1.0, score)
    
    def record_auction_result(self, won: bool, price: float = 0.0):
        """Record the result of an auction."""
        self.win_history.append(won)
        if won:
            self.total_wins += 1
            self.total_spend += price


class AdtechFragilitySimulator:
    """
    Simulates adtech ecosystem vulnerabilities to data poisoning.
    
    This simulator demonstrates how the real-time bidding ecosystem
    becomes fragile when subjected to signal pollution, cookie disruption,
    and coordinated attacks.
    
    Attributes:
        ecosystem_config: Configuration for the adtech ecosystem
        pollution_ratio: Current signal pollution level (0.0 to 1.0)
        sync_disruption_ratio: Cookie sync disruption level (0.0 to 1.0)
        ecosystem_fragility: Calculated fragility score (0.0 to 1.0)
    """
    
    ECOSYSTEM_CONFIGS = {
        "default": {
            "num_bidders": 8,
            "bidder_types": ["aggressive", "conservative", "premium", "budget", "programmatic"],
            "base_match_rate": 0.75,
            "base_signal_quality": 0.85,
            "auction_timeout_ms": 100
        },
        "fragmented": {
            "num_bidders": 15,
            "bidder_types": ["aggressive", "conservative", "premium", "budget", "programmatic"] * 3,
            "base_match_rate": 0.45,
            "base_signal_quality": 0.60,
            "auction_timeout_ms": 150
        },
        "consolidated": {
            "num_bidders": 4,
            "bidder_types": ["premium", "aggressive", "programmatic", "conservative"],
            "base_match_rate": 0.85,
            "base_signal_quality": 0.92,
            "auction_timeout_ms": 80
        }
    }
    
    def __init__(self, ecosystem_config: str = 'default', seed: Optional[int] = None):
        """
        Initialize the Adtech Fragility Simulator.
        
        Args:
            ecosystem_config: Configuration preset ('default', 'fragmented', 'consolidated')
            seed: Random seed for reproducibility
        """
        self.ecosystem_config = ecosystem_config
        self.config = self.ECOSYSTEM_CONFIGS.get(ecosystem_config, self.ECOSYSTEM_CONFIGS["default"])
        self.rng = np.random.default_rng(seed)
        random.seed(seed)
        
        # Initialize bidder agents
        self.bidders: List[BidderAgent] = []
        self._initialize_bidders()
        
        # State tracking
        self.auction_history: List[AuctionResult] = []
        self.cookie_sync_history: List[CookieSyncRecord] = []
        self.signal_metrics_history: List[SignalMetrics] = []
        
        # Pollution state
        self.pollution_ratio = 0.0
        self.sync_disruption_ratio = 0.0
        self.ecosystem_fragility = 0.0
        
        # Domains for cookie syncing simulation
        self.tracking_domains = [
            "googleads.com", "doubleclick.net", "facebook.com", "amazon-adsystem.com",
            "criteo.com", "rubiconproject.com", "appnexus.com", "pubmatic.com",
            "openx.com", "taboola.com", "outbrain.com", "taboola.com"
        ]
    
    def _initialize_bidders(self):
        """Initialize bidder agents based on ecosystem configuration."""
        self.bidders = []
        bidder_types = self.config["bidder_types"][:self.config["num_bidders"]]
        
        for i, btype in enumerate(bidder_types):
            bidder = BidderAgent(
                bidder_id=f"bidder_{i:03d}",
                bidder_type=btype,
                seed=self.rng.integers(0, 10000)
            )
            self.bidders.append(bidder)
    
    def simulate_rtb_auction(self, bid_requests: Optional[List[BidRequest]] = None) -> List[AuctionResult]:
        """
        Simulate real-time bidding auctions for a batch of impression requests.
        
        Args:
            bid_requests: List of bid requests to auction. If None, generates synthetic requests.
            
        Returns:
            List of AuctionResult for each impression
        """
        if bid_requests is None:
            bid_requests = self._generate_synthetic_bid_requests(100)
        
        auction_results = []
        
        for request in bid_requests:
            # Collect bids from all bidders
            bid_responses = []
            for bidder in self.bidders:
                try:
                    bid = bidder.generate_bid(request)
                    bid_responses.append(bid)
                except Exception:
                    # Bidder failed to respond (timeout or error)
                    continue
            
            # Run second-price auction
            result = self._run_second_price_auction(request, bid_responses)
            auction_results.append(result)
            
            # Update bidder records
            for i, bid in enumerate(bid_responses):
                won = (result.winning_bidder == bid.bidder_id)
                price = result.clearing_price if won else 0.0
                self.bidders[i].record_auction_result(won, price)
        
        self.auction_history.extend(auction_results)
        return auction_results
    
    def _generate_synthetic_bid_requests(self, count: int) -> List[BidRequest]:
        """Generate synthetic bid requests for simulation."""
        requests = []
        
        domains = ["publisher1.com", "news-site.com", "blog.net", "video-platform.com", "social-app.io"]
        formats = ["banner", "video", "native", "interstitial"]
        placements = ["above_fold", "below_fold", "sidebar"]
        devices = ["mobile", "desktop", "tablet"]
        locations = [("US", "CA"), ("US", "NY"), ("US", "TX"), ("UK", "London"), ("DE", "Berlin")]
        contexts = [
            ["technology", "gadgets"],
            ["finance", "investing"],
            ["sports", "fitness"],
            ["travel", "vacation"],
            ["food", "cooking"],
            ["fashion", "style"],
            ["business", "news"]
        ]
        
        for i in range(count):
            user_id = hashlib.sha256(
                f"user_{self.rng.integers(100000, 999999)}".encode()
            ).hexdigest()[:16]
            
            impression_id = hashlib.sha256(
                f"imp_{datetime.utcnow().timestamp()}_{i}".encode()
            ).hexdigest()[:16]
            
            # Generate user data (potentially poisoned)
            user_data = self._generate_user_data()
            
            request = BidRequest(
                impression_id=impression_id,
                user_id=user_id,
                publisher_domain=random.choice(domains),
                ad_format=random.choice(formats),
                placement=random.choice(placements),
                device_type=random.choice(devices),
                geo_location=random.choice(locations),
                context_keywords=random.choice(contexts),
                timestamp=datetime.utcnow(),
                user_data=user_data
            )
            requests.append(request)
        
        return requests
    
    def _generate_user_data(self) -> Dict[str, Any]:
        """Generate synthetic user data with potential pollution."""
        base_data = {
            "age_range": random.choice(["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]),
            "gender": random.choice(["M", "F", "U"]),
            "interests": random.sample(
                ["tech", "sports", "finance", "travel", "food", "fashion", "gaming", "health"],
                k=random.randint(2, 5)
            ),
            "income_bracket": random.choice(["low", "medium", "high"]),
            "purchase_intent": round(self.rng.random(), 2)
        }
        
        # Apply pollution if configured
        if self.pollution_ratio > 0 and self.rng.random() < self.pollution_ratio:
            base_data = self._pollute_user_data(base_data)
        
        return base_data
    
    def _pollute_user_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply pollution to user data."""
        polluted = user_data.copy()
        
        pollution_type = random.choice([
            "age_scramble", "interest_noise", "intent_inflation", "identity_spoof"
        ])
        
        if pollution_type == "age_scramble":
            polluted["age_range"] = random.choice(["18-24", "65+"])
        elif pollution_type == "interest_noise":
            polluted["interests"].extend(["spam", "noise", "fake"])
        elif pollution_type == "intent_inflation":
            polluted["purchase_intent"] = min(1.0, polluted["purchase_intent"] * 3)
        elif pollution_type == "identity_spoof":
            polluted["gender"] = "U"
            polluted["income_bracket"] = "unknown"
        
        return polluted
    
    def _run_second_price_auction(self, request: BidRequest, 
                                   bids: List[BidResponse]) -> AuctionResult:
        """
        Run a second-price sealed-bid auction.
        
        Highest bidder wins but pays the second-highest bid price.
        """
        if not bids:
            return AuctionResult(
                impression_id=request.impression_id,
                winning_bidder=None,
                winning_bid=0.0,
                clearing_price=0.0,
                bid_count=0,
                auction_duration_ms=0.0
            )
        
        # Sort bids by amount (descending)
        sorted_bids = sorted(bids, key=lambda b: b.bid_amount, reverse=True)
        
        winner = sorted_bids[0]
        second_price = sorted_bids[1].bid_amount if len(sorted_bids) > 1 else winner.bid_amount * 0.9
        
        auction_duration = max(b.response_time_ms for b in bids)
        
        return AuctionResult(
            impression_id=request.impression_id,
            winning_bidder=winner.bidder_id,
            winning_bid=winner.bid_amount,
            clearing_price=round(second_price, 2),
            bid_count=len(bids),
            auction_duration_ms=round(auction_duration, 1),
            all_bids=bids
        )
    
    def inject_signal_pollution(self, pollution_ratio: float = 0.1) -> Dict[str, Any]:
        """
        Inject noise into tracking signals to degrade data quality.
        
        Args:
            pollution_ratio: Ratio of signals to pollute (0.0 to 1.0)
            
        Returns:
            Metrics on pollution injection
        """
        self.pollution_ratio = min(1.0, max(0.0, pollution_ratio))
        
        pollution_metrics = {
            "clickstream_noise_injected": 0,
            "user_agent_spoofed": 0,
            "referrer_polluted": 0,
            "timestamp_jittered": 0,
            "total_signals_affected": 0
        }
        
        # Simulate pollution across different signal types
        num_signals = len(self.auction_history) * 3  # Approximate signal count
        
        pollution_metrics["clickstream_noise_injected"] = int(num_signals * pollution_ratio * 0.3)
        pollution_metrics["user_agent_spoofed"] = int(num_signals * pollution_ratio * 0.25)
        pollution_metrics["referrer_polluted"] = int(num_signals * pollution_ratio * 0.25)
        pollution_metrics["timestamp_jittered"] = int(num_signals * pollution_ratio * 0.2)
        pollution_metrics["total_signals_affected"] = sum([
            pollution_metrics["clickstream_noise_injected"],
            pollution_metrics["user_agent_spoofed"],
            pollution_metrics["referrer_polluted"],
            pollution_metrics["timestamp_jittered"]
        ])
        
        return pollution_metrics
    
    def poison_cookie_syncing(self, sync_ratio: float = 0.2) -> Dict[str, Any]:
        """
        Disrupt cookie synchronization between domains.
        
        Args:
            sync_ratio: Ratio of sync attempts to disrupt (0.0 to 1.0)
            
        Returns:
            Metrics on cookie sync disruption
        """
        self.sync_disruption_ratio = min(1.0, max(0.0, sync_ratio))
        
        # Simulate cookie sync attempts
        num_syncs = len(self.tracking_domains) * (len(self.tracking_domains) - 1)
        sync_results = {
            "total_sync_attempts": num_syncs,
            "successful_syncs": 0,
            "failed_syncs": 0,
            "match_rate_before": self.config["base_match_rate"],
            "match_rate_after": 0.0,
            "sync_records": []
        }
        
        for i, source in enumerate(self.tracking_domains):
            for j, target in enumerate(self.tracking_domains):
                if i >= j:
                    continue
                
                sync_id = hashlib.sha256(
                    f"sync_{source}_{target}_{datetime.utcnow().timestamp()}".encode()
                ).hexdigest()[:16]
                
                # Determine if sync would normally succeed
                base_success = self.rng.random() < self.config["base_match_rate"]
                
                # Apply disruption
                if self.rng.random() < self.sync_disruption_ratio:
                    # Sync fails due to poisoning
                    success = False
                else:
                    success = base_success
                
                sync_duration = self.rng.normal(50, 20) if success else self.rng.normal(200, 50)
                sync_duration = max(10, sync_duration)
                
                record = CookieSyncRecord(
                    sync_id=sync_id,
                    source_domain=source,
                    target_domain=target,
                    user_match=base_success,
                    sync_success=success,
                    matched_user_id=f"user_{self.rng.integers(10000, 99999)}" if success else None,
                    timestamp=datetime.utcnow(),
                    sync_duration_ms=round(sync_duration, 1)
                )
                
                sync_results["sync_records"].append(record)
                self.cookie_sync_history.append(record)
                
                if success:
                    sync_results["successful_syncs"] += 1
                else:
                    sync_results["failed_syncs"] += 1
        
        # Calculate post-disruption match rate
        if sync_results["total_sync_attempts"] > 0:
            sync_results["match_rate_after"] = (
                sync_results["successful_syncs"] / sync_results["total_sync_attempts"]
            )
        
        return sync_results
    
    def measure_ecosystem_fragility(self) -> SignalMetrics:
        """
        Calculate comprehensive ecosystem fragility metrics.
        
        Returns:
            SignalMetrics with current ecosystem health indicators
        """
        # Calculate user identification accuracy
        base_accuracy = self.config["base_signal_quality"]
        accuracy_degradation = self.pollution_ratio * 0.6  # Up to 60% degradation
        user_id_accuracy = max(0.1, base_accuracy - accuracy_degradation)
        
        # Calculate conversion attribution reliability
        attribution_base = 0.80
        attribution_degradation = (self.pollution_ratio * 0.4) + (self.sync_disruption_ratio * 0.3)
        attribution_reliability = max(0.1, attribution_base - attribution_degradation)
        
        # Calculate ROI distortion
        roi_distortion = min(0.95, (self.pollution_ratio * 0.5) + (self.sync_disruption_ratio * 0.35))
        
        # Calculate audience segmentation quality
        segmentation_base = 0.75
        segmentation_degradation = self.pollution_ratio * 0.5
        segmentation_quality = max(0.1, segmentation_base - segmentation_degradation)
        
        # Calculate cookie match rate
        cookie_match_rate = self.config["base_match_rate"] * (1 - self.sync_disruption_ratio * 0.8)
        
        # Calculate signal-to-noise ratio
        signal_quality = (user_id_accuracy + attribution_reliability + segmentation_quality) / 3
        noise_level = self.pollution_ratio
        snr = signal_quality / (noise_level + 0.1)  # Add small epsilon to avoid division by zero
        
        metrics = SignalMetrics(
            timestamp=datetime.utcnow(),
            user_identification_accuracy=round(user_id_accuracy, 3),
            conversion_attribution_reliability=round(attribution_reliability, 3),
            roi_calculation_distortion=round(roi_distortion, 3),
            audience_segmentation_quality=round(segmentation_quality, 3),
            cookie_match_rate=round(cookie_match_rate, 3),
            signal_to_noise_ratio=round(snr, 3)
        )
        
        self.signal_metrics_history.append(metrics)
        
        # Calculate overall ecosystem fragility
        self.ecosystem_fragility = self._calculate_fragility_score(metrics)
        
        return metrics
    
    def _calculate_fragility_score(self, metrics: SignalMetrics) -> float:
        """
        Calculate overall ecosystem fragility score.
        
        Higher score = more fragile (vulnerable to collapse)
        """
        # Weight different fragility components
        weights = {
            "accuracy_inverse": 0.25,
            "attribution_inverse": 0.20,
            "roi_distortion": 0.20,
            "segmentation_inverse": 0.15,
            "cookie_degradation": 0.20
        }
        
        fragility = (
            weights["accuracy_inverse"] * (1 - metrics.user_identification_accuracy) +
            weights["attribution_inverse"] * (1 - metrics.conversion_attribution_reliability) +
            weights["roi_distortion"] * metrics.roi_calculation_distortion +
            weights["segmentation_inverse"] * (1 - metrics.audience_segmentation_quality) +
            weights["cookie_degradation"] * (1 - metrics.cookie_match_rate)
        )
        
        return round(min(1.0, fragility), 3)
    
    def visualize_impact(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Generate comprehensive matplotlib visualizations of adtech fragility.
        
        Creates a multi-panel figure showing:
        1. RTB auction flow diagram
        2. Signal pollution impact over time
        3. Cookie sync match rate degradation
        4. Ecosystem fragility heatmap
        
        Args:
            save_path: Optional path to save the figure
            
        Returns:
            Matplotlib Figure object
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Adtech Ecosystem Fragility Analysis', fontsize=16, fontweight='bold')
        
        # Panel 1: RTB Auction Flow
        self._plot_auction_flow(axes[0, 0])
        
        # Panel 2: Signal Pollution Impact
        self._plot_signal_pollution_impact(axes[0, 1])
        
        # Panel 3: Cookie Sync Degradation
        self._plot_cookie_sync_degradation(axes[1, 0])
        
        # Panel 4: Ecosystem Fragility Heatmap
        self._plot_fragility_heatmap(axes[1, 1])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        
        return fig
    
    def _plot_auction_flow(self, ax: plt.Axes):
        """Plot RTB auction flow diagram."""
        ax.set_title('RTB Auction Flow', fontsize=12, fontweight='bold')
        ax.axis('off')
        
        # Create flow diagram using text and arrows
        positions = {
            'user': (0.1, 0.5),
            'publisher': (0.3, 0.5),
            'exchange': (0.5, 0.5),
            'bidders': (0.7, 0.5),
            'winner': (0.9, 0.5)
        }
        
        labels = ['User Visit', 'Publisher', 'Ad Exchange', 'Bidders', 'Winner']
        
        for label, (x, y) in zip(labels, positions.values()):
            ax.annotate(label, xy=(x, y), xytext=(x, y),
                       ha='center', va='center',
                       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7),
                       fontsize=10, fontweight='bold')
        
        # Draw arrows
        arrow_positions = [
            (positions['user'], positions['publisher']),
            (positions['publisher'], positions['exchange']),
            (positions['exchange'], positions['bidders']),
            (positions['bidders'], positions['exchange']),
            (positions['exchange'], positions['winner'])
        ]
        
        for start, end in arrow_positions:
            ax.annotate('', xy=end, xytext=start,
                       arrowprops=dict(arrowstyle='->', color='gray', lw=2))
        
        # Add auction stats
        if self.auction_history:
            avg_clearing = np.mean([a.clearing_price for a in self.auction_history])
            avg_bids = np.mean([a.bid_count for a in self.auction_history])
            stats_text = f'Avg Clearing: ${avg_clearing:.2f}\nAvg Bids: {avg_bids:.1f}'
            ax.text(0.5, 0.1, stats_text, transform=ax.transAxes,
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def _plot_signal_pollution_impact(self, ax: plt.Axes):
        """Plot signal pollution impact over simulation cycles."""
        ax.set_title('Signal Pollution Impact Over Time', fontsize=12, fontweight='bold')
        ax.set_xlabel('Simulation Cycle')
        ax.set_ylabel('Metric Value')
        
        # Generate time series data
        cycles = list(range(len(self.signal_metrics_history)))
        if not cycles:
            cycles = [0]
            # Create dummy metrics for visualization
            dummy_metrics = SignalMetrics(
                timestamp=datetime.utcnow(),
                user_identification_accuracy=0.85 - self.pollution_ratio * 0.6,
                conversion_attribution_reliability=0.80 - self.pollution_ratio * 0.4,
                roi_calculation_distortion=self.pollution_ratio * 0.5,
                audience_segmentation_quality=0.75 - self.pollution_ratio * 0.5,
                cookie_match_rate=self.config["base_match_rate"] * (1 - self.sync_disruption_ratio * 0.8),
                signal_to_noise_ratio=(0.8 - self.pollution_ratio * 0.6) / (self.pollution_ratio + 0.1)
            )
            self.signal_metrics_history = [dummy_metrics]
        
        accuracies = [m.user_identification_accuracy for m in self.signal_metrics_history]
        attributions = [m.conversion_attribution_reliability for m in self.signal_metrics_history]
        rois = [m.roi_calculation_distortion for m in self.signal_metrics_history]
        snrs = [m.signal_to_noise_ratio for m in self.signal_metrics_history]
        
        ax.plot(cycles, accuracies, 'b-o', label='User ID Accuracy', linewidth=2, markersize=6)
        ax.plot(cycles, attributions, 'g-s', label='Attribution Reliability', linewidth=2, markersize=6)
        ax.plot(cycles, rois, 'r-^', label='ROI Distortion', linewidth=2, markersize=6)
        ax.plot(cycles, snrs, 'm-d', label='Signal/Noise Ratio', linewidth=2, markersize=6)
        
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1.0)
    
    def _plot_cookie_sync_degradation(self, ax: plt.Axes):
        """Plot cookie sync match rate degradation."""
        ax.set_title('Cookie Sync Match Rate Degradation', fontsize=12, fontweight='bold')
        ax.set_xlabel('Sync Disruption Ratio')
        ax.set_ylabel('Match Rate')
        
        # Generate degradation curve
        disruption_ratios = np.linspace(0, 1, 20)
        match_rates = []
        
        for ratio in disruption_ratios:
            match_rate = self.config["base_match_rate"] * (1 - ratio * 0.8)
            match_rates.append(match_rate)
        
        ax.fill_between(disruption_ratios, match_rates, alpha=0.3, color='orange')
        ax.plot(disruption_ratios, match_rates, 'o-', color='darkorange', linewidth=2, markersize=6)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        
        # Add current point
        if self.sync_disruption_ratio > 0:
            current_rate = self.config["base_match_rate"] * (1 - self.sync_disruption_ratio * 0.8)
            ax.scatter([self.sync_disruption_ratio], [current_rate], 
                      c='red', s=100, zorder=5, label='Current')
            ax.legend(loc='upper right', fontsize=9)
    
    def _plot_fragility_heatmap(self, ax: plt.Axes):
        """Plot ecosystem fragility heatmap."""
        ax.set_title('Ecosystem Fragility Heatmap', fontsize=12, fontweight='bold')
        ax.set_xlabel('Signal Pollution')
        ax.set_ylabel('Cookie Disruption')
        
        # Generate fragility matrix
        pollution_levels = np.linspace(0, 1, 15)
        disruption_levels = np.linspace(0, 1, 15)
        
        fragility_matrix = np.zeros((len(disruption_levels), len(pollution_levels)))
        
        for i, disruption in enumerate(disruption_levels):
            for j, pollution in enumerate(pollution_levels):
                # Simulate metrics for this combination
                user_acc = max(0.1, self.config["base_signal_quality"] - pollution * 0.6)
                attr_rel = max(0.1, 0.80 - pollution * 0.4 - disruption * 0.3)
                roi_dist = min(0.95, pollution * 0.5 + disruption * 0.35)
                seg_qual = max(0.1, 0.75 - pollution * 0.5)
                cookie_rate = self.config["base_match_rate"] * (1 - disruption * 0.8)
                
                # Calculate fragility
                fragility = (
                    0.25 * (1 - user_acc) +
                    0.20 * (1 - attr_rel) +
                    0.20 * roi_dist +
                    0.15 * (1 - seg_qual) +
                    0.20 * (1 - cookie_rate)
                )
                fragility_matrix[i, j] = min(1.0, fragility)
        
        # Create heatmap
        cmap = LinearSegmentedColormap.from_list('fragility', 
                                                  ['green', 'yellow', 'orange', 'red'],
                                                  N=100)
        
        im = ax.imshow(fragility_matrix, cmap=cmap, origin='lower', 
                       extent=[0, 1, 0, 1], aspect='auto', vmin=0, vmax=1)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Fragility Score', fontsize=9)
        
        # Mark current operating point
        if self.pollution_ratio > 0 or self.sync_disruption_ratio > 0:
            ax.scatter([self.pollution_ratio], [self.sync_disruption_ratio],
                      c='blue', s=150, marker='X', zorder=5, label='Current')
            ax.legend(loc='upper left', fontsize=9)
    
    def export_report(self, output_path: str) -> Dict[str, Any]:
        """
        Generate comprehensive JSON/CSV report of simulation results.
        
        Args:
            output_path: Path to save the report (JSON or CSV based on extension)
            
        Returns:
            Report data as dictionary
        """
        report = {
            "simulation_metadata": {
                "ecosystem_config": self.ecosystem_config,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "pollution_ratio": self.pollution_ratio,
                "sync_disruption_ratio": self.sync_disruption_ratio,
                "ecosystem_fragility": self.ecosystem_fragility
            },
            "auction_summary": {
                "total_auctions": len(self.auction_history),
                "avg_clearing_price": round(np.mean([a.clearing_price for a in self.auction_history]), 2) if self.auction_history else 0,
                "avg_bid_count": round(np.mean([a.bid_count for a in self.auction_history]), 2) if self.auction_history else 0,
                "avg_auction_duration_ms": round(np.mean([a.auction_duration_ms for a in self.auction_history]), 2) if self.auction_history else 0
            },
            "cookie_sync_summary": {
                "total_syncs": len(self.cookie_sync_history),
                "successful_syncs": sum(1 for s in self.cookie_sync_history if s.sync_success),
                "failed_syncs": sum(1 for s in self.cookie_sync_history if not s.sync_success),
                "match_rate": round(sum(1 for s in self.cookie_sync_history if s.sync_success) / max(1, len(self.cookie_sync_history)), 3)
            },
            "signal_metrics": [m.to_dict() for m in self.signal_metrics_history],
            "bidder_performance": [
                {
                    "bidder_id": b.bidder_id,
                    "bidder_type": b.bidder_type,
                    "total_wins": b.total_wins,
                    "total_spend": round(b.total_spend, 2),
                    "win_rate": round(b.total_wins / max(1, len(b.win_history)), 3),
                    "avg_bid": round(np.mean(b.bid_history), 2) if b.bid_history else 0
                }
                for b in self.bidders
            ],
            "fragility_assessment": {
                "overall_fragility": self.ecosystem_fragility,
                "risk_level": self._get_risk_level(self.ecosystem_fragility),
                "recommendations": self._generate_recommendations()
            }
        }
        
        # Save to file
        path = Path(output_path)
        if path.suffix.lower() == '.json':
            with open(path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
        elif path.suffix.lower() == '.csv':
            import csv
            # Export signal metrics as CSV
            if self.signal_metrics_history:
                with open(path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.signal_metrics_history[0].to_dict().keys())
                    writer.writeheader()
                    for metrics in self.signal_metrics_history:
                        writer.writerow(metrics.to_dict())
        else:
            # Default to JSON
            with open(path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
        
        return report
    
    def _get_risk_level(self, fragility: float) -> str:
        """Convert fragility score to risk level."""
        if fragility < 0.3:
            return "LOW"
        elif fragility < 0.5:
            return "MODERATE"
        elif fragility < 0.7:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on simulation results."""
        recommendations = []
        
        if self.pollution_ratio > 0.3:
            recommendations.append("Implement signal validation to detect and filter polluted data")
        
        if self.sync_disruption_ratio > 0.3:
            recommendations.append("Diversify identity resolution methods beyond cookie syncing")
        
        if self.ecosystem_fragility > 0.5:
            recommendations.append("Ecosystem approaching collapse threshold - reduce dependency on fragile signals")
        
        if not recommendations:
            recommendations.append("Ecosystem operating within normal parameters")
        
        return recommendations


def run_educational_scenarios() -> Dict[str, Any]:
    """
    Run predefined educational scenarios demonstrating adtech fragility.
    
    Returns:
        Dictionary of scenario results
    """
    scenarios = {
        "low_pollution": {"pollution": 0.1, "disruption": 0.0},
        "medium_pollution": {"pollution": 0.25, "disruption": 0.1},
        "high_pollution": {"pollution": 0.5, "disruption": 0.3},
        "coordinated_attack": {"pollution": 0.5, "disruption": 0.5}
    }
    
    results = {}
    
    for scenario_name, params in scenarios.items():
        print(f"\n{'='*60}")
        print(f"Scenario: {scenario_name.upper()}")
        print(f"{'='*60}")
        
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        # Run auctions
        print("Running RTB auctions...")
        sim.simulate_rtb_auction()
        
        # Inject pollution
        print(f"Injecting signal pollution ({params['pollution']*100:.0f}%)...")
        pollution_metrics = sim.inject_signal_pollution(params['pollution'])
        
        # Disrupt cookie syncing
        print(f"Disrupting cookie syncing ({params['disruption']*100:.0f}%)...")
        sync_metrics = sim.poison_cookie_syncing(params['disruption'])
        
        # Measure fragility
        print("Measuring ecosystem fragility...")
        fragility_metrics = sim.measure_ecosystem_fragility()
        
        results[scenario_name] = {
            "parameters": params,
            "pollution_metrics": pollution_metrics,
            "sync_metrics": {
                "match_rate_before": sync_metrics["match_rate_before"],
                "match_rate_after": sync_metrics["match_rate_after"],
                "failed_syncs": sync_metrics["failed_syncs"]
            },
            "fragility_metrics": fragility_metrics.to_dict(),
            "ecosystem_fragility": sim.ecosystem_fragility,
            "risk_level": sim._get_risk_level(sim.ecosystem_fragility)
        }
        
        print(f"\nEcosystem Fragility: {sim.ecosystem_fragility:.3f}")
        print(f"Risk Level: {sim._get_risk_level(sim.ecosystem_fragility)}")
        print(f"User ID Accuracy: {fragility_metrics.user_identification_accuracy:.3f}")
        print(f"Cookie Match Rate: {fragility_metrics.cookie_match_rate:.3f}")
    
    return results


if __name__ == "__main__":
    print("="*60)
    print("NIFLHEIM Adtech Fragility Module")
    print("="*60)
    
    # Run educational scenarios
    results = run_educational_scenarios()
    
    # Generate visualization
    print("\n\nGenerating visualization...")
    sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
    sim.simulate_rtb_auction()
    sim.inject_signal_pollution(0.3)
    sim.poison_cookie_syncing(0.4)
    sim.measure_ecosystem_fragility()
    
    fig = sim.visualize_impact()
    plt.savefig("adtech_fragility_analysis.png", dpi=150, bbox_inches='tight')
    print("Visualization saved to: adtech_fragility_analysis.png")
    
    # Export report
    report = sim.export_report("adtech_fragility_report.json")
    print(f"Report exported to: adtech_fragility_report.json")
    print(f"\nOverall Ecosystem Fragility: {sim.ecosystem_fragility:.3f}")
    print(f"Risk Level: {sim._get_risk_level(sim.ecosystem_fragility)}")
    
    print("\n" + "="*60)
    print("Educational demonstration complete.")
    print("="*60)
