import pandas as pd
import numpy as np
from datetime import datetime
import random

class EuromillionsDrawing:
    """
    Class representing a single Euromillions drawing.
    """
    
    def __init__(self, date, numbers, stars):
        """
        Initialize a drawing with date, numbers, and stars.
        
        Parameters:
        -----------
        date : datetime.date or str
            The date of the draw
        numbers : list
            List of 5 main numbers (1-50)
        stars : list
            List of 2 star numbers (1-12)
        """
        # Convert date string to datetime if needed
        if isinstance(date, str):
            self.date = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            self.date = date
        
        # Ensure we have 5 unique numbers
        if len(numbers) != 5 or len(set(numbers)) != 5:
            raise ValueError("Must provide 5 unique main numbers")
        
        # Ensure numbers are in valid range
        if not all(1 <= n <= 50 for n in numbers):
            raise ValueError("Main numbers must be between 1 and 50")
        
        # Ensure we have 2 unique stars
        if len(stars) != 2 or len(set(stars)) != 2:
            raise ValueError("Must provide 2 unique star numbers")
        
        # Ensure stars are in valid range
        if not all(1 <= s <= 12 for s in stars):
            raise ValueError("Star numbers must be between 1 and 12")
        
        self.numbers = sorted(numbers)
        self.stars = sorted(stars)
        self.day_of_week = self.date.strftime('%A')
    
    def to_dict(self):
        """
        Convert the drawing to a dictionary suitable for DataFrame conversion.
        
        Returns:
        --------
        dict
            Dictionary representation of the drawing
        """
        result = {
            'date': self.date,
            'day_of_week': self.day_of_week
        }
        
        for i, num in enumerate(self.numbers):
            result[f'n{i+1}'] = num
        
        for i, star in enumerate(self.stars):
            result[f's{i+1}'] = star
        
        return result

class EuromillionsCombination:
    """
    Class representing a generated Euromillions combination.
    """
    
    def __init__(self, numbers, stars, score=None, strategy=None):
        """
        Initialize a combination with numbers, stars, and optional score.
        
        Parameters:
        -----------
        numbers : list
            List of 5 main numbers (1-50)
        stars : list
            List of 2 star numbers (1-12)
        score : float, optional
            A score or confidence value for this combination
        strategy : str, optional
            The strategy used to generate this combination
        """
        # Validate inputs
        if len(numbers) != 5 or len(set(numbers)) != 5:
            raise ValueError("Must provide 5 unique main numbers")
        
        if not all(1 <= n <= 50 for n in numbers):
            raise ValueError("Main numbers must be between 1 and 50")
        
        if len(stars) != 2 or len(set(stars)) != 2:
            raise ValueError("Must provide 2 unique star numbers")
        
        if not all(1 <= s <= 12 for s in stars):
            raise ValueError("Star numbers must be between 1 and 12")
        
        self.numbers = sorted(numbers)
        self.stars = sorted(stars)
        self.score = score
        self.strategy = strategy
    
    def to_dict(self):
        """
        Convert the combination to a dictionary.
        
        Returns:
        --------
        dict
            Dictionary representation of the combination
        """
        result = {
            'numbers': self.numbers,
            'stars': self.stars
        }
        
        if self.score is not None:
            result['score'] = self.score
        
        if self.strategy is not None:
            result['strategy'] = self.strategy
        
        return result
    
    def to_string(self):
        """
        Convert the combination to a formatted string.
        
        Returns:
        --------
        str
            String representation of the combination
        """
        numbers_str = ' - '.join(str(n) for n in self.numbers)
        stars_str = ' - '.join(str(s) for s in self.stars)
        
        if self.score is not None:
            return f"Numbers: {numbers_str} | Stars: {stars_str} | Score: {self.score:.2f}"
        else:
            return f"Numbers: {numbers_str} | Stars: {stars_str}"
    
    @classmethod
    def generate_random(cls):
        """
        Generate a random valid Euromillions combination.
        
        Returns:
        --------
        EuromillionsCombination
            A randomly generated combination
        """
        numbers = sorted(random.sample(range(1, 51), 5))
        stars = sorted(random.sample(range(1, 13), 2))
        
        return cls(numbers, stars)

