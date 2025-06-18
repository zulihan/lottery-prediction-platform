"""
Create 5 fusion combinations from the 10 French Loto mixed strategy combinations
Using mathematical averaging, cross-strategy blending, and frequency weighting
"""

import psycopg2
import os
from collections import Counter
import random

def get_original_10_combinations():
    """Get the original 10 French Loto combinations"""
    
    combinations = [
        # Frequency + Frequency Strategy (6 combinations)
        {'id': 1, 'numbers': [13, 15, 20, 22, 36], 'lucky': 7, 'strategy': 'Frequency + Frequency'},
        {'id': 2, 'numbers': [13, 15, 22, 33, 49], 'lucky': 7, 'strategy': 'Frequency + Frequency'},
        {'id': 3, 'numbers': [1, 11, 19, 33, 45], 'lucky': 7, 'strategy': 'Frequency + Frequency'},
        {'id': 4, 'numbers': [4, 10, 27, 45, 49], 'lucky': 7, 'strategy': 'Frequency + Frequency'},
        {'id': 5, 'numbers': [1, 4, 28, 45, 49], 'lucky': 7, 'strategy': 'Frequency + Frequency'},
        {'id': 6, 'numbers': [29, 32, 37, 38, 45], 'lucky': 7, 'strategy': 'Frequency + Frequency'},
        
        # Coverage + Balanced Strategy (4 combinations)
        {'id': 7, 'numbers': [7, 10, 18, 26, 46], 'lucky': 10, 'strategy': 'Coverage + Balanced'},
        {'id': 8, 'numbers': [8, 18, 22, 34, 45], 'lucky': 5, 'strategy': 'Coverage + Balanced'},
        {'id': 9, 'numbers': [6, 9, 27, 41, 43], 'lucky': 10, 'strategy': 'Coverage + Balanced'},
        {'id': 10, 'numbers': [16, 18, 26, 29, 39], 'lucky': 7, 'strategy': 'Coverage + Balanced'},
    ]
    
    return combinations

def analyze_number_frequency_across_combinations(combinations):
    """Analyze frequency of numbers across all combinations"""
    
    all_numbers = []
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
    
    number_freq = Counter(all_numbers)
    print("NUMBER FREQUENCY ANALYSIS:")
    print("Most frequent numbers across combinations:")
    for num, freq in number_freq.most_common(10):
        print(f"  {num}: appears {freq} times")
    print()
    
    return number_freq

def analyze_lucky_frequency_across_combinations(combinations):
    """Analyze lucky number frequency across all combinations"""
    
    all_lucky = [combo['lucky'] for combo in combinations]
    lucky_freq = Counter(all_lucky)
    
    print("LUCKY NUMBER FREQUENCY ANALYSIS:")
    for lucky, freq in lucky_freq.most_common():
        print(f"  Lucky {lucky}: appears {freq} times")
    print()
    
    return lucky_freq

def create_fusion_combination_1(combinations):
    """Fusion 1: Mathematical Average of Top Frequency Numbers"""
    
    # Get all numbers from Frequency+Frequency combinations (first 6)
    freq_combos = combinations[:6]
    all_freq_numbers = []
    for combo in freq_combos:
        all_freq_numbers.extend(combo['numbers'])
    
    # Get top 8 most frequent numbers and select 5
    number_freq = Counter(all_freq_numbers)
    top_numbers = [n for n, freq in number_freq.most_common(8)]
    
    # Select 5 numbers ensuring good distribution
    selected_numbers = []
    
    # Take top 3 most frequent
    selected_numbers.extend(top_numbers[:3])
    
    # Add 2 more from remaining, ensuring range coverage
    remaining = top_numbers[3:]
    
    # Ensure low, mid, high coverage
    low_remaining = [n for n in remaining if n <= 16]
    mid_remaining = [n for n in remaining if 17 <= n <= 32]
    high_remaining = [n for n in remaining if n >= 33]
    
    if low_remaining and len([n for n in selected_numbers if n <= 16]) == 0:
        selected_numbers.append(low_remaining[0])
        remaining.remove(low_remaining[0])
    
    if high_remaining and len([n for n in selected_numbers if n >= 33]) <= 1:
        for n in high_remaining:
            if n in remaining:
                selected_numbers.append(n)
                remaining.remove(n)
                break
    
    # Fill remaining slots
    while len(selected_numbers) < 5 and remaining:
        selected_numbers.append(remaining[0])
        remaining.remove(remaining[0])
    
    # Most frequent lucky from frequency combinations
    freq_lucky = [combo['lucky'] for combo in freq_combos]
    lucky = Counter(freq_lucky).most_common(1)[0][0]
    
    return {
        'numbers': sorted(selected_numbers[:5]),
        'lucky': lucky,
        'method': 'Mathematical Average of Frequency Numbers',
        'source': 'Combinations 1-6 (Frequency+Frequency)'
    }

