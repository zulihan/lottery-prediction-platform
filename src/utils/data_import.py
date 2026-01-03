"""
Enhanced Data Processor for Lottery Data Import

Handles multiple CSV formats with automatic format detection and robust parsing.
Supports various column naming conventions for dates, numbers, and stars.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Enhanced data processor for lottery data.

    Automatically detects CSV format and handles multiple column name variants.
    """

    def __init__(self, data):
        """
        Initialize the data processor with a pandas DataFrame.

        Parameters:
        -----------
        data : pandas.DataFrame
            The raw lottery data
        """
        self.raw_data = data
        self.processed_data = None
        self.format_info = None
        self.process_data()

    def process_data(self):
        """
        Process the raw data into a standardized format.

        Handles different CSV formats and ensures consistent column names and data types.
        """
        # Make a copy to avoid modifying the original data
        df = self.raw_data.copy()

        # Identify the data format based on column names
        self.format_info = self.identify_data_format(df)

        if self.format_info['format'] == "standard":
            self.process_standard_format(df)
        else:
            logger.warning("Unrecognized data format. Attempting custom processing...")
            self.process_custom_format(df)

    def identify_data_format(self, df):
        """
        Identify the format of the data based on column names.

        Checks for multiple column name variants to handle different CSV formats.

        Parameters:
        -----------
        df : pandas.DataFrame
            The data to analyze

        Returns:
        --------
        dict
            Format information including detected columns
        """
        # Define all known column name variants
        date_variants = ['date', 'draw_date', 'drawdate', 'date_of_draw', 'drawing_date']

        number_variants = [
            ['n1', 'n2', 'n3', 'n4', 'n5'],
            ['number1', 'number2', 'number3', 'number4', 'number5'],
            ['num1', 'num2', 'num3', 'num4', 'num5'],
            ['ball1', 'ball2', 'ball3', 'ball4', 'ball5'],
            ['numero_1', 'numero_2', 'numero_3', 'numero_4', 'numero_5']  # French variant
        ]

        star_variants = [
            ['s1', 's2'],
            ['star1', 'star2'],
            ['lucky_star1', 'lucky_star2'],
            ['ls1', 'ls2'],
            ['etoile_1', 'etoile_2']  # French variant
        ]

        # Check for date column
        date_col = None
        for variant in date_variants:
            # Case-insensitive search
            matching_cols = [col for col in df.columns if col.lower() == variant.lower()]
            if matching_cols:
                date_col = matching_cols[0]
                break

        # Check for number columns
        number_cols = None
        for variant in number_variants:
            # Case-insensitive search
            matching = []
            for v in variant:
                match = [col for col in df.columns if col.lower() == v.lower()]
                if match:
                    matching.append(match[0])
            if len(matching) == 5:
                number_cols = matching
                break

        # Check for star columns
        star_cols = None
        for variant in star_variants:
            matching = []
            for v in variant:
                match = [col for col in df.columns if col.lower() == v.lower()]
                if match:
                    matching.append(match[0])
            if len(matching) == 2:
                star_cols = matching
                break

        # Return identified columns or unknown format
        if date_col and number_cols and star_cols:
            logger.info(f"Detected standard format: date={date_col}, "
                       f"numbers={number_cols[:2]}..., stars={star_cols}")
            return {
                'format': 'standard',
                'date_col': date_col,
                'number_cols': number_cols,
                'star_cols': star_cols
            }
        elif date_col and number_cols:
            # French Loto format (no stars, has lucky_number)
            lucky_variants = ['lucky_number', 'numero_chance', 'chance', 'lucky']
            lucky_col = None
            for variant in lucky_variants:
                match = [col for col in df.columns if col.lower() == variant.lower()]
                if match:
                    lucky_col = match[0]
                    break

            if lucky_col:
                logger.info(f"Detected French Loto format: date={date_col}, "
                           f"numbers={number_cols[:2]}..., lucky={lucky_col}")
                return {
                    'format': 'french_loto',
                    'date_col': date_col,
                    'number_cols': number_cols,
                    'lucky_col': lucky_col
                }

        logger.warning(f"Unrecognized format. Columns: {list(df.columns)}")
        return {'format': 'unknown'}

    def process_standard_format(self, df):
        """
        Process data in standard Euromillions format with recognized column names.

        Parameters:
        -----------
        df : pandas.DataFrame
            The data to process
        """
        # Extract identified columns
        date_col = self.format_info['date_col']
        number_cols = self.format_info['number_cols']
        star_cols = self.format_info['star_cols']

        # Create standardized DataFrame
        processed = pd.DataFrame()

        # Process date - convert to datetime and then to date objects
        try:
            dates = pd.to_datetime(df[date_col], errors='coerce')
            processed['date'] = dates.apply(lambda x: x.date() if pd.notna(x) and hasattr(x, 'date') else x)
            processed['day_of_week'] = dates.dt.day_name()
        except Exception as e:
            logger.error(f"Error processing dates: {e}")
            processed['date'] = df[date_col]
            processed['day_of_week'] = None

        # Process numbers (rename to n1-n5)
        for i, col in enumerate(number_cols):
            try:
                processed[f'n{i+1}'] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
            except Exception as e:
                logger.error(f"Error processing number column {col}: {e}")
                processed[f'n{i+1}'] = df[col]

        # Process stars (rename to s1-s2)
        for i, col in enumerate(star_cols):
            try:
                processed[f's{i+1}'] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
            except Exception as e:
                logger.error(f"Error processing star column {col}: {e}")
                processed[f's{i+1}'] = df[col]

        # Sort by date descending (most recent first)
        processed = processed.sort_values('date', ascending=False).reset_index(drop=True)

        self.processed_data = processed
        logger.info(f"Processed {len(processed)} Euromillions records")

    def process_custom_format(self, df):
        """
        Process data in a custom or unrecognized format.

        Attempts to extract the required information based on column contents
        and position guessing.

        Parameters:
        -----------
        df : pandas.DataFrame
            The data to process
        """
        logger.warning("Attempting to process unrecognized format with best-guess approach")

        processed = pd.DataFrame()

        # Try to find date column by content analysis
        date_col = None
        for col in df.columns:
            try:
                # Attempt to parse as dates
                dates = pd.to_datetime(df[col], errors='coerce')
                # If more than 50% are valid dates, assume this is the date column
                if dates.notna().sum() / len(df) > 0.5:
                    date_col = col
                    processed['date'] = dates.apply(lambda x: x.date() if pd.notna(x) else None)
                    processed['day_of_week'] = dates.dt.day_name()
                    logger.info(f"Detected date column: {col}")
                    break
            except:
                continue

        if date_col is None:
            logger.warning("Could not detect date column. Using index as date.")
            processed['date'] = pd.date_range(start='2024-01-01', periods=len(df)).date
            processed['day_of_week'] = pd.date_range(start='2024-01-01', periods=len(df)).day_name()

        # Try to find numeric columns for numbers
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Remove date column if it was numeric
        if date_col and date_col in numeric_cols:
            numeric_cols.remove(date_col)

        # Assume first 5 numeric columns are the numbers
        if len(numeric_cols) >= 5:
            for i in range(5):
                processed[f'n{i+1}'] = df[numeric_cols[i]].astype('Int64')
            logger.info(f"Detected number columns: {numeric_cols[:5]}")

        # Assume next 2 numeric columns are stars (if they exist)
        if len(numeric_cols) >= 7:
            for i in range(2):
                processed[f's{i+1}'] = df[numeric_cols[5+i]].astype('Int64')
            logger.info(f"Detected star columns: {numeric_cols[5:7]}")
        else:
            # Generate dummy stars if not found
            logger.warning("Could not detect star columns. Using placeholder values.")
            processed['s1'] = 1
            processed['s2'] = 2

        # Sort by date
        processed = processed.sort_values('date', ascending=False).reset_index(drop=True)

        self.processed_data = processed
        logger.info(f"Processed {len(processed)} records using custom format detection")

    def get_processed_data(self):
        """
        Get the processed data.

        Returns:
        --------
        pandas.DataFrame
            The processed and standardized data
        """
        return self.processed_data


