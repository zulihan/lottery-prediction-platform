"""
Script to analyze French Loto historical data and identify patterns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import text
import database
import logging
import os
from datetime import date, timedelta, datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FrenchLotoStatistics:
    """
    Class for analyzing French Loto data and generating statistics
    """
    
    def __init__(self, data):
        """
        Initialize with French Loto data
        
        Args:
            data: pandas DataFrame containing French Loto data
        """
        self.data = data
        self.process_data()
        self.analyze_frequencies()
        self.hot_cold_numbers = self.get_hot_cold_numbers()
        self.pair_analysis = self.analyze_number_pairs()
        
    def process_data(self):
        """Process the data to ensure it's in the right format"""
        # Ensure date is in datetime format
        if 'date' in self.data.columns:
            self.data['date'] = pd.to_datetime(self.data['date'])
            
        # Rename columns if needed to standard format
        column_mapping = {
            'number1': 'n1',
            'number2': 'n2',
            'number3': 'n3',
            'number4': 'n4',
            'number5': 'n5',
            'lucky_number': 'lucky'
        }
        
        # Rename only if the columns exist
        for old_col, new_col in column_mapping.items():
            if old_col in self.data.columns and new_col not in self.data.columns:
                self.data.rename(columns={old_col: new_col}, inplace=True)
    
    def analyze_frequencies(self):
        """
        Analyze frequency of numbers in French Loto
        """
        if self.data is None or len(self.data) == 0:
            logger.error("No data available for frequency analysis")
            return
        
        # Create dictionaries to store frequencies
        self.main_number_freq = {}
        self.lucky_number_freq = {}
        
        # Get column names for main numbers
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        if 'n1' not in self.data.columns and 'number1' in self.data.columns:
            main_cols = ['number1', 'number2', 'number3', 'number4', 'number5']
        
        # Get column name for lucky number
        lucky_col = 'lucky' if 'lucky' in self.data.columns else 'lucky_number'
        
        # Count frequency of main numbers (1-49)
        main_numbers = []
        for col in main_cols:
            main_numbers.extend(self.data[col].tolist())
        
        for i in range(1, 50):
            self.main_number_freq[i] = main_numbers.count(i)
        
        # Count frequency of lucky numbers (1-10)
        lucky_numbers = self.data[lucky_col].tolist()
        for i in range(1, 11):
            self.lucky_number_freq[i] = lucky_numbers.count(i)
        
        # Sort dictionaries by frequency (descending)
        self.main_number_freq = dict(sorted(self.main_number_freq.items(), 
                                            key=lambda x: x[1], 
                                            reverse=True))
        self.lucky_number_freq = dict(sorted(self.lucky_number_freq.items(), 
                                             key=lambda x: x[1], 
                                             reverse=True))
    
    def get_hot_cold_numbers(self, period_days=365):
        """
        Identify hot and cold numbers based on recent drawings
        
        Args:
            period_days: Number of days to consider as 'recent'
            
        Returns:
            dict: Hot and cold numbers
        """
        if self.data is None or len(self.data) == 0:
            logger.error("No data available for hot/cold analysis")
            return {
                'hot_numbers': [],
                'cold_numbers': [],
                'hot_lucky': [],
                'cold_lucky': []
            }
        
        # Ensure date is datetime
        self.data['date'] = pd.to_datetime(self.data['date'])
        
        # Get latest date in dataset
        latest_date = self.data['date'].max()
        
        # Define recent period
        cutoff_date = latest_date - pd.Timedelta(days=period_days)
        
        # Split into recent and older data
        recent_data = self.data[self.data['date'] >= cutoff_date]
        
        # If recent data is very small, use more data
        if len(recent_data) < 10:
            # Use at least 20% of total data as recent
            min_recent_size = max(10, int(len(self.data) * 0.2))
            recent_data = self.data.sort_values('date', ascending=False).head(min_recent_size)
            cutoff_date = recent_data['date'].min()
        
        # Get column names for main numbers
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        if 'n1' not in self.data.columns and 'number1' in self.data.columns:
            main_cols = ['number1', 'number2', 'number3', 'number4', 'number5']
        
        # Get column name for lucky number
        lucky_col = 'lucky' if 'lucky' in self.data.columns else 'lucky_number'
        
        # Analyze recent frequency
        recent_main_numbers = []
        for col in main_cols:
            recent_main_numbers.extend(recent_data[col].tolist())
        
        recent_main_freq = {}
        for i in range(1, 50):
            recent_main_freq[i] = recent_main_numbers.count(i)
        
        recent_lucky_numbers = recent_data[lucky_col].tolist()
        recent_lucky_freq = {}
        for i in range(1, 11):
            recent_lucky_freq[i] = recent_lucky_numbers.count(i)
        
        # Identify hot numbers (above average frequency in recent period)
        avg_main_freq = sum(recent_main_freq.values()) / len(recent_main_freq)
        hot_numbers = [n for n, freq in recent_main_freq.items() 
                       if freq > avg_main_freq * 1.2]
        cold_numbers = [n for n, freq in recent_main_freq.items() 
                        if freq < avg_main_freq * 0.5]
        
        # Identify hot lucky numbers
        avg_lucky_freq = sum(recent_lucky_freq.values()) / len(recent_lucky_freq)
        hot_lucky = [n for n, freq in recent_lucky_freq.items() 
                     if freq > avg_lucky_freq * 1.2]
        cold_lucky = [n for n, freq in recent_lucky_freq.items() 
                      if freq < avg_lucky_freq * 0.5]
        
        return {
            'hot_numbers': sorted(hot_numbers),
            'cold_numbers': sorted(cold_numbers),
            'hot_lucky': sorted(hot_lucky),
            'cold_lucky': sorted(cold_lucky),
            'recent_period': f"{cutoff_date.date()} to {latest_date.date()}"
        }
    
    def analyze_number_pairs(self):
        """
        Analyze which pairs of numbers appear together most frequently
        
        Returns:
            dict: Top 20 number pairs by frequency
        """
        if self.data is None or len(self.data) == 0:
            logger.error("No data available for pair analysis")
            return {}
        
        # Get column names for main numbers
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        if 'n1' not in self.data.columns and 'number1' in self.data.columns:
            main_cols = ['number1', 'number2', 'number3', 'number4', 'number5']
        
        # Get all possible pairs from each drawing
        pairs = []
        
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in main_cols]
            for i in range(len(numbers)):
                for j in range(i+1, len(numbers)):
                    # Ensure pairs are ordered (smaller number first)
                    pair = tuple(sorted([numbers[i], numbers[j]]))
                    pairs.append(pair)
        
        # Count frequency of each pair
        pair_counts = {}
        for pair in pairs:
            pair_counts[pair] = pair_counts.get(pair, 0) + 1
        
        # Sort by frequency and get top 20
        top_pairs = dict(sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)[:20])
        
        return top_pairs
    
    def get_hot_numbers(self, count=10):
        """
        Get the most frequently drawn main numbers as a Series
        
        Args:
            count: Number of frequent numbers to return
            
        Returns:
            pandas.Series: Most frequent numbers with their frequencies
        """
        if not hasattr(self, 'main_number_freq'):
            self.analyze_frequencies()
            
        # Convert to pandas Series for easier display in the Streamlit app
        hot_numbers = pd.Series(
            {k: v for i, (k, v) in enumerate(self.main_number_freq.items()) if i < count}
        )
        
        return hot_numbers
            
    def get_most_frequent_numbers(self, count=5):
        """
        Get the most frequently drawn main numbers
        
        Args:
            count: Number of frequent numbers to return
            
        Returns:
            list: Most frequent numbers
        """
        if not hasattr(self, 'main_number_freq'):
            self.analyze_frequencies()
            
        return list(self.main_number_freq.keys())[:count]
    
    def get_most_frequent_lucky(self, count=2):
        """
        Get the most frequently drawn lucky numbers
        
        Args:
            count: Number of frequent lucky numbers to return
            
        Returns:
            list: Most frequent lucky numbers
        """
        if not hasattr(self, 'lucky_number_freq'):
            self.analyze_frequencies()
            
        return list(self.lucky_number_freq.keys())[:count]
    
    def get_least_frequent_numbers(self, count=5):
        """
        Get the least frequently drawn main numbers
        
        Args:
            count: Number of least frequent numbers to return
            
        Returns:
            list: Least frequent numbers
        """
        if not hasattr(self, 'main_number_freq'):
            self.analyze_frequencies()
            
        return list(self.main_number_freq.keys())[-count:]
    
    def get_least_frequent_lucky(self, count=2):
        """
        Get the least frequently drawn lucky numbers
        
        Args:
            count: Number of least frequent lucky numbers to return
            
        Returns:
            list: Least frequent lucky numbers
        """
        if not hasattr(self, 'lucky_number_freq'):
            self.analyze_frequencies()
            
        return list(self.lucky_number_freq.keys())[-count:]
        
    def get_hot_lucky_numbers(self, count=5):
        """
        Get the most frequently drawn lucky numbers as a Series
        
        Args:
            count: Number of frequent lucky numbers to return
            
        Returns:
            pandas.Series: Most frequent lucky numbers with their frequencies
        """
        if not hasattr(self, 'lucky_number_freq'):
            self.analyze_frequencies()
            
        # Convert to pandas Series for easier display in the Streamlit app
        hot_lucky = pd.Series(
            {k: v for i, (k, v) in enumerate(self.lucky_number_freq.items()) if i < count}
        )
        
        return hot_lucky
        
    def get_cold_numbers(self, count=10):
        """
        Get the least frequently drawn numbers as a Series
        
        Args:
            count: Number of cold numbers to return
            
        Returns:
            pandas.Series: Least frequent numbers with their frequencies
        """
        if not hasattr(self, 'main_number_freq'):
            self.analyze_frequencies()
        
        # Get the least frequent numbers
        cold_numbers_dict = dict(sorted(self.main_number_freq.items(), key=lambda x: x[1]))
        
        # Convert to pandas Series for easier display in the Streamlit app
        cold_numbers = pd.Series(
            {k: v for i, (k, v) in enumerate(cold_numbers_dict.items()) if i < count}
        )
        
        return cold_numbers
        
    def get_cold_lucky_numbers(self, count=5):
        """
        Get the least frequently drawn lucky numbers as a Series
        
        Args:
            count: Number of cold lucky numbers to return
            
        Returns:
            pandas.Series: Least frequent lucky numbers with their frequencies
        """
        if not hasattr(self, 'lucky_number_freq'):
            self.analyze_frequencies()
        
        # Get the least frequent lucky numbers
        cold_lucky_dict = dict(sorted(self.lucky_number_freq.items(), key=lambda x: x[1]))
        
        # Convert to pandas Series for easier display in the Streamlit app
        cold_lucky = pd.Series(
            {k: v for i, (k, v) in enumerate(cold_lucky_dict.items()) if i < count}
        )
        
        return cold_lucky
        
    def calculate_even_odd_distribution(self):
        """
        Calculate the distribution of even and odd numbers
        
        Returns:
            pandas.DataFrame: Distribution of even/odd combinations
        """
        if self.data is None or len(self.data) == 0:
            return pd.DataFrame()
            
        # Get column names for main numbers
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        if 'n1' not in self.data.columns and 'number1' in self.data.columns:
            main_cols = ['number1', 'number2', 'number3', 'number4', 'number5']
            
        # Create a dictionary to store counts of different even/odd combinations
        even_odd_dist = {
            '0 Even - 5 Odd': 0,
            '1 Even - 4 Odd': 0,
            '2 Even - 3 Odd': 0,
            '3 Even - 2 Odd': 0,
            '4 Even - 1 Odd': 0,
            '5 Even - 0 Odd': 0
        }
        
        # Count combinations
        for _, row in self.data.iterrows():
            even_count = sum(1 for col in main_cols if int(row[col]) % 2 == 0)
            odd_count = 5 - even_count
            key = f"{even_count} Even - {odd_count} Odd"
            even_odd_dist[key] += 1
            
        # Convert to DataFrame
        dist_df = pd.DataFrame({
            'Combination': list(even_odd_dist.keys()),
            'Count': list(even_odd_dist.values())
        })
        
        # Calculate percentage
        dist_df['Percentage'] = (dist_df['Count'] / len(self.data) * 100).round(2)
        
        return dist_df
        
    def calculate_sum_distribution(self):
        """
        Calculate the distribution of sum of drawn numbers
        
        Returns:
            pandas.DataFrame: Sum distribution grouped into ranges
        """
        if self.data is None or len(self.data) == 0:
            return pd.DataFrame()
            
        # Get column names for main numbers
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        if 'n1' not in self.data.columns and 'number1' in self.data.columns:
            main_cols = ['number1', 'number2', 'number3', 'number4', 'number5']
            
        # Calculate sum for each drawing
        self.data['sum'] = self.data[main_cols].sum(axis=1)
        
        # Create ranges for grouping
        ranges = [
            (0, 90), (91, 100), (101, 110), (111, 120), 
            (121, 130), (131, 140), (141, 150), (151, 160), 
            (161, 170), (171, 180), (181, 245)
        ]
        
        # Create bins and labels
        bins = [r[0] for r in ranges] + [ranges[-1][1] + 1]
        labels = [f"{r[0]}-{r[1]}" for r in ranges]
        
        # Group by range
        self.data['sum_range'] = pd.cut(self.data['sum'], bins=bins, labels=labels, right=False)
        sum_dist = self.data['sum_range'].value_counts().sort_index()
        
        # Convert to DataFrame
        dist_df = pd.DataFrame({
            'Range': sum_dist.index,
            'Count': sum_dist.values
        })
        
        # Calculate percentage
        dist_df['Percentage'] = (dist_df['Count'] / len(self.data) * 100).round(2)
        
        return dist_df
        
    def calculate_range_distribution(self):
        """
        Calculate the distribution of numbers across different ranges
        
        Returns:
            pandas.DataFrame: Distribution of numbers across ranges
        """
        if self.data is None or len(self.data) == 0:
            return pd.DataFrame()
            
        # Get column names for main numbers
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        if 'n1' not in self.data.columns and 'number1' in self.data.columns:
            main_cols = ['number1', 'number2', 'number3', 'number4', 'number5']
            
        # Define ranges
        ranges = [
            (1, 9), (10, 19), (20, 29), (30, 39), (40, 49)
        ]
        
        # Initialize counters for each range
        range_counts = {f"{r[0]}-{r[1]}": 0 for r in ranges}
        
        # Count numbers in each range
        for _, row in self.data.iterrows():
            for col in main_cols:
                num = int(row[col])
                for r in ranges:
                    if r[0] <= num <= r[1]:
                        range_counts[f"{r[0]}-{r[1]}"] += 1
                        break
        
        # Convert to DataFrame
        dist_df = pd.DataFrame({
            'Range': list(range_counts.keys()),
            'Count': list(range_counts.values())
        })
        
        # Calculate percentage
        total_numbers = len(self.data) * 5  # Total numbers drawn
        dist_df['Percentage'] = (dist_df['Count'] / total_numbers * 100).round(2)
        
        return dist_df
    
    def generate_basic_statistics(self):
        """
        Generate a dictionary of basic statistics about the data
        
        Returns:
            dict: Statistics dictionary
        """
        stats = {
            'total_drawings': len(self.data),
            'date_range': {
                'earliest': min(self.data['date']).date().isoformat(),
                'latest': max(self.data['date']).date().isoformat(),
            },
            'most_frequent_numbers': self.get_most_frequent_numbers(10),
            'most_frequent_lucky': self.get_most_frequent_lucky(5),
            'hot_cold': self.hot_cold_numbers,
            'top_pairs': list(self.pair_analysis.keys())[:5]
        }
        
        return stats

