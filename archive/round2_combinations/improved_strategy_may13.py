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

class ImprovedMay13Strategy:
    """
    Enhanced strategy for Euromillions based on May 6 and May 9 results analysis.
    This strategy applies lessons learned from both draws and reduces spread
    to concentrate matches within the same combinations.
    """
    
    def __init__(self):
        """Initialize the strategy with insights from May 6 and May 9 draws"""
        # Recent draws data - our foundation patterns
        self.recent_draws = [
            # May 9 draw
            {
                'date': '2025-05-09',
                'numbers': [15, 18, 25, 29, 47],
                'stars': [5, 9]
            },
            # May 6 draw
            {
                'date': '2025-05-06',
                'numbers': [8, 23, 24, 47, 48],
                'stars': [4, 9]
            }
        ]
        
        # Number group ranges
        self.number_groups = {
            'low': list(range(1, 18)),    # 1-17
            'mid': list(range(18, 35)),   # 18-34 - THREE May 9 numbers (18, 25, 29) were here!
            'high': list(range(35, 51))   # 35-50
        }
        
        # Updated optimal distribution based on May 9 results
        self.optimal_distribution = {
            'low_count': 1,    # 1 number from 1-17 range (May 9 had number 15)
            'mid_count': 3,    # 3 numbers from 18-34 range (May 9 had 18, 25, 29)
            'high_count': 1    # 1 number from 35-50 range (May 9 had 47)
        }
        
        # Key patterns observed across both draws
        self.observed_patterns = [
            # Mid-range importance (18-34)
            # Star 9 appeared in BOTH draws
            # Number 47 appeared in BOTH draws
            # Numbers 15, 25, 29 from May 9
            # Numbers 8, 23, 24, 48 from May 6
        ]
        
        # Number boosts based on both draws
        self.number_boosts = {
            # Numbers that appeared in May 9 draw
            15: 3.0, 18: 3.0, 25: 3.0, 29: 3.0, 47: 4.0,  # 47 appeared in BOTH draws!
            
            # Numbers that appeared in May 6 draw
            8: 2.0, 23: 2.0, 24: 2.0, 48: 2.0,
            
            # Numbers adjacent to winners
            14: 1.5, 16: 1.5, 17: 1.5, 19: 1.5,  # Adjacent to 15, 18
            26: 1.5, 27: 1.5, 28: 1.5, 30: 1.5,  # Adjacent to 25, 29
            46: 1.5, 49: 1.5, 50: 1.5,          # Adjacent to 47, 48
            
            # Mid-range numbers (18-34) get additional boost
            # as 3 of 5 numbers in May 9 were in this range
            20: 1.3, 21: 1.3, 22: 1.3, 31: 1.3, 32: 1.3, 33: 1.3, 34: 1.3
        }
        
        # Star boosts based on both draws
        self.star_boosts = {
            9: 5.0,     # Appeared in BOTH May 6 and May 9!
            5: 3.0,     # Appeared in May 9
            4: 2.5,     # Appeared in May 6
            
            # Adjacent to winning stars
            3: 1.5, 6: 1.5, 8: 1.5, 10: 1.5
        }
        
        # Load hot and cold numbers for additional weighting
        self.hot_numbers = [5, 7, 15, 17, 18, 19, 25, 29, 31, 37, 44, 47]
        self.cold_numbers = [1, 10, 13, 14, 26, 36, 38, 42, 45, 46]
        self.hot_stars = [3, 4, 5, 7, 9, 10]
        self.cold_stars = [1, 8, 11, 12]
        
        # Base weights for all numbers and stars
        self.number_weights = {n: 1.0 for n in range(1, 51)}
        self.star_weights = {s: 1.0 for s in range(1, 13)}
        
        # Apply all weights for this strategy
        self._apply_weights()
        
        # Track already generated combinations to avoid duplicates
        self.generated_combinations = []
    
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
        Generate an optimized combination for May 13th
        
        Args:
            risk_level: 0-1 risk level (higher = more volatile/unique numbers)
            
        Returns:
            tuple: (numbers, stars, score)
        """
        # Ensure we include some of the most important numbers and stars
        must_include_numbers = []
        must_include_stars = []
        
        # Must include one of the key pattern numbers with high probability
        if random.random() < (0.8 - (risk_level * 0.3)):
            # Include number 47 (appeared in BOTH May 6 and May 9)
            must_include_numbers.append(47)
        elif random.random() < (0.6 - (risk_level * 0.3)):
            # Include one of the May 9 mid-range numbers
            must_include_numbers.append(random.choice([18, 25, 29]))
        
        # Must include star 9 with high probability (appeared in BOTH draws)
        if random.random() < (0.9 - (risk_level * 0.3)):
            must_include_stars.append(9)
        
        # Possibly include star 5 or 4 (appeared in May 9 and May 6 respectively)
        if random.random() < (0.6 - (risk_level * 0.3)):
            if random.random() < 0.6:  # Slightly favor the more recent May 9 star
                must_include_stars.append(5)
            else:
                must_include_stars.append(4)
        
        # Prepare weights adjusted by risk level and must-include constraints
        adjusted_weights = self.number_weights.copy()
        
        # For higher risk levels, include some less frequent numbers
        if risk_level > 0.5:
            # Add extra randomness for variety
            for num in range(1, 51):
                random_factor = 1.0 + ((random.random() - 0.5) * risk_level)
                adjusted_weights[num] *= random_factor
        
        # Select numbers according to optimal distribution
        selected_numbers = must_include_numbers.copy()  # Start with must-include numbers
        
        # Select remaining numbers by range according to optimal distribution
        remaining_low_count = self.optimal_distribution['low_count']
        remaining_mid_count = self.optimal_distribution['mid_count']
        remaining_high_count = self.optimal_distribution['high_count']
        
        # Adjust counts based on already included numbers
        for num in selected_numbers:
            if num in self.number_groups['low']:
                remaining_low_count -= 1
            elif num in self.number_groups['mid']:
                remaining_mid_count -= 1
            elif num in self.number_groups['high']:
                remaining_high_count -= 1
        
        # Select from low range (1-17)
        if remaining_low_count > 0:
            low_nums = [n for n in self.number_groups['low'] if n not in selected_numbers]
            low_weights = [adjusted_weights[n] for n in low_nums]
            sum_weights = sum(low_weights) if low_weights else 0
            
            if sum_weights > 0:
                low_probs = [w/sum_weights for w in low_weights]
                
                chosen_low = np.random.choice(
                    low_nums, 
                    size=min(remaining_low_count, len(low_nums)),
                    replace=False,
                    p=low_probs
                )
                selected_numbers.extend(chosen_low)
        
        # Select from mid range (18-34) - MORE FOCUS HERE BASED ON MAY 9
        if remaining_mid_count > 0:
            mid_nums = [n for n in self.number_groups['mid'] if n not in selected_numbers]
            mid_weights = [adjusted_weights[n] for n in mid_nums]
            sum_weights = sum(mid_weights) if mid_weights else 0
            
            if sum_weights > 0:
                mid_probs = [w/sum_weights for w in mid_weights]
                
                chosen_mid = np.random.choice(
                    mid_nums, 
                    size=min(remaining_mid_count, len(mid_nums)),
                    replace=False,
                    p=mid_probs
                )
                selected_numbers.extend(chosen_mid)
        
        # Select from high range (35-50)
        if remaining_high_count > 0:
            high_nums = [n for n in self.number_groups['high'] if n not in selected_numbers]
            high_weights = [adjusted_weights[n] for n in high_nums]
            sum_weights = sum(high_weights) if high_weights else 0
            
            if sum_weights > 0:
                high_probs = [w/sum_weights for w in high_weights]
                
                chosen_high = np.random.choice(
                    high_nums, 
                    size=min(remaining_high_count, len(high_nums)),
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
        
        # Select stars - include at least one of the successful stars (9, 5)
        selected_stars = must_include_stars.copy()  # Start with must-include stars
        
        # Fill remaining star positions (up to 3 total)
        remaining_star_count = 3 - len(selected_stars)
        
        if remaining_star_count > 0:
            remaining_stars = [s for s in range(1, 13) if s not in selected_stars]
            
            if remaining_stars:
                remaining_star_weights = [self.star_weights.get(s, 1.0) for s in remaining_stars]
                sum_weights = sum(remaining_star_weights)
                remaining_star_probs = [w/sum_weights for w in remaining_star_weights] if sum_weights > 0 else None
                
                if remaining_star_probs:
                    chosen_stars = np.random.choice(
                        remaining_stars,
                        size=min(remaining_star_count, len(remaining_stars)),
                        replace=False,
                        p=remaining_star_probs
                    )
                    selected_stars.extend(chosen_stars)
        
        # Ensure we have exactly 3 stars
        while len(selected_stars) < 3:
            new_star = random.randint(1, 12)
            if new_star not in selected_stars:
                selected_stars.append(new_star)
        
        # Sort the final selections
        selected_numbers.sort()
        selected_stars.sort()
        
        # Calculate score and check for duplicates
        score = self.calculate_combination_score(selected_numbers, selected_stars)
        
        # Add to generated combinations list
        self.generated_combinations.append((selected_numbers, selected_stars))
        
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
        
        # Check recent draw number matches
        may9_matches = len(set(numbers).intersection(set(self.recent_draws[0]['numbers'])))
        may6_matches = len(set(numbers).intersection(set(self.recent_draws[1]['numbers'])))
        
        # Boost score for May 9 matches
        score += may9_matches * 3.5
        
        # Also boost for May 6 matches but less
        score += may6_matches * 2.0
        
        # Check for matches with number 47 (appeared in BOTH draws)
        if 47 in numbers:
            score += 4.0
        
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
        
        # Check for star 9 (appeared in BOTH draws)
        if 9 in stars:
            score += 5.0
        
        # Check for star 5 (appeared in May 9)
        if 5 in stars:
            score += 3.0
        
        # Check for star 4 (appeared in May 6)
        if 4 in stars:
            score += 2.0
        
        # Bonus for stars adjacent to winning stars
        for star in [3, 6, 8, 10]:
            if star in stars:
                score += 1.0
        
        # Check mid-range importance
        mid_range_count = len([n for n in numbers if 15 <= n <= 34])
        if mid_range_count >= 3:
            score += 3.0
        
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
        
        # Apply extra boost for key pattern numbers/stars
        number_counter[47] += 3  # Appeared in both draws!
        for num in [15, 18, 25, 29]:  # May 9 numbers
            number_counter[num] += 2
            
        star_counter[9] += 3  # Appeared in both draws!
        star_counter[5] += 2  # Appeared in May 9
        
        # Select numbers according to optimal distribution
        selected_numbers = []
        
        # Force include number 47 if it's in the top numbers
        if 47 in [n for n, _ in number_counter.most_common(10)]:
            selected_numbers.append(47)
        
        # Select from each range according to optimal distribution
        remaining_low_count = self.optimal_distribution['low_count']
        remaining_mid_count = self.optimal_distribution['mid_count']
        remaining_high_count = self.optimal_distribution['high_count']
        
        # Adjust counts based on already included numbers
        for num in selected_numbers:
            if num in self.number_groups['low']:
                remaining_low_count -= 1
            elif num in self.number_groups['mid']:
                remaining_mid_count -= 1
            elif num in self.number_groups['high']:
                remaining_high_count -= 1
        
        # Get most common numbers by range
        common_low = [n for n, _ in number_counter.most_common() if n in self.number_groups['low'] and n not in selected_numbers]
        common_mid = [n for n, _ in number_counter.most_common() if n in self.number_groups['mid'] and n not in selected_numbers]
        common_high = [n for n, _ in number_counter.most_common() if n in self.number_groups['high'] and n not in selected_numbers]
        
        # Select from each range
        selected_numbers.extend(common_low[:remaining_low_count])
        selected_numbers.extend(common_mid[:remaining_mid_count])
        selected_numbers.extend(common_high[:remaining_high_count])
        
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
        
        # Select 3 stars - prioritize stars 9 and 5
        selected_stars = []
        
        # Force include star 9 (appeared in BOTH draws)
        if 9 in [s for s, _ in star_counter.most_common(5)]:
            selected_stars.append(9)
        
        # Force include star 5 (appeared in May 9)
        if 5 in [s for s, _ in star_counter.most_common(5)] and 5 not in selected_stars:
            selected_stars.append(5)
        
        # Fill remaining star positions
        remaining_star_count = 3 - len(selected_stars)
        
        if remaining_star_count > 0:
            # Get remaining common stars
            remaining_common_stars = [s for s, _ in star_counter.most_common() if s not in selected_stars]
            
            if remaining_common_stars:
                selected_stars.extend(remaining_common_stars[:remaining_star_count])
        
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
        # Ultimate mix gets a bonus
        score = min(score + 5, 100) 
        
        return selected_numbers, selected_stars, score
    
    def generate_all_combinations(self, num_base=8, num_ultimate=4):
        """
        Generate multiple optimized combinations for May 13th
        
        Args:
            num_base: Number of base combinations to generate
            num_ultimate: Number of ultimate combinations to generate
            
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
                'strategy': 'May 13 Optimized (Risk: {:.2f})'.format(risk_level),
                'numbers': numbers,
                'stars': stars,
                'score': score
            })
        
        # Generate ultimate mix combinations
        for _ in range(num_ultimate):
            numbers, stars, score = self.create_ultimate_mix_combination(base_combinations)
            
            all_combinations.append({
                'strategy': 'Ultimate Mix for May 13',
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
    print("Generating Optimized Combinations for May 13th Euromillions Draw...")
    
    # Create the strategy with enhanced weights based on May 6 AND May 9 analyses
    optimizer = ImprovedMay13Strategy()
    
    # Generate combinations
    combinations = optimizer.generate_all_combinations(num_base=8, num_ultimate=4)
    
    # Display results
    print("\nGenerated Combinations for May 13th:\n")
    
    # Display base combinations
    print("May 13th Optimized Base Combinations:")
    for combo in combinations:
        if "May 13 Optimized" in combo['strategy']:
            print(f"  Strategy: {combo['strategy']}")
            print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
            print(f"  Stars: {', '.join(map(str, combo['stars']))}")
            print(f"  Score: {combo['score']:.2f}\n")
    
    # Display ultimate combinations
    print("\nUltimate Mix Combinations for May 13th:")
    for combo in combinations:
        if "Ultimate Mix" in combo['strategy']:
            print(f"  Strategy: {combo['strategy']}")
            print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
            print(f"  Stars: {', '.join(map(str, combo['stars']))}")
            print(f"  Score: {combo['score']:.2f}\n")
    
    # Save to database
    saved_ids = save_to_database(combinations)
    print(f"Saved {len(saved_ids)} combinations to database.")
    
    # Outline key improvements
    print("\nKey Strategy Improvements Based on May 9th Results Analysis:")
    print("1. Increased focus on mid-range numbers (18-34) where 3 of 5 winning numbers appeared")
    print("2. Strong emphasis on number 47 which appeared in BOTH May 6 and May 9 draws")
    print("3. Prioritized star 9 which also appeared in BOTH May 6 and May 9 draws")
    print("4. Added weight to star 5 which appeared in May 9 draw")
    print("5. Updated optimal distribution to match pattern from May 9 (1 low, 3 mid, 1 high)")
    print("6. Higher concentration of key numbers/stars within same combinations")

if __name__ == "__main__":
    main()