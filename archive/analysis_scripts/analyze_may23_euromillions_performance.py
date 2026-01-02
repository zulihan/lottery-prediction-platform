"""
Analyze the performance of our generated Euromillions combinations 
against the May 23, 2025 results: 10, 29, 43, 46, 49 / Stars: 7, 12
"""

def get_may23_actual_results():
    """Get the actual May 23, 2025 Euromillions results"""
    return {
        'numbers': [10, 29, 43, 46, 49],
        'stars': [7, 12]
    }

def get_focused_strategy_combinations():
    """Get the focused strategy combinations (Set 1)"""
    return [
        {'numbers': [3, 13, 29, 38, 50], 'stars': [2, 3], 'strategy': 'Hot Numbers Focus'},
        {'numbers': [1, 15, 25, 26, 42], 'stars': [3, 8], 'strategy': 'Balanced Hot-Cold Mix'},
        {'numbers': [1, 8, 25, 27, 44], 'stars': [8, 9], 'strategy': 'May 20 Winners Enhanced'},
        {'numbers': [9, 11, 14, 16, 32], 'stars': [5, 8], 'strategy': 'Conservative Frequency'},
        {'numbers': [6, 10, 17, 19, 27], 'stars': [2, 6], 'strategy': 'Aggressive Hot Strategy'},
        {'numbers': [2, 5, 11, 16, 37], 'stars': [3, 6], 'strategy': 'Range-Optimized Strategy'},
        {'numbers': [2, 10, 18, 23, 37], 'stars': [6, 12], 'strategy': 'Mixed Balance Approach'},
        {'numbers': [5, 12, 21, 23, 29], 'stars': [2, 9], 'strategy': 'Strategic Coverage'}
    ]

def get_fibonacci_hybrid_combinations():
    """Get the Fibonacci-Filtered Hybrid Strategy combinations (Set 2)"""
    return [
        {'numbers': [3, 8, 13, 21, 29], 'stars': [5, 8], 'strategy': 'Fibonacci-Filtered Frequency Analysis', 'score': 100},
        {'numbers': [1, 13, 21, 25, 44], 'stars': [2, 3], 'strategy': 'Fibonacci-Filtered Frequency Analysis', 'score': 100},
        {'numbers': [19, 22, 25, 36, 37], 'stars': [11, 12], 'strategy': 'Risk/Reward Balance', 'score': 74},
        {'numbers': [2, 3, 5, 8, 12], 'stars': [3, 9], 'strategy': 'Fibonacci-Filtered Markov Chain', 'score': 100},
        {'numbers': [8, 13, 21, 34, 42], 'stars': [1, 7], 'strategy': 'Fibonacci-Filtered Time Series', 'score': 100},
        {'numbers': [5, 8, 13, 29, 45], 'stars': [4, 11], 'strategy': 'Fibonacci-Filtered Hybrid Mix', 'score': 100},
        {'numbers': [1, 8, 21, 34, 47], 'stars': [6, 10], 'strategy': 'Ultimate Fibonacci Fusion', 'score': 100},
        {'numbers': [3, 5, 13, 25, 41], 'stars': [2, 7], 'strategy': 'Mathematical Precision Blend', 'score': 100}
    ]

def analyze_combination_performance(combination, actual_results, set_name):
    """Analyze how well a combination performed against actual results"""
    
    combo_numbers = set(combination['numbers'])
    actual_numbers = set(actual_results['numbers'])
    
    combo_stars = set(combination['stars'])
    actual_stars = set(actual_results['stars'])
    
    # Count matches
    number_matches = len(combo_numbers.intersection(actual_numbers))
    matched_numbers = list(combo_numbers.intersection(actual_numbers))
    
    star_matches = len(combo_stars.intersection(actual_stars))
    matched_stars = list(combo_stars.intersection(actual_stars))
    
    # Calculate performance score
    performance_score = (number_matches * 2) + (star_matches * 3)  # Numbers worth 2, stars worth 3
    max_possible = 16  # 5 numbers * 2 + 2 stars * 3 = 16
    
    return {
        'combination': combination,
        'set_name': set_name,
        'number_matches': number_matches,
        'matched_numbers': matched_numbers,
        'star_matches': star_matches,
        'matched_stars': matched_stars,
        'performance_score': performance_score,
        'percentage': (performance_score / max_possible) * 100
    }

