"""
Unit tests for prediction strategies.

Tests the PredictionStrategies class and individual strategy methods.
"""

import pytest
from tests.conftest import validate_combination_format


@pytest.mark.unit
@pytest.mark.strategies
class TestPredictionStrategies:
    """Test suite for PredictionStrategies class."""

    def test_initialization(self, euromillions_stats):
        """Test that strategies object initializes correctly."""
        from src.core.strategies import PredictionStrategies

        strategies = PredictionStrategies(euromillions_stats)

        assert strategies.stats is not None
        assert strategies.stats == euromillions_stats

    def test_frequency_strategy_output_format(self, prediction_strategies):
        """Test that frequency strategy returns correctly formatted combinations."""
        combos = prediction_strategies.frequency_strategy(num_combinations=5)

        assert isinstance(combos, list)
        assert len(combos) == 5

        for combo in combos:
            validate_combination_format(combo)

    def test_frequency_strategy_parameter_variations(self, prediction_strategies):
        """Test frequency strategy with different parameters."""
        # Test different recent_weight values
        for weight in [0.0, 0.3, 0.5, 0.7, 1.0]:
            combos = prediction_strategies.frequency_strategy(
                num_combinations=3,
                recent_weight=weight
            )
            assert len(combos) == 3
            for combo in combos:
                validate_combination_format(combo)

    def test_mixed_strategy_output_format(self, prediction_strategies):
        """Test that mixed strategy returns correctly formatted combinations."""
        combos = prediction_strategies.mixed_strategy(num_combinations=5)

        assert isinstance(combos, list)
        assert len(combos) == 5

        for combo in combos:
            validate_combination_format(combo)

    def test_mixed_strategy_hot_ratio_variations(self, prediction_strategies):
        """Test mixed strategy with different hot_ratio values."""
        for hot_ratio in [0.3, 0.5, 0.7, 0.9]:
            combos = prediction_strategies.mixed_strategy(
                num_combinations=3,
                hot_ratio=hot_ratio
            )
            assert len(combos) == 3
            for combo in combos:
                validate_combination_format(combo)

    def test_stratified_sampling_strategy(self, prediction_strategies):
        """Test stratified sampling strategy."""
        combos = prediction_strategies.stratified_sampling_strategy(
            num_combinations=5
        )

        assert isinstance(combos, list)
        assert len(combos) == 5

        for combo in combos:
            validate_combination_format(combo)

    def test_stratified_sampling_strata_types(self, prediction_strategies):
        """Test stratified sampling with different strata types."""
        for strata_type in ["range", "pattern", "sum"]:
            combos = prediction_strategies.stratified_sampling_strategy(
                num_combinations=3,
                strata_type=strata_type,
                balance_factor=0.7
            )
            assert len(combos) == 3
            for combo in combos:
                validate_combination_format(combo)

    def test_risk_reward_strategy(self, prediction_strategies):
        """Test risk/reward optimization strategy."""
        combos = prediction_strategies.risk_reward_strategy(
            num_combinations=5,
            risk_level=5
        )

        assert isinstance(combos, list)
        assert len(combos) == 5

        for combo in combos:
            validate_combination_format(combo)

    def test_risk_reward_risk_levels(self, prediction_strategies):
        """Test risk/reward with different risk levels."""
        # Test integer scale (1-10)
        for risk_level in [1, 5, 10]:
            combos = prediction_strategies.risk_reward_strategy(
                num_combinations=2,
                risk_level=risk_level
            )
            assert len(combos) == 2

        # Test float scale (0.0-1.0)
        for risk_level in [0.1, 0.5, 1.0]:
            combos = prediction_strategies.risk_reward_strategy(
                num_combinations=2,
                risk_level=risk_level
            )
            assert len(combos) == 2

    def test_cognitive_bias_strategy(self, prediction_strategies):
        """Test anti-cognitive bias strategy."""
        combos = prediction_strategies.cognitive_bias_strategy(num_combinations=5)

        assert isinstance(combos, list)
        assert len(combos) == 5

        for combo in combos:
            validate_combination_format(combo)

    def test_temporal_strategy(self, prediction_strategies):
        """Test temporal pattern strategy."""
        combos = prediction_strategies.temporal_strategy(
            num_combinations=5,
            lookback_period=20
        )

        assert isinstance(combos, list)
        assert len(combos) == 5

        for combo in combos:
            validate_combination_format(combo)

    def test_coverage_strategy(self, prediction_strategies):
        """Test coverage optimization strategy."""
        combos = prediction_strategies.coverage_strategy(
            num_combinations=5,
            balanced=True
        )

        assert isinstance(combos, list)
        assert len(combos) == 5

        for combo in combos:
            validate_combination_format(combo)

    def test_all_strategies_return_requested_count(self, prediction_strategies):
        """Test that all strategies return the requested number of combinations."""
        strategies_to_test = [
            'frequency_strategy',
            'mixed_strategy',
            'stratified_sampling_strategy',
            'risk_reward_strategy',
            'cognitive_bias_strategy',
            'coverage_strategy'
        ]

        for strategy_name in strategies_to_test:
            strategy_method = getattr(prediction_strategies, strategy_name)
            combos = strategy_method(num_combinations=7)

            assert len(combos) == 7, f"{strategy_name} should return 7 combinations"

    def test_combinations_have_unique_numbers(self, prediction_strategies):
        """Test that combinations don't have duplicate numbers within them."""
        combos = prediction_strategies.frequency_strategy(num_combinations=10)

        for combo in combos:
            # Check main numbers are unique
            assert len(combo['numbers']) == len(set(combo['numbers'])), \
                "Main numbers must be unique within combination"

            # Check stars are unique
            assert len(combo['stars']) == len(set(combo['stars'])), \
                "Stars must be unique within combination"

    def test_combinations_within_valid_ranges(self, prediction_strategies):
        """Test that all generated numbers are within valid ranges."""
        combos = prediction_strategies.mixed_strategy(num_combinations=10)

        for combo in combos:
            # Check main numbers
            assert all(1 <= n <= 50 for n in combo['numbers']), \
                "Main numbers must be between 1 and 50"

            # Check stars
            assert all(1 <= s <= 12 for s in combo['stars']), \
                "Stars must be between 1 and 12"

    def test_combinations_are_sorted(self, prediction_strategies):
        """Test that combinations are returned sorted."""
        combos = prediction_strategies.frequency_strategy(num_combinations=5)

        for combo in combos:
            assert combo['numbers'] == sorted(combo['numbers']), \
                "Main numbers should be sorted"
            assert combo['stars'] == sorted(combo['stars']), \
                "Stars should be sorted"


@pytest.mark.unit
@pytest.mark.strategies
class TestModelBasedStrategies:
    """Test suite for model-based strategies (Bayesian, Markov, Time Series)."""

    def test_bayesian_strategy(self, prediction_strategies):
        """Test Bayesian model strategy."""
        combos = prediction_strategies.bayesian_strategy(
            num_combinations=3,
            recent_draws_count=20
        )

        assert isinstance(combos, list)
        assert len(combos) == 3

        for combo in combos:
            validate_combination_format(combo)

    def test_markov_strategy(self, prediction_strategies):
        """Test Markov chain model strategy."""
        combos = prediction_strategies.markov_strategy(
            num_combinations=3,
            lag=1
        )

        assert isinstance(combos, list)
        assert len(combos) == 3

        for combo in combos:
            validate_combination_format(combo)

    def test_time_series_strategy(self, prediction_strategies):
        """Test time series model strategy."""
        combos = prediction_strategies.time_series_strategy(
            num_combinations=3,
            window_size=10
        )

        assert isinstance(combos, list)
        assert len(combos) == 3

        for combo in combos:
            validate_combination_format(combo)
