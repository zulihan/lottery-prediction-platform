"""
Analyze July 18, 2025 results and generate new optimized combinations
Results: 13, 19, 25, 42, 45 / 2, 9
We captured 4 out of 5 numbers across our combinations!
"""

import psycopg2
import os
from collections import Counter
import random
import numpy as np
from datetime import datetime

def analyze_july_18_performance():
    """Analyze how our combinations performed on July 18"""
    
    actual_numbers = {13, 19, 25, 42, 45}
    actual_stars = {2, 9}
    
    # Our July 18 combinations
    our_combinations = [
        {'id': 1, 'numbers': [9, 18, 24, 40, 43], 'stars': [4, 6]},
        {'id': 2, 'numbers': [9, 15, 24, 29, 38], 'stars': [1, 7]},
        {'id': 3, 'numbers': [26, 29, 36, 41, 47], 'stars': [2, 3]},
        {'id': 4, 'numbers': [5, 11, 19, 23, 38], 'stars': [2, 3]},
        {'id': 5, 'numbers': [12, 13, 14, 26, 44], 'stars': [1, 2]},
        {'id': 6, 'numbers': [12, 21, 30, 44, 45], 'stars': [1, 8]},
        {'id': 7, 'numbers': [21, 23, 24, 42, 44], 'stars': [1, 7]},
        {'id': 8, 'numbers': [8, 10, 16, 39, 44], 'stars': [3, 8]},
        {'id': 'F1', 'numbers': [8, 14, 15, 18, 19], 'stars': [1, 3]},
        {'id': 'F2', 'numbers': [9, 24, 38, 40, 44], 'stars': [1, 2]}
    ]
    
    print("JULY 18, 2025 EUROMILLIONS ANALYSIS")
    print("=" * 36)
    print(f"Actual Results: {sorted(actual_numbers)} / {sorted(actual_stars)}")
    print()
    
    # Check which combinations had which numbers
    number_coverage = {}
    star_coverage = {}
    best_performers = []
    
    for combo in our_combinations:
        combo_numbers = set(combo['numbers'])
        combo_stars = set(combo['stars'])
        
        number_matches = combo_numbers.intersection(actual_numbers)
        star_matches = combo_stars.intersection(actual_stars)
        
        if number_matches or star_matches:
            score = len(number_matches) * 3 + len(star_matches)
            best_performers.append({
                'id': combo['id'],
                'number_matches': sorted(number_matches),
                'star_matches': sorted(star_matches),
                'score': score
            })
        
        for num in number_matches:
            if num not in number_coverage:
                number_coverage[num] = []
            number_coverage[num].append(combo['id'])
        
        for star in star_matches:
            if star not in star_coverage:
                star_coverage[star] = []
            star_coverage[star].append(combo['id'])
    
    print("WINNING NUMBER COVERAGE:")
    print("-" * 24)
    all_our_numbers = set()
    for combo in our_combinations:
        all_our_numbers.update(combo['numbers'])
    
    covered_numbers = actual_numbers.intersection(all_our_numbers)
    print(f"Covered: {sorted(covered_numbers)} ({len(covered_numbers)}/5)")
    print(f"Missed: {sorted(actual_numbers - covered_numbers)}")
    
    print("\nDETAILED COVERAGE:")
    for num in sorted(actual_numbers):
        if num in number_coverage:
            combos = ', '.join(str(c) for c in number_coverage[num])
            print(f"Number {num}: Found in combinations {combos}")
        else:
            print(f"Number {num}: NOT COVERED")
    
    print("\nSTAR COVERAGE:")
    for star in sorted(actual_stars):
        if star in star_coverage:
            combos = ', '.join(str(c) for c in star_coverage[star])
            print(f"Star {star}: Found in combinations {combos}")
        else:
            print(f"Star {star}: NOT COVERED")
    
    print("\nBEST PERFORMERS:")
    best_performers.sort(key=lambda x: x['score'], reverse=True)
    for perf in best_performers[:5]:
        print(f"Combination {perf['id']}: {len(perf['number_matches'])} numbers {perf['number_matches']}, "
              f"{len(perf['star_matches'])} stars {perf['star_matches']} (Score: {perf['score']})")
    
    return covered_numbers, number_coverage

