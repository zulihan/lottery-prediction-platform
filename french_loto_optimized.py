"""
Script to generate optimized French Loto combinations based on historical data analysis
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import random
import json
from collections import Counter
from database import get_session, FrenchLotoDrawing, add_french_loto_drawing, get_french_loto_drawings
from sqlalchemy import desc, func

def get_recent_drawings(num_draws=10):
    """
    Get the most recent French Loto drawings from the database.
    
    Args:
        num_draws: Number of recent draws to retrieve
        
    Returns:
        list: List of FrenchLotoDrawing objects
    """
    session = get_session()
    try:
        recent_drawings = session.query(FrenchLotoDrawing) \
            .order_by(desc(FrenchLotoDrawing.date)) \
            .limit(num_draws) \
            .all()
        return recent_drawings
    finally:
        session.close()

def analyze_recent_draws(num_draws=10):
    """
    Analyze recent French Loto drawings for patterns.
    
    Returns:
        dict: Analysis results
    """
    drawings = get_recent_drawings(num_draws)
    
    if not drawings:
        print("No drawings found in the database.")
        return None
    
    # Initialize counters
    numbers = []
    lucky_numbers = []
    even_count = 0
    total_numbers = 0
    sum_values = []
    
    # Range analysis
    range_1_10 = 0
    range_11_20 = 0
    range_21_30 = 0
    range_31_40 = 0
    range_41_50 = 0
    
    # Analyze each drawing
    for drawing in drawings:
        draw_numbers = [drawing.n1, drawing.n2, drawing.n3, drawing.n4, drawing.n5]
        numbers.extend(draw_numbers)
        lucky_numbers.append(drawing.lucky)
        
        # Count even numbers
        even_count += sum(1 for n in draw_numbers if n % 2 == 0)
        total_numbers += len(draw_numbers)
        
        # Calculate sum
        sum_values.append(sum(draw_numbers))
        
        # Analyze number ranges
        range_1_10 += sum(1 for n in draw_numbers if 1 <= n <= 10)
        range_11_20 += sum(1 for n in draw_numbers if 11 <= n <= 20)
        range_21_30 += sum(1 for n in draw_numbers if 21 <= n <= 30)
        range_31_40 += sum(1 for n in draw_numbers if 31 <= n <= 40)
        range_41_50 += sum(1 for n in draw_numbers if 41 <= n <= 49)
    
    # Count frequencies
    number_freq = Counter(numbers)
    lucky_freq = Counter(lucky_numbers)
    
    # Get hot and cold numbers
    hot_numbers = [num for num, count in number_freq.most_common(10)]
    cold_numbers = [num for num, count in sorted(number_freq.items(), key=lambda x: x[1])[:10]]
    
    # Get hot and cold lucky numbers
    hot_lucky = [num for num, count in lucky_freq.most_common(5)]
    cold_lucky = [num for num, count in sorted(lucky_freq.items(), key=lambda x: x[1])[:5]]
    
    # Calculate statistics
    even_ratio = even_count / total_numbers
    odd_ratio = 1 - even_ratio
    
    avg_sum = sum(sum_values) / len(sum_values)
    min_sum = min(sum_values)
    max_sum = max(sum_values)
    
    # Calculate range distribution
    total_range = range_1_10 + range_11_20 + range_21_30 + range_31_40 + range_41_50
    range_dist = {
        "1-10": range_1_10 / total_range,
        "11-20": range_11_20 / total_range,
        "21-30": range_21_30 / total_range,
        "31-40": range_31_40 / total_range,
        "41-49": range_41_50 / total_range
    }
    
    # Check for repeating patterns
    repeating_pairs = []
    for i in range(len(drawings)-1):
        curr_numbers = set([drawings[i].n1, drawings[i].n2, drawings[i].n3, 
                           drawings[i].n4, drawings[i].n5])
        next_numbers = set([drawings[i+1].n1, drawings[i+1].n2, drawings[i+1].n3, 
                           drawings[i+1].n4, drawings[i+1].n5])
        
        common = curr_numbers.intersection(next_numbers)
        if common:
            repeating_pairs.extend(list(common))
    
    repeating_freq = Counter(repeating_pairs)
    most_repeating = [num for num, count in repeating_freq.most_common(5)]
    
    return {
        "hot_numbers": hot_numbers,
        "cold_numbers": cold_numbers,
        "hot_lucky": hot_lucky,
        "cold_lucky": cold_lucky,
        "even_ratio": even_ratio,
        "odd_ratio": odd_ratio,
        "avg_sum": avg_sum,
        "min_sum": min_sum,
        "max_sum": max_sum,
        "range_distribution": range_dist,
        "most_repeating": most_repeating
    }

def get_historical_patterns():
    """
    Analyze all historical drawings for long-term patterns.
    
    Returns:
        dict: Analysis results for long-term patterns
    """
    session = get_session()
    try:
        all_drawings = session.query(FrenchLotoDrawing).order_by(FrenchLotoDrawing.date).all()
        
        # Initialize pattern analysis
        consecutive_counts = 0
        total_pairs = 0
        
        # For finding patterns in consecutive numbers
        for drawing in all_drawings:
            numbers = sorted([drawing.n1, drawing.n2, drawing.n3, drawing.n4, drawing.n5])
            
            # Check for consecutive numbers
            for i in range(len(numbers)-1):
                total_pairs += 1
                if numbers[i+1] - numbers[i] == 1:
                    consecutive_counts += 1
        
        consecutive_ratio = consecutive_counts / total_pairs if total_pairs > 0 else 0
        
        return {
            "consecutive_ratio": consecutive_ratio
        }
    finally:
        session.close()

def generate_frequency_combinations(num_combinations=5):
    """
    Generate combinations based on frequency analysis.
    Uses the most frequently drawn numbers with some randomization.
    
    Args:
        num_combinations: Number of combinations to generate
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    # Get all drawings for frequency analysis
    session = get_session()
    try:
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
        
        # Generate combinations
        combinations = []
        for i in range(num_combinations):
            # Use weighted sampling for main numbers
            selected_numbers = np.random.choice(
                list(number_probs.keys()),
                size=5,
                replace=False,
                p=list(number_probs.values())
            )
            
            # Use weighted sampling for lucky number
            lucky_number = np.random.choice(
                list(lucky_probs.keys()),
                size=1,
                p=list(lucky_probs.values())
            )[0]
            
            combinations.append({
                "numbers": sorted(selected_numbers.tolist()),
                "lucky_number": int(lucky_number),
                "strategy": "Frequency Analysis",
                "score": 0  # Will calculate later
            })
        
        return combinations
    finally:
        session.close()

