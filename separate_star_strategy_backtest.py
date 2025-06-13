"""
Separate backtesting for star strategies vs number strategies
Test if stars perform better with different strategies than numbers
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

def get_backtest_data():
    """Get data split for backtesting (training vs test)"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # Training data: 2004-2018
    training_query = """
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    WHERE date < '2019-01-01'
    ORDER BY date
    """
    
    # Test data: 2019-2025
    test_query = """
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    WHERE date >= '2019-01-01'
    ORDER BY date
    """
    
    cursor.execute(training_query)
    training_data = cursor.fetchall()
    
    cursor.execute(test_query)
    test_data = cursor.fetchall()
    
    conn.close()
    return training_data, test_data

def generate_star_strategies(training_data, strategy_type):
    """Generate stars using different strategies"""
    
    all_stars = []
    for row in training_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_stars.extend([s1, s2])
    
    star_freq = Counter(all_stars)
    
    if strategy_type == 'frequency':
        # Most frequent stars
        top_stars = [s for s, freq in star_freq.most_common(8)]
        return random.sample(top_stars, 2)
    
    elif strategy_type == 'balanced':
        # Mix of frequent and medium frequency
        frequent = [s for s, freq in star_freq.most_common(6)]
        medium = [s for s, freq in star_freq.most_common(12)[6:]]
        selected = []
        selected.append(random.choice(frequent))
        remaining = medium + [s for s in frequent if s != selected[0]]
        selected.append(random.choice(remaining))
        return sorted(selected)
    
    elif strategy_type == 'overdue':
        # Least frequent stars (contrarian approach)
        least_frequent = [s for s, freq in star_freq.most_common()[-8:]]
        return random.sample(least_frequent, 2)
    
    elif strategy_type == 'markov':
        # Star transitions
        star_transitions = defaultdict(Counter)
        for row in training_data:
            date, n1, n2, n3, n4, n5, s1, s2 = row
            stars = sorted([s1, s2])
            if len(stars) == 2:
                star_transitions[stars[0]][stars[1]] += 1
        
        # Select first star from frequent ones
        first_star = random.choice([s for s, freq in star_freq.most_common(6)])
        
        # Select second star based on transitions
        if first_star in star_transitions and star_transitions[first_star]:
            candidates = list(star_transitions[first_star].keys())
            weights = [star_transitions[first_star][s] for s in candidates]
            second_star = random.choices(candidates, weights=weights)[0]
        else:
            remaining = [s for s in range(1, 13) if s != first_star]
            second_star = random.choice(remaining)
        
        return sorted([first_star, second_star])
    
    elif strategy_type == 'range_balanced':
        # Balance between low (1-6) and high (7-12) stars
        low_stars = [s for s in range(1, 7)]
        high_stars = [s for s in range(7, 13)]
        
        low_freq = {s: star_freq[s] for s in low_stars}
        high_freq = {s: star_freq[s] for s in high_stars}
        
        # Pick one from each range
        low_choice = max(low_freq.items(), key=lambda x: x[1])[0]
        high_choice = max(high_freq.items(), key=lambda x: x[1])[0]
        
        return sorted([low_choice, high_choice])

