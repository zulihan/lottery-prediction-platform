"""
A/B Testing System for Euromillions Prediction Strategies.

This module provides functionality to evaluate and compare different prediction strategies
based on various performance metrics.
"""

import pandas as pd
import numpy as np
import json
import datetime
import random
from statistics import EuromillionsStatistics 
from strategies import PredictionStrategies
import database

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
        
        # Set up the objects if not provided
        if self.data is None:
            self.data = database.get_all_drawings()
            
        if self.statistics is None and self.data is not None:
            self.statistics = EuromillionsStatistics(self.data)
            
        if self.strategies is None and self.statistics is not None:
            self.strategies = PredictionStrategies(self.statistics)
            
        # Define available metrics
        self.available_metrics = [
            "numbers_match_rate",      # How many numbers matched in test set
            "stars_match_rate",        # How many stars matched in test set
            "coverage_efficiency",     # How well the combinations cover the possible space
            "diversity_score",         # How diverse the generated combinations are
            "historical_similarity",   # Similarity to historical patterns
            "balance_factor"           # Balance of different properties
        ]
    
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
        # Make sure we have data sorted by date
        sorted_data = self.data.sort_values('date', ascending=True).reset_index(drop=True)
        
        # Split the data
        test_data = sorted_data.tail(test_period)
        
        if training_period is not None:
            training_data = sorted_data.iloc[-(test_period + training_period):-test_period]
        else:
            training_data = sorted_data.iloc[:-test_period]
        
        self.test_env = {
            'training_data': training_data,
            'test_data': test_data
        }
        
        # Create new statistics and strategies objects based on training data
        self.test_statistics = EuromillionsStatistics(training_data)
        self.test_strategies = PredictionStrategies(self.test_statistics)
        
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
        # Set up test environment if not already done
        if not hasattr(self, 'test_env'):
            self.setup_test_environment()
        
        # Use all strategies if none specified
        if strategies_to_test is None:
            strategies_to_test = [
                "frequency",
                "time_series", 
                "markov_chain",
                "stratified",
                "bayesian",
                "balanced"
            ]
            
        # Use all metrics if none specified
        if metrics is None:
            metrics = self.available_metrics
        
        # Dictionary to store results
        results = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'iterations': iterations,
            'num_combinations': num_combinations,
            'strategies_tested': strategies_to_test,
            'metrics': metrics,
            'results_by_strategy': {},
            'summary': {}
        }
        
        # Test each strategy
        for strategy in strategies_to_test:
            results['results_by_strategy'][strategy] = self._test_strategy(
                strategy, num_combinations, iterations, metrics
            )
        
        # Create summary statistics across all iterations
        summary = {}
        for strategy in strategies_to_test:
            summary[strategy] = {}
            for metric in metrics:
                # Extract all values for this metric across iterations
                metric_values = [
                    results['results_by_strategy'][strategy]['iterations'][i]['metrics'][metric]
                    for i in range(iterations)
                ]
                
                # Calculate summary statistics
                summary[strategy][metric] = {
                    'mean': np.mean(metric_values),
                    'median': np.median(metric_values),
                    'std': np.std(metric_values),
                    'min': np.min(metric_values),
                    'max': np.max(metric_values)
                }
        
        # Add summary to results
        results['summary'] = summary
        
        # Calculate rankings
        results['rankings'] = self._calculate_rankings(summary)
        
        # Save results to database
        strategies_string = ','.join(strategies_to_test)
        results_json = json.dumps(results)
        database.save_strategy_test_results(
            datetime.datetime.now(),
            strategies_string,
            iterations,
            num_combinations,
            results_json
        )
        
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
        # Dictionary to store results for this strategy
        strategy_results = {
            'strategy': strategy_name,
            'iterations': []
        }
        
        # Run multiple iterations with different random seeds
        for i in range(iterations):
            # Set random seed for reproducibility but different for each iteration
            random_seed = 42 + i
            np.random.seed(random_seed)
            random.seed(random_seed)
            
            # Generate combinations using the selected strategy
            combinations = []
            if strategy_name == "frequency":
                combinations = self._generate_frequency_strategy(num_combinations)
            elif strategy_name == "time_series":
                combinations = self._generate_time_series_strategy(num_combinations)
            elif strategy_name == "markov_chain":
                combinations = self._generate_markov_strategy(num_combinations)
            elif strategy_name == "stratified":
                combinations = self._generate_stratified_strategy(num_combinations)
            elif strategy_name == "bayesian":
                combinations = self._generate_bayesian_strategy(num_combinations)
            elif strategy_name == "balanced":
                combinations = self._generate_mixed_strategy(num_combinations)
            elif strategy_name == "cognitive_bias":
                combinations = self._generate_cognitive_bias_strategy(num_combinations)
            elif strategy_name == "coverage":
                combinations = self._generate_coverage_strategy(num_combinations)
            elif strategy_name == "risk_reward":
                combinations = self._generate_risk_reward_strategy(num_combinations)
            
            # Evaluate the combinations
            eval_results = self._evaluate_combinations(combinations, metrics)
            
            # Store results for this iteration
            iteration_result = {
                'iteration': i,
                'random_seed': random_seed,
                'metrics': eval_results
            }
            strategy_results['iterations'].append(iteration_result)
        
        return strategy_results
    
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
        # Extract test data in a more usable format
        test_draws = []
        for _, row in self.test_env['test_data'].iterrows():
            test_draws.append({
                'date': row['date'],
                'numbers': [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']],
                'stars': [row['s1'], row['s2']]
            })
        
        # Evaluate using each metric
        evaluation = {}
        
        # Calculate number match rate
        if "numbers_match_rate" in metrics:
            total_matches = 0
            max_possible = len(combinations) * len(test_draws) * 5  # 5 numbers per draw
            
            for combo in combinations:
                for draw in test_draws:
                    # Count matches
                    matches = len(set(combo['numbers']).intersection(set(draw['numbers'])))
                    total_matches += matches
            
            evaluation["numbers_match_rate"] = total_matches / max_possible if max_possible > 0 else 0
        
        # Calculate star match rate
        if "stars_match_rate" in metrics:
            total_matches = 0
            max_possible = len(combinations) * len(test_draws) * 2  # 2 stars per draw
            
            for combo in combinations:
                for draw in test_draws:
                    # Count matches
                    matches = len(set(combo['stars']).intersection(set(draw['stars'])))
                    total_matches += matches
            
            evaluation["stars_match_rate"] = total_matches / max_possible if max_possible > 0 else 0
        
        # Calculate coverage efficiency
        if "coverage_efficiency" in metrics:
            # Count unique numbers and stars across all combinations
            all_numbers = set()
            all_stars = set()
            
            for combo in combinations:
                all_numbers.update(combo['numbers'])
                all_stars.update(combo['stars'])
            
            # Calculate coverage percentages
            number_coverage = len(all_numbers) / 50  # 50 possible main numbers
            star_coverage = len(all_stars) / 12      # 12 possible star numbers
            
            # Weighted combination (80% numbers, 20% stars)
            evaluation["coverage_efficiency"] = 0.8 * number_coverage + 0.2 * star_coverage
        
        # Calculate diversity score
        if "diversity_score" in metrics:
            # Count how many times each number/star appears
            number_counts = {}
            star_counts = {}
            
            for combo in combinations:
                for num in combo['numbers']:
                    number_counts[num] = number_counts.get(num, 0) + 1
                for star in combo['stars']:
                    star_counts[star] = star_counts.get(star, 0) + 1
            
            # Calculate coefficient of variation (standard deviation / mean)
            if number_counts:
                number_counts_values = list(number_counts.values())
                number_cv = np.std(number_counts_values) / np.mean(number_counts_values) if np.mean(number_counts_values) > 0 else 0
            else:
                number_cv = 0
                
            if star_counts:
                star_counts_values = list(star_counts.values())
                star_cv = np.std(star_counts_values) / np.mean(star_counts_values) if np.mean(star_counts_values) > 0 else 0
            else:
                star_cv = 0
            
            # Lower CV means more uniform (higher diversity)
            number_diversity = 1 - min(number_cv, 1)  # Cap at 1
            star_diversity = 1 - min(star_cv, 1)      # Cap at 1
            
            # Weighted combination
            evaluation["diversity_score"] = 0.8 * number_diversity + 0.2 * star_diversity
        
        # Calculate historical similarity
        if "historical_similarity" in metrics:
            # Extract patterns from historical data
            historical_patterns = self._extract_patterns(test_draws)
            
            # Extract patterns from generated combinations
            generated_patterns = self._extract_patterns(combinations)
            
            # Calculate pattern similarity scores
            similarity_scores = []
            
            # Compare even-odd pattern distributions
            if historical_patterns.get('even_odd') and generated_patterns.get('even_odd'):
                even_odd_similarity = 1 - sum(abs(historical_patterns['even_odd'][i] - generated_patterns['even_odd'][i]) for i in range(6)) / 2
                similarity_scores.append(even_odd_similarity)
            
            # Compare sum ranges
            if historical_patterns.get('sum_range') and generated_patterns.get('sum_range'):
                sum_similarity = 1 - sum(abs(historical_patterns['sum_range'][i] - generated_patterns['sum_range'][i]) for i in range(len(historical_patterns['sum_range']))) / 2
                similarity_scores.append(sum_similarity)
            
            # Calculate overall similarity
            evaluation["historical_similarity"] = np.mean(similarity_scores) if similarity_scores else 0
        
        # Calculate balance factor
        if "balance_factor" in metrics:
            balance_scores = []
            
            for combo in combinations:
                # Calculate various balance metrics
                
                # Even-odd balance (ideally 2-3 or 3-2)
                even_count = sum(1 for num in combo['numbers'] if num % 2 == 0)
                odd_count = 5 - even_count
                even_odd_balance = 1 - abs(even_count - odd_count) / 5
                
                # High-low balance (ideally mix of high and low numbers)
                high_count = sum(1 for num in combo['numbers'] if num > 25)
                low_count = 5 - high_count
                high_low_balance = 1 - abs(high_count - low_count) / 5
                
                # Decade balance (ideally numbers from different decades)
                decades = {}
                for num in combo['numbers']:
                    decade = (num - 1) // 10
                    decades[decade] = decades.get(decade, 0) + 1
                
                max_per_decade = max(decades.values())
                decade_balance = 1 - (max_per_decade - 1) / 4  # 4 is max imbalance (all 5 in same decade)
                
                # Combine balance metrics
                combo_balance = (even_odd_balance + high_low_balance + decade_balance) / 3
                balance_scores.append(combo_balance)
            
            evaluation["balance_factor"] = np.mean(balance_scores)
        
        return evaluation
    
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
        patterns = {}
        
        # Count even-odd distributions
        even_odd_dist = [0] * 6  # 0 to 5 even numbers
        for draw in draws:
            even_count = sum(1 for num in draw['numbers'] if num % 2 == 0)
            even_odd_dist[even_count] += 1
        
        # Normalize to probabilities
        if draws:
            patterns['even_odd'] = [count / len(draws) for count in even_odd_dist]
        
        # Sum ranges
        sum_ranges = {
            '0-150': 0,
            '151-175': 0,
            '176-200': 0,
            '201-225': 0,
            '226+': 0
        }
        
        for draw in draws:
            total = sum(draw['numbers'])
            if total <= 150:
                sum_ranges['0-150'] += 1
            elif total <= 175:
                sum_ranges['151-175'] += 1
            elif total <= 200:
                sum_ranges['176-200'] += 1
            elif total <= 225:
                sum_ranges['201-225'] += 1
            else:
                sum_ranges['226+'] += 1
        
        # Normalize to probabilities
        if draws:
            patterns['sum_range'] = [count / len(draws) for count in sum_ranges.values()]
        
        return patterns
    
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
        rankings = {}
        
        # Get list of strategies and metrics
        strategies = list(summary.keys())
        
        if not strategies:
            return rankings
            
        metrics = list(summary[strategies[0]].keys())
        
        # Calculate rankings for each metric
        metric_rankings = {}
        for metric in metrics:
            # Sort strategies by mean value of this metric (higher is better)
            sorted_strategies = sorted(
                strategies,
                key=lambda s: summary[s][metric]['mean'],
                reverse=True
            )
            
            # Assign rankings
            metric_rankings[metric] = {
                strategy: rank + 1
                for rank, strategy in enumerate(sorted_strategies)
            }
        
        # Calculate overall ranking for each strategy
        for strategy in strategies:
            # Sum up ranks across all metrics
            rank_sum = sum(metric_rankings[metric][strategy] for metric in metrics)
            
            # Calculate average rank
            rankings[strategy] = {
                'average_rank': rank_sum / len(metrics),
                'ranks_by_metric': {
                    metric: metric_rankings[metric][strategy]
                    for metric in metrics
                }
            }
        
        # Sort strategies by average rank
        sorted_strategies = sorted(
            strategies,
            key=lambda s: rankings[s]['average_rank']
        )
        
        # Add overall ranking
        for rank, strategy in enumerate(sorted_strategies):
            rankings[strategy]['overall_rank'] = rank + 1
        
        return rankings
    
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
            # Convert results to JSON
            results_json = json.dumps(results)
            
            # Save to database
            database.save_strategy_test_results(
                datetime.datetime.now(),
                ','.join(results['strategies_tested']),
                results['iterations'],
                results['num_combinations'],
                results_json
            )
            
            return True
        except Exception as e:
            print(f"Error saving test results: {str(e)}")
            return False
    
    # Strategy generation methods (calling the actual strategy implementations)
    def _generate_frequency_strategy(self, num_combinations):
        """Generate combinations using frequency analysis strategy"""
        return self.test_strategies.frequency_strategy(num_combinations)
    
    def _generate_mixed_strategy(self, num_combinations):
        """Generate combinations using mixed/balanced strategy"""
        return self.test_strategies.mixed_strategy(num_combinations)
    
    def _generate_temporal_strategy(self, num_combinations):
        """Generate combinations using temporal analysis"""
        return self.test_strategies.temporal_strategy(num_combinations)
    
    def _generate_stratified_strategy(self, num_combinations):
        """Generate combinations using stratified sampling"""
        return self.test_strategies.stratified_sampling_strategy(num_combinations)
    
    def _generate_coverage_strategy(self, num_combinations):
        """Generate combinations optimizing coverage"""
        return self.test_strategies.coverage_strategy(num_combinations)
    
    def _generate_risk_reward_strategy(self, num_combinations):
        """Generate combinations with risk-reward optimization"""
        return self.test_strategies.risk_reward_strategy(num_combinations)
    
    def _generate_bayesian_strategy(self, num_combinations):
        """Generate combinations using Bayesian model"""
        return self.test_strategies.bayesian_strategy(num_combinations)
    
    def _generate_markov_strategy(self, num_combinations):
        """Generate combinations using Markov chain model"""
        return self.test_strategies.markov_strategy(num_combinations)
    
    def _generate_time_series_strategy(self, num_combinations):
        """Generate combinations using time series analysis"""
        return self.test_strategies.time_series_strategy(num_combinations)
    
    def _generate_cognitive_bias_strategy(self, num_combinations):
        """Generate combinations using anti-cognitive bias approach"""
        return self.test_strategies.cognitive_bias_strategy(num_combinations)