def generate_hot_cold_combinations(num_combinations=5, hot_ratio=0.6):
    """
    Generate combinations using a mix of hot and cold numbers.
    
    Args:
        num_combinations: Number of combinations to generate
        hot_ratio: Ratio of hot numbers to include (0-1)
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    analysis = analyze_recent_draws(20)  # Analyze last 20 draws
    
    if not analysis:
        return []
    
    combinations = []
    for i in range(num_combinations):
        # Determine number of hot vs cold numbers
        num_hot = int(5 * hot_ratio)
        num_cold = 5 - num_hot
        
        # Sample hot and cold numbers
        selected_hot = random.sample(analysis["hot_numbers"], min(num_hot, len(analysis["hot_numbers"])))
        
        # Ensure we don't select the same number twice
        remaining_cold = [n for n in analysis["cold_numbers"] if n not in selected_hot]
        selected_cold = random.sample(remaining_cold, min(num_cold, len(remaining_cold)))
        
        # If we need more numbers, select from the middle range
        selected = selected_hot + selected_cold
        while len(selected) < 5:
            # Select from numbers not in hot or cold lists
            middle_range = [n for n in range(1, 50) if n not in selected and 
                            n not in analysis["hot_numbers"] and 
                            n not in analysis["cold_numbers"]]
            if middle_range:
                selected.append(random.choice(middle_range))
            else:
                # If somehow we run out of middle range numbers, use any available
                available = [n for n in range(1, 50) if n not in selected]
                if available:
                    selected.append(random.choice(available))
                else:
                    break  # This should never happen with 5 numbers out of 49
        
        # For lucky number, prefer hot ones
        lucky = random.choice(analysis["hot_lucky"])
        
        combinations.append({
            "numbers": sorted(selected),
            "lucky_number": lucky,
            "strategy": f"Hot/Cold ({hot_ratio:.1f})",
            "score": 0  # Will calculate later
        })
    
    return combinations

def generate_pattern_combinations(num_combinations=5):
    """
    Generate combinations based on patterns in the recent drawings.
    
    Args:
        num_combinations: Number of combinations to generate
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    recent_analysis = analyze_recent_draws(10)
    historical_patterns = get_historical_patterns()
    
    if not recent_analysis:
        return []
    
    combinations = []
    for i in range(num_combinations):
        # Start with a base set of numbers that includes some repeating numbers
        base_numbers = []
        
        # Include 1-2 of the most repeating numbers
        num_repeating = random.randint(1, min(2, len(recent_analysis["most_repeating"])))
        if recent_analysis["most_repeating"]:
            base_numbers.extend(random.sample(recent_analysis["most_repeating"], num_repeating))
        
        # Add some hot numbers
        remaining_hot = [n for n in recent_analysis["hot_numbers"] if n not in base_numbers]
        num_hot = random.randint(1, min(2, len(remaining_hot)))
        if remaining_hot:
            base_numbers.extend(random.sample(remaining_hot, num_hot))
        
        # Fill the rest based on range distribution
        remaining_slots = 5 - len(base_numbers)
        if remaining_slots > 0:
            range_dist = recent_analysis["range_distribution"]
            
            # Calculate how many numbers to take from each range
            range_counts = {
                "1-10": int(remaining_slots * range_dist["1-10"]),
                "11-20": int(remaining_slots * range_dist["11-20"]),
                "21-30": int(remaining_slots * range_dist["21-30"]),
                "31-40": int(remaining_slots * range_dist["31-40"]),
                "41-49": int(remaining_slots * range_dist["41-49"])
            }
            
            # Adjust for rounding errors
            total_allocated = sum(range_counts.values())
            if total_allocated < remaining_slots:
                # Add the remaining to the highest probability range
                highest_range = max(range_dist.items(), key=lambda x: x[1])[0]
                range_counts[highest_range] += remaining_slots - total_allocated
            
            # Select numbers from each range
            for range_str, count in range_counts.items():
                if count <= 0:
                    continue
                    
                start, end = map(int, range_str.split("-"))
                
                # Available numbers in this range that aren't already selected
                available = [n for n in range(start, end+1) if n not in base_numbers]
                
                # Sample from available numbers
                if available:
                    base_numbers.extend(random.sample(available, min(count, len(available))))
        
        # If we still don't have 5 numbers, add random ones
        while len(base_numbers) < 5:
            available = [n for n in range(1, 50) if n not in base_numbers]
            if available:
                base_numbers.append(random.choice(available))
            else:
                break
        
        # For lucky number, use a mix strategy
        if random.random() < 0.7:  # 70% chance to use a hot lucky number
            lucky = random.choice(recent_analysis["hot_lucky"])
        else:  # 30% chance to use a cold lucky number
            lucky = random.choice(recent_analysis["cold_lucky"])
        
        combinations.append({
            "numbers": sorted(base_numbers),
            "lucky_number": lucky,
            "strategy": "Pattern Analysis",
            "score": 0  # Will calculate later
        })
    
    return combinations

