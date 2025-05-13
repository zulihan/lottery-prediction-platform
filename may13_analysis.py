"""
Analysis of May 13, 2025 Euromillions Results
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Actual drawing results for May 13, 2025
ACTUAL_RESULTS = {
    "numbers": [9, 19, 44, 47, 50],
    "stars": [2, 9]
}

# Original 8 base combinations
BASE_COMBINATIONS = [
    {"name": "Base 1 (Risk: 0.40)", "numbers": [2, 10, 20, 27, 36], "stars": [6, 11]},
    {"name": "Base 2 (Risk: 0.46)", "numbers": [4, 10, 19, 20, 43], "stars": [1, 8]},
    {"name": "Base 3 (Risk: 0.53)", "numbers": [5, 16, 21, 28, 48], "stars": [2, 9]},
    {"name": "Base 4 (Risk: 0.59)", "numbers": [7, 11, 20, 21, 35], "stars": [4, 8]},
    {"name": "Base 5 (Risk: 0.65)", "numbers": [3, 13, 21, 23, 35], "stars": [5, 9]},
    {"name": "Base 6 (Risk: 0.71)", "numbers": [1, 5, 18, 19, 37], "stars": [5, 6]},
    {"name": "Base 7 (Risk: 0.78)", "numbers": [2, 9, 19, 34, 36], "stars": [4, 5]},
    {"name": "Base 8 (Risk: 0.84)", "numbers": [6, 17, 18, 28, 49], "stars": [2, 8]}
]

# Mixed combinations
MIXED_COMBINATIONS = [
    {"name": "Original Mixed", "numbers": [5, 10, 19, 21, 35], "stars": [5, 8]},
    {"name": "New Mixed 1", "numbers": [1, 2, 20, 28, 36], "stars": [2, 6]},
    {"name": "New Mixed 2", "numbers": [5, 10, 19, 21, 36], "stars": [5, 8]},
    {"name": "New Mixed 3", "numbers": [3, 4, 18, 21, 35], "stars": [6, 11]},
    {"name": "Bonus Combination", "numbers": [1, 2, 20, 27, 35], "stars": [4, 11]}
]

def analyze_match(combination, actual_results):
    """
    Analyze how many numbers and stars match between a combination and the actual results.
    
    Args:
        combination: Dictionary with numbers and stars
        actual_results: Dictionary with actual numbers and stars
        
    Returns:
        dict: Match analysis
    """
    matched_numbers = set(combination["numbers"]).intersection(set(actual_results["numbers"]))
    matched_stars = set(combination["stars"]).intersection(set(actual_results["stars"]))
    
    return {
        "matched_numbers": matched_numbers,
        "matched_stars": matched_stars,
        "num_numbers_matched": len(matched_numbers),
        "num_stars_matched": len(matched_stars),
        "total_match_score": len(matched_numbers) + len(matched_stars)
    }

def analyze_all_combinations():
    """Analyze all combinations against the actual results."""
    logger.info("ACTUAL DRAWING RESULTS FOR MAY 13, 2025:")
    logger.info(f"Main Numbers: {', '.join(map(str, ACTUAL_RESULTS['numbers']))}")
    logger.info(f"Stars: {', '.join(map(str, ACTUAL_RESULTS['stars']))}")
    logger.info("")
    
    logger.info("ANALYSIS OF BASE COMBINATIONS:")
    base_results = []
    for combo in BASE_COMBINATIONS:
        match = analyze_match(combo, ACTUAL_RESULTS)
        base_results.append((combo, match))
        
        logger.info(f"{combo['name']}:")
        logger.info(f"  Numbers: {', '.join(map(str, combo['numbers']))}")
        logger.info(f"  Stars: {', '.join(map(str, combo['stars']))}")
        logger.info(f"  Matched Numbers: {', '.join(map(str, match['matched_numbers'])) if match['matched_numbers'] else 'None'}")
        logger.info(f"  Matched Stars: {', '.join(map(str, match['matched_stars'])) if match['matched_stars'] else 'None'}")
        logger.info(f"  Total Match Score: {match['num_numbers_matched']}/5 numbers + {match['num_stars_matched']}/2 stars = {match['total_match_score']}/7")
        logger.info("")
    
    logger.info("ANALYSIS OF MIXED COMBINATIONS:")
    mixed_results = []
    for combo in MIXED_COMBINATIONS:
        match = analyze_match(combo, ACTUAL_RESULTS)
        mixed_results.append((combo, match))
        
        logger.info(f"{combo['name']}:")
        logger.info(f"  Numbers: {', '.join(map(str, combo['numbers']))}")
        logger.info(f"  Stars: {', '.join(map(str, combo['stars']))}")
        logger.info(f"  Matched Numbers: {', '.join(map(str, match['matched_numbers'])) if match['matched_numbers'] else 'None'}")
        logger.info(f"  Matched Stars: {', '.join(map(str, match['matched_stars'])) if match['matched_stars'] else 'None'}")
        logger.info(f"  Total Match Score: {match['num_numbers_matched']}/5 numbers + {match['num_stars_matched']}/2 stars = {match['total_match_score']}/7")
        logger.info("")
    
    # Find best performing combinations
    all_results = base_results + mixed_results
    all_results.sort(key=lambda x: (x[1]['total_match_score'], x[1]['num_numbers_matched']), reverse=True)
    
    top_combo, top_match = all_results[0]
    
    logger.info("SUMMARY OF RESULTS:")
    logger.info(f"Best Performing Combination: {top_combo['name']}")
    logger.info(f"  Numbers: {', '.join(map(str, top_combo['numbers']))}")
    logger.info(f"  Stars: {', '.join(map(str, top_combo['stars']))}")
    logger.info(f"  Matched Numbers: {', '.join(map(str, top_match['matched_numbers'])) if top_match['matched_numbers'] else 'None'}")
    logger.info(f"  Matched Stars: {', '.join(map(str, top_match['matched_stars'])) if top_match['matched_stars'] else 'None'}")
    logger.info(f"  Total Match Score: {top_match['num_numbers_matched']}/5 numbers + {top_match['num_stars_matched']}/2 stars = {top_match['total_match_score']}/7")
    
    # Calculate overall performance
    base_avg = sum(r[1]['total_match_score'] for r in base_results) / len(base_results)
    mixed_avg = sum(r[1]['total_match_score'] for r in mixed_results) / len(mixed_results)
    
    logger.info(f"Average match score for base combinations: {base_avg:.2f}/7")
    logger.info(f"Average match score for mixed combinations: {mixed_avg:.2f}/7")
    
    # Count combinations with at least one match
    base_with_matches = sum(1 for _, r in base_results if r['total_match_score'] > 0)
    mixed_with_matches = sum(1 for _, r in mixed_results if r['total_match_score'] > 0)
    
    logger.info(f"Base combinations with at least one match: {base_with_matches}/{len(base_results)} ({base_with_matches/len(base_results)*100:.1f}%)")
    logger.info(f"Mixed combinations with at least one match: {mixed_with_matches}/{len(mixed_results)} ({mixed_with_matches/len(mixed_results)*100:.1f}%)")
    
    # Find specific numbers that worked well in our predictions
    predicted_numbers = set()
    for combo, _ in all_results:
        predicted_numbers.update(combo["numbers"])
    
    successful_numbers = predicted_numbers.intersection(set(ACTUAL_RESULTS["numbers"]))
    successful_stars = set()
    for combo, _ in all_results:
        combo_stars_set = set(combo["stars"])
        successful_stars.update(combo_stars_set.intersection(set(ACTUAL_RESULTS["stars"])))
    
    logger.info(f"Successfully predicted main numbers: {', '.join(map(str, sorted(successful_numbers)))}")
    logger.info(f"Successfully predicted stars: {', '.join(map(str, sorted(successful_stars)))}")
    
    # Identify which combinations had the lucky number 19
    combos_with_19 = []
    for combo, _ in all_results:
        if 19 in combo["numbers"]:
            combos_with_19.append(combo["name"])
    
    if combos_with_19:
        logger.info(f"Combinations that included the correct number 19: {', '.join(combos_with_19)}")
    
    # Combinations with star 2 or 9
    combos_with_star_2 = []
    combos_with_star_9 = []
    for combo, _ in all_results:
        if 2 in combo["stars"]:
            combos_with_star_2.append(combo["name"])
        if 9 in combo["stars"]:
            combos_with_star_9.append(combo["name"])
    
    if combos_with_star_2:
        logger.info(f"Combinations that included the correct star 2: {', '.join(combos_with_star_2)}")
    if combos_with_star_9:
        logger.info(f"Combinations that included the correct star 9: {', '.join(combos_with_star_9)}")

if __name__ == "__main__":
    analyze_all_combinations()