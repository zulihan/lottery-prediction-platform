"""
Generate a bonus optimized combination that's different from previous ones
for the May 13, 2025 Euromillions drawing.
"""

import logging
import random
from collections import Counter

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

# Previously generated mixed combinations
PREVIOUS_MIXED = [
    {"numbers": [5, 10, 19, 21, 35], "stars": [5, 8]},
    {"numbers": [1, 2, 20, 28, 36], "stars": [2, 6]},
    {"numbers": [5, 10, 19, 21, 36], "stars": [5, 8]},
    {"numbers": [3, 4, 18, 21, 35], "stars": [6, 11]}
]

def extract_triplets_from_base():
    """Extract all triplets (3 numbers) from base combinations"""
    triplets = []
    
    for combo in BASE_COMBINATIONS:
        numbers = combo["numbers"]
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                for k in range(j+1, len(numbers)):
                    triplet = tuple(sorted([numbers[i], numbers[j], numbers[k]]))
                    triplets.append(triplet)
    
    # Count the frequency of each triplet
    triplet_counts = Counter(triplets)
    
    logger.info("Most common triplets in base combinations:")
    for triplet, count in triplet_counts.most_common(5):
        logger.info(f"  {triplet}: {count} occurrences")
    
    return triplet_counts

def generate_bonus_combination():
    """Generate a unique bonus combination"""
    # Extract triplets
    triplet_counts = extract_triplets_from_base()
    
    # Analyze digits in existing mixes
    used_numbers = []
    for combo in PREVIOUS_MIXED:
        used_numbers.extend(combo["numbers"])
    
    used_number_counts = Counter(used_numbers)
    
    # Find underrepresented numbers (those used less than twice)
    underrepresented = [num for num in range(1, 51) 
                        if used_number_counts.get(num, 0) < 2]
    
    # Get hotspot number regions from base combinations
    all_base_numbers = []
    for combo in BASE_COMBINATIONS:
        all_base_numbers.extend(combo["numbers"])
    
    base_counts = Counter(all_base_numbers)
    hot_regions = []
    
    for i in range(1, 46, 5):  # Check regions of 5 numbers
        region = list(range(i, i+5))
        region_count = sum(base_counts.get(num, 0) for num in region)
        hot_regions.append((region, region_count))
    
    hot_regions.sort(key=lambda x: x[1], reverse=True)
    
    logger.info("Hot number regions:")
    for region, count in hot_regions[:3]:
        logger.info(f"  {region}: {count} total occurrences")
    
    # Start with a promising triplet that's not overused in existing mixes
    best_triplet = None
    min_overlap = 5  # Start with maximum possible overlap
    
    for triplet, _ in triplet_counts.most_common(10):
        # Calculate overlap with existing mixed combinations
        overlap = sum(1 for num in triplet if used_number_counts.get(num, 0) >= 2)
        
        if overlap < min_overlap:
            min_overlap = overlap
            best_triplet = triplet
    
    # If no good triplet found, start with less common but underrepresented numbers
    if not best_triplet or min_overlap > 1:
        # Use numbers from hot regions that are underrepresented
        hot_numbers = []
        for region, _ in hot_regions[:3]:
            for num in region:
                if num in underrepresented:
                    hot_numbers.append(num)
        
        # If we have enough underrepresented hot numbers, use them
        if len(hot_numbers) >= 3:
            best_triplet = tuple(sorted(random.sample(hot_numbers, 3)))
        else:
            # Fallback to any underrepresented numbers
            if len(underrepresented) >= 3:
                best_triplet = tuple(sorted(random.sample(underrepresented, 3)))
            else:
                # Last resort - use any numbers not in the latest mix
                available = [num for num in range(1, 51) 
                             if num not in PREVIOUS_MIXED[-1]["numbers"]]
                best_triplet = tuple(sorted(random.sample(available, 3)))
    
    logger.info(f"Starting with triplet: {best_triplet}")
    
    # Build the rest of the combination
    new_numbers = list(best_triplet)
    
    # Add two more numbers using a balanced approach
    available_numbers = [num for num in range(1, 51) if num not in new_numbers]
    
    # Check current distribution
    low_count = sum(1 for num in new_numbers if 1 <= num <= 17)
    mid_count = sum(1 for num in new_numbers if 18 <= num <= 34)
    high_count = sum(1 for num in new_numbers if 35 <= num <= 50)
    
    # Number 4 - focus on a number from an underrepresented range
    target_range = []
    if low_count < 2:
        target_range = [num for num in available_numbers if 1 <= num <= 17]
    elif mid_count < 2:
        target_range = [num for num in available_numbers if 18 <= num <= 34]
    elif high_count < 1:
        target_range = [num for num in available_numbers if 35 <= num <= 50]
    else:
        target_range = available_numbers
    
    # Filter for underrepresented numbers in that range
    target_range = [num for num in target_range if num in underrepresented]
    
    # If no good targets, fall back to any number in the range
    if not target_range:
        if low_count < 2:
            target_range = [num for num in available_numbers if 1 <= num <= 17]
        elif mid_count < 2:
            target_range = [num for num in available_numbers if 18 <= num <= 34]
        elif high_count < 1:
            target_range = [num for num in available_numbers if 35 <= num <= 50]
        else:
            target_range = available_numbers
    
    if target_range:
        # Sort by frequency in base combinations
        target_range.sort(key=lambda num: base_counts.get(num, 0), reverse=True)
        new_numbers.append(target_range[0])
    else:
        # Unlikely fallback
        new_numbers.append(random.choice(available_numbers))
    
    # Update available numbers
    available_numbers = [num for num in available_numbers if num not in new_numbers]
    
    # Number 5 - ensure a balanced distribution
    low_count = sum(1 for num in new_numbers if 1 <= num <= 17)
    mid_count = sum(1 for num in new_numbers if 18 <= num <= 34)
    high_count = sum(1 for num in new_numbers if 35 <= num <= 50)
    
    if low_count < 2:
        target_range = [num for num in available_numbers if 1 <= num <= 17]
    elif mid_count < 2:
        target_range = [num for num in available_numbers if 18 <= num <= 34]
    elif high_count < 1:
        target_range = [num for num in available_numbers if 35 <= num <= 50]
    else:
        # If distribution is already good, favor hot numbers
        target_range = [num for num in available_numbers 
                        if base_counts.get(num, 0) >= 2]
        if not target_range:
            target_range = available_numbers
    
    if target_range:
        # Sort by frequency in base combinations
        target_range.sort(key=lambda num: base_counts.get(num, 0), reverse=True)
        new_numbers.append(target_range[0])
    else:
        # Unlikely fallback
        new_numbers.append(random.choice(available_numbers))
    
    # Now for the stars
    # Analyze stars in existing mixes
    used_stars = []
    for combo in PREVIOUS_MIXED:
        used_stars.extend(combo["stars"])
    
    used_star_counts = Counter(used_stars)
    
    # Find stars that work well with these numbers
    star_compatibility = Counter()
    
    for combo in BASE_COMBINATIONS:
        # Check how many numbers from our combination appear in this base combo
        overlap = len(set(combo["numbers"]).intersection(set(new_numbers)))
        if overlap >= 2:  # If there's good overlap, its stars may work well
            for star in combo["stars"]:
                star_compatibility[star] += overlap
    
    # Sort stars by compatibility and counter usage in existing mixes
    star_candidates = list(range(1, 13))
    star_candidates.sort(key=lambda s: (star_compatibility.get(s, 0), -used_star_counts.get(s, 0)), 
                        reverse=True)
    
    # Take the top two most compatible stars
    new_stars = star_candidates[:2]
    
    # If stars match exactly a previous combination, choose a different pair
    for combo in PREVIOUS_MIXED:
        if set(new_stars) == set(combo["stars"]):
            # Get next best options
            new_stars = [star_candidates[0], star_candidates[2]]
            break
    
    return {
        "numbers": sorted(new_numbers),
        "stars": sorted(new_stars)
    }

