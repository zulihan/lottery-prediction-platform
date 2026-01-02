"""
Generate 10 diverse Euromillions combinations for the next draw
with minimal overlap with recent drawings.
"""
import random
import numpy as np
from collections import Counter

# Define the most recent Euromillions drawing
last_drawing = {
    'numbers': [6, 9, 25, 37, 46],
    'stars': [6, 12]
}

# Define additional recent drawings (would normally be from database)
recent_drawings = [
    {'numbers': [6, 9, 25, 37, 46], 'stars': [6, 12]},  # May 13
    {'numbers': [15, 21, 28, 35, 43], 'stars': [3, 9]}, # May 9
    {'numbers': [3, 7, 12, 24, 33], 'stars': [8, 11]}   # May 6
]

def get_hot_cold_numbers():
    """Get hot and cold numbers based on simulated historical data"""
    # In a real implementation, this would come from a database of all drawings
    # Here we're simulating historical frequencies with fixed lists
    
    # Hot numbers (drawn frequently in the past 3 months)
    hot_numbers = [3, 5, 7, 9, 15, 17, 19, 20, 21, 24, 27, 33, 37, 42, 44]
    
    # Medium frequency numbers
    medium_numbers = [1, 2, 8, 10, 12, 16, 23, 26, 28, 31, 35, 38, 39, 41, 43, 48, 49]
    
    # Cold numbers (drawn less frequently)
    cold_numbers = [4, 6, 11, 13, 14, 18, 22, 25, 29, 30, 32, 34, 36, 40, 45, 46, 47, 50]
    
    # Hot stars (drawn frequently)
    hot_stars = [2, 3, 8, 9]
    
    # Medium frequency stars
    medium_stars = [1, 6, 7, 10]
    
    # Cold stars (drawn less frequently)
    cold_stars = [4, 5, 11, 12]
    
    return {
        'hot_numbers': hot_numbers,
        'medium_numbers': medium_numbers,
        'cold_numbers': cold_numbers,
        'hot_stars': hot_stars,
        'medium_stars': medium_stars,
        'cold_stars': cold_stars
    }

def get_avoided_numbers(recent_drawings, emphasis=0.8):
    """
    Generate a list of numbers to avoid based on recent drawings.
    
    Args:
        recent_drawings: List of recent drawing dictionaries
        emphasis: How strongly to avoid (0-1), 1 means complete avoidance
        
    Returns:
        tuple: (avoid_list, reduced_probability_list)
    """
    if not recent_drawings:
        return [], []
    
    # Flatten all recent numbers
    recent_numbers = []
    recent_stars = []
    for drawing in recent_drawings:
        recent_numbers.extend(drawing['numbers'])
        recent_stars.extend(drawing['stars'])
    
    # Count occurrences
    number_counts = Counter(recent_numbers)
    star_counts = Counter(recent_stars)
    
    # Numbers appearing multiple times are strongly avoided
    strongly_avoid_numbers = [num for num, count in number_counts.items() if count > 1]
    strongly_avoid_stars = [star for star, count in star_counts.items() if count > 1]
    
    # Numbers appearing once have reduced probability based on emphasis
    if random.random() < emphasis:
        # Strong avoidance - most recent numbers not included
        avoid_list_numbers = list(number_counts.keys())
        reduced_list_numbers = []
        
        avoid_list_stars = list(star_counts.keys())
        reduced_list_stars = []
    else:
        # Moderate avoidance - only strongly avoid repeated numbers
        avoid_list_numbers = strongly_avoid_numbers
        reduced_list_numbers = [num for num, count in number_counts.items() 
                                if count == 1 and num not in strongly_avoid_numbers]
        
        avoid_list_stars = strongly_avoid_stars
        reduced_list_stars = [star for star, count in star_counts.items() 
                            if count == 1 and star not in strongly_avoid_stars]
    
    return {
        'avoid_numbers': avoid_list_numbers,
        'reduced_prob_numbers': reduced_list_numbers,
        'avoid_stars': avoid_list_stars,
        'reduced_prob_stars': reduced_list_stars
    }

