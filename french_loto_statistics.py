import pandas as pd
import numpy as np
import logging
import database
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FrenchLotoStatistics:
    """
    Class for analyzing French Loto data and generating statistical insights.
    The French Loto uses 5 numbers (1-49) and 1 lucky number (1-10).
    """
    
    def __init__(self, data=None):
        """
        Initialize with historical data.
        
        Args:
            data: DataFrame with French Loto data or None to load from database
        """
        if data is not None:
            self.data = data
        else:
            # Load data from database
            try:
                self.data = self.load_data_from_db()
                logger.info(f"Loaded {len(self.data)} records from database")
            except Exception as e:
                logger.error(f"Failed to load data from database: {e}")
                # Create empty DataFrame with correct columns
                self.data = pd.DataFrame(columns=[
                    'date', 'day_of_week', 'n1', 'n2', 'n3', 'n4', 'n5', 'lucky'
                ])
                logger.warning("Created empty DataFrame for French Loto data")
        
        # Number ranges for French Loto
        self.main_range = range(1, 50)  # 1-49
        self.lucky_range = range(1, 11)  # 1-10
        
        # Compute initial statistics
        self.compute_statistics()
    
    def load_data_from_db(self):
        """Load French Loto data from database"""
        try:
            # Custom SQL to fetch French Loto drawings
            query = """
            SELECT * FROM french_loto_drawings 
            ORDER BY date DESC
            """
            
            # Execute query
            conn = database.get_db_connection()
            if conn:
                return pd.read_sql_query(query, conn)
            else:
                logger.error("Failed to connect to database")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading data from database: {e}")
            return pd.DataFrame()
    
    def compute_statistics(self):
        """Compute basic statistics about the French Loto data"""
        if self.data.empty:
            logger.warning("No data available to compute statistics")
            return
        
        # Frequency analysis for main numbers
        all_numbers = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            all_numbers.extend(self.data[col].tolist())
        
        # Count frequencies
        number_counts = pd.Series(all_numbers).value_counts().reindex(self.main_range, fill_value=0)
        self.number_frequency = number_counts / number_counts.sum()
        
        # Frequency analysis for lucky numbers
        lucky_counts = self.data['lucky'].value_counts().reindex(self.lucky_range, fill_value=0)
        self.lucky_frequency = lucky_counts / lucky_counts.sum()
        
        # Compute historical patterns
        self.compute_historical_patterns()
    
    def compute_historical_patterns(self):
        """Compute historical patterns from the data"""
        if self.data.empty:
            return
        
        # Calculate patterns like even/odd distribution
        self.even_odd_distribution = self.calculate_even_odd_distribution()
        
        # Calculate sum distribution
        self.sum_distribution = self.calculate_sum_distribution()
        
        # Calculate range distribution (spread between min and max number)
        self.range_distribution = self.calculate_range_distribution()
    
    def calculate_even_odd_distribution(self):
        """Calculate distribution of even/odd numbers"""
        if self.data.empty:
            return {}
        
        result = {}
        try:
            # For each draw, count number of even numbers
            even_counts = []
            for _, row in self.data.iterrows():
                even_count = 0
                for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                    if row[col] % 2 == 0:
                        even_count += 1
                even_counts.append(even_count)
            
            # Calculate distribution
            for i in range(6):  # 0 to 5 even numbers
                result[i] = even_counts.count(i) / len(even_counts)
            
        except Exception as e:
            logger.error(f"Error calculating even/odd distribution: {e}")
        
        return result
    
    def calculate_sum_distribution(self):
        """Calculate distribution of sum of numbers"""
        if self.data.empty:
            return {}
        
        result = {}
        try:
            # Calculate sum for each draw
            sums = []
            for _, row in self.data.iterrows():
                total = sum(row[col] for col in ['n1', 'n2', 'n3', 'n4', 'n5'])
                sums.append(total)
            
            # Create bins for sum distribution
            bins = [50, 100, 125, 150, 175, 200, 250]
            labels = ['<100', '100-125', '125-150', '150-175', '175-200', '>200']
            
            # Assign each sum to a bin
            binned_sums = pd.cut(sums, bins=bins, labels=labels, right=False)
            
            # Calculate distribution
            for label in labels:
                result[label] = (binned_sums == label).mean()
            
        except Exception as e:
            logger.error(f"Error calculating sum distribution: {e}")
        
        return result
    
    def calculate_range_distribution(self):
        """Calculate distribution of range between min and max number"""
        if self.data.empty:
            return {}
        
        result = {}
        try:
            # Calculate range for each draw
            ranges = []
            for _, row in self.data.iterrows():
                numbers = [row[col] for col in ['n1', 'n2', 'n3', 'n4', 'n5']]
                ranges.append(max(numbers) - min(numbers))
            
            # Create bins for range distribution
            bins = [0, 20, 30, 40, 50]
            labels = ['<20', '20-30', '30-40', '>40']
            
            # Assign each range to a bin
            binned_ranges = pd.cut(ranges, bins=bins, labels=labels, right=False)
            
            # Calculate distribution
            for label in labels:
                result[label] = (binned_ranges == label).mean()
            
        except Exception as e:
            logger.error(f"Error calculating range distribution: {e}")
        
        return result
    
    def get_hot_numbers(self, count=10):
        """Get the most frequently drawn numbers"""
        return self.number_frequency.sort_values(ascending=False).head(count)
    
    def get_cold_numbers(self, count=10):
        """Get the least frequently drawn numbers"""
        return self.number_frequency.sort_values().head(count)
    
    def get_hot_lucky_numbers(self, count=5):
        """Get the most frequently drawn lucky numbers"""
        return self.lucky_frequency.sort_values(ascending=False).head(count)
    
    def get_cold_lucky_numbers(self, count=5):
        """Get the least frequently drawn lucky numbers"""
        return self.lucky_frequency.sort_values().head(count)
    
    def get_weighted_frequency(self, recent_weight=0.6):
        """
        Get weighted frequency of numbers, giving more weight to recent draws.
        
        Args:
            recent_weight: Weight to assign to recent draws (0-1)
            
        Returns:
            pandas.Series: Weighted frequency for each number
        """
        if self.data.empty:
            return pd.Series(dtype=float)
        
        historical_weight = 1 - recent_weight
        
        # Sort data by date
        sorted_data = self.data.sort_values('date')
        
        # Split data into recent and historical
        cutoff_index = int(len(sorted_data) * 0.7)  # Consider 70% as historical
        historical_data = sorted_data.iloc[:cutoff_index]
        recent_data = sorted_data.iloc[cutoff_index:]
        
        # Calculate frequency for each part
        historical_numbers = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            historical_numbers.extend(historical_data[col].tolist())
        
        recent_numbers = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            recent_numbers.extend(recent_data[col].tolist())
        
        # Count frequencies
        if historical_numbers:
            historical_counts = pd.Series(historical_numbers).value_counts().reindex(self.main_range, fill_value=0)
            historical_freq = historical_counts / historical_counts.sum()
        else:
            historical_freq = pd.Series(0, index=self.main_range)
        
        if recent_numbers:
            recent_counts = pd.Series(recent_numbers).value_counts().reindex(self.main_range, fill_value=0)
            recent_freq = recent_counts / recent_counts.sum()
        else:
            recent_freq = pd.Series(0, index=self.main_range)
        
        # Combine with weights
        weighted_freq = (historical_weight * historical_freq) + (recent_weight * recent_freq)
        
        return weighted_freq
    
    def get_weighted_lucky_frequency(self, recent_weight=0.6):
        """
        Get weighted frequency of lucky numbers, giving more weight to recent draws.
        
        Args:
            recent_weight: Weight to assign to recent draws (0-1)
            
        Returns:
            pandas.Series: Weighted frequency for each lucky number
        """
        if self.data.empty:
            return pd.Series(dtype=float)
        
        historical_weight = 1 - recent_weight
        
        # Sort data by date
        sorted_data = self.data.sort_values('date')
        
        # Split data into recent and historical
        cutoff_index = int(len(sorted_data) * 0.7)  # Consider 70% as historical
        historical_data = sorted_data.iloc[:cutoff_index]
        recent_data = sorted_data.iloc[cutoff_index:]
        
        # Calculate frequency for each part
        if not historical_data.empty:
            historical_counts = historical_data['lucky'].value_counts().reindex(self.lucky_range, fill_value=0)
            historical_freq = historical_counts / historical_counts.sum()
        else:
            historical_freq = pd.Series(0, index=self.lucky_range)
        
        if not recent_data.empty:
            recent_counts = recent_data['lucky'].value_counts().reindex(self.lucky_range, fill_value=0)
            recent_freq = recent_counts / recent_counts.sum()
        else:
            recent_freq = pd.Series(0, index=self.lucky_range)
        
        # Combine with weights
        weighted_freq = (historical_weight * historical_freq) + (recent_weight * recent_freq)
        
        return weighted_freq
    
    def get_recent_winning_combinations(self, count=10):
        """Get the most recent winning combinations"""
        if self.data.empty:
            return pd.DataFrame()
        
        recent_draws = self.data.sort_values('date', ascending=False).head(count)
        result = []
        
        for _, row in recent_draws.iterrows():
            result.append({
                'date': row['date'],
                'numbers': f"{row['n1']}-{row['n2']}-{row['n3']}-{row['n4']}-{row['n5']}",
                'lucky': row['lucky'],
                'day_of_week': row['day_of_week']
            })
        
        return pd.DataFrame(result)
    
    def get_performance_metrics(self):
        """Get performance metrics for French Loto data"""
        metrics = {}
        
        if not self.data.empty:
            # Total number of draws
            metrics['total_draws'] = len(self.data)
            
            # Date range
            metrics['date_range'] = f"{self.data['date'].min()} to {self.data['date'].max()}"
            
            # Most common numbers
            metrics['most_common_numbers'] = self.get_hot_numbers(5).index.tolist()
            
            # Most common lucky numbers
            metrics['most_common_lucky'] = self.get_hot_lucky_numbers(3).index.tolist()
            
            # Most common day of the week
            if 'day_of_week' in self.data.columns:
                day_counts = self.data['day_of_week'].value_counts()
                metrics['most_common_day'] = day_counts.index[0] if not day_counts.empty else "Unknown"
            
            # Pattern metrics
            metrics['even_odd_pattern'] = max(self.even_odd_distribution.items(), key=lambda x: x[1])[0] if self.even_odd_distribution else "Unknown"
            metrics['common_sum_range'] = max(self.sum_distribution.items(), key=lambda x: x[1])[0] if self.sum_distribution else "Unknown"
            metrics['common_number_range'] = max(self.range_distribution.items(), key=lambda x: x[1])[0] if self.range_distribution else "Unknown"
        
        return metrics