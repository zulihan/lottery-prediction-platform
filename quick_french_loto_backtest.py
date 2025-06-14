"""
Quick French Loto backtesting with optimized performance
"""

import psycopg2
import os
from collections import Counter
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

def score_loto(predicted_nums, predicted_lucky, actual_nums, actual_lucky):
    """Score French Loto combination"""
    num_matches = len(set(predicted_nums) & set(actual_nums))
    lucky_match = 1 if predicted_lucky == actual_lucky else 0
    
    if num_matches == 5 and lucky_match == 1:
        return 100
    elif num_matches == 5:
        return 20
    elif num_matches == 4 and lucky_match == 1:
        return 10
    elif num_matches == 4:
        return 5
    elif num_matches == 3 and lucky_match == 1:
        return 3
    elif num_matches == 3:
        return 2
    elif num_matches == 2:
        return 1
    else:
        return 0

def test_strategy(strategy_name, generator_func, training_data, test_data):
    """Test a single strategy"""
    
    total_score = 0
    total_num_matches = 0
    total_lucky_matches = 0
    tests = 0
    
    for test_row in test_data:
        date, n1, n2, n3, n4, n5, lucky = test_row
        actual_numbers = sorted([n1, n2, n3, n4, n5])
        actual_lucky = lucky
        
        try:
            predicted_numbers, predicted_lucky = generator_func(training_data)
            
            score = score_loto(predicted_numbers, predicted_lucky, actual_numbers, actual_lucky)
            num_matches = len(set(predicted_numbers) & set(actual_numbers))
            lucky_match = 1 if predicted_lucky == actual_lucky else 0
            
            total_score += score
            total_num_matches += num_matches
            total_lucky_matches += lucky_match
            tests += 1
            
        except:
            continue
    
    if tests > 0:
        return {
            'avg_score': total_score / tests,
            'avg_num_matches': total_num_matches / tests,
            'avg_lucky_matches': total_lucky_matches / tests,
            'total_tests': tests
        }
    return None

def risk_reward_generator(training_data):
    """Risk-Reward strategy for French Loto"""
    all_numbers = []
    all_lucky = []
    
    for row in training_data:
        _, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_lucky.append(lucky)
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
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
    
    # Fill if needed
    while len(combo) < 5:
        all_available = hot + warm + cold
        remaining = [n for n in all_available if n not in combo]
        if remaining:
            combo.append(random.choice(remaining))
        else:
            break
    
    top_lucky = [l for l, _ in lucky_freq.most_common(5)]
    combo_lucky = random.choice(top_lucky)
    
    return sorted(combo[:5]), combo_lucky

def coverage_generator(training_data):
    """Coverage Optimization strategy"""
    all_lucky = []
    for row in training_data:
        all_lucky.append(row[6])
    
    lucky_freq = Counter(all_lucky)
    
    # Range coverage: 1-16, 17-32, 33-49
    low = list(range(1, 17))
    mid = list(range(17, 33))
    high = list(range(33, 50))
    
    combo = []
    combo.extend(random.sample(low, 2))
    combo.extend(random.sample(mid, 2))
    combo.extend(random.sample(high, 1))
    
    top_lucky = [l for l, _ in lucky_freq.most_common(6)]
    combo_lucky = random.choice(top_lucky)
    
    return sorted(combo), combo_lucky

def frequency_generator(training_data):
    """Pure frequency strategy"""
    all_numbers = []
    all_lucky = []
    
    for row in training_data:
        _, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_lucky.append(lucky)
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    top_numbers = [n for n, _ in number_freq.most_common(15)]
    combo = random.sample(top_numbers, 5)
    combo_lucky = lucky_freq.most_common(1)[0][0]
    
    return sorted(combo), combo_lucky

def time_series_generator(training_data):
    """Time series strategy using recent trends"""
    recent_count = max(1, len(training_data) // 5)
    recent_data = training_data[-recent_count:]
    
    recent_numbers = []
    recent_lucky = []
    
    for row in recent_data:
        _, n1, n2, n3, n4, n5, lucky = row
        recent_numbers.extend([n1, n2, n3, n4, n5])
        recent_lucky.append(lucky)
    
    recent_freq = Counter(recent_numbers)
    recent_lucky_freq = Counter(recent_lucky)
    
    trending = [n for n, _ in recent_freq.most_common(12)]
    combo = random.sample(trending, 5)
    combo_lucky = recent_lucky_freq.most_common(1)[0][0]
    
    return sorted(combo), combo_lucky

def main():
    """Run comprehensive French Loto backtesting"""
    
    print("FRENCH LOTO COMPREHENSIVE BACKTESTING")
    print("=" * 37)
    
    data = get_french_loto_data()
    print(f"Total draws: {len(data)}")
    
    training_data, test_data = split_data(data)
    print(f"Training: {len(training_data)} draws")
    print(f"Test: {len(test_data)} draws")
    print()
    
    strategies = {
        'Risk-Reward': risk_reward_generator,
        'Coverage Optimization': coverage_generator,
        'Frequency Analysis': frequency_generator,
        'Time Series': time_series_generator
    }
    
    results = {}
    
    for name, generator in strategies.items():
        print(f"Testing {name}...")
        result = test_strategy(name, generator, training_data, test_data)
        if result:
            results[name] = result
            print(f"  Score: {result['avg_score']:.4f}, Numbers: {result['avg_num_matches']:.2f}, Lucky: {result['avg_lucky_matches']:.2f}")
        else:
            print(f"  Failed to generate results")
    
    print("\nSTRATEGY RANKING:")
    print("=" * 16)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['avg_score'], reverse=True)
    
    for i, (name, data) in enumerate(sorted_results, 1):
        score = data['avg_score']
        num_matches = data['avg_num_matches']
        lucky_matches = data['avg_lucky_matches']
        tests = data['total_tests']
        
        print(f"{i}. {name}")
        print(f"   Average Score: {score:.4f}")
        print(f"   Number Matches: {num_matches:.2f}/5 ({num_matches/5*100:.1f}%)")
        print(f"   Lucky Matches: {lucky_matches:.2f}/1 ({lucky_matches*100:.1f}%)")
        print(f"   Tests: {tests}")
        print()
    
    if sorted_results:
        best = sorted_results[0]
        worst = sorted_results[-1]
        improvement = (best[1]['avg_score'] - worst[1]['avg_score']) / worst[1]['avg_score'] * 100
        
        print("PERFORMANCE GAP:")
        print(f"Best: {best[0]} ({best[1]['avg_score']:.4f})")
        print(f"Worst: {worst[0]} ({worst[1]['avg_score']:.4f})")
        print(f"Improvement: {improvement:.1f}%")
        
        print(f"\nRECOMMENDATION:")
        print(f"Use {best[0]} strategy for optimal French Loto performance")
        print(f"Expected performance: {best[1]['avg_score']:.4f} average score")

if __name__ == "__main__":
    main()