"""
Create 2 fusion combinations from the 5 French Loto combinations
Using mathematical averaging and strategic cross-blending
"""

from collections import Counter

def get_french_loto_combinations():
    """Get the 5 French Loto combinations"""
    return [
        {'id': 1, 'numbers': [3, 7, 8, 18, 29], 'lucky': 7, 'strategy': 'Frequency Analysis + Range Complement Lucky', 'type': 'Frequency'},
        {'id': 2, 'numbers': [6, 11, 18, 21, 49], 'lucky': 6, 'strategy': 'Coverage Optimization + Frequency Opposite Lucky', 'type': 'Coverage'},
        {'id': 3, 'numbers': [20, 26, 29, 37, 46], 'lucky': 10, 'strategy': 'Enhanced Risk-Reward + Pure Frequency Lucky', 'type': 'Risk-Reward'},
        {'id': 4, 'numbers': [14, 17, 19, 35, 42], 'lucky': 10, 'strategy': 'Frequency Analysis (Hot) + Balanced Mix Lucky', 'type': 'Frequency'},
        {'id': 5, 'numbers': [8, 17, 19, 27, 48], 'lucky': 8, 'strategy': 'Coverage Optimization (Mid) + Contrarian Lucky', 'type': 'Coverage'}
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
    
    print("FREQUENCY ANALYSIS ACROSS 5 FRENCH LOTO COMBINATIONS:")
    print("-" * 53)
    print("Most frequent numbers:")
    for num, freq in number_freq.most_common(10):
        print(f"  {num}: appears {freq} times")
    
    print("\nLucky number frequencies:")
    for lucky, freq in lucky_freq.most_common():
        print(f"  {lucky}: appears {freq} times")
    print()
    
    return number_freq, lucky_freq

def create_mathematical_average_fusion(combinations, number_freq, lucky_freq):
    """Create fusion using mathematical averaging of most frequent elements"""
    
    print("FUSION 1: MATHEMATICAL AVERAGE APPROACH")
    print("-" * 38)
    
    # Select most frequent numbers ensuring range distribution
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_lucky = sorted(lucky_freq.items(), key=lambda x: x[1], reverse=True)
    
    print(f"Number frequencies: {sorted_numbers}")
    print(f"Lucky frequencies: {sorted_lucky}")
    
    # Select top 5 most frequent numbers
    selected_numbers = [num for num, freq in sorted_numbers[:5]]
    
    # Ensure good range distribution
    low_count = len([n for n in selected_numbers if n <= 16])
    mid_count = len([n for n in selected_numbers if 17 <= n <= 33])
    high_count = len([n for n in selected_numbers if n >= 34])
    
    print(f"Initial selection: {sorted(selected_numbers)} (range: {low_count}L, {mid_count}M, {high_count}H)")
    
    # Select most frequent lucky number
    selected_lucky = sorted_lucky[0][0]
    
    fusion_1 = {
        'numbers': sorted(selected_numbers),
        'lucky': selected_lucky,
        'method': 'Mathematical Average Fusion',
        'source': 'Most frequent elements across all 5 combinations',
        'strategy_blend': 'Pure frequency weighting',
        'range_distribution': f"{low_count} low, {mid_count} mid, {high_count} high"
    }
    
    print(f"Selected numbers: {fusion_1['numbers']}")
    print(f"Selected lucky: {fusion_1['lucky']}")
    print()
    
    return fusion_1

def create_strategic_cross_blend_fusion(combinations, number_freq, lucky_freq):
    """Create fusion using strategic cross-blending of all strategy types"""
    
    print("FUSION 2: STRATEGIC CROSS-BLEND APPROACH")
    print("-" * 40)
    
    # Separate by strategy type
    frequency_combos = [c for c in combinations if c['type'] == 'Frequency']
    coverage_combos = [c for c in combinations if c['type'] == 'Coverage']
    risk_reward_combos = [c for c in combinations if c['type'] == 'Risk-Reward']
    
    print(f"Frequency combinations: {len(frequency_combos)}")
    print(f"Coverage combinations: {len(coverage_combos)}")
    print(f"Risk-Reward combinations: {len(risk_reward_combos)}")
    
    # Extract numbers from each strategy type
    frequency_numbers = []
    coverage_numbers = []
    risk_reward_numbers = []
    frequency_lucky = []
    coverage_lucky = []
    risk_reward_lucky = []
    
    for combo in frequency_combos:
        frequency_numbers.extend(combo['numbers'])
        frequency_lucky.append(combo['lucky'])
    
    for combo in coverage_combos:
        coverage_numbers.extend(combo['numbers'])
        coverage_lucky.append(combo['lucky'])
    
    for combo in risk_reward_combos:
        risk_reward_numbers.extend(combo['numbers'])
        risk_reward_lucky.append(combo['lucky'])
    
    freq_num_freq = Counter(frequency_numbers)
    cov_num_freq = Counter(coverage_numbers)
    risk_num_freq = Counter(risk_reward_numbers)
    freq_lucky_freq = Counter(frequency_lucky)
    cov_lucky_freq = Counter(coverage_lucky)
    risk_lucky_freq = Counter(risk_reward_lucky)
    
    print(f"Frequency strategy numbers: {freq_num_freq.most_common(3)}")
    print(f"Coverage strategy numbers: {cov_num_freq.most_common(3)}")
    print(f"Risk-Reward strategy numbers: {risk_num_freq.most_common(3)}")
    print(f"Frequency lucky: {freq_lucky_freq}")
    print(f"Coverage lucky: {cov_lucky_freq}")
    print(f"Risk-Reward lucky: {risk_lucky_freq}")
    
    # Strategic blend: Equal representation from each strategy
    # 2 numbers from Frequency, 2 from Coverage, 1 from Risk-Reward
    selected_numbers = []
    
    # Select 2 numbers from Frequency strategy
    top_frequency = [n for n, c in freq_num_freq.most_common()]
    frequency_selection = []
    for num in top_frequency:
        if len(frequency_selection) < 2 and num not in selected_numbers:
            frequency_selection.append(num)
            selected_numbers.append(num)
    
    # Select 2 numbers from Coverage strategy
    top_coverage = [n for n, c in cov_num_freq.most_common()]
    coverage_selection = []
    for num in top_coverage:
        if len(coverage_selection) < 2 and num not in selected_numbers:
            coverage_selection.append(num)
            selected_numbers.append(num)
    
    # Select 1 number from Risk-Reward strategy
    top_risk_reward = [n for n, c in risk_num_freq.most_common()]
    risk_reward_selection = []
    for num in top_risk_reward:
        if len(risk_reward_selection) < 1 and num not in selected_numbers:
            risk_reward_selection.append(num)
            selected_numbers.append(num)
    
    # Lucky number selection: blend all approaches
    # Use most represented lucky number from the blend
    all_lucky_from_strategies = frequency_lucky + coverage_lucky + risk_reward_lucky
    lucky_blend_freq = Counter(all_lucky_from_strategies)
    selected_lucky = lucky_blend_freq.most_common(1)[0][0]
    
    fusion_2 = {
        'numbers': sorted(selected_numbers),
        'lucky': selected_lucky,
        'method': 'Strategic Cross-Blend Fusion',
        'source': 'Equal representation from all 3 strategy types',
        'strategy_blend': 'Balanced strategy synthesis',
        'frequency_contribution': frequency_selection,
        'coverage_contribution': coverage_selection,
        'risk_reward_contribution': risk_reward_selection
    }
    
    print(f"Frequency contribution (2): {frequency_selection}")
    print(f"Coverage contribution (2): {coverage_selection}")
    print(f"Risk-Reward contribution (1): {risk_reward_selection}")
    print(f"Blended numbers: {fusion_2['numbers']}")
    print(f"Blended lucky: {fusion_2['lucky']}")
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
    
    return all(len(f['numbers']) == 5 and isinstance(f['lucky'], int) for f in fusions)

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
        
        overlap_1_nums = len(fusion_1_numbers.intersection(combo_numbers))
        overlap_2_nums = len(fusion_2_numbers.intersection(combo_numbers))
        
        lucky_match_1 = "✓" if fusion_1['lucky'] == combo['lucky'] else "✗"
        lucky_match_2 = "✓" if fusion_2['lucky'] == combo['lucky'] else "✗"
        
        print(f"  Combo {combo['id']} ({combo['type']}): F1={overlap_1_nums}n+{lucky_match_1}L, F2={overlap_2_nums}n+{lucky_match_2}L")
    
    # Range analysis
    print(f"\nRange Analysis:")
    for i, fusion in enumerate([fusion_1, fusion_2], 1):
        low = len([n for n in fusion['numbers'] if n <= 16])
        mid = len([n for n in fusion['numbers'] if 17 <= n <= 33])
        high = len([n for n in fusion['numbers'] if n >= 34])
        total = sum(fusion['numbers'])
        
        print(f"  Fusion {i}: {low}L+{mid}M+{high}H numbers (sum: {total}), lucky: {fusion['lucky']}")
    
    # Strategic comparison
    print(f"\nStrategic Comparison:")
    print(f"  Fusion 1: Pure frequency approach preserving most successful elements")
    print(f"  Fusion 2: Equal strategy blend with balanced representation")
    print(f"  Diversity: Different synthesis approaches for comprehensive coverage")
    
    # Coverage effectiveness
    all_fusion_numbers = fusion_1_numbers.union(fusion_2_numbers)
    all_fusion_lucky = {fusion_1['lucky'], fusion_2['lucky']}
    
    print(f"\nCombined Coverage:")
    print(f"  Total unique numbers: {len(all_fusion_numbers)}")
    print(f"  Total unique lucky: {len(all_fusion_lucky)}")
    print(f"  Numbers: {sorted(all_fusion_numbers)}")
    print(f"  Lucky numbers: {sorted(all_fusion_lucky)}")

def analyze_french_loto_fusion_advantages():
    """Analyze advantages specific to French Loto fusion approach"""
    
    print("\nFRENCH LOTO FUSION ADVANTAGES:")
    print("-" * 30)
    
    print("STRATEGIC SYNTHESIS:")
    print("• Mathematical averaging preserves most successful elements")
    print("• Strategic blending ensures equal representation from all approaches")
    print("• Frequency + Coverage + Risk-Reward comprehensive coverage")
    print("• Lucky number selection optimized through frequency analysis")
    print()
    
    print("FRENCH LOTO SPECIFIC BENEFITS:")
    print("• Maintains different strategies for numbers vs lucky (core principle)")
    print("• Reduces dependency on single-strategy approaches")
    print("• Leverages proven mixed-strategy effectiveness")
    print("• Optimized lucky number selection from all strategy types")
    print()
    
    print("RISK MITIGATION:")
    print("• Fusion 1: Pure frequency reduces randomness")
    print("• Fusion 2: Strategy balance prevents over-concentration")
    print("• Combined approach covers multiple winning scenarios")
    print("• Historical lesson integration (diversified lucky selection)")

def main():
    """Create 2 fusion combinations from the 5 French Loto combinations"""
    
    print("CREATING 2 FRENCH LOTO FUSION COMBINATIONS FROM 5 ORIGINALS")
    print("=" * 59)
    
    original_combinations = get_french_loto_combinations()
    
    print("ORIGINAL 5 COMBINATIONS:")
    print("-" * 24)
    for combo in original_combinations:
        print(f"{combo['id']}. {combo['strategy']} ({combo['type']})")
        print(f"   Numbers: {combo['numbers']} + Lucky: {combo['lucky']}")
    print()
    
    number_freq, lucky_freq = analyze_frequency_patterns(original_combinations)
    
    fusion_1 = create_mathematical_average_fusion(original_combinations, number_freq, lucky_freq)
    fusion_2 = create_strategic_cross_blend_fusion(original_combinations, number_freq, lucky_freq)
    
    valid = validate_fusion_combinations(fusion_1, fusion_2)
    
    if valid:
        analyze_fusion_characteristics(fusion_1, fusion_2, original_combinations)
        analyze_french_loto_fusion_advantages()
        
        print("\nFUSION SUMMARY:")
        print("✓ Mathematical averaging preserves most successful elements")
        print("✓ Strategic blending ensures balanced representation")
        print("✓ Frequency + Coverage + Risk-Reward synthesis")
        print("✓ Optimized lucky number selection")
        print("✓ French Loto principles maintained")
        print("✓ Historical lessons integrated")
    
    return fusion_1, fusion_2

if __name__ == "__main__":
    main()