def generate_balanced_combinations(num_combinations=5, risk_level=0.5):
    """
    Generate combinations with a balanced approach based on historical data.
    
    Args:
        num_combinations: Number of combinations to generate
        risk_level: Risk level (0-1), higher means more cold/overdue numbers
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    recent_analysis = analyze_recent_draws(20)
    
    if not recent_analysis:
        return []
    
    combinations = []
    for i in range(num_combinations):
        # Mix of hot and cold numbers based on risk level
        num_hot = max(1, min(4, int(5 * (1 - risk_level))))
        num_cold = 5 - num_hot
        
        # Select hot numbers
        selected_hot = random.sample(recent_analysis["hot_numbers"], min(num_hot, len(recent_analysis["hot_numbers"])))
        
        # Select cold numbers
        remaining_cold = [n for n in recent_analysis["cold_numbers"] if n not in selected_hot]
        selected_cold = random.sample(remaining_cold, min(num_cold, len(remaining_cold)))
        
        # Combine selections
        selected_numbers = selected_hot + selected_cold
        
        # If we need more numbers, add balanced ones
        while len(selected_numbers) < 5:
            available = [n for n in range(1, 50) if n not in selected_numbers]
            if available:
                selected_numbers.append(random.choice(available))
            else:
                break
        
        # For lucky number, use hot or cold based on risk level
        if random.random() < risk_level:
            lucky = random.choice(recent_analysis["cold_lucky"])
        else:
            lucky = random.choice(recent_analysis["hot_lucky"])
        
        combinations.append({
            "numbers": sorted(selected_numbers),
            "lucky_number": lucky,
            "strategy": f"Balanced Risk ({risk_level:.1f})",
            "score": 0  # Will calculate later
        })
    
    return combinations

def evaluate_combination(combination, recent_analysis):
    """
    Evaluate a combination based on various factors and assign a score.
    
    Args:
        combination: Dictionary with 'numbers' and 'lucky_number'
        recent_analysis: Dictionary with recent draw analysis results
        
    Returns:
        float: Score from 0-100
    """
    score = 50  # Start with a neutral score
    
    numbers = combination["numbers"]
    lucky = combination["lucky_number"]
    
    # Factor 1: Number of hot numbers (positive)
    hot_count = len([n for n in numbers if n in recent_analysis["hot_numbers"]])
    score += hot_count * 3
    
    # Factor 2: Sum within typical range (positive)
    sum_numbers = sum(numbers)
    avg_sum = recent_analysis["avg_sum"]
    if abs(sum_numbers - avg_sum) < 10:
        score += 5
    elif abs(sum_numbers - avg_sum) < 20:
        score += 2
    
    # Factor 3: Even/odd ratio similar to historical (positive)
    even_count = len([n for n in numbers if n % 2 == 0])
    historical_even_ratio = recent_analysis["even_ratio"]
    if abs(even_count/5 - historical_even_ratio) < 0.2:
        score += 5
    
    # Factor 4: Range distribution similar to historical (positive)
    range_counts = {
        "1-10": len([n for n in numbers if 1 <= n <= 10]),
        "11-20": len([n for n in numbers if 11 <= n <= 20]),
        "21-30": len([n for n in numbers if 21 <= n <= 30]),
        "31-40": len([n for n in numbers if 31 <= n <= 40]),
        "41-49": len([n for n in numbers if 41 <= n <= 49])
    }
    
    range_similarity = 0
    for range_key, count in range_counts.items():
        expected = 5 * recent_analysis["range_distribution"][range_key]
        range_similarity += 5 - abs(count - expected)
    
    score += range_similarity
    
    # Factor 5: Hot lucky number (positive)
    if lucky in recent_analysis["hot_lucky"]:
        score += 5
    
    # Factor 6: Includes some repeating numbers (positive)
    repeating_count = len([n for n in numbers if n in recent_analysis["most_repeating"]])
    score += repeating_count * 2
    
    # Normalize score to 0-100 range
    score = max(0, min(100, score))
    
    return score

def generate_all_combinations(num_total=10):
    """
    Generate a set of optimized French Loto combinations using multiple strategies.
    
    Args:
        num_total: Total number of combinations to generate
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    # Allocate combinations across strategies
    num_freq = max(1, int(num_total * 0.2))
    num_hot_cold = max(1, int(num_total * 0.3))
    num_pattern = max(1, int(num_total * 0.2))
    num_balanced = num_total - num_freq - num_hot_cold - num_pattern
    
    # Generate combinations using each strategy
    all_combinations = []
    all_combinations.extend(generate_frequency_combinations(num_freq))
    all_combinations.extend(generate_hot_cold_combinations(num_hot_cold))
    all_combinations.extend(generate_pattern_combinations(num_pattern))
    all_combinations.extend(generate_balanced_combinations(num_balanced))
    
    # Evaluate all combinations
    recent_analysis = analyze_recent_draws(20)
    for combo in all_combinations:
        combo["score"] = evaluate_combination(combo, recent_analysis)
    
    # Sort by score (descending)
    all_combinations.sort(key=lambda x: x["score"], reverse=True)
    
    return all_combinations

