"""
Standalone script to initialize the database for the Euromillions Prediction App.
This script ensures that all required tables are created in the database.
"""

import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import database module
from database import Base, engine, init_db, EuromillionsDrawing, GeneratedCombination, UserSavedCombination, StrategyTestResult

def main():
    """Initialize the database and create all tables."""
    logger.info("Starting database initialization...")
    
    # First try to connect to the database
    try:
        # Check if we can connect to the database
        from sqlalchemy import text
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {str(e)}")
        logger.info("Waiting 5 seconds before retry...")
        time.sleep(5)
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                logger.info("Database connection successful on retry")
        except Exception as e:
            logger.error(f"Still failed to connect to the database: {str(e)}")
            return False
    
    # Initialize the database (create tables)
    try:
        # Create tables explicitly one by one
        logger.info("Creating tables...")
        tables = [
            EuromillionsDrawing.__table__,
            GeneratedCombination.__table__,
            UserSavedCombination.__table__,
            StrategyTestResult.__table__
        ]
        
        Base.metadata.create_all(engine, tables=tables)
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        logger.info(f"Existing tables in database: {existing_tables}")
        
        required_tables = [
            'euromillions_drawings',
            'generated_combinations',
            'user_saved_combinations',
            'strategy_test_results'
        ]
        
        for table in required_tables:
            if table in existing_tables:
                logger.info(f"Table {table} exists")
            else:
                logger.error(f"Table {table} was not created!")
        
        logger.info("Database initialization completed")
        return True
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("Database initialization successful!")
    else:
        print("Database initialization failed. Check the logs for details.")