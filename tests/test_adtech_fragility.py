"""
Test Suite for Adtech Fragility Module

Comprehensive tests for the AdtechFragilitySimulator class,
covering RTB auction simulation, signal pollution, cookie sync
disruption, and ecosystem fragility measurement.

Educational Purpose:
    - Validate RTB auction mechanics
    - Test signal pollution injection
    - Verify cookie sync disruption
    - Confirm fragility metric calculations
    - Ensure visualization and export functionality

Author: NIFLHEIM Educational Systems
Date: 2026-09-13
"""

import pytest
import json
import numpy as np
from datetime import datetime
from pathlib import Path
import tempfile
import os

# Import module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from maw.data_poisoning.adtech_fragility import (
    AdtechFragilitySimulator,
    BidderAgent,
    BidRequest,
    BidResponse,
    AuctionResult,
    CookieSyncRecord,
    SignalMetrics,
    run_educational_scenarios
)


class TestBidRequest:
    """Tests for BidRequest dataclass."""
    
    def test_bid_request_creation(self):
        """Test basic BidRequest creation."""
        request = BidRequest(
            impression_id="imp_001",
            user_id="user_123",
            publisher_domain="test.com",
            ad_format="banner",
            placement="above_fold",
            device_type="desktop",
            geo_location=("US", "CA"),
            context_keywords=["tech", "news"],
            timestamp=datetime.utcnow()
        )
        
        assert request.impression_id == "imp_001"
        assert request.user_id == "user_123"
        assert request.publisher_domain == "test.com"
        assert request.ad_format == "banner"
        assert len(request.context_keywords) == 2
    
    def test_bid_request_to_dict(self):
        """Test BidRequest serialization."""
        request = BidRequest(
            impression_id="imp_002",
            user_id="user_456",
            publisher_domain="example.com",
            ad_format="video",
            placement="below_fold",
            device_type="mobile",
            geo_location=("UK", "London"),
            context_keywords=["sports"],
            timestamp=datetime.utcnow(),
            user_data={"age": "25-34"}
        )
        
        data = request.to_dict()
        
        assert data["impression_id"] == "imp_002"
        assert data["user_id"] == "user_456"
        assert data["ad_format"] == "video"
        assert data["geo_location"] == ["UK", "London"]
        assert data["user_data"]["age"] == "25-34"


class TestBidResponse:
    """Tests for BidResponse dataclass."""
    
    def test_bid_response_creation(self):
        """Test basic BidResponse creation."""
        response = BidResponse(
            bidder_id="bidder_001",
            impression_id="imp_001",
            bid_amount=5.50,
            ad_creative_id="creative_123",
            targeting_score=0.85,
            win_probability=0.70,
            response_time_ms=45.2
        )
        
        assert response.bidder_id == "bidder_001"
        assert response.bid_amount == 5.50
        assert response.targeting_score == 0.85
        assert response.win_probability == 0.70
    
    def test_bid_response_to_dict(self):
        """Test BidResponse serialization."""
        response = BidResponse(
            bidder_id="bidder_002",
            impression_id="imp_002",
            bid_amount=8.25,
            ad_creative_id="creative_456",
            targeting_score=0.92,
            win_probability=0.88,
            response_time_ms=38.5
        )
        
        data = response.to_dict()
        
        assert data["bid_amount"] == 8.25
        assert data["targeting_score"] == 0.92
        assert "response_time_ms" in data


class TestAuctionResult:
    """Tests for AuctionResult dataclass."""
    
    def test_auction_result_creation(self):
        """Test basic AuctionResult creation."""
        result = AuctionResult(
            impression_id="imp_001",
            winning_bidder="bidder_001",
            winning_bid=7.50,
            clearing_price=6.25,
            bid_count=5,
            auction_duration_ms=78.3
        )
        
        assert result.winning_bidder == "bidder_001"
        assert result.winning_bid == 7.50
        assert result.clearing_price == 6.25
        assert result.bid_count == 5
    
    def test_auction_result_no_winner(self):
        """Test AuctionResult with no winner."""
        result = AuctionResult(
            impression_id="imp_002",
            winning_bidder=None,
            winning_bid=0.0,
            clearing_price=0.0,
            bid_count=0,
            auction_duration_ms=0.0
        )
        
        assert result.winning_bidder is None
        assert result.winning_bid == 0.0
    
    def test_auction_result_to_dict(self):
        """Test AuctionResult serialization."""
        result = AuctionResult(
            impression_id="imp_003",
            winning_bidder="bidder_003",
            winning_bid=9.00,
            clearing_price=8.50,
            bid_count=7,
            auction_duration_ms=65.0
        )
        
        data = result.to_dict()
        
        assert data["clearing_price"] == 8.50
        assert data["bid_count"] == 7
        assert "total_bid_value" in data


