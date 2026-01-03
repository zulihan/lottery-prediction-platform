import os
import pandas as pd
import time
import json
import logging
import random
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, ForeignKey, Table, MetaData, inspect, UniqueConstraint, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.pool import QueuePool
from sqlalchemy import exc
from sqlalchemy.engine.url import URL

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Flag to track if database is available
DB_AVAILABLE = True

# Constants for exponential backoff
MIN_RETRY_DELAY = 0.5  # Starting delay of 0.5 seconds
MAX_RETRY_DELAY = 10   # Maximum delay of 10 seconds
BACKOFF_FACTOR = 2     # Multiply delay by this factor for each retry
JITTER = 0.1           # Add random jitter to avoid thundering herd

def create_db_engine(max_retries=5):
    """
    Create SQLAlchemy engine with improved connection pooling and retry logic
    
    Returns:
        tuple: (engine, is_available)
    """
    global DB_AVAILABLE
    
    retries = 0
    retry_delay = MIN_RETRY_DELAY
    last_error = None
    
    while retries < max_retries:
        try:
            # Create engine with improved connection pooling settings
            if DATABASE_URL:
                engine = create_engine(
                    DATABASE_URL,
                    isolation_level="AUTOCOMMIT",
                    pool_size=3,  # Reduced pool size to avoid rate limits
                    max_overflow=5,  # Reduced overflow connections
                    pool_timeout=30,
                    pool_recycle=1800,  # Recycle connections after 30 minutes
                    pool_pre_ping=True,  # Verify connections before using them
                    poolclass=QueuePool,
                    connect_args={'connect_timeout': 10}
                )
            else:
                logger.error("No DATABASE_URL provided")
                raise ValueError("DATABASE_URL environment variable is not set")
            
            # Test connection quickly
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                
            logger.info("Successfully connected to database")
            return engine, True
            
        except exc.OperationalError as e:
            last_error = e
            retries += 1
            
            # Check if this is a rate limit error
            if "rate limit" in str(e).lower() or "too many connections" in str(e).lower():
                logger.warning(f"Rate limit hit (attempt {retries}/{max_retries}). Waiting before retry...")
            else:
                logger.warning(f"Database connection error (attempt {retries}/{max_retries}): {str(e)}")
            
            # Only retry if we haven't hit the max retries
            if retries < max_retries:
                # Calculate jittered exponential backoff
                jitter_amount = random.uniform(-JITTER, JITTER) * retry_delay
                actual_delay = retry_delay + jitter_amount
                logger.info(f"Retrying in {actual_delay:.2f} seconds...")
                time.sleep(actual_delay)
                retry_delay = min(retry_delay * BACKOFF_FACTOR, MAX_RETRY_DELAY)
            
        except Exception as e:
            logger.error(f"Unexpected database error: {str(e)}")
            last_error = e
            break
    
    # If we got here, all retries failed or an unexpected error occurred
    logger.error(f"Failed to establish database connection after {retries} attempts: {str(last_error)}")
    
    # Create a SQLite in-memory fallback
    logger.warning("Creating SQLite in-memory database for offline mode")
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
    return engine, False

# Try to create the engine with retry logic
engine, DB_AVAILABLE = create_db_engine()

# Create a scoped session to manage connections properly
Session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))

def get_session(max_retries=3):
    """
    Get a database session with smart retry logic for connection issues
    
    Args:
        max_retries: Maximum number of retry attempts
        
    Returns:
        SQLAlchemy session
    """
    if not DB_AVAILABLE:
        logger.info("Database unavailable, using SQLite memory database")
        return Session()
    
    retries = 0
    retry_delay = MIN_RETRY_DELAY
    last_error = None
    
    while retries < max_retries:
        try:
            # Create a new session
            session = Session()
            # Test connection with a simple query
            session.execute(text("SELECT 1"))
            return session
            
        except exc.DBAPIError as e:
            last_error = e
            retries += 1
            
            # Check if this is a rate limit error
            if "rate limit" in str(e).lower() or "too many connections" in str(e).lower():
                logger.warning(f"Rate limit hit (attempt {retries}/{max_retries}). Waiting before retry...")
            else:
                logger.warning(f"Database session error (attempt {retries}/{max_retries}): {str(e)}")
            
            # Close the session if it was created
            if 'session' in locals():
                session.close()
            
            # Only retry if we haven't hit the max retries
            if retries < max_retries:
                # Calculate jittered exponential backoff
                jitter_amount = random.uniform(-JITTER, JITTER) * retry_delay
                actual_delay = retry_delay + jitter_amount
                logger.info(f"Retrying in {actual_delay:.2f} seconds...")
                time.sleep(actual_delay)
                retry_delay = min(retry_delay * BACKOFF_FACTOR, MAX_RETRY_DELAY)
            
    # If we got here, all retries failed
    logger.error(f"Failed to establish database session after {max_retries} attempts: {str(last_error)}")
    # Return a session anyway - let the caller handle any exceptions
    return Session()

