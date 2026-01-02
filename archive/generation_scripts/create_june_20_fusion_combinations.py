"""
Create 5 fusion combinations from the 5 June 20 Euromillions combinations
Using mathematical averaging, cross-strategy blending, and frequency weighting
"""

import psycopg2
import os
from collections import Counter
import random

def get_original_5_combinations():
    """Get the original 5 June 20 combinations"""
    
    combinations = [
        {'id': 1, 'numbers': [10, 19, 20, 27, 29], 'stars': [2, 8], 'strategy': 'Frequency + Range Balanced', 'score': 0.0506},
        {'id': 2, 'numbers': [7, 8, 17, 21, 40], 'stars': [6, 9], 'strategy': 'Coverage + Range Balanced', 'score': 0.0476},
        {'id': 3, 'numbers': [20, 21, 29, 32, 46], 'stars': [2, 8], 'strategy': 'Risk-Reward + Frequency Stars', 'score': 0.0461},
        {'id': 4, 'numbers': [10, 17, 34, 42, 45], 'stars': [1, 10], 'strategy': 'Frequency + Range Balanced V2', 'score': 0.0506},
        {'id': 5, 'numbers': [8, 16, 21, 32, 37], 'stars': [5, 7], 'strategy': 'Risk-Reward + Range Balanced', 'score': 0.0490},
    ]
    
    return combinations

def analyze_frequency_across_combinations(combinations):
    """Analyze frequency of numbers and stars across all combinations"""
    
    all_numbers = []
    all_stars = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    print("FREQUENCY ANALYSIS ACROSS 5 COMBINATIONS:")
    print("-" * 41)
    print("Most frequent numbers:")
    for num, freq in number_freq.most_common(10):
        print(f"  {num}: appears {freq} times")
    
    print("\nMost frequent stars:")
    for star, freq in star_freq.most_common():
        print(f"  {star}: appears {freq} times")
    print()
    
    return number_freq, star_freq

def create_fusion_1_mathematical_average(combinations):
    """Fusion 1: Mathematical Average of Most Frequent Elements"""
    
    # Get all numbers and their frequencies
    all_numbers = []
    all_stars = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Select top 5 most frequent numbers
    top_numbers = [n for n, freq in number_freq.most_common(5)]
    
    # Select top 2 most frequent stars
    top_stars = [s for s, freq in star_freq.most_common(2)]
    
    return {
        'numbers': sorted(top_numbers),
        'stars': sorted(top_stars),
        'method': 'Mathematical Average (Most Frequent)',
        'source': 'Top frequency across all 5 combinations'
    }

def create_fusion_2_weighted_by_performance(combinations):
    """Fusion 2: Weighted Average by Strategy Performance"""
    
    # Weight combinations by their expected scores
    weighted_numbers = Counter()
    weighted_stars = Counter()
    
    for combo in combinations:
        weight = combo['score']
        
        for num in combo['numbers']:
            weighted_numbers[num] += weight
        
        for star in combo['stars']:
            weighted_stars[star] += weight
    
    # Select top weighted elements
    top_weighted_numbers = [n for n, weight in weighted_numbers.most_common(5)]
    top_weighted_stars = [s for s, weight in weighted_stars.most_common(2)]
    
    return {
        'numbers': sorted(top_weighted_numbers),
        'stars': sorted(top_weighted_stars),
        'method': 'Weighted Average by Performance',
        'source': 'Performance-weighted fusion (scores: 0.0506, 0.0476, 0.0461, 0.0506, 0.0490)'
    }

def create_fusion_3_range_balanced(combinations):
    """Fusion 3: Range Balanced Fusion"""
    
    # Collect all numbers and group by ranges
    all_numbers = []
    all_stars = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Separate numbers by ranges
    low_numbers = [(n, freq) for n, freq in number_freq.items() if n <= 16]
    mid_numbers = [(n, freq) for n, freq in number_freq.items() if 17 <= n <= 32]
    high_numbers = [(n, freq) for n, freq in number_freq.items() if n >= 33]
    
    # Sort by frequency within each range
    low_numbers.sort(key=lambda x: x[1], reverse=True)
    mid_numbers.sort(key=lambda x: x[1], reverse=True)
    high_numbers.sort(key=lambda x: x[1], reverse=True)
    
    # Select 2 low, 2 mid, 1 high for balance
    selected_numbers = []
    
    if low_numbers:
        selected_numbers.extend([n for n, freq in low_numbers[:2]])
    
    if mid_numbers:
        selected_numbers.extend([n for n, freq in mid_numbers[:2]])
    
    if high_numbers:
        selected_numbers.append(high_numbers[0][0])
    
    # Fill remaining if needed
    while len(selected_numbers) < 5:
        all_available = [n for n, freq in number_freq.most_common() if n not in selected_numbers]
        if all_available:
            selected_numbers.append(all_available[0])
        else:
            break
    
    # Stars: one from each range (1-6, 7-12)
    low_stars = [s for s in star_freq.keys() if 1 <= s <= 6]
    high_stars = [s for s in star_freq.keys() if 7 <= s <= 12]
    
    selected_stars = []
    if low_stars:
        low_star_freq = [(s, star_freq[s]) for s in low_stars]
        low_star_freq.sort(key=lambda x: x[1], reverse=True)
        selected_stars.append(low_star_freq[0][0])
    
    if high_stars:
        high_star_freq = [(s, star_freq[s]) for s in high_stars]
        high_star_freq.sort(key=lambda x: x[1], reverse=True)
        selected_stars.append(high_star_freq[0][0])
    
    # If only one range available, get second most frequent
    while len(selected_stars) < 2:
        all_star_available = [s for s, freq in star_freq.most_common() if s not in selected_stars]
        if all_star_available:
            selected_stars.append(all_star_available[0])
        else:
            break
    
    return {
        'numbers': sorted(selected_numbers[:5]),
        'stars': sorted(selected_stars[:2]),
        'method': 'Range Balanced Fusion (2-2-1 + 1-6/7-12)',
        'source': 'Optimized range distribution'
    }

