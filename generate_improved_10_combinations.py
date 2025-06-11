"""
Generate 10 improved French Loto combinations based on latest performance insights
Key learnings: Range balance effective, number 5 strategy worked, need better mid-range coverage
"""

import psycopg2
import os
from collections import Counter
import random

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    else:
        raise Exception("No database connection available")

def get_french_loto_data(limit=150):
    """Get recent French Loto historical data"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = """
    SELECT date, n1, n2, n3, n4, n5, lucky 
    FROM french_loto_drawings 
    ORDER BY date DESC 
    LIMIT %s
    """
    
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    
    conn.close()
    return results

def analyze_winning_patterns():
    """Analyze patterns from latest winning draw and historical data"""
    
    # Latest winning numbers: 5, 12, 25, 34, 38 / 10
    latest_winning = {
        'numbers': [5, 12, 25, 34, 38],
        'lucky': 10,
        'range_distribution': {'low': [5, 12], 'mid': [25], 'high': [34, 38]},
        'sum': 114,
        'spacings': [7, 13, 9, 4]
    }
    
    # Get historical data
    historical_data = get_french_loto_data(100)
    
    all_numbers = []
    all_lucky = []
    
    for row in historical_data:
        date, n1, n2, n3, n4, n5, lucky = row
        numbers = [n1, n2, n3, n4, n5]
        all_numbers.extend(numbers)
        all_lucky.append(lucky)
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    print("PERFORMANCE INSIGHTS ANALYSIS:")
    print("=" * 30)
    print("Latest winning: 5, 12, 25, 34, 38 / 10")
    print("Key insights from our performance:")
    print("- Range balance was effective (Range Cycling: 2 hits)")
    print("- Number 5 strategy worked (appeared in 4 winning combos)")
    print("- Missing mid-range coverage (25 was not covered)")
    print("- Lucky 10 was not covered by any combination")
    print()
    
    return latest_winning, number_freq, lucky_freq

def generate_improved_time_series_combinations():
    """Generate 5 improved Time Series combinations based on performance insights"""
    
    latest_winning, number_freq, lucky_freq = analyze_winning_patterns()
    
    combinations = []
    
    # 1. Enhanced Range Cycling - Improved version of our best performer
    # Focus on balanced range with better mid-range coverage
    low_range_numbers = [n for n in range(1, 17) if number_freq[n] >= 3]
    mid_range_numbers = [n for n in range(17, 34) if number_freq[n] >= 3]  # Enhanced mid-range
    high_range_numbers = [n for n in range(34, 50) if number_freq[n] >= 3]
    
    enhanced_range = []
    enhanced_range.extend(random.sample(low_range_numbers[:8], 2))  # 2 low
    enhanced_range.extend(random.sample(mid_range_numbers[:8], 2))  # 2 mid (improved)
    enhanced_range.extend(random.sample(high_range_numbers[:6], 1))  # 1 high
    
    combinations.append({
        'numbers': sorted(enhanced_range),
        'lucky': 10,  # Latest winning lucky number
        'strategy': 'Enhanced Range Cycling',
        'logic': 'Improved range balance with stronger mid-range coverage'
    })
    
    # 2. Low Number Emphasis - Based on number 5 success
    # Focus on numbers 1-20 with some balance
    low_emphasis_freq = {n: freq for n, freq in number_freq.most_common() if n <= 20}
    low_emphasis_numbers = list(low_emphasis_freq.keys())[:10]
    
    low_emphasis_combo = random.sample(low_emphasis_numbers, 4)
    # Add one higher number for balance
    high_balance = [n for n in range(30, 45) if number_freq[n] >= 4]
    if high_balance:
        low_emphasis_combo.append(random.choice(high_balance))
    
    combinations.append({
        'numbers': sorted(low_emphasis_combo),
        'lucky': 2,  # Frequently appearing lucky
        'strategy': 'Low Number Emphasis',
        'logic': 'Focus on 1-20 range where number 5 proved successful'
    })
    
    # 3. Mid-Range Recovery - Address the missing 25
    # Stronger focus on 17-33 range
    mid_range_focus = [n for n in range(17, 34) if number_freq[n] >= 2]
    mid_range_combo = random.sample(mid_range_focus, 3)
    
    # Add flanking numbers
    low_flank = [n for n in range(10, 17) if number_freq[n] >= 3]
    high_flank = [n for n in range(34, 42) if number_freq[n] >= 3]
    
    if low_flank:
        mid_range_combo.append(random.choice(low_flank))
    if high_flank:
        mid_range_combo.append(random.choice(high_flank))
    
    combinations.append({
        'numbers': sorted(mid_range_combo),
        'lucky': 6,  # Mid-range lucky number
        'strategy': 'Mid-Range Recovery',
        'logic': 'Stronger 17-33 coverage to catch numbers like 25'
    })
    
    # 4. Spacing Pattern Optimization
    # Use mathematical spacing similar to latest winning spacings [7, 13, 9, 4]
    spacing_start = random.choice([n for n in range(3, 10) if number_freq[n] >= 4])
    target_spacings = [7, 11, 8, 6]  # Similar to winning pattern
    
    spacing_combo = [spacing_start]
    for spacing in target_spacings:
        next_num = spacing_combo[-1] + spacing
        if next_num <= 49:
            spacing_combo.append(next_num)
    
    # If we don't have 5 numbers, fill strategically
    while len(spacing_combo) < 5:
        remaining_candidates = [n for n in range(1, 50) if n not in spacing_combo and number_freq[n] >= 3]
        if remaining_candidates:
            spacing_combo.append(random.choice(remaining_candidates))
        else:
            break
    
    combinations.append({
        'numbers': sorted(spacing_combo[:5]),
        'lucky': 4,  # Lucky number with good frequency
        'strategy': 'Spacing Pattern Optimization',
        'logic': 'Mathematical spacing similar to winning pattern'
    })
    
    # 5. Hybrid Success Synthesis
    # Combine elements from our successful combinations
    # Take numbers that appeared in our 2-match combinations
    successful_numbers = [5, 12, 34, 38]  # Numbers we correctly predicted
    synthesis_combo = successful_numbers.copy()
    
    # Add one strategic number to complete the set
    complementary_candidates = [n for n in range(20, 30) if number_freq[n] >= 4 and n not in synthesis_combo]
    if complementary_candidates:
        synthesis_combo.append(random.choice(complementary_candidates))
    
    combinations.append({
        'numbers': sorted(synthesis_combo),
        'lucky': 8,  # High frequency lucky
        'strategy': 'Hybrid Success Synthesis',
        'logic': 'Builds on our successful number predictions'
    })
    
    return combinations

def generate_improved_fusion_combinations(base_combinations):
    """Generate 5 improved fusion combinations"""
    
    # Extract all unique numbers and lucky numbers
    all_numbers = set()
    all_lucky = []
    
    for combo in base_combinations:
        all_numbers.update(combo['numbers'])
        all_lucky.append(combo['lucky'])
    
    all_numbers = sorted(list(all_numbers))
    
    fusion_combinations = []
    
    # 1. Performance-Based Fusion
    # Emphasize numbers that performed well in our analysis
    high_performers = [5, 12, 34, 38]  # Our successful numbers
    performance_combo = high_performers.copy()
    
    # Add one number from base combinations
    remaining_from_base = [n for n in all_numbers if n not in performance_combo]
    if remaining_from_base:
        performance_combo.append(random.choice(remaining_from_base))
    
    fusion_combinations.append({
        'numbers': sorted(performance_combo),
        'lucky': 10,  # Latest winning lucky
        'strategy': 'Performance-Based Fusion',
        'logic': 'Combines our successful predictions with base strategy numbers'
    })
    
    # 2. Range-Optimized Fusion
    # Better range distribution than our previous attempts
    low_from_base = [n for n in all_numbers if n <= 16]
    mid_from_base = [n for n in all_numbers if 17 <= n <= 33]
    high_from_base = [n for n in all_numbers if n >= 34]
    
    range_optimized = []
    if len(low_from_base) >= 2:
        range_optimized.extend(random.sample(low_from_base, 2))
    if len(mid_from_base) >= 2:
        range_optimized.extend(random.sample(mid_from_base, 2))
    if len(high_from_base) >= 1:
        range_optimized.extend(random.sample(high_from_base, 1))
    
    # Fill to 5 if needed
    while len(range_optimized) < 5:
        remaining = [n for n in all_numbers if n not in range_optimized]
        if remaining:
            range_optimized.append(random.choice(remaining))
        else:
            break
    
    fusion_combinations.append({
        'numbers': sorted(range_optimized[:5]),
        'lucky': 2,  # Balanced lucky choice
        'strategy': 'Range-Optimized Fusion',
        'logic': 'Optimized range distribution from base combinations'
    })
    
    # 3. Frequency-Weight Fusion
    # Weight numbers by their frequency in base combinations
    frequency_count = Counter()
    for combo in base_combinations:
        for num in combo['numbers']:
            frequency_count[num] += 1
    
    # Take top frequent numbers from base combinations
    top_frequent = [num for num, freq in frequency_count.most_common(8)]
    freq_fusion = random.sample(top_frequent, min(5, len(top_frequent)))
    
    fusion_combinations.append({
        'numbers': sorted(freq_fusion),
        'lucky': max(set(all_lucky), key=all_lucky.count),  # Most frequent lucky
        'strategy': 'Frequency-Weight Fusion',
        'logic': 'Highest frequency numbers from base combinations'
    })
    
    # 4. Strategic Balance Fusion
    # Balance between different strategy types from base
    strategic_balance = []
    
    # Take one number from each base combination
    for i, combo in enumerate(base_combinations):
        if len(strategic_balance) < 5:
            available_numbers = [n for n in combo['numbers'] if n not in strategic_balance]
            if available_numbers:
                strategic_balance.append(random.choice(available_numbers))
    
    fusion_combinations.append({
        'numbers': sorted(strategic_balance),
        'lucky': 6,  # Median lucky choice
        'strategy': 'Strategic Balance Fusion',
        'logic': 'Balances elements from all base strategies'
    })
    
    # 5. Gap-Filling Fusion
    # Target number ranges we missed in previous analysis
    gap_filling = []
    
    # Prioritize mid-range (where we missed 25)
    mid_range_base = [n for n in all_numbers if 20 <= n <= 30]
    if mid_range_base:
        gap_filling.extend(random.sample(mid_range_base, min(3, len(mid_range_base))))
    
    # Fill with strategic numbers from other ranges
    other_ranges = [n for n in all_numbers if n not in gap_filling]
    gap_filling.extend(random.sample(other_ranges, 5 - len(gap_filling)))
    
    fusion_combinations.append({
        'numbers': sorted(gap_filling[:5]),
        'lucky': 4,  # Strategic lucky choice
        'strategy': 'Gap-Filling Fusion',
        'logic': 'Targets ranges we missed in previous predictions'
    })
    
    return fusion_combinations

def main():
    print("IMPROVED 10 COMBINATIONS BASED ON PERFORMANCE INSIGHTS")
    print("=" * 56)
    
    # Generate base Time Series combinations
    base_combinations = generate_improved_time_series_combinations()
    
    print("5 IMPROVED TIME SERIES COMBINATIONS:")
    print("-" * 36)
    for i, combo in enumerate(base_combinations, 1):
        print(f"{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} + Lucky: {combo['lucky']}")
        print(f"   Logic: {combo['logic']}")
        print()
    
    # Generate improved fusion combinations
    fusion_combinations = generate_improved_fusion_combinations(base_combinations)
    
    print("5 IMPROVED FUSION COMBINATIONS:")
    print("-" * 31)
    for i, combo in enumerate(fusion_combinations, 6):
        print(f"{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} + Lucky: {combo['lucky']}")
        print(f"   Logic: {combo['logic']}")
        print()
    
    print("KEY IMPROVEMENTS APPLIED:")
    print("-" * 24)
    print("✓ Enhanced mid-range coverage (17-33) to catch numbers like 25")
    print("✓ Low number emphasis strategy based on number 5 success")
    print("✓ Inclusion of Lucky 10 (latest winner)")
    print("✓ Better range balance in fusion combinations")
    print("✓ Performance-based fusion using our successful predictions")
    print("✓ Mathematical spacing patterns similar to winning draw")

if __name__ == "__main__":
    main()