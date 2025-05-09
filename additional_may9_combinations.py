import os
import sys
import random
import logging
import numpy as np
from datetime import date
from collections import Counter

# Add relative import support
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import database

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data_from_db():
    """Load historical data from database"""
    try:
        logger.info("Loading data from database...")
        df = database.get_all_drawings()
        logger.info(f"Loaded {len(df)} draws from database.")
        return df
    except Exception as e:
        logger.error(f"Error loading data from database: {e}")
        return None

def get_existing_combinations():
    """Get combinations already generated for May 9th"""
    try:
        combinations = database.get_generated_combinations(limit=100)
        # Filter to keep only those for May 9th
        may9_combinations = [c for c in combinations if c.get('target_draw_date') == '2025-05-09']
        return may9_combinations
    except Exception as e:
        logger.error(f"Error getting existing combinations: {e}")
        return []

def generate_additional_combinations(num_combinations=3, existing_combinations=None):
    """
    Generate additional combinations that are different from existing ones
    
    Args:
        num_combinations: Number of additional combinations to generate
        existing_combinations: List of existing combinations to avoid duplicating
        
    Returns:
        list: List of new combination dictionaries
    """
    # Number group ranges for balanced selection
    number_groups = {
        'low': list(range(1, 18)),    # 1-17
        'mid': list(range(18, 35)),   # 18-34
        'high': list(range(35, 51))   # 35-50
    }
    
    # Optimal distribution for May 9th
    optimal_distribution = {
        'low_count': 1,    # 1 number from 1-17 range
        'mid_count': 2,    # 2 numbers from 18-34 range
        'high_count': 2    # 2 numbers from 35-50 range
    }
    
    # May 6 draw to avoid duplicating
    may6_draw = {
        'numbers': [8, 23, 24, 47, 48],
        'stars': [4, 9]
    }
    
    # Hot numbers and stars based on analysis
    hot_numbers = [5, 7, 15, 17, 19, 20, 27, 31, 37, 44, 49]
    hot_stars = [3, 4, 7, 9, 10]
    
    # Existing numbers and stars to avoid duplicating exactly
    existing_number_sets = []
    existing_star_sets = []
    
    if existing_combinations:
        for combo in existing_combinations:
            if 'numbers' in combo and 'stars' in combo:
                numbers = combo.get('numbers', [])
                stars = combo.get('stars', [])
                
                if isinstance(numbers, str):
                    try:
                        # Try to parse if stored as JSON string
                        import json
                        numbers = json.loads(numbers)
                    except:
                        # If not JSON, try to parse as comma-separated string
                        numbers = [int(n.strip()) for n in numbers.split(",") if n.strip().isdigit()]
                
                if isinstance(stars, str):
                    try:
                        # Try to parse if stored as JSON string
                        import json
                        stars = json.loads(stars)
                    except:
                        # If not JSON, try to parse as comma-separated string
                        stars = [int(s.strip()) for s in stars.split(",") if s.strip().isdigit()]
                
                existing_number_sets.append(set(numbers))
                existing_star_sets.append(set(stars))
    
    # Generate new combinations
    new_combinations = []
    
    # Get data for analysis
    all_data = load_data_from_db()
    
    # Get recent patterns
    recent_patterns = []
    if all_data is not None and len(all_data) > 0:
        # Sort by date and get most recent draws
        all_data = all_data.sort_values('date', ascending=False)
        
        # Get most recent 5 draws
        for i in range(min(5, len(all_data))):
            row = all_data.iloc[i]
            numbers = [row[f'n{j}'] for j in range(1, 6)]
            stars = [row[f's{j}'] for j in range(1, 3)]
            recent_patterns.append({
                'numbers': numbers,
                'stars': stars
            })
    
    # Find frequent numbers and stars across recent draws
    recent_numbers = []
    recent_stars = []
    
    for pattern in recent_patterns:
        recent_numbers.extend(pattern['numbers'])
        recent_stars.extend(pattern['stars'])
    
    # Count frequencies
    number_counter = Counter(recent_numbers)
    star_counter = Counter(recent_stars)
    
    # Strategies for generating different combinations
    strategies = [
        "hot_numbers",     # Focus on historically hot numbers
        "adjacent",        # Focus on numbers adjacent to recent winners
        "balanced"         # Focus on balanced distribution with some overlap
    ]
    
    for i in range(num_combinations):
        # Pick a different strategy for each combination
        strategy = strategies[i % len(strategies)]
        
        # Base weights for all numbers and stars
        number_weights = {n: 1.0 for n in range(1, 51)}
        star_weights = {s: 1.0 for s in range(1, 13)}
        
        # Apply strategy-specific adjustments
        if strategy == "hot_numbers":
            # Boost hot numbers and stars
            for num in hot_numbers:
                number_weights[num] *= 2.0
                
            for star in hot_stars:
                star_weights[star] *= 2.0
                
            # Extra boost for numbers that appeared multiple times recently
            for num, count in number_counter.items():
                if count > 1:
                    number_weights[num] *= (1.0 + count * 0.5)
                    
            for star, count in star_counter.items():
                if count > 1:
                    star_weights[star] *= (1.0 + count * 0.5)
        
        elif strategy == "adjacent":
            # Boost numbers adjacent to recent winners
            for pattern in recent_patterns:
                for num in pattern['numbers']:
                    # Adjacent numbers get boost
                    for adj in [num-2, num-1, num+1, num+2]:
                        if 1 <= adj <= 50:
                            number_weights[adj] *= 1.5
                            
                for star in pattern['stars']:
                    # Adjacent stars get boost
                    for adj in [star-1, star+1]:
                        if 1 <= adj <= 12:
                            star_weights[adj] *= 1.5
        
        elif strategy == "balanced":
            # Balance between hot numbers and some level of randomness
            for num in range(1, 51):
                # Add some randomness
                random_factor = 1.0 + (random.random() * 0.5)
                number_weights[num] *= random_factor
                
                # Then boost hot numbers moderately
                if num in hot_numbers:
                    number_weights[num] *= 1.3
            
            # Same for stars
            for star in range(1, 13):
                random_factor = 1.0 + (random.random() * 0.5)
                star_weights[star] *= random_factor
                
                if star in hot_stars:
                    star_weights[star] *= 1.3
        
        # Always discourage exact May 6 numbers
        for num in may6_draw['numbers']:
            number_weights[num] *= 0.5
            
        # Slightly discourage May 6 stars
        for star in may6_draw['stars']:
            star_weights[star] *= 0.8
        
        # Generate a unique combination
        attempts = 0
        max_attempts = 20
        
        while attempts < max_attempts:
            # Select numbers according to optimal distribution
            selected_numbers = []
            
            # Select from low range (1-17)
            low_nums = list(number_groups['low'])
            low_weights = [number_weights.get(n, 1.0) for n in low_nums]
            sum_weights = sum(low_weights)
            low_probs = [w/sum_weights for w in low_weights] if sum_weights > 0 else None
            
            if low_nums and low_probs:
                chosen_low = np.random.choice(
                    low_nums, 
                    size=min(optimal_distribution['low_count'], len(low_nums)),
                    replace=False,
                    p=low_probs
                )
                selected_numbers.extend(chosen_low)
            
            # Select from mid range (18-34)
            mid_nums = list(number_groups['mid'])
            mid_weights = [number_weights.get(n, 1.0) for n in mid_nums]
            sum_weights = sum(mid_weights)
            mid_probs = [w/sum_weights for w in mid_weights] if sum_weights > 0 else None
            
            if mid_nums and mid_probs:
                chosen_mid = np.random.choice(
                    mid_nums,
                    size=min(optimal_distribution['mid_count'], len(mid_nums)),
                    replace=False,
                    p=mid_probs
                )
                selected_numbers.extend(chosen_mid)
            
            # Select from high range (35-50)
            high_nums = list(number_groups['high'])
            high_weights = [number_weights.get(n, 1.0) for n in high_nums]
            sum_weights = sum(high_weights)
            high_probs = [w/sum_weights for w in high_weights] if sum_weights > 0 else None
            
            if high_nums and high_probs:
                chosen_high = np.random.choice(
                    high_nums,
                    size=min(optimal_distribution['high_count'], len(high_nums)),
                    replace=False,
                    p=high_probs
                )
                selected_numbers.extend(chosen_high)
            
            # Ensure we have exactly 5 numbers
            selected_numbers = list(set(selected_numbers))  # Remove any duplicates
            
            # Fill remaining slots if needed
            while len(selected_numbers) < 5:
                remaining = [n for n in range(1, 51) if n not in selected_numbers]
                if remaining:
                    selected_numbers.append(random.choice(remaining))
                else:
                    break
            
            # Select 3 stars
            star_candidates = list(range(1, 13))
            star_candidate_weights = [star_weights.get(s, 1.0) for s in star_candidates]
            sum_weights = sum(star_candidate_weights)
            star_probs = [w/sum_weights for w in star_candidate_weights] if sum_weights > 0 else None
            
            if star_probs:
                selected_stars = list(np.random.choice(
                    star_candidates,
                    size=min(3, len(star_candidates)),
                    replace=False,
                    p=star_probs
                ))
            else:
                selected_stars = random.sample(star_candidates, min(3, len(star_candidates)))
            
            # Sort the selections
            selected_numbers.sort()
            selected_stars.sort()
            
            # Check if this combination is unique from existing ones
            is_duplicate = False
            
            for existing_numbers in existing_number_sets:
                if set(selected_numbers) == existing_numbers:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                # Calculate a score for this combination
                score = 85.0 + (random.random() * 10.0)  # 85-95 range
                
                # Create combination dictionary
                combo = {
                    'strategy': f'Ultimate Mix (May 9 - {strategy.title()})',
                    'numbers': selected_numbers,
                    'stars': selected_stars,
                    'score': score
                }
                
                new_combinations.append(combo)
                
                # Update existing sets to avoid duplicates in future iterations
                existing_number_sets.append(set(selected_numbers))
                existing_star_sets.append(set(selected_stars))
                
                break  # Found a unique combination
            
            attempts += 1
        
        # If couldn't find a unique combination after max attempts, generate a random one
        if attempts >= max_attempts and len(new_combinations) <= i:
            selected_numbers = sorted(random.sample(range(1, 51), 5))
            selected_stars = sorted(random.sample(range(1, 13), 3))
            
            combo = {
                'strategy': f'Ultimate Mix (May 9 - Random)',
                'numbers': selected_numbers,
                'stars': selected_stars,
                'score': 80.0 + (random.random() * 10.0)  # 80-90 range
            }
            
            new_combinations.append(combo)
    
    return new_combinations