def analyze_all_combinations():
    """Analyze all combinations against May 23 results"""
    
    actual_results = get_may23_actual_results()
    focused_combos = get_focused_strategy_combinations()
    fibonacci_combos = get_fibonacci_hybrid_combinations()
    
    print("🎯 MAY 23, 2025 EUROMILLIONS RESULTS ANALYSIS")
    print("=" * 65)
    print(f"Actual Results: {actual_results['numbers']} / Stars: {actual_results['stars']}")
    print("=" * 65)
    
    all_results = []
    
    # Analyze Focused Strategy (Set 1)
    print("\n📊 FOCUSED STRATEGY COMBINATIONS PERFORMANCE:")
    print("-" * 55)
    
    for i, combo in enumerate(focused_combos, 1):
        result = analyze_combination_performance(combo, actual_results, "Focused Strategy")
        all_results.append(result)
        
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print(f"    Number Matches: {result['number_matches']} → {result['matched_numbers']}")
        print(f"    Star Matches: {result['star_matches']} → {result['matched_stars']}")
        print(f"    Performance: {result['performance_score']}/16 ({result['percentage']:.1f}%)")
        if result['number_matches'] > 0 or result['star_matches'] > 0:
            print(f"    ⭐ SUCCESS!")
        print()
    
    # Analyze Fibonacci Hybrid Strategy (Set 2)
    print("\n📊 FIBONACCI-FILTERED HYBRID STRATEGY PERFORMANCE:")
    print("-" * 60)
    
    for i, combo in enumerate(fibonacci_combos, 1):
        result = analyze_combination_performance(combo, actual_results, "Fibonacci Hybrid")
        all_results.append(result)
        
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print(f"    Number Matches: {result['number_matches']} → {result['matched_numbers']}")
        print(f"    Star Matches: {result['star_matches']} → {result['matched_stars']}")
        print(f"    Performance: {result['performance_score']}/16 ({result['percentage']:.1f}%)")
        if 'score' in combo:
            print(f"    Generation Score: {combo['score']}/100")
        if result['number_matches'] > 0 or result['star_matches'] > 0:
            print(f"    ⭐ SUCCESS!")
        print()
    
    return all_results

