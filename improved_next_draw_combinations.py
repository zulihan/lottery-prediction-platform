"""
Generate 10 improved combinations for next Euromillions draw
Applied learnings: Mid-range focus, consecutive pairs, true fusion, balanced distribution
"""

def generate_improved_combinations():
    """Generate 10 combinations applying lessons learned from June 6 analysis"""
    
    # Lessons learned:
    # 1. Mid-range (18-35) was dominant in winners
    # 2. Consecutive pairs appeared: (20,21), (29,30)
    # 3. Historical high numbers (44,23,50,38,19) over-represented
    # 4. True fusion needed, not independent generation
    # 5. Stars 2 and 12 both won
    
    combinations = [
        # 1. Mid-Range Consecutive Focus
        {
            'numbers': [19, 20, 26, 31, 35],
            'stars': [2, 12],
            'strategy': 'Mid-Range Consecutive Focus',
            'logic': 'Strong mid-range with consecutive pair potential + winning stars'
        },
        
        # 2. Balanced Range + Patterns
        {
            'numbers': [22, 23, 28, 33, 42],
            'stars': [7, 12],
            'strategy': 'Balanced Range Pattern',
            'logic': 'Mix of frequent (23) with mid-range emphasis + mathematical spacing'
        },
        
        # 3. True Fusion: June 6 Element Extraction
        {
            'numbers': [18, 21, 29, 32, 36],
            'stars': [2, 8],
            'strategy': 'June 6 Element Fusion',
            'logic': 'Extracts successful elements: 21, 29 from winners + mid-range neighbors'
        },
        
        # 4. Consecutive Pair Strategy
        {
            'numbers': [24, 25, 30, 34, 41],
            'stars': [12, 3],
            'strategy': 'Consecutive Pair Strategy',
            'logic': 'Consecutive pairs (24,25) + mid-range focus + balanced high number'
        },
        
        # 5. Mid-Range Mathematical
        {
            'numbers': [17, 22, 27, 32, 37],
            'stars': [2, 7],
            'strategy': 'Mid-Range Mathematical',
            'logic': 'Mathematical progression by 5 in winning range + frequent stars'
        },
        
        # 6. Even-Odd Balance Mid-Range
        {
            'numbers': [20, 25, 28, 31, 34],
            'stars': [12, 5],
            'strategy': 'Even-Odd Balance Mid-Range',
            'logic': '3 odd, 2 even like June 6 pattern + strong mid-range coverage'
        },
        
        # 7. Hybrid: Frequent + Mid-Range
        {
            'numbers': [19, 23, 26, 29, 44],
            'stars': [2, 9],
            'strategy': 'Hybrid Frequent + Mid-Range',
            'logic': 'Balances historical frequent (23,19,44) with mid-range (26,29)'
        },
        
        # 8. True Fusion: Pattern + Range Elements
        {
            'numbers': [16, 21, 30, 35, 43],
            'stars': [7, 12],
            'strategy': 'Pattern + Range Fusion',
            'logic': 'Fuses elements from best June 6 performers + range balance'
        },
        
        # 9. Consecutive + Gap Coverage
        {
            'numbers': [14, 27, 28, 33, 39],
            'stars': [2, 8],
            'strategy': 'Consecutive + Gap Coverage',
            'logic': 'Consecutive (27,28) + covers underrepresented ranges'
        },
        
        # 10. Ultimate Mid-Range Synthesis
        {
            'numbers': [21, 24, 29, 32, 38],
            'stars': [12, 7],
            'strategy': 'Ultimate Mid-Range Synthesis',
            'logic': 'Synthesizes June 6 winners (21,29) with balanced mid-range pattern'
        }
    ]
    
    return combinations

