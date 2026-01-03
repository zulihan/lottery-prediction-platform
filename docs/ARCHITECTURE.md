# Architecture Documentation

**Last Updated:** 2026-01-03
**Version:** 1.0 (Post-Refactoring)

---

## Overview

The Lottery Prediction Platform is a sophisticated statistical analysis system for Euromillions and French Loto lottery draws. It implements 15+ prediction strategies based on frequency analysis, Bayesian models, Markov chains, time series analysis, and other statistical approaches.

**Tech Stack:**
- **Frontend:** Streamlit (Python web framework)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly, Matplotlib
- **Statistical Models:** Custom implementations (Bayesian, Markov, Time Series)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Web UI (app.py)               │
│  - Data loading & visualization                             │
│  - User interaction & controls                              │
│  - Combination generation interface                         │
└───────────────────┬─────────────────────────────────────────┘
                    │
    ┌───────────────┴───────────────┐
    │                               │
    ▼                               ▼
┌─────────────────┐         ┌─────────────────┐
│  src/core/      │         │  src/utils/     │
│  Statistics     │         │  Utilities      │
│  - Frequency    │         │  - Analysis     │
│  - Patterns     │         │  - Recomm.      │
│  - Distributions│         └─────────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  src/core/strategies.py                 │
│  PredictionStrategies (15+ methods)     │
│  ┌─────────────────────────────────┐   │
│  │ • Frequency Strategy            │   │
│  │ • Mixed Strategy                │   │
│  │ • Temporal Strategy             │   │
│  │ • Risk/Reward Optimization      │   │
│  │ • Bayesian Model                │   │
│  │ • Markov Chain Model            │   │
│  │ • Time Series Model             │   │
│  │ • Anti-Cognitive Bias           │   │
│  │ • Coverage Strategy             │   │
│  │ • Stratified Sampling           │   │
│  └─────────────────────────────────┘   │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│  src/core/models.py                     │
│  Statistical Models                     │
│  - BayesianModel                        │
│  - MarkovModel                          │
│  - TimeSeriesModel                      │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│  src/core/database.py                   │
│  SQLAlchemy ORM & PostgreSQL            │
│  - EuromillionsDrawing                  │
│  - FrenchLotoDrawing                    │
│  - GeneratedCombination                 │
│  - FrenchLotoPrediction                 │
└─────────────────────────────────────────┘
```

---

## Core Components

### 1. Database Layer (`src/core/database.py`)

**Purpose:** Data persistence and retrieval using PostgreSQL.

**Key Components:**
- **SQLAlchemy ORM Models:**
  - `EuromillionsDrawing` - Historical Euromillions draws
  - `FrenchLotoDrawing` - Historical French Loto draws
  - `GeneratedCombination` - User-generated Euromillions predictions
  - `FrenchLotoPrediction` - User-generated French Loto predictions

- **Connection Management:**
  - Connection pooling (QueuePool)
  - Automatic retry logic with exponential backoff
  - Session management with scoped sessions
  - Database initialization (`init_db()`)

**Database Schema:**

```sql
-- Euromillions Drawings
CREATE TABLE euromillions_drawing (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    n1, n2, n3, n4, n5 INTEGER,  -- Main numbers (1-50)
    s1, s2 INTEGER                -- Star numbers (1-12)
);

-- French Loto Drawings
CREATE TABLE french_loto_drawing (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    n1, n2, n3, n4, n5 INTEGER,  -- Main numbers (1-49)
    lucky_number INTEGER          -- Lucky number (1-10)
);

-- Generated Combinations
CREATE TABLE generated_combination (
    id SERIAL PRIMARY KEY,
    created_at DATE,
    n1, n2, n3, n4, n5 INTEGER,
    s1, s2 INTEGER,
    strategy VARCHAR(100),
    score FLOAT
);

-- French Loto Predictions
CREATE TABLE french_loto_prediction (
    id SERIAL PRIMARY KEY,
    created_at DATE,
    numbers VARCHAR(50),         -- "n1-n2-n3-n4-n5"
    lucky_number INTEGER,
    strategy VARCHAR(100)
);
```

**Connection String:**
```python
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://...')
# Supports both local and remote PostgreSQL (Replit, etc.)
```

---

### 2. Statistics Layer (`src/core/statistics.py`, `src/core/french_loto_statistics.py`)

**Purpose:** Statistical analysis of historical draw data.

**Class: EuromillionsStatistics**

**Core Methods:**
- `get_frequency(number=None)` - Number occurrence frequency
- `get_star_frequency(star=None)` - Star occurrence frequency
- `get_weighted_frequency(recent_weight=0.5)` - Time-weighted frequency
- `get_hot_numbers(count=10)` - Most frequent numbers
- `get_cold_numbers(count=10)` - Least frequent numbers
- `get_distribution_stats()` - Statistical distribution analysis
- `get_sum_distribution()` - Sum ranges and patterns
- `get_consecutive_analysis()` - Consecutive number patterns
- `get_gap_analysis(number=None)` - Draw gaps between appearances
- `get_number_range_distribution(ranges=None)` - Distribution by ranges
- `get_even_odd_distribution()` - Even/odd ratio analysis

**Data Flow:**
```
Historical Data (DataFrame)
    ↓
