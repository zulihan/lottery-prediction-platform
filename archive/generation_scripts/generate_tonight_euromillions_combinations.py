"""
Generate 10 optimized Euromillions combinations for tonight's draw
Based on July 22 analysis: balanced distribution, hot stars 9 & 10, emerging low numbers
"""

import psycopg2
import os
from collections import Counter
import random
from datetime import datetime

def get_comprehensive_analysis():
    """Get comprehensive data for tonight's strategy"""
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get recent draws including July 22
    cursor.execute("""
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC
    LIMIT 15
    """)
    recent_draws = cursor.fetchall()
    
    # Get training data
    cursor.execute("""
    SELECT n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC
    LIMIT 2000
    """)
    training_data = cursor.fetchall()
    conn.close()
    
    # Analyze recent patterns
    recent_numbers = []
    recent_stars = []
    
    print("TONIGHT'S STRATEGIC DATA ANALYSIS")
    print("=" * 33)
    print("\nRECENT WINNING PATTERNS:")
    
    for i, (date, n1, n2, n3, n4, n5, s1, s2) in enumerate(recent_draws[:5]):
        numbers = sorted([n1, n2, n3, n4, n5])
        stars = [s1, s2]
        recent_numbers.extend(numbers)
        recent_stars.extend(stars)
        print(f"{date}: {numbers} / {stars}")
    
    # Frequency analysis
    all_numbers = []
    all_stars = []
    
    for row in training_data:
        n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    recent_number_freq = Counter(recent_numbers)
    recent_star_freq = Counter(recent_stars)
    
    # Categorize numbers
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    hot_numbers = [n for n, _ in sorted_numbers[:15]]
    frequent_numbers = [n for n, _ in sorted_numbers[:25]]
    medium_numbers = [n for n, _ in sorted_numbers[25:40]]
    
    # Identify emerging patterns
    low_range_hot = [n for n in recent_number_freq.keys() if n <= 17]
    mid_range_hot = [n for n in recent_number_freq.keys() if 18 <= n <= 34]
    high_range_hot = [n for n in recent_number_freq.keys() if n >= 35]
    
    print(f"\nKEY PATTERNS:")
    print(f"Hot numbers: {[n for n, _ in recent_number_freq.most_common(12)]}")
    print(f"Hot stars: {[s for s, _ in recent_star_freq.most_common(6)]}")
    print(f"Low range emerging: {low_range_hot[:5]}")
    print(f"Mid range strong: {mid_range_hot[:5]}")
    
    return {
        'hot_numbers': hot_numbers,
        'frequent_numbers': frequent_numbers,
        'medium_numbers': medium_numbers,
        'recent_hot': [n for n, _ in recent_number_freq.most_common(15)],
        'hot_stars': [s for s, _ in star_freq.most_common(6)],
        'recent_hot_stars': [s for s, _ in recent_star_freq.most_common(6)],
        'low_range_hot': low_range_hot,
        'mid_range_hot': mid_range_hot,
        'high_range_hot': high_range_hot
    }

