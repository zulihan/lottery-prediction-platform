"""
Create 2 fusion combinations from the 5 June 25 French Loto combinations
Using mathematical averaging and strategic blending
"""

from collections import Counter

def get_june_25_combinations():
    """Get the 5 June 25 French Loto combinations"""
    return [
        {'id': 1, 'numbers': [7, 12, 19, 24, 35], 'lucky': 10, 'strategy': 'Enhanced Frequency + Frequency', 'focus': 'Top frequency with diversified lucky'},
        {'id': 2, 'numbers': [7, 11, 19, 31, 42], 'lucky': 2, 'strategy': 'Enhanced Frequency + Frequency', 'focus': 'Frequency with low lucky'},
        {'id': 3, 'numbers': [11, 13, 15, 17, 44], 'lucky': 3, 'strategy': 'Enhanced Coverage + Balanced', 'focus': 'Balanced coverage with lucky 3'},
        {'id': 4, 'numbers': [4, 9, 19, 28, 38], 'lucky': 3, 'strategy': 'Enhanced Frequency + Frequency', 'focus': 'Varied frequency with strategic lucky'},
        {'id': 5, 'numbers': [4, 6, 8, 31, 40], 'lucky': 1, 'strategy': 'Enhanced Coverage + Balanced', 'focus': 'Balanced with low lucky'}
    ]

def analyze_frequency_patterns(combinations):
    """Analyze frequency patterns across the 5 combinations"""
    
    all_numbers = []
    all_lucky = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_lucky.append(combo['lucky'])
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    print("FREQUENCY ANALYSIS ACROSS 5 JUNE 25 COMBINATIONS:")
    print("-" * 49)
    print("Most frequent numbers:")
    for num, freq in number_freq.most_common(10):
        print(f"  {num}: appears {freq} times")
    
    print("\nLucky number frequencies:")
    for lucky, freq in lucky_freq.most_common():
        print(f"  {lucky}: appears {freq} times")
    print()
    
    return number_freq, lucky_freq

def create_mathematical_average_fusion(combinations, number_freq, lucky_freq):
    """Create fusion using mathematical averaging"""
    
    print("FUSION 1: MATHEMATICAL AVERAGE APPROACH")
    print("-" * 38)
    
    # Select most frequent numbers ensuring range distribution
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Ensure range balance: 1-2 low (1-16), 2-3 mid (17-33), 1-2 high (34-49)
    low_numbers = [(n, f) for n, f in sorted_numbers if n <= 16]
    mid_numbers = [(n, f) for n, f in sorted_numbers if 17 <= n <= 33]
    high_numbers = [(n, f) for n, f in sorted_numbers if n >= 34]
    
    selected_numbers = []
    
    # Select top from each range
    if low_numbers:
        selected_numbers.extend([n for n, f in low_numbers[:2]])
    if mid_numbers:
        selected_numbers.extend([n for n, f in mid_numbers[:2]])
    if high_numbers:
        selected_numbers.extend([n for n, f in high_numbers[:1]])
    
    # Fill remaining slots with highest frequency overall
    while len(selected_numbers) < 5:
        for num, freq in sorted_numbers:
            if num not in selected_numbers:
                selected_numbers.append(num)
                break
    
    # Select most frequent lucky number
    most_frequent_lucky = sorted(lucky_freq.items(), key=lambda x: x[1], reverse=True)[0][0]
    
    fusion_1 = {
        'numbers': sorted(selected_numbers[:5]),
        'lucky': most_frequent_lucky,
        'method': 'Mathematical Average Fusion',
        'source': 'Most frequent elements across all combinations',
        'strategy_blend': 'Frequency-weighted selection',
        'range_distribution': f"{len([n for n in selected_numbers if n <= 16])} low, {len([n for n in selected_numbers if 17 <= n <= 33])} mid, {len([n for n in selected_numbers if n >= 34])} high"
    }
    
    print(f"Selected numbers by frequency: {sorted_numbers[:8]}")
    print(f"Range-balanced selection: {fusion_1['numbers']}")
    print(f"Most frequent lucky: {most_frequent_lucky} (appears {lucky_freq[most_frequent_lucky]} times)")
    print(f"Range distribution: {fusion_1['range_distribution']}")
    print()
    
    return fusion_1

