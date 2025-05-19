"""
Generate 20 optimized French Loto combinations for the next draw
based on the analysis of May 19, 2025 results.
"""
import random
import numpy as np
from collections import Counter
from database import get_session, GeneratedCombination, FrenchLotoDrawing
from sqlalchemy import desc
import json
from datetime import date, timedelta

def get_last_drawing():
    """Get the last French Loto drawing"""
    session = get_session()
    try:
        last_drawing = session.query(FrenchLotoDrawing) \
            .order_by(desc(FrenchLotoDrawing.date)) \
            .first()
        
        if last_drawing:
            return {
                'date': last_drawing.date,
                'numbers': [last_drawing.n1, last_drawing.n2, last_drawing.n3, 
                           last_drawing.n4, last_drawing.n5],
                'lucky_number': last_drawing.lucky
            }
        return None
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

def get_hot_cold_numbers():
    """Get hot and cold numbers from historical data"""
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
        
        # Get hot and cold numbers
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

def create_hybrid_strategy_combination(last_drawing, hot_cold_data):
    """
    Create a combination using the hybrid mix strategy that performed well
    in the previous draw. This strategy mixes hot and cold numbers with
    a focus on numbers that appeared in the last drawing.
    """
    # Include 2-3 numbers from the last drawing
    num_from_last = random.randint(2, 3)
    selected_from_last = random.sample(last_drawing['numbers'], num_from_last)
    
    # Fill with a mix of hot/cold numbers
    remaining_needed = 5 - len(selected_from_last)
    
    # Prefer even numbers (3/5 of winning numbers were even)
    even_preference = 0.6  # 60% chance to select even numbers
    
    # 1-2 hot numbers that weren't in the last drawing
    num_hot = random.randint(1, min(2, remaining_needed))
    available_hot = [n for n in hot_cold_data['hot_numbers'] 
                    if n not in selected_from_last]
    
    # Filter for even/odd preference 
    if random.random() < even_preference:
        available_hot = [n for n in available_hot if n % 2 == 0] or available_hot
    
    selected_hot = random.sample(available_hot, min(num_hot, len(available_hot)))
    
    # Add cold numbers for the rest
    remaining_needed = 5 - (len(selected_from_last) + len(selected_hot))
    available_cold = [n for n in hot_cold_data['cold_numbers'] 
                     if n not in selected_from_last and n not in selected_hot]
    
    # Filter for even/odd preference
    if random.random() < even_preference:
        available_cold = [n for n in available_cold if n % 2 == 0] or available_cold
    
    selected_cold = random.sample(available_cold, min(remaining_needed, len(available_cold)))
    
    # If we still need more numbers, add medium numbers
    selected_numbers = selected_from_last + selected_hot + selected_cold
    remaining_needed = 5 - len(selected_numbers)
    
    if remaining_needed > 0:
        available_medium = [n for n in hot_cold_data['medium_numbers'] 
                           if n not in selected_numbers]
        
        # Filter for even/odd preference
        if random.random() < even_preference:
            available_medium = [n for n in available_medium if n % 2 == 0] or available_medium
            
        selected_medium = random.sample(available_medium, min(remaining_needed, len(available_medium)))
        selected_numbers.extend(selected_medium)
    
    # If by chance we still need more numbers, add any valid number
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 50) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # For lucky number, prefer the one that hit or a medium one
    if random.random() < 0.4:  # 40% chance to use the last lucky number
        lucky = last_drawing['lucky_number']
    else:
        # Otherwise use medium lucky numbers (last was medium)
        lucky = random.choice(hot_cold_data['medium_lucky'])
    
    return {
        'numbers': sorted(selected_numbers),
        'lucky_number': lucky,
        'strategy': 'Hybrid Mix Strategy',
        'score': 95.0  # High score for primary strategy
    }

