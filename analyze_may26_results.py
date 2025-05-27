"""
Analyze May 26, 2025 French Loto results against our generated combinations
Actual results: 24, 33, 36, 41, 45 / Lucky Number: 7
"""

def get_may26_actual_results():
    """Get the actual May 26, 2025 French Loto results"""
    return {
        'numbers': [24, 33, 36, 41, 45],
        'lucky': 7
    }

def get_may24_adapted_combinations():
    """Get the May 24 adapted combinations we generated"""
    return [
        {'numbers': [9, 18, 27, 36, 45], 'lucky': 9, 'strategy': 'Enhanced Lucky Number Focus', 'score': 100.0},
        {'numbers': [1, 11, 21, 31, 41], 'lucky': 1, 'strategy': 'Enhanced Lucky Number Focus', 'score': 100.0},
        {'numbers': [7, 14, 28, 35, 42], 'lucky': 7, 'strategy': 'Enhanced Lucky Number Focus', 'score': 100.0},
        {'numbers': [12, 26, 35, 42, 47], 'lucky': 8, 'strategy': 'High Range Emphasis', 'score': 98.0},
        {'numbers': [8, 24, 36, 44, 48], 'lucky': 10, 'strategy': 'High Range Emphasis', 'score': 98.0},
        {'numbers': [2, 16, 22, 38, 43], 'lucky': 4, 'strategy': 'Even Dominant Strategy', 'score': 96.0},
        {'numbers': [6, 18, 30, 46, 49], 'lucky': 6, 'strategy': 'Even Dominant Strategy', 'score': 96.0},
        {'numbers': [3, 17, 25, 34, 47], 'lucky': 5, 'strategy': 'Wide Spread Strategy', 'score': 94.0},
        {'numbers': [5, 19, 28, 37, 46], 'lucky': 2, 'strategy': 'Wide Spread Strategy', 'score': 94.0},
        {'numbers': [9, 16, 24, 39, 46], 'lucky': 9, 'strategy': 'Hybrid Adapted Strategy', 'score': 100.0}
    ]

def get_best_performing_combinations():
    """Get the best performing strategy combinations (Set 2)"""
    return [
        {'numbers': [6, 14, 27, 32, 40], 'lucky': 9, 'strategy': 'New Balanced Strategy', 'score': 100.0},
        {'numbers': [8, 14, 16, 29, 36], 'lucky': 8, 'strategy': 'Coverage Optimization', 'score': 100.0},
        {'numbers': [3, 9, 17, 39, 43], 'lucky': 3, 'strategy': 'Lucky Number Focus', 'score': 100.0},
        {'numbers': [16, 32, 38, 45, 48], 'lucky': 6, 'strategy': 'High Risk Strategy', 'score': 100.0},
        {'numbers': [9, 19, 25, 39, 47], 'lucky': 7, 'strategy': 'Maximum Diversity', 'score': 100.0},
        {'numbers': [14, 16, 27, 32, 36], 'lucky': 8, 'strategy': 'Hybrid Mix (1+2)', 'score': 100.0},
        {'numbers': [3, 17, 38, 45, 48], 'lucky': 6, 'strategy': 'Hybrid Mix (3+4)', 'score': 92.0},
        {'numbers': [6, 9, 19, 25, 32], 'lucky': 2, 'strategy': 'Hybrid Mix (5+1)', 'score': 93.8},
        {'numbers': [8, 14, 29, 36, 47], 'lucky': 4, 'strategy': 'Hybrid Mix (2+5)', 'score': 90.0},
        {'numbers': [3, 6, 9, 14, 27], 'lucky': 9, 'strategy': 'Hybrid Mix (3+1)', 'score': 100.0}
    ]

def analyze_combination_performance(combination, actual_results):
    """Analyze how well a combination performed against actual results"""
    
    combo_numbers = set(combination['numbers'])
    actual_numbers = set(actual_results['numbers'])
    
    # Count number matches
    number_matches = len(combo_numbers.intersection(actual_numbers))
    matched_numbers = list(combo_numbers.intersection(actual_numbers))
    
    # Check lucky number match
    lucky_match = combination['lucky'] == actual_results['lucky']
    
    # Calculate total score
    match_score = number_matches * 2  # 2 points per number match
    if lucky_match:
        match_score += 3  # 3 points for lucky match
    
    return {
        'combination': combination,
        'number_matches': number_matches,
        'matched_numbers': matched_numbers,
        'lucky_match': lucky_match,
        'match_score': match_score,
        'percentage': (match_score / 13) * 100  # Max possible: 10 + 3 = 13
    }

