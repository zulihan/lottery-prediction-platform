"""
Failure Analysis Framework

Systematic post-mortem analysis of lottery predictions to enable meta-learning
and strategy improvement.

Analyzes predictions across multiple dimensions:
- Overused numbers
- Missing winning numbers
- Range distribution
- Star patterns
"""

from collections import Counter
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class FailureAnalyzer:
    """
    Analyzes prediction failures to provide actionable insights for strategy improvement.
    """

    def __init__(self):
        """Initialize the failure analyzer."""
        self.analysis_results = {}

    def analyze_predictions(self, our_combinations, winning_numbers, winning_stars):
        """
        Systematic failure analysis across multiple dimensions.

        Args:
            our_combinations: List of dict with 'numbers' and 'stars' keys
            winning_numbers: List of winning numbers
            winning_stars: List of winning stars

        Returns:
            dict: Comprehensive analysis results with actionable insights
        """
        logger.info("=== FAILURE ANALYSIS: What Went Wrong ===")

        # Extract all numbers/stars from our combinations
        all_our_numbers = []
        all_our_stars = []
        for combo in our_combinations:
            all_our_numbers.extend(combo['numbers'])
            all_our_stars.extend(combo['stars'])

        number_freq = Counter(all_our_numbers)
        star_freq = Counter(all_our_stars)

        # Run analyses
        overused = self._analyze_overused_numbers(number_freq, winning_numbers)
        missing = self._analyze_missing_numbers(all_our_numbers, winning_numbers)
        star_analysis = self._analyze_stars(star_freq, winning_stars)
        range_analysis = self._analyze_range_distribution(all_our_numbers, winning_numbers)
        pattern_analysis = self._analyze_patterns(our_combinations, winning_numbers, winning_stars)

        # Compile results
        results = {
            'overused_numbers': overused,
            'missing_numbers': missing,
            'star_analysis': star_analysis,
            'range_analysis': range_analysis,
            'pattern_analysis': pattern_analysis,
            'recommendations': self._generate_recommendations(
                overused, missing, star_analysis, range_analysis
            )
        }

        self.analysis_results = results
        return results

    def _analyze_overused_numbers(self, number_freq, winning_numbers):
        """
        Identify numbers that appeared too many times in our predictions.

        Args:
            number_freq: Counter of number frequencies
            winning_numbers: List of winning numbers

        Returns:
            dict: Analysis of overused numbers
        """
        # Numbers used more than 2 times are considered overused
        overused_numbers = {num: count for num, count in number_freq.items() if count > 2}

        logger.info("\n1. OVERUSED NUMBERS (appeared in multiple combinations):")
        for num, count in sorted(overused_numbers.items(), key=lambda x: x[1], reverse=True):
            won = "✓ WON" if num in winning_numbers else "✗ LOST"
            logger.info(f"   Number {num}: used {count} times - {won}")

        return {
            'numbers': overused_numbers,
            'won_count': sum(1 for num in overused_numbers if num in winning_numbers),
            'lost_count': sum(1 for num in overused_numbers if num not in winning_numbers)
        }

    def _analyze_missing_numbers(self, all_our_numbers, winning_numbers):
        """
        Identify winning numbers that we completely missed.

        Args:
            all_our_numbers: List of all numbers we predicted
            winning_numbers: List of winning numbers

        Returns:
            dict: Analysis of missing numbers
        """
        missing_numbers = set(winning_numbers) - set(all_our_numbers)

        logger.info(f"\n2. MISSING WINNING NUMBERS:")
        for num in sorted(missing_numbers):
            logger.info(f"   Number {num}: COMPLETELY MISSED - appeared in 0 combinations")

        return {
            'numbers': list(missing_numbers),
            'count': len(missing_numbers),
            'percentage': len(missing_numbers) / len(winning_numbers) * 100
        }

    def _analyze_stars(self, star_freq, winning_stars):
        """
        Analyze star prediction performance.

        Args:
            star_freq: Counter of star frequencies
            winning_stars: List of winning stars

        Returns:
            dict: Star analysis
        """
        logger.info(f"\n3. STAR ANALYSIS:")

        hits = []
        misses = []

        for star in winning_stars:
            if star in star_freq:
                count = star_freq[star]
                logger.info(f"   Star {star}: used {count} times - ✓ WON")
                hits.append(star)
            else:
                logger.info(f"   Star {star}: COMPLETELY MISSED")
                misses.append(star)

        return {
            'hits': hits,
            'misses': misses,
            'hit_rate': len(hits) / len(winning_stars) * 100 if winning_stars else 0,
            'star_frequency': dict(star_freq)
        }

    def _analyze_range_distribution(self, all_our_numbers, winning_numbers):
        """
        Analyze range distribution comparison.

        Args:
            all_our_numbers: List of all our predicted numbers
            winning_numbers: List of winning numbers

        Returns:
            dict: Range distribution analysis
        """
        logger.info(f"\n4. RANGE DISTRIBUTION ANALYSIS:")

        # Define ranges
        ranges = {
            "1-10": (1, 10),
            "11-20": (11, 20),
            "21-30": (21, 30),
            "31-40": (31, 40),
            "41-50": (41, 50)
        }

        winning_ranges = {}
        our_ranges = {}
        gaps = []

        for range_name, (start, end) in ranges.items():
            win_count = sum(1 for n in winning_numbers if start <= n <= end)
            our_count = sum(1 for n in all_our_numbers if start <= n <= end)

            winning_ranges[range_name] = win_count
            our_ranges[range_name] = our_count

            match = '✓' if our_count >= win_count else '✗'
            logger.info(f"   {range_name}: Winning={win_count}, Ours={our_count} ({match})")

            if our_count < win_count:
                gaps.append({
                    'range': range_name,
                    'winning_count': win_count,
                    'our_count': our_count,
                    'gap': win_count - our_count
                })

        return {
            'winning_distribution': winning_ranges,
            'our_distribution': our_ranges,
            'underrepresented_ranges': gaps
        }

    def _analyze_patterns(self, our_combinations, winning_numbers, winning_stars):
        """
        Analyze number patterns (even/odd, consecutive, etc.).

        Args:
            our_combinations: List of our combinations
            winning_numbers: List of winning numbers
            winning_stars: List of winning stars

        Returns:
            dict: Pattern analysis
        """
        # Winning patterns
        win_even_count = sum(1 for n in winning_numbers if n % 2 == 0)
        win_odd_count = len(winning_numbers) - win_even_count

        # Our patterns (average across combinations)
        our_even_counts = []
        our_odd_counts = []
        consecutive_counts = []

        for combo in our_combinations:
            even_count = sum(1 for n in combo['numbers'] if n % 2 == 0)
            our_even_counts.append(even_count)
            our_odd_counts.append(5 - even_count)

            # Check for consecutive numbers
            sorted_nums = sorted(combo['numbers'])
            consecutive = sum(1 for i in range(len(sorted_nums)-1)
                            if sorted_nums[i+1] - sorted_nums[i] == 1)
            consecutive_counts.append(consecutive)

        avg_even = sum(our_even_counts) / len(our_even_counts) if our_even_counts else 0
        avg_consecutive = sum(consecutive_counts) / len(consecutive_counts) if consecutive_counts else 0

        return {
            'winning_even_count': win_even_count,
            'winning_odd_count': win_odd_count,
            'our_avg_even': round(avg_even, 2),
            'our_avg_odd': round(5 - avg_even, 2),
            'our_avg_consecutive': round(avg_consecutive, 2)
        }

    def _generate_recommendations(self, overused, missing, star_analysis, range_analysis):
        """
        Generate actionable recommendations based on analysis.

        Args:
            overused: Overused numbers analysis
            missing: Missing numbers analysis
            star_analysis: Star analysis
            range_analysis: Range analysis

        Returns:
            list: List of recommendation strings
        """
        recommendations = []

        # Overused numbers recommendations
        if overused['lost_count'] > 0:
            recommendations.append(
                f"Reduce repetition: {overused['lost_count']} overused numbers didn't win. "
                "Increase number diversity across combinations."
            )

        # Missing numbers recommendations
        if missing['percentage'] > 40:
            recommendations.append(
                f"Coverage gap: Missed {missing['percentage']:.0f}% of winning numbers. "
                "Expand number pool or reduce filtering."
            )

        # Star recommendations
        if star_analysis['hit_rate'] < 50:
            recommendations.append(
                f"Star prediction weak: Only {star_analysis['hit_rate']:.0f}% hit rate. "
                "Review star selection strategy."
            )

        # Range recommendations
        for gap in range_analysis['underrepresented_ranges']:
            if gap['gap'] >= 2:
                recommendations.append(
                    f"Range gap in {gap['range']}: Needed {gap['winning_count']} numbers, "
                    f"only had {gap['our_count']}. Increase coverage in this range."
                )

        # General recommendation if none specific
        if not recommendations:
            recommendations.append(
                "Overall good coverage. Fine-tune strategy parameters for better precision."
            )

        return recommendations

    def print_analysis_report(self):
        """
        Print a formatted analysis report to console.
        """
        if not self.analysis_results:
            logger.warning("No analysis results available. Run analyze_predictions() first.")
            return

        print("\n" + "="*70)
        print("LOTTERY PREDICTION FAILURE ANALYSIS REPORT")
        print("="*70)

        results = self.analysis_results

        print("\n📊 SUMMARY:")
        print(f"  - Overused numbers (>2 uses): {len(results['overused_numbers']['numbers'])}")
        print(f"  - Missing winning numbers: {results['missing_numbers']['count']}")
        print(f"  - Star hit rate: {results['star_analysis']['hit_rate']:.0f}%")
        print(f"  - Underrepresented ranges: {len(results['range_analysis']['underrepresented_ranges'])}")

        print("\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"  {i}. {rec}")

        print("\n" + "="*70)

    def get_summary_stats(self):
        """
        Get summary statistics from the analysis.

        Returns:
            dict: Summary statistics
        """
        if not self.analysis_results:
            return {}

        results = self.analysis_results

        return {
            'overused_count': len(results['overused_numbers']['numbers']),
            'missing_count': results['missing_numbers']['count'],
            'missing_percentage': results['missing_numbers']['percentage'],
            'star_hit_rate': results['star_analysis']['hit_rate'],
            'range_gaps_count': len(results['range_analysis']['underrepresented_ranges']),
            'recommendation_count': len(results['recommendations'])
        }


# Standalone function for quick analysis
def quick_analyze(our_combinations, winning_numbers, winning_stars):
    """
    Quick failure analysis without creating an analyzer instance.

    Args:
        our_combinations: List of our predicted combinations
        winning_numbers: List of winning numbers
        winning_stars: List of winning stars

    Returns:
        dict: Analysis results
    """
    analyzer = FailureAnalyzer()
    results = analyzer.analyze_predictions(our_combinations, winning_numbers, winning_stars)
    analyzer.print_analysis_report()
    return results


# Example usage
if __name__ == "__main__":
    # Example: Analyze some predictions
    example_combinations = [
        {'numbers': [1, 12, 23, 34, 45], 'stars': [2, 5]},
        {'numbers': [3, 14, 25, 36, 47], 'stars': [3, 6]},
        {'numbers': [5, 16, 27, 38, 49], 'stars': [2, 8]},
        {'numbers': [1, 11, 21, 31, 41], 'stars': [4, 9]},
        {'numbers': [2, 13, 24, 35, 46], 'stars': [5, 10]},
    ]

    example_winning = [7, 18, 29, 40, 42]
    example_stars = [5, 11]

    analyzer = FailureAnalyzer()
    results = analyzer.analyze_predictions(example_combinations, example_winning, example_stars)
    analyzer.print_analysis_report()
