"""
French Loto Strategy Backtesting Tool

This script evaluates the performance of different prediction strategies
by testing them against the historical French Loto drawings.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import logging
from database import get_db_connection, FrenchLotoDrawing, get_session
from french_loto_strategy import FrenchLotoStrategy
from french_loto_statistics import FrenchLotoStatistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StrategyBacktester:
    """Class to backtest French Loto strategies against historical data"""
    
    def __init__(self, data=None):
        """
        Initialize the backtester with French Loto data
        
        Args:
            data (pd.DataFrame, optional): French Loto data. If None, will load from DB.
        """
        self.data = data
        if self.data is None:
            self.load_data_from_db()
        
        # Sort data by date for chronological testing
        self.data = self.data.sort_values('date')
        
        # Initialize metrics
        self.results = {
            "frequency_strategy": {"hits": [], "matches": []},
            "temporal_pattern_strategy": {"hits": [], "matches": []},
            "stratified_sampling_strategy": {"hits": [], "matches": []},
            "coverage_optimization_strategy": {"hits": [], "matches": []},
            "bayesian_strategy": {"hits": [], "matches": []},
            "risk_reward_strategy": {"hits": [], "matches": []},
            "markov_chain_strategy": {"hits": [], "matches": []},
            "time_series_strategy": {"hits": [], "matches": []},
            "cognitive_bias_strategy": {"hits": [], "matches": []},
            "mixed_strategy": {"hits": [], "matches": []}
        }
        
    def load_data_from_db(self):
        """Load French Loto data from the database"""
        logger.info("Loading French Loto data from database...")
        
        conn = get_db_connection()
        if conn:
            try:
                query = "SELECT * FROM french_loto_drawings ORDER BY date ASC"
                self.data = pd.read_sql(query, conn)
                logger.info(f"Loaded {len(self.data)} French Loto drawings")
            except Exception as e:
                logger.error(f"Error loading data: {str(e)}")
                self.data = pd.DataFrame()
        else:
            logger.error("Could not connect to database")
            self.data = pd.DataFrame()
    
    def calculate_match_score(self, prediction, actual_draw):
        """
        Calculate the match score between a prediction and actual draw
        
        Args:
            prediction (dict): Prediction with number keys (could be 'numbers' or 'main_numbers' and 'lucky' or 'lucky_number') 
            actual_draw (pd.Series): Actual draw row from the dataset
            
        Returns:
            tuple: (match_score, numbers_matched, lucky_matched)
                match_score: 0-6 points (5 for numbers + 1 for lucky)
                numbers_matched: List of matched numbers
                lucky_matched: Boolean indicating if lucky number matched
        """
        # Extract actual numbers and lucky number
        actual_numbers = [actual_draw['n1'], actual_draw['n2'], actual_draw['n3'], 
                          actual_draw['n4'], actual_draw['n5']]
        actual_lucky = actual_draw['lucky']
        
        # Handle different key formats in the prediction object
        if 'numbers' in prediction:
            pred_numbers = prediction['numbers']
        elif 'main_numbers' in prediction:
            pred_numbers = prediction['main_numbers']
        else:
            # If format not recognized, return 0 matches
            return 0, [], False
        
        if 'lucky' in prediction:
            pred_lucky = prediction['lucky']
        elif 'lucky_number' in prediction:
            pred_lucky = prediction['lucky_number']
        else:
            # If format not recognized, return 0 matches
            return 0, [], False
        
        # Calculate matches
        numbers_matched = [n for n in pred_numbers if n in actual_numbers]
        lucky_matched = pred_lucky == actual_lucky
        
        # Calculate match score (0-6)
        match_score = len(numbers_matched) + (1 if lucky_matched else 0)
        
        return match_score, numbers_matched, lucky_matched
    
    def run_backtest(self, test_ratio=0.3, num_combinations=5, verbose=True):
        """
        Run a backtest of all strategies on historical data
        
        Args:
            test_ratio (float): Portion of data to use for testing (0.0-1.0)
            num_combinations (int): Number of combinations to generate per strategy
            verbose (bool): Whether to print detailed progress
            
        Returns:
            dict: Results of backtest for all strategies
        """
        if len(self.data) < 100:
            logger.error("Insufficient data for backtesting (need at least 100 records)")
            return {}
        
        # Split data into training and testing sets
        split_idx = int(len(self.data) * (1 - test_ratio))
        training_data = self.data.iloc[:split_idx]
        testing_data = self.data.iloc[split_idx:]
        
        logger.info(f"Backtesting with {len(training_data)} training drawings and {len(testing_data)} testing drawings")
        
        # Initialize statistics object with training data
        stats = FrenchLotoStatistics(training_data)
        
        # Initialize strategy generator with statistics object
        strategy = FrenchLotoStrategy(stats)
        
        # Define mapping of result keys to actual strategy method names
        strategy_method_map = {
            "frequency_strategy": "frequency_strategy",
            "temporal_pattern_strategy": "temporal_strategy",
            "stratified_sampling_strategy": "stratified_sampling_strategy",
            "coverage_optimization_strategy": "coverage_strategy",
            "bayesian_strategy": "bayesian_strategy",
            "risk_reward_strategy": "risk_reward_strategy",
            "markov_chain_strategy": "markov_strategy",
            "time_series_strategy": "time_series_strategy",
            "cognitive_bias_strategy": "cognitive_bias_strategy",
            "mixed_strategy": "mixed_strategy"
        }
        
        # Test each strategy
        all_strategies = list(self.results.keys())
        
        for strat_name in all_strategies:
            if verbose:
                logger.info(f"Backtesting {strat_name}...")
            
            # Set default parameters for each strategy
            params = {}
            if strat_name == "frequency_strategy":
                params = {"recent_weight": 0.3}
            elif strat_name == "temporal_pattern_strategy":
                params = {"lookback_period": 30}
            elif strat_name == "stratified_sampling_strategy":
                params = {"strata_type": "pattern", "balance_factor": 0.7}
            elif strat_name == "coverage_optimization_strategy":
                params = {"balanced": True}
            elif strat_name == "bayesian_strategy":
                params = {"recent_draws_count": 20}
            elif strat_name == "risk_reward_strategy":
                params = {"risk_level": 5}  # Note: Integer value as per method signature
            elif strat_name == "markov_chain_strategy":
                params = {"lag": 1}
            elif strat_name == "time_series_strategy":
                params = {"window_size": 10}
            elif strat_name == "cognitive_bias_strategy":
                params = {}
            elif strat_name == "mixed_strategy":
                params = {"hot_ratio": 0.7}
            
            # Generate predictions using the strategy
            try:
                # Get the actual method name from our mapping
                method_name = strategy_method_map.get(strat_name, strat_name)
                strategy_func = getattr(strategy, method_name)
                params['num_combinations'] = num_combinations
                predictions = strategy_func(**params)
                
                # Evaluate predictions against each test drawing
                for _, test_draw in testing_data.iterrows():
                    best_match_score = 0
                    best_numbers_matched = []
                    best_lucky_matched = False
                    
                    # Check all combinations for this strategy against the current draw
                    for pred in predictions:
                        match_score, numbers_matched, lucky_matched = self.calculate_match_score(pred, test_draw)
                        
                        # Keep track of the best match for this draw
                        if match_score > best_match_score:
                            best_match_score = match_score
                            best_numbers_matched = numbers_matched
                            best_lucky_matched = lucky_matched
                    
                    # Record the best match for this test drawing
                    self.results[strat_name]["hits"].append(best_match_score)
                    self.results[strat_name]["matches"].append({
                        "date": test_draw['date'],
                        "numbers_matched": best_numbers_matched,
                        "lucky_matched": best_lucky_matched,
                        "score": best_match_score
                    })
                
                if verbose:
                    avg_score = np.mean(self.results[strat_name]["hits"])
                    logger.info(f"  Average score: {avg_score:.2f}/6")
                
            except Exception as e:
                logger.error(f"Error testing {strat_name}: {str(e)}")
                continue
        
        return self.analyze_results()
    
    def analyze_results(self):
        """
        Analyze backtest results and calculate performance metrics for each strategy
        
        Returns:
            dict: Analyzed results with performance metrics
        """
        analysis = {}
        
        for strat_name, data in self.results.items():
            if not data["hits"]:
                continue
                
            hits = data["hits"]
            matches = data["matches"]
            
            # Calculate metrics
            analysis[strat_name] = {
                "avg_score": np.mean(hits),
                "median_score": np.median(hits),
                "max_score": np.max(hits),
                "min_score": np.min(hits),
                "std_dev": np.std(hits),
                "perfect_matches": sum(1 for h in hits if h == 6),
                "good_matches": sum(1 for h in hits if h >= 4),
                "winning_percentage": sum(1 for h in hits if h >= 3) / len(hits) * 100 if hits else 0,
                "total_tests": len(hits)
            }
            
            # Check for jackpot (5+lucky)
            jackpots = [m for m in matches if len(m["numbers_matched"]) == 5 and m["lucky_matched"]]
            analysis[strat_name]["jackpots"] = len(jackpots)
            
            # Calculate probability of hitting different match levels
            probs = {}
            for i in range(7):  # 0 to 6 matches
                probs[f"{i}_matches"] = sum(1 for h in hits if h == i) / len(hits) * 100
            analysis[strat_name]["match_probabilities"] = probs
            
        return analysis
    
    def print_summary(self, analysis):
        """
        Print a summary of the backtest results
        
        Args:
            analysis (dict): Analyzed results from analyze_results()
        """
        print("\n===== FRENCH LOTO STRATEGY BACKTEST RESULTS =====\n")
        
        # Sort strategies by average score (descending)
        sorted_strategies = sorted(
            analysis.items(), 
            key=lambda x: x[1]["avg_score"], 
            reverse=True
        )
        
        print(f"{'Strategy':<30} {'Avg Score':<10} {'Jackpots':<10} {'Good Matches':<15} {'Win %':<10}")
        print("-" * 75)
        
        for strat_name, metrics in sorted_strategies:
            print(f"{strat_name:<30} {metrics['avg_score']:<10.2f} {metrics['jackpots']:<10} "
                  f"{metrics['good_matches']:<15} {metrics['winning_percentage']:<10.2f}%")
        
        print("\nDetailed Analysis:\n")
        
        for strat_name, metrics in sorted_strategies:
            print(f"\n{strat_name}:")
            print(f"  Average Score: {metrics['avg_score']:.2f}/6")
            print(f"  Median Score: {metrics['median_score']}")
            print(f"  Maximum Score: {metrics['max_score']}")
            print(f"  Minimum Score: {metrics['min_score']}")
            print(f"  Standard Deviation: {metrics['std_dev']:.2f}")
            print(f"  Perfect Matches (6/6): {metrics['perfect_matches']}")
            print(f"  Good Matches (4+/6): {metrics['good_matches']}")
            print(f"  Winning Percentage (3+/6): {metrics['winning_percentage']:.2f}%")
            print(f"  Total Tests: {metrics['total_tests']}")
            
            print("\n  Match Probability Distribution:")
            for i in range(7):
                print(f"    {i} matches: {metrics['match_probabilities'][f'{i}_matches']:.2f}%")
        
        # Print the best strategy
        if sorted_strategies:
            best_strategy = sorted_strategies[0][0]
            best_score = sorted_strategies[0][1]['avg_score']
            print(f"\nBest performing strategy: {best_strategy} with average score {best_score:.2f}/6")

def main():
    """Run the backtesting process"""
    print("Starting French Loto strategy backtesting...")
    
    start_time = time.time()
    
    # Create backtester
    backtester = StrategyBacktester()
    
    # Run backtest with 30% of data as test set, 20 combinations per strategy
    # for more comprehensive testing
    analysis = backtester.run_backtest(test_ratio=0.3, num_combinations=20)
    
    # Print summary
    backtester.print_summary(analysis)
    
    elapsed_time = time.time() - start_time
    print(f"\nBacktesting completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()