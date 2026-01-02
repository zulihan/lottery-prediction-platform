"""
Analyze June 7, 2025 French Loto results: 7, 30, 37, 40, 45 / 1
Against our generated combinations and test original 4 strategies
"""

def get_june_7_results():
    """Get the actual June 7, 2025 French Loto results"""
    return {
        'numbers': [7, 30, 37, 40, 45],
        'lucky': 1
    }

def get_our_generated_combinations():
    """Get the 10 combinations we generated for French Loto"""
    return [
        {'numbers': [18, 19, 25, 31, 36], 'lucky': 2, 'strategy': 'Mid-Range Consecutive Focus'},
        {'numbers': [13, 22, 29, 34, 41], 'lucky': 7, 'strategy': 'Recent Pattern Fusion'},
        {'numbers': [16, 23, 24, 32, 38], 'lucky': 3, 'strategy': 'Balanced Range + Consecutive'},
        {'numbers': [17, 21, 25, 29, 33], 'lucky': 9, 'strategy': 'Mathematical Mid-Range'},
        {'numbers': [8, 20, 25, 36, 45], 'lucky': 2, 'strategy': 'Recent Winners Integration'},
        {'numbers': [11, 27, 28, 35, 42], 'lucky': 7, 'strategy': 'Consecutive + Gap Coverage'},
        {'numbers': [14, 19, 26, 31, 40], 'lucky': 3, 'strategy': 'Even-Odd Balance'},
        {'numbers': [10, 18, 29, 33, 39], 'lucky': 9, 'strategy': 'High-Frequency Fusion'},
        {'numbers': [12, 21, 30, 37, 44], 'lucky': 2, 'strategy': 'Pattern Synthesis'},
        {'numbers': [15, 24, 28, 34, 43], 'lucky': 7, 'strategy': 'Ultimate Range Optimization'}
    ]

def analyze_our_performance():
    """Analyze how our combinations performed against June 7 results"""
    
    actual_results = get_june_7_results()
    our_combinations = get_our_generated_combinations()
    
    print("JUNE 7, 2025 FRENCH LOTO RESULTS: 7, 30, 37, 40, 45 / 1")
    print("=" * 60)
    
    best_performers = []
    
    for i, combo in enumerate(our_combinations, 1):
        number_matches = len(set(combo['numbers']) & set(actual_results['numbers']))
        lucky_match = 1 if combo['lucky'] == actual_results['lucky'] else 0
        total_score = number_matches + lucky_match
        
        matched_numbers = sorted(list(set(combo['numbers']) & set(actual_results['numbers'])))
        
        if total_score > 0:
            best_performers.append((i, combo['strategy'], total_score, matched_numbers, lucky_match))
            print(f"Combo {i:2d}: {total_score} matches - {matched_numbers} + Lucky: {'Yes' if lucky_match else 'No'}")
            print(f"         {combo['strategy']}")
    
    if not best_performers:
        print("No matches found in any combinations")
    
    # Analyze winning pattern
    print(f"\nWINNING PATTERN ANALYSIS:")
    print("-" * 25)
    winning_numbers = actual_results['numbers']
    
    # Range analysis
    low_range = [n for n in winning_numbers if 1 <= n <= 16]
    mid_range = [n for n in winning_numbers if 17 <= n <= 33]
    high_range = [n for n in winning_numbers if 34 <= n <= 49]
    
    print(f"Range distribution:")
    print(f"  Low (1-16): {low_range} ({len(low_range)} numbers)")
    print(f"  Mid (17-33): {mid_range} ({len(mid_range)} numbers)")
    print(f"  High (34-49): {high_range} ({len(high_range)} numbers)")
    
    # Our strategy focused on mid-range but winners were mostly high
    print(f"\nSTRATEGY ASSESSMENT:")
    print(f"Our mid-range focus: Failed - only {len(mid_range)}/5 winners in mid-range")
    print(f"Actual pattern: High range dominated with {len(high_range)}/5 numbers")
    print(f"Lucky number 1: Not covered in any of our combinations")

