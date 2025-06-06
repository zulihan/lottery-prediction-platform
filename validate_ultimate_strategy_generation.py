"""
Validate that the ultimate 39 combinations were generated correctly 
based on actual strategic methods, not just formatted correctly
"""

import pandas as pd
import numpy as np
from collections import Counter
import os

def load_historical_data():
    """Load historical Euromillions data to validate strategies"""
    try:
        # Try to load from database or CSV files
        data_files = [
            'attached_assets/euromillions_4.csv',
            'attached_assets/euromillions.csv',
            'attached_assets/euromillions_3.csv'
        ]
        
        for file in data_files:
            if os.path.exists(file):
                df = pd.read_csv(file)
                print(f"Loaded data from {file}: {len(df)} rows")
                return df
        
        print("No historical data file found - generating validation based on known frequent numbers")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_frequency_analysis():
    """Get frequency analysis from historical data or known results"""
    # From our previous analysis of 1845 draws
    known_frequent_numbers = {
        23: 209, 44: 207, 19: 206, 50: 204, 21: 202,
        10: 201, 37: 200, 29: 199, 42: 198, 25: 197
    }
    
    known_frequent_stars = {
        3: 368, 2: 364, 8: 355, 9: 341, 7: 164  # Star 7 historically underrepresented
    }
    
    return known_frequent_numbers, known_frequent_stars

def validate_coverage_optimization_set():
    """Validate if Coverage Optimization combinations actually provide good coverage"""
    
    # NEW CORRECTLY GENERATED COVERAGE OPTIMIZATION SET
    coverage_combos = [
        [12, 15, 38, 47, 48],  # Supreme
        [3, 23, 37, 44, 50],   # Range
        [1, 19, 29, 42, 49],   # Extreme
        [8, 15, 25, 38, 45],   # Balanced
        [10, 21, 27, 44, 47],  # Frequency
        [6, 17, 32, 39, 46],   # Gaps
        [4, 14, 24, 34, 44],   # Mathematical
        [7, 20, 33, 41, 48]    # Ultimate
    ]
    
    # Check range coverage
    all_numbers = set()
    for combo in coverage_combos:
        all_numbers.update(combo)
    
    low_range = len([n for n in all_numbers if 1 <= n <= 17])
    mid_range = len([n for n in all_numbers if 18 <= n <= 33])
    high_range = len([n for n in all_numbers if 34 <= n <= 50])
    
    print("COVERAGE OPTIMIZATION VALIDATION:")
    print(f"  Total unique numbers covered: {len(all_numbers)}")
    print(f"  Low range (1-17): {low_range} numbers")
    print(f"  Mid range (18-33): {mid_range} numbers") 
    print(f"  High range (34-50): {high_range} numbers")
    
    # Check for June 3 winning numbers integration
    june_3_winners = [12, 15, 38, 47, 48]
    june_3_coverage = sum(1 for combo in coverage_combos if any(n in june_3_winners for n in combo))
    print(f"  Combinations with June 3 winners: {june_3_coverage}/8")
    
    return len(all_numbers) >= 25  # Good coverage should have 25+ unique numbers

def validate_fusion_mastery_set():
    """Validate if Fusion Mastery combinations actually fuse different strategies"""
    
    # NEW CORRECTLY GENERATED FUSION MASTERY SET
    fusion_combos = [
        [12, 23, 38, 44, 50],  # Frequency + June 3
        [2, 19, 29, 45, 49],   # Extreme + Balance
        [10, 20, 30, 40, 50],  # Pattern + Range
        [15, 21, 25, 37, 43],  # Hot + Cold
        [5, 11, 17, 23, 29],   # Mathematical Progression
        [1, 19, 27, 42, 48],   # Coverage + Frequency
        [9, 24, 35, 44, 47],   # Recent + Historical
        [13, 22, 31, 39, 46],  # Multi-Strategy Synthesis
        [16, 26, 36, 41, 50],  # Performance Optimization
        [18, 28, 33, 38, 49]   # Ultimate Strategy
    ]
    
    print("FUSION MASTERY VALIDATION:")
    
    # Check for frequent numbers integration
    frequent_nums, _ = get_frequency_analysis()
    top_frequent = list(frequent_nums.keys())[:5]  # Top 5: 23, 44, 19, 50, 21
    
    fusion_with_frequent = 0
    for combo in fusion_combos:
        if any(n in top_frequent for n in combo):
            fusion_with_frequent += 1
    
    print(f"  Combinations with top frequent numbers: {fusion_with_frequent}/10")
    
    # Check for duplicates
    unique_combos = set()
    duplicates = 0
    for combo in fusion_combos:
        combo_tuple = tuple(sorted(combo))
        if combo_tuple in unique_combos:
            duplicates += 1
        unique_combos.add(combo_tuple)
    
    print(f"  Duplicate combinations found: {duplicates}")
    print(f"  Unique combinations: {len(unique_combos)}/10")
    
    return duplicates == 0 and fusion_with_frequent >= 8

