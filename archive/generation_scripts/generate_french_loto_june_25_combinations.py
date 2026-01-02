"""
Generate 5 French Loto combinations for June 25, 2025
Incorporating lessons from June 18 analysis and maintaining mixed strategy approach
"""

import psycopg2
import os
from collections import Counter
import random

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    return psycopg2.connect(database_url)

def get_training_data():
    """Get French Loto training data"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = """
    SELECT date, n1, n2, n3, n4, n5, lucky 
    FROM french_loto_drawings 
    WHERE date < '2025-06-25'
    ORDER BY date DESC
    LIMIT 1000
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def analyze_june_18_lessons():
    """Analyze key lessons from June 18 performance"""
    
    print("JUNE 18 PERFORMANCE LESSONS:")
    print("-" * 28)
    
    june_18_results = {
        'numbers': [9, 13, 19, 24, 36],
        'lucky': 3
    }
    
    print(f"June 18 Results: {june_18_results['numbers']} / {june_18_results['lucky']}")
    print()
    
    lessons = {
        'successful_elements': [
            'Number 13 was correctly identified (appeared in 4 combinations)',
            'Mixed strategy approach showed partial success',
            'Frequency+Frequency strategy captured some winners'
        ],
        'missed_opportunities': [
            'Lucky 3 was completely missed (only played 7, 10, 5)',
            'Numbers 9, 19, 24 had limited coverage',
            'Over-reliance on lucky 7 (appeared 7 times)',
            'Need better low lucky number coverage (1-5)'
        ],
        'strategy_insights': [
            'Continue mixed strategy for main numbers',
            'Diversify lucky number selection',
            'Maintain same strategy alignment (not mixed like Euromillions)',
            'Include more low lucky numbers (1-5)'
        ]
    }
    
    print("Successful Elements:")
    for element in lessons['successful_elements']:
        print(f"  ✓ {element}")
    
    print("\nMissed Opportunities:")
    for missed in lessons['missed_opportunities']:
        print(f"  ❌ {missed}")
    
    print("\nStrategy Insights:")
    for insight in lessons['strategy_insights']:
        print(f"  → {insight}")
    
    print()
    return lessons

def generate_frequency_strategy_numbers(training_data, variation=0):
    """Generate numbers using frequency analysis strategy"""
    
    all_numbers = []
    for row in training_data:
        _, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
    
    number_freq = Counter(all_numbers)
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Top frequent numbers with variation
    top_numbers = [n for n, freq in sorted_numbers[:20]]
    
    # Apply variation to avoid identical combinations
    start_idx = variation * 3
    end_idx = start_idx + 15
    selection_pool = top_numbers[start_idx:end_idx] if end_idx <= len(top_numbers) else top_numbers
    
    # Ensure range distribution
    selected = []
    low_nums = [n for n in selection_pool if n <= 16]
    mid_nums = [n for n in selection_pool if 17 <= n <= 33]
    high_nums = [n for n in selection_pool if n >= 34]
    
    # Select with range balance
    if low_nums:
        selected.extend(random.sample(low_nums, min(2, len(low_nums))))
    if mid_nums:
        selected.extend(random.sample(mid_nums, min(2, len(mid_nums))))
    if high_nums:
        selected.extend(random.sample(high_nums, min(1, len(high_nums))))
    
    # Fill remaining slots
    while len(selected) < 5:
        remaining = [n for n in selection_pool if n not in selected]
        if remaining:
            selected.append(random.choice(remaining))
        else:
            break
    
    return sorted(selected[:5])

