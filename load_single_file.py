import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, date
import logging
import argparse
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    
    # Handle numeric date format (YYYYMMDD)
    if isinstance(date_str, (int, float)):
        try:
            date_str = str(int(date_str))
            if len(date_str) == 8:
                year = date_str[0:4]
                month = date_str[4:6]
                day = date_str[6:8]
                return f"{year}-{month}-{day}"
            else:
                logger.warning(f"Invalid numeric date format: {date_str}")
                return None
        except (ValueError, TypeError):
            logger.warning(f"Could not convert numeric date: {date_str}")
            return None
    
    logger.warning(f"Date is not a string or number: {date_str}")
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
        logger.info(f"Columns: {df.columns.tolist()}")
        
        # Check if this is a new or old format
        if 'numero_chance' in df.columns:
            # New format (5 numbers + 1 luck)
            return process_new_format(df, file_path)
        elif 'boule_complementaire' in df.columns or 'boule_6' in df.columns:
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
    number_cols = ['n1', 'n2', 'n3', 'n4', 'n5', 'lucky']
    for col in number_cols:
        if col in result_df.columns:
            try:
                result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
                result_df[col] = result_df[col].astype('Int64')  # Use nullable integer type
            except Exception as e:
                logger.error(f"Error converting {col} to integer: {e}")
    
    # Convert prize columns to float
    for col in ['prize_rank1', 'prize_rank2', 'prize_rank3', 
                'prize_rank4', 'prize_rank5', 'prize_rank6', 'prize_rank7']:
        if col in result_df.columns:
            result_df[col] = result_df[col].apply(clean_value)
            result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
    
    # Sort by date
    if 'date' in result_df.columns:
        result_df = result_df.sort_values('date')
    
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
        'boule_complementaire': 'complementary'
    }
    
    # Create a new DataFrame with standardized columns
    result_df = pd.DataFrame()
    
    # Copy columns that match our standard names
    for old_col, new_col in standard_columns.items():
        if old_col in df.columns:
            result_df[new_col] = df[old_col]
    
    # Convert date
    if 'date' in result_df.columns:
        result_df['date'] = result_df['date'].apply(convert_french_date)
    
    # For old format, use the 6th number as lucky
    if 'n6' in result_df.columns:
        result_df['lucky'] = result_df['n6']
        result_df = result_df.drop('n6', axis=1)
    elif 'complementary' in result_df.columns:
        result_df['lucky'] = result_df['complementary']
        result_df = result_df.drop('complementary', axis=1)
    
    # Set winners and prizes to 0 (since old format may not have this info)
    result_df['winners_rank1'] = 0
    result_df['prize_rank1'] = 0.0
    
    # Set currency to EUR
    result_df['currency'] = 'EUR'
    
    # Sort by date
    if 'date' in result_df.columns:
        result_df = result_df.sort_values('date')
    
    logger.info(f"Processed {len(result_df)} rows from {file_path} as old format")
    return result_df

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

def create_tables_if_not_exist(engine):
    """Create French Loto tables if they don't exist"""
    try:
        inspector = inspect(engine)
        
        # Check if tables exist
        if not inspector.has_table('french_loto_drawings'):
            # Create tables using direct SQL
            with engine.connect() as conn:
                conn.execute(text("""
                CREATE TABLE IF NOT EXISTS french_loto_drawings (
                    id SERIAL PRIMARY KEY,
                    date DATE NOT NULL UNIQUE,
                    day_of_week VARCHAR(20),
                    n1 INTEGER NOT NULL,
                    n2 INTEGER NOT NULL,
                    n3 INTEGER NOT NULL,
                    n4 INTEGER NOT NULL,
                    n5 INTEGER NOT NULL,
                    lucky INTEGER NOT NULL,
                    winners_rank1 INTEGER,
                    prize_rank1 FLOAT,
                    winners_rank2 INTEGER,
                    prize_rank2 FLOAT,
                    winners_rank3 INTEGER,
                    prize_rank3 FLOAT,
                    winners_rank4 INTEGER,
                    prize_rank4 FLOAT,
                    winners_rank5 INTEGER,
                    prize_rank5 FLOAT,
                    winners_rank6 INTEGER,
                    prize_rank6 FLOAT,
                    winners_rank7 INTEGER,
                    prize_rank7 FLOAT,
                    total_amount FLOAT,
                    currency VARCHAR(10)
                )
                """))
                
                conn.execute(text("""
                CREATE TABLE IF NOT EXISTS french_loto_generated_combinations (
                    id SERIAL PRIMARY KEY,
                    numbers VARCHAR NOT NULL,
                    lucky VARCHAR NOT NULL,
                    strategy VARCHAR,
                    score FLOAT,
                    date_generated DATE NOT NULL,
                    target_draw_date DATE,
                    was_played BOOLEAN DEFAULT FALSE,
                    matches INTEGER,
                    lucky_match BOOLEAN DEFAULT FALSE,
                    won_prize FLOAT DEFAULT 0
                )
                """))
                
                conn.commit()
                
            logger.info("Created French Loto tables")
        else:
            logger.info("French Loto tables already exist")
            
    except Exception as e:
        logger.error(f"Error creating tables: {e}")

