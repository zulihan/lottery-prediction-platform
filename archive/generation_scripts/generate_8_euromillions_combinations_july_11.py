"""
Generate 8 Euromillions combinations for July 11, 2025
Using proven Euromillions strategies with mixed approaches for numbers vs stars
Then generate 2 fusion combinations from the 8 main combinations
"""

import psycopg2
import os
from collections import Counter
import random
import numpy as np

def get_latest_euromillions_data():
    """Get latest Euromillions data including recent July draws"""
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

def analyze_recent_euromillions_patterns(latest_results):
    """Analyze patterns from recent Euromillions draws"""
    
    print("RECENT EUROMILLIONS DRAWS ANALYSIS")
    print("=" * 34)
    
    recent_numbers = []
    recent_stars = []
    
    for i, row in enumerate(latest_results[:6]):
        date, n1, n2, n3, n4, n5, s1, s2 = row
        numbers = [n1, n2, n3, n4, n5]
        stars = [s1, s2]
        recent_numbers.extend(numbers)
        recent_stars.extend(stars)
        
        print(f"{date}: {numbers} / {stars}")
    
    print()
    print("PATTERN INSIGHTS:")
    
    # Number patterns
    number_freq = Counter(recent_numbers)
    most_common_numbers = number_freq.most_common(10)
    print(f"Hot numbers (recent): {[n for n, _ in most_common_numbers[:8]]}")
    
    # Star patterns
    star_freq = Counter(recent_stars)
    most_common_stars = star_freq.most_common(6)
    print(f"Hot stars (recent): {[s for s, _ in most_common_stars[:6]]}")
    
    # Range analysis
    low_range = [n for n in recent_numbers if n <= 17]
    mid_range = [n for n in recent_numbers if 18 <= n <= 34]
    high_range = [n for n in recent_numbers if n >= 35]
    
    print(f"Range distribution: Low(1-17): {len(low_range)}, Mid(18-34): {len(mid_range)}, High(35-50): {len(high_range)}")
    
    return {
        'recent_numbers': recent_numbers,
        'recent_stars': recent_stars,
        'hot_numbers': [n for n, _ in most_common_numbers[:8]],
        'hot_stars': [s for s, _ in most_common_stars[:6]],
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

def generate_euromillions_number_strategies(historical_data, recent_patterns):
    """Generate 8 different number strategies for Euromillions"""
    
    frequent = historical_data['frequent_numbers']
    medium = historical_data['medium_numbers']
    rare = historical_data['rare_numbers']
    hot_recent = recent_patterns['hot_numbers']
    
    strategies = []
    
    # Strategy 1: Coverage Optimization Enhanced (June 3 winner)
    numbers1 = []
    numbers1.extend(random.sample([n for n in frequent if n in hot_recent], min(2, len([n for n in frequent if n in hot_recent]))))
    remaining_pool = [n for n in frequent + medium if n not in numbers1]
    numbers1.extend(random.sample(remaining_pool, 5 - len(numbers1)))
    
    # Range balancing
    low_range = [n for n in numbers1 if n <= 17]
    high_range = [n for n in numbers1 if n >= 35]
    if not low_range:
        numbers1[0] = random.choice([n for n in frequent + medium if n <= 17])
    if not high_range:
        numbers1[-1] = random.choice([n for n in frequent + medium if n >= 35])
    
    strategies.append({
        'numbers': sorted(numbers1),
        'strategy': 'Coverage Optimization Enhanced',
        'focus': 'Proven June 3 winner with recent hot integration'
    })
    
    # Strategy 2: Enhanced Risk-Reward (June 20 winner)
    numbers2 = []
    numbers2.extend(random.sample(medium, 3))
    numbers2.extend(random.sample(rare, 2))
    strategies.append({
        'numbers': sorted(numbers2),
        'strategy': 'Enhanced Risk-Reward',
        'focus': 'Proven June 20 winner - medium and rare emphasis'
    })
    
    # Strategy 3: Frequency Hot Pursuit
    hot_pool = list(set(frequent[:15] + hot_recent))
    numbers3 = random.sample(hot_pool, 5)
    strategies.append({
        'numbers': sorted(numbers3),
        'strategy': 'Frequency Hot Pursuit',
        'focus': 'Hot number concentration'
    })
    
    # Strategy 4: Balanced Hybrid
    numbers4 = []
    numbers4.extend(random.sample(frequent, 2))
    numbers4.extend(random.sample(medium, 2))
    numbers4.extend(random.sample(rare, 1))
    strategies.append({
        'numbers': sorted(numbers4),
        'strategy': 'Balanced Hybrid',
        'focus': 'Balanced frequency distribution'
    })
    
    # Strategy 5: Gap Analysis Strategy
    recent_numbers = set(recent_patterns['recent_numbers'])
    gap_candidates = [n for n in frequent + medium if n not in recent_numbers]
    numbers5 = random.sample(gap_candidates, min(5, len(gap_candidates)))
    if len(numbers5) < 5:
        numbers5.extend(random.sample(frequent + medium, 5 - len(numbers5)))
    strategies.append({
        'numbers': sorted(numbers5[:5]),
        'strategy': 'Gap Analysis',
        'focus': 'Overdue number focus'
    })
    
    # Strategy 6: Mathematical Range Balance
    numbers6 = []
    low_nums = [n for n in frequent + medium if n <= 17]
    mid_nums = [n for n in frequent + medium if 18 <= n <= 34]
    high_nums = [n for n in frequent + medium if n >= 35]
    
    numbers6.extend(random.sample(low_nums, 2))
    numbers6.extend(random.sample(mid_nums, 2))
    numbers6.extend(random.sample(high_nums, 1))
    strategies.append({
        'numbers': sorted(numbers6),
        'strategy': 'Mathematical Range Balance',
        'focus': 'Optimal range distribution'
    })
    
    # Strategy 7: Frequency Contrarian
    numbers7 = []
    numbers7.extend(random.sample(rare, 3))
    numbers7.extend(random.sample(medium, 2))
    strategies.append({
        'numbers': sorted(numbers7),
        'strategy': 'Frequency Contrarian',
        'focus': 'Rare number emphasis'
    })
    
    # Strategy 8: Recent Pattern Integration Enhanced
    numbers8 = []
    recent_integration = random.sample(hot_recent, min(3, len(hot_recent)))
    remaining_pool = [n for n in frequent + medium if n not in recent_integration]
    numbers8.extend(recent_integration)
    numbers8.extend(random.sample(remaining_pool, 5 - len(recent_integration)))
    strategies.append({
        'numbers': sorted(numbers8),
        'strategy': 'Recent Pattern Integration Enhanced',
        'focus': 'Recent hot numbers with historical balance'
    })
    
    return strategies

def generate_euromillions_star_strategies(historical_data, recent_patterns, combination_id):
    """Generate stars using DIFFERENT strategy than numbers (Euromillions mixed principle)"""
    
    frequent_stars = historical_data['frequent_stars']
    medium_stars = historical_data['medium_stars']
    rare_stars = historical_data['rare_stars']
    hot_recent_stars = recent_patterns['hot_stars']
    
    # 8 different star strategies
    star_strategies = [
        'frequency_dominant',      # Combination 1
        'recent_hot_focus',        # Combination 2
        'balanced_mix',            # Combination 3
        'contrarian_rare',         # Combination 4
        'mathematical_range',      # Combination 5
        'weighted_balance',        # Combination 6
        'gap_analysis_stars',      # Combination 7
        'strategic_rotation'       # Combination 8
    ]
    
    strategy = star_strategies[combination_id - 1]
    
    if strategy == 'frequency_dominant':
        # Use most frequent stars
        stars = random.sample(frequent_stars, 2)
    
    elif strategy == 'recent_hot_focus':
        # Use recent hot stars
        if len(hot_recent_stars) >= 2:
            stars = random.sample(hot_recent_stars, 2)
        else:
            stars = hot_recent_stars + random.sample(frequent_stars, 2 - len(hot_recent_stars))
    
    elif strategy == 'balanced_mix':
        # Mix frequent and medium
        pool = frequent_stars + medium_stars
        stars = random.sample(pool, 2)
    
    elif strategy == 'contrarian_rare':
        # Use rare stars (contrarian approach)
        if len(rare_stars) >= 2:
            stars = random.sample(rare_stars, 2)
        else:
            stars = rare_stars + random.sample(medium_stars, 2 - len(rare_stars))
    
    elif strategy == 'mathematical_range':
        # Use mathematical range approach (low + high)
        low_stars = [s for s in frequent_stars + medium_stars if s <= 6]
        high_stars = [s for s in frequent_stars + medium_stars if s >= 7]
        
        if low_stars and high_stars:
            stars = [random.choice(low_stars), random.choice(high_stars)]
        else:
            stars = random.sample(frequent_stars + medium_stars, 2)
    
    elif strategy == 'weighted_balance':
        # Weighted approach favoring frequent but including variety
        pool = frequent_stars * 2 + medium_stars
        stars = random.sample(pool, 2)
        stars = list(set(stars))  # Remove duplicates
        if len(stars) < 2:
            stars.extend(random.sample(frequent_stars + medium_stars, 2 - len(stars)))
    
    elif strategy == 'gap_analysis_stars':
        # Focus on stars that haven't appeared recently
        recent_stars = set(recent_patterns['recent_stars'])
        gap_star_candidates = [s for s in frequent_stars + medium_stars if s not in recent_stars]
        
        if len(gap_star_candidates) >= 2:
            stars = random.sample(gap_star_candidates, 2)
        else:
            stars = gap_star_candidates + random.sample(frequent_stars + medium_stars, 2 - len(gap_star_candidates))
    
    else:  # strategic_rotation
        # Rotate through different approaches based on combination ID
        all_stars = frequent_stars + medium_stars + rare_stars
        rotation_start = (combination_id * 2) % len(all_stars)
        stars = [all_stars[rotation_start], all_stars[(rotation_start + 1) % len(all_stars)]]
    
    return sorted(stars)

def generate_8_euromillions_combinations():
    """Generate 8 Euromillions combinations using proven strategies"""
    
    print("GENERATING 8 EUROMILLIONS COMBINATIONS FOR JULY 11, 2025")
    print("=" * 53)
    
    # Get data
    latest_results, training_results = get_latest_euromillions_data()
    recent_patterns = analyze_recent_euromillions_patterns(latest_results)
    historical_data = get_euromillions_historical_data(training_results)
    
    print("\nEUROMILLIONS STRATEGIC APPROACH:")
    print("-" * 32)
    print("Numbers: 8 different proven strategies")
    print("Stars: Different strategy per combination (Euromillions mixed principle)")
    print()
    
    # Generate number strategies
    number_strategies = generate_euromillions_number_strategies(historical_data, recent_patterns)
    
    # Generate complete combinations
    combinations = []
    
    for i, num_strategy in enumerate(number_strategies):
        combination_id = i + 1
        star_numbers = generate_euromillions_star_strategies(historical_data, recent_patterns, combination_id)
        
        # Star strategy names
        star_strategy_names = [
            'Frequency Dominant Stars',
            'Recent Hot Focus Stars',
            'Balanced Mix Stars',
            'Contrarian Rare Stars',
            'Mathematical Range Stars',
            'Weighted Balance Stars',
            'Gap Analysis Stars',
            'Strategic Rotation Stars'
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

def generate_2_fusion_combinations(main_combinations):
    """Generate 2 fusion combinations from the 8 main combinations"""
    
    print("\nGENERATING 2 FUSION COMBINATIONS")
    print("=" * 29)
    
    all_numbers = []
    all_stars = []
    
    for combo in main_combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    # Fusion 1: Proven Strategy Weighted Blend
    # Emphasize the proven strategies (Coverage Optimization and Enhanced Risk-Reward)
    strategy_weights = [0.25, 0.25, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05]  # Emphasize combinations 1&2
    
    weighted_numbers = []
    weighted_stars = []
    
    for i, combo in enumerate(main_combinations):
        weight = strategy_weights[i]
        num_numbers = max(1, int(8 * weight))
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
        'strategy': 'Proven Strategy Weighted Blend',
        'focus': 'Weighted blend emphasizing June 3 & June 20 winning strategies'
    }
    
    # Fusion 2: Mathematical Average Fusion
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Most common numbers and stars from all combinations
    most_common_numbers = [n for n, _ in number_freq.most_common(10)]
    fusion2_numbers = sorted(random.sample(most_common_numbers, 5))
    
    most_common_stars = [s for s, _ in star_freq.most_common(4)]
    fusion2_stars = sorted(random.sample(most_common_stars, 2))
    
    fusion2 = {
        'id': 'F2',
        'numbers': fusion2_numbers,
        'stars': fusion2_stars,
        'strategy': 'Mathematical Average Fusion',
        'focus': 'Frequency-weighted fusion of all 8 combinations'
    }
    
    return [fusion1, fusion2]

def display_complete_euromillions_set(main_combinations, fusion_combinations):
    """Display the complete Euromillions set"""
    
    print("\nCOMPLETE EUROMILLIONS SET FOR JULY 11, 2025")
    print("=" * 39)
    
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
    """Main function to generate Euromillions combinations"""
    
    # Generate 8 main combinations
    main_combinations = generate_8_euromillions_combinations()
    
    # Generate 2 fusion combinations
    fusion_combinations = generate_2_fusion_combinations(main_combinations)
    
    # Display complete set
    main_combinations, fusion_combinations = display_complete_euromillions_set(main_combinations, fusion_combinations)
    
    print("\nEUROMILLIONS STRATEGY PRINCIPLES:")
    print("-" * 33)
    print("✓ Using proven June 3 and June 20 winning strategies")
    print("✓ Incorporating latest July draw patterns")
    print("✓ Mixed star strategies per combination (Euromillions principle)")
    print("✓ 2000 historical draws statistical foundation")
    print("✓ Enhanced fusion methodology")
    print("✓ Comprehensive coverage optimization")

if __name__ == "__main__":
    main()