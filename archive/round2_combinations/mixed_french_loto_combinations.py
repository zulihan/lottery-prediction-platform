"""
Generate 5 mixed French Loto combinations by combining elements from the 20 corrected combinations.
"""
import random

# Define the 20 corrected combinations
corrected_combinations = [
    {'numbers': [2, 13, 30, 43, 48], 'strategy': 'Hybrid Mix Strategy', 'lucky_number': 9},
    {'numbers': [8, 20, 28, 30, 42], 'strategy': 'Hybrid Mix Strategy', 'lucky_number': 4},
    {'numbers': [20, 21, 34, 42, 43], 'strategy': 'Hybrid Mix Strategy', 'lucky_number': 6},
    {'numbers': [8, 30, 33, 34, 36], 'strategy': 'Hybrid Mix Strategy', 'lucky_number': 4},
    {'numbers': [8, 28, 30, 36, 42], 'strategy': 'Hybrid Mix Strategy', 'lucky_number': 6},
    {'numbers': [8, 37, 41, 42, 44], 'strategy': 'High Risk Strategy', 'lucky_number': 3},
    {'numbers': [8, 21, 23, 40, 43], 'strategy': 'High Risk Strategy', 'lucky_number': 9},
    {'numbers': [14, 21, 33, 42, 43], 'strategy': 'High Risk Strategy', 'lucky_number': 4},
    {'numbers': [8, 33, 37, 42, 47], 'strategy': 'High Risk Strategy', 'lucky_number': 10},
    {'numbers': [26, 33, 42, 43, 44], 'strategy': 'Sequential Pattern Strategy', 'lucky_number': 4},
    {'numbers': [6, 30, 39, 40, 43], 'strategy': 'Sequential Pattern Strategy', 'lucky_number': 4},
    {'numbers': [7, 8, 14, 31, 42], 'strategy': 'Sequential Pattern Strategy', 'lucky_number': 4},
    {'numbers': [15, 21, 23, 30, 34], 'strategy': 'Cold Numbers Focus', 'lucky_number': 2},
    {'numbers': [5, 18, 21, 23, 38], 'strategy': 'Cold Numbers Focus', 'lucky_number': 6},
    {'numbers': [15, 22, 23, 33, 42], 'strategy': 'Balanced Mix Strategy', 'lucky_number': 9},
    {'numbers': [2, 8, 28, 39, 42], 'strategy': 'Balanced Mix Strategy', 'lucky_number': 6},
    {'numbers': [12, 18, 42, 43, 46], 'strategy': 'High Range Focus', 'lucky_number': 10},
    {'numbers': [8, 13, 36, 38, 40], 'strategy': 'High Range Focus', 'lucky_number': 8},
    {'numbers': [3, 6, 18, 36, 38], 'strategy': 'Even Numbers Focus', 'lucky_number': 6},
    {'numbers': [8, 15, 26, 43, 48], 'strategy': 'Even Numbers Focus', 'lucky_number': 2}
]

def create_mixed_combination():
    """
    Create a mixed combination using elements from multiple combinations.
    
    Returns:
        dict: A new mixed combination
    """
    # Choose 2-3 combinations to mix
    num_to_mix = random.randint(2, 3)
    source_combos = random.sample(corrected_combinations, num_to_mix)
    
    # Strategy for selecting numbers from each combination
    numbers_from_each = 5 // num_to_mix
    extra_numbers = 5 % num_to_mix
    
    mixed_numbers = []
    for i, combo in enumerate(source_combos):
        # Take numbers from this combination
        numbers_to_take = numbers_from_each
        if i < extra_numbers:
            numbers_to_take += 1
        
        # Randomly select numbers from this combination
        available_numbers = [n for n in combo['numbers'] if n not in mixed_numbers]
        if len(available_numbers) >= numbers_to_take:
            selected = random.sample(available_numbers, numbers_to_take)
            mixed_numbers.extend(selected)
        else:
            # If not enough unique numbers available, take what we can
            mixed_numbers.extend(available_numbers)
    
    # If we don't have 5 numbers yet, add more from other combinations
    while len(mixed_numbers) < 5:
        other_combos = [c for c in corrected_combinations if c not in source_combos]
        if not other_combos:
            break
        
        combo = random.choice(other_combos)
        source_combos.append(combo)  # Add to source combos to avoid re-selection
        
        available_numbers = [n for n in combo['numbers'] if n not in mixed_numbers]
        if available_numbers:
            mixed_numbers.append(random.choice(available_numbers))
    
    # If we still don't have 5 numbers, generate random ones
    while len(mixed_numbers) < 5:
        available = [n for n in range(1, 50) if n not in mixed_numbers]
        if available:
            mixed_numbers.append(random.choice(available))
        else:
            break  # This should never happen
    
    # For lucky number, choose one from the source combinations
    lucky_source = random.choice(source_combos)
    lucky_number = lucky_source['lucky_number']
    
    # Create strategy name from the source strategies
    strategy_names = [c['strategy'].split(' ')[0] for c in source_combos]
    unique_strategies = list(set(strategy_names))  # Remove duplicates
    strategy_name = "Mixed " + "-".join(unique_strategies)
    
    return {
        'numbers': sorted(mixed_numbers),
        'lucky_number': lucky_number,
        'strategy': strategy_name
    }

def ensure_uniqueness(combinations):
    """
    Ensure all combinations are unique.
    
    Args:
        combinations: List of combinations to check and make unique
        
    Returns:
        list: List of unique combinations
    """
    # Check each combination against the others and against original combinations
    all_combinations = corrected_combinations.copy()
    
    for i in range(len(combinations)):
        num_set = frozenset(combinations[i]['numbers'])
        
        # Check against original combinations
        for combo in all_combinations:
            if frozenset(combo['numbers']) == num_set:
                # Need to recreate this combination
                combinations[i] = create_mixed_combination()
                # Update the set for next comparisons
                num_set = frozenset(combinations[i]['numbers'])
        
        # Check against other new combinations
        for j in range(i):
            if frozenset(combinations[j]['numbers']) == num_set:
                # Need to recreate this combination
                combinations[i] = create_mixed_combination()
                # Update the set for next comparisons
                num_set = frozenset(combinations[i]['numbers'])
        
        # Add to the full set for later checks
        all_combinations.append(combinations[i])
    
    return combinations

def main():
    """Generate 5 mixed French Loto combinations"""
    print("Generating 5 mixed French Loto combinations for May 21, 2025...")
    
    # Create mixed combinations
    mixed_combinations = []
    for _ in range(5):
        mixed_combinations.append(create_mixed_combination())
    
    # Ensure uniqueness
    mixed_combinations = ensure_uniqueness(mixed_combinations)
    
    # Print the results
    print("\n5 Mixed French Loto Combinations for May 21, 2025:")
    for i, combo in enumerate(mixed_combinations, 1):
        numbers_str = ", ".join(map(str, combo['numbers']))
        print(f"{i}. {combo['strategy']}")
        print(f"   Numbers: {numbers_str} | Lucky Number: {combo['lucky_number']}")
        print()
    
    return mixed_combinations

if __name__ == "__main__":
    main()