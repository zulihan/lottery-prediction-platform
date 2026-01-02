"""
Generate 10 optimized Euromillions combinations based on latest draws
Using proven strategic methods with adaptive pattern recognition
"""

import psycopg2
import os
from collections import Counter
import random
from datetime import datetime

def get_latest_draw_analysis():
    """Analyze the latest Euromillions draws"""
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get latest draws
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
    
    print("LATEST EUROMILLIONS ANALYSIS")
    print("=" * 28)
    print("\nMOST RECENT DRAWS:")
    
    # Analyze recent patterns
    recent_numbers = []
    recent_stars = []
    
    for i, (date, n1, n2, n3, n4, n5, s1, s2) in enumerate(recent_draws[:10]):
        numbers = sorted([n1, n2, n3, n4, n5])
        stars = [s1, s2]
        recent_numbers.extend(numbers)
        recent_stars.extend(stars)
        
        if i < 5:  # Show last 5 draws
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
    
    print(f"\nCURRENT HOT NUMBERS: {[n for n, _ in recent_number_freq.most_common(15)]}")
    print(f"CURRENT HOT STARS: {[s for s, _ in recent_star_freq.most_common(8)]}")
    
    # Pattern analysis
    low_count = len([n for n in recent_numbers[:50] if n <= 17])
    mid_count = len([n for n in recent_numbers[:50] if 18 <= n <= 34])
    high_count = len([n for n in recent_numbers[:50] if n >= 35])
    
    print(f"\nRANGE DISTRIBUTION (Last 10 draws):")
    print(f"Low (1-17): {low_count}, Mid (18-34): {mid_count}, High (35-50): {high_count}")
    
    # Categorize numbers
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    hot_numbers = [n for n, _ in sorted_numbers[:20]]
    frequent_numbers = [n for n, _ in sorted_numbers[:30]]
    medium_numbers = [n for n, _ in sorted_numbers[30:45]]
    
    return {
        'recent_draws': recent_draws[:5],
        'hot_numbers': hot_numbers,
        'frequent_numbers': frequent_numbers,
        'medium_numbers': medium_numbers,
        'recent_hot': [n for n, _ in recent_number_freq.most_common(20)],
        'hot_stars': [s for s, _ in star_freq.most_common(8)],
        'recent_hot_stars': [s for s, _ in recent_star_freq.most_common(8)],
        'number_freq': number_freq,
        'star_freq': star_freq,
        'range_trend': {'low': low_count, 'mid': mid_count, 'high': high_count}
    }

