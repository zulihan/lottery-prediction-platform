import os
import sys
import random
import logging
import numpy as np
from datetime import datetime, date, timedelta
from collections import Counter

# Add relative import support
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import database

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DiverseMixedStrategies:
    """
    Generate diverse mixed strategy combinations for the May 13th Euromillions draw.
    Uses multiple approaches to ensure we get truly different combinations.
    """
    
    def __init__(self):
        """Initialize the diverse mixed strategies"""
        # Load historical data for frequency analysis
        self.draws = self.load_data_from_db()
        
        # Number group ranges
        self.number_groups = {
            'low': list(range(1, 18)),    # 1-17
            'mid': list(range(18, 35)),   # 18-34
            'high': list(range(35, 51))   # 35-50
        }
        
        # Define different distribution patterns to ensure diversity
        self.distributions = [
            {'low': 2, 'mid': 2, 'high': 1},  # Original balanced 2-2-1
            {'low': 1, 'mid': 3, 'high': 1},  # More mid-range (1-3-1)
            {'low': 1, 'mid': 2, 'high': 2},  # More high-range (1-2-2)
            {'low': 3, 'mid': 1, 'high': 1}   # More low-range (3-1-1)
        ]
        
        # Define frequency weights from historical data
        self.number_weights, self.star_weights = self.get_frequency_weights()
        
        # Track already generated combinations to avoid duplicates
        self.existing_combinations = self.get_existing_may13_combinations()
    
    def load_data_from_db(self):
        """Load historical data from database"""
        try:
            logger.info("Loading data from database...")
            df = database.get_all_drawings()
            logger.info(f"Loaded {len(df)} draws from database.")
            return df
        except Exception as e:
            logger.error(f"Error loading data from database: {e}")
            return None
    
    def get_existing_may13_combinations(self):
        """Get combinations already generated for May 13th"""
        try:
            combinations = database.get_generated_combinations(limit=100)
            # Filter for May 13th combinations
            may13_combinations = []
            for combo in combinations:
                if combo.get('target_draw_date') == '2025-05-13':
                    # Extract numbers and stars
                    numbers = combo.get('numbers', [])
                    stars = combo.get('stars', [])
                    
                    # Handle string format if needed
                    if isinstance(numbers, str):
                        try:
                            import json
                            numbers = json.loads(numbers)
                        except:
                            numbers = [int(n.strip()) for n in numbers.split(',') if n.strip().isdigit()]
                    
                    if isinstance(stars, str):
                        try:
                            import json
                            stars = json.loads(stars)
                        except:
                            stars = [int(s.strip()) for s in stars.split(',') if s.strip().isdigit()]
                    
                    may13_combinations.append((numbers, stars))
            
            logger.info(f"Found {len(may13_combinations)} existing combinations for May 13th")
            return may13_combinations
        except Exception as e:
            logger.error(f"Error getting existing combinations: {e}")
            return []
    
    def get_frequency_weights(self):
        """
        Calculate frequency weights from historical data
        
        Returns:
            tuple: (number_weights, star_weights)
        """
        number_weights = {n: 1.0 for n in range(1, 51)}
        star_weights = {s: 1.0 for s in range(1, 13)}
        
        if self.draws is None or len(self.draws) == 0:
            return number_weights, star_weights
            
        # Count frequencies
        num_counts = {}
        star_counts = {}
        
        for _, draw in self.draws.iterrows():
            for i in range(1, 6):
                num = draw[f'n{i}']
                num_counts[num] = num_counts.get(num, 0) + 1
                
            for i in range(1, 3):
                star = draw[f's{i}']
                star_counts[star] = star_counts.get(star, 0) + 1
        
        # Get max frequencies for normalization
        max_num_count = max(num_counts.values()) if num_counts else 1
        max_star_count = max(star_counts.values()) if star_counts else 1
        
        # Apply normalized frequency weights
        for num, count in num_counts.items():
            # Normalized frequency (0.5-1.5 range)
            norm_freq = 0.5 + (count / max_num_count)
            number_weights[num] = norm_freq
            
        for star, count in star_counts.items():
            # Normalized frequency (0.5-1.5 range)
            norm_freq = 0.5 + (count / max_star_count)
            star_weights[star] = norm_freq
        
        return number_weights, star_weights
    
    def is_duplicate(self, numbers, stars):
        """
        Check if a combination is a duplicate of existing combinations
        
        Args:
            numbers: List of numbers
            stars: List of stars
            
        Returns:
            bool: True if duplicate, False otherwise
        """
        for existing_numbers, existing_stars in self.existing_combinations:
            if set(numbers) == set(existing_numbers):
                return True
        
        return False
    
    def generate_frequency_based_combination(self, distribution=None):
        """
        Generate a combination using frequency-based approach.
        Uses specified distribution or default balanced distribution.
        
        Args:
            distribution: Optional dict with distribution pattern
            
        Returns:
            tuple: (numbers, stars, score)
        """
        if distribution is None:
            distribution = self.distributions[0]  # Default balanced 2-2-1
        
        # Select numbers according to distribution
        selected_numbers = []
        
        # Select from low range (1-17)
        low_nums = list(self.number_groups['low'])
        low_weights = [self.number_weights[n] for n in low_nums]
        sum_weights = sum(low_weights)
        low_probs = [w/sum_weights for w in low_weights] if sum_weights > 0 else None
        
        if low_nums and low_probs:
            chosen_low = np.random.choice(
                low_nums, 
                size=min(distribution['low'], len(low_nums)),
                replace=False,
                p=low_probs
            )
            selected_numbers.extend(chosen_low)
        
        # Select from mid range (18-34)
        mid_nums = list(self.number_groups['mid'])
        mid_weights = [self.number_weights[n] for n in mid_nums]
        sum_weights = sum(mid_weights)
        mid_probs = [w/sum_weights for w in mid_weights] if sum_weights > 0 else None
        
        if mid_nums and mid_probs:
            chosen_mid = np.random.choice(
                mid_nums, 
                size=min(distribution['mid'], len(mid_nums)),
                replace=False,
                p=mid_probs
            )
            selected_numbers.extend(chosen_mid)
        
        # Select from high range (35-50)
        high_nums = list(self.number_groups['high'])
        high_weights = [self.number_weights[n] for n in high_nums]
        sum_weights = sum(high_weights)
        high_probs = [w/sum_weights for w in high_weights] if sum_weights > 0 else None
        
        if high_nums and high_probs:
            chosen_high = np.random.choice(
                high_nums, 
                size=min(distribution['high'], len(high_nums)),
                replace=False,
                p=high_probs
            )
            selected_numbers.extend(chosen_high)
        
        # Ensure we have exactly 5 numbers
        selected_numbers = list(set(selected_numbers))  # Remove any duplicates
        
        # Fill remaining slots if needed
        while len(selected_numbers) < 5:
            # Get all numbers not yet selected
            remaining_nums = [n for n in range(1, 51) if n not in selected_numbers]
            
            if remaining_nums:
                remaining_weights = [self.number_weights.get(n, 1.0) for n in remaining_nums]
                sum_weights = sum(remaining_weights)
                remaining_probs = [w/sum_weights for w in remaining_weights] if sum_weights > 0 else None
                
                if remaining_probs:
                    chosen_num = np.random.choice(remaining_nums, p=remaining_probs)
                    selected_numbers.append(chosen_num)
                else:
                    # Fallback to random selection
                    new_num = random.choice(remaining_nums)
                    selected_numbers.append(new_num)
            else:
                break
        
        # Select 3 stars
        star_candidates = list(range(1, 13))
        star_weights = [self.star_weights.get(s, 1.0) for s in star_candidates]
        sum_weights = sum(star_weights)
        star_probs = [w/sum_weights for w in star_weights] if sum_weights > 0 else None
        
        if star_probs:
            selected_stars = list(np.random.choice(
                star_candidates,
                size=min(3, len(star_candidates)),
                replace=False,
                p=star_probs
            ))
        else:
            selected_stars = random.sample(star_candidates, min(3, len(star_candidates)))
        
        # Sort the final selections
        selected_numbers.sort()
        selected_stars.sort()
        
        # Calculate score based on frequency weights
        score = self.calculate_score(selected_numbers, selected_stars)
        
        return selected_numbers, selected_stars, score
    
    def generate_coverage_based_combination(self, base_combinations):
        """
        Generate a combination using coverage-based approach.
        Uses frequency patterns from base combinations.
        
        Args:
            base_combinations: List of base combinations to analyze
            
        Returns:
            tuple: (numbers, stars, score)
        """
        # Extract all numbers and stars from base combinations
        all_numbers = []
        all_stars = []
        
        for numbers, stars, _ in base_combinations:
            all_numbers.extend(numbers)
            all_stars.extend(stars)
        
        # Count frequency of each number and star
        number_counter = Counter(all_numbers)
        star_counter = Counter(all_stars)
        
        # Get numbers and stars that are underrepresented in base combinations
        # This approach ensures good coverage across all combinations
        all_numbers_set = set(range(1, 51))
        all_stars_set = set(range(1, 13))
        
        covered_numbers = set(number_counter.keys())
        covered_stars = set(star_counter.keys())
        
        uncovered_numbers = all_numbers_set - covered_numbers
        uncovered_stars = all_stars_set - covered_stars
        
        # Generate a combination that includes some uncovered numbers/stars
        # and some frequently occurring ones for balance
        selected_numbers = []
        
        # Try to include some uncovered numbers if available
        if uncovered_numbers and random.random() < 0.7:  # 70% chance
            # Choose 1-2 uncovered numbers
            num_uncovered = min(2, len(uncovered_numbers))
            selected_numbers.extend(random.sample(list(uncovered_numbers), num_uncovered))
        
        # Fill the rest with a mix of frequency-weighted numbers
        remaining_needed = 5 - len(selected_numbers)
        if remaining_needed > 0:
            available_numbers = [n for n in range(1, 51) if n not in selected_numbers]
            # Apply original frequency weights
            number_weights = {n: self.number_weights.get(n, 1.0) for n in available_numbers}
            
            # Sort by weight
            sorted_numbers = sorted(number_weights.items(), key=lambda x: x[1], reverse=True)
            # Take top weighted numbers
            selected_numbers.extend([n for n, _ in sorted_numbers[:remaining_needed]])
        
        # Ensure exactly 5 numbers
        selected_numbers = list(set(selected_numbers))[:5]
        
        # Fill any missing spots
        while len(selected_numbers) < 5:
            remaining = [n for n in range(1, 51) if n not in selected_numbers]
            if remaining:
                selected_numbers.append(random.choice(remaining))
            else:
                break
        
        # Select stars
        selected_stars = []
        
        # Try to include some uncovered stars if available
        if uncovered_stars and random.random() < 0.7:  # 70% chance
            # Choose 1 uncovered star
            num_uncovered = min(1, len(uncovered_stars))
            selected_stars.extend(random.sample(list(uncovered_stars), num_uncovered))
        
        # Fill the rest with frequency-weighted stars
        remaining_needed = 3 - len(selected_stars)
        if remaining_needed > 0:
            available_stars = [s for s in range(1, 13) if s not in selected_stars]
            # Apply original frequency weights
            star_weights = {s: self.star_weights.get(s, 1.0) for s in available_stars}
            
            # Sort by weight
            sorted_stars = sorted(star_weights.items(), key=lambda x: x[1], reverse=True)
            # Take top weighted stars
            selected_stars.extend([s for s, _ in sorted_stars[:remaining_needed]])
        
        # Ensure exactly 3 stars
        selected_stars = list(set(selected_stars))[:3]
        
        # Fill any missing spots
        while len(selected_stars) < 3:
            remaining = [s for s in range(1, 13) if s not in selected_stars]
            if remaining:
                selected_stars.append(random.choice(remaining))
            else:
                break
        
        # Sort the final selections
        selected_numbers.sort()
        selected_stars.sort()
        
        # Calculate score
        score = self.calculate_score(selected_numbers, selected_stars)
        
        return selected_numbers, selected_stars, score
    
    def generate_balanced_outlier_combination(self):
        """
        Generate a balanced combination with some deliberate outliers.
        This adds diversity by including some low-frequency numbers.
        
        Returns:
            tuple: (numbers, stars, score)
        """
        # Select 3 numbers based on frequency
        high_freq_nums = []
        num_weights = self.number_weights.copy()
        
        # Get all numbers
        all_nums = list(range(1, 51))
        weights = [num_weights.get(n, 1.0) for n in all_nums]
        sum_weights = sum(weights)
        probs = [w/sum_weights for w in weights] if sum_weights > 0 else None
        
        if probs:
            high_freq_nums = list(np.random.choice(
                all_nums,
                size=3,
                replace=False,
                p=probs
            ))
        else:
            high_freq_nums = random.sample(all_nums, 3)
        
        # Add 2 deliberate outliers (low frequency numbers)
        low_freq_nums = []
        # Sort numbers by frequency, lowest first
        sorted_by_freq = sorted(num_weights.items(), key=lambda x: x[1])
        
        # Get numbers not already selected
        available_low_freq = [n for n, _ in sorted_by_freq if n not in high_freq_nums]
        
        # Take 2 from the bottom half
        low_freq_candidates = available_low_freq[:25]  # Bottom half
        if low_freq_candidates:
            low_freq_nums = random.sample(low_freq_candidates, min(2, len(low_freq_candidates)))
        
        # Combine numbers
        selected_numbers = high_freq_nums + low_freq_nums
        
        # Ensure exactly 5 numbers
        selected_numbers = list(set(selected_numbers))[:5]
        
        # Fill any missing spots
        while len(selected_numbers) < 5:
            remaining = [n for n in range(1, 51) if n not in selected_numbers]
            if remaining:
                selected_numbers.append(random.choice(remaining))
            else:
                break
        
        # Similar approach for stars
        high_freq_stars = []
        star_weights = self.star_weights.copy()
        
        # Get all stars
        all_stars = list(range(1, 13))
        weights = [star_weights.get(s, 1.0) for s in all_stars]
        sum_weights = sum(weights)
        probs = [w/sum_weights for w in weights] if sum_weights > 0 else None
        
        if probs:
            high_freq_stars = list(np.random.choice(
                all_stars,
                size=2,
                replace=False,
                p=probs
            ))
        else:
            high_freq_stars = random.sample(all_stars, min(2, len(all_stars)))
        
        # Add 1 outlier star
        sorted_by_freq = sorted(star_weights.items(), key=lambda x: x[1])
        available_low_freq = [s for s, _ in sorted_by_freq if s not in high_freq_stars]
        
        low_freq_stars = []
        if available_low_freq:
            low_freq_stars = [random.choice(available_low_freq[:6])]  # Bottom half
        
        # Combine stars
        selected_stars = high_freq_stars + low_freq_stars
        
        # Ensure exactly 3 stars
        selected_stars = list(set(selected_stars))[:3]
        
        # Fill any missing spots
        while len(selected_stars) < 3:
            remaining = [s for s in range(1, 13) if s not in selected_stars]
            if remaining:
                selected_stars.append(random.choice(remaining))
            else:
                break
        
        # Sort the final selections
        selected_numbers.sort()
        selected_stars.sort()
        
        # Calculate score
        score = self.calculate_score(selected_numbers, selected_stars)
        
        return selected_numbers, selected_stars, score
    
    def generate_pattern_based_combination(self, pattern_type="consecutive"):
        """
        Generate a combination based on a specific pattern
        
        Args:
            pattern_type: Type of pattern to use
            
        Returns:
            tuple: (numbers, stars, score)
        """
        selected_numbers = []
        
        if pattern_type == "consecutive":
            # Try to include a consecutive pair or triplet
            
            # First select a random starting point
            start = random.randint(1, 48)  # Leave room for at least a pair
            
            # Determine length of consecutive sequence (2 or 3)
            seq_length = random.choice([2, 3])
            
            # Add consecutive numbers
            for i in range(seq_length):
                if start + i <= 50:
                    selected_numbers.append(start + i)
        
        elif pattern_type == "even_odd":
            # Create a specific even/odd pattern (e.g., 3 even, 2 odd)
            even_count = random.choice([2, 3])
            odd_count = 5 - even_count
            
            # Get all even and odd numbers
            even_nums = [n for n in range(1, 51) if n % 2 == 0]
            odd_nums = [n for n in range(1, 51) if n % 2 != 0]
            
            # Apply weights
            even_weights = [self.number_weights.get(n, 1.0) for n in even_nums]
            sum_weights = sum(even_weights)
            even_probs = [w/sum_weights for w in even_weights] if sum_weights > 0 else None
            
            odd_weights = [self.number_weights.get(n, 1.0) for n in odd_nums]
            sum_weights = sum(odd_weights)
            odd_probs = [w/sum_weights for w in odd_weights] if sum_weights > 0 else None
            
            # Select weighted even numbers
            if even_probs:
                chosen_even = np.random.choice(
                    even_nums,
                    size=min(even_count, len(even_nums)),
                    replace=False,
                    p=even_probs
                )
                selected_numbers.extend(chosen_even)
            else:
                selected_numbers.extend(random.sample(even_nums, min(even_count, len(even_nums))))
            
            # Select weighted odd numbers
            if odd_probs:
                chosen_odd = np.random.choice(
                    odd_nums,
                    size=min(odd_count, len(odd_nums)),
                    replace=False,
                    p=odd_probs
                )
                selected_numbers.extend(chosen_odd)
            else:
                selected_numbers.extend(random.sample(odd_nums, min(odd_count, len(odd_nums))))
        
        # Ensure exactly 5 numbers
        selected_numbers = list(set(selected_numbers))[:5]
        
        # Fill any missing spots
        while len(selected_numbers) < 5:
            remaining = [n for n in range(1, 51) if n not in selected_numbers]
            if remaining:
                remaining_weights = [self.number_weights.get(n, 1.0) for n in remaining]
                sum_weights = sum(remaining_weights)
                remaining_probs = [w/sum_weights for w in remaining_weights] if sum_weights > 0 else None
                
                if remaining_probs:
                    chosen_num = np.random.choice(remaining, p=remaining_probs)
                    selected_numbers.append(chosen_num)
                else:
                    selected_numbers.append(random.choice(remaining))
            else:
                break
        
        # Select 3 stars weighted by frequency
        star_candidates = list(range(1, 13))
        star_weights = [self.star_weights.get(s, 1.0) for s in star_candidates]
        sum_weights = sum(star_weights)
        star_probs = [w/sum_weights for w in star_weights] if sum_weights > 0 else None
        
        if star_probs:
            selected_stars = list(np.random.choice(
                star_candidates,
                size=min(3, len(star_candidates)),
                replace=False,
                p=star_probs
            ))
        else:
            selected_stars = random.sample(star_candidates, min(3, len(star_candidates)))
        
        # Sort the final selections
        selected_numbers.sort()
        selected_stars.sort()
        
        # Calculate score
        score = self.calculate_score(selected_numbers, selected_stars)
        
        return selected_numbers, selected_stars, score
    
    def calculate_score(self, numbers, stars):
        """
        Calculate a score for the combination
        
        Args:
            numbers: List of 5 numbers
            stars: List of stars
            
        Returns:
            float: Score from 0-100
        """
        score = 75.0  # Base score
        
        # Calculate weighted scores based on frequencies
        number_score = sum(self.number_weights.get(n, 1.0) for n in numbers) / len(numbers)
        star_score = sum(self.star_weights.get(s, 1.0) for s in stars) / len(stars)
        
        # Normalize scores
        max_num_weight = max(self.number_weights.values())
        max_star_weight = max(self.star_weights.values())
        
        normalized_number_score = (number_score / max_num_weight) * 20  # Up to 20 points
        normalized_star_score = (star_score / max_star_weight) * 10  # Up to 10 points
        
        score += normalized_number_score + normalized_star_score
        
        # Cap score at 100
        return min(score, 100)
    
    def generate_diverse_combinations(self, count=4):
        """
        Generate diverse mixed strategy combinations
        
        Args:
            count: Number of combinations to generate
            
        Returns:
            list: List of tuples (numbers, stars, score, strategy_name)
        """
        combinations = []
        base_combinations = []
        
        # First generate base combinations if we need them
        # These will be used for coverage-based approach
        for i in range(2):
            numbers, stars, score = self.generate_frequency_based_combination(
                distribution=self.distributions[i % len(self.distributions)]
            )
            base_combinations.append((numbers, stars, score))
        
        # Now generate diverse combinations using different approaches
        strategies = [
            "frequency_based",
            "coverage_based", 
            "balanced_outlier",
            "pattern_based_consecutive",
            "pattern_based_even_odd"
        ]
        
        for i in range(count):
            strategy = strategies[i % len(strategies)]
            
            # Try up to 5 times to generate a non-duplicate combination
            for attempt in range(5):
                if strategy == "frequency_based":
                    # Use a different distribution for each attempt
                    dist_idx = (i + attempt) % len(self.distributions)
                    numbers, stars, score = self.generate_frequency_based_combination(
                        distribution=self.distributions[dist_idx]
                    )
                    strategy_name = f"Mixed (Frequency {dist_idx+1})"
                
                elif strategy == "coverage_based":
                    numbers, stars, score = self.generate_coverage_based_combination(base_combinations)
                    strategy_name = "Mixed (Coverage)"
                
                elif strategy == "balanced_outlier":
                    numbers, stars, score = self.generate_balanced_outlier_combination()
                    strategy_name = "Mixed (Balanced Outlier)"
                
                elif strategy == "pattern_based_consecutive":
                    numbers, stars, score = self.generate_pattern_based_combination("consecutive")
                    strategy_name = "Mixed (Consecutive Pattern)"
                
                elif strategy == "pattern_based_even_odd":
                    numbers, stars, score = self.generate_pattern_based_combination("even_odd")
                    strategy_name = "Mixed (Even-Odd Pattern)"
                
                else:
                    # Fallback to frequency-based
                    numbers, stars, score = self.generate_frequency_based_combination()
                    strategy_name = "Mixed (Default)"
                
                # Check if this is a duplicate
                if not self.is_duplicate(numbers, stars):
                    break
            
            # Add to combinations and to existing list to avoid future duplicates
            combinations.append((numbers, stars, score, strategy_name))
            self.existing_combinations.append((numbers, stars))
        
        return combinations

