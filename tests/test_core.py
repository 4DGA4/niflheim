"""Test MAW core functionality"""
import pytest
from maw.core import (  # type: ignore[import-untyped]
    solve_game,
    agent_strategy_game,
    bull_bear_game,
    compute_nash_2x2,
    find_pure_nash,
    compute_minimax,
    compute_regret_matrix,
)


def test_agent_strategy_game() -> None:
    """Test agent strategy game returns valid result."""
    result = agent_strategy_game()
    assert "pure_nash" in result
    assert "minimax_row" in result
    assert "regret" in result


def test_bull_bear_bullish() -> None:
    """Test bull market scenario."""
    result = bull_bear_game("BULLISH")
    assert result["dimensions"] == [2, 2]


def test_bull_bear_bearish() -> None:
    """Test bear market scenario."""
    result = bull_bear_game("BEARISH")
    assert result["dimensions"] == [2, 2]


def test_pure_nash_detection() -> None:
    """Test pure Nash equilibrium detection."""
    payoff_a = [[1, 0], [0, 0]]
    payoff_b = [[1, 0], [0, 0]]
    result = find_pure_nash(payoff_a, payoff_b)
    assert result["count"] >= 1


def test_minimax_maximizing() -> None:
    """Test minimax for maximizing player."""
    matrix = [[3, 1], [2, 4]]
    result = compute_minimax(matrix, maximizing_player=True)
    assert "value" in result
    assert result["player"] == "row_maximizer"


def test_minimax_minimizing() -> None:
    """Test minimax for minimizing player."""
    matrix = [[3, 1], [2, 4]]
    result = compute_minimax(matrix, maximizing_player=False)
    assert result["player"] == "col_minimizer"


def test_regret_matrix() -> None:
    """Test regret matrix computation."""
    payoff_a = [[3, 1], [2, 4]]
    payoff_b = [[2, 3], [1, 4]]
    result = compute_regret_matrix(payoff_a, payoff_b)
    assert "regret_matrix_player_a" in result
    assert "regret_matrix_player_b" in result
    assert "epsilon_correlated" in result


def test_solve_game_complete() -> None:
    """Test complete game solving."""
    payoff_a = [[3, 0], [5, 1]]
    payoff_b = [[3, 5], [0, 1]]
    result = solve_game(payoff_a, payoff_b)
    
    assert "dimensions" in result
    assert result["dimensions"] == [2, 2]
    assert "pure_nash" in result
    assert "mixed_nash" in result
    assert "minimax_row" in result
    assert "minimax_col" in result
    assert "regret" in result