def analyze_all_combinations():
    """Analyze all combinations against May 26 results"""
    
    actual_results = get_may26_actual_results()
    may24_combos = get_may24_adapted_combinations()
    best_combos = get_best_performing_combinations()
    
    print("🎯 MAY 26, 2025 FRENCH LOTO RESULTS ANALYSIS")
    print("=" * 60)
    print(f"Actual Results: {actual_results['numbers']} / Lucky: {actual_results['lucky']}")
    print("=" * 60)
    
    all_results = []
    
    # Analyze May 24 adapted combinations
    print("\n📊 MAY 24 ADAPTED COMBINATIONS PERFORMANCE:")
    print("-" * 50)
    
    for i, combo in enumerate(may24_combos, 1):
        result = analyze_combination_performance(combo, actual_results)
        all_results.append(result)
        
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        print(f"    Matches: {result['number_matches']} numbers {result['matched_numbers']}")
        if result['lucky_match']:
            print(f"    ⭐ LUCKY MATCH! ({actual_results['lucky']})")
        print(f"    Score: {result['match_score']}/13 ({result['percentage']:.1f}%)")
        print()
    
    # Analyze best performing combinations
    print("\n📊 BEST PERFORMING STRATEGY COMBINATIONS PERFORMANCE:")
    print("-" * 55)
    
    for i, combo in enumerate(best_combos, 1):
        result = analyze_combination_performance(combo, actual_results)
        all_results.append(result)
        
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        print(f"    Matches: {result['number_matches']} numbers {result['matched_numbers']}")
        if result['lucky_match']:
            print(f"    ⭐ LUCKY MATCH! ({actual_results['lucky']})")
        print(f"    Score: {result['match_score']}/13 ({result['percentage']:.1f}%)")
        print()
    
    return all_results

def find_best_performers(results):
    """Find the best performing combinations"""
    
    # Sort by match score
    sorted_results = sorted(results, key=lambda x: x['match_score'], reverse=True)
    
    print("🏆 TOP PERFORMING COMBINATIONS:")
    print("=" * 40)
    
    top_5 = sorted_results[:5]
    for i, result in enumerate(top_5, 1):
        combo = result['combination']
        print(f"{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        print(f"   Matches: {result['number_matches']} numbers {result['matched_numbers']}")
        if result['lucky_match']:
            print(f"   ⭐ LUCKY MATCH!")
        print(f"   Score: {result['match_score']}/13 ({result['percentage']:.1f}%)")
        print()
    
    return top_5

def analyze_winning_patterns(actual_results):
    """Analyze what made the winning numbers special"""
    
    numbers = actual_results['numbers']
    lucky = actual_results['lucky']
    
    print("🔍 WINNING NUMBER PATTERN ANALYSIS:")
    print("=" * 40)
    
    # Range analysis
    low_count = len([n for n in numbers if n <= 16])
    mid_count = len([n for n in numbers if 17 <= n <= 33])
    high_count = len([n for n in numbers if n >= 34])
    
    print(f"Range Distribution:")
    print(f"   Low (1-16): {low_count}/5 ({low_count/5*100:.0f}%)")
    print(f"   Mid (17-33): {mid_count}/5 ({mid_count/5*100:.0f}%)")
    print(f"   High (34-49): {high_count}/5 ({high_count/5*100:.0f}%)")
    
    # Even/odd analysis
    even_count = len([n for n in numbers if n % 2 == 0])
    odd_count = len([n for n in numbers if n % 2 == 1])
    
    print(f"\nEven/Odd Distribution:")
    print(f"   Even: {even_count}/5 ({even_count/5*100:.0f}%)")
    print(f"   Odd: {odd_count}/5 ({odd_count/5*100:.0f}%)")
    
    # Number characteristics
    print(f"\nNumber Characteristics:")
    print(f"   Numbers: {numbers}")
    print(f"   Sum: {sum(numbers)}")
    print(f"   Average: {sum(numbers)/5:.1f}")
    print(f"   Range span: {max(numbers) - min(numbers)}")
    print(f"   Lucky Number: {lucky}")
    
    # Consecutive analysis
    consecutive = []
    for i in range(len(numbers)-1):
        if numbers[i+1] - numbers[i] == 1:
            consecutive.append((numbers[i], numbers[i+1]))
    
    if consecutive:
        print(f"   Consecutive pairs: {consecutive}")
    else:
        print(f"   No consecutive pairs")

def strategy_performance_summary(results):
    """Summarize performance by strategy type"""
    
    print("\n📈 STRATEGY PERFORMANCE SUMMARY:")
    print("=" * 40)
    
    strategy_stats = {}
    
    for result in results:
        strategy = result['combination']['strategy']
        if strategy not in strategy_stats:
            strategy_stats[strategy] = {
                'total_score': 0,
                'count': 0,
                'best_score': 0,
                'lucky_matches': 0
            }
        
        strategy_stats[strategy]['total_score'] += result['match_score']
        strategy_stats[strategy]['count'] += 1
        strategy_stats[strategy]['best_score'] = max(strategy_stats[strategy]['best_score'], result['match_score'])
        if result['lucky_match']:
            strategy_stats[strategy]['lucky_matches'] += 1
    
    # Sort by average performance
    sorted_strategies = sorted(strategy_stats.items(), 
                             key=lambda x: x[1]['total_score']/x[1]['count'], 
                             reverse=True)
    
    for strategy, stats in sorted_strategies:
        avg_score = stats['total_score'] / stats['count']
        print(f"{strategy}:")
        print(f"   Average Score: {avg_score:.1f}/13")
        print(f"   Best Score: {stats['best_score']}/13")
        print(f"   Lucky Matches: {stats['lucky_matches']}/{stats['count']}")
        print()

def main():
    """Main analysis function"""
    
    # Analyze all combinations
    results = analyze_all_combinations()
    
    # Find best performers
    best_performers = find_best_performers(results)
    
    # Analyze winning patterns
    actual_results = get_may26_actual_results()
    analyze_winning_patterns(actual_results)
    
    # Strategy performance summary
    strategy_performance_summary(results)
    
    print("\n🚀 ANALYSIS COMPLETE!")
    print("=" * 30)
    print("Your combinations have been analyzed against the May 26 results!")

if __name__ == "__main__":
    main()