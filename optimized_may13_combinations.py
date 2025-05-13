"""
Generate 10 optimized combinations for the next Euromillions drawing
using insights from our strategy performance analysis.

This script focuses on creating combinations using Risk-Reward Balancing,
Overdue Numbers, and a blend of other top-performing strategies.
"""

import logging
import random
import numpy as np
from collections import Counter
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The last drawing results (May 13, 2025)
LAST_DRAWING = {
    "numbers": [9, 19, 44, 47, 50],
    "stars": [2, 9],
    "date": datetime.date(2025, 5, 13)
}

# Next drawing date (typically Friday after Tuesday drawing)
NEXT_DRAWING_DATE = datetime.date(2025, 5, 16) 

class CombinationGenerator:
    """Generate optimized combinations using multiple strategies"""
    
    def __init__(self):
        """Initialize the combination generator with strategy weights"""
        # Define numbers that are considered "hot" (appear frequently)
        self.hot_numbers = [3, 7, 9, 15, 19, 20, 23, 27, 37, 42, 44]
        
        # Define numbers that are considered "cold" (appear less frequently)
        self.cold_numbers = [1, 6, 11, 13, 33, 39, 43, 47, 49, 50]
        
        # Define overdue numbers (haven't appeared for a while)
        # Note: This would typically be updated based on newest draws
        self.overdue_numbers = [8, 12, 17, 24, 28, 31, 38, 45, 46, 48]
        
        # Recent numbers (appeared in last 2-3 drawings)
        self.recent_numbers = [9, 19, 44, 47, 50]
        
        # Star categories
        self.hot_stars = [2, 3, 5, 8, 9]
        self.cold_stars = [1, 4, 6, 7, 10, 11]
        self.recent_stars = [2, 9]
        
        # Numbers likely to appear together based on patterns
        self.pattern_groups = [
            [3, 9, 19, 27, 44],  # Frequent group
            [5, 17, 23, 32, 42],  # Middle frequency
            [1, 15, 28, 37, 46],  # Lower frequency
            [7, 20, 33, 38, 49],  # Mixed frequency
            [8, 16, 24, 36, 50]   # Mixed with high/low
        ]
        
        # Stars likely to appear together
        self.star_pairs = [(2, 5), (3, 9), (1, 8), (4, 11), (6, 10), (7, 12), (2, 8)]
        
        # Strategy weights (based on our analysis)
        self.strategy_weights = {
            "risk_reward": 0.30,    # Best performing
            "overdue": 0.25,        # Second best
            "frequency": 0.20,      # Third best
            "wheel": 0.15,          # Fourth best
            "hot_cold": 0.10        # Fifth best
        }
    
    def risk_reward_strategy(self, risk_level=0.5):
        """
        Generate a combination using the risk-reward balancing strategy
        
        Args:
            risk_level: 0-1 representing safety vs. reward
                (0 = all safe numbers, 1 = all risky numbers)
                
        Returns:
            dict: Combination with numbers and stars
        """
        # Define safe numbers (based on frequency analysis)
        safe_numbers = [3, 7, 9, 15, 19, 20, 23]
        safe_stars = [2, 3, 5, 8]
        
        # Define risky numbers (overdue or less frequent)
        risky_numbers = [12, 17, 28, 31, 38, 44, 45, 47, 50]
        risky_stars = [1, 6, 9, 11]
        
        # Calculate number of safe vs. risky numbers to include
        safe_count = int(5 * (1 - risk_level))
        risky_count = 5 - safe_count
        
        # Select numbers
        numbers = []
        if safe_count > 0:
            numbers.extend(random.sample(safe_numbers, min(safe_count, len(safe_numbers))))
        if risky_count > 0:
            numbers.extend(random.sample(risky_numbers, min(risky_count, len(risky_numbers))))
        
        # If we don't have 5 numbers (unlikely), fill with other numbers
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
    
    def overdue_numbers_strategy(self):
        """
        Generate a combination focusing on overdue numbers
        
        Returns:
            dict: Combination with numbers and stars
        """
        # Mix of overdue and regular numbers
        overdue_count = random.randint(2, 4)  # 2-4 overdue numbers
        regular_count = 5 - overdue_count
        
        # Select overdue numbers
        numbers = random.sample(self.overdue_numbers, min(overdue_count, len(self.overdue_numbers)))
        
        # Add some regular numbers (mix of hot and cold)
        regular_pool = list(set(self.hot_numbers + self.cold_numbers) - set(numbers))
        numbers.extend(random.sample(regular_pool, min(regular_count, len(regular_pool))))
        
        # If we still don't have 5 numbers, add random ones
        while len(numbers) < 5:
            additional = random.randint(1, 50)
            if additional not in numbers:
                numbers.append(additional)
        
        # For stars, include at least one overdue star
        overdue_stars = [star for star in range(1, 13) if star not in self.recent_stars]
        stars = [random.choice(overdue_stars)]
        
        # Add one more star (either hot or from a different category)
        second_star_candidates = [s for s in range(1, 13) if s not in stars]
        stars.append(random.choice(second_star_candidates))
        
        return {
            "numbers": sorted(numbers),
            "stars": sorted(stars),
            "strategy": "Overdue Numbers"
        }
    
    def frequency_analysis_strategy(self):
        """
        Generate a combination based on frequency analysis
        
        Returns:
            dict: Combination with numbers and stars
        """
        # Select mainly hot numbers with a few cold ones
        hot_count = random.randint(3, 4)  # 3-4 hot numbers
        cold_count = 5 - hot_count
        
        numbers = random.sample(self.hot_numbers, min(hot_count, len(self.hot_numbers)))
        numbers.extend(random.sample(self.cold_numbers, min(cold_count, len(self.cold_numbers))))
        
        # If we don't have 5 numbers, fill with random ones
        while len(numbers) < 5:
            additional = random.randint(1, 50)
            if additional not in numbers:
                numbers.append(additional)
        
        # Select stars with higher frequency
        stars = random.sample(self.hot_stars, min(2, len(self.hot_stars)))
        
        # If we don't have 2 stars, add another
        if len(stars) < 2:
            additional_star_candidates = [s for s in range(1, 13) if s not in stars]
            stars.append(random.choice(additional_star_candidates))
        
        return {
            "numbers": sorted(numbers),
            "stars": sorted(stars),
            "strategy": "Frequency Analysis"
        }
    
    def wheel_system_strategy(self):
        """
        Generate a combination using a wheel system approach
        
        Returns:
            dict: Combination with numbers and stars
        """
        # Core numbers to include (mix of hot and a few overdue)
        core_numbers = [9, 15, 19, 27, 44]  # Based on frequency and recent success
        core_stars = [2, 3, 5, 9]  # Hot/successful stars
        
        # How many core numbers to use
        core_count = random.randint(2, 4)
        additional_count = 5 - core_count
        
        # Select numbers
        numbers = random.sample(core_numbers, min(core_count, len(core_numbers)))
        
        # Add additional numbers not in core
        additional_pool = [n for n in range(1, 51) if n not in numbers]
        numbers.extend(random.sample(additional_pool, additional_count))
        
        # Select stars - at least one core star
        stars = [random.choice(core_stars)]
        additional_star_candidates = [s for s in range(1, 13) if s not in stars]
        stars.append(random.choice(additional_star_candidates))
        
        return {
            "numbers": sorted(numbers),
            "stars": sorted(stars),
            "strategy": "Wheel System"
        }
    
    def hot_cold_strategy(self):
        """
        Generate a combination using hot-cold approach
        
        Returns:
            dict: Combination with numbers and stars
        """
        # Mix of hot and cold numbers
        hot_count = 3  # Fixed 3 hot, 2 cold
        cold_count = 2
        
        numbers = random.sample(self.hot_numbers, min(hot_count, len(self.hot_numbers)))
        numbers.extend(random.sample(self.cold_numbers, min(cold_count, len(self.cold_numbers))))
        
        # If we don't have 5 numbers, fill with random ones
        while len(numbers) < 5:
            additional = random.randint(1, 50)
            if additional not in numbers:
                numbers.append(additional)
        
        # One hot, one cold star
        stars = [random.choice(self.hot_stars), random.choice(self.cold_stars)]
        
        return {
            "numbers": sorted(numbers),
            "stars": sorted(stars),
            "strategy": "Hot-Cold"
        }
    
    def _strategy_blended_combination(self):
        """
        Generate a combination using a weighted blend of strategies
        
        Returns:
            dict: Combination with numbers and stars
        """
        # Choose a strategy based on weights
        strategies = list(self.strategy_weights.keys())
        weights = list(self.strategy_weights.values())
        
        chosen_strategy = random.choices(strategies, weights=weights)[0]
        
        if chosen_strategy == "risk_reward":
            risk_level = random.uniform(0.3, 0.8)  # Favor medium to high risk
            return self.risk_reward_strategy(risk_level)
        elif chosen_strategy == "overdue":
            return self.overdue_numbers_strategy()
        elif chosen_strategy == "frequency":
            return self.frequency_analysis_strategy()
        elif chosen_strategy == "wheel":
            return self.wheel_system_strategy()
        else:  # hot_cold
            return self.hot_cold_strategy()
    
    def _check_balance(self, numbers):
        """
        Check if the numbers are well-balanced across ranges
        
        Args:
            numbers: List of 5 numbers
            
        Returns:
            bool: True if balanced, False otherwise
        """
        # Count numbers in each decade
        ranges = [
            (1, 10),
            (11, 20),
            (21, 30),
            (31, 40),
            (41, 50)
        ]
        
        counts = [0] * len(ranges)
        for num in numbers:
            for i, (low, high) in enumerate(ranges):
                if low <= num <= high:
                    counts[i] += 1
                    break
        
        # A balanced ticket should have numbers from at least 3 different ranges
        different_ranges = sum(1 for c in counts if c > 0)
        return different_ranges >= 3
    
    def _check_sum(self, numbers):
        """
        Check if the sum of numbers is within a good range
        
        Args:
            numbers: List of 5 numbers
            
        Returns:
            bool: True if the sum is in a good range, False otherwise
        """
        # Sum of the five numbers
        total = sum(numbers)
        
        # Based on historical data, most winning combinations have 
        # sums between 95 and 160
        return 95 <= total <= 160
    
    def _check_distribution(self, numbers):
        """
        Check if there's a good distribution of odd/even and low/high numbers
        
        Args:
            numbers: List of 5 numbers
            
        Returns:
            bool: True if well distributed, False otherwise
        """
        # Count odd and even numbers
        odd_count = sum(1 for n in numbers if n % 2 == 1)
        even_count = 5 - odd_count
        
        # Count low (1-25) and high (26-50) numbers
        low_count = sum(1 for n in numbers if 1 <= n <= 25)
        high_count = 5 - low_count
        
        # Good distribution typically avoids extremes (all odd/even or all low/high)
        return 1 <= odd_count <= 4 and 1 <= low_count <= 4
    
    def _check_pattern(self, numbers):
        """
        Check for common patterns to avoid
        
        Args:
            numbers: List of 5 numbers
            
        Returns:
            bool: True if no bad patterns, False otherwise
        """
        # Check for consecutive numbers (more than 2 is unusual)
        consecutive_count = 0
        for i in range(len(numbers) - 1):
            if numbers[i+1] == numbers[i] + 1:
                consecutive_count += 1
        
        # Check for numbers all in same decade (e.g., all in 30s)
        same_decade = False
        for decade_start in range(1, 50, 10):
            decade_end = decade_start + 9
            if all(decade_start <= n <= decade_end for n in numbers):
                same_decade = True
                break
        
        # Check for arithmetic sequences (e.g., 5, 10, 15, 20, 25)
        is_arithmetic = False
        if len(numbers) >= 3:
            for i in range(len(numbers) - 2):
                if numbers[i+1] - numbers[i] == numbers[i+2] - numbers[i+1]:
                    is_arithmetic = True
                    break
        
        return consecutive_count <= 2 and not same_decade and not is_arithmetic
    
    def _validate_combination(self, combination):
        """
        Validate a combination against various quality checks
        
        Args:
            combination: Dict with numbers and stars
            
        Returns:
            bool: True if the combination passes all checks
        """
        numbers = combination["numbers"]
        
        balance_check = self._check_balance(numbers)
        sum_check = self._check_sum(numbers)
        distribution_check = self._check_distribution(numbers)
        pattern_check = self._check_pattern(numbers)
        
        # Pass if it meets at least 3 of the 4 criteria
        checks_passed = sum([balance_check, sum_check, distribution_check, pattern_check])
        return checks_passed >= 3
    
    def _is_duplicate(self, new_combo, existing_combos):
        """
        Check if the new combination is too similar to existing ones
        
        Args:
            new_combo: New combination dict
            existing_combos: List of existing combination dicts
            
        Returns:
            bool: True if the new combo is a duplicate, False otherwise
        """
        new_numbers = set(new_combo["numbers"])
        new_stars = set(new_combo["stars"])
        
        for combo in existing_combos:
            existing_numbers = set(combo["numbers"])
            existing_stars = set(combo["stars"])
            
            # Consider it a duplicate if 4+ numbers match and both stars match
            numbers_match = len(new_numbers.intersection(existing_numbers))
            stars_match = len(new_stars.intersection(existing_stars))
            
            if numbers_match >= 4 and stars_match >= 2:
                return True
            
            # Also consider it a duplicate if all 5 numbers match regardless of stars
            if numbers_match == 5:
                return True
        
        return False
    
    def generate_combinations(self, count=10):
        """
        Generate a specified number of optimized combinations
        
        Args:
            count: Number of combinations to generate
            
        Returns:
            list: List of combination dictionaries
        """
        combinations = []
        
        # Risk-Reward combinations with varying risk levels
        risk_levels = [0.2, 0.4, 0.6, 0.8]
        for risk in risk_levels:
            combo = self.risk_reward_strategy(risk)
            if self._validate_combination(combo) and not self._is_duplicate(combo, combinations):
                combinations.append(combo)
        
        # Generate at least one of each core strategy
        strategies = [
            self.overdue_numbers_strategy,
            self.frequency_analysis_strategy,
            self.wheel_system_strategy,
            self.hot_cold_strategy
        ]
        
        for strategy_func in strategies:
            combo = strategy_func()
            if self._validate_combination(combo) and not self._is_duplicate(combo, combinations):
                combinations.append(combo)
        
        # Fill remaining slots with blended approaches
        while len(combinations) < count:
            combo = self._strategy_blended_combination()
            if self._validate_combination(combo) and not self._is_duplicate(combo, combinations):
                combinations.append(combo)
        
        # Ensure we have exactly the requested number
        while len(combinations) > count:
            combinations.pop()
        
        return combinations

