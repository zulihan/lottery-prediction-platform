import os
import sys
import logging
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random
from collections import defaultdict

# Add relative import support
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import database
from statistics import EuromillionsStatistics
import strategies  # Import the strategy module

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StrategyBacktester:
    """
    Backtester for Euromillions prediction strategies.
    Tests strategies against historical draw data to evaluate performance.
    """
    
    def __init__(self, num_draws=20):
        """
        Initialize backtester with database connection and parameters.
        
        Args:
            num_draws: Number of most recent draws to test against
        """
        self.load_data()
        self.num_draws = min(num_draws, len(self.all_data))
        
        # Get the test draws (most recent n draws)
        self.test_draws = self.all_data.sort_values('date', ascending=False).head(self.num_draws).copy()
        self.test_draws.reset_index(drop=True, inplace=True)
        
        # Available strategies to test
        self.strategies = [
            "frequency", 
            "risk_reward",
            "coverage",
            "bayesian",
            "combined",
            "may6_optimized"
        ]
        
        # Store results
        self.results = {}
        
    def load_data(self):
        """Load all drawing data from database"""
        try:
            logger.info("Loading data from database...")
            self.all_data = database.get_all_drawings()
            logger.info(f"Loaded {len(self.all_data)} draws from database.")
            
            # Ensure date column is datetime
            self.all_data['date'] = pd.to_datetime(self.all_data['date'])
            
        except Exception as e:
            logger.error(f"Error loading data from database: {e}")
            # Return empty DataFrame with correct structure in case of error
            self.all_data = pd.DataFrame(columns=['date', 'day_of_week', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2'])
    
    def prepare_training_data(self, test_date):
        """
        Prepare training data for a specific test date.
        Only includes draws before the test date.
        
        Args:
            test_date: The date of the draw being tested
            
        Returns:
            DataFrame with training data
        """
        # Convert test_date to datetime if it's a string
        if isinstance(test_date, str):
            test_date = pd.to_datetime(test_date)
            
        # Get all draws before the test date
        training_data = self.all_data[self.all_data['date'] < test_date].copy()
        
        return training_data
    
    def get_draw_numbers(self, draw_row):
        """
        Extract numbers and stars from a draw row
        
        Args:
            draw_row: Row from DataFrame containing draw information
            
        Returns:
            tuple: (numbers, stars)
        """
        numbers = [draw_row[f'n{i}'] for i in range(1, 6)]
        stars = [draw_row[f's{i}'] for i in range(1, 3)]
        return numbers, stars
    
    def generate_combinations_for_strategy(self, strategy_name, training_data, num_combinations=3):
        """
        Generate combinations using the specified strategy
        
        Args:
            strategy_name: Name of the strategy to use
            training_data: DataFrame with historical data to use for training
            num_combinations: Number of combinations to generate
            
        Returns:
            list: Generated combinations [(numbers, stars), ...]
        """
        combinations = []
        
        try:
            # Initialize appropriate strategy
            if strategy_name == "frequency":
                # Frequency strategy
                stats = EuromillionsStatistics(training_data)
                
                # Generate combinations with slightly different weights
                weights = [0.5, 0.6, 0.7]  # Different recency weights
                for weight in weights[:num_combinations]:
                    num_freq = stats.get_weighted_frequency(recent_weight=weight)
                    star_freq = stats.get_weighted_star_frequency(recent_weight=weight)
                    
                    # Select top numbers and stars by frequency
                    top_numbers = sorted(num_freq.items(), key=lambda x: x[1], reverse=True)[:15]
                    top_stars = sorted(star_freq.items(), key=lambda x: x[1], reverse=True)[:5]
                    
                    # Sample from top frequencies
                    numbers = sorted(random.sample([n for n, _ in top_numbers], 5))
                    stars = sorted(random.sample([s for s, _ in top_stars], 2))
                    
                    combinations.append((numbers, stars))
                
            elif strategy_name == "risk_reward":
                # Risk/Reward strategy from Strategies module
                # For backtesting, we'll simulate this with different risk levels
                s = strategies.EuromillionsStrategies(training_data)
                
                # Different risk levels
                risk_levels = [0.3, 0.6, 0.9][:num_combinations]
                for risk in risk_levels:
                    numbers, stars, _ = s.apply_risk_reward_strategy(risk_level=risk)
                    # Only keep 2 stars for fair comparison
                    stars = stars[:2] if len(stars) > 2 else stars
                    combinations.append((numbers, stars))
                    
            elif strategy_name == "coverage":
                # Coverage strategy
                s = strategies.EuromillionsStrategies(training_data)
                
                # Generate combinations with different coverage parameters
                for i in range(num_combinations):
                    numbers, stars, _ = s.apply_coverage_strategy()
                    # Only keep 2 stars for fair comparison
                    stars = stars[:2] if len(stars) > 2 else stars
                    combinations.append((numbers, stars))
                
            elif strategy_name == "bayesian":
                # Bayesian strategy
                s = strategies.EuromillionsStrategies(training_data)
                
                # Generate combinations with different prior strengths
                prior_strengths = [0.3, 0.5, 0.7][:num_combinations]
                for strength in prior_strengths:
                    numbers, stars, _ = s.apply_bayesian_strategy(prior_strength=strength)
                    # Only keep 2 stars for fair comparison
                    stars = stars[:2] if len(stars) > 2 else stars
                    combinations.append((numbers, stars))
                
            elif strategy_name == "combined":
                # Combined strategy (mix of multiple strategies)
                s = strategies.EuromillionsStrategies(training_data)
                
                for i in range(num_combinations):
                    # Using default parameters for combined
                    numbers, stars, _ = s.generate_ultimate_combination()
                    # Only keep 2 stars for fair comparison
                    stars = stars[:2] if len(stars) > 2 else stars
                    combinations.append((numbers, stars))
                    
            elif strategy_name == "may6_optimized":
                # Use our May 6 optimized strategy
                # Import the module dynamically
                import may6_optimized_strategy
                strategy = may6_optimized_strategy.May6OptimizedStrategy()
                
                for i in range(num_combinations):
                    if i % 2 == 0:
                        # Use Risk/Reward with different risk levels
                        risk_level = 0.7 + (i * 0.1)
                        numbers, stars, _ = strategy.generate_risk_reward_combination(risk_level=risk_level)
                    else:
                        # Use ultimate combined
                        numbers, stars, _ = strategy.generate_ultimate_combination()
                    
                    # Only keep 2 stars for fair comparison
                    stars = stars[:2] if len(stars) > 2 else stars
                    combinations.append((numbers, stars))
                
            # Ensure we have the requested number of combinations
            while len(combinations) < num_combinations:
                # Just duplicate the last one if we don't have enough
                if combinations:
                    combinations.append(combinations[-1])
                else:
                    # Random combination as fallback
                    numbers = sorted(random.sample(range(1, 51), 5))
                    stars = sorted(random.sample(range(1, 13), 2))
                    combinations.append((numbers, stars))
        
        except Exception as e:
            logger.error(f"Error generating combinations for {strategy_name}: {e}")
            # Return some random combinations if there's an error
            combinations = []
            for _ in range(num_combinations):
                numbers = sorted(random.sample(range(1, 51), 5))
                stars = sorted(random.sample(range(1, 13), 2))
                combinations.append((numbers, stars))
        
        return combinations
    
    def calculate_match_score(self, generated_numbers, generated_stars, actual_numbers, actual_stars):
        """
        Calculate match score for a combination
        
        Args:
            generated_numbers: List of 5 generated numbers
            generated_stars: List of 2 generated stars
            actual_numbers: List of 5 actual drawn numbers
            actual_stars: List of 2 actual drawn stars
            
        Returns:
            tuple: (matched_numbers, matched_stars, prize_tier)
        """
        # Convert to sets for intersection
        gen_nums_set = set(generated_numbers)
        gen_stars_set = set(generated_stars)
        actual_nums_set = set(actual_numbers)
        actual_stars_set = set(actual_stars)
        
        # Calculate matches
        matched_numbers = len(gen_nums_set.intersection(actual_nums_set))
        matched_stars = len(gen_stars_set.intersection(actual_stars_set))
        
        # Determine prize tier
        prize_tier = "No Prize"
        
        if matched_numbers == 5 and matched_stars == 2:
            prize_tier = "Jackpot"
        elif matched_numbers == 5 and matched_stars == 1:
            prize_tier = "2nd Prize"
        elif matched_numbers == 5 and matched_stars == 0:
            prize_tier = "3rd Prize"
        elif matched_numbers == 4 and matched_stars == 2:
            prize_tier = "4th Prize"
        elif matched_numbers == 4 and matched_stars == 1:
            prize_tier = "5th Prize"
        elif matched_numbers == 3 and matched_stars == 2:
            prize_tier = "6th Prize"
        elif matched_numbers == 4 and matched_stars == 0:
            prize_tier = "7th Prize"
        elif matched_numbers == 2 and matched_stars == 2:
            prize_tier = "8th Prize"
        elif matched_numbers == 3 and matched_stars == 1:
            prize_tier = "9th Prize"
        elif matched_numbers == 3 and matched_stars == 0:
            prize_tier = "10th Prize"
        elif matched_numbers == 1 and matched_stars == 2:
            prize_tier = "11th Prize"
        elif matched_numbers == 2 and matched_stars == 1:
            prize_tier = "12th Prize"
        elif matched_numbers == 2 and matched_stars == 0:
            prize_tier = "13th Prize"
        
        return matched_numbers, matched_stars, prize_tier
    
    def backtest_strategy(self, strategy_name, combinations_per_draw=3):
        """
        Backtest a single strategy against test draws
        
        Args:
            strategy_name: Name of the strategy to test
            combinations_per_draw: Number of combinations to generate per draw
            
        Returns:
            dict: Results of the backtest
        """
        logger.info(f"Backtesting {strategy_name} strategy...")
        
        # Results container
        strategy_results = {
            'strategy': strategy_name,
            'total_combinations': 0,
            'total_matched_numbers': 0,
            'total_matched_stars': 0,
            'prize_tiers': defaultdict(int),
            'avg_numbers_per_combination': 0,
            'avg_stars_per_combination': 0,
            'details_by_draw': []
        }
        
        # Test against each draw
        for _, draw in self.test_draws.iterrows():
            draw_date = draw['date']
            draw_numbers, draw_stars = self.get_draw_numbers(draw)
            
            # Prepare training data (all draws before this one)
            training_data = self.prepare_training_data(draw_date)
            
            # Generate combinations for this draw
            combinations = self.generate_combinations_for_strategy(
                strategy_name, 
                training_data,
                num_combinations=combinations_per_draw
            )
            
            # Test each combination
            draw_matched_numbers = 0
            draw_matched_stars = 0
            draw_prizes = defaultdict(int)
            
            draw_details = {
                'date': draw_date.strftime('%Y-%m-%d'),
                'actual_numbers': draw_numbers,
                'actual_stars': draw_stars,
                'combinations': []
            }
            
            for numbers, stars in combinations:
                matched_numbers, matched_stars, prize_tier = self.calculate_match_score(
                    numbers, stars, draw_numbers, draw_stars
                )
                
                # Update counters
                draw_matched_numbers += matched_numbers
                draw_matched_stars += matched_stars
                draw_prizes[prize_tier] += 1
                
                # Add combination details
                draw_details['combinations'].append({
                    'numbers': numbers,
                    'stars': stars,
                    'matched_numbers': matched_numbers,
                    'matched_stars': matched_stars,
                    'prize_tier': prize_tier
                })
            
            # Add draw results to details
            draw_details['total_matched_numbers'] = draw_matched_numbers
            draw_details['total_matched_stars'] = draw_matched_stars
            draw_details['prize_tiers'] = dict(draw_prizes)
            
            strategy_results['details_by_draw'].append(draw_details)
            
            # Update overall counters
            strategy_results['total_combinations'] += len(combinations)
            strategy_results['total_matched_numbers'] += draw_matched_numbers
            strategy_results['total_matched_stars'] += draw_matched_stars
            
            # Update prize tiers
            for tier, count in draw_prizes.items():
                strategy_results['prize_tiers'][tier] += count
        
        # Calculate averages
        if strategy_results['total_combinations'] > 0:
            strategy_results['avg_numbers_per_combination'] = (
                strategy_results['total_matched_numbers'] / strategy_results['total_combinations']
            )
            strategy_results['avg_stars_per_combination'] = (
                strategy_results['total_matched_stars'] / strategy_results['total_combinations']
            )
        
        # Convert defaultdict to dict for cleaner output
        strategy_results['prize_tiers'] = dict(strategy_results['prize_tiers'])
        
        return strategy_results
    
    def run_all_backtests(self, combinations_per_draw=3):
        """
        Run backtests for all strategies
        
        Args:
            combinations_per_draw: Number of combinations to generate per draw
            
        Returns:
            dict: Results of all backtests
        """
        for strategy in self.strategies:
            try:
                self.results[strategy] = self.backtest_strategy(
                    strategy, 
                    combinations_per_draw=combinations_per_draw
                )
            except Exception as e:
                logger.error(f"Error backtesting {strategy}: {e}")
                self.results[strategy] = {
                    'strategy': strategy,
                    'error': str(e)
                }
        
        return self.results
    
    def print_summary(self):
        """
        Print a summary of backtest results
        """
        if not self.results:
            print("No backtest results available. Run run_all_backtests() first.")
            return
        
        print(f"\n{'='*80}")
        print(f"BACKTEST RESULTS SUMMARY - Last {self.num_draws} draws")
        print(f"{'='*80}\n")
        
        # Sort strategies by average match rate
        ranked_strategies = sorted(
            self.results.values(), 
            key=lambda x: x.get('avg_numbers_per_combination', 0) + x.get('avg_stars_per_combination', 0) * 2,
            reverse=True
        )
        
        # Print ranked summary
        print(f"STRATEGY RANKING (by average match rate):")
        print(f"{'-'*80}")
        print(f"{'Rank':<5}{'Strategy':<20}{'Avg Numbers':<15}{'Avg Stars':<15}{'Prize Wins':<15}")
        print(f"{'-'*80}")
        
        for i, result in enumerate(ranked_strategies):
            if 'error' in result:
                print(f"{i+1:<5}{result['strategy']:<20}ERROR: {result['error']}")
                continue
                
            # Count total prize wins (anything except "No Prize")
            prize_wins = sum(
                count for tier, count in result['prize_tiers'].items() 
                if tier != "No Prize"
            )
            
            print(
                f"{i+1:<5}{result['strategy']:<20}"
                f"{result['avg_numbers_per_combination']:.2f} of 5      "
                f"{result['avg_stars_per_combination']:.2f} of 2      "
                f"{prize_wins:,}"
            )
        
        print(f"\n{'='*80}")
        print("DETAILED RESULTS BY STRATEGY:")
        print(f"{'='*80}")
        
        # Print detailed results for each strategy
        for result in ranked_strategies:
            if 'error' in result:
                continue
                
            strategy = result['strategy']
            print(f"\n{strategy.upper()} STRATEGY")
            print(f"{'-'*80}")
            
            # Overall statistics
            total_combinations = result['total_combinations']
            print(f"Total combinations tested: {total_combinations:,}")
            print(f"Average main numbers matched: {result['avg_numbers_per_combination']:.2f} of 5")
            print(f"Average stars matched: {result['avg_stars_per_combination']:.2f} of 2")
            
            # Prize breakdown
            print("\nPrize Tier Distribution:")
            prize_tiers = sorted(
                result['prize_tiers'].items(),
                key=lambda x: (x[0] != "No Prize", x[0])  # Sort with "No Prize" at the end
            )
            
            for tier, count in prize_tiers:
                percentage = (count / total_combinations) * 100
                print(f"  {tier+':':<15} {count:,} ({percentage:.2f}%)")
            
            # Best performing draw
            best_draw = max(
                result['details_by_draw'],
                key=lambda x: x['total_matched_numbers'] + x['total_matched_stars'] * 2
            )
            
            print(f"\nBest Performing Draw: {best_draw['date']}")
            print(f"  Actual numbers: {best_draw['actual_numbers']}")
            print(f"  Actual stars: {best_draw['actual_stars']}")
            print(f"  Total matched numbers: {best_draw['total_matched_numbers']}")
            print(f"  Total matched stars: {best_draw['total_matched_stars']}")
            
            # Best combination from that draw
            best_combo = max(
                best_draw['combinations'],
                key=lambda x: x['matched_numbers'] + x['matched_stars'] * 2
            )
            
            print(f"\n  Best combination:")
            print(f"    Numbers: {best_combo['numbers']}")
            print(f"    Stars: {best_combo['stars']}")
            print(f"    Matched: {best_combo['matched_numbers']} numbers, {best_combo['matched_stars']} stars")
            print(f"    Prize tier: {best_combo['prize_tier']}")
            
    def save_results(self, filename="backtest_results.json"):
        """
        Save backtest results to a JSON file
        
        Args:
            filename: Name of the file to save results to
        """
        if not self.results:
            logger.error("No backtest results available. Run run_all_backtests() first.")
            return
        
        # Convert dates to strings for JSON serialization
        serializable_results = {}
        
        for strategy, result in self.results.items():
            if 'error' in result:
                serializable_results[strategy] = result
                continue
                
            serializable_result = result.copy()
            
            # Process details by draw
            serializable_details = []
            for draw in result['details_by_draw']:
                serializable_draw = draw.copy()
                # Date is already converted to string in original code
                serializable_details.append(serializable_draw)
            
            serializable_result['details_by_draw'] = serializable_details
            serializable_results[strategy] = serializable_result
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)
            
        logger.info(f"Saved backtest results to {filename}")

def main():
    """Run backtests and print summary"""
    # Get number of draws to test from command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Backtest Euromillions prediction strategies')
    parser.add_argument('--draws', type=int, default=20, help='Number of recent draws to test against')
    parser.add_argument('--combinations', type=int, default=3, help='Number of combinations per draw')
    args = parser.parse_args()
    
    print(f"Running backtest on the last {args.draws} draws with {args.combinations} combinations per draw...")
    
    # Initialize and run backtester
    backtester = StrategyBacktester(num_draws=args.draws)
    backtester.run_all_backtests(combinations_per_draw=args.combinations)
    
    # Print and save results
    backtester.print_summary()
    backtester.save_results()
    
    print("\nBacktesting complete!")

if __name__ == "__main__":
    main()