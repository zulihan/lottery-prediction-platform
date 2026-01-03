# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📚 Documentation Index

**Quick Reference (This File):** Core commands, architecture overview, common patterns

**Comprehensive Documentation:**
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture, data flow, design patterns
- **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - Complete strategy API with examples
- **[docs/STATISTICS_API.md](docs/STATISTICS_API.md)** - Statistics class methods reference
- **[docs/REFACTORING_HISTORY.md](docs/REFACTORING_HISTORY.md)** - Refactoring phases & decisions
- **[docs/EXTRACTED_CODE.md](docs/EXTRACTED_CODE.md)** - Useful code from archived files
- **[strategy_descriptions.md](strategy_descriptions.md)** - User-facing strategy descriptions

---

## Project Overview

A comprehensive lottery prediction platform for Euromillions and French Loto that uses advanced statistical analysis and machine learning techniques. The application combines 15+ prediction strategies including frequency analysis, Fibonacci sequences, risk/reward models, Bayesian inference, Markov chains, and time series analysis.

## Core Commands

### Running the Application
```bash
# Main Streamlit application (default port 5000)
streamlit run app.py --server.port 5000

# Alternative: Simple Fibonacci test app
streamlit run simple_fibonacci_test.py --server.port 5001
```

### Database Setup
```bash
# Import Euromillions historical data
psql -U postgres -d lottery_prediction -f db_dump/euromillions_drawings.sql

# Import French Loto historical data
psql -U postgres -d lottery_prediction -f db_dump/french_loto_drawings.sql

# Connect to database (requires DATABASE_URL environment variable)
export DATABASE_URL="postgresql://postgres:password@localhost:5432/lottery_prediction"
```

### Testing
Note: Formal test infrastructure is planned for Phase 8. Current validation is through backtesting scripts.

## Architecture

**📚 For detailed architecture documentation, see:** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

### Project Structure (Post-Refactoring)
```
lottery-prediction-platform/
├── app.py                          # Main Streamlit application
├── src/
│   ├── core/                       # Core production code
│   │   ├── database.py            # PostgreSQL models & connection
│   │   ├── models.py              # ML models (Bayesian, Markov, TimeSeries)
│   │   ├── statistics.py          # Euromillions statistics
│   │   ├── strategies.py          # 15+ prediction strategies
│   │   ├── french_loto_strategy.py
│   │   ├── french_loto_statistics.py
│   │   └── fibonacci_strategy.py
│   └── utils/                      # Shared utilities
│       ├── combination_analysis.py
│       └── strategy_recommendation.py
├── archive/                        # Archived development files (139 files)
├── docs/                           # Comprehensive documentation
│   ├── ARCHITECTURE.md            # System design & data flow
│   ├── API_REFERENCE.md           # Strategy API reference
│   ├── STATISTICS_API.md          # Statistics class reference
│   ├── REFACTORING_HISTORY.md     # Refactoring log
│   └── EXTRACTED_CODE.md          # Code preserved from variants
└── tests/                          # Test suite (future)
```

### Application Stack
- **Frontend**: Streamlit-based web application
- **Database**: PostgreSQL 16 with SQLAlchemy ORM
- **Data Processing**: Pandas/NumPy for statistical analysis
- **Visualization**: Plotly and Matplotlib for interactive charts

### Database Architecture
The database uses SQLAlchemy with connection pooling and retry logic to handle rate limits:
- **Pool size**: 2-5 connections (configured to avoid rate limits on Replit)
- **Pool recycle**: 1800 seconds (30 minutes)
- **Retry logic**: Exponential backoff on connection failures
- **Fallback**: SQLite in-memory database if PostgreSQL unavailable

Key tables:
- `euromillions_drawings`: Historical results (n1-n5, s1-s2, date, day_of_week)
- `french_loto_drawings`: Historical results (n1-n5, lucky, date, draw_num, prize/winner data)
- `generated_combinations`: User-generated predictions with strategy metadata
- `french_loto_predictions`: French Loto specific predictions

### Strategy Engine Architecture

The platform implements a **multi-strategy approach** where different statistical methods work in parallel:

1. **Core Strategy Module** (`strategies.py`):
   - `PredictionStrategies` class contains 10+ strategy methods
   - Each strategy returns combinations with `numbers`, `stars`, and `score`
   - Strategies include: frequency, mixed, temporal, stratified_sampling, coverage, risk_reward, bayesian, markov, time_series, cognitive_bias

2. **French Loto Strategy Module** (`french_loto_strategy.py`):
   - `FrenchLotoStrategy` class handles French Loto specific logic
   - Generates 5 main numbers (1-49) + 1 lucky number (1-10)
   - Includes specific methods for lucky number prediction

3. **Fibonacci Strategy Module** (`fibonacci_strategy.py`):
   - Mathematical sequence-based prediction
   - Uses Fibonacci ratios and golden ratio patterns

