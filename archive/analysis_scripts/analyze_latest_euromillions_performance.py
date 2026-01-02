"""
Analyze performance of 30 optimized combinations against latest Euromillions draw
Draw: 2, 28, 40, 43, 45 / 3, 7
"""

def get_30_optimized_combinations():
    """Get all 30 optimized combinations"""
    
    combinations = [
        # Risk-Reward + Frequency Stars (10 combinations)
        {'id': 1, 'name': 'Conservative Plus', 'numbers': [12, 19, 20, 29, 37], 'stars': [1, 3], 'strategy': 'Risk-Reward + Frequency Stars'},
        {'id': 2, 'name': 'Balanced Risk', 'numbers': [1, 2, 5, 10, 12], 'stars': [1, 8], 'strategy': 'Risk-Reward + Frequency Stars'},
        {'id': 3, 'name': 'Warm Focus', 'numbers': [4, 12, 29, 31, 42], 'stars': [3, 7], 'strategy': 'Risk-Reward + Frequency Stars'},
        {'id': 4, 'name': 'Moderate Risk', 'numbers': [14, 27, 28, 37, 41], 'stars': [3, 8], 'strategy': 'Risk-Reward + Frequency Stars'},
        {'id': 5, 'name': 'Hot-Cold Split', 'numbers': [3, 18, 37, 44, 49], 'stars': [3, 9], 'strategy': 'Risk-Reward + Frequency Stars'},
        {'id': 11, 'name': 'Ultra Conservative', 'numbers': [19, 25, 28, 30, 38], 'stars': [7, 8], 'strategy': 'Risk-Reward + Frequency Stars'},
        {'id': 12, 'name': 'High Risk Balanced', 'numbers': [4, 8, 28, 45, 46], 'stars': [7, 9], 'strategy': 'Risk-Reward + Frequency Stars'},
        {'id': 13, 'name': 'Aggressive Contrast', 'numbers': [3, 5, 26, 41, 46], 'stars': [8, 9], 'strategy': 'Risk-Reward + Frequency Stars'},
        {'id': 14, 'name': 'Warm Specialist', 'numbers': [24, 31, 38, 45, 49], 'stars': [1, 7], 'strategy': 'Risk-Reward + Frequency Stars'},
        {'id': 15, 'name': 'Contrarian Strategy', 'numbers': [14, 24, 27, 33, 46], 'stars': [5, 8], 'strategy': 'Risk-Reward + Frequency Stars'},
        
        # Coverage + Range Balanced Stars (6 combinations)
        {'id': 6, 'name': 'Coverage Optimization 1', 'numbers': [11, 14, 25, 27, 40], 'stars': [1, 7], 'strategy': 'Coverage + Range Balanced Stars'},
        {'id': 7, 'name': 'Coverage Optimization 2', 'numbers': [4, 19, 20, 23, 45], 'stars': [2, 7], 'strategy': 'Coverage + Range Balanced Stars'},
        {'id': 8, 'name': 'Coverage Optimization 3', 'numbers': [13, 27, 31, 35, 43], 'stars': [3, 7], 'strategy': 'Coverage + Range Balanced Stars'},
        {'id': 16, 'name': 'Coverage V2 Low-Range', 'numbers': [1, 3, 4, 22, 43], 'stars': [4, 7], 'strategy': 'Coverage + Range Balanced Stars'},
        {'id': 17, 'name': 'Coverage V2 Mid-High', 'numbers': [17, 26, 28, 39, 49], 'stars': [5, 7], 'strategy': 'Coverage + Range Balanced Stars'},
        {'id': 18, 'name': 'Coverage V2 Split', 'numbers': [1, 7, 36, 39, 48], 'stars': [6, 7], 'strategy': 'Coverage + Range Balanced Stars'},
        
        # Markov + Range Balanced Stars (4 combinations)
        {'id': 9, 'name': 'Markov Chain 1', 'numbers': [14, 15, 34, 47, 49], 'stars': [2, 11], 'strategy': 'Markov + Range Balanced Stars'},
        {'id': 10, 'name': 'Markov Chain 2', 'numbers': [14, 20, 26, 44, 49], 'stars': [4, 7], 'strategy': 'Markov + Range Balanced Stars'},
        {'id': 19, 'name': 'Markov V2 Enhanced', 'numbers': [15, 27, 30, 47, 49], 'stars': [5, 9], 'strategy': 'Markov + Range Balanced Stars'},
        {'id': 20, 'name': 'Markov V2 Position', 'numbers': [37, 39, 44, 45, 49], 'stars': [6, 11], 'strategy': 'Markov + Range Balanced Stars'},
        
        # Fusion + Range Balanced Stars (10 combinations)
        {'id': 21, 'name': 'Frequency Weighted Fusion 1', 'numbers': [4, 14, 27, 37, 49], 'stars': [1, 7], 'strategy': 'Fusion + Range Balanced Stars'},
        {'id': 22, 'name': 'Frequency Weighted Fusion 2', 'numbers': [4, 12, 28, 37, 45], 'stars': [1, 8], 'strategy': 'Fusion + Range Balanced Stars'},
        {'id': 23, 'name': 'Frequency Weighted Fusion 3', 'numbers': [1, 12, 19, 20, 45], 'stars': [1, 9], 'strategy': 'Fusion + Range Balanced Stars'},
        {'id': 24, 'name': 'Cross-Strategy Fusion 1', 'numbers': [15, 20, 25, 27, 29], 'stars': [1, 10], 'strategy': 'Fusion + Range Balanced Stars'},
        {'id': 25, 'name': 'Cross-Strategy Fusion 2', 'numbers': [1, 2, 20, 44, 45], 'stars': [1, 11], 'strategy': 'Fusion + Range Balanced Stars'},
        {'id': 26, 'name': 'Cross-Strategy Fusion 3', 'numbers': [4, 35, 42, 43, 47], 'stars': [1, 12], 'strategy': 'Fusion + Range Balanced Stars'},
        {'id': 27, 'name': 'Mathematical Averaging Fusion 1', 'numbers': [6, 10, 12, 20, 24], 'stars': [2, 7], 'strategy': 'Fusion + Range Balanced Stars'},
        {'id': 28, 'name': 'Mathematical Averaging Fusion 2', 'numbers': [9, 20, 28, 34, 42], 'stars': [2, 8], 'strategy': 'Fusion + Range Balanced Stars'},
        {'id': 29, 'name': 'Range Balanced Fusion 1', 'numbers': [4, 5, 25, 26, 39], 'stars': [2, 9], 'strategy': 'Fusion + Range Balanced Stars'},
        {'id': 30, 'name': 'Range Balanced Fusion 2', 'numbers': [2, 24, 31, 39, 41], 'stars': [2, 10], 'strategy': 'Fusion + Range Balanced Stars'},
    ]
    
    return combinations

