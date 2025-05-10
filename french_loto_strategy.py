import pandas as pd
import numpy as np
import random
import logging
import datetime
import database

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FrenchLotoStrategy:
    """
    Class for generating French Loto number predictions using various strategies.
    The French Loto uses 5 numbers (1-49) and 1 lucky number (1-10).
    """
    
    def __init__(self, statistics=None):
        """
        Initialize with statistics.
        
        Args:
            statistics: FrenchLotoStatistics object or None to create a new one
        """
        self.statistics = statistics
        
        # Load database data directly if statistics not provided
        if self.statistics is None:
            from french_loto_statistics import FrenchLotoStatistics
            self.statistics = FrenchLotoStatistics()
        
        # Number ranges
        self.main_range = range(1, 50)  # 1-49
        self.lucky_range = range(1, 11)  # 1-10
        
        # Previous combinations to avoid duplicates
        self.previous_combinations = []
        self.load_previous_combinations()
    
    def load_previous_combinations(self):
        """Load previously generated combinations from database"""
        try:
            # Get database connection
            conn = database.get_db_connection()
            if not conn:
                logger.error("Failed to connect to database")
                return
            
            # Query for previous combinations
            query = """
            SELECT numbers, lucky, date_generated 
            FROM french_loto_predictions 
            ORDER BY date_generated DESC
            LIMIT 50
            """
            
            previous = pd.read_sql_query(query, conn)
            
            # Convert to list of tuples for easy checking
            for _, row in previous.iterrows():
                numbers = [int(n) for n in row['numbers'].split('-')]
                lucky = int(row['lucky'])
                self.previous_combinations.append((numbers, lucky))
            
            logger.info(f"Loaded {len(self.previous_combinations)} previous combinations")
            
        except Exception as e:
            logger.error(f"Error loading previous combinations: {e}")
    
    def check_is_duplicate(self, numbers, lucky):
        """
        Check if a combination already exists in previous combinations.
        
        Args:
            numbers: List of 5 main numbers
            lucky: Lucky number
            
        Returns:
            bool: True if duplicate
        """
        # Sort numbers for consistent comparison
        sorted_numbers = sorted(numbers)
        
        # Check against previous combinations
        for prev_numbers, prev_lucky in self.previous_combinations:
            if sorted(prev_numbers) == sorted_numbers and prev_lucky == lucky:
                return True
        
        return False
    
    def frequency_based_strategy(self, hot_weight=0.7):
        """
        Generate a combination based on number frequency.
        
        Args:
            hot_weight: Weight for hot numbers (0-1)
            
        Returns:
            tuple: (list of 5 numbers, lucky number)
        """
        # Get weighted frequency
        weighted_freq = self.statistics.get_weighted_frequency()
        lucky_weighted_freq = self.statistics.get_weighted_lucky_frequency()
        
        if weighted_freq.empty or lucky_weighted_freq.empty:
            # Fall back to random selection if no data
            return self.random_strategy()
        
        # Hot numbers (higher frequency)
        hot_numbers = weighted_freq.sort_values(ascending=False).head(15).index.tolist()
        
        # Cold numbers (lower frequency)
        cold_numbers = weighted_freq.sort_values().head(15).index.tolist()
        
        # Hot lucky numbers
        hot_lucky = lucky_weighted_freq.sort_values(ascending=False).head(5).index.tolist()
        
        # Cold lucky numbers
        cold_lucky = lucky_weighted_freq.sort_values().head(5).index.tolist()
        
        # Mix hot and cold numbers based on weight
        hot_count = int(5 * hot_weight)
        cold_count = 5 - hot_count
        
        selected_numbers = []
        
        # Select hot numbers
        if hot_numbers and hot_count > 0:
            # Use probabilities from weighted frequency
            hot_probs = [weighted_freq[n] for n in hot_numbers]
            hot_probs = [p / sum(hot_probs) for p in hot_probs]  # Normalize
            
            selected_hot = np.random.choice(
                hot_numbers, 
                size=min(hot_count, len(hot_numbers)), 
                replace=False,
                p=hot_probs
            ).tolist()
            
            selected_numbers.extend(selected_hot)
        
        # Select cold numbers
        if cold_numbers and cold_count > 0:
            # Filter out already selected numbers
            available_cold = [n for n in cold_numbers if n not in selected_numbers]
            
            if available_cold:
                # Use inverse probabilities for cold numbers
                cold_probs = [1 - weighted_freq[n] for n in available_cold]
                cold_probs = [p / sum(cold_probs) for p in cold_probs]  # Normalize
                
                selected_cold = np.random.choice(
                    available_cold, 
                    size=min(cold_count, len(available_cold)), 
                    replace=False,
                    p=cold_probs
                ).tolist()
                
                selected_numbers.extend(selected_cold)
        
        # If we don't have 5 numbers yet, fill with random numbers
        while len(selected_numbers) < 5:
            # Get random number not already selected
            num = random.choice([n for n in self.main_range if n not in selected_numbers])
            selected_numbers.append(num)
        
        # Select lucky number with 70% from hot and 30% from cold
        if random.random() < 0.7:
            lucky = random.choice(hot_lucky if hot_lucky else list(self.lucky_range))
        else:
            lucky = random.choice(cold_lucky if cold_lucky else list(self.lucky_range))
        
        return sorted(selected_numbers), lucky
    
    def balanced_distribution_strategy(self):
        """
        Generate a combination with balanced distribution across number ranges.
        
        Returns:
            tuple: (list of 5 numbers, lucky number)
        """
        # Define number ranges: low (1-16), mid (17-32), high (33-49)
        low_range = list(range(1, 17))
        mid_range = list(range(17, 33))
        high_range = list(range(33, 50))
        
        # Try different distributions
        # French Loto historical data tends to favor 2-2-1 distribution
        distributions = [
            (2, 2, 1),  # 2 low, 2 mid, 1 high
            (2, 1, 2),  # 2 low, 1 mid, 2 high
            (1, 2, 2),  # 1 low, 2 mid, 2 high
            (1, 3, 1),  # 1 low, 3 mid, 1 high
            (3, 1, 1)   # 3 low, 1 mid, 1 high
        ]
        
        # Choose distribution based on weighted probabilities
        # 2-2-1 has highest probability based on historical patterns
        probs = [0.3, 0.2, 0.2, 0.15, 0.15]
        chosen_dist = distributions[np.random.choice(len(distributions), p=probs)]
        
        selected_numbers = []
        
        # Select from low range
        selected_numbers.extend(random.sample(low_range, chosen_dist[0]))
        
        # Select from mid range
        selected_numbers.extend(random.sample(mid_range, chosen_dist[1]))
        
        # Select from high range
        selected_numbers.extend(random.sample(high_range, chosen_dist[2]))
        
        # Select lucky number (slightly favor historically frequent numbers)
        lucky_weighted_freq = self.statistics.get_weighted_lucky_frequency()
        
        if not lucky_weighted_freq.empty and random.random() < 0.7:
            # Use probabilities from weighted frequency
            lucky_probs = lucky_weighted_freq.values
            lucky = np.random.choice(
                lucky_weighted_freq.index, 
                size=1, 
                p=lucky_probs / lucky_probs.sum()
            )[0]
        else:
            lucky = random.choice(list(self.lucky_range))
        
        return sorted(selected_numbers), lucky
    
    def pattern_based_strategy(self):
        """
        Generate a combination based on historical patterns.
        
        Returns:
            tuple: (list of 5 numbers, lucky number)
        """
        # Get pattern data from statistics
        even_odd_distribution = self.statistics.even_odd_distribution
        sum_distribution = self.statistics.sum_distribution
        range_distribution = self.statistics.range_distribution
        
        if not all([even_odd_distribution, sum_distribution, range_distribution]):
            # Fall back to random if pattern data not available
            return self.random_strategy()
        
        # Determine target pattern values based on historical probabilities
        
        # Target number of even numbers
        even_count_probs = list(even_odd_distribution.values())
        even_count_vals = list(even_odd_distribution.keys())
        target_even = np.random.choice(even_count_vals, p=even_count_probs)
        
        # Target sum range (e.g., '125-150')
        sum_range_probs = list(sum_distribution.values())
        sum_range_vals = list(sum_distribution.keys())
        target_sum_range = np.random.choice(sum_range_vals, p=sum_range_probs)
        
        # Parse sum range
        if target_sum_range == '<100':
            target_sum_min, target_sum_max = 0, 99
        elif target_sum_range == '>200':
            target_sum_min, target_sum_max = 201, 300
        else:
            target_sum_min, target_sum_max = map(int, target_sum_range.split('-'))
        
        # Target number range (spread between min and max)
        range_probs = list(range_distribution.values())
        range_vals = list(range_distribution.keys())
        target_range = np.random.choice(range_vals, p=range_probs)
        
        # Parse range
        if target_range == '<20':
            target_range_min, target_range_max = 0, 19
        elif target_range == '>40':
            target_range_min, target_range_max = 41, 50
        else:
            target_range_min, target_range_max = map(int, target_range.split('-'))
        
        # Generate numbers that satisfy the patterns
        max_attempts = 1000
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            
            # Generate random 5 numbers
            numbers = sorted(random.sample(list(self.main_range), 5))
            
            # Check pattern matching
            even_count = sum(1 for num in numbers if num % 2 == 0)
            num_sum = sum(numbers)
            num_range = max(numbers) - min(numbers)
            
            # Check if all patterns match
            if (even_count == target_even and
                target_sum_min <= num_sum <= target_sum_max and
                target_range_min <= num_range <= target_range_max):
                break
        
        # Select lucky number
        lucky_weighted_freq = self.statistics.get_weighted_lucky_frequency()
        
        if not lucky_weighted_freq.empty:
            lucky_probs = lucky_weighted_freq.values
            lucky = np.random.choice(
                lucky_weighted_freq.index, 
                size=1, 
                p=lucky_probs / lucky_probs.sum()
            )[0]
        else:
            lucky = random.choice(list(self.lucky_range))
        
        return numbers, lucky
    
    def random_strategy(self):
        """
        Generate a pure random combination.
        
        Returns:
            tuple: (list of 5 numbers, lucky number)
        """
        numbers = sorted(random.sample(list(self.main_range), 5))
        lucky = random.choice(list(self.lucky_range))
        
        return numbers, lucky
    
    def anti_popular_strategy(self):
        """
        Generate combination avoiding most popular numbers.
        
        Returns:
            tuple: (list of 5 numbers, lucky number)
        """
        # Get the frequency data
        number_freq = self.statistics.number_frequency
        lucky_freq = self.statistics.lucky_frequency
        
        if number_freq.empty or lucky_freq.empty:
            # Fall back to random
            return self.random_strategy()
        
        # Get middle-popularity numbers (avoid most and least popular)
        mid_numbers = number_freq.sort_values().iloc[10:40].index.tolist()
        
        # If not enough numbers, add more from the full range
        if len(mid_numbers) < 10:
            mid_numbers = list(self.main_range)
        
        # Choose 5 numbers from the mid-popularity range
        numbers = sorted(random.sample(mid_numbers, 5))
        
        # Choose a less common lucky number
        less_common_lucky = lucky_freq.sort_values().head(5).index.tolist()
        
        if less_common_lucky:
            lucky = random.choice(less_common_lucky)
        else:
            lucky = random.choice(list(self.lucky_range))
        
        return numbers, lucky
    
    def mixed_strategy(self):
        """
        Generate a combination using a mix of different strategies.
        
        Returns:
            tuple: (list of 5 numbers, lucky number, strategy_name)
        """
        # List of strategies with weights
        strategies = [
            (self.frequency_based_strategy, 0.35),
            (self.balanced_distribution_strategy, 0.25),
            (self.pattern_based_strategy, 0.25),
            (self.anti_popular_strategy, 0.15)
        ]
        
        # Choose a strategy based on weights
        strategy_funcs, weights = zip(*strategies)
        chosen_strategy = np.random.choice(strategy_funcs, p=weights)
        
        # Generate combination using the chosen strategy
        if chosen_strategy == self.frequency_based_strategy:
            # Randomize hot_weight parameter
            hot_weight = random.uniform(0.6, 0.8)
            numbers, lucky = chosen_strategy(hot_weight)
            strategy_name = "Frequency Analysis"
        else:
            numbers, lucky = chosen_strategy()
            
            # Assign strategy name based on the function
            if chosen_strategy == self.balanced_distribution_strategy:
                strategy_name = "Balanced Distribution"
            elif chosen_strategy == self.pattern_based_strategy:
                strategy_name = "Pattern Analysis"
            elif chosen_strategy == self.anti_popular_strategy:
                strategy_name = "Anti-Popular Numbers"
            else:
                strategy_name = "Mixed Strategy"
        
        return numbers, lucky, strategy_name
    
    def generate_combinations(self, count=5, avoid_duplicates=True):
        """
        Generate multiple combinations using different strategies.
        
        Args:
            count: Number of combinations to generate
            avoid_duplicates: Whether to avoid duplicates with previously generated combinations
            
        Returns:
            list: List of dictionaries with combination details
        """
        results = []
        
        # Generate a combination using each strategy
        strategies = [
            ("Frequency Analysis", lambda: self.frequency_based_strategy()),
            ("Balanced Distribution", lambda: self.balanced_distribution_strategy()),
            ("Pattern Analysis", lambda: self.pattern_based_strategy()),
            ("Anti-Popular Numbers", lambda: self.anti_popular_strategy()),
            ("Random Selection", lambda: self.random_strategy())
        ]
        
        # Generate required number of combinations
        while len(results) < count:
            if len(results) < len(strategies):
                # Use each core strategy once
                strategy_name, strategy_func = strategies[len(results)]
                numbers, lucky = strategy_func()
            else:
                # Use mixed strategy for additional combinations
                numbers, lucky, strategy_name = self.mixed_strategy()
            
            # Check for duplicates if needed
            if avoid_duplicates and self.check_is_duplicate(numbers, lucky):
                continue  # Skip and try again
            
            # Calculate a score for the combination (1-100)
            # Higher score means better aligned with historical patterns
            score = self.calculate_combination_score(numbers, lucky)
            
            # Add to results
            results.append({
                'numbers': '-'.join(map(str, numbers)),
                'lucky': lucky,
                'score': score,
                'strategy': strategy_name,
                'date_generated': datetime.datetime.now().date()
            })
        
        return results
    
    def calculate_combination_score(self, numbers, lucky):
        """
        Calculate a score for a combination based on historical patterns.
        
        Args:
            numbers: List of 5 main numbers
            lucky: Lucky number
            
        Returns:
            float: Score from 0-100
        """
        # Initialize score components
        frequency_score = 0
        pattern_score = 0
        lucky_score = 0
        
        # FREQUENCY COMPONENT (40%)
        # Check if frequency data is available
        if not self.statistics.number_frequency.empty:
            # Get frequencies for selected numbers
            frequencies = [self.statistics.number_frequency.get(num, 0) for num in numbers]
            avg_frequency = sum(frequencies) / 5
            
            # Scale to 0-40
            frequency_score = min(40, avg_frequency * 1000)
        else:
            frequency_score = 20  # Neutral if no data
        
        # PATTERN COMPONENT (40%)
        if all([self.statistics.even_odd_distribution, 
                self.statistics.sum_distribution, 
                self.statistics.range_distribution]):
            
            # Even-odd pattern (15%)
            even_count = sum(1 for num in numbers if num % 2 == 0)
            if even_count in self.statistics.even_odd_distribution:
                even_odd_prob = self.statistics.even_odd_distribution[even_count]
                even_odd_score = even_odd_prob * 15
            else:
                even_odd_score = 7.5  # Neutral
            
            # Sum pattern (15%)
            num_sum = sum(numbers)
            sum_score = 0
            for sum_range, prob in self.statistics.sum_distribution.items():
                if sum_range == '<100' and num_sum < 100:
                    sum_score = prob * 15
                    break
                elif sum_range == '>200' and num_sum > 200:
                    sum_score = prob * 15
                    break
                elif '-' in sum_range:
                    min_val, max_val = map(int, sum_range.split('-'))
                    if min_val <= num_sum <= max_val:
                        sum_score = prob * 15
                        break
            
            # Range pattern (10%)
            num_range = max(numbers) - min(numbers)
            range_score = 0
            for range_str, prob in self.statistics.range_distribution.items():
                if range_str == '<20' and num_range < 20:
                    range_score = prob * 10
                    break
                elif range_str == '>40' and num_range > 40:
                    range_score = prob * 10
                    break
                elif '-' in range_str:
                    min_val, max_val = map(int, range_str.split('-'))
                    if min_val <= num_range <= max_val:
                        range_score = prob * 10
                        break
            
            pattern_score = even_odd_score + sum_score + range_score
        else:
            pattern_score = 20  # Neutral if no pattern data
        
        # LUCKY NUMBER COMPONENT (20%)
        if not self.statistics.lucky_frequency.empty:
            lucky_freq = self.statistics.lucky_frequency.get(lucky, 0)
            lucky_score = min(20, lucky_freq * 200)
        else:
            lucky_score = 10  # Neutral if no data
        
        # Calculate total score
        total_score = frequency_score + pattern_score + lucky_score
        
        # Ensure score is between 0-100
        return max(0, min(100, total_score))
    
    def save_combinations_to_db(self, combinations):
        """
        Save generated combinations to the database.
        
        Args:
            combinations: List of combination dictionaries
            
        Returns:
            int: Number of combinations saved
        """
        try:
            # Connect to database
            conn = database.get_db_connection()
            if not conn:
                logger.error("Failed to connect to database")
                return 0
            
            # Create a cursor
            cur = conn.cursor()
            
            # Insert each combination
            inserted_count = 0
            for combo in combinations:
                # Check if combination already exists
                check_query = """
                SELECT COUNT(*) FROM french_loto_predictions
                WHERE numbers = %s AND lucky = %s
                """
                cur.execute(check_query, (combo['numbers'], combo['lucky']))
                exists = cur.fetchone()[0] > 0
                
                if not exists:
                    # Insert new combination
                    insert_query = """
                    INSERT INTO french_loto_predictions
                    (numbers, lucky, score, strategy, date_generated)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cur.execute(
                        insert_query,
                        (
                            combo['numbers'],
                            combo['lucky'],
                            combo['score'],
                            combo['strategy'],
                            combo['date_generated']
                        )
                    )
                    inserted_count += 1
            
            # Commit changes
            conn.commit()
            
            # Add to previous combinations to avoid duplicates
            for combo in combinations:
                numbers = [int(n) for n in combo['numbers'].split('-')]
                lucky = combo['lucky']
                self.previous_combinations.append((numbers, lucky))
            
            logger.info(f"Saved {inserted_count} new combinations to database")
            return inserted_count
            
        except Exception as e:
            logger.error(f"Error saving combinations to database: {e}")
            return 0