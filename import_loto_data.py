import os
import pandas as pd
import psycopg2
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_db_connection():
    """Connect to the PostgreSQL database"""
    try:
        # Get credentials from environment variables
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            logger.error("DATABASE_URL environment variable not set")
            return None
            
        # Connect to the database
        conn = psycopg2.connect(database_url)
        logger.info("Connected to database")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        return None

def create_tables(conn):
    """Create the necessary tables if they don't exist"""
    try:
        with conn.cursor() as cur:
            # Create french_loto_drawings table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS french_loto_drawings (
                id SERIAL PRIMARY KEY,
                date DATE UNIQUE NOT NULL,
                day_of_week VARCHAR(20),
                n1 INTEGER NOT NULL,
                n2 INTEGER NOT NULL,
                n3 INTEGER NOT NULL,
                n4 INTEGER NOT NULL,
                n5 INTEGER NOT NULL,
                lucky INTEGER NOT NULL,
                winners_rank1 INTEGER DEFAULT 0,
                prize_rank1 FLOAT DEFAULT 0,
                winners_rank2 INTEGER DEFAULT 0,
                prize_rank2 FLOAT DEFAULT 0,
                winners_rank3 INTEGER DEFAULT 0,
                prize_rank3 FLOAT DEFAULT 0,
                winners_rank4 INTEGER DEFAULT 0,
                prize_rank4 FLOAT DEFAULT 0,
                winners_rank5 INTEGER DEFAULT 0,
                prize_rank5 FLOAT DEFAULT 0,
                winners_rank6 INTEGER DEFAULT 0,
                prize_rank6 FLOAT DEFAULT 0,
                winners_rank7 INTEGER DEFAULT 0,
                prize_rank7 FLOAT DEFAULT 0,
                total_amount FLOAT DEFAULT 0,
                currency VARCHAR(10) DEFAULT 'EUR'
            )
            """)
            
            # Create generated combinations table
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
                matches INTEGER DEFAULT 0,
                lucky_match BOOLEAN DEFAULT FALSE,
                won_prize FLOAT DEFAULT 0
            )
            """)
            
            conn.commit()
            logger.info("Tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        conn.rollback()

def count_existing_records(conn):
    """Count the existing records in the database"""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM french_loto_drawings")
            count = cur.fetchone()[0]
            logger.info(f"Database contains {count} French Loto drawings")
            return count
    except Exception as e:
        logger.error(f"Error counting records: {e}")
        return 0

def process_loto_csv(file_path):
    """Process a French Loto CSV file"""
    try:
        # Read the CSV file
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        logger.info(f"Read {len(df)} rows from {file_path}")
        
        # Determine the format based on column names
        if 'numero_chance' in df.columns:
            logger.info(f"File {file_path} has new format (5 numbers + 1 lucky)")
            return process_new_format(df)
        elif 'boule_complementaire' in df.columns or 'boule_6' in df.columns:
            logger.info(f"File {file_path} has old format (6 numbers + complementary)")
            return process_old_format(df)
        else:
            logger.error(f"Unknown format for file {file_path}")
            return None
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

def process_new_format(df):
    """Process new format Loto data (5 numbers + 1 lucky)"""
    data = []
    
    for _, row in df.iterrows():
        try:
            # Convert date
            if 'date_de_tirage' in row:
                date_str = row['date_de_tirage']
                if isinstance(date_str, str):
                    # Format DD/MM/YYYY -> YYYY-MM-DD
                    parts = date_str.split('/')
                    if len(parts) == 3:
                        date = f"{parts[2]}-{parts[1]}-{parts[0]}"
                    else:
                        continue
                else:
                    continue
            else:
                continue
            
            # Get day of week
            day_of_week = row.get('jour_de_tirage', '')
            if isinstance(day_of_week, str):
                day_of_week = day_of_week.strip()
                
            # Get numbers
            n1 = int(row.get('boule_1', 0))
            n2 = int(row.get('boule_2', 0))
            n3 = int(row.get('boule_3', 0))
            n4 = int(row.get('boule_4', 0))
            n5 = int(row.get('boule_5', 0))
            lucky = int(row.get('numero_chance', 0))
            
            # Get winners and prize data
            winners_rank1 = int(row.get('nombre_de_gagnant_au_rang1', 0))
            prize_rank1 = float(str(row.get('rapport_du_rang1', 0)).replace(',', '.').replace(' ', ''))
            winners_rank2 = int(row.get('nombre_de_gagnant_au_rang2', 0))
            prize_rank2 = float(str(row.get('rapport_du_rang2', 0)).replace(',', '.').replace(' ', ''))
            winners_rank3 = int(row.get('nombre_de_gagnant_au_rang3', 0))
            prize_rank3 = float(str(row.get('rapport_du_rang3', 0)).replace(',', '.').replace(' ', ''))
            winners_rank4 = int(row.get('nombre_de_gagnant_au_rang4', 0))
            prize_rank4 = float(str(row.get('rapport_du_rang4', 0)).replace(',', '.').replace(' ', ''))
            winners_rank5 = int(row.get('nombre_de_gagnant_au_rang5', 0))
            prize_rank5 = float(str(row.get('rapport_du_rang5', 0)).replace(',', '.').replace(' ', ''))
            winners_rank6 = int(row.get('nombre_de_gagnant_au_rang6', 0))
            prize_rank6 = float(str(row.get('rapport_du_rang6', 0)).replace(',', '.').replace(' ', ''))
            
            # Get currency
            currency = row.get('devise', 'EUR')
            
            # Check if we have data for 7th rank
            winners_rank7 = 0
            prize_rank7 = 0.0
            if 'nombre_de_gagnant_au_rang7' in row and 'rapport_du_rang7' in row:
                winners_rank7 = int(row.get('nombre_de_gagnant_au_rang7', 0))
                prize_rank7 = float(str(row.get('rapport_du_rang7', 0)).replace(',', '.').replace(' ', ''))
            
            # Add to data list
            data.append({
                'date': date,
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
    
    logger.info(f"Processed {len(data)} rows from new format")
    return data

def process_old_format(df):
    """Process old format Loto data (6 numbers + complementary)"""
    data = []
    
    for _, row in df.iterrows():
        try:
            # Convert date
            if 'date_de_tirage' in row:
                date_str = row['date_de_tirage']
                if isinstance(date_str, (int, float)):
                    # Format YYYYMMDD -> YYYY-MM-DD
                    date_str = str(int(date_str))
                    if len(date_str) == 8:
                        date = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
                    else:
                        continue
                else:
                    continue
            else:
                continue
            
            # Get day of week
            day_of_week = row.get('jour_de_tirage', '')
            
            # Get numbers
            n1 = int(row.get('boule_1', 0))
            n2 = int(row.get('boule_2', 0))
            n3 = int(row.get('boule_3', 0))
            n4 = int(row.get('boule_4', 0))
            n5 = int(row.get('boule_5', 0))
            
            # In old format, use either boule_6 or boule_complementaire as lucky
            if 'boule_6' in row:
                lucky = int(row.get('boule_6', 0))
            else:
                lucky = int(row.get('boule_complementaire', 0))
            
            # Old format may not have all ranks
            # Just set defaults for most
            winners_rank1 = int(row.get('nombre_de_gagnant_au_rang1', 0)) if 'nombre_de_gagnant_au_rang1' in row else 0
            prize_rank1 = 0.0
            if 'rapport_du_rang1' in row and row['rapport_du_rang1']:
                prize_str = str(row['rapport_du_rang1']).replace(',', '.').replace(' ', '')
                if prize_str and prize_str.replace('.', '').isdigit():
                    prize_rank1 = float(prize_str)
            
            # Add to data list with minimal info
            data.append({
                'date': date,
                'day_of_week': day_of_week,
                'n1': n1,
                'n2': n2,
                'n3': n3,
                'n4': n4,
                'n5': n5,
                'lucky': lucky,
                'winners_rank1': winners_rank1,
                'prize_rank1': prize_rank1,
                'winners_rank2': 0,
                'prize_rank2': 0.0,
                'winners_rank3': 0,
                'prize_rank3': 0.0,
                'winners_rank4': 0,
                'prize_rank4': 0.0,
                'winners_rank5': 0,
                'prize_rank5': 0.0,
                'winners_rank6': 0,
                'prize_rank6': 0.0,
                'winners_rank7': 0,
                'prize_rank7': 0.0,
                'currency': 'EUR'
            })
        except Exception as e:
            logger.warning(f"Error processing row: {e}")
    
    logger.info(f"Processed {len(data)} rows from old format")
    return data

def save_to_database(conn, data):
    """Save processed data to the database"""
    if not data:
        logger.warning("No data to save")
        return 0
    
    inserted_count = 0
    
    try:
        with conn.cursor() as cur:
            # Use ON CONFLICT DO NOTHING to handle duplicates
            for item in data:
                try:
                    # Check if date exists
                    cur.execute("SELECT id FROM french_loto_drawings WHERE date = %s", (item['date'],))
                    if cur.fetchone():
                        continue
                    
                    # Insert the record
                    cur.execute("""
                    INSERT INTO french_loto_drawings (
                        date, day_of_week, n1, n2, n3, n4, n5, lucky,
                        winners_rank1, prize_rank1, winners_rank2, prize_rank2,
                        winners_rank3, prize_rank3, winners_rank4, prize_rank4,
                        winners_rank5, prize_rank5, winners_rank6, prize_rank6,
                        winners_rank7, prize_rank7, currency
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        item['date'], item['day_of_week'], 
                        item['n1'], item['n2'], item['n3'], item['n4'], item['n5'], item['lucky'],
                        item['winners_rank1'], item['prize_rank1'], 
                        item['winners_rank2'], item['prize_rank2'],
                        item['winners_rank3'], item['prize_rank3'], 
                        item['winners_rank4'], item['prize_rank4'],
                        item['winners_rank5'], item['prize_rank5'], 
                        item['winners_rank6'], item['prize_rank6'],
                        item['winners_rank7'], item['prize_rank7'],
                        item['currency']
                    ))
                    
                    inserted_count += 1
                    
                    # Commit every 100 records
                    if inserted_count % 100 == 0:
                        conn.commit()
                        logger.info(f"Committed {inserted_count} records")
                
                except Exception as e:
                    logger.warning(f"Error inserting record: {e}")
                    continue
            
            # Final commit
            conn.commit()
            logger.info(f"Inserted {inserted_count} records in total")
            
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        conn.rollback()
    
    return inserted_count

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Import French Loto data')
    parser.add_argument('--file', required=True, help='Path to CSV file')
    args = parser.parse_args()
    
    # Connect to database
    conn = get_db_connection()
    if not conn:
        return
    
    # Create tables if they don't exist
    create_tables(conn)
    
    # Count existing records
    initial_count = count_existing_records(conn)
    
    # Process CSV file
    data = process_loto_csv(args.file)
    
    # Save to database
    if data:
        inserted = save_to_database(conn, data)
        
        # Count final records
        final_count = count_existing_records(conn)
        
        logger.info(f"Added {final_count - initial_count} new records to database")
        logger.info(f"Database now contains {final_count} French Loto drawings")
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    main()