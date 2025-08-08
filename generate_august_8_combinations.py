"""
Generate 10 optimized Euromillions combinations for Friday, August 8, 2025
Analyzing recent patterns and adjusting strategy after non-winning results
"""

import psycopg2
import os
from collections import Counter
import random
from datetime import datetime, timedelta

def analyze_recent_performance_and_patterns():
    """Analyze recent draws and identify new patterns"""
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get recent draws
    cursor.execute("""
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    WHERE date >= '2025-07-01'
    ORDER BY date DESC
    """)
    recent_draws = cursor.fetchall()
    
    # Get comprehensive historical data
    cursor.execute("""
    SELECT n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC
    LIMIT 2000
    """)
    all_draws = cursor.fetchall()
    conn.close()
    
    print("AUGUST 8, 2025 - EUROMILLIONS ANALYSIS")
    print("=" * 39)
    print("\nLATEST DRAWS (Since August):")
    
    # Analyze patterns
    august_numbers = []
    august_stars = []
    all_recent_numbers = []
    all_recent_stars = []
    
    for i, (date, n1, n2, n3, n4, n5, s1, s2) in enumerate(recent_draws):
        numbers = sorted([n1, n2, n3, n4, n5])
        stars = [s1, s2]
        
        if date.month == 8:  # August draws
            august_numbers.extend(numbers)
            august_stars.extend(stars)
            print(f"{date}: {numbers} / {stars}")
        
        if i < 15:  # Last 15 draws for pattern analysis
            all_recent_numbers.extend(numbers)
            all_recent_stars.extend(stars)
    
    # Frequency analysis
    all_numbers = []
    all_stars = []
    for row in all_draws:
        n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    # Create frequency counters
    august_freq = Counter(august_numbers) if august_numbers else Counter()
    recent_freq = Counter(all_recent_numbers)
    recent_star_freq = Counter(all_recent_stars)
    historical_freq = Counter(all_numbers)
    historical_star_freq = Counter(all_stars)
    
    print(f"\nAUGUST HOT NUMBERS: {[n for n, _ in august_freq.most_common(10)] if august_numbers else 'No August draws yet'}")
    print(f"RECENT HOT NUMBERS (15 draws): {[n for n, _ in recent_freq.most_common(15)]}")
    print(f"RECENT HOT STARS: {[s for s, _ in recent_star_freq.most_common(8)]}")
    
    # Pattern shifts analysis
    print("\nPATTERN SHIFTS DETECTED:")
    
    # Check range distribution shifts
    low_recent = len([n for n in all_recent_numbers[:75] if n <= 17])
    mid_recent = len([n for n in all_recent_numbers[:75] if 18 <= n <= 34])
    high_recent = len([n for n in all_recent_numbers[:75] if n >= 35])
    
    print(f"Range distribution (last 15 draws): Low: {low_recent}, Mid: {mid_recent}, High: {high_recent}")
    
    # Identify numbers that haven't appeared recently
    all_numbers_set = set(range(1, 51))
    recent_numbers_set = set(all_recent_numbers)
    overdue_numbers = all_numbers_set - recent_numbers_set
    
    print(f"Overdue numbers (not in last 15 draws): {sorted(list(overdue_numbers))[:10]}")
    
    # Categorize numbers
    sorted_historical = sorted(historical_freq.items(), key=lambda x: x[1], reverse=True)
    hot_historical = [n for n, _ in sorted_historical[:20]]
    frequent_historical = [n for n, _ in sorted_historical[:30]]
    medium_historical = [n for n, _ in sorted_historical[30:45]]
    
    return {
        'august_numbers': august_numbers,
        'august_stars': august_stars,
        'recent_hot': [n for n, _ in recent_freq.most_common(20)],
        'recent_hot_stars': [s for s, _ in recent_star_freq.most_common(8)],
        'hot_historical': hot_historical,
        'frequent_historical': frequent_historical,
        'medium_historical': medium_historical,
        'overdue_numbers': list(overdue_numbers),
        'historical_freq': historical_freq,
        'historical_star_freq': historical_star_freq,
        'range_trend': {'low': low_recent, 'mid': mid_recent, 'high': high_recent},
        'recent_draws': recent_draws[:10]
    }