def get_french_loto_data():
    """
    Get all French Loto data from the database
    
    Returns:
        pandas.DataFrame: DataFrame containing all French Loto drawings
    """
    conn = database.get_db_connection()
    
    if conn is None:
        logger.error("Could not connect to database")
        return None
    
    try:
        # Query all French Loto drawings
        query = """
            SELECT 
                date, 
                number1, number2, number3, number4, number5,
                lucky_number,
                draw_num
            FROM french_loto_drawings
            ORDER BY date DESC, draw_num DESC
        """
        
        # Load data into DataFrame
        df = pd.read_sql(query, conn)
        logger.info(f"Retrieved {len(df)} French Loto drawings from database")
        
        return df
    
    except Exception as e:
        logger.error(f"Error retrieving French Loto data: {e}")
        return None
    
    finally:
        conn.close()

def analyze_number_frequency(df):
    """
    Analyze the frequency of each number in the French Loto
    
    Args:
        df: DataFrame containing French Loto data
        
    Returns:
        tuple: (main_numbers_freq, lucky_numbers_freq)
    """
    if df is None or len(df) == 0:
        logger.error("No data available for analysis")
        return None, None
    
    # Create a list of all main numbers drawn
    main_numbers = []
    for col in ['number1', 'number2', 'number3', 'number4', 'number5']:
        main_numbers.extend(df[col].tolist())
    
    # Count frequency of main numbers (1-49)
    main_numbers_freq = {i: main_numbers.count(i) for i in range(1, 50)}
    
    # Count frequency of lucky numbers (1-10)
    lucky_numbers = df['lucky_number'].tolist()
    lucky_numbers_freq = {i: lucky_numbers.count(i) for i in range(1, 11)}
    
    # Sort by frequency
    main_numbers_freq = dict(sorted(main_numbers_freq.items(), key=lambda x: x[1], reverse=True))
    lucky_numbers_freq = dict(sorted(lucky_numbers_freq.items(), key=lambda x: x[1], reverse=True))
    
    return main_numbers_freq, lucky_numbers_freq