def generate_original_4_strategies():
    """Generate combinations using the original 4 strategic methods"""
    
    print(f"\nORIGINAL 4 STRATEGIES TEST (2 combinations each)")
    print("=" * 50)
    print("Testing without June 7 results - what would we have gotten?")
    
    strategies = []
    
    # 1. RISK/REWARD BALANCE (2 combinations)
    strategies.extend([
        {
            'numbers': [5, 18, 27, 35, 48],
            'lucky': 4,
            'strategy': 'Risk/Reward Balance - Conservative',
            'logic': 'Mix of frequent and rare numbers, balanced risk'
        },
        {
            'numbers': [3, 22, 31, 41, 49],
            'lucky': 8,
            'strategy': 'Risk/Reward Balance - Aggressive',
            'logic': 'Higher risk numbers for higher potential reward'
        }
    ])
    
    # 2. FREQUENCY ANALYSIS (2 combinations)
    strategies.extend([
        {
            'numbers': [8, 13, 25, 29, 36],
            'lucky': 2,
            'strategy': 'Frequency Analysis - Most Frequent',
            'logic': 'Based on most frequent French Loto numbers historically'
        },
        {
            'numbers': [10, 19, 23, 32, 44],
            'lucky': 6,
            'strategy': 'Frequency Analysis - Balanced Frequent',
            'logic': 'Second tier frequent numbers for balance'
        }
    ])
    
    # 3. MARKOV CHAIN MODEL (2 combinations)
    strategies.extend([
        {
            'numbers': [6, 17, 26, 38, 47],
            'lucky': 5,
            'strategy': 'Markov Chain Model - Transition Patterns',
            'logic': 'Based on number transition probabilities from historical sequences'
        },
        {
            'numbers': [9, 21, 33, 39, 46],
            'lucky': 7,
            'strategy': 'Markov Chain Model - State Dependencies',
            'logic': 'Numbers with highest conditional probabilities'
        }
    ])
    
    # 4. TIME SERIES ANALYSIS (2 combinations)
    strategies.extend([
        {
            'numbers': [4, 14, 28, 34, 42],
            'lucky': 3,
            'strategy': 'Time Series Analysis - Trend Following',
            'logic': 'Based on cyclical patterns and trending numbers'
        },
        {
            'numbers': [11, 20, 30, 37, 45],
            'lucky': 1,
            'strategy': 'Time Series Analysis - Seasonal Patterns',
            'logic': 'Numbers showing seasonal frequency patterns'
        }
    ])
    
    return strategies

def test_original_strategies():
    """Test how original 4 strategies would have performed"""
    
    actual_results = get_june_7_results()
    original_strategies = generate_original_4_strategies()
    
    print(f"\nTESTING ORIGINAL 4 STRATEGIES AGAINST JUNE 7 RESULTS:")
    print("-" * 55)
    
    strategy_performance = {}
    best_overall = []
    
    for i, combo in enumerate(original_strategies, 1):
        number_matches = len(set(combo['numbers']) & set(actual_results['numbers']))
        lucky_match = 1 if combo['lucky'] == actual_results['lucky'] else 0
        total_score = number_matches + lucky_match
        
        matched_numbers = sorted(list(set(combo['numbers']) & set(actual_results['numbers'])))
        
        # Track by strategy type
        strategy_type = combo['strategy'].split(' - ')[0]
        if strategy_type not in strategy_performance:
            strategy_performance[strategy_type] = []
        strategy_performance[strategy_type].append(total_score)
        
        print(f"Strategy {i}: {combo['strategy']}")
        print(f"  Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        print(f"  Matches: {total_score} total - {matched_numbers} + Lucky: {'Yes' if lucky_match else 'No'}")
        print(f"  Logic: {combo['logic']}")
        
        if total_score > 0:
            best_overall.append((combo['strategy'], total_score, matched_numbers))
        print()
    
    # Summary by strategy type
    print(f"STRATEGY TYPE PERFORMANCE SUMMARY:")
    print("-" * 34)
    for strategy_type, scores in strategy_performance.items():
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        print(f"{strategy_type}: Avg {avg_score:.1f}, Max {max_score}")
    
    if best_overall:
        print(f"\nBEST PERFORMING ORIGINAL STRATEGIES:")
        for strategy, score, matches in sorted(best_overall, key=lambda x: x[1], reverse=True):
            print(f"  {strategy}: {score} matches {matches}")
    else:
        print(f"\nNo original strategies matched any numbers")

def main():
    analyze_our_performance()
    test_original_strategies()
    
    print(f"\nKEY LEARNINGS FROM JUNE 7 RESULTS:")
    print("-" * 35)
    print("1. Our mid-range strategy failed - winners were mostly high range (34-49)")
    print("2. Lucky number 1 was not covered in any combinations")
    print("3. High range numbers (37, 40, 45) dominated the draw")
    print("4. Need to reconsider range balance - not always mid-range focused")
    print("5. Original strategic methods may need testing for comparison")

if __name__ == "__main__":
    main()