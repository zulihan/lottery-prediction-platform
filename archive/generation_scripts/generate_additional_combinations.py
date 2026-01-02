"""
Generate 10 additional optimized French Loto combinations by:
1. Creating some entirely new combinations with advanced strategies
2. Creating some hybrid combinations by mixing strong patterns from existing ones
3. Ensuring all 20 combinations together provide maximum coverage
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

def analyze_number_coverage(combinations):
    """
    Analyze the number coverage across all combinations.
    
    Returns a dictionary with coverage statistics
    """
    all_numbers = []
    lucky_numbers = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        lucky_numbers.append(combo['lucky_number'])
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(lucky_numbers)
    
    # Find uncovered and underrepresented numbers
    uncovered = [n for n in range(1, 50) if n not in number_freq]
    underrepresented = [n for n, count in number_freq.items() if count == 1]
    
    # Find overrepresented numbers
    overrepresented = [n for n, count in number_freq.items() if count >= 3]
    
    return {
        'number_freq': number_freq,
        'lucky_freq': lucky_freq,
        'uncovered': uncovered,
        'underrepresented': underrepresented,
        'overrepresented': overrepresented
    }

def get_hot_cold_numbers(limit=20):
    """Get hot and cold numbers from historical data"""
    session = get_session()
    try:
        # Get latest 100 drawings
        drawings = session.query(FrenchLotoDrawing) \
            .order_by(desc(FrenchLotoDrawing.date)) \
            .limit(100) \
            .all()
        
        # Extract numbers
        numbers = []
        lucky = []
        
        for drawing in drawings:
            numbers.extend([drawing.n1, drawing.n2, drawing.n3, drawing.n4, drawing.n5])
            lucky.append(drawing.lucky)
        
        # Count frequencies
        number_freq = Counter(numbers)
        lucky_freq = Counter(lucky)
        
        # Get hot and cold numbers
        hot_numbers = [n for n, _ in number_freq.most_common(limit)]
        cold_numbers = [n for n, _ in sorted(number_freq.items(), key=lambda x: x[1])[:limit]]
        
        # Get hot and cold lucky numbers
        hot_lucky = [n for n, _ in lucky_freq.most_common(5)]
        cold_lucky = [n for n, _ in sorted(lucky_freq.items(), key=lambda x: x[1])[:5]]
        
        return {
            'hot_numbers': hot_numbers,
            'cold_numbers': cold_numbers,
            'hot_lucky': hot_lucky,
            'cold_lucky': cold_lucky
        }
    finally:
        session.close()

def create_pattern_hybrid(existing_combinations, coverage_stats):
    """
    Create a hybrid combination using patterns from existing high-scoring combinations
    and incorporating uncovered or underrepresented numbers.
    """
    # Get the top 3 combinations by score
    top_combos = sorted(existing_combinations, key=lambda x: x['score'], reverse=True)[:3]
    
    # Extract common patterns
    common_pairs = []
    
    # Find number pairs that appear in at least 2 of the top combinations
    for i, combo1 in enumerate(top_combos):
        for j, combo2 in enumerate(top_combos[i+1:], i+1):
            for num1 in combo1['numbers']:
                for num2 in combo1['numbers']:
                    if num1 < num2 and num1 in combo2['numbers'] and num2 in combo2['numbers']:
                        common_pairs.append((num1, num2))
    
    # Start building a new combination
    new_numbers = set()
    
    # Add 1-2 strong pairs if available
    if common_pairs:
        selected_pairs = random.sample(common_pairs, min(2, len(common_pairs)))
        for pair in selected_pairs:
            new_numbers.add(pair[0])
            new_numbers.add(pair[1])
    
    # Add 1-2 uncovered numbers for better coverage
    if coverage_stats['uncovered']:
        num_to_add = min(2, 5 - len(new_numbers), len(coverage_stats['uncovered']))
        if num_to_add > 0:
            new_numbers.update(random.sample(coverage_stats['uncovered'], num_to_add))
    
    # Add some underrepresented numbers if needed
    if len(new_numbers) < 5 and coverage_stats['underrepresented']:
        num_to_add = min(5 - len(new_numbers), len(coverage_stats['underrepresented']))
        if num_to_add > 0:
            new_numbers.update(random.sample(coverage_stats['underrepresented'], num_to_add))
    
    # Fill remaining spots with hot numbers that aren't overrepresented
    hot_cold_stats = get_hot_cold_numbers()
    remaining_hot = [n for n in hot_cold_stats['hot_numbers'] 
                    if n not in new_numbers and n not in coverage_stats['overrepresented']]
    
    if len(new_numbers) < 5 and remaining_hot:
        num_to_add = min(5 - len(new_numbers), len(remaining_hot))
        if num_to_add > 0:
            new_numbers.update(random.sample(remaining_hot, num_to_add))
    
    # If we still need more numbers, add any valid numbers
    while len(new_numbers) < 5:
        remaining = [n for n in range(1, 50) if n not in new_numbers]
        if not remaining:
            break
        new_numbers.add(random.choice(remaining))
    
    # Choose a lucky number that's not overrepresented
    used_lucky = [c['lucky_number'] for c in existing_combinations]
    lucky_counter = Counter(used_lucky)
    
    # Prefer hot lucky numbers that aren't overused
    hot_lucky_not_overused = [n for n in hot_cold_stats['hot_lucky'] if lucky_counter.get(n, 0) <= 1]
    
    if hot_lucky_not_overused:
        lucky = random.choice(hot_lucky_not_overused)
    else:
        # If all hot are overused, choose any valid lucky number
        lucky = random.randint(1, 10)
    
    return {
        'numbers': sorted(list(new_numbers)),
        'lucky_number': lucky,
        'strategy': 'Pattern Hybrid',
        'score': 85.0  # Estimated score
    }

def create_coverage_optimized(existing_combinations, coverage_stats):
    """
    Create a combination optimized for coverage by using numbers 
    that are underrepresented in existing combinations
    """
    # Start with uncovered and underrepresented numbers
    priority_numbers = set(coverage_stats['uncovered'] + coverage_stats['underrepresented'])
    
    # If we don't have enough, add some less frequent numbers from historical data
    if len(priority_numbers) < 5:
        hot_cold_stats = get_hot_cold_numbers()
        remaining_cold = [n for n in hot_cold_stats['cold_numbers'] 
                         if n not in priority_numbers and n not in coverage_stats['overrepresented']]
        
        if remaining_cold:
            num_to_add = min(5 - len(priority_numbers), len(remaining_cold))
            priority_numbers.update(random.sample(remaining_cold, num_to_add))
    
    # If we have more than 5, select the optimal subset
    if len(priority_numbers) > 5:
        # Prioritize truly uncovered numbers first
        selected = set(coverage_stats['uncovered'][:5])
        
        # Then add underrepresented until we have 5
        if len(selected) < 5:
            remaining = [n for n in priority_numbers if n not in selected]
            selected.update(random.sample(remaining, min(5 - len(selected), len(remaining))))
    else:
        selected = priority_numbers
    
    # If we somehow still need more numbers, add random ones
    while len(selected) < 5:
        remaining = [n for n in range(1, 50) if n not in selected]
        if not remaining:
            break
        selected.add(random.choice(remaining))
    
    # For lucky number, choose one that's underrepresented
    used_lucky = [c['lucky_number'] for c in existing_combinations]
    lucky_counter = Counter(used_lucky)
    
    underused_lucky = [n for n in range(1, 11) if lucky_counter.get(n, 0) <= 1]
    if underused_lucky:
        lucky = random.choice(underused_lucky)
    else:
        lucky = random.randint(1, 10)
    
    return {
        'numbers': sorted(list(selected)),
        'lucky_number': lucky,
        'strategy': 'Coverage Optimization',
        'score': 80.0  # Estimated score
    }

def create_balanced_risk(risk_level=0.5):
    """
    Create a balanced combination with the specified risk level.
    Higher risk means more cold/overdue numbers.
    """
    hot_cold_stats = get_hot_cold_numbers()
    
    # Determine number of hot vs cold numbers based on risk level
    num_hot = max(1, min(4, int(5 * (1 - risk_level))))
    num_cold = 5 - num_hot
    
    # Sample hot and cold numbers
    selected_hot = random.sample(hot_cold_stats['hot_numbers'], min(num_hot, len(hot_cold_stats['hot_numbers'])))
    remaining_cold = [n for n in hot_cold_stats['cold_numbers'] if n not in selected_hot]
    selected_cold = random.sample(remaining_cold, min(num_cold, len(remaining_cold)))
    
    # Combine selections
    selected = selected_hot + selected_cold
    
    # If we need more numbers, add from the middle range
    while len(selected) < 5:
        middle_range = [n for n in range(1, 50) if n not in selected 
                       and n not in hot_cold_stats['hot_numbers'] 
                       and n not in hot_cold_stats['cold_numbers']]
        if middle_range:
            selected.append(random.choice(middle_range))
        else:
            # If somehow we run out of middle range numbers, use any available
            available = [n for n in range(1, 50) if n not in selected]
            if available:
                selected.append(random.choice(available))
            else:
                break
    
    # For lucky number, use hot or cold based on risk level
    if random.random() < risk_level:
        lucky = random.choice(hot_cold_stats['cold_lucky'])
    else:
        lucky = random.choice(hot_cold_stats['hot_lucky'])
    
    return {
        'numbers': sorted(selected),
        'lucky_number': lucky,
        'strategy': f'Balanced Risk ({risk_level:.1f})',
        'score': 90 - (risk_level * 20)  # Higher risk gets lower score
    }

def create_frequency_based():
    """Create a combination based on frequency analysis of all historical drawings"""
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
        
        # Calculate frequencies
        number_freq = Counter(all_numbers)
        lucky_freq = Counter(all_lucky)
        
        # Convert to probability distribution
        total_numbers = len(all_numbers)
        number_probs = {num: count/total_numbers for num, count in number_freq.items()}
        
        total_lucky = len(all_lucky)
        lucky_probs = {num: count/total_lucky for num, count in lucky_freq.items()}
        
        # Sample based on frequencies
        selected_numbers = np.random.choice(
            list(number_probs.keys()),
            size=5,
            replace=False,
            p=list(number_probs.values())
        )
        
        lucky_number = np.random.choice(
            list(lucky_probs.keys()),
            size=1,
            p=list(lucky_probs.values())
        )[0]
        
        return {
            'numbers': sorted(selected_numbers.tolist()),
            'lucky_number': int(lucky_number),
            'strategy': 'Frequency Analysis',
            'score': 82.0
        }
    finally:
        session.close()

def create_lucky_number_focus():
    """Create a combination that focuses on optimal lucky number selection"""
    hot_cold_stats = get_hot_cold_numbers()
    
    # Select primarily hot numbers
    selected = random.sample(hot_cold_stats['hot_numbers'], min(4, len(hot_cold_stats['hot_numbers'])))
    
    # Add one cold number for balance
    remaining_cold = [n for n in hot_cold_stats['cold_numbers'] if n not in selected]
    if remaining_cold:
        selected.append(random.choice(remaining_cold))
    
    # Fill if needed
    while len(selected) < 5:
        available = [n for n in range(1, 50) if n not in selected]
        if available:
            selected.append(random.choice(available))
        else:
            break
    
    # For this strategy, we specifically focus on the most frequent lucky number
    session = get_session()
    try:
        # Get lucky numbers from last 100 draws
        lucky_numbers = []
        recent_drawings = session.query(FrenchLotoDrawing) \
            .order_by(desc(FrenchLotoDrawing.date)) \
            .limit(100) \
            .all()
        
        for drawing in recent_drawings:
            lucky_numbers.append(drawing.lucky)
        
        lucky_freq = Counter(lucky_numbers)
        most_common = lucky_freq.most_common(1)[0][0]
        
        return {
            'numbers': sorted(selected),
            'lucky_number': most_common,
            'strategy': 'Lucky Number Focus',
            'score': 83.0
        }
    finally:
        session.close()

def create_mix_combination(combinations, index1, index2):
    """Create a hybrid combination by mixing two existing combinations"""
    combo1 = combinations[index1]
    combo2 = combinations[index2]
    
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
        'strategy': f'Hybrid Mix',
        'score': round(score, 1)
    }

def save_combinations_to_database(combinations):
    """
    Save generated combinations to the database.
    
    Args:
        combinations: List of dictionaries with generated combinations
        
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
                target_draw_date=date.today(),  # Assuming today's draw
                strategy=combo['strategy'],
                numbers=json.dumps(combo['numbers']),
                stars=json.dumps([combo['lucky_number']]),  # Store lucky as a list for API compatibility
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

