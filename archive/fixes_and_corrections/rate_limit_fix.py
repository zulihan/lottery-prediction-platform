"""
Script to test database connection and cache data to avoid rate limits
"""

import os
import pandas as pd
import time
import pickle
import logging
from sqlalchemy import create_engine, text
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache directory
CACHE_DIR = "temp_data"
os.makedirs(CACHE_DIR, exist_ok=True)

# Cache files
FRENCH_LOTO_CACHE = os.path.join(CACHE_DIR, "french_loto_cache.pkl")
EURO_CACHE = os.path.join(CACHE_DIR, "euro_cache.pkl")

def connect_with_backoff(max_attempts=3):
    """Try to connect to the database with exponential backoff"""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        logger.error("DATABASE_URL environment variable not set")
        return None
    
    for attempt in range(1, max_attempts + 1):
        try:
            # Create engine with minimal settings to avoid rate limits
            engine = create_engine(
                db_url,
                pool_size=1,
                max_overflow=0,
                pool_recycle=1800,
                pool_timeout=30,
                connect_args={"connect_timeout": 10}
            )
            
            # Test connection with a simple query
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info(f"✅ Successfully connected to database on attempt {attempt}")
            return engine
            
        except Exception as e:
            error_str = str(e).lower()
            
            if "rate limit" in error_str or "too many connections" in error_str:
                logger.warning(f"Database rate limit exceeded (attempt {attempt}/{max_attempts})")
            else:
                logger.error(f"Database error: {e}")
            
            if attempt < max_attempts:
                # Calculate backoff with jitter
                backoff_time = (2 ** (attempt - 1)) * 3  # 3s, 6s, 12s, etc.
                jitter = random.uniform(0, backoff_time / 2)
                wait_time = backoff_time + jitter
                
                logger.info(f"Waiting {wait_time:.1f} seconds before retry...")
                time.sleep(wait_time)
            else:
                logger.error("Failed to connect after all attempts")
    
    return None

def fetch_and_cache_french_loto():
    """Fetch French Loto data and cache it"""
    engine = connect_with_backoff()
    if not engine:
        logger.error("Could not connect to database to fetch French Loto data")
        return None
    
    try:
        logger.info("Fetching French Loto data...")
        
        # Use a simple query with limit to reduce data
        query = """
        SELECT date, day_of_week, n1, n2, n3, n4, n5, lucky
        FROM french_loto_drawings
        ORDER BY date DESC
        LIMIT 200
        """
        
        df = pd.read_sql_query(query, engine)
        
        # Convert date to datetime if it's a string
        if 'date' in df.columns and df['date'].dtype == 'object':
            df['date'] = pd.to_datetime(df['date'])
        
        logger.info(f"✅ Successfully fetched {len(df)} French Loto drawings")
        
        # Save to cache
        try:
            with open(FRENCH_LOTO_CACHE, 'wb') as f:
                pickle.dump(df, f)
            logger.info(f"✅ Saved French Loto data to cache: {FRENCH_LOTO_CACHE}")
        except Exception as e:
            logger.error(f"❌ Error saving cache: {e}")
        
        # Close engine to release connection
        engine.dispose()
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Error fetching French Loto data: {e}")
        
        if engine:
            engine.dispose()
        
        return None

def fetch_and_cache_euromillions():
    """Fetch Euromillions data and cache it"""
    # Wait a bit to avoid consecutive requests causing rate limits
    time.sleep(5)
    
    engine = connect_with_backoff()
    if not engine:
        logger.error("Could not connect to database to fetch Euromillions data")
        return None
    
    try:
        logger.info("Fetching Euromillions data...")
        
        # Use a simple query with limit to reduce data
        query = """
        SELECT date, day_of_week, n1, n2, n3, n4, n5, s1, s2
        FROM euromillions_drawings
        ORDER BY date DESC
        LIMIT 200
        """
        
        df = pd.read_sql_query(query, engine)
        
        # Convert date to datetime if it's a string
        if 'date' in df.columns and df['date'].dtype == 'object':
            df['date'] = pd.to_datetime(df['date'])
        
        logger.info(f"✅ Successfully fetched {len(df)} Euromillions drawings")
        
        # Save to cache
        try:
            with open(EURO_CACHE, 'wb') as f:
                pickle.dump(df, f)
            logger.info(f"✅ Saved Euromillions data to cache: {EURO_CACHE}")
        except Exception as e:
            logger.error(f"❌ Error saving cache: {e}")
        
        # Close engine to release connection
        engine.dispose()
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Error fetching Euromillions data: {e}")
        
        if engine:
            engine.dispose()
        
        return None

def load_cached_data(cache_path):
    """Load data from cache"""
    try:
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
            logger.info(f"✅ Loaded data from cache: {cache_path}")
            return data
        else:
            logger.warning(f"Cache file not found: {cache_path}")
            return None
    except Exception as e:
        logger.error(f"❌ Error loading cache: {e}")
        return None

def main():
    """Main function to fetch and cache data"""
    print("Testing database connection and caching data...")
    
    # First try to load from cache
    french_loto_df = load_cached_data(FRENCH_LOTO_CACHE)
    if french_loto_df is not None and not french_loto_df.empty:
        print(f"Loaded {len(french_loto_df)} French Loto drawings from cache")
    else:
        print("No cached French Loto data found, fetching from database...")
        french_loto_df = fetch_and_cache_french_loto()
        if french_loto_df is not None and not french_loto_df.empty:
            print(f"Fetched and cached {len(french_loto_df)} French Loto drawings")
        else:
            print("Failed to fetch French Loto data")
    
    # Print recent French Loto data
    if french_loto_df is not None and not french_loto_df.empty:
        print("\nRecent French Loto drawings:")
        pd.set_option('display.max_columns', None)
        print(french_loto_df.head(3))
    
    # Fetch Euromillions data
    euro_df = load_cached_data(EURO_CACHE)
    if euro_df is not None and not euro_df.empty:
        print(f"\nLoaded {len(euro_df)} Euromillions drawings from cache")
    else:
        print("\nNo cached Euromillions data found, fetching from database...")
        euro_df = fetch_and_cache_euromillions()
        if euro_df is not None and not euro_df.empty:
            print(f"Fetched and cached {len(euro_df)} Euromillions drawings")
        else:
            print("Failed to fetch Euromillions data")
    
    # Print recent Euromillions data
    if euro_df is not None and not euro_df.empty:
        print("\nRecent Euromillions drawings:")
        print(euro_df.head(3))

if __name__ == "__main__":
    main()