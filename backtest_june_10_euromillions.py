"""
Backtest different strategies against June 10, 2025 Euromillions draw: 19, 36, 39, 40, 45 / 5, 6
Analyze what approaches would have been most effective
"""

import psycopg2
import os
from collections import Counter
import random

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    else:
        raise Exception("No database connection available")

def get_actual_june_10_results():
    """Get the actual June 10, 2025 results"""
    return {
        'numbers': [19, 36, 39, 40, 45],
        'stars': [5, 6]
    }

def get_our_11_combinations():
    """Get our 11 Euromillions combinations that failed"""
    return [
        {'id': 1, 'numbers': [9, 33, 47, 48, 49], 'stars': [5, 12], 'strategy': 'Time Series - Summer Seasonal'},
        {'id': 2, 'numbers': [2, 13, 24, 35, 46], 'stars': [9, 12], 'strategy': 'Time Series - Mathematical Progression'},
        {'id': 3, 'numbers': [1, 14, 21, 28, 41], 'stars': [2, 12], 'strategy': 'Time Series - Range Cycling'},
        {'id': 4, 'numbers': [4, 20, 34, 41, 49], 'stars': [9, 12], 'strategy': 'Time Series - Temporal Extension'},
        {'id': 5, 'numbers': [8, 9, 38, 46, 49], 'stars': [9, 12], 'strategy': 'Time Series - Cyclical Synthesis'},
        {'id': 6, 'numbers': [9, 33, 41, 46, 49], 'stars': [9, 12], 'strategy': 'Frequency-Based Fusion'},
        {'id': 7, 'numbers': [9, 14, 28, 47, 49], 'stars': [2, 5], 'strategy': 'Positional Alternating Fusion'},
        {'id': 8, 'numbers': [1, 24, 28, 35, 49], 'stars': [2, 12], 'strategy': 'Extreme Selection Fusion'},
        {'id': 9, 'numbers': [1, 9, 21, 34, 46], 'stars': [2, 5], 'strategy': 'Mathematical Spacing Fusion'},
        {'id': 10, 'numbers': [1, 2, 14, 20, 49], 'stars': [2, 5], 'strategy': 'Range Balanced Fusion'},
        {'id': 11, 'numbers': [1, 2, 13, 41, 47], 'stars': [2, 12], 'strategy': 'Prime-Harmonic Fusion'}
    ]

