# Lucky Number & Star Strategies

**Last Updated:** 2026-01-04
**Version:** 1.0

---

## Overview

This module provides **separate optimization strategies** for lucky numbers (French Loto) and stars (Euromillions), allowing you to use different approaches for main numbers vs. bonus numbers.

**Location:** `src/core/lucky_number_strategies.py`

---

## Table of Contents

1. [Rationale](#rationale)
2. [French Loto - Lucky Number Strategies](#french-loto---lucky-number-strategies)
3. [Euromillions - Star Strategies](#euromillions---star-strategies)
4. [Backtesting](#backtesting)
5. [UI Integration](#ui-integration)
6. [API Reference](#api-reference)
7. [Best Practices](#best-practices)

---

## Rationale

### Why Separate Strategies?

Main numbers and bonus numbers (lucky/stars) have fundamentally different characteristics:

| Aspect | Main Numbers | Lucky/Stars |
|--------|--------------|-------------|
| **Range** | 1-49 (Loto) / 1-50 (Euro) | 1-10 (Loto) / 1-12 (Euro) |
| **Count per draw** | 5 numbers | 1 (Loto) / 2 (Euro) |
| **Probability space** | ~2M combinations | 10 (Loto) / 66 (Euro) |
| **Pattern types** | Range, frequency, gaps | Frequency, pairs, transitions |

**Benefit:** By optimizing each independently, you can:
- Use a conservative strategy for main numbers + aggressive for lucky
- Apply different time horizons (recent vs. historical)
- Match strategies to their specific probability characteristics

---

## French Loto - Lucky Number Strategies

### Available Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| `frequency` | Most frequently drawn lucky number | Consistent selection |
| `balanced` | Mix of frequent + medium frequency | Moderate risk |
| `contrarian` | Least frequent (overdue) numbers | Risk-takers |
| `time_series` | Based on recent 50 draws | Trend followers |
| `hot_cold` | 70% hot / 30% cold balance | Balanced approach |
| `range_balanced` | Balance between 1-5 and 6-10 | Coverage seekers |
| `weighted_random` | Random weighted by frequency | Exploration |

### Usage Example

```python
from src.core.lucky_number_strategies import LuckyNumberStrategies
import pandas as pd

# Load French Loto data
loto_data = pd.read_sql("SELECT * FROM french_loto_drawings", conn)

# Initialize strategies
lucky_strategies = LuckyNumberStrategies(loto_data)

# Generate using specific strategy
result = lucky_strategies.generate('contrarian')
print(f"Lucky Number: {result['lucky_number']}")
print(f"Strategy: {result['strategy']}")
print(f"Confidence Score: {result['score']}")

# Get statistics
stats = lucky_strategies.get_statistics()
print(f"Most frequent: {stats['most_frequent']}")
print(f"Least frequent: {stats['least_frequent']}")
```

### Strategy Details

#### 1. Frequency Strategy
```python
result = lucky_strategies.generate('frequency')
# Returns: The single most frequently drawn lucky number
```

#### 2. Balanced Strategy
```python
result = lucky_strategies.generate('balanced')
# Returns: Random selection from top 5 frequent + medium 5
```

#### 3. Contrarian Strategy
```python
result = lucky_strategies.generate('contrarian')
# Returns: Random selection from 5 least frequent (overdue)
```

#### 4. Time Series Strategy
```python
result = lucky_strategies.generate('time_series')
# Analyzes last 50 draws for trending numbers
```

#### 5. Hot/Cold Balanced Strategy
```python
result = lucky_strategies.generate('hot_cold')
# 70% chance: hot (recent frequent)
# 30% chance: cold (overall least frequent)
```

#### 6. Range Balanced Strategy
```python
result = lucky_strategies.generate('range_balanced')
# 50% chance: best from 1-5
# 50% chance: best from 6-10
```

#### 7. Weighted Random Strategy
```python
result = lucky_strategies.generate('weighted_random')
# Probability proportional to historical frequency
```

---

## Euromillions - Star Strategies

### Available Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| `frequency` | Most frequently drawn stars | Consistent selection |
| `balanced` | Mix of frequent + medium | Moderate risk |
| `contrarian` | Least frequent stars | Risk-takers |
| `range_balanced` | One from 1-6, one from 7-12 | Range coverage |
| `pair_frequency` | Most common star pairs | Pattern matching |
| `markov` | Based on star transitions | Sequential patterns |
| `time_series` | Recent 50 draws trend | Trend followers |
| `weighted_random` | Weighted random selection | Exploration |

### Usage Example

```python
from src.core.lucky_number_strategies import StarStrategies
import pandas as pd

# Load Euromillions data
euro_data = pd.read_sql("SELECT * FROM euromillions_drawings", conn)

# Initialize strategies
star_strategies = StarStrategies(euro_data)

# Generate using specific strategy
result = star_strategies.generate('pair_frequency')
print(f"Stars: {result['stars']}")  # e.g., [3, 9]
print(f"Strategy: {result['strategy']}")
print(f"Confidence Score: {result['score']}")

# Get statistics
stats = star_strategies.get_statistics()
print(f"Most frequent stars: {stats['most_frequent']}")
print(f"Most common pairs: {stats['most_common_pairs']}")
```

### Strategy Details

#### 1. Frequency Strategy
```python
result = star_strategies.generate('frequency')
# Returns: 2 randomly selected from top 6 most frequent
```

#### 2. Pair Frequency Strategy
```python
result = star_strategies.generate('pair_frequency')
# Returns: One of the 5 most common historical pairs
```

#### 3. Markov Strategy
```python
result = star_strategies.generate('markov')
# Selects first star from frequent, second based on transition probabilities
```

#### 4. Range Balanced Strategy
```python
result = star_strategies.generate('range_balanced')
# Returns: Most frequent from 1-6 + most frequent from 7-12
```

---

## Backtesting

### Lucky Number Backtest

```python
from src.core.lucky_number_strategies import backtest_lucky_strategies

# Run backtest (30% test set)
results = backtest_lucky_strategies(loto_data, test_size=0.3)

for strategy, data in results.items():
    print(f"{strategy}:")
    print(f"  Win Rate: {data['win_rate']}%")
    print(f"  Expected Random: {data['expected_random']}%")
```

**Output:**
```
frequency:
  Win Rate: 11.2%
  Expected Random: 10.0%
balanced:
  Win Rate: 10.8%
  Expected Random: 10.0%
contrarian:
  Win Rate: 9.5%
  Expected Random: 10.0%
...
```

### Star Backtest

```python
from src.core.lucky_number_strategies import backtest_star_strategies

# Run backtest (30% test set)
results = backtest_star_strategies(euro_data, test_size=0.3)

for strategy, data in results.items():
    print(f"{strategy}:")
    print(f"  Full Match (2/2): {data['full_match_rate']}%")
    print(f"  Partial Match (1/2): {data['partial_match_rate']}%")
    print(f"  Expected Random: {data['expected_random_full']}%")
```

---

## UI Integration

### Strategy Generation Tab

When generating combinations, you can now use separate strategies:

#### French Loto

1. Go to **Strategy Generation** → Select **French Loto**
2. Check **🍀 Use separate strategy for Lucky Number**
3. Select main number strategy (e.g., `Risk/Reward Balance`)
4. Select lucky number strategy (e.g., `contrarian`)
5. Click **Generate**

**Result:** Combinations use Risk/Reward for numbers + Contrarian for lucky

#### Euromillions

1. Go to **Strategy Generation** → Select **Euromillions**
2. Check **⭐ Use separate strategy for Stars**
3. Select main number strategy (e.g., `Markov Chain`)
4. Select star strategy (e.g., `pair_frequency`)
5. Click **Generate**

**Result:** Combinations use Markov for numbers + Pair Frequency for stars

### Strategy Performance Tab

Dedicated backtesting sections:

- **French Loto:** "🍀 Lucky Number Strategies" section
  - Run Lucky Number Backtest
  - Generate Lucky Numbers (shows all 7 strategies)
  
- **Euromillions:** "⭐ Star Strategies" section
  - Run Star Backtest
  - Generate Stars (shows all 8 strategies)

---

## API Reference

### LuckyNumberStrategies

```python
class LuckyNumberStrategies:
    def __init__(self, data: pd.DataFrame)
    def generate(self, strategy: str = 'balanced') -> dict
    def get_statistics(self) -> dict
    
    # Individual strategy methods
    def frequency_strategy(self) -> int
    def balanced_strategy(self) -> int
    def contrarian_strategy(self) -> int
    def time_series_strategy(self, lookback: int = 50) -> int
    def hot_cold_balanced_strategy(self) -> int
    def range_balanced_strategy(self) -> int
    def weighted_random_strategy(self) -> int
```

### StarStrategies

```python
class StarStrategies:
    def __init__(self, data: pd.DataFrame)
    def generate(self, strategy: str = 'balanced') -> dict
    def get_statistics(self) -> dict
    
    # Individual strategy methods
    def frequency_strategy(self) -> List[int]
    def balanced_strategy(self) -> List[int]
    def contrarian_strategy(self) -> List[int]
    def range_balanced_strategy(self) -> List[int]
    def pair_frequency_strategy(self) -> List[int]
    def markov_strategy(self) -> List[int]
    def time_series_strategy(self, lookback: int = 50) -> List[int]
    def weighted_random_strategy(self) -> List[int]
```

### Return Formats

#### Lucky Number Generate
```python
{
    'lucky_number': 7,        # int (1-10)
    'strategy': 'contrarian', # str
    'score': 85.5            # float (0-100 confidence)
}
```

#### Star Generate
```python
{
    'stars': [3, 9],          # List[int] (1-12)
    'strategy': 'pair_frequency', # str
    'score': 72.3             # float (0-100 confidence)
}
```

#### Statistics
```python
# Lucky Number
{
    'most_frequent': [(7, 245), (3, 238), (5, 231)],
    'least_frequent': [(10, 189), (1, 195), (8, 198)],
    'frequency_distribution': {1: 195, 2: 210, ...},
    'total_draws': 2543
}

# Stars
{
    'most_frequent': [(3, 456), (9, 442), (2, 438)],
    'least_frequent': [(11, 312), (6, 325), (10, 331)],
    'frequency_distribution': {1: 389, 2: 438, ...},
    'most_common_pairs': [((2, 9), 89), ((3, 8), 85), ...],
    'total_draws': 1876
}
```

---

## Best Practices

### Recommended Combinations

| Main Number Strategy | Recommended Lucky/Star Strategy | Rationale |
|---------------------|--------------------------------|-----------|
| Risk/Reward Balance | `contrarian` | Balance hot main numbers with overdue lucky |
| Frequency Analysis | `frequency` | Consistent approach across both |
| Markov Chain | `pair_frequency` (stars) | Both use pattern-based logic |
| Time Series | `time_series` | Both focus on recent trends |
| Coverage Optimization | `range_balanced` | Maximize range coverage |
| Mixed Strategy | `balanced` | Both use blended approaches |

### Probability Baseline

| Lottery | Lucky/Star | Random Probability |
|---------|------------|-------------------|
| French Loto | 1 Lucky (1-10) | 10% per draw |
| Euromillions | 2 Stars (1-12) | 1.52% for 2/2, 30.3% for 1/2 |

Any strategy consistently above these baselines is performing better than random chance.

### Tips

1. **Run backtests first** to see which strategies perform best on your historical data
2. **Different time periods** may favor different strategies
3. **Combine approaches**: Use frequency for main numbers, contrarian for lucky
4. **Monitor performance**: Track which combinations actually win

---

## Changelog

- **v1.0 (2026-01-04)**: Initial release
  - 7 lucky number strategies for French Loto
  - 8 star strategies for Euromillions
  - Backtesting functions
  - UI integration for separate strategy selection