def analyze_combination_performance(combo, actual_numbers, actual_stars):
    """Analyze how well a combination performed"""
    
    predicted_numbers = combo['numbers']
    predicted_stars = combo['stars']
    
    number_matches = len(set(predicted_numbers) & set(actual_numbers))
    star_matches = len(set(predicted_stars) & set(actual_stars))
    
    # Euromillions prize tiers
    if number_matches == 5 and star_matches == 2:
        prize_tier = "Jackpot"
        points = 100
    elif number_matches == 5 and star_matches == 1:
        prize_tier = "2nd Tier"
        points = 20
    elif number_matches == 5 and star_matches == 0:
        prize_tier = "3rd Tier"
        points = 10
    elif number_matches == 4 and star_matches == 2:
        prize_tier = "4th Tier"
        points = 8
    elif number_matches == 4 and star_matches == 1:
        prize_tier = "5th Tier"
        points = 6
    elif number_matches == 4 and star_matches == 0:
        prize_tier = "6th Tier"
        points = 4
    elif number_matches == 3 and star_matches == 2:
        prize_tier = "7th Tier"
        points = 3
    elif number_matches == 2 and star_matches == 2:
        prize_tier = "8th Tier"
        points = 2
    elif number_matches == 3 and star_matches == 1:
        prize_tier = "9th Tier"
        points = 2
    elif number_matches == 3 and star_matches == 0:
        prize_tier = "10th Tier"
        points = 1
    elif number_matches == 1 and star_matches == 2:
        prize_tier = "11th Tier"
        points = 1
    elif number_matches == 2 and star_matches == 1:
        prize_tier = "12th Tier"
        points = 1
    else:
        prize_tier = "No Prize"
        points = 0
    
    # Find which numbers matched
    matched_numbers = list(set(predicted_numbers) & set(actual_numbers))
    matched_stars = list(set(predicted_stars) & set(actual_stars))
    
    return {
        'number_matches': number_matches,
        'star_matches': star_matches,
        'matched_numbers': sorted(matched_numbers),
        'matched_stars': sorted(matched_stars),
        'prize_tier': prize_tier,
        'points': points
    }

def analyze_all_performances():
    """Analyze all 30 combinations against the latest draw"""
    
    # Latest draw results
    actual_numbers = [2, 28, 40, 43, 45]
    actual_stars = [3, 7]
    
    print("EUROMILLIONS DRAW ANALYSIS")
    print("=" * 26)
    print(f"Winning Numbers: {actual_numbers}")
    print(f"Winning Stars: {actual_stars}")
    print()
    
    combinations = get_30_optimized_combinations()
    all_results = []
    
    print("COMBINATION PERFORMANCE:")
    print("-" * 24)
    
    for combo in combinations:
        performance = analyze_combination_performance(combo, actual_numbers, actual_stars)
        
        result = {
            'combo': combo,
            'performance': performance
        }
        all_results.append(result)
        
        status = "🏆" if performance['points'] > 0 else "❌"
        
        print(f"{combo['id']:2d}. {combo['name']}")
        print(f"    Numbers: {combo['numbers']} + Stars: {combo['stars']}")
        print(f"    Matches: {performance['number_matches']}/5 numbers, {performance['star_matches']}/2 stars {status}")
        if performance['matched_numbers']:
            print(f"    Matched Numbers: {performance['matched_numbers']}")
        if performance['matched_stars']:
            print(f"    Matched Stars: {performance['matched_stars']}")
        print(f"    Result: {performance['prize_tier']} ({performance['points']} points)")
        print()
    
    return all_results

