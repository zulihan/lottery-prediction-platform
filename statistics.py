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
        
        return {
            "min_sum": sum_series.min(),
            "max_sum": sum_series.max(),
            "mean_sum": sum_series.mean(),
            "median_sum": sum_series.median(),
            "most_common_ranges": pd.cut(sum_series, bins=5).value_counts().to_dict()
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