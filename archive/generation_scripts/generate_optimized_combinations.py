import sys
import pandas as pd
import numpy as np
import json
import random
from datetime import datetime
import database
from statistics import EuromillionsStatistics
from strategies import PredictionStrategies

def load_data():
    """Load all drawing data from the database"""
    return database.get_all_drawings()

def generate_frequency_combinations(stats, strategies, count=4):
    """Generate combinations using the frequency strategy"""
    combinations = strategies.frequency_strategy(
        num_combinations=count,
        recent_weight=2.75  # Higher weight on recent draws
    )
    
    # Ensure we have 3 stars for each combination
    for combo in combinations:
        # Get the existing stars
        stars = combo['stars']
        
        # If we already have 3 or more stars, just take the first 3
        if len(stars) >= 3:
            combo['stars'] = stars[:3]
        else:
            # Add more stars to get to 3
            all_stars = list(range(1, 13))
            additional_stars = [s for s in all_stars if s not in stars]
            stars.extend(random.sample(additional_stars, 3 - len(stars)))
            combo['stars'] = stars
    
    return combinations

def generate_risk_reward_combinations(stats, strategies, count=3):
    """Generate combinations using the risk-reward strategy"""
    combinations = strategies.risk_reward_strategy(
        num_combinations=count,
        risk_level=6  # Medium-high risk level
    )
    
    # Ensure we have 3 stars for each combination
    for combo in combinations:
        # Get the existing stars
        stars = combo['stars']
        
        # If we already have 3 or more stars, just take the first 3
        if len(stars) >= 3:
            combo['stars'] = stars[:3]
        else:
            # Add more stars to get to 3
            all_stars = list(range(1, 13))
            additional_stars = [s for s in all_stars if s not in stars]
            stars.extend(random.sample(additional_stars, 3 - len(stars)))
            combo['stars'] = stars
    
    return combinations

def generate_ultimate_combination(all_combinations):
    """Generate one ultimate combination based on repeated numbers across all combinations"""
    # Extract all numbers and stars
    all_numbers = []
    all_stars = []
    
    for combo in all_combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    # Count frequency of each number and star
    number_counts = {}
    for num in all_numbers:
        number_counts[num] = number_counts.get(num, 0) + 1
    
    star_counts = {}
    for star in all_stars:
        star_counts[star] = star_counts.get(star, 0) + 1
    
    # Get most frequently occurring numbers and stars
    sorted_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_stars = sorted(star_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Select top 5 numbers and 3 stars
    numbers = [num for num, _ in sorted_numbers[:5]]
    stars = [star for star, _ in sorted_stars[:3]]
    
    # Ensure we have 5 numbers and 3 stars
    while len(numbers) < 5:
        num = random.randint(1, 50)
        if num not in numbers:
            numbers.append(num)
    
    while len(stars) < 3:
        star = random.randint(1, 12)
        if star not in stars:
            stars.append(star)
    
    # Sort the numbers and stars in ascending order
    numbers.sort()
    stars.sort()
    
    return {
        'numbers': numbers,
        'stars': stars,
        'score': 95.0,  # Ultimate combination gets a high score
        'strategy': 'Ultimate Combined'
    }

def main():
    """Generate optimized combinations for the next Euromillions draw"""
    # Load data
    data = load_data()
    
    # Initialize statistics and strategies
    stats = EuromillionsStatistics(data)
    strategies = PredictionStrategies(stats)
    
    # Generate combinations with different strategies
    frequency_combinations = generate_frequency_combinations(stats, strategies, count=4)
    risk_reward_combinations = generate_risk_reward_combinations(stats, strategies, count=3)
    
    # Combine all strategy combinations
    all_combinations = frequency_combinations + risk_reward_combinations
    
    # Generate one ultimate combination from all the others
    ultimate_combination = generate_ultimate_combination(all_combinations)
    
    # Add strategy names to combinations
    for combo in frequency_combinations:
        combo['strategy'] = 'Frequency'
    
    for combo in risk_reward_combinations:
        combo['strategy'] = 'Risk/Reward'
    
    # Final set of combinations
    final_combinations = all_combinations + [ultimate_combination]
    
    # Sort by score
    final_combinations.sort(key=lambda x: x['score'], reverse=True)
    
    # Print results
    print(f"Generated {len(final_combinations)} optimized combinations for the next Euromillions draw:\n")
    
    for i, combo in enumerate(final_combinations, 1):
        numbers_str = "-".join(map(str, combo['numbers']))
        stars_str = "-".join(map(str, combo['stars']))
        print(f"Combination {i}: {numbers_str} / {stars_str}")
        print(f"Strategy: {combo['strategy']}")
        print(f"Score: {combo['score']}\n")
    
    # Save to database if requested
    if len(sys.argv) > 1 and sys.argv[1] == '--save':
        draw_date = datetime.now().strftime("%Y-%m-%d")
        
        print(f"Saving combinations to database for {draw_date}...")
        
        for combo in final_combinations:
            database.save_user_combination(
                numbers=combo['numbers'],
                stars=combo['stars'],
                strategy=combo['strategy'],
                notes=f"Score: {combo['score']}"
            )
        
        print("Combinations saved to database.")

if __name__ == "__main__":
    main()