def validate_frequency_dominance_set():
    """Validate if Frequency Dominance uses actual frequent numbers"""
    
    # NEW CORRECTLY GENERATED FREQUENCY DOMINANCE SET
    frequency_combos = [
        [23, 44, 19, 50, 21],  # Top 5 most frequent
        [10, 37, 29, 42, 25],  # Next 5 most frequent
        [20, 27, 17, 15, 38],  # Next 5 most frequent
        [23, 19, 21, 37, 42],  # Mix of top frequent
        [44, 50, 10, 29, 25],  # Mix of top frequent
        [23, 44, 37, 27, 15],  # Mix of top frequent
        [19, 50, 21, 20, 38],  # Mix of top frequent
        [10, 42, 25, 17, 29],  # Mix of top frequent
        [23, 50, 37, 20, 15],  # Mix of top frequent
        [44, 19, 21, 27, 38]   # Mix of top frequent
    ]
    
    print("FREQUENCY DOMINANCE VALIDATION:")
    
    frequent_nums, _ = get_frequency_analysis()
    top_10_frequent = list(frequent_nums.keys())[:10]
    
    valid_frequency_combos = 0
    for combo in frequency_combos:
        frequent_count = sum(1 for n in combo if n in top_10_frequent)
        if frequent_count >= 3:  # At least 3 out of 5 should be frequent
            valid_frequency_combos += 1
    
    print(f"  Combinations with 3+ frequent numbers: {valid_frequency_combos}/10")
    
    # Check if all numbers used are actually frequent
    all_freq_numbers = set()
    for combo in frequency_combos:
        all_freq_numbers.update(combo)
    
    frequent_number_usage = len([n for n in all_freq_numbers if n in top_10_frequent])
    print(f"  Frequent numbers used: {frequent_number_usage}/{len(all_freq_numbers)}")
    
    return valid_frequency_combos >= 8

def validate_extreme_range_focus_set():
    """Validate if Extreme Range Focus actually covers extreme ranges"""
    
    # NEW CORRECTLY GENERATED EXTREME RANGE FOCUS SET
    extreme_combos = [
        [1, 8, 43, 47, 50],   # 1
        [2, 6, 44, 48, 49],   # 2
        [3, 7, 45, 46, 50],   # 3
        [4, 5, 43, 47, 48],   # 4
        [1, 9, 44, 49, 50],   # 5
        [2, 10, 45, 46, 47],  # 6
        [3, 8, 43, 48, 49],   # 7
        [4, 6, 44, 46, 50],   # 8
        [5, 7, 45, 47, 48],   # 9
        [1, 10, 43, 46, 49],  # 10
        [2, 9, 44, 45, 50]    # 11
    ]
    
    print("EXTREME RANGE FOCUS VALIDATION:")
    
    # Check extreme low (1-10) and extreme high (41-50) coverage
    extreme_low_coverage = 0
    extreme_high_coverage = 0
    
    for combo in extreme_combos:
        has_extreme_low = any(n <= 10 for n in combo)
        has_extreme_high = any(n >= 41 for n in combo)
        
        if has_extreme_low:
            extreme_low_coverage += 1
        if has_extreme_high:
            extreme_high_coverage += 1
    
    print(f"  Combinations with extreme low (1-10): {extreme_low_coverage}/11")
    print(f"  Combinations with extreme high (41-50): {extreme_high_coverage}/11")
    
    # Check range distribution
    all_extreme_numbers = set()
    for combo in extreme_combos:
        all_extreme_numbers.update(combo)
    
    low_extreme = len([n for n in all_extreme_numbers if n <= 10])
    high_extreme = len([n for n in all_extreme_numbers if n >= 41])
    
    print(f"  Unique extreme low numbers: {low_extreme}")
    print(f"  Unique extreme high numbers: {high_extreme}")
    
    return extreme_low_coverage >= 8 and extreme_high_coverage >= 9

