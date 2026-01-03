# Testing Guide

**Last Updated:** 2026-01-03
**Version:** 1.0

---

## Overview

This guide explains how to run tests and write new tests for the Lottery Prediction Platform.

**Test Framework:** pytest
**Test Location:** `tests/`
**Configuration:** `pytest.ini`

---

## Quick Start

### Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### Run All Tests

```bash
# Run all tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_statistics.py -v

# Run specific test class
pytest tests/test_strategies.py::TestPredictionStrategies -v

# Run specific test method
pytest tests/test_statistics.py::TestEuromillionsStatistics::test_get_frequency_all_numbers -v
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only statistics tests
pytest -m statistics

# Run only strategy tests
pytest -m strategies

# Run everything except slow tests
pytest -m "not slow"
```

---

## Test Structure

### Directory Layout

```
tests/
├── conftest.py              # Shared fixtures and helpers
├── test_statistics.py       # Tests for statistics classes
├── test_strategies.py       # Tests for prediction strategies
└── [future test files]
```

### Test Markers

Tests are categorized using pytest markers:

- `@pytest.mark.unit` - Unit tests for individual functions
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.statistics` - Statistics class tests
- `@pytest.mark.strategies` - Strategy tests
- `@pytest.mark.database` - Tests requiring database
- `@pytest.mark.slow` - Tests that take significant time

---

## Fixtures

### Available Fixtures (from `conftest.py`)

#### `sample_euromillions_data`
Returns a pandas DataFrame with 50 sample Euromillions draws.

```python
def test_example(sample_euromillions_data):
    assert len(sample_euromillions_data) == 50
    assert 'n1' in sample_euromillions_data.columns
```

#### `sample_french_loto_data`
Returns a pandas DataFrame with 50 sample French Loto draws.

```python
def test_example(sample_french_loto_data):
    assert len(sample_french_loto_data) == 50
```

#### `euromillions_stats`
Returns an initialized `EuromillionsStatistics` object with sample data.

```python
def test_example(euromillions_stats):
    freq = euromillions_stats.get_frequency()
    assert isinstance(freq, dict)
```

#### `prediction_strategies`
Returns an initialized `PredictionStrategies` object.

```python
def test_example(prediction_strategies):
    combos = prediction_strategies.frequency_strategy(5)
    assert len(combos) == 5
```

#### `french_loto_stats`
Returns an initialized `FrenchLotoStatistics` object with sample data.

```python
def test_example(french_loto_stats):
    freq = french_loto_stats.get_frequency()
    assert isinstance(freq, dict)
```

### Helper Functions

#### `validate_combination_format(combo)`
Validates that a Euromillions combination has the correct format.

```python
from tests.conftest import validate_combination_format

def test_combination(prediction_strategies):
    combos = prediction_strategies.frequency_strategy(1)
    validate_combination_format(combos[0])  # Raises AssertionError if invalid
```

#### `validate_french_loto_combination(combo)`
Validates that a French Loto combination has the correct format.

```python
from tests.conftest import validate_french_loto_combination

def test_loto_combination(french_loto_stats):
    combo = {...}
    validate_french_loto_combination(combo)
```

---

## Writing New Tests

### Basic Test Pattern

```python
import pytest
from tests.conftest import validate_combination_format

@pytest.mark.unit
@pytest.mark.strategies
class TestMyNewFeature:
    """Test suite for new feature."""

    def test_basic_functionality(self, prediction_strategies):
        """Test that the feature works."""
        result = prediction_strategies.my_new_method()

        assert result is not None
        assert len(result) > 0

    def test_edge_case(self):
        """Test edge case handling."""
        # Test code here
        pass
```

### Testing a Statistics Method

```python
@pytest.mark.unit
@pytest.mark.statistics
def test_new_statistics_method(euromillions_stats):
    """Test a new statistics calculation."""
    result = euromillions_stats.new_method()

    assert isinstance(result, dict)
    assert 'key1' in result
    assert result['key1'] > 0
```

### Testing a Strategy Method

```python
@pytest.mark.unit
@pytest.mark.strategies
def test_new_strategy(prediction_strategies):
    """Test a new prediction strategy."""
    combos = prediction_strategies.new_strategy(num_combinations=5)

    assert len(combos) == 5

    for combo in combos:
        validate_combination_format(combo)
        assert combo['score'] >= 0
```

### Testing with Parameters

```python
@pytest.mark.parametrize("param_value,expected", [
    (0.0, 5),
    (0.5, 10),
    (1.0, 15),
])
def test_with_parameters(prediction_strategies, param_value, expected):
    """Test method with different parameter values."""
    result = prediction_strategies.method(param=param_value)
    assert len(result) == expected
```

---

## Test Coverage

### Generate Coverage Report

```bash
# HTML report (opens in browser)
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Terminal report
pytest --cov=src --cov-report=term

