#!/usr/bin/env python3
"""
French CSV Converter for Euromillions data

This script converts French-format CSV files containing Euromillions draw data
to a standardized format that can be imported to our database.

The input files use semicolons as delimiters and have French column names.
"""

import pandas as pd
import numpy as np
import re
import os
import datetime
import logging
from database import init_db, load_drawings_from_dataframe

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_french_date(date_str):
    """
    Convert a date from French format (DD/MM/YYYY) to ISO format (YYYY-MM-DD)
    Also handles dates with dashes or other separators.
    
    Args:
        date_str: String date in French format
        
    Returns:
        String date in ISO format
    """
    # Handle non-string inputs
    if not isinstance(date_str, str):
        date_str = str(date_str)
    
    # Check if this is already in ISO format
    if re.match(r'^\d{4}[/.-]\d{1,2}[/.-]\d{1,2}$', date_str):
        return date_str
        
    # Extract components regardless of separator
    match = re.match(r'^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$', date_str)
    if match:
        day, month, year = match.groups()
        # Handle 2-digit years
        if len(year) == 2:
            year = '20' + year
        # Return in ISO format
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    else:
        # Try alternative formats with potential numeric date codes
        try:
            # If it's a numeric date code, try to interpret as YYYYMMDD
            if date_str.isdigit() and len(date_str) == 8:
                year = date_str[0:4]
                month = date_str[4:6]
                day = date_str[6:8]
                return f"{year}-{month}-{day}"
        except:
            pass
        
        # Return today's date as fallback
        logger.warning(f"Unknown date format: {date_str}, using today's date instead")
        return datetime.datetime.now().strftime("%Y-%m-%d")

def extract_numbers_from_string(s):
    """
    Extract numbers from a string like "-1-11-13-18-21-;-4-5-"
    
    Args:
        s: String containing numbers separated by dashes
        
    Returns:
        List of integers
    """
    if not isinstance(s, str) or not s:
        return []
    
    # Extract all numbers from the string
    numbers = re.findall(r'-(\d+)-', s)
    return [int(num) for num in numbers]

def process_french_csv(file_path, verbose=True):
    """
    Process a French-format CSV file containing Euromillions draw data.
    
    Args:
        file_path: Path to the CSV file
        verbose: Whether to print progress information
        
    Returns:
        DataFrame in standardized format
    """
    logger.info(f"Processing file: {file_path}")
    
    try:
        # First, try to detect the delimiter and read the header names
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            delimiter = ';' if ';' in first_line else ','
            
        # Read the CSV file with the detected delimiter
        df = pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8', on_bad_lines='skip')
        
        if verbose:
            logger.info(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
            logger.info(f"Columns: {df.columns.tolist()}")
            
        # Dictionary to map French column names to our standardized names
        column_mapping = {
            # Date column variations
            'date_de_tirage': 'date',
            # Main ball variations
            'boule_1': 'n1',
            'boule_2': 'n2',
            'boule_3': 'n3',
            'boule_4': 'n4',
            'boule_5': 'n5',
            # Star variations
            'etoile_1': 's1',
            'etoile_2': 's2',
            # Day of week
            'jour_de_tirage': 'day_of_week'
        }
        
        # Create a new DataFrame for standardized data
        standardized_df = pd.DataFrame()
        
        # Process the date
        if 'date_de_tirage' in df.columns:
            standardized_df['date'] = df['date_de_tirage'].apply(convert_french_date)
        else:
            # Try to find a date column
            for col in df.columns:
                if 'date' in col.lower():
                    standardized_df['date'] = df[col].apply(convert_french_date)
                    break
                    
        # Process day of week
        if 'jour_de_tirage' in df.columns:
            # Map abbreviated French day names to full English day names
            day_mapping = {
                'LU': 'Monday',
                'MA': 'Tuesday',
                'ME': 'Wednesday',
                'JE': 'Thursday',
                'VE': 'Friday',
                'SA': 'Saturday',
                'DI': 'Sunday',
                'LUNDI': 'Monday',
                'MARDI': 'Tuesday',
                'MERCREDI': 'Wednesday',
                'JEUDI': 'Thursday',
                'VENDREDI': 'Friday',
                'SAMEDI': 'Saturday',
                'DIMANCHE': 'Sunday'
            }
            standardized_df['day_of_week'] = df['jour_de_tirage'].apply(
                lambda x: day_mapping.get(str(x).strip().upper(), x) if x is not None else None
            )
            
        # Process numbers - either from individual columns or from combined strings
        if 'boule_1' in df.columns:
            # Direct number columns
            for i in range(1, 6):
                col_name = f'boule_{i}'
                if col_name in df.columns:
                    standardized_df[f'n{i}'] = df[col_name].astype(int)
                    
            # Star numbers
            for i in range(1, 3):
                col_name = f'etoile_{i}'
                if col_name in df.columns:
                    standardized_df[f's{i}'] = df[col_name].astype(int)
                    
        elif 'boules_gagnantes_en_ordre_croissant' in df.columns and 'etoiles_gagnantes_en_ordre_croissant' in df.columns:
            # Extract from combined strings
            numbers_list = df['boules_gagnantes_en_ordre_croissant'].apply(extract_numbers_from_string)
            stars_list = df['etoiles_gagnantes_en_ordre_croissant'].apply(extract_numbers_from_string)
            
            # Ensure we have 5 numbers and 2 stars
            for i in range(1, 6):
                standardized_df[f'n{i}'] = numbers_list.apply(lambda x: x[i-1] if len(x) >= i else np.nan)
                
            for i in range(1, 3):
                standardized_df[f's{i}'] = stars_list.apply(lambda x: x[i-1] if len(x) >= i else np.nan)
        
        # Add a metadata column to indicate the source file
        standardized_df['source_file'] = os.path.basename(file_path)
        
        # Drop rows with missing values in essential columns
        for col in ['n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']:
            if col not in standardized_df.columns:
                standardized_df[col] = np.nan
        
        # Drop any rows where any of the essential number columns are missing
        standardized_df = standardized_df.dropna(subset=['n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2'])
        
        # Make sure number columns are integers
        for col in ['n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']:
            standardized_df[col] = standardized_df[col].astype(int)
            
        # Sort by date (newest first)
        standardized_df = standardized_df.sort_values('date', ascending=False)
        
        if verbose:
            logger.info(f"Standardized data has {len(standardized_df)} rows")
            logger.info(f"Sample data:\n{standardized_df.head(2)}")
            
        return standardized_df
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")
        raise

def import_to_database(df):
    """
    Import a standardized DataFrame to the database.
    
    Args:
        df: DataFrame with standardized data
        
    Returns:
        Number of records inserted
    """
    # Initialize the database if needed
    init_db()
    
    # Import to database
    try:
        count = load_drawings_from_dataframe(df)
        logger.info(f"Successfully imported {count} records to database")
        return count
    except Exception as e:
        logger.error(f"Error importing to database: {str(e)}")
        raise

def main(file_paths):
    """
    Main function to process a list of files and import them to the database.
    
    Args:
        file_paths: List of paths to CSV files
        
    Returns:
        Total number of records inserted
    """
    total_count = 0
    
    for file_path in file_paths:
        try:
            # Process the file
            df = process_french_csv(file_path)
            
            # Import to database
            count = import_to_database(df)
            total_count += count
            
        except Exception as e:
            logger.error(f"Failed to process {file_path}: {str(e)}")
            
    return total_count

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python french_csv_converter.py file1.csv [file2.csv ...]")
        sys.exit(1)
        
    file_paths = sys.argv[1:]
    total_count = main(file_paths)
    
    print(f"Total records imported: {total_count}")