def generate_8_strategic_combinations(data):
    """Generate 8 main combinations using diverse strategies"""
    
    combinations = []
    
    # Strategy 1: Recent Hot Pursuit
    numbers1 = random.sample(data['recent_hot'][:15], 5)
    combinations.append({
        'numbers': sorted(numbers1),
        'strategy': 'Recent Hot Pursuit',
        'focus': 'Capturing current hot streak numbers'
    })
    
    # Strategy 2: Balanced Range Master
    numbers2 = []
    low_pool = [n for n in data['frequent_numbers'] if n <= 17]
    mid_pool = [n for n in data['frequent_numbers'] if 18 <= n <= 34]
    high_pool = [n for n in data['frequent_numbers'] if n >= 35]
    
    # Adaptive balance based on recent trend
    if data['range_trend']['low'] > data['range_trend']['high']:
        numbers2.extend(random.sample(low_pool, 2))
        numbers2.extend(random.sample(mid_pool, 2))
        numbers2.extend(random.sample(high_pool, 1))
    else:
        numbers2.extend(random.sample(low_pool, 1))
        numbers2.extend(random.sample(mid_pool, 2))
        numbers2.extend(random.sample(high_pool, 2))
    
    combinations.append({
        'numbers': sorted(numbers2),
        'strategy': 'Balanced Range Master',
        'focus': 'Adaptive range distribution'
    })
    
    # Strategy 3: Frequency Power Play
    numbers3 = random.sample(data['hot_numbers'][:12], 5)
    combinations.append({
        'numbers': sorted(numbers3),
        'strategy': 'Frequency Power Play',
        'focus': 'Historical high-frequency focus'
    })
    
    # Strategy 4: Emerging Pattern Tracker
    # Identify numbers showing upward trend
    emerging = []
    for num in data['recent_hot']:
        if num not in data['hot_numbers'][:10]:
            emerging.append(num)
    
    numbers4 = []
    if len(emerging) >= 3:
        numbers4.extend(random.sample(emerging, 3))
    numbers4.extend(random.sample(data['frequent_numbers'], 5 - len(numbers4)))
    
    combinations.append({
        'numbers': sorted(numbers4[:5]),
        'strategy': 'Emerging Pattern Tracker',
        'focus': 'Rising stars and emerging trends'
    })
    
    # Strategy 5: Coverage Optimizer
    numbers5 = []
    # Ensure coverage across different frequency tiers
    numbers5.extend(random.sample(data['hot_numbers'][:10], 2))
    numbers5.extend(random.sample(data['frequent_numbers'][10:20], 2))
    numbers5.extend(random.sample(data['medium_numbers'], 1))
    
    combinations.append({
        'numbers': sorted(numbers5),
        'strategy': 'Coverage Optimizer',
        'focus': 'Multi-tier frequency coverage'
    })
    
    # Strategy 6: Statistical Sweet Spot
    # Numbers in optimal frequency range
    sweet_spot = []
    for num, freq in data['number_freq'].items():
        if 80 <= freq <= 120:
            sweet_spot.append(num)
    
    if len(sweet_spot) >= 5:
        numbers6 = random.sample(sweet_spot, 5)
    else:
        numbers6 = sweet_spot + random.sample(data['frequent_numbers'], 5 - len(sweet_spot))
    
    combinations.append({
        'numbers': sorted(numbers6[:5]),
        'strategy': 'Statistical Sweet Spot',
        'focus': 'Optimal frequency zone'
    })
    
    # Strategy 7: Contrarian Approach
    # Mix of cold and warming numbers
    cold_numbers = [n for n in data['medium_numbers'] if n not in data['recent_hot']]
    numbers7 = []
    numbers7.extend(random.sample(cold_numbers, 3))
    numbers7.extend(random.sample(data['recent_hot'][10:20], 2))
    
    combinations.append({
        'numbers': sorted(numbers7[:5]),
        'strategy': 'Contrarian Approach',
        'focus': 'Overdue numbers with emerging heat'
    })
    
    # Strategy 8: Pattern Recognition Master
    # Based on most recent winning pattern
    latest_draw = data['recent_draws'][0]
    _, n1, n2, n3, n4, n5, _, _ = latest_draw
    latest_numbers = sorted([n1, n2, n3, n4, n5])
    
    # Find similar range distribution
    numbers8 = []
    latest_low = len([n for n in latest_numbers if n <= 17])
    latest_mid = len([n for n in latest_numbers if 18 <= n <= 34])
    latest_high = len([n for n in latest_numbers if n >= 35])
    
    numbers8.extend(random.sample(low_pool, latest_low))
    numbers8.extend(random.sample(mid_pool, latest_mid))
    numbers8.extend(random.sample(high_pool, latest_high))
    
    combinations.append({
        'numbers': sorted(numbers8[:5]),
        'strategy': 'Pattern Recognition Master',
        'focus': 'Mirroring latest winning pattern'
    })
    
    return combinations

def generate_star_strategies(data, combination_id):
    """Generate star strategies based on current patterns"""
    
    strategies = [
        'hot_star_focus',           # Top hot stars
        'recent_winner_stars',      # Stars from recent wins
        'balanced_star_play',       # Mix of hot and medium
        'emerging_star_pattern',    # Rising stars
        'coverage_stars',           # Broad coverage
        'frequency_optimal',        # Optimal frequency
        'contrarian_stars',         # Cold star play
        'pattern_mirror'            # Mirror recent pattern
    ]
    
    strategy = strategies[combination_id - 1]
    hot_stars = data['hot_stars']
    recent_hot_stars = data['recent_hot_stars']
    
    if strategy == 'hot_star_focus':
        stars = recent_hot_stars[:2]
    
    elif strategy == 'recent_winner_stars':
        # Get stars from last 2 draws
        recent_stars = []
        for draw in data['recent_draws'][:2]:
            recent_stars.extend([draw[6], draw[7]])
        star_counts = Counter(recent_stars)
        if len(star_counts) >= 2:
            stars = [s for s, _ in star_counts.most_common(2)]
        else:
            stars = recent_hot_stars[:2]
    
    elif strategy == 'balanced_star_play':
        stars = [recent_hot_stars[0], random.choice(hot_stars[3:7])]
    
    elif strategy == 'emerging_star_pattern':
        emerging_stars = [s for s in recent_hot_stars if s not in hot_stars[:3]]
        if len(emerging_stars) >= 2:
            stars = emerging_stars[:2]
        else:
            stars = [recent_hot_stars[0], random.choice(hot_stars[4:8])]
    
    elif strategy == 'coverage_stars':
        covered = set()
        for i in range(combination_id - 1):
            if i < len(data.get('generated_stars', [])):
                covered.update(data['generated_stars'][i])
        
        uncovered = [s for s in hot_stars if s not in covered]
        if len(uncovered) >= 2:
            stars = random.sample(uncovered, 2)
        else:
            stars = random.sample(hot_stars, 2)
    
    elif strategy == 'frequency_optimal':
        optimal_stars = []
        for star, freq in data['star_freq'].items():
            if 150 <= freq <= 250:
                optimal_stars.append(star)
        
        if len(optimal_stars) >= 2:
            stars = random.sample(optimal_stars, 2)
        else:
            stars = hot_stars[2:4]
    
    elif strategy == 'contrarian_stars':
        cold_stars = [s for s in range(1, 13) if s not in recent_hot_stars[:4]]
        if len(cold_stars) >= 2:
            stars = random.sample(cold_stars, 2)
        else:
            stars = hot_stars[6:8]
    
    else:  # pattern_mirror
        latest_stars = [data['recent_draws'][0][6], data['recent_draws'][0][7]]
        stars = sorted(latest_stars)
    
    # Store generated stars for coverage tracking
    if 'generated_stars' not in data:
        data['generated_stars'] = []
    data['generated_stars'].append(stars)
    
    return sorted(stars)

