# Archive Index - Round 2 Cleanup

**Date:** 2026-01-03
**Total Files Archived:** 121
**Files Remaining in Root:** 3 (app.py, utils.py, update_latest_draws.py)
**Reduction:** 124 → 3 files (97.6% reduction)

---

## Overview

This archive contains 121 Python files removed from the root directory during the Round 2 cleanup. These files were identified as one-off development scripts, experiments, and utilities that are no longer actively used by the main application.

**Key Preservation:**
- **Valuable code patterns** extracted to `/docs/EXTRACTED_CODE_ROUND2.md`
- **All files preserved** in git history (tag: pre-round2-cleanup)
- **Categorized organization** for easy retrieval

---

## Archive Categories

### 1. Import/Data Scripts (19 files)
**Location:** `archive/round2_import_data/`
**Purpose:** One-off data import scripts for historical lottery data

**Files:**
- `import_loto_201902.py` - Import 2019-02 historical data
- `import_loto_201911_historical.py` - Import 2019-11 historical data
- `import_loto2017.py` - Import 2017 historical data
- `import_loto2017_sqlalchemy.py` - SQLAlchemy version of 2017 import
- `import_from_csv.py` - Generic CSV importer
- `import_old_loto.py` - Legacy loto format importer
- `import_nouveau_loto.py` - New loto format importer
- `import_nouveau_loto_by_date.py` - Date-filtered import (contains valuable batch import pattern)
- `import_loto_data.py` - Generic data importer
- `import_all_french_loto.py` - Bulk French Loto import
- `import_latest_loto_data.py` - Latest data import
- `import_french_loto.py` - French Loto CSV import
- `import_dump_data.py` - Database dump import
- `import_processed_data.py` - Processed data import
- `import_sample.py` - Sample data import
- `continue_import_loto.py` - Continued import session
- `continue_import_loto_smaller_batches.py` - Batched import to avoid timeouts
- `load_data_to_db.py` - Data loading utility
- `load_single_file.py` - Single file loader

**Valuable Patterns:**
- ✅ Batch import with date filtering (`import_nouveau_loto_by_date.py`) - **Extracted**
- ✅ French date conversion utilities - **Extracted**

---

### 2. Backtest Scripts (12 files)
**Location:** `archive/round2_backtest/`
**Purpose:** Strategy backtesting scripts for historical validation

**Files:**
- `backtest_fibonacci_hybrid_strategy.py` - Fibonacci hybrid strategy backtest
- `backtest_june_10_euromillions.py` - June 10 specific backtest
- `backtest_optimized_strategy.py` - Optimized strategy backtest
- `comprehensive_strategy_backtest.py` - Comprehensive multi-strategy backtest
- `comprehensive_french_loto_backtest.py` - French Loto comprehensive backtest
- `french_loto_lucky_strategy_backtest.py` - Lucky number strategy backtest
- `french_loto_backtest.py` - Basic French Loto backtest
- `full_historical_backtest.py` - Full historical validation
- `quick_backtest_hybrid.py` - Quick hybrid strategy test
- `quick_french_loto_backtest.py` - Quick French Loto test
- `separate_star_strategy_backtest.py` - Star-specific strategy backtest
- `strategy_backtest.py` - Generic strategy backtester

**Valuable Patterns:**
- None - all contain similar backtesting logic already in app

---

### 3. Analysis Scripts (7 files)
**Location:** `archive/round2_analysis/`
**Purpose:** Result analysis and performance evaluation scripts

**Files:**
- `may13_analysis.py` - May 13, 2025 results analysis
- `may9_results_analysis.py` - May 9, 2025 results analysis
- `quick_july_15_analysis.py` - July 15 quick analysis
- `quick_june_6_analysis.py` - June 6 quick analysis
- `strategy_improvement_analysis.py` - Strategy performance evaluation
- `investigate_database_discrepancy.py` - Database debugging
- `failure_analysis_and_improved_strategy.py` - Systematic failure analysis framework

**Valuable Patterns:**
- ✅ **Failure Analysis Framework** (`failure_analysis_and_improved_strategy.py`) - **Extracted**
  - Systematic post-mortem analysis
  - Overused numbers detection
  - Missing patterns identification
  - Range distribution comparison

---

### 4. Date-Specific Combinations (24 files)
**Location:** `archive/round2_combinations/`
**Purpose:** One-off combination generation for specific draws

**Files:**

**May 2025 combinations:**
- `may6_optimized_strategy.py`
- `may9_optimized_combinations.py`
- `ultimate_may6_combinations.py`
- `additional_may9_combinations.py`
- `complete_may23_optimized_set.py`
- `balanced_strategy_may13.py`
- `improved_strategy_may13.py`
- `optimized_may13_combinations.py`
- `direct_may13_combinations.py`

