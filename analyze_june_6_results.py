"""
Analyze the June 6, 2025 Euromillions results against all generated combinations
Results: 20, 21, 29, 30, 35 / 2, 12
"""

def get_june_6_actual_results():
    """Get the actual June 6, 2025 Euromillions results"""
    return {
        'numbers': [20, 21, 29, 30, 35],
        'stars': [2, 12]
    }

def get_all_generated_combinations():
    """Get all combinations that were generated"""
    
    # Initial 20 corrected combinations
    initial_20 = [
        {'id': 'INIT-1', 'numbers': [12, 15, 38, 47, 49], 'stars': [5, 7], 'strategy': 'Coverage Optimization Enhanced'},
        {'id': 'INIT-2', 'numbers': [23, 44, 19, 50, 21], 'stars': [3, 7], 'strategy': 'Frequency Analysis Ultimate'},
        {'id': 'INIT-3', 'numbers': [47, 29, 15, 49, 23], 'stars': [5, 12], 'strategy': 'Recent Trends Analysis'},
        {'id': 'INIT-4', 'numbers': [10, 44, 50, 42, 37], 'stars': [7, 2], 'strategy': 'High-Range Pattern'},
        {'id': 'INIT-5', 'numbers': [15, 38, 23, 44, 19], 'stars': [7, 3], 'strategy': 'Star 7 Priority'},
        {'id': 'INIT-6', 'numbers': [23, 44, 50, 45, 47], 'stars': [5, 7], 'strategy': 'Extreme High Focus'},
        {'id': 'INIT-7', 'numbers': [23, 44, 19, 16, 48], 'stars': [7, 8], 'strategy': 'Hot-Cold Balance'},
        {'id': 'INIT-8', 'numbers': [23, 32, 39, 42, 46], 'stars': [5, 7], 'strategy': 'Time Series Pattern'},
        {'id': 'INIT-9', 'numbers': [23, 44, 19, 10, 37], 'stars': [7, 3], 'strategy': 'Coverage Maximizer'},
        {'id': 'INIT-10', 'numbers': [12, 38, 23, 44, 19], 'stars': [5, 7], 'strategy': 'Ultimate Synthesis'},
        {'id': 'INIT-11', 'numbers': [23, 44, 19, 12, 38], 'stars': [7, 3], 'strategy': 'Frequency-Coverage Fusion'},
        {'id': 'INIT-12', 'numbers': [50, 49, 48, 16, 29], 'stars': [5, 8], 'strategy': 'Extreme-Balance Fusion'},
        {'id': 'INIT-13', 'numbers': [32, 39, 42, 10, 37], 'stars': [7, 2], 'strategy': 'Pattern-Range Fusion'},
        {'id': 'INIT-14', 'numbers': [47, 15, 12, 23, 44], 'stars': [5, 12], 'strategy': 'Recent-Synthesis Fusion'},
        {'id': 'INIT-15', 'numbers': [12, 23, 50, 38, 44], 'stars': [7, 5], 'strategy': 'Triple Strategy Fusion'},
        {'id': 'INIT-16', 'numbers': [23, 44, 1, 2, 3], 'stars': [7, 1], 'strategy': 'Gap Coverage Fusion'},
        {'id': 'INIT-17', 'numbers': [10, 12, 44, 15, 23], 'stars': [7, 5], 'strategy': 'Star Optimization Fusion'},
        {'id': 'INIT-18', 'numbers': [2, 23, 30, 37, 44], 'stars': [3, 7], 'strategy': 'Mathematical Progression Enhanced'},
        {'id': 'INIT-19', 'numbers': [12, 15, 38, 23, 44], 'stars': [7, 3], 'strategy': 'High Performance Mix'},
        {'id': 'INIT-20', 'numbers': [15, 23, 19, 44, 38], 'stars': [5, 7], 'strategy': 'Ultimate Diversity Fusion'}
    ]
    
    # Ultimate 39 combinations - Fusion Mastery Set (combinations 9-18)
    fusion_mastery_set = [
        {'id': 'ULT-9', 'numbers': [12, 23, 38, 44, 50], 'stars': [7, 3], 'strategy': 'Fusion: Frequency + June 3'},
        {'id': 'ULT-10', 'numbers': [2, 19, 29, 45, 49], 'stars': [7, 5], 'strategy': 'Fusion: Extreme + Balance'},
        {'id': 'ULT-11', 'numbers': [10, 20, 30, 40, 50], 'stars': [7, 2], 'strategy': 'Fusion: Pattern + Range'},
        {'id': 'ULT-12', 'numbers': [15, 21, 25, 37, 43], 'stars': [7, 8], 'strategy': 'Fusion: Hot + Cold'},
        {'id': 'ULT-13', 'numbers': [5, 11, 17, 23, 29], 'stars': [7, 9], 'strategy': 'Fusion: Mathematical Progression'},
        {'id': 'ULT-14', 'numbers': [1, 19, 27, 42, 48], 'stars': [7, 12], 'strategy': 'Fusion: Coverage + Frequency'},
        {'id': 'ULT-15', 'numbers': [9, 24, 35, 44, 47], 'stars': [7, 3], 'strategy': 'Fusion: Recent + Historical'},
        {'id': 'ULT-16', 'numbers': [13, 22, 31, 39, 46], 'stars': [7, 2], 'strategy': 'Fusion: Multi-Strategy Synthesis'},
        {'id': 'ULT-17', 'numbers': [16, 26, 36, 41, 50], 'stars': [7, 8], 'strategy': 'Fusion: Performance Optimization'},
        {'id': 'ULT-18', 'numbers': [18, 28, 33, 38, 49], 'stars': [7, 5], 'strategy': 'Fusion: Ultimate Strategy'}
    ]
    
    # Fusion Mix 10 combinations
    fusion_mix_10 = [
        {'id': 'MIX-1', 'numbers': [12, 15, 23, 44, 47], 'stars': [5, 7], 'strategy': 'Fusion Mix 1: June 3 + Frequency Supreme'},
        {'id': 'MIX-2', 'numbers': [1, 19, 38, 46, 50], 'stars': [7, 3], 'strategy': 'Fusion Mix 2: Extreme Range + Coverage'},
        {'id': 'MIX-3', 'numbers': [21, 29, 37, 42, 49], 'stars': [7, 2], 'strategy': 'Fusion Mix 3: Hot Numbers + Pattern'},
        {'id': 'MIX-4', 'numbers': [15, 38, 44, 48, 50], 'stars': [5, 8], 'strategy': 'Fusion Mix 4: June 3 + Extreme High'},
        {'id': 'MIX-5', 'numbers': [10, 23, 27, 39, 44], 'stars': [7, 9], 'strategy': 'Fusion Mix 5: Frequency + Range Balance'},
        {'id': 'MIX-6', 'numbers': [6, 17, 25, 33, 41], 'stars': [7, 12], 'strategy': 'Fusion Mix 6: Coverage + Star 7 Focus'},
        {'id': 'MIX-7', 'numbers': [3, 19, 29, 45, 48], 'stars': [7, 5], 'strategy': 'Fusion Mix 7: Hybrid Extreme + Frequent'},
        {'id': 'MIX-8', 'numbers': [8, 16, 24, 32, 40], 'stars': [3, 7], 'strategy': 'Fusion Mix 8: Mathematical + Historical'},
        {'id': 'MIX-9', 'numbers': [12, 20, 28, 36, 44], 'stars': [2, 7], 'strategy': 'Fusion Mix 9: Ultimate Synthesis'},
        {'id': 'MIX-10', 'numbers': [11, 22, 33, 44, 47], 'stars': [7, 8], 'strategy': 'Fusion Mix 10: Master Fusion Supreme'}
    ]
    
    return initial_20, fusion_mastery_set, fusion_mix_10

