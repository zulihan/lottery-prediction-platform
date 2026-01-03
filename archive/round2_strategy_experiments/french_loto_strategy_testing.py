"""
Script to analyze which strategies would have performed best against recent French Loto draws.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from database import get_session, FrenchLotoDrawing
from sqlalchemy import desc, func
import random
from collections import Counter

def get_recent_drawings(num_draws=10):
    """
    Get the most recent French Loto drawings from the database.
    
    Args:
        num_draws: Number of recent draws to retrieve
        
    Returns:
        list: List of FrenchLotoDrawing objects
    """
    session = get_session()
    recent_drawings = session.query(FrenchLotoDrawing) \
        .order_by(desc(FrenchLotoDrawing.date)) \
        .limit(num_draws) \
        .all()
    session.close()
    return recent_drawings

def get_historical_data(exclude_recent=5):
    """
    Get historical French Loto data, excluding the most recent drawings.
    
    Args:
        exclude_recent: Number of recent drawings to exclude from the training data
        
    Returns:
        list: List of FrenchLotoDrawing objects
    """
    session = get_session()
    
    # Get the date of the Nth most recent drawing
    subquery = session.query(FrenchLotoDrawing.date) \
        .order_by(desc(FrenchLotoDrawing.date)) \
        .limit(exclude_recent) \
        .subquery()
    
    # Get all drawings before that date
    historical_data = session.query(FrenchLotoDrawing) \
        .filter(FrenchLotoDrawing.date < session.query(func.min(subquery.c.date))) \
        .order_by(desc(FrenchLotoDrawing.date)) \
        .all()
    
    session.close()
    return historical_data

def calculate_frequencies(historical_data):
    """
    Calculate frequencies of numbers and lucky numbers from historical data.
    
    Args:
        historical_data: List of FrenchLotoDrawing objects
        
    Returns:
        tuple: (number_frequencies, lucky_frequencies)
    """
    numbers = []
    lucky_numbers = []
    
    for drawing in historical_data:
        numbers.extend([drawing.n1, drawing.n2, drawing.n3, 
                        drawing.n4, drawing.n5])
        lucky_numbers.append(drawing.lucky)
    
    number_counts = Counter(numbers)
    lucky_counts = Counter(lucky_numbers)
    
    # Convert to frequency (probability)
    total_numbers = len(numbers)
    total_lucky = len(lucky_numbers)
    
    number_frequencies = {num: count/total_numbers for num, count in number_counts.items()}
    lucky_frequencies = {num: count/total_lucky for num, count in lucky_counts.items()}
    
    return number_frequencies, lucky_frequencies

def get_hot_numbers(number_frequencies, count=10):
    """
    Get the hot numbers (most frequent) from the frequencies.
    
    Args:
        number_frequencies: Dictionary of number frequencies
        count: Number of hot numbers to return
        
    Returns:
        list: Hot numbers
    """
    return [num for num, _ in sorted(number_frequencies.items(), 
                                     key=lambda x: x[1], 
                                     reverse=True)[:count]]

def get_cold_numbers(number_frequencies, count=10):
    """
    Get the cold numbers (least frequent) from the frequencies.
    
    Args:
        number_frequencies: Dictionary of number frequencies
        count: Number of cold numbers to return
        
    Returns:
        list: Cold numbers
    """
    return [num for num, _ in sorted(number_frequencies.items(), 
                                    key=lambda x: x[1])[:count]]

def get_overdue_numbers(historical_data, count=10):
    """
    Get numbers that haven't appeared for the longest time.
    
    Args:
        historical_data: List of FrenchLotoDrawing objects
        count: Number of overdue numbers to return
        
    Returns:
        list: Overdue numbers
    """
    # Initialize last appearance dictionary for all possible numbers
    last_appearance = {num: None for num in range(1, 50)}
    
    # Track the most recent appearance of each number
    for i, drawing in enumerate(historical_data):
        for num in [drawing.n1, drawing.n2, drawing.n3, 
                    drawing.n4, drawing.n5]:
            if last_appearance[num] is None:
                last_appearance[num] = i
    
    # Sort by least recent appearance (highest index value)
    overdue = sorted([(num, idx) for num, idx in last_appearance.items() if idx is not None], 
                    key=lambda x: x[1], 
                    reverse=True)
    
    return [num for num, _ in overdue[:count]]

def generate_frequency_strategy(historical_data, num_combinations=5):
    """
    Generate combinations using frequency analysis.
    
    Args:
        historical_data: List of FrenchLotoDrawing objects
        num_combinations: Number of combinations to generate
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    number_frequencies, lucky_frequencies = calculate_frequencies(historical_data)
    
    combinations = []
    for _ in range(num_combinations):
        # Sample 5 main numbers based on frequencies
        numbers = list(np.random.choice(
            list(number_frequencies.keys()), 
            size=5, 
            replace=False, 
            p=list(number_frequencies.values())
        ))
        
        # Sample lucky number based on frequencies
        lucky = np.random.choice(
            list(lucky_frequencies.keys()),
            size=1,
            p=list(lucky_frequencies.values())
        )[0]
        
        combinations.append({
            'numbers': sorted(numbers),
            'lucky_number': lucky,
            'strategy': 'Frequency Analysis'
        })
    
    return combinations

