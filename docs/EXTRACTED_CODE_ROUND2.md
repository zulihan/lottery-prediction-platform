# Extracted Code Patterns - Round 2 Archive

**Date:** 2026-01-03
**Source:** 121 root-level Python files scheduled for archival
**Purpose:** Preserve valuable code patterns before archiving unused development files

---

## Overview

During analysis of 121 root-level Python files prior to archival, we identified **8-10 genuinely valuable code patterns** that could enhance the main application. This document extracts and preserves these patterns for potential future implementation.

---

## Table of Contents

1. [High-Priority Patterns](#high-priority-patterns)
   - [Fibonacci-Filtered Hybrid Strategy](#1-fibonacci-filtered-hybrid-strategy)
   - [Strategic Fusion Ensemble](#2-strategic-fusion-ensemble)
   - [Jittered Exponential Backoff](#3-jittered-exponential-backoff)
   - [Enhanced Data Processor](#4-enhanced-data-processor)
   - [Failure Analysis Framework](#5-failure-analysis-framework)
2. [Medium-Priority Patterns](#medium-priority-patterns)
   - [Plotly Visualizations](#6-plotly-visualizations)
   - [Markov Multi-Level Transitions](#7-markov-multi-level-transitions)
3. [Low-Priority Patterns](#low-priority-patterns)
   - [Batch Import with Date Filtering](#8-batch-import-with-date-filtering)
   - [Locale Utilities](#9-locale-utilities)

---

## High-Priority Patterns

### 1. Fibonacci-Filtered Hybrid Strategy

**Source File:** `fibonacci_hybrid_strategy.py` (lines 163-250)
**Value:** Two-pass approach (generate → filter → score) more sophisticated than current single-pass strategies

#### Key Innovation

Instead of generating final combinations directly, this pattern uses a **meta-strategy framework**:

1. **Generate Phase:** Create candidates from multiple strategies (Risk/Reward, Frequency, Markov, Time Series)
2. **Filter Phase:** Apply Fibonacci mathematical filtering to enhance/score
3. **Select Phase:** Enforce diversity constraints (max number/strategy reuse)

#### Code Pattern

```python
def apply_fibonacci_filtering(candidates):
    """
    Apply Fibonacci filtering to enhance and score combinations.
    Two-pass approach: strategies generate → Fibonacci filters → diversity selection
    """
    fibonacci_numbers = get_fibonacci_numbers()  # [1, 1, 2, 3, 5, 8, 13, 21, 34]
    may20_fibonacci = [1, 8, 13]  # Historically successful Fibonacci numbers

    filtered_combinations = []

    for strategy_name, strategy_candidates in candidates.items():
        for candidate in strategy_candidates:
            # Calculate Fibonacci metrics
            fib_count = len([n for n in candidate['numbers'] if n in fibonacci_numbers])
            may20_fib_count = len([n for n in candidate['numbers'] if n in may20_fibonacci])
            fib_percentage = fib_count / 5 * 100

            # Calculate Fibonacci score boost
            fibonacci_boost = 0

            # Boost for Fibonacci presence
            if fib_percentage >= 60:  # 3+ Fibonacci numbers
                fibonacci_boost += 25
            elif fib_percentage >= 40:  # 2 Fibonacci numbers
                fibonacci_boost += 15
            elif fib_percentage >= 20:  # 1 Fibonacci number
                fibonacci_boost += 8

            # Extra boost for historically successful Fibonacci numbers
            fibonacci_boost += may20_fib_count * 5

            # Bonus for specific Fibonacci patterns
            if 1 in candidate['numbers'] and 8 in candidate['numbers']:
                fibonacci_boost += 10
            if 13 in candidate['numbers']:
                fibonacci_boost += 8

            # Calculate final hybrid score
            final_score = min(candidate['base_score'] + fibonacci_boost, 100.0)

            enhanced_combo = {
                'numbers': candidate['numbers'],
                'stars': candidate['stars'],
                'strategy': f"Fibonacci-Filtered {candidate['strategy']}",
                'fibonacci_count': fib_count,
                'fibonacci_percentage': fib_percentage,
                'final_score': final_score
            }

            filtered_combinations.append(enhanced_combo)

    # Sort by final score
    filtered_combinations.sort(key=lambda x: x['final_score'], reverse=True)
    return filtered_combinations


def select_best_hybrid_combinations(filtered_combinations, num_final=8):
    """
    Select best combinations with diversity constraints.
    Prevents overusing specific numbers or strategies.
    """
    selected = []
    number_usage = Counter()
    strategy_usage = Counter()

    for combo in filtered_combinations:
        # Enforce diversity - max 2 uses per number, max 3 per strategy
        numbers_ok = all(number_usage[n] < 2 for n in combo['numbers'])
        strategy_ok = strategy_usage[combo['base_strategy']] < 3

        if numbers_ok and strategy_ok and len(selected) < num_final:
            selected.append(combo)
            for n in combo['numbers']:
                number_usage[n] += 1
            strategy_usage[combo['base_strategy']] += 1

    return selected
```

#### How to Integrate

1. Create `src/core/ensemble.py` module
2. Implement generic two-pass framework:
   - Pass 1: Generate candidates from N strategies
   - Pass 2: Apply mathematical filter (Fibonacci, range balance, etc.)
   - Pass 3: Select with diversity constraints
3. Add as new strategy option in app.py: "Fibonacci-Filtered Ensemble"

---

### 2. Strategic Fusion Ensemble

**Source File:** `strategic_fusion_20_combinations.py` (lines 110-212)
**Value:** True ensemble method that intelligently combines elements from different strategies

#### Key Innovation

Unlike simple averaging, this pattern performs **structural fusion**:

- **Cross-Strategy Fusion:** Takes 2 numbers from Risk-Reward + 2 from Coverage + 1 from Markov
- **Mathematical Averaging:** Averages corresponding positions between combinations
- **Range-Balanced Fusion:** Ensures optimal distribution across low/mid/high ranges

#### Code Patterns

```python
def cross_strategy_fusion(analysis, num_fusions=3):
    """
    Create fusions by combining structural elements from different strategies.
    Not just averaging scores - actually takes specific numbers from each strategy.
    """
    risk_combos = analysis['risk_reward']
    coverage_combos = analysis['coverage']
    markov_combos = analysis['markov']

    fusions = []

    for i in range(num_fusions):
        fusion_numbers = []
        fusion_stars = []

        # Take 2 numbers from Risk-Reward strategy
        risk_combo = risk_combos[i % len(risk_combos)]
        fusion_numbers.extend(random.sample(risk_combo['numbers'], 2))

        # Take 2 numbers from Coverage strategy (avoid duplicates)
        coverage_combo = coverage_combos[i % len(coverage_combos)]
        coverage_available = [n for n in coverage_combo['numbers'] if n not in fusion_numbers]
        if len(coverage_available) >= 2:
            fusion_numbers.extend(random.sample(coverage_available, 2))

        # Take 1 number from Markov strategy (fill to 5)
        while len(fusion_numbers) < 5:
            markov_combo = markov_combos[i % len(markov_combos)]
            markov_available = [n for n in markov_combo['numbers'] if n not in fusion_numbers]
            if markov_available:
                fusion_numbers.append(random.choice(markov_available))
            else:
                break

        # Combine stars from different strategies
        fusion_stars = [risk_combo['stars'][0], coverage_combo['stars'][0]]
        if fusion_stars[0] == fusion_stars[1] and len(coverage_combo['stars']) > 1:
            fusion_stars[1] = coverage_combo['stars'][1]

        fusions.append({
            'numbers': sorted(fusion_numbers[:5]),
            'stars': sorted(fusion_stars),
            'strategy': f'Cross-Strategy Fusion {i+1}',
            'logic': f'2 Risk-Reward + 2 Coverage + 1 Markov numbers'
        })

    return fusions


def mathematical_averaging_fusion(combinations, num_fusions=2):
    """
    Create fusions using mathematical averaging of position-wise values.
    Averages the 1st number with 1st number, 2nd with 2nd, etc.
    """
    fusions = []
    high_priority = [c for c in combinations if c.get('priority', 999) <= 2]

    for i in range(num_fusions):
        # Select two combinations to average
        combo1 = high_priority[i * 2 % len(high_priority)]
        combo2 = high_priority[(i * 2 + 1) % len(high_priority)]

        # Average corresponding positions
        averaged_numbers = []
        for pos in range(5):
            if pos < len(combo1['numbers']) and pos < len(combo2['numbers']):
                avg = round((combo1['numbers'][pos] + combo2['numbers'][pos]) / 2)
                averaged_numbers.append(avg)

        # Remove duplicates and fill if needed
        averaged_numbers = list(dict.fromkeys(averaged_numbers))

        while len(averaged_numbers) < 5:
            all_nums = combo1['numbers'] + combo2['numbers']
            candidates = [n for n in all_nums if n not in averaged_numbers]
            if candidates:
                averaged_numbers.append(random.choice(candidates))
            else:
                break

        # Average stars (union)
        all_stars = combo1['stars'] + combo2['stars']
        averaged_stars = sorted(list(set(all_stars)))[:2]

        fusions.append({
            'numbers': sorted(averaged_numbers[:5]),
            'stars': averaged_stars,
            'strategy': f'Mathematical Averaging Fusion {i+1}',
            'logic': f'Position-wise average of combo {combo1["id"]} and {combo2["id"]}'
        })

    return fusions
```

#### How to Integrate

1. Add to `src/core/ensemble.py` module
2. Expose as "Ensemble Strategy" in app.py with sub-options:
   - Cross-Strategy Fusion (structural)
   - Mathematical Averaging (positional)
   - Frequency-Weighted (popularity-based)
3. Allow user to select which base strategies to combine

---

### 3. Jittered Exponential Backoff

**Source File:** `database_retry.py` (lines 25-100, 108-160)
**Value:** Production-grade database retry logic (better than current simple retry)

#### Key Innovation

Current `src/core/database.py` has basic retry. This pattern adds:

- **Exponential backoff:** 0.5s → 1s → 2s → 4s → 8s (up to 10s max)
- **Jittered delays:** Random ±10% to prevent thundering herd problem
- **Rate limit detection:** Specifically checks for "rate limit" or "too many connections" errors
- **Configurable parameters:** MIN_RETRY_DELAY, MAX_RETRY_DELAY, BACKOFF_FACTOR, JITTER

#### Code Pattern

```python
# Constants for exponential backoff
MIN_RETRY_DELAY = 0.5  # Starting delay of 0.5 seconds
MAX_RETRY_DELAY = 10   # Maximum delay of 10 seconds
BACKOFF_FACTOR = 2     # Multiply delay by this factor for each retry
JITTER = 0.1           # Add ±10% random jitter to avoid thundering herd


def create_db_engine(max_retries=5):
    """
    Create SQLAlchemy engine with jittered exponential backoff retry logic.
    """
    retries = 0
    retry_delay = MIN_RETRY_DELAY
    last_error = None

    while retries < max_retries:
        try:
            # Create engine with connection pooling
            engine = create_engine(
                DATABASE_URL,
                pool_size=3,
                max_overflow=5,
                pool_timeout=30,
                pool_recycle=1800,
                pool_pre_ping=True,
                poolclass=QueuePool,
                connect_args={'connect_timeout': 10}
            )

            # Test connection quickly
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            logger.info("Successfully connected to database")
            return engine, True

        except exc.OperationalError as e:
            last_error = e
            retries += 1

            # Check if this is a rate limit error
            if "rate limit" in str(e).lower() or "too many connections" in str(e).lower():
                logger.warning(f"Rate limit hit (attempt {retries}/{max_retries})")
            else:
                logger.warning(f"Database connection error (attempt {retries}/{max_retries})")

            # Only retry if we haven't hit max retries
            if retries < max_retries:
                # Calculate jittered exponential backoff
                jitter_amount = random.uniform(-JITTER, JITTER) * retry_delay
                actual_delay = retry_delay + jitter_amount
                logger.info(f"Retrying in {actual_delay:.2f} seconds...")
                time.sleep(actual_delay)

                # Exponential backoff (double each time, up to MAX_RETRY_DELAY)
                retry_delay = min(retry_delay * BACKOFF_FACTOR, MAX_RETRY_DELAY)

    # If all retries failed, create SQLite in-memory fallback
    logger.error(f"Failed after {retries} attempts: {str(last_error)}")
    logger.warning("Creating SQLite in-memory database for offline mode")
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
    return engine, False
```

#### How to Integrate

1. **Replace retry logic in `src/core/database.py`**:
   - Current: Simple try/except with fixed delays
   - New: Exponential backoff with jitter
2. **Add constants at top of file:**
   ```python
   MIN_RETRY_DELAY = 0.5
   MAX_RETRY_DELAY = 10
   BACKOFF_FACTOR = 2
   JITTER = 0.1
   ```
3. **Update `get_db_connection()` and `get_session()` functions**

---

### 4. Enhanced Data Processor

**Source File:** `data_processor.py` (lines 39-88)
**Value:** Robust CSV parsing that handles multiple formats automatically

#### Key Innovation

Current app assumes specific CSV column names. This pattern:

- **Auto-detects format:** Checks for multiple column name variants
- **Handles date variations:** 'date', 'draw_date', 'drawdate', 'date_of_draw'
- **Handles number variations:** 'n1-n5', 'number1-5', 'num1-5', 'ball1-5'
- **Handles star variations:** 's1-s2', 'star1-2', 'lucky_star1-2', 'ls1-2'
- **Graceful fallback:** If format unrecognized, attempts best-guess extraction

#### Code Pattern

```python
def identify_data_format(self, df):
    """
    Identify CSV format by checking for column name variants.
    Robust to different naming conventions.
    """
    # Define all known column name variants
    date_variants = ['date', 'draw_date', 'drawdate', 'date_of_draw']

    number_variants = [
        ['n1', 'n2', 'n3', 'n4', 'n5'],
        ['number1', 'number2', 'number3', 'number4', 'number5'],
        ['num1', 'num2', 'num3', 'num4', 'num5'],
        ['ball1', 'ball2', 'ball3', 'ball4', 'ball5']
    ]

    star_variants = [
        ['s1', 's2'],
        ['star1', 'star2'],
        ['lucky_star1', 'lucky_star2'],
        ['ls1', 'ls2']
    ]

    # Check for date column
    date_col = None
    for variant in date_variants:
        if variant in df.columns:
            date_col = variant
            break

    # Check for number columns
    number_cols = None
    for variant in number_variants:
        if all(col in df.columns for col in variant):
            number_cols = variant
            break

    # Check for star columns
    star_cols = None
    for variant in star_variants:
        if all(col in df.columns for col in variant):
            star_cols = variant
            break

    # Return identified columns or None if unrecognized
    if date_col and number_cols and star_cols:
        return {
            'format': 'standard',
            'date_col': date_col,
            'number_cols': number_cols,
            'star_cols': star_cols
        }
    else:
        return {'format': 'unknown'}


def process_standard_format(self, df, format_info):
    """
    Process CSV using identified column mappings.
    Standardizes to internal format (date, n1-n5, s1-s2).
    """
    # Extract identified columns
    date_col = format_info['date_col']
    number_cols = format_info['number_cols']
    star_cols = format_info['star_cols']

    # Create standardized DataFrame
    processed = pd.DataFrame()

    # Process date
    dates = pd.to_datetime(df[date_col])
    processed['date'] = dates.apply(lambda x: x.date())
    processed['day_of_week'] = dates.dt.day_name()

    # Process numbers (rename to n1-n5)
    for i, col in enumerate(number_cols):
        processed[f'n{i+1}'] = df[col].astype(int)

    # Process stars (rename to s1-s2)
    for i, col in enumerate(star_cols):
        processed[f's{i+1}'] = df[col].astype(int)

    # Sort by date descending
    processed = processed.sort_values('date', ascending=False).reset_index(drop=True)

    return processed
```

#### How to Integrate

1. **Create `src/utils/data_import.py`** with this logic
2. **Use in FDJ API import and CSV upload features:**
   ```python
   from src.utils.data_import import identify_data_format, process_standard_format

   # When loading CSV
   format_info = identify_data_format(raw_df)
   if format_info['format'] == 'standard':
       processed_df = process_standard_format(raw_df, format_info)
   else:
       # Show error or attempt custom parsing
   ```
3. **Benefits:** Users can upload CSVs with any common column naming

---

### 5. Failure Analysis Framework

**Source File:** `failure_analysis_and_improved_strategy.py` (lines 10-105)
**Value:** Meta-learning system to evaluate and improve strategies

#### Key Innovation

Current app generates predictions but doesn't systematically analyze failures. This pattern:

- **Decomposes failures across dimensions:** Overused numbers, missing numbers, range distribution, star patterns
- **Provides actionable insights:** Specific numbers that were overused, ranges that were underrepresented
- **Enables strategy improvement loop:** Use failure analysis to refine future predictions

#### Code Pattern

```python
def analyze_prediction_failures(our_combinations, winning_numbers, winning_stars):
    """
    Systematic failure analysis across multiple dimensions.
    Returns actionable insights for strategy improvement.
    """
    print("=== FAILURE ANALYSIS: What Went Wrong ===\n")

    # Extract all numbers/stars from our combinations
    all_our_numbers = []
    all_our_stars = []
    for combo in our_combinations:
        all_our_numbers.extend(combo['numbers'])
        all_our_stars.extend(combo['stars'])

    number_freq = Counter(all_our_numbers)
    star_freq = Counter(all_our_stars)

    # 1. OVERUSED NUMBERS (appeared too many times)
    print("1. OVERUSED NUMBERS (appeared in multiple combinations):")
    overused_numbers = {num: count for num, count in number_freq.items() if count > 2}
    for num, count in sorted(overused_numbers.items(), key=lambda x: x[1], reverse=True):
        won = "✓ WON" if num in winning_numbers else "✗ LOST"
        print(f"   Number {num}: used {count} times - {won}")

    # 2. MISSING WINNING NUMBERS
    print(f"\n2. MISSING WINNING NUMBERS:")
    missing_numbers = set(winning_numbers) - set(all_our_numbers)
    for num in sorted(missing_numbers):
        print(f"   Number {num}: COMPLETELY MISSED - appeared in 0 combinations")

    # 3. STAR ANALYSIS
    print(f"\n3. STAR ANALYSIS:")
    for star in winning_stars:
        if star in all_our_stars:
            count = star_freq[star]
            print(f"   Star {star}: used {count} times - ✓ WON")
        else:
            print(f"   Star {star}: COMPLETELY MISSED")

    # 4. RANGE DISTRIBUTION ANALYSIS
    print(f"\n4. RANGE DISTRIBUTION ANALYSIS:")
    winning_ranges = {
        "1-10": sum(1 for n in winning_numbers if 1 <= n <= 10),
        "11-20": sum(1 for n in winning_numbers if 11 <= n <= 20),
        "21-30": sum(1 for n in winning_numbers if 21 <= n <= 30),
        "31-40": sum(1 for n in winning_numbers if 31 <= n <= 40),
        "41-50": sum(1 for n in winning_numbers if 41 <= n <= 50)
    }

    our_ranges = {
        "1-10": sum(1 for n in all_our_numbers if 1 <= n <= 10),
        "11-20": sum(1 for n in all_our_numbers if 11 <= n <= 20),
        "21-30": sum(1 for n in all_our_numbers if 21 <= n <= 30),
        "31-40": sum(1 for n in all_our_numbers if 31 <= n <= 40),
        "41-50": sum(1 for n in all_our_numbers if 41 <= n <= 50)
    }

    print("   Winning vs Our Range Distribution:")
    for range_name in winning_ranges:
        win_count = winning_ranges[range_name]
        our_count = our_ranges[range_name]
        match = '✓' if our_count >= win_count else '✗'
        print(f"   {range_name}: Winning={win_count}, Ours={our_count} ({match})")

    # Return structured analysis
    return {
        'overused_numbers': overused_numbers,
        'missing_numbers': missing_numbers,
        'underrepresented_ranges': [
            r for r in winning_ranges
            if our_ranges[r] < winning_ranges[r]
        ],
        'star_coverage': {
            'hits': [s for s in winning_stars if s in all_our_stars],
            'misses': [s for s in winning_stars if s not in all_our_stars]
        }
    }
```

#### How to Integrate

1. **Create `src/utils/evaluation.py`** module with this framework
2. **Add "Evaluate Past Predictions" feature in app.py:**
   - User uploads: their combinations + actual winning numbers
   - System runs failure analysis
   - Displays insights: overused numbers, missing patterns, range gaps
3. **Use for strategy tuning:** Feed insights back into strategy weights/parameters

---

## Medium-Priority Patterns

### 6. Plotly Visualizations

**Source File:** `visualization.py` (lines 120-150)
**Value:** Interactive visualizations using Plotly (current app has minimal visualization)

#### Pattern: Number Pairs Heatmap

```python
import plotly.graph_objects as go
import numpy as np

def plot_number_pairs_heatmap(pairs_data):
    """
    Create interactive heatmap showing frequency of number pairs.

    Args:
        pairs_data: dict of {(num1, num2): frequency}

    Returns:
        Plotly figure object
    """
    # Create 50x50 matrix
    matrix = np.zeros((50, 50))

    for (i, j), freq in pairs_data.items():
        # Convert frequency to percentage
        matrix[i-1, j-1] = freq * 100
        # Mirror for symmetry (if (5, 12) appears, so should (12, 5))
        matrix[j-1, i-1] = freq * 100

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=list(range(1, 51)),
        y=list(range(1, 51)),
        colorscale='YlOrRd',
        hoverongaps=False,
        hovertemplate='Numbers: %{y} & %{x}<br>Frequency: %{z:.1f}%<extra></extra>'
    ))

    fig.update_layout(
        title='Number Pair Frequency Heatmap',
        xaxis_title='Number',
        yaxis_title='Number',
        width=800,
        height=800
    )

    return fig
```

#### How to Integrate

Add to app.py visualization section with `st.plotly_chart(fig)`.

---

### 7. Markov Multi-Level Transitions

**Source File:** `complete_markov_chain_2.py` (lines 35-68)
**Value:** More sophisticated Markov model than current basic version

#### Pattern: Multi-Dimensional Transition Tracking

```python
from collections import defaultdict, Counter

def build_markov_transitions(historical_data):
    """
    Build multi-level Markov transitions.

    Tracks:
    - Direct transitions: number -> next number in same draw
    - Position transitions: number at position i -> number at position i+2
    - Combination transitions: (num1, num2) -> num3
    """
    direct_transitions = defaultdict(Counter)
    position_transitions = defaultdict(Counter)
    combination_transitions = defaultdict(Counter)

    for draw in historical_data:
        numbers = draw['numbers']  # Already sorted

        # Direct transitions (consecutive numbers in sorted order)
        for i in range(len(numbers) - 1):
            direct_transitions[numbers[i]][numbers[i+1]] += 1

        # Position transitions (2 positions apart)
        for i in range(len(numbers) - 2):
            position_transitions[numbers[i]][numbers[i+2]] += 1

        # Combination transitions (pairs -> third number)
        for i in range(len(numbers) - 2):
            pair = (numbers[i], numbers[i+1])
            combination_transitions[pair][numbers[i+2]] += 1

    return {
        'direct': direct_transitions,
        'position': position_transitions,
        'combination': combination_transitions
    }


def score_number_with_markov(number, existing_numbers, transitions):
    """
    Score a candidate number based on multi-level Markov transitions.
    """
    score = 0

    # Check direct transitions from existing numbers
    for existing in existing_numbers:
        if number in transitions['direct'][existing]:
            score += transitions['direct'][existing][number] * 2.0

    # Check position transitions
    for existing in existing_numbers:
        if number in transitions['position'][existing]:
            score += transitions['position'][existing][number] * 1.5

    # Check combination transitions (if we have 2+ numbers)
    if len(existing_numbers) >= 2:
        for i in range(len(existing_numbers) - 1):
            pair = (existing_numbers[i], existing_numbers[i+1])
            if number in transitions['combination'][pair]:
                score += transitions['combination'][pair][number] * 3.0

    return score
```

#### How to Integrate

Upgrade `src/core/models.py` MarkovModel class with multi-level transitions.

---

## Low-Priority Patterns

### 8. Batch Import with Date Filtering

**Source File:** `import_nouveau_loto_by_date.py` (lines 50-84)
**Value:** Prevents database timeouts during large imports

```python
def import_csv_in_batches(filename, batch_size=25, start_date=None, end_date=None):
    """
    Import CSV in date-filtered batches to prevent timeouts.
    """
    parsed_start = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    parsed_end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    batch = []
    total_imported = 0

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Parse and filter by date
            record_date = datetime.strptime(row['date'], '%Y-%m-%d')

            if parsed_start and record_date < parsed_start:
                continue
            if parsed_end and record_date > parsed_end:
                continue

            batch.append(row)

            # Process batch when it reaches size limit
            if len(batch) >= batch_size:
                insert_batch_to_db(batch)
                total_imported += len(batch)
                logger.info(f"Imported {total_imported} records...")
                batch = []

        # Process remaining records
        if batch:
            insert_batch_to_db(batch)
            total_imported += len(batch)

    return total_imported
```

---

### 9. Locale Utilities

**Source File:** `import_nouveau_loto_by_date.py` (lines 18-48)
**Value:** French locale support (if internationalization is planned)

```python
# French date conversion
def convert_french_date(date_str):
    """Convert French DD/MM/YYYY to ISO YYYY-MM-DD"""
    day, month, year = date_str.strip().split('/')
    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

# French day name mapping
DAY_MAPPING = {
    'LUNDI': 'Monday',
    'MARDI': 'Tuesday',
    'MERCREDI': 'Wednesday',
    'JEUDI': 'Thursday',
    'VENDREDI': 'Friday',
    'SAMEDI': 'Saturday',
    'DIMANCHE': 'Sunday'
}

def translate_french_day(french_day):
    """Translate French day name to English"""
    return DAY_MAPPING.get(french_day.upper(), french_day)
```

---

## Summary Table

| Pattern | Source File | Priority | Effort | Impact |
|---------|-------------|----------|--------|--------|
| Fibonacci-Filtered Hybrid | fibonacci_hybrid_strategy.py | High | Medium | High |
| Strategic Fusion Ensemble | strategic_fusion_20_combinations.py | High | Medium | High |
| Jittered Exponential Backoff | database_retry.py | High | Low | High |
| Enhanced Data Processor | data_processor.py | High | Low | Medium |
| Failure Analysis Framework | failure_analysis_and_improved_strategy.py | High | Medium | High |
| Plotly Visualizations | visualization.py | Medium | Low | Medium |
| Markov Multi-Level Transitions | complete_markov_chain_2.py | Medium | Medium | Medium |
| Batch Import with Date Filter | import_nouveau_loto_by_date.py | Low | Low | Low |
| Locale Utilities | import_nouveau_loto_by_date.py | Low | Low | Low |

---

## Implementation Roadmap

### Phase 1: Quick Wins (1-2 hours)
1. ✅ Replace database retry logic with jittered exponential backoff
2. ✅ Add enhanced data processor for CSV imports

### Phase 2: Core Features (4-6 hours)
3. ⬜ Implement Fibonacci-Filtered Hybrid strategy
4. ⬜ Implement Strategic Fusion Ensemble
5. ⬜ Add Failure Analysis Framework (evaluation module)

### Phase 3: Enhancements (2-4 hours)
6. ⬜ Add Plotly visualizations
7. ⬜ Upgrade Markov model with multi-level transitions

### Phase 4: Polish (optional)
8. ⬜ Batch import utilities
9. ⬜ Locale support

---

## Files Analyzed

**Total root-level files:** 124
**Core files (kept):** 3 (app.py, update_latest_draws.py, utils.py)
**Analyzed for extraction:** 121
**Files with valuable patterns:** 8-10 (~6.6% contain unique value)

**Categories analyzed:**
- Import/Data scripts (18 files)
- Backtest scripts (11 files)
- Date-specific combinations (24 files)
- Strategy experiments (19 files)
- Database maintenance (10 files)
- Quick tests/debug (11 files)
- Analysis scripts (5 files)
- Data processing (7 files)
- Utilities (8 files)
- Uncertain/review (8 files)

**Conclusion:** Vast majority are one-off development scripts. Only ~10 files contain genuinely innovative patterns worth preserving. The rest can be safely archived.

---

**Document Version:** 1.0
**Last Updated:** 2026-01-03
**Next Review:** After Phase 1-2 implementation