class BayesianModel:
    """
    Class implementing a Bayesian model for Euromillions prediction with enhanced inference methods.
    """
    
    def __init__(self, historical_data, recent_draws_count=20, prior_type="empirical", 
                 update_method="standard", smoothing_factor=0.1):
        """
        Initialize the enhanced Bayesian model with historical data.
        
        Parameters:
        -----------
        historical_data : pandas.DataFrame
            Historical Euromillions data
        recent_draws_count : int
            Number of recent draws to use for updating
        prior_type : str
            Type of prior distribution to use:
            - "empirical": Based on historical frequencies
            - "uniform": Equal probabilities for all numbers
            - "informative": Uses external information about number patterns
        update_method : str
            Method for Bayesian updating:
            - "standard": Traditional Bayesian update
            - "sequential": Sequential updating using each draw
            - "adaptive": Adaptive updating with time decay
        smoothing_factor : float
            Laplace smoothing factor for handling zero probabilities
        """
        self.historical_data = historical_data
        self.recent_draws_count = min(recent_draws_count, len(historical_data))
        self.prior_type = prior_type
        self.update_method = update_method
        self.smoothing_factor = smoothing_factor
        
        # Split data into historical and recent
        self.recent_data = historical_data.iloc[:self.recent_draws_count]
        self.prior_data = historical_data.iloc[self.recent_draws_count:]
        
        # For tracking changes in probabilities
        self.probability_history = {
            'numbers': {},
            'stars': {}
        }
        
        # Calculate prior probabilities based on specified method
        self.calculate_priors()
        
        # Update with recent evidence
        self.update_probabilities()
    
    def calculate_priors(self):
        """
        Calculate prior probabilities based on the selected method.
        """
        # Initialize prior dictionaries
        self.number_priors = {}
        self.star_priors = {}
        
        if self.prior_type == "uniform":
            # Uniform priors - equal probability for all numbers and stars
            for num in range(1, 51):
                self.number_priors[num] = 1/50
            
            for star in range(1, 13):
                self.star_priors[star] = 1/12
                
        elif self.prior_type == "informative":
            # Informative priors based on number patterns and common knowledge
            # Calculate base uniform distribution
            for num in range(1, 51):
                self.number_priors[num] = 1/50
            
            for star in range(1, 13):
                self.star_priors[star] = 1/12
            
            # Apply adjustments based on "informative" patterns
            # - Numbers divisible by 5 or 10 are slightly less likely (as they're more commonly played)
            # - Popular numbers (1, 7, etc.) are less likely (for same reason)
            for num in range(1, 51):
                if num % 5 == 0:
                    self.number_priors[num] *= 1.05  # Slightly increase probability
                if num in [1, 7, 13, 17, 23, 42]:
                    self.number_priors[num] *= 0.95  # Slightly decrease probability
            
            # Normalize to ensure probabilities sum to 1
            total_prob = sum(self.number_priors.values())
            for num in range(1, 51):
                self.number_priors[num] /= total_prob
                
            # Similar for stars
            for star in range(1, 13):
                if star in [1, 7]:
                    self.star_priors[star] *= 0.95
                    
            # Normalize star probabilities
            total_prob = sum(self.star_priors.values())
            for star in range(1, 13):
                self.star_priors[star] /= total_prob
                
        else:  # "empirical" - default
            # Calculate prior probabilities for main numbers from historical data
            num_columns = [f'n{i}' for i in range(1, 6)]
            
            # Apply Laplace smoothing
            total_numbers = len(self.prior_data) * 5 + 50 * self.smoothing_factor
            for num in range(1, 51):
                count = sum((self.prior_data[col] == num).sum() for col in num_columns)
                # Add smoothing factor to avoid zero probabilities
                self.number_priors[num] = (count + self.smoothing_factor) / total_numbers
            
            # Calculate prior probabilities for star numbers with smoothing
            star_columns = [f's{i}' for i in range(1, 3)]
            
            total_stars = len(self.prior_data) * 2 + 12 * self.smoothing_factor
            for star in range(1, 13):
                count = sum((self.prior_data[col] == star).sum() for col in star_columns)
                self.star_priors[star] = (count + self.smoothing_factor) / total_stars
                
        # Store initial priors for comparison
        for num in range(1, 51):
            self.probability_history['numbers'][num] = [self.number_priors[num]]
            
        for star in range(1, 13):
            self.probability_history['stars'][star] = [self.star_priors[star]]
    
    def update_probabilities(self):
        """
        Update probabilities using different Bayesian updating methods.
        """
        # Common data for all methods
        num_columns = [f'n{i}' for i in range(1, 6)]
        star_columns = [f's{i}' for i in range(1, 3)]
        
        if self.update_method == "sequential":
            # Sequential updating processes each draw sequentially
            # Start with priors
            number_posteriors = self.number_priors.copy()
            star_posteriors = self.star_priors.copy()
            
            # Process each recent draw in sequence
            for idx in range(len(self.recent_data)):
                draw = self.recent_data.iloc[idx]
                
                # Update for each number in this draw
                draw_numbers = [draw[col] for col in num_columns]
                draw_stars = [draw[col] for col in star_columns]
                
                # Number updates
                number_likelihoods = {}
                for num in range(1, 51):
                    # Likelihood is higher if the number appeared in this draw
                    if num in draw_numbers:
                        number_likelihoods[num] = 5/50  # Probability of being selected (5 out of 50)
                    else:
                        number_likelihoods[num] = 45/50  # Probability of not being selected
                
                # Calculate posteriors using current posteriors as priors
                number_posteriors = self._normalize_posteriors(number_posteriors, number_likelihoods)
                
                # Track probability history for key numbers
                for num in range(1, 51):
                    self.probability_history['numbers'][num].append(number_posteriors[num])
                
                # Star updates
                star_likelihoods = {}
                for star in range(1, 13):
                    # Likelihood is higher if the star appeared in this draw
                    if star in draw_stars:
                        star_likelihoods[star] = 2/12  # Probability of being selected (2 out of 12)
                    else:
                        star_likelihoods[star] = 10/12  # Probability of not being selected
                
                # Calculate posteriors
                star_posteriors = self._normalize_posteriors(star_posteriors, star_likelihoods)
                
                # Track probability history
                for star in range(1, 13):
                    self.probability_history['stars'][star].append(star_posteriors[star])
            
            # Set final posteriors
            self.number_posteriors = number_posteriors
            self.star_posteriors = star_posteriors
            
        elif self.update_method == "adaptive":
            # Adaptive updating gives more weight to recent draws
            # Count occurrences in recent data with time decay
            number_counts = {}
            for num in range(1, 51):
                count = 0
                for idx, draw in self.recent_data.iterrows():
                    # More recent draws get higher weight (linear decay)
                    recency_weight = 1 - (idx / len(self.recent_data))
                    for col in num_columns:
                        if draw[col] == num:
                            count += recency_weight
                number_counts[num] = count
            
            # Star counts with time decay
            star_counts = {}
            for star in range(1, 13):
                count = 0
                for idx, draw in self.recent_data.iterrows():
                    recency_weight = 1 - (idx / len(self.recent_data))
                    for col in star_columns:
                        if draw[col] == star:
                            count += recency_weight
                star_counts[star] = count
            
            # Calculate posteriors with adaptive weighting
            # For numbers
            number_likelihoods = {}
            total_weighted_count = sum(number_counts.values())
            
            if total_weighted_count > 0:
                for num in range(1, 51):
                    number_likelihoods[num] = number_counts[num] / total_weighted_count
            else:
                # Fallback if no data
                for num in range(1, 51):
                    number_likelihoods[num] = 1/50
            
            self.number_posteriors = self._normalize_posteriors(self.number_priors, number_likelihoods)
            
            # For stars
            star_likelihoods = {}
            total_weighted_count = sum(star_counts.values())
            
            if total_weighted_count > 0:
                for star in range(1, 13):
                    star_likelihoods[star] = star_counts[star] / total_weighted_count
            else:
                # Fallback if no data
                for star in range(1, 13):
                    star_likelihoods[star] = 1/12
            
            self.star_posteriors = self._normalize_posteriors(self.star_priors, star_likelihoods)
            
        else:  # "standard" - default
            # Standard Bayesian update using batch data
            # Count recent occurrences of each number
            number_counts = {}
            for num in range(1, 51):
                count = sum((self.recent_data[col] == num).sum() for col in num_columns)
                number_counts[num] = count
            
            # Count recent occurrences of each star
            star_counts = {}
            for star in range(1, 13):
                count = sum((self.recent_data[col] == star).sum() for col in star_columns)
                star_counts[star] = count
            
            # Calculate likelihoods and posterior probabilities for numbers
            total_recent_numbers = len(self.recent_data) * 5
            number_likelihoods = {}
            
            for num in range(1, 51):
                # Simple binomial likelihood
                k = number_counts[num]  # Number of occurrences
                n = total_recent_numbers  # Total trials
                p = self.number_priors[num]  # Prior probability
                
                # Approximation of binomial PMF for likelihood
                number_likelihoods[num] = self._binomial_pmf(k, n, p)
            
            # Normalize to get posterior probabilities
            self.number_posteriors = self._normalize_posteriors(self.number_priors, number_likelihoods)
            
            # Same for star numbers
            total_recent_stars = len(self.recent_data) * 2
            star_likelihoods = {}
            
            for star in range(1, 13):
                k = star_counts[star]
                n = total_recent_stars
                p = self.star_priors[star]
                
                star_likelihoods[star] = self._binomial_pmf(k, n, p)
            
            self.star_posteriors = self._normalize_posteriors(self.star_priors, star_likelihoods)
        
        # Track final probabilities
        for num in range(1, 51):
            self.probability_history['numbers'][num].append(self.number_posteriors[num])
            
        for star in range(1, 13):
            self.probability_history['stars'][star].append(self.star_posteriors[star])
    
    def _binomial_pmf(self, k, n, p):
        """
        Calculate binomial PMF: probability of k successes in n trials with probability p.
        
        This is a simple approximation to avoid dependency on scipy.
        """
        if p == 0:
            return 0 if k == 0 else 0
        if p == 1:
            return 0 if k != n else 1
        
        # For numerical stability, we'll use a simple approximation for small values
        return np.exp(self._log_binomial_pmf(k, n, p))
    
    def _log_binomial_pmf(self, k, n, p):
        """
        Calculate log of binomial PMF to avoid numerical issues.
        """
        # Log of binomial coefficient
        log_coef = self._log_factorial(n) - self._log_factorial(k) - self._log_factorial(n - k)
        
        # Log of probability terms
        log_prob = k * np.log(p) + (n - k) * np.log(1 - p)
        
        return log_coef + log_prob
    
    def _log_factorial(self, n):
        """
        Calculate log of factorial using Stirling's approximation for large n.
        """
        if n <= 1:
            return 0
        
        # For small n, just calculate directly
        if n <= 20:
            return np.log(np.prod(np.arange(1, n + 1)))
        
        # For larger n, use Stirling's approximation
        return n * np.log(n) - n + 0.5 * np.log(2 * np.pi * n)
    
    def _normalize_posteriors(self, priors, likelihoods):
        """
        Normalize posterior probabilities.
        """
        posteriors = {}
        
        # Calculate denominator (evidence)
        evidence = sum(priors[i] * likelihoods[i] for i in priors)
        
        # Calculate posterior for each outcome
        for i in priors:
            if evidence > 0:
                posteriors[i] = (priors[i] * likelihoods[i]) / evidence
            else:
                # If evidence is zero (numerical issues), fall back to prior
                posteriors[i] = priors[i]
        
        return posteriors
    
    def get_number_probabilities(self):
        """
        Get the posterior probabilities for main numbers.
        
        Returns:
        --------
        dict
            Dictionary mapping numbers (1-50) to probabilities
        """
        return self.number_posteriors
    
    def get_star_probabilities(self):
        """
        Get the posterior probabilities for star numbers.
        
        Returns:
        --------
        dict
            Dictionary mapping stars (1-12) to probabilities
        """
        return self.star_posteriors
    
    def generate_combinations(self, num_combinations=5):
        """
        Generate combinations using the Bayesian model.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        
        Returns:
        --------
        list
            List of EuromillionsCombination objects
        """
        combinations = []
        
        for _ in range(num_combinations):
            # Convert posteriors to list for weighted sampling
            number_items = list(self.number_posteriors.items())
            numbers = []
            
            # Sample 5 unique numbers
            for _ in range(5):
                if not number_items:
                    break
                
                # Extract numbers and weights
                nums, weights = zip(*number_items)
                
                # Weighted random choice
                selected_idx = np.random.choice(len(nums), p=weights/np.sum(weights))
                selected_num = nums[selected_idx]
                
                numbers.append(selected_num)
                
                # Remove selected number from items
                number_items.pop(selected_idx)
            
            # Sample 2 unique stars
            star_items = list(self.star_posteriors.items())
            star_nums, star_weights = zip(*star_items)
            
            # Need to sample without replacement
            star_idxs = np.random.choice(
                len(star_nums), 
                size=2, 
                replace=False,
                p=star_weights/np.sum(star_weights)
            )
            
            stars = [star_nums[i] for i in star_idxs]
            
            # Calculate score as average probability
            score = (
                sum(self.number_posteriors[n] for n in numbers) / 5 + 
                sum(self.star_posteriors[s] for s in stars) / 2
            ) / 2 * 100
            
            combinations.append(EuromillionsCombination(
                numbers, 
                stars,
                score=score,
                strategy="Bayesian"
            ))
        
        return combinations