def create_high_risk_strategy_combination(last_drawing, hot_cold_data):
    """
    Create a combination using the high risk strategy that performed well
    in the previous draw. This strategy focuses on cold numbers with a few
    hot ones, and particularly emphasizes even numbers and numbers from
    the higher ranges.
    """
    # Start with 1-2 numbers from the last drawing
    num_from_last = random.randint(1, 2)
    selected_from_last = random.sample(last_drawing['numbers'], num_from_last)
    
    # Add mostly cold numbers (high risk)
    # This strategy had more success with the lucky number
    
    # Emphasize number ranges 31-40 and 41-49 which had 3/5 winning numbers
    high_range_numbers = [n for n in range(31, 50)]
    available_high_range = [n for n in high_range_numbers if n not in selected_from_last]
    
    # Select 2-3 numbers from high ranges
    num_high_range = random.randint(2, 3)
    selected_high_range = random.sample(available_high_range, min(num_high_range, len(available_high_range)))
    
    selected_numbers = selected_from_last + selected_high_range
    
    # Fill remaining with a preference for cold and even numbers
    remaining_needed = 5 - len(selected_numbers)
    available_cold = [n for n in hot_cold_data['cold_numbers'] 
                     if n not in selected_numbers]
    
    # Prefer even numbers
    available_cold_even = [n for n in available_cold if n % 2 == 0]
    if available_cold_even and random.random() < 0.7:  # 70% chance to prefer even
        selected_cold = random.sample(available_cold_even, min(remaining_needed, len(available_cold_even)))
    else:
        selected_cold = random.sample(available_cold, min(remaining_needed, len(available_cold)))
    
    selected_numbers.extend(selected_cold)
    
    # If we need more numbers, add any valid ones
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 50) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # For lucky number, use the one that hit in 50% of cases
    if random.random() < 0.5:
        lucky = last_drawing['lucky_number']
    else:
        # Otherwise medium or cold lucky (as the winner was medium)
        lucky_options = hot_cold_data['medium_lucky'] + hot_cold_data['cold_lucky']
        lucky = random.choice(lucky_options)
    
    return {
        'numbers': sorted(selected_numbers),
        'lucky_number': lucky,
        'strategy': 'High Risk Strategy',
        'score': 92.0
    }

def create_sequential_strategy_combination(last_drawing, hot_cold_data):
    """
    Create a combination that emphasizes sequential pairs, which appeared
    in the winning combination.
    """
    # Identify if there were sequential pairs in the last drawing
    last_numbers_sorted = sorted(last_drawing['numbers'])
    sequential_pairs = []
    
    for i in range(len(last_numbers_sorted) - 1):
        if last_numbers_sorted[i+1] - last_numbers_sorted[i] == 1:
            sequential_pairs.append((last_numbers_sorted[i], last_numbers_sorted[i+1]))
    
    selected_numbers = []
    
    # If sequential pairs exist, include one
    if sequential_pairs and random.random() < 0.7:  # 70% chance
        selected_pair = random.choice(sequential_pairs)
        selected_numbers.extend(selected_pair)
    else:
        # Create a new sequential pair
        # Prefer ranges with winning numbers (1-10, 31-40, 41-49)
        preferred_ranges = [(1, 10), (31, 40), (41, 49)]
        selected_range = random.choice(preferred_ranges)
        
        # Find valid starting points for sequences
        start_points = [n for n in range(selected_range[0], selected_range[1]) 
                      if n+1 <= selected_range[1]]
        
        if start_points:
            start = random.choice(start_points)
            selected_numbers.extend([start, start+1])
    
    # Add 1-2 numbers from the last drawing if not already included
    available_last = [n for n in last_drawing['numbers'] if n not in selected_numbers]
    if available_last:
        num_from_last = random.randint(1, min(2, len(available_last)))
        selected_from_last = random.sample(available_last, num_from_last)
        selected_numbers.extend(selected_from_last)
    
    # Fill remaining with a mix of hot/cold numbers
    # Emphasize even numbers
    remaining_needed = 5 - len(selected_numbers)
    
    if remaining_needed > 0:
        # Pool of remaining candidates
        all_candidates = []
        
        # Add some hot numbers
        available_hot = [n for n in hot_cold_data['hot_numbers'] if n not in selected_numbers]
        all_candidates.extend([(n, 'hot') for n in available_hot])
        
        # Add some cold numbers
        available_cold = [n for n in hot_cold_data['cold_numbers'] if n not in selected_numbers]
        all_candidates.extend([(n, 'cold') for n in available_cold])
        
        # Add some medium numbers
        available_medium = [n for n in hot_cold_data['medium_numbers'] if n not in selected_numbers]
        all_candidates.extend([(n, 'medium') for n in available_medium])
        
        # Shuffle and filter for preference of even numbers
        random.shuffle(all_candidates)
        even_candidates = [n for n, _ in all_candidates if n % 2 == 0]
        
        selected_remaining = []
        num_even_needed = min(int(remaining_needed * 0.6), remaining_needed)
        
        # Select even numbers first
        if even_candidates:
            selected_remaining.extend(random.sample(even_candidates, 
                                                 min(num_even_needed, len(even_candidates))))
        
        # Then fill with any remaining numbers
        still_needed = remaining_needed - len(selected_remaining)
        if still_needed > 0:
            available_candidates = [n for n, _ in all_candidates if n not in selected_remaining]
            if available_candidates:
                selected_remaining.extend(random.sample(available_candidates, 
                                                     min(still_needed, len(available_candidates))))
        
        selected_numbers.extend(selected_remaining)
    
    # If we still need more numbers, add any valid number
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 50) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # For lucky number, prefer the one from the last drawing
    if random.random() < 0.4:
        lucky = last_drawing['lucky_number']
    else:
        # Use medium lucky numbers as the winner was medium
        lucky = random.choice(hot_cold_data['medium_lucky'])
    
    return {
        'numbers': sorted(selected_numbers),
        'lucky_number': lucky,
        'strategy': 'Sequential Pattern Strategy',
        'score': 88.0
    }

