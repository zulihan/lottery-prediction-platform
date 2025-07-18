"""
Generate 8 Euromillions combinations + 2 fusion combinations for tonight's draw
Incorporating lessons from July 15 performance analysis
Using proven Euromillions strategies with mixed approaches
"""

import psycopg2
import os
from collections import Counter
import random
import numpy as np
from datetime import datetime

def get_latest_euromillions_data():
    """Get latest Euromillions data including July 15 results"""
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get latest draws for analysis
    latest_query = """
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC
    LIMIT 10
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

def analyze_recent_patterns_with_july_15(latest_results):
    """Analyze patterns including July 15 performance insights"""
    
    print("RECENT EUROMILLIONS DRAWS ANALYSIS")
    print("=" * 34)
    
    recent_numbers = []
    recent_stars = []
    
    for i, row in enumerate(latest_results[:8]):
        date, n1, n2, n3, n4, n5, s1, s2 = row
        numbers = [n1, n2, n3, n4, n5]
        stars = [s1, s2]
        recent_numbers.extend(numbers)
        recent_stars.extend(stars)
        
        # Highlight July 15 results
        if str(date) == '2025-07-15':
            print(f"{date}: {numbers} / {stars} ← JULY 15 RESULTS")
        else:
            print(f"{date}: {numbers} / {stars}")
    
    print()
    print("PATTERN INSIGHTS:")
    
    # Number patterns
    number_freq = Counter(recent_numbers)
    most_common_numbers = number_freq.most_common(12)
    print(f"Hot numbers (recent): {[n for n, _ in most_common_numbers[:10]]}")
    
    # Star patterns
    star_freq = Counter(recent_stars)
    most_common_stars = star_freq.most_common(8)
    print(f"Hot stars (recent): {[s for s, _ in most_common_stars[:8]]}")
    
    # Range analysis
    low_range = [n for n in recent_numbers if n <= 17]
    mid_range = [n for n in recent_numbers if 18 <= n <= 34]
    high_range = [n for n in recent_numbers if n >= 35]
    
    print(f"Range distribution: Low(1-17): {len(low_range)}, Mid(18-34): {len(mid_range)}, High(35-50): {len(high_range)}")
    
    # July 15 lessons
    print("\nJULY 15 PERFORMANCE LESSONS:")
    print("• Frequency Contrarian strategy performed best")
    print("• Recent Pattern Integration was also top performer")
    print("• High numbers (35-50) dominated the draw")
    print("• Star 6 appeared in winning combinations")
    print("• Need better coverage of number 49 range")
    
    return {
        'recent_numbers': recent_numbers,
        'recent_stars': recent_stars,
        'hot_numbers': [n for n, _ in most_common_numbers[:10]],
        'hot_stars': [s for s, _ in most_common_stars[:8]],
        'number_freq': number_freq,
        'star_freq': star_freq
    }

def get_euromillions_historical_data(training_results):
    """Get comprehensive Euromillions frequency analysis from 2000 draws"""
    
    all_numbers = []
    all_stars = []
    
    for row in training_results:
        _, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Categorize by frequency
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_stars = sorted(star_freq.items(), key=lambda x: x[1], reverse=True)
    
    total_numbers = len(sorted_numbers)
    total_stars = len(sorted_stars)
    
    frequent_numbers = [n for n, _ in sorted_numbers[:total_numbers//3]]
    medium_numbers = [n for n, _ in sorted_numbers[total_numbers//3:2*total_numbers//3]]
    rare_numbers = [n for n, _ in sorted_numbers[2*total_numbers//3:]]
    
    frequent_stars = [s for s, _ in sorted_stars[:total_stars//3]]
    medium_stars = [s for s, _ in sorted_stars[total_stars//3:2*total_stars//3]]
    rare_stars = [s for s, _ in sorted_stars[2*total_stars//3:]]
    
    return {
        'number_freq': number_freq,
        'star_freq': star_freq,
        'frequent_numbers': frequent_numbers,
        'medium_numbers': medium_numbers,
        'rare_numbers': rare_numbers,
        'frequent_stars': frequent_stars,
        'medium_stars': medium_stars,
        'rare_stars': rare_stars
    }

def generate_enhanced_number_strategies(historical_data, recent_patterns):
    """Generate 8 enhanced number strategies based on July 15 lessons"""
    
    frequent = historical_data['frequent_numbers']
    medium = historical_data['medium_numbers']
    rare = historical_data['rare_numbers']
    hot_recent = recent_patterns['hot_numbers']
    
    strategies = []
    
    # Strategy 1: Enhanced Frequency Contrarian (July 15 winner)
    numbers1 = []
    # Emphasize rare numbers with some medium
    numbers1.extend(random.sample(rare, 3))
    numbers1.extend(random.sample(medium, 2))
    # Ensure high number coverage (learned from July 15)
    high_numbers = [n for n in numbers1 if n >= 35]
    if len(high_numbers) < 2:
        high_rare = [n for n in rare + medium if n >= 35]
        if high_rare:
            numbers1[-1] = random.choice(high_rare)
    
    strategies.append({
        'numbers': sorted(numbers1),
        'strategy': 'Enhanced Frequency Contrarian',
        'focus': 'July 15 winner - rare numbers with high emphasis'
    })
    
    # Strategy 2: Recent Pattern Integration Enhanced (July 15 winner)
    numbers2 = []
    # Use recent hot numbers plus historical balance
    recent_integration = random.sample(hot_recent, min(3, len(hot_recent)))
    remaining_pool = [n for n in frequent + medium if n not in recent_integration]
    numbers2.extend(recent_integration)
    numbers2.extend(random.sample(remaining_pool, 5 - len(recent_integration)))
    
    strategies.append({
        'numbers': sorted(numbers2),
        'strategy': 'Recent Pattern Integration Enhanced',
        'focus': 'July 15 winner - recent hot with historical balance'
    })
    
    # Strategy 3: High Number Emphasis (July 15 lesson)
    numbers3 = []
    high_numbers_pool = [n for n in frequent + medium + rare if n >= 35]
    mid_high_pool = [n for n in frequent + medium if 25 <= n <= 34]
    numbers3.extend(random.sample(high_numbers_pool, 3))
    numbers3.extend(random.sample(mid_high_pool, 2))
    
    strategies.append({
        'numbers': sorted(numbers3),
        'strategy': 'High Number Emphasis',
        'focus': 'July 15 lesson - high number concentration'
    })
    
    # Strategy 4: Coverage Optimization Refined
    numbers4 = []
    # Balanced approach with recent hot integration
    numbers4.extend(random.sample([n for n in frequent if n in hot_recent], min(2, len([n for n in frequent if n in hot_recent]))))
    remaining_pool = [n for n in frequent + medium if n not in numbers4]
    numbers4.extend(random.sample(remaining_pool, 5 - len(numbers4)))
    
    # Ensure range balance
    low_range = [n for n in numbers4 if n <= 17]
    high_range = [n for n in numbers4 if n >= 35]
    if not low_range:
        numbers4[0] = random.choice([n for n in frequent + medium if n <= 17])
    if not high_range:
        numbers4[-1] = random.choice([n for n in frequent + medium if n >= 35])
    
    strategies.append({
        'numbers': sorted(numbers4),
        'strategy': 'Coverage Optimization Refined',
        'focus': 'Proven strategy with July 15 insights'
    })
    
    # Strategy 5: Gap Analysis Enhanced
    recent_numbers = set(recent_patterns['recent_numbers'])
    gap_candidates = [n for n in frequent + medium if n not in recent_numbers]
    numbers5 = random.sample(gap_candidates, min(5, len(gap_candidates)))
    if len(numbers5) < 5:
        numbers5.extend(random.sample(frequent + medium, 5 - len(numbers5)))
    
    strategies.append({
        'numbers': sorted(numbers5[:5]),
        'strategy': 'Gap Analysis Enhanced',
        'focus': 'Overdue numbers with July 15 adjustments'
    })
    
    # Strategy 6: Mathematical Range Balance Plus
    numbers6 = []
    low_nums = [n for n in frequent + medium if n <= 17]
    mid_nums = [n for n in frequent + medium if 18 <= n <= 34]
    high_nums = [n for n in frequent + medium if n >= 35]
    
    numbers6.extend(random.sample(low_nums, 1))
    numbers6.extend(random.sample(mid_nums, 2))
    numbers6.extend(random.sample(high_nums, 2))  # Increased high number coverage
    
    strategies.append({
        'numbers': sorted(numbers6),
        'strategy': 'Mathematical Range Balance Plus',
        'focus': 'Balanced with enhanced high number coverage'
    })
    
    # Strategy 7: Frequency Hot Pursuit Advanced
    hot_pool = list(set(frequent[:12] + hot_recent))
    # Ensure some high numbers in hot pursuit
    hot_high = [n for n in hot_pool if n >= 35]
    hot_other = [n for n in hot_pool if n < 35]
    
    numbers7 = []
    numbers7.extend(random.sample(hot_high, min(2, len(hot_high))))
    numbers7.extend(random.sample(hot_other, 5 - len(numbers7)))
    
    strategies.append({
        'numbers': sorted(numbers7),
        'strategy': 'Frequency Hot Pursuit Advanced',
        'focus': 'Hot numbers with high number emphasis'
    })
    
    # Strategy 8: Hybrid Balanced Evolution
    numbers8 = []
    numbers8.extend(random.sample(frequent, 2))
    numbers8.extend(random.sample(medium, 2))
    numbers8.extend(random.sample(rare, 1))
    
    # Ensure at least one high number
    high_in_selection = [n for n in numbers8 if n >= 35]
    if not high_in_selection:
        high_replacements = [n for n in frequent + medium + rare if n >= 35]
        if high_replacements:
            numbers8[-1] = random.choice(high_replacements)
    
    strategies.append({
        'numbers': sorted(numbers8),
        'strategy': 'Hybrid Balanced Evolution',
        'focus': 'Balanced approach with July 15 evolution'
    })
    
    return strategies

def generate_enhanced_star_strategies(historical_data, recent_patterns, combination_id):
    """Generate stars with enhanced strategies based on July 15 lessons"""
    
    frequent_stars = historical_data['frequent_stars']
    medium_stars = historical_data['medium_stars']
    rare_stars = historical_data['rare_stars']
    hot_recent_stars = recent_patterns['hot_stars']
    
    # 8 different enhanced star strategies
    star_strategies = [
        'contrarian_enhanced',         # Combination 1 - align with contrarian numbers
        'recent_pattern_focus',        # Combination 2 - align with recent pattern
        'high_frequency_plus',         # Combination 3 - enhanced frequency
        'balanced_coverage',           # Combination 4 - coverage alignment
        'gap_complement',              # Combination 5 - gap analysis complement
        'mathematical_range_star',     # Combination 6 - range balance complement
        'hot_pursuit_stars',           # Combination 7 - hot pursuit alignment
        'hybrid_evolution_stars'       # Combination 8 - hybrid evolution
    ]
    
    strategy = star_strategies[combination_id - 1]
    
    if strategy == 'contrarian_enhanced':
        # Use rare/medium stars (align with contrarian approach)
        candidates = rare_stars + medium_stars
        # Include star 6 (July 15 winner)
        if 6 in candidates:
            stars = [6]
            remaining = [s for s in candidates if s != 6]
            stars.append(random.choice(remaining))
        else:
            stars = random.sample(candidates, 2)
    
    elif strategy == 'recent_pattern_focus':
        # Use recent hot stars with strategic selection
        if len(hot_recent_stars) >= 2:
            stars = random.sample(hot_recent_stars, 2)
        else:
            stars = hot_recent_stars + random.sample(frequent_stars, 2 - len(hot_recent_stars))
    
    elif strategy == 'high_frequency_plus':
        # Enhanced frequency approach
        stars = random.sample(frequent_stars, 2)
    
    elif strategy == 'balanced_coverage':
        # Balanced mix with strategic coverage
        pool = frequent_stars + medium_stars
        stars = random.sample(pool, 2)
    
    elif strategy == 'gap_complement':
        # Focus on stars that haven't appeared recently
        recent_stars = set(recent_patterns['recent_stars'])
        gap_star_candidates = [s for s in frequent_stars + medium_stars if s not in recent_stars]
        
        if len(gap_star_candidates) >= 2:
            stars = random.sample(gap_star_candidates, 2)
        else:
            stars = gap_star_candidates + random.sample(frequent_stars + medium_stars, 2 - len(gap_star_candidates))
    
    elif strategy == 'mathematical_range_star':
        # Range approach with July 15 insight
        low_stars = [s for s in frequent_stars + medium_stars if s <= 6]
        high_stars = [s for s in frequent_stars + medium_stars if s >= 7]
        
        if low_stars and high_stars:
            stars = [random.choice(low_stars), random.choice(high_stars)]
        else:
            stars = random.sample(frequent_stars + medium_stars, 2)
    
    elif strategy == 'hot_pursuit_stars':
        # Hot pursuit alignment
        hot_star_pool = frequent_stars + [s for s in hot_recent_stars if s in frequent_stars + medium_stars]
        stars = random.sample(hot_star_pool, 2)
    
    else:  # hybrid_evolution_stars
        # Evolved hybrid approach
        weighted_pool = frequent_stars * 2 + medium_stars + rare_stars
        stars = random.sample(list(set(weighted_pool)), 2)
    
    return sorted(stars)

def generate_8_enhanced_combinations():
    """Generate 8 enhanced Euromillions combinations for tonight"""
    
    print("GENERATING 8 ENHANCED EUROMILLIONS COMBINATIONS FOR TONIGHT")
    print("=" * 57)
    
    # Get data
    latest_results, training_results = get_latest_euromillions_data()
    recent_patterns = analyze_recent_patterns_with_july_15(latest_results)
    historical_data = get_euromillions_historical_data(training_results)
    
    print("\nENHANCED STRATEGIC APPROACH:")
    print("-" * 28)
    print("Numbers: 8 enhanced strategies incorporating July 15 lessons")
    print("Stars: Different enhanced strategy per combination")
    print("Focus: Contrarian and Pattern Integration emphasis")
    print()
    
    # Generate number strategies
    number_strategies = generate_enhanced_number_strategies(historical_data, recent_patterns)
    
    # Generate complete combinations
    combinations = []
    
    for i, num_strategy in enumerate(number_strategies):
        combination_id = i + 1
        star_numbers = generate_enhanced_star_strategies(historical_data, recent_patterns, combination_id)
        
        # Enhanced star strategy names
        star_strategy_names = [
            'Contrarian Enhanced Stars',
            'Recent Pattern Focus Stars',
            'High Frequency Plus Stars',
            'Balanced Coverage Stars',
            'Gap Complement Stars',
            'Mathematical Range Stars',
            'Hot Pursuit Stars',
            'Hybrid Evolution Stars'
        ]
        
        combination = {
            'id': combination_id,
            'numbers': num_strategy['numbers'],
            'stars': star_numbers,
            'strategy': f"{num_strategy['strategy']} + {star_strategy_names[i]}",
            'focus': f"{num_strategy['focus']} + {star_strategy_names[i].lower()}",
            'number_strategy': num_strategy['strategy'],
            'star_strategy': star_strategy_names[i]
        }
        
        combinations.append(combination)
    
    return combinations

def generate_2_enhanced_fusion_combinations(main_combinations):
    """Generate 2 enhanced fusion combinations"""
    
    print("\nGENERATING 2 ENHANCED FUSION COMBINATIONS")
    print("=" * 37)
    
    all_numbers = []
    all_stars = []
    
    for combo in main_combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    # Fusion 1: July 15 Winners Weighted Blend
    # Emphasize the July 15 winning strategies (Contrarian and Pattern Integration)
    strategy_weights = [0.3, 0.3, 0.15, 0.1, 0.05, 0.05, 0.025, 0.025]  # Heavy emphasis on combos 1&2
    
    weighted_numbers = []
    weighted_stars = []
    
    for i, combo in enumerate(main_combinations):
        weight = strategy_weights[i]
        num_numbers = max(1, int(10 * weight))
        num_stars = max(1, int(4 * weight))
        
        selected_numbers = random.sample(combo['numbers'], min(num_numbers, len(combo['numbers'])))
        selected_stars = random.sample(combo['stars'], min(num_stars, len(combo['stars'])))
        
        weighted_numbers.extend(selected_numbers)
        weighted_stars.extend(selected_stars)
    
    # Remove duplicates and ensure correct counts
    fusion1_numbers = list(set(weighted_numbers))
    if len(fusion1_numbers) > 5:
        fusion1_numbers = sorted(fusion1_numbers)[:5]
    elif len(fusion1_numbers) < 5:
        remaining_pool = [n for combo in main_combinations for n in combo['numbers']]
        additional = [n for n in remaining_pool if n not in fusion1_numbers]
        fusion1_numbers.extend(random.sample(additional, 5 - len(fusion1_numbers)))
    
    fusion1_stars = list(set(weighted_stars))
    if len(fusion1_stars) > 2:
        fusion1_stars = sorted(fusion1_stars)[:2]
    elif len(fusion1_stars) < 2:
        remaining_stars = [s for combo in main_combinations for s in combo['stars']]
        additional_stars = [s for s in remaining_stars if s not in fusion1_stars]
        fusion1_stars.extend(random.sample(additional_stars, 2 - len(fusion1_stars)))
    
    fusion1 = {
        'id': 'F1',
        'numbers': sorted(fusion1_numbers),
        'stars': sorted(fusion1_stars),
        'strategy': 'July 15 Winners Weighted Blend',
        'focus': 'Heavy emphasis on July 15 winning strategies'
    }
    
    # Fusion 2: High Number Focus Fusion
    # Focus on high numbers (July 15 lesson) with frequency weighting
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Prioritize high numbers from all combinations
    high_numbers = [n for n, _ in number_freq.most_common() if n >= 35]
    other_numbers = [n for n, _ in number_freq.most_common() if n < 35]
    
    fusion2_numbers = []
    fusion2_numbers.extend(high_numbers[:3])  # Take top 3 high numbers
    fusion2_numbers.extend(other_numbers[:2])  # Take top 2 other numbers
    
    # Most common stars
    most_common_stars = [s for s, _ in star_freq.most_common(4)]
    fusion2_stars = sorted(random.sample(most_common_stars, 2))
    
    fusion2 = {
        'id': 'F2',
        'numbers': sorted(fusion2_numbers),
        'stars': fusion2_stars,
        'strategy': 'High Number Focus Fusion',
        'focus': 'High number emphasis with frequency weighting'
    }
    
    return [fusion1, fusion2]

def display_complete_enhanced_set(main_combinations, fusion_combinations):
    """Display the complete enhanced set"""
    
    print("\nCOMPLETE ENHANCED EUROMILLIONS SET FOR TONIGHT")
    print("=" * 42)
    
    print("8 MAIN COMBINATIONS:")
    print("-" * 19)
    for combo in main_combinations:
        print(f"{combo['id']}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} + Stars: {combo['stars']}")
        print(f"   Focus: {combo['focus']}")
        print()
    
    print("2 FUSION COMBINATIONS:")
    print("-" * 21)
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
    
    print("COVERAGE ANALYSIS:")
    print("-" * 17)
    print(f"Total unique numbers: {len(all_numbers)}/50")
    print(f"Total unique stars: {len(all_stars)}/12")
    print(f"Numbers used: {sorted(all_numbers)}")
    print(f"Stars used: {sorted(all_stars)}")
    
    return main_combinations, fusion_combinations

def main():
    """Main function to generate enhanced combinations"""
    
    # Generate 8 enhanced main combinations
    main_combinations = generate_8_enhanced_combinations()
    
    # Generate 2 enhanced fusion combinations
    fusion_combinations = generate_2_enhanced_fusion_combinations(main_combinations)
    
    # Display complete set
    main_combinations, fusion_combinations = display_complete_enhanced_set(main_combinations, fusion_combinations)
    
    print("\nENHANCED STRATEGY PRINCIPLES:")
    print("-" * 29)
    print("✓ Incorporating July 15 performance lessons")
    print("✓ Enhanced Frequency Contrarian emphasis")
    print("✓ Recent Pattern Integration focus")
    print("✓ High number coverage improvement")
    print("✓ Star 6 strategic inclusion")
    print("✓ 2000 historical draws foundation")
    print("✓ Mixed star strategies per combination")
    print("✓ Comprehensive coverage optimization")

if __name__ == "__main__":
    main()