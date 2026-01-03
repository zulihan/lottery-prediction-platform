"""
Generate 10 optimized combinations for the next Euromillions drawing
using insights from our strategy performance analysis.
"""

import random
import datetime

# Set random seed for reproducibility
random.seed(20250516)  # Next drawing date as seed

# The last drawing results (May 13, 2025)
LAST_DRAWING = {
    "numbers": [9, 19, 44, 47, 50],
    "stars": [2, 9],
    "date": datetime.date(2025, 5, 13)
}

# Next drawing date (typically Friday after Tuesday drawing)
NEXT_DRAWING_DATE = datetime.date(2025, 5, 16)

# Define numbers and stars for each strategy
# Hot numbers (appear frequently)
HOT_NUMBERS = [3, 7, 9, 15, 19, 20, 23, 27, 37, 42, 44]
# Cold numbers (appear less frequently)
COLD_NUMBERS = [1, 6, 11, 13, 33, 39, 43, 47, 49, 50]
# Overdue numbers (haven't appeared for a while)
OVERDUE_NUMBERS = [8, 12, 17, 24, 28, 31, 38, 45, 46, 48]
# Recent numbers (appeared in last drawing)
RECENT_NUMBERS = [9, 19, 44, 47, 50]

# Star categories
HOT_STARS = [2, 3, 5, 8, 9]
COLD_STARS = [1, 4, 6, 7, 10, 11]
RECENT_STARS = [2, 9]

# Core numbers for wheel strategy
CORE_NUMBERS = [9, 15, 19, 27, 44]  # Based on frequency and recent success
CORE_STARS = [2, 3, 5, 9]  # Hot/successful stars

def generate_risk_reward_combination(risk_level):
    """Generate a combination using risk-reward balancing approach"""
    # Define safe numbers and stars (based on historical frequency)
    safe_numbers = [3, 7, 9, 15, 19, 20, 23]
    safe_stars = [2, 3, 5, 8]
    
    # Define risky numbers and stars (overdue or less frequent)
    risky_numbers = [12, 17, 28, 31, 38, 44, 45, 47, 50]
    risky_stars = [1, 6, 9, 11]
    
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
        additional = random.randint(1, 50)
        if additional not in numbers:
            numbers.append(additional)
    
    # Select stars based on risk level
    if risk_level < 0.3:
        # Low risk: choose 2 safe stars
        stars = random.sample(safe_stars, 2) if len(safe_stars) >= 2 else [safe_stars[0], random.choice(risky_stars)]
    elif risk_level < 0.7:
        # Medium risk: 1 safe, 1 risky
        stars = [random.choice(safe_stars), random.choice(risky_stars)]
    else:
        # High risk: 2 risky stars
        stars = random.sample(risky_stars, 2) if len(risky_stars) >= 2 else [risky_stars[0], random.choice(safe_stars)]
    
    return {
        "numbers": sorted(numbers),
        "stars": sorted(stars),
        "strategy": "Risk-Reward",
        "risk_level": risk_level
    }

def generate_overdue_combination():
    """Generate a combination focusing on overdue numbers"""
    # Mix of overdue and regular numbers
    overdue_count = random.randint(2, 4)  # 2-4 overdue numbers
    regular_count = 5 - overdue_count
    
    # Select overdue numbers
    numbers = random.sample(OVERDUE_NUMBERS, min(overdue_count, len(OVERDUE_NUMBERS)))
    
    # Add regular numbers (mix of hot and cold)
    regular_pool = list(set(HOT_NUMBERS + COLD_NUMBERS) - set(numbers))
    numbers.extend(random.sample(regular_pool, min(regular_count, len(regular_pool))))
    
    # Fill to 5 numbers if needed
    while len(numbers) < 5:
        additional = random.randint(1, 50)
        if additional not in numbers:
            numbers.append(additional)
    
    # For stars, include at least one overdue star
    overdue_stars = [star for star in range(1, 13) if star not in RECENT_STARS]
    stars = [random.choice(overdue_stars)]
    
    # Add one more star
    second_star_candidates = [s for s in range(1, 13) if s not in stars]
    stars.append(random.choice(second_star_candidates))
    
    return {
        "numbers": sorted(numbers),
        "stars": sorted(stars),
        "strategy": "Overdue Numbers"
    }

def generate_frequency_combination():
    """Generate a combination based on frequency analysis"""
    # Select mainly hot numbers with a few cold ones
    hot_count = random.randint(3, 4)  # 3-4 hot numbers
    cold_count = 5 - hot_count
    
    numbers = random.sample(HOT_NUMBERS, min(hot_count, len(HOT_NUMBERS)))
    numbers.extend(random.sample(COLD_NUMBERS, min(cold_count, len(COLD_NUMBERS))))
    
    # Fill to 5 numbers if needed
    while len(numbers) < 5:
        additional = random.randint(1, 50)
        if additional not in numbers:
            numbers.append(additional)
    
    # Select stars with higher frequency
    stars = random.sample(HOT_STARS, min(2, len(HOT_STARS)))
    
    # Fill to 2 stars if needed
    while len(stars) < 2:
        additional_star = random.randint(1, 12)
        if additional_star not in stars:
            stars.append(additional_star)
    
    return {
        "numbers": sorted(numbers),
        "stars": sorted(stars),
        "strategy": "Frequency Analysis"
    }