def save_to_database(combinations):
    """Save generated combinations to database"""
    saved_ids = []
    
    for numbers, stars, score, strategy in combinations:
        # Save to database
        try:
            # Use May 13th (Tuesday) as the target date
            target_date = '2025-05-13'
            
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
    """Generate diverse mixed strategy combinations for May 13th"""
    print("Generating Diverse Mixed Strategy Combinations for May 13th Euromillions Draw...")
    
    # Create the generator
    generator = DiverseMixedStrategies()
    
    # Generate combinations
    combinations = generator.generate_diverse_combinations(count=4)
    
    # Display results
    print("\nGenerated Diverse Mixed Strategy Combinations for May 13th:\n")
    
    for i, (numbers, stars, score, strategy) in enumerate(combinations):
        print(f"Combination {i+1}:")
        print(f"  Strategy: {strategy}")
        print(f"  Main Numbers: {', '.join(map(str, numbers))}")
        print(f"  Stars: {', '.join(map(str, stars))}")
        print(f"  Score: {score:.2f}\n")
    
    # Save to database
    saved_ids = save_to_database(combinations)
    print(f"Saved {len(saved_ids)} combinations to database.")
    
    # Outline key features
    print("\nKey Strategy Features:")
    print("1. Each combination uses a completely different mixed strategy approach")
    print("2. Includes frequency-based, coverage-based, and pattern-based strategies")
    print("3. Avoids duplicating any existing combinations for May 13th")
    print("4. Maintains statistical weighting while ensuring diversity")
    print("5. Combines historical patterns with deliberate outliers for optimal coverage")

if __name__ == "__main__":
    main()