def create_cold_emphasis_combination(hot_cold_data):
    """
    Create a combination emphasizing cold numbers, since the winning numbers
    showed a strong bias toward cold numbers (4/5 were cold).
    """
    # Select 3-4 cold numbers
    num_cold = random.randint(3, 4)
    selected_cold = random.sample(hot_cold_data['cold_numbers'], min(num_cold, len(hot_cold_data['cold_numbers'])))
    
    # Add 1-2 hot numbers for balance
    num_hot = 5 - len(selected_cold)
    available_hot = [n for n in hot_cold_data['hot_numbers'] if n not in selected_cold]
    selected_hot = random.sample(available_hot, min(num_hot, len(available_hot)))
    
    selected_numbers = selected_cold + selected_hot
    
    # If we need more numbers, add medium numbers
    if len(selected_numbers) < 5:
        remaining_needed = 5 - len(selected_numbers)
        available_medium = [n for n in hot_cold_data['medium_numbers'] if n not in selected_numbers]
        selected_medium = random.sample(available_medium, min(remaining_needed, len(available_medium)))
        selected_numbers.extend(selected_medium)
    
    # If we still need more numbers, add any valid number
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 50) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # For lucky number, use medium or cold lucky
    lucky_options = hot_cold_data['medium_lucky'] + hot_cold_data['cold_lucky']
    lucky = random.choice(lucky_options)
    
    return {
        'numbers': sorted(selected_numbers),
        'lucky_number': lucky,
        'strategy': 'Cold Numbers Focus',
        'score': 85.0
    }

def create_balanced_strategy_combination(last_drawing, hot_cold_data):
    """
    Create a balanced combination with elements from all successful approaches.
    """
    # Include 1-2 numbers from the last drawing
    num_from_last = random.randint(1, 2)
    selected_from_last = random.sample(last_drawing['numbers'], num_from_last)
    
    # Add 1-2 hot numbers
    num_hot = random.randint(1, 2)
    available_hot = [n for n in hot_cold_data['hot_numbers'] if n not in selected_from_last]
    selected_hot = random.sample(available_hot, min(num_hot, len(available_hot)))
    
    # Add 1-2 cold numbers
    num_cold = random.randint(1, 2)
    available_cold = [n for n in hot_cold_data['cold_numbers'] 
                     if n not in selected_from_last and n not in selected_hot]
    selected_cold = random.sample(available_cold, min(num_cold, len(available_cold)))
    
    selected_numbers = selected_from_last + selected_hot + selected_cold
    
    # If we need more numbers, add some medium numbers
    remaining_needed = 5 - len(selected_numbers)
    if remaining_needed > 0:
        available_medium = [n for n in hot_cold_data['medium_numbers'] 
                           if n not in selected_numbers]
        selected_medium = random.sample(available_medium, min(remaining_needed, len(available_medium)))
        selected_numbers.extend(selected_medium)
    
    # If we still need more numbers, add any valid number
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 50) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # For lucky number, randomize with preference for the winning one
    if random.random() < 0.3:
        lucky = last_drawing['lucky_number']
    else:
        # Use any valid lucky number with preference for medium ones
        if random.random() < 0.6:  # 60% medium, 40% any
            lucky = random.choice(hot_cold_data['medium_lucky'])
        else:
            lucky = random.randint(1, 10)
    
    return {
        'numbers': sorted(selected_numbers),
        'lucky_number': lucky,
        'strategy': 'Balanced Mix Strategy',
        'score': 82.0
    }