def main():
    """Generate and display a bonus combination"""
    logger.info("Generating bonus combination for May 13, 2025...")
    
    combo = generate_bonus_combination()
    
    # Analyze distribution
    low_count = sum(1 for num in combo["numbers"] if 1 <= num <= 17)
    mid_count = sum(1 for num in combo["numbers"] if 18 <= num <= 34)
    high_count = sum(1 for num in combo["numbers"] if 35 <= num <= 50)
    
    logger.info("\n=== BONUS OPTIMIZED COMBINATION FOR MAY 13, 2025 ===")
    logger.info(f"Main Numbers: {', '.join(map(str, combo['numbers']))}")
    logger.info(f"Stars: {', '.join(map(str, combo['stars']))}")
    logger.info(f"Distribution: {low_count} low, {mid_count} mid, {high_count} high")
    
    # Check uniqueness vs previous combinations
    for i, prev in enumerate(PREVIOUS_MIXED):
        overlap_nums = len(set(combo["numbers"]).intersection(set(prev["numbers"])))
        overlap_stars = len(set(combo["stars"]).intersection(set(prev["stars"])))
        
        logger.info(f"Overlap with Mix {i+1}: {overlap_nums}/5 numbers, {overlap_stars}/2 stars")
    
    logger.info("\nRecommendation: Add this bonus combination to your May 13 selections")
    logger.info("This gives excellent coverage of underrepresented numbers while")
    logger.info("maintaining a strong probabilistic foundation.")

if __name__ == "__main__":
    main()