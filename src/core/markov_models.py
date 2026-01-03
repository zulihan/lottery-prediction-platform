"""
Enhanced Markov Chain Models

Multi-level transition tracking for more sophisticated Markov-based predictions:
- Direct transitions: number -> next number in same draw
- Position transitions: number at position i -> number at position i+2
- Combination transitions: (num1, num2) -> num3
"""

from collections import defaultdict, Counter
import random
import logging

logger = logging.getLogger(__name__)


class EnhancedMarkovModel:
    """
    Multi-dimensional Markov chain model for lottery number prediction.

    Tracks multiple levels of transitions to capture complex patterns
    in historical lottery data.
    """

    def __init__(self, historical_data):
        """
        Initialize the enhanced Markov model.

        Args:
            historical_data: List of dicts with 'numbers' key (sorted lists of 5 numbers)
        """
        self.historical_data = historical_data
        self.direct_transitions = defaultdict(Counter)
        self.position_transitions = defaultdict(Counter)
        self.combination_transitions = defaultdict(Counter)

        self._build_transitions()

    def _build_transitions(self):
        """
        Build multi-level transition matrices from historical data.
        """
        logger.info("Building enhanced Markov transition matrices...")

        for draw in self.historical_data:
            # Ensure numbers are sorted
            numbers = sorted(draw['numbers']) if isinstance(draw['numbers'], list) else sorted(draw['numbers'].tolist())

            # Build direct transitions (consecutive numbers in sorted draw)
            for i in range(len(numbers) - 1):
                self.direct_transitions[numbers[i]][numbers[i+1]] += 1

            # Build position transitions (2 positions apart)
            for i in range(len(numbers) - 2):
                self.position_transitions[numbers[i]][numbers[i+2]] += 1

            # Build combination transitions (pairs -> third number)
            for i in range(len(numbers) - 2):
                pair = (numbers[i], numbers[i+1])
                self.combination_transitions[pair][numbers[i+2]] += 1

        logger.info(f"Built transitions from {len(self.historical_data)} historical draws")
        logger.info(f"  - Direct transitions: {len(self.direct_transitions)} states")
        logger.info(f"  - Position transitions: {len(self.position_transitions)} states")
        logger.info(f"  - Combination transitions: {len(self.combination_transitions)} states")

    def score_number_with_transitions(self, number, existing_numbers):
        """
        Score a candidate number based on multi-level Markov transitions.

        Args:
            number: Candidate number to score
            existing_numbers: List of numbers already in the combination

        Returns:
            float: Score based on transition probabilities
        """
        score = 0.0

        # Direct transitions from existing numbers (weight: 2.0)
        for existing in existing_numbers:
            if number in self.direct_transitions[existing]:
                freq = self.direct_transitions[existing][number]
                score += freq * 2.0

        # Position transitions (weight: 1.5)
        for existing in existing_numbers:
            if number in self.position_transitions[existing]:
                freq = self.position_transitions[existing][number]
                score += freq * 1.5

        # Combination transitions (weight: 3.0 - highest weight)
        if len(existing_numbers) >= 2:
            for i in range(len(existing_numbers) - 1):
                pair = (existing_numbers[i], existing_numbers[i+1])
                if number in self.combination_transitions[pair]:
                    freq = self.combination_transitions[pair][number]
                    score += freq * 3.0

        return score

    def predict_next_numbers(self, num_predictions=5, seed_numbers=None):
        """
        Predict the next set of numbers using multi-level transitions.

        Args:
            num_predictions: Number of numbers to predict
            seed_numbers: Starting numbers (default: use most frequent)

        Returns:
            list: Predicted numbers
        """
        if seed_numbers is None:
            # Start with most common numbers from direct transitions
            all_numbers = []
            for num_dict in self.direct_transitions.values():
                all_numbers.extend(num_dict.keys())
            number_freq = Counter(all_numbers)
            seed_numbers = [number_freq.most_common(1)[0][0]] if number_freq else [random.randint(1, 50)]

        predicted = list(seed_numbers)

        while len(predicted) < num_predictions:
            # Score all candidate numbers
            candidates = {}
            for candidate in range(1, 51):
                if candidate not in predicted:
                    score = self.score_number_with_transitions(candidate, predicted)
                    if score > 0:  # Only consider numbers with positive score
                        candidates[candidate] = score

            if not candidates:
                # Fallback: pick random unused number
                available = [n for n in range(1, 51) if n not in predicted]
                if available:
                    predicted.append(random.choice(available))
                else:
                    break
            else:
                # Select number with highest score
                best_number = max(candidates.items(), key=lambda x: x[1])[0]
                predicted.append(best_number)

        return sorted(predicted[:num_predictions])

    def generate_combinations(self, num_combinations=5):
        """
        Generate multiple combinations using enhanced Markov model.

        Args:
            num_combinations: Number of combinations to generate

        Returns:
            list: List of number combinations (lists of 5 numbers)
        """
        combinations = []

        # Get most frequent numbers as potential seeds
        all_numbers = []
        for num_dict in self.direct_transitions.values():
            all_numbers.extend(num_dict.keys())
        number_freq = Counter(all_numbers)
        frequent_numbers = [num for num, _ in number_freq.most_common(20)]

        for i in range(num_combinations):
            # Vary seed to get diverse combinations
            if frequent_numbers:
                seed = [frequent_numbers[i % len(frequent_numbers)]]
            else:
                seed = [random.randint(1, 50)]

            combination = self.predict_next_numbers(num_predictions=5, seed_numbers=seed)
            combinations.append(combination)

        return combinations

    def get_transition_probabilities(self, number):
        """
        Get transition probabilities for a given number.

        Args:
            number: The number to get transitions for

        Returns:
            dict: Transition probabilities for all three levels
        """
        return {
            'direct': dict(self.direct_transitions[number]),
            'position': dict(self.position_transitions[number]),
            'combination': {
                str(pair): dict(trans)
                for pair, trans in self.combination_transitions.items()
                if number in pair
            }
        }

    def get_most_likely_next(self, current_number, transition_type='direct'):
        """
        Get the most likely next number given current number.

        Args:
            current_number: Current number
            transition_type: Type of transition ('direct', 'position', or 'combination')

        Returns:
            int or None: Most likely next number
        """
        if transition_type == 'direct':
            transitions = self.direct_transitions[current_number]
        elif transition_type == 'position':
            transitions = self.position_transitions[current_number]
        else:
            logger.warning(f"Invalid transition type: {transition_type}. Using 'direct'.")
            transitions = self.direct_transitions[current_number]

        if transitions:
            return transitions.most_common(1)[0][0]
        return None


# Helper function for easy integration with existing strategies
def create_markov_predictions(historical_data, num_combinations=5):
    """
    Create Markov-based predictions using enhanced multi-level transitions.

    Args:
        historical_data: List of historical draws with 'numbers' key
        num_combinations: Number of combinations to generate

    Returns:
        list: Generated combinations
    """
    model = EnhancedMarkovModel(historical_data)
    return model.generate_combinations(num_combinations)


# Example usage
if __name__ == "__main__":
    # Test with example data
    example_data = [
        {'numbers': [1, 8, 13, 21, 34]},
        {'numbers': [2, 13, 21, 34, 47]},
        {'numbers': [5, 13, 21, 29, 47]},
        {'numbers': [1, 8, 21, 34, 40]},
        {'numbers': [3, 13, 21, 29, 47]},
    ]

    model = EnhancedMarkovModel(example_data)
    predictions = model.generate_combinations(num_combinations=3)
    print("Enhanced Markov predictions:")
    for i, pred in enumerate(predictions, 1):
        print(f"  {i}. {pred}")