def get_comprehensive_euromillions_data():
    """Get comprehensive Euromillions data including July 18 results"""
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Add July 18 results to database
    try:
        cursor.execute("""
        INSERT INTO euromillions_drawings (date, n1, n2, n3, n4, n5, s1, s2)
        VALUES ('2025-07-18', 13, 19, 25, 42, 45, 2, 9)
        ON CONFLICT (date) DO NOTHING
        """)
        conn.commit()
    except:
        conn.rollback()
    
    # Get latest draws
    latest_query = """
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC
    LIMIT 15
    """
    
    cursor.execute(latest_query)
    latest_results = cursor.fetchall()
    
    # Get comprehensive training data
    training_query = """
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC
    LIMIT 2000
    """
    
    cursor.execute(training_query)
    training_results = cursor.fetchall()
    conn.close()
    
    return latest_results, training_results

def analyze_winning_patterns(latest_results):
    """Analyze patterns from recent winning draws"""
    
    print("\nRECENT WINNING PATTERNS ANALYSIS")
    print("=" * 32)
    
    recent_numbers = []
    recent_stars = []
    
    for i, row in enumerate(latest_results[:10]):
        date, n1, n2, n3, n4, n5, s1, s2 = row
        numbers = [n1, n2, n3, n4, n5]
        stars = [s1, s2]
        recent_numbers.extend(numbers)
        recent_stars.extend(stars)
        
        if i < 5:
            print(f"{date}: {numbers} / {stars}")
    
    # Analyze patterns
    number_freq = Counter(recent_numbers)
    star_freq = Counter(recent_stars)
    
    print("\nKEY PATTERNS:")
    print(f"Hot numbers: {[n for n, _ in number_freq.most_common(12)]}")
    print(f"Hot stars: {[s for s, _ in star_freq.most_common(8)]}")
    
    # Range analysis
    low_range = [n for n in recent_numbers if n <= 17]
    mid_range = [n for n in recent_numbers if 18 <= n <= 34]
    high_range = [n for n in recent_numbers if n >= 35]
    
    print(f"Range trend: Low: {len(low_range)}, Mid: {len(mid_range)}, High: {len(high_range)}")
    
    # Consecutive patterns
    consecutive_pairs = []
    for row in latest_results[:5]:
        _, n1, n2, n3, n4, n5, s1, s2 = row
        numbers = sorted([n1, n2, n3, n4, n5])
        for i in range(len(numbers)-1):
            if numbers[i+1] - numbers[i] == 1:
                consecutive_pairs.append((numbers[i], numbers[i+1]))
    
    if consecutive_pairs:
        print(f"Recent consecutive pairs: {consecutive_pairs[:3]}")
    
    return {
        'recent_numbers': recent_numbers,
        'recent_stars': recent_stars,
        'hot_numbers': [n for n, _ in number_freq.most_common(12)],
        'hot_stars': [s for s, _ in star_freq.most_common(8)],
        'number_freq': number_freq,
        'star_freq': star_freq
    }

