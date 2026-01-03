"""
Strategic fusion of 20 data-driven combinations using advanced mixing approaches
"""

from collections import Counter
import random

def get_all_20_combinations():
    """Get all 20 previously generated combinations"""
    return [
        # Original 10 combinations (1-10)
        {'id': 1, 'numbers': [12, 19, 20, 29, 37], 'stars': [1, 7], 'strategy': 'Risk-Reward (Conservative Plus)', 'priority': 1},
        {'id': 2, 'numbers': [1, 2, 5, 10, 12], 'stars': [2, 3], 'strategy': 'Risk-Reward (Balanced Risk)', 'priority': 1},
        {'id': 3, 'numbers': [4, 12, 29, 31, 42], 'stars': [7, 9], 'strategy': 'Risk-Reward (Warm Focus)', 'priority': 1},
        {'id': 4, 'numbers': [14, 27, 28, 37, 41], 'stars': [1, 9], 'strategy': 'Risk-Reward (Moderate Risk)', 'priority': 1},
        {'id': 5, 'numbers': [3, 18, 37, 44, 49], 'stars': [5, 9], 'strategy': 'Risk-Reward (Hot-Cold Split)', 'priority': 1},
        {'id': 6, 'numbers': [11, 14, 25, 27, 40], 'stars': [4, 9], 'strategy': 'Coverage Optimization 1', 'priority': 2},
        {'id': 7, 'numbers': [4, 19, 20, 23, 45], 'stars': [1, 5], 'strategy': 'Coverage Optimization 2', 'priority': 2},
        {'id': 8, 'numbers': [13, 27, 31, 35, 43], 'stars': [5, 8], 'strategy': 'Coverage Optimization 3', 'priority': 2},
        {'id': 9, 'numbers': [14, 15, 34, 47, 49], 'stars': [4, 8], 'strategy': 'Markov Chain 1', 'priority': 3},
        {'id': 10, 'numbers': [14, 20, 44, 49], 'stars': [4, 8], 'strategy': 'Markov Chain 2', 'priority': 3},
        
        # Additional 10 combinations (11-20)
        {'id': 11, 'numbers': [19, 25, 28, 30, 38], 'stars': [3, 5], 'strategy': 'Risk-Reward V2 (Ultra Conservative)', 'priority': 1},
        {'id': 12, 'numbers': [4, 8, 28, 45, 46], 'stars': [1, 6], 'strategy': 'Risk-Reward V2 (High Risk Balanced)', 'priority': 1},
        {'id': 13, 'numbers': [3, 5, 26, 41, 46], 'stars': [3, 10], 'strategy': 'Risk-Reward V2 (Aggressive Contrast)', 'priority': 1},
        {'id': 14, 'numbers': [24, 31, 38, 45, 49], 'stars': [4, 7], 'strategy': 'Risk-Reward V2 (Warm Specialist)', 'priority': 1},
        {'id': 15, 'numbers': [14, 24, 27, 33, 46], 'stars': [1, 3], 'strategy': 'Risk-Reward V2 (Contrarian Strategy)', 'priority': 1},
        {'id': 16, 'numbers': [1, 3, 4, 22, 43], 'stars': [2, 3], 'strategy': 'Coverage Optimization V2 1', 'priority': 2},
        {'id': 17, 'numbers': [17, 26, 28, 39, 49], 'stars': [6, 8], 'strategy': 'Coverage Optimization V2 2', 'priority': 2},
        {'id': 18, 'numbers': [1, 7, 36, 39, 48], 'stars': [2, 3], 'strategy': 'Coverage Optimization V2 3', 'priority': 2},
        {'id': 19, 'numbers': [15, 27, 30, 47, 49], 'stars': [8, 10], 'strategy': 'Markov Chain V2 1', 'priority': 3},
        {'id': 20, 'numbers': [37, 39, 44, 45, 49], 'stars': [3, 7], 'strategy': 'Markov Chain V2 2', 'priority': 3}
    ]