__init__(data)
    ↓
_calculate_frequencies()
    ↓
{number_frequency, star_frequency} dictionaries
    ↓
Analysis methods return insights
```

**Example Usage:**
```python
from src.core.statistics import EuromillionsStatistics
import pandas as pd

# Load historical data
df = load_euromillions_data()

# Create statistics instance
stats = EuromillionsStatistics(df)

# Get insights
hot_numbers = stats.get_hot_numbers(10)
frequency_dist = stats.get_weighted_frequency(0.7)
range_dist = stats.get_number_range_distribution()
even_odd = stats.get_even_odd_distribution()
```

---

### 3. Strategy Layer (`src/core/strategies.py`)

**Purpose:** Generate lottery combinations using various statistical strategies.

**Class: PredictionStrategies**

**Constructor:**
```python
def __init__(self, stats: EuromillionsStatistics):
    """
    Initialize strategies with statistical analysis object.

    Parameters:
        stats: EuromillionsStatistics instance with historical data
    """
```

**15+ Strategy Methods:**

| Strategy | Method | Key Parameters | Approach |
|----------|--------|----------------|----------|
| Frequency | `frequency_strategy()` | `recent_weight` | Weighted historical frequency |
| Mixed | `mixed_strategy()` | `hot_ratio` | Balance hot/cold numbers |
| Temporal | `temporal_strategy()` | `lookback_period` | Cyclical pattern detection |
| Stratified | `stratified_sampling_strategy()` | `strata_type`, `balance_factor` | Range-balanced sampling |
| Coverage | `coverage_strategy()` | `balanced` | Maximum number coverage |
| Risk/Reward | `risk_reward_strategy()` | `risk_level` | Optimize uniqueness |
| Bayesian | `bayesian_strategy()` | `recent_draws_count` | Bayesian probability |
| Markov | `markov_strategy()` | `lag` | Markov chain transitions |
| Time Series | `time_series_strategy()` | `window_size` | Temporal trends |
| Cognitive Bias | `cognitive_bias_strategy()` | - | Avoid human biases |

**Output Format:**
```python
[
    {
        'numbers': [5, 12, 23, 34, 45],  # Sorted main numbers
        'stars': [3, 9],                  # Sorted star numbers
        'score': 85.3,                    # Strategy confidence score
        'strategy': 'Frequency'           # Strategy name
    },
    # ... more combinations
]
```

**Strategy Selection Guide:**

- **Conservative Players:** Frequency, Stratified Sampling
- **Balanced Approach:** Mixed, Coverage, Bayesian
- **Aggressive Players:** Risk/Reward, Cognitive Bias
- **Data Scientists:** Markov, Time Series, Bayesian

---

### 4. Model Layer (`src/core/models.py`)

**Purpose:** Advanced statistical models for prediction.

#### BayesianModel
```python
class BayesianModel:
    """
    Bayesian probability model with prior/posterior updating.

    Methods:
        generate_combinations(num_combinations) -> List[Combination]
    """
```

**Approach:**
1. Establish prior probability distributions
2. Update with evidence from recent draws
3. Calculate posterior probabilities using Bayes' theorem
4. Sample numbers based on posteriors

#### MarkovModel
```python
class MarkovModel:
    """
    Markov chain model for sequence prediction.

    Methods:
        generate_combinations(num_combinations) -> List[Combination]
    """
```

**Approach:**
1. Build transition matrices from draw sequences
2. Calculate stationary probabilities
3. Use conditional probabilities based on recent draws
4. Sample from Markov chain distribution

#### TimeSeriesModel
```python
class TimeSeriesModel:
    """
    Time series analysis for temporal patterns.

    Methods:
        generate_combinations(num_combinations) -> List[Combination]
    """
```

**Approach:**
1. Apply time series decomposition (trend, seasonal, cyclical)
2. Use sliding window for pattern detection
3. Forecast based on temporal components
4. Generate combinations from forecasted probabilities

---

### 5. Application Layer (`app.py`)

**Purpose:** Streamlit web interface for user interaction.

**Key Sections:**

1. **Data Loading:**
   - Connect to PostgreSQL database
   - Load Euromillions/French Loto historical data
   - Display data preview and statistics

2. **Strategy Selection:**
   - User chooses strategy type
   - Configure strategy parameters
   - Number of combinations to generate

3. **Combination Generation:**
   - Execute selected strategy
   - Display generated combinations
   - Show confidence scores

4. **Visualization:**
   - Frequency charts (Plotly)
   - Distribution analysis
   - Pattern visualizations

5. **Persistence:**
   - Save combinations to database
   - Track generated predictions
   - Compare with future draws

**Session State Management:**
```python
st.session_state.processed_data      # Loaded historical data
st.session_state.loto_processed_data # French Loto data
```

---

## Data Flow

### Combination Generation Flow

```
User Selects Strategy
    ↓
