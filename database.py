import os
import pandas as pd
import time
import json
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, ForeignKey, Table, MetaData, inspect, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.pool import QueuePool
from sqlalchemy import exc

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Flag to track if database is available
DB_AVAILABLE = True

# Create SQLAlchemy engine with improved connection pooling
try:
    engine = create_engine(
        DATABASE_URL,
        isolation_level="AUTOCOMMIT",
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,  # Recycle connections after 30 minutes
        pool_pre_ping=True,  # Verify connections before using them
        poolclass=QueuePool,
        connect_args={'connect_timeout': 10}
    )
    # Test connection quickly
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("Successfully connected to database")
except Exception as e:
    logger.error(f"Database connection failed: {str(e)}")
    # Create a dummy engine for SQLAlchemy metadata
    import sqlite3
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
    DB_AVAILABLE = False
    
    # When using SQLite in-memory fallback, we need to create the tables
    # But we can't do this here yet because Base class is defined later in this file
    logger.warning("Running in offline mode with SQLite memory database")

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

def get_db_connection():
    """Get a direct database connection from engine"""
    if not DB_AVAILABLE:
        logger.error("Database not available")
        return None
    
    try:
        conn = engine.connect()
        # Test connection
        from sqlalchemy import text
        conn.execute(text("SELECT 1"))
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return None

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
    target_draw_date = Column(Date)  # Date of the draw this combination was generated for
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
            'target_draw_date': self.target_draw_date.strftime('%Y-%m-%d') if self.target_draw_date else None,
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
    played_date = Column(Date)  # The date this combination was played for
    
    def __repr__(self):
        return f"<UserSavedCombination(id='{self.id}', numbers='{self.numbers}', stars='{self.stars}')>"
    
    def to_dict(self):
        """Convert saved combination to dictionary format"""
        return {
            'id': self.id,
            'saved_at': self.saved_at.strftime('%Y-%m-%d') if self.saved_at else None,
            'played_date': self.played_date.strftime('%Y-%m-%d') if self.played_date else None,
            'numbers': json.loads(self.numbers),
            'stars': json.loads(self.stars),
            'strategy': self.strategy,
            'notes': self.notes,
            'played': self.played,
            'result': self.result
        }

class StrategyTestResult(Base):
    """Table for storing A/B test results for strategy comparison"""
    __tablename__ = 'strategy_test_results'
    
    id = Column(Integer, primary_key=True)
    test_date = Column(Date, nullable=False)
    strategies_tested = Column(String(500), nullable=False)  # Comma-separated list of tested strategies
    iterations = Column(Integer, nullable=False)
    num_combinations = Column(Integer, nullable=False)
    results = Column(String(50000), nullable=False)  # JSON string with detailed results
    
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

class FrenchLotoDrawing(Base):
    """Table for storing French Loto drawing history"""
    __tablename__ = 'french_loto_drawings'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    draw_num = Column(Integer, default=1)  # For days with multiple draws (1=first, 2=second)
    day_of_week = Column(String(20))
    n1 = Column(Integer, nullable=False)
    n2 = Column(Integer, nullable=False)
    n3 = Column(Integer, nullable=False)
    n4 = Column(Integer, nullable=False)
    n5 = Column(Integer, nullable=False)
    lucky = Column(Integer, nullable=False)
    
    # Winner information
    winners_rank1 = Column(Integer)
    winners_rank2 = Column(Integer)
    winners_rank3 = Column(Integer)
    winners_rank4 = Column(Integer)
    winners_rank5 = Column(Integer)
    winners_rank6 = Column(Integer)
    winners_rank7 = Column(Integer)
    
    # Prize amounts
    prize_rank1 = Column(Float)
    prize_rank2 = Column(Float)
    prize_rank3 = Column(Float)
    prize_rank4 = Column(Float)
    prize_rank5 = Column(Float)
    prize_rank6 = Column(Float)
    prize_rank7 = Column(Float)
    
    # Total jackpot amount
    total_amount = Column(Float)
    
    # Currency (FRF for French francs before 2002, EUR for euros after)
    currency = Column(String(10))
    
    # Add unique constraint for date + draw_num
    __table_args__ = (
        UniqueConstraint('date', 'draw_num', name='unique_french_loto_drawing'),
    )
    
    def __repr__(self):
        return f"<FrenchLotoDrawing(date='{self.date}', numbers=[{self.n1},{self.n2},{self.n3},{self.n4},{self.n5}], lucky={self.lucky})>"
    
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
            'lucky': self.lucky,
            'winners_rank1': self.winners_rank1,
            'winners_rank2': self.winners_rank2, 
            'winners_rank3': self.winners_rank3,
            'winners_rank4': self.winners_rank4,
            'winners_rank5': self.winners_rank5,
            'winners_rank6': self.winners_rank6,
            'winners_rank7': self.winners_rank7,
            'prize_rank1': self.prize_rank1,
            'prize_rank2': self.prize_rank2,
            'prize_rank3': self.prize_rank3,
            'prize_rank4': self.prize_rank4,
            'prize_rank5': self.prize_rank5,
            'prize_rank6': self.prize_rank6,
            'prize_rank7': self.prize_rank7,
            'total_amount': self.total_amount,
            'currency': self.currency
        }

