"""
Separate backtesting for French Loto lucky number strategies vs number strategies
Test if lucky numbers perform better with different strategies than main numbers
"""

import psycopg2
import os
from collections import Counter, defaultdict
import random

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    return psycopg2.connect(database_url)

def get_french_loto_data():
    """Get French Loto historical data"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = """
    SELECT date, n1, n2, n3, n4, n5, lucky 
    FROM french_loto_drawings 
    ORDER BY date
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def split_data(data):
    """Split into training (before 2019) and test (2019+)"""
    from datetime import datetime
    split_date = datetime.strptime('2019-01-01', '%Y-%m-%d').date()
    
    training = [row for row in data if row[0] < split_date]
    test = [row for row in data if row[0] >= split_date]
    
    return training, test

def generate_lucky_strategies(training_data, strategy_type):
    """Generate lucky numbers using different strategies"""
    
    all_lucky = []
    all_numbers = []
    
    for row in training_data:
        _, n1, n2, n3, n4, n5, lucky = row
        all_lucky.append(lucky)
        all_numbers.extend([n1, n2, n3, n4, n5])
    
    lucky_freq = Counter(all_lucky)
    number_freq = Counter(all_numbers)
    
    if strategy_type == 'frequency':
        # Most frequent lucky numbers
        return lucky_freq.most_common(1)[0][0]
    
    elif strategy_type == 'balanced':
        # Mix of frequent and medium frequency
        top_lucky = [l for l, freq in lucky_freq.most_common(5)]
        medium_lucky = [l for l, freq in lucky_freq.most_common(10)[5:]]
        all_candidates = top_lucky + medium_lucky
        return random.choice(all_candidates)
    
    elif strategy_type == 'overdue':
        # Least frequent lucky numbers (contrarian)
        least_frequent = [l for l, freq in lucky_freq.most_common()[-5:]]
        return random.choice(least_frequent)
    
    elif strategy_type == 'time_series':
        # Recent trending lucky numbers
        recent_count = max(1, len(training_data) // 5)
        recent_data = training_data[-recent_count:]
        recent_lucky = [row[6] for row in recent_data]
        recent_freq = Counter(recent_lucky)
        return recent_freq.most_common(1)[0][0]
    
    elif strategy_type == 'number_correlation':
        # Lucky numbers that correlate with frequent main numbers
        number_lucky_pairs = defaultdict(Counter)
        
        for row in training_data:
            _, n1, n2, n3, n4, n5, lucky = row
            numbers = [n1, n2, n3, n4, n5]
            for num in numbers:
                number_lucky_pairs[num][lucky] += 1
        
        # Get most frequent numbers
        top_numbers = [n for n, freq in number_freq.most_common(10)]
        
        # Find lucky numbers that appear most with frequent numbers
        lucky_scores = Counter()
        for num in top_numbers:
            for lucky, count in number_lucky_pairs[num].items():
                lucky_scores[lucky] += count
        
        return lucky_scores.most_common(1)[0][0]

def generate_number_strategies(training_data, strategy_type):
    """Generate numbers using different strategies"""
    
    all_numbers = []
    for row in training_data:
        _, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
    
    number_freq = Counter(all_numbers)
    
    if strategy_type == 'risk_reward':
        sorted_nums = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
        total = len(sorted_nums)
        
        hot = [n for n, _ in sorted_nums[:total//3]]
        warm = [n for n, _ in sorted_nums[total//3:2*total//3]]
        cold = [n for n, _ in sorted_nums[2*total//3:]]
        
        combo = []
        combo.extend(random.sample(hot, min(2, len(hot))))
        remaining_warm = [n for n in warm if n not in combo]
        combo.extend(random.sample(remaining_warm, min(2, len(remaining_warm))))
        remaining_cold = [n for n in cold if n not in combo]
        if remaining_cold:
            combo.append(random.choice(remaining_cold))
        
        while len(combo) < 5:
            all_available = hot + warm + cold
            remaining = [n for n in all_available if n not in combo]
            if remaining:
                combo.append(random.choice(remaining))
            else:
                break
        
        return sorted(combo[:5])
    
    elif strategy_type == 'coverage':
        low = list(range(1, 17))
        mid = list(range(17, 33))
        high = list(range(33, 50))
        
        combo = []
        combo.extend(random.sample(low, 2))
        combo.extend(random.sample(mid, 2))
        combo.extend(random.sample(high, 1))
        
        return sorted(combo)
    
    elif strategy_type == 'frequency':
        top_numbers = [n for n, _ in number_freq.most_common(15)]
        combo = random.sample(top_numbers, 5)
        return sorted(combo)

def score_combination(predicted_numbers, predicted_lucky, actual_numbers, actual_lucky):
    """Score a combination against actual results"""
    
    number_matches = len(set(predicted_numbers) & set(actual_numbers))
    lucky_match = 1 if predicted_lucky == actual_lucky else 0
    
    if number_matches == 5 and lucky_match == 1:
        return 100
    elif number_matches == 5:
        return 20
    elif number_matches == 4 and lucky_match == 1:
        return 10
    elif number_matches == 4:
        return 5
    elif number_matches == 3 and lucky_match == 1:
        return 3
    elif number_matches == 3:
        return 2
    elif number_matches == 2:
        return 1
    else:
        return 0

def backtest_strategy_combinations(training_data, test_data):
    """Test all combinations of number strategies with lucky strategies"""
    
    number_strategies = ['risk_reward', 'coverage', 'frequency']
    lucky_strategies = ['frequency', 'balanced', 'overdue', 'time_series', 'number_correlation']
    
    results = {}
    
    print("SEPARATE LUCKY STRATEGY BACKTESTING")
    print("=" * 35)
    print("Testing number strategies vs lucky strategies independently")
    print()
    
    total_combinations = len(number_strategies) * len(lucky_strategies)
    combination_count = 0
    
    for num_strategy in number_strategies:
        for lucky_strategy in lucky_strategies:
            combination_count += 1
            print(f"Testing {combination_count}/{total_combinations}: {num_strategy} + {lucky_strategy}")
            
            total_score = 0
            total_number_matches = 0
            total_lucky_matches = 0
            combinations_tested = 0
            
            for test_row in test_data:
                _, n1, n2, n3, n4, n5, actual_lucky = test_row
                actual_numbers = sorted([n1, n2, n3, n4, n5])
                
                try:
                    predicted_numbers = generate_number_strategies(training_data, num_strategy)
                    predicted_lucky = generate_lucky_strategies(training_data, lucky_strategy)
                    
                    score = score_combination(predicted_numbers, predicted_lucky, actual_numbers, actual_lucky)
                    number_matches = len(set(predicted_numbers) & set(actual_numbers))
                    lucky_match = 1 if predicted_lucky == actual_lucky else 0
                    
                    total_score += score
                    total_number_matches += number_matches
                    total_lucky_matches += lucky_match
                    combinations_tested += 1
                    
                except Exception as e:
                    continue
            
            if combinations_tested > 0:
                avg_score = total_score / combinations_tested
                avg_number_matches = total_number_matches / combinations_tested
                avg_lucky_matches = total_lucky_matches / combinations_tested
                
                results[f"{num_strategy}+{lucky_strategy}"] = {
                    'avg_score': avg_score,
                    'avg_number_matches': avg_number_matches,
                    'avg_lucky_matches': avg_lucky_matches,
                    'total_draws': combinations_tested,
                    'number_strategy': num_strategy,
                    'lucky_strategy': lucky_strategy
                }
                
                print(f"   Score: {avg_score:.4f}, Numbers: {avg_number_matches:.2f}, Lucky: {avg_lucky_matches:.2f}")
            else:
                print(f"   No valid combinations generated")
    
    return results

def analyze_results(results):
    """Analyze the backtesting results"""
    
    print("\n" + "="*70)
    print("LUCKY STRATEGY COMBINATION ANALYSIS")
    print("="*70)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['avg_score'], reverse=True)
    
    print("\nRANKING BY AVERAGE SCORE:")
    print("Rank | Number Strategy + Lucky Strategy      | Avg Score | Num Matches | Lucky Matches")
    print("-" * 85)
    
    for i, (combo_name, data) in enumerate(sorted_results, 1):
        num_strat = data['number_strategy']
        lucky_strat = data['lucky_strategy']
        print(f"{i:4d} | {num_strat:12s} + {lucky_strat:15s} | {data['avg_score']:9.4f} | {data['avg_number_matches']:11.2f} | {data['avg_lucky_matches']:13.2f}")
    
    print(f"\nBEST LUCKY STRATEGY FOR EACH NUMBER STRATEGY:")
    print("-" * 52)
    
    for num_strategy in ['risk_reward', 'coverage', 'frequency']:
        relevant_results = {k: v for k, v in results.items() if v['number_strategy'] == num_strategy}
        if relevant_results:
            best_combo = max(relevant_results.items(), key=lambda x: x[1]['avg_score'])
            best_lucky = best_combo[1]['lucky_strategy']
            best_score = best_combo[1]['avg_score']
            lucky_accuracy = best_combo[1]['avg_lucky_matches']
            print(f"{num_strategy:12s}: {best_lucky:18s} (Score: {best_score:.4f}, Lucky: {lucky_accuracy:.2f})")
    
    print(f"\nBEST NUMBER STRATEGY FOR EACH LUCKY STRATEGY:")
    print("-" * 52)
    
    for lucky_strategy in ['frequency', 'balanced', 'overdue', 'time_series', 'number_correlation']:
        relevant_results = {k: v for k, v in results.items() if v['lucky_strategy'] == lucky_strategy}
        if relevant_results:
            best_combo = max(relevant_results.items(), key=lambda x: x[1]['avg_score'])
            best_num = best_combo[1]['number_strategy']
            best_score = best_combo[1]['avg_score']
            print(f"{lucky_strategy:18s}: {best_num:12s} (Score: {best_score:.4f})")
    
    print(f"\nSAME vs DIFFERENT STRATEGY ANALYSIS:")
    print("-" * 40)
    
    same_strategy_scores = []
    different_strategy_scores = []
    
    for combo_name, data in results.items():
        # Check if strategies have similar approach
        num_strat = data['number_strategy']
        lucky_strat = data['lucky_strategy']
        
        if (num_strat == 'frequency' and lucky_strat == 'frequency') or \
           (num_strat in ['risk_reward', 'coverage'] and lucky_strat in ['balanced', 'time_series']):
            same_strategy_scores.append(data['avg_score'])
        else:
            different_strategy_scores.append(data['avg_score'])
    
    if same_strategy_scores and different_strategy_scores:
        avg_same = sum(same_strategy_scores) / len(same_strategy_scores)
        avg_different = sum(different_strategy_scores) / len(different_strategy_scores)
        print(f"Similar strategy approach:   {avg_same:.4f}")
        print(f"Different strategies:        {avg_different:.4f}")
        print(f"Difference:                  {avg_different - avg_same:+.4f}")
        
        if avg_different > avg_same:
            print("✅ Different strategies perform BETTER for French Loto")
        else:
            print("❌ Similar strategies perform better")

def main():
    """Run separate lucky strategy backtesting"""
    
    data = get_french_loto_data()
    training_data, test_data = split_data(data)
    
    print(f"French Loto data: {len(data)} total draws")
    print(f"Training: {len(training_data)} draws (pre-2019)")
    print(f"Test: {len(test_data)} draws (2019-2025)")
    print()
    
    results = backtest_strategy_combinations(training_data, test_data)
    analyze_results(results)

if __name__ == "__main__":
    main()