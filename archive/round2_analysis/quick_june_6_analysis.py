"""
Quick analysis of June 6 results: 20, 21, 29, 30, 35 / 2, 12
"""

def analyze_june_6_results():
    """Analyze the results against our combinations"""
    
    # Actual results
    winning_numbers = [20, 21, 29, 30, 35]
    winning_stars = [2, 12]
    
    print("JUNE 6, 2025 EUROMILLIONS RESULTS: 20, 21, 29, 30, 35 / 2, 12")
    print("=" * 65)
    
    # The "Fusion Mastery" set that had all 5 numbers distributed
    fusion_mastery = [
        ([12, 23, 38, 44, 50], [7, 3], 'Fusion: Frequency + June 3'),
        ([2, 19, 29, 45, 49], [7, 5], 'Fusion: Extreme + Balance'),
        ([10, 20, 30, 40, 50], [7, 2], 'Fusion: Pattern + Range'),
        ([15, 21, 25, 37, 43], [7, 8], 'Fusion: Hot + Cold'),
        ([5, 11, 17, 23, 29], [7, 9], 'Fusion: Mathematical Progression'),
        ([1, 19, 27, 42, 48], [7, 12], 'Fusion: Coverage + Frequency'),
        ([9, 24, 35, 44, 47], [7, 3], 'Fusion: Recent + Historical'),
        ([13, 22, 31, 39, 46], [7, 2], 'Fusion: Multi-Strategy Synthesis'),
        ([16, 26, 36, 41, 50], [7, 8], 'Fusion: Performance Optimization'),
        ([18, 28, 33, 38, 49], [7, 5], 'Fusion: Ultimate Strategy')
    ]
    
    print("FUSION MASTERY SET ANALYSIS:")
    print("-" * 28)
    
    # Check each combination for matches
    best_matches = []
    all_numbers_in_set = set()
    
    for i, (numbers, stars, strategy) in enumerate(fusion_mastery, 1):
        all_numbers_in_set.update(numbers)
        
        number_matches = len(set(numbers) & set(winning_numbers))
        star_matches = len(set(stars) & set(winning_stars))
        total_score = number_matches + star_matches
        
        matched_nums = sorted(list(set(numbers) & set(winning_numbers)))
        matched_stars = sorted(list(set(stars) & set(winning_stars)))
        
        if total_score > 0:
            best_matches.append((i, strategy, total_score, matched_nums, matched_stars))
            print(f"Combo {i:2d}: {total_score} matches - {matched_nums} + {matched_stars}")
            print(f"         {strategy}")
    
    print(f"\nWINNING NUMBER COVERAGE:")
    print("-" * 24)
    coverage = set(winning_numbers) & all_numbers_in_set
    print(f"Numbers in Fusion Mastery set: {sorted(list(all_numbers_in_set))}")
    print(f"Winning numbers covered: {sorted(list(coverage))} ({len(coverage)}/5)")
    
    # Find which combinations had which winning numbers
    print(f"\nWINNING NUMBER DISTRIBUTION:")
    print("-" * 28)
    for win_num in winning_numbers:
        found_in = []
        for i, (numbers, stars, strategy) in enumerate(fusion_mastery, 1):
            if win_num in numbers:
                found_in.append(f"Combo {i}")
        print(f"Number {win_num}: {', '.join(found_in) if found_in else 'NOT FOUND'}")
    
    # Check stars
    print(f"\nSTAR ANALYSIS:")
    print("-" * 14)
    for win_star in winning_stars:
        found_in = []
        for i, (numbers, stars, strategy) in enumerate(fusion_mastery, 1):
            if win_star in stars:
                found_in.append(f"Combo {i}")
        print(f"Star {win_star}: {', '.join(found_in) if found_in else 'NOT FOUND'}")
    
    print(f"\nFUSION MASTERY REALITY CHECK:")
    print("-" * 29)
    print("The name 'Fusion Mastery' was misleading - these weren't fusions of the initial 20.")
    print("They were independently generated combinations using different strategic approaches.")
    print("This explains why they captured all 5 winning numbers - they weren't constrained")
    print("by the number patterns in the initial 20 combinations.")

if __name__ == "__main__":
    analyze_june_6_results()