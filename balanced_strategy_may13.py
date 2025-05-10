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

class BalancedStrategy:
    """
    Balanced, probability-based strategy for Euromillions that avoids
    overweighting recently drawn numbers.
    """
    
    def __init__(self):
        """Initialize the balanced strategy"""
        # Load historical data for proper frequency analysis
        self.draws = self.load_data_from_db()
        
        # Number group ranges
        self.number_groups = {
            'low': list(range(1, 18)),    # 1-17
            'mid': list(range(18, 35)),   # 18-34
            'high': list(range(35, 51))   # 35-50
        }
        
        # Optimal distribution - balanced approach
        self.optimal_distribution = {
            'low_count': 2,    # 2 numbers from 1-17 range
            'mid_count': 2,    # 2 numbers from 18-34 range
            'high_count': 1    # 1 number from 35-50 range
        }
        
        # Define hot and cold numbers based on frequency analysis
        self.hot_cold_numbers = self.get_hot_cold_numbers()
        
        # Base weights for all numbers and stars
        self.number_weights = {n: 1.0 for n in range(1, 51)}
        self.star_weights = {s: 1.0 for s in range(1, 13)}
        
        # Apply weights from frequency analysis
        self._apply_frequency_weights()
        
        # Apply hot/cold adjustments (moderate effect)
        self._apply_hot_cold_adjustments()
        
        # Apply minor recent history adjustments
        self._apply_minor_history_adjustments()
        
        # Track already generated combinations to avoid duplicates
        self.generated_combinations = []
    
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
    
    def get_hot_cold_numbers(self):
        """
        Determine hot and cold numbers based on frequency analysis
        
        Returns:
            dict: Hot and cold numbers and stars
        """
        result = {
            'hot_numbers': [],
            'cold_numbers': [],
            'hot_stars': [],
            'cold_stars': []
        }
        
        if self.draws is None or len(self.draws) == 0:
            # Default values if no data
            result['hot_numbers'] = [5, 7, 15, 17, 19, 23, 27, 31, 37, 44, 49]
            result['cold_numbers'] = [1, 10, 13, 14, 26, 36, 38, 42, 45, 46]
            result['hot_stars'] = [3, 4, 6, 7, 9, 10]
            result['cold_stars'] = [1, 5, 8, 11]
            return result
        
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
        
        # Sort by frequency
        sorted_nums = sorted(num_counts.items(), key=lambda x: x[1], reverse=True)
        sorted_stars = sorted(star_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Define hot and cold numbers (top and bottom 20%)
        hot_count = max(int(len(sorted_nums) * 0.2), 5)
        cold_count = max(int(len(sorted_nums) * 0.2), 5)
        
        result['hot_numbers'] = [n for n, _ in sorted_nums[:hot_count]]
        result['cold_numbers'] = [n for n, _ in sorted_nums[-cold_count:]]
        
        # Define hot and cold stars (top and bottom 33%)
        hot_star_count = max(int(len(sorted_stars) * 0.33), 2)
        cold_star_count = max(int(len(sorted_stars) * 0.33), 2)
        
        result['hot_stars'] = [s for s, _ in sorted_stars[:hot_star_count]]
        result['cold_stars'] = [s for s, _ in sorted_stars[-cold_star_count:]]
        
        return result
    
    def _apply_frequency_weights(self):
        """Apply weights based on historical frequencies"""
        if self.draws is None or len(self.draws) == 0:
            return
            
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
            # Normalized frequency (0.5-1.5 range to moderate effect)
            norm_freq = 0.5 + (count / max_num_count)
            self.number_weights[num] *= norm_freq
            
        for star, count in star_counts.items():
            # Normalized frequency (0.5-1.5 range to moderate effect)
            norm_freq = 0.5 + (count / max_star_count)
            self.star_weights[star] *= norm_freq
    
    def _apply_hot_cold_adjustments(self):
        """Apply hot/cold adjustments to weights"""
        # Hot numbers get a boost
        for num in self.hot_cold_numbers['hot_numbers']:
            self.number_weights[num] *= 1.3  # 30% boost
            
        # Cold numbers get a penalty
        for num in self.hot_cold_numbers['cold_numbers']:
            self.number_weights[num] *= 0.8  # 20% penalty
            
        # Hot stars get a boost
        for star in self.hot_cold_numbers['hot_stars']:
            self.star_weights[star] *= 1.3  # 30% boost
            
        # Cold stars get a penalty
        for star in self.hot_cold_numbers['cold_stars']:
            self.star_weights[star] *= 0.8  # 20% penalty
    
    def _apply_minor_history_adjustments(self):
        """
        Apply very minor adjustments based on recent history
        Avoiding overweighting recent numbers/stars
        """
        if self.draws is None or len(self.draws) == 0:
            return
            
        # Get the 5 most recent draws
        recent_draws = self.draws.sort_values('date', ascending=False).head(5)
        
        # Track numbers and stars that appeared in recent draws
        recent_numbers = []
        recent_stars = []
        
        for _, draw in recent_draws.iterrows():
            for i in range(1, 6):
                recent_numbers.append(draw[f'n{i}'])
                
            for i in range(1, 3):
                recent_stars.append(draw[f's{i}'])
        
        # Count occurrences
        num_counter = Counter(recent_numbers)
        star_counter = Counter(recent_stars)
        
        # MINOR adjustment for numbers drawn more than once recently
        for num, count in num_counter.items():
            if count > 1:
                # SMALL PENALTY for repeated recent numbers - they're less likely to repeat again
                self.number_weights[num] *= (1.0 - (count * 0.05))  # 5-15% penalty
                
        # MINOR adjustment for stars drawn more than once recently
        for star, count in star_counter.items():
            if count > 1:
                # SMALL PENALTY for repeated recent stars - they're less likely to repeat again
                self.star_weights[star] *= (1.0 - (count * 0.05))  # 5-15% penalty
    
    def generate_optimized_combination(self, risk_level=0.5):
        """
        Generate an balanced, optimized combination
        
        Args:
            risk_level: 0-1 risk level (higher = more volatile/unique numbers)
            
        Returns:
            tuple: (numbers, stars, score)
        """
        # Prepare weights adjusted by risk level
        adjusted_weights = self.number_weights.copy()
        
        # For higher risk levels, include some randomness
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
        mid_weights = [adjusted_weights[n] for n in mid_nums]
        sum_weights = sum(mid_weights)
        mid_probs = [w/sum_weights for w in mid_weights] if sum_weights > 0 else None
        
        if mid_nums and mid_probs:
            chosen_mid = np.random.choice(
                mid_nums, 
                size=min(self.optimal_distribution['mid_count'], len(mid_nums)),
                replace=False,
                p=mid_probs
            )
            selected_numbers.extend(chosen_mid)
        
        # Select from high range (35-50)
        high_nums = list(self.number_groups['high'])
        high_weights = [adjusted_weights[n] for n in high_nums]
        sum_weights = sum(high_weights)
        high_probs = [w/sum_weights for w in high_weights] if sum_weights > 0 else None
        
        if high_nums and high_probs:
            chosen_high = np.random.choice(
                high_nums, 
                size=min(self.optimal_distribution['high_count'], len(high_nums)),
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
                remaining_weights = [adjusted_weights.get(n, 1.0) for n in remaining_nums]
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
        
        # Select stars based on weights
        selected_stars = []
        
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
        
        # Ensure we have exactly 3 stars
        while len(selected_stars) < 3:
            new_star = random.randint(1, 12)
            if new_star not in selected_stars:
                selected_stars.append(new_star)
        
        # Sort the final selections
        selected_numbers.sort()
        selected_stars.sort()
        
        # Calculate score
        score = self.calculate_combination_score(selected_numbers, selected_stars)
        
        # Add to generated combinations list
        self.generated_combinations.append((selected_numbers, selected_stars))
        
        return selected_numbers, selected_stars, score
    
    def calculate_combination_score(self, numbers, stars):
        """
        Calculate a score for the combination based on weights and patterns
        
        Args:
            numbers: List of 5 selected numbers
            stars: List of selected stars
            
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
        hot_numbers_included = len(set(numbers).intersection(set(self.hot_cold_numbers['hot_numbers'])))
        score += hot_numbers_included * 1.0
        
        # Bonus for including hot stars
        hot_stars_included = len(set(stars).intersection(set(self.hot_cold_numbers['hot_stars'])))
        score += hot_stars_included * 1.0
        
        # Cap score at 100
        return min(score, 100)
    
    def create_mixed_strategy_combination(self, base_combinations, strategy_weight=0.6):
        """
        Create a combination using a mixed strategy approach.
        Blends frequency analysis with coverage optimization.
        
        Args:
            base_combinations: List of tuples (numbers, stars, score)
            strategy_weight: Weight for frequency vs coverage (0-1)
            
        Returns:
            tuple: (numbers, stars, score)
        """
        # Extract all numbers and stars from base combinations
        all_numbers = []
        all_stars = []
        
        for numbers, stars, _ in base_combinations:
            all_numbers.extend(numbers)
            all_stars.extend(stars)
        
        # Count frequency of each number and star across combinations
        number_counter = Counter(all_numbers)
        star_counter = Counter(all_stars)
        
        # Add frequency weight
        for num, count in number_counter.items():
            weight = self.number_weights.get(num, 1.0)
            # Blend base weight with count-based weight
            number_counter[num] = (weight * strategy_weight) + (count * (1 - strategy_weight))
            
        for star, count in star_counter.items():
            weight = self.star_weights.get(star, 1.0)
            # Blend base weight with count-based weight
            star_counter[star] = (weight * strategy_weight) + (count * (1 - strategy_weight))
        
        # Select numbers according to optimal distribution but with additional coverage consideration
        selected_numbers = []
        
        # Get most common numbers by range
        common_low = [n for n, _ in number_counter.most_common() if n in self.number_groups['low']]
        common_mid = [n for n, _ in number_counter.most_common() if n in self.number_groups['mid']]
        common_high = [n for n, _ in number_counter.most_common() if n in self.number_groups['high']]
        
        # Try to include top numbers from each range
        selected_numbers.extend(common_low[:self.optimal_distribution['low_count']])
        selected_numbers.extend(common_mid[:self.optimal_distribution['mid_count']])
        selected_numbers.extend(common_high[:self.optimal_distribution['high_count']])
        
        # Ensure we have exactly 5 numbers
        selected_numbers = list(set(selected_numbers))[:5]
        
        # Fill any missing slots
        while len(selected_numbers) < 5:
            # Get remaining common numbers
            remaining_common = [n for n, _ in number_counter.most_common() if n not in selected_numbers]
            
            if remaining_common:
                selected_numbers.append(remaining_common[0])
            else:
                # If all else fails, pick a random number
                remaining = [n for n in range(1, 51) if n not in selected_numbers]
                if remaining:
                    selected_numbers.append(random.choice(remaining))
                else:
                    break
        
        # Select 3 stars from the most common
        selected_stars = []
        
        # Take top 3 stars
        top_stars = [s for s, _ in star_counter.most_common()]
        selected_stars = top_stars[:3]
        
        # Ensure we have exactly 3 stars
        while len(selected_stars) < 3:
            # Get all stars not yet selected
            remaining = [s for s in range(1, 13) if s not in selected_stars]
            if remaining:
                selected_stars.append(random.choice(remaining))
            else:
                break
        
        # Sort the final selections
        selected_numbers.sort()
        selected_stars.sort()
        
        # Calculate score
        score = self.calculate_combination_score(selected_numbers, selected_stars)
        
        return selected_numbers, selected_stars, score
    
    def generate_all_combinations(self, num_base=8, num_mixed=4):
        """
        Generate multiple optimized combinations
        
        Args:
            num_base: Number of base combinations to generate
            num_mixed: Number of mixed strategy combinations to generate
            
        Returns:
            list: List of dictionaries with combination details
        """
        all_combinations = []
        base_combinations = []
        
        # Generate base combinations with varying risk levels
        for i in range(num_base):
            # Vary risk level for more diversity
            risk_level = 0.4 + (i * 0.5 / num_base)
            numbers, stars, score = self.generate_optimized_combination(risk_level=risk_level)
            
            base_combinations.append((numbers, stars, score))
            
            all_combinations.append({
                'strategy': 'Balanced (Risk: {:.2f})'.format(risk_level),
                'numbers': numbers,
                'stars': stars,
                'score': score
            })
        
        # Generate mixed strategy combinations
        for i in range(num_mixed):
            # Vary strategy weight for diversity
            strategy_weight = 0.5 + (i * 0.1)
            numbers, stars, score = self.create_mixed_strategy_combination(
                base_combinations,
                strategy_weight=strategy_weight
            )
            
            all_combinations.append({
                'strategy': 'Mixed Strategy (Weight: {:.2f})'.format(strategy_weight),
                'numbers': numbers,
                'stars': stars,
                'score': score
            })
        
        return all_combinations

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
    """Generate optimized combinations for May 13th"""
    print("Generating Balanced Combinations for May 13th Euromillions Draw...")
    
    # Create the strategy
    optimizer = BalancedStrategy()
    
    # Generate combinations
    combinations = optimizer.generate_all_combinations(num_base=8, num_mixed=4)
    
    # Display results
    print("\nGenerated Combinations for May 13th:\n")
    
    # Display base combinations
    print("Balanced Base Combinations:")
    for combo in combinations:
        if "Balanced" in combo['strategy']:
            print(f"  Strategy: {combo['strategy']}")
            print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
            print(f"  Stars: {', '.join(map(str, combo['stars']))}")
            print(f"  Score: {combo['score']:.2f}\n")
    
    # Display mixed strategy combinations
    print("\nMixed Strategy Combinations:")
    for combo in combinations:
        if "Mixed Strategy" in combo['strategy']:
            print(f"  Strategy: {combo['strategy']}")
            print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
            print(f"  Stars: {', '.join(map(str, combo['stars']))}")
            print(f"  Score: {combo['score']:.2f}\n")
    
    # Save to database
    saved_ids = save_to_database(combinations)
    print(f"Saved {len(saved_ids)} combinations to database.")
    
    # Outline key features
    print("\nKey Strategy Features:")
    print("1. Balanced approach using historical frequencies with moderate recent result adjustments")
    print("2. Small penalty for numbers/stars that appeared multiple times recently (avoiding recency bias)")
    print("3. Diverse number range distribution (2 low, 2 mid, 1 high)")
    print("4. Includes mixed strategy combinations for optimal coverage")
    print("5. Risk level variations for diverse number selection")

if __name__ == "__main__":
    main()