app.py creates EuromillionsStatistics(data)
    ↓
app.py creates PredictionStrategies(stats)
    ↓
User clicks "Generate"
    ↓
strategies.frequency_strategy(params)
    ↓
Strategy accesses stats.get_frequency()
    ↓
Strategy applies algorithm
    ↓
Returns List[{'numbers': [...], 'stars': [...], 'score': ...}]
    ↓
app.py displays in UI
    ↓
User saves to database (optional)
    ↓
database.GeneratedCombination created
    ↓
Committed to PostgreSQL
```

### Backtest Flow

```
Load historical draws (past N months)
    ↓
For each draw date:
    ↓
    Split: training data (before date) + test draw (on date)
    ↓
    Generate combinations using training data
    ↓
    Compare with actual test draw
    ↓
    Calculate match scores (5+2, 5+1, 5+0, etc.)
    ↓
Aggregate results across all test draws
    ↓
Report strategy performance metrics
```

---

## Design Patterns

### 1. Strategy Pattern
**Usage:** `PredictionStrategies` class
**Benefit:** Easy to add new strategies without modifying existing code

### 2. Repository Pattern
**Usage:** `database.py` with SQLAlchemy
**Benefit:** Abstracts database operations from business logic

### 3. Dependency Injection
**Usage:** `PredictionStrategies(stats)`
**Benefit:** Testable, flexible, decoupled components

### 4. Factory Pattern
**Usage:** Model creation in `models.py`
**Benefit:** Encapsulates model instantiation logic

---

## Performance Considerations

### Database Connection Pooling
```python
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True  # Verify connections before use
)
```

### Caching Strategy
- Streamlit's `@st.cache_data` for data loading
- Session state for statistics objects
- Avoid redundant database queries

### Query Optimization
- Index on date columns
- Limit result sets with `.limit()`
- Use `.filter()` instead of loading all data

---

## Error Handling

### Database Errors
```python
try:
    session.commit()
except exc.IntegrityError:
    session.rollback()
    # Handle duplicate entries
except exc.OperationalError:
    # Retry with exponential backoff
```

### Data Validation
- Check number ranges (1-50 for main, 1-12 for stars)
- Ensure uniqueness within combinations
- Validate date formats

### Graceful Degradation
- Continue if optional features fail
- Display user-friendly error messages
- Log errors for debugging

---

## Security Considerations

### Database Access
- Use environment variables for credentials
- Never commit DATABASE_URL to git
- Use read-only connections where possible

### Input Validation
- Sanitize user inputs
- Prevent SQL injection (SQLAlchemy handles this)
- Validate parameter ranges

### Data Privacy
- No personal user data stored
- Combinations are anonymous
- Comply with data retention policies

---

## Deployment Architecture

### Local Development
```
Local PostgreSQL → Streamlit Dev Server → localhost:5000
```

### Production (Replit/Cloud)
```
Remote PostgreSQL → Streamlit Cloud → Public URL
Connection pooling enabled
Rate limiting configured
```

---

## Testing Strategy

### Unit Tests (Phase 8)
- Test each strategy method independently
- Mock `EuromillionsStatistics` for isolation
- Verify output format and constraints

### Integration Tests
- Test database operations
- Test full combination generation flow
- Verify data persistence

### Backtest Validation
- Historical accuracy testing
- Performance benchmarking
- Strategy comparison metrics

---

## Extension Points

### Adding New Strategies
1. Add method to `PredictionStrategies` class
2. Follow naming convention: `{name}_strategy()`
3. Accept `num_combinations` parameter
4. Return standard format: `List[dict]`
5. Update `strategy_descriptions.md`

### Adding New Games
1. Create new statistics class (e.g., `PowerballStatistics`)
2. Create new strategy class
3. Add database model for draws
4. Update UI in `app.py`

### Adding New Models
1. Create model class in `models.py`
2. Implement `generate_combinations()` method
3. Use in strategy methods as needed

---

## References

- **Strategy Descriptions:** `strategy_descriptions.md`
- **API Reference:** `docs/API_REFERENCE.md`
- **Statistics API:** `docs/STATISTICS_API.md`
- **Testing Guide:** `docs/TESTING_GUIDE.md`
- **Refactoring History:** `docs/REFACTORING_HISTORY.md`
