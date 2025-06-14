"""
Comprehensive backtesting of French Loto strategies against all historical data
Similar to Euromillions analysis but adapted for French Loto format (5 numbers + 1 lucky)
"""

import psycopg2
import os
from collections import Counter, defaultdict
import random
import numpy as np

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    else:
        raise Exception("No database connection available")

def get_french_loto_data():
    """Get all French Loto historical data"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # Get all French Loto data
    query = """
    SELECT date, n1, n2, n3, n4, n5, lucky 
    FROM french_loto_drawings 
    ORDER BY date
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.close()
    return results

def split_loto_data(data, split_year='2019-01-01'):
    """Split data into training and test sets"""
    
    from datetime import datetime
    split_date = datetime.strptime(split_year, '%Y-%m-%d').date()
    
    training_data = []
    test_data = []
    
    for row in data:
        date, n1, n2, n3, n4, n5, lucky = row
        if date < split_date:
            training_data.append(row)
        else:
            test_data.append(row)
    
    return training_data, test_data

def generate_risk_reward_loto(training_data):
    """Generate French Loto combination using Risk-Reward strategy"""
    
    all_numbers = []
    all_lucky = []
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_lucky.append(lucky)
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    # Categorize numbers by frequency
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    total = len(sorted_numbers)
    
    hot_numbers = [n for n, freq in sorted_numbers[:total//3]]
    warm_numbers = [n for n, freq in sorted_numbers[total//3:2*total//3]]
    cold_numbers = [n for n, freq in sorted_numbers[2*total//3:]]
    
    # Risk-reward balance: 2 hot, 2 warm, 1 cold
    combo_numbers = []
    if len(hot_numbers) >= 2:
        combo_numbers.extend(random.sample(hot_numbers, 2))
    if len(warm_numbers) >= 2:
        available_warm = [n for n in warm_numbers if n not in combo_numbers]
        combo_numbers.extend(random.sample(available_warm, min(2, len(available_warm))))
    if len(cold_numbers) >= 1:
        available_cold = [n for n in cold_numbers if n not in combo_numbers]
        if available_cold:
            combo_numbers.extend(random.sample(available_cold, 1))
    
    # Fill remaining slots if needed
    while len(combo_numbers) < 5:
        all_available = hot_numbers + warm_numbers + cold_numbers
        remaining = [n for n in all_available if n not in combo_numbers]
        if remaining:
            combo_numbers.append(random.choice(remaining))
        else:
            break
    
    # Select lucky number based on frequency
    top_lucky = [l for l, freq in lucky_freq.most_common(5)]
    combo_lucky = random.choice(top_lucky)
    
    return sorted(combo_numbers[:5]), combo_lucky

def generate_coverage_optimization_loto(training_data):
    """Generate French Loto combination using Coverage Optimization strategy"""
    
    all_numbers = []
    all_lucky = []
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_lucky.append(lucky)
    
    # Range-based coverage for French Loto (1-49)
    low_range = list(range(1, 17))    # 1-16
    mid_range = list(range(17, 33))   # 17-32
    high_range = list(range(33, 50))  # 33-49
    
    # Select from each range for coverage
    combo_numbers = []
    combo_numbers.extend(random.sample(low_range, 2))
    combo_numbers.extend(random.sample(mid_range, 2))
    combo_numbers.extend(random.sample(high_range, 1))
    
    # Lucky number from frequent ones
    lucky_freq = Counter(all_lucky)
    top_lucky = [l for l, freq in lucky_freq.most_common(6)]
    combo_lucky = random.choice(top_lucky)
    
    return sorted(combo_numbers), combo_lucky

def generate_frequency_analysis_loto(training_data):
    """Generate French Loto combination using pure Frequency Analysis"""
    
    all_numbers = []
    all_lucky = []
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_lucky.append(lucky)
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    # Select most frequent numbers
    top_numbers = [n for n, freq in number_freq.most_common(15)]
    combo_numbers = random.sample(top_numbers, 5)
    
    # Most frequent lucky number
    combo_lucky = lucky_freq.most_common(1)[0][0]
    
    return sorted(combo_numbers), combo_lucky

def generate_markov_chain_loto(training_data):
    """Generate French Loto combination using Markov Chain strategy"""
    
    # Build transition matrix
    number_transitions = defaultdict(Counter)
    lucky_from_numbers = defaultdict(Counter)
    
    all_numbers = []
    all_lucky = []
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, lucky = row
        numbers = sorted([n1, n2, n3, n4, n5])
        all_numbers.extend(numbers)
        all_lucky.append(lucky)
        
        # Build number transitions
        for i in range(len(numbers) - 1):
            current = numbers[i]
            next_num = numbers[i + 1]
            number_transitions[current][next_num] += 1
        
        # Build lucky transitions from numbers
        for num in numbers:
            lucky_from_numbers[num][lucky] += 1
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    # Generate using Markov chains
    start_num = random.choice([n for n, freq in number_freq.most_common(10)])
    combo_numbers = [start_num]
    current = start_num
    
    for _ in range(4):
        if current in number_transitions and number_transitions[current]:
            candidates = list(number_transitions[current].keys())
            available_candidates = [n for n in candidates if n not in combo_numbers]
            
            if available_candidates:
                weights = [number_transitions[current][n] for n in available_candidates]
                next_num = random.choices(available_candidates, weights=weights)[0]
                combo_numbers.append(next_num)
                current = next_num
            else:
                # Fallback to frequency
                remaining = [n for n in range(1, 50) if n not in combo_numbers]
                if remaining:
                    combo_numbers.append(random.choice(remaining))
        else:
            # Fallback to frequency
            remaining = [n for n in range(1, 50) if n not in combo_numbers]
            if remaining:
                combo_numbers.append(random.choice(remaining))
    
    # Generate lucky based on number influences
    lucky_candidates = Counter()
    for num in combo_numbers:
        if num in lucky_from_numbers:
            for lucky, count in lucky_from_numbers[num].items():
                lucky_candidates[lucky] += count
    
    if lucky_candidates:
        combo_lucky = lucky_candidates.most_common(1)[0][0]
    else:
        combo_lucky = lucky_freq.most_common(1)[0][0]
    
    return sorted(combo_numbers[:5]), combo_lucky

def generate_time_series_loto(training_data):
    """Generate French Loto combination using Time Series Analysis"""
    
    # Use recent trends (last 20% of training data)
    recent_count = max(1, len(training_data) // 5)
    recent_data = training_data[-recent_count:]
    
    recent_numbers = []
    recent_lucky = []
    
    for row in recent_data:
        date, n1, n2, n3, n4, n5, lucky = row
        recent_numbers.extend([n1, n2, n3, n4, n5])
        recent_lucky.append(lucky)
    
    recent_freq = Counter(recent_numbers)
    recent_lucky_freq = Counter(recent_lucky)
    
    # Trend-based selection
    trending_numbers = [n for n, freq in recent_freq.most_common(12)]
    combo_numbers = random.sample(trending_numbers, 5)
    
    # Trending lucky
    combo_lucky = recent_lucky_freq.most_common(1)[0][0]
    
    return sorted(combo_numbers), combo_lucky

def score_loto_combination(predicted_numbers, predicted_lucky, actual_numbers, actual_lucky):
    """Score a French Loto combination against actual results"""
    
    number_matches = len(set(predicted_numbers) & set(actual_numbers))
    lucky_match = 1 if predicted_lucky == actual_lucky else 0
    
    # French Loto scoring system
    if number_matches == 5 and lucky_match == 1:
        return 100  # Jackpot
    elif number_matches == 5 and lucky_match == 0:
        return 20   # Second tier
    elif number_matches == 4 and lucky_match == 1:
        return 10   # Third tier
    elif number_matches == 4 and lucky_match == 0:
        return 5    # Fourth tier
    elif number_matches == 3 and lucky_match == 1:
        return 3    # Fifth tier
    elif number_matches == 3 and lucky_match == 0:
        return 2
    elif number_matches == 2 and lucky_match == 1:
        return 2
    elif number_matches == 2 and lucky_match == 0:
        return 1
    elif number_matches == 1 and lucky_match == 1:
        return 1
    else:
        return 0

def backtest_loto_strategies(training_data, test_data):
    """Backtest all French Loto strategies"""
    
    strategies = {
        'Risk-Reward': generate_risk_reward_loto,
        'Coverage Optimization': generate_coverage_optimization_loto,
        'Frequency Analysis': generate_frequency_analysis_loto,
        'Markov Chain': generate_markov_chain_loto,
        'Time Series': generate_time_series_loto
    }
    
    results = {}
    
    print("FRENCH LOTO COMPREHENSIVE BACKTESTING")
    print("=" * 37)
    print(f"Training period: {len(training_data)} draws")
    print(f"Test period: {len(test_data)} draws")
    print()
    
    for strategy_name, strategy_func in strategies.items():
        print(f"Testing {strategy_name}...")
        
        total_score = 0
        total_number_matches = 0
        total_lucky_matches = 0
        combinations_tested = 0
        match_distribution = Counter()
        score_distribution = Counter()
        
        for test_row in test_data:
            date, n1, n2, n3, n4, n5, lucky = test_row
            actual_numbers = sorted([n1, n2, n3, n4, n5])
            actual_lucky = lucky
            
            try:
                # Generate prediction
                predicted_numbers, predicted_lucky = strategy_func(training_data)
                
                # Score the prediction
                score = score_loto_combination(predicted_numbers, predicted_lucky, actual_numbers, actual_lucky)
                number_matches = len(set(predicted_numbers) & set(actual_numbers))
                lucky_match = 1 if predicted_lucky == actual_lucky else 0
                
                total_score += score
                total_number_matches += number_matches
                total_lucky_matches += lucky_match
                combinations_tested += 1
                
                match_distribution[f"{number_matches}+{lucky_match}"] += 1
                score_distribution[score] += 1
                
            except Exception as e:
                print(f"   Error with {strategy_name}: {e}")
                continue
        
        if combinations_tested > 0:
            avg_score = total_score / combinations_tested
            avg_number_matches = total_number_matches / combinations_tested
            avg_lucky_matches = total_lucky_matches / combinations_tested
            
            results[strategy_name] = {
                'avg_score': avg_score,
                'avg_number_matches': avg_number_matches,
                'avg_lucky_matches': avg_lucky_matches,
                'total_score': total_score,
                'combinations_tested': combinations_tested,
                'match_distribution': dict(match_distribution),
                'score_distribution': dict(score_distribution)
            }
            
            print(f"   Avg Score: {avg_score:.4f}")
            print(f"   Avg Number Matches: {avg_number_matches:.2f}")
            print(f"   Avg Lucky Matches: {avg_lucky_matches:.2f}")
        else:
            print(f"   No valid combinations generated")
    
    return results

def analyze_loto_results(results):
    """Analyze the French Loto backtesting results"""
    
    print("\n" + "="*60)
    print("FRENCH LOTO STRATEGY ANALYSIS")
    print("="*60)
    
    # Sort by average score
    sorted_results = sorted(results.items(), key=lambda x: x[1]['avg_score'], reverse=True)
    
    print("\nSTRATEGY RANKING BY AVERAGE SCORE:")
    print("Rank | Strategy               | Avg Score | Number Matches | Lucky Matches | Total Tests")
    print("-" * 95)
    
    for i, (strategy, data) in enumerate(sorted_results, 1):
        print(f"{i:4d} | {strategy:22s} | {data['avg_score']:9.4f} | {data['avg_number_matches']:14.2f} | {data['avg_lucky_matches']:13.2f} | {data['combinations_tested']:11d}")
    
    # Detailed analysis for top strategies
    print(f"\nDETAILED ANALYSIS OF TOP 3 STRATEGIES:")
    print("-" * 41)
    
    for i, (strategy, data) in enumerate(sorted_results[:3], 1):
        print(f"\n{i}. {strategy} (Score: {data['avg_score']:.4f})")
        
        # Match distribution
        print(f"   Match Distribution:")
        for match_type, count in sorted(data['match_distribution'].items()):
            percentage = (count / data['combinations_tested']) * 100
            print(f"   • {match_type} matches: {count:3d} ({percentage:5.1f}%)")
        
        # Score distribution
        print(f"   Score Distribution:")
        for score, count in sorted(data['score_distribution'].items(), reverse=True):
            if count > 0:
                percentage = (count / data['combinations_tested']) * 100
                print(f"   • {score:3d} points: {count:3d} ({percentage:5.1f}%)")
    
    # Performance comparison
    print(f"\nPERFORMANCE COMPARISON:")
    print("-" * 22)
    
    best_strategy = sorted_results[0]
    worst_strategy = sorted_results[-1]
    
    improvement = best_strategy[1]['avg_score'] - worst_strategy[1]['avg_score']
    percentage_improvement = (improvement / worst_strategy[1]['avg_score']) * 100
    
    print(f"Best strategy: {best_strategy[0]} ({best_strategy[1]['avg_score']:.4f})")
    print(f"Worst strategy: {worst_strategy[0]} ({worst_strategy[1]['avg_score']:.4f})")
    print(f"Performance gap: {improvement:.4f} ({percentage_improvement:.1f}% improvement)")
    
    # Lucky number analysis
    print(f"\nLUCKY NUMBER PERFORMANCE:")
    print("-" * 25)
    
    for strategy, data in sorted_results:
        lucky_rate = data['avg_lucky_matches']
        print(f"{strategy:22s}: {lucky_rate:.3f} avg lucky matches ({lucky_rate*100:.1f}%)")

def main():
    """Run comprehensive French Loto backtesting"""
    
    # Get all historical data
    all_data = get_french_loto_data()
    
    if not all_data:
        print("No French Loto data found in database")
        return
    
    print(f"Total French Loto draws available: {len(all_data)}")
    
    # Split data
    training_data, test_data = split_loto_data(all_data)
    
    # Run backtesting
    results = backtest_loto_strategies(training_data, test_data)
    
    if results:
        analyze_loto_results(results)
        
        print(f"\nRECOMMENDATIONS:")
        print("• Use the top-performing strategy for primary combinations")
        print("• Consider combining multiple strategies for diversification")
        print("• Focus on lucky number optimization - it significantly impacts scores")
        print("• Monitor performance differences between strategies")
    else:
        print("No results generated - check data availability")

if __name__ == "__main__":
    main()