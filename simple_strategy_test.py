import os
import sys
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import logging
from collections import defaultdict

# Add relative import support
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import database

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleStrategyTester:
    """
    Simple strategy tester for Euromillions prediction strategies.
    """
    
    def __init__(self, num_draws=20):
        """Initialize with historical draw data"""
        self.load_draws()
        self.num_draws = min(num_draws, len(self.draws))
        
        # Get the most recent draws for testing
        self.test_draws = self.draws.sort_values('date', ascending=False).head(self.num_draws).copy()
        
        # Strategy performance results
        self.results = {}
        
    def load_draws(self):
        """Load draw data from database"""
        logger.info("Loading draw data from database...")
        try:
            self.draws = database.get_all_drawings()
            logger.info(f"Loaded {len(self.draws)} draws from database.")
            
            # Make sure the date column is datetime
            self.draws['date'] = pd.to_datetime(self.draws['date'])
        except Exception as e:
            logger.error(f"Error loading draws: {e}")
            self.draws = pd.DataFrame(columns=['date', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2'])
    
    def get_draw_numbers(self, draw):
        """
        Extract numbers and stars from a draw
        
        Args:
            draw: Row from the DataFrame
            
        Returns:
            tuple: (numbers, stars)
        """
        numbers = [draw[f'n{i}'] for i in range(1, 6)]
        stars = [draw[f's{i}'] for i in range(1, 3)]
        return numbers, stars
    
    def test_frequency_strategy(self, test_draws, combinations_per_draw=5):
        """
        Test frequency-based strategy
        
        Args:
            test_draws: DataFrame with test draws
            combinations_per_draw: Number of combinations to generate per draw
            
        Returns:
            dict: Performance results
        """
        logger.info("Testing Frequency Strategy...")
        
        # Initialize results
        results = {
            'strategy': 'Frequency',
            'total_combinations': 0,
            'total_matched_numbers': 0,
            'total_matched_stars': 0,
            'prize_tiers': defaultdict(int),
            'details_by_draw': []
        }
        
        # Test each draw
        for _, test_draw in test_draws.iterrows():
            test_date = test_draw['date']
            test_nums, test_stars = self.get_draw_numbers(test_draw)
            
            # Get all draws before the test date for training
            training_data = self.draws[self.draws['date'] < test_date].copy()
            
            # Generate combinations using frequency analysis
            combinations = self.generate_frequency_combinations(training_data, combinations_per_draw)
            
            # Evaluate combinations
            draw_results = self.evaluate_combinations(combinations, test_nums, test_stars)
            draw_results['date'] = test_date.strftime('%Y-%m-%d')
            draw_results['actual_numbers'] = test_nums
            draw_results['actual_stars'] = test_stars
            
            # Add to overall results
            results['total_combinations'] += len(combinations)
            results['total_matched_numbers'] += draw_results['total_matched_numbers']
            results['total_matched_stars'] += draw_results['total_matched_stars']
            
            # Update prize counts
            for tier, count in draw_results['prize_tiers'].items():
                results['prize_tiers'][tier] += count
            
            # Add draw details
            results['details_by_draw'].append(draw_results)
        
        # Calculate averages
        if results['total_combinations'] > 0:
            results['avg_numbers_per_combination'] = results['total_matched_numbers'] / results['total_combinations']
            results['avg_stars_per_combination'] = results['total_matched_stars'] / results['total_combinations']
        
        return results
    
    def test_risk_reward_strategy(self, test_draws, combinations_per_draw=5):
        """
        Test risk/reward strategy
        
        Args:
            test_draws: DataFrame with test draws
            combinations_per_draw: Number of combinations to generate per draw
            
        Returns:
            dict: Performance results
        """
        logger.info("Testing Risk/Reward Strategy...")
        
        # Initialize results
        results = {
            'strategy': 'Risk/Reward',
            'total_combinations': 0,
            'total_matched_numbers': 0,
            'total_matched_stars': 0,
            'prize_tiers': defaultdict(int),
            'details_by_draw': []
        }
        
        # Test each draw
        for _, test_draw in test_draws.iterrows():
            test_date = test_draw['date']
            test_nums, test_stars = self.get_draw_numbers(test_draw)
            
            # Get all draws before the test date for training
            training_data = self.draws[self.draws['date'] < test_date].copy()
            
            # Generate combinations using risk/reward approach
            combinations = self.generate_risk_reward_combinations(training_data, combinations_per_draw)
            
            # Evaluate combinations
            draw_results = self.evaluate_combinations(combinations, test_nums, test_stars)
            draw_results['date'] = test_date.strftime('%Y-%m-%d')
            draw_results['actual_numbers'] = test_nums
            draw_results['actual_stars'] = test_stars
            
            # Add to overall results
            results['total_combinations'] += len(combinations)
            results['total_matched_numbers'] += draw_results['total_matched_numbers']
            results['total_matched_stars'] += draw_results['total_matched_stars']
            
            # Update prize counts
            for tier, count in draw_results['prize_tiers'].items():
                results['prize_tiers'][tier] += count
            
            # Add draw details
            results['details_by_draw'].append(draw_results)
        
        # Calculate averages
        if results['total_combinations'] > 0:
            results['avg_numbers_per_combination'] = results['total_matched_numbers'] / results['total_combinations']
            results['avg_stars_per_combination'] = results['total_matched_stars'] / results['total_combinations']
        
        return results
    
    def test_may6_optimized_strategy(self, test_draws, combinations_per_draw=5):
        """
        Test the May 6 optimized strategy
        
        Args:
            test_draws: DataFrame with test draws
            combinations_per_draw: Number of combinations to generate per draw
            
        Returns:
            dict: Performance results
        """
        logger.info("Testing May 6 Optimized Strategy...")
        
        # Initialize results
        results = {
            'strategy': 'May 6 Optimized',
            'total_combinations': 0,
            'total_matched_numbers': 0,
            'total_matched_stars': 0,
            'prize_tiers': defaultdict(int),
            'details_by_draw': []
        }
        
        # Test each draw
        for _, test_draw in test_draws.iterrows():
            test_date = test_draw['date']
            test_nums, test_stars = self.get_draw_numbers(test_draw)
            
            # Generate combinations using May 6 optimized strategy
            combinations = self.generate_may6_optimized_combinations(combinations_per_draw)
            
            # Evaluate combinations
            draw_results = self.evaluate_combinations(combinations, test_nums, test_stars)
            draw_results['date'] = test_date.strftime('%Y-%m-%d')
            draw_results['actual_numbers'] = test_nums
            draw_results['actual_stars'] = test_stars
            
            # Add to overall results
            results['total_combinations'] += len(combinations)
            results['total_matched_numbers'] += draw_results['total_matched_numbers']
            results['total_matched_stars'] += draw_results['total_matched_stars']
            
            # Update prize counts
            for tier, count in draw_results['prize_tiers'].items():
                results['prize_tiers'][tier] += count
            
            # Add draw details
            results['details_by_draw'].append(draw_results)
        
        # Calculate averages
        if results['total_combinations'] > 0:
            results['avg_numbers_per_combination'] = results['total_matched_numbers'] / results['total_combinations']
            results['avg_stars_per_combination'] = results['total_matched_stars'] / results['total_combinations']
        
        return results
    
    def test_universal_strategy(self, test_draws, combinations_per_draw=5):
        """
        Test a universal (random) strategy for comparison
        
        Args:
            test_draws: DataFrame with test draws
            combinations_per_draw: Number of combinations to generate per draw
            
        Returns:
            dict: Performance results
        """
        logger.info("Testing Universal (Random) Strategy...")
        
        # Initialize results
        results = {
            'strategy': 'Universal (Random)',
            'total_combinations': 0,
            'total_matched_numbers': 0,
            'total_matched_stars': 0,
            'prize_tiers': defaultdict(int),
            'details_by_draw': []
        }
        
        # Test each draw
        for _, test_draw in test_draws.iterrows():
            test_date = test_draw['date']
            test_nums, test_stars = self.get_draw_numbers(test_draw)
            
            # Generate random combinations
            combinations = []
            for _ in range(combinations_per_draw):
                numbers = sorted(random.sample(range(1, 51), 5))
                stars = sorted(random.sample(range(1, 13), 2))
                combinations.append((numbers, stars))
            
            # Evaluate combinations
            draw_results = self.evaluate_combinations(combinations, test_nums, test_stars)
            draw_results['date'] = test_date.strftime('%Y-%m-%d')
            draw_results['actual_numbers'] = test_nums
            draw_results['actual_stars'] = test_stars
            
            # Add to overall results
            results['total_combinations'] += len(combinations)
            results['total_matched_numbers'] += draw_results['total_matched_numbers']
            results['total_matched_stars'] += draw_results['total_matched_stars']
            
            # Update prize counts
            for tier, count in draw_results['prize_tiers'].items():
                results['prize_tiers'][tier] += count
            
            # Add draw details
            results['details_by_draw'].append(draw_results)
        
        # Calculate averages
        if results['total_combinations'] > 0:
            results['avg_numbers_per_combination'] = results['total_matched_numbers'] / results['total_combinations']
            results['avg_stars_per_combination'] = results['total_matched_stars'] / results['total_combinations']
        
        return results
    
    def generate_frequency_combinations(self, training_data, count=5):
        """
        Generate combinations using frequency analysis
        
        Args:
            training_data: DataFrame with historical draws for analysis
            count: Number of combinations to generate
            
        Returns:
            list: List of tuples (numbers, stars)
        """
        combinations = []
        
        # Calculate frequency of each number and star
        num_freq = {}
        star_freq = {}
        
        # Basic frequency counting
        for _, draw in training_data.iterrows():
            for i in range(1, 6):  # 5 main numbers
                num = draw[f'n{i}']
                num_freq[num] = num_freq.get(num, 0) + 1
            
            for i in range(1, 3):  # 2 stars
                star = draw[f's{i}']
                star_freq[star] = star_freq.get(star, 0) + 1
        
        # Apply recency weighting - more recent draws get higher weight
        recent_draws = training_data.sort_values('date', ascending=False).head(10)
        for _, draw in recent_draws.iterrows():
            for i in range(1, 6):  # 5 main numbers
                num = draw[f'n{i}']
                num_freq[num] = num_freq.get(num, 0) + 0.5  # Add 50% boost
            
            for i in range(1, 3):  # 2 stars
                star = draw[f's{i}']
                star_freq[star] = star_freq.get(star, 0) + 0.5  # Add 50% boost
        
        # Generate combinations with different levels of randomness
        for i in range(count):
            # Sort by frequency
            sorted_nums = sorted(num_freq.items(), key=lambda x: x[1], reverse=True)
            sorted_stars = sorted(star_freq.items(), key=lambda x: x[1], reverse=True)
            
            # Get top numbers and stars, with more variety as i increases
            top_n = 15 + i * 2  # Increase pool size for each combination
            top_s = 5 + i  # Increase pool size for stars too
            
            # Take a random sample from the top frequencies
            numbers = sorted(random.sample([n for n, _ in sorted_nums[:top_n]], 5))
            stars = sorted(random.sample([s for s, _ in sorted_stars[:top_s]], 2))
            
            combinations.append((numbers, stars))
        
        return combinations
    
    def generate_risk_reward_combinations(self, training_data, count=5):
        """
        Generate combinations using risk/reward approach
        
        Args:
            training_data: DataFrame with historical draws for analysis
            count: Number of combinations to generate
            
        Returns:
            list: List of tuples (numbers, stars)
        """
        combinations = []
        
        # Calculate frequency of each number and star
        num_freq = {}
        star_freq = {}
        
        # Basic frequency counting
        for _, draw in training_data.iterrows():
            for i in range(1, 6):  # 5 main numbers
                num = draw[f'n{i}']
                num_freq[num] = num_freq.get(num, 0) + 1
            
            for i in range(1, 3):  # 2 stars
                star = draw[f's{i}']
                star_freq[star] = star_freq.get(star, 0) + 1
        
        # Get most recent draw for pattern analysis
        if len(training_data) > 0:
            recent_draw = training_data.sort_values('date', ascending=False).iloc[0]
            recent_nums = [recent_draw[f'n{i}'] for i in range(1, 6)]
            recent_stars = [recent_draw[f's{i}'] for i in range(1, 3)]
            
            # Boost numbers/stars from most recent draw
            for num in recent_nums:
                num_freq[num] = num_freq.get(num, 0) * 1.2  # 20% boost
            
            for star in recent_stars:
                star_freq[star] = star_freq.get(star, 0) * 1.3  # 30% boost
        
        # Define number ranges for balanced selection
        ranges = [
            (1, 17),    # Low
            (18, 34),   # Mid
            (35, 50)    # High
        ]
        
        # Generate combinations with different risk levels
        for i in range(count):
            # Risk level increases with i
            risk_level = 0.2 + (i * 0.15)  # 0.2, 0.35, 0.5, 0.65, 0.8
            
            # For higher risk, include some cold numbers
            sorted_nums = sorted(num_freq.items(), key=lambda x: x[1], reverse=True)
            sorted_stars = sorted(star_freq.items(), key=lambda x: x[1], reverse=True)
            
            if risk_level > 0.5:
                # Include some less frequent numbers for higher risk/reward
                hot_nums = [n for n, _ in sorted_nums[:15]]  # Top 15 numbers
                cold_nums = [n for n, _ in sorted_nums[-10:]]  # Bottom 10 numbers
                
                # Adjust ratio based on risk level
                cold_ratio = risk_level - 0.3
                cold_count = int(5 * cold_ratio)
                hot_count = 5 - cold_count
                
                # Select numbers from hot and cold pools
                selected_hot = random.sample(hot_nums, hot_count)
                selected_cold = random.sample(cold_nums, cold_count)
                
                numbers = sorted(selected_hot + selected_cold)
            else:
                # Lower risk - select numbers by range for balanced coverage
                selected_numbers = []
                
                # Get numbers in each range with their frequencies
                range_nums = {}
                for start, end in ranges:
                    range_nums[(start, end)] = [(n, f) for n, f in sorted_nums if start <= n <= end]
                
                # Sample from each range
                for (start, end), nums_in_range in range_nums.items():
                    # Determine how many to select from this range
                    if start == 1:  # Low range
                        count_from_range = 1
                    elif start == 18:  # Mid range
                        count_from_range = 2
                    else:  # High range
                        count_from_range = 2
                    
                    # Make sure we have enough numbers in the range
                    count_from_range = min(count_from_range, len(nums_in_range))
                    
                    # Select the top numbers from the range
                    range_selected = [n for n, _ in nums_in_range[:count_from_range]]
                    selected_numbers.extend(range_selected)
                
                # Fill remaining spots if needed
                remaining_spots = 5 - len(selected_numbers)
                if remaining_spots > 0:
                    # Get all numbers not yet selected
                    remaining_nums = [n for n, _ in sorted_nums if n not in selected_numbers]
                    
                    # Select from remaining
                    if remaining_nums:
                        selected_numbers.extend(random.sample(remaining_nums, min(remaining_spots, len(remaining_nums))))
                
                numbers = sorted(selected_numbers)
            
            # For stars, always include at least one from top 3
            top_stars = [s for s, _ in sorted_stars[:3]]
            if top_stars:
                selected_stars = [random.choice(top_stars)]
                
                # Get second star from the rest
                remaining_stars = [s for s in range(1, 13) if s not in selected_stars]
                if remaining_stars:
                    selected_stars.append(random.choice(remaining_stars))
                
                stars = sorted(selected_stars)
            else:
                stars = sorted(random.sample(range(1, 13), 2))
            
            # Ensure we have 5 numbers and 2 stars
            while len(numbers) < 5:
                new_num = random.randint(1, 50)
                if new_num not in numbers:
                    numbers.append(new_num)
            
            while len(stars) < 2:
                new_star = random.randint(1, 12)
                if new_star not in stars:
                    stars.append(new_star)
            
            # Sort the final selections
            numbers.sort()
            stars.sort()
            
            combinations.append((numbers, stars))
        
        return combinations
    
    def generate_may6_optimized_combinations(self, count=5):
        """
        Generate combinations using the May 6 optimized strategy
        
        Args:
            count: Number of combinations to generate
            
        Returns:
            list: List of tuples (numbers, stars)
        """
        # May 6 draw data
        may6_draw = {
            'numbers': [8, 23, 24, 47, 48],
            'stars': [4, 9]
        }
        
        combinations = []
        
        # Define groups for balanced selection
        number_groups = {
            'low': list(range(1, 18)),
            'mid': list(range(18, 35)),   # Includes 23, 24 from May 6
            'high': list(range(35, 51))   # Includes 47, 48 from May 6
        }
        
        # Optimal distribution based on May 6
        optimal_distribution = {
            'low_count': 1,
            'mid_count': 2,   # Mid range had 2 numbers (23, 24)
            'high_count': 2    # High range had 2 numbers (47, 48)
        }
        
        # Generate combinations with different balance of patterns
        for i in range(count):
            # Different risk levels for variety
            risk_level = 0.5 + (i * 0.1)  # 0.5, 0.6, 0.7, 0.8, 0.9
            
            # Initialize weights for all numbers
            number_weights = {n: 1.0 for n in range(1, 51)}
            star_weights = {s: 1.0 for s in range(1, 13)}
            
            # Boost May 6 numbers and stars
            for num in may6_draw['numbers']:
                number_weights[num] *= 2.0
                
            for star in may6_draw['stars']:
                star_weights[star] *= 3.0
            
            # Select numbers according to optimal distribution
            selected_numbers = []
            
            # Select from low range
            low_nums = number_groups['low']
            low_weights = [number_weights.get(n, 1.0) for n in low_nums]
            sum_weights = sum(low_weights)
            low_probs = [w/sum_weights for w in low_weights] if sum_weights > 0 else None
            
            if low_nums and low_probs:
                low_count = optimal_distribution['low_count']
                chosen_low = np.random.choice(low_nums, size=min(low_count, len(low_nums)), replace=False, p=low_probs)
                selected_numbers.extend(chosen_low)
            
            # Select from mid range
            mid_nums = number_groups['mid']
            
            # Prioritize 23, 24 which were in May 6 draw
            for priority_num in [23, 24]:
                if priority_num in mid_nums and random.random() < 0.6:
                    selected_numbers.append(priority_num)
                    mid_nums = [n for n in mid_nums if n != priority_num]
            
            # Select any remaining needed from mid range
            if mid_nums:
                mid_weights = [number_weights.get(n, 1.0) for n in mid_nums]
                sum_weights = sum(mid_weights)
                mid_probs = [w/sum_weights for w in mid_weights] if sum_weights > 0 else None
                
                if mid_probs:
                    mid_count = optimal_distribution['mid_count'] - len([n for n in selected_numbers if n in number_groups['mid']])
                    if mid_count > 0:
                        chosen_mid = np.random.choice(mid_nums, size=min(mid_count, len(mid_nums)), replace=False, p=mid_probs)
                        selected_numbers.extend(chosen_mid)
            
            # Select from high range
            high_nums = number_groups['high']
            
            # Prioritize 47, 48 which were in May 6 draw
            for priority_num in [47, 48]:
                if priority_num in high_nums and random.random() < 0.6:
                    selected_numbers.append(priority_num)
                    high_nums = [n for n in high_nums if n != priority_num]
            
            # Select any remaining needed from high range
            if high_nums:
                high_weights = [number_weights.get(n, 1.0) for n in high_nums]
                sum_weights = sum(high_weights)
                high_probs = [w/sum_weights for w in high_weights] if sum_weights > 0 else None
                
                if high_probs:
                    high_count = optimal_distribution['high_count'] - len([n for n in selected_numbers if n in number_groups['high']])
                    if high_count > 0:
                        chosen_high = np.random.choice(high_nums, size=min(high_count, len(high_nums)), replace=False, p=high_probs)
                        selected_numbers.extend(chosen_high)
            
            # Ensure we have exactly 5 numbers
            selected_numbers = list(set(selected_numbers))  # Remove any duplicates
            while len(selected_numbers) < 5:
                new_num = random.randint(1, 50)
                if new_num not in selected_numbers:
                    selected_numbers.append(new_num)
                    
            # If we somehow got more than 5, trim
            selected_numbers = selected_numbers[:5]
            
            # For stars - strong preference for 4 and 9
            selected_stars = []
            
            # Try to include at least one of the successful stars
            may6_stars = [4, 9]
            if random.random() < 0.8:  # 80% chance to include at least one May 6 star
                selected_stars.append(random.choice(may6_stars))
                
            # Fill the second star position
            remaining_stars = [s for s in range(1, 13) if s not in selected_stars]
            if remaining_stars:
                # Weighted selection favoring stars that weren't selected
                remaining_weights = [star_weights.get(s, 1.0) for s in remaining_stars]
                sum_weights = sum(remaining_weights)
                remaining_probs = [w/sum_weights for w in remaining_weights] if sum_weights > 0 else None
                
                if remaining_probs:
                    chosen_star = np.random.choice(remaining_stars, size=1, p=remaining_probs)[0]
                    selected_stars.append(chosen_star)
            
            # Ensure we have exactly 2 stars
            while len(selected_stars) < 2:
                new_star = random.randint(1, 12)
                if new_star not in selected_stars:
                    selected_stars.append(new_star)
            
            # Sort selections
            selected_numbers.sort()
            selected_stars.sort()
            
            combinations.append((selected_numbers, selected_stars))
        
        return combinations
    
    def evaluate_combinations(self, combinations, actual_numbers, actual_stars):
        """
        Evaluate combinations against actual draw results
        
        Args:
            combinations: List of (numbers, stars) tuples
            actual_numbers: List of actual drawn numbers
            actual_stars: List of actual drawn stars
            
        Returns:
            dict: Results including matches and prize tiers
        """
        # Convert actual numbers to sets for easier matching
        actual_numbers_set = set(actual_numbers)
        actual_stars_set = set(actual_stars)
        
        # Results for this draw
        draw_results = {
            'total_matched_numbers': 0,
            'total_matched_stars': 0,
            'prize_tiers': defaultdict(int),
            'combinations': []
        }
        
        # Evaluate each combination
        for numbers, stars in combinations:
            # Convert to sets
            numbers_set = set(numbers)
            stars_set = set(stars)
            
            # Calculate matches
            matched_numbers = len(numbers_set.intersection(actual_numbers_set))
            matched_stars = len(stars_set.intersection(actual_stars_set))
            
            # Determine prize tier
            prize_tier = self.get_prize_tier(matched_numbers, matched_stars)
            
            # Update counters
            draw_results['total_matched_numbers'] += matched_numbers
            draw_results['total_matched_stars'] += matched_stars
            draw_results['prize_tiers'][prize_tier] += 1
            
            # Add combination details
            draw_results['combinations'].append({
                'numbers': numbers,
                'stars': stars,
                'matched_numbers': matched_numbers,
                'matched_stars': matched_stars,
                'prize_tier': prize_tier
            })
        
        return draw_results
    
    def get_prize_tier(self, matched_numbers, matched_stars):
        """
        Determine prize tier based on matched numbers and stars
        
        Args:
            matched_numbers: Number of matched main numbers
            matched_stars: Number of matched stars
            
        Returns:
            str: Prize tier description
        """
        if matched_numbers == 5 and matched_stars == 2:
            return "Jackpot"
        elif matched_numbers == 5 and matched_stars == 1:
            return "2nd Prize"
        elif matched_numbers == 5 and matched_stars == 0:
            return "3rd Prize"
        elif matched_numbers == 4 and matched_stars == 2:
            return "4th Prize"
        elif matched_numbers == 4 and matched_stars == 1:
            return "5th Prize"
        elif matched_numbers == 3 and matched_stars == 2:
            return "6th Prize"
        elif matched_numbers == 4 and matched_stars == 0:
            return "7th Prize"
        elif matched_numbers == 2 and matched_stars == 2:
            return "8th Prize"
        elif matched_numbers == 3 and matched_stars == 1:
            return "9th Prize"
        elif matched_numbers == 3 and matched_stars == 0:
            return "10th Prize"
        elif matched_numbers == 1 and matched_stars == 2:
            return "11th Prize"
        elif matched_numbers == 2 and matched_stars == 1:
            return "12th Prize"
        elif matched_numbers == 2 and matched_stars == 0:
            return "13th Prize"
        else:
            return "No Prize"
    
    def run_all_tests(self, combinations_per_draw=5):
        """
        Run all strategy tests
        
        Args:
            combinations_per_draw: Number of combinations to generate per draw
            
        Returns:
            dict: Results for all strategies
        """
        # Test each strategy
        self.results['frequency'] = self.test_frequency_strategy(self.test_draws, combinations_per_draw)
        self.results['risk_reward'] = self.test_risk_reward_strategy(self.test_draws, combinations_per_draw)
        self.results['may6_optimized'] = self.test_may6_optimized_strategy(self.test_draws, combinations_per_draw)
        self.results['universal'] = self.test_universal_strategy(self.test_draws, combinations_per_draw)
        
        return self.results
    
    def print_results(self):
        """Print a summary of test results"""
        if not self.results:
            logger.error("No test results available. Run run_all_tests() first.")
            return
        
        print(f"\n{'='*100}")
        print(f"STRATEGY TEST RESULTS - Last {self.num_draws} draws")
        print(f"{'='*100}\n")
        
        # Sort strategies by performance
        sorted_results = sorted(
            self.results.values(),
            key=lambda x: (
                x.get('avg_numbers_per_combination', 0) + 
                x.get('avg_stars_per_combination', 0) * 2
            ),
            reverse=True
        )
        
        # Print ranking
        print(f"STRATEGY RANKING (by average match rate):")
        print(f"{'-'*100}")
        print(f"{'Rank':<6}{'Strategy':<20}{'Avg Numbers':<15}{'Avg Stars':<15}{'Total Wins':<15}{'Win Rate':<15}")
        print(f"{'-'*100}")
        
        for i, result in enumerate(sorted_results):
            strategy = result['strategy']
            
            # Count total wins (anything that's not "No Prize")
            total_combinations = result['total_combinations']
            total_wins = sum(
                count for tier, count in result['prize_tiers'].items()
                if tier != "No Prize"
            )
            win_rate = (total_wins / total_combinations) * 100 if total_combinations else 0
            
            print(
                f"{i+1:<6}{strategy:<20}"
                f"{result.get('avg_numbers_per_combination', 0):.2f} of 5      "
                f"{result.get('avg_stars_per_combination', 0):.2f} of 2      "
                f"{total_wins:<15}{win_rate:.2f}%"
            )
        
        # Print detailed results for each strategy
        for result in sorted_results:
            strategy = result['strategy']
            print(f"\n\n{'='*100}")
            print(f"{strategy.upper()} STRATEGY DETAILS")
            print(f"{'='*100}")
            
            # Overall statistics
            total_combinations = result['total_combinations']
            print(f"Total combinations tested: {total_combinations}")
            print(f"Average main numbers matched: {result.get('avg_numbers_per_combination', 0):.2f} of 5")
            print(f"Average stars matched: {result.get('avg_stars_per_combination', 0):.2f} of 2")
            
            # Prize tier breakdown
            print("\nPrize Tier Breakdown:")
            prize_tiers = sorted(
                [(tier, count) for tier, count in result['prize_tiers'].items()],
                key=lambda x: (x[0] != "No Prize", x[0])  # Sort with "No Prize" at the end
            )
            
            for tier, count in prize_tiers:
                percentage = (count / total_combinations) * 100 if total_combinations else 0
                print(f"  {tier+':':<20} {count} ({percentage:.2f}%)")
            
            # Find best performing draw
            best_draw = max(
                result['details_by_draw'],
                key=lambda x: x['total_matched_numbers'] + x['total_matched_stars'] * 2
            )
            
            print(f"\nBest Performing Draw: {best_draw['date']}")
            print(f"  Actual numbers: {best_draw['actual_numbers']}")
            print(f"  Actual stars: {best_draw['actual_stars']}")
            print(f"  Total matched numbers across all combinations: {best_draw['total_matched_numbers']}")
            print(f"  Total matched stars across all combinations: {best_draw['total_matched_stars']}")
            
            # Find best combination
            best_combo = max(
                best_draw['combinations'],
                key=lambda x: x['matched_numbers'] + x['matched_stars'] * 2
            )
            
            print(f"\n  Best combination for this draw:")
            print(f"    Numbers: {best_combo['numbers']}")
            print(f"    Stars: {best_combo['stars']}")
            print(f"    Matched: {best_combo['matched_numbers']} numbers and {best_combo['matched_stars']} stars")
            print(f"    Prize tier: {best_combo['prize_tier']}")
        
        # Final recommendation
        print(f"\n\n{'='*100}")
        print("FINAL RECOMMENDATION")
        print(f"{'='*100}")
        
        best_strategy = sorted_results[0]['strategy']
        print(f"The {best_strategy} strategy performed best in our tests.")
        
        # Compare to random
        if 'universal' in self.results:
            random_result = self.results['universal']
            best_result = sorted_results[0]
            
            numbers_improvement = (
                best_result.get('avg_numbers_per_combination', 0) / 
                random_result.get('avg_numbers_per_combination', 1)
            ) - 1
            
            stars_improvement = (
                best_result.get('avg_stars_per_combination', 0) / 
                random_result.get('avg_stars_per_combination', 1)
            ) - 1
            
            print(f"\nCompared to random selection:")
            print(f"- {numbers_improvement*100:.1f}% improvement in matching main numbers")
            print(f"- {stars_improvement*100:.1f}% improvement in matching stars")
        
        # Strategy-specific recommendations
        if best_strategy == "May 6 Optimized":
            print("\nRecommendations:")
            print("1. Continue using the May 6 optimized strategy for future draws")
            print("2. Pay special attention to including stars 4 and 9 in your combinations")
            print("3. Maintain the balanced number distribution (1 low, 2 mid, 2 high)")
            print("4. Consider numbers from the 20-25 range and 45-50 range in your selections")
        
        elif best_strategy == "Risk/Reward":
            print("\nRecommendations:")
            print("1. Focus on the Risk/Reward strategy with a medium-high risk level (0.6-0.8)")
            print("2. Include at least one recent hot number in each combination")
            print("3. For stars, prioritize those with highest historical frequency")
            print("4. Maintain a balanced distribution across number ranges")
        
        elif best_strategy == "Frequency":
            print("\nRecommendations:")
            print("1. Use the Frequency strategy with recent weight of 0.7-0.8")
            print("2. Focus more on recent draw patterns")
            print("3. For stars, stick strictly to the highest frequency stars")
            print("4. Consider a slight recency boost for numbers/stars from the last 5 draws")

def main():
    """Run strategy tests and print results"""
    # Get command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Test Euromillions prediction strategies')
    parser.add_argument('--draws', type=int, default=20, help='Number of recent draws to test against')
    parser.add_argument('--combinations', type=int, default=5, help='Number of combinations per draw')
    args = parser.parse_args()
    
    print(f"Testing strategies on the last {args.draws} draws with {args.combinations} combinations per draw...")
    
    # Initialize tester and run tests
    tester = SimpleStrategyTester(num_draws=args.draws)
    tester.run_all_tests(combinations_per_draw=args.combinations)
    tester.print_results()

if __name__ == "__main__":
    main()