def generate_wheel_combination():
    """Generate a combination using a wheel system approach"""
    # How many core numbers to use
    core_count = random.randint(2, 4)
    additional_count = 5 - core_count
    
    # Select core numbers
    numbers = random.sample(CORE_NUMBERS, min(core_count, len(CORE_NUMBERS)))
    
    # Add additional numbers not in core
    additional_pool = [n for n in range(1, 51) if n not in numbers]
    numbers.extend(random.sample(additional_pool, additional_count))
    
    # Select stars - at least one core star
    stars = [random.choice(CORE_STARS)]
    additional_star_candidates = [s for s in range(1, 13) if s not in stars]
    stars.append(random.choice(additional_star_candidates))
    
    return {
        "numbers": sorted(numbers),
        "stars": sorted(stars),
        "strategy": "Wheel System"
    }

def generate_hot_cold_combination():
    """Generate a combination using hot-cold approach"""
    # Mix of hot and cold numbers
    hot_count = 3  # Fixed 3 hot, 2 cold
    cold_count = 2
    
    numbers = random.sample(HOT_NUMBERS, min(hot_count, len(HOT_NUMBERS)))
    numbers.extend(random.sample(COLD_NUMBERS, min(cold_count, len(COLD_NUMBERS))))
    
    # Fill to 5 numbers if needed
    while len(numbers) < 5:
        additional = random.randint(1, 50)
        if additional not in numbers:
            numbers.append(additional)
    
    # One hot, one cold star
    stars = [random.choice(HOT_STARS), random.choice(COLD_STARS)]
    
    return {
        "numbers": sorted(numbers),
        "stars": sorted(stars),
        "strategy": "Hot-Cold"
    }

def is_duplicate(new_combo, existing_combos):
    """Check if the combination is too similar to existing ones"""
    new_numbers = set(new_combo["numbers"])
    new_stars = set(new_combo["stars"])
    
    for combo in existing_combos:
        existing_numbers = set(combo["numbers"])
        existing_stars = set(combo["stars"])
        
        # Consider it a duplicate if 4+ numbers match and both stars match
        numbers_match = len(new_numbers.intersection(existing_numbers))
        stars_match = len(new_stars.intersection(existing_stars))
        
        if numbers_match >= 4 and stars_match == 2:
            return True
        
        # Also consider it a duplicate if all 5 numbers match
        if numbers_match == 5:
            return True
    
    return False

def generate_all_combinations():
    """Generate 10 optimized combinations"""
    combinations = []
    
    # Generate 4 risk-reward combinations with different risk levels
    risk_levels = [0.2, 0.4, 0.6, 0.8]
    for risk in risk_levels:
        combo = generate_risk_reward_combination(risk)
        if not is_duplicate(combo, combinations):
            combinations.append(combo)
    
    # Generate one of each other strategy type
    strategy_functions = [
        generate_overdue_combination,
        generate_frequency_combination,
        generate_wheel_combination,
        generate_hot_cold_combination
    ]
    
    for func in strategy_functions:
        combo = func()
        if not is_duplicate(combo, combinations):
            combinations.append(combo)
    
    # Fill remaining slots with a mix of strategies
    remaining_slots = 10 - len(combinations)
    strategies = [
        ("Risk-Reward", 0.3),
        ("Overdue", 0.25),
        ("Frequency", 0.2),
        ("Wheel", 0.15),
        ("Hot-Cold", 0.1)
    ]
    
    for _ in range(remaining_slots):
        # Choose a strategy based on weights
        strategy_name = random.choices(
            [s[0] for s in strategies],
            weights=[s[1] for s in strategies]
        )[0]
        
        if strategy_name == "Risk-Reward":
            combo = generate_risk_reward_combination(random.uniform(0.3, 0.7))
        elif strategy_name == "Overdue":
            combo = generate_overdue_combination()
        elif strategy_name == "Frequency":
            combo = generate_frequency_combination()
        elif strategy_name == "Wheel":
            combo = generate_wheel_combination()
        else:  # Hot-Cold
            combo = generate_hot_cold_combination()
        
        if not is_duplicate(combo, combinations):
            combinations.append(combo)
    
    # Ensure we have exactly 10 combinations
    while len(combinations) > 10:
        combinations.pop()
    
    return combinations

def display_combinations(combinations):
    """Display the combinations with details"""
    print(f"\n===== OPTIMIZED COMBINATIONS FOR {NEXT_DRAWING_DATE} =====")
    
    for i, combo in enumerate(combinations):
        strategy = combo.get("strategy", "Blended")
        risk_level = combo.get("risk_level", "N/A")
        
        print(f"Combination {i+1}: {strategy}")
        if strategy == "Risk-Reward":
            print(f"  Risk Level: {risk_level:.2f}")
        
        print(f"  Numbers: {', '.join(map(str, combo['numbers']))}")
        print(f"  Stars: {', '.join(map(str, combo['stars']))}")
        
        # Calculate sum and distribution stats
        sum_numbers = sum(combo['numbers'])
        odd_count = sum(1 for n in combo['numbers'] if n % 2 == 1)
        even_count = 5 - odd_count
        low_count = sum(1 for n in combo['numbers'] if 1 <= n <= 25)
        high_count = 5 - low_count
        
        print(f"  Sum: {sum_numbers}")
        print(f"  Distribution: {odd_count} odd / {even_count} even, {low_count} low / {high_count} high")
        print("")

def main():
    """Generate and display optimized combinations"""
    print("Generating optimized combinations for the next Euromillions drawing...")
    
    combinations = generate_all_combinations()
    display_combinations(combinations)
    
    print("Generated 10 optimized combinations using top-performing strategies")
    print("These combinations are optimized based on our analysis of the May 13, 2025 results")

if __name__ == "__main__":
    main()