"""
Generate 4 French Loto combinations using proven strategic methods
French Loto: 5 numbers (1-49) + 1 lucky number (1-10)
Using DIFFERENT strategies for numbers vs lucky numbers
"""

import psycopg2
import os
from collections import Counter
import random
from datetime import datetime

def get_french_loto_data():
    """Get comprehensive French Loto historical data"""
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get recent draws
    recent_query = """
    SELECT date, n1, n2, n3, n4, n5, lucky 
    FROM french_loto_drawings 
    WHERE date <= '2025-07-23'
    ORDER BY date DESC
    LIMIT 10
    """
    
    cursor.execute(recent_query)
    recent_results = cursor.fetchall()
    
    # Get comprehensive training data
    training_query = """
    SELECT date, n1, n2, n3, n4, n5, lucky 
    FROM french_loto_drawings 
    WHERE date <= '2025-07-23'
    ORDER BY date DESC
    LIMIT 1000
    """
    
    cursor.execute(training_query)
    training_results = cursor.fetchall()
    conn.close()
    
    return recent_results, training_results

def analyze_french_loto_patterns(recent_results, training_results):
    """Analyze French Loto patterns"""
    
    print("FRENCH LOTO ANALYSIS")
    print("=" * 20)
    print("\nRECENT DRAWS:")
    
    recent_numbers = []
    recent_lucky = []
    
    for i, row in enumerate(recent_results[:5]):
        date, n1, n2, n3, n4, n5, lucky = row
        numbers = sorted([n1, n2, n3, n4, n5])
        recent_numbers.extend(numbers)
        recent_lucky.append(lucky)
        print(f"{date}: {numbers} + Lucky: {lucky}")
    
    # Analyze all training data
    all_numbers = []
    all_lucky = []
    
    for row in training_results:
        _, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_lucky.append(lucky)
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    recent_number_freq = Counter(recent_numbers)
    recent_lucky_freq = Counter(recent_lucky)
    
    print("\nPATTERN INSIGHTS:")
    print(f"Hot numbers (recent): {[n for n, _ in recent_number_freq.most_common(10)]}")
    print(f"Hot lucky numbers (recent): {[l for l, _ in recent_lucky_freq.most_common(5)]}")
    
    # Categorize numbers by frequency
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_lucky = sorted(lucky_freq.items(), key=lambda x: x[1], reverse=True)
    
    total_numbers = len(sorted_numbers)
    
    frequent_numbers = [n for n, _ in sorted_numbers[:total_numbers//3]]
    medium_numbers = [n for n, _ in sorted_numbers[total_numbers//3:2*total_numbers//3]]
    rare_numbers = [n for n, _ in sorted_numbers[2*total_numbers//3:]]
    
    frequent_lucky = [l for l, _ in sorted_lucky[:4]]
    medium_lucky = [l for l, _ in sorted_lucky[4:7]]
    rare_lucky = [l for l, _ in sorted_lucky[7:]]
    
    return {
        'number_freq': number_freq,
        'lucky_freq': lucky_freq,
        'frequent_numbers': frequent_numbers,
        'medium_numbers': medium_numbers,
        'rare_numbers': rare_numbers,
        'frequent_lucky': frequent_lucky,
        'medium_lucky': medium_lucky,
        'rare_lucky': rare_lucky,
        'recent_numbers': recent_numbers,
        'recent_lucky': recent_lucky
    }

def generate_french_loto_number_strategies(data):
    """Generate 4 different number strategies for French Loto"""
    
    strategies = []
    
    # Strategy 1: Frequency Hot Pursuit
    numbers1 = random.sample(data['frequent_numbers'][:20], 5)
    strategies.append({
        'numbers': sorted(numbers1),
        'strategy': 'Frequency Hot Pursuit',
        'focus': 'Most frequently drawn numbers'
    })
    
    # Strategy 2: Balanced Distribution
    numbers2 = []
    # Ensure range coverage
    low_nums = [n for n in data['frequent_numbers'] + data['medium_numbers'] if n <= 16]
    mid_nums = [n for n in data['frequent_numbers'] + data['medium_numbers'] if 17 <= n <= 33]
    high_nums = [n for n in data['frequent_numbers'] + data['medium_numbers'] if n >= 34]
    
    numbers2.extend(random.sample(low_nums, 2))
    numbers2.extend(random.sample(mid_nums, 2))
    numbers2.extend(random.sample(high_nums, 1))
    
    strategies.append({
        'numbers': sorted(numbers2),
        'strategy': 'Balanced Distribution',
        'focus': 'Perfect range balance'
    })
    
    # Strategy 3: Recent Pattern Integration
    recent_hot = Counter(data['recent_numbers']).most_common(15)
    recent_hot_numbers = [n for n, _ in recent_hot]
    
    numbers3 = []
    numbers3.extend(random.sample(recent_hot_numbers[:10], 3))
    # Add some medium frequency for balance
    remaining = [n for n in data['medium_numbers'] if n not in numbers3]
    numbers3.extend(random.sample(remaining, 2))
    
    strategies.append({
        'numbers': sorted(numbers3),
        'strategy': 'Recent Pattern Integration',
        'focus': 'Recent hot numbers with balance'
    })
    
    # Strategy 4: Contrarian Approach
    numbers4 = []
    # Mix rare and medium
    numbers4.extend(random.sample(data['rare_numbers'], 2))
    numbers4.extend(random.sample(data['medium_numbers'], 3))
    
    strategies.append({
        'numbers': sorted(numbers4),
        'strategy': 'Contrarian Approach',
        'focus': 'Underplayed numbers strategy'
    })
    
    return strategies

def generate_french_loto_lucky_strategies(data):
    """Generate 4 different lucky number strategies"""
    
    strategies = []
    
    # Lucky Strategy 1: Frequency Based (for combination 1)
    lucky1 = random.choice(data['frequent_lucky'])
    strategies.append({
        'lucky': lucky1,
        'strategy': 'High Frequency Lucky',
        'focus': 'Most common lucky number'
    })
    
    # Lucky Strategy 2: Recent Hot (for combination 2)
    recent_lucky_freq = Counter(data['recent_lucky'])
    if recent_lucky_freq:
        lucky2 = recent_lucky_freq.most_common(1)[0][0]
    else:
        lucky2 = random.choice(data['frequent_lucky'])
    strategies.append({
        'lucky': lucky2,
        'strategy': 'Recent Hot Lucky',
        'focus': 'Currently trending lucky'
    })
    
    # Lucky Strategy 3: Medium Frequency (for combination 3)
    lucky3 = random.choice(data['medium_lucky'])
    strategies.append({
        'lucky': lucky3,
        'strategy': 'Medium Frequency Lucky',
        'focus': 'Balanced lucky selection'
    })
    
    # Lucky Strategy 4: Contrarian Lucky (for combination 4)
    if data['rare_lucky']:
        lucky4 = random.choice(data['rare_lucky'])
    else:
        lucky4 = random.choice(data['medium_lucky'])
    strategies.append({
        'lucky': lucky4,
        'strategy': 'Contrarian Lucky',
        'focus': 'Underplayed lucky number'
    })
    
    return strategies

def generate_4_french_loto_combinations():
    """Generate 4 French Loto combinations with different strategies"""
    
    print("\nGENERATING 4 FRENCH LOTO COMBINATIONS")
    print("=" * 35)
    
    # Get data
    recent_results, training_results = get_french_loto_data()
    data = analyze_french_loto_patterns(recent_results, training_results)
    
    print("\nSTRATEGIC APPROACH:")
    print("-" * 18)
    print("✓ Different strategies for numbers vs lucky numbers")
    print("✓ Based on 1000 historical draws")
    print("✓ 4 unique strategic combinations")
    print()
    
    # Generate strategies
    number_strategies = generate_french_loto_number_strategies(data)
    lucky_strategies = generate_french_loto_lucky_strategies(data)
    
    # Combine into complete combinations
    combinations = []
    
    for i in range(4):
        combination = {
            'id': i + 1,
            'numbers': number_strategies[i]['numbers'],
            'lucky': lucky_strategies[i]['lucky'],
            'number_strategy': number_strategies[i]['strategy'],
            'lucky_strategy': lucky_strategies[i]['strategy'],
            'combined_strategy': f"{number_strategies[i]['strategy']} + {lucky_strategies[i]['strategy']}",
            'focus': f"{number_strategies[i]['focus']} with {lucky_strategies[i]['focus'].lower()}"
        }
        combinations.append(combination)
    
    return combinations

def display_french_loto_combinations(combinations):
    """Display the 4 French Loto combinations"""
    
    print("4 FRENCH LOTO COMBINATIONS:")
    print("-" * 27)
    
    for combo in combinations:
        print(f"\n{combo['id']}. {combo['combined_strategy']}")
        print(f"   Numbers: {combo['numbers']} + Lucky: {combo['lucky']}")
        print(f"   Focus: {combo['focus']}")
    
    # Coverage analysis
    all_numbers = set()
    all_lucky = set()
    
    for combo in combinations:
        all_numbers.update(combo['numbers'])
        all_lucky.add(combo['lucky'])
    
    print("\nCOVERAGE ANALYSIS:")
    print("-" * 17)
    print(f"Total unique numbers: {len(all_numbers)}/49")
    print(f"Total unique lucky numbers: {len(all_lucky)}/10")
    print(f"Numbers used: {sorted(all_numbers)}")
    print(f"Lucky numbers used: {sorted(all_lucky)}")
    
    return combinations

def main():
    """Main function to generate French Loto combinations"""
    
    # Generate 4 combinations
    combinations = generate_4_french_loto_combinations()
    
    # Display combinations
    combinations = display_french_loto_combinations(combinations)
    
    print("\nFRENCH LOTO STRATEGY PRINCIPLES:")
    print("-" * 32)
    print("✓ Different strategies for main numbers vs lucky numbers")
    print("✓ Based on 1000 historical draws analysis")
    print("✓ Range balance optimization")
    print("✓ Frequency-based selection")
    print("✓ Strategic diversity across combinations")
    print("\nBonne chance! 🍀")

if __name__ == "__main__":
    main()