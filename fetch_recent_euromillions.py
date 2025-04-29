#!/usr/bin/env python3
"""
Fetch recent Euromillions results using the National Lottery API
and update the database with the new data.
"""

import requests
import pandas as pd
import datetime
import logging
import json
import os
from database import init_db, EuromillionsDrawing, get_all_drawings
from sqlalchemy.orm import sessionmaker
from database import engine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a temporary directory for storing API responses
os.makedirs("temp_data", exist_ok=True)

def fetch_results_csv():
    """
    Directly download the historical Euromillions CSV data from the EU Lottery website.
    
    Returns:
        DataFrame: The parsed CSV data
    """
    try:
        # URL for the CSV file
        url = "https://media.national-lottery.co.uk/results/euromillions/draw-history/euromillions-draw-history.csv"
        
        # Download the CSV file
        logger.info(f"Downloading Euromillions data from {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        # Save the CSV to a temporary file
        temp_file = "temp_data/euromillions_history.csv"
        with open(temp_file, "wb") as f:
            f.write(response.content)
        
        # Parse the CSV
        df = pd.read_csv(temp_file)
        logger.info(f"Downloaded {len(df)} records")
        
        # Rename columns to match our schema
        column_mapping = {
            "DrawDate": "date",
            "Ball 1": "n1",
            "Ball 2": "n2",
            "Ball 3": "n3", 
            "Ball 4": "n4",
            "Ball 5": "n5",
            "Lucky Star 1": "s1",
            "Lucky Star 2": "s2",
            # Day of week not provided in this CSV
        }
        
        # Apply column mapping
        df = df.rename(columns=column_mapping)
        
        # Convert date format
        df["date"] = pd.to_datetime(df["date"])
        
        # Add day of week
        df["day_of_week"] = df["date"].dt.day_name()
        
        # Convert date to date object
        df["date"] = df["date"].dt.date
        
        # Sort by date (newest first)
        df = df.sort_values("date", ascending=False)
        
        return df
        
    except Exception as e:
        logger.error(f"Error fetching Euromillions data: {e}")
        return pd.DataFrame()

def add_to_database(df):
    """
    Add new results to the database.
    
    Args:
        df: DataFrame containing the results
        
    Returns:
        int: Number of records added
    """
    logger.info(f"Adding {len(df)} results to database...")
    
    # Initialize the database
    init_db()
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Get existing dates in the database
    try:
        existing_df = get_all_drawings()
        existing_dates = set(pd.to_datetime(existing_df['date']).dt.date.tolist())
        logger.info(f"Found {len(existing_dates)} existing dates in database")
    except Exception as e:
        logger.warning(f"Could not fetch existing dates: {e}")
        existing_dates = set()
    
    # Add new records
    count = 0
    for _, row in df.iterrows():
        try:
            # Skip if date already exists
            if row['date'] in existing_dates:
                continue
                
            # Create a new drawing
            drawing = EuromillionsDrawing(
                date=row['date'],
                day_of_week=row['day_of_week'],
                n1=int(row['n1']),
                n2=int(row['n2']),
                n3=int(row['n3']),
                n4=int(row['n4']),
                n5=int(row['n5']),
                s1=int(row['s1']),
                s2=int(row['s2'])
            )
            
            # Add to session
            session.add(drawing)
            count += 1
            
        except Exception as e:
            logger.error(f"Error adding record for {row['date']}: {e}")
            session.rollback()
            continue
    
    # Commit session
    try:
        session.commit()
        logger.info(f"Successfully added {count} new records")
    except Exception as e:
        logger.error(f"Error committing session: {e}")
        session.rollback()
        count = 0
        
    return count

def verify_database():
    """
    Verify the database has a complete set of data.
    """
    try:
        drawings = get_all_drawings()
        logger.info(f"Total drawings in database: {len(drawings)}")
        logger.info(f"Date range: {drawings['date'].min()} to {drawings['date'].max()}")
        
        # Calculate frequency
        drawings['date'] = pd.to_datetime(drawings['date'])
        drawings = drawings.sort_values('date')
        
        # Count drawings per year
        year_counts = drawings.groupby(drawings['date'].dt.year).size()
        logger.info("Drawings per year:")
        for year, count in year_counts.items():
            logger.info(f"  {year}: {count}")
            
        return len(drawings)
    except Exception as e:
        logger.error(f"Error verifying database: {e}")
        return 0

def main():
    """
    Main function to fetch results and add to database.
    """
    # Fetch results
    df = fetch_results_csv()
    
    # Check if any results were fetched
    if df.empty:
        logger.error("No results were fetched")
        return
        
    logger.info(f"Fetched {len(df)} results from {df['date'].min()} to {df['date'].max()}")
    
    # Add to database
    count = add_to_database(df)
    
    # Verify database
    total = verify_database()
    
    logger.info(f"Added {count} new records. Total records in database: {total}")

if __name__ == "__main__":
    main()