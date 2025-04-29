import pandas as pd
import json
from collections import Counter
import database

def analyze_full_combinations():
    """
    Analyze the full combinations (all 5 numbers + 2 stars) in the Euromillions history.
    Check if any complete combinations have ever repeated.
    
    Returns:
        dict: Analysis results including any repeated combinations and statistics
    """
    # Get all drawings from database
    data = database.get_all_drawings()
    if not isinstance(data, pd.DataFrame) or data.empty:
        return {"error": "No data available for analysis"}
    
    # Create combination strings for full combinations (5 numbers + 2 stars)
    full_combinations = []
    for _, row in data.iterrows():
        numbers = sorted([row['n1'], row['n2'], row['n3'], row['n4'], row['n5']])
        stars = sorted([row['s1'], row['s2']])
        combo_str = f"Numbers: {numbers}, Stars: {stars}"
        full_combinations.append({
            'date': row['date'],
            'combination': combo_str,
            'numbers': numbers,
            'stars': stars
        })
    
    # Check for repeated full combinations
    combo_counter = Counter([c['combination'] for c in full_combinations])
    repeated_combos = {combo: count for combo, count in combo_counter.items() if count > 1}
    
    # Find occurrences of repeated combinations with dates
    repeated_details = {}
    if repeated_combos:
        for combo_str, count in repeated_combos.items():
            repeated_details[combo_str] = [
                c['date'] for c in full_combinations if c['combination'] == combo_str
            ]
    
    return {
        'total_draws': len(full_combinations),
        'unique_combinations': len(combo_counter),
        'repeated_combinations': repeated_combos,
        'repeated_details': repeated_details
    }

def analyze_number_combinations(size=3):
    """
    Analyze partial combinations (subsets of the main 5 numbers) to find the most frequent ones.
    
    Args:
        size (int): Size of number subsets to analyze (default: 3, for triplets)
    
    Returns:
        dict: Analysis results including the most frequent number combinations
    """
    # Get all drawings from database
    data = database.get_all_drawings()
    if not isinstance(data, pd.DataFrame) or data.empty:
        return {"error": "No data available for analysis"}
    
    # Generate all subsets of the specified size
    number_combinations = []
    for _, row in data.iterrows():
        numbers = sorted([row['n1'], row['n2'], row['n3'], row['n4'], row['n5']])
        # Generate all possible combinations of size 'size'
        from itertools import combinations as itercombo
        for combo in itercombo(numbers, size):
            number_combinations.append(tuple(sorted(combo)))
    
    # Count occurrences of each combination
    combo_counter = Counter(number_combinations)
    
    # Get top combinations
    top_combos = combo_counter.most_common(20)  # Get top 20
    
    return {
        'size': size,
        'total_draws': len(data),
        'most_frequent_combinations': top_combos
    }

def analyze_star_combinations():
    """
    Analyze star combinations to find the most frequent pairs.
    
    Returns:
        dict: Analysis results including the most frequent star combinations
    """
    # Get all drawings from database
    data = database.get_all_drawings()
    if not isinstance(data, pd.DataFrame) or data.empty:
        return {"error": "No data available for analysis"}
    
    # Extract star combinations
    star_combinations = []
    for _, row in data.iterrows():
        stars = tuple(sorted([row['s1'], row['s2']]))
        star_combinations.append(stars)
    
    # Count occurrences of each combination
    combo_counter = Counter(star_combinations)
    
    # Get top combinations
    top_combos = combo_counter.most_common(12)  # Get all possible combinations (12 choose 2 = 66)
    
    return {
        'total_draws': len(data),
        'most_frequent_star_combinations': top_combos
    }

if __name__ == "__main__":
    # Test the functions
    full_result = analyze_full_combinations()
    print("Full combination analysis:")
    print(json.dumps(full_result, indent=2, default=str))
    
    triplets = analyze_number_combinations(size=3)
    print("\nTriplet analysis:")
    print(json.dumps(triplets, indent=2))
    
    star_result = analyze_star_combinations()
    print("\nStar combination analysis:")
    print(json.dumps(star_result, indent=2))