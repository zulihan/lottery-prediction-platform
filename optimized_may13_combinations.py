"""
Generate optimized mixed combinations based on a set of balanced base combinations
for the May 13, 2025 Euromillions drawing.
"""

import numpy as np
import pandas as pd
from collections import Counter
from database import get_db_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base combinations provided by the user
BASE_COMBINATIONS = [
    {"numbers": [2, 10, 20, 27, 36], "stars": [6, 11]},
    {"numbers": [4, 10, 19, 20, 43], "stars": [1, 8]},
    {"numbers": [5, 16, 21, 28, 48], "stars": [2, 9]},
    {"numbers": [7, 11, 20, 21, 35], "stars": [4, 8]},
    {"numbers": [3, 13, 21, 23, 35], "stars": [5, 9]},
    {"numbers": [1, 5, 18, 19, 37], "stars": [5, 6]},
    {"numbers": [2, 9, 19, 34, 36], "stars": [4, 5]},
    {"numbers": [6, 17, 18, 28, 49], "stars": [2, 8]}
]

# Already provided mixed combination
EXISTING_MIXED = {"numbers": [5, 10, 19, 21, 35], "stars": [5, 8]}

def load_euromillions_data():
    """Load Euromillions data from the database."""
    try:
        conn = get_db_connection()
        if conn:
            query = "SELECT * FROM euromillions_drawings ORDER BY date DESC"
            data = pd.read_sql(query, conn)
            logger.info(f"Loaded {len(data)} Euromillions drawings")
            return data
        else:
            logger.error("Could not connect to database.")
            return None
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return None

def find_frequent_pairs(data):
    """
    Find the most frequently occurring pairs of numbers and stars in historical data.
    
    Args:
        data: DataFrame with Euromillions historical data
        
    Returns:
        dict: Dictionary with frequent number pairs and star pairs
    """
    # Initialize containers for pairs
    number_pairs = []
    star_pairs = []
    
    # Extract pairs from each drawing
    for _, row in data.iterrows():
        numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
        stars = [row['s1'], row['s2']]
        
        # Get all number pairs from this drawing
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                pair = tuple(sorted([numbers[i], numbers[j]]))
                number_pairs.append(pair)
        
        # Add the star pair
        star_pairs.append(tuple(sorted(stars)))
    
    # Count frequencies
    number_pair_counts = Counter(number_pairs)
    star_pair_counts = Counter(star_pairs)
    
    # Get the most common pairs
    most_common_number_pairs = number_pair_counts.most_common(20)
    most_common_star_pairs = star_pair_counts.most_common(10)
    
    logger.info("Most common number pairs:")
    for pair, count in most_common_number_pairs[:10]:
        logger.info(f"  {pair}: {count} occurrences")
    
    logger.info("Most common star pairs:")
    for pair, count in most_common_star_pairs[:5]:
        logger.info(f"  {pair}: {count} occurrences")
    
    return {
        'number_pairs': most_common_number_pairs,
        'star_pairs': most_common_star_pairs
    }

def count_number_frequencies(combinations):
    """
    Count the frequency of each number and star across the base combinations.
    
    Args:
        combinations: List of combination dictionaries
        
    Returns:
        tuple: (number_counts, star_counts)
    """
    all_numbers = []
    all_stars = []
    
    for combo in combinations:
        all_numbers.extend(combo["numbers"])
        all_stars.extend(combo["stars"])
    
    number_counts = Counter(all_numbers)
    star_counts = Counter(all_stars)
    
    return number_counts, star_counts

def create_mixed_combination(base_combinations, frequent_pairs, number_counts, star_counts):
    """
    Create a mixed combination based on:
    1. Frequency in base combinations
    2. Frequent pairs in historical data
    3. Balanced distribution across number ranges
    
    Args:
        base_combinations: List of base combinations
        frequent_pairs: Dictionary with frequent number and star pairs
        number_counts: Counter of number frequencies in base combinations
        star_counts: Counter of star frequencies in base combinations
        
    Returns:
        dict: New mixed combination
    """
    logger.info("Creating a new mixed combination...")
    # Get most common numbers and stars from base combinations
    most_common_numbers = [num for num, _ in number_counts.most_common(15)]
    most_common_stars = [star for star, _ in star_counts.most_common(8)]
    
    # Extract frequently occurring pairs from historical data
    frequent_number_pairs = [pair for pair, _ in frequent_pairs['number_pairs']]
    frequent_star_pairs = [pair for pair, _ in frequent_pairs['star_pairs']]
    
    # Start with high-frequency pairs from both base combinations and historical data
    candidate_pairs = []
    for pair in frequent_number_pairs[:10]:
        if pair[0] in most_common_numbers and pair[1] in most_common_numbers:
            candidate_pairs.append(pair)
    
    # Select 2-3 pairs to form the backbone of our combination
    selected_pairs = []
    if len(candidate_pairs) >= 2:
        selected_pairs = candidate_pairs[:2]
    
    # Build a set of unique numbers from these pairs
    selected_numbers = set()
    for pair in selected_pairs:
        selected_numbers.update(pair)
    
    # Fill in additional numbers from high-frequency numbers
    while len(selected_numbers) < 5:
        for num in most_common_numbers:
            if num not in selected_numbers:
                # Check if this creates a balanced distribution
                if is_balanced_with_addition(list(selected_numbers), num):
                    selected_numbers.add(num)
                    break
        
        # Fallback if we can't find a "balanced" addition
        if len(selected_numbers) < 5:
            for num in most_common_numbers:
                if num not in selected_numbers:
                    selected_numbers.add(num)
                    break
    
    # For stars, start with a frequent historical pair if possible
    selected_stars = set()
    for pair in frequent_star_pairs:
        if pair[0] in most_common_stars and pair[1] in most_common_stars:
            selected_stars.update(pair)
            break
    
    # If we don't have 2 stars yet, add from most common
    while len(selected_stars) < 2:
        for star in most_common_stars:
            if star not in selected_stars:
                selected_stars.add(star)
                break
    
    return {
        "numbers": sorted(list(selected_numbers)),
        "stars": sorted(list(selected_stars))
    }