def save_combinations_to_database(combinations):
    """
    Save generated combinations to the database.
    
    Args:
        combinations: List of dictionaries with generated combinations
        
    Returns:
        bool: Success indicator
    """
    from database import GeneratedCombination, get_session
    from datetime import date
    import json
    
    session = get_session()
    try:
        for combo in combinations:
            # Create new combination record - note that our schema doesn't have lottery_type field
            new_combo = GeneratedCombination(
                created_at=date.today(),
                target_draw_date=date.today(),  # Assuming today's draw
                strategy=combo["strategy"],
                numbers=json.dumps(combo["numbers"]),
                stars=json.dumps([combo["lucky_number"]]),  # Store lucky as a list for API compatibility
                score=combo["score"]
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
    """Generate optimized French Loto combinations for tonight's draw"""
    print("Analyzing French Loto historical data...")
    recent_analysis = analyze_recent_draws(20)
    
    if not recent_analysis:
        print("No French Loto data found. Please ensure the database is populated.")
        return
    
    print("\nRecent French Loto Analysis:")
    print(f"Hot Numbers: {recent_analysis['hot_numbers']}")
    print(f"Cold Numbers: {recent_analysis['cold_numbers']}")
    print(f"Hot Lucky Numbers: {recent_analysis['hot_lucky']}")
    print(f"Cold Lucky Numbers: {recent_analysis['cold_lucky']}")
    print(f"Even/Odd Ratio: {recent_analysis['even_ratio']:.2f}/{recent_analysis['odd_ratio']:.2f}")
    print(f"Typical Sum Range: {int(recent_analysis['min_sum'])} - {int(recent_analysis['max_sum'])}")
    print(f"Most Frequently Repeating Numbers: {recent_analysis['most_repeating']}")
    
    print("\nGenerating optimized combinations...")
    combinations = generate_all_combinations(10)
    
    print("\nOptimized Combinations for Tonight's French Loto Draw:")
    for i, combo in enumerate(combinations, 1):
        numbers_str = ", ".join(map(str, combo["numbers"]))
        print(f"Combination {i} ({combo['strategy']}):")
        print(f"  Numbers: {numbers_str}")
        print(f"  Lucky Number: {combo['lucky_number']}")
        print(f"  Score: {combo['score']:.2f}")
        print()
    
    # Save to database
    print("Saving combinations to database...")
    if save_combinations_to_database(combinations):
        print("Combinations saved successfully.")
    else:
        print("Failed to save combinations to database.")
    
    return combinations

if __name__ == "__main__":
    main()