def generate_8_main_combinations(data):
    """Generate 8 main combinations with tonight's strategic focus"""
    
    combinations = []
    
    # Strategy 1: Low Number Resurgence
    low_pool = [n for n in data['frequent_numbers'] if n <= 17]
    numbers1 = random.sample(low_pool[:10], 3)
    # Add mid-range balance
    mid_pool = [n for n in data['frequent_numbers'] if 18 <= n <= 34]
    numbers1.extend(random.sample(mid_pool, 2))
    
    combinations.append({
        'numbers': sorted(numbers1),
        'strategy': 'Low Number Resurgence',
        'focus': 'Capitalizing on emerging low number trend'
    })
    
    # Strategy 2: Star 10 Power Play
    # Build around numbers that often appear with star 10
    numbers2 = []
    # Include 8 and 15 (from July 22)
    if 8 in data['frequent_numbers']:
        numbers2.append(8)
    if 15 in data['frequent_numbers']:
        numbers2.append(15)
    # Add hot numbers
    remaining = [n for n in data['hot_numbers'] if n not in numbers2]
    numbers2.extend(random.sample(remaining, 5 - len(numbers2)))
    
    combinations.append({
        'numbers': sorted(numbers2),
        'strategy': 'Star 10 Power Play',
        'focus': 'Numbers aligned with hot star 10'
    })
    
    # Strategy 3: Balanced Distribution Master
    numbers3 = []
    # Perfect balance: 2 low, 2 mid, 1 high
    low_nums = [n for n in data['recent_hot'] if n <= 17]
    mid_nums = [n for n in data['recent_hot'] if 18 <= n <= 34]
    high_nums = [n for n in data['recent_hot'] if n >= 35]
    
    if len(low_nums) >= 2:
        numbers3.extend(random.sample(low_nums, 2))
    if len(mid_nums) >= 2:
        numbers3.extend(random.sample(mid_nums, 2))
    if len(high_nums) >= 1:
        numbers3.extend(random.sample(high_nums, 1))
    
    # Fill any gaps
    while len(numbers3) < 5:
        numbers3.append(random.choice(data['frequent_numbers']))
    
    combinations.append({
        'numbers': sorted(numbers3[:5]),
        'strategy': 'Balanced Distribution Master',
        'focus': 'Perfect range coverage matching July 22 pattern'
    })
    
    # Strategy 4: Mid-Range Dominance
    # Focus on 18-34 range (dominated July 22)
    mid_focus = [n for n in data['mid_range_hot'] if 18 <= n <= 34]
    numbers4 = random.sample(mid_focus[:8], min(4, len(mid_focus)))
    # Add one outside for balance
    other = [n for n in data['frequent_numbers'] if n not in mid_focus]
    numbers4.extend(random.sample(other, 5 - len(numbers4)))
    
    combinations.append({
        'numbers': sorted(numbers4[:5]),
        'strategy': 'Mid-Range Dominance',
        'focus': 'Continuing July 22 mid-range strength'
    })
    
    # Strategy 5: Hot Number Concentration
    # Pure hot numbers
    numbers5 = random.sample(data['recent_hot'][:12], 5)
    
    combinations.append({
        'numbers': sorted(numbers5),
        'strategy': 'Hot Number Concentration',
        'focus': 'Maximum heat concentration'
    })
    
    # Strategy 6: Emerging Pattern Explorer
    # Mix of 8, 15, 26, 33 (July 22) with other patterns
    july_22_nums = [8, 15, 26, 33, 41]
    numbers6 = random.sample(july_22_nums, 2)
    # Add numbers that haven't appeared recently
    cold_pool = [n for n in data['medium_numbers'] if n not in data['recent_hot']]
    numbers6.extend(random.sample(cold_pool, 3))
    
    combinations.append({
        'numbers': sorted(numbers6),
        'strategy': 'Emerging Pattern Explorer',
        'focus': 'July 22 echoes with cold number balance'
    })
    
    # Strategy 7: Statistical Sweet Spot
    # Numbers with optimal frequency (not too hot, not too cold)
    sweet_spot = data['frequent_numbers'][10:25]
    numbers7 = random.sample(sweet_spot, 5)
    
    combinations.append({
        'numbers': sorted(numbers7),
        'strategy': 'Statistical Sweet Spot',
        'focus': 'Optimal frequency range selection'
    })
    
    # Strategy 8: Coverage Maximizer
    # Ensure we hit key ranges and patterns
    numbers8 = []
    # Must include at least one from each key group
    if data['low_range_hot']:
        numbers8.append(random.choice(data['low_range_hot'][:3]))
    if data['mid_range_hot']:
        numbers8.append(random.choice(data['mid_range_hot'][:3]))
    if data['high_range_hot']:
        numbers8.append(random.choice(data['high_range_hot'][:3]))
    
    # Fill remaining
    fill_pool = [n for n in data['hot_numbers'] if n not in numbers8]
    numbers8.extend(random.sample(fill_pool, 5 - len(numbers8)))
    
    combinations.append({
        'numbers': sorted(numbers8[:5]),
        'strategy': 'Coverage Maximizer',
        'focus': 'Maximum range and pattern coverage'
    })
    
    return combinations