def analyze_temporal_patterns(df):
    """
    Analyze temporal patterns in French Loto data
    
    Args:
        df: DataFrame containing French Loto data
        
    Returns:
        dict: Dictionary of temporal pattern analyses
    """
    if df is None or len(df) == 0:
        logger.error("No data available for analysis")
        return None
    
    # Ensure date is in datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Add day of week
    df['day_of_week'] = df['date'].dt.day_name()
    
    # Analyze by day of week
    day_of_week_counts = df['day_of_week'].value_counts().to_dict()
    
    # Analyze by month
    df['month'] = df['date'].dt.month
    month_counts = df['month'].value_counts().to_dict()
    
    # Analyze by year
    df['year'] = df['date'].dt.year
    year_counts = df['year'].value_counts().to_dict()
    
    return {
        'day_of_week': day_of_week_counts,
        'month': month_counts,
        'year': year_counts
    }

def analyze_number_pairs(df):
    """
    Analyze which pairs of numbers appear most frequently together
    
    Args:
        df: DataFrame containing French Loto data
        
    Returns:
        dict: Top 20 most frequent number pairs
    """
    if df is None or len(df) == 0:
        logger.error("No data available for analysis")
        return None
    
    # Get all possible pairs from each drawing
    pairs = []
    number_cols = ['number1', 'number2', 'number3', 'number4', 'number5']
    
    for _, row in df.iterrows():
        numbers = [row[col] for col in number_cols]
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                # Ensure pairs are ordered (smaller number first)
                pair = tuple(sorted([numbers[i], numbers[j]]))
                pairs.append(pair)
    
    # Count frequency of each pair
    pair_counts = {}
    for pair in pairs:
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    
    # Sort by frequency and get top 20
    top_pairs = dict(sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)[:20])
    
    return top_pairs