def generate_hot_cold_strategy(historical_data, num_combinations=5, hot_ratio=0.6):
    """
    Generate combinations using hot and cold numbers.
    
    Args:
        historical_data: List of FrenchLotoDrawing objects
        num_combinations: Number of combinations to generate
        hot_ratio: Ratio of hot numbers to include (0-1)
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    number_frequencies, lucky_frequencies = calculate_frequencies(historical_data)
    hot_numbers = get_hot_numbers(number_frequencies, count=20)
    cold_numbers = get_cold_numbers(number_frequencies, count=20)
    
    combinations = []
    for _ in range(num_combinations):
        # Determine number of hot vs cold numbers
        num_hot = int(5 * hot_ratio)
        num_cold = 5 - num_hot
        
        # Sample hot and cold numbers
        selected_hot = random.sample(hot_numbers, num_hot)
        selected_cold = random.sample(cold_numbers, num_cold)
        
        numbers = selected_hot + selected_cold
        
        # For lucky number, prefer hot ones
        hot_lucky = get_hot_numbers(lucky_frequencies, count=5)
        lucky = random.choice(hot_lucky)
        
        combinations.append({
            'numbers': sorted(numbers),
            'lucky_number': lucky,
            'strategy': f'Hot/Cold ({hot_ratio:.1f})'
        })
    
    return combinations

def generate_overdue_strategy(historical_data, num_combinations=5, overdue_ratio=0.6):
    """
    Generate combinations using overdue numbers.
    
    Args:
        historical_data: List of FrenchLotoDrawing objects
        num_combinations: Number of combinations to generate
        overdue_ratio: Ratio of overdue numbers to include (0-1)
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    number_frequencies, lucky_frequencies = calculate_frequencies(historical_data)
    overdue_numbers = get_overdue_numbers(historical_data, count=20)
    hot_numbers = get_hot_numbers(number_frequencies, count=20)
    
    combinations = []
    for _ in range(num_combinations):
        # Determine number of overdue vs hot numbers
        num_overdue = int(5 * overdue_ratio)
        num_hot = 5 - num_overdue
        
        # Sample overdue and hot numbers
        selected_overdue = random.sample(overdue_numbers, num_overdue)
        selected_hot = random.sample([n for n in hot_numbers if n not in selected_overdue], num_hot)
        
        numbers = selected_overdue + selected_hot
        
        # For lucky number, alternate between hot and overdue
        hot_lucky = get_hot_numbers(lucky_frequencies, count=5)
        overdue_lucky = sorted(lucky_frequencies.keys(), 
                              key=lambda x: lucky_frequencies[x])[:5]
        
        lucky = random.choice(overdue_lucky) if random.random() < 0.5 else random.choice(hot_lucky)
        
        combinations.append({
            'numbers': sorted(numbers),
            'lucky_number': lucky,
            'strategy': f'Overdue ({overdue_ratio:.1f})'
        })
    
    return combinations

