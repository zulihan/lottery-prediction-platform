"""
Create 1 fusion combination from the 5 June 24 enhanced combinations
Using mathematical averaging and frequency weighting
"""

from collections import Counter

def get_june_24_combinations():
    """Get the 5 June 24 enhanced combinations"""
    return [
        {'id': 1, 'numbers': [11, 18, 19, 29, 34], 'stars': [2, 9], 'strategy': 'Balanced + Cold', 'risk': 'Moderate'},
        {'id': 2, 'numbers': [13, 18, 28, 33, 38], 'stars': [2, 8], 'strategy': 'Cold Emphasis', 'risk': 'Aggressive'},
        {'id': 3, 'numbers': [10, 19, 22, 25, 48], 'stars': [6, 10], 'strategy': 'Conservative + Cold', 'risk': 'Conservative'},
        {'id': 4, 'numbers': [4, 5, 19, 44, 47], 'stars': [2, 9], 'strategy': 'Contrarian', 'risk': 'High Risk'},
        {'id': 5, 'numbers': [10, 11, 36, 48, 49], 'stars': [2, 8], 'strategy': 'Warm Focus', 'risk': 'Balanced'},
    ]

def analyze_frequency_across_combinations(combinations):
    """Analyze frequency of numbers and stars across all combinations"""
    
    all_numbers = []
    all_stars = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    print("FREQUENCY ANALYSIS ACROSS 5 JUNE 24 COMBINATIONS:")
    print("-" * 49)
    print("Most frequent numbers:")
    for num, freq in number_freq.most_common(10):
        print(f"  {num}: appears {freq} times")
    
    print("\nMost frequent stars:")
    for star, freq in star_freq.most_common():
        print(f"  {star}: appears {freq} times")
    print()
    
    return number_freq, star_freq

def create_ultimate_fusion_combination(combinations):
    """Create one ultimate fusion combination using weighted averaging"""
    
    print("CREATING ULTIMATE FUSION COMBINATION:")
    print("-" * 35)
    
    # Weight combinations by their risk diversity and strategic value
    # Give higher weight to moderate risk and proven approaches
    risk_weights = {
        'Moderate': 1.2,     # Balanced approach
        'Conservative': 1.1,  # Proven hot numbers
        'Balanced': 1.0,     # Standard weight
        'Aggressive': 0.9,   # High cold emphasis
        'High Risk': 0.8     # Contrarian approach
    }
    
    weighted_numbers = Counter()
    weighted_stars = Counter()
    
    print("Weighting Strategy:")
    for combo in combinations:
        weight = risk_weights.get(combo['risk'], 1.0)
        print(f"  {combo['strategy']}: weight {weight}")
        
        for num in combo['numbers']:
            weighted_numbers[num] += weight
        
        for star in combo['stars']:
            weighted_stars[star] += weight
    
    print()
    
    # Select numbers ensuring good range distribution
    sorted_weighted_numbers = sorted(weighted_numbers.items(), key=lambda x: x[1], reverse=True)
    
    # Ensure range balance: aim for 1-2 low, 2-3 mid, 1-2 high
    low_numbers = [(n, w) for n, w in sorted_weighted_numbers if n <= 16]
    mid_numbers = [(n, w) for n, w in sorted_weighted_numbers if 17 <= n <= 32]
    high_numbers = [(n, w) for n, w in sorted_weighted_numbers if n >= 33]
    
    selected_numbers = []
    
    # Select 2 from most weighted in each category, ensuring 5 total
    if low_numbers:
        selected_numbers.extend([n for n, w in low_numbers[:1]])
    
    if mid_numbers:
        selected_numbers.extend([n for n, w in mid_numbers[:2]])
    
    if high_numbers:
        selected_numbers.extend([n for n, w in high_numbers[:2]])
    
    # Fill remaining slots with highest weighted overall
    while len(selected_numbers) < 5:
        for num, weight in sorted_weighted_numbers:
            if num not in selected_numbers:
                selected_numbers.append(num)
                break
    
    # Select stars - top 2 weighted
    sorted_weighted_stars = sorted(weighted_stars.items(), key=lambda x: x[1], reverse=True)
    selected_stars = [s for s, w in sorted_weighted_stars[:2]]
    
    fusion_combination = {
        'numbers': sorted(selected_numbers[:5]),
        'stars': sorted(selected_stars),
        'method': 'Weighted Mathematical Fusion',
        'source': 'Risk-weighted average of all 5 enhanced combinations',
        'risk_profile': 'Optimized Balanced',
        'strategic_elements': [
            'Mathematical weighting by risk profile',
            'Range distribution optimization',
            'Frequency-based element selection',
            'Multi-strategy synthesis'
        ]
    }
    
    return fusion_combination