def analyze_hot_cold_numbers(df, period_days=365, as_of_date=None):
    """
    Analyze hot (frequently drawn) and cold (rarely drawn) numbers
    in a recent time period
    
    Args:
        df: DataFrame containing French Loto data
        period_days: Number of days to consider for recent drawings
        as_of_date: Date to consider as reference point (default: latest date in dataset)
        
    Returns:
        dict: Hot and cold numbers analysis
    """
    if df is None or len(df) == 0:
        logger.error("No data available for analysis")
        return None
    
    # Ensure date is in datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Determine reference date
    if as_of_date is None:
        as_of_date = df['date'].max()
    else:
        as_of_date = pd.to_datetime(as_of_date)
    
    # Filter to recent drawings
    cutoff_date = as_of_date - pd.Timedelta(days=period_days)
    recent_df = df[df['date'] >= cutoff_date]
    
    # Get frequency for recent period
    recent_main_freq, recent_lucky_freq = analyze_number_frequency(recent_df)
    
    # Get frequency for all time
    all_main_freq, all_lucky_freq = analyze_number_frequency(df)
    
    # Determine hot numbers (higher frequency in recent period)
    hot_numbers = []
    cold_numbers = []
    
    if recent_main_freq and all_main_freq:
        # Calculate average frequency for recent period
        avg_recent_freq = sum(recent_main_freq.values()) / len(recent_main_freq)
        
        for num in range(1, 50):
            if recent_main_freq.get(num, 0) > avg_recent_freq * 1.25:
                hot_numbers.append(num)
            elif recent_main_freq.get(num, 0) < avg_recent_freq * 0.75:
                cold_numbers.append(num)
    
    # Determine hot and cold lucky numbers
    hot_lucky = []
    cold_lucky = []
    
    if recent_lucky_freq and all_lucky_freq:
        # Calculate average frequency for recent period
        avg_recent_lucky = sum(recent_lucky_freq.values()) / len(recent_lucky_freq)
        
        for num in range(1, 11):
            if recent_lucky_freq.get(num, 0) > avg_recent_lucky * 1.25:
                hot_lucky.append(num)
            elif recent_lucky_freq.get(num, 0) < avg_recent_lucky * 0.75:
                cold_lucky.append(num)
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'hot_lucky': hot_lucky,
        'cold_lucky': cold_lucky,
        'recent_period': f"{cutoff_date.date()} to {as_of_date.date()}"
    }