class TestCookieSyncRecord:
    """Tests for CookieSyncRecord dataclass."""
    
    def test_cookie_sync_record_creation(self):
        """Test basic CookieSyncRecord creation."""
        record = CookieSyncRecord(
            sync_id="sync_001",
            source_domain="googleads.com",
            target_domain="doubleclick.net",
            user_match=True,
            sync_success=True,
            matched_user_id="user_12345",
            timestamp=datetime.utcnow(),
            sync_duration_ms=45.2
        )
        
        assert record.source_domain == "googleads.com"
        assert record.target_domain == "doubleclick.net"
        assert record.user_match is True
        assert record.sync_success is True
    
    def test_cookie_sync_record_failure(self):
        """Test CookieSyncRecord for failed sync."""
        record = CookieSyncRecord(
            sync_id="sync_002",
            source_domain="facebook.com",
            target_domain="amazon-adsystem.com",
            user_match=False,
            sync_success=False,
            matched_user_id=None,
            timestamp=datetime.utcnow(),
            sync_duration_ms=250.0
        )
        
        assert record.sync_success is False
        assert record.matched_user_id is None
    
    def test_cookie_sync_record_to_dict(self):
        """Test CookieSyncRecord serialization."""
        record = CookieSyncRecord(
            sync_id="sync_003",
            source_domain="criteo.com",
            target_domain="rubiconproject.com",
            user_match=True,
            sync_success=True,
            matched_user_id="user_67890",
            timestamp=datetime.utcnow(),
            sync_duration_ms=52.3
        )
        
        data = record.to_dict()
        
        assert data["sync_success"] is True
        assert "timestamp" in data
        assert "sync_duration_ms" in data


class TestSignalMetrics:
    """Tests for SignalMetrics dataclass."""
    
    def test_signal_metrics_creation(self):
        """Test basic SignalMetrics creation."""
        metrics = SignalMetrics(
            timestamp=datetime.utcnow(),
            user_identification_accuracy=0.85,
            conversion_attribution_reliability=0.78,
            roi_calculation_distortion=0.22,
            audience_segmentation_quality=0.72,
            cookie_match_rate=0.68,
            signal_to_noise_ratio=3.5
        )
        
        assert metrics.user_identification_accuracy == 0.85
        assert metrics.conversion_attribution_reliability == 0.78
        assert metrics.roi_calculation_distortion == 0.22
    
    def test_signal_metrics_to_dict(self):
        """Test SignalMetrics serialization."""
        metrics = SignalMetrics(
            timestamp=datetime.utcnow(),
            user_identification_accuracy=0.80,
            conversion_attribution_reliability=0.75,
            roi_calculation_distortion=0.30,
            audience_segmentation_quality=0.70,
            cookie_match_rate=0.65,
            signal_to_noise_ratio=3.2
        )
        
        data = metrics.to_dict()
        
        assert "timestamp" in data
        assert data["cookie_match_rate"] == 0.65
        assert data["signal_to_noise_ratio"] == 3.2


