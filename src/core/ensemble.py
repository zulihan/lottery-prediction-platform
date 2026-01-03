"""
Ensemble Strategy Module

Advanced meta-strategies that combine and filter multiple base strategies
for improved prediction performance.

Includes:
- Fibonacci-Filtered Hybrid Strategy (2-pass approach)
- Strategic Fusion Ensemble (cross-strategy combination)
"""

import random
from collections import Counter
import logging

logger = logging.getLogger(__name__)


def get_fibonacci_numbers(max_val=50):
    """
    Get Fibonacci numbers within lottery range.

    Args:
        max_val: Maximum value (default 50 for Euromillions)

    Returns:
        list: Fibonacci numbers in range
    """
    fib = [1, 1]
    while fib[-1] < max_val:
        fib.append(fib[-1] + fib[-2])

    # Remove duplicates and filter to range
    fibonacci_in_range = sorted(list(set([f for f in fib if 1 <= f <= max_val])))
    return fibonacci_in_range


class EnsembleStrategies:
    """
    Ensemble meta-strategies for lottery prediction.

    Combines multiple base strategies using advanced filtering and fusion techniques.
    """

    def __init__(self, base_strategies):
        """
        Initialize ensemble strategies.

        Args:
            base_strategies: PredictionStrategies instance with base strategy methods
        """
        self.strategies = base_strategies
        self.fibonacci_numbers = get_fibonacci_numbers()

    def fibonacci_filtered_hybrid_strategy(self, num_combinations=5, num_per_strategy=8):
        """
        Fibonacci-Filtered Hybrid Strategy - Two-pass meta-strategy.

        Phase 1: Generate candidates from multiple base strategies
        Phase 2: Apply Fibonacci mathematical filtering
        Phase 3: Select best with diversity constraints

        Args:
            num_combinations: Number of final combinations to return
            num_per_strategy: Number of candidates to generate per base strategy

        Returns:
            list: Filtered and scored combinations
        """
        logger.info(f"=== Fibonacci-Filtered Hybrid Strategy ===")
        logger.info(f"Generating {num_per_strategy} candidates from 4 base strategies...")

        # Phase 1: Generate candidates from base strategies
        candidates = {
            'risk_reward': self.strategies.risk_reward_strategy(
                num_combinations=num_per_strategy,
                risk_level=0.5
            ),
            'frequency': self.strategies.frequency_strategy(
                num_combinations=num_per_strategy,
                recent_weight=0.6
            ),
            'markov': self.strategies.markov_strategy(
                num_combinations=num_per_strategy,
                lag=1
            ),
            'coverage': self.strategies.coverage_strategy(
                num_combinations=num_per_strategy,
                balanced=True
            )
        }

        # Phase 2: Apply Fibonacci filtering
        filtered_combinations = self._apply_fibonacci_filtering(candidates)

        # Phase 3: Select best with diversity constraints
        selected = self._select_with_diversity(
            filtered_combinations,
            num_final=num_combinations
        )

        logger.info(f"Selected {len(selected)} final combinations with Fibonacci filtering")
        return selected

    def _apply_fibonacci_filtering(self, candidates):
        """
        Apply Fibonacci mathematical filtering to enhance and score combinations.

        Args:
            candidates: dict of {strategy_name: [combinations]}

        Returns:
            list: Filtered combinations with enhanced scores
        """
        filtered_combinations = []

        for strategy_name, strategy_candidates in candidates.items():
            for candidate in strategy_candidates:
                # Calculate Fibonacci metrics
                fib_count = len([n for n in candidate['numbers'] if n in self.fibonacci_numbers])
                fib_percentage = fib_count / 5 * 100

                # Calculate Fibonacci score boost
                fibonacci_boost = 0

                # Boost for Fibonacci presence
                if fib_percentage >= 60:  # 3+ Fibonacci numbers
                    fibonacci_boost += 25
                elif fib_percentage >= 40:  # 2 Fibonacci numbers
                    fibonacci_boost += 15
                elif fib_percentage >= 20:  # 1 Fibonacci number
                    fibonacci_boost += 8

                # Bonus for specific Fibonacci patterns
                if 1 in candidate['numbers'] and 8 in candidate['numbers']:
                    fibonacci_boost += 10
                if 13 in candidate['numbers']:
                    fibonacci_boost += 8
                if 21 in candidate['numbers']:
                    fibonacci_boost += 5

                # Star bonuses (common winning stars)
                star_boost = 0
                if 5 in candidate['stars']:
                    star_boost += 5
                if 6 in candidate['stars']:
                    star_boost += 5
                if 8 in candidate['stars']:
                    star_boost += 3

                # Calculate final hybrid score
                base_score = candidate.get('score', 50)
                final_score = min(base_score + fibonacci_boost + star_boost, 100.0)

                # Create enhanced combination
                enhanced_combo = {
                    'numbers': candidate['numbers'],
                    'stars': candidate['stars'],
                    'strategy': f"Fibonacci-Filtered {strategy_name.replace('_', ' ').title()}",
                    'base_strategy': strategy_name,
                    'fibonacci_count': fib_count,
                    'fibonacci_percentage': fib_percentage,
                    'base_score': base_score,
                    'fibonacci_boost': fibonacci_boost,
                    'star_boost': star_boost,
                    'score': final_score
                }

                filtered_combinations.append(enhanced_combo)

        # Sort by final score
        filtered_combinations.sort(key=lambda x: x['score'], reverse=True)

        return filtered_combinations

    def _select_with_diversity(self, filtered_combinations, num_final=8):
        """
        Select best combinations with diversity constraints.

        Prevents overusing specific numbers or strategies.

        Args:
            filtered_combinations: List of scored combinations
            num_final: Number of final combinations to select

        Returns:
            list: Selected combinations with diversity
        """
        selected = []
        number_usage = Counter()
        strategy_usage = Counter()

        for combo in filtered_combinations:
            # Enforce diversity constraints
            # - Max 2 uses per number across all combinations
            # - Max 3 combinations per base strategy
            numbers_ok = all(number_usage[n] < 2 for n in combo['numbers'])
            strategy_ok = strategy_usage[combo['base_strategy']] < 3

            if numbers_ok and strategy_ok and len(selected) < num_final:
                selected.append(combo)

                # Update usage counters
                for n in combo['numbers']:
                    number_usage[n] += 1
                strategy_usage[combo['base_strategy']] += 1

        return selected

    def strategic_fusion_ensemble(self, num_combinations=5, fusion_types=None):
        """
        Strategic Fusion Ensemble - Combines elements from different strategies.

        Uses multiple fusion techniques:
        - Cross-strategy fusion (structural combination)
        - Mathematical averaging (positional)
        - Frequency-weighted fusion

        Args:
            num_combinations: Number of combinations to generate
            fusion_types: List of fusion types to use (default: all)

        Returns:
            list: Fused combinations
        """
        if fusion_types is None:
            fusion_types = ['cross_strategy', 'mathematical', 'frequency']

        logger.info(f"=== Strategic Fusion Ensemble ===")
        logger.info(f"Fusion types: {fusion_types}")

        # Generate base combinations from different strategies
        risk_combos = self.strategies.risk_reward_strategy(num_combinations=5, risk_level=0.5)
        coverage_combos = self.strategies.coverage_strategy(num_combinations=5, balanced=True)
        markov_combos = self.strategies.markov_strategy(num_combinations=5, lag=1)

        analysis = {
            'risk_reward': risk_combos,
            'coverage': coverage_combos,
            'markov': markov_combos
        }

        all_fusions = []

        # Apply different fusion techniques
        if 'cross_strategy' in fusion_types:
            fusions = self._cross_strategy_fusion(analysis, num_fusions=2)
            all_fusions.extend(fusions)

        if 'mathematical' in fusion_types:
            all_combos = risk_combos + coverage_combos + markov_combos
            fusions = self._mathematical_averaging_fusion(all_combos, num_fusions=2)
            all_fusions.extend(fusions)

        if 'frequency' in fusion_types:
            all_combos = risk_combos + coverage_combos + markov_combos
            fusions = self._frequency_weighted_fusion(all_combos, num_fusions=1)
            all_fusions.extend(fusions)

        # Select best fusions
        return all_fusions[:num_combinations]

    def _cross_strategy_fusion(self, analysis, num_fusions=3):
        """
        Create fusions by combining structural elements from different strategies.

        Takes specific numbers from each strategy type:
        - 2 numbers from Risk-Reward
        - 2 numbers from Coverage
        - 1 number from Markov

        Args:
            analysis: dict with strategy combinations
            num_fusions: Number of fusions to create

        Returns:
            list: Fused combinations
        """
        risk_combos = analysis['risk_reward']
        coverage_combos = analysis['coverage']
        markov_combos = analysis['markov']

        fusions = []

        for i in range(num_fusions):
            fusion_numbers = []
            fusion_stars = []

            # Take 2 numbers from Risk-Reward strategy
            risk_combo = risk_combos[i % len(risk_combos)]
            fusion_numbers.extend(random.sample(risk_combo['numbers'], 2))

            # Take 2 numbers from Coverage strategy (avoid duplicates)
            coverage_combo = coverage_combos[i % len(coverage_combos)]
            coverage_available = [n for n in coverage_combo['numbers'] if n not in fusion_numbers]
            if len(coverage_available) >= 2:
                fusion_numbers.extend(random.sample(coverage_available, 2))
            elif coverage_available:
                fusion_numbers.extend(coverage_available[:1])

            # Take 1 number from Markov strategy (fill to 5)
            while len(fusion_numbers) < 5:
                markov_combo = markov_combos[i % len(markov_combos)]
                markov_available = [n for n in markov_combo['numbers'] if n not in fusion_numbers]
                if markov_available:
                    fusion_numbers.append(random.choice(markov_available))
                else:
                    # Fallback: pick any number from all combos not yet used
                    all_nums = set()
                    for combo in risk_combos + coverage_combos + markov_combos:
                        all_nums.update(combo['numbers'])
                    remaining = [n for n in all_nums if n not in fusion_numbers]
                    if remaining:
                        fusion_numbers.append(random.choice(remaining))
                    else:
                        break

            # Combine stars from different strategies
            fusion_stars = [risk_combo['stars'][0], coverage_combo['stars'][0]]
            if fusion_stars[0] == fusion_stars[1] and len(coverage_combo['stars']) > 1:
                fusion_stars[1] = coverage_combo['stars'][1]

            fusions.append({
                'numbers': sorted(fusion_numbers[:5]),
                'stars': sorted(fusion_stars),
                'strategy': f'Cross-Strategy Fusion {i+1}',
                'score': 75.0
            })

        return fusions

    def _mathematical_averaging_fusion(self, combinations, num_fusions=2):
        """
        Create fusions using mathematical averaging of position-wise values.

        Averages the 1st number with 1st number, 2nd with 2nd, etc.

        Args:
            combinations: List of combinations to fuse
            num_fusions: Number of fusions to create

        Returns:
            list: Averaged combinations
        """
        fusions = []

        for i in range(num_fusions):
            # Select two combinations to average
            combo1 = combinations[i * 2 % len(combinations)]
            combo2 = combinations[(i * 2 + 1) % len(combinations)]

            # Average corresponding positions
            averaged_numbers = []
            for pos in range(5):
                if pos < len(combo1['numbers']) and pos < len(combo2['numbers']):
                    avg = round((combo1['numbers'][pos] + combo2['numbers'][pos]) / 2)
                    averaged_numbers.append(avg)

            # Remove duplicates and fill if needed
            averaged_numbers = list(dict.fromkeys(averaged_numbers))

            while len(averaged_numbers) < 5:
                all_nums = combo1['numbers'] + combo2['numbers']
                candidates = [n for n in all_nums if n not in averaged_numbers]
                if candidates:
                    averaged_numbers.append(random.choice(candidates))
                else:
                    break

            # Average stars (union)
            all_stars = combo1['stars'] + combo2['stars']
            averaged_stars = sorted(list(set(all_stars)))[:2]

            fusions.append({
                'numbers': sorted(averaged_numbers[:5]),
                'stars': averaged_stars,
                'strategy': f'Mathematical Averaging Fusion {i+1}',
                'score': 70.0
            })

        return fusions

    def _frequency_weighted_fusion(self, combinations, num_fusions=1):
        """
        Create fusions based on number frequency across all combinations.

        Args:
            combinations: List of combinations
            num_fusions: Number of fusions to create

        Returns:
            list: Frequency-weighted combinations
        """
        all_numbers = []
        all_stars = []

        for combo in combinations:
            all_numbers.extend(combo['numbers'])
            all_stars.extend(combo['stars'])

        number_freq = Counter(all_numbers)
        star_freq = Counter(all_stars)

        fusions = []

        for i in range(num_fusions):
            # Select top frequent numbers with variation
            start_idx = i * 3
            top_numbers = [n for n, freq in number_freq.most_common(20)]
            fusion_numbers = top_numbers[start_idx:start_idx+5]

            # Select top frequent stars
            top_stars = [s for s, freq in star_freq.most_common(6)]
            fusion_stars = top_stars[i:i+2] if i+1 < len(top_stars) else top_stars[:2]

            fusions.append({
                'numbers': sorted(fusion_numbers),
                'stars': sorted(fusion_stars),
                'strategy': f'Frequency-Weighted Fusion {i+1}',
                'score': 72.0
            })

        return fusions
