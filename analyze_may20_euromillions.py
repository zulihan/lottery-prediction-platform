"""
Analyze how our Euromillions combinations performed against the May 20, 2025 draw
and provide insights for future strategy improvements.
"""

import pandas as pd
from database import get_db_connection
from sqlalchemy import text

def get_may20_combinations():
    """
    Get all combinations we generated for the May 20 Euromillions draw
    """
    try:
        engine = get_db_connection()
        
        query = """
        SELECT 
            strategy,
            numbers,
            stars,
            score,
            created_at,
            target_draw_date
        FROM generated_combinations 
        WHERE (target_draw_date = '2025-05-20' OR 
               (created_at >= '2025-05-19' AND created_at <= '2025-05-21' AND target_draw_date = '2025-05-21'))
        ORDER BY score DESC
        """
        
        df = pd.read_sql(query, engine)
            
        print(f"Found {len(df)} combinations for May 20, 2025 Euromillions draw")
        return df
        
    except Exception as e:
        print(f"Error retrieving combinations: {e}")
        return pd.DataFrame()

def get_may20_actual_results():
    """
    The actual Euromillions results for May 20, 2025:
    Numbers: 1, 8, 13, 29, 47
    Stars: 5, 6
    """
    return {
        'numbers': [1, 8, 13, 29, 47],
        'stars': [5, 6]
    }

def analyze_combination_performance(combination_row, actual_results):
    """
    Analyze how well a single combination performed
    """
    try:
        # Parse the combination numbers and stars
        numbers_str = combination_row['numbers'].strip('[]')
        numbers = [int(x.strip()) for x in numbers_str.split(',')]
        
        stars_str = combination_row['stars'].strip('[]')
        stars = [int(x.strip()) for x in stars_str.split(',')]
        
        # Calculate matches
        number_matches = len(set(numbers) & set(actual_results['numbers']))
        star_matches = len(set(stars) & set(actual_results['stars']))
        
        # Determine prize tier
        prize_tier = get_prize_tier(number_matches, star_matches)
        
        return {
            'strategy': combination_row['strategy'],
            'numbers': numbers,
            'stars': stars,
            'score': combination_row['score'],
            'number_matches': number_matches,
            'star_matches': star_matches,
            'prize_tier': prize_tier,
            'created_at': combination_row['created_at']
        }
        
    except Exception as e:
        print(f"Error analyzing combination: {e}")
        return None

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
        if result is None:
            continue
            
        strategy = result['strategy']
        if strategy not in strategy_stats:
            strategy_stats[strategy] = {
                'total_combinations': 0,
                'total_number_matches': 0,
                'total_star_matches': 0,
                'best_performance': 0,
                'prizes_won': 0
            }
        
        stats = strategy_stats[strategy]
        stats['total_combinations'] += 1
        stats['total_number_matches'] += result['number_matches']
        stats['total_star_matches'] += result['star_matches']
        
        # Track best performance (total matches)
        total_matches = result['number_matches'] + result['star_matches']
        if total_matches > stats['best_performance']:
            stats['best_performance'] = total_matches
            
        # Count prizes
        if result['prize_tier'] != "No Prize":
            stats['prizes_won'] += 1
    
    return strategy_stats

def analyze_winning_number_patterns(winning_numbers, winning_stars):
    """
    Analyze patterns in the actual winning numbers
    """
    patterns = {
        'sum': sum(winning_numbers),
        'range': max(winning_numbers) - min(winning_numbers),
        'even_count': sum(1 for n in winning_numbers if n % 2 == 0),
        'odd_count': sum(1 for n in winning_numbers if n % 2 == 1),
        'low_numbers': sum(1 for n in winning_numbers if n <= 25),
        'high_numbers': sum(1 for n in winning_numbers if n > 25),
        'consecutive_pairs': count_consecutive_pairs(winning_numbers),
        'star_sum': sum(winning_stars),
        'star_pattern': 'both_high' if all(s > 6 for s in winning_stars) else 'mixed'
    }
    
    return patterns

def count_consecutive_pairs(numbers):
    """Count consecutive number pairs"""
    sorted_nums = sorted(numbers)
    consecutive = 0
    for i in range(len(sorted_nums) - 1):
        if sorted_nums[i+1] - sorted_nums[i] == 1:
            consecutive += 1
    return consecutive

def find_closest_combinations(analyzed_results, top_n=5):
    """
    Find our combinations that came closest to winning
    """
    # Sort by total matches (numbers + stars)
    valid_results = [r for r in analyzed_results if r is not None]
    sorted_results = sorted(valid_results, 
                          key=lambda x: (x['number_matches'] + x['star_matches'], x['score']), 
                          reverse=True)
    
    return sorted_results[:top_n]

