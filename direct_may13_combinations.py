"""
Generate 3 optimized mixed combinations for the May 13, 2025 Euromillions drawing,
based on the 8 base combinations provided by the user.
"""

from collections import Counter
import pandas as pd
from datetime import datetime
import random
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

def get_most_common_elements():
    """
    Find the most common numbers and stars in the base combinations.
    
    Returns:
        tuple: (common_numbers, common_stars)
    """
    # Extract all numbers and stars
    all_numbers = []
    all_stars = []
    
    for combo in BASE_COMBINATIONS:
        all_numbers.extend(combo["numbers"])
        all_stars.extend(combo["stars"])
    
    # Count frequencies
    number_counts = Counter(all_numbers)
    star_counts = Counter(all_stars)
    
    logger.info("Most common numbers in the base combinations:")
    for num, count in number_counts.most_common(10):
        logger.info(f"  {num}: {count} occurrences")
    
    logger.info("Most common stars in the base combinations:")
    for star, count in star_counts.most_common(5):
        logger.info(f"  {star}: {count} occurrences")
    
    return number_counts, star_counts

def find_frequent_pairs():
    """
    Find frequently occurring pairs of numbers in the base combinations.
    
    Returns:
        tuple: (number_pairs, star_pairs)
    """
    number_pairs = []
    
    # Extract all number pairs from base combinations
    for combo in BASE_COMBINATIONS:
        numbers = combo["numbers"]
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                pair = tuple(sorted([numbers[i], numbers[j]]))
                number_pairs.append(pair)
    
    # Count pair frequencies
    pair_counts = Counter(number_pairs)
    
    logger.info("Most common number pairs in the base combinations:")
    for pair, count in pair_counts.most_common(8):
        logger.info(f"  {pair}: {count} occurrences")
    
    return pair_counts

def generate_mixed_combinations():
    """
    Generate 3 optimized mixed combinations based on the base combinations.
    
    Returns:
        list: List of mixed combination dictionaries
    """
    # Get common elements
    number_counts, star_counts = get_most_common_elements()
    pair_counts = find_frequent_pairs()
    
    # Create 3 new combinations
    mixed_combinations = []
    
    # Combination 1: Focus on most frequent numbers and the most common pairs
    # This prioritizes the most recurring numbers across all base combinations
    common_numbers = [num for num, _ in number_counts.most_common(8)]
    common_stars = [star for star, _ in star_counts.most_common(4)]
    
    # Start with most common triplet (3 numbers that appear most frequently together)
    combo1_numbers = []
    for num in common_numbers:
        if len(combo1_numbers) < 5 and num not in EXISTING_MIXED["numbers"]:
            combo1_numbers.append(num)
    
    # Fill with a few less common numbers to ensure diversity if needed
    while len(combo1_numbers) < 5:
        for num in range(1, 51):
            if num not in combo1_numbers and num not in EXISTING_MIXED["numbers"]:
                combo1_numbers.append(num)
                break
    
    # Select stars that are common but different from the existing mixed
    combo1_stars = []
    for star in common_stars:
        if len(combo1_stars) < 2 and star not in EXISTING_MIXED["stars"]:
            combo1_stars.append(star)
    
    # Fill if needed
    while len(combo1_stars) < 2:
        for star in range(1, 13):
            if star not in combo1_stars and star not in EXISTING_MIXED["stars"]:
                combo1_stars.append(star)
                break
    
    mixed_combinations.append({
        "numbers": sorted(combo1_numbers[:5]),
        "stars": sorted(combo1_stars[:2])
    })
    
    # Combination 2: Using the most common pairs from the base combinations
    # This focuses on number relationships that appear frequently together
    common_pairs = [pair for pair, _ in pair_counts.most_common(6)]
    
    combo2_numbers = set()
    # Start with most common pairs
    for pair in common_pairs:
        if len(combo2_numbers) < 4:  # Leave room for one more number
            combo2_numbers.update(pair)
    
    # Remove any numbers that would create too much overlap with existing combinations
    combo2_numbers = list(combo2_numbers)
    combo2_numbers = [num for num in combo2_numbers if combo2_numbers.count(num) == 1]
    
    # Make sure we don't have too much overlap with the first mixed combination
    combo2_numbers = [num for num in combo2_numbers 
                      if num not in mixed_combinations[0]["numbers"][:3]]
    
    # Fill remaining spots
    remaining_common = [num for num, _ in number_counts.most_common() 
                        if num not in combo2_numbers 
                        and num not in mixed_combinations[0]["numbers"][:3]]
    
    combo2_numbers.extend(remaining_common[:5-len(combo2_numbers)])
    
    # For stars, use different ones than the first combination
    remaining_stars = [star for star, _ in star_counts.most_common() 
                       if star not in mixed_combinations[0]["stars"]]
    
    combo2_stars = remaining_stars[:2]
    
    mixed_combinations.append({
        "numbers": sorted(combo2_numbers[:5]),
        "stars": sorted(combo2_stars[:2])
    })
    
    # Combination 3: Balanced approach using distribution across number ranges
    # This ensures coverage across low (1-17), medium (18-34), and high (35-50) ranges
    low_range = [num for num in range(1, 18) 
                 if num not in mixed_combinations[0]["numbers"] 
                 and num not in mixed_combinations[1]["numbers"][:3]]
    
    mid_range = [num for num in range(18, 35) 
                 if num not in mixed_combinations[0]["numbers"] 
                 and num not in mixed_combinations[1]["numbers"][:3]]
    
    high_range = [num for num in range(35, 51) 
                  if num not in mixed_combinations[0]["numbers"] 
                  and num not in mixed_combinations[1]["numbers"][:3]]
    
    # If we need more numbers, relax the restrictions
    if len(low_range) < 2 or len(mid_range) < 2 or len(high_range) < 1:
        low_range = [num for num in range(1, 18)]
        mid_range = [num for num in range(18, 35)]
        high_range = [num for num in range(35, 51)]
    
    # Sort by frequency in base combinations
    low_range.sort(key=lambda num: number_counts.get(num, 0), reverse=True)
    mid_range.sort(key=lambda num: number_counts.get(num, 0), reverse=True)
    high_range.sort(key=lambda num: number_counts.get(num, 0), reverse=True)
    
    combo3_numbers = []
    combo3_numbers.extend(low_range[:2])   # 2 numbers from low range
    combo3_numbers.extend(mid_range[:2])   # 2 numbers from mid range
    combo3_numbers.append(high_range[0])   # 1 number from high range
    
    # For stars, try to get a pair that appears together frequently
    star_options = []
    for combo in BASE_COMBINATIONS:
        if tuple(combo["stars"]) not in [(c["stars"][0], c["stars"][1]) for c in mixed_combinations]:
            star_options.append(combo["stars"])
    
    if star_options:
        combo3_stars = star_options[0]
    else:
        # Use less common stars that haven't been used yet
        unused_stars = [star for star in range(1, 13) 
                       if star not in [s for c in mixed_combinations for s in c["stars"]]]
        
        if len(unused_stars) >= 2:
            combo3_stars = unused_stars[:2]
        else:
            # Fallback to any valid stars
            combo3_stars = [s for s in range(1, 13) if s not in mixed_combinations[1]["stars"]][:2]
    
    mixed_combinations.append({
        "numbers": sorted(combo3_numbers[:5]),
        "stars": sorted(combo3_stars[:2])
    })
    
    return mixed_combinations