class FrenchLotoPrediction(Base):
    """Table for storing French Loto generated predictions"""
    __tablename__ = 'french_loto_predictions'
    
    id = Column(Integer, primary_key=True)
    date_generated = Column(Date, default=datetime.now().date())
    numbers = Column(String(50), nullable=False)  # Stored as dash-separated string, e.g. "1-5-12-32-45"
    lucky = Column(Integer, nullable=False)
    strategy = Column(String(100))
    score = Column(Float)
    
    def __repr__(self):
        return f"<FrenchLotoPrediction(id='{self.id}', numbers='{self.numbers}', lucky={self.lucky}, strategy='{self.strategy}')>"
    
    def to_dict(self):
        """Convert prediction to dictionary format"""
        return {
            'id': self.id,
            'date_generated': self.date_generated.strftime('%Y-%m-%d'),
            'numbers': self.numbers,
            'lucky': self.lucky,
            'strategy': self.strategy,
            'score': self.score
        }

class FrenchLotoPlayedCombination(Base):
    """Table for storing French Loto combinations played by the user"""
    __tablename__ = 'french_loto_played_combinations'
    
    id = Column(Integer, primary_key=True)
    played_date = Column(Date, nullable=False)  # Date when the combination was played
    draw_date = Column(Date, nullable=False)  # Date of the draw for which it was played
    numbers = Column(String(50), nullable=False)  # Stored as dash-separated string
    lucky = Column(Integer, nullable=False)
    strategy = Column(String(100))
    notes = Column(String(500))
    result = Column(String(50))  # Result of the play (win/loss, amount, etc.)
    
    def __repr__(self):
        return f"<FrenchLotoPlayedCombination(id='{self.id}', draw_date='{self.draw_date}', numbers='{self.numbers}', lucky={self.lucky})>"
    
    def to_dict(self):
        """Convert played combination to dictionary format"""
        return {
            'id': self.id,
            'played_date': self.played_date.strftime('%Y-%m-%d'),
            'draw_date': self.draw_date.strftime('%Y-%m-%d'),
            'numbers': self.numbers,
            'lucky': self.lucky,
            'strategy': self.strategy,
            'notes': self.notes,
            'result': self.result
        }

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
    date : datetime.date, pandas.Timestamp, or str
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
        # Convert date to a consistent datetime.date object format
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()
        elif hasattr(date, 'date') and callable(getattr(date, 'date')):  # Handle pandas Timestamp
            date = date.date()
        elif not isinstance(date, type(datetime.now().date())):
            # If it's still not a date object, try to convert with str
            date = datetime.strptime(str(date), '%Y-%m-%d').date()
            
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