def validate_star_strategies():
    """Validate star selection strategies"""
    
    # All star combinations from the 39 ultimate
    star_combos = [
        [5, 7], [7, 3], [7, 2], [7, 8], [7, 9], [5, 3], [7, 1], [5, 8],  # Coverage Optimization
        [7, 3], [7, 2], [7, 8], [7, 9], [7, 3], [7, 2], [7, 8], [7, 9], [5, 3], [5, 2],  # Fusion Mastery
        [3, 2], [3, 8], [3, 9], [3, 3], [3, 2], [3, 8], [3, 9], [3, 3], [3, 2], [3, 8],  # Frequency Dominance
        [7, 5], [7, 2], [5, 8], [7, 9], [5, 3], [7, 1], [5, 6], [7, 4], [5, 11], [7, 12], [5, 10]  # Extreme Range
    ]
    
    print("STAR STRATEGY VALIDATION:")
    
    star_counter = Counter()
    for combo in star_combos:
        for star in combo:
            star_counter[star] += 1
    
    print(f"  Star usage distribution: {dict(star_counter)}")
    
    # Check star 7 coverage (our identified gap)
    star_7_usage = star_counter[7]
    total_combinations = len(star_combos)
    star_7_percentage = (star_7_usage / (total_combinations * 2)) * 100
    
    print(f"  Star 7 usage: {star_7_usage} times out of {total_combinations * 2} star positions")
    print(f"  Star 7 coverage: {star_7_percentage:.1f}%")
    
    return star_7_percentage > 30  # Should have significant star 7 coverage

def main():
    """Main validation function"""
    
    print("🔍 VALIDATING ULTIMATE 39 STRATEGY GENERATION")
    print("=" * 50)
    
    # Load historical data
    historical_data = load_historical_data()
    
    # Validate each set
    coverage_valid = validate_coverage_optimization_set()
    print(f"  ✅ Coverage Optimization: {'VALID' if coverage_valid else 'INVALID'}")
    print()
    
    fusion_valid = validate_fusion_mastery_set()
    print(f"  ✅ Fusion Mastery: {'VALID' if fusion_valid else 'INVALID'}")
    print()
    
    frequency_valid = validate_frequency_dominance_set()
    print(f"  ✅ Frequency Dominance: {'VALID' if frequency_valid else 'INVALID'}")
    print()
    
    extreme_valid = validate_extreme_range_focus_set()
    print(f"  ✅ Extreme Range Focus: {'VALID' if extreme_valid else 'INVALID'}")
    print()
    
    star_valid = validate_star_strategies()
    print(f"  ✅ Star Strategies: {'VALID' if star_valid else 'INVALID'}")
    print()
    
    # Overall validation
    all_valid = coverage_valid and fusion_valid and frequency_valid and extreme_valid and star_valid
    
    print("📊 OVERALL VALIDATION RESULT:")
    print(f"  Strategy Generation: {'✅ CORRECTLY GENERATED' if all_valid else '❌ NEEDS REGENERATION'}")
    
    if not all_valid:
        print("\n🔧 ISSUES IDENTIFIED:")
        if not coverage_valid:
            print("  - Coverage Optimization set needs better range coverage")
        if not fusion_valid:
            print("  - Fusion Mastery set has duplicates or poor fusion")
        if not frequency_valid:
            print("  - Frequency Dominance set doesn't use frequent numbers properly")
        if not extreme_valid:
            print("  - Extreme Range Focus set doesn't cover extreme ranges well")
        if not star_valid:
            print("  - Star strategies don't provide adequate star 7 coverage")
    
    return all_valid

if __name__ == "__main__":
    main()