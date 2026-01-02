"""
Generate 8 French Loto combinations for July 7, 2025
Using proper French Loto strategy: DIFFERENT methods for numbers vs lucky numbers
Then generate 3 fusion combinations from the 8 main combinations
"""

import psycopg2
import os
from collections import Counter
import random
import numpy as np

def get_latest_french_loto_data():
    """Get latest French Loto draws and comprehensive training data"""
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get latest draws
    latest_query = """
    SELECT date, n1, n2, n3, n4, n5, lucky 
    FROM french_loto_drawings 
    ORDER BY date DESC
    LIMIT 10
    """
    
    cursor.execute(latest_query)
    latest_results = cursor.fetchall()
    
    # Get comprehensive training data
    training_query = """
    SELECT date, n1, n2, n3, n4, n5, lucky 
    FROM french_loto_drawings 
    ORDER BY date DESC
    LIMIT 2000
    """
    
    cursor.execute(training_query)
    training_results = cursor.fetchall()
    conn.close()
    
    return latest_results, training_results

def analyze_recent_french_loto_patterns(latest_results):
    """Analyze recent French Loto patterns"""
    
    print("RECENT FRENCH LOTO DRAWS ANALYSIS")
    print("=" * 33)
    
    recent_numbers = []
    recent_lucky = []
    
    for i, row in enumerate(latest_results[:6]):
        date, n1, n2, n3, n4, n5, lucky = row
        numbers = [n1, n2, n3, n4, n5]
        recent_numbers.extend(numbers)
        recent_lucky.append(lucky)
        
        print(f"{date}: {numbers} / {lucky}")
    
    print()
    print("PATTERN INSIGHTS:")
    
    # Number patterns
    number_freq = Counter(recent_numbers)
    most_common_numbers = number_freq.most_common(10)
    print(f"Hot numbers (recent): {[n for n, _ in most_common_numbers[:8]]}")
    
    # Lucky patterns
    lucky_freq = Counter(recent_lucky)
    most_common_lucky = lucky_freq.most_common(5)
    print(f"Hot lucky numbers (recent): {[l for l, _ in most_common_lucky[:5]]}")
    
    # Range analysis
    low_range = [n for n in recent_numbers if n <= 16]
    mid_range = [n for n in recent_numbers if 17 <= n <= 33]
    high_range = [n for n in recent_numbers if n >= 34]
    
    print(f"Range distribution: Low(1-16): {len(low_range)}, Mid(17-33): {len(mid_range)}, High(34-49): {len(high_range)}")
    
    return {
        'recent_numbers': recent_numbers,
        'recent_lucky': recent_lucky,
        'hot_numbers': [n for n, _ in most_common_numbers[:8]],
        'hot_lucky': [l for l, _ in most_common_lucky[:5]],
        'number_freq': number_freq,
        'lucky_freq': lucky_freq
    }

