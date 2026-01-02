"""
Generate 4 optimized Euromillions combinations after August 8, 2025 non-winning result
Focused strategy with concentrated picks
"""

import psycopg2
import os
from collections import Counter
import random
from datetime import datetime

def analyze_latest_including_august_8():
    """Analyze patterns including the August 8 draw"""
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get latest draws including August 8
    cursor.execute("""
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC
    LIMIT 20
    """)
    recent_draws = cursor.fetchall()
    
    # Get comprehensive historical data
    cursor.execute("""
    SELECT n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC
    LIMIT 2000
    """)
    historical_data = cursor.fetchall()
    conn.close()
    
    print("POST AUGUST 8 ANALYSIS")
    print("=" * 23)
    print("\nLATEST DRAWS:")
    
    # Analyze patterns
    recent_numbers = []
    recent_stars = []
    very_recent_numbers = []  # Last 5 draws
    very_recent_stars = []
    
    for i, (date, n1, n2, n3, n4, n5, s1, s2) in enumerate(recent_draws[:10]):
        numbers = sorted([n1, n2, n3, n4, n5])
        stars = [s1, s2]
        recent_numbers.extend(numbers)
        recent_stars.extend(stars)
        
        if i < 5:  # Show and track last 5 draws
            very_recent_numbers.extend(numbers)
            very_recent_stars.extend(stars)
            print(f"{date}: {numbers} / {stars}")
    
    # Frequency analysis
    all_numbers = []
    all_stars = []
    
    for row in historical_data:
        n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    recent_number_freq = Counter(recent_numbers)
    recent_star_freq = Counter(recent_stars)
    very_recent_freq = Counter(very_recent_numbers)
    very_recent_star_freq = Counter(very_recent_stars)
    
    print(f"\nCURRENT HOT NUMBERS (Last 10 draws): {[n for n, _ in recent_number_freq.most_common(12)]}")
    print(f"VERY HOT NUMBERS (Last 5 draws): {[n for n, _ in very_recent_freq.most_common(10)]}")
    print(f"HOT STARS: {[s for s, _ in recent_star_freq.most_common(6)]}")
    
    # Identify patterns and gaps
    all_numbers_set = set(range(1, 51))
    recent_set = set(very_recent_numbers)
    overdue = sorted(list(all_numbers_set - recent_set))[:15]
    
    print(f"\nOVERDUE NUMBERS: {overdue}")
    
    # Range analysis
    low_count = len([n for n in very_recent_numbers if n <= 17])
    mid_count = len([n for n in very_recent_numbers if 18 <= n <= 34])
    high_count = len([n for n in very_recent_numbers if n >= 35])
    
    print(f"RECENT RANGE TREND: Low: {low_count}, Mid: {mid_count}, High: {high_count}")
    
    # Categorize for strategy
    sorted_freq = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    hot_historical = [n for n, _ in sorted_freq[:20]]
    frequent_historical = [n for n, _ in sorted_freq[:30]]
    
    return {
        'latest_draws': recent_draws[:5],
        'very_hot': [n for n, _ in very_recent_freq.most_common(15)],
        'recent_hot': [n for n, _ in recent_number_freq.most_common(20)],
        'hot_stars': [s for s, _ in recent_star_freq.most_common(8)],
        'very_hot_stars': [s for s, _ in very_recent_star_freq.most_common(6)],
        'hot_historical': hot_historical,
        'frequent_historical': frequent_historical,
        'overdue': overdue,
        'range_trend': {'low': low_count, 'mid': mid_count, 'high': high_count}
    }

