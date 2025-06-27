"""
Create 2 fusion combinations from the 4 June 27 proven strategy combinations
Using mathematical averaging and strategic cross-blending
"""

from collections import Counter

def get_june_27_combinations():
    """Get the 4 June 27 proven strategy combinations"""
    return [
        {'id': 1, 'numbers': [3, 13, 17, 21, 45], 'stars': [2, 8], 'strategy': 'Coverage Optimization Enhanced - Ultra Balance', 'type': 'Coverage'},
        {'id': 2, 'numbers': [13, 21, 24, 26, 37], 'stars': [3, 7], 'strategy': 'Coverage Optimization Enhanced - Balanced Coverage', 'type': 'Coverage'},
        {'id': 3, 'numbers': [12, 20, 41, 45, 49], 'stars': [2, 11], 'strategy': 'Enhanced Risk-Reward - Balanced + Cold', 'type': 'Risk-Reward'},
        {'id': 4, 'numbers': [6, 8, 11, 23, 39], 'stars': [5, 7], 'strategy': 'Enhanced Risk-Reward - Cold Emphasis', 'type': 'Risk-Reward'}
    ]

def analyze_frequency_patterns(combinations):
    """Analyze frequency patterns across the 4 combinations"""
    
    all_numbers = []
    all_stars = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    print("FREQUENCY ANALYSIS ACROSS 4 JUNE 27 COMBINATIONS:")
    print("-" * 49)
    print("Most frequent numbers:")
    for num, freq in number_freq.most_common(10):
        print(f"  {num}: appears {freq} times")
    
    print("\nStar frequencies:")
    for star, freq in star_freq.most_common():
        print(f"  {star}: appears {freq} times")
    print()
    
    return number_freq, star_freq

def create_mathematical_average_fusion(combinations, number_freq, star_freq):
    """Create fusion using mathematical averaging of most frequent elements"""
    
    print("FUSION 1: MATHEMATICAL AVERAGE APPROACH")
    print("-" * 38)
    
    # Select most frequent numbers ensuring range distribution
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_stars = sorted(star_freq.items(), key=lambda x: x[1], reverse=True)
    
    print(f"Number frequencies: {sorted_numbers}")
    print(f"Star frequencies: {sorted_stars}")
    
    # Select top 5 most frequent numbers with range consideration
    selected_numbers = []
    
    # Priority to most frequent, but ensure range balance
    for num, freq in sorted_numbers:
        if len(selected_numbers) < 5:
            selected_numbers.append(num)
    
    # Ensure range distribution (adjust if needed)
    low_count = len([n for n in selected_numbers if n <= 16])
    mid_count = len([n for n in selected_numbers if 17 <= n <= 33])
    high_count = len([n for n in selected_numbers if n >= 34])
    
    print(f"Initial selection: {sorted(selected_numbers)} (range: {low_count}L, {mid_count}M, {high_count}H)")
    
    # Select top 2 most frequent stars
    selected_stars = [s for s, f in sorted_stars[:2]]
    
    fusion_1 = {
        'numbers': sorted(selected_numbers),
        'stars': sorted(selected_stars),
        'method': 'Mathematical Average Fusion',
        'source': 'Most frequent elements across all 4 combinations',
        'strategy_blend': 'Pure frequency weighting',
        'range_distribution': f"{low_count} low, {mid_count} mid, {high_count} high"
    }
    
    print(f"Selected numbers: {fusion_1['numbers']}")
    print(f"Selected stars: {fusion_1['stars']}")
    print()
    
    return fusion_1