def main():
    """
    Main analysis function
    """
    print("=== Euromillions May 20, 2025 Performance Analysis ===\n")
    
    # Get our combinations
    combinations_df = get_may20_combinations()
    if combinations_df.empty:
        print("No combinations found for May 20, 2025")
        return
    
    # Get actual results
    actual_results = get_may20_actual_results()
    print(f"Actual Results: Numbers {actual_results['numbers']}, Stars {actual_results['stars']}\n")
    
    # Analyze each combination
    analyzed_results = []
    for _, row in combinations_df.iterrows():
        result = analyze_combination_performance(row, actual_results)
        if result:
            analyzed_results.append(result)
    
    # Strategy performance analysis
    strategy_stats = analyze_strategy_performance(analyzed_results)
    
    print("=== STRATEGY PERFORMANCE SUMMARY ===")
    for strategy, stats in sorted(strategy_stats.items(), 
                                key=lambda x: x[1]['best_performance'], 
                                reverse=True):
        avg_number_matches = stats['total_number_matches'] / stats['total_combinations']
        avg_star_matches = stats['total_star_matches'] / stats['total_combinations']
        
        print(f"\n{strategy}:")
        print(f"  - Combinations: {stats['total_combinations']}")
        print(f"  - Best Performance: {stats['best_performance']} total matches")
        print(f"  - Average Number Matches: {avg_number_matches:.1f}")
        print(f"  - Average Star Matches: {avg_star_matches:.1f}")
        print(f"  - Prizes Won: {stats['prizes_won']}")
    
    # Find our best combinations
    print("\n=== TOP 5 CLOSEST COMBINATIONS ===")
    closest = find_closest_combinations(analyzed_results, 5)
    
    for i, result in enumerate(closest, 1):
        total_matches = result['number_matches'] + result['star_matches']
        print(f"\n{i}. {result['strategy']} (Score: {result['score']:.1f})")
        print(f"   Numbers: {result['numbers']} ({result['number_matches']} matches)")
        print(f"   Stars: {result['stars']} ({result['star_matches']} matches)")
        print(f"   Total Matches: {total_matches}")
        print(f"   Prize Tier: {result['prize_tier']}")
    
    # Analyze winning patterns
    patterns = analyze_winning_number_patterns(actual_results['numbers'], actual_results['stars'])
    
    print("\n=== WINNING NUMBER ANALYSIS ===")
    print(f"Numbers: {actual_results['numbers']}")
    print(f"Sum: {patterns['sum']} (typical range: 100-180)")
    print(f"Range: {patterns['range']} (span between highest and lowest)")
    print(f"Even/Odd: {patterns['even_count']} even, {patterns['odd_count']} odd")
    print(f"Low/High: {patterns['low_numbers']} low (≤25), {patterns['high_numbers']} high (>25)")
    print(f"Consecutive pairs: {patterns['consecutive_pairs']}")
    print(f"Stars: {actual_results['stars']} (sum: {patterns['star_sum']}, pattern: {patterns['star_pattern']})")
    
    # Overall performance summary
    total_combinations = len(analyzed_results)
    total_matches = sum(r['number_matches'] + r['star_matches'] for r in analyzed_results if r)
    total_prizes = sum(1 for r in analyzed_results if r and r['prize_tier'] != "No Prize")
    
    print(f"\n=== OVERALL PERFORMANCE ===")
    print(f"Total Combinations Played: {total_combinations}")
    print(f"Total Matches Achieved: {total_matches}")
    print(f"Average Matches per Combination: {total_matches/total_combinations:.1f}")
    print(f"Combinations with Prizes: {total_prizes}")
    print(f"Prize Rate: {(total_prizes/total_combinations)*100:.1f}%")
    
    if total_matches > 0:
        print(f"\n✓ We achieved matches! Our strategies are working.")
    else:
        print(f"\n→ No matches this time, but that's normal for lottery predictions.")
    
    print(f"\n=== RECOMMENDATIONS FOR NEXT DRAW ===")
    print("Based on this analysis:")
    
    # Find best performing strategy
    if strategy_stats:
        best_strategy = max(strategy_stats.items(), key=lambda x: x[1]['best_performance'])
        print(f"• Continue using {best_strategy[0]} - it performed best")
    
    print(f"• The winning numbers had these characteristics:")
    print(f"  - Sum of {patterns['sum']} (consider combinations with similar sums)")
    print(f"  - {patterns['even_count']}-{patterns['odd_count']} even-odd split")
    print(f"  - {patterns['low_numbers']}-{patterns['high_numbers']} low-high distribution")
    
    if patterns['consecutive_pairs'] > 0:
        print(f"  - {patterns['consecutive_pairs']} consecutive pairs appeared")
    else:
        print(f"  - No consecutive numbers (consider avoiding consecutive pairs)")

if __name__ == "__main__":
    main()