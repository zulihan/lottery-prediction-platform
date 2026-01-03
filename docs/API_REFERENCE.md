# API Reference - Strategy Methods

**Last Updated:** 2026-01-03
**Version:** 1.0 (Post-Refactoring)

---

## Overview

This document provides a complete API reference for all prediction strategies available in the Lottery Prediction Platform.

**Location:** `src/core/strategies.py`
**Main Class:** `PredictionStrategies`

---

## Table of Contents

1. [Initialization](#initialization)
2. [Core Strategies](#core-strategies)
3. [Advanced Strategies](#advanced-strategies)
4. [Model-Based Strategies](#model-based-strategies)
5. [Output Format](#output-format)
6. [Helper Methods](#helper-methods)

---

## Initialization

### `PredictionStrategies(stats)`

Initialize the strategies engine with statistical analysis.

**Parameters:**
- `stats` (`EuromillionsStatistics`): Statistics object containing historical data analysis

**Example:**
```python
from src.core.statistics import EuromillionsStatistics
from src.core.strategies import PredictionStrategies
import pandas as pd

# Load data
df = load_euromillions_data()

# Create statistics
stats = EuromillionsStatistics(df)

# Initialize strategies
strategies = PredictionStrategies(stats)
```

---

## Core Strategies

### 1. `frequency_strategy(num_combinations=5, recent_weight=0.6)`

Generate combinations based on weighted frequency analysis.

**Description:**
Selects numbers proportional to their historical occurrence frequency, with optional weighting toward recent draws.

**Parameters:**
- `num_combinations` (int, default=5): Number of combinations to generate
- `recent_weight` (float, 0.0-1.0, default=0.6): Weight given to recent draws
  - `0.0` = All draws weighted equally
  - `0.6` = 60% weight to recent draws
  - `1.0` = Only recent draws considered

**Returns:**
`List[dict]` - Each dict contains `numbers`, `stars`, `score`, `strategy`

**Algorithm:**
1. Calculate weighted frequency for each number
2. Apply recent_weight to prioritize recent draws
3. Sample numbers proportionally to weighted frequency
4. Score based on average frequency of selected numbers

**Example:**
```python
# Conservative: Equal weight to all history
combos = strategies.frequency_strategy(num_combinations=5, recent_weight=0.3)

# Balanced: Moderate recent bias
combos = strategies.frequency_strategy(num_combinations=10, recent_weight=0.6)

# Aggressive: Heavy recent bias
combos = strategies.frequency_strategy(num_combinations=5, recent_weight=0.9)
```

**Use Cases:**
- Conservative players who trust long-term trends
- When recent draws show consistency with historical patterns
- Baseline strategy for comparison

**File Location:** `src/core/strategies.py:40`

---

### 2. `mixed_strategy(num_combinations=5, hot_ratio=0.7)`

Mix hot (frequent) and cold (rare) numbers strategically.

**Description:**
Balances high-frequency numbers with strategic "due" numbers for diversification.

**Parameters:**
- `num_combinations` (int, default=5): Number of combinations to generate
- `hot_ratio` (float, 0.0-1.0, default=0.7): Proportion of hot numbers
  - `0.7` = 3-4 hot numbers, 1-2 cold numbers
  - `0.5` = Equal mix of hot and cold
  - `0.9` = Mostly hot numbers

**Returns:**
`List[dict]`

**Algorithm:**
1. Identify hot numbers (top 50% by frequency)
2. Identify cold numbers (bottom 50% by frequency)
3. Select `hot_ratio * 5` numbers from hot pool
4. Select remaining from cold pool
5. Score combines frequency value with diversity bonus

**Example:**
```python
# Hot-heavy: Trust frequent numbers
combos = strategies.mixed_strategy(num_combinations=5, hot_ratio=0.8)

# Balanced: Equal hot/cold mix
combos = strategies.mixed_strategy(num_combinations=10, hot_ratio=0.5)

# Cold-heavy: Bet on due numbers
combos = strategies.mixed_strategy(num_combinations=5, hot_ratio=0.3)
```

**Use Cases:**
- Balanced risk/reward approach
- Hedging between frequency and rarity
- When historical patterns are unclear

**File Location:** `src/core/strategies.py:218`

---

### 3. `temporal_strategy(num_combinations=5, lookback_period=20)`

Identify cyclical patterns and temporal relationships.

**Description:**
Analyzes recent draw sequences to detect emerging patterns, cycles, and "due" numbers.

**Parameters:**
- `num_combinations` (int, default=5): Number of combinations to generate
- `lookback_period` (int, 10-100, default=20): Number of recent draws to analyze

**Returns:**
`List[dict]`

**Algorithm:**
1. Focus on last N draws (lookback_period)
2. Detect cycles and periodicity in appearances
3. Calculate "due" numbers based on historical gaps
4. Weight selection by pattern strength and recency

**Example:**
```python
# Short-term patterns
combos = strategies.temporal_strategy(num_combinations=5, lookback_period=10)

# Medium-term cycles
combos = strategies.temporal_strategy(num_combinations=10, lookback_period=30)

# Long-term trends
combos = strategies.temporal_strategy(num_combinations=5, lookback_period=50)
```

**Use Cases:**
- When clear cyclical patterns exist
- Short-term trend following
- Complement to frequency strategies

**File Location:** `src/core/strategies.py:290`

---

### 4. `stratified_sampling_strategy(num_combinations=5, strata_type="range", balance_factor=0.7)`

Ensure balanced distribution across number ranges and patterns.

**Description:**
Divides number pool into segments (strata) and samples proportionally to ensure comprehensive coverage.

**Parameters:**
- `num_combinations` (int, default=5): Number of combinations to generate
- `strata_type` (str, default="range"): Type of stratification
  - `"range"` = By decade (1-10, 11-20, etc.)
  - `"pattern"` = By even/odd distribution
  - `"sum"` = By sum ranges
- `balance_factor` (float, 0.0-1.0, default=0.7): How strictly to balance across strata

**Returns:**
`List[dict]`

**Algorithm:**
1. Divide numbers into strata based on strata_type
2. Calculate target samples per stratum
3. Apply balance_factor to enforce distribution
4. Sample within each stratum proportionally

**Example:**
```python
# Range-based: One from each decade
combos = strategies.stratified_sampling_strategy(
    num_combinations=5,
    strata_type="range",
    balance_factor=0.8
)

# Pattern-based: Balance even/odd
combos = strategies.stratified_sampling_strategy(
    num_combinations=10,
    strata_type="pattern",
    balance_factor=0.7
)

# Sum-based: Balanced total sums
combos = strategies.stratified_sampling_strategy(
    num_combinations=5,
    strata_type="sum",
    balance_factor=0.9
)
```

**Use Cases:**
- Avoid number clustering
- Ensure full spectrum coverage
- Systematic approach

**File Location:** `src/core/strategies.py:330`

---

### 5. `coverage_strategy(num_combinations=5, balanced=True)`

Maximize coverage of potential winning combinations.

**Description:**
Generates combinations that collectively cover as many possible number pairs and combinations as feasible.

**Parameters:**
- `num_combinations` (int, default=5): Number of combinations to generate
- `balanced` (bool, default=True): Balance coverage with probability
  - `True` = Weighted coverage (considers frequency)
  - `False` = Maximum coverage (ignores frequency)

**Returns:**
`List[dict]`

**Algorithm:**
1. Start with frequency-based combinations
2. Track covered numbers and pairs
3. Add combinations that maximize uncovered elements
4. Balance between coverage and probability if balanced=True

**Example:**
```python
# Balanced: Coverage + frequency
combos = strategies.coverage_strategy(num_combinations=10, balanced=True)

# Maximum coverage: Ignore frequency
combos = strategies.coverage_strategy(num_combinations=15, balanced=False)
```

**Use Cases:**
- Playing multiple combinations
- Systematic coverage systems
- Lottery syndicates

**File Location:** `src/core/strategies.py:540`

---

## Advanced Strategies

### 6. `risk_reward_strategy(num_combinations=5, risk_level=5)`

Optimize for potential return on investment by avoiding commonly played combinations.

**Description:**
Generates combinations that are statistically valid but less likely to be played by others, minimizing jackpot sharing.

**Parameters:**
- `num_combinations` (int, default=5): Number of combinations to generate
- `risk_level` (int or float): Risk appetite
  - Integer scale: 1-10 (1=conservative, 10=risky)
  - Float scale: 0.0-1.0 (auto-converted from integer)

**Returns:**
`List[dict]`

**Algorithm:**
1. For high risk: Prefer uncommon numbers, unusual sums, varied patterns
2. For low risk: Prefer frequent numbers with some randomization
3. Analyze sum distributions to avoid "popular" totals
4. Score based on uniqueness (high risk) or frequency (low risk)

**Example:**
```python
# Conservative: Mostly frequent numbers
combos = strategies.risk_reward_strategy(num_combinations=5, risk_level=2)

# Balanced: Moderate uniqueness
combos = strategies.risk_reward_strategy(num_combinations=10, risk_level=5)

# Aggressive: Unique combinations
combos = strategies.risk_reward_strategy(num_combinations=5, risk_level=9)
```

**Use Cases:**
- Optimizing expected value
- Avoiding number combinations others play
- Strategic advantage seeking

**File Location:** `src/core/strategies.py:1010`

---

### 7. `cognitive_bias_strategy(num_combinations=5)`

Generate combinations that avoid common human selection biases.

**Description:**
Creates combinations that typical players overlook due to psychological biases.

**Parameters:**
- `num_combinations` (int, default=5): Number of combinations to generate

**Returns:**
`List[dict]`

**Algorithm:**
1. Identify common biases:
   - Birthdays (numbers 1-31)
   - Consecutive numbers
   - Pattern formations
   - Round/favorite numbers
2. Weight against these biased selections
3. Favor high numbers (>31), unpopular numbers (4, 13, etc.)
4. Avoid consecutive sequences
5. Create "unusual" but valid combinations

**Example:**
```python
# Anti-bias combinations
combos = strategies.cognitive_bias_strategy(num_combinations=10)
```

**Use Cases:**
- Minimizing jackpot sharing risk
- Contrarian play
- Taking advantage of human psychology

**File Location:** `src/core/strategies.py:1319`

---

## Model-Based Strategies

### 8. `bayesian_strategy(num_combinations=5, recent_draws_count=20, prior_type="uniform", update_method="full")`

Apply Bayesian probability theory with prior/posterior updating.

**Description:**
Uses Bayesian inference to update probability beliefs based on recent evidence.

**Parameters:**
- `num_combinations` (int, default=5): Number of combinations to generate
- `recent_draws_count` (int, 5-50, default=20): Recent draws for posterior update
- `prior_type` (str, default="uniform"): Prior distribution type
  - `"uniform"` = All numbers equally likely initially
  - `"frequency"` = Based on historical frequency
- `update_method` (str, default="full"): How to update posteriors
  - `"full"` = Full Bayesian update
  - `"incremental"` = Gradual update

**Returns:**
`List[dict]`

**Algorithm:**
1. Establish prior probability P(number)
2. Calculate likelihood P(recent_draws | number)
3. Compute posterior P(number | recent_draws) using Bayes' theorem
4. Sample numbers from posterior distribution

**Example:**
```python
# Uniform prior with recent evidence
combos = strategies.bayesian_strategy(
    num_combinations=5,
    recent_draws_count=20,
    prior_type="uniform"
)

# Frequency-based prior
combos = strategies.bayesian_strategy(
    num_combinations=10,
    recent_draws_count=30,
    prior_type="frequency",
    update_method="full"
)
```

**Use Cases:**
- Mathematically rigorous approach
- Incorporating recent trends into historical data
- Statistical modeling enthusiasts

**File Location:** `src/core/strategies.py:1169`

---

### 9. `markov_strategy(num_combinations=5, lag=1)`

Model number transitions using Markov chains.

**Description:**
Analyzes how numbers follow each other across consecutive draws to predict future states.

**Parameters:**
- `num_combinations` (int, default=5): Number of combinations to generate
- `lag` (int, 1-5, default=1): Number of previous draws to consider
  - `1` = First-order Markov (previous draw only)
  - `2` = Second-order Markov (two previous draws)

**Returns:**
`List[dict]`

**Algorithm:**
1. Build transition matrix P(number_t | number_t-lag)
2. Calculate stationary distribution
3. Use conditional probabilities from recent draws
4. Sample from Markov chain distribution

**Example:**
```python
# First-order: Only last draw matters
combos = strategies.markov_strategy(num_combinations=5, lag=1)

# Second-order: Last two draws matter
combos = strategies.markov_strategy(num_combinations=10, lag=2)
```

**Use Cases:**
- Sequence-based prediction
- When draws show serial correlation
- Advanced statistical modeling

**File Location:** `src/core/strategies.py:1242`

---

### 10. `time_series_strategy(num_combinations=5, window_size=10)`

Detect cycles, seasonality, and trends using time series analysis.

**Description:**
Applies time series decomposition to identify temporal patterns and forecast future draws.

**Parameters:**
- `num_combinations` (int, default=5): Number of combinations to generate
- `window_size` (int, 5-30, default=10): Sliding window size for pattern detection

**Returns:**
`List[dict]`

**Algorithm:**
1. Decompose time series (trend + seasonal + cyclical + residual)
2. Apply sliding window for local pattern detection
3. Forecast based on identified components
4. Sample from forecasted distribution

**Example:**
```python
# Short-term patterns
combos = strategies.time_series_strategy(num_combinations=5, window_size=7)

# Medium-term cycles
combos = strategies.time_series_strategy(num_combinations=10, window_size=15)

# Long-term trends
combos = strategies.time_series_strategy(num_combinations=5, window_size=25)
```

**Use Cases:**
- Long-term trend identification
- Seasonal pattern exploitation
- Advanced forecasting

**File Location:** `src/core/strategies.py:1285`

---

## Output Format

All strategy methods return the same standardized format:

```python
[
    {
        'numbers': [5, 12, 23, 34, 45],  # List[int], sorted, length=5, range 1-50
        'stars': [3, 9],                  # List[int], sorted, length=2, range 1-12
        'score': 85.3,                    # float, strategy confidence (0-100)
        'strategy': 'Frequency'           # str, strategy name
    },
    # ... num_combinations total
]
```

**Field Specifications:**

- `numbers`: 5 unique integers, sorted ascending, range [1, 50]
- `stars`: 2 unique integers, sorted ascending, range [1, 12]
- `score`: Float representing strategy confidence/quality, typically 0-100
- `strategy`: Human-readable strategy name (optional, some methods omit this)

**Validation:**
```python
def validate_combination(combo):
    assert len(combo['numbers']) == 5
    assert len(combo['stars']) == 2
    assert all(1 <= n <= 50 for n in combo['numbers'])
    assert all(1 <= s <= 12 for s in combo['stars'])
    assert len(set(combo['numbers'])) == 5  # Unique
    assert len(set(combo['stars'])) == 2    # Unique
    assert combo['numbers'] == sorted(combo['numbers'])
    assert combo['stars'] == sorted(combo['stars'])
```

---

## Helper Methods

### `_weighted_sample(frequency_dict, count)`

Internal method for weighted random sampling.

**Parameters:**
- `frequency_dict` (dict): `{number: frequency_weight}`
- `count` (int): Number of samples to draw

**Returns:**
`List[int]` - Sampled numbers (unique)

**Algorithm:**
Uses weighted random selection without replacement.

**File Location:** `src/core/strategies.py:24`

---

## Strategy Comparison Matrix

| Strategy | Complexity | Data Required | Best For | Risk Level |
|----------|-----------|---------------|----------|-----------|
| Frequency | Low | Historical draws | Beginners | Low |
| Mixed | Low | Historical draws | Balanced play | Medium |
| Temporal | Medium | Recent draws | Pattern players | Medium |
| Stratified | Medium | Historical draws | Coverage seekers | Low |
| Coverage | Medium | Historical draws | Syndicates | Low |
| Risk/Reward | Medium | Frequency data | ROI optimizers | Variable |
| Cognitive Bias | Medium | Frequency data | Contrarians | Medium-High |
| Bayesian | High | Recent + historical | Statisticians | Medium |
| Markov | High | Sequential draws | Quants | Medium-High |
| Time Series | High | Long history | Data scientists | Medium |

---

## Usage Examples

### Simple Usage
```python
from src.core.database import get_db_connection
from src.core.statistics import EuromillionsStatistics
from src.core.strategies import PredictionStrategies
import pandas as pd

# Load data
engine = get_db_connection()
df = pd.read_sql("SELECT * FROM euromillions_drawing ORDER BY date DESC", engine)

# Create statistics
stats = EuromillionsStatistics(df)

# Initialize strategies
strategies = PredictionStrategies(stats)

# Generate combinations
combos = strategies.frequency_strategy(num_combinations=5)

# Display
for i, combo in enumerate(combos, 1):
    print(f"#{i}: {combo['numbers']} + {combo['stars']} (Score: {combo['score']})")
```

### Multi-Strategy Approach
```python
# Generate one combo from each strategy
all_combos = []

all_combos.extend(strategies.frequency_strategy(1))
all_combos.extend(strategies.mixed_strategy(1))
all_combos.extend(strategies.bayesian_strategy(1))
all_combos.extend(strategies.markov_strategy(1))
all_combos.extend(strategies.cognitive_bias_strategy(1))

# 5 diverse combinations using different methods
print(f"Generated {len(all_combos)} combinations using 5 different strategies")
```

### Parameter Optimization
```python
# Test different parameters
for recent_weight in [0.3, 0.5, 0.7, 0.9]:
    combos = strategies.frequency_strategy(
        num_combinations=10,
        recent_weight=recent_weight
    )
    avg_score = sum(c['score'] for c in combos) / len(combos)
    print(f"recent_weight={recent_weight}: avg_score={avg_score:.2f}")
```

---

## Error Handling

All strategy methods may raise:

- `ValueError`: Invalid parameters (e.g., `num_combinations < 1`)
- `AttributeError`: Statistics object missing required methods
- `KeyError`: Missing required data in statistics

**Example Error Handling:**
```python
try:
    combos = strategies.frequency_strategy(num_combinations=5)
except ValueError as e:
    print(f"Invalid parameters: {e}")
except AttributeError as e:
    print(f"Statistics object incomplete: {e}")
```

---

## Performance Notes

- **Frequency-based strategies** (Frequency, Mixed): Fast (~10ms)
- **Model-based strategies** (Bayesian, Markov, Time Series): Slower (~100-500ms)
- **Coverage strategy**: Slowest for large num_combinations (~1s for 20+ combos)

**Optimization Tips:**
- Cache `EuromillionsStatistics` object
- Reuse `PredictionStrategies` instance
- Generate larger batches at once vs. multiple small batches

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [STATISTICS_API.md](STATISTICS_API.md) - Statistics class reference
- [strategy_descriptions.md](../strategy_descriptions.md) - User-facing strategy descriptions