def generate_8_adaptive_combinations(data):
    """Generate 8 main combinations with adaptive strategies"""
    
    combinations = []
    
    # Strategy 1: August Pattern Focus (if August data exists)
    if data['august_numbers']:
        august_hot = Counter(data['august_numbers']).most_common(10)
        numbers1 = [n for n, _ in august_hot[:5]]
        if len(numbers1) < 5:
            numbers1.extend(random.sample(data['recent_hot'], 5 - len(numbers1)))
    else:
        # Use recent hot as fallback
        numbers1 = random.sample(data['recent_hot'][:15], 5)
    
    combinations.append({
        'numbers': sorted(numbers1[:5]),
        'strategy': 'August Momentum',
        'focus': 'Capturing August-specific patterns'
    })
    
    # Strategy 2: Overdue Numbers Integration
    overdue_hot = [n for n in data['overdue_numbers'] if n in data['frequent_historical']]
    numbers2 = []
    if len(overdue_hot) >= 3:
        numbers2.extend(random.sample(overdue_hot, 3))
    numbers2.extend(random.sample(data['recent_hot'], 5 - len(numbers2)))
    
    combinations.append({
        'numbers': sorted(numbers2[:5]),
        'strategy': 'Overdue Integration',
        'focus': 'Combining overdue with hot numbers'
    })
    
    # Strategy 3: Range Rebalancing
    numbers3 = []
    # Adjust based on recent trend
    if data['range_trend']['high'] > data['range_trend']['low']:
        # High numbers dominating, increase low/mid
        low_pool = [n for n in data['frequent_historical'] if n <= 17]
        mid_pool = [n for n in data['frequent_historical'] if 18 <= n <= 34]
        numbers3.extend(random.sample(low_pool, 2))
        numbers3.extend(random.sample(mid_pool, 2))
        high_pool = [n for n in data['recent_hot'] if n >= 35]
        if high_pool:
            numbers3.extend(random.sample(high_pool, 1))
    else:
        # Balanced approach
        numbers3 = random.sample(data['frequent_historical'][:25], 5)
    
    combinations.append({
        'numbers': sorted(numbers3[:5]),
        'strategy': 'Range Rebalancing',
        'focus': 'Correcting range imbalances'
    })
    
    # Strategy 4: Historical Power Play
    numbers4 = random.sample(data['hot_historical'][:15], 5)
    
    combinations.append({
        'numbers': sorted(numbers4),
        'strategy': 'Historical Power Play',
        'focus': 'Pure historical frequency'
    })
    
    # Strategy 5: Pattern Breaker
    # Mix of different frequency tiers
    numbers5 = []
    numbers5.extend(random.sample(data['hot_historical'][:10], 2))
    numbers5.extend(random.sample(data['medium_historical'], 2))
    if data['overdue_numbers']:
        numbers5.append(random.choice(data['overdue_numbers'][:10]))
    else:
        numbers5.append(random.choice(data['frequent_historical']))
    
    combinations.append({
        'numbers': sorted(numbers5[:5]),
        'strategy': 'Pattern Breaker',
        'focus': 'Breaking recent patterns'
    })
    
    # Strategy 6: Consecutive Hunter
    numbers6 = []
    base_nums = random.sample(data['recent_hot'][:20], 3)
    numbers6.extend(base_nums)
    # Try to add consecutive pairs
    for num in base_nums:
        if num + 1 <= 50 and num + 1 not in numbers6 and len(numbers6) < 5:
            numbers6.append(num + 1)
        elif num - 1 >= 1 and num - 1 not in numbers6 and len(numbers6) < 5:
            numbers6.append(num - 1)
    
    # Fill remaining
    if len(numbers6) < 5:
        remaining = [n for n in data['frequent_historical'] if n not in numbers6]
        numbers6.extend(random.sample(remaining, 5 - len(numbers6)))
    
    combinations.append({
        'numbers': sorted(numbers6[:5]),
        'strategy': 'Consecutive Hunter',
        'focus': 'Strategic consecutive patterns'
    })
    
    # Strategy 7: Statistical Optimizer
    # Numbers in optimal frequency range
    optimal_numbers = []
    for num, freq in data['historical_freq'].items():
        if 85 <= freq <= 115:
            optimal_numbers.append(num)
    
    if len(optimal_numbers) >= 5:
        numbers7 = random.sample(optimal_numbers, 5)
    else:
        numbers7 = optimal_numbers + random.sample(data['frequent_historical'], 5 - len(optimal_numbers))
    
    combinations.append({
        'numbers': sorted(numbers7[:5]),
        'strategy': 'Statistical Optimizer',
        'focus': 'Optimal frequency zone'
    })
    
    # Strategy 8: Fresh Perspective
    # Completely different approach - use less common but warming numbers
    warming_numbers = []
    for num in data['medium_historical']:
        recent_count = data['recent_hot'].count(num) if num in data['recent_hot'] else 0
        if recent_count > 0:
            warming_numbers.append(num)
    
    if len(warming_numbers) >= 5:
        numbers8 = random.sample(warming_numbers, 5)
    else:
        numbers8 = warming_numbers + random.sample(data['frequent_historical'][15:30], 5 - len(warming_numbers))
    
    combinations.append({
        'numbers': sorted(numbers8[:5]),
        'strategy': 'Fresh Perspective',
        'focus': 'Warming medium-frequency numbers'
    })
    
    return combinations