def ensure_uniqueness(new_combinations, existing_combinations):
    """
    Ensure that all combinations are unique across both lists.
    Modifies new_combinations in place to replace duplicates.
    """
    existing_number_sets = [frozenset(c['numbers']) for c in existing_combinations]
    
    for i, combo in enumerate(new_combinations):
        numbers_set = frozenset(combo['numbers'])
        
        # Check if this combination is a duplicate of an existing one
        if numbers_set in existing_number_sets:
            # Replace with a new combination
            risk_level = random.uniform(0.4, 0.7)
            new_combo = create_balanced_risk(risk_level)
            
            # Make sure the replacement is not a duplicate either
            attempts = 0
            while frozenset(new_combo['numbers']) in existing_number_sets and attempts < 5:
                risk_level = random.uniform(0.3, 0.8)
                new_combo = create_balanced_risk(risk_level)
                attempts += 1
            
            # Update the combination
            new_combinations[i] = new_combo
            
            # Add to the existing set to continue checking for duplicates
            existing_number_sets.append(frozenset(new_combo['numbers']))
    
    # Now check for duplicates within the new combinations themselves
    for i in range(len(new_combinations)):
        for j in range(i+1, len(new_combinations)):
            if frozenset(new_combinations[i]['numbers']) == frozenset(new_combinations[j]['numbers']):
                # Replace the second duplicate
                risk_level = random.uniform(0.3, 0.8)
                new_combo = create_balanced_risk(risk_level)
                
                # Make sure the replacement is not a duplicate
                attempts = 0
                current_sets = [frozenset(c['numbers']) for c in existing_combinations + new_combinations]
                while frozenset(new_combo['numbers']) in current_sets and attempts < 5:
                    risk_level = random.uniform(0.3, 0.8)
                    new_combo = create_balanced_risk(risk_level)
                    attempts += 1
                
                # Update the combination
                new_combinations[j] = new_combo

