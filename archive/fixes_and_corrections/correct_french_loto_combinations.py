"""
Generate correct French Loto combinations with proper lucky number range (1-10)
"""
import random

# Original combinations with the erroneous lucky numbers
original_combinations = [
    {'numbers': [2, 13, 30, 43, 48], 'strategy': 'Hybrid Mix Strategy', 'lucky_number': 9},
    {'numbers': [8, 20, 28, 30, 42], 'strategy': 'Hybrid Mix Strategy', 'lucky_number': 4},
    {'numbers': [20, 21, 34, 42, 43], 'strategy': 'Hybrid Mix Strategy', 'lucky_number': 6},
    {'numbers': [8, 30, 33, 34, 36], 'strategy': 'Hybrid Mix Strategy', 'lucky_number': 4},
    {'numbers': [8, 28, 30, 36, 42], 'strategy': 'Hybrid Mix Strategy', 'lucky_number': 6},
    {'numbers': [8, 37, 41, 42, 44], 'strategy': 'High Risk Strategy', 'lucky_number': 3},
    {'numbers': [8, 21, 23, 40, 43], 'strategy': 'High Risk Strategy', 'lucky_number': 25},  # Invalid
    {'numbers': [14, 21, 33, 42, 43], 'strategy': 'High Risk Strategy', 'lucky_number': 4},
    {'numbers': [8, 33, 37, 42, 47], 'strategy': 'High Risk Strategy', 'lucky_number': 10},
    {'numbers': [26, 33, 42, 43, 44], 'strategy': 'Sequential Pattern Strategy', 'lucky_number': 4},
    {'numbers': [6, 30, 39, 40, 43], 'strategy': 'Sequential Pattern Strategy', 'lucky_number': 4},
    {'numbers': [7, 8, 14, 31, 42], 'strategy': 'Sequential Pattern Strategy', 'lucky_number': 4},
    {'numbers': [15, 21, 23, 30, 34], 'strategy': 'Cold Numbers Focus', 'lucky_number': 2},
    {'numbers': [5, 18, 21, 23, 38], 'strategy': 'Cold Numbers Focus', 'lucky_number': 22},  # Invalid
    {'numbers': [15, 22, 23, 33, 42], 'strategy': 'Balanced Mix Strategy', 'lucky_number': 9},
    {'numbers': [2, 8, 28, 39, 42], 'strategy': 'Balanced Mix Strategy', 'lucky_number': 6},
    {'numbers': [12, 18, 42, 43, 46], 'strategy': 'High Range Focus', 'lucky_number': 10},
    {'numbers': [8, 13, 36, 38, 40], 'strategy': 'High Range Focus', 'lucky_number': 8},
    {'numbers': [3, 6, 18, 36, 38], 'strategy': 'Even Numbers Focus', 'lucky_number': 6},
    {'numbers': [8, 15, 26, 43, 48], 'strategy': 'Even Numbers Focus', 'lucky_number': 2},
]

def correct_lucky_numbers(combinations):
    """
    Correct any invalid lucky numbers (outside 1-10 range) in the combinations.
    
    Args:
        combinations: List of combination dictionaries
        
    Returns:
        list: List of corrected combinations
    """
    corrected_combinations = []
    
    for combo in combinations:
        corrected_combo = combo.copy()
        
        # Check if lucky number is outside valid range
        if combo['lucky_number'] < 1 or combo['lucky_number'] > 10:
            # Replace with a valid lucky number
            corrected_combo['lucky_number'] = random.randint(1, 10)
            print(f"Fixed: Changed lucky number from {combo['lucky_number']} to {corrected_combo['lucky_number']} "
                 f"for combination {combo['numbers']}")
        
        corrected_combinations.append(corrected_combo)
    
    return corrected_combinations

def main():
    """Correct and display the French Loto combinations"""
    print("Correcting French Loto combinations with proper lucky number range (1-10)...")
    
    corrected_combinations = correct_lucky_numbers(original_combinations)
    
    # Print corrected combinations
    print("\nCorrected French Loto Combinations for May 21, 2025:")
    
    # Group combinations by strategy
    strategies = {}
    for combo in corrected_combinations:
        if combo['strategy'] not in strategies:
            strategies[combo['strategy']] = []
        strategies[combo['strategy']].append(combo)
    
    # Print by strategy group
    for strategy, combos in strategies.items():
        print(f"\n{strategy} Combinations:")
        for i, combo in enumerate(combos, 1):
            numbers_str = ", ".join(map(str, combo['numbers']))
            print(f"  Numbers: {numbers_str} | Lucky Number: {combo['lucky_number']}")
    
    return corrected_combinations

if __name__ == "__main__":
    main()