def save_to_database(df, engine):
    """Save processed DataFrame to the database"""
    if df is None or len(df) == 0:
        logger.warning("No data to save to database")
        return 0
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    count = 0
    batch_size = 100
    rows_to_insert = []
    
    try:
        for _, row in df.iterrows():
            try:
                # Convert date string to datetime.date object
                draw_date = None
                if isinstance(row['date'], str):
                    try:
                        draw_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                    except ValueError:
                        logger.warning(f"Skipping row with invalid date format: {row['date']}")
                        continue
                else:
                    logger.warning(f"Skipping row with invalid date: {row['date']}")
                    continue
                
                # Check if this draw date already exists
                with engine.connect() as conn:
                    result = conn.execute(
                        text("SELECT id FROM french_loto_drawings WHERE date = :date"),
                        {"date": draw_date}
                    )
                    existing = result.first()
                
                if existing:
                    logger.debug(f"Draw for {draw_date} already exists in database")
                    continue
                
                # Make sure number values are valid
                try:
                    n1 = int(row['n1'])
                    n2 = int(row['n2'])
                    n3 = int(row['n3'])
                    n4 = int(row['n4'])
                    n5 = int(row['n5'])
                    lucky = int(row['lucky'])
                except (ValueError, TypeError):
                    logger.warning(f"Skipping row with invalid number values: {row}")
                    continue
                
                # Add row to batch
                rows_to_insert.append({
                    "date": draw_date,
                    "day_of_week": str(row.get('day_of_week', '')),
                    "n1": n1,
                    "n2": n2,
                    "n3": n3,
                    "n4": n4,
                    "n5": n5,
                    "lucky": lucky,
                    "winners_rank1": int(row.get('winners_rank1', 0)) if pd.notna(row.get('winners_rank1', 0)) else 0,
                    "prize_rank1": float(row.get('prize_rank1', 0.0)) if pd.notna(row.get('prize_rank1', 0.0)) else 0.0,
                    "winners_rank2": int(row.get('winners_rank2', 0)) if pd.notna(row.get('winners_rank2', 0)) else 0,
                    "prize_rank2": float(row.get('prize_rank2', 0.0)) if pd.notna(row.get('prize_rank2', 0.0)) else 0.0,
                    "winners_rank3": int(row.get('winners_rank3', 0)) if pd.notna(row.get('winners_rank3', 0)) else 0,
                    "prize_rank3": float(row.get('prize_rank3', 0.0)) if pd.notna(row.get('prize_rank3', 0.0)) else 0.0,
                    "winners_rank4": int(row.get('winners_rank4', 0)) if pd.notna(row.get('winners_rank4', 0)) else 0,
                    "prize_rank4": float(row.get('prize_rank4', 0.0)) if pd.notna(row.get('prize_rank4', 0.0)) else 0.0,
                    "winners_rank5": int(row.get('winners_rank5', 0)) if pd.notna(row.get('winners_rank5', 0)) else 0,
                    "prize_rank5": float(row.get('prize_rank5', 0.0)) if pd.notna(row.get('prize_rank5', 0.0)) else 0.0,
                    "winners_rank6": int(row.get('winners_rank6', 0)) if pd.notna(row.get('winners_rank6', 0)) else 0,
                    "prize_rank6": float(row.get('prize_rank6', 0.0)) if pd.notna(row.get('prize_rank6', 0.0)) else 0.0,
                    "winners_rank7": int(row.get('winners_rank7', 0)) if pd.notna(row.get('winners_rank7', 0)) else 0,
                    "prize_rank7": float(row.get('prize_rank7', 0.0)) if pd.notna(row.get('prize_rank7', 0.0)) else 0.0,
                    "total_amount": float(row.get('total_amount', 0.0)) if pd.notna(row.get('total_amount', 0.0)) else 0.0,
                    "currency": str(row.get('currency', 'EUR'))
                })
                
                count += 1
                
                # Insert in batches
                if len(rows_to_insert) >= batch_size:
                    with engine.connect() as conn:
                        conn.execute(
                            text("""
                            INSERT INTO french_loto_drawings (
                                date, day_of_week, n1, n2, n3, n4, n5, lucky,
                                winners_rank1, prize_rank1, winners_rank2, prize_rank2,
                                winners_rank3, prize_rank3, winners_rank4, prize_rank4,
                                winners_rank5, prize_rank5, winners_rank6, prize_rank6,
                                winners_rank7, prize_rank7, total_amount, currency
                            ) VALUES (
                                :date, :day_of_week, :n1, :n2, :n3, :n4, :n5, :lucky,
                                :winners_rank1, :prize_rank1, :winners_rank2, :prize_rank2,
                                :winners_rank3, :prize_rank3, :winners_rank4, :prize_rank4,
                                :winners_rank5, :prize_rank5, :winners_rank6, :prize_rank6,
                                :winners_rank7, :prize_rank7, :total_amount, :currency
                            )
                            """),
                            rows_to_insert
                        )
                        conn.commit()
                    
                    logger.info(f"Inserted {len(rows_to_insert)} records")
                    rows_to_insert = []
                
            except Exception as e:
                logger.error(f"Error processing row: {e}")
                continue
        
        # Insert any remaining rows
        if rows_to_insert:
            with engine.connect() as conn:
                conn.execute(
                    text("""
                    INSERT INTO french_loto_drawings (
                        date, day_of_week, n1, n2, n3, n4, n5, lucky,
                        winners_rank1, prize_rank1, winners_rank2, prize_rank2,
                        winners_rank3, prize_rank3, winners_rank4, prize_rank4,
                        winners_rank5, prize_rank5, winners_rank6, prize_rank6,
                        winners_rank7, prize_rank7, total_amount, currency
                    ) VALUES (
                        :date, :day_of_week, :n1, :n2, :n3, :n4, :n5, :lucky,
                        :winners_rank1, :prize_rank1, :winners_rank2, :prize_rank2,
                        :winners_rank3, :prize_rank3, :winners_rank4, :prize_rank4,
                        :winners_rank5, :prize_rank5, :winners_rank6, :prize_rank6,
                        :winners_rank7, :prize_rank7, :total_amount, :currency
                    )
                    """),
                    rows_to_insert
                )
                conn.commit()
            
            logger.info(f"Inserted final {len(rows_to_insert)} records")
        
        logger.info(f"Total of {count} records saved to database")
    
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        count = 0
    
    finally:
        session.close()
    
    return count

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
    """Main function to process a single French Loto data file"""
    parser = argparse.ArgumentParser(description='Process a single French Loto CSV file')
    parser.add_argument('--file', '-f', required=True, help='Path to CSV file')
    args = parser.parse_args()
    
    # Get database connection
    engine = get_database_connection()
    if engine is None:
        return
    
    # Create tables if they don't exist
    create_tables_if_not_exist(engine)
    
    # Count existing records
    initial_count = count_database_records(engine)
    
    # Process file
    df = process_csv_file(args.file)
    
    if df is not None:
        logger.info(f"Processed {len(df)} rows from {args.file}")
        
        # Save to database
        saved_count = save_to_database(df, engine)
        
        # Count final records
        final_count = count_database_records(engine)
        
        logger.info(f"Added {final_count - initial_count} new records to database")
        logger.info(f"Database now contains {final_count} French Loto drawings")
    else:
        logger.warning("No data to save")

if __name__ == "__main__":
    main()