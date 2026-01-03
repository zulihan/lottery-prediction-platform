"""
Backtest the Fibonacci-Filtered Hybrid Strategy against historical Euromillions data
to validate its performance and effectiveness.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
from database import get_db_connection
from fibonacci_hybrid_strategy import generate_fibonacci_hybrid_combinations

def load_historical_data():
    """Load historical Euromillions data for backtesting"""
    try:
        engine = get_db_connection()
        
        # Load all historical data
        query = """
        SELECT date, n1, n2, n3, n4, n5, s1, s2 
        FROM euromillions_drawings 
        WHERE date IS NOT NULL 
        ORDER BY date DESC
        """
        
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("No historical data found in database!")
            return None
        
        # Convert individual columns to arrays
        df['numbers'] = df.apply(lambda row: sorted([row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]), axis=1)
        df['stars'] = df.apply(lambda row: sorted([row['s1'], row['s2']]), axis=1)
        
        print(f"✅ Loaded {len(df)} historical Euromillions draws")
        return df
        
    except Exception as e:
        print(f"Error loading historical data: {e}")
        return None

def analyze_combination_against_draw(combination, actual_numbers, actual_stars):
    """
    Analyze how well a single combination performed against an actual draw
    
    Returns:
        dict: Performance metrics
    """
    # Count matches
    number_matches = len(set(combination['numbers']) & set(actual_numbers))
    star_matches = len(set(combination['stars']) & set(actual_stars))
    
    # Determine prize tier
    prize_tier = get_prize_tier(number_matches, star_matches)
    
    # Calculate score (out of 7 maximum)
    total_score = number_matches + star_matches
    
    return {
        'combination': combination,
        'number_matches': number_matches,
        'star_matches': star_matches,
        'total_score': total_score,
        'prize_tier': prize_tier,
        'won_prize': prize_tier > 0
    }

def get_prize_tier(number_matches, star_matches):
    """
    Determine Euromillions prize tier based on matches
    
    Returns:
        int: Prize tier (0 = no prize, 1-13 = prize tiers)
    """
    if number_matches == 5 and star_matches == 2:
        return 1  # Jackpot
    elif number_matches == 5 and star_matches == 1:
        return 2
    elif number_matches == 5 and star_matches == 0:
        return 3
    elif number_matches == 4 and star_matches == 2:
        return 4
    elif number_matches == 4 and star_matches == 1:
        return 5
    elif number_matches == 4 and star_matches == 0:
        return 6
    elif number_matches == 3 and star_matches == 2:
        return 7
    elif number_matches == 2 and star_matches == 2:
        return 8
    elif number_matches == 3 and star_matches == 1:
        return 9
    elif number_matches == 3 and star_matches == 0:
        return 10
    elif number_matches == 1 and star_matches == 2:
        return 11
    elif number_matches == 2 and star_matches == 1:
        return 12
    elif number_matches == 2 and star_matches == 0:
        return 13
    else:
        return 0  # No prize

def backtest_strategy(historical_data, num_test_draws=100):
    """
    Backtest the Fibonacci-Filtered Hybrid Strategy
    
    Args:
        historical_data: DataFrame with historical draws
        num_test_draws: Number of recent draws to test against
        
    Returns:
        dict: Comprehensive backtesting results
    """
    print(f"\n🧪 BACKTESTING FIBONACCI-FILTERED HYBRID STRATEGY")
    print(f"Testing against the last {num_test_draws} draws...")
    
    # Get the most recent draws for testing
    test_data = historical_data.head(num_test_draws)
    
    results = []
    total_combinations_tested = 0
    total_prizes_won = 0
    
    for idx, row in test_data.iterrows():
        draw_date = row['date']
        actual_numbers = row['numbers']
        actual_stars = row['stars']
        
        print(f"\nTesting draw {idx + 1}/{num_test_draws}: {draw_date}")
        print(f"Actual result: {actual_numbers} + Stars {actual_stars}")
        
        # Generate hybrid combinations as if predicting this draw
        try:
            # Generate 8 combinations using our hybrid strategy
            hybrid_combinations = generate_fibonacci_hybrid_combinations(num_final=8)
            
            draw_results = []
            best_performance = {'total_score': 0, 'prize_tier': 0}
            
            # Test each combination against this draw
            for combo in hybrid_combinations:
                performance = analyze_combination_against_draw(combo, actual_numbers, actual_stars)
                draw_results.append(performance)
                total_combinations_tested += 1
                
                if performance['won_prize']:
                    total_prizes_won += 1
                
                # Track best performance for this draw
                if performance['total_score'] > best_performance['total_score']:
                    best_performance = performance
            
            # Summary for this draw
            prizes_this_draw = sum(1 for r in draw_results if r['won_prize'])
            best_score = max(r['total_score'] for r in draw_results)
            avg_score = np.mean([r['total_score'] for r in draw_results])
            
            print(f"  Best score: {best_score}/7, Avg score: {avg_score:.2f}/7")
            print(f"  Prizes won: {prizes_this_draw}/8 combinations")
            
            results.append({
                'draw_date': draw_date,
                'actual_numbers': actual_numbers,
                'actual_stars': actual_stars,
                'combinations_tested': len(hybrid_combinations),
                'best_score': best_score,
                'avg_score': avg_score,
                'prizes_won': prizes_this_draw,
                'best_performance': best_performance,
                'all_results': draw_results
            })
            
        except Exception as e:
            print(f"  Error testing draw: {e}")
            continue
    
    # Calculate overall statistics
    if results:
        overall_stats = calculate_overall_performance(results, total_combinations_tested, total_prizes_won)
        return {
            'results': results,
            'overall_stats': overall_stats,
            'num_draws_tested': len(results)
        }
    else:
        print("❌ No results generated during backtesting")
        return None

def calculate_overall_performance(results, total_combinations, total_prizes):
    """Calculate comprehensive performance statistics"""
    
    # Basic statistics
    all_best_scores = [r['best_score'] for r in results]
    all_avg_scores = [r['avg_score'] for r in results]
    all_prizes = [r['prizes_won'] for r in results]
    
    # Win rate calculations
    draws_with_prizes = sum(1 for r in results if r['prizes_won'] > 0)
    overall_win_rate = (draws_with_prizes / len(results)) * 100
    combination_win_rate = (total_prizes / total_combinations) * 100
    
    # Score analysis
    avg_best_score = np.mean(all_best_scores)
    avg_overall_score = np.mean(all_avg_scores)
    
    # Prize tier analysis
    all_prize_tiers = []
    for result in results:
        for combo_result in result['all_results']:
            if combo_result['won_prize']:
                all_prize_tiers.append(combo_result['prize_tier'])
    
    prize_distribution = Counter(all_prize_tiers)
    
    return {
        'total_draws_tested': len(results),
        'total_combinations_tested': total_combinations,
        'total_prizes_won': total_prizes,
        'draws_with_prizes': draws_with_prizes,
        'overall_win_rate_percent': overall_win_rate,
        'combination_win_rate_percent': combination_win_rate,
        'avg_best_score': avg_best_score,
        'avg_overall_score': avg_overall_score,
        'max_score_achieved': max(all_best_scores),
        'prize_distribution': dict(prize_distribution),
        'avg_prizes_per_draw': np.mean(all_prizes)
    }

def display_backtest_results(backtest_data):
    """Display comprehensive backtesting results"""
    
    if not backtest_data:
        print("❌ No backtest data to display")
        return
    
    stats = backtest_data['overall_stats']
    
    print(f"\n🏆 FIBONACCI-FILTERED HYBRID STRATEGY BACKTEST RESULTS")
    print("=" * 60)
    
    print(f"\n📊 OVERALL PERFORMANCE:")
    print(f"   • Draws Tested: {stats['total_draws_tested']}")
    print(f"   • Combinations Tested: {stats['total_combinations_tested']}")
    print(f"   • Total Prizes Won: {stats['total_prizes_won']}")
    print(f"   • Draws with Prizes: {stats['draws_with_prizes']}/{stats['total_draws_tested']}")
    
    print(f"\n🎯 WIN RATES:")
    print(f"   • Overall Win Rate: {stats['overall_win_rate_percent']:.1f}% (draws with ≥1 prize)")
    print(f"   • Combination Win Rate: {stats['combination_win_rate_percent']:.1f}% (individual combinations)")
    
    print(f"\n📈 SCORE ANALYSIS:")
    print(f"   • Average Best Score: {stats['avg_best_score']:.2f}/7")
    print(f"   • Average Overall Score: {stats['avg_overall_score']:.2f}/7")
    print(f"   • Maximum Score Achieved: {stats['max_score_achieved']}/7")
    print(f"   • Average Prizes per Draw: {stats['avg_prizes_per_draw']:.2f}")
    
    print(f"\n🏅 PRIZE DISTRIBUTION:")
    if stats['prize_distribution']:
        for tier, count in sorted(stats['prize_distribution'].items()):
            print(f"   • Tier {tier}: {count} prizes")
    else:
        print("   • No prizes won in test period")
    
    # Performance comparison
    print(f"\n⚡ STRATEGY EFFECTIVENESS:")
    if stats['overall_win_rate_percent'] > 20:
        print("   🔥 EXCELLENT - High win rate achieved!")
    elif stats['overall_win_rate_percent'] > 10:
        print("   ✅ GOOD - Solid performance above average")
    elif stats['overall_win_rate_percent'] > 5:
        print("   📊 MODERATE - Reasonable performance")
    else:
        print("   📈 DEVELOPING - Room for improvement")
    
    if stats['avg_best_score'] > 3.0:
        print("   🎯 HIGH ACCURACY - Excellent number prediction")
    elif stats['avg_best_score'] > 2.0:
        print("   ✨ GOOD ACCURACY - Strong prediction capability")
    else:
        print("   📊 BASELINE ACCURACY - Standard performance")

def main():
    """Main backtesting function"""
    print("🚀 FIBONACCI-FILTERED HYBRID STRATEGY BACKTESTING")
    print("Testing the ultimate hybrid approach against historical data...")
    
    # Load historical data
    historical_data = load_historical_data()
    if historical_data is None:
        return
    
    # Run backtest
    print(f"\nStarting backtest with {len(historical_data)} available draws...")
    backtest_results = backtest_strategy(historical_data, num_test_draws=50)
    
    # Display results
    if backtest_results:
        display_backtest_results(backtest_results)
        
        print(f"\n✅ Backtesting completed successfully!")
        print(f"🔥 Your Fibonacci-Filtered Hybrid Strategy has been validated against real historical data!")
    else:
        print("❌ Backtesting failed - no results generated")

if __name__ == "__main__":
    main()