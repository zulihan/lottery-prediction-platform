"""
Comprehensive historical backtesting of different lottery strategies
Tests multiple strategies against actual Euromillions historical data
"""

import psycopg2
import os
from collections import Counter, defaultdict
import random
import math
from datetime import datetime, timedelta

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    else:
        raise Exception("No database connection available")

def get_historical_euromillions_data(limit=500):
    """Get comprehensive historical Euromillions data"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = """
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC 
    LIMIT %s
    """
    
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    
    conn.close()
    return results

def split_data_for_backtesting(historical_data, test_ratio=0.3):
    """Split data into training and testing sets"""
    
    total_draws = len(historical_data)
    test_size = int(total_draws * test_ratio)
    
    # Most recent draws for testing, older draws for training
    test_data = historical_data[:test_size]
    training_data = historical_data[test_size:]
    
    print(f"Data split: {len(training_data)} training draws, {len(test_data)} test draws")
    
    return training_data, test_data

def generate_frequency_analysis_combinations(training_data, num_combos=5):
    """Generate combinations using frequency analysis"""
    
    all_numbers = []
    all_stars = []
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    combinations = []
    
    for i in range(num_combos):
        # Take most frequent numbers with some variation
        start_idx = i * 2
        top_numbers = [n for n, freq in number_freq.most_common(30)]
        combo_numbers = top_numbers[start_idx:start_idx+5]
        
        # Take most frequent stars
        top_stars = [s for s, freq in star_freq.most_common(6)]
        combo_stars = top_stars[i:i+2] if i+1 < len(top_stars) else top_stars[:2]
        
        combinations.append({
            'numbers': sorted(combo_numbers),
            'stars': sorted(combo_stars),
            'strategy': 'Frequency Analysis'
        })
    
    return combinations

def generate_time_series_combinations(training_data, num_combos=5):
    """Generate combinations using time series analysis"""
    
    # Analyze recent trends vs historical
    recent_data = training_data[:50]  # Last 50 draws
    historical_data = training_data[50:]  # Older draws
    
    recent_numbers = []
    recent_stars = []
    historical_numbers = []
    historical_stars = []
    
    for row in recent_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        recent_numbers.extend([n1, n2, n3, n4, n5])
        recent_stars.extend([s1, s2])
    
    for row in historical_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        historical_numbers.extend([n1, n2, n3, n4, n5])
        historical_stars.extend([s1, s2])
    
    recent_freq = Counter(recent_numbers)
    historical_freq = Counter(historical_numbers)
    recent_star_freq = Counter(recent_stars)
    historical_star_freq = Counter(historical_stars)
    
    combinations = []
    
    for i in range(num_combos):
        combo_numbers = []
        combo_stars = []
        
        if i % 2 == 0:  # Recent trend emphasis
            top_recent = [n for n, freq in recent_freq.most_common(15)]
            combo_numbers = random.sample(top_recent, 5)
            top_recent_stars = [s for s, freq in recent_star_freq.most_common(4)]
            combo_stars = random.sample(top_recent_stars, 2)
        else:  # Historical stability emphasis
            top_historical = [n for n, freq in historical_freq.most_common(15)]
            combo_numbers = random.sample(top_historical, 5)
            top_historical_stars = [s for s, freq in historical_star_freq.most_common(4)]
            combo_stars = random.sample(top_historical_stars, 2)
        
        combinations.append({
            'numbers': sorted(combo_numbers),
            'stars': sorted(combo_stars),
            'strategy': 'Time Series Analysis'
        })
    
    return combinations

def generate_markov_chain_combinations(training_data, num_combos=5):
    """Generate combinations using Markov chain analysis"""
    
    # Build transition matrices for number sequences
    number_transitions = defaultdict(Counter)
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        numbers = sorted([n1, n2, n3, n4, n5])
        
        # Track transitions between consecutive numbers
        for i in range(len(numbers) - 1):
            current = numbers[i]
            next_num = numbers[i + 1]
            number_transitions[current][next_num] += 1
    
    combinations = []
    
    for i in range(num_combos):
        # Start with a frequent number
        all_numbers = []
        for row in training_data:
            date, n1, n2, n3, n4, n5, s1, s2 = row
            all_numbers.extend([n1, n2, n3, n4, n5])
        
        freq_counter = Counter(all_numbers)
        start_candidates = [n for n, freq in freq_counter.most_common(20)]
        
        combo_numbers = [random.choice(start_candidates)]
        
        # Use Markov chain to generate next numbers
        for _ in range(4):
            current = combo_numbers[-1]
            if current in number_transitions and number_transitions[current]:
                # Get most likely next numbers
                next_candidates = list(number_transitions[current].keys())
                next_num = random.choice(next_candidates)
                if next_num not in combo_numbers:
                    combo_numbers.append(next_num)
                else:
                    # Fallback to random from frequent numbers
                    remaining = [n for n in start_candidates if n not in combo_numbers]
                    if remaining:
                        combo_numbers.append(random.choice(remaining))
            else:
                # Fallback to frequent numbers
                remaining = [n for n in start_candidates if n not in combo_numbers]
                if remaining:
                    combo_numbers.append(random.choice(remaining))
        
        # Generate stars using frequency
        all_stars = []
        for row in training_data:
            date, n1, n2, n3, n4, n5, s1, s2 = row
            all_stars.extend([s1, s2])
        
        star_freq = Counter(all_stars)
        combo_stars = random.sample([s for s, freq in star_freq.most_common(8)], 2)
        
        combinations.append({
            'numbers': sorted(combo_numbers[:5]),
            'stars': sorted(combo_stars),
            'strategy': 'Markov Chain'
        })
    
    return combinations

def generate_coverage_optimization_combinations(training_data, num_combos=5):
    """Generate combinations using coverage optimization"""
    
    # Analyze range distributions
    all_numbers = []
    all_stars = []
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    # Divide into ranges and ensure coverage
    low_numbers = [n for n in all_numbers if 1 <= n <= 16]
    mid_numbers = [n for n in all_numbers if 17 <= n <= 33]
    high_numbers = [n for n in all_numbers if 34 <= n <= 49]
    
    low_freq = Counter(low_numbers)
    mid_freq = Counter(mid_numbers)
    high_freq = Counter(high_numbers)
    star_freq = Counter(all_stars)
    
    combinations = []
    
    for i in range(num_combos):
        combo_numbers = []
        
        # Ensure balanced coverage: 1-2 low, 2-3 mid, 1-2 high
        coverage_patterns = [
            (2, 2, 1),  # 2 low, 2 mid, 1 high
            (1, 3, 1),  # 1 low, 3 mid, 1 high
            (1, 2, 2),  # 1 low, 2 mid, 2 high
            (2, 1, 2),  # 2 low, 1 mid, 2 high
            (1, 1, 3)   # 1 low, 1 mid, 3 high
        ]
        
        pattern = coverage_patterns[i % len(coverage_patterns)]
        low_count, mid_count, high_count = pattern
        
        # Select numbers according to pattern
        if low_freq and low_count > 0:
            low_candidates = [n for n, freq in low_freq.most_common(10)]
            combo_numbers.extend(random.sample(low_candidates, min(low_count, len(low_candidates))))
        
        if mid_freq and mid_count > 0:
            mid_candidates = [n for n, freq in mid_freq.most_common(15)]
            combo_numbers.extend(random.sample(mid_candidates, min(mid_count, len(mid_candidates))))
        
        if high_freq and high_count > 0:
            high_candidates = [n for n, freq in high_freq.most_common(10)]
            combo_numbers.extend(random.sample(high_candidates, min(high_count, len(high_candidates))))
        
        # Fill to 5 if needed
        while len(combo_numbers) < 5:
            all_candidates = [n for n, freq in Counter(all_numbers).most_common(30)]
            remaining = [n for n in all_candidates if n not in combo_numbers]
            if remaining:
                combo_numbers.append(random.choice(remaining))
            else:
                break
        
        combo_stars = random.sample([s for s, freq in star_freq.most_common(8)], 2)
        
        combinations.append({
            'numbers': sorted(combo_numbers[:5]),
            'stars': sorted(combo_stars),
            'strategy': 'Coverage Optimization'
        })
    
    return combinations

def generate_risk_reward_combinations(training_data, num_combos=5):
    """Generate combinations using risk-reward analysis"""
    
    all_numbers = []
    all_stars = []
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Categorize numbers by frequency (risk level)
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    total_numbers = len(sorted_numbers)
    
    hot_numbers = [n for n, freq in sorted_numbers[:total_numbers//3]]  # Top third - low risk
    warm_numbers = [n for n, freq in sorted_numbers[total_numbers//3:2*total_numbers//3]]  # Middle third
    cold_numbers = [n for n, freq in sorted_numbers[2*total_numbers//3:]]  # Bottom third - high risk
    
    combinations = []
    
    risk_profiles = [
        {'hot': 4, 'warm': 1, 'cold': 0, 'name': 'Conservative'},
        {'hot': 3, 'warm': 2, 'cold': 0, 'name': 'Moderate'},
        {'hot': 2, 'warm': 2, 'cold': 1, 'name': 'Balanced'},
        {'hot': 1, 'warm': 2, 'cold': 2, 'name': 'Aggressive'},
        {'hot': 0, 'warm': 2, 'cold': 3, 'name': 'High Risk'}
    ]
    
    for i in range(num_combos):
        profile = risk_profiles[i % len(risk_profiles)]
        combo_numbers = []
        
        # Select according to risk profile
        if profile['hot'] > 0 and hot_numbers:
            combo_numbers.extend(random.sample(hot_numbers, min(profile['hot'], len(hot_numbers))))
        
        if profile['warm'] > 0 and warm_numbers:
            combo_numbers.extend(random.sample(warm_numbers, min(profile['warm'], len(warm_numbers))))
        
        if profile['cold'] > 0 and cold_numbers:
            combo_numbers.extend(random.sample(cold_numbers, min(profile['cold'], len(cold_numbers))))
        
        # Fill to 5 if needed
        while len(combo_numbers) < 5:
            all_available = hot_numbers + warm_numbers + cold_numbers
            remaining = [n for n in all_available if n not in combo_numbers]
            if remaining:
                combo_numbers.append(random.choice(remaining))
            else:
                break
        
        combo_stars = random.sample([s for s, freq in star_freq.most_common(8)], 2)
        
        combinations.append({
            'numbers': sorted(combo_numbers[:5]),
            'stars': sorted(combo_stars),
            'strategy': f'Risk-Reward ({profile["name"]})'
        })
    
    return combinations

def test_strategy_performance(strategy_combinations, test_data):
    """Test how well a strategy performs against historical draws"""
    
    total_score = 0
    total_combinations = len(strategy_combinations)
    total_draws = len(test_data)
    
    detailed_results = []
    
    for draw in test_data:
        date, n1, n2, n3, n4, n5, s1, s2 = draw
        actual_numbers = [n1, n2, n3, n4, n5]
        actual_stars = [s1, s2]
        
        draw_results = []
        
        for combo in strategy_combinations:
            number_matches = len(set(combo['numbers']) & set(actual_numbers))
            star_matches = len(set(combo['stars']) & set(actual_stars))
            combo_score = number_matches + star_matches
            
            draw_results.append({
                'combo': combo,
                'number_matches': number_matches,
                'star_matches': star_matches,
                'total_score': combo_score
            })
        
        # Best performing combination for this draw
        best_combo_result = max(draw_results, key=lambda x: x['total_score'])
        total_score += best_combo_result['total_score']
        
        detailed_results.append({
            'date': date,
            'actual_numbers': actual_numbers,
            'actual_stars': actual_stars,
            'best_result': best_combo_result,
            'all_results': draw_results
        })
    
    avg_score = total_score / total_draws
    
    return {
        'strategy_name': strategy_combinations[0]['strategy'],
        'total_score': total_score,
        'average_score': avg_score,
        'total_draws': total_draws,
        'total_combinations': total_combinations,
        'detailed_results': detailed_results
    }

def run_comprehensive_backtest():
    """Run comprehensive backtesting across all strategies"""
    
    print("COMPREHENSIVE STRATEGY BACKTESTING")
    print("=" * 35)
    
    # Get historical data
    historical_data = get_historical_euromillions_data(400)
    training_data, test_data = split_data_for_backtesting(historical_data, test_ratio=0.25)
    
    print(f"Testing period: {len(test_data)} draws")
    print(f"Training period: {len(training_data)} draws")
    print()
    
    # Generate combinations for each strategy
    strategies = [
        ('Frequency Analysis', generate_frequency_analysis_combinations),
        ('Time Series Analysis', generate_time_series_combinations),
        ('Markov Chain', generate_markov_chain_combinations),
        ('Coverage Optimization', generate_coverage_optimization_combinations),
        ('Risk-Reward', generate_risk_reward_combinations)
    ]
    
    strategy_results = []
    
    for strategy_name, generator_func in strategies:
        print(f"Testing {strategy_name}...")
        
        # Generate combinations using training data
        combinations = generator_func(training_data, num_combos=5)
        
        # Test against test data
        performance = test_strategy_performance(combinations, test_data)
        strategy_results.append(performance)
        
        print(f"  Average score: {performance['average_score']:.3f}")
        print(f"  Total score: {performance['total_score']}")
        print()
    
    return strategy_results

def analyze_strategy_rankings(strategy_results):
    """Analyze and rank strategy performance"""
    
    print("STRATEGY PERFORMANCE RANKINGS")
    print("-" * 29)
    
    # Sort by average score
    sorted_results = sorted(strategy_results, key=lambda x: x['average_score'], reverse=True)
    
    for i, result in enumerate(sorted_results, 1):
        print(f"{i}. {result['strategy_name']}")
        print(f"   Average Score: {result['average_score']:.3f}")
        print(f"   Total Score: {result['total_score']}")
        print(f"   Score per Draw: {result['total_score']/result['total_draws']:.3f}")
        print()
    
    return sorted_results

def detailed_performance_analysis(strategy_results):
    """Provide detailed performance analysis"""
    
    print("DETAILED PERFORMANCE ANALYSIS")
    print("-" * 29)
    
    for result in strategy_results:
        print(f"\n{result['strategy_name']} DETAILED ANALYSIS:")
        print("-" * (len(result['strategy_name']) + 19))
        
        # Analyze score distribution
        scores = [dr['best_result']['total_score'] for dr in result['detailed_results']]
        score_distribution = Counter(scores)
        
        print(f"Score Distribution:")
        for score in sorted(score_distribution.keys(), reverse=True):
            count = score_distribution[score]
            percentage = (count / len(scores)) * 100
            print(f"  {score} points: {count} draws ({percentage:.1f}%)")
        
        # Find best performance examples
        best_draws = sorted(result['detailed_results'], 
                          key=lambda x: x['best_result']['total_score'], reverse=True)[:3]
        
        print(f"\nBest Performances:")
        for i, draw in enumerate(best_draws, 1):
            br = draw['best_result']
            print(f"  {i}. Date: {draw['date']}")
            print(f"     Actual: {draw['actual_numbers']} + {draw['actual_stars']}")
            print(f"     Best combo: {br['combo']['numbers']} + {br['combo']['stars']}")
            print(f"     Matches: {br['number_matches']} numbers + {br['star_matches']} stars = {br['total_score']}")

def main():
    """Main backtesting function"""
    
    # Run comprehensive backtest
    strategy_results = run_comprehensive_backtest()
    
    # Analyze rankings
    ranked_results = analyze_strategy_rankings(strategy_results)
    
    # Detailed analysis
    detailed_performance_analysis(strategy_results)
    
    print("\nKEY INSIGHTS:")
    print("-" * 13)
    best_strategy = ranked_results[0]
    worst_strategy = ranked_results[-1]
    
    print(f"1. Best performing strategy: {best_strategy['strategy_name']}")
    print(f"   Average score: {best_strategy['average_score']:.3f}")
    
    print(f"2. Worst performing strategy: {worst_strategy['strategy_name']}")
    print(f"   Average score: {worst_strategy['average_score']:.3f}")
    
    performance_gap = best_strategy['average_score'] - worst_strategy['average_score']
    print(f"3. Performance gap: {performance_gap:.3f} points per draw")
    
    print(f"4. Recommended approach: Use top 2-3 strategies in combination")

if __name__ == "__main__":
    main()