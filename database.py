import os
import pandas as pd
import time
import json
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, ForeignKey, Table, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.pool import QueuePool
from sqlalchemy import exc

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine with improved connection pooling
engine = create_engine(
    DATABASE_URL,
    isolation_level="AUTOCOMMIT",
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_pre_ping=True,  # Verify connections before using them
    poolclass=QueuePool
)

# Create a scoped session to manage connections properly
Session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))

# Function to get a fresh session with retry logic
def get_session(max_retries=3, retry_delay=1):
    """Get a database session with retry logic for connection issues"""
    retries = 0
    last_error = None
    
    while retries < max_retries:
        try:
            # Create a new session
            session = Session()
            # Test connection with a simple query using text() to properly declare SQL
            from sqlalchemy import text
            session.execute(text("SELECT 1"))
            return session
        except exc.DBAPIError as e:
            last_error = e
            logger.warning(f"Database connection error (attempt {retries+1}/{max_retries}): {str(e)}")
            # Close the session if it was created
            if 'session' in locals():
                session.close()
            # Wait before retrying
            time.sleep(retry_delay)
            retries += 1
            
    # If we got here, all retries failed
    logger.error(f"Failed to establish database connection after {max_retries} attempts: {str(last_error)}")
    # Return a session anyway - let the caller handle any exceptions
    return Session()

# Create Base class for declarative models
Base = declarative_base()

class EuromillionsDrawing(Base):
    """Table for storing Euromillions drawing history"""
    __tablename__ = 'euromillions_drawings'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=True)
    day_of_week = Column(String(20))
    n1 = Column(Integer, nullable=False)
    n2 = Column(Integer, nullable=False)
    n3 = Column(Integer, nullable=False)
    n4 = Column(Integer, nullable=False)
    n5 = Column(Integer, nullable=False)
    s1 = Column(Integer, nullable=False)
    s2 = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<EuromillionsDrawing(date='{self.date}', numbers=[{self.n1},{self.n2},{self.n3},{self.n4},{self.n5}], stars=[{self.s1},{self.s2}])>"
    
    def to_dict(self):
        """Convert drawing to dictionary format"""
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'day_of_week': self.day_of_week,
            'n1': self.n1,
            'n2': self.n2,
            'n3': self.n3,
            'n4': self.n4,
            'n5': self.n5,
            's1': self.s1,
            's2': self.s2
        }

class GeneratedCombination(Base):
    """Table for storing user-generated combinations"""
    __tablename__ = 'generated_combinations'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(Date, default=datetime.now().date())
    numbers = Column(String(50), nullable=False)  # Stored as JSON string
    stars = Column(String(20), nullable=False)    # Stored as JSON string
    strategy = Column(String(100))
    score = Column(Float)
    
    def __repr__(self):
        return f"<GeneratedCombination(strategy='{self.strategy}', numbers={self.numbers}, stars={self.stars}, score={self.score})>"
    
    def to_dict(self):
        """Convert combination to dictionary format"""
        return {
            'id': self.id,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'numbers': json.loads(self.numbers),
            'stars': json.loads(self.stars),
            'strategy': self.strategy,
            'score': self.score
        }

class UserSavedCombination(Base):
    """Table for storing user-saved combinations with notes"""
    __tablename__ = 'user_saved_combinations'
    
    id = Column(Integer, primary_key=True)
    saved_at = Column(Date, default=datetime.now().date())
    numbers = Column(String(50), nullable=False)  # Stored as JSON string
    stars = Column(String(20), nullable=False)    # Stored as JSON string
    strategy = Column(String(100))
    notes = Column(String(500))
    played = Column(Boolean, default=False)
    result = Column(String(50))  # What was the result if played

class StrategyTestResult(Base):
    """Table for storing A/B test results for strategy comparison"""
    __tablename__ = 'strategy_test_results'
    
    id = Column(Integer, primary_key=True)
    test_date = Column(Date, nullable=False)
    strategies_tested = Column(String(500), nullable=False)  # Comma-separated list of tested strategies
    iterations = Column(Integer, nullable=False)
    num_combinations = Column(Integer, nullable=False)
    results = Column(String(10000), nullable=False)  # JSON string with detailed results
    
    def __repr__(self):
        return f"<StrategyTestResult(id='{self.id}', test_date='{self.test_date}', strategies='{self.strategies_tested}')>"
    
    def to_dict(self):
        """Convert test result to dictionary format"""
        return {
            'id': self.id,
            'test_date': self.test_date.strftime('%Y-%m-%d'),
            'strategies_tested': self.strategies_tested.split(','),
            'iterations': self.iterations,
            'num_combinations': self.num_combinations,
            'results': json.loads(self.results)
        }

