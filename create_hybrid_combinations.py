"""
Create 4 hybrid Euromillions combinations that mix elements from both sets.
"""
import random

# Define the two sets of combinations we generated
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

def create_hybrid_combination(set1, set2):
    """
    Create a hybrid combination by combining elements from both sets.
    
    Args:
        set1: First set of combinations
        set2: Second set of combinations
        
    Returns:
        dict: New hybrid combination
    """
    # Choose 2 combinations, one from each set
    combo1 = random.choice(set1)
    combo2 = random.choice(set2)
    
    # Take some numbers from each
    num_from_first = random.randint(2, 3)
    selected_from_first = random.sample(combo1['numbers'], num_from_first)
    
    # Take remaining from second
    remaining_needed = 5 - len(selected_from_first)
    available_from_second = [n for n in combo2['numbers'] if n not in selected_from_first]
    
    if len(available_from_second) >= remaining_needed:
        selected_from_second = random.sample(available_from_second, remaining_needed)
    else:
        # If not enough numbers in combo2, take all available and fill the rest
        selected_from_second = available_from_second
        
        # Fill remaining from other combinations in set2
        still_needed = 5 - len(selected_from_first) - len(selected_from_second)
        if still_needed > 0:
            all_set2_numbers = []
            for c in set2:
                all_set2_numbers.extend(c['numbers'])
            
            # Remove numbers already selected
            available_numbers = [n for n in set(all_set2_numbers) 
                               if n not in selected_from_first and n not in selected_from_second]
            
            if available_numbers and still_needed > 0:
                selected_from_second.extend(random.sample(available_numbers, min(still_needed, len(available_numbers))))
    
    # If we still need numbers, use any valid number
    all_selected = selected_from_first + selected_from_second
    while len(all_selected) < 5:
        available = [n for n in range(1, 51) if n not in all_selected]
        if available:
            all_selected.append(random.choice(available))
        else:
            break
    
    # For stars, take one from each set
    selected_stars = []
    
    # Take one star from first combination
    selected_stars.append(random.choice(combo1['stars']))
    
    # Take one star from second combination, ensuring it's different
    available_stars = [s for s in combo2['stars'] if s not in selected_stars]
    if available_stars:
        selected_stars.append(random.choice(available_stars))
    else:
        # If no stars available from combo2, use one from another combo
        other_stars = []
        for c in set2:
            other_stars.extend(c['stars'])
        
        available_stars = [s for s in set(other_stars) if s not in selected_stars]
        if available_stars:
            selected_stars.append(random.choice(available_stars))
        else:
            # If somehow we still need a star, use any valid one
            available = [s for s in range(1, 13) if s not in selected_stars]
            if available:
                selected_stars.append(random.choice(available))
    
    # Create a strategy name that reflects the hybrid nature
    strategy1 = combo1['strategy'].split(' ')[0]  # Get first word of strategy
    strategy2 = combo2['strategy'].split(' ')[0]  # Get first word of strategy
    
    strategy_name = f"Hybrid {strategy1}-{strategy2}"
    
    return {
        'numbers': sorted(all_selected),
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
    # Check each combination against the others
    for i in range(len(combinations)):
        for j in range(i):
            # Check if numbers and stars are the same
            if set(combinations[i]['numbers']) == set(combinations[j]['numbers']) and \
               set(combinations[i]['stars']) == set(combinations[j]['stars']):
                # Need to modify combination i
                numbers = list(combinations[i]['numbers'])
                
                # Replace 1-2 numbers
                num_to_replace = random.randint(1, 2)
                indices_to_replace = random.sample(range(5), num_to_replace)
                
                for idx in indices_to_replace:
                    # Find available numbers
                    available = [n for n in range(1, 51) if n not in numbers]
                    if available:
                        numbers[idx] = random.choice(available)
                
                # Update the combination
                combinations[i]['numbers'] = sorted(numbers)
                
                # If numbers are still the same, change stars too
                if set(combinations[i]['numbers']) == set(combinations[j]['numbers']):
                    stars = list(combinations[i]['stars'])
                    
                    # Replace one star
                    idx_to_replace = random.randint(0, 1)
                    
                    # Find available stars
                    available = [s for s in range(1, 13) if s not in stars]
                    if available:
                        stars[idx_to_replace] = random.choice(available)
                    
                    # Update the combination
                    combinations[i]['stars'] = sorted(stars)
    
    return combinations

def main():
    """Generate 4 hybrid Euromillions combinations"""
    print("Generating 4 hybrid Euromillions combinations...")
    
    # Create hybrid combinations
    hybrid_combinations = []
    
    for _ in range(4):
        hybrid_combinations.append(create_hybrid_combination(first_set, second_set))
    
    # Ensure uniqueness
    hybrid_combinations = ensure_uniqueness(hybrid_combinations)
    
    # Print results
    print("\n4 Hybrid Euromillions Combinations:")
    for i, combo in enumerate(hybrid_combinations, 1):
        print(f"{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']}")
        print(f"   Stars: {combo['stars']}")
        print()
    
    return hybrid_combinations

if __name__ == "__main__":
    main()