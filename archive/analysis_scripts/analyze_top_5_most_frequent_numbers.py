"""
Analyze the 5 numbers that appear most frequently across all 69 combinations
"""

def get_all_69_combinations():
    """Get all 69 combinations (20 initial + 39 ultimate + 10 fusion)"""
    
    # Initial 20 corrected combinations
    initial_20 = [
        [12, 15, 38, 47, 49], [23, 44, 19, 50, 21], [47, 29, 15, 49, 23],
        [10, 44, 50, 42, 37], [15, 38, 23, 44, 19], [23, 44, 50, 45, 47],
        [23, 44, 19, 16, 48], [23, 32, 39, 42, 46], [23, 44, 19, 10, 37],
        [12, 38, 23, 44, 19], [23, 44, 19, 12, 38], [50, 49, 48, 16, 29],
        [32, 39, 42, 10, 37], [47, 15, 12, 23, 44], [12, 23, 50, 38, 44],
        [23, 44, 1, 2, 3], [10, 12, 44, 15, 23], [2, 23, 30, 37, 44],
        [12, 15, 38, 23, 44], [15, 23, 19, 44, 38]
    ]
    
    # Ultimate 39 combinations
    ultimate_39 = [
        [12, 15, 38, 47, 48], [3, 23, 37, 44, 50], [1, 19, 29, 42, 49],
        [8, 15, 25, 38, 45], [10, 21, 27, 44, 47], [6, 17, 32, 39, 46],
        [4, 14, 24, 34, 44], [7, 20, 33, 41, 48], [12, 23, 38, 44, 50],
        [2, 19, 29, 45, 49], [10, 20, 30, 40, 50], [15, 21, 25, 37, 43],
        [5, 11, 17, 23, 29], [1, 19, 27, 42, 48], [9, 24, 35, 44, 47],
        [13, 22, 31, 39, 46], [16, 26, 36, 41, 50], [18, 28, 33, 38, 49],
        [23, 44, 19, 50, 21], [10, 37, 29, 42, 25], [20, 27, 17, 15, 38],
        [23, 19, 21, 37, 42], [44, 50, 10, 29, 25], [23, 44, 37, 27, 15],
        [19, 50, 21, 20, 38], [10, 42, 25, 17, 29], [23, 50, 37, 20, 15],
        [44, 19, 21, 27, 38], [1, 8, 43, 47, 50], [2, 6, 44, 48, 49],
        [3, 7, 45, 46, 50], [4, 5, 43, 47, 48], [1, 9, 44, 49, 50],
        [2, 10, 45, 46, 47], [3, 8, 43, 48, 49], [4, 6, 44, 46, 50],
        [5, 7, 45, 47, 48], [1, 10, 43, 46, 49], [2, 9, 44, 45, 50]
    ]
    
    # Fusion Mix 10 combinations
    fusion_10 = [
        [12, 15, 23, 44, 47], [1, 19, 38, 46, 50], [21, 29, 37, 42, 49],
        [15, 38, 44, 48, 50], [10, 23, 27, 39, 44], [6, 17, 25, 33, 41],
        [3, 19, 29, 45, 48], [8, 16, 24, 32, 40], [12, 20, 28, 36, 44],
        [11, 22, 33, 44, 47]
    ]
    
    return initial_20 + ultimate_39 + fusion_10

def count_number_frequencies():
    """Count frequency of each number across all 69 combinations"""
    
    all_combinations = get_all_69_combinations()
    frequency_count = {}
    
    # Count each number across all combinations
    for combination in all_combinations:
        for number in combination:
            frequency_count[number] = frequency_count.get(number, 0) + 1
    
    # Sort by frequency (highest first)
    sorted_frequencies = sorted(frequency_count.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_frequencies, len(all_combinations)

def analyze_top_5_numbers():
    """Analyze the top 5 most frequent numbers"""
    
    frequencies, total_combinations = count_number_frequencies()
    top_5 = frequencies[:5]
    
    print("🔍 TOP 5 MOST FREQUENT NUMBERS ACROSS ALL 69 COMBINATIONS")
    print("=" * 60)
    print(f"Analysis based on {total_combinations} total combinations")
    print()
    
    print("RANKING:")
    print("-" * 8)
    for i, (number, count) in enumerate(top_5, 1):
        percentage = (count / total_combinations) * 100
        print(f"{i}. Number {number:2d}: appears {count:2d} times ({percentage:4.1f}% of combinations)")
    
    print()
    print("FREQUENCY DISTRIBUTION:")
    print("-" * 22)
    
    # Show all numbers with their frequencies for context
    for number, count in frequencies:
        percentage = (count / total_combinations) * 100
        if count >= 5:  # Show numbers appearing 5+ times
            stars = "★" * min(5, count // 3)  # Visual indicator
            print(f"Number {number:2d}: {count:2d} times ({percentage:4.1f}%) {stars}")
    
    print()
    print("TOP 5 ANALYSIS:")
    print("-" * 14)
    top_5_numbers = [num for num, count in top_5]
    print(f"The 5 most frequent numbers: {top_5_numbers}")
    
    # Analyze ranges
    low_range = len([n for n in top_5_numbers if 1 <= n <= 17])
    mid_range = len([n for n in top_5_numbers if 18 <= n <= 33])
    high_range = len([n for n in top_5_numbers if 34 <= n <= 50])
    
    print(f"Range distribution:")
    print(f"  Low range (1-17): {low_range} numbers")
    print(f"  Mid range (18-33): {mid_range} numbers")
    print(f"  High range (34-50): {high_range} numbers")
    
    # Check if they match historical frequent numbers
    historical_top_5 = [23, 44, 19, 50, 21]  # From 1845 draws analysis
    matches = len(set(top_5_numbers) & set(historical_top_5))
    
    print(f"Historical alignment: {matches}/5 match historical top frequent numbers")
    print(f"Historical top 5: {historical_top_5}")
    
    # Check June 3 integration
    june_3_numbers = [12, 15, 38, 47, 48]
    june_3_matches = len(set(top_5_numbers) & set(june_3_numbers))
    print(f"June 3 integration: {june_3_matches}/5 are June 3 winning numbers")
    
    return top_5_numbers

def show_combinations_with_top_5():
    """Show which combinations contain the most of the top 5 numbers"""
    
    top_5_numbers = analyze_top_5_numbers()
    all_combinations = get_all_69_combinations()
    
    print()
    print("COMBINATIONS WITH MOST TOP 5 NUMBERS:")
    print("-" * 37)
    
    combination_scores = []
    for i, combo in enumerate(all_combinations):
        score = len(set(combo) & set(top_5_numbers))
        combination_scores.append((i + 1, combo, score))
    
    # Sort by score (highest first)
    combination_scores.sort(key=lambda x: x[2], reverse=True)
    
    # Show top scoring combinations
    max_score = combination_scores[0][2]
    print(f"Maximum possible matches: 5")
    print(f"Highest actual matches: {max_score}")
    print()
    
    for combo_num, combo, score in combination_scores[:10]:  # Show top 10
        if score >= 3:  # Only show combinations with 3+ matches
            matched_numbers = set(combo) & set(top_5_numbers)
            print(f"Combo {combo_num:2d}: {combo} - {score}/5 matches {sorted(list(matched_numbers))}")
    
    return top_5_numbers

def main():
    show_combinations_with_top_5()

if __name__ == "__main__":
    main()