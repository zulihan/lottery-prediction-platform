"""
Full historical backtesting on all 1,847 Euromillions draws (2004-2025)
More comprehensive analysis with time-based validation
"""

import psycopg2
import os
from collections import Counter, defaultdict
import random
from datetime import datetime

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    else:
        raise Exception("No database connection available")

def get_all_historical_data():
    """Get all historical Euromillions data"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = """
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date ASC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.close()
    return results

def time_based_split(historical_data, train_years=15):
    """Split data chronologically - use first 15 years for training, rest for testing"""
    
    total_draws = len(historical_data)
    print(f"Total historical draws: {total_draws}")
    print(f"Date range: {historical_data[0][0]} to {historical_data[-1][0]}")
    
    # Split based on years rather than percentage for more realistic validation
    train_cutoff_year = 2004 + train_years  # Train on 2004-2019, test on 2020-2025
    
    training_data = []
    testing_data = []
    
    for row in historical_data:
        date = row[0]
        year = date.year if hasattr(date, 'year') else int(str(date)[:4])
        
        if year < train_cutoff_year:
            training_data.append(row)
        else:
            testing_data.append(row)
    
    print(f"Training data: {len(training_data)} draws (2004-{train_cutoff_year-1})")
    print(f"Testing data: {len(testing_data)} draws ({train_cutoff_year}-2025)")
    
    return training_data, testing_data

def generate_frequency_strategy(training_data, num_combos=10):
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
        # Vary the frequency selection
        start_idx = i * 2
        top_numbers = [n for n, freq in number_freq.most_common(40)]
        combo_numbers = top_numbers[start_idx:start_idx+5]
        
        top_stars = [s for s, freq in star_freq.most_common(8)]
        combo_stars = top_stars[i%6:i%6+2] if i%6+1 < len(top_stars) else top_stars[:2]
        
        combinations.append({
            'numbers': sorted(combo_numbers),
            'stars': sorted(combo_stars),
            'strategy': 'Frequency Analysis'
        })
    
    return combinations

def generate_markov_strategy(training_data, num_combos=10):
    """Generate combinations using Markov chain analysis"""
    
    # Build comprehensive transition matrix
    number_transitions = defaultdict(Counter)
    star_transitions = defaultdict(Counter)
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        numbers = sorted([n1, n2, n3, n4, n5])
        stars = sorted([s1, s2])
        
        # Build number transitions
        for i in range(len(numbers) - 1):
            current = numbers[i]
            next_num = numbers[i + 1]
            number_transitions[current][next_num] += 1
        
        # Build star transitions
        if len(stars) > 1:
            star_transitions[stars[0]][stars[1]] += 1
    
    # Get frequency for fallback
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
        # Start with different frequent numbers for variation
        start_candidates = [n for n, freq in number_freq.most_common(25)]
        start_num = start_candidates[i % len(start_candidates)]
        
        combo_numbers = [start_num]
        current = start_num
        
        # Generate using Markov chain
        for _ in range(4):
            if current in number_transitions and number_transitions[current]:
                next_options = number_transitions[current]
                candidates = [num for num in next_options.keys() if num not in combo_numbers]
                
                if candidates:
                    weights = [next_options[num] for num in candidates]
                    next_num = random.choices(candidates, weights=weights)[0]
                    combo_numbers.append(next_num)
                    current = next_num
                else:
                    # Fallback
                    remaining = [n for n in start_candidates if n not in combo_numbers]
                    if remaining:
                        next_num = random.choice(remaining)
                        combo_numbers.append(next_num)
                        current = next_num
            else:
                # Fallback to frequent numbers
                remaining = [n for n in start_candidates if n not in combo_numbers]
                if remaining:
                    next_num = random.choice(remaining)
                    combo_numbers.append(next_num)
                    current = next_num
        
        # Generate stars
        star_candidates = [s for s, freq in star_freq.most_common(8)]
        combo_stars = random.sample(star_candidates, 2)
        
        combinations.append({
            'numbers': sorted(combo_numbers[:5]),
            'stars': sorted(combo_stars),
            'strategy': 'Markov Chain'
        })
    
    return combinations

