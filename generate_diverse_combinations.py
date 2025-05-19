"""
Generate 20 optimized French Loto combinations for the next draw
with reduced emphasis on recently drawn numbers.
"""
import random
import numpy as np
from collections import Counter
from database import get_session, GeneratedCombination, FrenchLotoDrawing
from sqlalchemy import desc
import json
from datetime import date, timedelta

def get_last_drawings(num_drawings=3):
    """Get the last few French Loto drawings"""
    session = get_session()
    try:
        recent_drawings = session.query(FrenchLotoDrawing) \
            .order_by(desc(FrenchLotoDrawing.date)) \
            .limit(num_drawings) \
            .all()
        
        results = []
        for drawing in recent_drawings:
            results.append({
                'date': drawing.date,
                'numbers': [drawing.n1, drawing.n2, drawing.n3, 
                           drawing.n4, drawing.n5],
                'lucky_number': drawing.lucky
            })
        
        return results
    finally:
        session.close()

def get_next_draw_date(last_draw_date):
    """Calculate the next draw date, assuming French Loto draws are on Monday, Wednesday, and Saturday"""
    # Days to next draw based on current day of week
    # Monday (0) -> Wednesday (2): +2 days
    # Wednesday (2) -> Saturday (5): +3 days
    # Saturday (5) -> Monday (0): +2 days
    weekday = last_draw_date.weekday()
    
    if weekday == 0:  # Monday
        days_to_add = 2  # Wednesday
    elif weekday == 2:  # Wednesday
        days_to_add = 3  # Saturday
    elif weekday == 5:  # Saturday
        days_to_add = 2  # Monday
    else:
        # Should not happen with regular draw schedule, add fallback
        if weekday < 2:  # Tuesday
            days_to_add = 2 - weekday  # To Wednesday
        elif weekday < 5:  # Thursday, Friday
            days_to_add = 5 - weekday  # To Saturday
        else:  # Sunday
            days_to_add = 1  # To Monday
    
    return last_draw_date + timedelta(days=days_to_add)

def get_hot_cold_numbers(recent_numbers):
    """Get hot and cold numbers from historical data, considering recent numbers less favorable"""
    session = get_session()
    try:
        # Get all drawings
        all_drawings = session.query(FrenchLotoDrawing).all()
        
        # Extract numbers and lucky numbers
        all_numbers = []
        all_lucky = []
        
        for drawing in all_drawings:
            all_numbers.extend([drawing.n1, drawing.n2, drawing.n3, drawing.n4, drawing.n5])
            all_lucky.append(drawing.lucky)
        
        # Count frequencies
        number_freq = Counter(all_numbers)
        lucky_freq = Counter(all_lucky)
        
        # Adjust frequencies to de-emphasize recent numbers
        # by reducing their count in the frequency calculation
        for num in recent_numbers:
            if num in number_freq and number_freq[num] > 2:
                number_freq[num] -= 2  # Reduce frequency to make them less likely
        
        # Get hot and cold numbers after adjustment
        hot_numbers = [n for n, _ in number_freq.most_common(15)]
        cold_numbers = [n for n, _ in sorted(number_freq.items(), key=lambda x: x[1])[:15]]
        
        # Get medium numbers (neither hot nor cold)
        medium_numbers = [n for n in range(1, 50) 
                         if n not in hot_numbers and n not in cold_numbers]
        
        # Get hot and cold lucky numbers
        hot_lucky = [n for n, _ in lucky_freq.most_common(3)]
        cold_lucky = [n for n, _ in sorted(lucky_freq.items(), key=lambda x: x[1])[:3]]
        medium_lucky = [n for n in range(1, 11) 
                       if n not in hot_lucky and n not in cold_lucky]
        
        return {
            'hot_numbers': hot_numbers,
            'medium_numbers': medium_numbers,
            'cold_numbers': cold_numbers,
            'hot_lucky': hot_lucky,
            'medium_lucky': medium_lucky,
            'cold_lucky': cold_lucky,
            'number_freq': dict(number_freq),
            'lucky_freq': dict(lucky_freq)
        }
    finally:
        session.close()

