"""
Generate 10 additional optimized French Loto combinations with a simplified approach
"""
import random
import numpy as np
from collections import Counter
from database import get_session, GeneratedCombination, FrenchLotoDrawing
from sqlalchemy import desc
import json
from datetime import date

def get_existing_combinations():
    """Get the 10 most recently generated combinations"""
    session = get_session()
    try:
        existing_combos = session.query(GeneratedCombination) \
            .filter(GeneratedCombination.created_at == date.today()) \
            .order_by(GeneratedCombination.score.desc()) \
            .limit(10) \
            .all()
        
        combinations = []
        for combo in existing_combos:
            combinations.append({
                'id': combo.id,
                'numbers': json.loads(combo.numbers),
                'lucky_number': json.loads(combo.stars)[0],
                'strategy': combo.strategy,
                'score': combo.score
            })
        
        return combinations
    finally:
        session.close()

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
        
        # Get hot and cold lucky numbers
        hot_lucky = [n for n, _ in lucky_freq.most_common(5)]
        cold_lucky = [n for n, _ in sorted(lucky_freq.items(), key=lambda x: x[1])[:5]]
        
        return {
            'hot_numbers': hot_numbers,
            'cold_numbers': cold_numbers,
            'hot_lucky': hot_lucky,
            'cold_lucky': cold_lucky,
            'number_freq': number_freq
        }
    finally:
        session.close()

def create_mixing_combination(existing_combinations, index1, index2):
    """Create a hybrid combination by mixing two existing combinations"""
    combo1 = existing_combinations[index1]
    combo2 = existing_combinations[index2]
    
    # Take 2-3 numbers from combo1
    num_from_first = random.randint(2, 3)
    selected_from_first = random.sample(combo1['numbers'], num_from_first)
    
    # Take remaining numbers from combo2, avoiding duplicates
    remaining_needed = 5 - len(selected_from_first)
    available_from_second = [n for n in combo2['numbers'] if n not in selected_from_first]
    
    if len(available_from_second) >= remaining_needed:
        selected_from_second = random.sample(available_from_second, remaining_needed)
    else:
        # If not enough numbers in combo2, take all available and fill the rest
        selected_from_second = available_from_second
        
        # Fill remaining from any available numbers
        still_needed = 5 - (len(selected_from_first) + len(selected_from_second))
        if still_needed > 0:
            used = selected_from_first + selected_from_second
            remaining = [n for n in range(1, 50) if n not in used]
            selected_from_second.extend(random.sample(remaining, still_needed))
    
    # Combine
    all_selected = selected_from_first + selected_from_second
    
    # For lucky number, randomly choose between the two combinations
    lucky = combo1['lucky_number'] if random.random() < 0.5 else combo2['lucky_number']
    
    # Calculate approximate score - average of parent scores with small random variation
    avg_score = (combo1['score'] + combo2['score']) / 2
    score = avg_score + random.uniform(-3, 3)  # Small random adjustment
    
    return {
        'numbers': sorted(all_selected),
        'lucky_number': lucky,
        'strategy': f'Hybrid Mix ({index1+1}+{index2+1})',
        'score': round(score, 1)
    }

def create_new_combination(hot_cold_data, existing_numbers, strategy_name):
    """Create a new combination using hot/cold data and avoiding existing numbers"""
    # Use a mix of hot and cold numbers
    selected = []
    
    # Add 2-3 hot numbers
    num_hot = random.randint(2, 3)
    available_hot = [n for n in hot_cold_data['hot_numbers'] if n not in selected]
    if available_hot:
        selected.extend(random.sample(available_hot, min(num_hot, len(available_hot))))
    
    # Add 1-2 cold numbers
    num_cold = random.randint(1, 2)
    available_cold = [n for n in hot_cold_data['cold_numbers'] if n not in selected]
    if available_cold:
        selected.extend(random.sample(available_cold, min(num_cold, len(available_cold))))
    
    # Find uncovered numbers from existing combinations
    flat_existing = []
    for combo in existing_numbers:
        flat_existing.extend(combo)
    
    existing_freq = Counter(flat_existing)
    uncovered = [n for n in range(1, 50) if n not in existing_freq]
    underused = [n for n, count in existing_freq.items() if count == 1]
    
    # Add some uncovered or underused numbers if available
    priority_numbers = uncovered + underused
    available_priority = [n for n in priority_numbers if n not in selected]
    
    if available_priority and len(selected) < 5:
        num_to_add = min(5 - len(selected), len(available_priority))
        selected.extend(random.sample(available_priority, num_to_add))
    
    # Fill any remaining spots with random numbers
    while len(selected) < 5:
        available = [n for n in range(1, 50) if n not in selected]
        if available:
            selected.append(random.choice(available))
        else:
            break
    
    # For lucky number, alternate between hot and cold
    if random.random() < 0.7:  # 70% chance for hot lucky
        lucky = random.choice(hot_cold_data['hot_lucky'])
    else:  # 30% chance for cold lucky
        lucky = random.choice(hot_cold_data['cold_lucky'])
    
    # Generate a score based on frequency data
    score_base = 75  # Base score
    for num in selected:
        # Add points based on frequency (normalized to 0-10 range)
        freq = hot_cold_data['number_freq'].get(num, 0)
        max_freq = max(hot_cold_data['number_freq'].values())
        normalized_freq = (freq / max_freq) * 10
        score_base += normalized_freq
    
    # Normalize final score to 0-100 range
    score = min(100, max(0, score_base))
    
    return {
        'numbers': sorted(selected),
        'lucky_number': lucky,
        'strategy': strategy_name,
        'score': round(score, 1)
    }

