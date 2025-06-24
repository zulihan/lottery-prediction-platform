"""
Analyze June 20, 2025 Euromillions results against all generated combinations
Results: 5, 8, 24, 37, 47 / 3, 9
"""

def get_actual_results():
    """Get the actual June 20, 2025 Euromillions results"""
    return {
        'numbers': [5, 8, 24, 37, 47],
        'stars': [3, 9]
    }

def get_original_5_combinations():
    """Get the original 5 June 20 combinations"""
    return [
        {'id': 1, 'numbers': [10, 19, 20, 27, 29], 'stars': [2, 8], 'strategy': 'Frequency + Range Balanced', 'score': 0.0506},
        {'id': 2, 'numbers': [7, 8, 17, 21, 40], 'stars': [6, 9], 'strategy': 'Coverage + Range Balanced', 'score': 0.0476},
        {'id': 3, 'numbers': [20, 21, 29, 32, 46], 'stars': [2, 8], 'strategy': 'Risk-Reward + Frequency Stars', 'score': 0.0461},
        {'id': 4, 'numbers': [10, 17, 34, 42, 45], 'stars': [1, 10], 'strategy': 'Frequency + Range Balanced V2', 'score': 0.0506},
        {'id': 5, 'numbers': [8, 16, 21, 32, 37], 'stars': [5, 7], 'strategy': 'Risk-Reward + Range Balanced', 'score': 0.0490},
    ]

def get_fusion_combinations():
    """Get the 5 fusion combinations"""
    return [
        {'id': 1, 'numbers': [8, 10, 20, 21, 29], 'stars': [2, 8], 'method': 'Mathematical Average'},
        {'id': 2, 'numbers': [10, 17, 20, 21, 29], 'stars': [2, 8], 'method': 'Weighted Performance'},
        {'id': 3, 'numbers': [8, 10, 20, 21, 40], 'stars': [2, 8], 'method': 'Range Balanced'},
        {'id': 4, 'numbers': [7, 10, 20, 21, 32], 'stars': [2, 8], 'method': 'Cross-Strategy Blend'},
        {'id': 5, 'numbers': [10, 19, 20, 27, 40], 'stars': [6, 9], 'method': 'Complementary Selection'},
    ]

def analyze_combination_performance(combo, actual_results, combo_type="Original"):
    """Analyze how well a combination performed against actual results"""
    
    combo_numbers = set(combo['numbers'])
    combo_stars = set(combo['stars'])
    
    actual_numbers = set(actual_results['numbers'])
    actual_stars = set(actual_results['stars'])
    
    # Count matches
    number_matches = len(combo_numbers.intersection(actual_numbers))
    star_matches = len(combo_stars.intersection(actual_stars))
    
    # Matched numbers and stars
    matched_numbers = list(combo_numbers.intersection(actual_numbers))
    matched_stars = list(combo_stars.intersection(actual_stars))
    
    # Calculate prize tier
    prize_tier = get_prize_tier(number_matches, star_matches)
    
    return {
        'combo_id': combo['id'],
        'strategy': combo.get('strategy', combo.get('method', 'Unknown')),
        'combo_type': combo_type,
        'numbers': combo['numbers'],
        'stars': combo['stars'],
        'number_matches': number_matches,
        'star_matches': star_matches,
        'matched_numbers': sorted(matched_numbers),
        'matched_stars': sorted(matched_stars),
        'prize_tier': prize_tier,
        'points': get_points_for_tier(prize_tier)
    }

def get_prize_tier(number_matches, star_matches):
    """Determine Euromillions prize tier based on matches"""
    
    prize_tiers = {
        (5, 2): "1st - Jackpot",
        (5, 1): "2nd",
        (5, 0): "3rd", 
        (4, 2): "4th",
        (4, 1): "5th",
        (4, 0): "6th",
        (3, 2): "7th",
        (2, 2): "8th",
        (3, 1): "9th",
        (3, 0): "10th",
        (1, 2): "11th",
        (2, 1): "12th",
        (2, 0): "13th"
    }
    
    return prize_tiers.get((number_matches, star_matches), "No Prize")

def get_points_for_tier(tier):
    """Assign points based on prize tier"""
    
    points_map = {
        "1st - Jackpot": 100,
        "2nd": 50,
        "3rd": 25,
        "4th": 15,
        "5th": 10,
        "6th": 8,
        "7th": 6,
        "8th": 5,
        "9th": 4,
        "10th": 3,
        "11th": 2,
        "12th": 1,
        "13th": 1,
        "No Prize": 0
    }
    
    return points_map.get(tier, 0)