def analyze_combination_pools():
    """Analyze the 20 combinations to understand patterns"""
    
    combinations = get_all_20_combinations()
    
    # Extract all numbers and stars
    all_numbers = []
    all_stars = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Categorize combinations by strategy
    risk_reward_combos = [c for c in combinations if 'Risk-Reward' in c['strategy']]
    coverage_combos = [c for c in combinations if 'Coverage' in c['strategy']]
    markov_combos = [c for c in combinations if 'Markov' in c['strategy']]
    
    print("ANALYSIS OF 20 BASE COMBINATIONS:")
    print("-" * 33)
    print(f"Risk-Reward combinations: {len(risk_reward_combos)}")
    print(f"Coverage combinations: {len(coverage_combos)}")
    print(f"Markov combinations: {len(markov_combos)}")
    print(f"Most frequent numbers: {[n for n, freq in number_freq.most_common(10)]}")
    print(f"Most frequent stars: {[s for s, freq in star_freq.most_common(6)]}")
    print()
    
    return {
        'all_numbers': all_numbers,
        'all_stars': all_stars,
        'number_freq': number_freq,
        'star_freq': star_freq,
        'risk_reward': risk_reward_combos,
        'coverage': coverage_combos,
        'markov': markov_combos
    }

def frequency_weighted_fusion(combinations, num_fusions=3):
    """Create fusions based on number frequency across all combinations"""
    
    all_numbers = []
    all_stars = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    fusions = []
    
    for i in range(num_fusions):
        # Select top frequent numbers with variation
        start_idx = i * 3
        top_numbers = [n for n, freq in number_freq.most_common(20)]
        fusion_numbers = top_numbers[start_idx:start_idx+5]
        
        # Select top frequent stars
        top_stars = [s for s, freq in star_freq.most_common(6)]
        fusion_stars = top_stars[i:i+2] if i+1 < len(top_stars) else top_stars[:2]
        
        fusions.append({
            'numbers': sorted(fusion_numbers),
            'stars': sorted(fusion_stars),
            'strategy': f'Frequency Weighted Fusion {i+1}',
            'logic': f'Top frequent numbers/stars from all 20 combinations (offset {start_idx})'
        })
    
    return fusions

def cross_strategy_fusion(analysis, num_fusions=3):
    """Create fusions by combining elements from different strategy types"""
    
    risk_combos = analysis['risk_reward']
    coverage_combos = analysis['coverage']
    markov_combos = analysis['markov']
    
    fusions = []
    
    for i in range(num_fusions):
        fusion_numbers = []
        fusion_stars = []
        
        # Take 2 numbers from Risk-Reward
        risk_combo = risk_combos[i % len(risk_combos)]
        fusion_numbers.extend(random.sample(risk_combo['numbers'], 2))
        
        # Take 2 numbers from Coverage
        coverage_combo = coverage_combos[i % len(coverage_combos)]
        coverage_available = [n for n in coverage_combo['numbers'] if n not in fusion_numbers]
        if len(coverage_available) >= 2:
            fusion_numbers.extend(random.sample(coverage_available, 2))
        elif coverage_available:
            fusion_numbers.extend(coverage_available)
        
        # Take 1 number from Markov (fill to 5)
        while len(fusion_numbers) < 5:
            markov_combo = markov_combos[i % len(markov_combos)]
            markov_available = [n for n in markov_combo['numbers'] if n not in fusion_numbers]
            if markov_available:
                fusion_numbers.append(random.choice(markov_available))
            else:
                # Fallback to any available number
                all_available = set()
                for combo in risk_combos + coverage_combos + markov_combos:
                    all_available.update(combo['numbers'])
                remaining = [n for n in all_available if n not in fusion_numbers]
                if remaining:
                    fusion_numbers.append(random.choice(remaining))
                else:
                    break
        
        # Combine stars from different strategies
        risk_stars = risk_combo['stars']
        coverage_stars = coverage_combo['stars']
        
        fusion_stars = [risk_stars[0], coverage_stars[0]]
        if fusion_stars[0] == fusion_stars[1] and len(coverage_stars) > 1:
            fusion_stars[1] = coverage_stars[1]
        
        fusions.append({
            'numbers': sorted(fusion_numbers[:5]),
            'stars': sorted(fusion_stars),
            'strategy': f'Cross-Strategy Fusion {i+1}',
            'logic': f'2 Risk-Reward + 2 Coverage + 1 Markov numbers, mixed stars'
        })
    
    return fusions