def ensure_uniqueness(new_combinations, existing_combinations):
    """Ensure that all combinations are unique, replacing duplicates if needed"""
    # Extract just the number sets from existing combinations
    existing_number_sets = [frozenset(c['numbers']) for c in existing_combinations]
    
    # Check each new combination against existing ones
    for i, combo in enumerate(new_combinations):
        number_set = frozenset(combo['numbers'])
        
        # Also check against other new combinations
        other_new_sets = [frozenset(new_combinations[j]['numbers']) for j in range(len(new_combinations)) if j != i]
        
        if number_set in existing_number_sets or number_set in other_new_sets:
            # Replace with a newly generated combination
            hot_cold_data = get_hot_cold_numbers()
            existing_flat = [c['numbers'] for c in existing_combinations + new_combinations]
            new_combo = create_new_combination(hot_cold_data, existing_flat, f"Replacement #{i+1}")
            
            # Replace the duplicate
            new_combinations[i] = new_combo

def save_combinations_to_database(combinations):
    """Save generated combinations to the database"""
    from database import GeneratedCombination, get_session
    import json
    
    session = get_session()
    try:
        for combo in combinations:
            new_combo = GeneratedCombination(
                created_at=date.today(),
                target_draw_date=date.today(),
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
    """Generate 10 additional optimized French Loto combinations"""
    print("Retrieving existing combinations...")
    existing_combinations = get_existing_combinations()
    
    if not existing_combinations:
        print("No existing combinations found. Please run french_loto_optimized.py first.")
        return
    
    print(f"Found {len(existing_combinations)} existing combinations.")
    
    # Get hot/cold number data
    print("Analyzing hot and cold numbers...")
    hot_cold_data = get_hot_cold_numbers()
    
    # Generate new combinations
    new_combinations = []
    
    # 1. Create 5 hybrid mixes by combining pairs of existing combinations
    print("Creating hybrid combinations...")
    pairs = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]  # Use all existing combinations in pairs
    for idx1, idx2 in pairs:
        if idx1 < len(existing_combinations) and idx2 < len(existing_combinations):
            new_combinations.append(create_mixing_combination(existing_combinations, idx1, idx2))
    
    # 2. Create 5 entirely new combinations using different strategies
    print("Creating new optimized combinations...")
    strategies = [
        "New Balanced Strategy", 
        "Coverage Optimization", 
        "Lucky Number Focus",
        "High Risk Strategy", 
        "Maximum Diversity"
    ]
    
    existing_flat = [c['numbers'] for c in existing_combinations + new_combinations]
    for strategy in strategies:
        new_combinations.append(create_new_combination(hot_cold_data, existing_flat, strategy))
    
    # Ensure all combinations are unique
    print("Ensuring combination uniqueness...")
    ensure_uniqueness(new_combinations, existing_combinations)
    
    # Sort by score
    new_combinations.sort(key=lambda x: x['score'], reverse=True)
    
    # Print the combinations
    print("\nAdditional 10 Optimized Combinations:")
    for i, combo in enumerate(new_combinations, 1):
        numbers_str = ", ".join(map(str, combo['numbers']))
        print(f"Combination {i} ({combo['strategy']}):")
        print(f"  Numbers: {numbers_str}")
        print(f"  Lucky Number: {combo['lucky_number']}")
        print(f"  Score: {combo['score']:.2f}")
        print()
    
    # Save to database
    print("Saving combinations to database...")
    if save_combinations_to_database(new_combinations):
        print("Combinations saved successfully.")
    else:
        print("Failed to save combinations to database.")
    
    return new_combinations

if __name__ == "__main__":
    main()