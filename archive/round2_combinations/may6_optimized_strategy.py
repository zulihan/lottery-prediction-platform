import os
import sys
import random
import json
import logging
from datetime import date, timedelta

# Add relative import support
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import database

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class May6OptimizedStrategy:
    """
    Optimized strategy based on May 6, 2025 draw results analysis.
    Focuses on the key insights from the successful draw.
    """
    
    def __init__(self):
        """Initialize the strategy with May 6 insights"""
        # Recent draw results
        self.recent_draw = {
            'date': '2025-05-06',
            'numbers': [8, 23, 24, 47, 48],
            'stars': [4, 9]
        }
        
        # Probability boost for numbers/stars that appeared in the recent draw
        self.boost_numbers = {num: 3.0 for num in self.recent_draw['numbers']}
        self.boost_stars = {star: 4.0 for star in self.recent_draw['stars']}
        
        # Number groups for balanced distribution
        self.number_groups = {
            'low': list(range(1, 18)),
            'mid': list(range(18, 35)),  # Include more from this range (23, 24 appeared)
            'high': list(range(35, 51))  # Include more from this range (47, 48 appeared)
        }
        
        # Optimal distribution based on May 6 analysis
        self.optimal_distribution = {
            'low_count': 1,    # 1-17 range
            'mid_count': 2,    # 18-34 range - increase based on 23, 24 appearing
            'high_count': 2,   # 35-50 range - increase based on 47, 48 appearing
        }
        
        # Lucky patterns from May 6
        self.lucky_patterns = [
            [20, 23, 24],      # Middle range cluster
            [47, 48],          # Consecutive high numbers
            [4, 9]             # Lucky star pair
        ]
        
        # Initialize stats from historical data
        self.hot_numbers = [5, 7, 9, 15, 17, 19, 20, 23, 27, 31, 37, 44, 49]
        self.cold_numbers = [1, 10, 13, 14, 26, 36, 38, 42, 45, 46]
        self.hot_stars = [2, 3, 4, 9, 10]
        self.cold_stars = [1, 5, 8, 11]
    
    def generate_risk_reward_combination(self, risk_level=0.8):
        """
        Generate a risk/reward optimized combination
        
        Args:
            risk_level: 0-1 risk level, higher means more volatile
            
        Returns:
            tuple: (numbers, stars, score)
        """
        logger.info(f"Generating optimized Risk/Reward combination with risk={risk_level}")
        
        # Base weights for all numbers/stars
        number_weights = {n: 1.0 for n in range(1, 51)}
        star_weights = {s: 1.0 for s in range(1, 13)}
        
        # Boost hot numbers/stars
        for num in self.hot_numbers:
            number_weights[num] = number_weights.get(num, 1.0) * 1.5
            
        for star in self.hot_stars:
            star_weights[star] = star_weights.get(star, 1.0) * 1.8
        
        # Apply boosts from recent draw
        for num, boost in self.boost_numbers.items():
            number_weights[num] = number_weights.get(num, 1.0) * boost
            
        for star, boost in self.boost_stars.items():
            star_weights[star] = star_weights.get(star, 1.0) * boost
        
        # Ensure at least one number from 20-25 range (successful in last draw)
        selected_numbers = []
        
        # If taking high risk, include some less frequent numbers
        if risk_level > 0.6:
            # Include some cold numbers for higher risk/reward
            for num in self.cold_numbers[:int(risk_level * 5)]:
                number_weights[num] = number_weights.get(num, 1.0) * 0.8
        
        # Select numbers according to optimal distribution
        # First from low range (1-17)
        low_nums = list(self.number_groups['low'])
        low_weights = [number_weights.get(n, 1.0) for n in low_nums]
        total_weight = sum(low_weights)
        low_probs = [w/total_weight for w in low_weights]
        
        # Select from low range
        if low_nums:
            low_count = self.optimal_distribution['low_count']
            chosen_low = random.choices(low_nums, weights=low_probs, k=min(low_count, len(low_nums)))
            selected_numbers.extend(chosen_low)
        
        # Select from mid range (18-34)
        mid_nums = list(self.number_groups['mid'])
        mid_weights = [number_weights.get(n, 1.0) for n in mid_nums]
        total_weight = sum(mid_weights)
        mid_probs = [w/total_weight for w in mid_weights] if total_weight > 0 else None
        
        # Ensure we include one number from the 20-25 range
        mid_20s = [n for n in mid_nums if 20 <= n <= 25]
        mid_20s_weights = [number_weights.get(n, 1.0) for n in mid_20s]
        total_20s_weight = sum(mid_20s_weights)
        mid_20s_probs = [w/total_20s_weight for w in mid_20s_weights] if total_20s_weight > 0 else None
        
        # Force at least one number from 20-25 range
        if mid_20s and mid_20s_probs:
            chosen_20s = random.choices(mid_20s, weights=mid_20s_probs, k=1)
            selected_numbers.extend(chosen_20s)
            
            # Remove selected numbers from mid range
            for num in chosen_20s:
                if num in mid_nums:
                    mid_nums.remove(num)
                    mid_weights = [number_weights.get(n, 1.0) for n in mid_nums]
                    total_weight = sum(mid_weights)
                    mid_probs = [w/total_weight for w in mid_weights] if total_weight > 0 else None
        
        # Select remaining from mid range
        if mid_nums and mid_probs:
            remaining_mid_count = self.optimal_distribution['mid_count'] - len([n for n in selected_numbers if n in self.number_groups['mid']])
            if remaining_mid_count > 0:
                chosen_mid = random.choices(mid_nums, weights=mid_probs, k=min(remaining_mid_count, len(mid_nums)))
                selected_numbers.extend(chosen_mid)
        
        # Select from high range (35-50)
        high_nums = list(self.number_groups['high'])
        
        # Prioritize 47 and 48 which appeared in the last draw
        high_priority = [47, 48]
        for priority_num in high_priority:
            if priority_num in high_nums and len(selected_numbers) < 5 and random.random() < 0.7:
                selected_numbers.append(priority_num)
                high_nums.remove(priority_num)
        
        # Select remaining from high range
        high_weights = [number_weights.get(n, 1.0) for n in high_nums]
        total_weight = sum(high_weights)
        high_probs = [w/total_weight for w in high_weights] if total_weight > 0 else None
        
        if high_nums and high_probs:
            remaining_high_count = self.optimal_distribution['high_count'] - len([n for n in selected_numbers if n in self.number_groups['high']])
            if remaining_high_count > 0:
                chosen_high = random.choices(high_nums, weights=high_probs, k=min(remaining_high_count, len(high_nums)))
                selected_numbers.extend(chosen_high)
        
        # If we don't have 5 numbers yet, fill with random weighted selection
        all_remaining = [n for n in range(1, 51) if n not in selected_numbers]
        all_weights = [number_weights.get(n, 1.0) for n in all_remaining]
        total_weight = sum(all_weights)
        all_probs = [w/total_weight for w in all_weights] if total_weight > 0 else None
        
        while len(selected_numbers) < 5 and all_remaining and all_probs:
            chosen = random.choices(all_remaining, weights=all_probs, k=1)[0]
            selected_numbers.append(chosen)
            
            # Update remaining numbers
            all_remaining.remove(chosen)
            all_weights = [number_weights.get(n, 1.0) for n in all_remaining]
            total_weight = sum(all_weights)
            all_probs = [w/total_weight for w in all_weights] if total_weight > 0 else None
        
        # Ensure no duplicates and exactly 5 numbers
        selected_numbers = list(set(selected_numbers))
        while len(selected_numbers) < 5:
            new_num = random.randint(1, 50)
            if new_num not in selected_numbers:
                selected_numbers.append(new_num)
        
        # Sort numbers
        selected_numbers.sort()
        
        # Select stars - prioritize the successful pair from May 6 (4, 9)
        selected_stars = []
        
        # Always include at least one of the May 6 stars
        may6_stars = [4, 9]
        if random.random() < 0.9:  # 90% chance to include at least one May 6 star
            selected_stars.append(random.choice(may6_stars))
        
        # Select remaining stars
        remaining_stars = [s for s in range(1, 13) if s not in selected_stars]
        remaining_weights = [star_weights.get(s, 1.0) for s in remaining_stars]
        total_weight = sum(remaining_weights)
        star_probs = [w/total_weight for w in remaining_weights] if total_weight > 0 else None
        
        # Select 2 more stars to have 3 total
        if remaining_stars and star_probs:
            chosen_stars = random.choices(remaining_stars, weights=star_probs, k=min(3 - len(selected_stars), len(remaining_stars)))
            selected_stars.extend(chosen_stars)
        
        # Ensure no duplicates and exactly 3 stars
        selected_stars = list(set(selected_stars))
        while len(selected_stars) < 3:
            new_star = random.randint(1, 12)
            if new_star not in selected_stars:
                selected_stars.append(new_star)
        
        # Sort stars
        selected_stars.sort()
        
        # Calculate score - higher for combinations that include May 6 patterns
        score = 80.0  # Base score
        
        # Boost score based on number of matches with May 6 draw
        num_matches = len(set(selected_numbers).intersection(set(self.recent_draw['numbers'])))
        star_matches = len(set(selected_stars).intersection(set(self.recent_draw['stars'])))
        
        score += num_matches * 2.0   # +2 points per matched number
        score += star_matches * 5.0  # +5 points per matched star
        
        # Boost for distribution matching the optimal pattern
        low_count = len([n for n in selected_numbers if n in self.number_groups['low']])
        mid_count = len([n for n in selected_numbers if n in self.number_groups['mid']])
        high_count = len([n for n in selected_numbers if n in self.number_groups['high']])
        
        if low_count == self.optimal_distribution['low_count']:
            score += 2.0
        if mid_count == self.optimal_distribution['mid_count']:
            score += 3.0
        if high_count == self.optimal_distribution['high_count']:
            score += 3.0
            
        # Boost if includes 20-25 range number
        if any(20 <= n <= 25 for n in selected_numbers):
            score += 3.0
            
        # Risk level affects final score (higher risk = potentially higher score)
        score += risk_level * 5.0
        
        return selected_numbers, selected_stars, min(score, 100.0)
    
    def generate_ultimate_combination(self):
        """
        Generate the ultimate optimized combination based on May 6 analysis
        
        Returns:
            tuple: (numbers, stars, score)
        """
        logger.info("Generating Ultimate May 6 Optimized combination")
        
        # Generate multiple Risk/Reward combinations
        combinations = []
        for _ in range(5):
            risk_level = random.uniform(0.7, 0.9)
            numbers, stars, score = self.generate_risk_reward_combination(risk_level=risk_level)
            combinations.append((numbers, stars, score))
        
        # Count frequency of each number and star across all combinations
        number_counts = {}
        star_counts = {}
        
        for numbers, stars, _ in combinations:
            for num in numbers:
                number_counts[num] = number_counts.get(num, 0) + 1
            for star in stars:
                star_counts[star] = star_counts.get(star, 0) + 1
        
        # Apply extra boost for May 6 draw numbers/stars
        for num in self.recent_draw['numbers']:
            number_counts[num] = number_counts.get(num, 0) + 3
            
        for star in self.recent_draw['stars']:
            star_counts[star] = star_counts.get(star, 0) + 4
            
        # Create probability distributions
        number_items = list(number_counts.items())
        numbers = [n for n, _ in number_items]
        number_weights = [c for _, c in number_items]
        total_weight = sum(number_weights)
        number_probs = [w/total_weight for w in number_weights] if total_weight > 0 else None
        
        star_items = list(star_counts.items())
        stars = [s for s, _ in star_items]
        star_weights = [c for _, c in star_items]
        total_weight = sum(star_weights)
        star_probs = [w/total_weight for w in star_weights] if total_weight > 0 else None
        
        # Select numbers and stars based on distributions
        selected_numbers = []
        if numbers and number_probs:
            # Select according to optimal distribution
            # From low range
            low_indices = [i for i, n in enumerate(numbers) if n in self.number_groups['low']]
            if low_indices:
                low_probs = [number_probs[i] for i in low_indices]
                total_prob = sum(low_probs)
                low_probs = [p/total_prob for p in low_probs] if total_prob > 0 else None
                
                if low_probs:
                    selected_low = random.choices([numbers[i] for i in low_indices], weights=low_probs, k=min(self.optimal_distribution['low_count'], len(low_indices)))
                    selected_numbers.extend(selected_low)
            
            # From mid range
            mid_indices = [i for i, n in enumerate(numbers) if n in self.number_groups['mid'] and n not in selected_numbers]
            if mid_indices:
                mid_probs = [number_probs[i] for i in mid_indices]
                total_prob = sum(mid_probs)
                mid_probs = [p/total_prob for p in mid_probs] if total_prob > 0 else None
                
                if mid_probs:
                    selected_mid = random.choices([numbers[i] for i in mid_indices], weights=mid_probs, k=min(self.optimal_distribution['mid_count'], len(mid_indices)))
                    selected_numbers.extend(selected_mid)
            
            # From high range
            high_indices = [i for i, n in enumerate(numbers) if n in self.number_groups['high'] and n not in selected_numbers]
            if high_indices:
                high_probs = [number_probs[i] for i in high_indices]
                total_prob = sum(high_probs)
                high_probs = [p/total_prob for p in high_probs] if total_prob > 0 else None
                
                if high_probs:
                    selected_high = random.choices([numbers[i] for i in high_indices], weights=high_probs, k=min(self.optimal_distribution['high_count'], len(high_indices)))
                    selected_numbers.extend(selected_high)
        
        # Fill remaining slots if needed
        while len(selected_numbers) < 5:
            remaining = [n for n in range(1, 51) if n not in selected_numbers]
            if remaining:
                selected_numbers.append(random.choice(remaining))
            else:
                break
        
        # Ensure no duplicates and exactly 5 numbers
        selected_numbers = list(set(selected_numbers))
        while len(selected_numbers) < 5:
            new_num = random.randint(1, 50)
            if new_num not in selected_numbers:
                selected_numbers.append(new_num)
        
        # Sort numbers
        selected_numbers.sort()
        
        # Select stars - always include 4 or 9 if possible
        selected_stars = []
        for must_include in [4, 9]:
            if must_include in stars and len(selected_stars) < 2:
                selected_stars.append(must_include)
        
        # Fill remaining stars
        if stars and star_probs and len(selected_stars) < 3:
            # Filter out already selected
            remaining_indices = [i for i, s in enumerate(stars) if s not in selected_stars]
            if remaining_indices:
                remaining_probs = [star_probs[i] for i in remaining_indices]
                total_prob = sum(remaining_probs)
                remaining_probs = [p/total_prob for p in remaining_probs] if total_prob > 0 else None
                
                if remaining_probs:
                    count_needed = 3 - len(selected_stars)
                    chosen_stars = random.choices([stars[i] for i in remaining_indices], weights=remaining_probs, k=min(count_needed, len(remaining_indices)))
                    selected_stars.extend(chosen_stars)
        
        # Ensure no duplicates and exactly 3 stars
        selected_stars = list(set(selected_stars))
        while len(selected_stars) < 3:
            new_star = random.randint(1, 12)
            if new_star not in selected_stars:
                selected_stars.append(new_star)
        
        # Sort stars
        selected_stars.sort()
        
        # Fixed score for ultimate combination
        return selected_numbers, selected_stars, 95.0
    
    def generate_optimized_combinations(self):
        """
        Generate optimized combinations based on May 6 analysis
        
        Returns:
            list: List of optimized combinations
        """
        results = []
        
        # Generate 2 risk/reward combinations
        for _ in range(2):
            risk_level = random.uniform(0.75, 0.9)
            numbers, stars, score = self.generate_risk_reward_combination(risk_level=risk_level)
            results.append({
                'strategy': 'Risk/Reward Strategy',
                'numbers': numbers,
                'stars': stars,
                'score': score
            })
        
        # Generate ultimate combined strategy
        numbers, stars, score = self.generate_ultimate_combination()
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
            # Next week date as target draw date
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
    """Generate optimized combinations based on May 6 analysis"""
    print("Initializing May 6 optimized strategy...")
    strategy = May6OptimizedStrategy()
    
    print("\nGenerating optimized combinations based on May 6 draw analysis...")
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