class MarkovModel:
    """
    Class implementing a Markov model for Euromillions prediction.
    """
    
    def __init__(self, historical_data, lag=1):
        """
        Initialize the Markov model with historical data.
        
        Parameters:
        -----------
        historical_data : pandas.DataFrame
            Historical Euromillions data
        lag : int
            Number of draws to look back
        """
        self.historical_data = historical_data
        self.lag = lag
        
        # Calculate transition matrices
        self.calculate_transition_matrices()
    
    def calculate_transition_matrices(self):
        """
        Calculate transition matrices for numbers and stars.
        """
        # Initialize transition counts matrix for numbers
        self.number_transitions = np.zeros((51, 51))
        
        # Number columns
        num_columns = [f'n{i}' for i in range(1, 6)]
        
        # Calculate transitions for numbers
        for draw_idx in range(self.lag, len(self.historical_data)):
            current_draw = set(self.historical_data.iloc[draw_idx][num_columns])
            previous_draw = set(self.historical_data.iloc[draw_idx-self.lag][num_columns])
            
            # Count transitions from previous to current
            for prev_num in previous_draw:
                for curr_num in current_draw:
                    self.number_transitions[prev_num, curr_num] += 1
        
        # Calculate probabilities
        self.number_transition_probs = np.zeros((51, 51))
        for i in range(1, 51):
            row_sum = self.number_transitions[i].sum()
            if row_sum > 0:
                self.number_transition_probs[i] = self.number_transitions[i] / row_sum
        
        # Create DataFrame for easier handling
        self.number_transition_matrix = pd.DataFrame(
            self.number_transition_probs[1:51, 1:51],
            index=range(1, 51),
            columns=range(1, 51)
        )
        
        # Initialize transition counts matrix for stars
        self.star_transitions = np.zeros((13, 13))
        
        # Star columns
        star_columns = [f's{i}' for i in range(1, 3)]
        
        # Calculate transitions for stars
        for draw_idx in range(self.lag, len(self.historical_data)):
            current_stars = set(self.historical_data.iloc[draw_idx][star_columns])
            previous_stars = set(self.historical_data.iloc[draw_idx-self.lag][star_columns])
            
            # Count transitions from previous to current
            for prev_star in previous_stars:
                for curr_star in current_stars:
                    self.star_transitions[prev_star, curr_star] += 1
        
        # Calculate probabilities
        self.star_transition_probs = np.zeros((13, 13))
        for i in range(1, 13):
            row_sum = self.star_transitions[i].sum()
            if row_sum > 0:
                self.star_transition_probs[i] = self.star_transitions[i] / row_sum
        
        # Create DataFrame for easier handling
        self.star_transition_matrix = pd.DataFrame(
            self.star_transition_probs[1:13, 1:13],
            index=range(1, 13),
            columns=range(1, 13)
        )
    
    def get_number_transition_matrix(self):
        """
        Get the transition matrix for main numbers.
        
        Returns:
        --------
        pandas.DataFrame
            Transition matrix for numbers
        """
        return self.number_transition_matrix
    
    def get_star_transition_matrix(self):
        """
        Get the transition matrix for star numbers.
        
        Returns:
        --------
        pandas.DataFrame
            Transition matrix for stars
        """
        return self.star_transition_matrix
    
    def generate_combinations(self, num_combinations=5, seed_numbers=None, seed_stars=None):
        """
        Generate combinations using the Markov model.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        seed_numbers : list, optional
            Initial numbers to start the Markov chain
        seed_stars : list, optional
            Initial stars to start the Markov chain
        
        Returns:
        --------
        list
            List of EuromillionsCombination objects
        """
        # If no seed provided, use the most recent draw
        if seed_numbers is None or seed_stars is None:
            most_recent = self.historical_data.iloc[0]
            seed_numbers = [most_recent[f'n{i}'] for i in range(1, 6)]
            seed_stars = [most_recent[f's{i}'] for i in range(1, 3)]
        
        combinations = []
        
        for _ in range(num_combinations):
            # Generate numbers using Markov transitions
            selected_numbers = []
            
            # Start with one random seed number
            current_num = random.choice(seed_numbers)
            selected_numbers.append(current_num)
            
            # Generate the rest based on transitions
            while len(selected_numbers) < 5:
                # Get transition probabilities from current number
                probs = self.number_transition_probs[current_num]
                
                # Set zero probability for already selected numbers
                for num in selected_numbers:
                    probs[num] = 0
                
                # If all probabilities are zero, choose randomly
                if np.sum(probs) == 0:
                    candidates = [n for n in range(1, 51) if n not in selected_numbers]
                    next_num = random.choice(candidates)
                else:
                    # Normalize probabilities
                    probs = probs / np.sum(probs)
                    
                    # Choose next number based on transition probabilities
                    next_num = np.random.choice(range(1, 51), p=probs[1:51])
                
                selected_numbers.append(next_num)
                current_num = next_num
            
            # Generate stars using Markov transitions
            selected_stars = []
            
            # Start with one random seed star
            current_star = random.choice(seed_stars)
            selected_stars.append(current_star)
            
            # Generate the second star based on transitions
            # Get transition probabilities from current star
            probs = self.star_transition_probs[current_star]
            
            # Set zero probability for already selected star
            probs[current_star] = 0
            
            # If all probabilities are zero, choose randomly
            if np.sum(probs) == 0:
                candidates = [s for s in range(1, 13) if s not in selected_stars]
                next_star = random.choice(candidates)
            else:
                # Normalize probabilities
                probs = probs / np.sum(probs)
                
                # Choose next star based on transition probabilities
                next_star = np.random.choice(range(1, 13), p=probs[1:13])
            
            selected_stars.append(next_star)
            
            # Calculate score based on transition probabilities
            # Use average transition probability between consecutive numbers
            sorted_numbers = sorted(selected_numbers)
            transition_scores = []
            
            for i in range(len(sorted_numbers) - 1):
                from_num = sorted_numbers[i]
                to_num = sorted_numbers[i + 1]
                score = self.number_transition_matrix.loc[from_num, to_num]
                transition_scores.append(score)
            
            # Add star transition
            from_star = selected_stars[0]
            to_star = selected_stars[1]
            star_score = self.star_transition_matrix.loc[from_star, to_star]
            
            avg_score = (sum(transition_scores) / len(transition_scores) if transition_scores else 0)
            combined_score = (avg_score * 0.7 + star_score * 0.3) * 100
            
            combinations.append(EuromillionsCombination(
                selected_numbers, 
                selected_stars,
                score=combined_score,
                strategy="Markov"
            ))
        
        return combinations