**June 2025 combinations:**
- `create_june_24_single_fusion.py`
- `create_june_25_french_loto_fusion.py`

**Strategy fusion experiments:**
- `strategic_fusion_20_combinations.py` - **Contains valuable fusion patterns**
- `time_series_strategy_combinations.py`
- `mixed_french_loto_combinations.py`
- `mathematical_fusion_combinations.py`
- `improved_french_loto_combinations.py`

**Other generation:**
- `next_draw_10_combinations.py`
- `quick_fresh_combinations.py`
- `quick_may24_adapted_combinations.py`

**39-combination experiments:**
- `final_corrected_39_unique.py`
- `corrected_39_unique_combinations.py`
- `regenerate_correct_ultimate_39.py`
- `show_39_unique_ultimate_combinations.py`
- `finalize_corrected_ultimate_39.py`

**Valuable Patterns:**
- ✅ **Strategic Fusion Ensemble** (`strategic_fusion_20_combinations.py`) - **Extracted**
  - Cross-strategy fusion (2 Risk-Reward + 2 Coverage + 1 Markov)
  - Mathematical averaging fusion
  - Frequency-weighted fusion
  - Range-balanced fusion

---

### 5. Database Maintenance (10 files)
**Location:** `archive/round2_database_maintenance/`
**Purpose:** Database cleanup and maintenance scripts

**Files:**
- `check_database_structure.py` - Schema validation
- `check_real_database.py` - Production database check
- `clear_french_loto_table.py` - Clear French Loto table
- `clear_and_reload_database.py` - Full database reload
- `migrate_french_loto_table.py` - Schema migration
- `clean_future_dates.py` - Remove future-dated records
- `remove_duplicate_loto_drawings.py` - Deduplication utility
- `export_database.py` - Database export tool
- `init_database.py` - Database initialization
- `database_retry.py` - **Contains valuable retry logic**

**Valuable Patterns:**
- ✅ **Jittered Exponential Backoff** (`database_retry.py`) - **Extracted**
  - Production-grade retry logic
  - Exponential backoff with jitter
  - Rate limit detection
  - SQLite fallback

---

### 6. Quick Tests/Debug (11 files)
**Location:** `archive/round2_quick_tests/`
**Purpose:** Quick experiments and debugging scripts

**Files:**
- `test_app.py` - App testing
- `test_hybrid_generation.py` - Hybrid strategy testing
- `simple_strategy_test.py` - Simple strategy validation
- `simple_fibonacci_test.py` - Fibonacci strategy test
- `simple_backtest_june_10.py` - June 10 quick backtest
- `simple_french_loto_data.py` - French Loto data test
- `simple_fibonacci_app.py` - Simplified Fibonacci app
- `quick_lucky_strategy_test.py` - Lucky number strategy test
- `debug_risk_reward.py` - Risk/reward debugging
- `validate_ultimate_strategy_generation.py` - Ultimate strategy validation
- `verify_and_fix_ultimate_39.py` - 39-combination verification

**Valuable Patterns:**
- None - all are simple test scripts

---

### 7. Strategy Experiments (20 files)
**Location:** `archive/round2_strategy_experiments/`
**Purpose:** Experimental strategy development and testing

**Fibonacci strategies:**
- `fibonacci_hybrid_strategy.py` - **Contains valuable 2-pass filtering**
- `fibonacci_hybrid_french_loto.py`
- `fibonacci_enhanced_strategy.py`
- `fibonacci_lottery_research.py`
- `quick_fibonacci_hybrid_french_loto.py`
- `create_simple_fibonacci_display.py`

**Enhanced/Improved strategies:**
- `enhanced_strategy.py`
- `improved_strategy.py`
- `improved_next_draw_combinations.py`

**Ultimate strategies:**
- `ultimate_euromillions_strategy_june_6.py`

**French Loto experiments:**
- `french_loto_strategy_testing.py`
- `french_loto_strategy_update.py`
- `french_loto_optimized.py`
- `french_loto_double_lucky.py`

**Other experiments:**
- `diverse_mixed_strategies.py`
- `strategy_testing.py`
- `add_fibonacci_to_app.py`
- `add_hybrid_strategy_to_app.py`
- `regenerate_optimized_star_combinations.py`
- `optimized_star_combinations_final.py`

**Valuable Patterns:**
- ✅ **Fibonacci-Filtered Hybrid** (`fibonacci_hybrid_strategy.py`) - **Extracted**
  - Two-pass approach: generate → filter → score
  - Fibonacci mathematical filtering
  - Diversity enforcement (max number/strategy reuse)
  - Meta-strategy framework

---

### 8. Data Processing (8 files)
**Location:** `archive/round2_data_processing/`
**Purpose:** Data conversion and preprocessing utilities