def analyze_all_combinations():
    """Analyze all combinations against June 20 results"""
    
    actual_results = get_actual_results()
    original_combos = get_original_5_combinations()
    fusion_combos = get_fusion_combinations()
    
    print("ANALYSIS: JUNE 20, 2025 EUROMILLIONS RESULTS")
    print("=" * 45)
    print(f"Winning Numbers: {actual_results['numbers']}")
    print(f"Winning Stars: {actual_results['stars']}")
    print()
    
    all_analysis = []
    
    # Analyze original combinations
    print("ORIGINAL 5 COMBINATIONS PERFORMANCE:")
    print("-" * 36)
    
    for combo in original_combos:
        analysis = analyze_combination_performance(combo, actual_results, "Original")
        all_analysis.append(analysis)
        
        print(f"{analysis['combo_id']}. {analysis['strategy']}")
        print(f"   Numbers: {analysis['numbers']} (Matched: {analysis['matched_numbers']})")
        print(f"   Stars: {analysis['stars']} (Matched: {analysis['matched_stars']})")
        print(f"   Result: {analysis['number_matches']} numbers + {analysis['star_matches']} stars = {analysis['prize_tier']}")
        print(f"   Points: {analysis['points']}")
        print()
    
    # Analyze fusion combinations
    print("FUSION 5 COMBINATIONS PERFORMANCE:")
    print("-" * 34)
    
    for combo in fusion_combos:
        analysis = analyze_combination_performance(combo, actual_results, "Fusion")
        all_analysis.append(analysis)
        
        print(f"{analysis['combo_id']}. {analysis['strategy']}")
        print(f"   Numbers: {analysis['numbers']} (Matched: {analysis['matched_numbers']})")
        print(f"   Stars: {analysis['stars']} (Matched: {analysis['matched_stars']})")
        print(f"   Result: {analysis['number_matches']} numbers + {analysis['star_matches']} stars = {analysis['prize_tier']}")
        print(f"   Points: {analysis['points']}")
        print()
    
    return all_analysis

def find_best_performers(all_analysis):
    """Find the best performing combinations"""
    
    # Sort by points and then by matches
    sorted_analysis = sorted(all_analysis, key=lambda x: (x['points'], x['number_matches'], x['star_matches']), reverse=True)
    
    print("BEST PERFORMERS:")
    print("-" * 16)
    
    best_performers = []
    
    for i, analysis in enumerate(sorted_analysis[:5]):
        if analysis['points'] > 0:
            best_performers.append(analysis)
            print(f"{i+1}. {analysis['combo_type']} #{analysis['combo_id']} - {analysis['strategy']}")
            print(f"   {analysis['number_matches']} numbers + {analysis['star_matches']} stars = {analysis['prize_tier']} ({analysis['points']} points)")
    
    if not best_performers:
        print("No winning combinations this draw.")
        # Show closest misses
        print("\nCLOSEST MISSES:")
        for i, analysis in enumerate(sorted_analysis[:3]):
            print(f"{i+1}. {analysis['combo_type']} #{analysis['combo_id']} - {analysis['strategy']}")
            print(f"   {analysis['number_matches']} numbers + {analysis['star_matches']} stars")
    
    print()
    return best_performers

def analyze_winning_number_coverage(all_analysis, actual_results):
    """Analyze how well we covered the winning numbers"""
    
    winning_numbers = set(actual_results['numbers'])
    winning_stars = set(actual_results['stars'])
    
    print("WINNING NUMBER COVERAGE ANALYSIS:")
    print("-" * 33)
    
    # Track which winning numbers appeared in our combinations
    number_coverage = {num: [] for num in winning_numbers}
    star_coverage = {star: [] for star in winning_stars}
    
    for analysis in all_analysis:
        combo_numbers = set(analysis['numbers'])
        combo_stars = set(analysis['stars'])
        
        # Check which winning numbers this combo covered
        for num in winning_numbers:
            if num in combo_numbers:
                number_coverage[num].append(f"{analysis['combo_type']} #{analysis['combo_id']}")
        
        # Check which winning stars this combo covered
        for star in winning_stars:
            if star in combo_stars:
                star_coverage[star].append(f"{analysis['combo_type']} #{analysis['combo_id']}")
    
    print("Winning Numbers Coverage:")
    for num in sorted(winning_numbers):
        combos = number_coverage[num]
        print(f"  Number {num}: Covered by {len(combos)} combinations")
        if combos:
            print(f"    {', '.join(combos[:3])}{'...' if len(combos) > 3 else ''}")
    
    print("\nWinning Stars Coverage:")
    for star in sorted(winning_stars):
        combos = star_coverage[star]
        print(f"  Star {star}: Covered by {len(combos)} combinations")
        if combos:
            print(f"    {', '.join(combos[:3])}{'...' if len(combos) > 3 else ''}")
    
    print()

