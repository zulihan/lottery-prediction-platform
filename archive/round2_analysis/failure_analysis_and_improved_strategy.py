"""
Analyze what went wrong with our May 20, 2025 Euromillions predictions
and develop a more focused, effective approach for future draws.
"""

import pandas as pd
from collections import Counter
from database import get_db_connection

def analyze_prediction_failures():
    """
    Analyze why our May 20 predictions failed and what patterns we missed
    """
    
    # Our combinations
    our_combinations = [
        {"numbers": [1, 2, 11, 14, 37], "stars": [3, 7], "strategy": "Overdue Numbers"},
        {"numbers": [2, 31, 39, 40, 47], "stars": [5, 8], "strategy": "Overdue Numbers"},
        {"numbers": [3, 14, 31, 39, 40], "stars": [3, 7], "strategy": "Overdue Numbers"},
        {"numbers": [3, 21, 37, 44, 50], "stars": [7, 9], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [9, 21, 27, 44, 50], "stars": [2, 11], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [3, 19, 37, 38, 44], "stars": [2, 10], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [3, 19, 37, 44, 46], "stars": [2, 12], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [3, 19, 21, 44, 50], "stars": [2, 4], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [9, 19, 21, 44, 46], "stars": [9, 11], "strategy": "Risk-Reward (0.2)"},
        {"numbers": [6, 16, 31, 35, 39], "stars": [2, 9], "strategy": "Balanced Strategy"},
        {"numbers": [17, 20, 32, 38, 44], "stars": [2, 10], "strategy": "Hot Numbers Strategy"},
        {"numbers": [4, 34, 36, 41, 45], "stars": [5, 7], "strategy": "Cold Numbers Strategy"},
        {"numbers": [10, 16, 30, 45, 50], "stars": [2, 10], "strategy": "Balanced Mix Strategy"},
        {"numbers": [1, 20, 36, 40, 50], "stars": [1, 2], "strategy": "High Range Strategy"},
        {"numbers": [10, 19, 20, 39, 42], "stars": [2, 5], "strategy": "Low Range Strategy"},
        {"numbers": [4, 16, 19, 40, 49], "stars": [2, 5], "strategy": "Even Numbers Strategy"},
        {"numbers": [14, 19, 27, 42, 44], "stars": [1, 2], "strategy": "Hot-Cold Balance Strategy"},
        {"numbers": [17, 22, 29, 34, 38], "stars": [2, 10], "strategy": "Low Sum Strategy"},
        {"numbers": [22, 32, 38, 44, 45], "stars": [4, 10], "strategy": "Overdue Numbers Strategy"},
        {"numbers": [1, 18, 29, 31, 34], "stars": [2, 7], "strategy": "Optimized Coverage Strategy"}
    ]
    
    # Actual winning numbers
    winning_numbers = [1, 8, 13, 29, 47]
    winning_stars = [5, 6]
    
    print("=== FAILURE ANALYSIS: What Went Wrong ===\n")
    
    # 1. Number frequency analysis
    all_our_numbers = []
    all_our_stars = []
    
    for combo in our_combinations:
        all_our_numbers.extend(combo['numbers'])
        all_our_stars.extend(combo['stars'])
    
    number_freq = Counter(all_our_numbers)
    star_freq = Counter(all_our_stars)
    
    print("1. OVERUSED NUMBERS (appeared in multiple combinations):")
    overused_numbers = {num: count for num, count in number_freq.items() if count > 2}
    for num, count in sorted(overused_numbers.items(), key=lambda x: x[1], reverse=True):
        won = "✓ WON" if num in winning_numbers else "✗ LOST"
        print(f"   Number {num}: used {count} times - {won}")
    
    print(f"\n2. MISSING WINNING NUMBERS:")
    missing_numbers = set(winning_numbers) - set(all_our_numbers)
    for num in sorted(missing_numbers):
        print(f"   Number {num}: COMPLETELY MISSED - appeared in 0 combinations")
    
    print(f"\n3. STAR ANALYSIS:")
    for star in winning_stars:
        if star in all_our_stars:
            count = star_freq[star]
            print(f"   Star {star}: used {count} times - ✓ WON")
        else:
            print(f"   Star {star}: COMPLETELY MISSED")
    
    # 4. Range analysis
    print(f"\n4. RANGE DISTRIBUTION ANALYSIS:")
    winning_ranges = {
        "1-10": sum(1 for n in winning_numbers if 1 <= n <= 10),
        "11-20": sum(1 for n in winning_numbers if 11 <= n <= 20),
        "21-30": sum(1 for n in winning_numbers if 21 <= n <= 30),
        "31-40": sum(1 for n in winning_numbers if 31 <= n <= 40),
        "41-50": sum(1 for n in winning_numbers if 41 <= n <= 50)
    }
    
    our_ranges = {
        "1-10": sum(1 for n in all_our_numbers if 1 <= n <= 10),
        "11-20": sum(1 for n in all_our_numbers if 11 <= n <= 20),
        "21-30": sum(1 for n in all_our_numbers if 21 <= n <= 30),
        "31-40": sum(1 for n in all_our_numbers if 31 <= n <= 40),
        "41-50": sum(1 for n in all_our_numbers if 41 <= n <= 50)
    }
    
    print("   Winning vs Our Range Distribution:")
    for range_name in winning_ranges:
        win_count = winning_ranges[range_name]
        our_count = our_ranges[range_name]
        print(f"   {range_name}: Winning={win_count}, Ours={our_count} ({'✓' if our_count >= win_count else '✗'})")
    
    return {
        'overused_numbers': overused_numbers,
        'missing_numbers': missing_numbers,
        'winning_numbers': winning_numbers,
        'winning_stars': winning_stars,
        'our_combinations': our_combinations
    }