# Generate coverage and run tests
pytest --cov=src --cov-report=term-missing tests/
```

### Current Coverage Targets

| Module | Target Coverage | Current |
|--------|----------------|---------|
| src/core/statistics.py | >70% | TBD |
| src/core/strategies.py | >60% | TBD |
| src/core/models.py | >50% | TBD |
| src/core/database.py | >40% | TBD |

---

## Common Testing Patterns

### Pattern 1: Test Output Format

```python
def test_output_format(prediction_strategies):
    """Verify method returns correctly formatted data."""
    result = prediction_strategies.frequency_strategy(5)

    assert isinstance(result, list)
    assert len(result) == 5

    for combo in result:
        validate_combination_format(combo)
```

### Pattern 2: Test Parameter Validation

```python
def test_parameter_validation(prediction_strategies):
    """Test that invalid parameters raise errors."""
    with pytest.raises(ValueError):
        prediction_strategies.frequency_strategy(num_combinations=-1)

    with pytest.raises(ValueError):
        prediction_strategies.frequency_strategy(recent_weight=1.5)
```

### Pattern 3: Test Statistical Properties

```python
def test_statistical_properties(euromillions_stats):
    """Test that statistical calculations are correct."""
    freq = euromillions_stats.get_frequency()

    # Total should match number of draws * numbers per draw
    total_count = sum(freq.values())
    expected = len(euromillions_stats.data) * 5

    assert total_count == expected
```

### Pattern 4: Test Consistency

```python
def test_consistency(prediction_strategies):
    """Test that methods return consistent results."""
    combos1 = prediction_strategies.frequency_strategy(5, recent_weight=0.5)
    combos2 = prediction_strategies.frequency_strategy(5, recent_weight=0.5)

    # Both should have same length
    assert len(combos1) == len(combos2)

    # Both should be valid
    for combo in combos1 + combos2:
        validate_combination_format(combo)
```

---

## Debugging Failed Tests

### Verbose Output

```bash
# Show full error traces
pytest -vv

# Show print statements
pytest -s

# Drop into debugger on failure
pytest --pdb
```

### Test Individual Methods

```bash
# Run just one test
pytest tests/test_statistics.py::TestEuromillionsStatistics::test_get_frequency_all_numbers -v

# Show local variables on failure
pytest --showlocals
```

### Common Issues

#### Import Errors
```
ModuleNotFoundError: No module named 'src'
```

**Solution:** Ensure you're running pytest from the project root:
```bash
cd /Users/zu/_Dev/lottery-prediction-platform
pytest tests/
```

#### Fixture Not Found
```
fixture 'euromillions_stats' not found
```

**Solution:** Check that `conftest.py` is in the `tests/` directory and contains the fixture.

#### Assertion Failures

Check the test output for details:
```bash
pytest tests/test_statistics.py -v --tb=long
```

---

## Best Practices

### 1. Test One Thing at a Time

```python
# Good: Focused test
def test_frequency_returns_dict():
    freq = stats.get_frequency()
    assert isinstance(freq, dict)

# Bad: Testing multiple things
def test_everything():
    freq = stats.get_frequency()
    assert isinstance(freq, dict)
    assert len(freq) == 50
    hot = stats.get_hot_numbers(10)
    assert len(hot) == 10
```

### 2. Use Descriptive Names

```python
# Good
def test_frequency_strategy_returns_five_combinations_when_requested()

# Bad
def test1()
```

### 3. Use Fixtures for Setup

```python
# Good: Use fixture
def test_method(euromillions_stats):
    result = euromillions_stats.get_frequency()

# Bad: Create in test
def test_method():
    data = pd.DataFrame(...)
    stats = EuromillionsStatistics(data)
    result = stats.get_frequency()
```

### 4. Test Edge Cases

```python
def test_edge_cases(prediction_strategies):
    # Minimum
    combos = prediction_strategies.frequency_strategy(1)
    assert len(combos) == 1

    # Maximum
    combos = prediction_strategies.frequency_strategy(100)
    assert len(combos) == 100

    # Zero (should raise error or return empty)
    with pytest.raises(ValueError):
        prediction_strategies.frequency_strategy(0)
```

---

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: Run tests
      run: pytest --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

## Future Testing

### Areas to Add Tests

1. **Database Integration Tests**
   - Connection handling
   - Model CRUD operations
   - Retry logic

2. **Model Tests**
   - BayesianModel
   - MarkovModel
   - TimeSeriesModel

3. **French Loto Tests**
   - FrenchLotoStatistics
   - FrenchLotoStrategy

4. **End-to-End Tests**
   - Full combination generation flow
   - Data loading → Statistics → Strategies → Output

5. **Performance Tests**
   - Strategy execution time
   - Large dataset handling

---

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [pytest markers](https://docs.pytest.org/en/stable/mark.html)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [API_REFERENCE.md](API_REFERENCE.md) - Strategy API reference
- [STATISTICS_API.md](STATISTICS_API.md) - Statistics API reference
