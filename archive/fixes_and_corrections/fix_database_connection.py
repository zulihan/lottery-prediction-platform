"""
Script to fix the database connection issue with rate limiting
"""

import os
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")

def test_connection():
    """Test the database connection with improved handling for rate limits"""
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable is not set")
        return False
    
    # Try to connect with rate limit awareness
    for attempt in range(1, 4):  # 3 attempts
        try:
            # Create a minimal engine with reduced connections
            engine = create_engine(
                DATABASE_URL,
                pool_size=1,
                max_overflow=0,
                pool_timeout=10,
                connect_args={'connect_timeout': 5}
            )
            
            # Simple query to test connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                row = result.fetchone()
                if row and row[0] == 1:
                    logger.info(f"Database connection successful on attempt {attempt}")
                    return True
        
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check for rate limit errors
            if "rate limit" in error_msg or "too many connections" in error_msg:
                logger.warning(f"Rate limit hit (attempt {attempt}/3). Waiting before retry...")
                # Exponential backoff
                wait_time = 3 * (2 ** (attempt - 1))  # 3, 6, 12 seconds
                logger.info(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                logger.error(f"Database connection error: {str(e)}")
                return False
    
    logger.error("Failed to connect to database after multiple attempts")
    return False

if __name__ == "__main__":
    print("Testing database connection...")
    if test_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed")