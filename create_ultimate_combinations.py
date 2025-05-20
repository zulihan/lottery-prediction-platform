"""
Create 3 ultimate Euromillions combinations by mixing elements from all three sets.
"""
import random

# Define the three sets of combinations
first_set = [
    {'numbers': [1, 2, 11, 14, 37], 'stars': [3, 7], 'strategy': 'Overdue Numbers'},
    {'numbers': [2, 31, 39, 40, 47], 'stars': [5, 8], 'strategy': 'Overdue Numbers'},
    {'numbers': [3, 14, 31, 39, 40], 'stars': [3, 7], 'strategy': 'Overdue Numbers'},
    {'numbers': [3, 21, 37, 44, 50], 'stars': [7, 9], 'strategy': 'Risk-Reward (0.2)'},
    {'numbers': [9, 21, 27, 44, 50], 'stars': [2, 11], 'strategy': 'Risk-Reward (0.2)'},
    {'numbers': [3, 19, 37, 38, 44], 'stars': [2, 10], 'strategy': 'Risk-Reward (0.2)'},
    {'numbers': [3, 19, 37, 44, 46], 'stars': [2, 12], 'strategy': 'Risk-Reward (0.2)'},
    {'numbers': [3, 19, 21, 44, 50], 'stars': [2, 4], 'strategy': 'Risk-Reward (0.2)'},
    {'numbers': [9, 19, 21, 44, 46], 'stars': [9, 11], 'strategy': 'Risk-Reward (0.2)'},
    {'numbers': [6, 16, 31, 35, 39], 'stars': [2, 9], 'strategy': 'Balanced Strategy'}
]

second_set = [
    {'numbers': [17, 20, 32, 38, 44], 'stars': [2, 10], 'strategy': 'Hot Numbers Strategy'},
    {'numbers': [4, 34, 36, 41, 45], 'stars': [5, 7], 'strategy': 'Cold Numbers Strategy'},
    {'numbers': [10, 16, 30, 45, 50], 'stars': [2, 10], 'strategy': 'Balanced Mix Strategy'},
    {'numbers': [1, 20, 36, 40, 50], 'stars': [1, 2], 'strategy': 'High Range Strategy'},
    {'numbers': [10, 19, 20, 39, 42], 'stars': [2, 5], 'strategy': 'Low Range Strategy'},
    {'numbers': [4, 16, 19, 40, 49], 'stars': [2, 5], 'strategy': 'Even Numbers Strategy'},
    {'numbers': [14, 19, 27, 42, 44], 'stars': [1, 2], 'strategy': 'Hot-Cold Balance Strategy'},
    {'numbers': [17, 22, 29, 34, 38], 'stars': [2, 10], 'strategy': 'Low Sum Strategy'},
    {'numbers': [22, 32, 38, 44, 45], 'stars': [4, 10], 'strategy': 'Overdue Numbers Strategy'},
    {'numbers': [1, 18, 29, 31, 34], 'stars': [2, 7], 'strategy': 'Optimized Coverage Strategy'}
]

third_set = [
    {'numbers': [4, 21, 36, 37, 50], 'stars': [7, 9], 'strategy': 'Hybrid Risk-Reward-Cold Strategy'},
    {'numbers': [14, 29, 31, 34, 40], 'stars': [3, 7], 'strategy': 'Hybrid Overdue-Optimized Strategy'},
    {'numbers': [9, 22, 27, 38, 44], 'stars': [10, 11], 'strategy': 'Hybrid Risk-Reward-Low Strategy'},
    {'numbers': [2, 14, 37, 38, 44], 'stars': [3, 4], 'strategy': 'Hybrid Overdue-Overdue Strategy'}
]