def generate_adaptive_star_strategies(data, combination_id):
    """Generate star strategies with fresh approach"""
    
    strategies = [
        'august_stars',         # August-specific if available
        'hot_pursuit',          # Current hot stars
        'overdue_stars',        # Stars not seen recently
        'balanced_play',        # Mix of frequencies
        'pattern_mirror',       # Mirror recent pattern
        'frequency_optimal',    # Optimal frequency
        'contrarian',          # Against the trend
        'coverage_max'         # Maximum coverage
    ]
    
    strategy = strategies[combination_id - 1]
    hot_stars = data['recent_hot_stars']
    all_stars = list(range(1, 13))
    
    if strategy == 'august_stars':
        if data['august_stars']:
            august_star_freq = Counter(data['august_stars'])
            stars = [s for s, _ in august_star_freq.most_common(2)]
        else:
            stars = hot_stars[:2]
    
    elif strategy == 'hot_pursuit':
        stars = hot_stars[:2]
    
    elif strategy == 'overdue_stars':
        recent_stars_set = set(hot_stars[:6])
        overdue = [s for s in all_stars if s not in recent_stars_set]
        if len(overdue) >= 2:
            stars = random.sample(overdue, 2)
        else:
            stars = [overdue[0] if overdue else random.choice(all_stars), hot_stars[0]]
    
    elif strategy == 'balanced_play':
        stars = [hot_stars[0], random.choice(all_stars[5:10])]
    
    elif strategy == 'pattern_mirror':
        if data['recent_draws']:
            latest_stars = [data['recent_draws'][0][6], data['recent_draws'][0][7]]
            stars = sorted(latest_stars)
        else:
            stars = hot_stars[:2]
    
    elif strategy == 'frequency_optimal':
        optimal_stars = []
        for star, freq in data['historical_star_freq'].items():
            if 160 <= freq <= 240:
                optimal_stars.append(star)
        
        if len(optimal_stars) >= 2:
            stars = random.sample(optimal_stars, 2)
        else:
            stars = hot_stars[1:3]
    
    elif strategy == 'contrarian':
        cold_stars = [s for s in all_stars if s not in hot_stars[:4]]
        if len(cold_stars) >= 2:
            stars = random.sample(cold_stars, 2)
        else:
            stars = [cold_stars[0], hot_stars[3]]
    
    else:  # coverage_max
        # Try to use stars not used in previous combinations
        if combination_id > 1 and 'used_stars' in data:
            unused = [s for s in all_stars if s not in data['used_stars']]
            if len(unused) >= 2:
                stars = random.sample(unused, 2)
            else:
                stars = random.sample(hot_stars[2:6], 2)
        else:
            stars = random.sample(hot_stars[2:6], 2)
            data['used_stars'] = set()
        
        data['used_stars'].update(stars)
    
    return sorted(stars)

