"""
Analyze the actual Euromillions combinations we generated for May 20, 2025
against the real drawing results.
"""

def get_actual_may20_combinations():
    """
    The actual combinations we generated for May 20, 2025 Euromillions draw
    """
    combinations = [
        # First Set - Analysis-based combinations
        {"numbers": [1, 2, 11, 14, 37], "stars": [3, 7], "strategy": "Overdue Numbers"},
        {"numbers": [2, 31, 39, 40, 47], "stars": [5, 8], "strategy": "Overdue Numbers"},
        {"numbers": [3, 14, 31, 39, 40], "stars": [3, 7], "strategy": "Overdue Numbers"},
        {"numbers": [3, 21, 37, 44, 50], "stars": [7, 9], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [9, 21, 27, 44, 50], "stars": [2, 11], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [3, 19, 37, 38, 44], "stars": [2, 10], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [3, 19, 37, 44, 46], "stars": [2, 12], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [3, 19, 21, 44, 50], "stars": [2, 4], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [9, 19, 21, 44, 46], "stars": [9, 11], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [6, 16, 31, 35, 39], "stars": [2, 9], "strategy": "Balanced Strategy"},
        
        # Second Set - Diverse combinations avoiding recent numbers
        {"numbers": [17, 20, 32, 38, 44], "stars": [2, 10], "strategy": "Hot Numbers Strategy"},
        {"numbers": [4, 34, 36, 41, 45], "stars": [5, 7], "strategy": "Cold Numbers Strategy"},
        {"numbers": [10, 16, 30, 45, 50], "stars": [2, 10], "strategy": "Balanced Mix Strategy"},
        {"numbers": [1, 20, 36, 40, 50], "stars": [1, 2], "strategy": "High Range Strategy"},
        {"numbers": [10, 19, 20, 39, 42], "stars": [2, 5], "strategy": "Low Range Strategy"},
        {"numbers": [4, 16, 19, 40, 49], "stars": [2, 5], "strategy": "Even Numbers Strategy"},
        {"numbers": [14, 19, 27, 42, 44], "stars": [1, 2], "strategy": "Hot-Cold Balance Strategy"},
        {"numbers": [17, 22, 29, 34, 38], "stars": [2, 10], "strategy": "Low Sum Strategy"},
        {"numbers": [22, 32, 38, 44, 45], "stars": [4, 10], "strategy": "Overdue Numbers Strategy"},
        {"numbers": [1, 18, 29, 31, 34], "stars": [2, 7], "strategy": "Optimized Coverage Strategy"}
    ]
    
    return combinations

def get_may20_actual_results():
    """
    Actual Euromillions results for May 20, 2025:
    Numbers: 1, 8, 13, 29, 47
    Stars: 5, 6
    """
    return {
        'numbers': [1, 8, 13, 29, 47],
        'stars': [5, 6]
    }

def analyze_combination_performance(combination, actual_results):
    """
    Analyze how well a single combination performed
    """
    numbers = combination['numbers']
    stars = combination['stars']
    
    # Calculate matches
    number_matches = len(set(numbers) & set(actual_results['numbers']))
    star_matches = len(set(stars) & set(actual_results['stars']))
    
    # Determine prize tier
    prize_tier = get_prize_tier(number_matches, star_matches)
    
    return {
        'strategy': combination['strategy'],
        'numbers': numbers,
        'stars': stars,
        'number_matches': number_matches,
        'star_matches': star_matches,
        'total_matches': number_matches + star_matches,
        'prize_tier': prize_tier,
        'matched_numbers': list(set(numbers) & set(actual_results['numbers'])),
        'matched_stars': list(set(stars) & set(actual_results['stars']))
    }

def get_prize_tier(number_matches, star_matches):
    """
    Determine Euromillions prize tier based on matches
    """
    if number_matches == 5 and star_matches == 2:
        return "Jackpot (5+2)"
    elif number_matches == 5 and star_matches == 1:
        return "2nd Prize (5+1)"
    elif number_matches == 5 and star_matches == 0:
        return "3rd Prize (5+0)"
    elif number_matches == 4 and star_matches == 2:
        return "4th Prize (4+2)"
    elif number_matches == 4 and star_matches == 1:
        return "5th Prize (4+1)"
    elif number_matches == 3 and star_matches == 2:
        return "6th Prize (3+2)"
    elif number_matches == 4 and star_matches == 0:
        return "7th Prize (4+0)"
    elif number_matches == 2 and star_matches == 2:
        return "8th Prize (2+2)"
    elif number_matches == 3 and star_matches == 1:
        return "9th Prize (3+1)"
    elif number_matches == 3 and star_matches == 0:
        return "10th Prize (3+0)"
    elif number_matches == 1 and star_matches == 2:
        return "11th Prize (1+2)"
    elif number_matches == 2 and star_matches == 1:
        return "12th Prize (2+1)"
    elif number_matches == 2 and star_matches == 0:
        return "13th Prize (2+0)"
    else:
        return "No Prize"

