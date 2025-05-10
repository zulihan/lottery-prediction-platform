"""
French Loto prediction strategies
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FrenchLotoStrategy:
    """
    Class implementing various strategies for French Loto number prediction
    """
    
    def __init__(self, statistics):
        """
        Initialize with French Loto statistics
        
        Args:
            statistics: FrenchLotoStatistics object
        """
        self.statistics = statistics
        self.data = statistics.data
        
    def generate_frequency_based(self, strength=0.6):
        """
        Generate numbers using frequency-based strategy
        
        Args:
            strength: How strongly to weight frequent numbers (0-1)
            
        Returns:
            tuple: (main_numbers, lucky_number)
        """
        # Get frequency dictionaries
        if not hasattr(self.statistics, 'main_number_freq'):
            self.statistics.analyze_frequencies()
            
        main_freq = self.statistics.main_number_freq
        lucky_freq = self.statistics.lucky_number_freq
        
        # Create weights proportional to frequencies
        number_weights = {}
        for num, freq in main_freq.items():
            # Apply the strength parameter (blend between frequency and uniform)
            # Higher strength means more weight to frequent numbers
            uniform_weight = 1.0
            number_weights[num] = (freq * strength) + (uniform_weight * (1 - strength))
        
        # Lucky number weights
        lucky_weights = {}
        for num, freq in lucky_freq.items():
            lucky_weights[num] = (freq * strength) + (1.0 * (1 - strength))
        
        # Select main numbers using weighted random selection
        main_numbers = []
        numbers_list = list(range(1, 50))
        weights_list = [number_weights.get(n, 1.0) for n in numbers_list]
        
        # Normalize weights
        weights_sum = sum(weights_list)
        weights_list = [w/weights_sum for w in weights_list]
        
        while len(main_numbers) < 5:
            # Select a number based on weights
            selected = np.random.choice(numbers_list, p=weights_list)
            
            # If not already selected, add it
            if selected not in main_numbers:
                main_numbers.append(selected)
                
                # Remove selected number from choices for next picks
                idx = numbers_list.index(selected)
                numbers_list.pop(idx)
                weights_list.pop(idx)
                
                # Renormalize weights
                if weights_list:
                    weights_sum = sum(weights_list)
                    weights_list = [w/weights_sum for w in weights_list]
        
        # Select lucky number
        lucky_numbers_list = list(range(1, 11))
        lucky_weights_list = [lucky_weights.get(n, 1.0) for n in lucky_numbers_list]
        weights_sum = sum(lucky_weights_list)
        lucky_weights_list = [w/weights_sum for w in lucky_weights_list]
        
        lucky_number = np.random.choice(lucky_numbers_list, p=lucky_weights_list)
        
        return sorted(main_numbers), lucky_number
    
    def generate_hot_cold_balanced(self):
        """
        Generate a combination with a mix of hot and cold numbers
        
        Returns:
            tuple: (main_numbers, lucky_number)
        """
        # Get hot and cold numbers
        hot_cold = self.statistics.hot_cold_numbers
        
        hot_numbers = hot_cold['hot_numbers']
        cold_numbers = hot_cold['cold_numbers']
        hot_lucky = hot_cold['hot_lucky']
        cold_lucky = hot_cold['cold_lucky']
        
        # If we don't have enough hot or cold numbers, supplement with random ones
        all_numbers = list(range(1, 50))
        neutral_numbers = [n for n in all_numbers if n not in hot_numbers and n not in cold_numbers]
        
        # Decide on mix: 2-3 hot, 1-2 cold, remainder neutral
        hot_count = min(3, len(hot_numbers))
        if hot_count == 0:
            hot_count = 0
        else:
            hot_count = random.randint(1, hot_count)
            
        cold_count = min(2, len(cold_numbers))
        if cold_count == 0:
            cold_count = 0
        else:
            cold_count = random.randint(1, cold_count)
            
        neutral_count = 5 - hot_count - cold_count
        
        # Select numbers from each category
        selected = []
        
        if hot_count > 0 and hot_numbers:
            selected.extend(random.sample(hot_numbers, hot_count))
        
        if cold_count > 0 and cold_numbers:
            selected.extend(random.sample(cold_numbers, cold_count))
        
        if neutral_count > 0 and neutral_numbers:
            selected.extend(random.sample(neutral_numbers, neutral_count))
        
        # If we still need more numbers, select randomly from all numbers
        while len(selected) < 5:
            remaining = [n for n in all_numbers if n not in selected]
            selected.append(random.choice(remaining))
        
        # Select lucky number with bias toward hot ones
        if hot_lucky and random.random() < 0.6:  # 60% chance to pick hot lucky
            lucky = random.choice(hot_lucky)
        elif cold_lucky and random.random() < 0.3:  # 30% of remaining (12% overall) to pick cold
            lucky = random.choice(cold_lucky)
        else:  # Otherwise pick randomly from all
            lucky = random.randint(1, 10)
        
        return sorted(selected), lucky
    
    def generate_balanced_range(self):
        """
        Generate a combination with a balance of high and low numbers
        
        Returns:
            tuple: (main_numbers, lucky_number)
        """
        # Create balanced ranges
        low_range = list(range(1, 26))
        high_range = list(range(26, 50))
        
        # Select 2-3 from low range
        low_count = random.randint(2, 3)
        low_selected = random.sample(low_range, low_count)
        
        # Select remaining from high range
        high_count = 5 - low_count
        high_selected = random.sample(high_range, high_count)
        
        # Combine and sort
        main_numbers = sorted(low_selected + high_selected)
        
        # Select lucky number
        lucky_number = random.randint(1, 10)
        
        return main_numbers, lucky_number
    
    def generate_pattern_based(self):
        """
        Generate based on pattern analysis in previous drawings
        
        Returns:
            tuple: (main_numbers, lucky_number)
        """
        # Get column names for main numbers
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        if 'n1' not in self.data.columns and 'number1' in self.data.columns:
            main_cols = ['number1', 'number2', 'number3', 'number4', 'number5']
        
        # Get column name for lucky number
        lucky_col = 'lucky' if 'lucky' in self.data.columns else 'lucky_number'
        
        # Get recent drawings (last 10)
        recent_data = self.data.sort_values('date', ascending=False).head(10)
        
        # Analyze patterns: check sums, distribution, etc.
        sum_stats = []
        for _, row in recent_data.iterrows():
            numbers = [row[col] for col in main_cols]
            sum_stats.append(sum(numbers))
        
        # Calculate target sum range (within 1 std dev of recent sums)
        mean_sum = np.mean(sum_stats)
        std_sum = np.std(sum_stats)
        target_min = int(max(5 * 1, mean_sum - std_sum))  # Minimum possible sum is 1+2+3+4+5 = 15
        target_max = int(min(5 * 49, mean_sum + std_sum))  # Maximum possible sum is 45+46+47+48+49 = 235
        
        # Generate combinations until we find one in target range
        for _ in range(100):  # Limit attempts
            # Use frequency strategy as base
            main_numbers, lucky = self.generate_frequency_based(strength=0.4)
            
            # Check if sum is in target range
            if target_min <= sum(main_numbers) <= target_max:
                return main_numbers, lucky
        
        # If we couldn't find a matching pattern, just return frequency-based
        return self.generate_frequency_based(strength=0.4)
    
    def generate_optimized_combination(self, strategy="balanced"):
        """
        Generate an optimized combination based on specified strategy
        
        Args:
            strategy: Strategy to use ("frequency", "hot_cold", "balanced_range", "pattern")
            
        Returns:
            tuple: (main_numbers, lucky_number, strategy_used)
        """
        if strategy == "frequency":
            main_numbers, lucky_number = self.generate_frequency_based()
            return main_numbers, lucky_number, "Frequency-based"
        
        elif strategy == "hot_cold":
            main_numbers, lucky_number = self.generate_hot_cold_balanced()
            return main_numbers, lucky_number, "Hot-Cold Balance"
        
        elif strategy == "balanced_range":
            main_numbers, lucky_number = self.generate_balanced_range()
            return main_numbers, lucky_number, "Balanced Range"
        
        elif strategy == "pattern":
            main_numbers, lucky_number = self.generate_pattern_based()
            return main_numbers, lucky_number, "Pattern Analysis"
        
        else:  # "balanced" or any other input
            # Use a mix of strategies
            strategies = [
                self.generate_frequency_based,
                self.generate_hot_cold_balanced,
                self.generate_balanced_range,
                self.generate_pattern_based
            ]
            
            strategy_func = random.choice(strategies)
            main_numbers, lucky_number = strategy_func()
            
            if strategy_func == self.generate_frequency_based:
                strategy_name = "Frequency-based"
            elif strategy_func == self.generate_hot_cold_balanced:
                strategy_name = "Hot-Cold Balance"
            elif strategy_func == self.generate_balanced_range:
                strategy_name = "Balanced Range"
            else:
                strategy_name = "Pattern Analysis"
                
            return main_numbers, lucky_number, strategy_name
    
    def generate_multiple_combinations(self, count=5, strategy="mixed"):
        """
        Generate multiple optimized combinations
        
        Args:
            count: Number of combinations to generate
            strategy: Strategy to use (or "mixed" for variety)
            
        Returns:
            list: List of dictionaries containing combinations and metadata
        """
        combinations = []
        
        # Keep track of combinations to avoid duplicates
        generated_sets = set()
        
        # Generate the requested number of combinations
        attempts = 0
        while len(combinations) < count and attempts < count * 3:
            attempts += 1
            
            if strategy == "mixed":
                # Choose a random strategy for each combination
                strat = random.choice(["frequency", "hot_cold", "balanced_range", "pattern", "balanced"])
            else:
                strat = strategy
            
            # Generate the combination
            main_numbers, lucky_number, strategy_used = self.generate_optimized_combination(strat)
            
            # Create a hashable representation to check for duplicates
            combo_key = tuple(sorted(main_numbers + [lucky_number]))
            
            # Only add if not a duplicate
            if combo_key not in generated_sets:
                generated_sets.add(combo_key)
                
                # Calculate a score for this combination (1-100)
                # This could be based on various factors
                score = random.randint(70, 95)  # Placeholder for a more complex scoring algorithm
                
                combinations.append({
                    'main_numbers': main_numbers,
                    'lucky_number': lucky_number,
                    'strategy': strategy_used,
                    'score': score,
                    'date_generated': datetime.now().strftime('%Y-%m-%d'),
                })
        
        # Sort by score (highest first)
        combinations.sort(key=lambda x: x['score'], reverse=True)
        
        return combinations