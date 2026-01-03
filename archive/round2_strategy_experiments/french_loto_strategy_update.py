"""
French Loto Strategy Update based on May 12, 2025 results
This script analyzes our recent performance and generates improved combinations
"""

import random
import datetime
from collections import Counter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Last draw results (May 12, 2025)
LAST_DRAW = {
    "numbers": [2, 6, 12, 16, 24],
    "lucky": 4,
    "date": datetime.date(2025, 5, 12)
}

# Our previous prediction (the one that got 3 hits)
SUCCESSFUL_PREDICTION = {
    "numbers": [2, 12, 14, 24, 25],
    "lucky": 6,
    "strategy": "Risk/Reward Balance",
    "score": 83.00
}

# Tonight's draw date
TONIGHT = datetime.date(2025, 5, 16)

# Define number categories for French Loto (1-49 for main numbers, 1-10 for lucky)
# Hot numbers (high frequency)
HOT_NUMBERS = [1, 2, 3, 7, 9, 12, 16, 22, 24, 26, 32, 33, 41, 45]
HOT_LUCKY = [1, 3, 4, 6, 8, 9]

# Cold numbers (low frequency)
COLD_NUMBERS = [4, 5, 10, 18, 20, 23, 29, 31, 37, 38, 42, 46, 47, 49]
COLD_LUCKY = [2, 5, 7, 10]

# Numbers from previous 3 draws
RECENT_NUMBERS = [2, 6, 8, 12, 14, 15, 16, 18, 24, 25, 28, 31, 36, 43, 49]
RECENT_LUCKY = [4, 6, 8]

# Overdue numbers (not drawn for a long time)
OVERDUE_NUMBERS = [11, 13, 17, 19, 21, 27, 30, 34, 35, 39, 40, 44, 48]
OVERDUE_LUCKY = [1, 2, 5, 10]