def mathematical_averaging_fusion(combinations, num_fusions=2):
    """Create fusions using mathematical averaging of combination pairs"""
    
    fusions = []
    
    # Select high-performing combination pairs for averaging
    high_priority = [c for c in combinations if c['priority'] <= 2]
    
    for i in range(num_fusions):
        # Select two combinations to average
        combo1 = high_priority[i * 2 % len(high_priority)]
        combo2 = high_priority[(i * 2 + 1) % len(high_priority)]
        
        # Average corresponding positions
        averaged_numbers = []
        for pos in range(5):
            if pos < len(combo1['numbers']) and pos < len(combo2['numbers']):
                avg = round((combo1['numbers'][pos] + combo2['numbers'][pos]) / 2)
                averaged_numbers.append(avg)
        
        # Remove duplicates and fill if needed
        averaged_numbers = list(dict.fromkeys(averaged_numbers))  # Remove duplicates, preserve order
        
        # Fill to 5 numbers if needed
        while len(averaged_numbers) < 5:
            all_nums = combo1['numbers'] + combo2['numbers']
            candidates = [n for n in all_nums if n not in averaged_numbers]
            if candidates:
                averaged_numbers.append(random.choice(candidates))
            else:
                break
        
        # Average stars
        all_stars = combo1['stars'] + combo2['stars']
        averaged_stars = sorted(list(set(all_stars)))[:2]
        
        fusions.append({
            'numbers': sorted(averaged_numbers[:5]),
            'stars': averaged_stars,
            'strategy': f'Mathematical Averaging Fusion {i+1}',
            'logic': f'Averaged positions between combo {combo1["id"]} and {combo2["id"]}'
        })
    
    return fusions

def range_balanced_fusion(analysis, num_fusions=2):
    """Create fusions ensuring optimal range balance across all combinations"""
    
    combinations = get_all_20_combinations()
    
    # Analyze range distribution across all combinations
    low_numbers = []    # 1-16
    mid_numbers = []    # 17-33
    high_numbers = []   # 34-49
    
    for combo in combinations:
        for num in combo['numbers']:
            if 1 <= num <= 16:
                low_numbers.append(num)
            elif 17 <= num <= 33:
                mid_numbers.append(num)
            elif 34 <= num <= 49:
                high_numbers.append(num)
    
    low_freq = Counter(low_numbers)
    mid_freq = Counter(mid_numbers)
    high_freq = Counter(high_numbers)
    
    fusions = []
    
    # Range distribution patterns for optimal balance
    patterns = [
        (2, 2, 1),  # Balanced
        (1, 2, 2)   # High emphasis
    ]
    
    for i in range(num_fusions):
        pattern = patterns[i % len(patterns)]
        low_count, mid_count, high_count = pattern
        
        fusion_numbers = []
        
        # Select from each range based on frequency
        if low_count > 0:
            top_low = [n for n, freq in low_freq.most_common(8)]
            fusion_numbers.extend(random.sample(top_low, min(low_count, len(top_low))))
        
        if mid_count > 0:
            top_mid = [n for n, freq in mid_freq.most_common(10)]
            available_mid = [n for n in top_mid if n not in fusion_numbers]
            fusion_numbers.extend(random.sample(available_mid, min(mid_count, len(available_mid))))
        
        if high_count > 0:
            top_high = [n for n, freq in high_freq.most_common(8)]
            available_high = [n for n in top_high if n not in fusion_numbers]
            fusion_numbers.extend(random.sample(available_high, min(high_count, len(available_high))))
        
        # Select balanced stars
        star_freq = analysis['star_freq']
        top_stars = [s for s, freq in star_freq.most_common(6)]
        fusion_stars = random.sample(top_stars, 2)
        
        fusions.append({
            'numbers': sorted(fusion_numbers),
            'stars': sorted(fusion_stars),
            'strategy': f'Range Balanced Fusion {i+1}',
            'logic': f'Optimal range balance: {low_count} low + {mid_count} mid + {high_count} high'
        })
    
    return fusions