def get_avoided_numbers(recent_drawings, emphasis=0.9):
    """
    Generate a list of numbers to avoid based on recent drawings.
    
    Args:
        recent_drawings: List of recent drawing details
        emphasis: How strongly to avoid (0-1), 1 means complete avoidance
        
    Returns:
        tuple: (avoid_list, reduced_probability_list)
    """
    if not recent_drawings:
        return [], []
    
    # Flatten all recent numbers
    recent_numbers = []
    for drawing in recent_drawings:
        recent_numbers.extend(drawing['numbers'])
    
    # Count occurrences
    number_counts = Counter(recent_numbers)
    
    # Numbers appearing multiple times are strongly avoided
    strongly_avoid = [num for num, count in number_counts.items() if count > 1]
    
    # Numbers appearing once have reduced probability based on emphasis
    if random.random() < emphasis:
        # Strong avoidance - most recent numbers not included
        avoid_list = list(number_counts.keys())
        reduced_list = []
    else:
        # Moderate avoidance - only strongly avoid repeated numbers
        avoid_list = strongly_avoid
        reduced_list = [num for num, count in number_counts.items() if count == 1]
    
    return avoid_list, reduced_list

def create_diverse_combination(hot_cold_data, avoid_numbers, reduced_prob_numbers, strategy_name):
    """
    Create a combination avoiding recent numbers.
    
    Args:
        hot_cold_data: Dictionary with hot/cold numbers data
        avoid_numbers: List of numbers to completely avoid
        reduced_prob_numbers: List of numbers to use with reduced probability
        strategy_name: Name of the strategy
        
    Returns:
        dict: Generated combination
    """
    # Create pools of numbers with different weights
    available_hot = [n for n in hot_cold_data['hot_numbers'] 
                    if n not in avoid_numbers]
    available_medium = [n for n in hot_cold_data['medium_numbers'] 
                       if n not in avoid_numbers]
    available_cold = [n for n in hot_cold_data['cold_numbers'] 
                     if n not in avoid_numbers]
    
    # Create pool with reduced probability for some numbers
    reduced_hot = [n for n in available_hot if n in reduced_prob_numbers]
    reduced_medium = [n for n in available_medium if n in reduced_prob_numbers]
    reduced_cold = [n for n in available_cold if n in reduced_prob_numbers]
    
    # Normal probability for non-reduced numbers
    normal_hot = [n for n in available_hot if n not in reduced_prob_numbers]
    normal_medium = [n for n in available_medium if n not in reduced_prob_numbers]
    normal_cold = [n for n in available_cold if n not in reduced_prob_numbers]
    
    # Determine distribution based on strategy
    if "Hot" in strategy_name:
        # Favor hot numbers
        num_hot = random.randint(2, 3)
        num_medium = random.randint(1, 2)
        num_cold = 5 - num_hot - num_medium
    elif "Cold" in strategy_name:
        # Favor cold numbers
        num_cold = random.randint(2, 3)
        num_medium = random.randint(1, 2)
        num_hot = 5 - num_cold - num_medium
    elif "Balanced" in strategy_name:
        # Even distribution
        num_hot = random.randint(1, 2)
        num_medium = random.randint(1, 2)
        num_cold = 5 - num_hot - num_medium
    else:
        # Default distribution
        num_hot = random.randint(1, 2)
        num_medium = random.randint(1, 2)
        num_cold = 5 - num_hot - num_medium
    
    # Select numbers with preference for normal probability ones
    selected_hot = []
    if normal_hot and len(normal_hot) >= num_hot:
        selected_hot = random.sample(normal_hot, num_hot)
    else:
        # Use some reduced probability ones if needed
        if normal_hot:
            selected_hot.extend(normal_hot)
        remaining_hot = num_hot - len(selected_hot)
        if remaining_hot > 0 and reduced_hot:
            selected_hot.extend(random.sample(reduced_hot, min(remaining_hot, len(reduced_hot))))
    
    selected_medium = []
    if normal_medium and len(normal_medium) >= num_medium:
        selected_medium = random.sample(normal_medium, num_medium)
    else:
        # Use some reduced probability ones if needed
        if normal_medium:
            selected_medium.extend(normal_medium)
        remaining_medium = num_medium - len(selected_medium)
        if remaining_medium > 0 and reduced_medium:
            selected_medium.extend(random.sample(reduced_medium, min(remaining_medium, len(reduced_medium))))
    
    selected_cold = []
    if normal_cold and len(normal_cold) >= num_cold:
        selected_cold = random.sample(normal_cold, num_cold)
    else:
        # Use some reduced probability ones if needed
        if normal_cold:
            selected_cold.extend(normal_cold)
        remaining_cold = num_cold - len(selected_cold)
        if remaining_cold > 0 and reduced_cold:
            selected_cold.extend(random.sample(reduced_cold, min(remaining_cold, len(reduced_cold))))
    
    # Combine all selected numbers
    selected_numbers = selected_hot + selected_medium + selected_cold
    
    # If we don't have enough, add random available numbers
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 50) 
                     if n not in selected_numbers and n not in avoid_numbers]
        if available:
            selected_numbers.append(random.choice(available))
        else:
            # If somehow we've run out of available numbers, use any number
            remaining = [n for n in range(1, 50) if n not in selected_numbers]
            if remaining:
                selected_numbers.append(random.choice(remaining))
            else:
                break  # This should never happen with only 5 out of 49 numbers
    
    # Select lucky number - avoid recent lucky numbers
    recent_lucky = [drawing['lucky_number'] for drawing in last_drawings]
    available_lucky = [n for n in range(1, 11) if n not in recent_lucky]
    
    if available_lucky:
        lucky = random.choice(available_lucky)
    else:
        # If all were recently drawn, select any
        lucky = random.randint(1, 10)
    
    # Calculate a score based on uniqueness and strategy alignment
    base_score = 80
    # Bonus for not using any recent numbers
    recent_count = len([n for n in selected_numbers if n in reduced_prob_numbers])
    unique_bonus = 10 - (recent_count * 2)
    
    # Strategy alignment bonus
    if "Hot" in strategy_name:
        hot_count = len([n for n in selected_numbers if n in hot_cold_data['hot_numbers']])
        strategy_bonus = hot_count * 2
    elif "Cold" in strategy_name:
        cold_count = len([n for n in selected_numbers if n in hot_cold_data['cold_numbers']])
        strategy_bonus = cold_count * 2
    elif "Balanced" in strategy_name:
        # Bonus for good distribution
        hot_count = len([n for n in selected_numbers if n in hot_cold_data['hot_numbers']])
        cold_count = len([n for n in selected_numbers if n in hot_cold_data['cold_numbers']])
        medium_count = 5 - hot_count - cold_count
        strategy_bonus = 5 if (hot_count > 0 and cold_count > 0 and medium_count > 0) else 0
    elif "Even" in strategy_name:
        # Bonus for more even numbers
        even_count = len([n for n in selected_numbers if n % 2 == 0])
        strategy_bonus = even_count * 2
    elif "Range" in strategy_name:
        # Bonus for numbers in preferred range
        if "High" in strategy_name:
            high_count = len([n for n in selected_numbers if n >= 31])
            strategy_bonus = high_count * 2
        elif "Low" in strategy_name:
            low_count = len([n for n in selected_numbers if n <= 20])
            strategy_bonus = low_count * 2
        else:
            strategy_bonus = 0
    elif "Sequential" in strategy_name:
        # Bonus for sequential pairs
        sorted_numbers = sorted(selected_numbers)
        sequential_pairs = 0
        for i in range(len(sorted_numbers) - 1):
            if sorted_numbers[i+1] - sorted_numbers[i] == 1:
                sequential_pairs += 1
        strategy_bonus = sequential_pairs * 5
    else:
        strategy_bonus = 0
    
    # Calculate final score
    score = min(100, base_score + unique_bonus + strategy_bonus)
    
    return {
        'numbers': sorted(selected_numbers),
        'lucky_number': lucky,
        'strategy': strategy_name,
        'score': round(score, 1)
    }