def create_fusion_4_cross_strategy_blend(combinations):
    """Fusion 4: Cross-Strategy Blend (Best from Each Strategy Type)"""
    
    # Group combinations by strategy type
    frequency_combos = [c for c in combinations if 'Frequency' in c['strategy']]
    coverage_combos = [c for c in combinations if 'Coverage' in c['strategy']]
    risk_reward_combos = [c for c in combinations if 'Risk-Reward' in c['strategy']]
    
    # Get numbers from each strategy type
    freq_numbers = []
    coverage_numbers = []
    risk_numbers = []
    
    for combo in frequency_combos:
        freq_numbers.extend(combo['numbers'])
    
    for combo in coverage_combos:
        coverage_numbers.extend(combo['numbers'])
    
    for combo in risk_reward_combos:
        risk_numbers.extend(combo['numbers'])
    
    # Select most frequent from each strategy
    freq_counter = Counter(freq_numbers)
    coverage_counter = Counter(coverage_numbers)
    risk_counter = Counter(risk_numbers)
    
    # Take 2 from frequency, 2 from risk-reward, 1 from coverage
    selected_numbers = []
    
    if freq_counter:
        top_freq = [n for n, count in freq_counter.most_common(3)]
        selected_numbers.extend(top_freq[:2])
    
    if risk_counter:
        top_risk = [n for n, count in risk_counter.most_common(3)]
        for num in top_risk:
            if num not in selected_numbers and len(selected_numbers) < 4:
                selected_numbers.append(num)
    
    if coverage_counter:
        top_coverage = [n for n, count in coverage_counter.most_common(2)]
        for num in top_coverage:
            if num not in selected_numbers and len(selected_numbers) < 5:
                selected_numbers.append(num)
    
    # Fill remaining if needed
    all_numbers = []
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
    
    all_counter = Counter(all_numbers)
    while len(selected_numbers) < 5:
        for num, count in all_counter.most_common():
            if num not in selected_numbers:
                selected_numbers.append(num)
                break
    
    # Stars: mix range balanced and frequency
    all_stars = []
    for combo in combinations:
        all_stars.extend(combo['stars'])
    
    star_counter = Counter(all_stars)
    selected_stars = [s for s, count in star_counter.most_common(2)]
    
    return {
        'numbers': sorted(selected_numbers[:5]),
        'stars': sorted(selected_stars),
        'method': 'Cross-Strategy Blend (2 Freq + 2 Risk + 1 Cov)',
        'source': 'Mixed strategy optimization'
    }

def create_fusion_5_complementary_selection(combinations):
    """Fusion 5: Complementary Selection (Least Overlapping)"""
    
    # Find numbers that appear less frequently (more unique)
    all_numbers = []
    all_stars = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Select numbers that appear only once or twice (unique selections)
    unique_numbers = [n for n, freq in number_freq.items() if freq <= 2]
    moderate_numbers = [n for n, freq in number_freq.items() if freq == 3]
    
    # Combine and ensure we have enough
    selection_pool = unique_numbers + moderate_numbers
    
    if len(selection_pool) < 5:
        # Add some frequent ones if needed
        frequent_numbers = [n for n, freq in number_freq.most_common()]
        for num in frequent_numbers:
            if num not in selection_pool and len(selection_pool) < 8:
                selection_pool.append(num)
    
    # Ensure range distribution
    selected_numbers = []
    low_available = [n for n in selection_pool if n <= 16]
    mid_available = [n for n in selection_pool if 17 <= n <= 32]
    high_available = [n for n in selection_pool if n >= 33]
    
    # Get at least one from each range if available
    if low_available:
        selected_numbers.append(low_available[0])
    if mid_available:
        selected_numbers.append(mid_available[0])
    if high_available:
        selected_numbers.append(high_available[0])
    
    # Fill remaining
    remaining_pool = [n for n in selection_pool if n not in selected_numbers]
    selected_numbers.extend(remaining_pool[:5-len(selected_numbers)])
    
    # Stars: least frequent for diversity
    unique_stars = [s for s, freq in star_freq.items() if freq == 1]
    if len(unique_stars) >= 2:
        selected_stars = sorted(unique_stars[:2])
    else:
        # Fall back to least frequent overall
        selected_stars = [s for s, freq in sorted(star_freq.items(), key=lambda x: x[1])[:2]]
    
    return {
        'numbers': sorted(selected_numbers[:5]),
        'stars': sorted(selected_stars),
        'method': 'Complementary Selection (Unique/Moderate Frequency)',
        'source': 'Diversified anti-overlap strategy'
    }

