#!/usr/bin/env python3
"""
Process French Euromillions CSV files and save to a standardized CSV format
without requiring database access.
"""

import pandas as pd
import os
import re
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_french_date(date_str):
    """Convert date from French format DD/MM/YYYY to ISO format YYYY-MM-DD"""
    # Handle non-string inputs
    if not isinstance(date_str, str):
        date_str = str(date_str)
    
    # Check if this is already in ISO format
    if re.match(r'^\d{4}[/.-]\d{1,2}[/.-]\d{1,2}$', date_str):
        return date_str
    
    # Check for format YYYYMMDD (numeric date)
    if date_str.isdigit() and len(date_str) == 8:
        year = date_str[0:4]
        month = date_str[4:6]
        day = date_str[6:8]
        return f"{year}-{month}-{day}"
    
    # Handle French format with various delimiters (DD/MM/YYYY)
    match = re.match(r'^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$', date_str)
    if match:
        day, month, year = match.groups()
        # Handle 2-digit years
        if len(year) == 2:
            year = '20' + year
        # Return in ISO format
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    # Try to handle dates with French format (e.g., "20110506" as string)
    try:
        if len(date_str) == 8 and not date_str.isdigit():
            # Try to extract a date pattern
            year = date_str[4:8]
            month = date_str[2:4]
            day = date_str[0:2]
            if year.isdigit() and month.isdigit() and day.isdigit():
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    except:
        pass
    
    # If all else fails, log a warning and use a fallback
    logger.warning(f"Unknown date format: {date_str}, using today's date instead")
    return datetime.datetime.now().strftime("%Y-%m-%d")

def process_csv_file(file_path, output_dir='processed_data'):
    """Process a CSV file and save to a standardized format"""
    logger.info(f"Processing file: {file_path}")
    
    try:
        # Make sure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # First, try to detect the delimiter and read the header names
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            delimiter = ';' if ';' in first_line else ','
            
        # Read the CSV file with the detected delimiter
        df = pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8', on_bad_lines='skip')
        
        logger.info(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
        logger.info(f"Columns: {df.columns.tolist()}")
        
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
            
        # Process main ball numbers
        if 'boule_1' in df.columns:
            for i in range(1, 6):
                col_name = f'boule_{i}'
                if col_name in df.columns:
                    standardized_df[f'n{i}'] = df[col_name].astype(int)
        
        # Process star numbers
        if 'etoile_1' in df.columns:
            for i in range(1, 3):
                col_name = f'etoile_{i}'
                if col_name in df.columns:
                    standardized_df[f's{i}'] = df[col_name].astype(int)
        
        # Add source file metadata
        standardized_df['source_file'] = os.path.basename(file_path)
        
        # Make sure essential columns are present (fill with NaN if missing)
        essential_columns = ['date', 'day_of_week', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']
        for col in essential_columns:
            if col not in standardized_df.columns:
                standardized_df[col] = pd.NA
        
        # Sort by date
        standardized_df = standardized_df.sort_values('date', ascending=False)
        
        # Generate output file path
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_processed.csv")
        
        # Save to CSV
        standardized_df.to_csv(output_path, index=False)
        logger.info(f"Saved {len(standardized_df)} rows to {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")
        raise

def main(file_paths):
    """Process multiple CSV files"""
    processed_files = []
    
    for file_path in file_paths:
        try:
            output_path = process_csv_file(file_path)
            processed_files.append(output_path)
        except Exception as e:
            logger.error(f"Failed to process {file_path}: {str(e)}")
    
    # Print summary
    logger.info(f"Processed {len(processed_files)} out of {len(file_paths)} files")
    for file_path in processed_files:
        logger.info(f"  - {file_path}")
    
    # If we have multiple processed files, also create a combined file
    if len(processed_files) > 1:
        try:
            combined_df = pd.DataFrame()
            
            for file_path in processed_files:
                df = pd.read_csv(file_path)
                combined_df = pd.concat([combined_df, df])
                
            # Remove duplicates based on date and numbers
            combined_df = combined_df.drop_duplicates(subset=['date', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2'])
            
            # Sort by date
            combined_df = combined_df.sort_values('date', ascending=False)
            
            # Save combined file
            output_path = os.path.join('processed_data', 'euromillions_combined.csv')
            combined_df.to_csv(output_path, index=False)
            logger.info(f"Created combined file with {len(combined_df)} rows: {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating combined file: {str(e)}")
    
    return processed_files

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python process_french_csv.py file1.csv [file2.csv ...]")
        sys.exit(1)
        
    file_paths = sys.argv[1:]
    main(file_paths)