def create_strategic_blend_fusion(combinations, number_freq, lucky_freq):
    """Create fusion using strategic cross-strategy blending"""
    
    print("FUSION 2: STRATEGIC CROSS-BLEND APPROACH")
    print("-" * 40)
    
    # Separate by strategy type
    frequency_combos = [c for c in combinations if 'Frequency + Frequency' in c['strategy']]
    coverage_combos = [c for c in combinations if 'Coverage + Balanced' in c['strategy']]
    
    print(f"Frequency combinations: {len(frequency_combos)}")
    print(f"Coverage combinations: {len(coverage_combos)}")
    
    # Blend: 60% from Frequency, 40% from Coverage (based on June 18 analysis)
    frequency_numbers = []
    coverage_numbers = []
    
    for combo in frequency_combos:
        frequency_numbers.extend(combo['numbers'])
    
    for combo in coverage_combos:
        coverage_numbers.extend(combo['numbers'])
    
    freq_number_count = Counter(frequency_numbers)
    cov_number_count = Counter(coverage_numbers)
    
    # Select 3 numbers from frequency strategy (60%)
    top_freq_numbers = [n for n, c in freq_number_count.most_common(10)]
    
    # Select 2 numbers from coverage strategy (40%)
    top_cov_numbers = [n for n, c in cov_number_count.most_common(10)]
    
    # Blend selection ensuring no duplicates and range balance
    selected_numbers = []
    
    # Add 3 from frequency
    for num in top_freq_numbers:
        if len(selected_numbers) < 3 and num not in selected_numbers:
            selected_numbers.append(num)
    
    # Add 2 from coverage
    for num in top_cov_numbers:
        if len(selected_numbers) < 5 and num not in selected_numbers:
            selected_numbers.append(num)
    
    # Fill remaining if needed
    all_available = set(frequency_numbers + coverage_numbers)
    while len(selected_numbers) < 5:
        remaining = [n for n in all_available if n not in selected_numbers]
        if remaining:
            selected_numbers.append(min(remaining))  # Add smallest remaining for balance
        else:
            break
    
    # Lucky number: blend strategy - favor low numbers from lessons learned
    frequency_lucky = [c['lucky'] for c in frequency_combos]
    coverage_lucky = [c['lucky'] for c in coverage_combos]
    
    # Prioritize low lucky numbers (1-5) based on June 18 lessons
    low_lucky_candidates = [l for l in frequency_lucky + coverage_lucky if l <= 5]
    if low_lucky_candidates:
        blend_lucky = min(low_lucky_candidates)  # Take lowest for strategic advantage
    else:
        all_lucky = frequency_lucky + coverage_lucky
        blend_lucky = min(all_lucky)
    
    fusion_2 = {
        'numbers': sorted(selected_numbers),
        'lucky': blend_lucky,
        'method': 'Strategic Cross-Blend Fusion',
        'source': '60% Frequency + 40% Coverage blend',
        'strategy_blend': 'Cross-strategy synthesis',
        'strategic_rationale': 'Combines best of both proven approaches'
    }
    
    print(f"Frequency strategy numbers: {freq_number_count.most_common(5)}")
    print(f"Coverage strategy numbers: {cov_number_count.most_common(5)}")
    print(f"Blended selection (3F+2C): {fusion_2['numbers']}")
    print(f"Strategic lucky choice: {blend_lucky} (low number priority)")
    print()
    
    return fusion_2

def validate_fusion_combinations(fusion_1, fusion_2):
    """Validate both fusion combinations"""
    
    print("FUSION COMBINATIONS VALIDATION:")
    print("-" * 31)
    
    fusions = [fusion_1, fusion_2]
    
    for i, fusion in enumerate(fusions, 1):
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
        
        status = "✓" if valid else f"✗ ({', '.join(issues)})"
        
        print(f"Fusion {i}: {fusion['method']}")
        print(f"  Numbers: {numbers} + Lucky: {lucky} {status}")
        print(f"  Source: {fusion['source']}")
        print(f"  Strategy: {fusion['strategy_blend']}")
        print()
    
    return all(len(f['numbers']) == 5 and 1 <= f['lucky'] <= 10 for f in fusions)