def analyze_number_positions(df):
    """
    Analyze which positions (1st to 5th) each number appears most frequently
    
    Args:
        df: DataFrame containing French Loto data
        
    Returns:
        dict: Position analysis for each number
    """
    if df is None or len(df) == 0:
        logger.error("No data available for analysis")
        return None
    
    positions = {}
    
    for num in range(1, 50):
        positions[num] = {
            'position1': len(df[df['number1'] == num]),
            'position2': len(df[df['number2'] == num]),
            'position3': len(df[df['number3'] == num]),
            'position4': len(df[df['number4'] == num]),
            'position5': len(df[df['number5'] == num]),
            'total': sum([
                len(df[df['number1'] == num]),
                len(df[df['number2'] == num]),
                len(df[df['number3'] == num]),
                len(df[df['number4'] == num]),
                len(df[df['number5'] == num])
            ])
        }
        
        # Calculate favorite position
        max_pos = max(positions[num].items(), key=lambda x: x[1] if x[0] != 'total' else 0)
        positions[num]['favorite_position'] = max_pos[0]
    
    return positions

def print_number_frequency(main_freq, lucky_freq):
    """
    Print number frequency analysis in a readable format
    
    Args:
        main_freq: Dictionary of main number frequencies
        lucky_freq: Dictionary of lucky number frequencies
    """
    print("\n=== FRENCH LOTO NUMBER FREQUENCY ANALYSIS ===")
    
    # Print top 10 most frequent main numbers
    print("\nTop 10 Most Frequent Main Numbers:")
    for i, (num, count) in enumerate(list(main_freq.items())[:10]):
        print(f"{i+1}. Number {num}: {count} occurrences")
    
    # Print top 5 most frequent lucky numbers
    print("\nMost Frequent Lucky Numbers:")
    for i, (num, count) in enumerate(list(lucky_freq.items())[:10]):
        print(f"{i+1}. Lucky Number {num}: {count} occurrences")
    
    # Print 5 least frequent main numbers
    print("\n5 Least Frequent Main Numbers:")
    for i, (num, count) in enumerate(list(main_freq.items())[-5:]):
        print(f"{i+1}. Number {num}: {count} occurrences")

