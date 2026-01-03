"""
Pytest fixtures and configuration for lottery prediction platform tests.

This file contains shared fixtures that can be used across all test modules.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta


@pytest.fixture
def sample_euromillions_data():
    """
    Create sample Euromillions draw data for testing.

    Returns 50 draws with known patterns for predictable testing.
    """
    data = []
    base_date = datetime(2024, 1, 1)

    for i in range(50):
        # Create predictable but varied patterns
        data.append({
            'date': base_date + timedelta(days=i*3),  # Every 3 days
            'n1': (i % 50) + 1,          # Cycles through 1-50
            'n2': ((i + 10) % 50) + 1,
            'n3': ((i + 20) % 50) + 1,
            'n4': ((i + 30) % 50) + 1,
            'n5': ((i + 40) % 50) + 1,
            's1': (i % 12) + 1,          # Cycles through 1-12
            's2': ((i + 6) % 12) + 1
        })

    return pd.DataFrame(data)


@pytest.fixture
def sample_french_loto_data():
    """
    Create sample French Loto draw data for testing.

    Returns 50 draws with known patterns.
    """
    data = []
    base_date = datetime(2024, 1, 1)

    for i in range(50):
        data.append({
            'date': base_date + timedelta(days=i*3),
            'n1': (i % 49) + 1,          # Cycles through 1-49
            'n2': ((i + 10) % 49) + 1,
            'n3': ((i + 20) % 49) + 1,
            'n4': ((i + 30) % 49) + 1,
            'n5': ((i + 40) % 49) + 1,
            'lucky_number': (i % 10) + 1  # Cycles through 1-10
        })

    return pd.DataFrame(data)


@pytest.fixture
def euromillions_stats(sample_euromillions_data):
    """
    Create EuromillionsStatistics instance with sample data.

    Uses sample_euromillions_data fixture.
    """
    from src.core.statistics import EuromillionsStatistics
    return EuromillionsStatistics(sample_euromillions_data)


@pytest.fixture
def prediction_strategies(euromillions_stats):
    """
    Create PredictionStrategies instance with sample statistics.

    Uses euromillions_stats fixture.
    """
    from src.core.strategies import PredictionStrategies
    return PredictionStrategies(euromillions_stats)


@pytest.fixture
def french_loto_stats(sample_french_loto_data):
    """
    Create FrenchLotoStatistics instance with sample data.

    Uses sample_french_loto_data fixture.
    """
    from src.core.french_loto_statistics import FrenchLotoStatistics
    return FrenchLotoStatistics(sample_french_loto_data)


# Helper functions for test validation

def validate_combination_format(combo):
    """
    Validate that a combination has the correct format.

    Args:
        combo: Combination dictionary to validate

    Returns:
        bool: True if valid, raises AssertionError if invalid
    """
    assert 'numbers' in combo, "Combination must have 'numbers' key"
    assert 'stars' in combo, "Combination must have 'stars' key"
    assert 'score' in combo, "Combination must have 'score' key"

    assert len(combo['numbers']) == 5, "Must have exactly 5 numbers"
    assert len(combo['stars']) == 2, "Must have exactly 2 stars"

    assert all(1 <= n <= 50 for n in combo['numbers']), "Numbers must be 1-50"
    assert all(1 <= s <= 12 for s in combo['stars']), "Stars must be 1-12"

    assert len(set(combo['numbers'])) == 5, "Numbers must be unique"
    assert len(set(combo['stars'])) == 2, "Stars must be unique"

    assert combo['numbers'] == sorted(combo['numbers']), "Numbers must be sorted"
    assert combo['stars'] == sorted(combo['stars']), "Stars must be sorted"

    return True


def validate_french_loto_combination(combo):
    """
    Validate that a French Loto combination has the correct format.

    Args:
        combo: Combination dictionary to validate

    Returns:
        bool: True if valid, raises AssertionError if invalid
    """
    assert 'numbers' in combo, "Combination must have 'numbers' key"
    assert 'lucky_number' in combo, "Combination must have 'lucky_number' key"

    assert len(combo['numbers']) == 5, "Must have exactly 5 numbers"
    assert all(1 <= n <= 49 for n in combo['numbers']), "Numbers must be 1-49"
    assert 1 <= combo['lucky_number'] <= 10, "Lucky number must be 1-10"

    assert len(set(combo['numbers'])) == 5, "Numbers must be unique"
    assert combo['numbers'] == sorted(combo['numbers']), "Numbers must be sorted"

    return True