def analyze_recent_performance():
    """Analyze what worked and what didn't in our most recent predictions"""
    # Successful numbers (what we got right)
    successful_numbers = set(SUCCESSFUL_PREDICTION["numbers"]).intersection(set(LAST_DRAW["numbers"]))
    logger.info("Performance Analysis:")
    logger.info(f"Successful numbers: {', '.join(map(str, successful_numbers))}")
    
    # Missed numbers and their characteristics
    missed_numbers = set(LAST_DRAW["numbers"]) - successful_numbers
    logger.info(f"Missed numbers: {', '.join(map(str, missed_numbers))}")
    
    # Lucky number performance
    if SUCCESSFUL_PREDICTION["lucky"] == LAST_DRAW["lucky"]:
        logger.info(f"Successfully predicted lucky number: {LAST_DRAW['lucky']}")
    else:
        logger.info(f"Missed lucky number: predicted {SUCCESSFUL_PREDICTION['lucky']}, actual {LAST_DRAW['lucky']}")
    
    # Analyze characteristics of hits vs. misses
    hits_hot = sum(1 for num in successful_numbers if num in HOT_NUMBERS)
    hits_cold = sum(1 for num in successful_numbers if num in COLD_NUMBERS)
    hits_overdue = sum(1 for num in successful_numbers if num in OVERDUE_NUMBERS)
    
    misses_hot = sum(1 for num in missed_numbers if num in HOT_NUMBERS)
    misses_cold = sum(1 for num in missed_numbers if num in COLD_NUMBERS)
    misses_overdue = sum(1 for num in missed_numbers if num in OVERDUE_NUMBERS)
    
    logger.info("\nHit Characteristics:")
    logger.info(f"Hot numbers: {hits_hot}/{len(successful_numbers)}")
    logger.info(f"Cold numbers: {hits_cold}/{len(successful_numbers)}")
    logger.info(f"Overdue numbers: {hits_overdue}/{len(successful_numbers)}")
    
    logger.info("\nMiss Characteristics:")
    logger.info(f"Hot numbers: {misses_hot}/{len(missed_numbers)}")
    logger.info(f"Cold numbers: {misses_cold}/{len(missed_numbers)}")
    logger.info(f"Overdue numbers: {misses_overdue}/{len(missed_numbers)}")
    
    # Identify number patterns
    sum_hit_numbers = sum(successful_numbers)
    avg_hit = sum_hit_numbers / len(successful_numbers) if successful_numbers else 0
    
    sum_missed = sum(missed_numbers)
    avg_missed = sum_missed / len(missed_numbers) if missed_numbers else 0
    
    logger.info(f"\nAverage of hit numbers: {avg_hit:.2f}")
    logger.info(f"Average of missed numbers: {avg_missed:.2f}")
    
    # Parity analysis
    hits_odd = sum(1 for num in successful_numbers if num % 2 == 1)
    hits_even = len(successful_numbers) - hits_odd
    
    misses_odd = sum(1 for num in missed_numbers if num % 2 == 1)
    misses_even = len(missed_numbers) - misses_odd
    
    logger.info(f"\nHit parity: {hits_odd} odd, {hits_even} even")
    logger.info(f"Miss parity: {misses_odd} odd, {misses_even} even")
    
    # Range analysis
    hits_low = sum(1 for num in successful_numbers if 1 <= num <= 25)
    hits_high = len(successful_numbers) - hits_low
    
    misses_low = sum(1 for num in missed_numbers if 1 <= num <= 25)
    misses_high = len(missed_numbers) - misses_low
    
    logger.info(f"\nHit range: {hits_low} low (1-25), {hits_high} high (26-49)")
    logger.info(f"Miss range: {misses_low} low (1-25), {misses_high} high (26-49)")
    
    return {
        "hits": successful_numbers,
        "misses": missed_numbers,
        "lucky_hit": SUCCESSFUL_PREDICTION["lucky"] == LAST_DRAW["lucky"],
        "hit_characteristics": {
            "hot": hits_hot,
            "cold": hits_cold,
            "overdue": hits_overdue,
            "odd": hits_odd,
            "even": hits_even,
            "low": hits_low,
            "high": hits_high,
            "avg": avg_hit
        },
        "miss_characteristics": {
            "hot": misses_hot,
            "cold": misses_cold,
            "overdue": misses_overdue,
            "odd": misses_odd,
            "even": misses_even,
            "low": misses_low,
            "high": misses_high,
            "avg": avg_missed
        }
    }

def identify_strategy_improvements(analysis):
    """Identify improvements to our strategy based on analysis"""
    improvements = []
    
    # Check if hot numbers performed well
    if analysis["hit_characteristics"]["hot"] > analysis["miss_characteristics"]["hot"]:
        improvements.append("Increase weight of hot numbers")
    else:
        improvements.append("Reduce weight of hot numbers")
    
    # Check overdue numbers
    if analysis["hit_characteristics"]["overdue"] > 0:
        improvements.append("Maintain inclusion of some overdue numbers")
    else:
        improvements.append("Reduce focus on overdue numbers")
    
    # Check lucky number strategy
    if not analysis["lucky_hit"]:
        improvements.append("Improve lucky number selection - focus more on hot lucky numbers")
    
    # Check parity balance
    hit_odd_ratio = analysis["hit_characteristics"]["odd"] / len(analysis["hits"]) if analysis["hits"] else 0
    all_odd_ratio = (analysis["hit_characteristics"]["odd"] + analysis["miss_characteristics"]["odd"]) / 5
    
    if abs(hit_odd_ratio - all_odd_ratio) > 0.2:
        if hit_odd_ratio > all_odd_ratio:
            improvements.append("Increase odd numbers in combinations")
        else:
            improvements.append("Increase even numbers in combinations")
    
    # Check number range balance
    hit_low_ratio = analysis["hit_characteristics"]["low"] / len(analysis["hits"]) if analysis["hits"] else 0
    all_low_ratio = (analysis["hit_characteristics"]["low"] + analysis["miss_characteristics"]["low"]) / 5
    
    if abs(hit_low_ratio - all_low_ratio) > 0.2:
        if hit_low_ratio > all_low_ratio:
            improvements.append("Focus more on lower numbers (1-25)")
        else:
            improvements.append("Focus more on higher numbers (26-49)")
    
    return improvements

