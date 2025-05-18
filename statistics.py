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
    
    def get_frequency(self, number):
        """Get frequency of a main number"""
        return self.number_frequency.get(number, 0)
    
    def get_star_frequency(self, star):
        """Get frequency of a star number"""
        return self.star_frequency.get(star, 0)
    
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