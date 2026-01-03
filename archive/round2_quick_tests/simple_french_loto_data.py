"""
Simple script to fetch French Loto data from database with improved connection handling
"""

import pandas as pd
import os
import time
import logging
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_french_loto_data():
    """
    Fetch French Loto data with optimized connection handling
    to avoid rate limiting issues
    """
    # Get DB URL
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        logger.error("DATABASE_URL environment variable not set")
        return None
    
    try:
        # Create engine with minimal connection settings
        engine = create_engine(
            db_url,
            pool_size=1,
            max_overflow=0,
            pool_recycle=1800,
            connect_args={"connect_timeout": 10}
        )
        
        # Direct SQL query
        query = """
        SELECT 
            date, day_of_week, 
            n1, n2, n3, n4, n5, lucky
        FROM 
            french_loto_drawings
        ORDER BY 
            date DESC
        LIMIT 100
        """
        
        # Execute query directly to DataFrame
        df = pd.read_sql(query, engine)
        
        logger.info(f"Successfully loaded {len(df)} French Loto drawings")
        return df
        
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return None

def display_data(df):
    """Display the data in a formatted way"""
    if df is None or df.empty:
        print("No data available")
        return
    
    print(f"\nMost recent French Loto drawings ({len(df)} total):")
    print("-" * 80)
    
    for i, row in df.head(5).iterrows():
        date_str = row['date'].strftime('%Y-%m-%d') if hasattr(row['date'], 'strftime') else row['date']
        print(f"Date: {date_str} ({row['day_of_week']})")
        print(f"Numbers: {row['n1']}, {row['n2']}, {row['n3']}, {row['n4']}, {row['n5']} | Lucky: {row['lucky']}")
        print("-" * 80)

if __name__ == "__main__":
    print("Fetching French Loto data...")
    df = get_french_loto_data()
    
    if df is not None and not df.empty:
        print("✅ Successfully retrieved data!")
        display_data(df)
    else:
        print("❌ Failed to retrieve data")