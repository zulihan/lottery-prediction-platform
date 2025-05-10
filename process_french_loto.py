import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import argparse
import json
from sqlalchemy import create_engine, text, Column, Integer, String, Date, Float, Boolean, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

Base = declarative_base()

class FrenchLotoDrawing(Base):
    __tablename__ = 'french_loto_drawings'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=True)
    day_of_week = Column(String(20))
    n1 = Column(Integer, nullable=False)
    n2 = Column(Integer, nullable=False)
    n3 = Column(Integer, nullable=False)
    n4 = Column(Integer, nullable=False)
    n5 = Column(Integer, nullable=False)
    lucky = Column(Integer, nullable=False)
    winners_rank1 = Column(Integer)
    prize_rank1 = Column(Float)
    winners_rank2 = Column(Integer)
    prize_rank2 = Column(Float)
    winners_rank3 = Column(Integer)
    prize_rank3 = Column(Float)
    winners_rank4 = Column(Integer)
    prize_rank4 = Column(Float)
    winners_rank5 = Column(Integer)
    prize_rank5 = Column(Float)
    winners_rank6 = Column(Integer)
    prize_rank6 = Column(Float)
    winners_rank7 = Column(Integer)
    prize_rank7 = Column(Float)
    total_amount = Column(Float)
    currency = Column(String(10))
    
    def __repr__(self):
        return f"<FrenchLotoDrawing(date='{self.date}', numbers='{self.n1},{self.n2},{self.n3},{self.n4},{self.n5}', lucky='{self.lucky}')>"

class FrenchLotoGeneratedCombination(Base):
    __tablename__ = 'french_loto_generated_combinations'
    
    id = Column(Integer, primary_key=True)
    numbers = Column(String, nullable=False)
    lucky = Column(String, nullable=False)
    strategy = Column(String)
    score = Column(Float)
    date_generated = Column(Date, nullable=False)
    target_draw_date = Column(Date)
    was_played = Column(Boolean, default=False)
    matches = Column(Integer)
    lucky_match = Column(Boolean, default=False)
    won_prize = Column(Float, default=0)
    
    def __repr__(self):
        return f"<FrenchLotoGeneratedCombination(id='{self.id}', numbers='{self.numbers}', lucky='{self.lucky}')>"

def convert_french_date(date_str):
    """Convert date from French format DD/MM/YYYY to ISO format YYYY-MM-DD"""
    if isinstance(date_str, str):
        try:
            day, month, year = date_str.split('/')
            # Make sure day, month, year are zero-padded to 2 digits if needed
            day = day.zfill(2)
            month = month.zfill(2)
            # Format as ISO date
            return f"{year}-{month}-{day}"
        except (ValueError, AttributeError):
            logger.warning(f"Could not parse date: {date_str}")
            return None
    logger.warning(f"Date is not a string: {date_str}")
    return None

def get_day_of_week(day_abbr):
    """Convert French day abbreviation to full English day name."""
    if isinstance(day_abbr, str):
        day_abbr = day_abbr.strip().upper()
        days_map = {
            'LU': 'Monday',
            'LUNDI': 'Monday',
            'MA': 'Tuesday',
            'MARDI': 'Tuesday',
            'ME': 'Wednesday',
            'MERCREDI': 'Wednesday',
            'JE': 'Thursday',
            'JEUDI': 'Thursday',
            'VE': 'Friday',
            'VENDREDI': 'Friday',
            'SA': 'Saturday',
            'SAMEDI': 'Saturday',
            'DI': 'Sunday',
            'DIMANCHE': 'Sunday'
        }
        return days_map.get(day_abbr, day_abbr)
    return day_abbr

def clean_value(value):
    """Clean numeric values from French format"""
    if isinstance(value, str):
        return value.replace(',', '.').replace(' ', '')
    return value

def process_csv_file(file_path):
    """Process a French Loto CSV file and return a DataFrame with standardized columns"""
    try:
        # Read CSV file with semicolon delimiter
        df = pd.read_csv(file_path, sep=';', encoding='utf-8', low_memory=False)
        logger.info(f"Successfully read {file_path} with {len(df)} rows")
        
        # Check if this is a new or old format
        if 'numero_chance' in df.columns:
            # New format (5 numbers + 1 luck)
            return process_new_format(df, file_path)
        elif 'boule_complementaire' in df.columns:
            # Old format (6 numbers + 1 complementary)
            return process_old_format(df, file_path)
        else:
            logger.error(f"Unknown format for file {file_path}")
            return None
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return None

