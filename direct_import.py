import os
import pandas as pd
import sqlite3
import logging
import argparse
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_db_connection():
    """Get a connection to the PostgreSQL database"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable not set")
        return None
    
    try:
        conn = psycopg2.connect(database_url)
        logger.info("Successfully connected to database")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None

def create_tables(conn):
    """Create tables if they don't exist"""
    try:
        with conn.cursor() as cur:
            # Create drawings table
            cur.execute("""
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
            """)
            
            # Create combinations table
            cur.execute("""
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
            """)
            
            conn.commit()
            logger.info("Tables created if they didn't exist")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        conn.rollback()

def convert_french_date(date_str):
    """Convert date from French format DD/MM/YYYY to ISO format YYYY-MM-DD"""
    if isinstance(date_str, str):
        try:
            day, month, year = date_str.split('/')
            # Format as ISO date
            return f"{year}-{month}-{day}"
        except (ValueError, AttributeError):
            return None
    # Handle numeric format
    elif isinstance(date_str, (int, float)):
        try:
            date_str = str(int(date_str))
            if len(date_str) == 8:
                year = date_str[0:4]
                month = date_str[4:6]
                day = date_str[6:8]
                return f"{year}-{month}-{day}"
        except:
            pass
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

def process_loto_file(file_path, new_format=True):
    """Process a French Loto CSV file"""
    try:
        # Read CSV file
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        logger.info(f"Successfully read {file_path} with {len(df)} rows")
        
        # Create result DataFrame
        result = []
        
        for _, row in df.iterrows():
            try:
                # Try to determine format based on columns
                if 'numero_chance' in df.columns:
                    new_format = True
                elif 'boule_complementaire' in df.columns or 'boule_6' in df.columns:
                    new_format = False
                
                if new_format:
                    # Extract data from new format
                    date_str = convert_french_date(row.get('date_de_tirage'))
                    if not date_str:
                        continue
                        
                    day_of_week = get_day_of_week(row.get('jour_de_tirage', ''))
                    
                    n1 = int(row.get('boule_1', 0))
                    n2 = int(row.get('boule_2', 0))
                    n3 = int(row.get('boule_3', 0))
                    n4 = int(row.get('boule_4', 0))
                    n5 = int(row.get('boule_5', 0))
                    lucky = int(row.get('numero_chance', 0))
                    
                    winners_rank1 = int(row.get('nombre_de_gagnant_au_rang1', 0))
                    prize_rank1 = float(clean_value(row.get('rapport_du_rang1', 0)))
                    winners_rank2 = int(row.get('nombre_de_gagnant_au_rang2', 0))
                    prize_rank2 = float(clean_value(row.get('rapport_du_rang2', 0)))
                    winners_rank3 = int(row.get('nombre_de_gagnant_au_rang3', 0))
                    prize_rank3 = float(clean_value(row.get('rapport_du_rang3', 0)))
                    winners_rank4 = int(row.get('nombre_de_gagnant_au_rang4', 0))
                    prize_rank4 = float(clean_value(row.get('rapport_du_rang4', 0)))
                    winners_rank5 = int(row.get('nombre_de_gagnant_au_rang5', 0))
                    prize_rank5 = float(clean_value(row.get('rapport_du_rang5', 0)))
                    winners_rank6 = int(row.get('nombre_de_gagnant_au_rang6', 0))
                    prize_rank6 = float(clean_value(row.get('rapport_du_rang6', 0)))
                    winners_rank7 = int(row.get('nombre_de_gagnant_au_rang7', 0)) if 'nombre_de_gagnant_au_rang7' in df.columns else 0
                    prize_rank7 = float(clean_value(row.get('rapport_du_rang7', 0))) if 'rapport_du_rang7' in df.columns else 0.0
                    
                    currency = row.get('devise', 'EUR')
                    
                else:
                    # Extract data from old format
                    date_str = convert_french_date(row.get('date_de_tirage'))
                    if not date_str:
                        continue
                        
                    day_of_week = get_day_of_week(row.get('jour_de_tirage', ''))
                    
                    n1 = int(row.get('boule_1', 0))
                    n2 = int(row.get('boule_2', 0))
                    n3 = int(row.get('boule_3', 0))
                    n4 = int(row.get('boule_4', 0))
                    n5 = int(row.get('boule_5', 0))
                    
                    # For old format, use either boule_6 or boule_complementaire as the lucky number
                    if 'boule_6' in df.columns:
                        lucky = int(row.get('boule_6', 0))
                    else:
                        lucky = int(row.get('boule_complementaire', 0))
                    
                    # Old format may not have all the rank information
                    winners_rank1 = int(row.get('nombre_de_gagnant_au_rang1', 0)) if 'nombre_de_gagnant_au_rang1' in df.columns else 0
                    prize_rank1 = float(clean_value(row.get('rapport_du_rang1', 0))) if 'rapport_du_rang1' in df.columns else 0.0
                    winners_rank2 = int(row.get('nombre_de_gagnant_au_rang2', 0)) if 'nombre_de_gagnant_au_rang2' in df.columns else 0
                    prize_rank2 = float(clean_value(row.get('rapport_du_rang2', 0))) if 'rapport_du_rang2' in df.columns else 0.0
                    
                    # Set remaining ranks to 0
                    winners_rank3 = 0
                    prize_rank3 = 0.0
                    winners_rank4 = 0
                    prize_rank4 = 0.0
                    winners_rank5 = 0
                    prize_rank5 = 0.0
                    winners_rank6 = 0
                    prize_rank6 = 0.0
                    winners_rank7 = 0
                    prize_rank7 = 0.0
                    
                    currency = 'EUR'
                
                # Add row to result
                result.append({
                    'date': date_str,
                    'day_of_week': day_of_week,
                    'n1': n1,
                    'n2': n2,
                    'n3': n3,
                    'n4': n4,
                    'n5': n5,
                    'lucky': lucky,
                    'winners_rank1': winners_rank1,
                    'prize_rank1': prize_rank1,
                    'winners_rank2': winners_rank2,
                    'prize_rank2': prize_rank2,
                    'winners_rank3': winners_rank3,
                    'prize_rank3': prize_rank3,
                    'winners_rank4': winners_rank4,
                    'prize_rank4': prize_rank4,
                    'winners_rank5': winners_rank5,
                    'prize_rank5': prize_rank5,
                    'winners_rank6': winners_rank6,
                    'prize_rank6': prize_rank6,
                    'winners_rank7': winners_rank7,
                    'prize_rank7': prize_rank7,
                    'currency': currency
                })
                
            except Exception as e:
                logger.warning(f"Error processing row: {e}")
                continue
        
        logger.info(f"Processed {len(result)} rows from {file_path}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return []

def save_to_database(conn, data):
    """Save processed data to database"""
    if not data:
        logger.warning("No data to save")
        return 0
    
    count = 0
    try:
        with conn.cursor() as cur:
            # Prepare data for batch insert
            rows = []
            for item in data:
                # Convert date to datetime object
                date_str = item['date']
                
                # Check if draw already exists
                cur.execute("SELECT id FROM french_loto_drawings WHERE date = %s", (date_str,))
                if cur.fetchone():
                    logger.debug(f"Draw for {date_str} already exists, skipping")
                    continue
                
                rows.append((
                    date_str,
                    item['day_of_week'],
                    item['n1'],
                    item['n2'],
                    item['n3'],
                    item['n4'],
                    item['n5'],
                    item['lucky'],
                    item['winners_rank1'],
                    item['prize_rank1'],
                    item['winners_rank2'],
                    item['prize_rank2'],
                    item['winners_rank3'],
                    item['prize_rank3'],
                    item['winners_rank4'],
                    item['prize_rank4'],
                    item['winners_rank5'],
                    item['prize_rank5'],
                    item['winners_rank6'],
                    item['prize_rank6'],
                    item['winners_rank7'],
                    item['prize_rank7'],
                    0.0,  # total_amount
                    item['currency']
                ))
            
            # Insert data in batches
            if rows:
                batch_size = 100
                for i in range(0, len(rows), batch_size):
                    batch = rows[i:i+batch_size]
                    execute_values(cur, """
                    INSERT INTO french_loto_drawings (
                        date, day_of_week, n1, n2, n3, n4, n5, lucky,
                        winners_rank1, prize_rank1, winners_rank2, prize_rank2,
                        winners_rank3, prize_rank3, winners_rank4, prize_rank4,
                        winners_rank5, prize_rank5, winners_rank6, prize_rank6,
                        winners_rank7, prize_rank7, total_amount, currency
                    ) VALUES %s
                    """, batch)
                    
                    count += len(batch)
                    logger.info(f"Inserted {len(batch)} records")
                
                conn.commit()
                logger.info(f"Total of {count} records saved to database")
            else:
                logger.info("No new records to insert")
    
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        conn.rollback()
        count = 0
    
    return count

def count_records(conn):
    """Count records in the database"""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM french_loto_drawings")
            count = cur.fetchone()[0]
            logger.info(f"Database contains {count} French Loto drawings")
            return count
    except Exception as e:
        logger.error(f"Error counting records: {e}")
        return 0

def process_all_files(directory='./attached_assets'):
    """Process all Loto CSV files in the directory"""
    # Get database connection
    conn = get_db_connection()
    if not conn:
        return
    
    # Create tables
    create_tables(conn)
    
    # Count initial records
    initial_count = count_records(conn)
    
    # Process all files
    file_list = []
    for file in os.listdir(directory):
        if file.endswith('.csv') and ('loto' in file.lower() or 'nouveau' in file.lower()):
            file_list.append(os.path.join(directory, file))
    
    logger.info(f"Found {len(file_list)} potential Loto CSV files")
    
    # Sort files by name to process them in a consistent order
    file_list.sort()
    
    for file_path in file_list:
        try:
            # Determine format based on filename
            new_format = True
            if 'loto.csv' in file_path.lower():
                new_format = False
            
            # Process file
            data = process_loto_file(file_path, new_format)
            
            # Save to database
            if data:
                save_to_database(conn, data)
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
    
    # Count final records
    final_count = count_records(conn)
    
    logger.info(f"Added {final_count - initial_count} new records to database")
    logger.info(f"Database now contains {final_count} French Loto drawings")
    
    # Close connection
    conn.close()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Process French Loto data files')
    parser.add_argument('--file', '-f', help='Process a specific CSV file')
    parser.add_argument('--directory', '-d', default='./attached_assets', help='Directory containing CSV files')
    args = parser.parse_args()
    
    if args.file:
        # Get database connection
        conn = get_db_connection()
        if not conn:
            return
        
        # Create tables
        create_tables(conn)
        
        # Count initial records
        initial_count = count_records(conn)
        
        # Process file
        data = process_loto_file(args.file)
        
        # Save to database
        if data:
            save_to_database(conn, data)
        
        # Count final records
        final_count = count_records(conn)
        
        logger.info(f"Added {final_count - initial_count} new records to database")
        logger.info(f"Database now contains {final_count} French Loto drawings")
        
        # Close connection
        conn.close()
    else:
        # Process all files
        process_all_files(args.directory)

if __name__ == "__main__":
    main()