"""
Generate 10 optimized Euromillions combinations based on backtesting results
Primary: Markov Chain (1.860 avg) + Coverage Optimization (1.750 avg) + Risk-Reward (1.710 avg)
"""

import psycopg2
import os
from collections import Counter, defaultdict
import random

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    else:
        raise Exception("No database connection available")

def get_recent_euromillions_data(limit=200):
    """Get recent Euromillions data for strategy generation"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = """
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC 
    LIMIT %s
    """
    
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    
    conn.close()
    return results

def build_markov_transition_matrix(historical_data):
    """Build Markov chain transition matrix from historical data"""
    
    number_transitions = defaultdict(Counter)
    star_transitions = defaultdict(Counter)
    
    for row in historical_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        numbers = sorted([n1, n2, n3, n4, n5])
        stars = sorted([s1, s2])
        
        # Build number transitions
        for i in range(len(numbers) - 1):
            current = numbers[i]
            next_num = numbers[i + 1]
            number_transitions[current][next_num] += 1
        
        # Build star transitions
        if len(stars) > 1:
            star_transitions[stars[0]][stars[1]] += 1
    
    return number_transitions, star_transitions

def generate_markov_chain_combination(number_transitions, star_transitions, all_numbers, all_stars, variation=0):
    """Generate a single combination using Markov chain analysis"""
    
    # Start with a frequent number based on variation
    number_freq = Counter(all_numbers)
    start_candidates = [n for n, freq in number_freq.most_common(20)]
    start_num = start_candidates[variation % len(start_candidates)]
    
    combo_numbers = [start_num]
    
    # Use Markov chain to generate sequence
    current = start_num
    attempts = 0
    max_attempts = 50
    
    while len(combo_numbers) < 5 and attempts < max_attempts:
        attempts += 1
        
        if current in number_transitions and number_transitions[current]:
            # Get weighted next candidates
            next_options = number_transitions[current]
            candidates = [num for num in next_options.keys() if num not in combo_numbers]
            
            if candidates:
                # Weight by frequency in transitions
                weights = [next_options[num] for num in candidates]
                # Use weighted random selection
                if weights:
                    next_num = random.choices(candidates, weights=weights)[0]
                    combo_numbers.append(next_num)
                    current = next_num
                else:
                    # Fallback to frequent numbers
                    remaining = [n for n in start_candidates if n not in combo_numbers]
                    if remaining:
                        next_num = random.choice(remaining)
                        combo_numbers.append(next_num)
                        current = next_num
            else:
                # No valid transitions, pick from frequent numbers
                remaining = [n for n in start_candidates if n not in combo_numbers]
                if remaining:
                    next_num = random.choice(remaining)
                    combo_numbers.append(next_num)
                    current = next_num
        else:
            # No transitions for current number, pick from frequent
            remaining = [n for n in start_candidates if n not in combo_numbers]
            if remaining:
                next_num = random.choice(remaining)
                combo_numbers.append(next_num)
                current = next_num
    
    # Fill remaining slots if needed
    while len(combo_numbers) < 5:
        remaining = [n for n in range(1, 50) if n not in combo_numbers]
        if remaining:
            combo_numbers.append(random.choice(remaining))
        else:
            break
    
    # Generate stars using Markov transitions and frequency
    star_freq = Counter(all_stars)
    frequent_stars = [s for s, freq in star_freq.most_common(8)]
    
    combo_stars = []
    if frequent_stars:
        first_star = frequent_stars[variation % len(frequent_stars)]
        combo_stars.append(first_star)
        
        # Try to use Markov transition for second star
        if first_star in star_transitions and star_transitions[first_star]:
            second_options = [s for s in star_transitions[first_star].keys() if s != first_star]
            if second_options:
                weights = [star_transitions[first_star][s] for s in second_options]
                second_star = random.choices(second_options, weights=weights)[0]
                combo_stars.append(second_star)
            else:
                # Fallback to frequent star
                remaining_stars = [s for s in frequent_stars if s != first_star]
                if remaining_stars:
                    combo_stars.append(random.choice(remaining_stars))
        else:
            # No transition, use frequent star
            remaining_stars = [s for s in frequent_stars if s != first_star]
            if remaining_stars:
                combo_stars.append(random.choice(remaining_stars))
    
    # Ensure we have 2 stars
    while len(combo_stars) < 2:
        remaining_stars = [s for s in range(1, 13) if s not in combo_stars]
        if remaining_stars:
            combo_stars.append(random.choice(remaining_stars))
        else:
            break
    
    return sorted(combo_numbers[:5]), sorted(combo_stars[:2])

def generate_coverage_optimization_combination(all_numbers, all_stars, pattern_idx):
    """Generate combination using coverage optimization"""
    
    # Analyze range distributions
    low_numbers = [n for n in all_numbers if 1 <= n <= 16]
    mid_numbers = [n for n in all_numbers if 17 <= n <= 33]
    high_numbers = [n for n in all_numbers if 34 <= n <= 49]
    
    low_freq = Counter(low_numbers)
    mid_freq = Counter(mid_numbers)
    high_freq = Counter(high_numbers)
    star_freq = Counter(all_stars)
    
    # Coverage patterns for balanced distribution
    coverage_patterns = [
        (2, 2, 1),  # 2 low, 2 mid, 1 high
        (1, 3, 1),  # 1 low, 3 mid, 1 high
        (1, 2, 2),  # 1 low, 2 mid, 2 high
        (2, 1, 2),  # 2 low, 1 mid, 2 high
        (1, 1, 3)   # 1 low, 1 mid, 3 high
    ]
    
    pattern = coverage_patterns[pattern_idx % len(coverage_patterns)]
    low_count, mid_count, high_count = pattern
    
    combo_numbers = []
    
    # Select according to pattern
    if low_count > 0 and low_freq:
        low_candidates = [n for n, freq in low_freq.most_common(12)]
        selected = random.sample(low_candidates, min(low_count, len(low_candidates)))
        combo_numbers.extend(selected)
    
    if mid_count > 0 and mid_freq:
        mid_candidates = [n for n, freq in mid_freq.most_common(15)]
        mid_candidates = [n for n in mid_candidates if n not in combo_numbers]
        selected = random.sample(mid_candidates, min(mid_count, len(mid_candidates)))
        combo_numbers.extend(selected)
    
    if high_count > 0 and high_freq:
        high_candidates = [n for n, freq in high_freq.most_common(12)]
        high_candidates = [n for n in high_candidates if n not in combo_numbers]
        selected = random.sample(high_candidates, min(high_count, len(high_candidates)))
        combo_numbers.extend(selected)
    
    # Fill remaining slots
    while len(combo_numbers) < 5:
        all_freq = Counter(all_numbers)
        remaining = [n for n, freq in all_freq.most_common(30) if n not in combo_numbers]
        if remaining:
            combo_numbers.append(random.choice(remaining))
        else:
            break
    
    # Select stars
    top_stars = [s for s, freq in star_freq.most_common(8)]
    combo_stars = random.sample(top_stars, min(2, len(top_stars)))
    
    return sorted(combo_numbers[:5]), sorted(combo_stars)

def generate_risk_reward_combination(all_numbers, all_stars, risk_level):
    """Generate combination using risk-reward analysis"""
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Categorize numbers by frequency
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    total_numbers = len(sorted_numbers)
    
    hot_numbers = [n for n, freq in sorted_numbers[:total_numbers//3]]
    warm_numbers = [n for n, freq in sorted_numbers[total_numbers//3:2*total_numbers//3]]
    cold_numbers = [n for n, freq in sorted_numbers[2*total_numbers//3:]]
    
    # Risk profiles
    risk_profiles = [
        {'hot': 4, 'warm': 1, 'cold': 0},  # Conservative
        {'hot': 3, 'warm': 2, 'cold': 0},  # Moderate
        {'hot': 2, 'warm': 2, 'cold': 1},  # Balanced
        {'hot': 1, 'warm': 3, 'cold': 1},  # Moderate Risk
        {'hot': 1, 'warm': 2, 'cold': 2}   # Aggressive
    ]
    
    profile = risk_profiles[risk_level % len(risk_profiles)]
    combo_numbers = []
    
    # Select according to risk profile
    if profile['hot'] > 0 and hot_numbers:
        selected = random.sample(hot_numbers, min(profile['hot'], len(hot_numbers)))
        combo_numbers.extend(selected)
    
    if profile['warm'] > 0 and warm_numbers:
        available_warm = [n for n in warm_numbers if n not in combo_numbers]
        selected = random.sample(available_warm, min(profile['warm'], len(available_warm)))
        combo_numbers.extend(selected)
    
    if profile['cold'] > 0 and cold_numbers:
        available_cold = [n for n in cold_numbers if n not in combo_numbers]
        selected = random.sample(available_cold, min(profile['cold'], len(available_cold)))
        combo_numbers.extend(selected)
    
    # Fill remaining
    while len(combo_numbers) < 5:
        all_available = hot_numbers + warm_numbers + cold_numbers
        remaining = [n for n in all_available if n not in combo_numbers]
        if remaining:
            combo_numbers.append(random.choice(remaining))
        else:
            break
    
    # Select stars
    top_stars = [s for s, freq in star_freq.most_common(8)]
    combo_stars = random.sample(top_stars, min(2, len(top_stars)))
    
    return sorted(combo_numbers[:5]), sorted(combo_stars)

def generate_optimized_combinations():
    """Generate 10 optimized combinations based on backtesting results"""
    
    print("GENERATING 10 OPTIMIZED COMBINATIONS")
    print("Based on backtesting performance rankings")
    print("=" * 40)
    
    # Get historical data
    historical_data = get_recent_euromillions_data(200)
    
    # Extract all numbers and stars for analysis
    all_numbers = []
    all_stars = []
    
    for row in historical_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_stars.extend([s1, s2])
    
    # Build Markov transition matrix
    number_transitions, star_transitions = build_markov_transition_matrix(historical_data)
    
    combinations = []
    
    # Generate combinations using top strategies
    # 4 Markov Chain combinations (best performer)
    for i in range(4):
        numbers, stars = generate_markov_chain_combination(
            number_transitions, star_transitions, all_numbers, all_stars, i
        )
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Markov Chain {i+1}',
            'priority': 1
        })
    
    # 3 Coverage Optimization combinations (second best)
    for i in range(3):
        numbers, stars = generate_coverage_optimization_combination(all_numbers, all_stars, i)
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Coverage Optimization {i+1}',
            'priority': 2
        })
    
    # 3 Risk-Reward combinations (third best)
    for i in range(3):
        numbers, stars = generate_risk_reward_combination(all_numbers, all_stars, i)
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Risk-Reward {i+1}',
            'priority': 3
        })
    
    return combinations

def validate_and_display_combinations(combinations):
    """Validate and display the generated combinations"""
    
    print("\n10 OPTIMIZED EUROMILLIONS COMBINATIONS:")
    print("-" * 38)
    
    for i, combo in enumerate(combinations, 1):
        # Validate format
        numbers = combo['numbers']
        stars = combo['stars']
        
        # Check constraints
        valid = True
        if len(numbers) != 5 or len(stars) != 2:
            valid = False
        if not all(1 <= n <= 49 for n in numbers):
            valid = False
        if not all(1 <= s <= 12 for s in stars):
            valid = False
        if len(set(numbers)) != 5 or len(set(stars)) != 2:
            valid = False
        
        status = "✓" if valid else "✗"
        
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {numbers} + Stars: {stars} {status}")
        print(f"    Priority: {combo['priority']} (Based on backtest ranking)")
        print()
    
    # Summary statistics
    all_numbers = set()
    all_stars = set()
    
    for combo in combinations:
        all_numbers.update(combo['numbers'])
        all_stars.update(combo['stars'])
    
    print("COVERAGE ANALYSIS:")
    print(f"Unique numbers used: {len(all_numbers)} out of 49")
    print(f"Unique stars used: {len(all_stars)} out of 12")
    print(f"Number range: {min(all_numbers)} to {max(all_numbers)}")
    print(f"Star range: {min(all_stars)} to {max(all_stars)}")

def main():
    """Generate and display optimized combinations"""
    
    combinations = generate_optimized_combinations()
    validate_and_display_combinations(combinations)
    
    print("\nSTRATEGY ALLOCATION:")
    print("-" * 19)
    print("• 4 Markov Chain (1.860 avg score)")
    print("• 3 Coverage Optimization (1.750 avg score)")
    print("• 3 Risk-Reward (1.710 avg score)")
    print("\nBased on 100-draw historical backtesting analysis")

if __name__ == "__main__":
    main()