# Standalone utility functions for common use cases

def convert_french_date(date_str):
    """
    Convert French DD/MM/YYYY format to ISO YYYY-MM-DD.

    Parameters:
    -----------
    date_str : str
        Date in French format (DD/MM/YYYY)

    Returns:
    --------
    str
        Date in ISO format (YYYY-MM-DD)
    """
    try:
        day, month, year = date_str.strip().split('/')
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    except Exception as e:
        logger.error(f"Error converting French date '{date_str}': {e}")
        return date_str


# French day name mapping (for locale support)
DAY_MAPPING = {
    'LUNDI': 'Monday',
    'MARDI': 'Tuesday',
    'MERCREDI': 'Wednesday',
    'JEUDI': 'Thursday',
    'VENDREDI': 'Friday',
    'SAMEDI': 'Saturday',
    'DIMANCHE': 'Sunday'
}


def translate_french_day(french_day):
    """
    Translate French day name to English.

    Parameters:
    -----------
    french_day : str
        French day name (e.g., 'LUNDI')

    Returns:
    --------
    str
        English day name (e.g., 'Monday')
    """
    return DAY_MAPPING.get(french_day.upper(), french_day)


# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_data = pd.DataFrame({
        'draw_date': ['2024-01-01', '2024-01-04', '2024-01-08'],
        'number1': [1, 5, 10],
        'number2': [12, 15, 20],
        'number3': [23, 25, 30],
        'number4': [34, 35, 40],
        'number5': [45, 47, 49],
        'star1': [2, 3, 5],
        'star2': [8, 9, 11]
    })

    processor = DataProcessor(sample_data)
    print(processor.get_processed_data())
