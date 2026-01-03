import pandas as pd
import numpy as np
from collections import Counter

class EuromillionsStatistics:
    """
    Class for analyzing Euromillions data and calculating various statistics.
    """
    
    def __init__(self, data):
        """
        Initialize with Euromillions drawing data.
        
        Parameters:
        -----------
        data : pandas.DataFrame
            DataFrame containing Euromillions drawing data
        """
        self.data = data
        self.number_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        self.star_cols = ['s1', 's2']
        
        # Calculate basic frequency statistics
        self._calculate_frequencies()
    
    def _calculate_frequencies(self):
        """Calculate frequency statistics for numbers and stars"""
        # Get all drawn numbers
        all_numbers = pd.Series(self.data[self.number_cols].values.flatten())
        all_stars = pd.Series(self.data[self.star_cols].values.flatten())
        
        # Calculate frequencies
        self.number_frequency = all_numbers.value_counts().to_dict()
        self.star_frequency = all_stars.value_counts().to_dict()
        
        # Fill in missing values
        for i in range(1, 51):
            if i not in self.number_frequency:
                self.number_frequency[i] = 0
        
        for i in range(1, 13):
            if i not in self.star_frequency:
                self.star_frequency[i] = 0
    
    def get_frequency(self, number=None):
        """
        Get frequency of a main number.
        If number is None, returns the full dictionary of frequencies.
        """
        if number is None:
            return self.number_frequency
        return self.number_frequency.get(number, 0)
    
    def get_star_frequency(self, star=None):
        """
        Get frequency of a star number.
        If star is None, returns the full dictionary of frequencies.
        """
        if star is None:
            return self.star_frequency
        return self.star_frequency.get(star, 0)
        
    def get_number_statistics(self, number):
        """Get detailed statistics for a specific number
        
        Parameters:
        -----------
        number : int
            The number to analyze
            
        Returns:
        --------
        dict
            Dictionary with statistics for the number
        """
        # Default statistics with no pattern
        stats = {
            'frequency': self.get_frequency(number),
            'cyclic_pattern': 0,
            'draws_since_last': 0
        }
        
        # Check for the number in each draw to find patterns
        appearances = []
        for i, row in self.data.iterrows():
            if number in [row[col] for col in self.number_cols]:
                appearances.append(i)
        
        # Calculate draws since last appearance
        if appearances:
            stats['draws_since_last'] = len(self.data) - appearances[0] - 1
        
        # Analyze for cyclical patterns
        if len(appearances) >= 3:
            # Calculate gaps between appearances
            gaps = [appearances[i] - appearances[i+1] for i in range(len(appearances)-1)]
            
            # Calculate average gap (cycle)
            avg_gap = sum(gaps) / len(gaps)
            
            # Only consider it a cycle if variance is low
            gap_variance = sum((g - avg_gap)**2 for g in gaps) / len(gaps)
            if gap_variance < (avg_gap * 0.5):  # Low variance relative to average
                stats['cyclic_pattern'] = avg_gap
        
        return stats
    
    def get_hot_numbers(self, count=10):
        """Get the most frequent main numbers"""
        sorted_freq = sorted(self.number_frequency.items(), key=lambda x: x[1], reverse=True)
        return [num for num, _ in sorted_freq[:count]]
    
    def get_cold_numbers(self, count=10):
        """Get the least frequent main numbers"""
        sorted_freq = sorted(self.number_frequency.items(), key=lambda x: x[1])
        return [num for num, _ in sorted_freq[:count]]
    
    def get_hot_stars(self, count=5):
        """Get the most frequent star numbers"""
        sorted_freq = sorted(self.star_frequency.items(), key=lambda x: x[1], reverse=True)
        return [star for star, _ in sorted_freq[:count]]
    
    def get_cold_stars(self, count=5):
        """Get the least frequent star numbers"""
        sorted_freq = sorted(self.star_frequency.items(), key=lambda x: x[1])
        return [star for star, _ in sorted_freq[:count]]
    
    def get_weighted_frequency(self, recent_weight=0.5):
        """
        Get frequency with optional weighting for recent draws.
        
        Parameters:
        -----------
        recent_weight : float
            Weight to give recent draws (0.0 - 1.0)
            
        Returns:
        --------
        dict
            Dictionary mapping numbers to weighted frequencies
        """
        # Base frequency
        weighted_freq = self.number_frequency.copy()
        
        # If recent weighting is requested
        if recent_weight > 0:
            # Get recent draws (last 20%)
            recent_count = max(1, int(len(self.data) * 0.2))
            recent_data = self.data.head(recent_count)
            
            # Calculate recent frequencies
            recent_numbers = pd.Series(recent_data[self.number_cols].values.flatten())
            recent_freq = recent_numbers.value_counts().to_dict()
            
            # Apply weighted combination
            for num in weighted_freq:
                recent_val = recent_freq.get(num, 0) 
                base_val = self.number_frequency[num]
                
                # Scale recent to match base scale
                if sum(recent_freq.values()) > 0:
                    scale_factor = sum(self.number_frequency.values()) / sum(recent_freq.values())
                    recent_val = recent_val * scale_factor
                
                # Combine with weighting
                weighted_freq[num] = (1 - recent_weight) * base_val + recent_weight * recent_val
        
        return weighted_freq
    
    def get_weighted_star_frequency(self, recent_weight=0.5):
        """
        Get star frequency with optional weighting for recent draws.
        
        Parameters:
        -----------
        recent_weight : float
            Weight to give recent draws (0.0 - 1.0)
            
        Returns:
        --------
        dict
            Dictionary mapping stars to weighted frequencies
        """
        # Base frequency
        weighted_freq = self.star_frequency.copy()
        
        # If recent weighting is requested
        if recent_weight > 0:
            # Get recent draws (last 20%)
            recent_count = max(1, int(len(self.data) * 0.2))
            recent_data = self.data.head(recent_count)
            
            # Calculate recent frequencies
            recent_stars = pd.Series(recent_data[self.star_cols].values.flatten())
            recent_freq = recent_stars.value_counts().to_dict()
            
            # Apply weighted combination
            for star in weighted_freq:
                recent_val = recent_freq.get(star, 0) 
                base_val = self.star_frequency[star]
                
                # Scale recent to match base scale
                if sum(recent_freq.values()) > 0:
                    scale_factor = sum(self.star_frequency.values()) / sum(recent_freq.values())
                    recent_val = recent_val * scale_factor
                
                # Combine with weighting
                weighted_freq[star] = (1 - recent_weight) * base_val + recent_weight * recent_val
        
        return weighted_freq
    
    def get_distribution_stats(self):
        """
        Get statistics about number distributions.
        
        Returns:
        --------
        dict
            Dictionary with distribution statistics
        """
        even_odd_patterns = []
        low_high_patterns = []
        
        # Analyze each draw
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in self.number_cols]
            
            # Even/odd analysis
            odd_count = sum(1 for n in numbers if n % 2 == 1)
            even_count = 5 - odd_count
            even_odd_patterns.append(f"{even_count}e-{odd_count}o")
            
            # Low/high analysis
            low_count = sum(1 for n in numbers if n <= 25)
            high_count = 5 - low_count
            low_high_patterns.append(f"{low_count}l-{high_count}h")
        
        # Count patterns
        even_odd_counts = Counter(even_odd_patterns)
        low_high_counts = Counter(low_high_patterns)
        
        # Get most common patterns
        most_common_even_odd = even_odd_counts.most_common(1)[0][0] if even_odd_counts else "Unknown"
        most_common_low_high = low_high_counts.most_common(1)[0][0] if low_high_counts else "Unknown"
        
        return {
            "even_odd_pattern": most_common_even_odd,
            "low_high_pattern": most_common_low_high
        }
    
    def get_recency_stats(self, draws=20):
        """
        Get statistics for the most recent draws.
        
        Parameters:
        -----------
        draws : int
            Number of recent draws to analyze
            
        Returns:
        --------
        dict
            Dictionary with recency statistics
        """
        # Get recent data
        recent_data = self.data.head(min(draws, len(self.data)))
        
        # Calculate frequencies
        recent_numbers = pd.Series(recent_data[self.number_cols].values.flatten())
        recent_stars = pd.Series(recent_data[self.star_cols].values.flatten())
        
        recent_number_freq = recent_numbers.value_counts()
        recent_star_freq = recent_stars.value_counts()
        
        # Get hot numbers and stars
        hot_numbers = list(recent_number_freq.head(5).index)
        hot_stars = list(recent_star_freq.head(3).index)
        
        return {
            "hot_numbers": hot_numbers,
            "hot_lucky": hot_stars
        }
        
    def get_sum_distribution(self):
        """
        Analyze the sum distribution of drawn numbers.
        
        Returns:
        --------
        dict
            Dictionary with sum distribution statistics
        """
        # Calculate sums of each draw
        sums = []
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in self.number_cols]
            sums.append(sum(numbers))
            
        # Analyze the distribution of sums
        sum_series = pd.Series(sums)
        
        # Convert numeric values to integers or floats as appropriate
        min_sum = int(sum_series.min()) if not pd.isna(sum_series.min()) else 0
        max_sum = int(sum_series.max()) if not pd.isna(sum_series.max()) else 0
        mean_sum = float(sum_series.mean()) if not pd.isna(sum_series.mean()) else 0.0
        median_sum = float(sum_series.median()) if not pd.isna(sum_series.median()) else 0.0
        
        # Create range distribution as a separate object
        try:
            range_counts = pd.cut(sum_series, bins=5).value_counts()
            range_dict = {str(k): int(v) for k, v in range_counts.items()}
        except:
            range_dict = {}
        
        return {
            "min_sum": min_sum,
            "max_sum": max_sum,
            "mean_sum": mean_sum,
            "median_sum": median_sum,
            "most_common_ranges": range_dict
        }
        
    def get_consecutive_analysis(self):
        """
        Analyze the presence of consecutive numbers in drawings.
        
        Returns:
        --------
        dict
            Dictionary with consecutive number statistics
        """
        consecutive_counts = []
        
        # Check each draw for consecutive numbers
        for _, row in self.data.iterrows():
            numbers = sorted([row[col] for col in self.number_cols])
            consecutive_count = 0
            
            # Count consecutive pairs
            for i in range(len(numbers)-1):
                if numbers[i+1] - numbers[i] == 1:
                    consecutive_count += 1
            
            consecutive_counts.append(consecutive_count)
        
        consecutive_series = pd.Series(consecutive_counts)
        
        return {
            "max_consecutive": consecutive_series.max(),
            "mean_consecutive": consecutive_series.mean(),
            "pct_with_consecutive": (consecutive_series > 0).mean() * 100,
            "distribution": consecutive_series.value_counts().sort_index().to_dict()
        }
    
    def get_gap_analysis(self, number=None):
        """
        Analyze the gaps between appearances of a specific number.
        
        Parameters:
        -----------
        number : int
            The number to analyze gaps for
            
        Returns:
        --------
        dict
            Dictionary with gap statistics
        """
        if number is None:  # Return a summary for all numbers if none specified
            avg_gaps = {}
            for num in range(1, 51):
                appearances = []
                for i, row in self.data.iterrows():
                    if num in [row[col] for col in self.number_cols]:
                        appearances.append(i)
                
                if len(appearances) > 1:
                    gaps = [appearances[i] - appearances[i+1] for i in range(len(appearances)-1)]
                    avg_gaps[num] = sum(gaps) / len(gaps) if gaps else 0
            
            return {
                "average_gaps": avg_gaps,
                "most_regular": sorted(avg_gaps.items(), key=lambda x: x[1], reverse=True)[:5]
            }
        else:
            # Find appearances of the specific number
            appearances = []
            for i, row in self.data.iterrows():
                if number in [row[col] for col in self.number_cols]:
                    appearances.append(i)
            
            if len(appearances) <= 1:
                return {"gaps": [], "avg_gap": 0, "last_appearance": appearances[0] if appearances else -1}
            
            # Calculate gaps between appearances
            gaps = [appearances[i] - appearances[i+1] for i in range(len(appearances)-1)]
            
            return {
                "gaps": gaps,
                "avg_gap": sum(gaps) / len(gaps),
                "last_appearance": appearances[0],
                "draws_since_last": appearances[0] if appearances else -1
            }

    def get_number_range_distribution(self, ranges=None):
        """
        Get distribution of numbers across specified ranges.

        Parameters:
        -----------
        ranges : list of tuples, optional
            List of (start, end) tuples defining ranges
            Default: [(1,10), (11,20), (21,30), (31,40), (41,50)]

        Returns:
        --------
        dict
            Dictionary mapping range labels to occurrence counts
            Example: {"1-10": 45, "11-20": 52, ...}
        """
        if ranges is None:
            ranges = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 50)]

        distribution = {}
        for start, end in ranges:
            range_label = f"{start}-{end}"
            count = sum(
                self.number_frequency.get(num, 0)
                for num in range(start, end + 1)
            )
            distribution[range_label] = count

        return distribution

    def get_even_odd_distribution(self):
        """
        Get distribution of even vs odd numbers in historical draws.

        Returns:
        --------
        dict
            Dictionary with even/odd counts and ratios:
            {
                'even_count': int,      # Total occurrences of even numbers
                'odd_count': int,       # Total occurrences of odd numbers
                'even_ratio': float,    # Proportion of even numbers (0.0-1.0)
                'odd_ratio': float,     # Proportion of odd numbers (0.0-1.0)
                0: int,                 # Count of draws with 0 even numbers
                1: int,                 # Count of draws with 1 even number
                2: int,                 # Count of draws with 2 even numbers
                3: int,                 # Count of draws with 3 even numbers
                4: int,                 # Count of draws with 4 even numbers
                5: int                  # Count of draws with 5 even numbers
            }
        """
        # Calculate total even/odd occurrences across all draws
        even_count = sum(
            count for num, count in self.number_frequency.items()
            if num % 2 == 0
        )
        odd_count = sum(
            count for num, count in self.number_frequency.items()
            if num % 2 == 1
        )
        total = even_count + odd_count

        # Calculate how many draws have 0, 1, 2, 3, 4, or 5 even numbers
        even_per_draw = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in self.number_cols]
            even_in_draw = sum(1 for n in numbers if n % 2 == 0)
            even_per_draw[even_in_draw] = even_per_draw.get(even_in_draw, 0) + 1

        return {
            'even_count': even_count,
            'odd_count': odd_count,
            'even_ratio': even_count / total if total > 0 else 0,
            'odd_ratio': odd_count / total if total > 0 else 0,
            **even_per_draw  # Unpack the distribution of even numbers per draw
        }