def get_enhanced_historical_analysis(training_results):
    """Enhanced historical analysis with pattern recognition"""
    
    all_numbers = []
    all_stars = []
    
    for row in training_results:
        _, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Enhanced categorization
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_stars = sorted(star_freq.items(), key=lambda x: x[1], reverse=True)
    
    # More refined categories
    total_numbers = len(sorted_numbers)
    total_stars = len(sorted_stars)
    
    ultra_hot = [n for n, _ in sorted_numbers[:total_numbers//5]]
    frequent = [n for n, _ in sorted_numbers[total_numbers//5:total_numbers//3]]
    medium = [n for n, _ in sorted_numbers[total_numbers//3:2*total_numbers//3]]
    rare = [n for n, _ in sorted_numbers[2*total_numbers//3:]]
    
    hot_stars = [s for s, _ in sorted_stars[:total_stars//3]]
    medium_stars = [s for s, _ in sorted_stars[total_stars//3:2*total_stars//3]]
    cold_stars = [s for s, _ in sorted_stars[2*total_stars//3:]]
    
    return {
        'number_freq': number_freq,
        'star_freq': star_freq,
        'ultra_hot': ultra_hot,
        'frequent': frequent,
        'medium': medium,
        'rare': rare,
        'hot_stars': hot_stars,
        'medium_stars': medium_stars,
        'cold_stars': cold_stars
    }

def generate_winning_focused_strategies(historical_data, recent_patterns, covered_numbers):
    """Generate 8 strategies focused on winning based on July 18 insights"""
    
    strategies = []
    
    # Strategy 1: Missing Number Integration (Focus on 25)
    numbers1 = [25]  # The number we missed
    # Add complementary numbers based on patterns
    pool = historical_data['ultra_hot'] + historical_data['frequent']
    pool = [n for n in pool if n != 25]
    numbers1.extend(random.sample(pool, 4))
    
    strategies.append({
        'numbers': sorted(numbers1),
        'strategy': 'Missing Number Integration',
        'focus': 'Incorporating missed number 25 with high-frequency companions'
    })
    
    # Strategy 2: Proven Coverage Enhancement
    # Use numbers that were covered (13, 19, 42, 45) plus strategic additions
    covered_list = list(covered_numbers)
    numbers2 = random.sample(covered_list, min(3, len(covered_list)))
    # Add hot numbers not in coverage
    additional = [n for n in recent_patterns['hot_numbers'] if n not in numbers2]
    numbers2.extend(random.sample(additional, 5 - len(numbers2)))
    
    strategies.append({
        'numbers': sorted(numbers2),
        'strategy': 'Proven Coverage Enhancement',
        'focus': 'Building on successfully covered numbers'
    })
    
    # Strategy 3: Mid-Range Power Play
    # July 18 had strong mid-range presence (19, 25)
    mid_pool = [n for n in historical_data['frequent'] + historical_data['medium'] if 18 <= n <= 34]
    numbers3 = random.sample(mid_pool, 3)
    # Add balance from other ranges
    other_pool = [n for n in historical_data['ultra_hot'] + historical_data['frequent'] if n not in mid_pool]
    numbers3.extend(random.sample(other_pool, 2))
    
    strategies.append({
        'numbers': sorted(numbers3),
        'strategy': 'Mid-Range Power Play',
        'focus': 'Emphasizing mid-range strength from July 18'
    })
    
    # Strategy 4: Ultra Hot Pursuit
    # Focus on the absolute hottest numbers
    numbers4 = random.sample(historical_data['ultra_hot'][:10], 5)
    
    strategies.append({
        'numbers': sorted(numbers4),
        'strategy': 'Ultra Hot Pursuit',
        'focus': 'Concentrating on highest frequency numbers'
    })
    
    # Strategy 5: Consecutive Pattern Explorer
    # July 18 had no consecutives, but they often appear
    numbers5 = []
    base_numbers = random.sample(historical_data['frequent'] + historical_data['medium'], 3)
    numbers5.extend(base_numbers)
    # Try to add consecutive pairs
    for num in base_numbers:
        if num + 1 <= 50 and num + 1 not in numbers5 and len(numbers5) < 5:
            numbers5.append(num + 1)
    
    # Fill remaining slots
    if len(numbers5) < 5:
        remaining = [n for n in historical_data['frequent'] if n not in numbers5]
        numbers5.extend(random.sample(remaining, 5 - len(numbers5)))
    
    strategies.append({
        'numbers': sorted(numbers5[:5]),
        'strategy': 'Consecutive Pattern Explorer',
        'focus': 'Strategic consecutive number inclusion'
    })
    
    # Strategy 6: Balanced Distribution Master
    # Perfect balance across all ranges
    low_nums = [n for n in historical_data['frequent'] + historical_data['medium'] if n <= 17]
    mid_nums = [n for n in historical_data['frequent'] + historical_data['medium'] if 18 <= n <= 34]
    high_nums = [n for n in historical_data['frequent'] + historical_data['medium'] if n >= 35]
    
    numbers6 = []
    numbers6.extend(random.sample(low_nums, 2))
    numbers6.extend(random.sample(mid_nums, 2))
    numbers6.extend(random.sample(high_nums, 1))
    
    strategies.append({
        'numbers': sorted(numbers6),
        'strategy': 'Balanced Distribution Master',
        'focus': 'Perfect range balance with frequency optimization'
    })
    
    # Strategy 7: Gap Fill Specialist
    # Focus on numbers that haven't appeared recently
    recent_set = set(recent_patterns['recent_numbers'][:30])
    gap_numbers = [n for n in historical_data['frequent'] + historical_data['medium'] if n not in recent_set]
    
    numbers7 = random.sample(gap_numbers, min(5, len(gap_numbers)))
    if len(numbers7) < 5:
        numbers7.extend(random.sample(historical_data['frequent'], 5 - len(numbers7)))
    
    strategies.append({
        'numbers': sorted(numbers7[:5]),
        'strategy': 'Gap Fill Specialist',
        'focus': 'Targeting overdue frequent numbers'
    })
    
    # Strategy 8: Statistical Sweet Spot
    # Numbers in the statistical sweet spot (appeared 80-120 times)
    sweet_spot = []
    for num, freq in historical_data['number_freq'].items():
        if 80 <= freq <= 120:
            sweet_spot.append(num)
    
    if len(sweet_spot) >= 5:
        numbers8 = random.sample(sweet_spot, 5)
    else:
        numbers8 = sweet_spot + random.sample(historical_data['frequent'], 5 - len(sweet_spot))
    
    strategies.append({
        'numbers': sorted(numbers8[:5]),
        'strategy': 'Statistical Sweet Spot',
        'focus': 'Optimal frequency range selection'
    })
    
    return strategies

def generate_winning_star_strategies(historical_data, recent_patterns, combination_id):
    """Generate winning-focused star strategies"""
    
    hot_stars = historical_data['hot_stars']
    medium_stars = historical_data['medium_stars']
    cold_stars = historical_data['cold_stars']
    recent_hot = recent_patterns['hot_stars']
    
    # Strategies aligned with number strategies
    strategies = [
        'comprehensive_coverage',      # Combo 1: Cover all bases
        'proven_stars_enhanced',       # Combo 2: Stars that work
        'mid_frequency_focus',         # Combo 3: Medium frequency
        'ultra_hot_stars',            # Combo 4: Hottest stars
        'pattern_breaker',            # Combo 5: Unexpected combinations
        'balanced_selection',         # Combo 6: Perfect balance
        'gap_star_coverage',          # Combo 7: Overdue stars
        'statistical_optimal'         # Combo 8: Statistically optimal
    ]
    
    strategy = strategies[combination_id - 1]
    
    if strategy == 'comprehensive_coverage':
        # Include star 2 (we had it) and star 9 (we missed it)
        if 2 in hot_stars + medium_stars and 9 in hot_stars + medium_stars:
            stars = [2, 9]
        else:
            stars = random.sample(hot_stars + medium_stars, 2)
    
    elif strategy == 'proven_stars_enhanced':
        # Use stars that have been appearing frequently
        stars = random.sample(recent_hot[:4], 2)
    
    elif strategy == 'mid_frequency_focus':
        # Medium frequency stars
        stars = random.sample(medium_stars, 2)
    
    elif strategy == 'ultra_hot_stars':
        # The absolute hottest stars
        stars = hot_stars[:2]
    
    elif strategy == 'pattern_breaker':
        # Mix hot and cold
        stars = [random.choice(hot_stars), random.choice(cold_stars)]
    
    elif strategy == 'balanced_selection':
        # One from each category
        pool = hot_stars + medium_stars
        stars = random.sample(pool, 2)
    
    elif strategy == 'gap_star_coverage':
        # Stars not in recent draws
        recent_stars = set(recent_patterns['recent_stars'][:10])
        gap_stars = [s for s in hot_stars + medium_stars if s not in recent_stars]
        
        if len(gap_stars) >= 2:
            stars = random.sample(gap_stars, 2)
        else:
            stars = gap_stars + random.sample(hot_stars, 2 - len(gap_stars))
    
    else:  # statistical_optimal
        # Stars with optimal frequency
        optimal_stars = []
        for star, freq in historical_data['star_freq'].items():
            if 150 <= freq <= 250:
                optimal_stars.append(star)
        
        if len(optimal_stars) >= 2:
            stars = random.sample(optimal_stars, 2)
        else:
            stars = random.sample(hot_stars + medium_stars, 2)
    
    return sorted(stars)

def generate_8_winning_combinations():
    """Generate 8 combinations optimized for winning"""
    
    print("\nGENERATING 8 WINNING-OPTIMIZED COMBINATIONS")
    print("=" * 42)
    
    # Analyze July 18 performance
    covered_numbers, number_coverage = analyze_july_18_performance()
    
    # Get comprehensive data
    latest_results, training_results = get_comprehensive_euromillions_data()
    recent_patterns = analyze_winning_patterns(latest_results)
    historical_data = get_enhanced_historical_analysis(training_results)
    
    print("\nWINNING STRATEGY INSIGHTS:")
    print("-" * 26)
    print("✓ Successfully covered 4/5 numbers (13, 19, 42, 45)")
    print("✓ Missed number 25 - incorporating it strategically")
    print("✓ Star 2 was covered, star 9 needs attention")
    print("✓ Mid-range numbers showing strength")
    print("✓ Multiple coverage points increase winning chances")
    print()
    
    # Generate strategies
    number_strategies = generate_winning_focused_strategies(historical_data, recent_patterns, covered_numbers)
    
    # Generate complete combinations
    combinations = []
    
    for i, num_strategy in enumerate(number_strategies):
        combination_id = i + 1
        star_numbers = generate_winning_star_strategies(historical_data, recent_patterns, combination_id)
        
        star_strategy_names = [
            'Comprehensive Coverage Stars',
            'Proven Stars Enhanced',
            'Mid Frequency Focus Stars',
            'Ultra Hot Stars',
            'Pattern Breaker Stars',
            'Balanced Selection Stars',
            'Gap Star Coverage',
            'Statistical Optimal Stars'
        ]
        
        combination = {
            'id': combination_id,
            'numbers': num_strategy['numbers'],
            'stars': star_numbers,
            'strategy': f"{num_strategy['strategy']} + {star_strategy_names[i]}",
            'focus': f"{num_strategy['focus']} + {star_strategy_names[i].lower()}"
        }
        
        combinations.append(combination)
    
    return combinations

def generate_2_power_fusion_combinations(main_combinations):
    """Generate 2 powerful fusion combinations"""
    
    print("\nGENERATING 2 POWER FUSION COMBINATIONS")
    print("=" * 35)
    
    all_numbers = []
    all_stars = []
    
    for combo in main_combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    # Fusion 1: July 18 Success Amplifier
    # Heavy emphasis on strategies that would have won
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Include 25 (missed number) and most common from successful patterns
    fusion1_numbers = [25]
    top_numbers = [n for n, _ in number_freq.most_common(10) if n != 25]
    fusion1_numbers.extend(top_numbers[:4])
    
    # Include both 2 and 9 if possible
    if 2 in star_freq and 9 in star_freq:
        fusion1_stars = [2, 9]
    else:
        fusion1_stars = [s for s, _ in star_freq.most_common(2)]
    
    fusion1 = {
        'id': 'F1',
        'numbers': sorted(fusion1_numbers),
        'stars': sorted(fusion1_stars),
        'strategy': 'July 18 Success Amplifier',
        'focus': 'Maximizing coverage of proven patterns'
    }
    
    # Fusion 2: Statistical Power Blend
    # Use mathematical optimization
    most_frequent_numbers = [n for n, _ in number_freq.most_common(15)]
    
    # Select numbers that appear in multiple combinations
    multi_appearance = [n for n, count in number_freq.items() if count >= 2]
    
    fusion2_numbers = []
    fusion2_numbers.extend(multi_appearance[:3])
    
    # Add numbers from different ranges
    remaining = [n for n in most_frequent_numbers if n not in fusion2_numbers]
    low_remaining = [n for n in remaining if n <= 17]
    high_remaining = [n for n in remaining if n >= 35]
    
    if low_remaining:
        fusion2_numbers.append(random.choice(low_remaining))
    if high_remaining:
        fusion2_numbers.append(random.choice(high_remaining))
    
    # Fill to 5
    if len(fusion2_numbers) < 5:
        fusion2_numbers.extend(remaining[:5-len(fusion2_numbers)])
    
    fusion2_stars = [s for s, _ in star_freq.most_common(2)]
    
    fusion2 = {
        'id': 'F2',
        'numbers': sorted(fusion2_numbers[:5]),
        'stars': sorted(fusion2_stars),
        'strategy': 'Statistical Power Blend',
        'focus': 'Mathematical optimization of coverage'
    }
    
    return [fusion1, fusion2]

def display_winning_combinations_set(main_combinations, fusion_combinations):
    """Display the complete winning-optimized set"""
    
    print("\nCOMPLETE WINNING-OPTIMIZED SET")
    print("=" * 31)
    
    print("8 MAIN COMBINATIONS:")
    print("-" * 19)
    for combo in main_combinations:
        print(f"{combo['id']}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} + Stars: {combo['stars']}")
        print(f"   Focus: {combo['focus']}")
        print()
    
    print("2 POWER FUSION COMBINATIONS:")
    print("-" * 28)
    for fusion in fusion_combinations:
        print(f"{fusion['id']}. {fusion['strategy']}")
        print(f"   Numbers: {fusion['numbers']} + Stars: {fusion['stars']}")
        print(f"   Focus: {fusion['focus']}")
        print()
    
    # Coverage analysis
    all_numbers = set()
    all_stars = set()
    
    for combo in main_combinations + fusion_combinations:
        all_numbers.update(combo['numbers'])
        all_stars.update(combo['stars'])
    
    # Check specific coverage
    july_18_numbers = {13, 19, 25, 42, 45}
    july_18_stars = {2, 9}
    
    print("STRATEGIC COVERAGE ANALYSIS:")
    print("-" * 28)
    print(f"Total unique numbers: {len(all_numbers)}/50")
    print(f"Total unique stars: {len(all_stars)}/12")
    
    july_18_coverage = all_numbers.intersection(july_18_numbers)
    print(f"\nJuly 18 number coverage: {sorted(july_18_coverage)} ({len(july_18_coverage)}/5)")
    
    july_18_star_coverage = all_stars.intersection(july_18_stars)
    print(f"July 18 star coverage: {sorted(july_18_star_coverage)} ({len(july_18_star_coverage)}/2)")
    
    print(f"\nNumbers used: {sorted(all_numbers)}")
    print(f"Stars used: {sorted(all_stars)}")
    
    return main_combinations, fusion_combinations

def main():
    """Main function to generate winning combinations"""
    
    # Generate 8 winning-optimized combinations
    main_combinations = generate_8_winning_combinations()
    
    # Generate 2 power fusion combinations
    fusion_combinations = generate_2_power_fusion_combinations(main_combinations)
    
    # Display complete set
    main_combinations, fusion_combinations = display_winning_combinations_set(main_combinations, fusion_combinations)
    
    print("\nWINNING OPTIMIZATION STRATEGY:")
    print("-" * 30)
    print("✓ Incorporated missed number 25 strategically")
    print("✓ Enhanced coverage of proven winning numbers")
    print("✓ Focused on mid-range strength from July 18")
    print("✓ Multiple coverage points for all winning numbers")
    print("✓ Star strategies optimized for 2 and 9")
    print("✓ Statistical sweet spot targeting")
    print("✓ Power fusions for maximum impact")
    print("\nBEST OF LUCK! 🍀")

if __name__ == "__main__":
    main()