def create_diverse_combination(hot_cold_data, avoid_data, strategy_name):
    """
    Create a diverse combination that avoids recently drawn numbers.
    
    Args:
        hot_cold_data: Dictionary with hot/cold numbers data
        avoid_data: Dictionary with numbers to avoid/reduce
        strategy_name: Name of the strategy
        
    Returns:
        dict: Generated combination
    """
    # Extract data
    avoid_numbers = avoid_data['avoid_numbers']
    reduced_prob_numbers = avoid_data['reduced_prob_numbers']
    avoid_stars = avoid_data['avoid_stars']
    reduced_prob_stars = avoid_data['reduced_prob_stars']
    
    # Available number pools excluding avoided numbers
    available_hot = [n for n in hot_cold_data['hot_numbers'] if n not in avoid_numbers]
    available_medium = [n for n in hot_cold_data['medium_numbers'] if n not in avoid_numbers]
    available_cold = [n for n in hot_cold_data['cold_numbers'] if n not in avoid_numbers]
    
    # Apply strategy-specific distributions
    if "Hot" in strategy_name:
        hot_weight = 0.6
        medium_weight = 0.3
        cold_weight = 0.1
    elif "Cold" in strategy_name:
        hot_weight = 0.1
        medium_weight = 0.3
        cold_weight = 0.6
    elif "Balanced" in strategy_name:
        hot_weight = 0.33
        medium_weight = 0.34
        cold_weight = 0.33
    elif "Overdue" in strategy_name:
        # Focus on cold and medium numbers
        hot_weight = 0.1
        medium_weight = 0.4
        cold_weight = 0.5
    elif "Range" in strategy_name:
        # For range-based strategies, set weights based on specific range
        if "High" in strategy_name:
            hot_weight = 0.2
            medium_weight = 0.3
            cold_weight = 0.5  # More cold numbers include high values
        elif "Low" in strategy_name:
            hot_weight = 0.5  # More hot numbers include low values
            medium_weight = 0.3
            cold_weight = 0.2
        else:
            hot_weight = 0.33
            medium_weight = 0.34
            cold_weight = 0.33
    elif "Even" in strategy_name:
        # For even/odd strategies, we'll set weights normally 
        # and filter for even/odd later
        hot_weight = 0.33
        medium_weight = 0.34
        cold_weight = 0.33
    else:
        # Default balanced distribution
        hot_weight = 0.33
        medium_weight = 0.34
        cold_weight = 0.33
    
    # Determine number of numbers to select from each category
    # based on weights and randomness
    total_needed = 5
    expected_hot = int(total_needed * hot_weight)
    expected_medium = int(total_needed * medium_weight)
    expected_cold = total_needed - expected_hot - expected_medium
    
    # Add some randomness while maintaining approximate weights
    adjustment = random.randint(-1, 1)
    if adjustment != 0:
        # Adjust hot numbers
        expected_hot += adjustment
        # Keep within bounds
        expected_hot = max(0, min(5, expected_hot))
        # Adjust others to compensate
        remaining = total_needed - expected_hot
        expected_medium = int(remaining * (medium_weight / (medium_weight + cold_weight)))
        expected_cold = remaining - expected_medium
    
    # Generate the combination using the selected distribution
    selected_numbers = []
    
    # Select numbers from each category
    if available_hot and expected_hot > 0:
        selected_numbers.extend(random.sample(available_hot, min(expected_hot, len(available_hot))))
    
    if available_medium and expected_medium > 0:
        selected_numbers.extend(random.sample(available_medium, min(expected_medium, len(available_medium))))
    
    if available_cold and expected_cold > 0:
        selected_numbers.extend(random.sample(available_cold, min(expected_cold, len(available_cold))))
    
    # If we don't have enough, try including reduced probability numbers
    if len(selected_numbers) < 5:
        remaining_needed = 5 - len(selected_numbers)
        available_reduced = [n for n in reduced_prob_numbers if n not in selected_numbers]
        
        if available_reduced:
            # Only use some of the reduced probability numbers
            num_to_use = min(remaining_needed, len(available_reduced), 2)  # Max 2 recent numbers
            selected_numbers.extend(random.sample(available_reduced, num_to_use))
    
    # If we still need more, use any valid number
    if len(selected_numbers) < 5:
        remaining_needed = 5 - len(selected_numbers)
        all_available = [n for n in range(1, 51) if n not in selected_numbers and n not in avoid_numbers]
        
        if all_available:
            selected_numbers.extend(random.sample(all_available, min(remaining_needed, len(all_available))))
    
    # If we somehow still don't have 5 numbers, use any valid number
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 51) if n not in selected_numbers]
        if available:
            selected_numbers.append(random.choice(available))
        else:
            break  # This should never happen
    
    # Apply special strategy modifiers for certain strategies
    if "Even" in strategy_name:
        # Try to ensure more even numbers for Even strategies
        # or more odd numbers for Odd strategies
        current_even = len([n for n in selected_numbers if n % 2 == 0])
        target_even = 3 if "Even" in strategy_name else 2
        
        if current_even != target_even and len(selected_numbers) == 5:
            # We need to adjust the even/odd balance
            if current_even < target_even:
                # Need more even numbers
                odd_indices = [i for i, n in enumerate(selected_numbers) if n % 2 == 1]
                if odd_indices:
                    # Replace one odd number with an even one
                    idx_to_replace = random.choice(odd_indices)
                    # Find available even numbers not in avoid list
                    available_even = [n for n in range(2, 51, 2) 
                                    if n not in selected_numbers 
                                    and n not in avoid_numbers]
                    if available_even:
                        selected_numbers[idx_to_replace] = random.choice(available_even)
            else:
                # Need more odd numbers
                even_indices = [i for i, n in enumerate(selected_numbers) if n % 2 == 0]
                if even_indices:
                    # Replace one even number with an odd one
                    idx_to_replace = random.choice(even_indices)
                    # Find available odd numbers not in avoid list
                    available_odd = [n for n in range(1, 51, 2) 
                                    if n not in selected_numbers 
                                    and n not in avoid_numbers]
                    if available_odd:
                        selected_numbers[idx_to_replace] = random.choice(available_odd)
    
    elif "Range" in strategy_name:
        # Adjust for range-specific strategies
        if "High" in strategy_name:
            # Ensure more high range numbers (35-50)
            high_count = len([n for n in selected_numbers if n >= 35])
            target_high = 3  # Want at least 3 high numbers
            
            if high_count < target_high and len(selected_numbers) == 5:
                # Replace some low numbers with high ones
                low_indices = [i for i, n in enumerate(selected_numbers) if n < 35]
                if low_indices:
                    # How many to replace
                    to_replace = min(target_high - high_count, len(low_indices))
                    for _ in range(to_replace):
                        idx = random.choice(low_indices)
                        low_indices.remove(idx)
                        
                        # Find available high numbers
                        available_high = [n for n in range(35, 51) 
                                         if n not in selected_numbers 
                                         and n not in avoid_numbers]
                        if available_high:
                            selected_numbers[idx] = random.choice(available_high)
        
        elif "Low" in strategy_name:
            # Ensure more low range numbers (1-20)
            low_count = len([n for n in selected_numbers if n <= 20])
            target_low = 3  # Want at least 3 low numbers
            
            if low_count < target_low and len(selected_numbers) == 5:
                # Replace some high numbers with low ones
                high_indices = [i for i, n in enumerate(selected_numbers) if n > 20]
                if high_indices:
                    # How many to replace
                    to_replace = min(target_low - low_count, len(high_indices))
                    for _ in range(to_replace):
                        idx = random.choice(high_indices)
                        high_indices.remove(idx)
                        
                        # Find available low numbers
                        available_low = [n for n in range(1, 21) 
                                       if n not in selected_numbers 
                                       and n not in avoid_numbers]
                        if available_low:
                            selected_numbers[idx] = random.choice(available_low)
    
    elif "Sum" in strategy_name:
        # Adjust for sum-related strategies
        current_sum = sum(selected_numbers)
        
        if "Low Sum" in strategy_name and current_sum > 100:
            # Try to replace one high number with a lower one
            highest_idx = selected_numbers.index(max(selected_numbers))
            available_low = [n for n in range(1, 31) 
                           if n not in selected_numbers 
                           and n not in avoid_numbers]
            if available_low:
                selected_numbers[highest_idx] = random.choice(available_low)
        
        elif "High Sum" in strategy_name and current_sum < 120:
            # Try to replace one low number with a higher one
            lowest_idx = selected_numbers.index(min(selected_numbers))
            available_high = [n for n in range(30, 51) 
                             if n not in selected_numbers 
                             and n not in avoid_numbers]
            if available_high:
                selected_numbers[lowest_idx] = random.choice(available_high)
    
    # Select stars
    # Available star pools excluding avoided stars
    available_hot_stars = [s for s in hot_cold_data['hot_stars'] if s not in avoid_stars]
    available_medium_stars = [s for s in hot_cold_data['medium_stars'] if s not in avoid_stars]
    available_cold_stars = [s for s in hot_cold_data['cold_stars'] if s not in avoid_stars]
    
    selected_stars = []
    
    # Strategy-specific star selection
    if "Hot" in strategy_name:
        # Prefer hot stars
        if available_hot_stars:
            selected_stars.append(random.choice(available_hot_stars))
        
        # Second star from medium or cold, with preference for medium
        if available_medium_stars:
            remaining_medium = [s for s in available_medium_stars if s not in selected_stars]
            if remaining_medium:
                selected_stars.append(random.choice(remaining_medium))
        
        if len(selected_stars) < 2 and available_cold_stars:
            remaining_cold = [s for s in available_cold_stars if s not in selected_stars]
            if remaining_cold:
                selected_stars.append(random.choice(remaining_cold))
    
    elif "Cold" in strategy_name or "Overdue" in strategy_name:
        # Prefer cold stars
        if available_cold_stars:
            selected_stars.append(random.choice(available_cold_stars))
        
        # Second star from medium or hot, with preference for medium
        if available_medium_stars:
            remaining_medium = [s for s in available_medium_stars if s not in selected_stars]
            if remaining_medium:
                selected_stars.append(random.choice(remaining_medium))
        
        if len(selected_stars) < 2 and available_hot_stars:
            remaining_hot = [s for s in available_hot_stars if s not in selected_stars]
            if remaining_hot:
                selected_stars.append(random.choice(remaining_hot))
    
    else:
        # Balanced approach - one hot/medium and one cold/medium
        star_sources = []
        
        if available_hot_stars:
            star_sources.append(('hot', available_hot_stars))
        
        if available_medium_stars:
            star_sources.append(('medium', available_medium_stars))
        
        if available_cold_stars:
            star_sources.append(('cold', available_cold_stars))
        
        if len(star_sources) >= 2:
            # Select 2 different sources
            selected_sources = random.sample(star_sources, 2)
            
            for source_type, source_list in selected_sources:
                if source_list:  # Should always be true here
                    selected_stars.append(random.choice(source_list))
                    
                    # Remove the selected star from other source lists
                    for other_type, other_list in selected_sources:
                        if other_type != source_type and selected_stars[-1] in other_list:
                            other_list.remove(selected_stars[-1])
    
    # If we still don't have 2 stars, use reduced probability stars
    if len(selected_stars) < 2:
        available_reduced = [s for s in reduced_prob_stars if s not in selected_stars]
        
        if available_reduced:
            # Only use some of the reduced probability stars
            num_to_use = min(2 - len(selected_stars), len(available_reduced), 1)  # Max 1 recent star
            selected_stars.extend(random.sample(available_reduced, num_to_use))
    
    # If we still need more, use any valid star
    if len(selected_stars) < 2:
        all_available = [s for s in range(1, 13) if s not in selected_stars and s not in avoid_stars]
        
        if all_available:
            selected_stars.extend(random.sample(all_available, min(2 - len(selected_stars), len(all_available))))
    
    # If we somehow still don't have 2 stars, use any valid star
    while len(selected_stars) < 2:
        available = [s for s in range(1, 13) if s not in selected_stars]
        if available:
            selected_stars.append(random.choice(available))
        else:
            break  # This should never happen
    
    # Calculate score based on strategy and attributes
    # Base score
    score = 85
    
    # Bonus for avoiding recent numbers
    recent_numbers_used = len([n for n in selected_numbers if n in avoid_data['avoid_numbers']])
    recent_stars_used = len([s for s in selected_stars if s in avoid_data['avoid_stars']])
    
    # Penalize for using recent numbers/stars
    score -= recent_numbers_used * 3
    score -= recent_stars_used * 2
    
    # Strategy-specific adjustments
    if ("Hot" in strategy_name and hot_weight > 0.5) or \
       ("Cold" in strategy_name and cold_weight > 0.5) or \
       ("Balanced" in strategy_name) or \
       ("Range" in strategy_name) or \
       ("Even" in strategy_name):
        # Strategies aligned with their goals get bonuses
        score += 5
    
    # Final score between 0 and 100
    score = max(0, min(100, score))
    
    return {
        'numbers': sorted(selected_numbers),
        'stars': sorted(selected_stars),
        'strategy': strategy_name,
        'score': score
    }