def generate_pattern_strategy(historical_data, num_combinations=5):
    """
    Generate combinations based on patterns in recent draws.
    
    Args:
        historical_data: List of FrenchLotoDrawing objects
        num_combinations: Number of combinations to generate
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    # Extract recent drawing details for pattern analysis
    recent = historical_data[:10]
    
    # Analyze distribution of even/odd numbers
    even_count = 0
    total_numbers = 0
    
    # Analyze sum ranges
    sums = []
    
    # Analyze number ranges
    low_range = 0  # 1-16
    mid_range = 0  # 17-33
    high_range = 0  # 34-49
    total_range_counts = 0
    
    for drawing in recent:
        numbers = [drawing.n1, drawing.n2, drawing.n3, 
                  drawing.n4, drawing.n5]
        
        # Count even numbers
        even_count += sum(1 for n in numbers if n % 2 == 0)
        total_numbers += len(numbers)
        
        # Calculate sum
        sums.append(sum(numbers))
        
        # Count number ranges
        low_range += sum(1 for n in numbers if 1 <= n <= 16)
        mid_range += sum(1 for n in numbers if 17 <= n <= 33)
        high_range += sum(1 for n in numbers if 34 <= n <= 49)
        total_range_counts += len(numbers)
    
    # Calculate probabilities
    even_prob = even_count / total_numbers
    low_prob = low_range / total_range_counts
    mid_prob = mid_range / total_range_counts
    high_prob = high_range / total_range_counts
    
    # Calculate typical sum range
    mean_sum = sum(sums) / len(sums)
    min_sum = min(sums)
    max_sum = max(sums)
    
    # Generate combinations based on observed patterns
    number_frequencies, lucky_frequencies = calculate_frequencies(historical_data)
    combinations = []
    
    for _ in range(num_combinations):
        # Generate candidate pool with more numbers than needed
        candidates = list(range(1, 50))
        random.shuffle(candidates)
        
        # Apply even/odd pattern
        num_even = int(5 * even_prob)
        num_odd = 5 - num_even
        
        selected = []
        
        # Select according to range distribution
        num_low = int(5 * low_prob)
        num_mid = int(5 * mid_prob)
        num_high = 5 - num_low - num_mid
        
        # Adjust if necessary
        if num_low + num_mid + num_high != 5:
            num_high += 5 - (num_low + num_mid + num_high)
        
        # Select low range
        low_candidates = [n for n in candidates if 1 <= n <= 16]
        selected.extend(random.sample(low_candidates, min(num_low, len(low_candidates))))
        
        # Select mid range
        mid_candidates = [n for n in candidates if 17 <= n <= 33 and n not in selected]
        selected.extend(random.sample(mid_candidates, min(num_mid, len(mid_candidates))))
        
        # Select high range
        high_candidates = [n for n in candidates if 34 <= n <= 49 and n not in selected]
        selected.extend(random.sample(high_candidates, min(num_high, len(high_candidates))))
        
        # Fill remaining spots if needed
        remaining = [n for n in candidates if n not in selected]
        while len(selected) < 5 and remaining:
            selected.append(remaining.pop(0))
        
        # Make sure sum is in the typical range (allow some variance)
        sum_selected = sum(selected)
        attempts = 0
        
        # Try to get sum in typical range, but don't get stuck in infinite loop
        while (sum_selected < min_sum * 0.9 or sum_selected > max_sum * 1.1) and attempts < 5:
            if len(selected) < 5:
                break
                
            # Replace a random number
            idx_to_replace = random.randint(0, 4)
            replacement_candidates = [n for n in range(1, 50) if n not in selected]
            
            if replacement_candidates:
                # Try to push sum towards mean
                if sum_selected < mean_sum:
                    higher_replacements = [n for n in replacement_candidates if n > selected[idx_to_replace]]
                    if higher_replacements:
                        selected[idx_to_replace] = random.choice(higher_replacements)
                else:
                    lower_replacements = [n for n in replacement_candidates if n < selected[idx_to_replace]]
                    if lower_replacements:
                        selected[idx_to_replace] = random.choice(lower_replacements)
                        
                sum_selected = sum(selected)
            
            attempts += 1
        
        # Choose lucky number based on frequency
        hot_lucky = get_hot_numbers(lucky_frequencies, count=5)
        lucky = random.choice(hot_lucky)
        
        combinations.append({
            'numbers': sorted(selected),
            'lucky_number': lucky,
            'strategy': 'Pattern Analysis'
        })
    
    return combinations

def generate_balanced_strategy(historical_data, num_combinations=5, risk_level=0.5):
    """
    Generate combinations using a balanced approach of hot, cold, and overdue numbers.
    
    Args:
        historical_data: List of FrenchLotoDrawing objects
        num_combinations: Number of combinations to generate
        risk_level: Risk level (0-1), higher means more overdue numbers
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    number_frequencies, lucky_frequencies = calculate_frequencies(historical_data)
    hot_numbers = get_hot_numbers(number_frequencies, count=15)
    cold_numbers = get_cold_numbers(number_frequencies, count=15)
    overdue_numbers = get_overdue_numbers(historical_data, count=15)
    
    combinations = []
    for _ in range(num_combinations):
        # Allocate numbers based on risk level
        num_hot = max(1, min(3, int(5 * (1 - risk_level))))
        num_overdue = max(1, min(3, int(5 * risk_level)))
        num_cold = 5 - num_hot - num_overdue
        
        # Sample hot, cold and overdue numbers
        selected_hot = random.sample(hot_numbers, num_hot)
        
        # Avoid duplicates
        remaining_cold = [n for n in cold_numbers if n not in selected_hot]
        selected_cold = random.sample(remaining_cold, min(num_cold, len(remaining_cold)))
        
        remaining_overdue = [n for n in overdue_numbers if n not in selected_hot + selected_cold]
        selected_overdue = random.sample(remaining_overdue, min(num_overdue, len(remaining_overdue)))
        
        # Combine all selections
        selected = selected_hot + selected_cold + selected_overdue
        
        # Fill any remaining slots if needed
        if len(selected) < 5:
            remaining = [n for n in range(1, 50) if n not in selected]
            selected.extend(random.sample(remaining, 5 - len(selected)))
        
        # For lucky number, use hot or overdue based on risk level
        if random.random() < risk_level:
            overdue_lucky = sorted(lucky_frequencies.keys(), 
                                  key=lambda x: lucky_frequencies[x])[:5]
            lucky = random.choice(overdue_lucky)
        else:
            hot_lucky = get_hot_numbers(lucky_frequencies, count=5)
            lucky = random.choice(hot_lucky)
        
        combinations.append({
            'numbers': sorted(selected),
            'lucky_number': lucky,
            'strategy': f'Balanced (Risk: {risk_level:.1f})'
        })
    
    return combinations