def create_high_range_combination(hot_cold_data):
    """
    Create a combination focusing on high ranges (31-49) which had 3/5 winning numbers.
    """
    # Get numbers in high ranges
    high_range_numbers = [n for n in range(31, 50)]
    
    # Select 3-4 numbers from the high range
    num_high = random.randint(3, 4)
    selected_high = random.sample(high_range_numbers, num_high)
    
    # Add 1-2 numbers from lower ranges for balance
    low_range_numbers = [n for n in range(1, 31)]
    num_low = 5 - len(selected_high)
    selected_low = random.sample(low_range_numbers, num_low)
    
    selected_numbers = selected_high + selected_low
    
    # For lucky number, use medium ones as the winner was medium
    lucky = random.choice(hot_cold_data['medium_lucky'])
    
    return {
        'numbers': sorted(selected_numbers),
        'lucky_number': lucky,
        'strategy': 'High Range Focus',
        'score': 80.0
    }

def create_even_number_combination(hot_cold_data):
    """
    Create a combination emphasizing even numbers, as 3/5 of the winning numbers were even.
    """
    # Get all even numbers
    even_numbers = [n for n in range(1, 50) if n % 2 == 0]
    
    # Select 3-4 even numbers
    num_even = random.randint(3, 4)
    selected_even = random.sample(even_numbers, num_even)
    
    # Add 1-2 odd numbers for balance
    odd_numbers = [n for n in range(1, 50) if n % 2 == 1]
    num_odd = 5 - len(selected_even)
    selected_odd = random.sample(odd_numbers, num_odd)
    
    selected_numbers = selected_even + selected_odd
    
    # For lucky number, use medium ones
    lucky = random.choice(hot_cold_data['medium_lucky'])
    
    return {
        'numbers': sorted(selected_numbers),
        'lucky_number': lucky,
        'strategy': 'Even Numbers Focus',
        'score': 78.0
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
                lucky = combinations[idx]['lucky_number']
                
                # Replace 1-2 numbers to make it unique
                new_numbers = list(combinations[idx]['numbers'])
                num_to_replace = random.randint(1, 2)
                indices_to_replace = random.sample(range(5), num_to_replace)
                
                for replace_idx in indices_to_replace:
                    # Find a replacement that doesn't create another duplicate
                    available_replacements = [n for n in range(1, 50) if n not in new_numbers]
                    
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

def main():
    """Generate 20 optimized French Loto combinations for the next draw"""
    print("Generating optimized combinations for the next French Loto draw...")
    
    # Get the last drawing details
    last_drawing = get_last_drawing()
    
    if not last_drawing:
        print("No previous drawings found in the database.")
        return
    
    print(f"Last drawing ({last_drawing['date']}): {last_drawing['numbers']} / Lucky: {last_drawing['lucky_number']}")
    
    # Calculate the next draw date
    next_draw_date = get_next_draw_date(last_drawing['date'])
    print(f"Next draw date: {next_draw_date}")
    
    # Get hot/cold number data
    hot_cold_data = get_hot_cold_numbers()
    
    # Generate combinations using the best performing strategies
    combinations = []
    
    # 5 Hybrid Mix Strategy combinations
    print("Generating Hybrid Mix Strategy combinations...")
    for _ in range(5):
        combinations.append(create_hybrid_strategy_combination(last_drawing, hot_cold_data))
    
    # 4 High Risk Strategy combinations
    print("Generating High Risk Strategy combinations...")
    for _ in range(4):
        combinations.append(create_high_risk_strategy_combination(last_drawing, hot_cold_data))
    
    # 3 Sequential Pattern Strategy combinations
    print("Generating Sequential Pattern Strategy combinations...")
    for _ in range(3):
        combinations.append(create_sequential_strategy_combination(last_drawing, hot_cold_data))
    
    # 2 Cold Numbers Focus combinations
    print("Generating Cold Numbers Focus combinations...")
    for _ in range(2):
        combinations.append(create_cold_emphasis_combination(hot_cold_data))
    
    # 2 Balanced Mix Strategy combinations
    print("Generating Balanced Mix Strategy combinations...")
    for _ in range(2):
        combinations.append(create_balanced_strategy_combination(last_drawing, hot_cold_data))
    
    # 2 High Range Focus combinations
    print("Generating High Range Focus combinations...")
    for _ in range(2):
        combinations.append(create_high_range_combination(hot_cold_data))
    
    # 2 Even Numbers Focus combinations
    print("Generating Even Numbers Focus combinations...")
    for _ in range(2):
        combinations.append(create_even_number_combination(hot_cold_data))
    
    # Ensure all combinations are unique
    print("Ensuring combination uniqueness...")
    combinations = ensure_uniqueness(combinations)
    
    # Sort by score
    combinations.sort(key=lambda x: x['score'], reverse=True)
    
    # Print the combinations
    print(f"\n20 Optimized Combinations for French Loto Draw on {next_draw_date}:")
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