def process_new_format(df, file_path):
    """Process new format of French Loto (5 numbers + 1 lucky number)"""
    # Standardize column names
    standard_columns = {
        'date_de_tirage': 'date',
        'jour_de_tirage': 'day_of_week',
        'boule_1': 'n1',
        'boule_2': 'n2', 
        'boule_3': 'n3',
        'boule_4': 'n4',
        'boule_5': 'n5',
        'numero_chance': 'lucky',
        'nombre_de_gagnant_au_rang1': 'winners_rank1',
        'rapport_du_rang1': 'prize_rank1',
        'nombre_de_gagnant_au_rang2': 'winners_rank2',
        'rapport_du_rang2': 'prize_rank2',
        'nombre_de_gagnant_au_rang3': 'winners_rank3',
        'rapport_du_rang3': 'prize_rank3',
        'nombre_de_gagnant_au_rang4': 'winners_rank4',
        'rapport_du_rang4': 'prize_rank4',
        'nombre_de_gagnant_au_rang5': 'winners_rank5',
        'rapport_du_rang5': 'prize_rank5',
        'nombre_de_gagnant_au_rang6': 'winners_rank6',
        'rapport_du_rang6': 'prize_rank6',
        'nombre_de_gagnant_au_rang7': 'winners_rank7',
        'rapport_du_rang7': 'prize_rank7',
        'devise': 'currency'
    }
    
    # Create a new DataFrame with standardized columns
    result_df = pd.DataFrame()
    
    # Copy columns that match our standard names
    for old_col, new_col in standard_columns.items():
        if old_col in df.columns:
            result_df[new_col] = df[old_col]
    
    # Convert date and clean numeric values
    result_df['date'] = result_df['date'].apply(convert_french_date)
    result_df['day_of_week'] = result_df['day_of_week'].apply(get_day_of_week)
    
    # Convert number columns to integers
    for col in ['n1', 'n2', 'n3', 'n4', 'n5', 'lucky', 
                'winners_rank1', 'winners_rank2', 'winners_rank3', 
                'winners_rank4', 'winners_rank5', 'winners_rank6', 'winners_rank7']:
        if col in result_df.columns:
            result_df[col] = pd.to_numeric(result_df[col], errors='coerce').fillna(0).astype(int)
    
    # Convert prize columns to float
    for col in ['prize_rank1', 'prize_rank2', 'prize_rank3', 
                'prize_rank4', 'prize_rank5', 'prize_rank6', 'prize_rank7']:
        if col in result_df.columns:
            result_df[col] = result_df[col].apply(clean_value)
            result_df[col] = pd.to_numeric(result_df[col], errors='coerce').fillna(0)
    
    # Sort by date
    if 'date' in result_df.columns:
        result_df = result_df.sort_values('date')
    
    # Add total amount if available
    if 'total_amount' not in result_df.columns:
        # Try to find it in the original dataframe
        for col in df.columns:
            if "total" in col.lower() or "amount" in col.lower() or "montant" in col.lower():
                result_df['total_amount'] = df[col].apply(clean_value)
                result_df['total_amount'] = pd.to_numeric(result_df['total_amount'], errors='coerce').fillna(0)
                break
    
    logger.info(f"Processed {len(result_df)} rows from {file_path} as new format")
    return result_df

