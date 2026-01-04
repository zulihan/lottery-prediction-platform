"""
Separate strategies for Lucky Numbers (French Loto) and Stars (Euromillions)
These strategies can be backtested and used independently from main number strategies
"""

import pandas as pd
import numpy as np
import random
from collections import Counter, defaultdict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LuckyNumberStrategies:
    """
    Strategies for French Loto lucky number (1-10) selection
    """
    
    def __init__(self, data):
        """
        Initialize with French Loto historical data
        
        Args:
            data: DataFrame with columns including 'lucky' or 'lucky_number'
        """
        self.data = data
        self._analyze_frequencies()
    
    def _analyze_frequencies(self):
        """Analyze lucky number frequencies"""
        lucky_col = 'lucky' if 'lucky' in self.data.columns else 'lucky_number'
        self.lucky_numbers = self.data[lucky_col].tolist()
        self.lucky_freq = Counter(self.lucky_numbers)
        
        # Ensure all numbers 1-10 are represented
        for i in range(1, 11):
            if i not in self.lucky_freq:
                self.lucky_freq[i] = 0
    
    def frequency_strategy(self):
        """
        Select the most frequent lucky number
        
        Returns:
            int: Lucky number
        """
        return self.lucky_freq.most_common(1)[0][0]
    
    def balanced_strategy(self):
        """
        Select from a mix of frequent and medium frequency numbers
        
        Returns:
            int: Lucky number
        """
        sorted_lucky = sorted(self.lucky_freq.items(), key=lambda x: x[1], reverse=True)
        # Top 5 most frequent + medium 5
        top_lucky = [l for l, _ in sorted_lucky[:5]]
        medium_lucky = [l for l, _ in sorted_lucky[5:10]]
        candidates = top_lucky + medium_lucky
        return random.choice(candidates)
    
    def contrarian_strategy(self):
        """
        Select from least frequent (overdue) lucky numbers
        
        Returns:
            int: Lucky number
        """
        sorted_lucky = sorted(self.lucky_freq.items(), key=lambda x: x[1])
        least_frequent = [l for l, _ in sorted_lucky[:5]]
        return random.choice(least_frequent)
    
    def time_series_strategy(self, lookback=50):
        """
        Select based on recent trends
        
        Args:
            lookback: Number of recent draws to analyze
            
        Returns:
            int: Lucky number
        """
        recent_data = self.data.sort_values('date', ascending=False).head(lookback)
        lucky_col = 'lucky' if 'lucky' in recent_data.columns else 'lucky_number'
        recent_lucky = recent_data[lucky_col].tolist()
        recent_freq = Counter(recent_lucky)
        
        if recent_freq:
            return recent_freq.most_common(1)[0][0]
        return self.frequency_strategy()
    
    def hot_cold_balanced_strategy(self):
        """
        Balance between hot (recent) and cold (overall less frequent) numbers
        
        Returns:
            int: Lucky number
        """
        # Get recent hot numbers
        recent_data = self.data.sort_values('date', ascending=False).head(30)
        lucky_col = 'lucky' if 'lucky' in recent_data.columns else 'lucky_number'
        recent_lucky = recent_data[lucky_col].tolist()
        recent_freq = Counter(recent_lucky)
        
        # Hot = high in recent, Cold = low overall
        hot = [l for l, f in recent_freq.most_common(3)]
        cold = [l for l, f in sorted(self.lucky_freq.items(), key=lambda x: x[1])[:3]]
        
        # 70% chance hot, 30% chance cold
        if random.random() < 0.7:
            return random.choice(hot) if hot else self.frequency_strategy()
        else:
            return random.choice(cold) if cold else self.frequency_strategy()
    
    def range_balanced_strategy(self):
        """
        Balance between low (1-5) and high (6-10) numbers
        
        Returns:
            int: Lucky number
        """
        low_freq = {l: self.lucky_freq[l] for l in range(1, 6)}
        high_freq = {l: self.lucky_freq[l] for l in range(6, 11)}
        
        # 50/50 chance for low or high
        if random.random() < 0.5:
            return max(low_freq.items(), key=lambda x: x[1])[0]
        else:
            return max(high_freq.items(), key=lambda x: x[1])[0]
    
    def weighted_random_strategy(self):
        """
        Weighted random selection based on historical frequency
        
        Returns:
            int: Lucky number
        """
        numbers = list(range(1, 11))
        weights = [self.lucky_freq.get(n, 1) for n in numbers]
        weights_sum = sum(weights)
        weights = [w / weights_sum for w in weights]
        return np.random.choice(numbers, p=weights)
    
    def generate(self, strategy='balanced'):
        """
        Generate a lucky number using the specified strategy
        
        Args:
            strategy: Strategy name
            
        Returns:
            dict: {lucky_number, strategy, score}
        """
        strategies = {
            'frequency': self.frequency_strategy,
            'balanced': self.balanced_strategy,
            'contrarian': self.contrarian_strategy,
            'time_series': self.time_series_strategy,
            'hot_cold': self.hot_cold_balanced_strategy,
            'range_balanced': self.range_balanced_strategy,
            'weighted_random': self.weighted_random_strategy
        }
        
        if strategy not in strategies:
            strategy = 'balanced'
        
        lucky = strategies[strategy]()
        
        # Calculate confidence score based on frequency
        freq = self.lucky_freq.get(lucky, 0)
        max_freq = max(self.lucky_freq.values()) if self.lucky_freq else 1
        score = (freq / max_freq) * 100 if max_freq > 0 else 50
        
        return {
            'lucky_number': int(lucky),
            'strategy': strategy,
            'score': round(score, 2)
        }
    
    def get_statistics(self):
        """
        Get statistics about lucky numbers
        
        Returns:
            dict: Statistics
        """
        sorted_freq = sorted(self.lucky_freq.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'most_frequent': sorted_freq[:3],
            'least_frequent': sorted_freq[-3:],
            'frequency_distribution': dict(sorted_freq),
            'total_draws': len(self.data)
        }


