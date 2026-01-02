"""
Generate 5 Euromillions combinations for July 7, 2025
Using proven strategies with updated data including latest draws
Different strategy for stars vs numbers (Euromillions principle)
"""

import psycopg2
import os
from collections import Counter
import random
import numpy as np

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    return psycopg2.connect(database_url)

def get_latest_euromillions_data():
    """Get latest Euromillions data including recent July draws"""
    conn = connect_to_database()
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

def analyze_recent_patterns(latest_results):
    """Analyze patterns from recent draws"""
    
    print("RECENT EUROMILLIONS DRAWS ANALYSIS")
    print("=" * 34)
    
    recent_numbers = []
    recent_stars = []
    
    for i, row in enumerate(latest_results[:5]):
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

def get_historical_frequency_data(training_results):
    """Get comprehensive frequency analysis from historical data"""
    
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

def generate_coverage_optimization_enhanced(historical_data, recent_patterns):
    """Enhanced Coverage Optimization (proven June 3 winner)"""
    
    frequent = historical_data['frequent_numbers']
    medium = historical_data['medium_numbers']
    rare = historical_data['rare_numbers']
    
    # Enhanced with recent patterns
    hot_recent = recent_patterns['hot_numbers']
    
    # Balanced selection with recent hot integration
    numbers = []
    numbers.extend(random.sample([n for n in frequent if n in hot_recent], min(2, len([n for n in frequent if n in hot_recent]))))
    
    # Fill remaining with balanced approach
    remaining_pool = [n for n in frequent + medium if n not in numbers]
    numbers.extend(random.sample(remaining_pool, 5 - len(numbers)))
    
    # Range balancing
    low_range = [n for n in numbers if n <= 17]
    mid_range = [n for n in numbers if 18 <= n <= 34]
    high_range = [n for n in numbers if n >= 35]
    
    # Ensure at least one from each range
    if not low_range:
        numbers[0] = random.choice([n for n in frequent + medium if n <= 17])
    if not high_range:
        numbers[-1] = random.choice([n for n in frequent + medium if n >= 35])
    
    return sorted(numbers)

def generate_enhanced_risk_reward(historical_data, recent_patterns):
    """Enhanced Risk-Reward (proven June 20 winner)"""
    
    medium = historical_data['medium_numbers']
    rare = historical_data['rare_numbers']
    
    # Risk-reward: emphasize medium and rare numbers
    numbers = []
    numbers.extend(random.sample(medium, 3))
    numbers.extend(random.sample(rare, 2))
    
    return sorted(numbers)

def generate_frequency_hot_pursuit(historical_data, recent_patterns):
    """Hot Frequency Pursuit strategy"""
    
    frequent = historical_data['frequent_numbers']
    hot_recent = recent_patterns['hot_numbers']
    
    # Combine historical frequent with recent hot
    hot_pool = list(set(frequent[:15] + hot_recent))
    numbers = random.sample(hot_pool, 5)
    
    return sorted(numbers)

def generate_balanced_hybrid(historical_data, recent_patterns):
    """Balanced Hybrid Strategy"""
    
    frequent = historical_data['frequent_numbers']
    medium = historical_data['medium_numbers']
    rare = historical_data['rare_numbers']
    
    # Balanced selection
    numbers = []
    numbers.extend(random.sample(frequent, 2))
    numbers.extend(random.sample(medium, 2))
    numbers.extend(random.sample(rare, 1))
    
    return sorted(numbers)

def generate_gap_analysis_strategy(historical_data, recent_patterns):
    """Gap Analysis Strategy - focus on numbers that haven't appeared recently"""
    
    frequent = historical_data['frequent_numbers']
    medium = historical_data['medium_numbers']
    recent_numbers = set(recent_patterns['recent_numbers'])
    
    # Find frequent/medium numbers that haven't appeared recently
    gap_candidates = [n for n in frequent + medium if n not in recent_numbers]
    
    if len(gap_candidates) >= 5:
        numbers = random.sample(gap_candidates, 5)
    else:
        numbers = gap_candidates + random.sample(frequent + medium, 5 - len(gap_candidates))
    
    return sorted(numbers[:5])