def process_old_format(df, file_path):
    """Process old format of French Loto (6 numbers + 1 complementary)"""
    # Standardize column names
    standard_columns = {
        'date_de_tirage': 'date',
        'jour_de_tirage': 'day_of_week',
        'boule_1': 'n1',
        'boule_2': 'n2', 
        'boule_3': 'n3',
        'boule_4': 'n4',
        'boule_5': 'n5',
        'boule_6': 'n6',
        'boule_complementaire': 'complementary',
        'nombre_de_gagnant_au_rang1': 'winners_rank1',
        'rapport_du_rang1': 'prize_rank1',
        'nombre_de_gagnant_au_rang2': 'winners_rank2',
        'rapport_du_rang2': 'prize_rank2'
        # Add other ranks as needed
    }
    
    # Create a new DataFrame with standardized columns
    result_df = pd.DataFrame()
    
    # Copy columns that match our standard names
    for old_col, new_col in standard_columns.items():
        if old_col in df.columns:
            result_df[new_col] = df[old_col]
    
    # Convert date and clean numeric values
    result_df['date'] = result_df['date'].apply(convert_french_date)
    result_df['day_of_week'] = result_df['day_of_week'].apply(get_day_of_week)
    
    # For old format, we need to extract 5 numbers + lucky from the 6 numbers + complementary
    # In this case, we'll use the 6th number as the lucky number
    if 'n6' in result_df.columns:
        result_df['lucky'] = result_df['n6']
        result_df = result_df.drop('n6', axis=1)
    else:
        # If n6 isn't available, we'll use the complementary as the lucky number
        result_df['lucky'] = result_df['complementary']
    
    if 'complementary' in result_df.columns:
        result_df = result_df.drop('complementary', axis=1)
    
    # Convert number columns to integers
    for col in ['n1', 'n2', 'n3', 'n4', 'n5', 'lucky', 
                'winners_rank1', 'winners_rank2']:
        if col in result_df.columns:
            result_df[col] = pd.to_numeric(result_df[col], errors='coerce').fillna(0).astype(int)
    
    # Convert prize columns to float
    for col in ['prize_rank1', 'prize_rank2']:
        if col in result_df.columns:
            result_df[col] = result_df[col].apply(clean_value)
            result_df[col] = pd.to_numeric(result_df[col], errors='coerce').fillna(0)
    
    # Sort by date
    if 'date' in result_df.columns:
        result_df = result_df.sort_values('date')
    
    # Add currency (assume EUR for older draws)
    if 'currency' not in result_df.columns:
        result_df['currency'] = 'EUR'
    
    logger.info(f"Processed {len(result_df)} rows from {file_path} as old format")
    return result_df

def combine_dataframes(dataframes):
    """Combine multiple processed DataFrames into one, handling overlaps by keeping the newest"""
    if not dataframes:
        return None
    
    # Combine all dataframes
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Make sure date is string type for all records
    combined_df['date'] = combined_df['date'].astype(str)
    
    # Remove duplicates, keeping the last occurrence (assuming more recent file has better data)
    combined_df = combined_df.drop_duplicates(subset=['date'], keep='last')
    
    # Sort by date (as string)
    combined_df = combined_df.sort_values('date')
    
    return combined_df

def create_database_tables(engine):
    """Create database tables if they don't exist"""
    # Check if tables already exist
    inspector = inspect(engine)
    
    if not inspector.has_table('french_loto_drawings'):
        # Create french_loto_drawings table
        Base.metadata.create_all(engine, tables=[FrenchLotoDrawing.__table__])
        logger.info("Created french_loto_drawings table")
    else:
        logger.info("french_loto_drawings table already exists")
    
    if not inspector.has_table('french_loto_generated_combinations'):
        # Create french_loto_generated_combinations table
        Base.metadata.create_all(engine, tables=[FrenchLotoGeneratedCombination.__table__])
        logger.info("Created french_loto_generated_combinations table")
    else:
        logger.info("french_loto_generated_combinations table already exists")