def generate_star_strategies(data, combination_id):
    """Generate star strategies with focus on 9 and 10"""
    
    # MUST include stars 9 and 10 prominently
    strategies = [
        'star_10_focus',        # Heavy on star 10
        'star_9_10_combo',      # Both 9 and 10
        'star_10_alternate',    # 10 with different partner
        'star_9_power',         # 9 with hot partner
        'hot_star_combo',       # Top 2 hot stars
        'star_10_balance',      # 10 with medium star
        'emerging_pattern',     # Based on recent pattern
        'coverage_stars'        # Different coverage
    ]
    
    strategy = strategies[combination_id - 1]
    
    hot_stars = data['hot_stars']
    recent_hot_stars = data['recent_hot_stars']
    
    if strategy == 'star_10_focus':
        stars = [10, random.choice([s for s in hot_stars if s != 10][:3])]
    
    elif strategy == 'star_9_10_combo':
        stars = [9, 10]
    
    elif strategy == 'star_10_alternate':
        partner_pool = [s for s in hot_stars if s not in [9, 10]]
        stars = [10, random.choice(partner_pool[:4])]
    
    elif strategy == 'star_9_power':
        partner_pool = [s for s in recent_hot_stars if s != 9]
        stars = [9, random.choice(partner_pool[:3])]
    
    elif strategy == 'hot_star_combo':
        stars = recent_hot_stars[:2]
    
    elif strategy == 'star_10_balance':
        medium_stars = [s for s in range(1, 13) if s not in recent_hot_stars[:3]]
        stars = [10, random.choice(medium_stars)]
    
    elif strategy == 'emerging_pattern':
        # Use the pattern from recent draws
        if 9 in recent_hot_stars and 10 in recent_hot_stars:
            stars = [9, 10]
        else:
            stars = random.sample(recent_hot_stars[:4], 2)
    
    else:  # coverage_stars
        # Different combination for coverage
        covered_stars = [9, 10]
        other_stars = [s for s in hot_stars if s not in covered_stars]
        stars = random.sample(other_stars[:6], 2)
    
    return sorted(stars)

def generate_2_fusion_combinations(main_combinations, data):
    """Generate 2 powerful fusion combinations"""
    
    print("\nGENERATING FUSION COMBINATIONS")
    print("-" * 30)
    
    # Count frequency across main combinations
    all_numbers = []
    all_stars = []
    
    for combo in main_combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Fusion 1: Persistent Winners Focus
    # Numbers that keep appearing + must-have stars
    fusion1_numbers = []
    
    # Include 8, 15 from July 22
    must_include = [8, 15]
    for num in must_include:
        if num in data['frequent_numbers']:
            fusion1_numbers.append(num)
    
    # Add most common from our combinations
    top_recurring = [n for n, _ in number_freq.most_common(8) if n not in fusion1_numbers]
    fusion1_numbers.extend(top_recurring[:5-len(fusion1_numbers)])
    
    fusion1 = {
        'id': 'F1',
        'numbers': sorted(fusion1_numbers[:5]),
        'stars': [9, 10],  # Both hot stars
        'strategy': 'Persistent Winners Focus',
        'focus': 'July 22 echoes with dual hot stars'
    }
    
    # Fusion 2: Mathematical Optimization
    # Perfect distribution with star optimization
    fusion2_numbers = []
    
    # Get numbers that appear multiple times
    multi_appearance = [n for n, count in number_freq.items() if count >= 2]
    
    # Build balanced set
    low_multi = [n for n in multi_appearance if n <= 17]
    mid_multi = [n for n in multi_appearance if 18 <= n <= 34]
    high_multi = [n for n in multi_appearance if n >= 35]
    
    if low_multi:
        fusion2_numbers.append(random.choice(low_multi))
    if mid_multi:
        fusion2_numbers.extend(random.sample(mid_multi, min(2, len(mid_multi))))
    if high_multi:
        fusion2_numbers.append(random.choice(high_multi))
    
    # Fill remaining
    remaining_pool = [n for n in data['hot_numbers'] if n not in fusion2_numbers]
    fusion2_numbers.extend(random.sample(remaining_pool, 5 - len(fusion2_numbers)))
    
    # For stars, use most common combo
    top_stars = [s for s, _ in star_freq.most_common(2)]
    
    fusion2 = {
        'id': 'F2',
        'numbers': sorted(fusion2_numbers[:5]),
        'stars': sorted(top_stars),
        'strategy': 'Mathematical Optimization',
        'focus': 'Statistically optimized coverage'
    }
    
    return [fusion1, fusion2]

