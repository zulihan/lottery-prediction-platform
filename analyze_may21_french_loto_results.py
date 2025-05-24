"""
Analyze French Loto combinations performance against May 21, 2025 results
Actual results: 7, 10, 11, 18, 49 / Lucky Number: 3
"""

def analyze_combination_performance():
    """Analyze how our combinations performed against actual results"""
    
    # Actual May 21, 2025 French Loto results
    actual_numbers = [7, 10, 11, 18, 49]
    actual_lucky = 3
    
    print("🎯 FRENCH LOTO MAY 21, 2025 - PERFORMANCE ANALYSIS")
    print("=" * 65)
    print(f"Actual Results: {actual_numbers} / Lucky Number: {actual_lucky}")
    print("=" * 65)
    
    # All generated combinations
    all_combinations = [
        # Hybrid Mix Strategy
        {'numbers': [2, 13, 30, 43, 48], 'lucky': 9, 'strategy': 'Hybrid Mix Strategy'},
        {'numbers': [8, 20, 28, 30, 42], 'lucky': 4, 'strategy': 'Hybrid Mix Strategy'},
        {'numbers': [20, 21, 34, 42, 43], 'lucky': 6, 'strategy': 'Hybrid Mix Strategy'},
        {'numbers': [8, 30, 33, 34, 36], 'lucky': 4, 'strategy': 'Hybrid Mix Strategy'},
        {'numbers': [8, 28, 30, 36, 42], 'lucky': 6, 'strategy': 'Hybrid Mix Strategy'},
        
        # High Risk Strategy
        {'numbers': [8, 37, 41, 42, 44], 'lucky': 3, 'strategy': 'High Risk Strategy'},
        {'numbers': [8, 21, 23, 40, 43], 'lucky': 9, 'strategy': 'High Risk Strategy'},
        {'numbers': [14, 21, 33, 42, 43], 'lucky': 4, 'strategy': 'High Risk Strategy'},
        {'numbers': [8, 33, 37, 42, 47], 'lucky': 10, 'strategy': 'High Risk Strategy'},
        
        # Sequential Pattern Strategy
        {'numbers': [26, 33, 42, 43, 44], 'lucky': 4, 'strategy': 'Sequential Pattern Strategy'},
        {'numbers': [6, 30, 39, 40, 43], 'lucky': 4, 'strategy': 'Sequential Pattern Strategy'},
        {'numbers': [7, 8, 14, 31, 42], 'lucky': 4, 'strategy': 'Sequential Pattern Strategy'},
        
        # Cold Numbers Focus
        {'numbers': [15, 21, 23, 30, 34], 'lucky': 2, 'strategy': 'Cold Numbers Focus'},
        {'numbers': [5, 18, 21, 23, 38], 'lucky': 6, 'strategy': 'Cold Numbers Focus'},
        
        # Balanced Mix Strategy
        {'numbers': [15, 22, 23, 33, 42], 'lucky': 9, 'strategy': 'Balanced Mix Strategy'},
        {'numbers': [2, 8, 28, 39, 42], 'lucky': 6, 'strategy': 'Balanced Mix Strategy'},
        
        # High Range Focus
        {'numbers': [12, 18, 42, 43, 46], 'lucky': 10, 'strategy': 'High Range Focus'},
        {'numbers': [8, 13, 36, 38, 40], 'lucky': 8, 'strategy': 'High Range Focus'},
        
        # Even Numbers Focus
        {'numbers': [3, 6, 18, 36, 38], 'lucky': 6, 'strategy': 'Even Numbers Focus'},
        {'numbers': [8, 15, 26, 43, 48], 'lucky': 2, 'strategy': 'Even Numbers Focus'},
        
        # Mixed Combinations
        {'numbers': [21, 26, 33, 42, 44], 'lucky': 4, 'strategy': 'High-Sequential Mix'},
        {'numbers': [21, 23, 30, 42, 43], 'lucky': 9, 'strategy': 'High-Cold Mix'},
        {'numbers': [13, 20, 26, 30, 34], 'lucky': 6, 'strategy': 'Hybrid-Even Mix'},
        {'numbers': [8, 21, 26, 30, 40], 'lucky': 9, 'strategy': 'High-Hybrid-Even Mix'},
        {'numbers': [2, 28, 36, 39, 42], 'lucky': 6, 'strategy': 'Hybrid-Balanced Mix'}
    ]
    
    # Analyze each combination
    results = []
    best_performers = []
    
    for i, combo in enumerate(all_combinations, 1):
        # Count number matches
        number_matches = len(set(combo['numbers']) & set(actual_numbers))
        lucky_match = 1 if combo['lucky'] == actual_lucky else 0
        
        # Calculate total score
        total_matches = number_matches + lucky_match
        
        # Determine prize tier
        if number_matches == 5 and lucky_match == 1:
            prize_tier = "JACKPOT!"
        elif number_matches == 5:
            prize_tier = "Rank 2 (5 numbers)"
        elif number_matches == 4 and lucky_match == 1:
            prize_tier = "Rank 3 (4+lucky)"
        elif number_matches == 4:
            prize_tier = "Rank 4 (4 numbers)"
        elif number_matches == 3 and lucky_match == 1:
            prize_tier = "Rank 5 (3+lucky)"
        elif number_matches == 3:
            prize_tier = "Rank 6 (3 numbers)"
        elif number_matches == 2 and lucky_match == 1:
            prize_tier = "Rank 7 (2+lucky)"
        else:
            prize_tier = "No prize"
        
        result = {
            'combination': i,
            'numbers': combo['numbers'],
            'lucky': combo['lucky'],
            'strategy': combo['strategy'],
            'number_matches': number_matches,
            'lucky_match': lucky_match,
            'total_matches': total_matches,
            'prize_tier': prize_tier,
            'matched_numbers': list(set(combo['numbers']) & set(actual_numbers))
        }
        
        results.append(result)
        
        if total_matches >= 2:  # Any significant performance
            best_performers.append(result)
    
    return results, best_performers

