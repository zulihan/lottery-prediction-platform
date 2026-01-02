"""
Quick fix for database rate limiting
Modify this file to adjust connection parameters
"""

import os
import time
import random
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection parameters - adjust these to reduce rate limiting
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 5  # seconds
MAX_RETRY_DELAY = 30  # seconds

def get_french_loto_data():
    """
    Get French Loto data with rate limit handling
    Returns DataFrame with French Loto drawings
    """
    # Get database URL from environment
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        logger.error("DATABASE_URL not set")
        return pd.DataFrame()
    
    # Connection retry loop
    retry_count = 0
    retry_delay = INITIAL_RETRY_DELAY
    
    while retry_count < MAX_RETRIES:
        try:
            # Create minimal engine with limited connection pool
            engine = create_engine(
                db_url,
                pool_size=1,
                max_overflow=0,
                pool_recycle=3600,
                connect_args={"connect_timeout": 10}
            )
            
            # Execute query with minimal connection time
            query = """
            SELECT date, day_of_week, n1, n2, n3, n4, n5, lucky
            FROM french_loto_drawings
            ORDER BY date DESC
            """
            
            # Read directly into DataFrame to minimize connection time
            df = pd.read_sql_query(query, engine)
            
            # Convert date string to datetime if needed
            if 'date' in df.columns and df['date'].dtype == 'object':
                df['date'] = pd.to_datetime(df['date'])
            
            logger.info(f"Successfully loaded {len(df)} French Loto drawings")
            return df
            
        except Exception as e:
            retry_count += 1
            error_str = str(e).lower()
            
            if "rate limit" in error_str or "too many connections" in error_str:
                logger.warning(f"Database rate limit exceeded (attempt {retry_count}/{MAX_RETRIES})")
            else:
                logger.error(f"Database error: {str(e)}")
            
            if retry_count < MAX_RETRIES:
                # Add jitter to avoid thundering herd
                jitter = random.uniform(0, 2)
                wait_time = min(retry_delay + jitter, MAX_RETRY_DELAY)
                logger.info(f"Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                # Exponential backoff
                retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)
            else:
                logger.error("Max retries exceeded, returning empty DataFrame")
                return pd.DataFrame()
    
    return pd.DataFrame()

def get_euromillions_data():
    """
    Get Euromillions data with rate limit handling
    Returns DataFrame with Euromillions drawings
    """
    # Get database URL from environment
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        logger.error("DATABASE_URL not set")
        return pd.DataFrame()
    
    # Connection retry loop
    retry_count = 0
    retry_delay = INITIAL_RETRY_DELAY
    
    while retry_count < MAX_RETRIES:
        try:
            # Create minimal engine with limited connection pool
            engine = create_engine(
                db_url,
                pool_size=1,
                max_overflow=0,
                pool_recycle=3600,
                connect_args={"connect_timeout": 10}
            )
            
            # Execute query with minimal connection time
            query = """
            SELECT date, day_of_week, n1, n2, n3, n4, n5, s1, s2
            FROM euromillions_drawings
            ORDER BY date DESC
            """
            
            # Read directly into DataFrame to minimize connection time
            df = pd.read_sql_query(query, engine)
            
            # Convert date string to datetime if needed
            if 'date' in df.columns and df['date'].dtype == 'object':
                df['date'] = pd.to_datetime(df['date'])
            
            logger.info(f"Successfully loaded {len(df)} Euromillions drawings")
            return df
            
        except Exception as e:
            retry_count += 1
            error_str = str(e).lower()
            
            if "rate limit" in error_str or "too many connections" in error_str:
                logger.warning(f"Database rate limit exceeded (attempt {retry_count}/{MAX_RETRIES})")
            else:
                logger.error(f"Database error: {str(e)}")
            
            if retry_count < MAX_RETRIES:
                # Add jitter to avoid thundering herd
                jitter = random.uniform(0, 2)
                wait_time = min(retry_delay + jitter, MAX_RETRY_DELAY)
                logger.info(f"Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                # Exponential backoff
                retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)
            else:
                logger.error("Max retries exceeded, returning empty DataFrame")
                return pd.DataFrame()
    
    return pd.DataFrame()

# Test the functions if run directly
if __name__ == "__main__":
    print("Testing database connection...")
    
    # Try to get French Loto data
    loto_df = get_french_loto_data()
    if not loto_df.empty:
        print(f"✅ Successfully retrieved {len(loto_df)} French Loto drawings")
        print("Recent drawings:")
        pd.set_option('display.max_columns', None)
        print(loto_df.head(3))
    else:
        print("❌ Failed to retrieve French Loto data")
    
    # Wait before trying Euromillions to avoid rate limiting
    print("\nWaiting 10 seconds before Euromillions query...")
    time.sleep(10)
    
    # Try to get Euromillions data
    euro_df = get_euromillions_data()
    if not euro_df.empty:
        print(f"✅ Successfully retrieved {len(euro_df)} Euromillions drawings")
        print("Recent drawings:")
        print(euro_df.head(3))
    else:
        print("❌ Failed to retrieve Euromillions data")