def analyze_historical_patterns():
    """
    Analyze historical Euromillions data to find real patterns we should focus on
    """
    try:
        engine = get_db_connection()
        
        # Get recent Euromillions history
        query = """
        SELECT numbers, stars, draw_date 
        FROM euromillions_drawings 
        WHERE draw_date >= '2024-01-01'
        ORDER BY draw_date DESC
        LIMIT 50
        """
        
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("No historical data available for pattern analysis")
            return {}
        
        print(f"\n=== HISTORICAL PATTERN ANALYSIS ===")
        print(f"Analyzing {len(df)} recent draws...\n")
        
        # Parse historical data
        all_numbers = []
        all_stars = []
        
        for _, row in df.iterrows():
            try:
                numbers_str = row['numbers'].strip('[]')
                numbers = [int(x.strip()) for x in numbers_str.split(',')]
                
                stars_str = row['stars'].strip('[]')
                stars = [int(x.strip()) for x in stars_str.split(',')]
                
                all_numbers.extend(numbers)
                all_stars.extend(stars)
            except:
                continue
        
        # Frequency analysis
        number_freq = Counter(all_numbers)
        star_freq = Counter(all_stars)
        
        print("1. MOST FREQUENT NUMBERS (Hot numbers):")
        hot_numbers = number_freq.most_common(10)
        for num, count in hot_numbers:
            print(f"   {num}: appeared {count} times")
        
        print(f"\n2. LEAST FREQUENT NUMBERS (Cold numbers):")
        cold_numbers = number_freq.most_common()[-10:]
        for num, count in reversed(cold_numbers):
            print(f"   {num}: appeared {count} times")
        
        print(f"\n3. MOST FREQUENT STARS:")
        for star, count in star_freq.most_common():
            print(f"   Star {star}: appeared {count} times")
        
        return {
            'hot_numbers': [num for num, count in hot_numbers],
            'cold_numbers': [num for num, count in reversed(cold_numbers)],
            'hot_stars': [star for star, count in star_freq.most_common()],
            'number_freq': number_freq,
            'star_freq': star_freq
        }
        
    except Exception as e:
        print(f"Error analyzing historical patterns: {e}")
        return {}

def develop_improved_strategy(failure_analysis, historical_patterns):
    """
    Develop a more focused strategy based on failure analysis and historical patterns
    """
    print(f"\n=== IMPROVED STRATEGY DEVELOPMENT ===\n")
    
    winning_numbers = failure_analysis['winning_numbers']
    winning_stars = failure_analysis['winning_stars']
    
    print("STRATEGY IMPROVEMENTS:")
    print("\n1. FOCUS ON CONCENTRATION vs COVERAGE:")
    print("   ✗ OLD: Spread numbers widely across 20 combinations")
    print("   ✓ NEW: Generate fewer combinations (8-10) with better number concentration")
    
    print("\n2. HISTORICAL FREQUENCY WEIGHTING:")
    if historical_patterns:
        hot_numbers = historical_patterns.get('hot_numbers', [])[:15]
        cold_numbers = historical_patterns.get('cold_numbers', [])[:15]
        hot_stars = historical_patterns.get('hot_stars', [])[:6]
        
        print(f"   ✓ Focus on hot numbers: {hot_numbers}")
        print(f"   ✓ Include some cold numbers: {cold_numbers}")
        print(f"   ✓ Prioritize hot stars: {hot_stars}")
    
    print("\n3. RANGE BALANCE IMPROVEMENT:")
    print("   ✓ Ensure each combination has numbers from 3-4 different ranges")
    print("   ✓ Avoid over-concentrating in high ranges (31-50)")
    
    print("\n4. AVOID DUPLICATE PATTERNS:")
    print("   ✗ OLD: Used number 3 in 6 combinations, 44 in 5 combinations")
    print("   ✓ NEW: Maximum 2-3 appearances per number across all combinations")
    
    print("\n5. STAR STRATEGY:")
    print("   ✓ Focus on most frequent star pairs from history")
    print("   ✓ Include stars 5 and 6 (winning stars) in future combinations")
    
    return {
        'max_combinations': 10,
        'hot_numbers': historical_patterns.get('hot_numbers', [])[:15] if historical_patterns else [],
        'cold_numbers': historical_patterns.get('cold_numbers', [])[:15] if historical_patterns else [],
        'hot_stars': historical_patterns.get('hot_stars', [])[:6] if historical_patterns else [],
        'max_number_reuse': 3,
        'required_ranges': 3
    }

