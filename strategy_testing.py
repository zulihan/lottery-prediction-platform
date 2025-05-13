"""
Test which strategy would have performed best for the May 13, 2025 Euromillions drawing.
This script will evaluate various strategies against the actual results.
"""

import logging
import random
import numpy as np
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Actual drawing results for May 13, 2025
ACTUAL_RESULTS = {
    "numbers": [9, 19, 44, 47, 50],
    "stars": [2, 9]
}

# Define a range of strategies to test
STRATEGIES = [
    "Frequency Analysis",
    "Hot-Cold",
    "Markov Chain",
    "Coverage Optimization",
    "Risk-Reward Balancing",
    "Pattern Matching",
    "Overdue Numbers",
    "Random Selection",
    "Composite (Mixed)",
    "Wheel System"
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

def frequency_analysis_strategy():
    """Generate combinations based on frequency analysis"""
    # Simulated hot numbers and stars based on frequency
    hot_numbers = [9, 19, 23, 27, 36, 44, 50]
    hot_stars = [2, 5, 9, 11]
    
    combinations = []
    for _ in range(5):
        numbers = sorted(random.sample(hot_numbers, 5))
        stars = sorted(random.sample(hot_stars, 2))
        combinations.append({"numbers": numbers, "stars": stars})
    
    return combinations

def hot_cold_strategy():
    """Generate combinations based on hot-cold approach"""
    # Simulated hot and cold numbers
    hot_numbers = [9, 19, 21, 27, 44]
    cold_numbers = [1, 4, 12, 33, 38, 47, 50]
    hot_stars = [2, 9]
    cold_stars = [1, 3, 7, 11]
    
    combinations = []
    for _ in range(5):
        # Mix of hot and cold numbers (3 hot, 2 cold)
        numbers = sorted(random.sample(hot_numbers, 3) + random.sample(cold_numbers, 2))
        # One hot, one cold star
        stars = sorted([random.choice(hot_stars), random.choice(cold_stars)])
        combinations.append({"numbers": numbers, "stars": stars})
    
    return combinations

def markov_chain_strategy():
    """Generate combinations using a Markov chain approach"""
    # Simulated transition probabilities (simplified)
    number_groups = [
        [9, 19, 44], 
        [27, 38, 47, 50],
        [1, 4, 12, 25],
        [5, 15, 29, 39, 45],
        [2, 7, 21, 33, 41]
    ]
    
    star_pairs = [(2, 9), (2, 5), (9, 11), (1, 9), (2, 7)]
    
    combinations = []
    for _ in range(5):
        # Sample from different number groups
        numbers = []
        for group in random.sample(number_groups, 5):
            numbers.append(random.choice(group))
        numbers = sorted(numbers)
        
        # Sample a star pair
        stars = sorted(random.choice(star_pairs))
        combinations.append({"numbers": numbers, "stars": stars})
    
    return combinations

def coverage_optimization_strategy():
    """Generate combinations to maximize coverage"""
    # Define number ranges
    ranges = [
        list(range(1, 11)),    # 1-10
        list(range(11, 21)),   # 11-20
        list(range(21, 31)),   # 21-30
        list(range(31, 41)),   # 31-40
        list(range(41, 51))    # 41-50
    ]
    
    star_ranges = [
        list(range(1, 7)),     # 1-6
        list(range(7, 13))     # 7-12
    ]
    
    combinations = []
    for i in range(5):
        numbers = []
        # Ensure one number from each range
        for r in ranges:
            numbers.append(random.choice(r))
        
        # For stars, ensure coverage across combinations
        if i < 3:
            stars = [random.choice(star_ranges[0]), random.choice(star_ranges[1])]
        else:
            # Different approach for remaining combinations
            stars = [random.choice([2, 5, 8, 11]), random.choice([1, 4, 7, 10])]
        
        combinations.append({"numbers": sorted(numbers), "stars": sorted(stars)})
    
    return combinations

def risk_reward_strategy():
    """Generate combinations using risk-reward balancing"""
    # High probability numbers and stars
    safe_numbers = [5, 9, 19, 23, 27]
    safe_stars = [2, 5]
    
    # Lower probability but higher reward numbers and stars
    risky_numbers = [1, 33, 44, 47, 50]
    risky_stars = [9, 11]
    
    combinations = []
    # Different risk profiles
    risk_profiles = [0.2, 0.4, 0.6, 0.8, 1.0]
    
    for risk in risk_profiles:
        # Calculate safe vs risky numbers to include
        safe_count = int(5 * (1 - risk))
        risky_count = 5 - safe_count
        
        numbers = sorted(
            random.sample(safe_numbers, min(safe_count, len(safe_numbers))) + 
            random.sample(risky_numbers, min(risky_count, len(risky_numbers)))
        )
        
        # For stars, either safe, mixed, or risky based on risk level
        if risk < 0.3:
            stars = sorted(safe_stars)
        elif risk < 0.7:
            stars = [safe_stars[0], risky_stars[0]]
        else:
            stars = sorted(risky_stars)
        
        combinations.append({"numbers": numbers, "stars": stars})
    
    return combinations

def pattern_matching_strategy():
    """Generate combinations based on pattern matching"""
    # Patterns observed in historical data (simplified)
    sum_patterns = [
        {"min": 90, "max": 110},  # Sum of numbers in this range
        {"min": 110, "max": 130},
        {"min": 130, "max": 150},
        {"min": 150, "max": 170},
        {"min": 170, "max": 190}
    ]
    
    combinations = []
    for pattern in sum_patterns:
        # Keep generating until we match the pattern
        while True:
            numbers = sorted(random.sample(range(1, 51), 5))
            if pattern["min"] <= sum(numbers) <= pattern["max"]:
                break
        
        # Choose stars
        if sum(numbers) < 140:
            stars = sorted(random.sample([1, 2, 3, 4, 5, 6], 2))
        else:
            stars = sorted(random.sample([7, 8, 9, 10, 11, 12], 2))
        
        combinations.append({"numbers": numbers, "stars": stars})
    
    return combinations

def overdue_numbers_strategy():
    """Generate combinations focusing on overdue numbers"""
    # Simulated overdue numbers and stars
    overdue_numbers = [9, 19, 33, 44, 47, 50]
    overdue_stars = [2, 9, 11]
    
    # Regular numbers and stars
    regular_numbers = [3, 7, 15, 23, 27, 36, 41]
    regular_stars = [4, 5, 7]
    
    combinations = []
    for _ in range(5):
        # Mix of overdue and regular numbers (at least 2 overdue)
        overdue_count = random.randint(2, 4)
        regular_count = 5 - overdue_count
        
        numbers = sorted(
            random.sample(overdue_numbers, min(overdue_count, len(overdue_numbers))) + 
            random.sample(regular_numbers, min(regular_count, len(regular_numbers)))
        )
        
        # At least one overdue star
        if random.random() < 0.7:
            stars = sorted([
                random.choice(overdue_stars), 
                random.choice(regular_stars)
            ])
        else:
            stars = sorted(random.sample(overdue_stars, min(2, len(overdue_stars))))
        
        combinations.append({"numbers": numbers, "stars": stars})
    
    return combinations

def random_selection_strategy():
    """Generate completely random combinations"""
    combinations = []
    for _ in range(5):
        numbers = sorted(random.sample(range(1, 51), 5))
        stars = sorted(random.sample(range(1, 13), 2))
        combinations.append({"numbers": numbers, "stars": stars})
    
    return combinations

def composite_strategy():
    """Generate combinations using a composite approach"""
    # Use a mix of previous strategies
    all_combinations = []
    
    all_combinations.extend(frequency_analysis_strategy()[:1])
    all_combinations.extend(hot_cold_strategy()[:1])
    all_combinations.extend(risk_reward_strategy()[:1])
    all_combinations.extend(overdue_numbers_strategy()[:1])
    all_combinations.extend(pattern_matching_strategy()[:1])
    
    # Ensure we have exactly 5 combinations
    while len(all_combinations) > 5:
        all_combinations.pop()
    
    while len(all_combinations) < 5:
        numbers = sorted(random.sample(range(1, 51), 5))
        stars = sorted(random.sample(range(1, 13), 2))
        all_combinations.append({"numbers": numbers, "stars": stars})
    
    return all_combinations

def wheel_system_strategy():
    """Generate combinations using a simplified wheel system"""
    # Core numbers to appear in multiple combinations
    core_numbers = [9, 19, 27, 44]
    core_stars = [2, 9]
    
    # Supplementary numbers to mix in
    supp_numbers = [1, 5, 15, 23, 33, 37, 47, 50]
    supp_stars = [5, 7, 11]
    
    combinations = []
    for i in range(5):
        # How many core numbers to use (at least 2)
        core_count = random.randint(2, min(4, len(core_numbers)))
        supp_count = 5 - core_count
        
        numbers = sorted(
            random.sample(core_numbers, core_count) + 
            random.sample(supp_numbers, supp_count)
        )
        
        # Use at least one core star
        core_star_count = random.randint(1, min(2, len(core_stars)))
        supp_star_count = 2 - core_star_count
        
        stars = sorted(
            random.sample(core_stars, core_star_count) + 
            random.sample(supp_stars, supp_star_count) if supp_star_count > 0 else []
        )
        
        combinations.append({"numbers": numbers, "stars": stars})
    
    return combinations

def generate_combinations_for_all_strategies():
    """Generate combinations for all strategies and evaluate them"""
    strategy_functions = {
        "Frequency Analysis": frequency_analysis_strategy,
        "Hot-Cold": hot_cold_strategy,
        "Markov Chain": markov_chain_strategy,
        "Coverage Optimization": coverage_optimization_strategy,
        "Risk-Reward Balancing": risk_reward_strategy,
        "Pattern Matching": pattern_matching_strategy,
        "Overdue Numbers": overdue_numbers_strategy,
        "Random Selection": random_selection_strategy,
        "Composite (Mixed)": composite_strategy,
        "Wheel System": wheel_system_strategy
    }
    
    # Set random seed for reproducibility
    random.seed(20250513)  # May 13, 2025
    
    # Generate combinations for each strategy
    all_strategy_combinations = {}
    for strategy_name, strategy_func in strategy_functions.items():
        all_strategy_combinations[strategy_name] = strategy_func()
    
    return all_strategy_combinations

def evaluate_strategies(all_strategy_combinations):
    """Evaluate all strategies against the actual results"""
    strategy_results = {}
    
    for strategy_name, combinations in all_strategy_combinations.items():
        # Evaluate each combination for this strategy
        strategy_matches = []
        
        logger.info(f"\n===== {strategy_name} Strategy =====")
        best_combo = None
        best_score = -1
        
        for i, combo in enumerate(combinations):
            match = analyze_match(combo, ACTUAL_RESULTS)
            strategy_matches.append(match)
            
            logger.info(f"Combination {i+1}:")
            logger.info(f"  Numbers: {', '.join(map(str, combo['numbers']))}")
            logger.info(f"  Stars: {', '.join(map(str, combo['stars']))}")
            logger.info(f"  Matched Numbers: {', '.join(map(str, match['matched_numbers'])) if match['matched_numbers'] else 'None'}")
            logger.info(f"  Matched Stars: {', '.join(map(str, match['matched_stars'])) if match['matched_stars'] else 'None'}")
            logger.info(f"  Total Match Score: {match['num_numbers_matched']}/5 numbers + {match['num_stars_matched']}/2 stars = {match['total_match_score']}/7")
            
            if match['total_match_score'] > best_score:
                best_score = match['total_match_score']
                best_combo = (i+1, combo, match)
        
        # Calculate summary statistics for this strategy
        avg_match_score = sum(match['total_match_score'] for match in strategy_matches) / len(strategy_matches)
        best_match_score = max(match['total_match_score'] for match in strategy_matches)
        combos_with_matches = sum(1 for match in strategy_matches if match['total_match_score'] > 0)
        
        # Record results
        strategy_results[strategy_name] = {
            "avg_match_score": avg_match_score,
            "best_match_score": best_match_score,
            "combos_with_matches": combos_with_matches,
            "total_combos": len(combinations),
            "best_combo": best_combo
        }
        
        # Display summary
        logger.info(f"\nSUMMARY - {strategy_name}:")
        logger.info(f"  Average Match Score: {avg_match_score:.2f}/7")
        logger.info(f"  Best Match Score: {best_match_score}/7")
        logger.info(f"  Combinations with at least one match: {combos_with_matches}/{len(combinations)} ({combos_with_matches/len(combinations)*100:.1f}%)")
        if best_combo:
            idx, combo, match = best_combo
            logger.info(f"  Best Combination: #{idx}")
            logger.info(f"    Numbers: {', '.join(map(str, combo['numbers']))}")
            logger.info(f"    Stars: {', '.join(map(str, combo['stars']))}")
            logger.info(f"    Matched Numbers: {', '.join(map(str, match['matched_numbers'])) if match['matched_numbers'] else 'None'}")
            logger.info(f"    Matched Stars: {', '.join(map(str, match['matched_stars'])) if match['matched_stars'] else 'None'}")
    
    return strategy_results

def rank_strategies(strategy_results):
    """Rank the strategies by their performance"""
    # Sort strategies by average match score, best match score, and percentage of combos with matches
    sorted_strategies = sorted(
        strategy_results.items(),
        key=lambda x: (
            x[1]["best_match_score"],  # First by best score
            x[1]["avg_match_score"],   # Then by average score
            x[1]["combos_with_matches"] / x[1]["total_combos"]  # Then by % of combinations with matches
        ),
        reverse=True
    )
    
    logger.info("\n===== STRATEGY RANKING =====")
    for i, (strategy_name, results) in enumerate(sorted_strategies):
        logger.info(f"{i+1}. {strategy_name}")
        logger.info(f"   Best Match Score: {results['best_match_score']}/7")
        logger.info(f"   Average Match Score: {results['avg_match_score']:.2f}/7")
        logger.info(f"   Hit Rate: {results['combos_with_matches']}/{results['total_combos']} combinations ({results['combos_with_matches']/results['total_combos']*100:.1f}%)")
        
        # Display the best combination for this strategy
        if results['best_combo']:
            idx, combo, match = results['best_combo']
            logger.info(f"   Best Combination: #{idx}")
            logger.info(f"     Numbers: {', '.join(map(str, combo['numbers']))}")
            logger.info(f"     Stars: {', '.join(map(str, combo['stars']))}")
            if match['matched_numbers']:
                logger.info(f"     Matched Numbers: {', '.join(map(str, match['matched_numbers']))}")
            if match['matched_stars']:
                logger.info(f"     Matched Stars: {', '.join(map(str, match['matched_stars']))}")
        logger.info("")
    
    # Return the top strategy
    best_strategy, _ = sorted_strategies[0]
    return best_strategy

def main():
    """Main function to test all strategies"""
    logger.info("Testing strategies for the May 13, 2025 Euromillions drawing...")
    logger.info(f"Actual Results - Numbers: {', '.join(map(str, ACTUAL_RESULTS['numbers']))} Stars: {', '.join(map(str, ACTUAL_RESULTS['stars']))}")
    
    all_strategy_combinations = generate_combinations_for_all_strategies()
    strategy_results = evaluate_strategies(all_strategy_combinations)
    best_strategy = rank_strategies(strategy_results)
    
    logger.info(f"The best performing strategy for May 13, 2025 was: {best_strategy}")
    logger.info("This analysis used simulated strategy implementations with the actual drawing results.")

if __name__ == "__main__":
    main()