def save_generated_combination(numbers, stars, strategy, score, target_draw_date=None):
    """
    Save a generated combination to the database
    
    Parameters:
    -----------
    numbers : list
        List of 5 main numbers
    stars : list
        List of 2 or 3 star numbers
    strategy : str
        Strategy used to generate the combination
    score : float or numpy.float64
        Score or confidence value
    target_draw_date : datetime.date, str, or None
        The date of the draw this combination is generated for
        
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
        
        # Process target_draw_date if provided
        if target_draw_date:
            if isinstance(target_draw_date, str):
                target_draw_date = datetime.strptime(target_draw_date, '%Y-%m-%d').date()
            elif hasattr(target_draw_date, 'date') and callable(getattr(target_draw_date, 'date')):
                target_draw_date = target_draw_date.date()
        
        # Create new combination record
        combination = GeneratedCombination(
            numbers=numbers_json,
            stars=stars_json,
            strategy=strategy,
            score=score,
            created_at=datetime.now().date(),
            target_draw_date=target_draw_date
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
    logger.info(f"Attempting to get generated combinations, strategy={strategy}, limit={limit}")
    
    for attempt in range(max_retries):
        session = get_session()
        result = []
        
        try:
            query = session.query(GeneratedCombination)
            
            if strategy:
                query = query.filter_by(strategy=strategy)
                
            combinations = query.order_by(GeneratedCombination.created_at.desc()).limit(limit).all()
            logger.info(f"Found {len(combinations)} combinations for strategy={strategy}")
            
            result = []
            for combination in combinations:
                try:
                    # Manually ensure JSON parsing works
                    combo_dict = {
                        'id': combination.id,
                        'created_at': combination.created_at.strftime('%Y-%m-%d') if combination.created_at else None,
                        'target_draw_date': combination.target_draw_date.strftime('%Y-%m-%d') if combination.target_draw_date else None,
                        'strategy': combination.strategy,
                        'score': combination.score
                    }
                    
                    # Parse numbers and stars with explicit error handling
                    try:
                        combo_dict['numbers'] = json.loads(combination.numbers)
                    except json.JSONDecodeError as je:
                        logger.error(f"Error parsing numbers JSON: {str(je)}. Raw value: {combination.numbers}")
                        combo_dict['numbers'] = []
                    
                    try:
                        combo_dict['stars'] = json.loads(combination.stars)
                    except json.JSONDecodeError as je:
                        logger.error(f"Error parsing stars JSON: {str(je)}. Raw value: {combination.stars}")
                        combo_dict['stars'] = []
                    
                    result.append(combo_dict)
                except Exception as inner_e:
                    logger.error(f"Error processing combination {combination.id}: {str(inner_e)}")
            
            logger.info(f"Successfully converted {len(result)} combinations to dictionary format")
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
            logger.error(f"Unexpected error retrieving combinations: {str(e)}")
            if attempt < max_retries - 1:
                # Wait before retrying (exponential backoff)
                retry_delay = 2 ** attempt
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                # Return empty list as a fallback
                return []
        finally:
            session.close()
            
    # If all attempts failed, return an empty list
    return []

def save_user_combination(numbers, stars, strategy=None, notes=None, played_date=None):
    """
    Save a user-selected combination
    
    Parameters:
    -----------
    numbers : list
        List of 5 main numbers
    stars : list
        List of 2 or 3 star numbers
    strategy : str, optional
        Strategy that generated this combination
    notes : str, optional
        User notes
    played_date : datetime.date, str, or None
        The date this combination was/will be played for
        
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
        
        # Process played_date if provided
        if played_date:
            if isinstance(played_date, str):
                played_date = datetime.strptime(played_date, '%Y-%m-%d').date()
            elif hasattr(played_date, 'date') and callable(getattr(played_date, 'date')):
                played_date = played_date.date()
                
        # Create new saved combination record
        saved = UserSavedCombination(
            numbers=numbers_json,
            stars=stars_json,
            strategy=strategy,
            notes=notes,
            saved_at=datetime.now().date(),
            played_date=played_date
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
            
    # If all attempts failed, return an empty list
    return []

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
            
    # This line will only be reached if all retry attempts have failed
    return []

# French Loto Database Functions

def get_french_loto_drawings(max_retries=3):
    """
    Get all French Loto drawings from the database
    
    Parameters:
    -----------
    max_retries : int
        Maximum number of retry attempts
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing all drawings
    """
    for attempt in range(max_retries):
        session = get_session()
        try:
            drawings = session.query(FrenchLotoDrawing).order_by(FrenchLotoDrawing.date.desc()).all()
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
                logger.error(f"Failed to retrieve French Loto drawings after {max_retries} attempts")
                # Return empty DataFrame as a fallback
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error retrieving French Loto drawings: {str(e)}")
            return pd.DataFrame()
        finally:
            session.close()

def add_french_loto_drawing(date, numbers, lucky, day_of_week=None):
    """
    Add a new French Loto drawing to the database
    
    Parameters:
    -----------
    date : datetime.date, pandas.Timestamp, or str
        Date of the drawing
    numbers : list
        List of 5 main numbers
    lucky : int
        Lucky number
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
        # Convert date to a consistent datetime.date object format
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()
        elif hasattr(date, 'date') and callable(getattr(date, 'date')):  # Handle pandas Timestamp
            date = date.date()
        elif not isinstance(date, type(datetime.now().date())):
            # If it's still not a date object, try to convert with str
            date = datetime.strptime(str(date), '%Y-%m-%d').date()
            
        # Check if this drawing already exists
        existing = session.query(FrenchLotoDrawing).filter_by(date=date).first()
        if existing:
            logger.info(f"French Loto drawing for date {date} already exists, skipping")
            return False
            
        # Create new drawing record
        drawing = FrenchLotoDrawing(
            date=date,
            day_of_week=day_of_week,
            n1=numbers[0],
            n2=numbers[1],
            n3=numbers[2],
            n4=numbers[3],
            n5=numbers[4],
            lucky=lucky
        )
        
        # Add to the database
        session.add(drawing)
        session.commit()
        success = True
        logger.info(f"Added new French Loto drawing for date {date}")
        
    except Exception as e:
        logger.error(f"Error adding new French Loto drawing: {str(e)}")
        session.rollback()
    finally:
        session.close()
        
    return success
    
def add_french_loto_drawing_with_details(date, numbers, lucky, day_of_week=None, winners=None, prizes=None, total_amount=None, currency='EUR', draw_num=1):
    """
    Add a single French Loto drawing to the database with detailed winner and prize information
    
    Parameters:
    -----------
    date : datetime.date, pandas.Timestamp, or str
        The date of the drawing
    numbers : list
        List of 5 main numbers
    lucky : int
        The lucky number
    day_of_week : str, optional
        The day of the week for the drawing
    winners : dict, optional
        Dictionary of winners at each rank (rank1, rank2, etc.)
    prizes : dict, optional
        Dictionary of prize amounts at each rank (rank1, rank2, etc.)
    total_amount : float, optional
        Total prize pool amount
    currency : str, optional
        Currency of the prizes (EUR, FRF, etc.)
    draw_num : int, optional
        The draw number for this date (1=first draw, 2=second draw)
        
    Returns:
    --------
    bool
        True if the drawing was added successfully
    """
    session = get_session()
    success = False
    
    try:
        # Convert date to a consistent datetime.date object format
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()
        elif hasattr(date, 'date') and callable(getattr(date, 'date')):  # Handle pandas Timestamp
            date = date.date()
        elif not isinstance(date, type(datetime.now().date())):
            # If it's still not a date object, try to convert with str
            date = datetime.strptime(str(date), '%Y-%m-%d').date()
            
        # Convert draw_num to int if needed
        draw_num = int(draw_num)
            
        # Check if this drawing already exists for this date and draw number
        existing = session.query(FrenchLotoDrawing).filter_by(date=date, draw_num=draw_num).first()
        if existing:
            logger.info(f"French Loto drawing for date {date} draw {draw_num} already exists, updating with details")
            
            # Update existing drawing with more details
            if winners:
                existing.winners_rank1 = winners.get('rank1', 0)
                existing.winners_rank2 = winners.get('rank2', 0)
                existing.winners_rank3 = winners.get('rank3', 0)
                existing.winners_rank4 = winners.get('rank4', 0)
                existing.winners_rank5 = winners.get('rank5', 0)
                existing.winners_rank6 = winners.get('rank6', 0)
                existing.winners_rank7 = winners.get('rank7', 0)
            
            if prizes:
                existing.prize_rank1 = prizes.get('rank1', 0.0)
                existing.prize_rank2 = prizes.get('rank2', 0.0)
                existing.prize_rank3 = prizes.get('rank3', 0.0)
                existing.prize_rank4 = prizes.get('rank4', 0.0)
                existing.prize_rank5 = prizes.get('rank5', 0.0)
                existing.prize_rank6 = prizes.get('rank6', 0.0)
                existing.prize_rank7 = prizes.get('rank7', 0.0)
            
            if total_amount is not None:
                existing.total_amount = total_amount
                
            if currency:
                existing.currency = currency
                
            # Update draw info as well
            existing.n1 = numbers[0]
            existing.n2 = numbers[1]
            existing.n3 = numbers[2]
            existing.n4 = numbers[3]
            existing.n5 = numbers[4]
            existing.lucky = lucky
            
            if day_of_week:
                existing.day_of_week = day_of_week
                
            session.commit()
            success = True
        else:
            # Create new drawing with all details
            drawing = FrenchLotoDrawing(
                date=date,
                draw_num=draw_num,
                day_of_week=day_of_week,
                n1=numbers[0],
                n2=numbers[1],
                n3=numbers[2],
                n4=numbers[3],
                n5=numbers[4],
                lucky=lucky,
                winners_rank1=winners.get('rank1', 0) if winners else 0,
                winners_rank2=winners.get('rank2', 0) if winners else 0,
                winners_rank3=winners.get('rank3', 0) if winners else 0,
                winners_rank4=winners.get('rank4', 0) if winners else 0,
                winners_rank5=winners.get('rank5', 0) if winners else 0,
                winners_rank6=winners.get('rank6', 0) if winners else 0,
                winners_rank7=winners.get('rank7', 0) if winners else 0,
                prize_rank1=prizes.get('rank1', 0.0) if prizes else 0.0,
                prize_rank2=prizes.get('rank2', 0.0) if prizes else 0.0,
                prize_rank3=prizes.get('rank3', 0.0) if prizes else 0.0,
                prize_rank4=prizes.get('rank4', 0.0) if prizes else 0.0,
                prize_rank5=prizes.get('rank5', 0.0) if prizes else 0.0,
                prize_rank6=prizes.get('rank6', 0.0) if prizes else 0.0,
                prize_rank7=prizes.get('rank7', 0.0) if prizes else 0.0,
                total_amount=total_amount if total_amount is not None else 0.0,
                currency=currency
            )
            
            session.add(drawing)
            session.commit()
            success = True
            logger.info(f"Added French Loto drawing with details for {date}, draw {draw_num}")
    except Exception as e:
        logger.error(f"Error adding French Loto drawing with details: {str(e)}")
        session.rollback()
    finally:
        session.close()
        
    return success

def save_french_loto_prediction(numbers, lucky, strategy, score):
    """
    Save a French Loto prediction to the database
    
    Parameters:
    -----------
    numbers : list
        List of 5 main numbers
    lucky : int
        Lucky number
    strategy : str
        Strategy used to generate the combination
    score : float
        Confidence score (0-100)
        
    Returns:
    --------
    int
        ID of the saved prediction, or 0 if save failed
    """
    session = get_session()
    prediction_id = 0
    
    try:
        # Convert numbers to string format "1-5-12-32-45"
        if isinstance(numbers, list):
            numbers_str = "-".join(map(str, sorted(numbers)))
        else:
            numbers_str = numbers  # Assume it's already formatted
        
        # Create new prediction
        prediction = FrenchLotoPrediction(
            date_generated=datetime.now().date(),
            numbers=numbers_str,
            lucky=int(lucky),
            strategy=strategy,
            score=float(score)
        )
        
        # Add to database
        session.add(prediction)
        session.commit()
        prediction_id = prediction.id
        
    except Exception as e:
        logger.error(f"Error saving French Loto prediction: {str(e)}")
        session.rollback()
    finally:
        session.close()
        
    return prediction_id

def get_french_loto_predictions(limit=50):
    """
    Get French Loto predictions from the database
    
    Parameters:
    -----------
    limit : int
        Maximum number of predictions to retrieve
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing predictions
    """
    session = get_session()
    try:
        predictions = session.query(FrenchLotoPrediction).order_by(FrenchLotoPrediction.date_generated.desc()).limit(limit).all()
        if not predictions:
            return pd.DataFrame()
            
        # Convert to list of dictionaries
        records = [pred.to_dict() for pred in predictions]
        return pd.DataFrame(records)
        
    except Exception as e:
        logger.error(f"Error retrieving French Loto predictions: {str(e)}")
        return pd.DataFrame()
    finally:
        session.close()

def save_french_loto_played_combination(numbers, lucky, strategy, draw_date, notes=""):
    """
    Save a played French Loto combination
    
    Parameters:
    -----------
    numbers : list or str
        List of 5 main numbers or formatted string
    lucky : int
        Lucky number
    strategy : str
        Strategy used to generate the combination
    draw_date : datetime.date, pandas.Timestamp, or str
        Date of the draw this combination was played for
    notes : str, optional
        User notes about this combination
        
    Returns:
    --------
    int
        ID of the saved combination, or 0 if save failed
    """
    session = get_session()
    combo_id = 0
    
    try:
        # Process numbers
        if isinstance(numbers, list):
            numbers_str = "-".join(map(str, sorted(numbers)))
        else:
            numbers_str = numbers  # Assume already formatted
            
        # Process draw date
        if isinstance(draw_date, str):
            draw_date = datetime.strptime(draw_date, '%Y-%m-%d').date()
        elif hasattr(draw_date, 'date') and callable(getattr(draw_date, 'date')):
            draw_date = draw_date.date()
        
        # Create new record
        played = FrenchLotoPlayedCombination(
            played_date=datetime.now().date(),
            draw_date=draw_date,
            numbers=numbers_str,
            lucky=int(lucky),
            strategy=strategy,
            notes=notes
        )
        
        # Add to database
        session.add(played)
        session.commit()
        combo_id = played.id
        
    except Exception as e:
        logger.error(f"Error saving played French Loto combination: {str(e)}")
        session.rollback()
    finally:
        session.close()
        
    return combo_id

def get_french_loto_played_combinations():
    """
    Get all played French Loto combinations
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing played combinations
    """
    session = get_session()
    try:
        combinations = session.query(FrenchLotoPlayedCombination).order_by(FrenchLotoPlayedCombination.played_date.desc()).all()
        if not combinations:
            return pd.DataFrame()
            
        # Convert to list of dictionaries
        records = [combo.to_dict() for combo in combinations]
        return pd.DataFrame(records)
        
    except Exception as e:
        logger.error(f"Error retrieving played French Loto combinations: {str(e)}")
        return pd.DataFrame()
    finally:
        session.close()

def update_french_loto_result(combo_id, result):
    """
    Update the result of a played French Loto combination
    
    Parameters:
    -----------
    combo_id : int
        ID of the played combination
    result : str
        Result of the play (e.g., "3 correct", "Won €10", etc.)
        
    Returns:
    --------
    bool
        True if the update was successful
    """
    session = get_session()
    success = False
    
    try:
        # Find the combination
        played = session.query(FrenchLotoPlayedCombination).filter_by(id=combo_id).first()
        if not played:
            logger.warning(f"Played French Loto combination with ID {combo_id} not found")
            return False
            
        # Update result
        played.result = result
        session.commit()
        success = True
        
    except Exception as e:
        logger.error(f"Error updating French Loto result: {str(e)}")
        session.rollback()
    finally:
        session.close()
        
    return success

# Initialize the database if this module is run directly
if __name__ == "__main__":
    init_db()