def display_combinations(combinations):
    """Display the generated combinations with details"""
    logger.info(f"\n===== OPTIMIZED COMBINATIONS FOR {NEXT_DRAWING_DATE} =====")
    
    for i, combo in enumerate(combinations):
        strategy = combo.get("strategy", "Blended")
        risk_level = combo.get("risk_level", "N/A")
        
        logger.info(f"Combination {i+1}: {strategy}")
        if strategy == "Risk-Reward":
            logger.info(f"  Risk Level: {risk_level:.2f}")
        
        logger.info(f"  Numbers: {', '.join(map(str, combo['numbers']))}")
        logger.info(f"  Stars: {', '.join(map(str, combo['stars']))}")
        
        # Calculate sum and distribution stats
        sum_numbers = sum(combo['numbers'])
        odd_count = sum(1 for n in combo['numbers'] if n % 2 == 1)
        even_count = 5 - odd_count
        low_count = sum(1 for n in combo['numbers'] if 1 <= n <= 25)
        high_count = 5 - low_count
        
        logger.info(f"  Sum: {sum_numbers}")
        logger.info(f"  Distribution: {odd_count} odd / {even_count} even, {low_count} low / {high_count} high")
        logger.info("")

def main():
    """Generate and display optimized combinations"""
    logger.info("Generating optimized combinations for the next Euromillions drawing...")
    
    # Set random seed for reproducibility
    random.seed(20250516)  # Next drawing date as seed
    
    generator = CombinationGenerator()
    combinations = generator.generate_combinations(10)
    
    display_combinations(combinations)
    
    logger.info("Generated 10 optimized combinations using top-performing strategies")
    logger.info("These combinations are optimized based on our analysis of the May 13, 2025 results")

if __name__ == "__main__":
    main()