def generate_coverage_strategy(training_data, num_combos=10):
    """Generate combinations using coverage optimization"""
    
    all_numbers = []
    all_stars = []
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    # Range analysis
    low_numbers = [n for n in all_numbers if 1 <= n <= 16]
    mid_numbers = [n for n in all_numbers if 17 <= n <= 33]
    high_numbers = [n for n in all_numbers if 34 <= n <= 49]
    
    low_freq = Counter(low_numbers)
    mid_freq = Counter(mid_numbers)
    high_freq = Counter(high_numbers)
    star_freq = Counter(all_stars)
    
    coverage_patterns = [
        (2, 2, 1), (1, 3, 1), (1, 2, 2), (2, 1, 2), (1, 1, 3),
        (3, 1, 1), (1, 4, 0), (0, 3, 2), (2, 0, 3), (0, 2, 3)
    ]
    
    combinations = []
    
    for i in range(num_combos):
        pattern = coverage_patterns[i % len(coverage_patterns)]
        low_count, mid_count, high_count = pattern
        
        combo_numbers = []
        
        if low_count > 0 and low_freq:
            low_candidates = [n for n, freq in low_freq.most_common(15)]
            selected = random.sample(low_candidates, min(low_count, len(low_candidates)))
            combo_numbers.extend(selected)
        
        if mid_count > 0 and mid_freq:
            mid_candidates = [n for n, freq in mid_freq.most_common(20)]
            mid_candidates = [n for n in mid_candidates if n not in combo_numbers]
            selected = random.sample(mid_candidates, min(mid_count, len(mid_candidates)))
            combo_numbers.extend(selected)
        
        if high_count > 0 and high_freq:
            high_candidates = [n for n, freq in high_freq.most_common(15)]
            high_candidates = [n for n in high_candidates if n not in combo_numbers]
            selected = random.sample(high_candidates, min(high_count, len(high_candidates)))
            combo_numbers.extend(selected)
        
        # Fill remaining
        while len(combo_numbers) < 5:
            all_freq = Counter(all_numbers)
            remaining = [n for n, freq in all_freq.most_common(35) if n not in combo_numbers]
            if remaining:
                combo_numbers.append(random.choice(remaining))
            else:
                break
        
        top_stars = [s for s, freq in star_freq.most_common(8)]
        combo_stars = random.sample(top_stars, min(2, len(top_stars)))
        
        combinations.append({
            'numbers': sorted(combo_numbers[:5]),
            'stars': sorted(combo_stars),
            'strategy': 'Coverage Optimization'
        })
    
    return combinations