4. **Statistical Models** (`models.py`):
   - `BayesianModel`: Probabilistic modeling with prior/posterior distributions
   - `MarkovModel`: Markov chain transition probabilities
   - `TimeSeriesModel`: Temporal pattern detection and forecasting

### Data Flow

```
Historical Data (PostgreSQL)
    ↓
Statistics Module (frequency analysis, pattern detection)
    ↓
Strategy Engine (parallel execution of 10+ strategies)
    ↓
Combination Generator (filtered & optimized)
    ↓
Validation/Backtesting (historical performance)
    ↓
Streamlit UI (interactive visualization)
```

### Key Design Patterns

1. **Connection Management**:
   - Use `get_session()` for database operations (includes retry logic)
   - Always close sessions: `session.close()`
   - Use `get_db_connection()` for raw SQL with pandas

2. **Strategy Pattern**:
   - All strategies follow the same interface: `strategy_name(num_combinations, **params)`
   - Return format: `[{'numbers': [n1-n5], 'stars': [s1-s2], 'score': float}]`

3. **Statistics Initialization**:
   - Strategies require a statistics object (e.g., `EuromillionsStatistics`)
   - Statistics objects calculate frequencies, patterns, and distributions from historical data
   - Create strategy instance: `strategies = PredictionStrategies(statistics)`

## File Organization

### Core Application Files
- `app.py`: Main Streamlit application with sidebar navigation
- `database.py`: SQLAlchemy models and connection management
- `strategies.py`: Euromillions prediction strategies
- `french_loto_strategy.py`: French Loto prediction strategies
- `french_loto_statistics.py`: French Loto statistical analysis
- `fibonacci_strategy.py`: Fibonacci-based prediction methods
- `combination_analysis.py`: Tools for analyzing combinations
- `statistics.py`: Core statistical computation functions

### Important Conventions
- The codebase contains 268 Python files (many are analysis/generation scripts from development)
- Scripts prefixed with `generate_*` create specific combinations for past draws
- Scripts prefixed with `analyze_*` perform post-draw analysis
- Scripts prefixed with `backtest_*` validate strategies against historical data
- Main production code: `app.py`, `database.py`, `strategies.py`, `french_loto_*.py`

### Data Files
- `db_dump/`: SQL dumps and CSV exports of historical data
- `sample_data/`: Sample data for testing
- `processed_data/`: Intermediate processed data
- `attached_assets/`: Images and assets

## Development Notes

### When Adding New Strategies
1. Add method to `PredictionStrategies` class following naming convention: `strategy_name_strategy()`
2. Method must return list of dicts with `numbers`, `stars`, and `score`
3. Update `strategy_descriptions.md` with methodology and parameters
4. Add strategy to the UI in `app.py` if user-facing

### Database Connection Handling
- **CRITICAL**: Database connection pooling is configured for rate-limited environments (Replit)
- Pool size is intentionally small (2-5) to prevent hitting connection limits
- If you see "rate limit" errors, the retry logic should handle it automatically
- Connection recycling happens every 30 minutes to prevent stale connections

### Streamlit-Specific Considerations
- Use `st.session_state` for maintaining data across reruns
- Always check if data is loaded before running strategies: `if st.session_state.data_loaded:`
- Cache expensive computations using `@st.cache_data` or file-based caching
- Multi-page apps use sidebar navigation

### Common Patterns

**Loading and using strategies:**
```python
# Get database session
session = get_session()

# Load data
drawings = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date.desc()).limit(1000).all()

# Create statistics object
from statistics import EuromillionsStatistics
stats = EuromillionsStatistics(drawings)

# Create strategy instance
from strategies import PredictionStrategies
strategies = PredictionStrategies(stats)

# Generate combinations
combinations = strategies.frequency_strategy(num_combinations=5, recent_weight=0.6)

session.close()
```

**Saving combinations to database:**
```python
import json
from database import GeneratedCombination, get_session

session = get_session()
for combo in combinations:
    generated = GeneratedCombination(
        target_draw_date=target_date,
        numbers=json.dumps(combo['numbers']),
        stars=json.dumps(combo['stars']),
        strategy='frequency_strategy',
        score=combo['score']
    )
    session.add(generated)
session.commit()
session.close()
```

## Environment Variables

Required:
- `DATABASE_URL`: PostgreSQL connection string (format: `postgresql://user:password@host:port/database`)

Optional (for PostgreSQL):
- `PGHOST`: Database host
- `PGPORT`: Database port
- `PGUSER`: Database user
- `PGPASSWORD`: Database password
- `PGDATABASE`: Database name

## Deployment

This application is configured for deployment on Replit with:
- **Deployment type**: Autoscale
- **Runtime**: Python 3.11 with Nix package management
- **Main port**: 5000 (Euromillions Prediction App)
- **Secondary port**: 5001 (Simple Fibonacci Test)
- **Process management**: Parallel workflow execution

See `.replit` configuration for complete deployment settings.