def find_best_performers(results):
    """Find the best performing combinations"""
    
    # Sort by performance score
    sorted_results = sorted(results, key=lambda x: x['performance_score'], reverse=True)
    
    print("🏆 TOP PERFORMING COMBINATIONS:")
    print("=" * 45)
    
    top_performers = [r for r in sorted_results if r['performance_score'] > 0]
    
    if not top_performers:
        print("❌ No combinations achieved any matches with the winning numbers.")
        print("\n🔍 CLOSEST COMBINATIONS (by highest potential):")
        top_5 = sorted_results[:5]
    else:
        print(f"✅ {len(top_performers)} combinations achieved matches!")
        top_5 = top_performers[:5] if len(top_performers) >= 5 else top_performers
    
    for i, result in enumerate(top_5, 1):
        combo = result['combination']
        print(f"{i}. {combo['strategy']} ({result['set_name']})")
        print(f"   Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print(f"   Matches: {result['number_matches']} numbers {result['matched_numbers']}, {result['star_matches']} stars {result['matched_stars']}")
        print(f"   Performance: {result['performance_score']}/16 ({result['percentage']:.1f}%)")
        print()
    
    return top_5

def analyze_winning_patterns(actual_results):
    """Analyze what made the May 23 winning numbers special"""
    
    numbers = actual_results['numbers']
    stars = actual_results['stars']
    
    print("🔍 MAY 23 WINNING NUMBER ANALYSIS:")
    print("=" * 45)
    
    # Range analysis
    low_count = len([n for n in numbers if n <= 17])
    mid_count = len([n for n in numbers if 18 <= n <= 34])
    high_count = len([n for n in numbers if n >= 35])
    
    print(f"Range Distribution:")
    print(f"   Low (1-17): {low_count}/5 ({low_count/5*100:.0f}%) → {[n for n in numbers if n <= 17]}")
    print(f"   Mid (18-34): {mid_count}/5 ({mid_count/5*100:.0f}%) → {[n for n in numbers if 18 <= n <= 34]}")
    print(f"   High (35-50): {high_count}/5 ({high_count/5*100:.0f}%) → {[n for n in numbers if n >= 35]}")
    
    # Even/odd analysis
    even_count = len([n for n in numbers if n % 2 == 0])
    odd_count = len([n for n in numbers if n % 2 == 1])
    
    print(f"\nEven/Odd Distribution:")
    print(f"   Even: {even_count}/5 ({even_count/5*100:.0f}%) → {[n for n in numbers if n % 2 == 0]}")
    print(f"   Odd: {odd_count}/5 ({odd_count/5*100:.0f}%) → {[n for n in numbers if n % 2 == 1]}")
    
    # Number characteristics
    print(f"\nNumber Characteristics:")
    print(f"   Numbers: {numbers}")
    print(f"   Sum: {sum(numbers)}")
    print(f"   Average: {sum(numbers)/5:.1f}")
    print(f"   Range span: {max(numbers) - min(numbers)}")
    print(f"   Stars: {stars}")
    print(f"   High star presence: {len([s for s in stars if s >= 7])}/2")

def strategy_performance_comparison(results):
    """Compare performance between the two strategy sets"""
    
    print("\n📈 STRATEGY SET COMPARISON:")
    print("=" * 35)
    
    focused_results = [r for r in results if r['set_name'] == "Focused Strategy"]
    fibonacci_results = [r for r in results if r['set_name'] == "Fibonacci Hybrid"]
    
    # Calculate averages
    focused_avg = sum([r['performance_score'] for r in focused_results]) / len(focused_results)
    fibonacci_avg = sum([r['performance_score'] for r in fibonacci_results]) / len(fibonacci_results)
    
    # Count successful combinations
    focused_hits = len([r for r in focused_results if r['performance_score'] > 0])
    fibonacci_hits = len([r for r in fibonacci_results if r['performance_score'] > 0])
    
    print(f"Focused Strategy (Set 1):")
    print(f"   Average Performance: {focused_avg:.1f}/16")
    print(f"   Successful Combinations: {focused_hits}/8")
    print(f"   Success Rate: {focused_hits/8*100:.1f}%")
    
    print(f"\nFibonacci Hybrid Strategy (Set 2):")
    print(f"   Average Performance: {fibonacci_avg:.1f}/16")
    print(f"   Successful Combinations: {fibonacci_hits}/8")
    print(f"   Success Rate: {fibonacci_hits/8*100:.1f}%")
    
    if focused_avg > fibonacci_avg:
        print(f"\n🏆 Focused Strategy performed better overall!")
    elif fibonacci_avg > focused_avg:
        print(f"\n🏆 Fibonacci Hybrid Strategy performed better overall!")
    else:
        print(f"\n🤝 Both strategies performed equally!")

def main():
    """Main analysis function"""
    
    # Analyze all combinations
    results = analyze_all_combinations()
    
    # Find best performers
    best_performers = find_best_performers(results)
    
    # Analyze winning patterns
    actual_results = get_may23_actual_results()
    analyze_winning_patterns(actual_results)
    
    # Compare strategy performance
    strategy_performance_comparison(results)
    
    print("\n🚀 ANALYSIS COMPLETE!")
    print("=" * 30)
    print("Your combinations have been analyzed against the May 23 results!")

if __name__ == "__main__":
    main()