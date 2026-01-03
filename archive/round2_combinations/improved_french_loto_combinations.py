"""
Generate 10 improved French Loto combinations applying Euromillions learnings
French Loto: 5 numbers (1-49) + 1 Lucky number (1-10)
"""

def get_latest_french_loto_data():
    """Get the latest French Loto results for pattern analysis"""
    # Based on recent draws analysis - you mentioned adding latest draw
    recent_results = [
        {'numbers': [8, 13, 25, 29, 36], 'lucky': 2, 'date': '2025-06-02'},
        {'numbers': [14, 32, 39, 45, 9], 'lucky': 9, 'date': '2025-05-24'},  
        {'numbers': [24, 33, 36, 41, 45], 'lucky': 7, 'date': '2025-05-26'},
        {'numbers': [7, 10, 11, 18, 49], 'lucky': 3, 'date': '2025-05-21'}
    ]
    return recent_results

def analyze_french_loto_patterns():
    """Analyze patterns in recent French Loto draws"""
    recent_draws = get_latest_french_loto_data()
    
    all_numbers = []
    all_lucky = []
    
    for draw in recent_draws:
        all_numbers.extend(draw['numbers'])
        all_lucky.append(draw['lucky'])
    
    # Range analysis for French Loto (1-49)
    low_range = [n for n in all_numbers if 1 <= n <= 16]
    mid_range = [n for n in all_numbers if 17 <= n <= 33] 
    high_range = [n for n in all_numbers if 34 <= n <= 49]
    
    print("FRENCH LOTO PATTERN ANALYSIS")
    print("=" * 29)
    print(f"Recent draws analyzed: {len(recent_draws)}")
    print(f"Low range (1-16): {len(low_range)} numbers")
    print(f"Mid range (17-33): {len(mid_range)} numbers") 
    print(f"High range (34-49): {len(high_range)} numbers")
    print(f"Lucky numbers used: {all_lucky}")
    
    # Check for consecutive patterns
    consecutive_count = 0
    for draw in recent_draws:
        numbers = sorted(draw['numbers'])
        for i in range(len(numbers) - 1):
            if numbers[i+1] - numbers[i] == 1:
                consecutive_count += 1
                break
    
    print(f"Draws with consecutive pairs: {consecutive_count}/{len(recent_draws)}")
    
    return {
        'mid_range_percentage': len(mid_range) / len(all_numbers) * 100,
        'consecutive_frequency': consecutive_count / len(recent_draws),
        'frequent_lucky': max(set(all_lucky), key=all_lucky.count),
        'range_balance': (len(low_range), len(mid_range), len(high_range))
    }

def generate_improved_french_loto():
    """Generate 10 improved French Loto combinations"""
    
    # Apply Euromillions learnings adapted for French Loto:
    # - Mid-range focus (17-33 for Loto vs 18-35 for Euromillions)
    # - Consecutive pairs emphasis
    # - Recent pattern integration
    # - Lucky number strategy based on frequency
    
    combinations = [
        # 1. Mid-Range Consecutive Focus
        {
            'numbers': [18, 19, 25, 31, 36],
            'lucky': 2,
            'strategy': 'Mid-Range Consecutive Focus',
            'logic': 'Consecutive pair (18,19) + mid-range emphasis + recent lucky 2'
        },
        
        # 2. Recent Pattern Fusion
        {
            'numbers': [13, 22, 29, 34, 41],
            'lucky': 7,
            'strategy': 'Recent Pattern Fusion',
            'logic': 'Integrates recent winners (13,29,41) with balanced distribution'
        },
        
        # 3. Balanced Range + Consecutive
        {
            'numbers': [16, 23, 24, 32, 38],
            'lucky': 3,
            'strategy': 'Balanced Range + Consecutive',
            'logic': 'Consecutive (23,24) + even distribution across ranges'
        },
        
        # 4. Mathematical Mid-Range
        {
            'numbers': [17, 21, 25, 29, 33],
            'lucky': 9,
            'strategy': 'Mathematical Mid-Range',
            'logic': 'Progression by 4 in mid-range + recent lucky winner'
        },
        
        # 5. Recent Winners Integration
        {
            'numbers': [8, 20, 25, 36, 45],
            'lucky': 2,
            'strategy': 'Recent Winners Integration',
            'logic': 'Uses recent winners (8,25,36,45) with mid-range balance'
        },
        
        # 6. Consecutive + Gap Coverage
        {
            'numbers': [11, 27, 28, 35, 42],
            'lucky': 7,
            'strategy': 'Consecutive + Gap Coverage',
            'logic': 'Consecutive (27,28) + covers underrepresented ranges'
        },
        
        # 7. Even-Odd Balance
        {
            'numbers': [14, 19, 26, 31, 40],
            'lucky': 3,
            'strategy': 'Even-Odd Balance',
            'logic': '3 odd, 2 even pattern + strategic range distribution'
        },
        
        # 8. High-Frequency Fusion
        {
            'numbers': [10, 18, 29, 33, 39],
            'lucky': 9,
            'strategy': 'High-Frequency Fusion',
            'logic': 'Combines historically frequent Loto numbers + recent patterns'
        },
        
        # 9. Pattern Synthesis
        {
            'numbers': [12, 21, 30, 37, 44],
            'lucky': 2,
            'strategy': 'Pattern Synthesis',
            'logic': 'Mathematical spacing + range balance + winning lucky'
        },
        
        # 10. Ultimate Range Optimization
        {
            'numbers': [15, 24, 28, 34, 43],
            'lucky': 7,
            'strategy': 'Ultimate Range Optimization',
            'logic': 'Optimized range coverage + recent draw insights'
        }
    ]
    
    return combinations