def print_pair_analysis(pairs):
    """
    Print pair analysis in a readable format
    
    Args:
        pairs: Dictionary of number pair frequencies
    """
    print("\n=== MOST FREQUENT NUMBER PAIRS ===")
    for i, (pair, count) in enumerate(pairs.items()):
        print(f"{i+1}. Numbers {pair[0]} and {pair[1]}: {count} occurrences")

def print_hot_cold_analysis(hot_cold):
    """
    Print hot/cold analysis in a readable format
    
    Args:
        hot_cold: Dictionary of hot/cold analysis
    """
    print(f"\n=== HOT & COLD NUMBERS ANALYSIS ({hot_cold['recent_period']}) ===")
    
    print("\nHot Main Numbers (appearing more frequently recently):")
    print(', '.join(str(n) for n in hot_cold['hot_numbers']))
    
    print("\nCold Main Numbers (appearing less frequently recently):")
    print(', '.join(str(n) for n in hot_cold['cold_numbers']))
    
    print("\nHot Lucky Numbers:")
    print(', '.join(str(n) for n in hot_cold['hot_lucky']))
    
    print("\nCold Lucky Numbers:")
    print(', '.join(str(n) for n in hot_cold['cold_lucky']))

def generate_recommendations(main_freq, lucky_freq, hot_cold, pairs):
    """
    Generate lottery number recommendations based on analysis
    
    Args:
        main_freq: Dictionary of main number frequencies
        lucky_freq: Dictionary of lucky number frequencies
        hot_cold: Dictionary of hot/cold analysis
        pairs: Dictionary of number pair frequencies
        
    Returns:
        list: List of recommended number combinations
    """
    import random
    
    # Create list of all numbers with their weights based on frequency
    numbers = list(range(1, 50))
    weights = [main_freq.get(n, 0) for n in numbers]
    
    # Normalize weights
    if sum(weights) > 0:
        weights = [w/sum(weights) for w in weights]
    
    # Add some bias toward hot numbers
    for num in hot_cold['hot_numbers']:
        idx = numbers.index(num)
        weights[idx] *= 1.5
    
    # Create recommendations
    recommendations = []
    
    # Strategy 1: Frequency-based (higher weight to frequent numbers)
    freq_numbers = random.choices(numbers, weights=weights, k=5)
    freq_numbers = sorted(list(set(freq_numbers)))
    # If we didn't get 5 unique numbers, fill in the rest
    while len(freq_numbers) < 5:
        freq_numbers.append(random.choice([n for n in numbers if n not in freq_numbers]))
    freq_lucky = random.choices(range(1, 11), 
                              weights=[lucky_freq.get(n, 0) for n in range(1, 11)],
                              k=1)[0]
    
    recommendations.append({
        'strategy': 'Frequency-based',
        'main_numbers': sorted(freq_numbers),
        'lucky_number': freq_lucky
    })
    
    # Strategy 2: Hot-Cold Mix (3 hot, 2 cold)
    hot_cold_mix = []
    # Add 3 hot numbers if available, otherwise use high-frequency numbers
    if len(hot_cold['hot_numbers']) >= 3:
        hot_cold_mix.extend(random.sample(hot_cold['hot_numbers'], 3))
    else:
        # Use top frequency numbers to fill
        top_numbers = [n for n, _ in sorted(main_freq.items(), key=lambda x: x[1], reverse=True)]
        hot_cold_mix.extend(top_numbers[:3])
    
    # Add 2 cold numbers if available, otherwise use random
    if len(hot_cold['cold_numbers']) >= 2:
        hot_cold_mix.extend(random.sample(hot_cold['cold_numbers'], 2))
    else:
        # Use random numbers not already selected
        remaining = [n for n in numbers if n not in hot_cold_mix]
        hot_cold_mix.extend(random.sample(remaining, 2))
    
    # Select lucky number
    if hot_cold['hot_lucky']:
        lucky = random.choice(hot_cold['hot_lucky'])
    else:
        lucky = random.choices(range(1, 11), 
                             weights=[lucky_freq.get(n, 0) for n in range(1, 11)],
                             k=1)[0]
    
    recommendations.append({
        'strategy': 'Hot-Cold Mix',
        'main_numbers': sorted(hot_cold_mix),
        'lucky_number': lucky
    })
    
    # Strategy 3: Pair-based (include at least one frequent pair)
    pair_based = []
    if pairs:
        # Choose one of the frequent pairs
        chosen_pair = random.choice(list(pairs.keys()))
        pair_based.extend(chosen_pair)
        
        # Add 3 more unique random numbers with frequency weights
        remaining = [n for n in numbers if n not in pair_based]
        remaining_weights = [main_freq.get(n, 0) for n in remaining]
        if sum(remaining_weights) > 0:
            remaining_weights = [w/sum(remaining_weights) for w in remaining_weights]
        else:
            remaining_weights = None
            
        additional = random.choices(remaining, weights=remaining_weights, k=3)
        pair_based.extend(additional)
        
        # Ensure we have 5 unique numbers
        pair_based = sorted(list(set(pair_based)))
        while len(pair_based) < 5:
            pair_based.append(random.choice([n for n in numbers if n not in pair_based]))
    else:
        # Fallback if no pair data
        pair_based = random.sample(numbers, 5)
    
    # Choose lucky number with slight bias toward frequent ones
    lucky_numbers = list(range(1, 11))
    lucky_weights = [lucky_freq.get(n, 0) for n in lucky_numbers]
    lucky = random.choices(lucky_numbers, weights=lucky_weights, k=1)[0]
    
    recommendations.append({
        'strategy': 'Pair-based',
        'main_numbers': sorted(pair_based),
        'lucky_number': lucky
    })
    
    # Strategy 4: Balanced (mix of high and low numbers)
    low_range = list(range(1, 25))
    high_range = list(range(25, 50))
    
    # Select 2-3 from low range and 2-3 from high range
    low_count = random.choice([2, 3])
    high_count = 5 - low_count
    
    balanced_numbers = random.sample(low_range, low_count)
    balanced_numbers.extend(random.sample(high_range, high_count))
    
    # Choose lucky number
    lucky = random.choice(range(1, 11))
    
    recommendations.append({
        'strategy': 'Balanced Range',
        'main_numbers': sorted(balanced_numbers),
        'lucky_number': lucky
    })
    
    return recommendations

