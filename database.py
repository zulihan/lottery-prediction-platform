import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, ForeignKey, Table, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

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
    
    def __repr__(self):
        return f"<UserSavedCombination(id='{self.id}', numbers={self.numbers}, stars={self.stars}, played={self.played})>"
    
    def to_dict(self):
        """Convert saved combination to dictionary format"""
        return {
            'id': self.id,
            'saved_at': self.saved_at.strftime('%Y-%m-%d'),
            'numbers': json.loads(self.numbers),
            'stars': json.loads(self.stars),
            'strategy': self.strategy,
            'notes': self.notes,
            'played': self.played,
            'result': self.result
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
    
    return len(drawings)

def get_all_drawings():
    """
    Get all Euromillions drawings from the database
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing all drawing records
    """
    drawings = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date.desc()).all()
    if not drawings:
        return pd.DataFrame()
        
    # Convert to list of dictionaries
    records = [drawing.to_dict() for drawing in drawings]
    return pd.DataFrame(records)

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
    return True

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
    return combination.id

def get_generated_combinations(strategy=None, limit=100):
    """
    Get generated combinations from the database
    
    Parameters:
    -----------
    strategy : str, optional
        Filter by strategy
    limit : int, optional
        Maximum number of combinations to return
        
    Returns:
    --------
    list
        List of dictionaries containing combination data
    """
    query = session.query(GeneratedCombination)
    
    if strategy:
        query = query.filter_by(strategy=strategy)
        
    combinations = query.order_by(GeneratedCombination.created_at.desc()).limit(limit).all()
    
    return [combination.to_dict() for combination in combinations]

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
    return saved.id

def get_user_saved_combinations(limit=50):
    """
    Get user-saved combinations from the database
    
    Parameters:
    -----------
    limit : int, optional
        Maximum number of combinations to return
        
    Returns:
    --------
    list
        List of dictionaries containing saved combination data
    """
    saved = session.query(UserSavedCombination).order_by(UserSavedCombination.saved_at.desc()).limit(limit).all()
    return [combo.to_dict() for combo in saved]

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
    return True

# Initialize the database if this module is run directly
if __name__ == "__main__":
    init_db()