def validate_improved_strategy(combinations):
    """Validate the improved combinations against learned principles"""
    
    print("VALIDATION AGAINST LEARNED PRINCIPLES")
    print("=" * 38)
    
    # Count mid-range numbers (18-35)
    total_mid_range = 0
    total_consecutive_pairs = 0
    total_numbers = 0
    star_12_usage = 0
    star_2_usage = 0
    
    for combo in combinations:
        numbers = combo['numbers']
        stars = combo['stars']
        
        # Mid-range count
        mid_range_count = len([n for n in numbers if 18 <= n <= 35])
        total_mid_range += mid_range_count
        total_numbers += 5
        
        # Consecutive pairs
        consecutive_count = 0
        for i in range(len(numbers) - 1):
            if numbers[i+1] - numbers[i] == 1:
                consecutive_count += 1
        total_consecutive_pairs += consecutive_count
        
        # Star analysis
        if 12 in stars:
            star_12_usage += 1
        if 2 in stars:
            star_2_usage += 1
    
    mid_range_percentage = (total_mid_range / total_numbers) * 100
    star_12_percentage = (star_12_usage / len(combinations)) * 100
    star_2_percentage = (star_2_usage / len(combinations)) * 100
    
    print(f"Mid-range (18-35) coverage: {total_mid_range}/{total_numbers} numbers ({mid_range_percentage:.1f}%)")
    print(f"Consecutive pairs total: {total_consecutive_pairs}")
    print(f"Star 12 usage: {star_12_usage}/{len(combinations)} combinations ({star_12_percentage:.0f}%)")
    print(f"Star 2 usage: {star_2_usage}/{len(combinations)} combinations ({star_2_percentage:.0f}%)")
    
    # Improvement metrics
    print(f"\nIMPROVEMENT METRICS:")
    print(f"✓ Mid-range focus: {'STRONG' if mid_range_percentage >= 60 else 'WEAK'}")
    print(f"✓ Consecutive coverage: {'GOOD' if total_consecutive_pairs >= 3 else 'LIMITED'}")
    print(f"✓ Winning stars integration: {'EXCELLENT' if star_12_percentage >= 70 and star_2_percentage >= 50 else 'MODERATE'}")

def analyze_vs_june_6_patterns(combinations):
    """Analyze how combinations align with June 6 winning patterns"""
    
    june_6_winners = [20, 21, 29, 30, 35]
    june_6_stars = [2, 12]
    
    print(f"\nJUNE 6 PATTERN ALIGNMENT")
    print("=" * 25)
    
    for i, combo in enumerate(combinations, 1):
        # Check for June 6 winner integration
        winner_overlap = len(set(combo['numbers']) & set(june_6_winners))
        star_overlap = len(set(combo['stars']) & set(june_6_stars))
        
        # Check for consecutive pairs like June 6
        consecutive_pairs = []
        numbers = sorted(combo['numbers'])
        for j in range(len(numbers) - 1):
            if numbers[j+1] - numbers[j] == 1:
                consecutive_pairs.append((numbers[j], numbers[j+1]))
        
        # Range analysis like June 6 (4 mid-range, 1 high)
        mid_range = [n for n in combo['numbers'] if 18 <= n <= 35]
        high_range = [n for n in combo['numbers'] if 36 <= n <= 50]
        
        pattern_score = 0
        if len(mid_range) >= 3:  # Strong mid-range like June 6
            pattern_score += 2
        if len(consecutive_pairs) > 0:  # Has consecutive pairs
            pattern_score += 2
        if star_overlap >= 1:  # Uses winning stars
            pattern_score += 1
        
        print(f"Combo {i:2d}: Pattern score {pattern_score}/5 - {len(mid_range)} mid-range, {len(consecutive_pairs)} consecutive pairs")

def display_improved_combinations():
    """Display the 10 improved combinations with analysis"""
    
    combinations = generate_improved_combinations()
    
    print("IMPROVED COMBINATIONS FOR NEXT EUROMILLIONS DRAW")
    print("Applied Learnings from June 6, 2025 Analysis")
    print("=" * 55)
    
    for i, combo in enumerate(combinations, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print(f"    Logic: {combo['logic']}")
        
        # Quick analysis
        mid_range_count = len([n for n in combo['numbers'] if 18 <= n <= 35])
        has_consecutive = any(combo['numbers'][j+1] - combo['numbers'][j] == 1 
                            for j in range(len(combo['numbers']) - 1))
        uses_winning_stars = bool(set(combo['stars']) & {2, 12})
        
        features = []
        if mid_range_count >= 3:
            features.append(f"{mid_range_count} mid-range")
        if has_consecutive:
            features.append("consecutive")
        if uses_winning_stars:
            features.append("winning stars")
        
        print(f"    Features: {', '.join(features) if features else 'balanced'}")
        print()
    
    validate_improved_strategy(combinations)
    analyze_vs_june_6_patterns(combinations)
    
    print(f"\nKEY IMPROVEMENTS APPLIED:")
    print(f"• Shifted focus from high numbers to mid-range (18-35)")
    print(f"• Incorporated consecutive number pairs strategy")
    print(f"• Used winning stars 2 and 12 frequently")
    print(f"• Created true fusions using successful elements")
    print(f"• Reduced over-reliance on historical frequency")
    print(f"• Maintained mathematical balance and pattern diversity")
    
    return combinations

def main():
    display_improved_combinations()

if __name__ == "__main__":
    main()