def generate_strategic_fusions():
    """Generate strategic fusions of the 20 base combinations"""
    
    print("STRATEGIC FUSION OF 20 DATA-DRIVEN COMBINATIONS")
    print("=" * 47)
    
    # Analyze the base combinations
    analysis = analyze_combination_pools()
    
    all_fusions = []
    
    # 1. Frequency Weighted Fusion (3 combinations)
    freq_fusions = frequency_weighted_fusion(get_all_20_combinations(), 3)
    all_fusions.extend(freq_fusions)
    
    # 2. Cross-Strategy Fusion (3 combinations)
    cross_fusions = cross_strategy_fusion(analysis, 3)
    all_fusions.extend(cross_fusions)
    
    # 3. Mathematical Averaging Fusion (2 combinations)
    avg_fusions = mathematical_averaging_fusion(get_all_20_combinations(), 2)
    all_fusions.extend(avg_fusions)
    
    # 4. Range Balanced Fusion (2 combinations)
    range_fusions = range_balanced_fusion(analysis, 2)
    all_fusions.extend(range_fusions)
    
    return all_fusions

def validate_and_display_fusions(fusions):
    """Validate and display the strategic fusion combinations"""
    
    print("10 STRATEGIC FUSION COMBINATIONS:")
    print("-" * 33)
    
    for i, fusion in enumerate(fusions, 21):  # Start from 21
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
        
        print(f"{i:2d}. {fusion['strategy']}")
        print(f"    Numbers: {numbers} + Stars: {stars} {status}")
        print(f"    Logic: {fusion['logic']}")
        print()
    
    # Coverage analysis
    all_numbers = set()
    all_stars = set()
    fusion_types = Counter()
    
    for fusion in fusions:
        all_numbers.update(fusion['numbers'])
        all_stars.update(fusion['stars'])
        fusion_type = fusion['strategy'].split()[0]
        fusion_types[fusion_type] += 1
    
    print("FUSION SUMMARY:")
    for fusion_type, count in fusion_types.items():
        print(f"• {fusion_type}: {count} combinations")
    print()
    
    print("FUSION COVERAGE:")
    print(f"Unique numbers: {len(all_numbers)}/49 ({len(all_numbers)/49*100:.1f}%)")
    print(f"Unique stars: {len(all_stars)}/12 ({len(all_stars)/12*100:.1f}%)")
    print(f"Number range: {min(all_numbers)}-{max(all_numbers)}")
    print(f"Star range: {min(all_stars)}-{max(all_stars)}")

def main():
    """Generate strategic fusions"""
    
    fusions = generate_strategic_fusions()
    validate_and_display_fusions(fusions)
    
    print("\nFUSION METHODOLOGY:")
    print("• Frequency Weighted: Most frequent numbers/stars across all 20")
    print("• Cross-Strategy: Combines Risk-Reward + Coverage + Markov elements")
    print("• Mathematical Averaging: Averages number positions from high-priority pairs")
    print("• Range Balanced: Optimizes low/mid/high range distribution")
    print("\nThese 10 fusions leverage the collective intelligence of all 20 base combinations")

if __name__ == "__main__":
    main()