def main():
    """Generate 10 additional optimized French Loto combinations"""
    print("Retrieving existing combinations...")
    existing_combinations = get_existing_combinations()
    
    if not existing_combinations:
        print("No existing combinations found. Please run french_loto_optimized.py first.")
        return
    
    print(f"Found {len(existing_combinations)} existing combinations.")
    
    # Analyze coverage of existing combinations
    coverage_stats = analyze_number_coverage(existing_combinations)
    
    print(f"Uncovered numbers: {coverage_stats['uncovered']}")
    print(f"Underrepresented numbers: {coverage_stats['underrepresented']}")
    print(f"Overrepresented numbers: {coverage_stats['overrepresented']}")
    
    # Generate new combinations using a variety of methods
    new_combinations = []
    
    # 1. Create 2 pattern hybrid combinations
    for _ in range(2):
        new_combinations.append(create_pattern_hybrid(existing_combinations, coverage_stats))
    
    # 2. Create 2 coverage-optimized combinations
    for _ in range(2):
        new_combinations.append(create_coverage_optimized(existing_combinations, coverage_stats))
    
    # 3. Create 2 balanced risk combinations with different risk levels
    new_combinations.append(create_balanced_risk(0.3))  # Low risk
    new_combinations.append(create_balanced_risk(0.7))  # High risk
    
    # 4. Create 1 frequency-based combination
    new_combinations.append(create_frequency_based())
    
    # 5. Create 1 lucky number focused combination
    new_combinations.append(create_lucky_number_focus())
    
    # 6. Create 2 hybrid combinations by mixing pairs of top existing combinations
    new_combinations.append(create_mix_combination(existing_combinations, 0, 1))  # Mix top 2
    new_combinations.append(create_mix_combination(existing_combinations, 2, 3))  # Mix 3rd and 4th
    
    # Ensure all combinations are unique
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
    
    # Show overall coverage statistics for all 20 combinations combined
    all_combinations = existing_combinations + new_combinations
    final_coverage_stats = analyze_number_coverage(all_combinations)
    
    total_numbers_used = sum(final_coverage_stats['number_freq'].values())
    unique_numbers_used = len(final_coverage_stats['number_freq'])
    
    print(f"\nFinal Coverage Analysis (All 20 Combinations):")
    print(f"Total numbers used: {total_numbers_used}")
    print(f"Unique numbers used: {unique_numbers_used}/49")
    print(f"Uncovered numbers: {len(final_coverage_stats['uncovered'])}")
    print(f"Average usage per number: {total_numbers_used/unique_numbers_used:.2f}")
    
    # Calculate and display coverage percentage
    coverage_percent = (unique_numbers_used / 49) * 100
    print(f"Number coverage: {coverage_percent:.1f}%")
    
    return new_combinations

if __name__ == "__main__":
    main()