class TimeSeriesModel:
    """
    Class implementing a time series model for Euromillions prediction.
    """
    
    def __init__(self, historical_data, window_size=10):
        """
        Initialize the time series model with historical data.
        
        Parameters:
        -----------
        historical_data : pandas.DataFrame
            Historical Euromillions data
        window_size : int
            Size of the rolling window for analysis
        """
        self.historical_data = historical_data
        self.window_size = min(window_size, len(historical_data))
        
        # Calculate time series metrics
        self.calculate_time_series_metrics()
    
    def calculate_time_series_metrics(self):
        """
        Calculate time series metrics for all numbers and stars.
        """
        self.number_metrics = {}
        num_columns = [f'n{i}' for i in range(1, 6)]
        
        # Calculate metrics for each number
        for number in range(1, 51):
            # Create time series for this number
            occurrences = []
            for idx, row in self.historical_data.iterrows():
                if any(row[col] == number for col in num_columns):
                    occurrences.append(idx)
            
            # Calculate gaps between occurrences
            gaps = [occurrences[i] - occurrences[i+1] - 1 for i in range(len(occurrences)-1)]
            avg_gap = np.mean(gaps) if gaps else 0
            
            # Calculate draws since last appearance
            draws_since_last = occurrences[0] if occurrences else len(self.historical_data)
            
            # Try to identify cyclic patterns
            cyclic_pattern = None
            if len(gaps) >= 5:
                # Look for repeating patterns in the gap sequence
                if len(set(gaps[:3])) == 1 and gaps[0] == gaps[3]:
                    cyclic_pattern = gaps[0] + 1  # +1 because we measure gaps
                elif len(gaps) >= 10:
                    # Use autocorrelation to detect cycles
                    autocorr = pd.Series(gaps).autocorr(lag=1)
                    if autocorr > 0.5:
                        # Possible cyclic pattern
                        cyclic_pattern = round(np.mean(gaps)) + 1
            
            # Store metrics for this number
            self.number_metrics[number] = {
                'occurrences': len(occurrences),
                'avg_gap': avg_gap,
                'draws_since_last': draws_since_last,
                'cyclic_pattern': cyclic_pattern,
                'due_score': self._calculate_due_score(avg_gap, draws_since_last, cyclic_pattern)
            }
        
        # Do the same for stars
        self.star_metrics = {}
        star_columns = [f's{i}' for i in range(1, 3)]
        
        for star in range(1, 13):
            # Create time series for this star
            occurrences = []
            for idx, row in self.historical_data.iterrows():
                if any(row[col] == star for col in star_columns):
                    occurrences.append(idx)
            
            # Calculate gaps between occurrences
            gaps = [occurrences[i] - occurrences[i+1] - 1 for i in range(len(occurrences)-1)]
            avg_gap = np.mean(gaps) if gaps else 0
            
            # Calculate draws since last appearance
            draws_since_last = occurrences[0] if occurrences else len(self.historical_data)
            
            # Try to identify cyclic patterns (simpler for stars)
            cyclic_pattern = None
            if len(gaps) >= 3:
                if len(set(gaps[:2])) == 1 and gaps[0] == gaps[2]:
                    cyclic_pattern = gaps[0] + 1
            
            # Store metrics for this star
            self.star_metrics[star] = {
                'occurrences': len(occurrences),
                'avg_gap': avg_gap,
                'draws_since_last': draws_since_last,
                'cyclic_pattern': cyclic_pattern,
                'due_score': self._calculate_due_score(avg_gap, draws_since_last, cyclic_pattern)
            }
    
    def _calculate_due_score(self, avg_gap, draws_since_last, cyclic_pattern):
        """
        Calculate a 'due' score for a number or star.
        Higher score means the number is more likely to appear soon.
        
        Parameters:
        -----------
        avg_gap : float
            Average gap between occurrences
        draws_since_last : int
            Number of draws since last appearance
        cyclic_pattern : int or None
            Identified cyclic pattern, if any
        
        Returns:
        --------
        float
            Due score (0-1)
        """
        if cyclic_pattern is not None:
            # If we identified a cycle, use it for prediction
            cycle_ratio = draws_since_last / cyclic_pattern
            
            # Score is higher as we approach the cycle length
            if cycle_ratio >= 0.8:
                return min(cycle_ratio, 0.99)  # Cap at 0.99
            else:
                return 0.5 * cycle_ratio  # Lower score for early in the cycle
        else:
            # Use the average gap as a fallback
            if avg_gap > 0:
                gap_ratio = draws_since_last / avg_gap
                
                # Score is higher as we approach the average gap
                if gap_ratio >= 0.7:
                    return min(gap_ratio * 0.8, 0.9)  # Cap at 0.9 (less certain than cycle)
                else:
                    return 0.4 * gap_ratio  # Lower score for early in the gap
            else:
                return 0.1  # Default low score if we can't calculate
    
    def get_due_numbers(self, top_n=10):
        """
        Get the top N numbers most likely to appear soon based on time patterns.
        
        Parameters:
        -----------
        top_n : int
            Number of numbers to return
        
        Returns:
        --------
        list of tuples
            List of (number, due_score) tuples, sorted by score
        """
        # Sort numbers by due score
        sorted_numbers = sorted(
            [(num, metrics['due_score']) for num, metrics in self.number_metrics.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_numbers[:top_n]
    
    def get_due_stars(self, top_n=5):
        """
        Get the top N stars most likely to appear soon based on time patterns.
        
        Parameters:
        -----------
        top_n : int
            Number of stars to return
        
        Returns:
        --------
        list of tuples
            List of (star, due_score) tuples, sorted by score
        """
        # Sort stars by due score
        sorted_stars = sorted(
            [(star, metrics['due_score']) for star, metrics in self.star_metrics.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_stars[:top_n]
    
    def generate_combinations(self, num_combinations=5):
        """
        Generate combinations using the time series model.
        
        Parameters:
        -----------
        num_combinations : int
            Number of combinations to generate
        
        Returns:
        --------
        list
            List of EuromillionsCombination objects
        """
        combinations = []
        
        for _ in range(num_combinations):
            # Get top due numbers and stars
            due_numbers = self.get_due_numbers(20)  # Get more than we need
            due_stars = self.get_due_stars(6)
            
            # Select 5 numbers with weighted probability based on due scores
            numbers = []
            remaining_numbers = due_numbers.copy()
            
            for _ in range(5):
                if not remaining_numbers:
                    break
                
                # Extract numbers and weights
                nums, weights = zip(*remaining_numbers)
                
                # Normalize weights
                weights = np.array(weights)
                weights = weights / np.sum(weights)
                
                # Weighted random choice
                selected_idx = np.random.choice(len(nums), p=weights)
                selected_num = nums[selected_idx]
                
                numbers.append(selected_num)
                
                # Remove selected number
                remaining_numbers.pop(selected_idx)
            
            # If we still need more numbers, add randomly
            while len(numbers) < 5:
                num = random.randint(1, 50)
                if num not in numbers:
                    numbers.append(num)
            
            # Select 2 stars with weighted probability
            stars = []
            remaining_stars = due_stars.copy()
            
            for _ in range(2):
                if not remaining_stars:
                    break
                
                # Extract stars and weights
                star_nums, star_weights = zip(*remaining_stars)
                
                # Normalize weights
                star_weights = np.array(star_weights)
                star_weights = star_weights / np.sum(star_weights)
                
                # Weighted random choice
                selected_idx = np.random.choice(len(star_nums), p=star_weights)
                selected_star = star_nums[selected_idx]
                
                stars.append(selected_star)
                
                # Remove selected star
                remaining_stars.pop(selected_idx)
            
            # If we still need more stars, add randomly
            while len(stars) < 2:
                star = random.randint(1, 12)
                if star not in stars:
                    stars.append(star)
            
            # Calculate score as average due score
            number_scores = [self.number_metrics[n]['due_score'] for n in numbers]
            star_scores = [self.star_metrics[s]['due_score'] for s in stars]
            
            avg_score = (sum(number_scores) / 5 + sum(star_scores) / 2) / 2
            normalized_score = avg_score * 100
            
            combinations.append(EuromillionsCombination(
                numbers, 
                stars,
                score=normalized_score,
                strategy="TimeSeries"
            ))
        
        return combinations
