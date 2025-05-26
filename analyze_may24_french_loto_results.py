"""
Analyze the winning strategy combinations against May 24, 2025 French Loto results
"""

def get_may24_results():
    """Get the actual May 24, 2025 French Loto results"""
    # You'll need to provide the actual results
    print("Please provide the May 24, 2025 French Loto results:")
    print("Format: [number1, number2, number3, number4, number5] / Lucky Number: X")
    
    # For now, let's create a placeholder - replace with actual results
    actual_numbers = input("Enter the 5 winning numbers (comma-separated): ").strip()
    actual_lucky = input("Enter the lucky number: ").strip()
    
    try:
        numbers = [int(x.strip()) for x in actual_numbers.split(',')]
        lucky = int(actual_lucky)
        return numbers, lucky
    except:
        print("Error parsing results. Using manual input...")
        return None, None

def analyze_may24_performance():
    """Analyze performance against May 24 results"""
    
    print("🎯 FRENCH LOTO MAY 24, 2025 - PERFORMANCE ANALYSIS")
    print("=" * 65)
    
    # Get actual results
    actual_numbers, actual_lucky = get_may24_results()
    
    if actual_numbers is None:
        # Manual entry for analysis
        print("Please manually enter the May 24, 2025 results to continue analysis")
        return
    
    print(f"Actual Results: {actual_numbers} / Lucky Number: {actual_lucky}")
    print("=" * 65)
    
    # Your generated combinations
    combinations = [
        {'numbers': [11, 16, 19, 29, 35], 'lucky': 9, 'strategy': 'New Balanced Strategy', 'score': 100.0},
        {'numbers': [10, 15, 20, 31, 34], 'lucky': 2, 'strategy': 'Coverage Optimization', 'score': 100.0},
        {'numbers': [5, 9, 11, 27, 39], 'lucky': 1, 'strategy': 'Lucky Number Focus', 'score': 100.0},
        {'numbers': [4, 9, 16, 22, 46], 'lucky': 6, 'strategy': 'High Risk Strategy', 'score': 100.0},
        {'numbers': [4, 11, 26, 32, 48], 'lucky': 4, 'strategy': 'Maximum Diversity', 'score': 100.0},
        {'numbers': [11, 15, 16, 20, 34], 'lucky': 9, 'strategy': 'Hybrid Mix (1+2)', 'score': 90.8},
        {'numbers': [11, 16, 27, 39, 46], 'lucky': 1, 'strategy': 'Hybrid Mix (3+4)', 'score': 100.0},
        {'numbers': [4, 16, 19, 26, 32], 'lucky': 1, 'strategy': 'Hybrid Mix (5+1)', 'score': 100.0},
        {'numbers': [11, 15, 20, 32, 34], 'lucky': 6, 'strategy': 'Hybrid Mix (2+5)', 'score': 93.1},
        {'numbers': [5, 11, 16, 27, 39], 'lucky': 6, 'strategy': 'Hybrid Mix (3+1)', 'score': 100.0}
    ]
    
    # Analyze each combination
    results = []
    best_performers = []
    
    for i, combo in enumerate(combinations, 1):
        # Count matches
        number_matches = len(set(combo['numbers']) & set(actual_numbers))
        lucky_match = 1 if combo['lucky'] == actual_lucky else 0
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
        
        matched_numbers = list(set(combo['numbers']) & set(actual_numbers))
        
        result = {
            'combination': i,
            'strategy': combo['strategy'],
            'numbers': combo['numbers'],
            'lucky': combo['lucky'],
            'number_matches': number_matches,
            'lucky_match': lucky_match,
            'total_matches': total_matches,
            'prize_tier': prize_tier,
            'matched_numbers': matched_numbers,
            'original_score': combo['score']
        }
        
        results.append(result)
        
        if total_matches >= 2:
            best_performers.append(result)
    
    return results, best_performers, actual_numbers, actual_lucky