def analyze_combination_performance(combo, actual_results):
    """Analyze how well a combination performed against actual results"""
    
    number_matches = len(set(combo['numbers']) & set(actual_results['numbers']))
    star_matches = len(set(combo['stars']) & set(actual_results['stars']))
    
    # Find which specific numbers/stars matched
    matched_numbers = set(combo['numbers']) & set(actual_results['numbers'])
    matched_stars = set(combo['stars']) & set(actual_results['stars'])
    
    return {
        'combo_id': combo['id'],
        'strategy': combo['strategy'],
        'numbers': combo['numbers'],
        'stars': combo['stars'],
        'number_matches': number_matches,
        'star_matches': star_matches,
        'matched_numbers': sorted(list(matched_numbers)),
        'matched_stars': sorted(list(matched_stars)),
        'total_score': number_matches + star_matches
    }

def find_winning_number_coverage():
    """Find which combinations had all 5 winning numbers distributed across them"""
    
    actual_results = get_june_6_actual_results()
    winning_numbers = set(actual_results['numbers'])  # {20, 21, 29, 30, 35}
    
    initial_20, fusion_mastery, fusion_mix = get_all_generated_combinations()
    
    print("🔍 ANALYZING WINNING NUMBER COVERAGE")
    print("Winning numbers: 20, 21, 29, 30, 35")
    print("=" * 45)
    
    # Check Fusion Mastery set specifically
    print("FUSION MASTERY SET ANALYSIS:")
    print("-" * 28)
    
    fusion_numbers = set()
    for combo in fusion_mastery:
        fusion_numbers.update(combo['numbers'])
        
    coverage = winning_numbers & fusion_numbers
    print(f"Numbers covered by Fusion Mastery set: {sorted(list(coverage))}")
    print(f"Coverage: {len(coverage)}/5 winning numbers")
    
    # Show which combinations contributed which winning numbers
    print("\nWINNING NUMBER SOURCES:")
    for winning_num in sorted(winning_numbers):
        contributors = []
        for combo in fusion_mastery:
            if winning_num in combo['numbers']:
                contributors.append(combo['id'])
        print(f"Number {winning_num}: found in {contributors}")
    
    return coverage