def analyze_strategy_effectiveness(all_analysis):
    """Analyze which strategies performed best"""
    
    print("STRATEGY EFFECTIVENESS ANALYSIS:")
    print("-" * 32)
    
    # Group by strategy type
    strategy_performance = {}
    
    for analysis in all_analysis:
        strategy = analysis['strategy']
        if strategy not in strategy_performance:
            strategy_performance[strategy] = []
        strategy_performance[strategy].append(analysis)
    
    # Calculate average performance per strategy
    strategy_averages = {}
    for strategy, analyses in strategy_performance.items():
        total_points = sum(a['points'] for a in analyses)
        total_number_matches = sum(a['number_matches'] for a in analyses)
        total_star_matches = sum(a['star_matches'] for a in analyses)
        count = len(analyses)
        
        strategy_averages[strategy] = {
            'total_points': total_points,
            'avg_points': total_points / count,
            'avg_number_matches': total_number_matches / count,
            'avg_star_matches': total_star_matches / count,
            'count': count
        }
    
    # Sort by performance
    sorted_strategies = sorted(strategy_averages.items(), key=lambda x: x[1]['total_points'], reverse=True)
    
    for strategy, stats in sorted_strategies:
        print(f"{strategy}:")
        print(f"  Total Points: {stats['total_points']}")
        print(f"  Avg Number Matches: {stats['avg_number_matches']:.1f}")
        print(f"  Avg Star Matches: {stats['avg_star_matches']:.1f}")
        print()

def analyze_winning_draw_characteristics():
    """Analyze what made this draw special"""
    
    actual_results = get_actual_results()
    winning_numbers = actual_results['numbers']
    winning_stars = actual_results['stars']
    
    print("WINNING DRAW CHARACTERISTICS:")
    print("-" * 29)
    
    # Range analysis
    low_count = len([n for n in winning_numbers if n <= 16])
    mid_count = len([n for n in winning_numbers if 17 <= n <= 32])
    high_count = len([n for n in winning_numbers if n >= 33])
    
    print(f"Numbers: {winning_numbers}")
    print(f"Range Distribution: {low_count} low (1-16), {mid_count} mid (17-32), {high_count} high (33-49)")
    print(f"Sum: {sum(winning_numbers)}")
    
    # Consecutive analysis
    consecutive_pairs = []
    for i in range(len(winning_numbers)-1):
        if winning_numbers[i+1] - winning_numbers[i] == 1:
            consecutive_pairs.append((winning_numbers[i], winning_numbers[i+1]))
    
    print(f"Consecutive Pairs: {consecutive_pairs if consecutive_pairs else 'None'}")
    
    # Odd/Even analysis
    odd_numbers = [n for n in winning_numbers if n % 2 == 1]
    even_numbers = [n for n in winning_numbers if n % 2 == 0]
    
    print(f"Odd/Even: {len(odd_numbers)} odd, {len(even_numbers)} even")
    
    # Star analysis
    print(f"Stars: {winning_stars}")
    low_stars = [s for s in winning_stars if s <= 6]
    high_stars = [s for s in winning_stars if s >= 7]
    print(f"Star Range: {len(low_stars)} low (1-6), {len(high_stars)} high (7-12)")
    
    print()

def main():
    """Analyze all combinations against June 20 results"""
    
    all_analysis = analyze_all_combinations()
    best_performers = find_best_performers(all_analysis)
    
    actual_results = get_actual_results()
    analyze_winning_number_coverage(all_analysis, actual_results)
    analyze_strategy_effectiveness(all_analysis)
    analyze_winning_draw_characteristics()
    
    # Summary
    print("PERFORMANCE SUMMARY:")
    print("-" * 19)
    
    original_winners = [a for a in all_analysis if a['combo_type'] == 'Original' and a['points'] > 0]
    fusion_winners = [a for a in all_analysis if a['combo_type'] == 'Fusion' and a['points'] > 0]
    
    total_original_points = sum(a['points'] for a in all_analysis if a['combo_type'] == 'Original')
    total_fusion_points = sum(a['points'] for a in all_analysis if a['combo_type'] == 'Fusion')
    
    print(f"Original Combinations: {len(original_winners)}/5 won prizes ({total_original_points} total points)")
    print(f"Fusion Combinations: {len(fusion_winners)}/5 won prizes ({total_fusion_points} total points)")
    print(f"Overall Performance: {len(best_performers)}/10 combinations won prizes")
    
    if best_performers:
        best_type = "Original" if best_performers[0]['combo_type'] == 'Original' else "Fusion"
        print(f"Best Performer: {best_type} #{best_performers[0]['combo_id']} - {best_performers[0]['strategy']}")

if __name__ == "__main__":
    main()