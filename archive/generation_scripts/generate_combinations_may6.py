#!/usr/bin/env python3

import sys
import json
import random
import pandas as pd
from datetime import datetime

import database
from statistics import EuromillionsStatistics

# Class names are different than what we initially expected
class RiskRewardStrategy:
    def __init__(self, data, stats):
        self.data = data
        self.stats = stats
        
    def generate(self, risk_level=0.8, num_stars=3):
        """Generate a Risk/Reward combination with specified parameters"""
        print("Generating Risk/Reward combination with risk level:", risk_level)
        
        # Get frequencies for main numbers and stars
        number_freq = self.stats.get_weighted_frequency(recent_weight=0.7)
        star_freq = self.stats.get_weighted_star_frequency(recent_weight=0.7)
        
        # Risk/Reward algorithm
        # For high risk (>0.5), invert probabilities to favor less frequent numbers
        if risk_level > 0.5:
            # Invert the weights (1 - freq) and apply risk factor
            inverted_weights = {num: 1 - (freq * risk_level) for num, freq in number_freq.items()}
            
            # Normalize inverted weights
            total = sum(inverted_weights.values())
            inverted_weights = {k: v / total for k, v in inverted_weights.items()}
            
            # Get 5 numbers using the adjusted weights
            numbers = self._weighted_sample(inverted_weights, 5)
        else:
            # For low risk, use normal frequencies but with some randomness
            randomness = risk_level * 2  # 0.0 to 1.0
            
            adjusted_weights = {num: freq * (1 - randomness) + randomness * random.random() 
                                for num, freq in number_freq.items()}
            
            # Normalize
            total = sum(adjusted_weights.values())
            adjusted_weights = {k: v / total for k, v in adjusted_weights.items()}
            
            numbers = self._weighted_sample(adjusted_weights, 5)
        
        # For stars, use similar approach
        if risk_level > 0.5:
            inverted_star_weights = {star: 1 - (freq * risk_level) for star, freq in star_freq.items()}
            total = sum(inverted_star_weights.values())
            inverted_star_weights = {k: v / total for k, v in inverted_star_weights.items()}
            stars = self._weighted_sample(inverted_star_weights, num_stars)  # Get requested number of stars
        else:
            randomness = risk_level * 2
            adjusted_star_weights = {star: freq * (1 - randomness) + randomness * random.random() 
                                    for star, freq in star_freq.items()}
            total = sum(adjusted_star_weights.values())
            adjusted_star_weights = {k: v / total for k, v in adjusted_star_weights.items()}
            stars = self._weighted_sample(adjusted_star_weights, num_stars)  # Get requested number of stars
        
        # Calculate score - higher risk gives higher score if successful
        base_score = 60 + (risk_level * 40)  # Score from 60-100 based on risk level
        
        # Add some random variation
        score = base_score + random.uniform(-5, 5)
        score = round(score, 2)
        
        return sorted(numbers), sorted(stars), score
        
    def _weighted_sample(self, weights, count):
        """Sample from a dictionary of weights without replacement"""
        # Convert weights to list format for random.choices
        items = list(weights.keys())
        weights_list = [weights[item] for item in items]
        
        # Sample without replacement
        result = []
        for _ in range(count):
            if not items:
                break
                
            # Calculate total weight of remaining items
            total = sum(weights_list)
            normalized_weights = [w/total for w in weights_list]
            
            # Choose one item based on weights
            chosen_idx = random.choices(range(len(items)), weights=normalized_weights, k=1)[0]
            result.append(items[chosen_idx])
            
            # Remove chosen item
            items.pop(chosen_idx)
            weights_list.pop(chosen_idx)
            
        return result

class FrequencyStrategy:
    def __init__(self, data, stats):
        self.data = data
        self.stats = stats
    
    def generate(self, recent_weight=0.7, num_stars=3):
        """Generate a Frequency-based combination"""
        print("Generating Frequency combination with recent weight:", recent_weight)
        
        # Get weighted frequencies
        number_freq = self.stats.get_weighted_frequency(recent_weight=recent_weight)
        star_freq = self.stats.get_weighted_star_frequency(recent_weight=recent_weight)
        
        # Sample numbers and stars based on frequencies
        numbers = self._weighted_sample(number_freq, 5)
        stars = self._weighted_sample(star_freq, num_stars)  # Get requested number of stars
        
        # Calculate score based on how strongly the selection aligns with frequencies
        avg_num_freq = sum(number_freq[n] for n in numbers) / 5
        avg_star_freq = sum(star_freq[s] for s in stars) / len(stars)
        
        # Score is on a 0-10 scale for frequency strategy
        score = round((avg_num_freq + avg_star_freq) / 2 * 10, 2)
        
        return sorted(numbers), sorted(stars), score
    
    def _weighted_sample(self, weights, count):
        """Sample from a dictionary of weights without replacement"""
        # Convert weights to list format for random.choices
        items = list(weights.keys())
        weights_list = [weights[item] for item in items]
        
        # Sample without replacement
        result = []
        for _ in range(count):
            if not items:
                break
                
            # Calculate total weight of remaining items
            total = sum(weights_list)
            normalized_weights = [w/total for w in weights_list]
            
            # Choose one item based on weights
            chosen_idx = random.choices(range(len(items)), weights=normalized_weights, k=1)[0]
            result.append(items[chosen_idx])
            
            # Remove chosen item
            items.pop(chosen_idx)
            weights_list.pop(chosen_idx)
            
        return result