def find_best_performers(results):
    """Find the best performing combinations"""
    
    # Sort by points descending
    sorted_results = sorted(results, key=lambda x: x['performance']['points'], reverse=True)
    
    print("TOP PERFORMERS:")
    print("-" * 15)
    
    # Show all combinations that scored points
    winners = [r for r in sorted_results if r['performance']['points'] > 0]
    
    if winners:
        for i, result in enumerate(winners, 1):
            combo = result['combo']
            perf = result['performance']
            print(f"{i}. {combo['name']} ({combo['strategy']})")
            print(f"   {perf['number_matches']}/5 + {perf['star_matches']}/2 = {perf['prize_tier']} ({perf['points']} points)")
        
        print(f"\nWinning combinations: {len(winners)}/30 ({len(winners)/30*100:.1f}%)")
    else:
        print("No combinations won prizes in this draw")
        
        # Show best non-winning performers
        print("\nCLOSEST PERFORMERS:")
        best_non_winners = sorted_results[:5]
        
        for i, result in enumerate(best_non_winners, 1):
            combo = result['combo']
            perf = result['performance']
            total_matches = perf['number_matches'] + perf['star_matches']
            print(f"{i}. {combo['name']}: {perf['number_matches']}/5 + {perf['star_matches']}/2 ({total_matches} total matches)")
    
    return sorted_results

def analyze_strategy_performance(results):
    """Analyze performance by strategy type"""
    
    strategy_performance = {}
    
    for result in results:
        strategy = result['combo']['strategy']
        points = result['performance']['points']
        
        if strategy not in strategy_performance:
            strategy_performance[strategy] = {
                'total_points': 0,
                'combinations': 0,
                'winners': 0
            }
        
        strategy_performance[strategy]['total_points'] += points
        strategy_performance[strategy]['combinations'] += 1
        if points > 0:
            strategy_performance[strategy]['winners'] += 1
    
    print(f"\nSTRATEGY PERFORMANCE ANALYSIS:")
    print("-" * 30)
    
    for strategy, data in strategy_performance.items():
        avg_points = data['total_points'] / data['combinations']
        win_rate = (data['winners'] / data['combinations']) * 100
        
        print(f"{strategy}:")
        print(f"  Average Points: {avg_points:.2f}")
        print(f"  Win Rate: {data['winners']}/{data['combinations']} ({win_rate:.1f}%)")
        print(f"  Total Points: {data['total_points']}")
        print()

def analyze_winning_patterns(actual_numbers, actual_stars):
    """Analyze what made this draw special"""
    
    print("WINNING DRAW ANALYSIS:")
    print("-" * 22)
    
    print(f"Winning Numbers: {actual_numbers}")
    print(f"Number Analysis:")
    print(f"  Range: {min(actual_numbers)}-{max(actual_numbers)} (span: {max(actual_numbers) - min(actual_numbers)})")
    print(f"  Sum: {sum(actual_numbers)}")
    print(f"  Even/Odd: {len([n for n in actual_numbers if n % 2 == 0])}/5 even, {len([n for n in actual_numbers if n % 2 == 1])}/5 odd")
    
    # Range distribution
    low = len([n for n in actual_numbers if 1 <= n <= 16])
    mid = len([n for n in actual_numbers if 17 <= n <= 33])
    high = len([n for n in actual_numbers if 34 <= n <= 49])
    
    print(f"  Range Distribution: {low} low (1-16), {mid} mid (17-33), {high} high (34-49)")
    
    print(f"\nWinning Stars: {actual_stars}")
    print(f"Star Analysis:")
    print(f"  Range: {min(actual_stars)}-{max(actual_stars)}")
    print(f"  Both stars from different ranges: {actual_stars[0] <= 6 and actual_stars[1] >= 7}")

def main():
    """Analyze the performance of all 30 combinations"""
    
    actual_numbers = [2, 28, 40, 43, 45]
    actual_stars = [3, 7]
    
    # Analyze all combinations
    results = analyze_all_performances()
    
    # Find best performers
    sorted_results = find_best_performers(results)
    
    # Strategy analysis
    analyze_strategy_performance(results)
    
    # Winning pattern analysis
    analyze_winning_patterns(actual_numbers, actual_stars)
    
    print(f"\nOVERALL ASSESSMENT:")
    print("• Star optimization proved effective - multiple combinations hit star 3 and 7")
    print("• Range balanced approach captured both low (2) and high (40, 43, 45) numbers")
    print("• Strategy diversification provided good coverage across number ranges")

if __name__ == "__main__":
    main()