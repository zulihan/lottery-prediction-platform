"""
Unit tests for statistics classes.

Tests the EuromillionsStatistics and related statistical analysis methods.
"""

import pytest


@pytest.mark.unit
@pytest.mark.statistics
class TestEuromillionsStatistics:
    """Test suite for EuromillionsStatistics class."""

    def test_initialization(self, sample_euromillions_data):
        """Test that statistics object initializes correctly."""
        from src.core.statistics import EuromillionsStatistics

        stats = EuromillionsStatistics(sample_euromillions_data)

        assert stats.data is not None
        assert len(stats.data) == 50
        assert stats.number_frequency is not None
        assert stats.star_frequency is not None

    def test_get_frequency_all_numbers(self, euromillions_stats):
        """Test getting frequency for all numbers."""
        freq = euromillions_stats.get_frequency()

        assert isinstance(freq, dict)
        assert len(freq) == 50  # Should have all numbers 1-50
        assert all(1 <= n <= 50 for n in freq.keys())
        assert all(count >= 0 for count in freq.values())

    def test_get_frequency_specific_number(self, euromillions_stats):
        """Test getting frequency for a specific number."""
        freq_1 = euromillions_stats.get_frequency(1)

        assert isinstance(freq_1, int)
        assert freq_1 >= 0

    def test_get_star_frequency(self, euromillions_stats):
        """Test getting star frequency."""
        star_freq = euromillions_stats.get_star_frequency()

        assert isinstance(star_freq, dict)
        assert len(star_freq) == 12  # Should have all stars 1-12
        assert all(1 <= s <= 12 for s in star_freq.keys())

    def test_get_hot_numbers(self, euromillions_stats):
        """Test getting hot (most frequent) numbers."""
        hot = euromillions_stats.get_hot_numbers(10)

        assert isinstance(hot, list)
        assert len(hot) == 10
        assert all(1 <= n <= 50 for n in hot)
        assert len(set(hot)) == 10  # All unique

    def test_get_cold_numbers(self, euromillions_stats):
        """Test getting cold (least frequent) numbers."""
        cold = euromillions_stats.get_cold_numbers(10)

        assert isinstance(cold, list)
        assert len(cold) == 10
        assert all(1 <= n <= 50 for n in cold)
        assert len(set(cold)) == 10  # All unique

    def test_get_weighted_frequency(self, euromillions_stats):
        """Test weighted frequency calculation."""
        freq = euromillions_stats.get_weighted_frequency(recent_weight=0.7)

        assert isinstance(freq, dict)
        assert len(freq) > 0
        assert all(weight >= 0 for weight in freq.values())

    def test_get_number_range_distribution(self, euromillions_stats):
        """Test number range distribution analysis."""
        range_dist = euromillions_stats.get_number_range_distribution()

        assert isinstance(range_dist, dict)
        assert '1-10' in range_dist
        assert '11-20' in range_dist
        assert '21-30' in range_dist
        assert '31-40' in range_dist
        assert '41-50' in range_dist

        # Total occurrences should equal 5 numbers * 50 draws = 250
        total = sum(range_dist.values())
        assert total == 250

    def test_get_number_range_distribution_custom_ranges(self, euromillions_stats):
        """Test range distribution with custom ranges."""
        custom_ranges = [(1, 25), (26, 50)]
        range_dist = euromillions_stats.get_number_range_distribution(custom_ranges)

        assert '1-25' in range_dist
        assert '26-50' in range_dist
        assert len(range_dist) == 2

    def test_get_even_odd_distribution(self, euromillions_stats):
        """Test even/odd distribution analysis."""
        even_odd = euromillions_stats.get_even_odd_distribution()

        assert 'even_count' in even_odd
        assert 'odd_count' in even_odd
        assert 'even_ratio' in even_odd
        assert 'odd_ratio' in even_odd

        # Check per-draw distribution
        for i in range(6):
            assert i in even_odd  # Should have keys 0, 1, 2, 3, 4, 5

        # Ratios should sum to 1.0 (approximately)
        assert abs(even_odd['even_ratio'] + even_odd['odd_ratio'] - 1.0) < 0.01

    def test_get_distribution_stats(self, euromillions_stats):
        """Test general distribution statistics."""
        dist_stats = euromillions_stats.get_distribution_stats()

        assert 'mean' in dist_stats
        assert 'median' in dist_stats
        assert 'std' in dist_stats
        assert 'min' in dist_stats
        assert 'max' in dist_stats

        assert dist_stats['mean'] > 0
        assert dist_stats['std'] >= 0

    def test_get_sum_distribution(self, euromillions_stats):
        """Test sum distribution analysis."""
        sum_dist = euromillions_stats.get_sum_distribution()

        assert 'sum_frequency' in sum_dist
        assert 'mean_sum' in sum_dist
        assert isinstance(sum_dist['sum_frequency'], dict)
        assert sum_dist['mean_sum'] > 0

    def test_get_gap_analysis_all_numbers(self, euromillions_stats):
        """Test gap analysis for all numbers."""
        gaps = euromillions_stats.get_gap_analysis()

        assert 'average_gaps' in gaps
        assert 'most_regular' in gaps
        assert isinstance(gaps['average_gaps'], dict)
        assert isinstance(gaps['most_regular'], list)

    def test_get_gap_analysis_specific_number(self, euromillions_stats):
        """Test gap analysis for a specific number."""
        gap = euromillions_stats.get_gap_analysis(1)

        assert 'gaps' in gap
        assert 'avg_gap' in gap
        assert 'last_appearance' in gap
        assert isinstance(gap['gaps'], list)
        assert gap['avg_gap'] >= 0