def enhanced_risk_reward_strategy(risk_level=0.6):
    """
    Enhanced Risk/Reward Balance strategy for French Loto based on recent performance
    
    Args:
        risk_level: 0-1 value representing how risky the combination should be
                   (higher = more risky/overdue numbers)
    
    Returns:
        dict: Combination with numbers and lucky number
    """
    # Define safe numbers (based on frequency and recency)
    safe_numbers = [2, 3, 7, 9, 12, 16, 22, 24, 26, 32, 33, 41, 45]
    
    # Define risky numbers (overdue or cold)
    risky_numbers = [11, 13, 17, 19, 21, 27, 30, 34, 35, 39, 40, 44, 48]
    
    # Calculate mix of safe vs risky numbers
    safe_count = int(5 * (1 - risk_level))
    risky_count = 5 - safe_count
    
    # Select numbers
    numbers = []
    if safe_count > 0:
        numbers.extend(random.sample(safe_numbers, min(safe_count, len(safe_numbers))))
    if risky_count > 0:
        numbers.extend(random.sample(risky_numbers, min(risky_count, len(risky_numbers))))
    
    # Fill to 5 numbers if needed
    while len(numbers) < 5:
        additional = random.randint(1, 49)
        if additional not in numbers:
            numbers.append(additional)
    
    # Select lucky number - heavier weight on hot lucky numbers
    if random.random() < 0.7:  # 70% chance of hot lucky
        lucky = random.choice(HOT_LUCKY)
    else:
        lucky = random.choice(COLD_LUCKY)
    
    # Calculate a score based on expected performance
    score = calculate_score(numbers, lucky, risk_level)
    
    return {
        "numbers": sorted(numbers),
        "lucky": lucky,
        "strategy": "Enhanced Risk/Reward",
        "risk_level": risk_level,
        "score": score
    }

def enhanced_frequency_strategy():
    """
    Enhanced Frequency Analysis strategy for French Loto
    
    Returns:
        dict: Combination with numbers and lucky number
    """
    # Updated based on last draw - more focus on hot numbers
    numbers = []
    
    # 3-4 hot numbers
    hot_count = random.randint(3, 4)
    numbers.extend(random.sample(HOT_NUMBERS, min(hot_count, len(HOT_NUMBERS))))
    
    # 1-2 other numbers (mix of cold and overdue)
    other_count = 5 - len(numbers)
    other_pool = list(set(COLD_NUMBERS + OVERDUE_NUMBERS) - set(numbers))
    numbers.extend(random.sample(other_pool, min(other_count, len(other_pool))))
    
    # Fill to 5 numbers if needed (unlikely)
    while len(numbers) < 5:
        additional = random.randint(1, 49)
        if additional not in numbers:
            numbers.append(additional)
    
    # Select lucky number - 80% chance of hot lucky
    if random.random() < 0.8:
        lucky = random.choice(HOT_LUCKY)
    else:
        lucky = random.choice(COLD_LUCKY)
    
    # Calculate score
    score = calculate_score(numbers, lucky, 0.5)  # Medium risk level
    
    return {
        "numbers": sorted(numbers),
        "lucky": lucky,
        "strategy": "Enhanced Frequency",
        "score": score
    }

