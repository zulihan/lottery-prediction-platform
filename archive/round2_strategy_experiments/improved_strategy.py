import json
import os
import sys
import random
import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
import logging
from collections import Counter

# Add relative import support
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import database
from statistics import EuromillionsStatistics

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImprovedEuromillionsStrategy:
    """
    Improved Euromillions strategy based on May 6 results analysis
    """
    def __init__(self, data=None):
        """Initialize with historical draw data"""
        self.data = data if data is not None else self.load_data_from_db()
        self.stats = EuromillionsStatistics(self.data)
        
        # Initialize recent draw information
        self.recent_draw = {
            'date': '2025-05-06',
            'numbers': [8, 23, 24, 47, 48],
            'stars': [4, 9]
        }
        
        # Performance weights adjusted based on May 6 results
        self.strategy_weights = {
            'risk_reward': 0.6,  # Increased weight - performed best
            'frequency': 0.3,    # Moderate weight - OK number matching
            'coverage': 0.1      # Low weight but still valuable for diversity
        }
        
        # Ranges to group numbers
        self.number_groups = {
            'low': list(range(1, 18)),
            'mid': list(range(18, 35)),
            'high': list(range(35, 51))
        }

    def load_data_from_db(self):
        """Load historical data from database"""
        try:
            logger.info("Loading data from database...")
            df = database.get_all_drawings()
            logger.info(f"Loaded {len(df)} draws from database.")
            return df
        except Exception as e:
            logger.error(f"Error loading data from database: {e}")
            # Return empty DataFrame with correct structure in case of error
            return pd.DataFrame(columns=['date', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2'])
    
    def get_number_frequency(self, recent_weight=0.7):
        """
        Get number frequency with higher weight to recent draws
        
        Args:
            recent_weight: Weight to apply to more recent draws (0-1)
        
        Returns:
            Two dicts with frequencies for numbers and stars
        """
        # Get base frequencies
        num_freq = self.stats.get_frequency()
        star_freq = self.stats.get_star_frequency()
        
        # Apply weighted frequencies if requested
        if recent_weight > 0:
            weighted_num_freq = self.stats.get_weighted_frequency(recent_weight=recent_weight)
            weighted_star_freq = self.stats.get_weighted_star_frequency(recent_weight=recent_weight)
            
            # Blend weighted and unweighted frequencies
            for num in num_freq:
                if num in weighted_num_freq:
                    num_freq[num] = (num_freq[num] * 0.3) + (weighted_num_freq[num] * 0.7)
                    
            for star in star_freq:
                if star in weighted_star_freq:
                    star_freq[star] = (star_freq[star] * 0.3) + (weighted_star_freq[star] * 0.7)
        
        # Factor in the recent draw with higher weight
        if hasattr(self, 'recent_draw') and self.recent_draw:
            boost = 2.0  # Strong boost for numbers in last draw
            for num in self.recent_draw['numbers']:
                if num in num_freq:
                    num_freq[num] += boost
            for star in self.recent_draw['stars']:
                if star in star_freq:
                    star_freq[star] += boost
        
        return num_freq, star_freq
    
    def get_hot_cold_numbers(self):
        """
        Get hot and cold numbers and stars
        
        Returns:
            dict: Dictionary with hot and cold numbers/stars
        """
        # We'll use the weighted frequency to determine hot/cold
        num_freq, star_freq = self.get_number_frequency(recent_weight=0.8)
        
        # Get sorted numbers and stars by frequency
        sorted_numbers = sorted(num_freq.items(), key=lambda x: x[1], reverse=True)
        sorted_stars = sorted(star_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Get hot numbers (top 33%)
        hot_count = len(sorted_numbers) // 3
        hot_numbers = [n for n, _ in sorted_numbers[:hot_count]]
        
        # Get cold numbers (bottom 33%)
        cold_count = len(sorted_numbers) // 3
        cold_numbers = [n for n, _ in sorted_numbers[-cold_count:]]
        
        # Get hot stars (top 33%)
        hot_star_count = max(1, len(sorted_stars) // 3)
        hot_stars = [s for s, _ in sorted_stars[:hot_star_count]]
        
        # Get cold stars (bottom 33%)
        cold_star_count = max(1, len(sorted_stars) // 3)
        cold_stars = [s for s, _ in sorted_stars[-cold_star_count:]]
        
        return {
            'hot_numbers': hot_numbers,
            'cold_numbers': cold_numbers,
            'hot_stars': hot_stars,
            'cold_stars': cold_stars
        }
    
    def get_number_correlations(self):
        """
        Get correlations between numbers
        
        Returns:
            dict: Dictionary with number pair correlations
        """
        # Get top correlated pairs
        correlated_pairs = self.stats.get_top_correlated_pairs(n=20, positive=True)
        
        # Convert to dictionary for easier lookup
        correlations = {}
        for pair, correlation in correlated_pairs:
            correlations[pair] = correlation
            
        return correlations
    
    def get_star_correlations(self):
        """
        Get correlations between stars
        
        Returns:
            dict: Dictionary with star pair correlations
        """
        # Create a simple correlation mapping based on star pairs frequency
        star_pairs = self.stats.get_star_pairs_frequency()
        
        # Normalize to get correlation-like values
        max_freq = max(star_pairs.values()) if star_pairs else 1
        correlations = {pair: freq / max_freq for pair, freq in star_pairs.items()}
        
        return correlations
    
    def get_optimal_distribution(self):
        """
        Get optimal distribution of numbers based on analysis of successful draws
        
        Returns:
            dict: Distribution pattern that maximizes win likelihood
        """
        # Based on May 6 analysis, a balanced distribution across ranges is best
        distribution = {
            'low_count': 1,   # 1-17 range
            'mid_count': 2,   # 18-34 range - increase based on 23, 24 appearing
            'high_count': 2,  # 35-50 range - increase based on 47, 48 appearing
            'consecutive': 0, # Consecutive numbers (0 = none, 1, 2 = pairs)
            'star_pairs': [(4, 9)]  # Prioritize the successful star pair
        }
        
        return distribution
    
    def get_correlation_adjusted_scores(self):
        """
        Calculate correlation-adjusted scores for numbers and stars
        
        Returns:
            Two dicts with adjusted scores for numbers and stars
        """
        # Get basic frequencies
        num_freq, star_freq = self.get_number_frequency(recent_weight=0.7)
        
        # Get hot/cold analysis
        hot_cold = self.get_hot_cold_numbers()
        
        # Calculate correlation scores from past draws
        num_corr = self.get_number_correlations()
        star_corr = self.get_star_correlations()
        
        # Adjust scores based on May 6 draw - boost numbers that appeared
        num_boost = {n: 1.5 for n in self.recent_draw['numbers']}
        star_boost = {s: 2.0 for s in self.recent_draw['stars']}
        
        # Combine all factors for final scores
        num_scores = {}
        for num in range(1, 51):
            score = num_freq.get(num, 0) * 0.4  # Base frequency
            
            # Add hot/cold factor
            if num in hot_cold['hot_numbers']:
                score *= 1.2
            elif num in hot_cold['cold_numbers']:
                score *= 0.8
            
            # Add correlation boost for numbers that appear with recent draw numbers
            corr_boost = 1.0
            for recent_num in self.recent_draw['numbers']:
                pair = (num, recent_num) if num < recent_num else (recent_num, num)
                if pair in num_corr:
                    corr_factor = num_corr.get(pair, 0)
                    corr_boost += corr_factor * 0.5
            
            score *= corr_boost
            
            # Apply direct boost for recently drawn numbers
            if num in num_boost:
                score *= num_boost[num]
                
            num_scores[num] = score
        
        # Similar process for stars
        star_scores = {}
        for star in range(1, 13):
            score = star_freq.get(star, 0) * 0.5  # Base frequency
            
            # Add hot/cold factor
            if star in hot_cold['hot_stars']:
                score *= 1.3
            elif star in hot_cold['cold_stars']:
                score *= 0.7
            
            # Add correlation boost
            corr_boost = 1.0
            for recent_star in self.recent_draw['stars']:
                pair = (star, recent_star) if star < recent_star else (recent_star, star)
                if pair in star_corr:
                    corr_factor = star_corr.get(pair, 0)
                    corr_boost += corr_factor * 0.7
            
            score *= corr_boost
            
            # Apply direct boost for recently drawn stars
            if star in star_boost:
                score *= star_boost[star]
                
            star_scores[star] = score
            
        return num_scores, star_scores
    
    def apply_risk_reward_strategy(self, risk_level=0.8):
        """
        Apply risk/reward strategy with adjustments based on May 6 results
        
        Args:
            risk_level: Level of risk (0-1), higher means more volatile combinations
        
        Returns:
            tuple: (numbers, stars, confidence_score)
        """
        logger.info(f"Generating Risk/Reward combination with risk level: {risk_level}")
        
        num_scores, star_scores = self.get_correlation_adjusted_scores()
        
        # Sort numbers by score
        sorted_numbers = sorted(num_scores.items(), key=lambda x: x[1], reverse=True)
        sorted_stars = sorted(star_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Ensure at least one number from 20-25 range after May 6 analysis
        mid_range_nums = [n for n, _ in sorted_numbers if 20 <= n <= 25]
        
        # Get optimal distribution
        distribution = self.get_optimal_distribution()
        
        # Apply risk level - higher risk includes more volatile numbers
        if risk_level > 0.7:
            # High risk: Include some less frequent numbers for higher payouts
            top_n = int(15 + (risk_level * 10))  # More risk = larger pool
            number_pool = [n for n, _ in sorted_numbers[:top_n]]
            
            # Ensure we have numbers from desired ranges
            low_range = [n for n in number_pool if n in self.number_groups['low']]
            mid_range = [n for n in number_pool if n in self.number_groups['mid']]
            high_range = [n for n in number_pool if n in self.number_groups['high']]
            
            # Force inclusion of at least one number from 20-25 range
            if not any(20 <= n <= 25 for n in mid_range) and mid_range_nums:
                mid_range.append(mid_range_nums[0])
            
            # Adjust pool based on distribution
            selected_numbers = []
            
            # Select from low range
            selected_numbers.extend(random.sample(low_range, min(distribution['low_count'], len(low_range))))
            
            # Select from mid range
            selected_numbers.extend(random.sample(mid_range, min(distribution['mid_count'], len(mid_range))))
            
            # Select from high range
            selected_numbers.extend(random.sample(high_range, min(distribution['high_count'], len(high_range))))
            
            # If we don't have 5 numbers yet, fill from the remaining pool
            remaining_count = 5 - len(selected_numbers)
            if remaining_count > 0:
                remaining_pool = [n for n in number_pool if n not in selected_numbers]
                selected_numbers.extend(random.sample(remaining_pool, min(remaining_count, len(remaining_pool))))
            
            # Ensure exactly 5 numbers
            while len(selected_numbers) < 5:
                remaining = [n for n, _ in sorted_numbers if n not in selected_numbers]
                if remaining:
                    selected_numbers.append(random.choice(remaining))
                else:
                    break
            
            # If we somehow got more than 5, trim
            selected_numbers = selected_numbers[:5]
            
            # Sort the final selection
            selected_numbers.sort()
            
            # Select stars - always include at least one of the successful stars from May 6
            success_stars = [4, 9]  # The successful stars from May 6
            star_pool = [s for s, _ in sorted_stars[:8]]  # Top 8 stars
            
            # Ensure at least one successful star is included
            selected_stars = []
            available_success_stars = [s for s in success_stars if s in star_pool]
            
            if available_success_stars:
                # Add at least one of the successful stars
                selected_stars.append(random.choice(available_success_stars))
                
                # Add remaining stars from pool (excluding already selected)
                remaining_stars = [s for s in star_pool if s not in selected_stars]
                num_to_add = 2  # We want 3 stars total
                selected_stars.extend(random.sample(remaining_stars, min(num_to_add, len(remaining_stars))))
            else:
                # If no success stars in pool, just take top 3
                selected_stars = [s for s, _ in sorted_stars[:3]]
            
            # Sort stars
            selected_stars.sort()
            
            # Calculate confidence score (0-100)
            # Higher risk choices get higher confidence scores when using risk/reward
            total_score = sum(num_scores[n] for n in selected_numbers) + sum(star_scores[s] for s in selected_stars)
            avg_score = total_score / (len(selected_numbers) + len(selected_stars))
            confidence = 70 + (avg_score * 15) + (risk_level * 20)  # Scale to 0-100 range
            
            return selected_numbers, selected_stars, min(confidence, 100)
        
        else:
            # Lower risk: Focus more on frequent numbers
            top_n = int(10 + (risk_level * 10))  # Less risk = smaller, more focused pool
            number_pool = [n for n, _ in sorted_numbers[:top_n]]
            
            # Select 5 numbers with emphasis on balanced distribution
            selected_numbers = []
            
            # Force inclusion of 47 or 48 if available (successful in last draw)
            high_value_numbers = [47, 48]
            available_high_value = [n for n in high_value_numbers if n in number_pool]
            if available_high_value:
                selected_numbers.append(random.choice(available_high_value))
            
            # Force inclusion of one number from 20-25 range if available
            available_mid_range = [n for n in mid_range_nums if n in number_pool and n not in selected_numbers]
            if available_mid_range:
                selected_numbers.append(random.choice(available_mid_range))
            
            # Fill remaining spots from top numbers
            remaining_count = 5 - len(selected_numbers)
            remaining_pool = [n for n in number_pool if n not in selected_numbers]
            selected_numbers.extend(random.sample(remaining_pool, min(remaining_count, len(remaining_pool))))
            
            # Ensure exactly 5 numbers
            while len(selected_numbers) < 5:
                remaining = [n for n, _ in sorted_numbers if n not in selected_numbers]
                if remaining:
                    selected_numbers.append(random.choice(remaining))
                else:
                    break
                    
            # Sort the final selection
            selected_numbers.sort()
            
            # Select stars - prioritize 4 and 9 for at least one star
            selected_stars = []
            
            # Force inclusion of at least one star from the May 6 draw
            success_stars = [4, 9]
            available_stars = [s for s in success_stars if s in star_scores]
            if available_stars:
                selected_stars.append(random.choice(available_stars))
            
            # Fill remaining spots from top stars
            star_pool = [s for s, _ in sorted_stars if s not in selected_stars]
            remaining_count = 3 - len(selected_stars)  # 3 stars total
            selected_stars.extend([s for s, _ in sorted_stars[:remaining_count] if s not in selected_stars])
            
            # Ensure we have exactly 3 stars
            while len(selected_stars) < 3:
                remaining = [s for s in range(1, 13) if s not in selected_stars]
                if remaining:
                    selected_stars.append(random.choice(remaining))
                else:
                    break
                    
            # Sort stars
            selected_stars.sort()
            
            # Calculate confidence score (0-100)
            # Lower risk choices get slightly lower confidence in risk/reward strategy
            total_score = sum(num_scores[n] for n in selected_numbers) + sum(star_scores[s] for s in selected_stars)
            avg_score = total_score / (len(selected_numbers) + len(selected_stars))
            confidence = 60 + (avg_score * 20) + (risk_level * 10)  # Scale to 0-100 range
            
            return selected_numbers, selected_stars, min(confidence, 100)
    
    def apply_frequency_strategy(self, recent_weight=0.7):
        """
        Apply frequency-based strategy with recency weighting
        
        Args:
            recent_weight: Weight for recent draws (0-1)
            
        Returns:
            tuple: (numbers, stars, confidence_score)
        """
        logger.info(f"Generating Frequency combination with recent weight: {recent_weight}")
        
        # Get frequency data
        num_freq, star_freq = self.get_number_frequency(recent_weight=recent_weight)
        
        # Boost numbers 47-48 based on May 6 results
        for boost_num in [47, 48]:
            if boost_num in num_freq:
                num_freq[boost_num] *= 1.5
                
        # Boost stars 4 and 9 based on May 6 results
        for boost_star in [4, 9]:
            if boost_star in star_freq:
                star_freq[boost_star] *= 2.0
        
        # Select numbers using weighted random sampling
        num_items = list(num_freq.items())
        nums = [n for n, _ in num_items]
        num_weights = np.array([f for _, f in num_items])
        num_weights = num_weights / num_weights.sum()  # Normalize
        
        # Get optimal distribution
        distribution = self.get_optimal_distribution()
        
        # Select numbers with balanced distribution
        selected_numbers = []
        
        # Select from each range according to distribution
        for range_name, count in [('low', distribution['low_count']), 
                                 ('mid', distribution['mid_count']), 
                                 ('high', distribution['high_count'])]:
            range_nums = self.number_groups[range_name]
            range_indices = [i for i, n in enumerate(nums) if n in range_nums]
            
            if range_indices:
                range_weights = num_weights[range_indices]
                range_weights = range_weights / range_weights.sum()  # Normalize
                
                # Select 'count' numbers from this range
                for _ in range(count):
                    if len(range_indices) > 0:
                        idx = np.random.choice(range_indices, p=range_weights)
                        selected_numbers.append(nums[idx])
                        
                        # Remove selected number for next iteration
                        remove_idx = range_indices.index(idx)
                        range_indices.pop(remove_idx)
                        range_weights = np.delete(range_weights, remove_idx)
                        if len(range_weights) > 0:
                            range_weights = range_weights / range_weights.sum()  # Renormalize
        
        # Fill remaining slots if needed
        remaining_count = 5 - len(selected_numbers)
        if remaining_count > 0:
            # Remove already selected numbers
            remaining_indices = [i for i, n in enumerate(nums) if n not in selected_numbers]
            if remaining_indices:
                remaining_weights = num_weights[remaining_indices]
                remaining_weights = remaining_weights / remaining_weights.sum()  # Normalize
                
                # Select remaining numbers
                remaining_nums = [nums[i] for i in remaining_indices]
                selected_numbers.extend(np.random.choice(
                    remaining_nums,
                    size=min(remaining_count, len(remaining_nums)),
                    replace=False,
                    p=remaining_weights
                ))
        
        # Force inclusion of one 20-25 range number if missing
        if not any(20 <= n <= 25 for n in selected_numbers):
            mid_range = [n for n in range(20, 26) if n not in selected_numbers]
            if mid_range and len(selected_numbers) > 0:
                # Replace a random number with one from 20-25 range
                selected_numbers[random.randrange(len(selected_numbers))] = random.choice(mid_range)
        
        # Ensure exactly 5 unique numbers
        while len(selected_numbers) < 5:
            remaining = [n for n in range(1, 51) if n not in selected_numbers]
            if remaining:
                selected_numbers.append(random.choice(remaining))
            else:
                break
                
        # Sort numbers
        selected_numbers.sort()
        
        # Select stars - include at least one from the May 6 draw if possible
        star_items = list(star_freq.items())
        stars = [s for s, _ in star_items]
        star_weights = np.array([f for _, f in star_items])
        star_weights = star_weights / star_weights.sum()  # Normalize
        
        # Try to include at least one of the most successful stars
        selected_stars = []
        for target_star in [4, 9]:  # May 6 stars
            if target_star in stars:
                selected_stars.append(target_star)
                if len(selected_stars) >= 1:  # We want at least one
                    break
        
        # Fill remaining slots
        remaining_count = 3 - len(selected_stars)  # We want 3 stars total
        if remaining_count > 0:
            # Remove already selected stars
            remaining_indices = [i for i, s in enumerate(stars) if s not in selected_stars]
            if remaining_indices:
                remaining_weights = star_weights[remaining_indices]
                remaining_weights = remaining_weights / remaining_weights.sum()  # Normalize
                
                # Select remaining stars
                remaining_stars = [stars[i] for i in remaining_indices]
                selected_stars.extend(np.random.choice(
                    remaining_stars,
                    size=min(remaining_count, len(remaining_stars)),
                    replace=False,
                    p=remaining_weights
                ))
        
        # Ensure exactly 3 unique stars
        while len(selected_stars) < 3:
            remaining = [s for s in range(1, 13) if s not in selected_stars]
            if remaining:
                selected_stars.append(random.choice(remaining))
            else:
                break
                
        # Sort stars
        selected_stars.sort()
        
        # Calculate confidence score (0-100)
        avg_num_freq = sum(num_freq.get(n, 0) for n in selected_numbers) / len(selected_numbers)
        avg_star_freq = sum(star_freq.get(s, 0) for s in selected_stars) / len(selected_stars)
        
        # Calculate confidence as a percentage of maximum possible frequency
        max_num_freq = max(num_freq.values()) if num_freq else 1
        max_star_freq = max(star_freq.values()) if star_freq else 1
        
        num_confidence = (avg_num_freq / max_num_freq) * 100 if max_num_freq else 50
        star_confidence = (avg_star_freq / max_star_freq) * 100 if max_star_freq else 50
        
        # Weight stars more due to their importance in winning
        confidence = (num_confidence * 0.4) + (star_confidence * 0.6)
        
        return selected_numbers, selected_stars, confidence
    
    def apply_ultimate_combined_strategy(self):
        """
        Apply the ultimate combined strategy that blends multiple approaches
        
        Returns:
            tuple: (numbers, stars, confidence_score)
        """
        # Generate several combinations using different strategies
        combinations = []
        
        # Generate 3 combinations with Frequency strategy
        for _ in range(3):
            weight = 0.7  # High recency weight
            numbers, stars, score = self.apply_frequency_strategy(recent_weight=weight)
            combinations.append((numbers, stars, score, 'frequency'))
        
        # Generate 3 combinations with Risk/Reward strategy
        for _ in range(3):
            risk = 0.6  # Moderate risk
            numbers, stars, score = self.apply_risk_reward_strategy(risk_level=risk)
            combinations.append((numbers, stars, score, 'risk_reward'))
        
        # Mix elements from the combinations
        # Create a score-weighted distribution for selection
        all_numbers = []
        all_stars = []
        number_weights = {}
        star_weights = {}
        
        for comb_numbers, comb_stars, comb_score, strategy in combinations:
            # Apply strategy weight
            adjusted_score = comb_score * self.strategy_weights.get(strategy, 1.0)
            
            for num in comb_numbers:
                all_numbers.append(num)
                number_weights[num] = number_weights.get(num, 0) + adjusted_score
                
            for star in comb_stars:
                all_stars.append(star)
                star_weights[star] = star_weights.get(star, 0) + adjusted_score
        
        # Count frequencies of each number and star
        number_counter = Counter(all_numbers)
        star_counter = Counter(all_stars)
        
        # Combine counters with weights
        for num, count in number_counter.items():
            number_weights[num] = number_weights.get(num, 0) * count
            
        for star, count in star_counter.items():
            star_weights[star] = star_weights.get(star, 0) * count
            
        # Force inclusion of stars 4 and 9 if they're in our pool
        selected_stars = []
        for must_include in [4, 9]:
            if must_include in star_weights:
                selected_stars.append(must_include)
                if len(selected_stars) >= 2:  # We want at least 2 from these
                    break
                
        # Fill the rest of stars (up to 3 total)
        remaining_stars_needed = 3 - len(selected_stars)
        if remaining_stars_needed > 0:
            # Remove already selected
            remaining_stars = {s: w for s, w in star_weights.items() if s not in selected_stars}
            
            # Sort by weight
            sorted_stars = sorted(remaining_stars.items(), key=lambda x: x[1], reverse=True)
            selected_stars.extend([s for s, _ in sorted_stars[:remaining_stars_needed]])
            
        # Ensure we have exactly 3 stars
        while len(selected_stars) < 3:
            remaining = [s for s in range(1, 13) if s not in selected_stars]
            if remaining:
                selected_stars.append(random.choice(remaining))
            else:
                break
        
        # Get optimal distribution for numbers
        distribution = self.get_optimal_distribution()
        
        # Select from each range according to distribution
        selected_numbers = []
        for range_name, count in [('low', distribution['low_count']), 
                                 ('mid', distribution['mid_count']), 
                                 ('high', distribution['high_count'])]:
            # Get numbers in this range with weights
            range_numbers = {n: w for n, w in number_weights.items() 
                            if n in self.number_groups[range_name] and n not in selected_numbers}
            
            # Sort by weight
            sorted_range = sorted(range_numbers.items(), key=lambda x: x[1], reverse=True)
            
            # Select top weighted numbers from this range
            selected_numbers.extend([n for n, _ in sorted_range[:count]])
            
        # If we don't have 5 numbers, fill with highest weighted remaining
        if len(selected_numbers) < 5:
            # Remove already selected
            remaining_numbers = {n: w for n, w in number_weights.items() if n not in selected_numbers}
            
            # Sort by weight
            sorted_numbers = sorted(remaining_numbers.items(), key=lambda x: x[1], reverse=True)
            
            # Add highest weighted remaining until we have 5
            needed = 5 - len(selected_numbers)
            selected_numbers.extend([n for n, _ in sorted_numbers[:needed]])
        
        # Ensure we have exactly 5 numbers
        while len(selected_numbers) < 5:
            remaining = [n for n in range(1, 51) if n not in selected_numbers]
            if remaining:
                selected_numbers.append(random.choice(remaining))
            else:
                break
        
        # Sort the final selections
        selected_numbers.sort()
        selected_stars.sort()
        
        # Return with fixed score of 95 for this combined strategy
        return selected_numbers, selected_stars, 95.0

    def generate_optimized_combinations(self):
        """
        Generate optimized combinations based on all strategies
        
        Returns:
            list: List of optimized combinations with scores
        """
        # Results container
        results = []
        
        # Generate risk/reward combinations
        for _ in range(2):
            numbers, stars, score = self.apply_risk_reward_strategy(risk_level=0.8)
            results.append({
                'strategy': 'Risk/Reward Strategy',
                'numbers': numbers,
                'stars': stars,
                'score': score
            })
        
        # Generate ultimate combined strategy combination
        numbers, stars, score = self.apply_ultimate_combined_strategy()
        results.append({
            'strategy': 'Ultimate Combined Strategy',
            'numbers': numbers,
            'stars': stars,
            'score': score
        })
        
        return results

def save_to_database(combinations):
    """Save generated combinations to database"""
    for combo in combinations:
        strategy = combo['strategy']
        numbers = combo['numbers']
        stars = combo['stars']
        score = combo['score']
        
        # Save to database
        try:
            # Current date as target draw date
            target_date = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
            combination_id = database.save_generated_combination(
                numbers=numbers,
                stars=stars,
                strategy=strategy,
                score=score,
                target_draw_date=target_date
            )
            logger.info(f"Saved combination to database with ID: {combination_id}")
        except Exception as e:
            logger.error(f"Error saving combination to database: {e}")

def main():
    """Generate optimized combinations with enhanced strategy"""
    print("Loading data from database...")
    strategy = ImprovedEuromillionsStrategy()
    print(f"Loaded {len(strategy.data)} draws from database.")
    print("Initializing statistics and strategies...\n")
    
    print("Generating Risk/Reward combinations...")
    
    # Generate and print combinations
    combinations = strategy.generate_optimized_combinations()
    
    print("\nGenerated Combinations:\n")
    
    # Show Risk/Reward combinations
    print("Risk/Reward Strategy Combinations:")
    for combo in combinations:
        if combo['strategy'] == 'Risk/Reward Strategy':
            print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
            print(f"  Stars: {', '.join(map(str, combo['stars']))}")
            print(f"  Score: {combo['score']:.2f}\n")
    
    # Show Ultimate Combined Strategy
    for combo in combinations:
        if combo['strategy'] == 'Ultimate Combined Strategy':
            print("Ultimate Combined Strategy:")
            print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
            print(f"  Stars: {', '.join(map(str, combo['stars']))}")
            print(f"  Score: {combo['score']:.2f}\n")
    
    # Save to database
    save_to_database(combinations)
    print("All combinations have been saved to the database.")

if __name__ == "__main__":
    main()