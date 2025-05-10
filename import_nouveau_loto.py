"""
Script to import 'nouveau_loto.csv' data into the French Loto database
This file contains French Loto data with a semicolon-separated format
"""

import pandas as pd
from sqlalchemy import text
import database
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_french_date(date_str):
    """Convert date from French format DD/MM/YYYY to ISO format YYYY-MM-DD"""
    try:
        date_obj = datetime.strptime(date_str.strip(), '%d/%m/%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError as e:
        logger.error(f"Error converting date {date_str}: {e}")
        return None

def import_nouveau_loto_csv(filename='attached_assets/nouveau_loto.csv', batch_size=25, max_rows=100):
    """
    Import data from nouveau_loto.csv file to the database
    
    Args:
        filename: Path to the CSV file
        batch_size: Number of records to insert in each batch
        max_rows: Maximum number of rows to process (to avoid timeout)
    
    Returns:
        int: Number of records inserted
    """
    logger.info(f"Starting import from {filename}")
    
    try:
        # Read CSV file
        df = pd.read_csv(filename, sep=';', encoding='utf-8')
        logger.info(f"Successfully read {len(df)} rows from {filename}")
        
        # Get database connection
        conn = database.get_db_connection()
        if conn is None:
            logger.error("Could not connect to database")
            return 0
        
        # Create date column in ISO format
        df['date'] = df['date_de_tirage'].apply(convert_french_date)
        
        # Filter out rows with invalid dates
        df = df.dropna(subset=['date'])
        
        # Count records before Jan 1, 2023 (not future dates)
        future_cutoff = '2023-01-01'
        valid_df = df[df['date'] < future_cutoff]
        logger.info(f"Found {len(valid_df)} valid records before {future_cutoff}")
        
        # Track successful inserts
        total_inserted = 0
        
        # Limit number of rows to process to avoid timeout
        if max_rows and max_rows < len(valid_df):
            logger.info(f"Limiting to first {max_rows} records (out of {len(valid_df)} total)")
            valid_df = valid_df.head(max_rows)
            
        # Process in batches
        for i in range(0, len(valid_df), batch_size):
            batch = valid_df.iloc[i:i + batch_size]
            inserted = 0
            
            # Process each row in the batch
            for _, row in batch.iterrows():
                try:
                    # Extract values
                    draw_date = row['date']
                    number1 = int(row['boule_1'])
                    number2 = int(row['boule_2'])
                    number3 = int(row['boule_3'])
                    number4 = int(row['boule_4'])
                    number5 = int(row['boule_5'])
                    lucky_number = int(row['numero_chance'])
                    
                    # Determine draw number from the day of the week
                    # Since this format doesn't have explicit draw_num, we'll use 1 for typical draws
                    # and 2 for special draws if we can detect them
                    draw_num = 1
                    
                    # Check if record already exists
                    check_query = text("""
                        SELECT id FROM french_loto_drawings 
                        WHERE date = :date AND draw_num = :draw_num
                    """)
                    
                    result = conn.execute(check_query, {"date": draw_date, "draw_num": draw_num})
                    existing = result.fetchone()
                    
                    if existing:
                        logger.debug(f"Record for {draw_date} (draw #{draw_num}) already exists, skipping")
                        continue
                    
                    # Insert record
                    insert_query = text("""
                        INSERT INTO french_loto_drawings 
                        (date, n1, n2, n3, n4, n5, lucky, draw_num)
                        VALUES (:date, :n1, :n2, :n3, :n4, :n5, :lucky, :draw_num)
                    """)
                    
                    conn.execute(insert_query, {
                        "date": draw_date,
                        "n1": number1,
                        "n2": number2,
                        "n3": number3,
                        "n4": number4,
                        "n5": number5,
                        "lucky": lucky_number,
                        "draw_num": draw_num
                    })
                    
                    inserted += 1
                    
                except Exception as e:
                    logger.error(f"Error inserting row for {row.get('date', 'unknown date')}: {e}")
            
            # Commit batch
            conn.commit()
            total_inserted += inserted
            logger.info(f"Imported batch {i//batch_size + 1}/{(len(valid_df) + batch_size - 1)//batch_size}: {inserted} records")
        
        conn.close()
        logger.info(f"Import completed. Total records inserted: {total_inserted}")
        return total_inserted
    
    except Exception as e:
        logger.error(f"Error during import: {e}")
        return 0

def verify_import():
    """
    Verify the import by showing basic statistics
    """
    conn = database.get_db_connection()
    if conn is None:
        logger.error("Could not connect to database")
        return
    
    try:
        # Get count by year
        query = text("""
            SELECT EXTRACT(YEAR FROM date) as year, COUNT(*) as count
            FROM french_loto_drawings
            GROUP BY year
            ORDER BY year
        """)
        
        result = conn.execute(query)
        rows = result.fetchall()
        
        logger.info("French Loto drawings by year:")
        for row in rows:
            logger.info(f"  {int(row[0])}: {row[1]} drawings")
        
        # Get total count
        query = text("SELECT COUNT(*) FROM french_loto_drawings")
        result = conn.execute(query)
        total = result.fetchone()[0]
        logger.info(f"Total French Loto drawings in database: {total}")
        
        conn.close()
        
    except Exception as e:
        logger.error(f"Error verifying import: {e}")

def main():
    """
    Main function to import the nouveau_loto.csv file
    """
    filename = 'attached_assets/nouveau_loto.csv'
    
    if not os.path.exists(filename):
        logger.error(f"File {filename} not found")
        return
    
    # Import data with a limit to avoid timeout
    # We're starting with 100 records for initial testing
    batch_size = 25
    max_rows = 100
    
    num_imported = import_nouveau_loto_csv(filename=filename, batch_size=batch_size, max_rows=max_rows)
    
    if num_imported > 0:
        logger.info(f"Successfully imported {num_imported} records from {filename}")
        
        # Verify import
        verify_import()
    else:
        logger.error(f"Failed to import data from {filename}")

if __name__ == "__main__":
    main()