def generate_coverage_strategy_numbers(training_data, variation=0):
    """Generate numbers using coverage/balanced strategy"""
    
    all_numbers = []
    for row in training_data:
        _, n1, n2, n3, n4, n5, lucky = row
        all_numbers.extend([n1, n2, n3, n4, n5])
    
    number_freq = Counter(all_numbers)
    
    # Balanced approach: some frequent, some medium, some rare
    sorted_numbers = sorted(number_freq.items(), key=lambda x: x[1], reverse=True)
    total = len(sorted_numbers)
    
    frequent = [n for n, freq in sorted_numbers[:total//3]]
    medium = [n for n, freq in sorted_numbers[total//3:2*total//3]]
    rare = [n for n, freq in sorted_numbers[2*total//3:]]
    
    # Balanced selection with variation
    selected = []
    
    # 2 frequent, 2 medium, 1 rare (with variation)
    if frequent:
        start = (variation * 2) % len(frequent)
        selected.extend(frequent[start:start+2] if start+2 <= len(frequent) else frequent[:2])
    
    if medium and len(selected) < 4:
        start = (variation * 2) % len(medium)
        needed = 4 - len(selected)
        selected.extend(medium[start:start+needed] if start+needed <= len(medium) else medium[:needed])
    
    if rare and len(selected) < 5:
        start = variation % len(rare)
        selected.append(rare[start])
    
    # Fill remaining
    while len(selected) < 5:
        all_available = frequent + medium + rare
        remaining = [n for n in all_available if n not in selected]
        if remaining:
            selected.append(random.choice(remaining))
        else:
            break
    
    return sorted(selected[:5])

def generate_enhanced_lucky_strategy(training_data, strategy_type, variation=0):
    """Generate lucky number with enhanced distribution"""
    
    all_lucky = []
    for row in training_data:
        _, n1, n2, n3, n4, n5, lucky = row
        all_lucky.append(lucky)
    
    lucky_freq = Counter(all_lucky)
    sorted_lucky = sorted(lucky_freq.items(), key=lambda x: x[1], reverse=True)
    
    # June 18 lesson: diversify lucky numbers, include more 1-5
    low_lucky = [l for l in range(1, 6)]    # 1-5
    mid_lucky = [l for l in range(6, 8)]    # 6-7  
    high_lucky = [l for l in range(8, 11)]  # 8-10
    
    if strategy_type == 'frequency':
        # Frequency but with low number bias
        top_lucky = [l for l, freq in sorted_lucky[:8]]
        
        # Ensure low numbers are included
        enhanced_pool = top_lucky + [l for l in low_lucky if l not in top_lucky]
        return enhanced_pool[variation % len(enhanced_pool)]
    
    else:  # coverage/balanced
        # Balanced distribution with low number preference
        if variation < 3:
            return low_lucky[variation % len(low_lucky)]
        elif variation < 5:
            return mid_lucky[(variation-3) % len(mid_lucky)]
        else:
            return high_lucky[(variation-5) % len(high_lucky)]

def generate_june_25_combinations():
    """Generate 5 combinations for June 25, 2025"""
    
    print("GENERATING 5 FRENCH LOTO COMBINATIONS FOR JUNE 25, 2025")
    print("=" * 56)
    
    training_data = get_training_data()
    lessons = analyze_june_18_lessons()
    
    print(f"Using {len(training_data)} historical draws")
    print("Applying enhanced mixed strategy with lucky number diversification")
    print()
    
    combinations = []
    
    # Combination 1: Frequency + Frequency (Enhanced)
    numbers_1 = generate_frequency_strategy_numbers(training_data, 0)
    lucky_1 = generate_enhanced_lucky_strategy(training_data, 'frequency', 0)
    
    combinations.append({
        'id': 1,
        'numbers': numbers_1,
        'lucky': lucky_1,
        'strategy': 'Enhanced Frequency + Frequency',
        'focus': 'Top frequency with low lucky bias',
        'lesson_applied': 'Diversified lucky selection'
    })
    
    # Combination 2: Frequency + Frequency (Low Lucky Focus)
    numbers_2 = generate_frequency_strategy_numbers(training_data, 1)
    lucky_2 = generate_enhanced_lucky_strategy(training_data, 'frequency', 1)
    
    combinations.append({
        'id': 2,
        'numbers': numbers_2,
        'lucky': lucky_2,
        'strategy': 'Enhanced Frequency + Frequency',
        'focus': 'Frequency numbers with lucky 1-5',
        'lesson_applied': 'Low lucky number inclusion'
    })
    
    # Combination 3: Coverage + Balanced (Low Lucky)
    numbers_3 = generate_coverage_strategy_numbers(training_data, 0)
    lucky_3 = generate_enhanced_lucky_strategy(training_data, 'coverage', 2)
    
    combinations.append({
        'id': 3,
        'numbers': numbers_3,
        'lucky': lucky_3,
        'strategy': 'Enhanced Coverage + Balanced',
        'focus': 'Balanced coverage with low lucky',
        'lesson_applied': 'Better range distribution'
    })
    
    # Combination 4: Frequency + Frequency (Mid Range)
    numbers_4 = generate_frequency_strategy_numbers(training_data, 2)
    lucky_4 = generate_enhanced_lucky_strategy(training_data, 'frequency', 4)
    
    combinations.append({
        'id': 4,
        'numbers': numbers_4,
        'lucky': lucky_4,
        'strategy': 'Enhanced Frequency + Frequency',
        'focus': 'Varied frequency with mid lucky',
        'lesson_applied': 'Strategic variation'
    })
    
    # Combination 5: Coverage + Balanced (Diversified)
    numbers_5 = generate_coverage_strategy_numbers(training_data, 1)
    lucky_5 = generate_enhanced_lucky_strategy(training_data, 'coverage', 0)
    
    combinations.append({
        'id': 5,
        'numbers': numbers_5,
        'lucky': lucky_5,
        'strategy': 'Enhanced Coverage + Balanced',
        'focus': 'Balanced with lucky diversification',
        'lesson_applied': 'Complete strategy coverage'
    })
    
    return combinations

def validate_and_display_combinations(combinations):
    """Validate and display the combinations"""
    
    print("5 ENHANCED COMBINATIONS FOR JUNE 25, 2025:")
    print("-" * 41)
    
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
        print(f"   Focus: {combo['focus']}")
        print(f"   Lesson Applied: {combo['lesson_applied']}")
        print()
    
    print("COVERAGE SUMMARY:")
    print(f"Valid combinations: {valid_count}/5")
    print(f"Unique numbers: {len(all_numbers)}/49 ({len(all_numbers)/49*100:.1f}%)")
    print(f"Unique lucky numbers: {len(all_lucky)}/10 ({len(all_lucky)/10*100:.1f}%)")
    print(f"Lucky numbers used: {sorted(all_lucky)}")
    
    # Lucky distribution analysis
    low_lucky = len([l for l in all_lucky if l <= 5])
    high_lucky = len([l for l in all_lucky if l >= 6])
    print(f"Lucky distribution: {low_lucky} low (1-5), {high_lucky} high (6-10)")
    
    return combinations

def analyze_improvements():
    """Analyze the improvements made"""
    
    print("\nIMPROVEMENTS FROM JUNE 18 ANALYSIS:")
    print("-" * 35)
    
    print("KEY ENHANCEMENTS:")
    print("• Enhanced lucky number diversification (avoid over-reliance on 7)")
    print("• Increased low lucky number inclusion (1-5 range)")
    print("• Maintained same strategy alignment (proven effective)")
    print("• Improved range distribution for main numbers")
    print("• Strategic variation to avoid identical combinations")
    print()
    
    print("JUNE 18 LESSONS APPLIED:")
    print("• Lucky number 3 type coverage increased")
    print("• Reduced frequency bias for lucky numbers")
    print("• Better balance between frequency and coverage strategies")
    print("• Enhanced number selection with range awareness")
    print()
    
    print("STRATEGIC RATIONALE:")
    print("• French Loto benefits from same strategy alignment")
    print("• Different from Euromillions mixed approach")
    print("• Frequency+Frequency remains primary (60%)")
    print("• Coverage+Balanced provides diversity (40%)")
    print("• Lucky number strategy now more balanced")

def main():
    """Generate combinations for June 25, 2025"""
    
    combinations = generate_june_25_combinations()
    validate_and_display_combinations(combinations)
    analyze_improvements()
    
    print("\nKEY FEATURES FOR JUNE 25:")
    print("✓ Enhanced lucky number diversification")
    print("✓ Increased low lucky number coverage (1-5)")
    print("✓ Maintained proven same strategy alignment")
    print("✓ Improved range distribution")
    print("✓ Applied June 18 performance lessons")

if __name__ == "__main__":
    main()