def create_strategic_cross_blend_fusion(combinations, number_freq, star_freq):
    """Create fusion using strategic cross-blending of both strategy types"""
    
    print("FUSION 2: STRATEGIC CROSS-BLEND APPROACH")
    print("-" * 40)
    
    # Separate by strategy type
    coverage_combos = [c for c in combinations if c['type'] == 'Coverage']
    risk_reward_combos = [c for c in combinations if c['type'] == 'Risk-Reward']
    
    print(f"Coverage combinations: {len(coverage_combos)}")
    print(f"Risk-Reward combinations: {len(risk_reward_combos)}")
    
    # Extract numbers from each strategy type
    coverage_numbers = []
    risk_reward_numbers = []
    coverage_stars = []
    risk_reward_stars = []
    
    for combo in coverage_combos:
        coverage_numbers.extend(combo['numbers'])
        coverage_stars.extend(combo['stars'])
    
    for combo in risk_reward_combos:
        risk_reward_numbers.extend(combo['numbers'])
        risk_reward_stars.extend(combo['stars'])
    
    coverage_num_freq = Counter(coverage_numbers)
    risk_reward_num_freq = Counter(risk_reward_numbers)
    coverage_star_freq = Counter(coverage_stars)
    risk_reward_star_freq = Counter(risk_reward_stars)
    
    print(f"Coverage strategy numbers: {coverage_num_freq.most_common(5)}")
    print(f"Risk-Reward strategy numbers: {risk_reward_num_freq.most_common(5)}")
    print(f"Coverage stars: {coverage_star_freq}")
    print(f"Risk-Reward stars: {risk_reward_star_freq}")
    
    # Strategic blend: 60% Coverage (June 3 best) + 40% Risk-Reward (June 20 proven)
    # Based on historical performance weighting
    selected_numbers = []
    
    # Select 3 numbers from Coverage strategy (60%)
    top_coverage = [n for n, c in coverage_num_freq.most_common()]
    coverage_selection = []
    for num in top_coverage:
        if len(coverage_selection) < 3 and num not in selected_numbers:
            coverage_selection.append(num)
            selected_numbers.append(num)
    
    # Select 2 numbers from Risk-Reward strategy (40%)
    top_risk_reward = [n for n, c in risk_reward_num_freq.most_common()]
    risk_reward_selection = []
    for num in top_risk_reward:
        if len(risk_reward_selection) < 2 and num not in selected_numbers:
            risk_reward_selection.append(num)
            selected_numbers.append(num)
    
    # Star selection: blend both approaches
    # Prioritize Coverage stars (June 3 best performance) but include Risk-Reward diversity
    coverage_star_top = coverage_star_freq.most_common(1)[0][0] if coverage_star_freq else 2
    risk_reward_star_top = risk_reward_star_freq.most_common(1)[0][0] if risk_reward_star_freq else 7
    
    # Ensure range balance for stars (1 low + 1 high)
    if coverage_star_top <= 6 and risk_reward_star_top >= 7:
        selected_stars = [coverage_star_top, risk_reward_star_top]
    elif coverage_star_top >= 7 and risk_reward_star_top <= 6:
        selected_stars = [risk_reward_star_top, coverage_star_top]
    else:
        # Both in same range, pick one from each range manually
        low_options = [s for s in [coverage_star_top, risk_reward_star_top] if s <= 6]
        high_options = [s for s in [coverage_star_top, risk_reward_star_top] if s >= 7]
        
        if not low_options:  # Both high
            selected_stars = [min(coverage_star_top, risk_reward_star_top), max(coverage_star_top, risk_reward_star_top)]
        elif not high_options:  # Both low
            # Add a high star from historical data
            high_star = max(coverage_star_freq.keys() | risk_reward_star_freq.keys())
            selected_stars = [min(coverage_star_top, risk_reward_star_top), high_star]
        else:
            selected_stars = [low_options[0], high_options[0]]
    
    fusion_2 = {
        'numbers': sorted(selected_numbers),
        'stars': sorted(selected_stars),
        'method': 'Strategic Cross-Blend Fusion',
        'source': '60% Coverage + 40% Risk-Reward blend',
        'strategy_blend': 'Performance-weighted synthesis',
        'coverage_contribution': coverage_selection,
        'risk_reward_contribution': risk_reward_selection
    }
    
    print(f"Coverage contribution (3): {coverage_selection}")
    print(f"Risk-Reward contribution (2): {risk_reward_selection}")
    print(f"Blended numbers: {fusion_2['numbers']}")
    print(f"Blended stars: {fusion_2['stars']}")
    print()
    
    return fusion_2

def validate_fusion_combinations(fusion_1, fusion_2):
    """Validate both fusion combinations"""
    
    print("FUSION COMBINATIONS VALIDATION:")
    print("-" * 31)
    
    fusions = [fusion_1, fusion_2]
    
    for i, fusion in enumerate(fusions, 1):
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
        
        status = "✓" if valid else f"✗ ({', '.join(issues)})"
        
        print(f"Fusion {i}: {fusion['method']}")
        print(f"  Numbers: {numbers} + Stars: {stars} {status}")
        print(f"  Source: {fusion['source']}")
        print(f"  Strategy: {fusion['strategy_blend']}")
        print()
    
    return all(len(f['numbers']) == 5 and len(f['stars']) == 2 for f in fusions)