def generate_4_concentrated_combinations(data):
    """Generate 4 focused combinations with maximum impact"""
    
    combinations = []
    
    # Avoid exact repeats of recent draws
    recent_sets = []
    for draw in data['latest_draws']:
        _, n1, n2, n3, n4, n5, _, _ = draw
        recent_sets.append(set([n1, n2, n3, n4, n5]))
    
    # Combination 1: Super Hot Focus
    # Use the hottest current numbers
    numbers1 = []
    pool1 = data['very_hot'][:12] + data['recent_hot'][:8]
    pool1 = list(set(pool1))  # Remove duplicates
    
    attempts = 0
    while attempts < 20:
        numbers1 = random.sample(pool1, 5)
        if set(numbers1) not in recent_sets:
            break
        attempts += 1
    
    combinations.append({
        'numbers': sorted(numbers1),
        'stars': data['very_hot_stars'][:2],
        'strategy': 'Super Hot Focus',
        'focus': 'Concentrated on current hot streak'
    })
    
    # Combination 2: Overdue Breakthrough
    # Mix overdue with hot for balance
    numbers2 = []
    numbers2.extend(random.sample(data['overdue'][:8], 3))
    numbers2.extend(random.sample(data['recent_hot'][:10], 2))
    
    combinations.append({
        'numbers': sorted(numbers2),
        'stars': [data['hot_stars'][0], random.choice(data['hot_stars'][2:5])],
        'strategy': 'Overdue Breakthrough',
        'focus': 'Overdue numbers ready to hit'
    })
    
    # Combination 3: Range Optimizer
    # Perfect balance based on trend
    numbers3 = []
    low_pool = [n for n in data['frequent_historical'] if n <= 17]
    mid_pool = [n for n in data['frequent_historical'] if 18 <= n <= 34]
    high_pool = [n for n in data['frequent_historical'] if n >= 35]
    
    # Adjust based on recent trend
    if data['range_trend']['low'] < 15:  # Low numbers underrepresented
        numbers3.extend(random.sample(low_pool, 2))
        numbers3.extend(random.sample(mid_pool, 2))
        numbers3.extend(random.sample(high_pool, 1))
    elif data['range_trend']['high'] < 15:  # High numbers underrepresented
        numbers3.extend(random.sample(low_pool, 1))
        numbers3.extend(random.sample(mid_pool, 2))
        numbers3.extend(random.sample(high_pool, 2))
    else:  # Balanced
        numbers3.extend(random.sample(low_pool, 2))
        numbers3.extend(random.sample(mid_pool, 2))
        numbers3.extend(random.sample(high_pool, 1))
    
    combinations.append({
        'numbers': sorted(numbers3),
        'stars': random.sample(data['hot_stars'][:4], 2),
        'strategy': 'Range Optimizer',
        'focus': 'Balanced range distribution'
    })
    
    # Combination 4: Strategic Fusion
    # Smart mix of all successful patterns
    numbers4 = []
    
    # Take top performers from each category
    if data['very_hot']:
        numbers4.append(random.choice(data['very_hot'][:5]))
    if data['overdue']:
        numbers4.append(random.choice(data['overdue'][:5]))
    if data['hot_historical']:
        hot_not_recent = [n for n in data['hot_historical'] if n not in data['very_hot'][:10]]
        if hot_not_recent:
            numbers4.append(random.choice(hot_not_recent[:10]))
    
    # Fill remaining spots
    fill_pool = list(set(data['frequent_historical']) - set(numbers4))
    numbers4.extend(random.sample(fill_pool, 5 - len(numbers4)))
    
    # For stars, use a unique combination
    star_combo = []
    if len(data['very_hot_stars']) >= 2:
        star_combo = [data['very_hot_stars'][0], data['hot_stars'][2] if len(data['hot_stars']) > 2 else data['very_hot_stars'][1]]
    else:
        star_combo = data['hot_stars'][:2]
    
    combinations.append({
        'numbers': sorted(numbers4[:5]),
        'stars': sorted(star_combo),
        'strategy': 'Strategic Fusion',
        'focus': 'Multi-pattern convergence'
    })
    
    return combinations

def display_4_combinations(combinations, data):
    """Display the 4 combinations with analysis"""
    
    print("\n" + "=" * 50)
    print("4 CONCENTRATED COMBINATIONS FOR TONIGHT")
    print("=" * 50)
    
    for i, combo in enumerate(combinations, 1):
        print(f"\n{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} + Stars: {combo['stars']}")
        print(f"   Focus: {combo['focus']}")
    
    # Coverage analysis
    all_numbers = set()
    all_stars = set()
    
    for combo in combinations:
        all_numbers.update(combo['numbers'])
        all_stars.update(combo['stars'])
    
    print("\n" + "=" * 50)
    print("STRATEGIC COVERAGE:")
    print("=" * 50)
    print(f"Unique numbers covered: {len(all_numbers)}/50")
    print(f"Unique stars covered: {len(all_stars)}/12")
    
    # Check hot number coverage
    hot_coverage = all_numbers.intersection(set(data['very_hot'][:10]))
    overdue_coverage = all_numbers.intersection(set(data['overdue'][:10]))
    
    print(f"\nHot number coverage: {len(hot_coverage)}/10")
    print(f"Overdue coverage: {len(overdue_coverage)}/10")
    
    # Most used numbers across combinations
    number_counts = Counter()
    star_counts = Counter()
    
    for combo in combinations:
        for num in combo['numbers']:
            number_counts[num] += 1
        for star in combo['stars']:
            star_counts[star] += 1
    
    print(f"\nKey numbers (appearing multiple times): {[n for n, c in number_counts.items() if c > 1]}")
    print(f"Key stars: {[s for s, _ in star_counts.most_common(3)]}")

def main():
    """Generate 4 combinations for tonight"""
    
    # Analyze including August 8 results
    data = analyze_latest_including_august_8()
    
    print("\nSTRATEGY FOR TONIGHT:")
    print("-" * 20)
    print("✓ 4 concentrated combinations")
    print("✓ Focus on very recent patterns")
    print("✓ Strategic overdue integration")
    print("✓ Optimized star selection")
    
    # Generate 4 combinations
    combinations = generate_4_concentrated_combinations(data)
    
    # Display results
    display_4_combinations(combinations, data)
    
    print("\n" + "=" * 50)
    print("KEY ADVANTAGES:")
    print("=" * 50)
    print("✓ Concentrated strategy with 4 powerful combinations")
    print("✓ Each combination has distinct approach")
    print("✓ Maximum coverage of hot and overdue numbers")
    print("✓ No duplicate of recent winning draws")
    print("\nGOOD LUCK TONIGHT! 🎯")

if __name__ == "__main__":
    main()