class StarStrategies:
    """
    Strategies for Euromillions star (1-12) selection
    """
    
    def __init__(self, data):
        """
        Initialize with Euromillions historical data
        
        Args:
            data: DataFrame with columns s1, s2
        """
        self.data = data
        self._analyze_frequencies()
    
    def _analyze_frequencies(self):
        """Analyze star frequencies"""
        self.all_stars = []
        for _, row in self.data.iterrows():
            self.all_stars.extend([row['s1'], row['s2']])
        
        self.star_freq = Counter(self.all_stars)
        
        # Analyze star pairs
        self.star_pairs = Counter()
        for _, row in self.data.iterrows():
            pair = tuple(sorted([row['s1'], row['s2']]))
            self.star_pairs[pair] += 1
        
        # Ensure all stars 1-12 are represented
        for i in range(1, 13):
            if i not in self.star_freq:
                self.star_freq[i] = 0
    
    def frequency_strategy(self):
        """
        Select the two most frequent stars
        
        Returns:
            list: Two star numbers
        """
        top_stars = [s for s, _ in self.star_freq.most_common(6)]
        return sorted(random.sample(top_stars, 2))
    
    def balanced_strategy(self):
        """
        Mix of frequent and medium frequency stars
        
        Returns:
            list: Two star numbers
        """
        sorted_stars = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
        frequent = [s for s, _ in sorted_stars[:6]]
        medium = [s for s, _ in sorted_stars[6:]]
        
        first = random.choice(frequent)
        remaining = [s for s in medium + frequent if s != first]
        second = random.choice(remaining)
        
        return sorted([first, second])
    
    def contrarian_strategy(self):
        """
        Select from least frequent (overdue) stars
        
        Returns:
            list: Two star numbers
        """
        sorted_stars = sorted(self.star_freq.items(), key=lambda x: x[1])
        least_frequent = [s for s, _ in sorted_stars[:8]]
        return sorted(random.sample(least_frequent, 2))
    
    def range_balanced_strategy(self):
        """
        Balance between low (1-6) and high (7-12) stars
        
        Returns:
            list: Two star numbers
        """
        low_stars = list(range(1, 7))
        high_stars = list(range(7, 13))
        
        low_freq = {s: self.star_freq[s] for s in low_stars}
        high_freq = {s: self.star_freq[s] for s in high_stars}
        
        low_choice = max(low_freq.items(), key=lambda x: x[1])[0]
        high_choice = max(high_freq.items(), key=lambda x: x[1])[0]
        
        return sorted([low_choice, high_choice])
    
    def pair_frequency_strategy(self):
        """
        Select based on most frequent star pairs
        
        Returns:
            list: Two star numbers
        """
        if self.star_pairs:
            top_pairs = [pair for pair, _ in self.star_pairs.most_common(5)]
            pair = random.choice(top_pairs)
            return list(pair)
        return self.frequency_strategy()
    
    def markov_strategy(self):
        """
        Select second star based on first star's transitions
        
        Returns:
            list: Two star numbers
        """
        # Build transition matrix
        transitions = defaultdict(Counter)
        for _, row in self.data.iterrows():
            s1, s2 = sorted([row['s1'], row['s2']])
            transitions[s1][s2] += 1
        
        # Select first star from frequent ones
        first = random.choice([s for s, _ in self.star_freq.most_common(6)])
        
        # Select second based on transitions
        if first in transitions and transitions[first]:
            candidates = list(transitions[first].keys())
            weights = [transitions[first][s] for s in candidates]
            second = random.choices(candidates, weights=weights)[0]
        else:
            remaining = [s for s in range(1, 13) if s != first]
            second = random.choice(remaining)
        
        return sorted([first, second])
    
    def time_series_strategy(self, lookback=50):
        """
        Select based on recent trends
        
        Args:
            lookback: Number of recent draws to analyze
            
        Returns:
            list: Two star numbers
        """
        recent_data = self.data.sort_values('date', ascending=False).head(lookback)
        recent_stars = []
        for _, row in recent_data.iterrows():
            recent_stars.extend([row['s1'], row['s2']])
        
        recent_freq = Counter(recent_stars)
        if recent_freq:
            top_recent = [s for s, _ in recent_freq.most_common(6)]
            return sorted(random.sample(top_recent, 2))
        return self.frequency_strategy()
    
    def weighted_random_strategy(self):
        """
        Weighted random selection based on historical frequency
        
        Returns:
            list: Two star numbers
        """
        stars = list(range(1, 13))
        weights = [self.star_freq.get(s, 1) for s in stars]
        weights_sum = sum(weights)
        weights = [w / weights_sum for w in weights]
        
        selected = np.random.choice(stars, size=2, replace=False, p=weights)
        return sorted(selected.tolist())
    
    def generate(self, strategy='balanced'):
        """
        Generate stars using the specified strategy
        
        Args:
            strategy: Strategy name
            
        Returns:
            dict: {stars, strategy, score}
        """
        strategies = {
            'frequency': self.frequency_strategy,
            'balanced': self.balanced_strategy,
            'contrarian': self.contrarian_strategy,
            'range_balanced': self.range_balanced_strategy,
            'pair_frequency': self.pair_frequency_strategy,
            'markov': self.markov_strategy,
            'time_series': self.time_series_strategy,
            'weighted_random': self.weighted_random_strategy
        }
        
        if strategy not in strategies:
            strategy = 'balanced'
        
        stars = strategies[strategy]()
        
        # Calculate confidence score
        avg_freq = sum(self.star_freq.get(s, 0) for s in stars) / 2
        max_freq = max(self.star_freq.values()) if self.star_freq else 1
        score = (avg_freq / max_freq) * 100 if max_freq > 0 else 50
        
        return {
            'stars': [int(s) for s in stars],
            'strategy': strategy,
            'score': round(score, 2)
        }
    
    def get_statistics(self):
        """
        Get statistics about stars
        
        Returns:
            dict: Statistics
        """
        sorted_freq = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
        sorted_pairs = sorted(self.star_pairs.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'most_frequent': sorted_freq[:3],
            'least_frequent': sorted_freq[-3:],
            'frequency_distribution': dict(sorted_freq),
            'most_common_pairs': sorted_pairs[:5],
            'total_draws': len(self.data)
        }


