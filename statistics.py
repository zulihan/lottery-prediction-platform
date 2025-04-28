import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter, defaultdict
import itertools

class EuromillionsStatistics:
    """
    Class for statistical analysis of Euromillions data.
    """
    
    def __init__(self, data):
        """
        Initialize the statistics class with processed Euromillions data.
        
        Parameters:
        -----------
        data : pandas.DataFrame
            The processed Euromillions data
        """
        self.data = data
        self.num_columns = [f'n{i}' for i in range(1, 6)]
        self.star_columns = [f's{i}' for i in range(1, 3)]
        
        # Calculate basic statistics
        self.calculate_basic_stats()
    
    def calculate_basic_stats(self):
        """
        Calculate basic statistics about the dataset.
        """
        self.total_draws = len(self.data)
        
        # Calculate number frequencies
        self.number_freq = {}
        for i in range(1, 51):
            count = sum((self.data[col] == i).sum() for col in self.num_columns)
            self.number_freq[i] = count / (self.total_draws * 5)  # Normalized frequency
        
        # Calculate star frequencies
        self.star_freq = {}
        for i in range(1, 13):
            count = sum((self.data[col] == i).sum() for col in self.star_columns)
            self.star_freq[i] = count / (self.total_draws * 2)  # Normalized frequency
        
        # Calculate number pairs frequency
        self.calculate_number_pairs()
        
        # Calculate star pairs frequency
        self.calculate_star_pairs()
    
    def calculate_number_pairs(self):
        """
        Calculate the frequency of number pairs.
        """
        # Initialize the frequency dictionary for all possible pairs
        self.number_pairs = {(i, j): 0 for i in range(1, 50) for j in range(i+1, 51)}
        
        # Count occurrences of each pair
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in self.num_columns]
            for i, j in itertools.combinations(sorted(numbers), 2):
                self.number_pairs[(i, j)] += 1
        
        # Normalize frequencies
        for pair in self.number_pairs:
            self.number_pairs[pair] /= self.total_draws
    
    def calculate_star_pairs(self):
        """
        Calculate the frequency of star pairs.
        """
        # Initialize the frequency dictionary for all possible star pairs
        self.star_pairs = {(i, j): 0 for i in range(1, 12) for j in range(i+1, 13)}
        
        # Count occurrences of each pair
        for _, row in self.data.iterrows():
            stars = [row[col] for col in self.star_columns]
            if stars[0] < stars[1]:
                self.star_pairs[(stars[0], stars[1])] += 1
            else:
                self.star_pairs[(stars[1], stars[0])] += 1
        
        # Normalize frequencies
        for pair in self.star_pairs:
            self.star_pairs[pair] /= self.total_draws
    
    def get_frequency(self):
        """
        Get the frequency of all numbers.
        
        Returns:
        --------
        pandas.Series
            The frequency of each number (1-50)
        """
        return pd.Series(self.number_freq)
    
    def get_star_frequency(self):
        """
        Get the frequency of all star numbers.
        
        Returns:
        --------
        pandas.Series
            The frequency of each star number (1-12)
        """
        return pd.Series(self.star_freq)
    
    def get_weighted_frequency(self, recent_weight=0.6):
        """
        Get a weighted frequency that combines recent and historical data.
        
        Parameters:
        -----------
        recent_weight : float
            Weight to give to recent draws (0.0 - 1.0)
        
        Returns:
        --------
        pandas.Series
            The weighted frequency of each number (1-50)
        """
        historical_weight = 1.0 - recent_weight
        
        # Define recent vs. historical split (last 20% of draws are considered recent)
        split_idx = int(self.total_draws * 0.2)
        
        # Calculate frequencies for recent draws
        recent_data = self.data.iloc[:split_idx]
        recent_total = len(recent_data)
        
        recent_freq = {}
        for i in range(1, 51):
            count = sum((recent_data[col] == i).sum() for col in self.num_columns)
            recent_freq[i] = count / (recent_total * 5)
        
        # Calculate frequencies for historical draws
        historical_data = self.data.iloc[split_idx:]
        historical_total = len(historical_data)
        
        historical_freq = {}
        for i in range(1, 51):
            count = sum((historical_data[col] == i).sum() for col in self.num_columns)
            historical_freq[i] = count / (historical_total * 5)
        
        # Combine with weights
        weighted_freq = {}
        for i in range(1, 51):
            weighted_freq[i] = (recent_weight * recent_freq[i]) + (historical_weight * historical_freq[i])
        
        return pd.Series(weighted_freq)
    
    def get_weighted_star_frequency(self, recent_weight=0.6):
        """
        Get a weighted frequency that combines recent and historical data for stars.
        
        Parameters:
        -----------
        recent_weight : float
            Weight to give to recent draws (0.0 - 1.0)
        
        Returns:
        --------
        pandas.Series
            The weighted frequency of each star number (1-12)
        """
        historical_weight = 1.0 - recent_weight
        
        # Define recent vs. historical split (last 20% of draws are considered recent)
        split_idx = int(self.total_draws * 0.2)
        
        # Calculate frequencies for recent draws
        recent_data = self.data.iloc[:split_idx]
        recent_total = len(recent_data)
        
        recent_freq = {}
        for i in range(1, 13):
            count = sum((recent_data[col] == i).sum() for col in self.star_columns)
            recent_freq[i] = count / (recent_total * 2)
        
        # Calculate frequencies for historical draws
        historical_data = self.data.iloc[split_idx:]
        historical_total = len(historical_data)
        
        historical_freq = {}
        for i in range(1, 13):
            count = sum((historical_data[col] == i).sum() for col in self.star_columns)
            historical_freq[i] = count / (historical_total * 2)
        
        # Combine with weights
        weighted_freq = {}
        for i in range(1, 13):
            weighted_freq[i] = (recent_weight * recent_freq[i]) + (historical_weight * historical_freq[i])
        
        return pd.Series(weighted_freq)
    
    def get_number_pairs_frequency(self):
        """
        Get the frequency of number pairs.
        
        Returns:
        --------
        dict
            Dictionary mapping number pairs to their frequencies
        """
        return self.number_pairs
    
    def get_star_pairs_frequency(self):
        """
        Get the frequency of star pairs.
        
        Returns:
        --------
        dict
            Dictionary mapping star pairs to their frequencies
        """
        return self.star_pairs
    
    def get_top_number_pairs(self, n=10):
        """
        Get the top N most frequent number pairs.
        
        Parameters:
        -----------
        n : int
            Number of pairs to return
        
        Returns:
        --------
        list of tuples
            List of (pair, count) tuples, sorted by count
        """
        # Convert frequencies to counts
        pair_counts = {pair: int(freq * self.total_draws) for pair, freq in self.number_pairs.items()}
        
        # Sort by count and take the top N
        return sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def get_number_time_series(self, number):
        """
        Get time series data for a specific number.
        
        Parameters:
        -----------
        number : int
            The number to analyze (1-50)
        
        Returns:
        --------
        pandas.DataFrame
            DataFrame with dates and occurrence info
        """
        if not 1 <= number <= 50:
            raise ValueError("Number must be between 1 and 50")
        
        # Create a time series with all dates
        dates = sorted(self.data['date'].unique())
        time_series = pd.DataFrame({'date': dates})
        
        # Add occurrence column (1 if the number appears in that draw, 0 otherwise)
        occurrences = []
        for date in dates:
            draw = self.data[self.data['date'] == date]
            if any([(draw[col] == number).any() for col in self.num_columns]):
                occurrences.append(1)
            else:
                occurrences.append(0)
        
        time_series['occurrence'] = occurrences
        
        # Add a cumulative sum column
        time_series['cumulative'] = time_series['occurrence'].cumsum()
        
        # Add a rolling average column (last 10 draws)
        time_series['rolling_avg'] = time_series['occurrence'].rolling(window=10, min_periods=1).mean()
        
        return time_series
    
    def get_number_statistics(self, number):
        """
        Get detailed statistics for a specific number.
        
        Parameters:
        -----------
        number : int
            The number to analyze (1-50)
        
        Returns:
        --------
        dict
            Dictionary with various statistics about the number
        """
        if not 1 <= number <= 50:
            raise ValueError("Number must be between 1 and 50")
        
        # Basic frequency
        frequency = self.number_freq[number] * 100  # Convert to percentage
        
        # Occurrences and gaps
        occurrences = []
        for idx, row in self.data.iterrows():
            if any([(row[col] == number).any() if isinstance(row[col], pd.Series) else row[col] == number for col in self.num_columns]):
                occurrences.append(idx)
        
        # Calculate gaps between occurrences
        gaps = [occurrences[i] - occurrences[i+1] - 1 for i in range(len(occurrences)-1)]
        avg_gap = np.mean(gaps) if gaps else 0
        
        # Calculate draws since last appearance
        draws_since_last = occurrences[0] if occurrences else self.total_draws
        
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
        
        # Return all statistics
        return {
            'frequency': frequency,
            'occurrences': len(occurrences),
            'avg_gap': avg_gap,
            'draws_since_last': draws_since_last,
            'cyclic_pattern': cyclic_pattern
        }
    
    def get_day_of_week_distribution(self, number):
        """
        Get the distribution of occurrences by day of week for a specific number.
        
        Parameters:
        -----------
        number : int
            The number to analyze (1-50)
        
        Returns:
        --------
        pandas.Series
            Series with day of week as index and occurrences as values
        """
        if not 1 <= number <= 50:
            raise ValueError("Number must be between 1 and 50")
        
        # Get draws where the number appears
        number_draws = self.data[
            (self.data['n1'].astype(int) == number) |
            (self.data['n2'].astype(int) == number) |
            (self.data['n3'].astype(int) == number) |
            (self.data['n4'].astype(int) == number) |
            (self.data['n5'].astype(int) == number)
        ]
        
        if number_draws.empty:
            return None
        
        # Count occurrences by day of week
        day_counts = number_draws['day_of_week'].value_counts()
        
        # Calculate the total draws for each day of week
        total_by_day = self.data['day_of_week'].value_counts()
        
        # Calculate the percentage for each day
        day_percentages = (day_counts / total_by_day) * 100
        
        # Ensure all days are represented
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in all_days:
            if day not in day_percentages:
                day_percentages[day] = 0
        
        # Sort by day of week
        day_order = {day: i for i, day in enumerate(all_days)}
        return day_percentages.sort_index(key=lambda x: x.map(day_order))
    
    def get_even_odd_distribution(self):
        """
        Get the distribution of even/odd numbers in winning combinations.
        
        Returns:
        --------
        dict
            Dictionary with counts for each even/odd combination
        """
        # Initialize counts for all possible combinations (0-5 even numbers)
        counts = {i: 0 for i in range(6)}
        
        # Count even numbers in each draw
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in self.num_columns]
            even_count = sum(1 for num in numbers if num % 2 == 0)
            counts[even_count] += 1
        
        # Convert to percentages
        total = sum(counts.values())
        percentages = {k: (v / total) * 100 for k, v in counts.items()}
        
        return percentages
    
    def get_common_even_odd_patterns(self):
        """
        Get the most common patterns of even/odd numbers.
        
        Returns:
        --------
        dict
            Dictionary with patterns and their occurrence counts
        """
        patterns = {}
        
        for _, row in self.data.iterrows():
            numbers = sorted([row[col] for col in self.num_columns])
            pattern = ''.join(['E' if num % 2 == 0 else 'O' for num in numbers])
            patterns[pattern] = patterns.get(pattern, 0) + 1
        
        # Sort by count
        return dict(sorted(patterns.items(), key=lambda x: x[1], reverse=True))
    
    def get_number_range_distribution(self):
        """
        Get the distribution of numbers across different ranges.
        
        Returns:
        --------
        dict
            Dictionary with ranges and their percentages
        """
        ranges = {"1-10": 0, "11-20": 0, "21-30": 0, "31-40": 0, "41-50": 0}
        total_numbers = self.total_draws * 5
        
        for _, row in self.data.iterrows():
            for col in self.num_columns:
                num = row[col]
                if 1 <= num <= 10:
                    ranges["1-10"] += 1
                elif 11 <= num <= 20:
                    ranges["11-20"] += 1
                elif 21 <= num <= 30:
                    ranges["21-30"] += 1
                elif 31 <= num <= 40:
                    ranges["31-40"] += 1
                elif 41 <= num <= 50:
                    ranges["41-50"] += 1
        
        # Convert to percentages
        return {k: (v / total_numbers) * 100 for k, v in ranges.items()}
    
    def get_sum_distribution(self):
        """
        Get the distribution of sums of the 5 main numbers.
        
        Returns:
        --------
        dict
            Dictionary with sum ranges and their percentages
        """
        # Calculate sum for each draw
        sums = []
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in self.num_columns]
            sums.append(sum(numbers))
        
        # Create buckets for the sums
        min_sum, max_sum = min(sums), max(sums)
        buckets = {}
        
        # Create 10 buckets
        step = (max_sum - min_sum) // 10
        for i in range(10):
            lower = min_sum + (i * step)
            upper = min_sum + ((i + 1) * step) if i < 9 else max_sum + 1
            bucket_name = f"{lower}-{upper-1}"
            buckets[bucket_name] = sum(1 for s in sums if lower <= s < upper)
        
        # Convert to percentages
        total = len(sums)
        return {k: (v / total) * 100 for k, v in buckets.items()}
    
    def get_average_sum(self):
        """
        Get the average sum of the 5 main numbers.
        
        Returns:
        --------
        float
            The average sum
        """
        sums = []
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in self.num_columns]
            sums.append(sum(numbers))
        
        return np.mean(sums)
    
    def get_most_common_sums(self, n=5):
        """
        Get the most common sums of the 5 main numbers.
        
        Parameters:
        -----------
        n : int
            Number of common sums to return
        
        Returns:
        --------
        list of tuples
            List of (sum, count) tuples
        """
        sums = []
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in self.num_columns]
            sums.append(sum(numbers))
        
        # Count occurrences
        sum_counts = Counter(sums)
        
        # Return most common
        return sum_counts.most_common(n)
    
    def get_top_correlated_pairs(self, n=5, positive=True):
        """
        Get the top N most correlated number pairs.
        
        Parameters:
        -----------
        n : int
            Number of pairs to return
        positive : bool
            If True, return positively correlated pairs, otherwise negative
        
        Returns:
        --------
        list of tuples
            List of ((num1, num2), correlation) tuples
        """
        # Create a matrix to hold occurrences of each number
        occurrences = np.zeros((51, self.total_draws))
        
        for draw_idx, (_, row) in enumerate(self.data.iterrows()):
            for col in self.num_columns:
                num = row[col]
                occurrences[num, draw_idx] = 1
        
        # Calculate correlations between all pairs
        correlations = []
        for i in range(1, 51):
            for j in range(i+1, 51):
                corr = np.corrcoef(occurrences[i], occurrences[j])[0, 1]
                correlations.append(((i, j), corr))
        
        # Sort by correlation
        if positive:
            # Return pairs with highest positive correlation
            return sorted(correlations, key=lambda x: x[1], reverse=True)[:n]
        else:
            # Return pairs with most negative correlation
            return sorted(correlations, key=lambda x: x[1])[:n]
    
    def get_markov_transition_matrix(self, lag=1):
        """
        Calculate a Markov transition matrix for numbers.
        Shows the probability of a number appearing after another.
        
        Parameters:
        -----------
        lag : int
            Number of draws to look back
        
        Returns:
        --------
        pandas.DataFrame
            Transition matrix
        """
        # Initialize transition counts matrix
        transition_counts = np.zeros((51, 51))
        
        # Calculate transitions
        for draw_idx in range(lag, self.total_draws):
            current_draw = set([self.data.iloc[draw_idx][col] for col in self.num_columns])
            previous_draw = set([self.data.iloc[draw_idx-lag][col] for col in self.num_columns])
            
            # Count transitions from previous to current
            for prev_num in previous_draw:
                for curr_num in current_draw:
                    transition_counts[prev_num, curr_num] += 1
        
        # Calculate probabilities
        transition_probs = np.zeros((51, 51))
        for i in range(1, 51):
            row_sum = transition_counts[i].sum()
            if row_sum > 0:
                transition_probs[i] = transition_counts[i] / row_sum
        
        # Create DataFrame for easier handling
        transition_matrix = pd.DataFrame(
            transition_probs[1:51, 1:51],
            index=range(1, 51),
            columns=range(1, 51)
        )
        
        return transition_matrix
    
    def get_bayesian_probabilities(self, num_recent_draws=20):
        """
        Calculate Bayesian updated probabilities for each number.
        
        Parameters:
        -----------
        num_recent_draws : int
            Number of recent draws to use for updating
        
        Returns:
        --------
        pandas.Series
            Updated probabilities for each number
        """
        # Prior probabilities (based on historical data excluding recent draws)
        historical_data = self.data.iloc[num_recent_draws:]
        historical_total = len(historical_data) * 5  # 5 numbers per draw
        
        prior_probs = {}
        for i in range(1, 51):
            count = sum((historical_data[col] == i).sum() for col in self.num_columns)
            prior_probs[i] = count / historical_total
        
        # Evidence from recent draws
        recent_data = self.data.iloc[:num_recent_draws]
        recent_counts = {}
        for i in range(1, 51):
            recent_counts[i] = sum((recent_data[col] == i).sum() for col in self.num_columns)
        
        # Calculate likelihood
        total_recent_numbers = num_recent_draws * 5
        likelihood = {}
        for i in range(1, 51):
            # Use a simple binomial likelihood
            k = recent_counts[i]  # Number of successes
            n = total_recent_numbers  # Number of trials
            p = prior_probs[i]  # Prior probability
            
            # Binomial PMF: likelihood of k successes in n trials with probability p
            likelihood[i] = stats.binom.pmf(k, n, p)
        
        # Calculate posterior probabilities
        posterior_probs = {}
        total_likelihood = sum(prior_probs[i] * likelihood[i] for i in range(1, 51))
        
        for i in range(1, 51):
            posterior_probs[i] = (prior_probs[i] * likelihood[i]) / total_likelihood
        
        return pd.Series(posterior_probs)
