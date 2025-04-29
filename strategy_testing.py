"""
A/B Testing System for Euromillions Prediction Strategies.

This module provides functionality to evaluate and compare different prediction strategies
based on various performance metrics.
"""

import pandas as pd
import numpy as np
from statistics import EuromillionsStatistics
from strategies import PredictionStrategies
import database
from datetime import datetime, timedelta
import random

class StrategyTester:
    """
    A class for testing and comparing different prediction strategies.
    """
    
    def __init__(self, data=None, statistics=None, strategies=None):
        """
        Initialize the strategy tester with data and strategies.
        
        Parameters:
        -----------
        data : pandas.DataFrame, optional
            Historical Euromillions data
        statistics : EuromillionsStatistics, optional
            Calculated statistics object
        strategies : PredictionStrategies, optional
            Strategy implementation object
        """
        self.data = data
        self.statistics = statistics
        self.strategies = strategies
        self.strategy_methods = {
            "Frequency Strategy": self._generate_frequency_strategy,
            "Mixed Strategy": self._generate_mixed_strategy,
            "Temporal Strategy": self._generate_temporal_strategy,
            "Stratified Sampling": self._generate_stratified_strategy,
            "Coverage Strategy": self._generate_coverage_strategy,
            "Risk/Reward Optimization": self._generate_risk_reward_strategy,
            "Bayesian Model": self._generate_bayesian_strategy,
            "Markov Chain Model": self._generate_markov_strategy,
            "Time Series Model": self._generate_time_series_strategy,
            "Anti-Cognitive Bias": self._generate_cognitive_bias_strategy
        }
        
    def setup_test_environment(self, test_period=30, training_period=None):
        """
        Set up a test environment by splitting data into training and evaluation sets.
        
        Parameters:
        -----------
        test_period : int
            Number of most recent draws to use for testing
        training_period : int, optional
            Number of draws to use for training (excluding test_period).
            If None, use all available data except test_period.
            
        Returns:
        --------
        dict
            Dictionary containing training and test datasets
        """
        if self.data is None:
            # Get data from database
            self.data = database.get_all_draws()
            
        # Ensure data is sorted by date (newest first)
        self.data = self.data.sort_values(by='draw_date', ascending=False).reset_index(drop=True)
        
        # Split data into training and test sets
        test_data = self.data.iloc[:test_period].copy()
        
        if training_period is None:
            training_data = self.data.iloc[test_period:].copy()
        else:
            training_data = self.data.iloc[test_period:test_period + training_period].copy()
        
        # Reset indices
        training_data = training_data.reset_index(drop=True)
        test_data = test_data.reset_index(drop=True)
        
        # Create statistics object for training data
        training_stats = EuromillionsStatistics(training_data)
        
        # Create strategies object with training data
        training_strategies = PredictionStrategies(training_stats)
        
        # Store test environment
        self.test_env = {
            'training_data': training_data,
            'test_data': test_data,
            'training_stats': training_stats,
            'training_strategies': training_strategies
        }
        
        return self.test_env
    
    def run_ab_test(self, strategies_to_test=None, num_combinations=10, iterations=5, metrics=None):
        """
        Run an A/B test comparing multiple strategies.
        
        Parameters:
        -----------
        strategies_to_test : list, optional
            List of strategy names to test. If None, test all available strategies.
        num_combinations : int
            Number of combinations to generate per strategy
        iterations : int
            Number of test iterations to run (with different random seeds)
        metrics : list, optional
            List of metrics to evaluate. If None, use all available metrics.
            
        Returns:
        --------
        dict
            Dictionary containing test results for each strategy and metric
        """
        if not hasattr(self, 'test_env'):
            self.setup_test_environment()
            
        if strategies_to_test is None:
            strategies_to_test = list(self.strategy_methods.keys())
            
        if metrics is None:
            metrics = [
                'hit_rate',                 # How many numbers are correctly predicted
                'full_match_rate',          # How often all 7 numbers are correctly predicted
                'partial_match_rate',       # How often some matches occur (min 2 numbers + 1 star)
                'prize_simulation',         # Simulated prize money
                'average_distance',         # Average distance to actual drawn numbers
                'strategy_consistency',     # Consistency of strategy across iterations
                'pattern_analysis',         # How well the strategy captures patterns
                'diversity_score'           # Diversity of generated combinations
            ]
        
        # Initialize results dictionary
        results = {
            'strategy_names': strategies_to_test,
            'metrics': metrics,
            'iterations': iterations,
            'num_combinations': num_combinations,
            'detailed_results': {},
            'summary': {}
        }
        
        # Run test for each strategy
        for strategy_name in strategies_to_test:
            results['detailed_results'][strategy_name] = self._test_strategy(
                strategy_name, num_combinations, iterations, metrics
            )
        
        # Compile summary
        for metric in metrics:
            results['summary'][metric] = {}
            for strategy_name in strategies_to_test:
                avg_score = np.mean(results['detailed_results'][strategy_name][metric])
                results['summary'][metric][strategy_name] = avg_score
        
        # Calculate overall rankings
        results['rankings'] = self._calculate_rankings(results['summary'])
        
        # Store results in database
        self._save_test_results(results)
        
        return results
    
    def _test_strategy(self, strategy_name, num_combinations, iterations, metrics):
        """
        Test a specific strategy over multiple iterations.
        
        Parameters:
        -----------
        strategy_name : str
            Name of the strategy to test
        num_combinations : int
            Number of combinations to generate
        iterations : int
            Number of iterations to run
        metrics : list
            List of metrics to evaluate
            
        Returns:
        --------
        dict
            Dictionary containing test results for each metric and iteration
        """
        if strategy_name not in self.strategy_methods:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        # Initialize results
        results = {metric: [] for metric in metrics}
        
        # Run iterations
        for i in range(iterations):
            # Set a different random seed for each iteration
            random.seed(i * 100)
            
            # Generate combinations using strategy
            combinations = self.strategy_methods[strategy_name](num_combinations)
            
            # Evaluate combinations against test data
            eval_results = self._evaluate_combinations(combinations, metrics)
            
            # Store results
            for metric in metrics:
                results[metric].append(eval_results[metric])
        
        return results
    
    def _evaluate_combinations(self, combinations, metrics):
        """
        Evaluate combinations against test data using specified metrics.
        
        Parameters:
        -----------
        combinations : list
            List of combination dictionaries
        metrics : list
            List of metrics to evaluate
            
        Returns:
        --------
        dict
            Dictionary containing evaluation results for each metric
        """
        results = {}
        
        # Get actual drawn numbers/stars from test data
        actual_draws = []
        for _, row in self.test_env['test_data'].iterrows():
            actual_draws.append({
                'numbers': [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']],
                'stars': [row['s1'], row['s2']]
            })
        
        # Calculate hit rate (average number of correctly predicted numbers across all combinations)
        if 'hit_rate' in metrics:
            hit_rates = []
            for combo in combinations:
                combo_hit_rates = []
                for actual in actual_draws:
                    # Calculate number matches
                    num_matches = len(set(combo['numbers']).intersection(set(actual['numbers'])))
                    # Calculate star matches
                    star_matches = len(set(combo['stars']).intersection(set(actual['stars'])))
                    # Calculate overall hit rate (weighted: numbers = 0.7, stars = 0.3)
                    hit_rate = 0.7 * (num_matches / 5) + 0.3 * (star_matches / 2)
                    combo_hit_rates.append(hit_rate)
                hit_rates.append(np.mean(combo_hit_rates))
            results['hit_rate'] = np.mean(hit_rates)
        
        # Calculate full match rate (matching all 7 numbers)
        if 'full_match_rate' in metrics:
            full_matches = 0
            total_comparisons = len(combinations) * len(actual_draws)
            for combo in combinations:
                for actual in actual_draws:
                    # Check if all numbers match
                    if (set(combo['numbers']) == set(actual['numbers']) and 
                        set(combo['stars']) == set(actual['stars'])):
                        full_matches += 1
            results['full_match_rate'] = full_matches / total_comparisons
        
        # Calculate partial match rate (prizes: min 2 numbers + 1 star)
        if 'partial_match_rate' in metrics:
            partial_matches = 0
            total_comparisons = len(combinations) * len(actual_draws)
            for combo in combinations:
                for actual in actual_draws:
                    # Count number matches
                    num_matches = len(set(combo['numbers']).intersection(set(actual['numbers'])))
                    # Count star matches
                    star_matches = len(set(combo['stars']).intersection(set(actual['stars'])))
                    # Check if it would win any prize (min 2 numbers + 1 star or 1 number + 2 stars)
                    if (num_matches >= 2 and star_matches >= 1) or (num_matches >= 1 and star_matches == 2):
                        partial_matches += 1
            results['partial_match_rate'] = partial_matches / total_comparisons
        
        # Calculate prize simulation (estimated prize money)
        if 'prize_simulation' in metrics:
            total_prize = 0
            for combo in combinations:
                combo_prize = 0
                for actual in actual_draws:
                    # Count number matches
                    num_matches = len(set(combo['numbers']).intersection(set(actual['numbers'])))
                    # Count star matches
                    star_matches = len(set(combo['stars']).intersection(set(actual['stars'])))
                    
                    # Calculate prize based on matches (rough estimates of average Euromillions prizes)
                    if num_matches == 5 and star_matches == 2:
                        combo_prize += 30000000  # Jackpot (average estimate)
                    elif num_matches == 5 and star_matches == 1:
                        combo_prize += 500000
                    elif num_matches == 5 and star_matches == 0:
                        combo_prize += 50000
                    elif num_matches == 4 and star_matches == 2:
                        combo_prize += 5000
                    elif num_matches == 4 and star_matches == 1:
                        combo_prize += 200
                    elif num_matches == 4 and star_matches == 0:
                        combo_prize += 100
                    elif num_matches == 3 and star_matches == 2:
                        combo_prize += 90
                    elif num_matches == 3 and star_matches == 1:
                        combo_prize += 15
                    elif num_matches == 3 and star_matches == 0:
                        combo_prize += 10
                    elif num_matches == 2 and star_matches == 2:
                        combo_prize += 20
                    elif num_matches == 2 and star_matches == 1:
                        combo_prize += 8
                    elif num_matches == 1 and star_matches == 2:
                        combo_prize += 10
                    # No prize for other combinations
                
                # Add to total
                total_prize += combo_prize
            
            # Calculate average prize per combination
            results['prize_simulation'] = total_prize / len(combinations)
        
        # Calculate average distance to actual drawn numbers
        if 'average_distance' in metrics:
            distances = []
            for combo in combinations:
                for actual in actual_draws:
                    # Calculate Euclidean distance between number sets
                    num_distance = 0
                    for n1 in combo['numbers']:
                        min_dist = min(abs(n1 - n2) for n2 in actual['numbers'])
                        num_distance += min_dist
                    
                    # Calculate distance for stars
                    star_distance = 0
                    for s1 in combo['stars']:
                        min_dist = min(abs(s1 - s2) for s2 in actual['stars'])
                        star_distance += min_dist
                    
                    # Combine distances (weighted)
                    total_distance = (num_distance / 5) * 0.7 + (star_distance / 2) * 0.3
                    distances.append(total_distance)
            
            # Lower distance is better
            results['average_distance'] = np.mean(distances)
        
        # Calculate strategy consistency (variation across combinations)
        if 'strategy_consistency' in metrics:
            # Calculate consistency of number distribution
            all_numbers = []
            for combo in combinations:
                all_numbers.extend(combo['numbers'])
            
            # Count frequency of each number
            number_counts = {}
            for n in range(1, 51):
                number_counts[n] = all_numbers.count(n)
            
            # Calculate standard deviation of counts
            count_std = np.std(list(number_counts.values()))
            
            # Normalize to [0, 1] where 1 is perfectly consistent
            max_possible_std = np.std([len(combinations) * 5] + [0] * 49)  # Most extreme case
            normalized_consistency = 1 - (count_std / max_possible_std)
            
            results['strategy_consistency'] = normalized_consistency
        
        # Calculate pattern analysis score
        if 'pattern_analysis' in metrics:
            pattern_scores = []
            
            # Analyze patterns in actual draws
            actual_patterns = self._extract_patterns(actual_draws)
            
            # Compare to patterns in generated combinations
            for combo in combinations:
                combo_pattern = {
                    'even_odd_ratio': len([n for n in combo['numbers'] if n % 2 == 0]) / 5,
                    'sum': sum(combo['numbers']),
                    'range_spread': max(combo['numbers']) - min(combo['numbers']),
                    'star_sum': sum(combo['stars'])
                }
                
                # Calculate similarity to actual patterns
                similarity = (
                    (1 - abs(combo_pattern['even_odd_ratio'] - actual_patterns['even_odd_ratio'])) * 0.3 +
                    (1 - abs(combo_pattern['sum'] - actual_patterns['sum']) / 150) * 0.3 +
                    (1 - abs(combo_pattern['range_spread'] - actual_patterns['range_spread']) / 45) * 0.2 +
                    (1 - abs(combo_pattern['star_sum'] - actual_patterns['star_sum']) / 25) * 0.2
                )
                pattern_scores.append(similarity)
            
            results['pattern_analysis'] = np.mean(pattern_scores)
        
        # Calculate diversity score
        if 'diversity_score' in metrics:
            # Calculate unique numbers/stars used
            unique_numbers = set()
            unique_stars = set()
            for combo in combinations:
                unique_numbers.update(combo['numbers'])
                unique_stars.update(combo['stars'])
                
            # Calculate diversity as % of possible numbers used
            number_diversity = len(unique_numbers) / 50
            star_diversity = len(unique_stars) / 12
            
            # Combine scores (weighted)
            results['diversity_score'] = 0.7 * number_diversity + 0.3 * star_diversity
        
        return results
    
    def _extract_patterns(self, draws):
        """
        Extract patterns from a set of draws.
        
        Parameters:
        -----------
        draws : list
            List of draw dictionaries with 'numbers' and 'stars'
            
        Returns:
        --------
        dict
            Dictionary containing extracted patterns
        """
        even_odd_ratios = []
        sums = []
        range_spreads = []
        star_sums = []
        
        for draw in draws:
            # Calculate even-odd ratio
            even_count = len([n for n in draw['numbers'] if n % 2 == 0])
            even_odd_ratios.append(even_count / 5)
            
            # Calculate sum
            sums.append(sum(draw['numbers']))
            
            # Calculate range spread
            range_spreads.append(max(draw['numbers']) - min(draw['numbers']))
            
            # Calculate star sum
            star_sums.append(sum(draw['stars']))
        
        # Return average patterns
        return {
            'even_odd_ratio': np.mean(even_odd_ratios),
            'sum': np.mean(sums),
            'range_spread': np.mean(range_spreads),
            'star_sum': np.mean(star_sums)
        }
    
    def _calculate_rankings(self, summary):
        """
        Calculate overall rankings based on all metrics.
        
        Parameters:
        -----------
        summary : dict
            Summary of test results
            
        Returns:
        --------
        dict
            Dictionary containing rankings for each strategy
        """
        # Initialize rankings
        metrics = list(summary.keys())
        strategies = list(summary[metrics[0]].keys())
        rankings = {strategy: [] for strategy in strategies}
        
        # Determine if metric should be maximized or minimized
        minimize_metrics = ['average_distance']
        
        # Calculate ranking for each metric
        for metric in metrics:
            # Get scores for this metric
            scores = [(strategy, summary[metric][strategy]) for strategy in strategies]
            
            # Sort based on whether to maximize or minimize
            if metric in minimize_metrics:
                scores.sort(key=lambda x: x[1])  # Lower is better
            else:
                scores.sort(key=lambda x: x[1], reverse=True)  # Higher is better
            
            # Assign rankings
            for rank, (strategy, _) in enumerate(scores):
                rankings[strategy].append(rank + 1)  # 1-based ranking
        
        # Calculate average ranking
        avg_rankings = {}
        for strategy in strategies:
            avg_rankings[strategy] = np.mean(rankings[strategy])
        
        # Sort strategies by average ranking
        sorted_rankings = sorted(avg_rankings.items(), key=lambda x: x[1])
        
        # Format results
        result = {
            'detailed_rankings': rankings,
            'average_rankings': avg_rankings,
            'overall_ranking': [strategy for strategy, _ in sorted_rankings]
        }
        
        return result
    
    def _save_test_results(self, results):
        """
        Save test results to database.
        
        Parameters:
        -----------
        results : dict
            Dictionary containing test results
            
        Returns:
        --------
        bool
            True if successful, False otherwise
        """
        try:
            # Serialize results for database storage
            import json
            serialized_results = json.dumps(results)
            
            # Save to database
            database.save_strategy_test_results(
                test_date=datetime.now(),
                strategies_tested=','.join(results['strategy_names']),
                iterations=results['iterations'],
                num_combinations=results['num_combinations'],
                results=serialized_results
            )
            
            return True
        except Exception as e:
            print(f"Error saving test results: {str(e)}")
            return False
    
    # Strategy generation methods for testing
    def _generate_frequency_strategy(self, num_combinations):
        return self.test_env['training_strategies'].frequency_strategy(
            num_combinations=num_combinations, 
            recent_weight=0.6
        )
    
    def _generate_mixed_strategy(self, num_combinations):
        return self.test_env['training_strategies'].mixed_strategy(
            num_combinations=num_combinations,
            hot_ratio=0.7
        )
    
    def _generate_temporal_strategy(self, num_combinations):
        return self.test_env['training_strategies'].temporal_strategy(
            num_combinations=num_combinations,
            lookback_period=30
        )
    
    def _generate_stratified_strategy(self, num_combinations):
        return self.test_env['training_strategies'].stratified_sampling_strategy(
            num_combinations=num_combinations,
            strata_type="pattern",
            balance_factor=0.7
        )
    
    def _generate_coverage_strategy(self, num_combinations):
        return self.test_env['training_strategies'].coverage_strategy(
            num_combinations=num_combinations,
            balanced=True
        )
    
    def _generate_risk_reward_strategy(self, num_combinations):
        return self.test_env['training_strategies'].risk_reward_strategy(
            num_combinations=num_combinations,
            risk_level=5
        )
    
    def _generate_bayesian_strategy(self, num_combinations):
        return self.test_env['training_strategies'].bayesian_strategy(
            num_combinations=num_combinations,
            recent_draws_count=20,
            prior_type="empirical",
            update_method="sequential",
            smoothing_factor=0.1
        )
    
    def _generate_markov_strategy(self, num_combinations):
        return self.test_env['training_strategies'].markov_strategy(
            num_combinations=num_combinations,
            lag=1
        )
    
    def _generate_time_series_strategy(self, num_combinations):
        return self.test_env['training_strategies'].time_series_strategy(
            num_combinations=num_combinations,
            window_size=10
        )
    
    def _generate_cognitive_bias_strategy(self, num_combinations):
        return self.test_env['training_strategies'].cognitive_bias_strategy(
            num_combinations=num_combinations
        )