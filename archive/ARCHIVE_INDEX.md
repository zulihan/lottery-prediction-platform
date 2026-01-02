# Archive Index - Lottery Prediction Platform

**Archive Date:** 2026-01-02
**Archived By:** Codebase Audit & Refactoring Initiative
**Total Files Archived:** ~200+

## Purpose

This archive contains code from the development phase of the lottery prediction platform (2024-2025). Files here were used for:
- One-time analysis of specific draws
- Experimental strategy implementations
- Date-specific combination generation
- Debugging and fixes
- Application prototypes and variants

They are preserved for historical reference but are not part of the active codebase.

## Archive Categories

### 1. App Variants (`archive/app_variants/`)
**Purpose:** Backup versions, experimental UI features, alternative implementations
**Files:** TBD
**Status:** Pending archival

### 2. Analysis Scripts (`archive/analysis_scripts/`)
**Purpose:** Date-specific draw analysis and performance evaluation
**Pattern:** `analyze_*_results.py`, `analyze_*_performance.py`
**Files:** TBD
**Status:** Pending archival

### 3. Generation Scripts (`archive/generation_scripts/`)
**Purpose:** One-time combination generation for specific draws
**Pattern:** `generate_*_combinations.py`, `create_*_combinations.py`
**Files:** TBD
**Status:** Pending archival

### 4. Strategy Experiments (`archive/strategy_experiments/`)
**Purpose:** Experimental strategy algorithms and variations
**Pattern:** `improved_strategy.py`, `enhanced_strategy.py`, etc.
**Files:** TBD
**Status:** Pending archival

### 5. Backtest Scripts (`archive/backtest_scripts/`)
**Purpose:** Historical validation scripts (some may be duplicates of tools/)
**Pattern:** `backtest_*.py`, `*_backtest.py`
**Files:** TBD
**Status:** Pending archival

### 6. Fixes and Corrections (`archive/fixes_and_corrections/`)
**Purpose:** One-time database fixes, data corrections, emergency patches
**Pattern:** `correct_*.py`, `fix_*.py`, `*_fix.py`
**Files:** TBD
**Status:** Pending archival

## How to Use This Archive

### Retrieving a File
```bash
# Copy from archive back to working directory
cp archive/[category]/[filename].py .

# Run if needed
python [filename].py
```

### Searching for Insights
Many analysis scripts contain valuable insights in code comments:
```bash
# Search for conclusions across analysis scripts
grep -r "insight\|conclusion\|finding\|result" archive/analysis_scripts/

# Search for specific draw date
grep -r "may.*20" archive/
```

### Restoration of Pre-Refactor State
If you need to restore the entire codebase to pre-refactoring state:
```bash
# Option 1: Git tag
git checkout pre-refactor-20260102

# Option 2: Backup archive
cd /Users/zu/_Dev
tar -xzf lottery-platform-backup-20260102.tar.gz
```

## Detailed File Listings

*Will be populated as files are archived during Phase 2-3*

## Notes
- All archived code is preserved in git history
- Database dumps from this period: `db_dump/`
- Unique code extracted from variants: `docs/EXTRACTED_CODE.md`
- This archive was created as part of comprehensive codebase cleanup
- See `docs/REFACTORING_HISTORY.md` for details on the refactoring process