class TestBidderAgent:
    """Tests for BidderAgent class."""
    
    def test_bidder_agent_creation(self):
        """Test BidderAgent initialization."""
        agent = BidderAgent(
            bidder_id="test_bidder_001",
            bidder_type="aggressive",
            seed=42
        )
        
        assert agent.bidder_id == "test_bidder_001"
        assert agent.bidder_type == "aggressive"
        assert agent.config["base_bid"] == 8.0
    
    def test_bidder_agent_types(self):
        """Test different bidder types."""
        types = ["aggressive", "conservative", "premium", "budget", "programmatic"]
        
        for bidder_type in types:
            agent = BidderAgent(
                bidder_id=f"test_{bidder_type}",
                bidder_type=bidder_type,
                seed=42
            )
            assert agent.bidder_type == bidder_type
            assert "base_bid" in agent.config
    
    def test_bidder_agent_generate_bid(self):
        """Test bid generation."""
        agent = BidderAgent(
            bidder_id="test_bidder_002",
            bidder_type="programmatic",
            seed=42
        )
        
        request = BidRequest(
            impression_id="imp_test_001",
            user_id="user_test",
            publisher_domain="test.com",
            ad_format="banner",
            placement="above_fold",
            device_type="desktop",
            geo_location=("US", "CA"),
            context_keywords=["tech"],
            timestamp=datetime.utcnow()
        )
        
        bid = agent.generate_bid(request)
        
        assert bid.bidder_id == "test_bidder_002"
        assert bid.impression_id == "imp_test_001"
        assert bid.bid_amount > 0
        assert 0 <= bid.targeting_score <= 1
        assert 0 <= bid.win_probability <= 1
    
    def test_bidder_agent_record_result(self):
        """Test auction result recording."""
        agent = BidderAgent(
            bidder_id="test_bidder_003",
            bidder_type="conservative",
            seed=42
        )
        
        # Record wins and losses
        agent.record_auction_result(won=True, price=5.50)
        agent.record_auction_result(won=False, price=0.0)
        agent.record_auction_result(won=True, price=6.25)
        
        assert agent.total_wins == 2
        assert abs(agent.total_spend - 11.75) < 0.01
        assert len(agent.win_history) == 3
    
    def test_bidder_agent_targeting_score(self):
        """Test targeting score calculation."""
        agent = BidderAgent(
            bidder_id="test_bidder_004",
            bidder_type="premium",
            seed=42
        )
        
        # High-value request
        high_value_request = BidRequest(
            impression_id="imp_high",
            user_id="user_001",
            publisher_domain="test.com",
            ad_format="video",
            placement="above_fold",
            device_type="desktop",
            geo_location=("US", "NY"),
            context_keywords=["finance", "technology"],
            timestamp=datetime.utcnow()
        )
        
        # Low-value request
        low_value_request = BidRequest(
            impression_id="imp_low",
            user_id="user_002",
            publisher_domain="test.com",
            ad_format="banner",
            placement="below_fold",
            device_type="mobile",
            geo_location=("US", "CA"),
            context_keywords=["general"],
            timestamp=datetime.utcnow()
        )
        
        bid_high = agent.generate_bid(high_value_request)
        bid_low = agent.generate_bid(low_value_request)
        
        # High-value should have better targeting score
        assert bid_high.targeting_score > bid_low.targeting_score