def display_results(results, best_performers):
    """Display the analysis results"""
    
    print(f"\n🏆 BEST PERFORMING COMBINATIONS")
    print("=" * 50)
    
    if best_performers:
        # Sort by total matches
        best_performers.sort(key=lambda x: (x['total_matches'], x['number_matches']), reverse=True)
        
        for result in best_performers:
            print(f"\n🎯 Combination {result['combination']}: {result['strategy']}")
            print(f"   Numbers: {result['numbers']} | Lucky: {result['lucky']}")
            print(f"   Matches: {result['number_matches']}/5 numbers + {result['lucky_match']}/1 lucky = {result['total_matches']} total")
            if result['matched_numbers']:
                print(f"   Matched Numbers: {result['matched_numbers']}")
            print(f"   Prize Tier: {result['prize_tier']}")
    else:
        print("No combinations achieved 2+ matches this draw.")
    
    print(f"\n📊 STRATEGY PERFORMANCE SUMMARY")
    print("=" * 45)
    
    # Group by strategy
    strategy_performance = {}
    for result in results:
        strategy = result['strategy']
        if strategy not in strategy_performance:
            strategy_performance[strategy] = {'combinations': 0, 'total_matches': 0, 'best_match': 0}
        
        strategy_performance[strategy]['combinations'] += 1
        strategy_performance[strategy]['total_matches'] += result['total_matches']
        strategy_performance[strategy]['best_match'] = max(strategy_performance[strategy]['best_match'], result['total_matches'])
    
    # Sort strategies by performance
    sorted_strategies = sorted(strategy_performance.items(), 
                             key=lambda x: (x[1]['best_match'], x[1]['total_matches']), reverse=True)
    
    for strategy, stats in sorted_strategies:
        avg_matches = stats['total_matches'] / stats['combinations']
        print(f"\n{strategy}:")
        print(f"   Best Match: {stats['best_match']} total matches")
        print(f"   Average: {avg_matches:.1f} matches per combination")
        print(f"   Combinations: {stats['combinations']}")

def analyze_winning_patterns():
    """Analyze what made the winning numbers special"""
    
    actual_numbers = [7, 10, 11, 18, 49]
    actual_lucky = 3
    
    print(f"\n🔍 WINNING PATTERN ANALYSIS")
    print("=" * 40)
    print(f"Winning Numbers: {actual_numbers}")
    print(f"Lucky Number: {actual_lucky}")
    
    # Range analysis
    low_count = len([n for n in actual_numbers if n <= 16])
    mid_count = len([n for n in actual_numbers if 17 <= n <= 33])
    high_count = len([n for n in actual_numbers if n >= 34])
    
    print(f"\nRange Distribution:")
    print(f"   Low (1-16): {low_count} numbers - {[n for n in actual_numbers if n <= 16]}")
    print(f"   Mid (17-33): {mid_count} numbers - {[n for n in actual_numbers if 17 <= n <= 33]}")
    print(f"   High (34-49): {high_count} numbers - {[n for n in actual_numbers if n >= 34]}")
    
    # Even/odd analysis
    even_count = len([n for n in actual_numbers if n % 2 == 0])
    odd_count = len([n for n in actual_numbers if n % 2 == 1])
    
    print(f"\nEven/Odd Distribution:")
    print(f"   Even: {even_count} numbers - {[n for n in actual_numbers if n % 2 == 0]}")
    print(f"   Odd: {odd_count} numbers - {[n for n in actual_numbers if n % 2 == 1]}")
    
    # Consecutive analysis
    consecutive_pairs = []
    sorted_numbers = sorted(actual_numbers)
    for i in range(len(sorted_numbers)-1):
        if sorted_numbers[i+1] - sorted_numbers[i] == 1:
            consecutive_pairs.append((sorted_numbers[i], sorted_numbers[i+1]))
    
    if consecutive_pairs:
        print(f"\nConsecutive Pairs: {consecutive_pairs}")
    else:
        print(f"\nNo consecutive pairs in winning numbers")

def main():
    """Main analysis function"""
    
    # Analyze performance
    results, best_performers = analyze_combination_performance()
    
    # Display results
    display_results(results, best_performers)
    
    # Analyze winning patterns
    analyze_winning_patterns()
    
    print(f"\n💡 KEY INSIGHTS FOR FUTURE STRATEGY")
    print("=" * 45)
    print("✓ Analyze which strategies performed best")
    print("✓ Note the winning pattern characteristics") 
    print("✓ Adjust future combinations based on performance")
    print("✓ Consider patterns that worked vs. those that didn't")

if __name__ == "__main__":
    main()