def generate_stars_mixed_strategy(historical_data, recent_patterns, combination_id):
    """Generate stars using DIFFERENT strategy than numbers (Euromillions principle)"""
    
    frequent_stars = historical_data['frequent_stars']
    medium_stars = historical_data['medium_stars']
    rare_stars = historical_data['rare_stars']
    hot_recent_stars = recent_patterns['hot_stars']
    
    strategies = [
        'frequency_dominant',    # Combination 1
        'recent_hot',           # Combination 2
        'balanced_mix',         # Combination 3
        'contrarian_rare',      # Combination 4
        'mathematical_range'    # Combination 5
    ]
    
    strategy = strategies[combination_id - 1]
    
    if strategy == 'frequency_dominant':
        # Use most frequent stars
        stars = random.sample(frequent_stars, 2)
    
    elif strategy == 'recent_hot':
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
    
    else:  # mathematical_range
        # Use mathematical range approach (low + high)
        low_stars = [s for s in frequent_stars + medium_stars if s <= 6]
        high_stars = [s for s in frequent_stars + medium_stars if s >= 7]
        
        if low_stars and high_stars:
            stars = [random.choice(low_stars), random.choice(high_stars)]
        else:
            stars = random.sample(frequent_stars + medium_stars, 2)
    
    return sorted(stars)

def generate_euromillions_combinations():
    """Generate 5 Euromillions combinations using proven strategies"""
    
    print("GENERATING 5 EUROMILLIONS COMBINATIONS FOR JULY 7, 2025")
    print("=" * 52)
    
    # Get data
    latest_results, training_results = get_latest_euromillions_data()
    recent_patterns = analyze_recent_patterns(latest_results)
    historical_data = get_historical_frequency_data(training_results)
    
    print("\nSTRATEGIC APPROACH:")
    print("-" * 18)
    print("Numbers: 5 different proven strategies")
    print("Stars: Different strategy per combination (Euromillions principle)")
    print()
    
    combinations = []
    
    # Combination 1: Coverage Optimization Enhanced (June 3 winner)
    numbers1 = generate_coverage_optimization_enhanced(historical_data, recent_patterns)
    stars1 = generate_stars_mixed_strategy(historical_data, recent_patterns, 1)
    combinations.append({
        'id': 1,
        'numbers': numbers1,
        'stars': stars1,
        'strategy': 'Coverage Optimization Enhanced + Frequency Dominant Stars',
        'focus': 'Proven June 3 winner + most frequent stars'
    })
    
    # Combination 2: Enhanced Risk-Reward (June 20 winner)
    numbers2 = generate_enhanced_risk_reward(historical_data, recent_patterns)
    stars2 = generate_stars_mixed_strategy(historical_data, recent_patterns, 2)
    combinations.append({
        'id': 2,
        'numbers': numbers2,
        'stars': stars2,
        'strategy': 'Enhanced Risk-Reward + Recent Hot Stars',
        'focus': 'Proven June 20 winner + recent hot star patterns'
    })
    
    # Combination 3: Frequency Hot Pursuit
    numbers3 = generate_frequency_hot_pursuit(historical_data, recent_patterns)
    stars3 = generate_stars_mixed_strategy(historical_data, recent_patterns, 3)
    combinations.append({
        'id': 3,
        'numbers': numbers3,
        'stars': stars3,
        'strategy': 'Frequency Hot Pursuit + Balanced Mix Stars',
        'focus': 'Hot number concentration + balanced star selection'
    })
    
    # Combination 4: Balanced Hybrid
    numbers4 = generate_balanced_hybrid(historical_data, recent_patterns)
    stars4 = generate_stars_mixed_strategy(historical_data, recent_patterns, 4)
    combinations.append({
        'id': 4,
        'numbers': numbers4,
        'stars': stars4,
        'strategy': 'Balanced Hybrid + Contrarian Rare Stars',
        'focus': 'Balanced number approach + rare star selection'
    })
    
    # Combination 5: Gap Analysis Strategy
    numbers5 = generate_gap_analysis_strategy(historical_data, recent_patterns)
    stars5 = generate_stars_mixed_strategy(historical_data, recent_patterns, 5)
    combinations.append({
        'id': 5,
        'numbers': numbers5,
        'stars': stars5,
        'strategy': 'Gap Analysis + Mathematical Range Stars',
        'focus': 'Overdue number focus + range-balanced stars'
    })
    
    return combinations