class TestAdtechFragilitySimulator:
    """Tests for AdtechFragilitySimulator class."""
    
    def test_simulator_initialization(self):
        """Test simulator initialization with different configs."""
        configs = ["default", "fragmented", "consolidated"]
        
        for config in configs:
            sim = AdtechFragilitySimulator(ecosystem_config=config, seed=42)
            assert sim.ecosystem_config == config
            assert len(sim.bidders) > 0
            assert sim.pollution_ratio == 0.0
    
    def test_simulator_default_config(self):
        """Test default ecosystem configuration."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        assert sim.config["num_bidders"] == 8
        assert sim.config["base_match_rate"] == 0.75
        assert sim.config["base_signal_quality"] == 0.85
    
    def test_simulate_rtb_auction(self):
        """Test RTB auction simulation."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        results = sim.simulate_rtb_auction()
        
        assert len(results) > 0
        assert len(sim.auction_history) == len(results)
        
        # Check auction result structure
        for result in results:
            assert isinstance(result, AuctionResult)
            assert result.bid_count >= 0
            assert result.clearing_price >= 0
    
    def test_simulate_rtb_auction_custom_requests(self):
        """Test auction simulation with custom bid requests."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        custom_requests = [
            BidRequest(
                impression_id=f"custom_{i}",
                user_id=f"user_{i}",
                publisher_domain="custom.com",
                ad_format="banner",
                placement="above_fold",
                device_type="desktop",
                geo_location=("US", "CA"),
                context_keywords=["test"],
                timestamp=datetime.utcnow()
            )
            for i in range(10)
        ]
        
        results = sim.simulate_rtb_auction(custom_requests)
        
        assert len(results) == 10
        assert all(r.impression_id.startswith("custom_") for r in results)
    
    def test_inject_signal_pollution(self):
        """Test signal pollution injection."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        # Run some auctions first
        sim.simulate_rtb_auction()
        
        pollution_metrics = sim.inject_signal_pollution(pollution_ratio=0.3)
        
        assert sim.pollution_ratio == 0.3
        assert pollution_metrics["total_signals_affected"] > 0
        assert "clickstream_noise_injected" in pollution_metrics
        assert "user_agent_spoofed" in pollution_metrics
    
    def test_inject_signal_pollution_extreme(self):
        """Test signal pollution at extreme levels."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        sim.simulate_rtb_auction()
        
        # Test 0% pollution
        metrics_0 = sim.inject_signal_pollution(0.0)
        assert sim.pollution_ratio == 0.0
        
        # Test 100% pollution
        metrics_100 = sim.inject_signal_pollution(1.0)
        assert sim.pollution_ratio == 1.0
        assert metrics_100["total_signals_affected"] > metrics_0["total_signals_affected"]
    
    def test_poison_cookie_syncing(self):
        """Test cookie syncing disruption."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        sync_results = sim.poison_cookie_syncing(sync_ratio=0.4)
        
        assert sim.sync_disruption_ratio == 0.4
        assert sync_results["total_sync_attempts"] > 0
        assert "match_rate_before" in sync_results
        assert "match_rate_after" in sync_results
        assert sync_results["match_rate_after"] < sync_results["match_rate_before"]
    
    def test_poison_cookie_syncing_extreme(self):
        """Test cookie syncing at extreme disruption levels."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        # Test 0% disruption
        results_0 = sim.poison_cookie_syncing(0.0)
        assert sim.sync_disruption_ratio == 0.0
        
        # Test 100% disruption
        results_100 = sim.poison_cookie_syncing(1.0)
        assert sim.sync_disruption_ratio == 1.0
        assert results_100["match_rate_after"] < results_0["match_rate_after"]
    
    def test_measure_ecosystem_fragility(self):
        """Test ecosystem fragility measurement."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        # Run simulation
        sim.simulate_rtb_auction()
        sim.inject_signal_pollution(0.3)
        sim.poison_cookie_syncing(0.3)
        
        metrics = sim.measure_ecosystem_fragility()
        
        assert isinstance(metrics, SignalMetrics)
        assert 0 <= metrics.user_identification_accuracy <= 1
        assert 0 <= metrics.conversion_attribution_reliability <= 1
        assert 0 <= metrics.roi_calculation_distortion <= 1
        assert 0 <= sim.ecosystem_fragility <= 1
    
    def test_measure_ecosystem_fragility_no_pollution(self):
        """Test fragility with no pollution."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        sim.simulate_rtb_auction()
        
        metrics = sim.measure_ecosystem_fragility()
        
        # Should have low fragility with no pollution
        assert sim.ecosystem_fragility < 0.5
        assert metrics.user_identification_accuracy > 0.7
    
    def test_measure_ecosystem_fragility_high_pollution(self):
        """Test fragility with high pollution."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        sim.simulate_rtb_auction()
        sim.inject_signal_pollution(0.7)
        sim.poison_cookie_syncing(0.7)
        
        metrics = sim.measure_ecosystem_fragility()
        
        # Should have high fragility
        assert sim.ecosystem_fragility > 0.5
        assert metrics.roi_calculation_distortion > 0.3
    
    def test_visualize_impact(self):
        """Test visualization generation."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        sim.simulate_rtb_auction()
        sim.inject_signal_pollution(0.3)
        sim.poison_cookie_syncing(0.3)
        sim.measure_ecosystem_fragility()
        
        save_path = "test_viz_temp.png"
        try:
            fig = sim.visualize_impact(save_path=save_path)
            assert fig is not None
            assert Path(save_path).exists()
            assert Path(save_path).stat().st_size > 0
        finally:
            if Path(save_path).exists():
                try:
                    os.unlink(save_path)
                except PermissionError:
                    pass  # Windows may lock the file
    
    def test_export_report_json(self):
        """Test JSON report export."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        sim.simulate_rtb_auction()
        sim.inject_signal_pollution(0.3)
        sim.poison_cookie_syncing(0.3)
        sim.measure_ecosystem_fragility()
        
        save_path = "test_report_temp.json"
        try:
            report = sim.export_report(save_path)
            
            assert "simulation_metadata" in report
            assert "auction_summary" in report
            assert "cookie_sync_summary" in report
            assert "signal_metrics" in report
            assert "bidder_performance" in report
            assert "fragility_assessment" in report
            
            assert report["simulation_metadata"]["pollution_ratio"] == 0.3
            assert report["simulation_metadata"]["sync_disruption_ratio"] == 0.3
            
            # Verify file was created
            assert Path(save_path).exists()
            assert Path(save_path).stat().st_size > 0
            
            # Verify JSON is valid
            with open(save_path, 'r') as f:
                loaded = json.load(f)
                assert loaded == report
        finally:
            if Path(save_path).exists():
                try:
                    os.unlink(save_path)
                except PermissionError:
                    pass  # Windows may lock the file
    
    def test_export_report_csv(self):
        """Test CSV report export."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        sim.simulate_rtb_auction()
        sim.inject_signal_pollution(0.2)
        sim.poison_cookie_syncing(0.2)
        sim.measure_ecosystem_fragility()
        
        save_path = "test_report_temp.csv"
        try:
            report = sim.export_report(save_path)
            
            assert Path(save_path).exists()
            assert Path(save_path).stat().st_size > 0
            
            # Verify CSV has headers
            with open(save_path, 'r') as f:
                header = f.readline()
                assert "timestamp" in header
                assert "user_identification_accuracy" in header
        finally:
            if Path(save_path).exists():
                try:
                    os.unlink(save_path)
                except PermissionError:
                    pass  # Windows may lock the file
    
    def test_risk_level_assessment(self):
        """Test risk level classification."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        # Test different fragility levels
        assert sim._get_risk_level(0.2) == "LOW"
        assert sim._get_risk_level(0.4) == "MODERATE"
        assert sim._get_risk_level(0.6) == "HIGH"
        assert sim._get_risk_level(0.8) == "CRITICAL"
    
    def test_recommendations_generation(self):
        """Test recommendation generation."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        # Low pollution - should have minimal recommendations
        sim.pollution_ratio = 0.1
        sim.sync_disruption_ratio = 0.1
        sim.ecosystem_fragility = 0.2
        recs = sim._generate_recommendations()
        assert len(recs) > 0
        
        # High pollution - should have recommendations
        sim.pollution_ratio = 0.5
        sim.sync_disruption_ratio = 0.5
        sim.ecosystem_fragility = 0.7
        recs = sim._generate_recommendations()
        assert len(recs) > 1
        assert any("signal" in r.lower() for r in recs)


class TestEducationalScenarios:
    """Tests for educational scenario execution."""
    
    def test_run_educational_scenarios(self):
        """Test running all educational scenarios."""
        results = run_educational_scenarios()
        
        assert "low_pollution" in results
        assert "medium_pollution" in results
        assert "high_pollution" in results
        assert "coordinated_attack" in results
        
        # Check structure
        for scenario_name, scenario_results in results.items():
            assert "parameters" in scenario_results
            assert "pollution_metrics" in scenario_results
            assert "sync_metrics" in scenario_results
            assert "fragility_metrics" in scenario_results
            assert "ecosystem_fragility" in scenario_results
            assert "risk_level" in scenario_results
    
    def test_scenario_pollution_escalation(self):
        """Test that fragility increases with pollution."""
        results = run_educational_scenarios()
        
        low_fragility = results["low_pollution"]["ecosystem_fragility"]
        medium_fragility = results["medium_pollution"]["ecosystem_fragility"]
        high_fragility = results["high_pollution"]["ecosystem_fragility"]
        attack_fragility = results["coordinated_attack"]["ecosystem_fragility"]
        
        # Fragility should generally increase with pollution
        assert medium_fragility >= low_fragility
        assert high_fragility >= medium_fragility
        assert attack_fragility >= high_fragility
    
    def test_scenario_risk_levels(self):
        """Test risk level progression across scenarios."""
        results = run_educational_scenarios()
        
        low_risk = results["low_pollution"]["risk_level"]
        attack_risk = results["coordinated_attack"]["risk_level"]
        
        # Coordinated attack should have higher risk
        risk_order = {"LOW": 0, "MODERATE": 1, "HIGH": 2, "CRITICAL": 3}
        assert risk_order[attack_risk] >= risk_order[low_risk]


class TestIntegration:
    """Integration tests with other modules."""
    
    def test_full_simulation_workflow(self):
        """Test complete simulation workflow."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        # Step 1: Run auctions
        auction_results = sim.simulate_rtb_auction()
        assert len(auction_results) > 0
        
        # Step 2: Inject pollution
        pollution_metrics = sim.inject_signal_pollution(0.3)
        assert pollution_metrics["total_signals_affected"] > 0
        
        # Step 3: Disrupt cookie syncing
        sync_results = sim.poison_cookie_syncing(0.3)
        assert sync_results["failed_syncs"] > 0
        
        # Step 4: Measure fragility
        fragility_metrics = sim.measure_ecosystem_fragility()
        assert isinstance(fragility_metrics, SignalMetrics)
        
        # Step 5: Generate visualization
        viz_path = "test_workflow_viz.png"
        try:
            fig = sim.visualize_impact(save_path=viz_path)
            assert fig is not None
            assert Path(viz_path).exists()
        finally:
            if Path(viz_path).exists():
                try:
                    os.unlink(viz_path)
                except PermissionError:
                    pass
        
        # Step 6: Export report
        report_path = "test_workflow_report.json"
        try:
            report = sim.export_report(report_path)
            assert report is not None
            assert Path(report_path).exists()
        finally:
            if Path(report_path).exists():
                try:
                    os.unlink(report_path)
                except PermissionError:
                    pass
    
    def test_multiple_ecosystem_configs(self):
        """Test simulation across different ecosystem configurations."""
        configs = ["default", "fragmented", "consolidated"]
        
        for config in configs:
            sim = AdtechFragilitySimulator(ecosystem_config=config, seed=42)
            sim.simulate_rtb_auction()
            sim.inject_signal_pollution(0.3)
            sim.poison_cookie_syncing(0.3)
            metrics = sim.measure_ecosystem_fragility()
            
            assert metrics is not None
            assert sim.ecosystem_fragility >= 0
    
    def test_reproducibility_with_seed(self):
        """Test that results are reproducible with same seed."""
        sim1 = AdtechFragilitySimulator(ecosystem_config='default', seed=123)
        sim2 = AdtechFragilitySimulator(ecosystem_config='default', seed=123)
        
        # Run identical simulations
        sim1.simulate_rtb_auction()
        sim2.simulate_rtb_auction()
        
        sim1.inject_signal_pollution(0.3)
        sim2.inject_signal_pollution(0.3)
        
        sim1.poison_cookie_syncing(0.3)
        sim2.poison_cookie_syncing(0.3)
        
        metrics1 = sim1.measure_ecosystem_fragility()
        metrics2 = sim2.measure_ecosystem_fragility()
        
        # Metrics should be identical
        assert metrics1.user_identification_accuracy == metrics2.user_identification_accuracy
        assert metrics1.conversion_attribution_reliability == metrics2.conversion_attribution_reliability
        assert sim1.ecosystem_fragility == sim2.ecosystem_fragility
    
    def test_auction_statistics(self):
        """Test auction statistics calculation."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        sim.simulate_rtb_auction()
        
        # Check auction history
        assert len(sim.auction_history) > 0
        
        # Calculate statistics
        clearing_prices = [a.clearing_price for a in sim.auction_history]
        bid_counts = [a.bid_count for a in sim.auction_history]
        
        assert np.mean(clearing_prices) > 0
        assert np.mean(bid_counts) > 0
        assert len(bid_counts) == len(sim.auction_history)


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_zero_pollution(self):
        """Test simulation with zero pollution."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        sim.simulate_rtb_auction()
        
        pollution_metrics = sim.inject_signal_pollution(0.0)
        assert pollution_metrics["total_signals_affected"] == 0
        
        metrics = sim.measure_ecosystem_fragility()
        assert metrics.user_identification_accuracy > 0.8
    
    def test_maximum_pollution(self):
        """Test simulation with maximum pollution."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        sim.simulate_rtb_auction()
        
        pollution_metrics = sim.inject_signal_pollution(1.0)
        assert sim.pollution_ratio == 1.0
        assert pollution_metrics["total_signals_affected"] > 0
        
        metrics = sim.measure_ecosystem_fragility()
        assert metrics.user_identification_accuracy < 0.5
    
    def test_empty_auction_batch(self):
        """Test handling of empty auction batch."""
        sim = AdtechFragilitySimulator(ecosystem_config='default', seed=42)
        
        results = sim.simulate_rtb_auction([])
        assert len(results) == 0
    
    def test_single_bidder_auction(self):
        """Test auction with single bidder."""
        sim = AdtechFragilitySimulator(ecosystem_config='consolidated', seed=42)
        
        # Manually reduce to single bidder
        sim.bidders = [sim.bidders[0]]
        
        results = sim.simulate_rtb_auction()
        assert len(results) > 0
        
        # Single bidder should still have valid clearing price
        for result in results:
            if result.bid_count > 0:
                assert result.clearing_price > 0
    
    def test_invalid_ecosystem_config(self):
        """Test handling of invalid ecosystem config."""
        # Should default to 'default' config
        sim = AdtechFragilitySimulator(ecosystem_config='invalid_config', seed=42)
        
        assert sim.ecosystem_config == 'invalid_config'
        assert len(sim.bidders) > 0  # Should still initialize


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
