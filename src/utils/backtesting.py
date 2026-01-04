"""
Comprehensive Strategy Backtesting

Dynamically calculates performance metrics for all lottery strategies by:
- Loading historical data from database
- Splitting into train/test sets
- Running each strategy on training data
- Testing predictions against actual results
- Computing average scores, win rates, and other metrics
"""

import pandas as pd
import numpy as np
from collections import Counter
import logging
from typing import Dict, List, Tuple, Any

logger = logging.getLogger(__name__)


class StrategyBacktester:
    """
    Backtesting engine for lottery prediction strategies.

    Evaluates strategy performance against historical data.
    """

    def __init__(self, historical_data: pd.DataFrame, lottery_type: str = "euromillions"):
        """
        Initialize backtester with historical data.

        Args:
            historical_data: DataFrame with historical draws
            lottery_type: "euromillions" or "french_loto"
        """
        self.historical_data = historical_data
        self.lottery_type = lottery_type
        self.results = {}

    def split_data(self, test_ratio: float = 0.3) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split data into training and testing sets.

        Args:
            test_ratio: Ratio of data to use for testing (default 30%)

        Returns:
            Tuple of (training_data, test_data)
        """
        # Sort by date descending (most recent first)
        sorted_data = self.historical_data.sort_values('date', ascending=False).reset_index(drop=True)

        total_draws = len(sorted_data)
        test_size = int(total_draws * test_ratio)

        # Most recent draws for testing, older draws for training
        test_data = sorted_data.iloc[:test_size]
        training_data = sorted_data.iloc[test_size:]

        logger.info(f"Data split: {len(training_data)} training draws, {len(test_data)} test draws")

        return training_data, test_data

    def score_prediction_euromillions(self, predicted: Dict, actual: Dict) -> float:
        """
        Score a Euromillions prediction against actual result.

        Args:
            predicted: {'numbers': [5 ints], 'stars': [2 ints]}
            actual: {'numbers': [5 ints], 'stars': [2 ints]}

        Returns:
            Score (0-12): number matches + star matches
        """
        number_matches = len(set(predicted['numbers']) & set(actual['numbers']))
        star_matches = len(set(predicted['stars']) & set(actual['stars']))

        return number_matches + star_matches

    def score_prediction_french_loto(self, predicted: Dict, actual: Dict) -> float:
        """
        Score a French Loto prediction against actual result.

        Args:
            predicted: {'main_numbers': [5 ints], 'lucky_number': int}
            actual: {'main_numbers': [5 ints], 'lucky_number': int}

        Returns:
            Score (0-6): number matches + lucky match
        """
        # Handle different key formats
        pred_numbers = predicted.get('main_numbers') or predicted.get('numbers', [])
        actual_numbers = actual.get('main_numbers') or actual.get('numbers', [])
        pred_lucky = predicted.get('lucky_number') or predicted.get('lucky')
        actual_lucky = actual.get('lucky_number') or actual.get('lucky')

        number_matches = len(set(pred_numbers) & set(actual_numbers))
        lucky_match = 1 if pred_lucky == actual_lucky else 0

        return number_matches + lucky_match

    def is_winning_prediction(self, score: float) -> bool:
        """
        Determine if a prediction is a winning prediction.

        Args:
            score: Prediction score

        Returns:
            True if score is high enough to win a prize
        """
        if self.lottery_type == "euromillions":
            # Euromillions: Need at least 2 main numbers or 2 stars
            return score >= 2
        else:  # french_loto
            # French Loto: Need at least 3 numbers or 2+lucky
            return score >= 3

    def backtest_strategy(self,
                         strategy_function,
                         strategy_name: str,
                         num_predictions: int = 20,
                         **strategy_params) -> Dict[str, Any]:
        """
        Backtest a single strategy.

        Args:
            strategy_function: Strategy method to test
            strategy_name: Name of the strategy
            num_predictions: Number of predictions to generate per test
            **strategy_params: Additional parameters for the strategy

        Returns:
            Dict with performance metrics
        """
        logger.info(f"Backtesting {strategy_name}...")

        # Split data
        training_data, test_data = self.split_data()

        # Initialize strategy with training data
        if self.lottery_type == "euromillions":
            from src.core.statistics import EuromillionsStatistics
            from src.core.strategies import PredictionStrategies

            stats = EuromillionsStatistics(training_data)
            strategies = PredictionStrategies(stats)
        else:  # french_loto
            from src.core.french_loto_statistics import FrenchLotoStatistics
            from src.core.french_loto_strategy import FrenchLotoStrategy

            stats = FrenchLotoStatistics(training_data)
            strategies = FrenchLotoStrategy(stats)

        # Generate predictions using the strategy
        try:
            predictions = strategy_function(
                strategies,
                num_combinations=num_predictions,
                **strategy_params
            )
        except Exception as e:
            logger.error(f"Error generating predictions for {strategy_name}: {e}")
            return {
                'strategy': strategy_name,
                'error': str(e),
                'avg_score': 0.0,
                'win_rate': 0.0,
                'max_score': 0,
                'std_score': 0.0,
                'total_predictions': 0,
                'total_tests': 0,
                'total_scores': 0
            }

        # Score predictions against test data
        scores = []
        wins = 0

        for test_idx, test_row in test_data.iterrows():
            # Extract actual result
            if self.lottery_type == "euromillions":
                actual = {
                    'numbers': [test_row['n1'], test_row['n2'], test_row['n3'],
                               test_row['n4'], test_row['n5']],
                    'stars': [test_row['s1'], test_row['s2']]
                }
            else:  # french_loto
                actual = {
                    'main_numbers': [test_row['n1'], test_row['n2'], test_row['n3'],
                                    test_row['n4'], test_row['n5']],
                    'lucky_number': test_row.get('lucky', test_row.get('lucky_number'))
                }

            # Score each prediction against this actual result
            for pred in predictions:
                if self.lottery_type == "euromillions":
                    score = self.score_prediction_euromillions(pred, actual)
                else:
                    score = self.score_prediction_french_loto(pred, actual)

                scores.append(score)

                if self.is_winning_prediction(score):
                    wins += 1

        # Calculate metrics
        avg_score = np.mean(scores) if scores else 0
        win_rate = (wins / len(scores) * 100) if scores else 0
        max_score = max(scores) if scores else 0
        std_score = np.std(scores) if scores else 0

        results = {
            'strategy': strategy_name,
            'avg_score': round(avg_score, 2),
            'win_rate': round(win_rate, 2),
            'max_score': max_score,
            'std_score': round(std_score, 2),
            'total_predictions': len(predictions),
            'total_tests': len(test_data),
            'total_scores': len(scores)
        }

        logger.info(f"{strategy_name}: Avg Score={avg_score:.2f}, Win Rate={win_rate:.2f}%")

        return results

    def backtest_all_strategies(self, num_predictions: int = 20) -> pd.DataFrame:
        """
        Backtest all available strategies.

        Args:
            num_predictions: Number of predictions per strategy

        Returns:
            DataFrame with results for all strategies
        """
        logger.info(f"Starting comprehensive backtest of all strategies ({self.lottery_type})...")

        if self.lottery_type == "euromillions":
            strategies_to_test = [
                ('Frequency Analysis', lambda s, **kw: s.frequency_strategy(**kw), {}),
                ('Risk/Reward Balance', lambda s, **kw: s.risk_reward_strategy(**kw), {}),
                ('Markov Chain Model', lambda s, **kw: s.markov_strategy(**kw), {}),
                ('Time Series Analysis', lambda s, **kw: s.time_series_strategy(**kw), {}),
                ('Bayesian Inference', lambda s, **kw: s.bayesian_strategy(**kw), {}),
                ('Coverage Optimization', lambda s, **kw: s.coverage_optimization_strategy(**kw), {}),
                ('Temporal Patterns', lambda s, **kw: s.temporal_pattern_strategy(**kw), {}),
                ('Stratified Sampling', lambda s, **kw: s.stratified_sampling_strategy(**kw), {}),
                ('Anti-Cognitive Bias', lambda s, **kw: s.cognitive_bias_strategy(**kw), {}),
                ('Mixed Strategy', lambda s, **kw: s.mixed_strategy(**kw), {}),
            ]
        else:  # french_loto
            strategies_to_test = [
                ('Frequency Analysis', lambda s, **kw: s.frequency_strategy(**kw), {}),
                ('Risk/Reward Balance', lambda s, **kw: s.risk_reward_strategy(**kw), {}),
                ('Markov Chain Model', lambda s, **kw: s.markov_strategy(**kw), {}),
                ('Time Series Analysis', lambda s, **kw: s.time_series_strategy(**kw), {}),
                ('Bayesian Inference', lambda s, **kw: s.bayesian_strategy(**kw), {}),
                # Note: Coverage Optimization and Temporal Patterns not implemented for French Loto
                ('Stratified Sampling', lambda s, **kw: s.stratified_sampling_strategy(**kw), {}),
                ('Anti-Cognitive Bias', lambda s, **kw: s.cognitive_bias_strategy(**kw), {}),
                ('Mixed Strategy', lambda s, **kw: s.mixed_strategy(**kw), {}),
            ]

        results = []

        for strategy_name, strategy_func, params in strategies_to_test:
            try:
                result = self.backtest_strategy(
                    strategy_func,
                    strategy_name,
                    num_predictions=num_predictions,
                    **params
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to backtest {strategy_name}: {e}")
                results.append({
                    'strategy': strategy_name,
                    'error': str(e),
                    'avg_score': 0.0,
                    'win_rate': 0.0,
                    'max_score': 0,
                    'std_score': 0.0,
                    'total_predictions': 0,
                    'total_tests': 0,
                    'total_scores': 0
                })

        # Create DataFrame and sort by win rate
        df = pd.DataFrame(results)
        df = df.sort_values('win_rate', ascending=False)

        self.results = df

        logger.info(f"Backtest complete! Tested {len(results)} strategies.")

        return df


def quick_backtest(lottery_type: str = "euromillions",
                   num_predictions: int = 20) -> pd.DataFrame:
    """
    Quick backtest of all strategies using database data.

    Args:
        lottery_type: "euromillions" or "french_loto"
        num_predictions: Number of predictions per strategy

    Returns:
        DataFrame with performance metrics
    """
    from src.core.database import get_db_connection

    # Load data from database
    conn = get_db_connection()
    if not conn:
        raise Exception("Could not connect to database")

    if lottery_type == "euromillions":
        query = "SELECT * FROM euromillions_drawings ORDER BY date DESC LIMIT 500"
    else:
        query = "SELECT * FROM french_loto_drawings ORDER BY date DESC LIMIT 500"

    data = pd.read_sql(query, conn)

    if len(data) < 100:
        raise Exception(f"Insufficient data for backtesting. Found {len(data)} draws, need at least 100.")

    # Run backtest
    backtester = StrategyBacktester(data, lottery_type)
    results = backtester.backtest_all_strategies(num_predictions=num_predictions)

    return results


# Example usage
if __name__ == "__main__":
    # Test with Euromillions
    print("Running Euromillions backtest...")
    results_euro = quick_backtest("euromillions", num_predictions=10)
    print("\n=== Euromillions Results ===")
    print(results_euro[['strategy', 'avg_score', 'win_rate']])

    # Test with French Loto
    print("\n\nRunning French Loto backtest...")
    results_loto = quick_backtest("french_loto", num_predictions=10)
    print("\n=== French Loto Results ===")
    print(results_loto[['strategy', 'avg_score', 'win_rate']])