def generate_2_power_fusions(main_combinations, data):
    """Generate 2 fusion combinations with fresh approach"""
    
    all_numbers = []
    all_stars = []
    
    for combo in main_combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Fusion 1: Convergence Point
    # Numbers appearing most across strategies
    fusion1_numbers = []
    top_recurring = [n for n, count in number_freq.most_common() if count >= 2]
    
    if len(top_recurring) >= 5:
        fusion1_numbers = top_recurring[:5]
    else:
        fusion1_numbers = top_recurring + random.sample(data['recent_hot'], 5 - len(top_recurring))
    
    fusion1_stars = [s for s, _ in star_freq.most_common(2)]
    
    fusion1 = {
        'id': 'F1',
        'numbers': sorted(fusion1_numbers[:5]),
        'stars': sorted(fusion1_stars),
        'strategy': 'Strategic Convergence',
        'focus': 'Multi-strategy consensus picks'
    }
    
    # Fusion 2: Adaptive Balance
    # Smart mix based on current patterns
    fusion2_numbers = []
    
    # Include at least one overdue if available
    if data['overdue_numbers']:
        fusion2_numbers.append(random.choice(data['overdue_numbers'][:5]))
    
    # Add hot numbers
    fusion2_numbers.extend(random.sample(data['recent_hot'][:10], 2))
    
    # Add medium frequency
    fusion2_numbers.extend(random.sample(data['medium_historical'], 2))
    
    # Ensure we have 5 numbers
    if len(fusion2_numbers) < 5:
        remaining = [n for n in data['frequent_historical'] if n not in fusion2_numbers]
        fusion2_numbers.extend(random.sample(remaining, 5 - len(fusion2_numbers)))
    
    # Different star strategy
    all_star_options = list(set(range(1, 13)) - set(fusion1_stars))
    fusion2_stars = random.sample(all_star_options, 2)
    
    fusion2 = {
        'id': 'F2',
        'numbers': sorted(fusion2_numbers[:5]),
        'stars': sorted(fusion2_stars),
        'strategy': 'Adaptive Balance',
        'focus': 'Smart frequency distribution'
    }
    
    return [fusion1, fusion2]

def display_august_8_combinations(main_combinations, fusion_combinations, data):
    """Display the complete set for August 8"""
    
    print("\n" + "=" * 50)
    print("10 COMBINATIONS FOR FRIDAY, AUGUST 8, 2025")
    print("=" * 50)
    
    print("\n8 MAIN STRATEGIC COMBINATIONS:")
    print("-" * 30)
    
    for i, combo in enumerate(main_combinations):
        print(f"\n{i+1}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} + Stars: {combo['stars']}")
        print(f"   Focus: {combo['focus']}")
    
    print("\n2 POWER FUSION COMBINATIONS:")
    print("-" * 28)
    
    for fusion in fusion_combinations:
        print(f"\n{fusion['id']}. {fusion['strategy']}")
        print(f"   Numbers: {fusion['numbers']} + Stars: {fusion['stars']}")
        print(f"   Focus: {fusion['focus']}")
    
    # Analysis
    all_numbers = set()
    all_stars = set()
    
    for combo in main_combinations + fusion_combinations:
        all_numbers.update(combo['numbers'])
        all_stars.update(combo['stars'])
    
    print("\n" + "=" * 50)
    print("STRATEGIC COVERAGE:")
    print("=" * 50)
    print(f"Total unique numbers: {len(all_numbers)}/50")
    print(f"Total unique stars: {len(all_stars)}/12")
    
    # Key number coverage
    number_counts = Counter()
    for combo in main_combinations + fusion_combinations:
        for num in combo['numbers']:
            number_counts[num] += 1
    
    print(f"\nMost used numbers: {[n for n, _ in number_counts.most_common(5)]}")
    
    # Overdue coverage
    if data['overdue_numbers']:
        overdue_covered = all_numbers.intersection(set(data['overdue_numbers']))
        print(f"Overdue numbers covered: {len(overdue_covered)}/{len(data['overdue_numbers'][:10])}")
    
    print("\n" + "=" * 50)
    print("FRESH APPROACH ADVANTAGES:")
    print("=" * 50)
    print("✓ Adapted strategy after non-winning results")
    print("✓ Overdue numbers integrated strategically")
    print("✓ Range rebalancing applied")
    print("✓ Fresh star combinations")
    print("✓ Multi-strategy convergence in fusions")

def main():
    """Generate combinations for August 8, 2025"""
    
    # Analyze current patterns
    data = analyze_recent_performance_and_patterns()
    
    print("\nSTRATEGIC ADJUSTMENTS FOR AUGUST 8:")
    print("-" * 35)
    print("✓ Fresh approach after non-winning results")
    print("✓ Integrating overdue numbers")
    print("✓ Adaptive range balancing")
    print("✓ New star selection strategies")
    
    # Generate 8 main combinations
    main_combinations = generate_8_adaptive_combinations(data)
    
    # Add star strategies
    for i, combo in enumerate(main_combinations):
        combo['stars'] = generate_adaptive_star_strategies(data, i + 1)
    
    # Generate 2 fusion combinations
    fusion_combinations = generate_2_power_fusions(main_combinations, data)
    
    # Display complete set
    display_august_8_combinations(main_combinations, fusion_combinations, data)
    
    print("\nGOOD LUCK FOR TONIGHT'S DRAW! 🍀")

if __name__ == "__main__":
    main()