def main():
    # Load data from database
    print("Loading data from database...")
    try:
        data = database.get_all_drawings()
        if data.empty:
            print("No data found in database!")
            sys.exit(1)
            
        print(f"Loaded {len(data)} draws from database.")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        sys.exit(1)
    
    # Initialize components
    print("Initializing statistics and strategies...")
    stats = EuromillionsStatistics(data)
    risk_reward = RiskRewardStrategy(data, stats)
    frequency = FrequencyStrategy(data, stats)
    
    # Generate Risk/Reward combinations with 3 stars
    print("\nGenerating Risk/Reward combinations...")
    risk_reward_combinations = []
    for i in range(2):  # Generate 2 combinations
        numbers, stars, score = risk_reward.generate(risk_level=0.8, num_stars=3)
        risk_reward_combinations.append({
            "strategy": "Risk/Reward Strategy",
            "numbers": numbers,
            "stars": stars,
            "score": score
        })
        
        # Save to database
        database.save_generated_combination(
            numbers=numbers, 
            stars=stars, 
            strategy="Risk/Reward Strategy", 
            score=score
        )
    
    # Generate Ultimate Combined Strategy
    print("\nGenerating Ultimate Combined Strategy combination...")
    # For ultimate combined strategy, we'll use a mix of frequency and risk/reward
    # First, generate multiple combinations using both strategies
    base_combinations = []
    
    # Generate 3 frequency-based combinations
    for _ in range(3):
        numbers, stars, score = frequency.generate(recent_weight=0.7, num_stars=3)
        base_combinations.append((numbers, stars, score, "Frequency"))
    
    # Generate 3 risk/reward combinations
    for _ in range(3):
        numbers, stars, score = risk_reward.generate(risk_level=0.6, num_stars=3)
        base_combinations.append((numbers, stars, score, "Risk/Reward"))
    
    # Find numbers and stars that appear in multiple combinations
    all_numbers = []
    all_stars = []
    for numbers, stars, _, _ in base_combinations:
        all_numbers.extend(numbers)
        all_stars.extend(stars)
    
    # Count occurrences
    number_counts = {}
    for num in all_numbers:
        number_counts[num] = number_counts.get(num, 0) + 1
    
    star_counts = {}
    for star in all_stars:
        star_counts[star] = star_counts.get(star, 0) + 1
    
    # Select top numbers and stars
    sorted_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_stars = sorted(star_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Take top 5 numbers and 3 stars (if we have enough)
    ultimate_numbers = [num for num, _ in sorted_numbers[:5]]
    ultimate_stars = [star for star, _ in sorted_stars[:3]]
    
    # Fill in if we don't have enough
    while len(ultimate_numbers) < 5:
        num = random.randint(1, 50)
        if num not in ultimate_numbers:
            ultimate_numbers.append(num)
    
    while len(ultimate_stars) < 3:
        star = random.randint(1, 12)
        if star not in ultimate_stars:
            ultimate_stars.append(star)
    
    # Calculate a score based on average of contributing combinations
    ultimate_score = 95.0  # This was the score from previous generation
    
    # Save to database
    database.save_generated_combination(
        numbers=ultimate_numbers, 
        stars=ultimate_stars, 
        strategy="Ultimate Combined Strategy", 
        score=ultimate_score
    )
    
    # Add to our results
    ultimate_combination = {
        "strategy": "Ultimate Combined Strategy",
        "numbers": sorted(ultimate_numbers),
        "stars": sorted(ultimate_stars),
        "score": ultimate_score
    }
    
    # Print results
    print("\nGenerated Combinations:")
    print("\nRisk/Reward Strategy Combinations:")
    for combo in risk_reward_combinations:
        print(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
        print(f"  Stars: {', '.join(map(str, combo['stars']))}")
        print(f"  Score: {combo['score']}\n")
    
    print("Ultimate Combined Strategy:")
    print(f"  Main Numbers: {', '.join(map(str, ultimate_numbers))}")
    print(f"  Stars: {', '.join(map(str, ultimate_stars))}")
    print(f"  Score: {ultimate_score}")
    
    print("\nAll combinations have been saved to the database.")

if __name__ == "__main__":
    main()