def ensure_unique_combinations(combinations):
    """
    Ensure all combinations are unique.
    
    Args:
        combinations: List of combination dictionaries
        
    Returns:
        list: List of unique combinations
    """
    # Extract number and star sets
    for i in range(len(combinations)):
        # Check for duplicates with previous combinations
        for j in range(i):
            # Both numbers and stars need to match to be considered a duplicate
            if set(combinations[i]['numbers']) == set(combinations[j]['numbers']) and \
               set(combinations[i]['stars']) == set(combinations[j]['stars']):
                # Need to modify combination i
                # Change 1-2 numbers
                numbers = combinations[i]['numbers'].copy()
                
                # Remove 1-2 numbers
                num_to_change = random.randint(1, 2)
                indices_to_change = random.sample(range(len(numbers)), num_to_change)
                
                # Find numbers not in any combination
                all_used_numbers = set()
                for combo in combinations:
                    all_used_numbers.update(combo['numbers'])
                
                available_numbers = [n for n in range(1, 51) if n not in all_used_numbers]
                
                # If there are no completely unused numbers, use any that aren't in this combo
                if not available_numbers:
                    available_numbers = [n for n in range(1, 51) if n not in numbers]
                
                # Replace the selected numbers
                if available_numbers:
                    for idx in indices_to_change:
                        if available_numbers:
                            replacement = random.choice(available_numbers)
                            numbers[idx] = replacement
                            available_numbers.remove(replacement)
                
                # Update the combination
                combinations[i]['numbers'] = sorted(numbers)
                
                # If we still have a duplicate, change a star too
                if set(combinations[i]['numbers']) == set(combinations[j]['numbers']):
                    stars = combinations[i]['stars'].copy()
                    
                    # Change one star
                    idx_to_change = random.randint(0, 1)
                    
                    # Find stars not used in this combination
                    available_stars = [s for s in range(1, 13) if s not in stars]
                    
                    if available_stars:
                        stars[idx_to_change] = random.choice(available_stars)
                    
                    # Update the combination
                    combinations[i]['stars'] = sorted(stars)
    
    return combinations