def analyze_fusion_mastery_issue():
    """Analyze why Fusion Mastery wasn't actually a fusion of initial 20"""
    
    initial_20, fusion_mastery, fusion_mix = get_all_generated_combinations()
    
    print("\n🚨 FUSION MASTERY ANALYSIS - WHY IT WASN'T TRULY FUSION")
    print("=" * 60)
    
    # Get numbers from initial 20
    initial_numbers = set()
    for combo in initial_20:
        initial_numbers.update(combo['numbers'])
    
    # Check how much Fusion Mastery actually used from initial 20
    print("FUSION MASTERY vs INITIAL 20 OVERLAP:")
    print("-" * 37)
    
    total_fusion_numbers = set()
    for combo in fusion_mastery:
        total_fusion_numbers.update(combo['numbers'])
    
    overlap = initial_numbers & total_fusion_numbers
    fusion_only = total_fusion_numbers - initial_numbers
    
    print(f"Numbers in Initial 20: {len(initial_numbers)} unique numbers")
    print(f"Numbers in Fusion Mastery: {len(total_fusion_numbers)} unique numbers")
    print(f"Overlap: {len(overlap)} numbers")
    print(f"Fusion Mastery introduced: {len(fusion_only)} new numbers")
    print(f"New numbers: {sorted(list(fusion_only))}")
    
    print(f"\nFUSION REALITY CHECK:")
    print(f"True fusion percentage: {(len(overlap)/len(total_fusion_numbers))*100:.1f}%")
    print(f"This explains why it had all 5 winning numbers - it wasn't constrained by the initial 20!")

def main():
    """Main analysis function"""
    
    actual_results = get_june_6_actual_results()
    initial_20, fusion_mastery, fusion_mix = get_all_generated_combinations()
    
    print("🎯 JUNE 6, 2025 EUROMILLIONS RESULTS ANALYSIS")
    print("Results: 20, 21, 29, 30, 35 / 2, 12")
    print("=" * 50)
    
    # Analyze all combinations
    all_results = []
    
    # Initial 20
    print("INITIAL 20 PERFORMANCE:")
    print("-" * 23)
    for combo in initial_20:
        result = analyze_combination_performance(combo, actual_results)
        all_results.append(result)
        if result['total_score'] >= 2:
            print(f"{result['combo_id']}: {result['number_matches']} numbers, {result['star_matches']} stars - {result['matched_numbers']} + {result['matched_stars']}")
    
    # Fusion Mastery
    print(f"\nFUSION MASTERY PERFORMANCE:")
    print("-" * 27)
    for combo in fusion_mastery:
        result = analyze_combination_performance(combo, actual_results)
        all_results.append(result)
        if result['total_score'] >= 1:
            print(f"{result['combo_id']}: {result['number_matches']} numbers, {result['star_matches']} stars - {result['matched_numbers']} + {result['matched_stars']}")
    
    # Fusion Mix
    print(f"\nFUSION MIX PERFORMANCE:")
    print("-" * 23)
    for combo in fusion_mix:
        result = analyze_combination_performance(combo, actual_results)
        all_results.append(result)
        if result['total_score'] >= 1:
            print(f"{result['combo_id']}: {result['number_matches']} numbers, {result['star_matches']} stars - {result['matched_numbers']} + {result['matched_stars']}")
    
    # Find best performers
    best_performers = sorted(all_results, key=lambda x: x['total_score'], reverse=True)[:5]
    
    print(f"\nTOP 5 PERFORMERS:")
    print("-" * 17)
    for i, result in enumerate(best_performers, 1):
        print(f"{i}. {result['combo_id']}: {result['total_score']} total matches ({result['strategy']})")
    
    # Analyze the coverage issue
    find_winning_number_coverage()
    analyze_fusion_mastery_issue()

if __name__ == "__main__":
    main()