def create_fusion_combination_2(combinations):
    """Fusion 2: Cross-Strategy Blend (Frequency + Coverage)"""
    
    freq_combos = combinations[:6]
    coverage_combos = combinations[6:]
    
    # Take 3 numbers from most frequent in frequency combos
    freq_numbers = []
    for combo in freq_combos:
        freq_numbers.extend(combo['numbers'])
    freq_counter = Counter(freq_numbers)
    top_freq = [n for n, count in freq_counter.most_common(5)]
    
    # Take 2 numbers from coverage combos
    coverage_numbers = []
    for combo in coverage_combos:
        coverage_numbers.extend(combo['numbers'])
    coverage_counter = Counter(coverage_numbers)
    top_coverage = [n for n, count in coverage_counter.most_common(5)]
    
    # Blend: 3 from frequency, 2 from coverage (avoiding duplicates)
    selected_numbers = top_freq[:3]
    
    for num in top_coverage:
        if num not in selected_numbers and len(selected_numbers) < 5:
            selected_numbers.append(num)
    
    # If still need more, fill from remaining
    if len(selected_numbers) < 5:
        all_available = list(set(top_freq + top_coverage))
        for num in all_available:
            if num not in selected_numbers and len(selected_numbers) < 5:
                selected_numbers.append(num)
    
    # Lucky: blend frequencies from both strategies
    all_lucky = [combo['lucky'] for combo in combinations]
    lucky = Counter(all_lucky).most_common(1)[0][0]
    
    return {
        'numbers': sorted(selected_numbers[:5]),
        'lucky': lucky,
        'method': 'Cross-Strategy Blend (3 Freq + 2 Coverage)',
        'source': 'Mixed from both strategy types'
    }

def create_fusion_combination_3(combinations):
    """Fusion 3: Range Balanced Fusion"""
    
    # Ensure good range distribution across all combinations
    all_numbers = []
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
    
    number_freq = Counter(all_numbers)
    
    # Separate by ranges
    low_numbers = [(n, freq) for n, freq in number_freq.items() if n <= 16]
    mid_numbers = [(n, freq) for n, freq in number_freq.items() if 17 <= n <= 32]
    high_numbers = [(n, freq) for n, freq in number_freq.items() if n >= 33]
    
    # Sort by frequency within each range
    low_numbers.sort(key=lambda x: x[1], reverse=True)
    mid_numbers.sort(key=lambda x: x[1], reverse=True)
    high_numbers.sort(key=lambda x: x[1], reverse=True)
    
    # Select 2 low, 2 mid, 1 high (most frequent in each range)
    selected_numbers = []
    
    if low_numbers:
        selected_numbers.extend([n for n, freq in low_numbers[:2]])
    
    if mid_numbers:
        selected_numbers.extend([n for n, freq in mid_numbers[:2]])
    
    if high_numbers:
        selected_numbers.append(high_numbers[0][0])
    
    # Fill remaining slots if needed
    while len(selected_numbers) < 5:
        all_available = [n for n, freq in number_freq.most_common() if n not in selected_numbers]
        if all_available:
            selected_numbers.append(all_available[0])
        else:
            break
    
    # Second most frequent lucky
    all_lucky = [combo['lucky'] for combo in combinations]
    lucky_freq = Counter(all_lucky)
    lucky = lucky_freq.most_common(2)[1][0] if len(lucky_freq.most_common()) > 1 else lucky_freq.most_common(1)[0][0]
    
    return {
        'numbers': sorted(selected_numbers[:5]),
        'lucky': lucky,
        'method': 'Range Balanced Fusion (2-2-1 distribution)',
        'source': 'Optimized range distribution'
    }