def generate_risk_reward_strategy(training_data, num_combos=10):
    """Generate combinations using risk-reward analysis"""
    
    all_numbers = []
    all_stars = []
    
    for row in training_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Categorize by frequency
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    total_numbers = len(sorted_numbers)
    
    hot_numbers = [n for n, freq in sorted_numbers[:total_numbers//3]]
    warm_numbers = [n for n, freq in sorted_numbers[total_numbers//3:2*total_numbers//3]]
    cold_numbers = [n for n, freq in sorted_numbers[2*total_numbers//3:]]
    
    risk_profiles = [
        {'hot': 4, 'warm': 1, 'cold': 0},  # Conservative
        {'hot': 3, 'warm': 2, 'cold': 0},  # Moderate Conservative
        {'hot': 3, 'warm': 1, 'cold': 1},  # Moderate
        {'hot': 2, 'warm': 2, 'cold': 1},  # Balanced
        {'hot': 2, 'warm': 1, 'cold': 2},  # Moderate Aggressive
        {'hot': 1, 'warm': 2, 'cold': 2},  # Aggressive
        {'hot': 1, 'warm': 1, 'cold': 3},  # Very Aggressive
        {'hot': 0, 'warm': 2, 'cold': 3},  # Contrarian
        {'hot': 2, 'warm': 3, 'cold': 0},  # Warm Focus
        {'hot': 1, 'warm': 3, 'cold': 1}   # Warm Balanced
    ]
    
    combinations = []
    
    for i in range(num_combos):
        profile = risk_profiles[i % len(risk_profiles)]
        combo_numbers = []
        
        if profile['hot'] > 0 and hot_numbers:
            selected = random.sample(hot_numbers, min(profile['hot'], len(hot_numbers)))
            combo_numbers.extend(selected)
        
        if profile['warm'] > 0 and warm_numbers:
            available = [n for n in warm_numbers if n not in combo_numbers]
            selected = random.sample(available, min(profile['warm'], len(available)))
            combo_numbers.extend(selected)
        
        if profile['cold'] > 0 and cold_numbers:
            available = [n for n in cold_numbers if n not in combo_numbers]
            selected = random.sample(available, min(profile['cold'], len(available)))
            combo_numbers.extend(selected)
        
        # Fill remaining
        while len(combo_numbers) < 5:
            all_available = hot_numbers + warm_numbers + cold_numbers
            remaining = [n for n in all_available if n not in combo_numbers]
            if remaining:
                combo_numbers.append(random.choice(remaining))
            else:
                break
        
        top_stars = [s for s, freq in star_freq.most_common(8)]
        combo_stars = random.sample(top_stars, min(2, len(top_stars)))
        
        combinations.append({
            'numbers': sorted(combo_numbers[:5]),
            'stars': sorted(combo_stars),
            'strategy': 'Risk-Reward'
        })
    
    return combinations

def test_strategy_on_full_history(strategy_combinations, test_data):
    """Test strategy against full historical test data"""
    
    total_score = 0
    total_draws = len(test_data)
    score_distribution = Counter()
    monthly_performance = defaultdict(list)
    
    print(f"  Testing {len(strategy_combinations)} combinations against {total_draws} draws...")
    
    for i, draw in enumerate(test_data):
        if i % 50 == 0:
            print(f"    Progress: {i}/{total_draws} draws processed")
        
        date, n1, n2, n3, n4, n5, s1, s2 = draw
        actual_numbers = [n1, n2, n3, n4, n5]
        actual_stars = [s1, s2]
        
        # Test all combinations for this draw
        best_score = 0
        for combo in strategy_combinations:
            number_matches = len(set(combo['numbers']) & set(actual_numbers))
            star_matches = len(set(combo['stars']) & set(actual_stars))
            combo_score = number_matches + star_matches
            
            if combo_score > best_score:
                best_score = combo_score
        
        total_score += best_score
        score_distribution[best_score] += 1
        
        # Track monthly performance
        month_key = f"{date.year}-{date.month:02d}" if hasattr(date, 'year') else str(date)[:7]
        monthly_performance[month_key].append(best_score)
    
    avg_score = total_score / total_draws
    
    return {
        'total_score': total_score,
        'average_score': avg_score,
        'total_draws': total_draws,
        'score_distribution': score_distribution,
        'monthly_performance': monthly_performance
    }

def run_full_historical_backtest():
    """Run comprehensive backtest on all historical data"""
    
    print("FULL HISTORICAL BACKTESTING - 1,847 DRAWS")
    print("=" * 42)
    
    # Load all historical data
    print("Loading all historical data...")
    historical_data = get_all_historical_data()
    
    # Split chronologically
    training_data, testing_data = time_based_split(historical_data, train_years=15)
    
    print(f"\nGenerating strategies using {len(training_data)} training draws...")
    print("Testing against recent years for realistic validation")
    print()
    
    # Generate strategies
    strategies = [
        ('Frequency Analysis', generate_frequency_strategy),
        ('Markov Chain', generate_markov_strategy),
        ('Coverage Optimization', generate_coverage_strategy),
        ('Risk-Reward', generate_risk_reward_strategy)
    ]
    
    strategy_results = []
    
    for strategy_name, generator_func in strategies:
        print(f"Testing {strategy_name}...")
        
        combinations = generator_func(training_data, num_combos=10)
        performance = test_strategy_on_full_history(combinations, testing_data)
        performance['strategy_name'] = strategy_name
        
        strategy_results.append(performance)
        
        print(f"  Average score: {performance['average_score']:.4f}")
        print(f"  Total score: {performance['total_score']}")
        print()
    
    return strategy_results

def analyze_full_results(strategy_results):
    """Analyze results from full historical backtest"""
    
    print("FULL HISTORICAL BACKTEST RESULTS")
    print("-" * 33)
    
    # Sort by performance
    sorted_results = sorted(strategy_results, key=lambda x: x['average_score'], reverse=True)
    
    for i, result in enumerate(sorted_results, 1):
        print(f"{i}. {result['strategy_name']}")
        print(f"   Average Score: {result['average_score']:.4f}")
        print(f"   Total Score: {result['total_score']}")
        
        # Score distribution
        dist = result['score_distribution']
        print(f"   Score Distribution:")
        for score in sorted(dist.keys(), reverse=True):
            count = dist[score]
            percentage = (count / result['total_draws']) * 100
            print(f"     {score} points: {count} draws ({percentage:.1f}%)")
        print()
    
    # Performance comparison
    best = sorted_results[0]
    worst = sorted_results[-1]
    gap = best['average_score'] - worst['average_score']
    
    print("INSIGHTS:")
    print(f"• Best strategy: {best['strategy_name']} ({best['average_score']:.4f} avg)")
    print(f"• Worst strategy: {worst['strategy_name']} ({worst['average_score']:.4f} avg)")
    print(f"• Performance gap: {gap:.4f} points per draw")
    print(f"• Sample size: {best['total_draws']} draws over 5+ years")

def main():
    """Run full historical backtesting"""
    
    strategy_results = run_full_historical_backtest()
    analyze_full_results(strategy_results)

if __name__ == "__main__":
    main()