def get_french_loto_historical_data(training_results):
    """Get comprehensive French Loto historical frequency analysis"""
    
    all_numbers = []
    all_lucky = []
    
    for row in training_results:
        _, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_lucky.append(lucky)
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    # Categorize by frequency
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_lucky = sorted(lucky_freq.items(), key=lambda x: x[1], reverse=True)
    
    total_numbers = len(sorted_numbers)
    total_lucky = len(sorted_lucky)
    
    frequent_numbers = [n for n, _ in sorted_numbers[:total_numbers//3]]
    medium_numbers = [n for n, _ in sorted_numbers[total_numbers//3:2*total_numbers//3]]
    rare_numbers = [n for n, _ in sorted_numbers[2*total_numbers//3:]]
    
    frequent_lucky = [l for l, _ in sorted_lucky[:total_lucky//3]]
    medium_lucky = [l for l, _ in sorted_lucky[total_lucky//3:2*total_lucky//3]]
    rare_lucky = [l for l, _ in sorted_lucky[2*total_lucky//3:]]
    
    return {
        'number_freq': number_freq,
        'lucky_freq': lucky_freq,
        'frequent_numbers': frequent_numbers,
        'medium_numbers': medium_numbers,
        'rare_numbers': rare_numbers,
        'frequent_lucky': frequent_lucky,
        'medium_lucky': medium_lucky,
        'rare_lucky': rare_lucky
    }

def generate_french_loto_number_strategies(historical_data, recent_patterns):
    """Generate 8 different number strategies for French Loto"""
    
    frequent = historical_data['frequent_numbers']
    medium = historical_data['medium_numbers']
    rare = historical_data['rare_numbers']
    hot_recent = recent_patterns['hot_numbers']
    
    strategies = []
    
    # Strategy 1: Enhanced Coverage Optimization
    numbers1 = []
    low_range = [n for n in frequent + medium if n <= 16]
    mid_range = [n for n in frequent + medium if 17 <= n <= 33]
    high_range = [n for n in frequent + medium if n >= 34]
    
    numbers1.extend(random.sample(low_range, 2))
    numbers1.extend(random.sample(mid_range, 2))
    numbers1.extend(random.sample(high_range, 1))
    
    strategies.append({
        'numbers': sorted(numbers1),
        'strategy': 'Enhanced Coverage Optimization',
        'focus': 'Balanced range distribution'
    })
    
    # Strategy 2: Frequency Analysis Enhanced
    numbers2 = random.sample(frequent[:15], 5)
    strategies.append({
        'numbers': sorted(numbers2),
        'strategy': 'Frequency Analysis Enhanced',
        'focus': 'Hot number concentration'
    })
    
    # Strategy 3: Risk-Reward Refined
    numbers3 = []
    numbers3.extend(random.sample(medium, 3))
    numbers3.extend(random.sample(rare, 2))
    strategies.append({
        'numbers': sorted(numbers3),
        'strategy': 'Risk-Reward Refined',
        'focus': 'Cold number emphasis'
    })
    
    # Strategy 4: Recent Pattern Integration
    numbers4 = []
    recent_integration = random.sample(hot_recent, min(3, len(hot_recent)))
    remaining_pool = [n for n in frequent + medium if n not in recent_integration]
    numbers4.extend(recent_integration)
    numbers4.extend(random.sample(remaining_pool, 5 - len(recent_integration)))
    strategies.append({
        'numbers': sorted(numbers4),
        'strategy': 'Recent Pattern Integration',
        'focus': 'Recent hot numbers + historical balance'
    })
    
    # Strategy 5: Mathematical Balance
    numbers5 = []
    target_sum_range = (120, 160)
    attempts = 0
    while attempts < 50:
        temp_numbers = []
        temp_numbers.extend(random.sample(frequent, 2))
        temp_numbers.extend(random.sample(medium, 2))
        temp_numbers.extend(random.sample(rare, 1))
        
        if target_sum_range[0] <= sum(temp_numbers) <= target_sum_range[1]:
            numbers5 = temp_numbers
            break
        attempts += 1
    
    if not numbers5:
        numbers5 = random.sample(frequent + medium, 5)
    
    strategies.append({
        'numbers': sorted(numbers5),
        'strategy': 'Mathematical Balance',
        'focus': 'Sum-optimized selection'
    })
    
    # Strategy 6: Gap Analysis
    recent_numbers = set(recent_patterns['recent_numbers'])
    gap_candidates = [n for n in frequent + medium if n not in recent_numbers]
    numbers6 = random.sample(gap_candidates, min(5, len(gap_candidates)))
    if len(numbers6) < 5:
        numbers6.extend(random.sample(frequent + medium, 5 - len(numbers6)))
    
    strategies.append({
        'numbers': sorted(numbers6),
        'strategy': 'Gap Analysis',
        'focus': 'Overdue number focus'
    })
    
    # Strategy 7: Hybrid Balanced
    numbers7 = []
    numbers7.extend(random.sample(frequent, 2))
    numbers7.extend(random.sample(medium, 2))
    numbers7.extend(random.sample(rare, 1))
    strategies.append({
        'numbers': sorted(numbers7),
        'strategy': 'Hybrid Balanced',
        'focus': 'Balanced frequency distribution'
    })
    
    # Strategy 8: Enhanced Range Focus
    numbers8 = []
    # Focus on mid-range numbers with some low/high
    mid_heavy = [n for n in frequent + medium if 17 <= n <= 33]
    numbers8.extend(random.sample(mid_heavy, 3))
    
    low_high = [n for n in frequent + medium if n <= 16 or n >= 34]
    numbers8.extend(random.sample(low_high, 2))
    
    strategies.append({
        'numbers': sorted(numbers8),
        'strategy': 'Enhanced Range Focus',
        'focus': 'Mid-range emphasis with balance'
    })
    
    return strategies

def generate_french_loto_lucky_strategies(historical_data, recent_patterns, combination_id):
    """Generate lucky number using DIFFERENT strategy than numbers (French Loto principle)"""
    
    frequent_lucky = historical_data['frequent_lucky']
    medium_lucky = historical_data['medium_lucky']
    rare_lucky = historical_data['rare_lucky']
    hot_recent_lucky = recent_patterns['hot_lucky']
    
    lucky_strategies = [
        'frequency_opposite',      # Combo 1: Opposite of frequency approach
        'pure_frequency',          # Combo 2: Pure frequency (different from enhanced)
        'contrarian_rare',         # Combo 3: Contrarian to risk-reward
        'recent_hot_complement',   # Combo 4: Complement to recent pattern
        'mathematical_pattern',    # Combo 5: Mathematical pattern (different from balance)
        'balanced_medium',         # Combo 6: Balanced approach (different from gap)
        'range_complement',        # Combo 7: Range complement (different from hybrid)
        'strategic_rotation'       # Combo 8: Strategic rotation approach
    ]
    
    strategy = lucky_strategies[combination_id - 1]
    
    if strategy == 'frequency_opposite':
        # Use rare/medium lucky (opposite of frequency)
        candidates = rare_lucky + medium_lucky
        return random.choice(candidates) if candidates else random.choice(frequent_lucky)
    
    elif strategy == 'pure_frequency':
        # Use most frequent lucky
        return frequent_lucky[0] if frequent_lucky else 1
    
    elif strategy == 'contrarian_rare':
        # Use least frequent lucky
        return random.choice(rare_lucky) if rare_lucky else random.choice(medium_lucky)
    
    elif strategy == 'recent_hot_complement':
        # Use hot recent if available, otherwise complement
        if hot_recent_lucky:
            return random.choice(hot_recent_lucky)
        else:
            return random.choice(frequent_lucky + medium_lucky)
    
    elif strategy == 'mathematical_pattern':
        # Use mathematical pattern (different from number sum)
        pattern_lucky = ((combination_id * 3) % 10) + 1
        if pattern_lucky > 10:
            pattern_lucky = pattern_lucky - 10
        return pattern_lucky
    
    elif strategy == 'balanced_medium':
        # Use medium frequency lucky
        return random.choice(medium_lucky) if medium_lucky else random.choice(frequent_lucky)
    
    elif strategy == 'range_complement':
        # Use range complement approach
        if combination_id <= 4:
            # Low ID: use higher lucky numbers
            high_lucky = [l for l in frequent_lucky + medium_lucky if l >= 6]
            return random.choice(high_lucky) if high_lucky else random.choice(frequent_lucky)
        else:
            # High ID: use lower lucky numbers
            low_lucky = [l for l in frequent_lucky + medium_lucky if l <= 5]
            return random.choice(low_lucky) if low_lucky else random.choice(frequent_lucky)
    
    else:  # strategic_rotation
        # Rotate through different approaches
        rotation_options = frequent_lucky + medium_lucky + rare_lucky
        return rotation_options[combination_id % len(rotation_options)] if rotation_options else 1

def generate_8_french_loto_combinations():
    """Generate 8 French Loto combinations using different strategies"""
    
    print("GENERATING 8 FRENCH LOTO COMBINATIONS FOR JULY 7, 2025")
    print("=" * 51)
    
    # Get data
    latest_results, training_results = get_latest_french_loto_data()
    recent_patterns = analyze_recent_french_loto_patterns(latest_results)
    historical_data = get_french_loto_historical_data(training_results)
    
    print("\nFRENCH LOTO STRATEGIC APPROACH:")
    print("-" * 31)
    print("Numbers: 8 different proven strategies")
    print("Lucky: DIFFERENT strategy per combination (French Loto principle)")
    print()
    
    # Generate number strategies
    number_strategies = generate_french_loto_number_strategies(historical_data, recent_patterns)
    
    # Generate complete combinations
    combinations = []
    
    for i, num_strategy in enumerate(number_strategies):
        combination_id = i + 1
        lucky_number = generate_french_loto_lucky_strategies(historical_data, recent_patterns, combination_id)
        
        # Lucky strategy names
        lucky_strategy_names = [
            'Frequency Opposite Lucky',
            'Pure Frequency Lucky',
            'Contrarian Rare Lucky',
            'Recent Hot Complement Lucky',
            'Mathematical Pattern Lucky',
            'Balanced Medium Lucky',
            'Range Complement Lucky',
            'Strategic Rotation Lucky'
        ]
        
        combination = {
            'id': combination_id,
            'numbers': num_strategy['numbers'],
            'lucky': lucky_number,
            'strategy': f"{num_strategy['strategy']} + {lucky_strategy_names[i]}",
            'focus': f"{num_strategy['focus']} + {lucky_strategy_names[i].lower()}",
            'number_strategy': num_strategy['strategy'],
            'lucky_strategy': lucky_strategy_names[i]
        }
        
        combinations.append(combination)
    
    return combinations

def generate_3_fusion_combinations(main_combinations):
    """Generate 3 fusion combinations from the 8 main combinations"""
    
    print("\nGENERATING 3 FUSION COMBINATIONS")
    print("=" * 29)
    
    all_numbers = []
    all_lucky = []
    
    for combo in main_combinations:
        all_numbers.extend(combo['numbers'])
        all_lucky.append(combo['lucky'])
    
    # Fusion 1: Mathematical Average Fusion
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    most_common_numbers = [n for n, _ in number_freq.most_common(12)]
    fusion1_numbers = sorted(random.sample(most_common_numbers, 5))
    
    fusion1_lucky = lucky_freq.most_common(1)[0][0]
    
    fusion1 = {
        'id': 'F1',
        'numbers': fusion1_numbers,
        'lucky': fusion1_lucky,
        'strategy': 'Mathematical Average Fusion',
        'focus': 'Frequency-weighted fusion of all 8 combinations'
    }
    
    # Fusion 2: Strategic Weighted Blend (emphasize proven strategies)
    # Emphasize strategies 1, 2, 4 (Coverage, Frequency, Recent Pattern)
    strategy_weights = [0.2, 0.2, 0.1, 0.2, 0.1, 0.1, 0.05, 0.05]
    
    weighted_numbers = []
    weighted_lucky = []
    
    for i, combo in enumerate(main_combinations):
        weight = strategy_weights[i]
        num_numbers = max(1, int(8 * weight))
        
        selected_numbers = random.sample(combo['numbers'], min(num_numbers, len(combo['numbers'])))
        weighted_numbers.extend(selected_numbers)
        weighted_lucky.append(combo['lucky'])
    
    fusion2_numbers = list(set(weighted_numbers))
    if len(fusion2_numbers) > 5:
        fusion2_numbers = sorted(fusion2_numbers)[:5]
    elif len(fusion2_numbers) < 5:
        remaining_pool = [n for combo in main_combinations for n in combo['numbers']]
        additional = [n for n in remaining_pool if n not in fusion2_numbers]
        fusion2_numbers.extend(random.sample(additional, 5 - len(fusion2_numbers)))
    
    fusion2_lucky = Counter(weighted_lucky).most_common(1)[0][0]
    
    fusion2 = {
        'id': 'F2',
        'numbers': sorted(fusion2_numbers),
        'lucky': fusion2_lucky,
        'strategy': 'Strategic Weighted Blend',
        'focus': 'Weighted blend emphasizing proven strategies'
    }
    
    # Fusion 3: Balanced Synthesis
    # Create balanced fusion using middle-performing strategies
    mid_strategies = main_combinations[2:6]  # Strategies 3-6
    
    synthesis_numbers = []
    synthesis_lucky = []
    
    for combo in mid_strategies:
        synthesis_numbers.extend(combo['numbers'])
        synthesis_lucky.append(combo['lucky'])
    
    # Remove duplicates and select best
    synthesis_freq = Counter(synthesis_numbers)
    fusion3_numbers = sorted([n for n, _ in synthesis_freq.most_common(5)])
    
    fusion3_lucky = Counter(synthesis_lucky).most_common(1)[0][0]
    
    fusion3 = {
        'id': 'F3',
        'numbers': fusion3_numbers,
        'lucky': fusion3_lucky,
        'strategy': 'Balanced Synthesis',
        'focus': 'Balanced fusion from mid-tier strategies'
    }
    
    return [fusion1, fusion2, fusion3]

def display_complete_french_loto_set(main_combinations, fusion_combinations):
    """Display the complete French Loto set"""
    
    print("\nCOMPLETE FRENCH LOTO SET FOR JULY 7, 2025")
    print("=" * 37)
    
    print("8 MAIN COMBINATIONS:")
    print("-" * 19)
    for combo in main_combinations:
        print(f"{combo['id']}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} + Lucky: {combo['lucky']}")
        print(f"   Focus: {combo['focus']}")
        print()
    
    print("3 FUSION COMBINATIONS:")
    print("-" * 21)
    for fusion in fusion_combinations:
        print(f"{fusion['id']}. {fusion['strategy']}")
        print(f"   Numbers: {fusion['numbers']} + Lucky: {fusion['lucky']}")
        print(f"   Focus: {fusion['focus']}")
        print()
    
    # Coverage analysis
    all_numbers = set()
    all_lucky = set()
    
    for combo in main_combinations + fusion_combinations:
        all_numbers.update(combo['numbers'])
        all_lucky.add(combo['lucky'])
    
    print("COVERAGE ANALYSIS:")
    print("-" * 17)
    print(f"Total unique numbers: {len(all_numbers)}/49")
    print(f"Total unique lucky: {len(all_lucky)}/10")
    print(f"Lucky numbers used: {sorted(all_lucky)}")
    
    return main_combinations, fusion_combinations

def main():
    """Main function to generate French Loto combinations"""
    
    # Generate 8 main combinations
    main_combinations = generate_8_french_loto_combinations()
    
    # Generate 3 fusion combinations
    fusion_combinations = generate_3_fusion_combinations(main_combinations)
    
    # Display complete set
    main_combinations, fusion_combinations = display_complete_french_loto_set(main_combinations, fusion_combinations)
    
    print("\nFRENCH LOTO STRATEGY PRINCIPLES:")
    print("-" * 32)
    print("✓ 8 different number strategies applied")
    print("✓ Different lucky strategy per combination")
    print("✓ Proper French Loto methodology maintained")
    print("✓ 3 fusion combinations with different approaches")
    print("✓ Comprehensive coverage optimization")

if __name__ == "__main__":
    main()