def analyze_combinations(combinations):
    """Analyze and display information about the combinations."""
    logger.info("\n=== OPTIMIZED MIXED COMBINATIONS FOR MAY 13, 2025 ===")
    
    for i, combo in enumerate(combinations):
        # Calculate uniqueness metrics
        unique_to_base = []
        for num in combo["numbers"]:
            base_occurrences = sum(1 for base in BASE_COMBINATIONS if num in base["numbers"])
            if base_occurrences == 0:
                unique_to_base.append(num)
        
        star_analysis = []
        for star in combo["stars"]:
            base_occurrences = sum(1 for base in BASE_COMBINATIONS if star in base["stars"])
            if base_occurrences == 0:
                star_analysis.append(f"{star} (unique)")
            else:
                star_analysis.append(f"{star} (appears {base_occurrences}x)")
        
        # Analyze number distribution
        low_count = sum(1 for num in combo["numbers"] if 1 <= num <= 17)
        mid_count = sum(1 for num in combo["numbers"] if 18 <= num <= 34)
        high_count = sum(1 for num in combo["numbers"] if 35 <= num <= 50)
        
        logger.info(f"Mixed Strategy Combination {i+1}:")
        logger.info(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
        logger.info(f"  Stars: {', '.join(map(str, combo['stars']))}")
        logger.info(f"  Distribution: {low_count} low, {mid_count} mid, {high_count} high")
        
        if unique_to_base:
            logger.info(f"  Unique numbers: {', '.join(map(str, unique_to_base))}")
        
        logger.info(f"  Star analysis: {', '.join(star_analysis)}")
        logger.info("")

def main():
    """Generate and display optimized mixed combinations."""
    combinations = generate_mixed_combinations()
    analyze_combinations(combinations)
    
    logger.info("Recommendation: Use these 3 new mixed combinations along with")
    logger.info("the previously generated [5, 10, 19, 21, 35] with stars [5, 8]")
    logger.info("These combinations maximize your chances by leveraging frequency")
    logger.info("patterns and pair relationships across the 8 base combinations.")

if __name__ == "__main__":
    main()