def generate_all_strategies(historical_data, num_combinations_per_strategy=2):
    """
    Generate combinations using all strategies.
    
    Args:
        historical_data: List of FrenchLotoDrawing objects
        num_combinations_per_strategy: Number of combinations to generate per strategy
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    all_combinations = []
    
    # Generate combinations for each strategy
    all_combinations.extend(generate_frequency_strategy(historical_data, num_combinations_per_strategy))
    
    all_combinations.extend(generate_hot_cold_strategy(historical_data, num_combinations_per_strategy, hot_ratio=0.8))
    all_combinations.extend(generate_hot_cold_strategy(historical_data, num_combinations_per_strategy, hot_ratio=0.6))
    
    all_combinations.extend(generate_overdue_strategy(historical_data, num_combinations_per_strategy, overdue_ratio=0.6))
    all_combinations.extend(generate_overdue_strategy(historical_data, num_combinations_per_strategy, overdue_ratio=0.4))
    
    all_combinations.extend(generate_pattern_strategy(historical_data, num_combinations_per_strategy))
    
    all_combinations.extend(generate_balanced_strategy(historical_data, num_combinations_per_strategy, risk_level=0.3))
    all_combinations.extend(generate_balanced_strategy(historical_data, num_combinations_per_strategy, risk_level=0.5))
    all_combinations.extend(generate_balanced_strategy(historical_data, num_combinations_per_strategy, risk_level=0.7))
    
    return all_combinations

def check_matches(combination, actual_drawing):
    """
    Check how many numbers in the combination match the actual drawing.
    
    Args:
        combination: Dictionary with 'numbers' and 'lucky_number'
        actual_drawing: FrenchLotoDrawing object
        
    Returns:
        tuple: (num_matches, lucky_match, score)
    """
    actual_numbers = [
        actual_drawing.n1, 
        actual_drawing.n2, 
        actual_drawing.n3,
        actual_drawing.n4,
        actual_drawing.n5
    ]
    
    num_matches = len([n for n in combination['numbers'] if n in actual_numbers])
    lucky_match = 1 if combination['lucky_number'] == actual_drawing.lucky else 0
    
    # Score calculation: each number = 2 points, lucky number = 1 point
    score = num_matches * 2 + lucky_match
    
    return (num_matches, lucky_match, score)

def test_strategies_against_actual(all_combinations, recent_drawings):
    """
    Test how well each strategy performed against actual drawings.
    
    Args:
        all_combinations: List of dictionaries with generated combinations
        recent_drawings: List of FrenchLotoDrawing objects
        
    Returns:
        DataFrame: Performance data for each strategy
    """
    results = []
    
    for drawing in recent_drawings:
        for combo in all_combinations:
            num_matches, lucky_match, score = check_matches(combo, drawing)
            
            results.append({
                'drawing_date': drawing.date,
                'strategy': combo['strategy'],
                'numbers': combo['numbers'],
                'lucky_number': combo['lucky_number'],
                'num_matches': num_matches,
                'lucky_match': lucky_match,
                'score': score
            })
    
    # Convert to DataFrame for analysis
    df_results = pd.DataFrame(results)
    
    return df_results

def analyze_strategy_performance(df_results):
    """
    Analyze performance of each strategy.
    
    Args:
        df_results: DataFrame with test results
        
    Returns:
        DataFrame: Summary of strategy performance
    """
    # Group by strategy and calculate average performance
    strategy_performance = df_results.groupby('strategy').agg({
        'num_matches': ['mean', 'max'],
        'lucky_match': ['mean', 'max'],
        'score': ['mean', 'max']
    }).reset_index()
    
    # Flatten column names
    strategy_performance.columns = [
        'strategy', 
        'avg_num_matches', 'max_num_matches',
        'avg_lucky_match', 'max_lucky_match',
        'avg_score', 'max_score'
    ]
    
    # Sort by average score (higher is better)
    strategy_performance = strategy_performance.sort_values('avg_score', ascending=False)
    
    return strategy_performance

def generate_optimized_combinations(historical_data, top_strategies, num_combinations=10):
    """
    Generate combinations using the top performing strategies.
    
    Args:
        historical_data: List of FrenchLotoDrawing objects
        top_strategies: List of top performing strategy names
        num_combinations: Total number of combinations to generate
        
    Returns:
        list: List of dictionaries with generated combinations
    """
    optimized_combinations = []
    
    # Distribute combinations evenly among top strategies
    combinations_per_strategy = max(1, num_combinations // len(top_strategies))
    
    for strategy in top_strategies:
        if 'Frequency' in strategy:
            optimized_combinations.extend(
                generate_frequency_strategy(historical_data, combinations_per_strategy)
            )
        elif 'Hot/Cold' in strategy:
            # Extract hot ratio if available
            hot_ratio = 0.7  # Default
            if '(' in strategy:
                try:
                    hot_ratio = float(strategy.split('(')[1].split(')')[0])
                except:
                    pass
                
            optimized_combinations.extend(
                generate_hot_cold_strategy(historical_data, combinations_per_strategy, hot_ratio)
            )
        elif 'Overdue' in strategy:
            # Extract overdue ratio if available
            overdue_ratio = 0.6  # Default
            if '(' in strategy:
                try:
                    overdue_ratio = float(strategy.split('(')[1].split(')')[0])
                except:
                    pass
                
            optimized_combinations.extend(
                generate_overdue_strategy(historical_data, combinations_per_strategy, overdue_ratio)
            )
        elif 'Pattern' in strategy:
            optimized_combinations.extend(
                generate_pattern_strategy(historical_data, combinations_per_strategy)
            )
        elif 'Balanced' in strategy:
            # Extract risk level if available
            risk_level = 0.5  # Default
            if 'Risk:' in strategy:
                try:
                    risk_level = float(strategy.split('Risk:')[1].strip().split(')')[0])
                except:
                    pass
                
            optimized_combinations.extend(
                generate_balanced_strategy(historical_data, combinations_per_strategy, risk_level)
            )
    
    # If we need more combinations, add some balanced ones
    while len(optimized_combinations) < num_combinations:
        optimized_combinations.extend(
            generate_balanced_strategy(historical_data, 1, risk_level=0.5)
        )
    
    # Return exactly the requested number
    return optimized_combinations[:num_combinations]

def main():
    # Number of recent drawings to test against
    num_test_draws = 5
    
    print(f"Testing strategies against the {num_test_draws} most recent French Loto drawings...")
    
    # Get recent drawings for testing
    recent_drawings = get_recent_drawings(num_test_draws)
    
    if not recent_drawings:
        print("No recent drawings found in the database.")
        sys.exit(1)
    
    print(f"Found {len(recent_drawings)} recent drawings.")
    print("Most recent drawing date:", recent_drawings[0].date)
    
    # Get historical data for training, excluding the test drawings
    historical_data = get_historical_data(exclude_recent=num_test_draws)
    
    if not historical_data:
        print("No historical data found in the database.")
        sys.exit(1)
    
    print(f"Using {len(historical_data)} historical drawings for training.")
    
    # Generate combinations using all strategies
    all_combinations = generate_all_strategies(historical_data)
    print(f"Generated {len(all_combinations)} combinations across all strategies.")
    
    # Test strategies against actual drawings
    df_results = test_strategies_against_actual(all_combinations, recent_drawings)
    
    # Analyze strategy performance
    strategy_performance = analyze_strategy_performance(df_results)
    
    print("\nStrategy Performance:")
    print(strategy_performance.to_string(index=False))
    
    # Get top performing strategies
    top_strategies = strategy_performance.head(3)['strategy'].tolist()
    
    print("\nTop Performing Strategies:")
    for i, strategy in enumerate(top_strategies, 1):
        print(f"{i}. {strategy}")
    
    # Generate optimized combinations using top strategies
    print("\nGenerating 10 optimized combinations for tonight's draw...")
    optimized_combinations = generate_optimized_combinations(
        historical_data, top_strategies, num_combinations=10
    )
    
    print("\nOptimized Combinations for Tonight's French Loto Draw:")
    for i, combo in enumerate(optimized_combinations, 1):
        numbers_str = ", ".join(map(str, combo['numbers']))
        print(f"Combination {i} ({combo['strategy']}):")
        print(f"  Numbers: {numbers_str}")
        print(f"  Lucky Number: {combo['lucky_number']}")
        print()
    
    return optimized_combinations

if __name__ == "__main__":
    main()