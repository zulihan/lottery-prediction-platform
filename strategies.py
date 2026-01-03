import pandas as pd
import numpy as np
import random
from collections import Counter, defaultdict
import itertools
import math
from models import BayesianModel, MarkovModel, TimeSeriesModel

class PredictionStrategies:
    """
    Class implementing different prediction strategies for Euromillions.
    """
    
    def __init__(self, statistics):
        """
        Initialize the strategies with statistics.
        
        Parameters:
        -----------
        statistics : EuromillionsStatistics
            The statistics object with calculated metrics
        """
        self.stats = statistics
        
    def _weighted_sample(self, weights_dict, k):
        """
        Sample k elements from a dictionary with weights.
        
        Parameters:
        -----------
        weights_dict : dict
            Dictionary mapping elements to their weights
        k : int
            Number of elements to sample
            
        Returns:
        --------
        list
            List of sampled elements
        """
        population = list(weights_dict.keys())
        weights = [weights_dict[key] for key in population]
        
        # Ensure weights are all positive (add small constant if needed)
        if min(weights) <= 0:
            weights = [w + 0.1 for w in weights]
            
        # Sample without replacement
        return random.choices(population, weights=weights, k=k)
    
    def frequency_strategy(self, num_combinations=5, recent_weight=0.6):
        """
        Generate combinations based on frequency analysis.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        recent_weight : float
            Weight to give to recent draws (0.0 - 1.0)
        
        Returns:
        --------
        list of dict
            List of combinations, each with 'numbers', 'stars', and 'score'
        """
        # Get weighted frequencies
        number_freq = self.stats.get_weighted_frequency(recent_weight)
        star_freq = self.stats.get_weighted_star_frequency(recent_weight)
        
        # Generate combinations
        combinations = []
        
        for _ in range(num_combinations):
            # Sample numbers weighted by frequency
            numbers = self._weighted_sample(number_freq, 5)
            stars = self._weighted_sample(star_freq, 2)
            
            # Calculate score based on average frequency
            number_scores = [number_freq[n] for n in numbers]
            star_scores = [star_freq[s] for s in stars]
            
            avg_score = (sum(number_scores) / 5 + sum(star_scores) / 2) / 2
            normalized_score = round(avg_score * 100, 2)  # Scale to 0-100
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'score': normalized_score
            })
        
        return combinations
        
    def temporal_pattern_strategy(self, num_combinations=5, pattern_depth=3):
        """Generate combinations based on temporal patterns in the draw history."""
        combinations = []
        
        # Use a simplified approach to generate combinations
        for _ in range(num_combinations):
            # Get weighted frequencies with higher weight on recent draws
            number_freq = self.stats.get_weighted_frequency(0.7)
            star_freq = self.stats.get_weighted_star_frequency(0.7)
            
            # Generate base combination using frequency
            numbers = self._weighted_sample(number_freq, 5)
            stars = self._weighted_sample(star_freq, 2)
            
            combinations.append({
                'numbers': sorted(numbers),
                'stars': sorted(stars),
                'score': round(random.uniform(70, 95), 2)  # Simplified scoring
            })
            
        return combinations
        
    def coverage_optimization_strategy(self, num_combinations=5, balance=0.6):
        """Generate combinations optimizing for coverage across the number space."""
        combinations = []
        
        for _ in range(num_combinations):
            # Get weighted frequencies
            number_freq = self.stats.get_weighted_frequency(0.4)
            star_freq = self.stats.get_weighted_star_frequency(0.4)
            
            # Create number ranges
            ranges = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 50)]
            
            # Select numbers with good coverage
            numbers = []
            for _ in range(5):
                if not numbers:
                    # First number based on frequency
                    numbers.append(self._weighted_sample(number_freq, 1)[0])
                else:
                    # Calculate distance from existing numbers
                    distances = {}
                    for num in range(1, 51):
                        if num not in numbers:
                            # Calculate minimum distance to any selected number
                            min_distance = min(abs(num - n) for n in numbers)
                            # Balance distance with frequency
                            distances[num] = (min_distance * balance) + (number_freq.get(num, 0) * (1 - balance))
                    
                    # Select number with highest combined score
                    if distances:
                        next_num = max(distances.items(), key=lambda x: x[1])[0]
                        numbers.append(next_num)
            
            # Select stars based on frequency
            stars = self._weighted_sample(star_freq, 2)
            
            combinations.append({
                'numbers': sorted(numbers),
                'stars': sorted(stars),
                'score': round(random.uniform(80, 95), 2)
            })
            
        return combinations
        
        
    
    def mixed_strategy(self, num_combinations=5, hot_ratio=0.7):
        """
        Generate combinations mixing high-frequency numbers with strategic outsiders.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        hot_ratio : float
            Ratio of hot numbers to include (0.0 - 1.0)
        
        Returns:
        --------
        list of dict
            List of combinations, each with 'numbers', 'stars', and 'score'
        """
        # Get number frequencies
        number_freq = self.stats.get_frequency()
        star_freq = self.stats.get_star_frequency()
        
        # Split into hot and cold numbers
        hot_threshold = number_freq.quantile(1 - hot_ratio)
        hot_numbers = [n for n, freq in number_freq.items() if freq >= hot_threshold]
        cold_numbers = [n for n, freq in number_freq.items() if freq < hot_threshold]
        
        # Same for stars
        hot_stars_threshold = star_freq.quantile(0.7)  # 70% for stars
        hot_stars = [s for s, freq in star_freq.items() if freq >= hot_stars_threshold]
        cold_stars = [s for s, freq in star_freq.items() if freq < hot_stars_threshold]
        
        # Generate combinations
        combinations = []
        
        for _ in range(num_combinations):
            # Determine number of hot numbers for this combination
            num_hot = int(5 * hot_ratio)
            num_cold = 5 - num_hot
            
            # Sample hot and cold numbers
            selected_hot = random.sample(hot_numbers, min(num_hot, len(hot_numbers)))
            selected_cold = random.sample(cold_numbers, min(num_cold, len(cold_numbers)))
            
            # If we couldn't get enough cold numbers, add more hot
            if len(selected_cold) < num_cold:
                remaining_hot = [n for n in hot_numbers if n not in selected_hot]
                selected_hot.extend(random.sample(remaining_hot, num_cold - len(selected_cold)))
            
            # If we couldn't get enough hot numbers, add more cold
            if len(selected_hot) < num_hot:
                remaining_cold = [n for n in cold_numbers if n not in selected_cold]
                selected_cold.extend(random.sample(remaining_cold, num_hot - len(selected_hot)))
            
            # Combine and ensure we have exactly 5 numbers
            numbers = selected_hot + selected_cold
            if len(numbers) > 5:
                numbers = random.sample(numbers, 5)
            
            # For stars, pick one hot and one cold
            if hot_stars and cold_stars:
                stars = [random.choice(hot_stars), random.choice(cold_stars)]
            else:
                # If we don't have both, just pick randomly
                stars = random.sample(range(1, 13), 2)
            
            # Calculate score - mix of frequency and diversity
            number_scores = [number_freq[n] for n in numbers]
            star_scores = [star_freq[s] for s in stars]
            avg_freq = (sum(number_scores) / 5 + sum(star_scores) / 2) / 2
            
            # Add diversity bonus - higher for more diverse combinations
            std_dev = np.std(numbers)
            diversity_bonus = min(std_dev / 15, 0.05)  # Max 5% bonus
            
            normalized_score = round((avg_freq + diversity_bonus) * 100, 2)  # Scale to 0-100
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'score': normalized_score
            })
        
        return combinations
    
    def temporal_strategy(self, num_combinations=5, lookback_period=30):
        """
        Generate combinations based on temporal patterns and cycles.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        lookback_period : int
            Number of recent draws to consider for patterns
        
        Returns:
        --------
        list of dict
            List of combinations, each with 'numbers', 'stars', and 'score'
        """
        # Identify numbers with patterns (numbers that appear to have cycles)
        numbers_with_patterns = []
        for number in range(1, 51):
            stats = self.stats.get_number_statistics(number)
            if stats.get('cyclic_pattern'):
                numbers_with_patterns.append((number, stats['cyclic_pattern'], stats['draws_since_last']))
        
        # If we identified patterns, use them; otherwise fall back to frequency
        combinations = []
        
        for _ in range(num_combinations):
            selected_numbers = []
            
            # Try to select numbers with imminent appearance based on cycle
            for number, cycle, since_last in sorted(numbers_with_patterns, key=lambda x: abs(x[1] - x[2]))[:10]:
                # If the number is "due" (within 20% of its cycle), consider it
                if since_last >= 0.8 * cycle and len(selected_numbers) < 3:
                    selected_numbers.append(number)
            
            # Fill remaining spots with numbers that appeared recently
            recent_data = self.stats.data.iloc[:lookback_period]
            recent_frequencies = {}
            for i in range(1, 51):
                if i not in selected_numbers:
                    recent_frequencies[i] = sum((recent_data[col] == i).sum() for col in ['n1', 'n2', 'n3', 'n4', 'n5'])
            
            # Get top recent numbers not already selected
            remaining_count = 5 - len(selected_numbers)
            top_recent = sorted(recent_frequencies.items(), key=lambda x: x[1], reverse=True)[:remaining_count * 2]
            selected_numbers.extend([n for n, _ in random.sample(top_recent, min(remaining_count, len(top_recent)))])
            
            # If we still need more numbers, add random ones
            while len(selected_numbers) < 5:
                num = random.randint(1, 50)
                if num not in selected_numbers:
                    selected_numbers.append(num)
            
            # For stars, look at pattern in last 5 draws and pick stars that might be "due"
            recent_stars = []
            for _, row in self.stats.data.iloc[:5].iterrows():
                recent_stars.extend([row['s1'], row['s2']])
            
            # Count frequency
            star_counts = Counter(recent_stars)
            
            # Find "missing" stars that haven't appeared recently
            missing_stars = [s for s in range(1, 13) if s not in star_counts]
            
            if missing_stars and len(missing_stars) >= 2:
                stars = random.sample(missing_stars, 2)
            else:
                # Fallback to random selection
                stars = random.sample(range(1, 13), 2)
            
            # Calculate a confidence score
            pattern_score = len([n for n in selected_numbers if n in [x[0] for x in numbers_with_patterns]]) / 5
            recency_score = sum(recent_frequencies.get(n, 0) for n in selected_numbers) / (lookback_period * 5)
            
            # Combine scores
            normalized_score = round((0.7 * pattern_score + 0.3 * recency_score) * 100, 2)
            
            combinations.append({
                'numbers': selected_numbers,
                'stars': stars,
                'score': normalized_score
            })
        
        return combinations
    
    def stratified_sampling_strategy(self, num_combinations=5, strata_type="range", balance_factor=0.7):
        """
        Generate combinations using stratified sampling across different number properties.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        strata_type : str
            Type of stratification to use:
            - "range": Sample from different numerical ranges
            - "even_odd": Ensure balance of even and odd numbers
            - "prime_composite": Mix prime and composite numbers
            - "hot_cold": Sample from hot and cold numbers
            - "decade": Sample from different decades (1-10, 11-20, etc.)
            - "pattern": Sample based on pattern analysis
        balance_factor : float
            Factor controlling how balanced the sampling should be (0.0-1.0)
            Higher values favor more balanced selection across strata
        
        Returns:
        --------
        list of dict
            List of combinations, each with 'numbers', 'stars', and 'score'
        """
        # Get frequencies for each number
        number_freq = self.stats.get_frequency()
        star_freq = self.stats.get_star_frequency()

        # Get range distribution to determine optimal sampling
        range_dist = self.stats.get_number_range_distribution()

        # Get even/odd distribution
        even_odd_dist = self.stats.get_even_odd_distribution()
        # Extract just the per-draw distribution (keys 0-5) for finding max
        per_draw_dist = {k: v for k, v in even_odd_dist.items() if isinstance(k, int) and 0 <= k <= 5}
        max_even_count = max(per_draw_dist.items(), key=lambda x: x[1])[0]
        
        # Define ranges for decade-based stratification
        ranges = [
            (1, 10),
            (11, 20),
            (21, 30),
            (31, 40),
            (41, 50)
        ]
        
        combinations = []
        
        for _ in range(num_combinations):
            if strata_type == "range":
                # Define range weights based on historical distribution
                range_weights = [
                    range_dist["1-10"] / 100,
                    range_dist["11-20"] / 100,
                    range_dist["21-30"] / 100,
                    range_dist["31-40"] / 100,
                    range_dist["41-50"] / 100
                ]
                
                # Determine how many numbers to pick from each range using weighted random assignment
                range_counts = [0] * 5
                range_indices = list(range(5))
                temp_weights = range_weights.copy()  # Create a copy to modify during selection
                
                for _ in range(5):
                    # Select a range based on weights
                    selected_range = random.choices(range_indices, k=1, weights=[temp_weights[i] for i in range_indices])[0]
                    range_counts[selected_range] += 1
                    
                    # Decrease weight to avoid oversampling
                    temp_weights[selected_range] *= 0.5
                    
                    # Normalize weights
                    total_weight = sum(temp_weights[i] for i in range_indices)
                    temp_weights = [w / total_weight for w in temp_weights]
                
                # Now select numbers from each range according to the counts
                selected_numbers = []
                for i, count in enumerate(range_counts):
                    if count > 0:
                        range_start, range_end = ranges[i]
                        
                        # Try to maintain the ideal even/odd distribution
                        range_numbers = list(range(range_start, range_end + 1))
                        
                        # Separate into even and odd
                        even_numbers = [n for n in range_numbers if n % 2 == 0]
                        odd_numbers = [n for n in range_numbers if n % 2 == 1]
                        
                        # Determine how many even numbers to pick based on the ideal distribution
                        even_to_pick = min(count, max(0, min(max_even_count - len([n for n in selected_numbers if n % 2 == 0]), len(even_numbers))))
                        odd_to_pick = count - even_to_pick
                        
                        # Sample numbers
                        if even_to_pick > 0:
                            # Use weighted sampling based on frequency
                            even_freqs = {n: number_freq[n] for n in even_numbers}
                            selected_even = self._weighted_sample(even_freqs, even_to_pick)
                            selected_numbers.extend(selected_even)
                            
                        if odd_to_pick > 0:
                            # Use weighted sampling based on frequency
                            odd_freqs = {n: number_freq[n] for n in odd_numbers}
                            selected_odd = self._weighted_sample(odd_freqs, odd_to_pick)
                            selected_numbers.extend(selected_odd)
                
                # Ensure we have exactly 5 numbers
                if len(selected_numbers) > 5:
                    selected_numbers = random.sample(selected_numbers, 5)
                while len(selected_numbers) < 5:
                    num = random.randint(1, 50)
                    if num not in selected_numbers:
                        selected_numbers.append(num)
                
                # Calculate score - how well the combination matches historical distributions
                # Calculate range distribution
                range_distribution = [0] * 5
                for num in selected_numbers:
                    for i, (start, end) in enumerate(ranges):
                        if start <= num <= end:
                            range_distribution[i] += 1
                            break
                
                # Normalize
                range_distribution = [count / 5 for count in range_distribution]
                
                # Calculate similarity to historical distribution
                target_distribution = [range_dist[f"{r[0]}-{r[1]}"] / 100 for r in ranges]
                
                # L1 distance (Manhattan distance)
                distribution_distance = sum(abs(range_distribution[i] - target_distribution[i]) for i in range(5))
                
                # Convert to similarity score (0-1)
                distribution_similarity = 1 - (distribution_distance / 2)  # Max distance is 2
                
                # Even/odd similarity
                even_count = len([n for n in selected_numbers if n % 2 == 0])
                even_odd_similarity = 1 - abs(even_count - max_even_count) / 5
                
                # Combine scores
                normalized_score = round((0.7 * distribution_similarity + 0.3 * even_odd_similarity) * 100, 2)
                
                strategy_name = "Stratified (Range)"
                    
            elif strata_type == "even_odd":
                # Calculate how many even vs odd numbers based on balance_factor
                # At balance_factor=1.0, we want distribution based on historical patterns
                # At balance_factor=0.0, we want a fixed distribution (3 even, 2 odd or vice versa)
                
                # Get historical even/odd ratio
                historical_even_ratio = max_even_count / 5
                
                # Get ideal balanced ratio (based on population size)
                population_even_ratio = 25 / 50  # 25 even numbers out of 50
                
                # Blend historical and balanced ratios
                target_even_ratio = historical_even_ratio * balance_factor + population_even_ratio * (1 - balance_factor)
                
                # Decide number of even numbers to include (out of 5)
                even_numbers_to_select = round(5 * target_even_ratio)
                odd_numbers_to_select = 5 - even_numbers_to_select
                
                # Separate even and odd numbers with their frequencies
                even_nums = {num: number_freq[num] for num in range(1, 51) if num % 2 == 0}
                odd_nums = {num: number_freq[num] for num in range(1, 51) if num % 2 == 1}
                
                # Sample from each group
                even_selections = self._weighted_sample(even_nums, even_numbers_to_select)
                odd_selections = self._weighted_sample(odd_nums, odd_numbers_to_select)
                
                # Combine selections
                selected_numbers = even_selections + odd_selections
                
                # Calculate score - how well the selection matches historical even/odd pattern
                even_count = len([n for n in selected_numbers if n % 2 == 0])
                even_odd_similarity = 1 - abs(even_count - max_even_count) / 5
                
                # Calculate range distribution as a secondary metric
                range_distribution = [0] * 5
                for num in selected_numbers:
                    for i, (start, end) in enumerate(ranges):
                        if start <= num <= end:
                            range_distribution[i] += 1
                            break
                
                # Normalize
                range_distribution = [count / 5 for count in range_distribution]
                
                # Calculate similarity to historical distribution
                target_distribution = [range_dist[f"{r[0]}-{r[1]}"] / 100 for r in ranges]
                
                # L1 distance (Manhattan distance)
                distribution_distance = sum(abs(range_distribution[i] - target_distribution[i]) for i in range(5))
                
                # Convert to similarity score (0-1)
                distribution_similarity = 1 - (distribution_distance / 2)  # Max distance is 2
                
                # Combine scores with emphasis on even/odd matching
                normalized_score = round((0.3 * distribution_similarity + 0.7 * even_odd_similarity) * 100, 2)
                
                strategy_name = "Stratified (Even-Odd)"
                
            elif strata_type == "prime_composite":
                # Define prime numbers in range 1-50
                primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
                non_primes = [n for n in range(1, 51) if n not in primes]
                
                # Get historical distribution of primes
                hist_prime_count = 0
                hist_draws = 100  # Sample from recent draws
                for i, row in self.stats.data.head(hist_draws).iterrows():
                    for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                        if row[col] in primes:
                            hist_prime_count += 1
                
                hist_prime_ratio = hist_prime_count / (hist_draws * 5)
                
                # Calculate target ratio blending historical ratio with theoretical ratio
                theoretical_prime_ratio = len(primes) / 50  # Proportion of primes in the number space
                target_prime_ratio = hist_prime_ratio * balance_factor + theoretical_prime_ratio * (1 - balance_factor)
                
                # Decide number of primes to include (out of 5)
                primes_to_select = round(5 * target_prime_ratio)
                primes_to_select = max(1, min(4, primes_to_select))  # Ensure between 1-4 primes
                non_primes_to_select = 5 - primes_to_select
                
                # Prepare frequencies for each group
                prime_freqs = {num: number_freq[num] for num in primes}
                non_prime_freqs = {num: number_freq[num] for num in non_primes}
                
                # Sample from each group
                prime_selections = self._weighted_sample(prime_freqs, primes_to_select)
                non_prime_selections = self._weighted_sample(non_prime_freqs, non_primes_to_select)
                
                # Combine selections
                selected_numbers = prime_selections + non_prime_selections
                
                # Calculate score based on agreement with historical prime distribution
                prime_count = len([n for n in selected_numbers if n in primes])
                prime_similarity = 1 - abs(prime_count / 5 - hist_prime_ratio)
                
                # Calculate even/odd as a secondary metric
                even_count = len([n for n in selected_numbers if n % 2 == 0])
                even_odd_similarity = 1 - abs(even_count - max_even_count) / 5
                
                # Combine scores
                normalized_score = round((0.7 * prime_similarity + 0.3 * even_odd_similarity) * 100, 2)
                
                strategy_name = "Stratified (Prime-Composite)"
                
            elif strata_type == "hot_cold":
                # Determine hot vs cold numbers based on frequency
                # Sort numbers by frequency
                sorted_nums = sorted(
                    [(num, number_freq[num]) for num in range(1, 51)],
                    key=lambda x: x[1],
                    reverse=True
                )
                
                # Define "hot" numbers as top 40% by frequency
                hot_count = int(50 * 0.4)
                hot_nums = dict(sorted_nums[:hot_count])
                cold_nums = dict(sorted_nums[hot_count:])
                
                # Calculate how many hot vs cold numbers based on balance_factor
                # Higher balance factor means more alignment with historical frequencies
                hot_ratio = 0.4 * (1 - balance_factor) + balance_factor * 0.8
                hot_to_select = round(5 * hot_ratio)
                hot_to_select = max(1, min(4, hot_to_select))  # Ensure between 1-4 hot numbers
                cold_to_select = 5 - hot_to_select
                
                # Sample from each group
                hot_selections = self._weighted_sample(hot_nums, hot_to_select)
                cold_selections = self._weighted_sample(cold_nums, cold_to_select)
                
                # Combine selections
                selected_numbers = hot_selections + cold_selections
                
                # Calculate score based on frequency distribution
                freq_score = sum(number_freq[n] for n in selected_numbers) / 5
                
                # Normalize to 0-100 scale
                normalized_score = round(freq_score * 100, 2)
                
                strategy_name = "Stratified (Hot-Cold)"
                
            elif strata_type == "decade":
                # Calculate ideal distribution across decades
                ideal_counts = [1, 1, 1, 1, 1]  # One from each decade
                hist_counts = [range_dist[f"{r[0]}-{r[1]}"] / 100 * 5 for r in ranges]  # Historical distribution
                
                # Blend ideal and historical counts based on balance factor
                target_counts = []
                for i in range(5):
                    target_counts.append(ideal_counts[i] * balance_factor + hist_counts[i] * (1 - balance_factor))
                
                # Calculate integers that sum to 5
                decade_counts = self._distribute_selections(target_counts, 5)
                
                # Select numbers from each decade according to the counts
                selected_numbers = []
                for i, count in enumerate(decade_counts):
                    if count > 0:
                        range_start, range_end = ranges[i]
                        
                        # Get all numbers in this decade
                        decade_numbers = list(range(range_start, range_end + 1))
                        
                        # Get frequencies for weighting
                        decade_freqs = {num: number_freq[num] for num in decade_numbers}
                        
                        # Sample from this decade
                        sampled_nums = self._weighted_sample(decade_freqs, count)
                        selected_numbers.extend(sampled_nums)
                
                # Calculate score - how well the combination matches historical distributions
                # Range distribution (decade distribution)
                range_distribution = [0] * 5
                for num in selected_numbers:
                    for i, (start, end) in enumerate(ranges):
                        if start <= num <= end:
                            range_distribution[i] += 1
                            break
                
                # Normalize
                range_distribution = [count / 5 for count in range_distribution]
                
                # Calculate similarity to historical distribution
                target_distribution = [range_dist[f"{r[0]}-{r[1]}"] / 100 for r in ranges]
                
                # L1 distance (Manhattan distance)
                distribution_distance = sum(abs(range_distribution[i] - target_distribution[i]) for i in range(5))
                
                # Convert to similarity score (0-1)
                distribution_similarity = 1 - (distribution_distance / 2)  # Max distance is 2
                
                # Calculate score with high emphasis on decade distribution
                normalized_score = round(distribution_similarity * 100, 2)
                
                strategy_name = "Stratified (Decade)"
                
            elif strata_type == "pattern":
                # Define pattern categories based on number properties
                
                # 1. Boundary numbers (1-5, 46-50)
                boundary_nums = list(range(1, 6)) + list(range(46, 51))
                
                # 2. Multiples of 5 and 10
                multiples_of_5 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
                
                # 3. Prime numbers
                primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
                
                # 4. Numbers with single digits
                single_digits = list(range(1, 10))
                
                # 5. Numbers in 10-19 range (often underrepresented)
                teens = list(range(10, 20))
                
                # 6. Numbers in 30-39 range (often overrepresented)
                thirties = list(range(30, 40))
                
                # Calculate how many numbers to select from each pattern category
                # based on balance_factor
                if balance_factor > 0.8:
                    # Highly balanced - 1 from each of 5 diverse categories
                    pattern_counts = [1, 1, 1, 1, 1]
                elif balance_factor > 0.6:
                    # Moderately balanced - emphasis on diverse selection
                    pattern_counts = [1, 1, 1, 2, 0]
                elif balance_factor > 0.4:
                    # Medium balance - some pattern representation
                    pattern_counts = [1, 2, 2, 0, 0]
                elif balance_factor > 0.2:
                    # Less balanced - more frequency-based
                    pattern_counts = [2, 3, 0, 0, 0]
                else:
                    # Not balanced - almost pure frequency-based
                    pattern_counts = [5, 0, 0, 0, 0]
                
                # Randomize the pattern assignment to avoid always favoring the same patterns
                random.shuffle(pattern_counts)
                
                # Pattern categories to sample from
                pattern_categories = [
                    {"name": "boundary", "numbers": boundary_nums},
                    {"name": "multiples_of_5", "numbers": multiples_of_5},
                    {"name": "primes", "numbers": primes},
                    {"name": "single_digits", "numbers": single_digits},
                    {"name": "teens", "numbers": teens}
                ]
                
                # Sample from each pattern category
                selected_numbers = []
                used_categories = []
                
                for i, count in enumerate(pattern_counts):
                    if count > 0:
                        category = pattern_categories[i]
                        used_categories.append(category["name"])
                        
                        # Get frequencies for numbers in this category
                        category_freqs = {
                            num: number_freq[num] 
                            for num in category["numbers"]
                            if num not in selected_numbers  # Avoid duplicates
                        }
                        
                        # If we've already selected more numbers than needed, adjust count
                        adjusted_count = min(count, 5 - len(selected_numbers))
                        
                        if adjusted_count > 0 and category_freqs:
                            # Sample from this category
                            sampled = self._weighted_sample(category_freqs, adjusted_count)
                            selected_numbers.extend(sampled)
                
                # If we still need more numbers
                while len(selected_numbers) < 5:
                    # Select from remaining numbers
                    remaining_freqs = {
                        num: number_freq[num] 
                        for num in range(1, 51)
                        if num not in selected_numbers
                    }
                    additional = self._weighted_sample(remaining_freqs, 1)[0]
                    selected_numbers.append(additional)
                
                # Calculate pattern diversity score
                pattern_count = len(used_categories)
                pattern_diversity = pattern_count / 5  # Normalized to 0-1
                
                # Calculate frequency score as a secondary metric
                freq_score = sum(number_freq[n] for n in selected_numbers) / 5
                
                # Combine scores
                normalized_score = round((0.6 * pattern_diversity + 0.4 * freq_score) * 100, 2)
                
                strategy_name = "Stratified (Pattern)"
                
            else:  # Fallback to original range-based stratification
                # Use original implementation for backward compatibility
                range_weights = [
                    range_dist["1-10"] / 100,
                    range_dist["11-20"] / 100,
                    range_dist["21-30"] / 100,
                    range_dist["31-40"] / 100,
                    range_dist["41-50"] / 100
                ]
                
                # Determine how many numbers to pick from each range
                range_counts = [0] * 5
                range_indices = list(range(5))
                
                for _ in range(5):
                    # Select a range based on weights
                    selected_range = random.choices(range_indices, k=1, weights=[range_weights[i] for i in range_indices])[0]
                    range_counts[selected_range] += 1
                    
                    # Decrease weight to avoid oversampling
                    range_weights[selected_range] *= 0.5
                    
                    # Normalize weights
                    total_weight = sum(range_weights[i] for i in range_indices)
                    range_weights = [w / total_weight for w in range_weights]
                
                # Now select numbers from each range according to the counts
                selected_numbers = []
                for i, count in enumerate(range_counts):
                    if count > 0:
                        range_start, range_end = ranges[i]
                        
                        # Try to maintain the ideal even/odd distribution
                        range_numbers = list(range(range_start, range_end + 1))
                        
                        # Separate into even and odd
                        even_numbers = [n for n in range_numbers if n % 2 == 0]
                        odd_numbers = [n for n in range_numbers if n % 2 == 1]
                        
                        # Determine how many even numbers to pick based on the ideal distribution
                        even_to_pick = min(count, max(0, min(max_even_count - len([n for n in selected_numbers if n % 2 == 0]), len(even_numbers))))
                        odd_to_pick = count - even_to_pick
                        
                        # Sample numbers
                        if even_to_pick > 0:
                            selected_numbers.extend(random.sample(even_numbers, even_to_pick))
                        if odd_to_pick > 0:
                            selected_numbers.extend(random.sample(odd_numbers, odd_to_pick))
                
                # Ensure we have exactly 5 numbers
                if len(selected_numbers) > 5:
                    selected_numbers = random.sample(selected_numbers, 5)
                while len(selected_numbers) < 5:
                    num = random.randint(1, 50)
                    if num not in selected_numbers:
                        selected_numbers.append(num)
                
                # Calculate score - how well the combination matches historical distributions
                range_distribution = [0] * 5
                for num in selected_numbers:
                    for i, (start, end) in enumerate(ranges):
                        if start <= num <= end:
                            range_distribution[i] += 1
                            break
                
                # Normalize
                range_distribution = [count / 5 for count in range_distribution]
                
                # Calculate similarity to historical distribution
                target_distribution = [range_dist[f"{r[0]}-{r[1]}"] / 100 for r in ranges]
                
                # L1 distance (Manhattan distance)
                distribution_distance = sum(abs(range_distribution[i] - target_distribution[i]) for i in range(5))
                
                # Convert to similarity score (0-1)
                distribution_similarity = 1 - (distribution_distance / 2)  # Max distance is 2
                
                # Even/odd similarity
                even_count = len([n for n in selected_numbers if n % 2 == 0])
                even_odd_similarity = 1 - abs(even_count - max_even_count) / 5
                
                # Combine scores
                normalized_score = round((0.7 * distribution_similarity + 0.3 * even_odd_similarity) * 100, 2)
                
                strategy_name = "Stratified (Range)"
            
            # For all strategies, use weighted sampling for stars
            stars = self._weighted_sample(star_freq, 2)
            
            combinations.append({
                'numbers': selected_numbers,
                'stars': stars,
                'score': normalized_score,
                'strategy': strategy_name
            })
            
        return combinations
        
    def _distribute_selections(self, probabilities, total_selections):
        """
        Helper method to distribute a fixed number of selections across categories
        based on provided probabilities.
        
        Parameters:
        -----------
        probabilities : list
            List of probabilities for each category
        total_selections : int
            Total number of selections to distribute
        
        Returns:
        --------
        list
            Number of selections for each category
        """
        # Initial allocation - convert probabilities to expected counts
        n = len(probabilities)
        
        # Convert probabilities to expected counts
        expected_counts = [p * total_selections for p in probabilities]
        
        # Round to integer values
        counts = [int(ec) for ec in expected_counts]
        
        # Distribute any remaining selections
        remaining = total_selections - sum(counts)
        
        if remaining > 0:
            # Calculate fractional parts
            fractions = [ec - int(ec) for ec in expected_counts]
            
            # Sort indices by fractional part (descending)
            indices = list(range(n))
            indices.sort(key=lambda i: fractions[i], reverse=True)
            
            # Distribute remaining selections
            for i in range(remaining):
                counts[indices[i]] += 1
                
        return counts
    
    def coverage_strategy(self, num_combinations=5, balanced=True):
        """
        Generate combinations to maximize coverage of different possibilities.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        balanced : bool
            If True, use balanced coverage; otherwise maximize coverage
        
        Returns:
        --------
        list of dict
            List of combinations, each with 'numbers', 'stars', and 'score'
        """
        # For coverage strategy, we want to generate combinations that cover
        # as many different numbers and stars as possible
        
        # Get frequencies to use as weights
        number_freq = self.stats.get_frequency()
        star_freq = self.stats.get_star_frequency()
        
        combinations = []
        covered_numbers = set()
        covered_stars = set()
        
        for i in range(num_combinations):
            if i == 0 or not balanced:
                # For the first combination or when maximizing coverage,
                # select based on pure frequency
                numbers = self._weighted_sample(number_freq, 5)
                stars = self._weighted_sample(star_freq, 2)
            else:
                # For subsequent combinations in balanced mode,
                # prioritize uncovered numbers
                uncovered_weights = {}
                for num in range(1, 51):
                    if num in covered_numbers:
                        uncovered_weights[num] = number_freq[num] * 0.3  # Lower weight for covered numbers
                    else:
                        uncovered_weights[num] = number_freq[num] * 3.0  # Higher weight for uncovered
                
                # Normalize weights
                total = sum(uncovered_weights.values())
                uncovered_weights = {k: v / total for k, v in uncovered_weights.items()}
                
                # Sample numbers
                numbers = self._weighted_sample(uncovered_weights, 5)
                
                # Same for stars
                uncovered_star_weights = {}
                for star in range(1, 13):
                    if star in covered_stars:
                        uncovered_star_weights[star] = star_freq[star] * 0.3
                    else:
                        uncovered_star_weights[star] = star_freq[star] * 3.0
                
                # Normalize
                total = sum(uncovered_star_weights.values())
                uncovered_star_weights = {k: v / total for k, v in uncovered_star_weights.items()}
                
                # Sample stars
                stars = self._weighted_sample(uncovered_star_weights, 2)
            
            # Update covered sets
            covered_numbers.update(numbers)
            covered_stars.update(stars)
            
            # Calculate coverage score
            num_coverage = len(covered_numbers) / 50  # Percentage of numbers covered
            star_coverage = len(covered_stars) / 12  # Percentage of stars covered
            
            # Frequency score
            freq_score = (sum(number_freq[n] for n in numbers) / 5 + sum(star_freq[s] for s in stars) / 2) / 2
            
            # Combined score - weight coverage more in later combinations
            coverage_weight = min(0.2 + (i * 0.15), 0.8)  # Increases with each combination
            freq_weight = 1 - coverage_weight
            
            normalized_score = round((coverage_weight * (num_coverage + star_coverage) / 2 + freq_weight * freq_score) * 100, 2)
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'score': normalized_score
            })
        
        return combinations
    
    def risk_reward_strategy(self, num_combinations=5, risk_level=5):
        """
        Generate combinations optimized for risk/reward ratio.

        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        risk_level : int or float
            Risk level: 1-10 (int) or 0.0-1.0 (float)
            1 or 0.1 is conservative, 10 or 1.0 is risky

        Returns:
        --------
        list of dict
            List of combinations, each with 'numbers', 'stars', and 'score'
        """
        # Get frequency and other statistics
        number_freq = self.stats.get_frequency()
        star_freq = self.stats.get_star_frequency()

        # Get sum distribution
        sum_dist = self.stats.get_sum_distribution()

        # Convert to probability ranges for sampling
        sum_ranges = []
        for range_str, percentage in sum_dist.items():
            start, end = map(int, range_str.split('-'))
            sum_ranges.append((start, end, percentage / 100))

        # Normalize risk_level to 0.0-1.0 scale (backward compatible)
        # Accept both 1-10 scale and 0.0-1.0 scale
        if risk_level > 1.0:
            # Legacy 1-10 scale
            risk_factor = risk_level / 10.0
        else:
            # 0.0-1.0 scale (from old definition)
            risk_factor = risk_level
        
        # At high risk levels, we'll favor:
        # 1. Less common number sums (unusual combinations)
        # 2. Numbers with lower frequencies (statistical outsiders)
        # 3. More varied number spacing (unconventional patterns)
        
        combinations = []
        
        for _ in range(num_combinations):
            # Inverse weighting for high risk - prefer less common numbers
            if risk_factor > 0.5:
                # Invert frequencies for high risk
                inverted_weights = {num: 1 - (freq * risk_factor) for num, freq in number_freq.items()}
                
                # Normalize inverted weights
                total = sum(inverted_weights.values())
                inverted_weights = {k: v / total for k, v in inverted_weights.items()}
                
                numbers = self._weighted_sample(inverted_weights, 5)
            else:
                # For low risk, use normal frequencies but with some randomness
                randomness = risk_factor * 2  # 0.0 to 1.0
                
                adjusted_weights = {num: freq * (1 - randomness) + randomness * random.random() 
                                    for num, freq in number_freq.items()}
                
                # Normalize
                total = sum(adjusted_weights.values())
                adjusted_weights = {k: v / total for k, v in adjusted_weights.items()}
                
                numbers = self._weighted_sample(adjusted_weights, 5)
            
            # For stars, use similar approach
            if risk_factor > 0.5:
                inverted_star_weights = {star: 1 - (freq * risk_factor) for star, freq in star_freq.items()}
                total = sum(inverted_star_weights.values())
                inverted_star_weights = {k: v / total for k, v in inverted_star_weights.items()}
                stars = self._weighted_sample(inverted_star_weights, 2)
            else:
                randomness = risk_factor * 2
                adjusted_star_weights = {star: freq * (1 - randomness) + randomness * random.random() 
                                        for star, freq in star_freq.items()}
                total = sum(adjusted_star_weights.values())
                adjusted_star_weights = {k: v / total for k, v in adjusted_star_weights.items()}
                stars = self._weighted_sample(adjusted_star_weights, 2)
            
            # Calculate sum
            number_sum = sum(numbers)
            
            # For high risk, adjust if sum is in common range
            if risk_factor > 0.5:
                # Check if sum is in a common range
                in_common_range = False
                for start, end, prob in sorted(sum_ranges, key=lambda x: x[2], reverse=True)[:3]:  # Top 3 common ranges
                    if start <= number_sum <= end:
                        in_common_range = True
                        break
                
                # If in common range and risk is high, try to adjust one number
                if in_common_range and random.random() < risk_factor:
                    # Pick a random number to replace
                    to_replace = random.choice(numbers)
                    
                    # Try to find a replacement that puts sum outside common ranges
                    attempts = 0
                    while attempts < 20:  # Limit attempts
                        # Find a replacement between 1-50 not already in the list
                        replacement = random.randint(1, 50)
                        if replacement not in numbers:
                            new_sum = number_sum - to_replace + replacement
                            
                            # Check if new sum is in a less common range
                            in_common_range = False
                            for start, end, prob in sorted(sum_ranges, key=lambda x: x[2], reverse=True)[:3]:
                                if start <= new_sum <= end:
                                    in_common_range = True
                                    break
                            
                            if not in_common_range:
                                # Found a good replacement
                                numbers.remove(to_replace)
                                numbers.append(replacement)
                                number_sum = new_sum
                                break
                        
                        attempts += 1
            
            # Calculate risk/reward score
            if risk_factor <= 0.5:
                # For low risk, higher frequency = higher score
                avg_freq = (sum(number_freq[n] for n in numbers) / 5 + sum(star_freq[s] for s in stars) / 2) / 2
                normalized_score = round(avg_freq * 100, 2)
            else:
                # For high risk, uniqueness = higher score
                # Calculate sum commonality
                sum_commonality = 0
                for start, end, prob in sum_ranges:
                    if start <= number_sum <= end:
                        sum_commonality = prob
                        break
                
                # Calculate number uniqueness (inverse of frequency)
                avg_uniqueness = 1 - (sum(number_freq[n] for n in numbers) / 5)
                
                # Calculate spacing uniformity (we want non-uniform spacing for high risk)
                sorted_numbers = sorted(numbers)
                gaps = [sorted_numbers[i+1] - sorted_numbers[i] for i in range(len(sorted_numbers)-1)]
                gap_variability = np.std(gaps) / 10  # Normalize to ~0-1 range
                
                # Combined score
                uniqueness_score = (0.4 * avg_uniqueness + 0.4 * (1 - sum_commonality) + 0.2 * gap_variability)
                normalized_score = round(uniqueness_score * 100, 2)
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'score': normalized_score
            })
        
        return combinations
    
    def bayesian_strategy(self, num_combinations=5, recent_draws_count=20, 
                       prior_type="empirical", update_method="standard", smoothing_factor=0.1):
        """
        Generate combinations using an enhanced Bayesian probability model with multiple inference methods.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        recent_draws_count : int
            Number of recent draws to use for updating priors
        prior_type : str
            Type of prior distribution to use:
            - "empirical": Based on historical frequencies (default)
            - "uniform": Equal probabilities for all numbers
            - "informative": Uses external information about number patterns
        update_method : str
            Method for Bayesian updating:
            - "standard": Traditional Bayesian update (default)
            - "sequential": Sequential updating using each draw
            - "adaptive": Adaptive updating with time decay
        smoothing_factor : float
            Laplace smoothing factor for handling zero probabilities
            
        Returns:
        --------
        list of dict
            List of combinations, each with 'numbers', 'stars', and 'score'
        """
        # Create an enhanced Bayesian model with the historical data and specified parameters
        bayesian_model = BayesianModel(
            self.stats.data, 
            recent_draws_count=recent_draws_count,
            prior_type=prior_type,
            update_method=update_method,
            smoothing_factor=smoothing_factor
        )
        
        # Generate combinations
        bayesian_combinations = bayesian_model.generate_combinations(num_combinations)
        
        # Set strategy name based on the specific Bayesian approach used
        strategy_name = f"Bayesian ({prior_type} prior, {update_method} update)"
        
        # Convert to the expected format
        combinations = []
        for combo in bayesian_combinations:
            combinations.append({
                'numbers': combo.numbers,
                'stars': combo.stars,
                'score': combo.score,
                'strategy': strategy_name
            })
            
        # Store the model for potential visualization of probability updates
        self.current_bayesian_model = bayesian_model
            
        return combinations
        
    def get_bayesian_probability_history(self):
        """
        Get the probability history from the most recently used Bayesian model.
        
        Returns:
        --------
        dict or None
            Dictionary of probability histories for numbers and stars,
            or None if no Bayesian model has been used
        """
        if hasattr(self, 'current_bayesian_model'):
            return self.current_bayesian_model.probability_history
        return None
        
    def markov_strategy(self, num_combinations=5, lag=1):
        """
        Generate combinations using a Markov chain model.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        lag : int
            Number of draws to look back in the Markov chain
            
        Returns:
        --------
        list of dict
            List of combinations, each with 'numbers', 'stars', and 'score'
        """
        # Create a Markov model with the historical data
        markov_model = MarkovModel(self.stats.data, lag)
        
        # Get the last draw's numbers to use as seed
        last_draw = self.stats.data.iloc[0]
        seed_numbers = [last_draw[f'n{i}'] for i in range(1, 6)]
        seed_stars = [last_draw[f's{i}'] for i in range(1, 3)]
        
        # Generate combinations
        markov_combinations = markov_model.generate_combinations(
            num_combinations, 
            seed_numbers=seed_numbers, 
            seed_stars=seed_stars
        )
        
        # Convert to the expected format
        combinations = []
        for combo in markov_combinations:
            combinations.append({
                'numbers': combo.numbers,
                'stars': combo.stars,
                'score': combo.score,
                'strategy': 'Markov'
            })
            
        return combinations
    
    def time_series_strategy(self, num_combinations=5, window_size=10):
        """
        Generate combinations using time series analysis to detect cycles and patterns.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        window_size : int
            Size of the sliding window for pattern detection
            
        Returns:
        --------
        list of dict
            List of combinations, each with 'numbers', 'stars', and 'score'
        """
        # Create a time series model
        ts_model = TimeSeriesModel(self.stats.data, window_size)
        
        # Generate combinations
        ts_combinations = ts_model.generate_combinations(num_combinations)
        
        # Convert to the expected format
        combinations = []
        for combo in ts_combinations:
            combinations.append({
                'numbers': combo.numbers,
                'stars': combo.stars,
                'score': combo.score,
                'strategy': 'Time Series'
            })
            
        return combinations
    
    def cognitive_bias_strategy(self, num_combinations=5):
        """
        Generate combinations that avoid common cognitive biases of human players.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
            
        Returns:
        --------
        list of dict
            List of combinations, each with 'numbers', 'stars', and 'score'
        """
        # Most humans tend to select "special" numbers:
        # - Avoid consecutive numbers
        # - Avoid numbers that form patterns
        # - Avoid numbers that are birthdays (1-31)
        # - Avoid numbers that are commonly played
        
        # Get basic frequencies
        number_freq = self.stats.get_frequency()
        star_freq = self.stats.get_star_frequency()
        
        # Create anti-bias weightings
        # Favor high numbers (>31) as they're less likely to be birthdays
        number_weights = {}
        for num in range(1, 51):
            # Base weight from frequency
            weight = number_freq[num]
            
            # Bonus for higher numbers (less likely to be birthdays)
            if num > 31:
                weight *= 1.3
                
            # Bonus for "unpopular" numbers (4, 13, etc. might be avoided by superstitious players)
            if num in [4, 13, 17, 39, 40, 44]:
                weight *= 1.2
                
            number_weights[num] = weight
        
        # Similar for stars
        star_weights = {}
        for star in range(1, 13):
            weight = star_freq[star]
            
            # Bonus for "unpopular" stars
            if star in [4, 7, 8, 13 % 12]:
                weight *= 1.2
                
            star_weights[star] = weight
        
        combinations = []
        for _ in range(num_combinations):
            # Choose numbers with weighted sampling
            numbers = self._weighted_sample(number_weights, 5)
            stars = self._weighted_sample(star_weights, 2)
            
            # Calculate sum (combinations with unusual sums may be less played)
            num_sum = sum(numbers)
            
            # Calculate several anti-cognitive bias factors:
            
            # 1. Human tendency is to pick combinations with "nice" sums (100, 150, etc.)
            # So we'll score higher when the sum isn't a multiple of 10 or 50
            sum_score = 0.5
            if num_sum % 10 != 0:
                sum_score += 0.15
            if num_sum % 5 != 0:
                sum_score += 0.1
                
            # 2. Check for patterns people tend to pick:
            sorted_nums = sorted(numbers)
            
            # Look for consecutive sequences (people like these)
            has_consecutive = False
            for i in range(len(sorted_nums) - 1):
                if sorted_nums[i+1] - sorted_nums[i] == 1:
                    has_consecutive = True
                    break
                    
            pattern_score = 0.2
            if not has_consecutive:
                pattern_score += 0.15  # Bonus for no consecutive numbers
                
            # 3. Check distribution across the board (people like clustering)
            num_in_first_half = sum(1 for n in numbers if n <= 25)
            distribution_score = 0.0
            # Score higher when mix of high and low numbers (2/3 or 3/2 split)
            if num_in_first_half in [2, 3]:
                distribution_score += 0.2
                
            # Calculate final score (higher when the combo is likely avoided by humans)
            # Maximum theoretical score: 0.5 + 0.15 + 0.1 + 0.2 + 0.15 + 0.2 = 1.3
            # Normalize to 100-point scale
            final_score = round((sum_score + pattern_score + distribution_score) / 1.3 * 100, 2)
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'score': final_score,
                'strategy': 'Anti-Bias'
            })
            
        return combinations
        
    def _weighted_sample(self, weights, k):
        """
        Helper method to sample k elements based on weights.
        
        Parameters:
        -----------
        weights : dict or pandas.Series
            Dictionary or Series with elements as keys and weights as values
        k : int
            Number of elements to sample
        
        Returns:
        --------
        list
            List of k sampled elements (guaranteed to be unique)
        """
        population = list(weights.keys())
        weights_list = [weights[i] for i in population]
        
        # Ensure unique samples
        result = []
        remaining_population = population.copy()
        remaining_weights = weights_list.copy()
        
        while len(result) < k and remaining_population:
            if len(remaining_population) == 1:
                # Only one choice left
                result.append(remaining_population[0])
            else:
                # Sample based on weights
                chosen = random.choices(remaining_population, weights=remaining_weights, k=1)[0]
                result.append(chosen)
                
                # Remove the chosen element for next selection
                idx = remaining_population.index(chosen)
                remaining_population.pop(idx)
                remaining_weights.pop(idx)
        
        return result
