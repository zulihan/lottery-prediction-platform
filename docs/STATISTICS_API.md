# Statistics API Reference

**Last Updated:** 2026-01-03
**Version:** 1.0 (Post-Refactoring)

---

## Overview

This document provides complete API documentation for the statistics analysis classes used in the Lottery Prediction Platform.

**Files:**
- `src/core/statistics.py` - EuromillionsStatistics
- `src/core/french_loto_statistics.py` - FrenchLotoStatistics

---

## Table of Contents

1. [EuromillionsStatistics](#euromillionsstatistics)
2. [FrenchLotoStatistics](#frenchlotostatistics)
3. [Common Patterns](#common-patterns)
4. [Usage Examples](#usage-examples)

---

## EuromillionsStatistics

**Location:** `src/core/statistics.py`

### Class Overview

```python
class EuromillionsStatistics:
    """
    Statistical analysis for Euromillions historical draw data.

    Provides frequency analysis, distribution statistics, pattern detection,
    and temporal analysis for main numbers (1-50) and star numbers (1-12).
    """
```

### Constructor

#### `__init__(data)`

Initialize statistics with historical draw data.

**Parameters:**
- `data` (pandas.DataFrame): Historical Euromillions draws with columns:
  - `date` (datetime): Draw date
  - `n1`, `n2`, `n3`, `n4`, `n5` (int): Main numbers (1-50)
  - `s1`, `s2` (int): Star numbers (1-12)

**Example:**
```python
import pandas as pd
from src.core.statistics import EuromillionsStatistics

# Load data
df = pd.read_sql("SELECT * FROM euromillions_drawing", engine)

# Create statistics instance
stats = EuromillionsStatistics(df)
```

**Internal State:**
- `self.data`: DataFrame of historical draws
- `self.number_cols`: `['n1', 'n2', 'n3', 'n4', 'n5']`
- `self.star_cols`: `['s1', 's2']`
- `self.number_frequency`: Dict `{number: occurrence_count}`
- `self.star_frequency`: Dict `{star: occurrence_count}`

---

### Frequency Methods

#### `get_frequency(number=None)`

Get occurrence frequency of main numbers.

**Parameters:**
- `number` (int, optional): Specific number to query (1-50)
  - If `None`, returns all frequencies

**Returns:**
- If `number` provided: `int` - Occurrence count
- If `number=None`: `dict` - `{number: count}` for all numbers 1-50

**Example:**
```python
# Get all frequencies
all_freq = stats.get_frequency()  # {1: 45, 2: 52, ..., 50: 38}

# Get specific number
freq_7 = stats.get_frequency(7)  # 48
```

**File Location:** `src/core/statistics.py:45`

---

#### `get_star_frequency(star=None)`

Get occurrence frequency of star numbers.

**Parameters:**
- `star` (int, optional): Specific star to query (1-12)
  - If `None`, returns all frequencies

**Returns:**
- If `star` provided: `int` - Occurrence count
- If `star=None`: `dict` - `{star: count}` for all stars 1-12

**Example:**
```python
# Get all star frequencies
all_star_freq = stats.get_star_frequency()  # {1: 28, 2: 35, ..., 12: 22}

# Get specific star
freq_star_3 = stats.get_star_frequency(3)  # 31
```

**File Location:** `src/core/statistics.py:54`

---

#### `get_weighted_frequency(recent_weight=0.5)`

Get frequency with temporal weighting (recent draws weighted higher).

**Parameters:**
- `recent_weight` (float, 0.0-1.0, default=0.5): Weight for recent draws
  - `0.0` = All draws equally weighted
  - `0.5` = Balanced (50% recent, 50% historical)
  - `1.0` = Only recent draws (last 20%)

**Returns:**
- `dict` - `{number: weighted_frequency}` for all main numbers

**Algorithm:**
```
recent_draws = last 20% of data
historical_draws = first 80% of data

weighted_freq[n] = (recent_weight * freq_recent[n] +
                    (1 - recent_weight) * freq_historical[n])
```

**Example:**
```python
# Equal weighting
freq = stats.get_weighted_frequency(recent_weight=0.0)

# Balanced
freq = stats.get_weighted_frequency(recent_weight=0.5)

# Recent-heavy
freq = stats.get_weighted_frequency(recent_weight=0.8)
```

**Use Cases:**
- Adaptive strategies that respond to recent trends
- Balancing long-term frequency with short-term patterns
- Testing sensitivity to temporal weighting

**File Location:** `src/core/statistics.py:128`

---

#### `get_weighted_star_frequency(recent_weight=0.5)`

Get star frequency with temporal weighting.

**Parameters:**
- `recent_weight` (float, 0.0-1.0, default=0.5): Weight for recent draws

**Returns:**
- `dict` - `{star: weighted_frequency}` for all stars

**Example:**
```python
star_freq = stats.get_weighted_star_frequency(recent_weight=0.7)
```

**File Location:** `src/core/statistics.py:170`

---

### Hot/Cold Number Methods

#### `get_hot_numbers(count=10)`

Get most frequently drawn numbers.

**Parameters:**
- `count` (int, default=10): Number of hot numbers to return

**Returns:**
- `List[int]` - Top `count` numbers sorted by frequency (descending)

**Example:**
```python
# Top 10 hot numbers
hot = stats.get_hot_numbers(10)  # [7, 23, 44, 19, 5, ...]

# Top 5
hot_5 = stats.get_hot_numbers(5)  # [7, 23, 44, 19, 5]
```

**File Location:** `src/core/statistics.py:108`

---

#### `get_cold_numbers(count=10)`

Get least frequently drawn numbers.

**Parameters:**
- `count` (int, default=10): Number of cold numbers to return

**Returns:**
- `List[int]` - Bottom `count` numbers sorted by frequency (ascending)

**Example:**
```python
# Bottom 10 cold numbers
cold = stats.get_cold_numbers(10)  # [46, 13, 2, 41, ...]
```

**File Location:** `src/core/statistics.py:113`

---

#### `get_hot_stars(count=5)`

Get most frequently drawn stars.

**Parameters:**
- `count` (int, default=5): Number of hot stars to return

**Returns:**
- `List[int]` - Top `count` stars sorted by frequency (descending)

**Example:**
```python
hot_stars = stats.get_hot_stars(5)  # [2, 3, 5, 9, 1]
```

**File Location:** `src/core/statistics.py:118`

---

#### `get_cold_stars(count=5)`

Get least frequently drawn stars.

**Parameters:**
- `count` (int, default=5): Number of cold stars to return

**Returns:**
- `List[int]` - Bottom `count` stars sorted by frequency (ascending)

**Example:**
```python
cold_stars = stats.get_cold_stars(5)  # [12, 4, 10, 6, 11]
```

**File Location:** `src/core/statistics.py:123`

---

### Distribution Analysis Methods

#### `get_distribution_stats()`

Get comprehensive distribution statistics for all numbers.

**Parameters:** None

**Returns:**
```python
{
    'mean': float,           # Average frequency per number
    'median': float,         # Median frequency
    'std': float,            # Standard deviation
    'min': int,              # Minimum frequency
    'max': int,              # Maximum frequency
    'variance': float,       # Variance in frequencies
    'range': int,            # max - min
    'coefficient_of_variation': float  # std / mean
}
```

**Example:**
```python
dist_stats = stats.get_distribution_stats()
print(f"Mean frequency: {dist_stats['mean']:.2f}")
print(f"Std deviation: {dist_stats['std']:.2f}")
print(f"Range: {dist_stats['range']}")
```

**Use Cases:**
- Understanding frequency distribution uniformity
- Detecting anomalies in draw patterns
- Statistical analysis and reporting

**File Location:** `src/core/statistics.py:212`

---

#### `get_number_range_distribution(ranges=None)`

Get distribution of numbers across specified ranges.

**Parameters:**
- `ranges` (List[Tuple[int, int]], optional): Range definitions
  - Default: `[(1,10), (11,20), (21,30), (31,40), (41,50)]`

**Returns:**
```python
{
    '1-10': int,   # Total occurrences in range 1-10
    '11-20': int,  # Total occurrences in range 11-20
    '21-30': int,
    '31-40': int,
    '41-50': int
}
```

**Example:**
```python
# Default ranges (by decade)
range_dist = stats.get_number_range_distribution()
# {'1-10': 245, '11-20': 252, '21-30': 248, '31-40': 251, '41-50': 254}

# Custom ranges
custom_ranges = [(1, 25), (26, 50)]
range_dist = stats.get_number_range_distribution(custom_ranges)
# {'1-25': 625, '26-50': 625}
```

**Use Cases:**
- Stratified sampling strategies
- Ensuring balanced number selection
- Detecting range biases

**File Location:** `src/core/statistics.py:405`

---

#### `get_even_odd_distribution()`

Get distribution of even vs odd numbers.

**Parameters:** None

**Returns:**
```python
{
    'even_count': int,      # Total even number occurrences
    'odd_count': int,       # Total odd number occurrences
    'even_ratio': float,    # Proportion even (0.0-1.0)
    'odd_ratio': float,     # Proportion odd (0.0-1.0)
    0: int,                 # Draws with 0 even numbers
    1: int,                 # Draws with 1 even number
    2: int,                 # Draws with 2 even numbers
    3: int,                 # Draws with 3 even numbers
    4: int,                 # Draws with 4 even numbers
    5: int                  # Draws with 5 even numbers
}
```

**Example:**
```python
even_odd = stats.get_even_odd_distribution()

print(f"Even ratio: {even_odd['even_ratio']:.2%}")
print(f"Odd ratio: {even_odd['odd_ratio']:.2%}")
print(f"Most common: {max(even_odd[0:6].items(), key=lambda x: x[1])}")

# Output:
# Even ratio: 48.50%
# Odd ratio: 51.50%
# Most common: (3, 45)  # 3 even numbers per draw is most common
```

**Use Cases:**
- Pattern-based stratified sampling
- Identifying even/odd preferences in draws
- Statistical distribution analysis

**File Location:** `src/core/statistics.py:435`

---

### Temporal Analysis Methods

#### `get_recency_stats(draws=20)`

Get statistics focusing on recent draws.

**Parameters:**
- `draws` (int, default=20): Number of recent draws to analyze

**Returns:**
```python
{
    'hot_in_recent': List[int],        # Hot numbers in recent draws
    'cold_in_recent': List[int],       # Cold numbers in recent draws
    'emerging_numbers': List[int],     # Numbers gaining momentum
    'fading_numbers': List[int],       # Numbers losing momentum
    'recent_frequency': Dict[int, int] # Frequency in recent draws
}
```

**Example:**
```python
# Last 20 draws
recent = stats.get_recency_stats(draws=20)
print(f"Emerging: {recent['emerging_numbers']}")
print(f"Fading: {recent['fading_numbers']}")

# Last 50 draws
recent_50 = stats.get_recency_stats(draws=50)
```

**Use Cases:**
- Temporal strategy development
- Identifying short-term trends
- Momentum-based prediction

**File Location:** `src/core/statistics.py:251`

---

#### `get_gap_analysis(number=None)`

Analyze gaps between number appearances.

**Parameters:**
- `number` (int, optional): Specific number to analyze (1-50)
  - If `None`, returns analysis for all numbers

**Returns:**
- If `number` provided:
```python
{
    'gaps': List[int],       # List of gaps between appearances
    'avg_gap': float,        # Average gap
    'last_appearance': int,  # Index of last appearance
    'draws_since_last': int  # Draws since last seen
}
```

- If `number=None`:
```python
{
    'average_gaps': Dict[int, float],  # {number: avg_gap}
    'most_regular': List[Tuple[int, float]]  # Top 5 most regular numbers
}
```

**Example:**
```python
# Analyze all numbers
gap_analysis = stats.get_gap_analysis()
print(f"Most regular numbers: {gap_analysis['most_regular']}")

# Analyze specific number
gap_7 = stats.get_gap_analysis(7)
print(f"Number 7 average gap: {gap_7['avg_gap']:.2f} draws")
print(f"Draws since last appearance: {gap_7['draws_since_last']}")
```

**Use Cases:**
- Identifying "due" numbers
- Understanding draw regularity
- Temporal pattern strategies

**File Location:** `src/core/statistics.py:355`

---

### Sum and Pattern Methods

#### `get_sum_distribution()`

Analyze distribution of sum totals in draws.

**Parameters:** None

**Returns:**
```python
{
    'sum_frequency': Dict[int, int],  # {sum_value: occurrence_count}
    'mean_sum': float,                # Average sum across all draws
    'median_sum': float,              # Median sum
    'most_common_sums': List[int],    # Top 5 most common sums
    'sum_ranges': Dict[str, int]      # Counts by sum range
}
```

**Example:**
```python
sum_dist = stats.get_sum_distribution()
print(f"Mean sum: {sum_dist['mean_sum']:.2f}")
print(f"Most common sums: {sum_dist['most_common_sums']}")

# Output:
# Mean sum: 127.5
# Most common sums: [125, 130, 128, 132, 120]
```

**Use Cases:**
- Sum-based filtering strategies
- Identifying typical sum ranges
- Pattern validation

**File Location:** `src/core/statistics.py:284`

---

#### `get_consecutive_analysis()`

Analyze consecutive number patterns in draws.

**Parameters:** None

**Returns:**
```python
{
    'consecutive_frequency': int,     # Draws with consecutive numbers
    'consecutive_ratio': float,       # Proportion with consecutives
    'avg_consecutive_count': float,   # Average consecutives per draw
    'max_consecutive_run': int        # Longest consecutive run seen
}
```

**Example:**
```python
consec = stats.get_consecutive_analysis()
print(f"Draws with consecutives: {consec['consecutive_ratio']:.1%}")
print(f"Max consecutive run: {consec['max_consecutive_run']}")

# Output:
# Draws with consecutives: 45.3%
# Max consecutive run: 3
```

**Use Cases:**
- Pattern-based strategies
- Avoiding/seeking consecutive numbers
- Statistical distribution understanding

**File Location:** `src/core/statistics.py:323`

---

### Number Details Method

#### `get_number_statistics(number)`

Get comprehensive statistics for a specific number.

**Parameters:**
- `number` (int): Number to analyze (1-50)

**Returns:**
```python
{
    'frequency': int,              # Total occurrences
    'last_seen': datetime,         # Date of last appearance
    'days_since_last': int,        # Days since last draw
    'average_gap': float,          # Average draws between appearances
    'longest_gap': int,            # Longest gap observed
    'shortest_gap': int,           # Shortest gap observed
    'recent_frequency': int,       # Occurrences in last 20 draws
    'trend': str                   # 'increasing', 'stable', 'decreasing'
}
```

**Example:**
```python
# Detailed stats for number 7
stats_7 = stats.get_number_statistics(7)

print(f"Number 7:")
print(f"  Frequency: {stats_7['frequency']}")
print(f"  Last seen: {stats_7['last_seen']}")
print(f"  Days since: {stats_7['days_since_last']}")
print(f"  Trend: {stats_7['trend']}")
```

**Use Cases:**
- Individual number investigation
- Decision support for number selection
- Detailed reporting

**File Location:** `src/core/statistics.py:63`

---

## FrenchLotoStatistics

**Location:** `src/core/french_loto_statistics.py`

### Class Overview

```python
class FrenchLotoStatistics:
    """
    Statistical analysis for French Loto historical draw data.

    Similar to EuromillionsStatistics but for French Loto:
    - Main numbers: 1-49 (5 numbers)
    - Lucky number: 1-10 (1 number)
    """
```

### Key Differences from EuromillionsStatistics

1. **Number Range:** 1-49 instead of 1-50
2. **Lucky Number:** 1-10 instead of stars 1-12
3. **Single Lucky Number:** Only 1 lucky number instead of 2 stars

### Methods

FrenchLotoStatistics implements all the same methods as EuromillionsStatistics with appropriate adjustments:

- `get_frequency(number=None)` - Main numbers 1-49
- `get_lucky_number_frequency(lucky=None)` - Lucky numbers 1-10 (replaces `get_star_frequency`)
- `get_weighted_frequency(recent_weight=0.5)`
- `get_weighted_lucky_number_frequency(recent_weight=0.5)` (replaces `get_weighted_star_frequency`)
- `get_hot_numbers(count=10)`
- `get_cold_numbers(count=10)`
- `get_hot_lucky_numbers(count=5)` (replaces `get_hot_stars`)
- `get_cold_lucky_numbers(count=5)` (replaces `get_cold_stars`)
- All distribution and analysis methods

**Example:**
```python
from src.core.french_loto_statistics import FrenchLotoStatistics

# Load French Loto data
df = pd.read_sql("SELECT * FROM french_loto_drawing", engine)

# Create statistics
loto_stats = FrenchLotoStatistics(df)

# Use same API
hot = loto_stats.get_hot_numbers(10)
lucky_freq = loto_stats.get_lucky_number_frequency()
range_dist = loto_stats.get_number_range_distribution([(1,10), (11,20), (21,30), (31,40), (41,49)])
```

---

## Common Patterns

### Pattern 1: Basic Frequency Analysis

```python
# Load data and create statistics
stats = EuromillionsStatistics(data)

# Get hot/cold numbers
hot = stats.get_hot_numbers(15)
cold = stats.get_cold_numbers(15)

# Get weighted frequency
freq = stats.get_weighted_frequency(recent_weight=0.6)
```

### Pattern 2: Temporal Analysis

```python
# Recent trend analysis
recent = stats.get_recency_stats(draws=30)

# Gap analysis for "due" numbers
gaps = stats.get_gap_analysis()
due_numbers = [n for n, avg_gap in gaps['average_gaps'].items()
               if stats.get_number_statistics(n)['days_since_last'] > avg_gap * 1.5]
```

### Pattern 3: Distribution Validation

```python
# Ensure balanced distribution
range_dist = stats.get_number_range_distribution()
even_odd = stats.get_even_odd_distribution()
sum_dist = stats.get_sum_distribution()

# Check if combination matches typical patterns
def validate_combination(numbers):
    combo_sum = sum(numbers)
    even_count = sum(1 for n in numbers if n % 2 == 0)

    # Check against typical ranges
    is_valid_sum = (sum_dist['mean_sum'] - 30) <= combo_sum <= (sum_dist['mean_sum'] + 30)
    is_typical_even_odd = even_count in [2, 3]  # Most common

    return is_valid_sum and is_typical_even_odd
```

### Pattern 4: Comprehensive Number Profiling

```python
# Deep dive on specific number
def profile_number(stats, number):
    details = stats.get_number_statistics(number)
    gap_info = stats.get_gap_analysis(number)

    profile = {
        'number': number,
        'is_hot': number in stats.get_hot_numbers(10),
        'is_cold': number in stats.get_cold_numbers(10),
        'frequency': details['frequency'],
        'last_seen': details['last_seen'],
        'avg_gap': gap_info['avg_gap'],
        'is_due': gap_info['draws_since_last'] > gap_info['avg_gap'],
        'trend': details['trend']
    }

    return profile

# Profile all numbers
profiles = {n: profile_number(stats, n) for n in range(1, 51)}
```

---

## Performance Considerations

### Caching

Statistics objects perform frequency calculations on initialization. Reuse instances:

```python
# Good: Create once, use many times
stats = EuromillionsStatistics(data)
strategies = PredictionStrategies(stats)
combos1 = strategies.frequency_strategy(5)
combos2 = strategies.mixed_strategy(10)

# Bad: Recreate for each use
for i in range(10):
    stats = EuromillionsStatistics(data)  # Wasteful!
    combos = strategies.frequency_strategy(5)
```

### Large Datasets

For very large datasets (>10,000 draws), consider:

```python
# Limit historical data
recent_data = data.tail(5000)  # Last 5000 draws
stats = EuromillionsStatistics(recent_data)
```

### Memory Usage

Statistics objects store:
- Original DataFrame
- Frequency dictionaries (small)
- No caching of computed values

**Estimated Memory:** DataFrame size + ~10KB

---

## Error Handling

### Common Errors

```python
# Empty data
try:
    stats = EuromillionsStatistics(pd.DataFrame())
except ValueError:
    print("Cannot create statistics from empty data")

# Missing columns
try:
    stats = EuromillionsStatistics(data_missing_columns)
except KeyError as e:
    print(f"Missing required column: {e}")

# Invalid number range
try:
    freq = stats.get_frequency(100)  # Out of range
except KeyError:
    print("Number not in valid range (1-50)")
```

---

## Testing

### Unit Test Example

```python
import pytest
from src.core.statistics import EuromillionsStatistics

def test_frequency_calculation():
    # Create mock data
    data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=10),
        'n1': [1]*10, 'n2': [2]*10, 'n3': [3]*10,
        'n4': [4]*10, 'n5': [5]*10,
        's1': [1]*10, 's2': [2]*10
    })

    stats = EuromillionsStatistics(data)

    # Test frequency
    assert stats.get_frequency(1) == 10
    assert stats.get_frequency(6) == 0

    # Test hot numbers
    hot = stats.get_hot_numbers(5)
    assert 1 in hot
    assert 2 in hot

def test_range_distribution():
    stats = EuromillionsStatistics(sample_data)

    range_dist = stats.get_number_range_distribution()

    assert '1-10' in range_dist
    assert sum(range_dist.values()) > 0
```

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [API_REFERENCE.md](API_REFERENCE.md) - Strategy API reference
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing best practices