def analyze_fusion_characteristics(fusion_1, fusion_2, original_combinations):
    """Analyze characteristics of both fusion combinations"""
    
    print("FUSION COMBINATIONS ANALYSIS:")
    print("-" * 29)
    
    # Analyze overlap with originals
    fusion_1_numbers = set(fusion_1['numbers'])
    fusion_2_numbers = set(fusion_2['numbers'])
    
    print("Overlap with Original Combinations:")
    for combo in original_combinations:
        combo_numbers = set(combo['numbers'])
        
        overlap_1 = len(fusion_1_numbers.intersection(combo_numbers))
        overlap_2 = len(fusion_2_numbers.intersection(combo_numbers))
        lucky_match_1 = "✓" if fusion_1['lucky'] == combo['lucky'] else "❌"
        lucky_match_2 = "✓" if fusion_2['lucky'] == combo['lucky'] else "❌"
        
        print(f"  Combo {combo['id']}: Fusion1={overlap_1}nums+{lucky_match_1}, Fusion2={overlap_2}nums+{lucky_match_2}")
    
    # Coverage analysis
    all_fusion_numbers = fusion_1_numbers.union(fusion_2_numbers)
    all_original_numbers = set()
    for combo in original_combinations:
        all_original_numbers.update(combo['numbers'])
    
    coverage_rate = len(all_fusion_numbers.intersection(all_original_numbers)) / len(all_original_numbers) * 100
    
    print(f"\nCoverage Analysis:")
    print(f"  Combined fusion coverage: {len(all_fusion_numbers)} unique numbers")
    print(f"  Original combinations coverage: {len(all_original_numbers)} unique numbers") 
    print(f"  Overlap rate: {coverage_rate:.1f}%")
    
    # Strategic comparison
    print(f"\nStrategic Comparison:")
    print(f"  Fusion 1: Pure frequency approach with range balance")
    print(f"  Fusion 2: Strategic blend (60% Freq + 40% Coverage)")
    print(f"  Lucky strategies: {fusion_1['lucky']} vs {fusion_2['lucky']}")
    
    # Range analysis
    for i, fusion in enumerate([fusion_1, fusion_2], 1):
        low = len([n for n in fusion['numbers'] if n <= 16])
        mid = len([n for n in fusion['numbers'] if 17 <= n <= 33])
        high = len([n for n in fusion['numbers'] if n >= 34])
        total = sum(fusion['numbers'])
        
        print(f"  Fusion {i} range: {low} low, {mid} mid, {high} high (sum: {total})")

def main():
    """Create 2 fusion combinations from the 5 June 25 combinations"""
    
    print("CREATING 2 FUSION COMBINATIONS FROM 5 JUNE 25 FRENCH LOTO")
    print("=" * 59)
    
    original_combinations = get_june_25_combinations()
    
    print("ORIGINAL 5 COMBINATIONS:")
    print("-" * 24)
    for combo in original_combinations:
        print(f"{combo['id']}. {combo['strategy']}: {combo['numbers']} + {combo['lucky']}")
        print(f"   Focus: {combo['focus']}")
    print()
    
    number_freq, lucky_freq = analyze_frequency_patterns(original_combinations)
    
    fusion_1 = create_mathematical_average_fusion(original_combinations, number_freq, lucky_freq)
    fusion_2 = create_strategic_blend_fusion(original_combinations, number_freq, lucky_freq)
    
    valid = validate_fusion_combinations(fusion_1, fusion_2)
    
    if valid:
        analyze_fusion_characteristics(fusion_1, fusion_2, original_combinations)
        
        print("\nFUSION ADVANTAGES:")
        print("✓ Mathematical averaging preserves most successful elements")
        print("✓ Strategic blending optimizes Frequency+Coverage balance")
        print("✓ Low lucky number prioritization from June 18 lessons")
        print("✓ Range-balanced number selection")
        print("✓ Reduced single-strategy dependency risk")
    
    return fusion_1, fusion_2

if __name__ == "__main__":
    main()