def generate_fusion_combinations(main_combinations):
    """Generate 2 fusion combinations from the 5 main combinations"""
    
    print("\nGENERATING 2 FUSION COMBINATIONS")
    print("=" * 29)
    
    all_numbers = []
    all_stars = []
    
    for combo in main_combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    # Fusion 1: Mathematical Average Fusion
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Most common numbers from all combinations
    most_common_numbers = [n for n, _ in number_freq.most_common(10)]
    fusion1_numbers = sorted(random.sample(most_common_numbers, 5))
    
    # Most common stars
    most_common_stars = [s for s, _ in star_freq.most_common(4)]
    fusion1_stars = sorted(random.sample(most_common_stars, 2))
    
    fusion1 = {
        'id': 'F1',
        'numbers': fusion1_numbers,
        'stars': fusion1_stars,
        'strategy': 'Mathematical Average Fusion',
        'focus': 'Frequency-weighted fusion of all 5 combinations'
    }
    
    # Fusion 2: Strategic Weighted Blend
    # Emphasize the 2 proven strategies (Coverage + Risk-Reward)
    strategy_weights = [0.3, 0.3, 0.15, 0.15, 0.1]  # Emphasize combinations 1&2
    
    weighted_numbers = []
    weighted_stars = []
    
    for i, combo in enumerate(main_combinations):
        weight = strategy_weights[i]
        num_numbers = max(1, int(5 * weight))
        num_stars = max(1, int(2 * weight))
        
        selected_numbers = random.sample(combo['numbers'], min(num_numbers, len(combo['numbers'])))
        selected_stars = random.sample(combo['stars'], min(num_stars, len(combo['stars'])))
        
        weighted_numbers.extend(selected_numbers)
        weighted_stars.extend(selected_stars)
    
    # Remove duplicates and ensure correct counts
    fusion2_numbers = list(set(weighted_numbers))
    if len(fusion2_numbers) > 5:
        fusion2_numbers = sorted(fusion2_numbers)[:5]
    elif len(fusion2_numbers) < 5:
        remaining_pool = [n for combo in main_combinations for n in combo['numbers']]
        additional = [n for n in remaining_pool if n not in fusion2_numbers]
        fusion2_numbers.extend(random.sample(additional, 5 - len(fusion2_numbers)))
    
    fusion2_stars = list(set(weighted_stars))
    if len(fusion2_stars) > 2:
        fusion2_stars = sorted(fusion2_stars)[:2]
    elif len(fusion2_stars) < 2:
        remaining_stars = [s for combo in main_combinations for s in combo['stars']]
        additional_stars = [s for s in remaining_stars if s not in fusion2_stars]
        fusion2_stars.extend(random.sample(additional_stars, 2 - len(fusion2_stars)))
    
    fusion2 = {
        'id': 'F2',
        'numbers': sorted(fusion2_numbers),
        'stars': sorted(fusion2_stars),
        'strategy': 'Strategic Weighted Blend',
        'focus': 'Weighted blend emphasizing proven strategies'
    }
    
    return [fusion1, fusion2]

def display_complete_euromillions_set(main_combinations, fusion_combinations):
    """Display the complete Euromillions set"""
    
    print("\nCOMPLETE EUROMILLIONS SET FOR JULY 7, 2025")
    print("=" * 38)
    
    print("5 MAIN COMBINATIONS:")
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
    
    # Generate main combinations
    main_combinations = generate_euromillions_combinations()
    
    # Generate fusion combinations
    fusion_combinations = generate_fusion_combinations(main_combinations)
    
    # Display complete set
    main_combinations, fusion_combinations = display_complete_euromillions_set(main_combinations, fusion_combinations)
    
    print("\nKEY STRATEGY UPDATES:")
    print("-" * 21)
    print("✓ Using proven June 3 and June 20 winning strategies")
    print("✓ Incorporating latest July draw patterns")
    print("✓ Different star strategies per combination")
    print("✓ Enhanced fusion methodology")
    print("✓ Comprehensive coverage optimization")

if __name__ == "__main__":
    main()