def get_db_connection(max_retries=3):
    """
    Get a direct database connection from engine with retry logic
    
    Args:
        max_retries: Maximum number of retry attempts
        
    Returns:
        SQLAlchemy connection or None if unavailable
    """
    if not DB_AVAILABLE:
        logger.error("Database not available")
        return None
    
    retries = 0
    retry_delay = MIN_RETRY_DELAY
    last_error = None
    
    while retries < max_retries:
        try:
            conn = engine.connect()
            # Test connection
            conn.execute(text("SELECT 1"))
            return conn
            
        except Exception as e:
            last_error = e
            retries += 1
            
            # Check if this is a rate limit error
            if "rate limit" in str(e).lower() or "too many connections" in str(e).lower():
                logger.warning(f"Rate limit hit (attempt {retries}/{max_retries}). Waiting before retry...")
            else:
                logger.warning(f"Database connection error (attempt {retries}/{max_retries}): {str(e)}")
            
            # Close the connection if it was created
            if 'conn' in locals():
                conn.close()
                
            # Only retry if we haven't hit the max retries
            if retries < max_retries:
                # Calculate jittered exponential backoff
                jitter_amount = random.uniform(-JITTER, JITTER) * retry_delay
                actual_delay = retry_delay + jitter_amount
                logger.info(f"Retrying in {actual_delay:.2f} seconds...")
                time.sleep(actual_delay)
                retry_delay = min(retry_delay * BACKOFF_FACTOR, MAX_RETRY_DELAY)
    
    # If we got here, all retries failed
    logger.error(f"Failed to establish database connection after {max_retries} attempts: {str(last_error)}")
    return None

# Create Base class for declarative models
Base = declarative_base()

# Import model definitions from original database.py
from database import EuromillionsDrawing, GeneratedCombination, UserSavedCombination
from database import StrategyTestResult, FrenchLotoDrawing, FrenchLotoPrediction, FrenchLotoPlayedCombination

def init_db():
    """Initialize the database by creating all tables if they don't exist"""
    global DB_AVAILABLE
    try:
        # Attempt to create tables whether in online or offline mode
        Base.metadata.create_all(engine)
        if DB_AVAILABLE:
            print("Database initialized and tables created.")
        else:
            print("SQLite memory database initialized for offline mode.")
            logger.info("SQLite memory database initialized for offline mode.")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        logger.error(f"Error initializing database: {str(e)}")
        # Mark database as unavailable
        DB_AVAILABLE = False

def get_all_draws():
    """
    Get all Euromillions draws from the database
    
    Returns:
        list: List of EuromillionsDrawing objects
    """
    if not DB_AVAILABLE:
        logger.warning("Database unavailable for get_all_draws request, returning empty list")
        return []
    
    session = get_session()
    try:
        drawings = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date.desc()).all()
        return drawings
    except Exception as e:
        logger.error(f"Error fetching draws: {str(e)}")
        return []
    finally:
        session.close()

def get_all_french_loto_draws():
    """
    Get all French Loto draws from the database
    
    Returns:
        list: List of FrenchLotoDrawing objects
    """
    if not DB_AVAILABLE:
        logger.warning("Database unavailable for get_all_french_loto_draws request, returning empty list")
        return []
    
    session = get_session()
    try:
        drawings = session.query(FrenchLotoDrawing).order_by(FrenchLotoDrawing.date.desc()).all()
        return drawings
    except Exception as e:
        logger.error(f"Error fetching French Loto draws: {str(e)}")
        return []
    finally:
        session.close()

def save_generated_combination(numbers, stars, strategy=None, score=None, target_date=None):
    """
    Save a generated combination to the database
    
    Args:
        numbers: List of 5 numbers
        stars: List of 2 stars
        strategy: Strategy used to generate the combination
        score: Score of the combination
        target_date: Target draw date for this combination
        
    Returns:
        bool: True if successful
    """
    if not DB_AVAILABLE:
        logger.warning("Database unavailable for save_generated_combination request, skipping")
        return False
    
    session = get_session()
    try:
        # Convert numbers and stars to JSON strings
        numbers_json = json.dumps(numbers)
        stars_json = json.dumps(stars)
        
        # Create combination record
        combination = GeneratedCombination(
            created_at=datetime.now().date(),
            target_draw_date=target_date,
            numbers=numbers_json,
            stars=stars_json,
            strategy=strategy,
            score=score
        )
        
        # Add to database
        session.add(combination)
        session.commit()
        return True
    except Exception as e:
        logger.error(f"Error saving combination: {str(e)}")
        session.rollback()
        return False
    finally:
        session.close()

def save_french_loto_prediction(numbers, lucky, strategy=None, score=None):
    """
    Save a French Loto prediction to the database
    
    Args:
        numbers: List of 5 numbers
        lucky: Lucky number
        strategy: Strategy used
        score: Prediction score
        
    Returns:
        bool: True if successful
    """
    if not DB_AVAILABLE:
        logger.warning("Database unavailable for save_french_loto_prediction request, skipping")
        return False
    
    session = get_session()
    try:
        # Convert numbers to dash-separated string
        numbers_str = "-".join(str(n) for n in sorted(numbers))
        
        # Create prediction record
        prediction = FrenchLotoPrediction(
            date_generated=datetime.now().date(),
            numbers=numbers_str,
            lucky=lucky,
            strategy=strategy,
            score=score
        )
        
        # Add to database
        session.add(prediction)
        session.commit()
        return True
    except Exception as e:
        logger.error(f"Error saving French Loto prediction: {str(e)}")
        session.rollback()
        return False
    finally:
        session.close()

# Initialize database on import
init_db()