def display_tonight_combinations(main_combinations, fusion_combinations):
    """Display tonight's complete set"""
    
    print("\nTONIGHT'S OPTIMIZED COMBINATIONS")
    print("=" * 33)
    
    print("\n8 MAIN STRATEGIC COMBINATIONS:")
    print("-" * 30)
    
    for i, combo in enumerate(main_combinations):
        stars = combo['stars']
        print(f"\n{i+1}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} + Stars: {stars}")
        print(f"   Focus: {combo['focus']}")
    
    print("\n2 POWER FUSION COMBINATIONS:")
    print("-" * 28)
    
    for fusion in fusion_combinations:
        print(f"\n{fusion['id']}. {fusion['strategy']}")
        print(f"   Numbers: {fusion['numbers']} + Stars: {fusion['stars']}")
        print(f"   Focus: {fusion['focus']}")
    
    # Coverage analysis
    all_numbers = set()
    all_stars = set()
    
    for combo in main_combinations + fusion_combinations:
        all_numbers.update(combo['numbers'])
        all_stars.update(combo['stars'])
    
    print("\nCOVERAGE OPTIMIZATION:")
    print("-" * 22)
    print(f"Total unique numbers: {len(all_numbers)}/50")
    print(f"Total unique stars: {len(all_stars)}/12")
    
    # Check key coverage
    key_numbers = [8, 15, 26, 33, 41]  # July 22
    key_coverage = all_numbers.intersection(set(key_numbers))
    print(f"\nJuly 22 pattern coverage: {sorted(key_coverage)} ({len(key_coverage)}/5)")
    
    # Star coverage check
    must_have_stars = [9, 10]
    star_coverage = all_stars.intersection(set(must_have_stars))
    print(f"Hot star coverage: {sorted(star_coverage)} ({len(star_coverage)}/2)")
    
    # Count how many combos have star 10
    star_10_count = sum(1 for combo in main_combinations + fusion_combinations if 10 in combo['stars'])
    star_9_count = sum(1 for combo in main_combinations + fusion_combinations if 9 in combo['stars'])
    
    print(f"\nStar 10 appears in: {star_10_count} combinations")
    print(f"Star 9 appears in: {star_9_count} combinations")

def main():
    """Generate tonight's optimized combinations"""
    
    # Get comprehensive analysis
    data = get_comprehensive_analysis()
    
    print("\nTONIGHT'S STRATEGIC FOCUS:")
    print("-" * 26)
    print("✓ Low numbers returning (include more 1-17)")
    print("✓ Star 10 is MUST-HAVE (very hot)")
    print("✓ Star 9 coverage essential (hot streak)")
    print("✓ Balanced distribution (not just high numbers)")
    print("✓ Mid-range strength from July 22")
    
    # Generate 8 main combinations
    main_combinations = generate_8_main_combinations(data)
    
    # Add star strategies
    for i, combo in enumerate(main_combinations):
        combo['stars'] = generate_star_strategies(data, i + 1)
    
    # Generate 2 fusion combinations
    fusion_combinations = generate_2_fusion_combinations(main_combinations, data)
    
    # Display complete set
    display_tonight_combinations(main_combinations, fusion_combinations)
    
    print("\n" + "=" * 50)
    print("STRATEGIC ADVANTAGES:")
    print("=" * 50)
    print("✓ Multiple combinations with star 10 (super hot)")
    print("✓ Strong star 9 coverage (emerging pattern)")
    print("✓ Low number inclusion (8, 1, etc.)")
    print("✓ Balanced range distribution")
    print("✓ July 22 pattern recognition")
    print("✓ Mathematical optimization in fusions")
    print("\nGOOD LUCK TONIGHT! 🎯")

if __name__ == "__main__":
    main()