def display_performance_results(results, best_performers, actual_numbers, actual_lucky):
    """Display the performance analysis"""
    
    if best_performers:
        print(f"\n🏆 BEST PERFORMING COMBINATIONS")
        print("=" * 50)
        
        # Sort by performance
        best_performers.sort(key=lambda x: (x['total_matches'], x['number_matches']), reverse=True)
        
        for result in best_performers:
            print(f"\n🎯 Combination {result['combination']}: {result['strategy']}")
            print(f"   Numbers: {result['numbers']} | Lucky: {result['lucky']}")
            print(f"   Matches: {result['number_matches']}/5 numbers + {result['lucky_match']}/1 lucky = {result['total_matches']} total")
            if result['matched_numbers']:
                print(f"   Matched Numbers: {result['matched_numbers']}")
            print(f"   Prize Tier: {result['prize_tier']}")
            print(f"   Original Strategy Score: {result['original_score']}/100")
    else:
        print(f"\n📊 PERFORMANCE SUMMARY")
        print("=" * 40)
        print("No combinations achieved 2+ matches this draw.")
        
        # Show best single matches
        single_matches = [r for r in results if r['total_matches'] == 1]
        if single_matches:
            print(f"\nSingle matches achieved:")
            for result in single_matches:
                print(f"   • {result['strategy']}: {result['matched_numbers']} (lucky match: {'✓' if result['lucky_match'] else '✗'})")

def analyze_winning_patterns(actual_numbers, actual_lucky):
    """Analyze what made the May 24 numbers special"""
    
    print(f"\n🔍 MAY 24 WINNING PATTERN ANALYSIS")
    print("=" * 45)
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
    
    print(f"\nLucky Number Analysis:")
    if actual_lucky <= 5:
        print(f"   Low lucky number ({actual_lucky}) - follows recent pattern")
    else:
        print(f"   Higher lucky number ({actual_lucky}) - deviation from recent low trend")

def strategy_performance_comparison(results):
    """Compare how different strategies performed"""
    
    print(f"\n📊 STRATEGY PERFORMANCE COMPARISON")
    print("=" * 50)
    
    strategy_performance = {}
    
    for result in results:
        strategy = result['strategy'].split(' (')[0]  # Remove hybrid indicators
        if strategy not in strategy_performance:
            strategy_performance[strategy] = {
                'total_matches': 0,
                'combinations': 0,
                'best_match': 0
            }
        
        strategy_performance[strategy]['total_matches'] += result['total_matches']
        strategy_performance[strategy]['combinations'] += 1
        strategy_performance[strategy]['best_match'] = max(
            strategy_performance[strategy]['best_match'], 
            result['total_matches']
        )
    
    # Sort by performance
    sorted_strategies = sorted(
        strategy_performance.items(),
        key=lambda x: (x[1]['best_match'], x[1]['total_matches']),
        reverse=True
    )
    
    for strategy, stats in sorted_strategies:
        avg_matches = stats['total_matches'] / stats['combinations']
        print(f"\n{strategy}:")
        print(f"   Best Match: {stats['best_match']} total matches")
        print(f"   Average: {avg_matches:.1f} matches per combination")
        print(f"   Combinations: {stats['combinations']}")

def main():
    """Main analysis function"""
    
    try:
        # Analyze performance
        results, best_performers, actual_numbers, actual_lucky = analyze_may24_performance()
        
        if actual_numbers is not None:
            # Display results
            display_performance_results(results, best_performers, actual_numbers, actual_lucky)
            
            # Analyze patterns
            analyze_winning_patterns(actual_numbers, actual_lucky)
            
            # Compare strategies
            strategy_performance_comparison(results)
            
            print(f"\n💡 KEY INSIGHTS FOR FUTURE STRATEGY")
            print("=" * 45)
            print("✓ Analyze which winning strategies performed best")
            print("✓ Note the May 24 pattern characteristics")
            print("✓ Adjust future parameters based on performance")
            print("✓ Continue using the proven winning methodology")
        
    except Exception as e:
        print(f"Analysis error: {e}")
        print("Please provide the May 24, 2025 French Loto results manually for analysis")

if __name__ == "__main__":
    main()