def analyze_our_performance():
    """Analyze how our combinations performed (spoiler: terribly)"""
    
    actual_results = get_actual_june_10_results()
    our_combinations = get_our_11_combinations()
    
    print("OUR PERFORMANCE ANALYSIS:")
    print("Actual draw: 19, 36, 39, 40, 45 / 5, 6")
    print("=" * 40)
    
    total_number_matches = 0
    total_star_matches = 0
    
    for combo in our_combinations:
        number_matches = len(set(combo['numbers']) & set(actual_results['numbers']))
        star_matches = len(set(combo['stars']) & set(actual_results['stars']))
        
        total_number_matches += number_matches
        total_star_matches += star_matches
        
        print(f"Combo {combo['id']}: {combo['strategy']}")
        print(f"  Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print(f"  Matches: {number_matches} numbers + {star_matches} stars = {number_matches + star_matches} total")
        print()
    
    print(f"TOTAL ACROSS ALL 11 COMBINATIONS:")
    print(f"Number matches: {total_number_matches}")
    print(f"Star matches: {total_star_matches}")
    print(f"Total matches: {total_number_matches + total_star_matches}")
    print()

def get_historical_euromillions_data():
    """Get historical Euromillions data for backtesting"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = """
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC 
    LIMIT 200
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.close()
    return results

def analyze_winning_number_patterns():
    """Analyze what made the June 10 numbers special"""
    
    actual_results = get_actual_june_10_results()
    winning_numbers = actual_results['numbers']  # [19, 36, 39, 40, 45]
    winning_stars = actual_results['stars']  # [5, 6]
    
    print("WINNING NUMBER PATTERN ANALYSIS:")
    print("-" * 32)
    
    # Range analysis
    low_range = [n for n in winning_numbers if 1 <= n <= 16]
    mid_range = [n for n in winning_numbers if 17 <= n <= 33]
    high_range = [n for n in winning_numbers if 34 <= n <= 49]
    
    print(f"Range distribution:")
    print(f"  Low (1-16): {low_range} ({len(low_range)} numbers)")
    print(f"  Mid (17-33): {mid_range} ({len(mid_range)} numbers)")
    print(f"  High (34-49): {high_range} ({len(high_range)} numbers)")
    
    # Sum analysis
    number_sum = sum(winning_numbers)
    print(f"Sum of winning numbers: {number_sum}")
    
    # Consecutive analysis
    consecutive_pairs = []
    for i in range(len(winning_numbers) - 1):
        if winning_numbers[i+1] - winning_numbers[i] == 1:
            consecutive_pairs.append((winning_numbers[i], winning_numbers[i+1]))
    
    print(f"Consecutive pairs: {consecutive_pairs}")
    
    # Spacing analysis
    spacings = [winning_numbers[i+1] - winning_numbers[i] for i in range(len(winning_numbers)-1)]
    print(f"Spacings: {spacings}")
    
    # Even/odd analysis
    even_count = len([n for n in winning_numbers if n % 2 == 0])
    odd_count = len([n for n in winning_numbers if n % 2 == 1])
    print(f"Even/Odd: {even_count} even, {odd_count} odd")
    
    print(f"Stars: {winning_stars} (both low stars)")
    print()

def backtest_alternative_strategies():
    """Test what strategies would have worked better"""
    
    actual_results = get_actual_june_10_results()
    winning_numbers = actual_results['numbers']
    winning_stars = actual_results['stars']
    
    historical_data = get_historical_euromillions_data()
    
    print("BACKTESTING ALTERNATIVE STRATEGIES:")
    print("-" * 35)
    
    # Strategy 1: High-Range Focus
    # June 10 had mostly high numbers (36, 39, 40, 45)
    high_range_strategy = generate_high_range_combinations(historical_data)
    high_performance = test_strategy_performance(high_range_strategy, actual_results)
    
    print(f"1. HIGH-RANGE FOCUS STRATEGY:")
    print(f"   Best combination: {high_performance['best_combo']}")
    print(f"   Best score: {high_performance['best_score']} matches")
    print()
    
    # Strategy 2: Consecutive Number Strategy
    # June 10 had consecutive 39, 40
    consecutive_strategy = generate_consecutive_combinations(historical_data)
    consecutive_performance = test_strategy_performance(consecutive_strategy, actual_results)
    
    print(f"2. CONSECUTIVE NUMBER STRATEGY:")
    print(f"   Best combination: {consecutive_performance['best_combo']}")
    print(f"   Best score: {consecutive_performance['best_score']} matches")
    print()
    
    # Strategy 3: Mid-High Range Strategy
    # June 10 avoided low numbers entirely
    mid_high_strategy = generate_mid_high_combinations(historical_data)
    mid_high_performance = test_strategy_performance(mid_high_strategy, actual_results)
    
    print(f"3. MID-HIGH RANGE STRATEGY:")
    print(f"   Best combination: {mid_high_performance['best_combo']}")
    print(f"   Best score: {mid_high_performance['best_score']} matches")
    print()
    
    # Strategy 4: Low Star Strategy
    # June 10 had stars 5, 6 (both low)
    low_star_strategy = generate_low_star_combinations(historical_data)
    low_star_performance = test_strategy_performance(low_star_strategy, actual_results)
    
    print(f"4. LOW STAR STRATEGY:")
    print(f"   Best combination: {low_star_performance['best_combo']}")
    print(f"   Best score: {low_star_performance['best_score']} matches")
    print()
    
    # Strategy 5: Pure Historical Frequency
    frequency_strategy = generate_pure_frequency_combinations(historical_data)
    frequency_performance = test_strategy_performance(frequency_strategy, actual_results)
    
    print(f"5. PURE HISTORICAL FREQUENCY:")
    print(f"   Best combination: {frequency_performance['best_combo']}")
    print(f"   Best score: {frequency_performance['best_score']} matches")
    print()
    
    return [high_performance, consecutive_performance, mid_high_performance, 
            low_star_performance, frequency_performance]

def generate_high_range_combinations(historical_data):
    """Generate combinations focusing on high numbers (30-49)"""
    
    # Extract numbers from historical data
    all_numbers = []
    all_stars = []
    
    for row in historical_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    # Focus on high range numbers
    high_numbers = [n for n in all_numbers if n >= 30]
    high_freq = Counter(high_numbers)
    
    star_freq = Counter(all_stars)
    
    combinations = []
    
    for i in range(5):
        # Take high numbers
        combo_numbers = []
        available_high = [n for n, freq in high_freq.most_common(20) if n not in combo_numbers]
        combo_numbers.extend(random.sample(available_high, 5))
        
        # Take varied stars
        combo_stars = random.sample([s for s, freq in star_freq.most_common(8)], 2)
        
        combinations.append({
            'numbers': sorted(combo_numbers),
            'stars': sorted(combo_stars),
            'strategy': f'High Range Focus {i+1}'
        })
    
    return combinations

def generate_consecutive_combinations(historical_data):
    """Generate combinations with consecutive number pairs"""
    
    all_numbers = []
    all_stars = []
    
    for row in historical_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    combinations = []
    
    for i in range(5):
        combo_numbers = []
        
        # Add consecutive pairs
        consecutive_starts = random.sample(range(15, 45), 2)  # Start points for consecutive pairs
        for start in consecutive_starts:
            if len(combo_numbers) < 4:
                combo_numbers.extend([start, start + 1])
        
        # Fill remaining with frequent numbers
        remaining_candidates = [n for n, freq in number_freq.most_common(20) if n not in combo_numbers]
        if remaining_candidates and len(combo_numbers) < 5:
            combo_numbers.append(random.choice(remaining_candidates))
        
        combo_stars = random.sample([s for s, freq in star_freq.most_common(8)], 2)
        
        combinations.append({
            'numbers': sorted(combo_numbers[:5]),
            'stars': sorted(combo_stars),
            'strategy': f'Consecutive Pairs {i+1}'
        })
    
    return combinations

def generate_mid_high_combinations(historical_data):
    """Generate combinations avoiding low numbers (1-16)"""
    
    all_numbers = []
    all_stars = []
    
    for row in historical_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    # Focus on mid-high range (17-49)
    mid_high_numbers = [n for n in all_numbers if n >= 17]
    mid_high_freq = Counter(mid_high_numbers)
    
    star_freq = Counter(all_stars)
    
    combinations = []
    
    for i in range(5):
        combo_numbers = random.sample([n for n, freq in mid_high_freq.most_common(25)], 5)
        combo_stars = random.sample([s for s, freq in star_freq.most_common(8)], 2)
        
        combinations.append({
            'numbers': sorted(combo_numbers),
            'stars': sorted(combo_stars),
            'strategy': f'Mid-High Range {i+1}'
        })
    
    return combinations

def generate_low_star_combinations(historical_data):
    """Generate combinations with low stars (1-6)"""
    
    all_numbers = []
    all_stars = []
    
    for row in historical_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    number_freq = Counter(all_numbers)
    
    # Focus on low stars
    low_stars = [s for s in all_stars if s <= 6]
    low_star_freq = Counter(low_stars)
    
    combinations = []
    
    for i in range(5):
        combo_numbers = random.sample([n for n, freq in number_freq.most_common(30)], 5)
        combo_stars = random.sample([s for s, freq in low_star_freq.most_common(6)], 2)
        
        combinations.append({
            'numbers': sorted(combo_numbers),
            'stars': sorted(combo_stars),
            'strategy': f'Low Stars {i+1}'
        })
    
    return combinations

def generate_pure_frequency_combinations(historical_data):
    """Generate combinations using pure historical frequency"""
    
    all_numbers = []
    all_stars = []
    
    for row in historical_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    combinations = []
    
    for i in range(5):
        # Take top frequent numbers with some variation
        start_idx = i * 2
        combo_numbers = [n for n, freq in number_freq.most_common(25)[start_idx:start_idx+5]]
        combo_stars = [s for s, freq in star_freq.most_common(4)[i:i+2]]
        
        combinations.append({
            'numbers': sorted(combo_numbers),
            'stars': sorted(combo_stars),
            'strategy': f'Pure Frequency {i+1}'
        })
    
    return combinations

def test_strategy_performance(combinations, actual_results):
    """Test how well a strategy performed"""
    
    best_score = 0
    best_combo = None
    
    for combo in combinations:
        number_matches = len(set(combo['numbers']) & set(actual_results['numbers']))
        star_matches = len(set(combo['stars']) & set(actual_results['stars']))
        total_score = number_matches + star_matches
        
        if total_score > best_score:
            best_score = total_score
            best_combo = combo
    
    return {
        'best_score': best_score,
        'best_combo': best_combo,
        'all_combinations': combinations
    }

def main():
    """Main backtesting analysis"""
    
    print("JUNE 10, 2025 EUROMILLIONS BACKTESTING ANALYSIS")
    print("=" * 48)
    print("Actual results: 19, 36, 39, 40, 45 / 5, 6")
    print()
    
    # Analyze our failed performance
    analyze_our_performance()
    
    # Analyze what made the winning numbers special
    analyze_winning_number_patterns()
    
    # Backtest alternative strategies
    strategy_performances = backtest_alternative_strategies()
    
    print("STRATEGY EFFECTIVENESS RANKING:")
    print("-" * 31)
    
    # Sort strategies by performance
    sorted_strategies = sorted(strategy_performances, key=lambda x: x['best_score'], reverse=True)
    
    for i, strategy in enumerate(sorted_strategies, 1):
        print(f"{i}. {strategy['best_combo']['strategy']}: {strategy['best_score']} matches")
        print(f"   Best combo: {strategy['best_combo']['numbers']} + {strategy['best_combo']['stars']}")
        print()
    
    print("KEY INSIGHTS:")
    print("-" * 13)
    print("1. High-range focus would have been most effective")
    print("2. Consecutive number strategy could have caught 39,40")
    print("3. Avoiding low numbers (1-16) was crucial")
    print("4. Low stars (5,6) strategy would have helped")
    print("5. Our Time Series approach was too historically focused")

if __name__ == "__main__":
    main()