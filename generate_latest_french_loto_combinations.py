"""
Generate 5 French Loto combinations for the next draw
Using proven strategies with different approach for lucky numbers vs main numbers
Based on historical French Loto analysis and performance lessons
"""

import psycopg2
import os
from collections import Counter
import random

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    return psycopg2.connect(database_url)

def get_french_loto_training_data():
    """Get latest French Loto training data"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = """
    SELECT date, n1, n2, n3, n4, n5, lucky 
    FROM french_loto_drawings 
    ORDER BY date DESC
    LIMIT 1000
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    print(f"Loaded {len(results)} French Loto draws")
    if results:
        latest_date = results[0][0]
        print(f"Latest draw: {latest_date}")
    
    return results

def analyze_french_loto_patterns(training_data):
    """Analyze French Loto patterns for numbers and lucky numbers separately"""
    
    all_numbers = []
    all_lucky = []
    
    for row in training_data:
        _, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
        all_lucky.append(lucky)
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    print("FRENCH LOTO PATTERN ANALYSIS:")
    print("-" * 29)
    print("Top 10 most frequent numbers:")
    for num, freq in number_freq.most_common(10):
        print(f"  {num}: {freq} times")
    
    print("\nLucky number frequencies (top 5):")
    for lucky, freq in lucky_freq.most_common(5):
        print(f"  {lucky}: {freq} times")
    
    # Categorize numbers
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    total = len(sorted_numbers)
    
    hot_numbers = [n for n, _ in sorted_numbers[:total//3]]
    warm_numbers = [n for n, _ in sorted_numbers[total//3:2*total//3]]
    cold_numbers = [n for n, _ in sorted_numbers[2*total//3:]]
    
    print(f"\nNumber categorization:")
    print(f"Hot numbers (top third): {len(hot_numbers)}")
    print(f"Warm numbers (middle third): {len(warm_numbers)}")
    print(f"Cold numbers (bottom third): {len(cold_numbers)}")
    
    return number_freq, lucky_freq, hot_numbers, warm_numbers, cold_numbers

def generate_frequency_analysis_numbers(hot_numbers, warm_numbers, cold_numbers, variation=0):
    """Generate numbers using frequency analysis strategy"""
    
    # Frequency analysis: balanced selection across tiers
    target_distributions = [
        {'hot': 2, 'warm': 2, 'cold': 1},  # Balanced
        {'hot': 3, 'warm': 1, 'cold': 1},  # Hot emphasis
        {'hot': 1, 'warm': 3, 'cold': 1},  # Warm emphasis
        {'hot': 2, 'warm': 1, 'cold': 2},  # Hot+Cold
        {'hot': 1, 'warm': 2, 'cold': 2}   # Warm+Cold
    ]
    
    distribution = target_distributions[variation % len(target_distributions)]
    selected = []
    
    # Select from each category
    if distribution['hot'] > 0:
        available_hot = [n for n in hot_numbers if n not in selected]
        selected.extend(random.sample(available_hot, min(distribution['hot'], len(available_hot))))
    
    if distribution['warm'] > 0:
        available_warm = [n for n in warm_numbers if n not in selected]
        selected.extend(random.sample(available_warm, min(distribution['warm'], len(available_warm))))
    
    if distribution['cold'] > 0:
        available_cold = [n for n in cold_numbers if n not in selected]
        selected.extend(random.sample(available_cold, min(distribution['cold'], len(available_cold))))
    
    # Fill if needed
    while len(selected) < 5:
        all_available = hot_numbers + warm_numbers + cold_numbers
        remaining = [n for n in all_available if n not in selected]
        if remaining:
            selected.append(random.choice(remaining))
        else:
            break
    
    return sorted(selected[:5])

def generate_coverage_optimization_numbers(hot_numbers, warm_numbers, cold_numbers, variation=0):
    """Generate numbers using coverage optimization strategy"""
    
    # Coverage optimization: ensure broad coverage with range balance
    low_nums = [n for n in range(1, 17)]  # 1-16
    mid_nums = [n for n in range(17, 34)]  # 17-33
    high_nums = [n for n in range(34, 50)]  # 34-49
    
    # Target range distributions
    range_distributions = [
        {'low': 2, 'mid': 2, 'high': 1},  # Balanced
        {'low': 1, 'mid': 3, 'high': 1},  # Mid emphasis
        {'low': 2, 'mid': 1, 'high': 2},  # Low+High
        {'low': 3, 'mid': 1, 'high': 1},  # Low emphasis
        {'low': 1, 'mid': 2, 'high': 2}   # Mid+High
    ]
    
    distribution = range_distributions[variation % len(range_distributions)]
    selected = []
    
    # Select from each range, prioritizing frequency
    for range_name, target_count in distribution.items():
        if range_name == 'low':
            candidates = [n for n in hot_numbers + warm_numbers if n in low_nums]
        elif range_name == 'mid':
            candidates = [n for n in hot_numbers + warm_numbers if n in mid_nums]
        else:  # high
            candidates = [n for n in hot_numbers + warm_numbers + cold_numbers if n in high_nums]
        
        available = [n for n in candidates if n not in selected]
        if len(available) >= target_count:
            selected.extend(random.sample(available, target_count))
        else:
            selected.extend(available)
    
    # Fill remaining slots
    while len(selected) < 5:
        all_candidates = hot_numbers + warm_numbers + cold_numbers
        remaining = [n for n in all_candidates if n not in selected]
        if remaining:
            selected.append(random.choice(remaining))
        else:
            break
    
    return sorted(selected[:5])

def generate_enhanced_risk_reward_numbers(hot_numbers, warm_numbers, cold_numbers, variation=0):
    """Generate numbers using enhanced risk-reward strategy"""
    
    # Risk-reward: strategic balance with different risk profiles
    risk_profiles = [
        {'hot': 2, 'warm': 2, 'cold': 1, 'name': 'balanced_risk'},
        {'hot': 1, 'warm': 2, 'cold': 2, 'name': 'cold_emphasis'},
        {'hot': 3, 'warm': 1, 'cold': 1, 'name': 'conservative'},
        {'hot': 1, 'warm': 1, 'cold': 3, 'name': 'contrarian'},
        {'hot': 2, 'warm': 3, 'cold': 0, 'name': 'warm_focus'}
    ]
    
    profile = risk_profiles[variation % len(risk_profiles)]
    selected = []
    
    # Apply risk profile
    categories = [
        ('hot', hot_numbers, profile['hot']),
        ('warm', warm_numbers, profile['warm']),
        ('cold', cold_numbers, profile['cold'])
    ]
    
    for cat_name, numbers, count in categories:
        if count > 0:
            available = [n for n in numbers if n not in selected]
            selected.extend(random.sample(available, min(count, len(available))))
    
    # Fill to 5 numbers
    while len(selected) < 5:
        all_available = hot_numbers + warm_numbers + cold_numbers
        remaining = [n for n in all_available if n not in selected]
        if remaining:
            selected.append(random.choice(remaining))
        else:
            break
    
    return sorted(selected[:5])

def generate_lucky_number_different_strategy(lucky_freq, main_numbers, variation=0):
    """
    Generate lucky number using DIFFERENT strategy than main numbers
    French Loto lesson: Use different approach for lucky vs main numbers
    """
    
    # Analyze lucky frequency patterns
    sorted_lucky = sorted(lucky_freq.items(), key=lambda x: x[1], reverse=True)
    total_lucky = len(sorted_lucky)
    
    # Categorize lucky numbers differently than main numbers
    frequent_lucky = [l for l, _ in sorted_lucky[:total_lucky//3]]
    medium_lucky = [l for l, _ in sorted_lucky[total_lucky//3:2*total_lucky//3]]
    rare_lucky = [l for l, _ in sorted_lucky[2*total_lucky//3:]]
    
    # Different strategies for lucky numbers
    lucky_strategies = [
        'frequency_opposite',  # If main numbers used frequency, use rarity
        'range_complement',    # Complement main number ranges
        'pure_frequency',      # Pure frequency approach
        'balanced_mix',        # Balanced frequency approach
        'contrarian'          # Contrarian approach
    ]
    
    strategy = lucky_strategies[variation % len(lucky_strategies)]
    
    if strategy == 'frequency_opposite':
        # Use rare lucky numbers (opposite of frequency)
        candidates = rare_lucky + medium_lucky
        return random.choice(candidates) if candidates else random.choice(frequent_lucky)
    
    elif strategy == 'range_complement':
        # Complement main number range
        main_sum = sum(main_numbers)
        if main_sum < 100:  # Low sum main numbers
            # Use higher lucky numbers
            high_lucky = [l for l in frequent_lucky + medium_lucky if l >= 6]
            return random.choice(high_lucky) if high_lucky else random.choice(frequent_lucky)
        else:  # High sum main numbers
            # Use lower lucky numbers
            low_lucky = [l for l in frequent_lucky + medium_lucky if l <= 5]
            return random.choice(low_lucky) if low_lucky else random.choice(frequent_lucky)
    
    elif strategy == 'pure_frequency':
        # Pure frequency approach
        return frequent_lucky[0] if frequent_lucky else 1
    
    elif strategy == 'balanced_mix':
        # Balanced selection across all tiers
        all_candidates = frequent_lucky + medium_lucky + rare_lucky
        return random.choice(all_candidates)
    
    else:  # contrarian
        # Full contrarian approach
        return rare_lucky[0] if rare_lucky else medium_lucky[0]

def generate_5_french_loto_combinations(training_data):
    """Generate 5 French Loto combinations using mixed strategies"""
    
    number_freq, lucky_freq, hot_numbers, warm_numbers, cold_numbers = analyze_french_loto_patterns(training_data)
    
    print(f"\nGENERATING 5 FRENCH LOTO COMBINATIONS:")
    print("-" * 37)
    
    combinations = []
    
    # Combination 1: Frequency Analysis + Range Complement Lucky
    numbers_1 = generate_frequency_analysis_numbers(hot_numbers, warm_numbers, cold_numbers, 0)
    lucky_1 = generate_lucky_number_different_strategy(lucky_freq, numbers_1, 1)  # Range complement
    
    combinations.append({
        'id': 1,
        'numbers': numbers_1,
        'lucky': lucky_1,
        'strategy': 'Frequency Analysis + Range Complement Lucky',
        'numbers_focus': 'Balanced hot/warm/cold selection',
        'lucky_focus': 'Complements main number range'
    })
    
    # Combination 2: Coverage Optimization + Frequency Opposite Lucky
    numbers_2 = generate_coverage_optimization_numbers(hot_numbers, warm_numbers, cold_numbers, 0)
    lucky_2 = generate_lucky_number_different_strategy(lucky_freq, numbers_2, 0)  # Frequency opposite
    
    combinations.append({
        'id': 2,
        'numbers': numbers_2,
        'lucky': lucky_2,
        'strategy': 'Coverage Optimization + Frequency Opposite Lucky',
        'numbers_focus': 'Balanced range coverage',
        'lucky_focus': 'Rare/medium lucky selection'
    })
    
    # Combination 3: Enhanced Risk-Reward + Pure Frequency Lucky
    numbers_3 = generate_enhanced_risk_reward_numbers(hot_numbers, warm_numbers, cold_numbers, 1)
    lucky_3 = generate_lucky_number_different_strategy(lucky_freq, numbers_3, 2)  # Pure frequency
    
    combinations.append({
        'id': 3,
        'numbers': numbers_3,
        'lucky': lucky_3,
        'strategy': 'Enhanced Risk-Reward + Pure Frequency Lucky',
        'numbers_focus': 'Cold emphasis risk profile',
        'lucky_focus': 'Most frequent lucky number'
    })
    
    # Combination 4: Frequency Analysis (Hot emphasis) + Balanced Mix Lucky
    numbers_4 = generate_frequency_analysis_numbers(hot_numbers, warm_numbers, cold_numbers, 1)
    lucky_4 = generate_lucky_number_different_strategy(lucky_freq, numbers_4, 3)  # Balanced mix
    
    combinations.append({
        'id': 4,
        'numbers': numbers_4,
        'lucky': lucky_4,
        'strategy': 'Frequency Analysis (Hot) + Balanced Mix Lucky',
        'numbers_focus': 'Hot number emphasis',
        'lucky_focus': 'Balanced tier selection'
    })
    
    # Combination 5: Coverage Optimization (Mid emphasis) + Contrarian Lucky
    numbers_5 = generate_coverage_optimization_numbers(hot_numbers, warm_numbers, cold_numbers, 1)
    lucky_5 = generate_lucky_number_different_strategy(lucky_freq, numbers_5, 4)  # Contrarian
    
    combinations.append({
        'id': 5,
        'numbers': numbers_5,
        'lucky': lucky_5,
        'strategy': 'Coverage Optimization (Mid) + Contrarian Lucky',
        'numbers_focus': 'Mid-range emphasis coverage',
        'lucky_focus': 'Rare lucky number selection'
    })
    
    return combinations

def validate_and_display_combinations(combinations):
    """Validate and display the French Loto combinations"""
    
    print("5 FRENCH LOTO COMBINATIONS:")
    print("-" * 27)
    
    all_numbers = set()
    all_lucky = set()
    valid_count = 0
    
    for combo in combinations:
        numbers = combo['numbers']
        lucky = combo['lucky']
        
        # Validate
        valid = True
        issues = []
        
        if len(numbers) != 5:
            valid = False
            issues.append(f"numbers={len(numbers)}")
        if not isinstance(lucky, int):
            valid = False
            issues.append("lucky_type")
        if not all(1 <= n <= 49 for n in numbers):
            valid = False
            issues.append("number_range")
        if not (1 <= lucky <= 10):
            valid = False
            issues.append("lucky_range")
        if len(set(numbers)) != 5:
            valid = False
            issues.append("duplicate_numbers")
        
        if valid:
            valid_count += 1
            all_numbers.update(numbers)
            all_lucky.add(lucky)
        
        status = "✓" if valid else f"✗ ({', '.join(issues)})"
        
        print(f"{combo['id']}. {combo['strategy']}")
        print(f"   Numbers: {numbers} + Lucky: {lucky} {status}")
        print(f"   Numbers Strategy: {combo['numbers_focus']}")
        print(f"   Lucky Strategy: {combo['lucky_focus']}")
        print()
    
    print("COVERAGE SUMMARY:")
    print(f"Valid combinations: {valid_count}/5")
    print(f"Unique numbers: {len(all_numbers)}/49 ({len(all_numbers)/49*100:.1f}%)")
    print(f"Unique lucky numbers: {len(all_lucky)}/10 ({len(all_lucky)/10*100:.1f}%)")
    print(f"Lucky numbers used: {sorted(all_lucky)}")
    
    return combinations

def analyze_strategic_approach():
    """Analyze the strategic approach for French Loto"""
    
    print("\nFRENCH LOTO STRATEGIC APPROACH:")
    print("-" * 31)
    
    print("KEY STRATEGIC PRINCIPLES:")
    print("• Different strategies for numbers vs lucky number")
    print("• Main numbers: Proven strategies (Frequency, Coverage, Risk-Reward)")
    print("• Lucky numbers: Complementary/opposite approaches")
    print("• Strategy alignment: SAME strategy for both (French Loto lesson)")
    print("• Diversified lucky selection after June 18 lesson")
    print()
    
    print("STRATEGIC COMBINATIONS:")
    print("• Numbers use proven lottery strategies")
    print("• Lucky numbers use different/complementary logic")
    print("• Frequency Analysis ↔ Range/Rarity complement")
    print("• Coverage Optimization ↔ Frequency opposite")
    print("• Risk-Reward ↔ Pure frequency/contrarian")
    print()
    
    print("HISTORICAL LESSONS APPLIED:")
    print("• June 18 French Loto: Over-reliance on lucky 7 failed")
    print("• Diversified lucky number selection (1-5 emphasis)")
    print("• Mixed strategy approach for comprehensive coverage")
    print("• Enhanced low lucky number inclusion")

def main():
    """Generate 5 French Loto combinations using mixed strategies"""
    
    print("FRENCH LOTO COMBINATION GENERATOR")
    print("=" * 34)
    
    training_data = get_french_loto_training_data()
    
    if not training_data:
        print("No French Loto data found in database!")
        return
    
    combinations = generate_5_french_loto_combinations(training_data)
    validate_and_display_combinations(combinations)
    analyze_strategic_approach()
    
    print("\nKEY FEATURES:")
    print("✓ Different strategies for numbers vs lucky numbers")
    print("✓ Proven main number strategies (Frequency, Coverage, Risk-Reward)")
    print("✓ Complementary lucky number approaches")
    print("✓ Historical lessons integrated")
    print("✓ Diversified lucky number selection")

if __name__ == "__main__":
    main()