def create_ultimate_combination():
    """
    Create an ultimate combination by taking elements from all three sets.
    
    Returns:
        dict: Ultimate combination
    """
    # Choose one combination from each set
    combo1 = random.choice(first_set)
    combo2 = random.choice(second_set)
    combo3 = random.choice(third_set)
    
    # Take numbers from each set with different weights
    # First set: 2 numbers (analysis-based)
    # Second set: 1 number (diverse)
    # Third set: 1 number (hybrid)
    # The fifth number will be chosen from all three sets' numbers
    
    selected_numbers = []
    
    # Take 2 numbers from first set
    selected_from_first = random.sample(combo1['numbers'], 2)
    selected_numbers.extend(selected_from_first)
    
    # Take 1 number from second set
    available_from_second = [n for n in combo2['numbers'] if n not in selected_numbers]
    if available_from_second:
        selected_from_second = random.sample(available_from_second, 1)
        selected_numbers.extend(selected_from_second)
    
    # Take 1 number from third set
    available_from_third = [n for n in combo3['numbers'] if n not in selected_numbers]
    if available_from_third:
        selected_from_third = random.sample(available_from_third, 1)
        selected_numbers.extend(selected_from_third)
    
    # For the fifth number, gather all numbers from the three sets
    all_possible_numbers = set()
    for combo in first_set + second_set + third_set:
        all_possible_numbers.update(combo['numbers'])
    
    # Remove already selected numbers
    available_numbers = [n for n in all_possible_numbers if n not in selected_numbers]
    
    # Add one more number
    if available_numbers:
        selected_numbers.append(random.choice(available_numbers))
    
    # If we somehow still don't have 5 numbers, add random ones
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 51) if n not in selected_numbers]
        if available:
            selected_numbers.append(random.choice(available))
        else:
            break
    
    # For stars, take one star from two different sets
    star_sources = [combo1['stars'], combo2['stars'], combo3['stars']]
    source_indices = random.sample(range(3), 2)  # Select 2 different sources
    
    selected_stars = []
    selected_stars.append(random.choice(star_sources[source_indices[0]]))
    
    # Ensure the second star is different from the first
    second_source = star_sources[source_indices[1]]
    available_stars = [s for s in second_source if s != selected_stars[0]]
    
    if available_stars:
        selected_stars.append(random.choice(available_stars))
    else:
        # If no different stars in the second source, use any valid star
        all_possible_stars = set()
        for combo in first_set + second_set + third_set:
            all_possible_stars.update(combo['stars'])
        
        available_stars = [s for s in all_possible_stars if s not in selected_stars]
        if available_stars:
            selected_stars.append(random.choice(available_stars))
        else:
            # If somehow we still need a star, use any valid one
            available = [s for s in range(1, 13) if s not in selected_stars]
            if available:
                selected_stars.append(random.choice(available))
    
    # Create a strategy name that reflects the ultimate nature
    strategies = [combo1['strategy'].split(' ')[0], 
                 combo2['strategy'].split(' ')[0], 
                 combo3['strategy'].split(' ')[0]]
    
    strategy_name = "Ultimate " + "-".join(strategies)
    
    return {
        'numbers': sorted(selected_numbers),
        'stars': sorted(selected_stars),
        'strategy': strategy_name
    }

def ensure_uniqueness(combinations):
    """
    Ensure all combinations are unique.
    
    Args:
        combinations: List of combination dictionaries
        
    Returns:
        list: List of unique combinations
    """
    all_combinations = first_set + second_set + third_set + combinations
    
    for i in range(len(combinations)):
        # Check if this combination matches any previous combination
        duplicate_found = False
        for j in range(i):
            if set(combinations[i]['numbers']) == set(combinations[j]['numbers']) and \
               set(combinations[i]['stars']) == set(combinations[j]['stars']):
                duplicate_found = True
                break
        
        # Also check against all previous sets
        for other_combo in first_set + second_set + third_set:
            if set(combinations[i]['numbers']) == set(other_combo['numbers']) and \
               set(combinations[i]['stars']) == set(other_combo['stars']):
                duplicate_found = True
                break
        
        if duplicate_found:
            # Need to create a new combination
            combinations[i] = create_ultimate_combination()
            
            # Check again (recursive call to ensure uniqueness)
            # But limit recursion to avoid infinite loop
            attempts = 0
            while duplicate_found and attempts < 5:
                duplicate_found = False
                
                for j in range(i):
                    if set(combinations[i]['numbers']) == set(combinations[j]['numbers']) and \
                       set(combinations[i]['stars']) == set(combinations[j]['stars']):
                        duplicate_found = True
                        break
                
                for other_combo in first_set + second_set + third_set:
                    if set(combinations[i]['numbers']) == set(other_combo['numbers']) and \
                       set(combinations[i]['stars']) == set(other_combo['stars']):
                        duplicate_found = True
                        break
                
                if duplicate_found:
                    combinations[i] = create_ultimate_combination()
                    attempts += 1
                
    return combinations

def main():
    """Generate 3 ultimate Euromillions combinations"""
    print("Generating 3 ultimate Euromillions combinations...")
    
    # Create ultimate combinations
    ultimate_combinations = []
    
    for _ in range(3):
        ultimate_combinations.append(create_ultimate_combination())
    
    # Ensure uniqueness
    ultimate_combinations = ensure_uniqueness(ultimate_combinations)
    
    # Print results
    print("\n3 Ultimate Euromillions Combinations:")
    for i, combo in enumerate(ultimate_combinations, 1):
        print(f"{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']}")
        print(f"   Stars: {combo['stars']}")
        print()
    
    return ultimate_combinations

if __name__ == "__main__":
    main()