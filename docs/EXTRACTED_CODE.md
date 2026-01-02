# Extracted Code from Archived Files

**Last Updated:** 2026-01-02

This document preserves unique and potentially useful code extracted from files before they were archived during the codebase audit and refactoring initiative.

---

## Purpose

Many experimental and variant files contain valuable code that shouldn't be lost when archiving. This document serves as a reference for:
- Innovative algorithms or approaches
- UI improvements
- Performance optimizations
- Useful utility functions

The code snippets here can be integrated into the main codebase if needed.

---

## Extraction Guidelines

When extracting code, include:
1. **Source File:** Original filename and location
2. **Line Numbers:** Where the code was located
3. **Purpose:** What the code does
4. **Extraction Date:** When it was extracted
5. **Integration Notes:** How to integrate if needed
6. **Code Snippet:** The actual code

---

## Extracted Code Sections

### From app_with_cache.py

**Extraction Date:** 2026-01-02
**Source File:** `app_with_cache.py`
**Lines:** 36-145 (caching implementation)
**Purpose:** File-based caching system with 24-hour expiration for database queries

#### Caching Implementation

```python
import pickle
import os
import time
import logging

# Path for cached data
CACHE_DIR = "temp_data"
os.makedirs(CACHE_DIR, exist_ok=True)

# Cache file paths
FRENCH_LOTO_CACHE = os.path.join(CACHE_DIR, "french_loto_cache.pkl")
EURO_CACHE = os.path.join(CACHE_DIR, "euromillions_cache.pkl")

# Cache expiration (24 hours in seconds)
CACHE_EXPIRY = 24 * 60 * 60

def is_cache_valid(cache_path):
    """Check if cache file exists and is not expired"""
    if not os.path.exists(cache_path):
        return False

    # Check file modification time
    mtime = os.path.getmtime(cache_path)
    cache_age = time.time() - mtime

    return cache_age < CACHE_EXPIRY

def load_cached_data(cache_path):
    """Load data from cache file"""
    try:
        with open(cache_path, 'rb') as f:
            data = pickle.load(f)
        logger.info(f"Loaded data from cache: {cache_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading cache: {str(e)}")
        return None

def save_to_cache(data, cache_path):
    """Save data to cache file"""
    try:
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)
        logger.info(f"Saved data to cache: {cache_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving cache: {str(e)}")
        return False

def load_french_loto_data():
    """Load French Loto data with caching and rate limit protection"""
    # Try to load from cache first
    if is_cache_valid(FRENCH_LOTO_CACHE):
        cached_data = load_cached_data(FRENCH_LOTO_CACHE)
        if cached_data is not None:
            return cached_data

    # If no valid cache, query database
    # ... database query code with retry logic ...

    # Save to cache for future use
    save_to_cache(df, FRENCH_LOTO_CACHE)

    return df
```

**Key Features:**
- 24-hour cache expiration
- Pickle-based serialization
- Rate limit protection for database
- Retry logic with jitter to avoid thundering herd
- Graceful fallback on errors

**Integration Notes:**
- Can be added to `src/utils/cache_utils.py`
- Useful for production deployments with connection limits
- Consider using `@st.cache_data` for Streamlit-specific caching instead
- Or use `functools.lru_cache` for simpler in-memory caching

**When to Use:**
- Production environments with database rate limits (like Replit)
- When data doesn't change frequently
- To reduce database load

---

### From app_with_fibonacci.py

**Extraction Date:** 2026-01-02
**Source File:** `app_with_fibonacci.py`
**Lines:** 495-501, 571-583
**Purpose:** Enhanced UI for Fibonacci strategy selection with variant chooser

#### Fibonacci Strategy UI Component

```python
# In strategy selection area (lines 495-501)
elif base_strategy_type == "Fibonacci Enhanced":
    fibonacci_variant = st.selectbox(
        "Fibonacci Strategy Type",
        ["Mixed", "Pure Fibonacci", "Reverted Fibonacci", "Hot Fibonacci"],
        help="Choose the type of Fibonacci strategy to use"
    )
    st.info("🔥 Fibonacci Enhanced uses mathematical sequences for prediction. "
            "Mixed approach recommended based on May 20 analysis showing 60% Fibonacci presence!")

# In combination generation (lines 571-583)
elif base_strategy_type == "Fibonacci Enhanced":
    # Use Fibonacci strategy module
    from fibonacci_strategy import generate_fibonacci_combinations, save_fibonacci_to_database

    combinations = generate_fibonacci_combinations(
        strategy_variant=fibonacci_variant,
        num_combinations=num_combinations
    )

    # Save to database
    success, result = save_fibonacci_to_database(combinations, engine)
    if success:
        st.success(f"✅ Saved {result} Fibonacci combinations to database!")
```

**Key Features:**
- Variant selection: Mixed, Pure, Reverted, Hot Fibonacci
- Integration with existing `fibonacci_strategy.py` module
- Database persistence of generated combinations
- User guidance based on historical analysis

**Integration Notes:**
- Add to main `app.py` in strategy selection section
- Requires `fibonacci_strategy.py` module (already exists in codebase)
- Works with existing Euromillions strategy interface
- Can be added as another strategy option in dropdown

**Current Status:**
- The main `app.py` may already have Fibonacci integration
- This shows the enhanced UI with variant selection
- Database save functionality is valuable for tracking

### From Strategy Experiment Files

*Extraction pending - Phase 3*

---

## Integration Checklist

Before integrating extracted code:
- [ ] Review for compatibility with current codebase
- [ ] Check for dependencies
- [ ] Add proper error handling
- [ ] Add docstrings and comments
- [ ] Add unit tests
- [ ] Test integration thoroughly
- [ ] Update relevant documentation

---

## Notes

- All extracted code is preserved here for future reference
- Original files are archived and accessible in archive/ directory
- Git history contains complete evolution of all code
- See REFACTORING_HISTORY.md for context on why files were archived