**Files:**
- `data_converter.py` - Generic data converter
- `data_processor.py` - **Contains valuable format detection**
- `french_csv_converter.py` - French CSV format converter
- `process_french_csv.py` - French CSV processor
- `process_french_loto.py` - French Loto data processor
- `extract_and_load.py` - ETL pipeline
- `direct_import.py` - Direct database import
- `old_loto_importer.py` - Legacy loto importer

**Valuable Patterns:**
- ✅ **Enhanced Data Processor** (`data_processor.py`) - **Extracted**
  - Auto-detects CSV format (multiple column name variants)
  - Handles date/number/star variations
  - Graceful fallback for unrecognized formats

---

### 9. Utilities (7 files)
**Location:** `archive/round2_utilities/`
**Purpose:** Miscellaneous utility scripts

**Files:**
- `fetch_recent_euromillions.py` - Fetch latest Euromillions results
- `scrape_recent_results.py` - Web scraping utility
- `view_combinations.py` - Combination viewer
- `save_may6_combinations.py` - Save combinations to database
- `visualization.py` - **Contains Plotly visualizations**
- `push_to_github.py` - GitHub deployment utility
- `french_loto_visualization.py` - French Loto charts

**Valuable Patterns:**
- ✅ **Plotly Visualizations** (`visualization.py`) - **Extracted**
  - Number pairs heatmap
  - Interactive frequency charts

---

### 10. Miscellaneous (3 files)
**Location:** `archive/round2_misc/`
**Purpose:** Uncategorized scripts

**Files:**
- `bonus_combination.py` - Bonus combination logic
- `complete_combination_overview.py` - Combination overview generator
- `complete_markov_chain_2.py` - **Contains multi-level Markov transitions**

**Valuable Patterns:**
- ✅ **Markov Multi-Level Transitions** (`complete_markov_chain_2.py`) - **Extracted**
  - Direct transitions (number → next number)
  - Position transitions (number at i → number at i+2)
  - Combination transitions ((num1, num2) → num3)

---

## Summary Statistics

| Category | Files | Valuable Patterns | Status |
|----------|-------|-------------------|--------|
| Import/Data | 19 | 1 | ✅ Archived |
| Backtest | 12 | 0 | ✅ Archived |
| Analysis | 7 | 1 | ✅ Archived |
| Combinations | 24 | 1 | ✅ Archived |
| DB Maintenance | 10 | 1 | ✅ Archived |
| Quick Tests | 11 | 0 | ✅ Archived |
| Strategy Experiments | 20 | 1 | ✅ Archived |
| Data Processing | 8 | 1 | ✅ Archived |
| Utilities | 7 | 1 | ✅ Archived |
| Miscellaneous | 3 | 1 | ✅ Archived |
| **TOTAL** | **121** | **8** | **✅ Complete** |

---

## Valuable Patterns Extracted

All valuable code patterns have been extracted to `/docs/EXTRACTED_CODE_ROUND2.md`:

1. **Fibonacci-Filtered Hybrid Strategy** (HIGH) - `fibonacci_hybrid_strategy.py`
2. **Strategic Fusion Ensemble** (HIGH) - `strategic_fusion_20_combinations.py`
3. **Jittered Exponential Backoff** (HIGH) - `database_retry.py`
4. **Enhanced Data Processor** (HIGH) - `data_processor.py`
5. **Failure Analysis Framework** (HIGH) - `failure_analysis_and_improved_strategy.py`
6. **Plotly Visualizations** (MEDIUM) - `visualization.py`
7. **Markov Multi-Level Transitions** (MEDIUM) - `complete_markov_chain_2.py`
8. **Batch Import with Date Filter** (LOW) - `import_nouveau_loto_by_date.py`

---

## How to Retrieve Archived Files

### Restore Single File
```bash
# Example: Restore fibonacci_hybrid_strategy.py
cp archive/round2_strategy_experiments/fibonacci_hybrid_strategy.py .
```

### Restore Entire Category
```bash
# Example: Restore all backtest scripts
cp archive/round2_backtest/*.py .
```

### Search for Specific Pattern
```bash
# Example: Find files containing "fibonacci"
find archive/round2_* -name "*fibonacci*.py"
```

---

## Git History

All archived files remain in git history and can be restored via:

```bash
# View file history
git log -- <filename>

# Restore from specific commit
git checkout <commit-hash> -- <filename>
```

---

## Related Documentation

- **Extracted Code Patterns:** `/docs/EXTRACTED_CODE_ROUND2.md`
- **Round 1 Archive:** `/archive/ARCHIVE_INDEX.md` (if exists)
- **Refactoring History:** `/docs/REFACTORING_HISTORY.md`

---

**Archive Created:** 2026-01-03
**Created By:** Claude Code (Automated Cleanup)
**Status:** Complete
**Next Review:** Only if archived patterns need to be re-integrated
