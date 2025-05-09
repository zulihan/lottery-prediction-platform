import os
import sys
import random
import json
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

class UltimateMay6Optimizer:
    """
    Advanced strategy for generating optimized Euromillions combinations
    based on the successful May 6 draw and subsequent analysis.
    """
    
    def __init__(self):
        """Initialize the optimizer with May 6 insights and patterns"""
        # May 6 draw data - our foundation pattern
        self.may6_draw = {
            'numbers': [8, 23, 24, 47, 48],
            'stars': [4, 9]
        }
        
        # Number group ranges for optimal distribution
        self.number_groups = {
            'low': list(range(1, 18)),    # 1-17 (May 6 had number 8)
            'mid': list(range(18, 35)),   # 18-34 (May 6 had 23, 24)
            'high': list(range(35, 51))   # 35-50 (May 6 had 47, 48)
        }
        
        # Optimal distribution based on May 6 analysis
        self.optimal_distribution = {
            'low_count': 1,    # 1 number from 1-17 range
            'mid_count': 2,    # 2 numbers from 18-34 range
            'high_count': 2    # 2 numbers from 35-50 range
        }
        
        # Probability boosts for May 6 numbers and ranges
        self.number_boosts = {
            # Direct May 6 numbers get highest boost
            8: 3.0, 23: 3.0, 24: 3.0, 47: 3.0, 48: 3.0,
            
            # Mid-range (20-25) gets medium boost
            20: 1.8, 21: 1.8, 22: 1.8, 25: 1.8,
            
            # High range (45-50) gets medium boost
            45: 1.8, 46: 1.8, 49: 1.8, 50: 1.8
        }
        
        # Star boosts - 4 and 9 get highest boost
        self.star_boosts = {
            4: 4.0, 9: 4.0,         # May 6 stars get highest boost
            3: 1.5, 7: 1.5, 10: 1.5  # Other historically frequent stars
        }
        
        # Load hot and cold numbers for additional weighting
        self.hot_numbers = [5, 7, 15, 17, 19, 20, 23, 27, 31, 37, 44, 47, 48, 49]
        self.cold_numbers = [1, 10, 13, 14, 26, 36, 38, 42, 45, 46]
        self.hot_stars = [2, 3, 4, 7, 9, 10]
        self.cold_stars = [1, 5, 8, 11]
        
        # Base weights for all numbers and stars
        self.number_weights = {n: 1.0 for n in range(1, 51)}
        self.star_weights = {s: 1.0 for s in range(1, 13)}
        
        # Apply the various boosts to weights
        self._apply_weights()
    
    def _apply_weights(self):
        """Apply all weight adjustments to the base weights"""
        # Apply hot/cold adjustments
        for num in self.hot_numbers:
            self.number_weights[num] *= 1.5
        for num in self.cold_numbers:
            self.number_weights[num] *= 0.8
            
        for star in self.hot_stars:
            self.star_weights[star] *= 1.5
        for star in self.cold_stars:
            self.star_weights[star] *= 0.8
        
        # Apply specific number/star boosts
        for num, boost in self.number_boosts.items():
            self.number_weights[num] *= boost
            
        for star, boost in self.star_boosts.items():
            self.star_weights[star] *= boost
    
    def generate_optimized_combination(self, risk_level=0.5):
        """
        Generate an optimized combination using the May 6 pattern
        
        Args:
            risk_level: 0-1 risk level (higher = more volatile/unique numbers)
            
        Returns:
            tuple: (numbers, stars, score)
        """
        # Prepare weights adjusted by risk level
        adjusted_weights = self.number_weights.copy()
        
        # For higher risk levels, include some less frequent numbers
        if risk_level > 0.5:
            # Add extra randomness for variety
            for num in range(1, 51):
                random_factor = 1.0 + ((random.random() - 0.5) * risk_level)
                adjusted_weights[num] *= random_factor
        
        # Select numbers according to optimal distribution
        selected_numbers = []
        
        # Select from low range (1-17)
        low_nums = list(self.number_groups['low'])
        low_weights = [adjusted_weights[n] for n in low_nums]
        sum_weights = sum(low_weights)
        low_probs = [w/sum_weights for w in low_weights] if sum_weights > 0 else None
        
        if low_nums and low_probs:
            chosen_low = np.random.choice(
                low_nums, 
                size=min(self.optimal_distribution['low_count'], len(low_nums)),
                replace=False,
                p=low_probs
            )
            selected_numbers.extend(chosen_low)
        
        # Select from mid range (18-34)
        mid_nums = list(self.number_groups['mid'])
        
        # May 6 pattern had numbers 23 and 24 - prioritize these
        for priority_num in [23, 24]:
            if priority_num in mid_nums and random.random() < (0.6 - (risk_level * 0.4)):
                selected_numbers.append(priority_num)
                mid_nums.remove(priority_num)
        
        # Fill remaining mid range slots
        if mid_nums:
            mid_weights = [adjusted_weights[n] for n in mid_nums]
            sum_weights = sum(mid_weights)
            mid_probs = [w/sum_weights for w in mid_weights] if sum_weights > 0 else None
            
            if mid_probs:
                remaining_mid = self.optimal_distribution['mid_count'] - len([n for n in selected_numbers if n in self.number_groups['mid']])
                if remaining_mid > 0:
                    chosen_mid = np.random.choice(
                        mid_nums,
                        size=min(remaining_mid, len(mid_nums)),
                        replace=False,
                        p=mid_probs
                    )
                    selected_numbers.extend(chosen_mid)
        
        # Select from high range (35-50)
        high_nums = list(self.number_groups['high'])
        
        # May 6 pattern had numbers 47 and 48 - prioritize these
        for priority_num in [47, 48]:
            if priority_num in high_nums and random.random() < (0.6 - (risk_level * 0.4)):
                selected_numbers.append(priority_num)
                high_nums.remove(priority_num)
        
        # Fill remaining high range slots
        if high_nums:
            high_weights = [adjusted_weights[n] for n in high_nums]
            sum_weights = sum(high_weights)
            high_probs = [w/sum_weights for w in high_weights] if sum_weights > 0 else None
            
            if high_probs:
                remaining_high = self.optimal_distribution['high_count'] - len([n for n in selected_numbers if n in self.number_groups['high']])
                if remaining_high > 0:
                    chosen_high = np.random.choice(
                        high_nums,
                        size=min(remaining_high, len(high_nums)),
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
            remaining_weights = [adjusted_weights[n] for n in remaining_nums]
            sum_weights = sum(remaining_weights)
            remaining_probs = [w/sum_weights for w in remaining_weights] if sum_weights > 0 else None
            
            if remaining_probs:
                chosen_num = np.random.choice(remaining_nums, p=remaining_probs)
                selected_numbers.append(chosen_num)
            else:
                # Fallback to random selection
                new_num = random.randint(1, 50)
                if new_num not in selected_numbers:
                    selected_numbers.append(new_num)
        
        # Select 3 stars with priority to 4 and 9
        selected_stars = []
        
        # Strong preference for May 6 stars
        may6_stars = [4, 9]
        for star in may6_stars:
            if len(selected_stars) < 2 and random.random() < (0.9 - (risk_level * 0.3)):
                selected_stars.append(star)
        
        # Fill remaining star positions (up to 3 total)
        remaining_stars = [s for s in range(1, 13) if s not in selected_stars]
        remaining_star_weights = [self.star_weights[s] for s in remaining_stars]
        sum_weights = sum(remaining_star_weights)
        remaining_star_probs = [w/sum_weights for w in remaining_star_weights] if sum_weights > 0 else None
        
        # Select remaining stars
        remaining_count = 3 - len(selected_stars)
        if remaining_count > 0 and remaining_star_probs:
            chosen_stars = np.random.choice(
                remaining_stars,
                size=min(remaining_count, len(remaining_stars)),
                replace=False,
                p=remaining_star_probs
            )
            selected_stars.extend(chosen_stars)
        
        # Fill any remaining star positions if needed
        while len(selected_stars) < 3:
            new_star = random.randint(1, 12)
            if new_star not in selected_stars:
                selected_stars.append(new_star)
        
        # Sort the final selections
        selected_numbers.sort()
        selected_stars.sort()
        
        # Calculate score based on pattern matches and alignments
        score = self.calculate_combination_score(selected_numbers, selected_stars)
        
        return selected_numbers, selected_stars, score
    
    def calculate_combination_score(self, numbers, stars):
        """
        Calculate a score for the combination based on pattern matches
        
        Args:
            numbers: List of 5 selected numbers
            stars: List of selected stars
            
        Returns:
            float: Score from 0-100
        """
        score = 75.0  # Base score
        
        # Check for May 6 number matches
        may6_num_matches = len(set(numbers).intersection(set(self.may6_draw['numbers'])))
        may6_star_matches = len(set(stars).intersection(set(self.may6_draw['stars'])))
        
        # Bonus for May 6 matches
        score += may6_num_matches * 3.0
        score += may6_star_matches * 4.0
        
        # Check distribution pattern
        low_count = len([n for n in numbers if n in self.number_groups['low']])
        mid_count = len([n for n in numbers if n in self.number_groups['mid']])
        high_count = len([n for n in numbers if n in self.number_groups['high']])
        
        # Bonus for optimal distribution
        if low_count == self.optimal_distribution['low_count']:
            score += 2.0
        if mid_count == self.optimal_distribution['mid_count']:
            score += 2.0
        if high_count == self.optimal_distribution['high_count']:
            score += 2.0
        
        # Bonus for including hot numbers
        hot_num_matches = len(set(numbers).intersection(set(self.hot_numbers)))
        score += hot_num_matches * 1.0
        
        # Bonus for including hot stars
        hot_star_matches = len(set(stars).intersection(set(self.hot_stars)))
        score += hot_star_matches * 1.0
        
        # Cap score at 100
        return min(score, 100)
    
    def create_ultimate_mix_combination(self, base_combinations):
        """
        Create an ultimate mix combination by analyzing frequency patterns
        across multiple base combinations
        
        Args:
            base_combinations: List of tuples (numbers, stars, score)
            
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
        
        # Apply extra boost for May 6 draw numbers/stars
        for num in self.may6_draw['numbers']:
            number_counter[num] += 3
            
        for star in self.may6_draw['stars']:
            star_counter[star] += 4
        
        # Get the most frequent numbers and stars
        most_common_numbers = [n for n, _ in number_counter.most_common(10)]
        most_common_stars = [s for s, _ in star_counter.most_common(5)]
        
        # Maintain optimal distribution
        selected_numbers = []
        
        # Select from each range according to optimal distribution
        for range_name, count in self.optimal_distribution.items():
            range_nums = self.number_groups[range_name[:-6]]  # Remove '_count' suffix
            
            # Get numbers in this range from most common
            common_in_range = [n for n in most_common_numbers if n in range_nums]
            
            # Take the most common from this range
            selected_from_range = common_in_range[:count]
            selected_numbers.extend(selected_from_range)
            
            # If we didn't get enough from common numbers, fill with highest weighted
            remaining = count - len(selected_from_range)
            if remaining > 0:
                # Filter out already selected
                available_in_range = [n for n in range_nums if n not in selected_numbers]
                
                # Sort by weight
                weighted_nums = [(n, self.number_weights[n]) for n in available_in_range]
                weighted_nums.sort(key=lambda x: x[1], reverse=True)
                
                # Add top weighted
                selected_numbers.extend([n for n, _ in weighted_nums[:remaining]])
        
        # Ensure we have exactly 5 numbers
        selected_numbers = list(set(selected_numbers))[:5]
        
        # Fill any missing slots
        while len(selected_numbers) < 5:
            # Get all numbers not yet selected
            remaining = [n for n in range(1, 51) if n not in selected_numbers]
            if remaining:
                # Sort by weight
                weighted_nums = [(n, self.number_weights[n]) for n in remaining]
                weighted_nums.sort(key=lambda x: x[1], reverse=True)
                
                # Add top weighted
                selected_numbers.append(weighted_nums[0][0])
            else:
                break
        
        # Select 3 stars - prioritize May 6 stars
        selected_stars = []
        
        # Always include at least one May 6 star if possible
        for must_include in [4, 9]:
            if must_include in most_common_stars and len(selected_stars) < 1:
                selected_stars.append(must_include)
        
        # Fill with most common stars
        for star in most_common_stars:
            if star not in selected_stars and len(selected_stars) < 3:
                selected_stars.append(star)
        
        # Ensure we have exactly 3 stars
        while len(selected_stars) < 3:
            # Get all stars not yet selected
            remaining = [s for s in range(1, 13) if s not in selected_stars]
            if remaining:
                # Sort by weight
                weighted_stars = [(s, self.star_weights[s]) for s in remaining]
                weighted_stars.sort(key=lambda x: x[1], reverse=True)
                
                # Add top weighted
                selected_stars.append(weighted_stars[0][0])
            else:
                break
        
        # Sort the final selections
        selected_numbers.sort()
        selected_stars.sort()
        
        # Calculate score - fixed high score for ultimate mix
        score = 98.0
        
        return selected_numbers, selected_stars, score
    
    def generate_all_combinations(self, num_base=8, num_ultimate=4):
        """
        Generate multiple optimized combinations
        
        Args:
            num_base: Number of base combinations to generate
            num_ultimate: Number of ultimate combinations to generate
            
        Returns:
            list: List of dictionaries with combination details
        """
        all_combinations = []
        
        # Generate base combinations with varying risk levels
        base_combinations = []
        
        for i in range(num_base):
            # Vary risk level for more diversity
            risk_level = 0.4 + (i * 0.5 / num_base)
            numbers, stars, score = self.generate_optimized_combination(risk_level=risk_level)
            
            base_combinations.append((numbers, stars, score))
            
            all_combinations.append({
                'strategy': 'May 6 Optimized (Risk: {:.2f})'.format(risk_level),
                'numbers': numbers,
                'stars': stars,
                'score': score
            })
        
        # Generate ultimate mix combinations
        for _ in range(num_ultimate):
            numbers, stars, score = self.create_ultimate_mix_combination(base_combinations)
            
            all_combinations.append({
                'strategy': 'Ultimate Mix',
                'numbers': numbers,
                'stars': stars,
                'score': score
            })
        
        return all_combinations

def save_to_database(combinations):
    """Save generated combinations to database"""
    for combo in combinations:
        strategy = combo['strategy']
        numbers = combo['numbers']
        stars = combo['stars']
        score = combo['score']
        
        # Save to database
        try:
            # Next draw date (Friday after today or Tuesday if today is Saturday or Sunday)
            today = date.today()
            days_to_friday = (4 - today.weekday()) % 7
            days_to_tuesday = (1 - today.weekday()) % 7
            
            if days_to_friday <= days_to_tuesday:
                target_date = today + timedelta(days=days_to_friday)
            else:
                target_date = today + timedelta(days=days_to_tuesday)
                
            target_date_str = target_date.strftime('%Y-%m-%d')
            
            combination_id = database.save_generated_combination(
                numbers=numbers,
                stars=stars,
                strategy=strategy,
                score=score,
                target_draw_date=target_date_str
            )
            logger.info(f"Saved combination to database with ID: {combination_id}")
        except Exception as e:
            logger.error(f"Error saving combination to database: {e}")

def main():
    """Generate optimized combinations based on May 6 analysis"""
    print("Generating Ultimate May 6 Optimized Combinations...")
    optimizer = UltimateMay6Optimizer()
    
    # Generate combinations
    combinations = optimizer.generate_all_combinations(num_base=8, num_ultimate=4)
    
    # Display results
    print("\nGenerated Combinations:\n")
    
    # Display base combinations
    print("May 6 Optimized Base Combinations:")
    for combo in combinations:
        if "May 6 Optimized" in combo['strategy']:
            print(f"  Strategy: {combo['strategy']}")
            print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
            print(f"  Stars: {', '.join(map(str, combo['stars']))}")
            print(f"  Score: {combo['score']:.2f}\n")
    
    # Display ultimate combinations
    print("\nUltimate Mix Combinations:")
    for combo in combinations:
        if combo['strategy'] == "Ultimate Mix":
            print(f"  Strategy: {combo['strategy']}")
            print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
            print(f"  Stars: {', '.join(map(str, combo['stars']))}")
            print(f"  Score: {combo['score']:.2f}\n")
    
    # Save to database
    save_to_database(combinations)
    print("All combinations have been saved to the database.")

if __name__ == "__main__":
    main()