def print_recommendations(recommendations):
    """
    Print number recommendations in a readable format
    
    Args:
        recommendations: List of recommendation dictionaries
    """
    print("\n=== FRENCH LOTO NUMBER RECOMMENDATIONS ===")
    
    for i, rec in enumerate(recommendations):
        print(f"\nStrategy {i+1}: {rec['strategy']}")
        print(f"Main Numbers: {', '.join(str(n) for n in rec['main_numbers'])}")
        print(f"Lucky Number: {rec['lucky_number']}")

def main():
    """
    Main function to run the analysis
    """
    # Get data
    df = get_french_loto_data()
    
    if df is None or len(df) == 0:
        print("No data available for analysis. Please import French Loto data first.")
        return
    
    print(f"Analyzing {len(df)} French Loto drawings from {df['date'].min()} to {df['date'].max()}")
    
    # Analyze number frequency
    main_freq, lucky_freq = analyze_number_frequency(df)
    print_number_frequency(main_freq, lucky_freq)
    
    # Analyze number pairs
    pairs = analyze_number_pairs(df)
    print_pair_analysis(pairs)
    
    # Analyze hot and cold numbers (last 1 year)
    hot_cold = analyze_hot_cold_numbers(df, period_days=365)
    print_hot_cold_analysis(hot_cold)
    
    # Generate recommendations
    recommendations = generate_recommendations(main_freq, lucky_freq, hot_cold, pairs)
    print_recommendations(recommendations)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()