def init_db():
    """Initialize the database by creating all tables if they don't exist"""
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    print("Database initialized and tables created.")

def load_drawings_from_dataframe(df):
    """
    Load Euromillions drawings from a DataFrame into the database
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing Euromillions drawing data
    
    Returns:
    --------
    int
        Number of records inserted
    """
    # Get a fresh session
    session = get_session()
    count = 0
    
    try:
        # Convert DataFrame to list of dictionaries
        drawings = []
        for _, row in df.iterrows():
            # Convert date string to date object if it's a string
            if isinstance(row['date'], str):
                date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            else:
                date = row['date']
                
            # Check if this drawing already exists
            existing = session.query(EuromillionsDrawing).filter_by(date=date).first()
            if existing:
                continue
                
            # Create new drawing record
            drawing = EuromillionsDrawing(
                date=date,
                day_of_week=row.get('day_of_week', ''),
                n1=int(row['n1']),
                n2=int(row['n2']),
                n3=int(row['n3']),
                n4=int(row['n4']),
                n5=int(row['n5']),
                s1=int(row['s1']),
                s2=int(row['s2'])
            )
            drawings.append(drawing)
        
        # Add all drawings to the database
        if drawings:
            session.add_all(drawings)
            session.commit()
            count = len(drawings)
        
    except Exception as e:
        logger.error(f"Error loading drawings: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()
    
    return count

def get_all_draws(max_retries=3):
    """
    Alias for get_all_drawings() for compatibility with strategy testing module
    """
    return get_all_drawings(max_retries)
    
def get_all_drawings(max_retries=3):
    """
    Get all Euromillions drawings from the database with retry logic
    
    Parameters:
    -----------
    max_retries : int
        Maximum number of retry attempts
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing all drawing records
    """
    for attempt in range(max_retries):
        session = get_session()
        try:
            drawings = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date.desc()).all()
            if not drawings:
                return pd.DataFrame()
                
            # Convert to list of dictionaries
            records = [drawing.to_dict() for drawing in drawings]
            return pd.DataFrame(records)
        except exc.OperationalError as e:
            # Handle specific database operational errors
            logger.warning(f"Database operational error (attempt {attempt+1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                # Wait before retrying (exponential backoff)
                retry_delay = 2 ** attempt
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Create a fresh engine and session factory if needed
                if "SSL connection has been closed" in str(e):
                    logger.info("Resetting database connection pool")
                    Session.remove()  # Close all sessions
            else:
                logger.error(f"Failed to retrieve drawings after {max_retries} attempts")
                # Return empty DataFrame as a fallback
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error retrieving drawings: {str(e)}")
            return pd.DataFrame()
        finally:
            session.close()

def add_new_drawing(date, numbers, stars, day_of_week=None):
    """
    Add a new Euromillions drawing to the database
    
    Parameters:
    -----------
    date : datetime.date or str
        Date of the drawing
    numbers : list
        List of 5 main numbers
    stars : list
        List of 2 star numbers
    day_of_week : str, optional
        Day of the week
        
    Returns:
    --------
    bool
        True if the drawing was added successfully
    """
    session = get_session()
    success = False
    
    try:
        # Convert date string to date object if it's a string
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()
            
        # Check if this drawing already exists
        existing = session.query(EuromillionsDrawing).filter_by(date=date).first()
        if existing:
            return False
            
        # Create new drawing record
        drawing = EuromillionsDrawing(
            date=date,
            day_of_week=day_of_week,
            n1=numbers[0],
            n2=numbers[1],
            n3=numbers[2],
            n4=numbers[3],
            n5=numbers[4],
            s1=stars[0],
            s2=stars[1]
        )
        
        # Add to the database
        session.add(drawing)
        session.commit()
        success = True
        
    except Exception as e:
        logger.error(f"Error adding new drawing: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()
        
    return success

def save_generated_combination(numbers, stars, strategy, score):
    """
    Save a generated combination to the database
    
    Parameters:
    -----------
    numbers : list
        List of 5 main numbers
    stars : list
        List of 2 star numbers
    strategy : str
        Strategy used to generate the combination
    score : float or numpy.float64
        Score or confidence value
        
    Returns:
    --------
    int
        ID of the saved combination
    """
    session = get_session()
    combo_id = None
    
    try:
        # Convert NumPy values to native Python types for database compatibility
        # Convert numbers and stars to standard Python lists
        numbers = [int(n) for n in numbers]
        stars = [int(s) for s in stars]
        
        # Convert score to a standard Python float if it's a NumPy type
        if hasattr(score, 'item'):  # Check if it's a NumPy scalar
            score = float(score)
        
        # Convert lists to JSON strings
        numbers_json = json.dumps(numbers)
        stars_json = json.dumps(stars)
        
        # Create new combination record
        combination = GeneratedCombination(
            numbers=numbers_json,
            stars=stars_json,
            strategy=strategy,
            score=score,
            created_at=datetime.now().date()
        )
        
        # Add to the database
        session.add(combination)
        session.commit()
        combo_id = combination.id
        
    except Exception as e:
        logger.error(f"Error saving generated combination: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()
        
    return combo_id

def get_generated_combinations(strategy=None, limit=100, max_retries=3):
    """
    Get generated combinations from the database with retry logic
    
    Parameters:
    -----------
    strategy : str, optional
        Filter by strategy
    limit : int, optional
        Maximum number of combinations to return
    max_retries : int
        Maximum number of retry attempts
        
    Returns:
    --------
    list
        List of dictionaries containing combination data
    """
    for attempt in range(max_retries):
        session = get_session()
        result = []
        
        try:
            query = session.query(GeneratedCombination)
            
            if strategy:
                query = query.filter_by(strategy=strategy)
                
            combinations = query.order_by(GeneratedCombination.created_at.desc()).limit(limit).all()
            result = [combination.to_dict() for combination in combinations]
            return result
            
        except exc.OperationalError as e:
            # Handle specific database operational errors
            logger.warning(f"Database operational error (attempt {attempt+1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                # Wait before retrying (exponential backoff)
                retry_delay = 2 ** attempt
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Create a fresh engine and session factory if needed
                if "SSL connection has been closed" in str(e):
                    logger.info("Resetting database connection pool")
                    Session.remove()  # Close all sessions
            else:
                logger.error(f"Failed to retrieve generated combinations after {max_retries} attempts")
                # Return empty list as a fallback
                return []
        except Exception as e:
            logger.error(f"Error retrieving generated combinations: {str(e)}")
            return []
        finally:
            session.close()
            
    return result

def save_user_combination(numbers, stars, strategy=None, notes=None):
    """
    Save a user-selected combination
    
    Parameters:
    -----------
    numbers : list
        List of 5 main numbers
    stars : list
        List of 2 star numbers
    strategy : str, optional
        Strategy that generated this combination
    notes : str, optional
        User notes
        
    Returns:
    --------
    int
        ID of the saved combination
    """
    session = get_session()
    saved_id = None
    
    try:
        # Convert NumPy values to native Python types for database compatibility
        # Convert numbers and stars to standard Python lists
        numbers = [int(n) for n in numbers]
        stars = [int(s) for s in stars]
        
        # Convert lists to JSON strings
        numbers_json = json.dumps(numbers)
        stars_json = json.dumps(stars)
        
        # Create new saved combination record
        saved = UserSavedCombination(
            numbers=numbers_json,
            stars=stars_json,
            strategy=strategy,
            notes=notes,
            saved_at=datetime.now().date()
        )
        
        # Add to the database
        session.add(saved)
        session.commit()
        saved_id = saved.id
        
    except Exception as e:
        logger.error(f"Error saving user combination: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()
        
    return saved_id

def get_user_saved_combinations(limit=50, max_retries=3):
    """
    Get user-saved combinations from the database with retry logic
    
    Parameters:
    -----------
    limit : int, optional
        Maximum number of combinations to return
    max_retries : int
        Maximum number of retry attempts
        
    Returns:
    --------
    list
        List of dictionaries containing saved combination data
    """
    for attempt in range(max_retries):
        session = get_session()
        result = []
        
        try:
            saved = session.query(UserSavedCombination).order_by(UserSavedCombination.saved_at.desc()).limit(limit).all()
            result = [combo.to_dict() for combo in saved]
            return result
        except exc.OperationalError as e:
            # Handle specific database operational errors
            logger.warning(f"Database operational error (attempt {attempt+1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                # Wait before retrying (exponential backoff)
                retry_delay = 2 ** attempt
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Create a fresh engine and session factory if needed
                if "SSL connection has been closed" in str(e):
                    logger.info("Resetting database connection pool")
                    Session.remove()  # Close all sessions
            else:
                logger.error(f"Failed to retrieve saved combinations after {max_retries} attempts")
                # Return empty list as a fallback
                return []
        except Exception as e:
            logger.error(f"Error retrieving saved combinations: {str(e)}")
            return []
        finally:
            session.close()
            
    return result

def update_user_combination(id, played=None, result=None, notes=None):
    """
    Update a user-saved combination
    
    Parameters:
    -----------
    id : int
        ID of the combination to update
    played : bool, optional
        Whether the combination was played
    result : str, optional
        Result if played (e.g., "Won €10", "No win")
    notes : str, optional
        Updated user notes
        
    Returns:
    --------
    bool
        True if the combination was updated successfully
    """
    session = get_session()
    success = False
    
    try:
        saved = session.query(UserSavedCombination).filter_by(id=id).first()
        if not saved:
            return False
        
        if played is not None:
            saved.played = played
        if result is not None:
            saved.result = result
        if notes is not None:
            saved.notes = notes
        
        session.commit()
        success = True
        
    except Exception as e:
        logger.error(f"Error updating user combination: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()
        
    return success

def save_strategy_test_results(test_date, strategies_tested, iterations, num_combinations, results):
    """
    Save A/B test results to the database
    
    Parameters:
    -----------
    test_date : datetime.datetime
        Date of the test
    strategies_tested : str
        Comma-separated list of tested strategies
    iterations : int
        Number of test iterations
    num_combinations : int
        Number of combinations generated per strategy
    results : str
        JSON string with detailed test results
        
    Returns:
    --------
    int
        ID of the saved test result
    """
    session = get_session()
    test_id = None
    
    try:
        # Convert date to date object if it's a datetime
        if isinstance(test_date, datetime):
            test_date = test_date.date()
            
        # Create new test result record
        test_result = StrategyTestResult(
            test_date=test_date,
            strategies_tested=strategies_tested,
            iterations=iterations,
            num_combinations=num_combinations,
            results=results
        )
        
        # Add to the database
        session.add(test_result)
        session.commit()
        test_id = test_result.id
        
    except Exception as e:
        logger.error(f"Error saving strategy test results: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()
        
    return test_id

def get_strategy_test_results(limit=10, max_retries=3):
    """
    Get strategy test results from the database with retry logic
    
    Parameters:
    -----------
    limit : int, optional
        Maximum number of test results to return
    max_retries : int
        Maximum number of retry attempts
        
    Returns:
    --------
    list
        List of dictionaries containing test result data
    """
    for attempt in range(max_retries):
        session = get_session()
        result = []
        
        try:
            test_results = session.query(StrategyTestResult).order_by(StrategyTestResult.test_date.desc()).limit(limit).all()
            result = [test.to_dict() for test in test_results]
            return result
        except exc.OperationalError as e:
            # Handle specific database operational errors
            logger.warning(f"Database operational error (attempt {attempt+1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                # Wait before retrying (exponential backoff)
                retry_delay = 2 ** attempt
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Create a fresh engine and session factory if needed
                if "SSL connection has been closed" in str(e):
                    logger.info("Resetting database connection pool")
                    Session.remove()  # Close all sessions
            else:
                logger.error(f"Failed to retrieve test results after {max_retries} attempts")
                # Return empty list as a fallback
                return []
        except Exception as e:
            logger.error(f"Error retrieving test results: {str(e)}")
            return []
        finally:
            session.close()
            
    return result

# Initialize the database if this module is run directly
if __name__ == "__main__":
    init_db()