def create_fusion_combination_4(combinations):
    """Fusion 4: Weighted Average by Strategy Performance"""
    
    # Weight frequency combinations more heavily (0.1700 score vs 0.1300)
    freq_weight = 0.65  # 65% weight for frequency combinations
    coverage_weight = 0.35  # 35% weight for coverage combinations
    
    freq_combos = combinations[:6]
    coverage_combos = combinations[6:]
    
    # Weighted number selection
    weighted_numbers = Counter()
    
    # Add frequency numbers with higher weight
    for combo in freq_combos:
        for num in combo['numbers']:
            weighted_numbers[num] += freq_weight
    
    # Add coverage numbers with lower weight
    for combo in coverage_combos:
        for num in combo['numbers']:
            weighted_numbers[num] += coverage_weight
    
    # Select top 5 weighted numbers
    top_weighted = [n for n, weight in weighted_numbers.most_common(5)]
    
    # Weighted lucky selection
    weighted_lucky = Counter()
    for combo in freq_combos:
        weighted_lucky[combo['lucky']] += freq_weight
    for combo in coverage_combos:
        weighted_lucky[combo['lucky']] += coverage_weight
    
    lucky = weighted_lucky.most_common(1)[0][0]
    
    return {
        'numbers': sorted(top_weighted),
        'lucky': lucky,
        'method': 'Weighted Average (65% Freq + 35% Coverage)',
        'source': 'Performance-weighted fusion'
    }

def create_fusion_combination_5(combinations):
    """Fusion 5: Unique Numbers Fusion (least overlap)"""
    
    # Find numbers that appear in fewer combinations (unique picks)
    all_numbers = []
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
    
    number_freq = Counter(all_numbers)
    
    # Select numbers that appear 2-3 times (not too rare, not too common)
    moderate_freq_numbers = [n for n, freq in number_freq.items() if 2 <= freq <= 3]
    
    # If not enough, add some that appear 4 times
    if len(moderate_freq_numbers) < 5:
        freq_4_numbers = [n for n, freq in number_freq.items() if freq == 4]
        moderate_freq_numbers.extend(freq_4_numbers)
    
    # If still not enough, add most frequent
    if len(moderate_freq_numbers) < 5:
        top_numbers = [n for n, freq in number_freq.most_common()]
        for num in top_numbers:
            if num not in moderate_freq_numbers and len(moderate_freq_numbers) < 5:
                moderate_freq_numbers.append(num)
    
    # Ensure range distribution
    selected_numbers = []
    low_available = [n for n in moderate_freq_numbers if n <= 16]
    mid_available = [n for n in moderate_freq_numbers if 17 <= n <= 32]
    high_available = [n for n in moderate_freq_numbers if n >= 33]
    
    # Try to get at least 1 from each range
    if low_available:
        selected_numbers.append(low_available[0])
    if mid_available:
        selected_numbers.append(mid_available[0])
    if high_available:
        selected_numbers.append(high_available[0])
    
    # Fill remaining with available numbers
    remaining_available = [n for n in moderate_freq_numbers if n not in selected_numbers]
    selected_numbers.extend(remaining_available[:5-len(selected_numbers)])
    
    # Use least frequent lucky
    all_lucky = [combo['lucky'] for combo in combinations]
    lucky_freq = Counter(all_lucky)
    lucky = min(lucky_freq, key=lucky_freq.get)
    
    return {
        'numbers': sorted(selected_numbers[:5]),
        'lucky': lucky,
        'method': 'Unique Numbers Fusion (moderate frequency)',
        'source': 'Diversified selection strategy'
    }