def validate_french_loto_strategy(combinations):
    """Validate the French Loto combinations against improved principles"""
    
    total_mid_range = 0
    consecutive_pairs = 0
    lucky_2_usage = 0
    lucky_7_usage = 0
    lucky_9_usage = 0
    
    for combo in combinations:
        # Mid-range count (17-33 for French Loto)
        mid_range_count = len([n for n in combo['numbers'] if 17 <= n <= 33])
        total_mid_range += mid_range_count
        
        # Consecutive pairs
        numbers = sorted(combo['numbers'])
        for i in range(len(numbers) - 1):
            if numbers[i+1] - numbers[i] == 1:
                consecutive_pairs += 1
                break
        
        # Lucky number frequency
        if combo['lucky'] == 2:
            lucky_2_usage += 1
        elif combo['lucky'] == 7:
            lucky_7_usage += 1
        elif combo['lucky'] == 9:
            lucky_9_usage += 1
    
    mid_range_percentage = (total_mid_range / 50) * 100
    
    print(f"\nFRENCH LOTO STRATEGY VALIDATION:")
    print(f"Mid-range (17-33) focus: {total_mid_range}/50 numbers ({mid_range_percentage:.0f}%)")
    print(f"Consecutive pairs: {consecutive_pairs}/10 combinations")
    print(f"Lucky number distribution:")
    print(f"  Lucky 2: {lucky_2_usage}/10 combinations")
    print(f"  Lucky 7: {lucky_7_usage}/10 combinations") 
    print(f"  Lucky 9: {lucky_9_usage}/10 combinations")

def display_french_loto_combinations():
    """Display the improved French Loto combinations"""
    
    print("10 IMPROVED FRENCH LOTO COMBINATIONS")
    print("Applied Euromillions learnings adapted for Loto format")
    print("=" * 52)
    
    patterns = analyze_french_loto_patterns()
    combinations = generate_improved_french_loto()
    
    for i, combo in enumerate(combinations, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        print(f"    Logic: {combo['logic']}")
        
        # Quick feature analysis
        mid_range_count = len([n for n in combo['numbers'] if 17 <= n <= 33])
        has_consecutive = any(combo['numbers'][j+1] - combo['numbers'][j] == 1 
                            for j in range(len(sorted(combo['numbers'])) - 1))
        
        features = []
        if mid_range_count >= 3:
            features.append(f"{mid_range_count} mid-range")
        if has_consecutive:
            features.append("consecutive")
        if combo['lucky'] in [2, 7, 9]:  # Recent frequent lucky numbers
            features.append("recent lucky")
        
        print(f"    Features: {', '.join(features) if features else 'balanced'}")
        print()
    
    validate_french_loto_strategy(combinations)
    
    print(f"\nKEY ADAPTATIONS FOR FRENCH LOTO:")
    print(f"• Mid-range focus adapted to 17-33 (Loto range 1-49 vs Euromillions 1-50)")
    print(f"• Lucky numbers based on recent draw frequency")
    print(f"• Consecutive pairs strategy maintained")
    print(f"• Recent winner integration from latest draws")
    print(f"• Balanced range distribution optimized for Loto")
    
    return combinations

def main():
    display_french_loto_combinations()

if __name__ == "__main__":
    main()