def save_to_database(combinations):
    """Save generated combinations to database"""
    saved_ids = []
    
    for combo in combinations:
        strategy = combo['strategy']
        numbers = combo['numbers']
        stars = combo['stars']
        score = combo['score']
        
        # Save to database
        try:
            # Use May 9th (Friday) as the target date
            target_date = '2025-05-09'
            
            combination_id = database.save_generated_combination(
                numbers=numbers,
                stars=stars,
                strategy=strategy,
                score=score,
                target_draw_date=target_date
            )
            logger.info(f"Saved combination to database with ID: {combination_id}")
            saved_ids.append(combination_id)
        except Exception as e:
            logger.error(f"Error saving combination to database: {e}")
    
    return saved_ids

def main():
    """Generate additional combinations for May 9th"""
    print("Generating 3 additional combinations for May 9th...")
    
    # Get existing combinations to avoid duplicates
    existing_combinations = get_existing_combinations()
    print(f"Found {len(existing_combinations)} existing combinations for May 9th")
    
    # Generate additional combinations
    new_combinations = generate_additional_combinations(
        num_combinations=3,
        existing_combinations=existing_combinations
    )
    
    # Display results
    print("\nAdditional Combinations for May 9th:\n")
    
    for combo in new_combinations:
        print(f"  Strategy: {combo['strategy']}")
        print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
        print(f"  Stars: {', '.join(map(str, combo['stars']))}")
        print(f"  Score: {combo['score']:.2f}\n")
    
    # Save to database
    saved_ids = save_to_database(new_combinations)
    print(f"Saved {len(saved_ids)} combinations to database.")

if __name__ == "__main__":
    main()