def is_balanced_with_addition(current_numbers, new_number):
    """
    Check if adding a new number would maintain a balanced distribution.
    We want a roughly even distribution across low (1-17), medium (18-34), and high (35-50) ranges.
    
    Args:
        current_numbers: Current list of numbers
        new_number: Number to be added
        
    Returns:
        bool: True if addition would maintain balance
    """
    # Count numbers in each range
    low_count = sum(1 for num in current_numbers if 1 <= num <= 17)
    mid_count = sum(1 for num in current_numbers if 18 <= num <= 34)
    high_count = sum(1 for num in current_numbers if 35 <= num <= 50)
    
    # Check which range the new number belongs to
    if 1 <= new_number <= 17:
        low_count += 1
    elif 18 <= new_number <= 34:
        mid_count += 1
    else:
        high_count += 1
    
    # Check if this creates a balanced distribution (no more than 2 in any range)
    return low_count <= 2 and mid_count <= 2 and high_count <= 2

def combination_similarity(combo1, combo2):
    """
    Calculate how similar two combinations are.
    
    Args:
        combo1, combo2: Combinations to compare
        
    Returns:
        float: Similarity score (0-1)
    """
    number_overlap = len(set(combo1["numbers"]).intersection(set(combo2["numbers"])))
    star_overlap = len(set(combo1["stars"]).intersection(set(combo2["stars"])))
    
    # Calculate similarity as weighted average of overlaps
    number_similarity = number_overlap / 5.0
    star_similarity = star_overlap / 2.0
    
    # Weight numbers more than stars
    similarity = 0.7 * number_similarity + 0.3 * star_similarity
    
    return similarity

def ensure_diversity(new_combo, existing_combos, threshold=0.5):
    """
    Check if a new combination is sufficiently different from existing ones.
    
    Args:
        new_combo: New combination to check
        existing_combos: List of existing combinations
        threshold: Maximum similarity threshold
        
    Returns:
        bool: True if the combination is diverse enough
    """
    for combo in existing_combos:
        similarity = combination_similarity(new_combo, combo)
        if similarity > threshold:
            return False
    return True

def generate_mixed_combinations(base_combinations=BASE_COMBINATIONS, 
                               existing_mixed=EXISTING_MIXED, 
                               num_combos=3):
    """
    Generate optimized mixed combinations from base combinations.
    
    Args:
        base_combinations: List of base combinations
        existing_mixed: Already generated mixed combination
        num_combos: Number of new combinations to generate
        
    Returns:
        list: List of new mixed combinations
    """
    # Load historical data
    data = load_euromillions_data()
    if data is None:
        logger.error("Cannot generate combinations without historical data")
        return []
    
    # Find frequent pairs in historical data
    frequent_pairs = find_frequent_pairs(data)
    
    # Count frequencies in base combinations
    number_counts, star_counts = count_number_frequencies(base_combinations)
    
    logger.info("Most frequent numbers in base combinations:")
    for num, count in number_counts.most_common(10):
        logger.info(f"  {num}: {count} occurrences")
    
    logger.info("Most frequent stars in base combinations:")
    for star, count in star_counts.most_common(5):
        logger.info(f"  {star}: {count} occurrences")
    
    # Create mixed combinations
    new_combinations = []
    existing_to_check = base_combinations + [existing_mixed]
    
    for _ in range(num_combos * 2):  # Generate more than needed to ensure diversity
        if len(new_combinations) >= num_combos:
            break
            
        new_combo = create_mixed_combination(
            base_combinations, frequent_pairs, number_counts, star_counts
        )
        
        # Only add if sufficiently different from existing combinations
        if ensure_diversity(new_combo, existing_to_check + new_combinations):
            new_combinations.append(new_combo)
            logger.info(f"Generated diverse combination: {new_combo}")
    
    return new_combinations[:num_combos]

def main():
    """Generate 3 new optimized mixed combinations for May 13, 2025."""
    logger.info("Generating optimized mixed combinations for May 13, 2025")
    
    # Generate 3 new combinations
    mixed_combinations = generate_mixed_combinations(
        base_combinations=BASE_COMBINATIONS,
        existing_mixed=EXISTING_MIXED,
        num_combos=3
    )
    
    # Display the new combinations
    logger.info("\n=== OPTIMIZED MIXED COMBINATIONS FOR MAY 13, 2025 ===")
    
    for i, combo in enumerate(mixed_combinations):
        logger.info(f"Mixed Strategy Combination {i+1}:")
        logger.info(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
        logger.info(f"  Stars: {', '.join(map(str, combo['stars']))}")
        logger.info("")
    
    return mixed_combinations

if __name__ == "__main__":
    main()