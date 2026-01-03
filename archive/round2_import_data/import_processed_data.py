#!/usr/bin/env python3
"""
Import processed Euromillions data from CSV into the database.
"""

import pandas as pd
import logging
from database import init_db, load_drawings_from_dataframe, get_all_drawings
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def import_csv_to_database(csv_file):
    """
    Import data from a processed CSV file to the database.
    
    Args:
        csv_file: Path to the CSV file
        
    Returns:
        int: Number of records inserted
    """
    logger.info(f"Reading data from {csv_file}")
    
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} rows from CSV")
        
        # Check for required columns
        required_columns = ['date', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Required column '{col}' not found in CSV")
        
        # Convert the date column to datetime format
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        # Initialize the database
        logger.info("Initializing database...")
        init_db()
        
        # Get existing drawings to prevent duplicates
        logger.info("Fetching existing drawings...")
        try:
            existing_df = get_all_drawings()
            logger.info(f"Found {len(existing_df)} existing drawings")
            
            # Convert existing dates to the same format for comparison
            existing_df['date'] = pd.to_datetime(existing_df['date']).dt.date
            
            # Find dates in the new data that already exist in the database
            existing_dates = set(existing_df['date'].tolist())
            new_df = df[~df['date'].isin(existing_dates)]
            logger.info(f"{len(df) - len(new_df)} duplicate records will be skipped")
            
            # If all records already exist, exit
            if len(new_df) == 0:
                logger.info("No new records to insert")
                return 0
            
            # Import only new records
            record_count = load_drawings_from_dataframe(new_df)
            logger.info(f"Successfully inserted {record_count} new records")
            return record_count
            
        except Exception as e:
            logger.warning(f"Could not check for duplicates: {str(e)}. Will try to insert all records.")
            
            # Fall back to inserting all records
            record_count = load_drawings_from_dataframe(df)
            logger.info(f"Inserted {record_count} records")
            return record_count
            
    except Exception as e:
        logger.error(f"Error importing data: {str(e)}")
        raise

def main():
    """Main function"""
    try:
        # Import combined data
        csv_file = "processed_data/euromillions_combined.csv"
        record_count = import_csv_to_database(csv_file)
        logger.info(f"Total records imported: {record_count}")
        
        # Verify the data was imported
        try:
            drawings = get_all_drawings()
            logger.info(f"Total drawings in database: {len(drawings)}")
            logger.info(f"Date range: {drawings['date'].min()} to {drawings['date'].max()}")
        except Exception as e:
            logger.error(f"Could not verify import: {str(e)}")
        
    except Exception as e:
        logger.error(f"Import failed: {str(e)}")

if __name__ == "__main__":
    main()