def ensure_uniqueness(combinations):
    """
    Ensure all combinations are unique, replacing duplicates if needed.
    """
    # Extract just the number sets from combinations
    number_sets = [frozenset(c['numbers']) for c in combinations]
    
    # Check each combination against others
    for i in range(len(combinations)):
        current_set = frozenset(combinations[i]['numbers'])
        
        # Count occurrences of this set
        if number_sets.count(current_set) > 1:
            # Found a duplicate, need to replace
            # First find all indices of this set
            duplicate_indices = [j for j in range(len(combinations)) 
                               if frozenset(combinations[j]['numbers']) == current_set]
            
            # Replace all but the first occurrence
            for idx in duplicate_indices[1:]:
                # Create a replacement by modifying the strategy
                strategy = combinations[idx]['strategy']
                
                # Replace 1-2 numbers to make it unique
                new_numbers = list(combinations[idx]['numbers'])
                num_to_replace = random.randint(1, 2)
                indices_to_replace = random.sample(range(5), num_to_replace)
                
                for replace_idx in indices_to_replace:
                    # Find a replacement that doesn't create another duplicate
                    avoid_numbers = []
                    for combo in combinations:
                        avoid_numbers.extend(combo['numbers'])
                    
                    available_replacements = [n for n in range(1, 50) 
                                            if n not in new_numbers and 
                                            n not in avoid_numbers]
                    
                    if not available_replacements:
                        available_replacements = [n for n in range(1, 50) 
                                                if n not in new_numbers]
                    
                    if available_replacements:
                        new_numbers[replace_idx] = random.choice(available_replacements)
                
                # Update the combination
                combinations[idx]['numbers'] = sorted(new_numbers)
                
                # Update the set in number_sets
                number_sets[idx] = frozenset(combinations[idx]['numbers'])
    
    return combinations

