#!/usr/bin/env python3
"""
Script to clear all data from the database and reload from processed CSV files.
"""

import pandas as pd
import logging
import os
import sys
from sqlalchemy import text
from database import engine, Base, init_db, load_drawings_from_dataframe, get_all_drawings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clear_database():
    """
    Drop and recreate all tables in the database.
    """
    logger.info("Clearing database...")
    
    try:
        # Connect to the database
        with engine.connect() as connection:
            # Drop all tables - will cascade and remove all data
            logger.info("Dropping all tables...")
            Base.metadata.drop_all(engine)
            connection.execute(text("COMMIT"))
            
            # Recreate the tables
            logger.info("Recreating tables...")
            Base.metadata.create_all(engine)
            connection.execute(text("COMMIT"))
            
        logger.info("Database cleared successfully")
        return True
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        return False

def import_csv_file(csv_file):
    """
    Import data from a CSV file to the database.
    
    Args:
        csv_file: Path to the CSV file
        
    Returns:
        int: Number of records inserted
    """
    logger.info(f"Importing data from {csv_file}")
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} rows from {csv_file}")
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        # Import to database
        count = load_drawings_from_dataframe(df)
        logger.info(f"Imported {count} rows to database")
        return count
    except Exception as e:
        logger.error(f"Error importing {csv_file}: {str(e)}")
        return 0

def verify_import():
    """
    Verify data was imported correctly.
    """
    try:
        # Get all drawings
        drawings = get_all_drawings()
        logger.info(f"Total drawings in database: {len(drawings)}")
        logger.info(f"Date range: {drawings['date'].min()} to {drawings['date'].max()}")
        return True
    except Exception as e:
        logger.error(f"Error verifying import: {str(e)}")
        return False

def main():
    """
    Main function to clear database and reload data.
    """
    # Get confirmation from user
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        proceed = True
    else:
        response = input("This will delete ALL data in the database. Are you sure? (y/n): ")
        proceed = response.lower() in ('y', 'yes')
    
    if not proceed:
        logger.info("Operation cancelled")
        return
    
    # Clear the database
    if not clear_database():
        logger.error("Failed to clear database, aborting")
        return
    
    # Check if processed data directory exists
    if not os.path.exists("processed_data"):
        logger.error("Processed data directory not found")
        return
    
    # Import all CSV files in the processed data directory
    total_count = 0
    
    # First import the combined file if it exists
    combined_file = os.path.join("processed_data", "euromillions_combined.csv")
    if os.path.exists(combined_file):
        count = import_csv_file(combined_file)
        total_count += count
    else:
        # If no combined file, import individual processed files
        for filename in os.listdir("processed_data"):
            if filename.endswith("_processed.csv"):
                file_path = os.path.join("processed_data", filename)
                count = import_csv_file(file_path)
                total_count += count
    
    # Import any additional original CSV files if specified
    for arg in sys.argv[1:]:
        if arg != "--force" and os.path.exists(arg) and arg.endswith(".csv"):
            # Process the file first
            from process_french_csv import process_csv_file
            try:
                output_path = process_csv_file(arg)
                count = import_csv_file(output_path)
                total_count += count
            except Exception as e:
                logger.error(f"Failed to process and import {arg}: {str(e)}")
    
    logger.info(f"Total records imported: {total_count}")
    
    # Verify the import
    verify_import()

if __name__ == "__main__":
    main()