def pattern_based_strategy():
    """
    Pattern-based strategy that looks for number patterns from previous draws
    
    Returns:
        dict: Combination with numbers and lucky number
    """
    # Use patterns from last draw
    # 1. Number pairs often repeat (e.g., 2+12, 16+24 from last draw)
    numbers = []
    
    # Start with 1-2 pairs from recent draws
    pair_count = random.randint(1, 2)
    pairs = [
        [2, 12],
        [16, 24],
        [2, 16],
        [12, 24],
        [6, 16]
    ]
    
    selected_pairs = random.sample(pairs, min(pair_count, len(pairs)))
    for pair in selected_pairs:
        for num in pair:
            if num not in numbers and len(numbers) < 5:
                numbers.append(num)
    
    # Add additional numbers to reach 5
    remaining_count = 5 - len(numbers)
    if remaining_count > 0:
        remaining_pool = list(set(range(1, 50)) - set(numbers))
        numbers.extend(random.sample(remaining_pool, remaining_count))
    
    # Select lucky number based on patterns
    # The lucky number is often within +/-2 of a recent lucky number
    recent_lucky = LAST_DRAW["lucky"]
    lucky_pool = [max(1, recent_lucky - 2), max(1, recent_lucky - 1), 
                 min(10, recent_lucky + 1), min(10, recent_lucky + 2)]
    lucky_pool = [l for l in lucky_pool if 1 <= l <= 10]
    lucky = random.choice(lucky_pool)
    
    # Calculate score
    score = calculate_score(numbers, lucky, 0.5)
    
    return {
        "numbers": sorted(numbers),
        "lucky": lucky,
        "strategy": "Pattern-Based",
        "score": score
    }

def balanced_distribution_strategy():
    """
    Strategy that ensures balanced distribution of numbers
    
    Returns:
        dict: Combination with numbers and lucky number
    """
    numbers = []
    
    # Ensure coverage across ranges
    ranges = [
        (1, 10),
        (11, 20),
        (21, 30),
        (31, 40),
        (41, 49)
    ]
    
    # Select one number from each range
    for low, high in random.sample(ranges, 5):
        number = random.randint(low, high)
        while number in numbers:
            number = random.randint(low, high)
        numbers.append(number)
    
    # Ensure a mix of odd/even
    while True:
        odd_count = sum(1 for n in numbers if n % 2 == 1)
        if 2 <= odd_count <= 3:  # Balanced odd/even
            break
        
        # Replace a random number to fix balance
        if odd_count < 2:  # Need more odd
            even_indices = [i for i, n in enumerate(numbers) if n % 2 == 0]
            idx_to_replace = random.choice(even_indices)
            
            range_index = next(i for i, (low, high) in enumerate(ranges) 
                              if low <= numbers[idx_to_replace] <= high)
            low, high = ranges[range_index]
            
            # Find odd numbers in this range
            odd_options = [n for n in range(low, high+1) if n % 2 == 1 and n not in numbers]
            if odd_options:
                numbers[idx_to_replace] = random.choice(odd_options)
        
        elif odd_count > 3:  # Need more even
            odd_indices = [i for i, n in enumerate(numbers) if n % 2 == 1]
            idx_to_replace = random.choice(odd_indices)
            
            range_index = next(i for i, (low, high) in enumerate(ranges) 
                              if low <= numbers[idx_to_replace] <= high)
            low, high = ranges[range_index]
            
            # Find even numbers in this range
            even_options = [n for n in range(low, high+1) if n % 2 == 0 and n not in numbers]
            if even_options:
                numbers[idx_to_replace] = random.choice(even_options)
        else:
            break  # Already balanced
    
    # Select lucky number - prefer middle range (4-7)
    lucky = random.randint(4, 7)
    
    # Calculate score
    score = calculate_score(numbers, lucky, 0.5)
    
    return {
        "numbers": sorted(numbers),
        "lucky": lucky,
        "strategy": "Balanced Distribution",
        "score": score
    }

def calculate_score(numbers, lucky, risk_level=0.5):
    """Calculate a score from 0-100 for the combination"""
    score = 50.0  # Start with a base score
    
    # Add points for hot numbers
    hot_count = sum(1 for n in numbers if n in HOT_NUMBERS)
    score += hot_count * 5
    
    # Add points for balance
    odd_count = sum(1 for n in numbers if n % 2 == 1)
    if 2 <= odd_count <= 3:
        score += 5
    
    # Add points for range balance
    low_count = sum(1 for n in numbers if 1 <= n <= 25)
    if 2 <= low_count <= 3:
        score += 5
    
    # Add points for hot lucky number
    if lucky in HOT_LUCKY:
        score += 10
    
    # Adjustment for risk preference
    score = score * (1 - risk_level) + (100 - score) * risk_level
    
    # Cap score between 0-100
    return min(100, max(0, score))