def validate_fusion_combinations(fusion_combinations):
    """Validate all fusion combinations"""
    
    print("FUSION COMBINATIONS VALIDATION:")
    print("-" * 31)
    
    valid_count = 0
    all_fusion_numbers = set()
    all_fusion_stars = set()
    
    for i, fusion in enumerate(fusion_combinations, 1):
        numbers = fusion['numbers']
        stars = fusion['stars']
        
        # Validate
        valid = True
        issues = []
        
        if len(numbers) != 5:
            valid = False
            issues.append(f"numbers={len(numbers)}")
        if len(stars) != 2:
            valid = False
            issues.append(f"stars={len(stars)}")
        if not all(1 <= n <= 49 for n in numbers):
            valid = False
            issues.append("number_range")
        if not all(1 <= s <= 12 for s in stars):
            valid = False
            issues.append("star_range")
        if len(set(numbers)) != 5:
            valid = False
            issues.append("duplicate_numbers")
        if len(set(stars)) != 2:
            valid = False
            issues.append("duplicate_stars")
        
        if valid:
            valid_count += 1
            all_fusion_numbers.update(numbers)
            all_fusion_stars.update(stars)
        
        status = "✓" if valid else f"✗ ({', '.join(issues)})"
        
        print(f"{i}. {fusion['method']}")
        print(f"   Numbers: {numbers} + Stars: {stars} {status}")
        print(f"   Source: {fusion['source']}")
        print()
    
    print(f"Valid fusion combinations: {valid_count}/5")
    print(f"Unique numbers in fusions: {len(all_fusion_numbers)}/49 ({len(all_fusion_numbers)/49*100:.1f}%)")
    print(f"Unique stars in fusions: {len(all_fusion_stars)}/12 ({len(all_fusion_stars)/12*100:.1f}%)")
    
    return fusion_combinations

def main():
    """Create 5 fusion combinations from the 5 June 20 combinations"""
    
    print("CREATING 5 FUSION COMBINATIONS FROM JUNE 20 COMBINATIONS")
    print("=" * 57)
    
    original_combinations = get_original_5_combinations()
    
    print("ANALYZING ORIGINAL 5 COMBINATIONS:")
    print("-" * 34)
    
    for combo in original_combinations:
        print(f"{combo['id']}. {combo['strategy']}: {combo['numbers']} + {combo['stars']}")
    print()
    
    number_freq, star_freq = analyze_frequency_across_combinations(original_combinations)
    
    print("CREATING FUSION COMBINATIONS:")
    print("-" * 29)
    
    fusion_combinations = []
    
    fusion_1 = create_fusion_1_mathematical_average(original_combinations)
    fusion_combinations.append(fusion_1)
    
    fusion_2 = create_fusion_2_weighted_by_performance(original_combinations)
    fusion_combinations.append(fusion_2)
    
    fusion_3 = create_fusion_3_range_balanced(original_combinations)
    fusion_combinations.append(fusion_3)
    
    fusion_4 = create_fusion_4_cross_strategy_blend(original_combinations)
    fusion_combinations.append(fusion_4)
    
    fusion_5 = create_fusion_5_complementary_selection(original_combinations)
    fusion_combinations.append(fusion_5)
    
    validate_fusion_combinations(fusion_combinations)
    
    print("\nFUSION METHODOLOGY SUMMARY:")
    print("1. Mathematical Average: Most frequent elements across all")
    print("2. Weighted by Performance: Weighted by strategy scores")
    print("3. Range Balanced: Optimized distribution (2-2-1, 1-6/7-12)")
    print("4. Cross-Strategy Blend: Best from each strategy type")
    print("5. Complementary Selection: Unique/moderate frequency for diversity")
    
    print("\nKEY FUSION ADVANTAGES:")
    print("✓ Captures synergies between original 5 combinations")
    print("✓ Maintains mixed strategy optimization principles")
    print("✓ Reduces overlap while preserving high-performing elements")
    print("✓ Leverages mathematical blending and performance weighting")
    print("✓ Ensures broader coverage through diversification")

if __name__ == "__main__":
    main()