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

class May9Optimizer:
    """
    Strategy optimizer for the May 9th Euromillions draw.
    Uses insights from May 6th success but avoids repeating the exact numbers.
    """
    
    def __init__(self):
        """Initialize the optimizer with insights from May 6 but oriented to May 9"""
        # May 6 draw data - reference but not to be duplicated
        self.may6_draw = {
            'numbers': [8, 23, 24, 47, 48],
            'stars': [4, 9]
        }
        
        # Number group ranges - maintain the optimal distribution pattern
        self.number_groups = {
            'low': list(range(1, 18)),    # 1-17
            'mid': list(range(18, 35)),   # 18-34
            'high': list(range(35, 51))   # 35-50
        }
        
        # Optimal distribution pattern - 1-2-2 split was successful
        self.optimal_distribution = {
            'low_count': 1,    # 1 number from 1-17 range
            'mid_count': 2,    # 2 numbers from 18-34 range
            'high_count': 2    # 2 numbers from 35-50 range
        }
        
        # Probability adjustments - boost similar numbers but not the exact same ones
        self.number_boosts = {
            # Adjacent to May 6 numbers get boost
            7: 1.5, 9: 1.5,           # Near 8
            21: 1.5, 22: 1.5, 25: 1.5, 26: 1.5,  # Near 23-24
            45: 1.5, 46: 1.5, 49: 1.5, 50: 1.5   # Near 47-48
        }
        
        # Star boosts - still favor 4 and 9 but include others
        self.star_boosts = {
            4: 2.0, 9: 2.0,            # May 6 stars still good
            2: 1.3, 3: 1.5, 7: 1.5, 10: 1.5  # Other historically frequent stars
        }
        
        # Hot and cold numbers
        self.hot_numbers = [5, 7, 15, 17, 19, 20, 23, 27, 31, 37, 44, 49]
        self.cold_numbers = [1, 10, 13, 14, 26, 36, 38, 42, 45, 46]
        self.hot_stars = [2, 3, 4, 7, 9, 10]
        self.cold_stars = [1, 5, 8, 11]
        
        # Base weights for all numbers and stars
        self.number_weights = {n: 1.0 for n in range(1, 51)}
        self.star_weights = {s: 1.0 for s in range(1, 13)}
        
        # Get historical draws to analyze patterns
        self.draws = self.load_data_from_db()
        
        # Initialize with 3-draw pattern analysis
        self.analyze_recent_patterns(3)
        
        # Apply all weights
        self._apply_weights()
        
        # Discourage exact May 6 numbers to avoid duplication
        self._apply_penalties()
    
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
    
    def analyze_recent_patterns(self, num_draws=3):
        """
        Analyze patterns in the most recent draws
        
        Args:
            num_draws: Number of most recent draws to analyze
        """
        if self.draws is None or len(self.draws) == 0:
            logger.warning("No draw data available for pattern analysis")
            return
            
        # Get most recent draws
        recent_draws = self.draws.sort_values('date', ascending=False).head(num_draws)
        
        if len(recent_draws) == 0:
            return
            
        # Analyze number frequencies
        num_freqs = {}
        star_freqs = {}
        
        for _, draw in recent_draws.iterrows():
            for i in range(1, 6):
                num = draw[f'n{i}']
                num_freqs[num] = num_freqs.get(num, 0) + 1
                
            for i in range(1, 3):
                star = draw[f's{i}']
                star_freqs[star] = star_freqs.get(star, 0) + 1
        
        # Store numbers that appeared multiple times
        self.recent_repeat_numbers = [n for n, freq in num_freqs.items() if freq > 1]
        self.recent_repeat_stars = [s for s, freq in star_freqs.items() if freq > 1]
        
        # Analyze patterns in distribution
        self.recent_low_count = 0
        self.recent_mid_count = 0
        self.recent_high_count = 0
        
        for _, draw in recent_draws.iterrows():
            for i in range(1, 6):
                num = draw[f'n{i}']
                if num in self.number_groups['low']:
                    self.recent_low_count += 1
                elif num in self.number_groups['mid']:
                    self.recent_mid_count += 1
                else:
                    self.recent_high_count += 1
        
        # Determine average distribution
        total_numbers = len(recent_draws) * 5
        self.recent_low_ratio = self.recent_low_count / total_numbers
        self.recent_mid_ratio = self.recent_mid_count / total_numbers
        self.recent_high_ratio = self.recent_high_count / total_numbers
        
        # Adjust optimal distribution based on recent patterns
        if self.recent_low_ratio > 0.3:
            self.optimal_distribution['low_count'] += 1
            self.optimal_distribution['mid_count'] -= 1
        elif self.recent_high_ratio > 0.5:
            self.optimal_distribution['high_count'] += 1
            self.optimal_distribution['mid_count'] -= 1
            
        # Cap at minimum 1 for each range
        for key in self.optimal_distribution:
            self.optimal_distribution[key] = max(1, self.optimal_distribution[key])
            
        # Ensure total is 5
        total = sum(self.optimal_distribution.values())
        if total > 5:
            # Adjust down proportionally
            max_key = max(self.optimal_distribution, key=self.optimal_distribution.get)
            self.optimal_distribution[max_key] -= (total - 5)
        elif total < 5:
            # Adjust up proportionally
            max_key = max(self.optimal_distribution, key=self.optimal_distribution.get)
            self.optimal_distribution[max_key] += (5 - total)
    
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
        
        # Apply boosts based on recent repeat numbers
        if hasattr(self, 'recent_repeat_numbers'):
            for num in self.recent_repeat_numbers:
                self.number_weights[num] *= 1.3
                
        if hasattr(self, 'recent_repeat_stars'):
            for star in self.recent_repeat_stars:
                self.star_weights[star] *= 1.3
    
    def _apply_penalties(self):
        """Apply penalties to discourage exact duplication of May 6 numbers"""
        # Reduce weight of exact May 6 combination to avoid duplication
        for num in self.may6_draw['numbers']:
            self.number_weights[num] *= 0.6
        
        # But don't penalize the stars too much
        for star in self.may6_draw['stars']:
            self.star_weights[star] *= 0.9
    
    def generate_optimized_combination(self, risk_level=0.5):
        """
        Generate an optimized combination for May 9
        
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
        
        # Exclude exact May 6 numbers with high probability
        for exclude_num in [23, 24]:
            if exclude_num in mid_nums and random.random() < 0.9:
                mid_nums.remove(exclude_num)
        
        # Select mid range numbers
        if mid_nums:
            mid_weights = [adjusted_weights[n] for n in mid_nums]
            sum_weights = sum(mid_weights)
            mid_probs = [w/sum_weights for w in mid_weights] if sum_weights > 0 else None
            
            if mid_probs:
                chosen_mid = np.random.choice(
                    mid_nums,
                    size=min(self.optimal_distribution['mid_count'], len(mid_nums)),
                    replace=False,
                    p=mid_probs
                )
                selected_numbers.extend(chosen_mid)
        
        # Select from high range (35-50)
        high_nums = list(self.number_groups['high'])
        
        # Exclude exact May 6 numbers with high probability
        for exclude_num in [47, 48]:
            if exclude_num in high_nums and random.random() < 0.9:
                high_nums.remove(exclude_num)
        
        # Select high range numbers
        if high_nums:
            high_weights = [adjusted_weights[n] for n in high_nums]
            sum_weights = sum(high_weights)
            high_probs = [w/sum_weights for w in high_weights] if sum_weights > 0 else None
            
            if high_probs:
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
            
            # Exclude May 6 numbers with high probability
            for exclude_num in self.may6_draw['numbers']:
                if exclude_num in remaining_nums and random.random() < 0.8:
                    remaining_nums.remove(exclude_num)
            
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
                # If somehow we've excluded all numbers, just pick a random one
                new_num = random.randint(1, 50)
                if new_num not in selected_numbers:
                    selected_numbers.append(new_num)
        
        # Select 3 stars - include at least one May 6 star (they performed well)
        selected_stars = []
        
        # Try to include exactly one of the May 6 stars
        may6_stars = [4, 9]
        random.shuffle(may6_stars)  # Randomize order
        
        if random.random() < 0.7:  # 70% chance to include one May 6 star
            selected_stars.append(may6_stars[0])
        
        # Fill remaining star positions (up to 3 total)
        remaining_stars = [s for s in range(1, 13) if s not in selected_stars]
        
        # Exclude remaining May 6 star with some probability
        for exclude_star in may6_stars:
            if exclude_star in remaining_stars and random.random() < 0.6:
                remaining_stars.remove(exclude_star)
        
        if remaining_stars:
            remaining_star_weights = [self.star_weights.get(s, 1.0) for s in remaining_stars]
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
        
        # Check distribution pattern
        low_count = len([n for n in numbers if n in self.number_groups['low']])
        mid_count = len([n for n in numbers if n in self.number_groups['mid']])
        high_count = len([n for n in numbers if n in self.number_groups['high']])
        
        # Bonus for optimal distribution
        if low_count == self.optimal_distribution['low_count']:
            score += 3.0
        if mid_count == self.optimal_distribution['mid_count']:
            score += 3.0
        if high_count == self.optimal_distribution['high_count']:
            score += 3.0
        
        # Bonus for including hot numbers and stars
        hot_num_matches = len(set(numbers).intersection(set(self.hot_numbers)))
        score += hot_num_matches * 1.5
        
        hot_star_matches = len(set(stars).intersection(set(self.hot_stars)))
        score += hot_star_matches * 1.5
        
        # Check for May 6 number matches - PENALIZE duplicate matches
        may6_matches = len(set(numbers).intersection(set(self.may6_draw['numbers'])))
        if may6_matches > 2:  # More than 2 matches is suspicious
            score -= (may6_matches - 2) * 10  # Strong penalty
        
        # But do reward including one May 6 star
        may6_star_matches = len(set(stars).intersection(set(self.may6_draw['stars'])))
        if may6_star_matches == 1:
            score += 5.0  # Good to have one
        elif may6_star_matches > 1:
            score -= 5.0  # Not good to have both
        
        # Bonus for new patterns based on recent analysis
        if hasattr(self, 'recent_repeat_numbers'):
            repeat_matches = len(set(numbers).intersection(set(self.recent_repeat_numbers)))
            score += repeat_matches * 2.0
        
        # Cap score at 100
        return min(max(score, 50), 100)  # Keep between 50-100
    
    def create_ultimate_mix_combination(self, base_combinations):
        """
        Create an ultimate mix combination by analyzing patterns
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
        
        # Apply extra boost for hot numbers/stars
        for num in self.hot_numbers:
            number_counter[num] = number_counter.get(num, 0) + 1
            
        for star in self.hot_stars:
            star_counter[star] = star_counter.get(star, 0) + 1
        
        # Apply penalty for May 6 exact numbers
        for num in self.may6_draw['numbers']:
            number_counter[num] = number_counter.get(num, 0) - 2
            
        # Just a small penalty for May 6 stars
        for star in self.may6_draw['stars']:
            star_counter[star] = max(0, star_counter.get(star, 0) - 1)
        
        # Get the most frequent numbers and stars
        most_common_numbers = [n for n, _ in number_counter.most_common(20) if number_counter[n] > 0]
        most_common_stars = [s for s, _ in star_counter.most_common(10) if star_counter[s] > 0]
        
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
                # Filter out already selected and May 6 numbers
                available_in_range = [n for n in range_nums if n not in selected_numbers 
                                    and n not in self.may6_draw['numbers']]
                
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
            remaining = [n for n in range(1, 51) if n not in selected_numbers 
                        and n not in self.may6_draw['numbers']]
            
            if remaining:
                # Sort by weight
                weighted_nums = [(n, self.number_weights[n]) for n in remaining]
                weighted_nums.sort(key=lambda x: x[1], reverse=True)
                
                # Add top weighted
                selected_numbers.append(weighted_nums[0][0])
            else:
                # If all else fails, pick a random number
                remaining = [n for n in range(1, 51) if n not in selected_numbers]
                if remaining:
                    selected_numbers.append(random.choice(remaining))
                else:
                    break
        
        # Select 3 stars - prioritize common stars but avoid duplicating May 6
        selected_stars = []
        
        # Take exactly one May 6 star if in common stars
        may6_stars_in_common = [s for s in self.may6_draw['stars'] if s in most_common_stars]
        if may6_stars_in_common and random.random() < 0.7:  # 70% chance
            selected_stars.append(random.choice(may6_stars_in_common))
        
        # Fill with most common stars (excluding any May 6 stars already selected)
        for star in most_common_stars:
            if star not in selected_stars and star not in self.may6_draw['stars'] and len(selected_stars) < 3:
                selected_stars.append(star)
                
        # If we still need more, add from remaining May 6 stars
        if len(selected_stars) < 3 and random.random() < 0.3:  # 30% chance
            remaining_may6_stars = [s for s in self.may6_draw['stars'] if s not in selected_stars]
            if remaining_may6_stars:
                selected_stars.append(random.choice(remaining_may6_stars))
        
        # Fill any remaining star positions
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
        
        # Calculate score
        score = self.calculate_combination_score(selected_numbers, selected_stars)
        
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
                'strategy': 'May 9 Optimized (Risk: {:.2f})'.format(risk_level),
                'numbers': numbers,
                'stars': stars,
                'score': score
            })
        
        # Generate ultimate mix combinations
        for i in range(num_ultimate):
            numbers, stars, score = self.create_ultimate_mix_combination(base_combinations)
            
            all_combinations.append({
                'strategy': 'Ultimate Mix for May 9',
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
        except Exception as e:
            logger.error(f"Error saving combination to database: {e}")

def main():
    """Generate optimized combinations for May 9th"""
    print("Generating Optimized Combinations for May 9th Euromillions Draw...")
    optimizer = May9Optimizer()
    
    # Generate combinations
    combinations = optimizer.generate_all_combinations(num_base=8, num_ultimate=4)
    
    # Display results
    print("\nGenerated Combinations:\n")
    
    # Display base combinations
    print("May 9th Optimized Base Combinations:")
    for combo in combinations:
        if "May 9 Optimized" in combo['strategy']:
            print(f"  Strategy: {combo['strategy']}")
            print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
            print(f"  Stars: {', '.join(map(str, combo['stars']))}")
            print(f"  Score: {combo['score']:.2f}\n")
    
    # Display ultimate combinations
    print("\nUltimate Mix Combinations for May 9th:")
    for combo in combinations:
        if combo['strategy'] == "Ultimate Mix for May 9":
            print(f"  Strategy: {combo['strategy']}")
            print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
            print(f"  Stars: {', '.join(map(str, combo['stars']))}")
            print(f"  Score: {combo['score']:.2f}\n")
    
    # Save to database
    save_to_database(combinations)
    print("All combinations have been saved to the database.")

if __name__ == "__main__":
    main()