def main():
    """Generate 10 diverse Euromillions combinations"""
    print("Generating diverse Euromillions combinations...")
    
    # Get hot/cold data
    hot_cold_data = get_hot_cold_numbers()
    
    # Get numbers to avoid from recent drawings
    avoid_data = get_avoided_numbers(recent_drawings, emphasis=0.75)
    
    print(f"Numbers to avoid from recent drawings: {avoid_data['avoid_numbers']}")
    print(f"Stars to avoid from recent drawings: {avoid_data['avoid_stars']}")
    
    # Define diverse strategies
    strategies = [
        "Diverse Hot Numbers Strategy",
        "Diverse Cold Numbers Strategy",
        "Diverse Balanced Mix Strategy",
        "Diverse High Range Strategy",
        "Diverse Low Range Strategy",
        "Diverse Even Numbers Strategy",
        "Diverse Low Sum Strategy",
        "Diverse Overdue Numbers Strategy",
        "Diverse Hot-Cold Balance Strategy",
        "Diverse Optimized Coverage Strategy"
    ]
    
    # Generate combinations
    combinations = []
    
    for strategy in strategies:
        combination = create_diverse_combination(hot_cold_data, avoid_data, strategy)
        combinations.append(combination)
    
    # Ensure all combinations are unique
    combinations = ensure_unique_combinations(combinations)
    
    # Sort by score
    combinations.sort(key=lambda x: x['score'], reverse=True)
    
    # Print results
    print("\n10 Diverse Euromillions Combinations:")
    for i, combo in enumerate(combinations, 1):
        print(f"{i}. Strategy: {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']}")
        print(f"   Stars: {combo['stars']}")
        print(f"   Score: {combo['score']:.1f}")
        print()
    
    return combinations

if __name__ == "__main__":
    main()