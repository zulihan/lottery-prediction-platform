"""
Generate 10 improved combinations for next Euromillions draw
"""

def generate_next_draw_combinations():
    """Generate 10 combinations applying June 6 lessons"""
    
    combinations = [
        # 1. Mid-Range Consecutive Focus
        {
            'numbers': [19, 20, 26, 31, 35],
            'stars': [2, 12],
            'strategy': 'Mid-Range Consecutive Focus'
        },
        
        # 2. Balanced Range Pattern
        {
            'numbers': [22, 23, 28, 33, 42],
            'stars': [7, 12],
            'strategy': 'Balanced Range Pattern'
        },
        
        # 3. June 6 Element Fusion
        {
            'numbers': [18, 21, 29, 32, 36],
            'stars': [2, 8],
            'strategy': 'June 6 Element Fusion'
        },
        
        # 4. Consecutive Pair Strategy
        {
            'numbers': [24, 25, 30, 34, 41],
            'stars': [12, 3],
            'strategy': 'Consecutive Pair Strategy'
        },
        
        # 5. Mid-Range Mathematical
        {
            'numbers': [17, 22, 27, 32, 37],
            'stars': [2, 7],
            'strategy': 'Mid-Range Mathematical'
        },
        
        # 6. Even-Odd Balance Mid-Range
        {
            'numbers': [20, 25, 28, 31, 34],
            'stars': [12, 5],
            'strategy': 'Even-Odd Balance Mid-Range'
        },
        
        # 7. Hybrid Frequent + Mid-Range
        {
            'numbers': [19, 23, 26, 29, 44],
            'stars': [2, 9],
            'strategy': 'Hybrid Frequent + Mid-Range'
        },
        
        # 8. Pattern + Range Fusion
        {
            'numbers': [16, 21, 30, 35, 43],
            'stars': [7, 12],
            'strategy': 'Pattern + Range Fusion'
        },
        
        # 9. Consecutive + Gap Coverage
        {
            'numbers': [14, 27, 28, 33, 39],
            'stars': [2, 8],
            'strategy': 'Consecutive + Gap Coverage'
        },
        
        # 10. Ultimate Mid-Range Synthesis
        {
            'numbers': [21, 24, 29, 32, 38],
            'stars': [12, 7],
            'strategy': 'Ultimate Mid-Range Synthesis'
        }
    ]
    
    return combinations

def main():
    combinations = generate_next_draw_combinations()
    
    print("10 IMPROVED COMBINATIONS FOR NEXT EUROMILLIONS DRAW")
    print("Applied learnings from June 6, 2025 analysis")
    print("=" * 55)
    
    for i, combo in enumerate(combinations, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
    
    # Analysis
    total_mid_range = 0
    consecutive_pairs = 0
    star_12_usage = 0
    star_2_usage = 0
    
    for combo in combinations:
        mid_range_count = len([n for n in combo['numbers'] if 18 <= n <= 35])
        total_mid_range += mid_range_count
        
        numbers = sorted(combo['numbers'])
        for j in range(len(numbers) - 1):
            if numbers[j+1] - numbers[j] == 1:
                consecutive_pairs += 1
                break
        
        if 12 in combo['stars']:
            star_12_usage += 1
        if 2 in combo['stars']:
            star_2_usage += 1
    
    print(f"\nSTRATEGY IMPROVEMENTS APPLIED:")
    print(f"Mid-range (18-35) focus: {total_mid_range}/50 numbers ({(total_mid_range/50)*100:.0f}%)")
    print(f"Consecutive pairs: {consecutive_pairs}/10 combinations")
    print(f"Star 12 usage: {star_12_usage}/10 combinations")
    print(f"Star 2 usage: {star_2_usage}/10 combinations")
    
    print(f"\nKEY CHANGES FROM PREVIOUS STRATEGY:")
    print(f"• Shifted from high numbers (44,23,50) to mid-range focus")
    print(f"• Added consecutive number pairs like June 6 winners (20,21) (29,30)")
    print(f"• Integrated winning stars 2 and 12 frequently")
    print(f"• Reduced historical frequency over-reliance")
    print(f"• Created true fusions using successful elements")

if __name__ == "__main__":
    main()