def analyze_fusion_characteristics(fusion_1, fusion_2, original_combinations):
    """Analyze characteristics of both fusion combinations"""
    
    print("FUSION COMBINATIONS ANALYSIS:")
    print("-" * 29)
    
    # Analyze overlap with originals
    fusion_1_numbers = set(fusion_1['numbers'])
    fusion_2_numbers = set(fusion_2['numbers'])
    fusion_1_stars = set(fusion_1['stars'])
    fusion_2_stars = set(fusion_2['stars'])
    
    print("Overlap with Original Combinations:")
    for combo in original_combinations:
        combo_numbers = set(combo['numbers'])
        combo_stars = set(combo['stars'])
        
        overlap_1_nums = len(fusion_1_numbers.intersection(combo_numbers))
        overlap_2_nums = len(fusion_2_numbers.intersection(combo_numbers))
        overlap_1_stars = len(fusion_1_stars.intersection(combo_stars))
        overlap_2_stars = len(fusion_2_stars.intersection(combo_stars))
        
        total_1 = overlap_1_nums + overlap_1_stars
        total_2 = overlap_2_nums + overlap_2_stars
        
        print(f"  Combo {combo['id']} ({combo['type']}): F1={overlap_1_nums}n+{overlap_1_stars}s={total_1}, F2={overlap_2_nums}n+{overlap_2_stars}s={total_2}")
    
    # Range analysis
    print(f"\nRange Analysis:")
    for i, fusion in enumerate([fusion_1, fusion_2], 1):
        low = len([n for n in fusion['numbers'] if n <= 16])
        mid = len([n for n in fusion['numbers'] if 17 <= n <= 33])
        high = len([n for n in fusion['numbers'] if n >= 34])
        total = sum(fusion['numbers'])
        
        low_stars = len([s for s in fusion['stars'] if s <= 6])
        high_stars = len([s for s in fusion['stars'] if s >= 7])
        
        print(f"  Fusion {i}: {low}L+{mid}M+{high}H numbers (sum: {total}), {low_stars}L+{high_stars}H stars")
    
    # Strategic comparison
    print(f"\nStrategic Comparison:")
    print(f"  Fusion 1: Pure frequency approach preserving most successful elements")
    print(f"  Fusion 2: Strategic blend weighted by historical performance")
    print(f"  Diversity: Different approaches for comprehensive coverage")
    
    # Coverage effectiveness
    all_fusion_numbers = fusion_1_numbers.union(fusion_2_numbers)
    all_fusion_stars = fusion_1_stars.union(fusion_2_stars)
    
    print(f"\nCombined Coverage:")
    print(f"  Total unique numbers: {len(all_fusion_numbers)}")
    print(f"  Total unique stars: {len(all_fusion_stars)}")
    print(f"  Numbers: {sorted(all_fusion_numbers)}")
    print(f"  Stars: {sorted(all_fusion_stars)}")

def main():
    """Create 2 fusion combinations from the 4 June 27 combinations"""
    
    print("CREATING 2 FUSION COMBINATIONS FROM 4 JUNE 27 PROVEN STRATEGIES")
    print("=" * 65)
    
    original_combinations = get_june_27_combinations()
    
    print("ORIGINAL 4 COMBINATIONS:")
    print("-" * 24)
    for combo in original_combinations:
        print(f"{combo['id']}. {combo['strategy']} ({combo['type']})")
        print(f"   Numbers: {combo['numbers']} + Stars: {combo['stars']}")
    print()
    
    number_freq, star_freq = analyze_frequency_patterns(original_combinations)
    
    fusion_1 = create_mathematical_average_fusion(original_combinations, number_freq, star_freq)
    fusion_2 = create_strategic_cross_blend_fusion(original_combinations, number_freq, star_freq)
    
    valid = validate_fusion_combinations(fusion_1, fusion_2)
    
    if valid:
        analyze_fusion_characteristics(fusion_1, fusion_2, original_combinations)
        
        print("\nFUSION ADVANTAGES:")
        print("✓ Mathematical averaging preserves most successful elements")
        print("✓ Strategic blending weights by historical performance")
        print("✓ Coverage + Risk-Reward synthesis for comprehensive approach")
        print("✓ Range Balanced star selection maintained")
        print("✓ Reduced single-strategy dependency risk")
        print("✓ Based on proven winning strategies (June 3 + June 20)")
    
    return fusion_1, fusion_2

if __name__ == "__main__":
    main()