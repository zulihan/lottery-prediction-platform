"""
Quick test of French Loto lucky strategies vs number strategies
"""

import psycopg2
import os
from collections import Counter
import random

def get_data():
    """Get French Loto data"""
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    cursor.execute("SELECT date, n1, n2, n3, n4, n5, lucky FROM french_loto_drawings ORDER BY date")
    results = cursor.fetchall()
    conn.close()
    
    from datetime import datetime
    split_date = datetime.strptime('2019-01-01', '%Y-%m-%d').date()
    
    training = [row for row in results if row[0] < split_date]
    test = [row for row in results if row[0] >= split_date]
    
    return training, test

def score(pred_nums, pred_lucky, actual_nums, actual_lucky):
    """Score combination"""
    num_matches = len(set(pred_nums) & set(actual_nums))
    lucky_match = 1 if pred_lucky == actual_lucky else 0
    
    if num_matches == 5 and lucky_match == 1: return 100
    elif num_matches == 5: return 20
    elif num_matches == 4 and lucky_match == 1: return 10
    elif num_matches == 4: return 5
    elif num_matches == 3 and lucky_match == 1: return 3
    elif num_matches == 3: return 2
    elif num_matches == 2: return 1
    else: return 0

def test_combo(training, test, num_gen, lucky_gen):
    """Test a number+lucky strategy combination"""
    total_score = 0
    total_lucky = 0
    tests = 0
    
    for test_row in test[:100]:  # Limit tests for speed
        _, n1, n2, n3, n4, n5, actual_lucky = test_row
        actual_numbers = sorted([n1, n2, n3, n4, n5])
        
        try:
            pred_numbers = num_gen(training)
            pred_lucky = lucky_gen(training)
            
            s = score(pred_numbers, pred_lucky, actual_numbers, actual_lucky)
            lucky_match = 1 if pred_lucky == actual_lucky else 0
            
            total_score += s
            total_lucky += lucky_match
            tests += 1
        except:
            continue
    
    return (total_score / tests, total_lucky / tests) if tests > 0 else (0, 0)

def frequency_numbers(training):
    """Frequency-based numbers"""
    all_nums = []
    for row in training:
        all_nums.extend([row[1], row[2], row[3], row[4], row[5]])
    freq = Counter(all_nums)
    top = [n for n, _ in freq.most_common(15)]
    return sorted(random.sample(top, 5))

def coverage_numbers(training):
    """Coverage-based numbers"""
    return sorted(random.sample(range(1, 17), 2) + random.sample(range(17, 33), 2) + random.sample(range(33, 50), 1))

def frequency_lucky(training):
    """Most frequent lucky"""
    all_lucky = [row[6] for row in training]
    return Counter(all_lucky).most_common(1)[0][0]

def balanced_lucky(training):
    """Balanced lucky selection"""
    all_lucky = [row[6] for row in training]
    freq = Counter(all_lucky)
    top = [l for l, _ in freq.most_common(5)]
    return random.choice(top)

def time_series_lucky(training):
    """Recent trending lucky"""
    recent = training[-len(training)//5:]
    recent_lucky = [row[6] for row in recent]
    return Counter(recent_lucky).most_common(1)[0][0]

def correlation_lucky(training):
    """Lucky correlated with frequent numbers"""
    all_nums = []
    for row in training:
        all_nums.extend([row[1], row[2], row[3], row[4], row[5]])
    
    num_freq = Counter(all_nums)
    top_nums = [n for n, _ in num_freq.most_common(10)]
    
    lucky_scores = Counter()
    for row in training:
        nums = [row[1], row[2], row[3], row[4], row[5]]
        if any(n in top_nums for n in nums):
            lucky_scores[row[6]] += 1
    
    return lucky_scores.most_common(1)[0][0]

def main():
    """Test all combinations quickly"""
    
    training, test = get_data()
    print(f"Testing with {len(training)} training, {len(test)} test draws")
    
    num_strategies = {
        'frequency': frequency_numbers,
        'coverage': coverage_numbers
    }
    
    lucky_strategies = {
        'frequency': frequency_lucky,
        'balanced': balanced_lucky,
        'time_series': time_series_lucky,
        'correlation': correlation_lucky
    }
    
    results = []
    
    for num_name, num_func in num_strategies.items():
        for lucky_name, lucky_func in lucky_strategies.items():
            score_avg, lucky_avg = test_combo(training, test, num_func, lucky_func)
            results.append((f"{num_name}+{lucky_name}", score_avg, lucky_avg))
            print(f"{num_name} + {lucky_name}: Score {score_avg:.4f}, Lucky {lucky_avg:.2f}")
    
    print("\nRANKING:")
    for i, (combo, score_avg, lucky_avg) in enumerate(sorted(results, key=lambda x: x[1], reverse=True), 1):
        print(f"{i}. {combo}: {score_avg:.4f} (Lucky: {lucky_avg:.2f})")
    
    print("\nBEST LUCKY STRATEGIES:")
    for num_name in num_strategies.keys():
        best = max([r for r in results if r[0].startswith(num_name)], key=lambda x: x[1])
        lucky_name = best[0].split('+')[1]
        print(f"{num_name} numbers → {lucky_name} lucky: {best[1]:.4f}")

if __name__ == "__main__":
    main()