def validate_fusion_combination(fusion):
    """Validate the fusion combination"""
    
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
    
    print("ULTIMATE FUSION COMBINATION:")
    print("-" * 27)
    print(f"Numbers: {numbers} + Stars: {stars} {status}")
    print(f"Method: {fusion['method']}")
    print(f"Risk Profile: {fusion['risk_profile']}")
    print(f"Source: {fusion['source']}")
    print()
    
    print("Strategic Elements:")
    for element in fusion['strategic_elements']:
        print(f"• {element}")
    print()
    
    return valid

def analyze_fusion_characteristics(fusion, original_combinations):
    """Analyze the characteristics of the fusion combination"""
    
    print("FUSION COMBINATION ANALYSIS:")
    print("-" * 28)
    
    fusion_numbers = set(fusion['numbers'])
    fusion_stars = set(fusion['stars'])
    
    # Analyze which original elements were preserved
    preserved_elements = {}
    
    for combo in original_combinations:
        combo_numbers = set(combo['numbers'])
        combo_stars = set(combo['stars'])
        
        number_overlap = len(fusion_numbers.intersection(combo_numbers))
        star_overlap = len(fusion_stars.intersection(combo_stars))
        
        preserved_elements[combo['strategy']] = {
            'number_overlap': number_overlap,
            'star_overlap': star_overlap,
            'total_overlap': number_overlap + star_overlap
        }
    
    print("Overlap with Original Combinations:")
    for strategy, overlap in preserved_elements.items():
        print(f"  {strategy}: {overlap['number_overlap']} numbers + {overlap['star_overlap']} stars = {overlap['total_overlap']} total")
    
    # Range analysis
    low_count = len([n for n in fusion['numbers'] if n <= 16])
    mid_count = len([n for n in fusion['numbers'] if 17 <= n <= 32])
    high_count = len([n for n in fusion['numbers'] if n >= 33])
    
    print(f"\nRange Distribution: {low_count} low (1-16), {mid_count} mid (17-32), {high_count} high (33-49)")
    print(f"Sum: {sum(fusion['numbers'])}")
    
    # Star analysis
    low_stars = [s for s in fusion['stars'] if s <= 6]
    high_stars = [s for s in fusion['stars'] if s >= 7]
    print(f"Star Distribution: {len(low_stars)} low (1-6), {len(high_stars)} high (7-12)")
    
    # Strategic balance
    print(f"\nStrategic Balance:")
    print(f"• Incorporates elements from all 5 risk profiles")
    print(f"• Maintains range balanced approach (proven effective)")
    print(f"• Synthesizes cold number insights with frequency optimization")
    print(f"• Uses weighted averaging to preserve best-performing elements")

def main():
    """Create the ultimate fusion combination"""
    
    print("CREATING ULTIMATE FUSION FROM 5 JUNE 24 COMBINATIONS")
    print("=" * 54)
    
    original_combinations = get_june_24_combinations()
    
    print("ORIGINAL 5 COMBINATIONS:")
    print("-" * 24)
    for combo in original_combinations:
        print(f"{combo['id']}. {combo['strategy']}: {combo['numbers']} + {combo['stars']} ({combo['risk']})")
    print()
    
    number_freq, star_freq = analyze_frequency_across_combinations(original_combinations)
    
    fusion = create_ultimate_fusion_combination(original_combinations)
    valid = validate_fusion_combination(fusion)
    
    if valid:
        analyze_fusion_characteristics(fusion, original_combinations)
        
        print("\nULTIMATE FUSION ADVANTAGES:")
        print("✓ Mathematically weighted by risk profile effectiveness")
        print("✓ Incorporates insights from all 5 strategic approaches")
        print("✓ Maintains proven Range Balanced star optimization")
        print("✓ Balances cold number inclusion with frequency analysis")
        print("✓ Synthesizes diverse risk profiles into optimal combination")
    
    return fusion

if __name__ == "__main__":
    main()