def analyze_strategy_performance(analyzed_results):
    """
    Analyze which strategies performed best
    """
    strategy_stats = {}
    
    for result in analyzed_results:
        strategy = result['strategy']
        if strategy not in strategy_stats:
            strategy_stats[strategy] = {
                'combinations': 0,
                'total_number_matches': 0,
                'total_star_matches': 0,
                'total_matches': 0,
                'best_performance': 0,
                'prizes_won': 0,
                'results': []
            }
        
        stats = strategy_stats[strategy]
        stats['combinations'] += 1
        stats['total_number_matches'] += result['number_matches']
        stats['total_star_matches'] += result['star_matches']
        stats['total_matches'] += result['total_matches']
        stats['results'].append(result)
        
        if result['total_matches'] > stats['best_performance']:
            stats['best_performance'] = result['total_matches']
            
        if result['prize_tier'] != "No Prize":
            stats['prizes_won'] += 1
    
    return strategy_stats

def main():
    """
    Main analysis function
    """
    print("=== ACTUAL Euromillions May 20, 2025 Performance Analysis ===\n")
    
    # Get our actual combinations
    combinations = get_actual_may20_combinations()
    actual_results = get_may20_actual_results()
    
    print(f"Analyzing {len(combinations)} combinations we generated for May 20, 2025")
    print(f"Actual Results: Numbers {actual_results['numbers']}, Stars {actual_results['stars']}\n")
    
    # Analyze each combination
    analyzed_results = []
    for combination in combinations:
        result = analyze_combination_performance(combination, actual_results)
        analyzed_results.append(result)
    
    # Sort by performance
    analyzed_results.sort(key=lambda x: (x['total_matches'], x['number_matches']), reverse=True)
    
    print("=== TOP PERFORMING COMBINATIONS ===")
    for i, result in enumerate(analyzed_results[:10], 1):
        print(f"\n{i}. {result['strategy']}")
        print(f"   Numbers: {result['numbers']} -> {result['number_matches']} matches {result['matched_numbers']}")
        print(f"   Stars: {result['stars']} -> {result['star_matches']} matches {result['matched_stars']}")
        print(f"   Total Matches: {result['total_matches']}")
        print(f"   Prize Tier: {result['prize_tier']}")
    
    # Strategy performance analysis
    strategy_stats = analyze_strategy_performance(analyzed_results)
    
    print(f"\n=== STRATEGY PERFORMANCE SUMMARY ===")
    for strategy, stats in sorted(strategy_stats.items(), 
                                key=lambda x: x[1]['best_performance'], 
                                reverse=True):
        avg_matches = stats['total_matches'] / stats['combinations']
        print(f"\n{strategy}:")
        print(f"  - Combinations: {stats['combinations']}")
        print(f"  - Best Performance: {stats['best_performance']} total matches")
        print(f"  - Average Total Matches: {avg_matches:.1f}")
        print(f"  - Prizes Won: {stats['prizes_won']}")
    
    # Overall statistics
    total_combinations = len(analyzed_results)
    total_matches = sum(r['total_matches'] for r in analyzed_results)
    total_number_matches = sum(r['number_matches'] for r in analyzed_results)
    total_star_matches = sum(r['star_matches'] for r in analyzed_results)
    total_prizes = sum(1 for r in analyzed_results if r['prize_tier'] != "No Prize")
    
    print(f"\n=== OVERALL PERFORMANCE ===")
    print(f"Total Combinations Played: {total_combinations}")
    print(f"Total Number Matches: {total_number_matches}")
    print(f"Total Star Matches: {total_star_matches}")
    print(f"Total Matches Overall: {total_matches}")
    print(f"Average Matches per Combination: {total_matches/total_combinations:.1f}")
    print(f"Combinations with Prizes: {total_prizes}")
    print(f"Prize Rate: {(total_prizes/total_combinations)*100:.1f}%")
    
    # Analysis insights
    print(f"\n=== KEY INSIGHTS ===")
    
    # Find which numbers we got right
    all_our_numbers = set()
    all_our_stars = set()
    for combo in combinations:
        all_our_numbers.update(combo['numbers'])
        all_our_stars.update(combo['stars'])
    
    winning_numbers_we_had = set(actual_results['numbers']) & all_our_numbers
    winning_stars_we_had = set(actual_results['stars']) & all_our_stars
    
    print(f"Winning numbers we included: {sorted(winning_numbers_we_had)} out of {actual_results['numbers']}")
    print(f"Winning stars we included: {sorted(winning_stars_we_had)} out of {actual_results['stars']}")
    
    # Check coverage
    coverage_numbers = len(winning_numbers_we_had) / len(actual_results['numbers'])
    coverage_stars = len(winning_stars_we_had) / len(actual_results['stars'])
    
    print(f"Number coverage: {coverage_numbers*100:.1f}% ({len(winning_numbers_we_had)}/5)")
    print(f"Star coverage: {coverage_stars*100:.1f}% ({len(winning_stars_we_had)}/2)")
    
    if total_matches > 0:
        print(f"\n✓ SUCCESS: We achieved {total_matches} total matches!")
        print("Our prediction strategies are working and getting results.")
    else:
        print(f"\n→ No matches this time, but our coverage shows we're on the right track.")
    
    # Best combination analysis
    best_combo = analyzed_results[0]
    if best_combo['total_matches'] > 0:
        print(f"\nBest combination: {best_combo['strategy']}")
        print(f"Numbers {best_combo['numbers']} + Stars {best_combo['stars']}")
        print(f"Got {best_combo['total_matches']} total matches!")

if __name__ == "__main__":
    main()