def backtest_lucky_strategies(data, test_size=0.3):
    """
    Backtest all lucky number strategies
    
    Args:
        data: Full DataFrame
        test_size: Proportion of data to use for testing
        
    Returns:
        dict: Results for each strategy
    """
    # Sort by date and split
    data = data.sort_values('date')
    split_idx = int(len(data) * (1 - test_size))
    train_data = data.iloc[:split_idx]
    test_data = data.iloc[split_idx:]
    
    lucky_col = 'lucky' if 'lucky' in data.columns else 'lucky_number'
    
    strategies = LuckyNumberStrategies(train_data)
    
    results = {}
    strategy_names = ['frequency', 'balanced', 'contrarian', 'time_series', 
                      'hot_cold', 'range_balanced', 'weighted_random']
    
    for strategy in strategy_names:
        matches = 0
        predictions = 0
        
        for _ in range(20):  # Generate 20 predictions per strategy
            for _, actual in test_data.iterrows():
                pred = strategies.generate(strategy)
                predictions += 1
                if pred['lucky_number'] == actual[lucky_col]:
                    matches += 1
        
        win_rate = (matches / predictions * 100) if predictions > 0 else 0
        
        results[strategy] = {
            'predictions': predictions,
            'matches': matches,
            'win_rate': round(win_rate, 2),
            'expected_random': round(10.0, 2)  # 1/10 = 10%
        }
    
    return results