def generate_number_strategies(training_data, strategy_type):
    """Generate numbers using different strategies (same as before but isolated)"""
    
    all_numbers = []
    for row in training_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
    
    number_freq = Counter(all_numbers)
    
    if strategy_type == 'risk_reward':
        # Balanced frequency approach
        sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
        total = len(sorted_numbers)
        
        hot_numbers = [n for n, freq in sorted_numbers[:total//3]]
        warm_numbers = [n for n, freq in sorted_numbers[total//3:2*total//3]]
        cold_numbers = [n for n, freq in sorted_numbers[2*total//3:]]
        
        # Balanced selection
        combo = []
        combo.extend(random.sample(hot_numbers, 2))
        combo.extend(random.sample(warm_numbers, 2))
        combo.extend(random.sample(cold_numbers, 1))
        
        return sorted(combo)
    
    elif strategy_type == 'coverage':
        # Range-based coverage
        low_nums = [n for n in range(1, 17)]
        mid_nums = [n for n in range(17, 34)]
        high_nums = [n for n in range(34, 50)]
        
        combo = []
        combo.extend(random.sample(low_nums, 2))
        combo.extend(random.sample(mid_nums, 2))
        combo.extend(random.sample(high_nums, 1))
        
        return sorted(combo)
    
    elif strategy_type == 'frequency':
        # Pure frequency approach
        top_numbers = [n for n, freq in number_freq.most_common(20)]
        return sorted(random.sample(top_numbers, 5))

def score_combination(predicted_numbers, predicted_stars, actual_numbers, actual_stars):
    """Score a combination against actual results"""
    
    number_matches = len(set(predicted_numbers) & set(actual_numbers))
    star_matches = len(set(predicted_stars) & set(actual_stars))
    
    # Euromillions scoring system
    if number_matches == 5 and star_matches == 2:
        return 100  # Jackpot
    elif number_matches == 5 and star_matches == 1:
        return 10   # Second tier
    elif number_matches == 5 and star_matches == 0:
        return 8    # Third tier
    elif number_matches == 4 and star_matches == 2:
        return 6    # Fourth tier
    elif number_matches == 4 and star_matches == 1:
        return 4    # Fifth tier
    elif number_matches == 4 and star_matches == 0:
        return 3
    elif number_matches == 3 and star_matches == 2:
        return 3
    elif number_matches == 2 and star_matches == 2:
        return 2
    elif number_matches == 3 and star_matches == 1:
        return 2
    elif number_matches == 3 and star_matches == 0:
        return 1
    elif number_matches == 1 and star_matches == 2:
        return 1
    elif number_matches == 2 and star_matches == 1:
        return 1
    else:
        return 0

def backtest_strategy_combinations(training_data, test_data):
    """Test all combinations of number strategies with star strategies"""
    
    number_strategies = ['risk_reward', 'coverage', 'frequency']
    star_strategies = ['frequency', 'balanced', 'overdue', 'markov', 'range_balanced']
    
    results = {}
    
    print("SEPARATE STRATEGY BACKTESTING")
    print("=" * 29)
    print("Testing number strategies vs star strategies independently")
    print()
    
    total_combinations = len(number_strategies) * len(star_strategies)
    combination_count = 0
    
    for num_strategy in number_strategies:
        for star_strategy in star_strategies:
            combination_count += 1
            print(f"Testing {combination_count}/{total_combinations}: {num_strategy} + {star_strategy}")
            
            total_score = 0
            total_number_matches = 0
            total_star_matches = 0
            combinations_tested = 0
            
            # Test against each draw in test period
            for test_row in test_data:
                date, n1, n2, n3, n4, n5, s1, s2 = test_row
                actual_numbers = sorted([n1, n2, n3, n4, n5])
                actual_stars = sorted([s1, s2])
                
                # Generate prediction using strategies
                try:
                    predicted_numbers = generate_number_strategies(training_data, num_strategy)
                    predicted_stars = generate_star_strategies(training_data, star_strategy)
                    
                    # Score the prediction
                    score = score_combination(predicted_numbers, predicted_stars, actual_numbers, actual_stars)
                    number_matches = len(set(predicted_numbers) & set(actual_numbers))
                    star_matches = len(set(predicted_stars) & set(actual_stars))
                    
                    total_score += score
                    total_number_matches += number_matches
                    total_star_matches += star_matches
                    combinations_tested += 1
                    
                except Exception as e:
                    print(f"   Error generating combination: {e}")
                    continue
            
            # Calculate averages
            if combinations_tested > 0:
                avg_score = total_score / combinations_tested
                avg_number_matches = total_number_matches / combinations_tested
                avg_star_matches = total_star_matches / combinations_tested
                
                results[f"{num_strategy}+{star_strategy}"] = {
                    'avg_score': avg_score,
                    'avg_number_matches': avg_number_matches,
                    'avg_star_matches': avg_star_matches,
                    'total_draws': combinations_tested,
                    'number_strategy': num_strategy,
                    'star_strategy': star_strategy
                }
                
                print(f"   Avg Score: {avg_score:.4f}, Number Matches: {avg_number_matches:.2f}, Star Matches: {avg_star_matches:.2f}")
            else:
                print(f"   No valid combinations generated")
    
    return results

def analyze_results(results):
    """Analyze the backtesting results"""
    
    print("\n" + "="*60)
    print("STRATEGY COMBINATION ANALYSIS")
    print("="*60)
    
    # Sort by average score
    sorted_results = sorted(results.items(), key=lambda x: x[1]['avg_score'], reverse=True)
    
    print("\nRANKING BY AVERAGE SCORE:")
    print("Rank | Number Strategy + Star Strategy         | Avg Score | Num Matches | Star Matches")
    print("-" * 85)
    
    for i, (combo_name, data) in enumerate(sorted_results, 1):
        num_strat = data['number_strategy']
        star_strat = data['star_strategy']
        print(f"{i:4d} | {num_strat:12s} + {star_strat:15s} | {data['avg_score']:9.4f} | {data['avg_number_matches']:11.2f} | {data['avg_star_matches']:12.2f}")
    
    # Analyze best star strategies for each number strategy
    print(f"\nBEST STAR STRATEGY FOR EACH NUMBER STRATEGY:")
    print("-" * 50)
    
    for num_strategy in ['risk_reward', 'coverage', 'frequency']:
        relevant_results = {k: v for k, v in results.items() if v['number_strategy'] == num_strategy}
        if relevant_results:
            best_combo = max(relevant_results.items(), key=lambda x: x[1]['avg_score'])
            best_star = best_combo[1]['star_strategy']
            best_score = best_combo[1]['avg_score']
            print(f"{num_strategy:12s}: {best_star:15s} (Score: {best_score:.4f})")
    
    # Analyze best number strategies for each star strategy
    print(f"\nBEST NUMBER STRATEGY FOR EACH STAR STRATEGY:")
    print("-" * 50)
    
    for star_strategy in ['frequency', 'balanced', 'overdue', 'markov', 'range_balanced']:
        relevant_results = {k: v for k, v in results.items() if v['star_strategy'] == star_strategy}
        if relevant_results:
            best_combo = max(relevant_results.items(), key=lambda x: x[1]['avg_score'])
            best_num = best_combo[1]['number_strategy']
            best_score = best_combo[1]['avg_score']
            print(f"{star_strategy:15s}: {best_num:12s} (Score: {best_score:.4f})")
    
    # Find if same strategy for both is optimal
    print(f"\nSAME vs DIFFERENT STRATEGY ANALYSIS:")
    print("-" * 40)
    
    same_strategy_scores = []
    different_strategy_scores = []
    
    for combo_name, data in results.items():
        if data['number_strategy'] == data['star_strategy']:
            same_strategy_scores.append(data['avg_score'])
        else:
            different_strategy_scores.append(data['avg_score'])
    
    if same_strategy_scores and different_strategy_scores:
        avg_same = np.mean(same_strategy_scores)
        avg_different = np.mean(different_strategy_scores)
        print(f"Same strategy for both:     {avg_same:.4f}")
        print(f"Different strategies:       {avg_different:.4f}")
        print(f"Difference:                 {avg_different - avg_same:+.4f}")
        
        if avg_different > avg_same:
            print("✅ Different strategies perform BETTER than same strategy")
        else:
            print("❌ Same strategy performs better than different strategies")

def main():
    """Run separate strategy backtesting"""
    
    training_data, test_data = get_backtest_data()
    print(f"Training data: {len(training_data)} draws (2004-2018)")
    print(f"Test data: {len(test_data)} draws (2019-2025)")
    print()
    
    results = backtest_strategy_combinations(training_data, test_data)
    analyze_results(results)

if __name__ == "__main__":
    main()