def is_duplicate(new_combo, existing_combos):
    """Check if a combination is too similar to existing ones"""
    new_numbers = set(new_combo["numbers"])
    
    for combo in existing_combos:
        existing_numbers = set(combo["numbers"])
        
        # Consider it a duplicate if 4+ numbers match
        if len(new_numbers.intersection(existing_numbers)) >= 4:
            return True
        
        # Consider it a duplicate if 3+ numbers match and same lucky
        if len(new_numbers.intersection(existing_numbers)) >= 3 and new_combo["lucky"] == combo["lucky"]:
            return True
    
    return False

def generate_combinations(count=10):
    """Generate optimized combinations for French Loto"""
    combinations = []
    
    # 4 risk-reward combinations with varying risk levels
    risk_levels = [0.3, 0.5, 0.7, 0.9]
    for risk in risk_levels:
        combo = enhanced_risk_reward_strategy(risk)
        if not is_duplicate(combo, combinations):
            combinations.append(combo)
    
    # 2 frequency-based combinations
    for _ in range(2):
        combo = enhanced_frequency_strategy()
        if not is_duplicate(combo, combinations):
            combinations.append(combo)
    
    # 2 pattern-based combinations
    for _ in range(2):
        combo = pattern_based_strategy()
        if not is_duplicate(combo, combinations):
            combinations.append(combo)
    
    # 2 balanced distribution combinations
    for _ in range(2):
        combo = balanced_distribution_strategy()
        if not is_duplicate(combo, combinations):
            combinations.append(combo)
    
    # Fill any remaining slots with risk-reward
    while len(combinations) < count:
        risk = random.uniform(0.4, 0.8)
        combo = enhanced_risk_reward_strategy(risk)
        if not is_duplicate(combo, combinations):
            combinations.append(combo)
    
    # Ensure we have exactly the requested number
    while len(combinations) > count:
        combinations.pop()
    
    return combinations

def display_combinations(combinations):
    """Display the generated combinations"""
    logger.info(f"\n===== OPTIMIZED COMBINATIONS FOR FRENCH LOTO {TONIGHT} =====")
    
    for i, combo in enumerate(combinations):
        strategy = combo.get("strategy", "Combined")
        risk_level = combo.get("risk_level", "N/A")
        
        logger.info(f"Combination {i+1}: {strategy}")
        if "risk_level" in combo:
            logger.info(f"  Risk Level: {risk_level:.2f}")
        
        logger.info(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
        logger.info(f"  Lucky Number: {combo['lucky']}")
        logger.info(f"  Score: {combo['score']:.2f}/100")
        
        # Calculate distribution stats
        odd_count = sum(1 for n in combo['numbers'] if n % 2 == 1)
        even_count = 5 - odd_count
        low_count = sum(1 for n in combo['numbers'] if 1 <= n <= 25)
        high_count = 5 - low_count
        
        logger.info(f"  Distribution: {odd_count} odd / {even_count} even, {low_count} low / {high_count} high")
        logger.info("")

def main():
    """Analyze recent performance and generate improved combinations"""
    logger.info("Analyzing French Loto performance from May 12, 2025 draw...")
    
    # Set random seed for reproducibility
    random.seed(int(TONIGHT.strftime("%Y%m%d")))
    
    analysis = analyze_recent_performance()
    improvements = identify_strategy_improvements(analysis)
    
    logger.info("\nStrategy Improvements:")
    for i, improvement in enumerate(improvements):
        logger.info(f"{i+1}. {improvement}")
    
    # Generate combinations with improved strategies
    combinations = generate_combinations(10)
    display_combinations(combinations)
    
    logger.info("Generated 10 optimized combinations using enhanced strategies")
    logger.info("These combinations are optimized based on our analysis of the May 12, 2025 results")

if __name__ == "__main__":
    main()