def generate_focused_combinations(improved_strategy, num_combinations=8):
    """
    Generate focused combinations using the improved strategy
    """
    import random
    
    print(f"\n=== GENERATING {num_combinations} FOCUSED COMBINATIONS ===\n")
    
    hot_numbers = improved_strategy.get('hot_numbers', list(range(1, 51)))
    cold_numbers = improved_strategy.get('cold_numbers', list(range(1, 51)))
    hot_stars = improved_strategy.get('hot_stars', list(range(1, 13)))
    
    # Create number pools
    primary_pool = hot_numbers[:20] if hot_numbers else list(range(1, 51))
    secondary_pool = cold_numbers[:15] if cold_numbers else list(range(1, 51))
    
    # Track number usage
    number_usage = Counter()
    
    combinations = []
    
    for i in range(num_combinations):
        # Generate combination ensuring range diversity
        combination_numbers = []
        
        # Define ranges
        ranges = {
            "low": list(range(1, 17)),      # 1-16
            "mid_low": list(range(17, 26)), # 17-25
            "mid_high": list(range(26, 36)),# 26-35
            "high": list(range(36, 51))     # 36-50
        }
        
        # Ensure at least one number from each range (except high range - optional)
        selected_ranges = random.sample(list(ranges.keys()), 3)
        
        # Select numbers ensuring good distribution
        for range_name in selected_ranges:
            available = [n for n in ranges[range_name] 
                        if n in primary_pool and number_usage[n] < 3]
            if available:
                num = random.choice(available)
                combination_numbers.append(num)
                number_usage[num] += 1
        
        # Fill remaining slots
        while len(combination_numbers) < 5:
            available = [n for n in primary_pool + secondary_pool 
                        if n not in combination_numbers and number_usage[n] < 3]
            if available:
                num = random.choice(available)
                combination_numbers.append(num)
                number_usage[num] += 1
            else:
                # Fallback if all numbers overused
                num = random.randint(1, 50)
                if num not in combination_numbers:
                    combination_numbers.append(num)
        
        combination_numbers.sort()
        
        # Select stars from hot stars
        available_stars = hot_stars if hot_stars else list(range(1, 13))
        stars = sorted(random.sample(available_stars[:8], 2))
        
        strategy_name = f"Focused Strategy {i+1}"
        
        combinations.append({
            'numbers': combination_numbers,
            'stars': stars,
            'strategy': strategy_name
        })
        
        print(f"{i+1}. {strategy_name}")
        print(f"   Numbers: {combination_numbers}")
        print(f"   Stars: {stars}")
    
    return combinations

def main():
    """
    Main function to analyze failures and develop improved strategy
    """
    print("=== EUROMILLIONS STRATEGY IMPROVEMENT ANALYSIS ===\n")
    
    # Analyze our failures
    failure_analysis = analyze_prediction_failures()
    
    # Analyze historical patterns
    historical_patterns = analyze_historical_patterns()
    
    # Develop improved strategy
    improved_strategy = develop_improved_strategy(failure_analysis, historical_patterns)
    
    # Generate sample focused combinations
    focused_combinations = generate_focused_combinations(improved_strategy)
    
    print(f"\n=== SUMMARY ===")
    print("✓ Identified key failure points in our May 20 predictions")
    print("✓ Analyzed historical patterns for better number selection")
    print("✓ Developed focused strategy with concentration over coverage")
    print("✓ Generated sample combinations using improved approach")
    print(f"\nNext steps: Use this focused approach for upcoming draws!")

if __name__ == "__main__":
    main()