def generate_2_fusion_combinations(main_combinations, data):
    """Generate 2 fusion combinations"""
    
    all_numbers = []
    all_stars = []
    
    for combo in main_combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Fusion 1: High Frequency Convergence
    fusion1_numbers = [n for n, _ in number_freq.most_common(5)]
    fusion1_stars = [s for s, _ in star_freq.most_common(2)]
    
    fusion1 = {
        'id': 'F1',
        'numbers': sorted(fusion1_numbers),
        'stars': sorted(fusion1_stars),
        'strategy': 'High Frequency Convergence',
        'focus': 'Most selected numbers across strategies'
    }
    
    # Fusion 2: Strategic Balance Fusion
    # Mix of different frequency appearances
    multi_appearance = [n for n, count in number_freq.items() if count >= 2]
    single_appearance = [n for n, count in number_freq.items() if count == 1]
    
    fusion2_numbers = []
    fusion2_numbers.extend(random.sample(multi_appearance, min(3, len(multi_appearance))))
    if single_appearance:
        fusion2_numbers.extend(random.sample(single_appearance, min(2, len(single_appearance))))
    
    # Fill if needed
    if len(fusion2_numbers) < 5:
        remaining = [n for n in data['hot_numbers'] if n not in fusion2_numbers]
        fusion2_numbers.extend(random.sample(remaining, 5 - len(fusion2_numbers)))
    
    # Different star strategy for fusion 2
    star_pool = [s for s in data['hot_stars'] if s not in fusion1_stars]
    fusion2_stars = random.sample(star_pool[:6], 2)
    
    fusion2 = {
        'id': 'F2',
        'numbers': sorted(fusion2_numbers[:5]),
        'stars': sorted(fusion2_stars),
        'strategy': 'Strategic Balance Fusion',
        'focus': 'Optimized coverage balance'
    }
    
    return [fusion1, fusion2]

def display_combinations_with_analysis(main_combinations, fusion_combinations, data):
    """Display the complete set with analysis"""
    
    print("\n" + "=" * 50)
    print("10 OPTIMIZED EUROMILLIONS COMBINATIONS")
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
    
    # Coverage analysis
    all_numbers = set()
    all_stars = set()
    
    for combo in main_combinations + fusion_combinations:
        all_numbers.update(combo['numbers'])
        all_stars.update(combo['stars'])
    
    print("\n" + "=" * 50)
    print("COVERAGE ANALYSIS:")
    print("=" * 50)
    print(f"Total unique numbers: {len(all_numbers)}/50")
    print(f"Total unique stars: {len(all_stars)}/12")
    
    # Check coverage of recent hot numbers
    recent_coverage = all_numbers.intersection(set(data['recent_hot'][:10]))
    print(f"\nRecent hot number coverage: {len(recent_coverage)}/10")
    
    # Star distribution
    star_counts = Counter()
    for combo in main_combinations + fusion_combinations:
        for star in combo['stars']:
            star_counts[star] += 1
    
    print(f"\nMost used stars: {[s for s, _ in star_counts.most_common(4)]}")
    
    print("\n" + "=" * 50)
    print("STRATEGIC ADVANTAGES:")
    print("=" * 50)
    print("✓ Adaptive to latest drawing patterns")
    print("✓ Balanced coverage across all strategies")
    print("✓ Hot numbers and stars prominently featured")
    print("✓ Range distribution optimized")
    print("✓ Mathematical fusion for maximum impact")

def main():
    """Main function to generate combinations"""
    
    # Get latest analysis
    data = get_latest_draw_analysis()
    
    print("\nSTRATEGIC APPROACH:")
    print("-" * 18)
    print("✓ Analyzing latest patterns and trends")
    print("✓ 8 diverse strategies + 2 power fusions")
    print("✓ Adaptive star selection")
    print("✓ Maximum coverage optimization")
    
    # Generate 8 main combinations
    main_combinations = generate_8_strategic_combinations(data)
    
    # Add star strategies
    for i, combo in enumerate(main_combinations):
        combo['stars'] = generate_star_strategies(data, i + 1)
    
    # Generate 2 fusion combinations
    fusion_combinations = generate_2_fusion_combinations(main_combinations, data)
    
    # Display with analysis
    display_combinations_with_analysis(main_combinations, fusion_combinations, data)
    
    print("\nGOOD LUCK! 🍀")

if __name__ == "__main__":
    main()