def save_combinations_to_database(combinations, target_date):
    """
    Save generated combinations to the database.
    
    Args:
        combinations: List of dictionaries with generated combinations
        target_date: Date of the target draw
        
    Returns:
        bool: Success indicator
    """
    from database import GeneratedCombination, get_session
    import json
    
    session = get_session()
    try:
        for combo in combinations:
            new_combo = GeneratedCombination(
                created_at=date.today(),
                target_draw_date=target_date,
                strategy=combo['strategy'],
                numbers=json.dumps(combo['numbers']),
                stars=json.dumps([combo['lucky_number']]),
                score=combo['score']
            )
            session.add(new_combo)
        
        session.commit()
        return True
    except Exception as e:
        print(f"Error saving combinations to database: {str(e)}")
        session.rollback()
        return False
    finally:
        session.close()

def create_diverse_strategies(hot_cold_data, avoid_numbers, reduced_prob_numbers, count=20):
    """
    Create a diverse set of combinations using different strategies.
    """
    strategies = [
        "Diverse Hot Numbers Focus",
        "Diverse Cold Numbers Focus",
        "Diverse Balanced Mix",
        "Diverse Even Numbers Focus",
        "Diverse High Range Focus",
        "Diverse Low Range Focus",
        "Diverse Sequential Pattern",
        "Diverse Mixed Strategy"
    ]
    
    combinations = []
    
    # Distribute combinations among strategies
    strategy_counts = {}
    for i in range(count):
        # Cycle through strategies
        strategy = strategies[i % len(strategies)]
        strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        combinations.append(
            create_diverse_combination(hot_cold_data, avoid_numbers, reduced_prob_numbers, strategy)
        )
    
    return combinations

def main():
    """Generate 20 diverse French Loto combinations for the next draw"""
    print("Generating diverse combinations for the next French Loto draw...")
    
    # Get the recent drawings
    global last_drawings  # Make available for stratgies
    last_drawings = get_last_drawings(3)  # Get last 3 drawings
    
    if not last_drawings:
        print("No previous drawings found in the database.")
        return
    
    most_recent = last_drawings[0]
    print(f"Most recent drawing ({most_recent['date']}): {most_recent['numbers']} / Lucky: {most_recent['lucky_number']}")
    
    # Get all recently drawn numbers (to avoid)
    recent_numbers = []
    for drawing in last_drawings:
        recent_numbers.extend(drawing['numbers'])
    
    # Calculate the next draw date
    next_draw_date = get_next_draw_date(most_recent['date'])
    print(f"Next draw date: {next_draw_date}")
    
    # Get hot/cold number data with reduced emphasis on recent numbers
    hot_cold_data = get_hot_cold_numbers(recent_numbers)
    
    # Get numbers to avoid or use with reduced probability
    avoid_numbers, reduced_prob_numbers = get_avoided_numbers(last_drawings, emphasis=0.8)
    
    print(f"Numbers to avoid (from recent drawings): {avoid_numbers}")
    print(f"Numbers to use with reduced probability: {reduced_prob_numbers}")
    
    # Generate diverse combinations
    print("Generating diverse combinations across multiple strategies...")
    combinations = create_diverse_strategies(hot_cold_data, avoid_numbers, reduced_prob_numbers, count=20)
    
    # Ensure all combinations are unique
    print("Ensuring combination uniqueness...")
    combinations = ensure_uniqueness(combinations)
    
    # Sort by score
    combinations.sort(key=lambda x: x['score'], reverse=True)
    
    # Print the combinations
    print(f"\n20 Diverse Combinations for French Loto Draw on {next_draw_date}:")
    for i, combo in enumerate(combinations, 1):
        numbers_str = ", ".join(map(str, combo['numbers']))
        print(f"Combination {i} ({combo['strategy']}):")
        print(f"  Numbers: {numbers_str}")
        print(f"  Lucky Number: {combo['lucky_number']}")
        print(f"  Score: {combo['score']:.2f}")
        print()
    
    # Save to database
    print("Saving combinations to database...")
    if save_combinations_to_database(combinations, next_draw_date):
        print("Combinations saved successfully.")
    else:
        print("Failed to save combinations to database.")
    
    return combinations

if __name__ == "__main__":
    main()