def save_to_database(df, engine):
    """Save processed DataFrame to the database"""
    if df is None or len(df) == 0:
        logger.warning("No data to save to database")
        return 0
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    count = 0
    try:
        for _, row in df.iterrows():
            # Convert date string to datetime.date object
            try:
                draw_date = None
                if isinstance(row['date'], str):
                    from datetime import datetime
                    draw_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                else:
                    logger.warning(f"Skipping row with invalid date: {row['date']}")
                    continue
                
                # Check if this draw date already exists
                existing = session.query(FrenchLotoDrawing).filter_by(date=draw_date).first()
                if existing:
                    logger.debug(f"Draw for {draw_date} already exists in database")
                    continue
                
                # Create a new FrenchLotoDrawing object
                drawing = FrenchLotoDrawing(
                    date=draw_date,
                    day_of_week=row.get('day_of_week'),
                    n1=int(row['n1']),
                    n2=int(row['n2']),
                    n3=int(row['n3']),
                    n4=int(row['n4']),
                    n5=int(row['n5']),
                    lucky=int(row['lucky']),
                    winners_rank1=int(row.get('winners_rank1', 0)),
                    prize_rank1=float(row.get('prize_rank1', 0.0)),
                    winners_rank2=int(row.get('winners_rank2', 0)),
                    prize_rank2=float(row.get('prize_rank2', 0.0)),
                    winners_rank3=int(row.get('winners_rank3', 0)),
                    prize_rank3=float(row.get('prize_rank3', 0.0)),
                    winners_rank4=int(row.get('winners_rank4', 0)),
                    prize_rank4=float(row.get('prize_rank4', 0.0)),
                    winners_rank5=int(row.get('winners_rank5', 0)),
                    prize_rank5=float(row.get('prize_rank5', 0.0)),
                    winners_rank6=int(row.get('winners_rank6', 0)),
                    prize_rank6=float(row.get('prize_rank6', 0.0)),
                    winners_rank7=int(row.get('winners_rank7', 0)),
                    prize_rank7=float(row.get('prize_rank7', 0.0)),
                    total_amount=float(row.get('total_amount', 0.0)),
                    currency=str(row.get('currency', 'EUR'))
                )
                
                # Add to session
                session.add(drawing)
                count += 1
                
                # Commit every 100 records to avoid large transactions
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Committed {count} records to database")
            
            except Exception as e:
                logger.error(f"Error processing row: {e}")
                continue
        
        # Final commit
        session.commit()
        logger.info(f"Total of {count} records saved to database")
    
    except Exception as e:
        session.rollback()
        logger.error(f"Error saving to database: {e}")
        count = 0
    
    finally:
        session.close()
    
    return count

def get_database_connection():
    """Get SQLAlchemy engine from environment variables"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable not set")
        return None
    
    try:
        engine = create_engine(database_url)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Successfully connected to database")
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None

def list_csv_files(directory='./attached_assets'):
    """List all CSV files in the specified directory that might contain Loto data"""
    loto_csv_files = []
    
    for file in os.listdir(directory):
        if file.endswith('.csv') and ('loto' in file.lower() or 'nouveau' in file.lower()):
            loto_csv_files.append(os.path.join(directory, file))
    
    return loto_csv_files

def count_database_records(engine):
    """Count number of records in the database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM french_loto_drawings"))
            count = result.scalar()
            logger.info(f"Database contains {count} French Loto drawings")
            return count
    except Exception as e:
        logger.error(f"Error counting database records: {e}")
        return 0

def main():
    """Main function to process French Loto data files and save to database"""
    parser = argparse.ArgumentParser(description='Process French Loto CSV files and save to database')
    parser.add_argument('--directory', '-d', default='./attached_assets',
                        help='Directory containing CSV files (default: ./attached_assets)')
    parser.add_argument('--file', '-f', help='Process a specific CSV file')
    parser.add_argument('--clear', '-c', action='store_true', 
                        help='Clear existing data before importing')
    args = parser.parse_args()
    
    # Get database connection
    engine = get_database_connection()
    if engine is None:
        return
    
    # Create tables if they don't exist
    create_database_tables(engine)
    
    # Clear existing data if requested
    if args.clear:
        try:
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM french_loto_drawings"))
                conn.commit()
            logger.info("Cleared existing data from french_loto_drawings table")
        except Exception as e:
            logger.error(f"Error clearing existing data: {e}")
    
    # Count existing records
    initial_count = count_database_records(engine)
    
    # Process files
    dataframes = []
    
    if args.file:
        # Process a specific file
        df = process_csv_file(args.file)
        if df is not None:
            dataframes.append(df)
    else:
        # Process all CSV files in the directory
        csv_files = list_csv_files(args.directory)
        logger.info(f"Found {len(csv_files)} potential Loto CSV files")
        
        for file in csv_files:
            if 'loto' in file.lower():
                df = process_csv_file(file)
                if df is not None:
                    dataframes.append(df)
    
    # Combine all dataframes
    combined_df = combine_dataframes(dataframes)
    
    if combined_df is not None:
        logger.info(f"Combined {len(combined_df)} unique drawings")
        
        # Save to database
        saved_count = save_to_database(combined_df, engine)
        
        # Count final records
        final_count = count_database_records(engine)
        
        logger.info(f"Added {final_count - initial_count} new records to database")
        logger.info(f"Database now contains {final_count} French Loto drawings")
    else:
        logger.warning("No data to save")

if __name__ == "__main__":
    main()