def validate_fusion_combinations(fusion_combinations):
    """Validate all fusion combinations"""
    
    print("FUSION COMBINATIONS VALIDATION:")
    print("-" * 31)
    
    valid_count = 0
    all_fusion_numbers = set()
    all_fusion_lucky = set()
    
    for i, fusion in enumerate(fusion_combinations, 1):
        numbers = fusion['numbers']
        lucky = fusion['lucky']
        
        # Validate
        valid = True
        issues = []
        
        if len(numbers) != 5:
            valid = False
            issues.append(f"numbers={len(numbers)}")
        if not isinstance(lucky, int):
            valid = False
            issues.append("lucky_type")
        if not all(1 <= n <= 49 for n in numbers):
            valid = False
            issues.append("number_range")
        if not (1 <= lucky <= 10):
            valid = False
            issues.append("lucky_range")
        if len(set(numbers)) != 5:
            valid = False
            issues.append("duplicate_numbers")
        
        if valid:
            valid_count += 1
            all_fusion_numbers.update(numbers)
            all_fusion_lucky.add(lucky)
        
        status = "✓" if valid else f"✗ ({', '.join(issues)})"
        
        print(f"{i}. {fusion['method']}")
        print(f"   Numbers: {numbers} + Lucky: {lucky} {status}")
        print(f"   Source: {fusion['source']}")
        print()
    
    print(f"Valid fusion combinations: {valid_count}/5")
    print(f"Unique numbers in fusions: {len(all_fusion_numbers)}/49 ({len(all_fusion_numbers)/49*100:.1f}%)")
    print(f"Unique lucky numbers: {len(all_fusion_lucky)}/10 ({len(all_fusion_lucky)/10*100:.1f}%)")
    
    return fusion_combinations

def main():
    """Create 5 fusion combinations from the 10 French Loto combinations"""
    
    print("CREATING 5 FUSION COMBINATIONS FROM 10 FRENCH LOTO COMBINATIONS")
    print("=" * 63)
    
    original_combinations = get_original_10_combinations()
    
    print("ANALYZING ORIGINAL 10 COMBINATIONS:")
    print("-" * 35)
    number_freq = analyze_number_frequency_across_combinations(original_combinations)
    lucky_freq = analyze_lucky_frequency_across_combinations(original_combinations)
    
    print("CREATING FUSION COMBINATIONS:")
    print("-" * 29)
    
    fusion_combinations = []
    
    fusion_1 = create_fusion_combination_1(original_combinations)
    fusion_combinations.append(fusion_1)
    
    fusion_2 = create_fusion_combination_2(original_combinations)
    fusion_combinations.append(fusion_2)
    
    fusion_3 = create_fusion_combination_3(original_combinations)
    fusion_combinations.append(fusion_3)
    
    fusion_4 = create_fusion_combination_4(original_combinations)
    fusion_combinations.append(fusion_4)
    
    fusion_5 = create_fusion_combination_5(original_combinations)
    fusion_combinations.append(fusion_5)
    
    validate_fusion_combinations(fusion_combinations)
    
    print("\nFUSION METHODOLOGY SUMMARY:")
    print("1. Mathematical Average: Most frequent from Frequency+Frequency")
    print("2. Cross-Strategy Blend: 3 Frequency + 2 Coverage numbers")
    print("3. Range Balanced: Optimized 2-2-1 distribution")
    print("4. Weighted Average: 65% Frequency + 35% Coverage weights")
    print("5. Unique Numbers: Moderate frequency for diversification")
    
    print("\nKEY FUSION ADVANTAGES:")
    print("✓ Captures best elements from both strategy types")
    print("✓ Reduces single-strategy dependency risk")
    print("✓ Maintains frequency optimization advantages")
    print("✓ Ensures broader number coverage")
    print("✓ Leverages mathematical blending techniques")

if __name__ == "__main__":
    main()