def backtest_star_strategies(data, test_size=0.3):
    """
    Backtest all star strategies
    
    Args:
        data: Full DataFrame
        test_size: Proportion of data to use for testing
        
    Returns:
        dict: Results for each strategy
    """
    # Sort by date and split
    data = data.sort_values('date')
    split_idx = int(len(data) * (1 - test_size))
    train_data = data.iloc[:split_idx]
    test_data = data.iloc[split_idx:]
    
    strategies = StarStrategies(train_data)
    
    results = {}
    strategy_names = ['frequency', 'balanced', 'contrarian', 'range_balanced', 
                      'pair_frequency', 'markov', 'time_series', 'weighted_random']
    
    for strategy in strategy_names:
        full_matches = 0  # Both stars correct
        partial_matches = 0  # One star correct
        predictions = 0
        
        for _ in range(20):  # Generate 20 predictions per strategy
            for _, actual in test_data.iterrows():
                pred = strategies.generate(strategy)
                pred_stars = set(pred['stars'])
                actual_stars = {actual['s1'], actual['s2']}
                
                predictions += 1
                matches = len(pred_stars & actual_stars)
                
                if matches == 2:
                    full_matches += 1
                elif matches == 1:
                    partial_matches += 1
        
        full_rate = (full_matches / predictions * 100) if predictions > 0 else 0
        partial_rate = (partial_matches / predictions * 100) if predictions > 0 else 0
        
        results[strategy] = {
            'predictions': predictions,
            'full_matches': full_matches,
            'partial_matches': partial_matches,
            'full_match_rate': round(full_rate, 2),
            'partial_match_rate': round(partial_rate, 2),
            'expected_random_full': round(1/66 * 100, 2)  # C(12,2) = 66
        }
    
    return results

