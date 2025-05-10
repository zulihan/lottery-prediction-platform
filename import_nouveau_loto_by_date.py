#!/usr/bin/env python
"""
Script to import data from the nouveau_loto.csv file within a specific date range.
This version allows processing specific date ranges to break up large imports.
"""

import os
import logging
import pandas as pd
from datetime import datetime, date
import database
from sqlalchemy import text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_french_date(date_str):
    """Convert date from French format DD/MM/YYYY to ISO format YYYY-MM-DD"""
    try:
        # Parse the date in French format (DD/MM/YYYY)
        day, month, year = date_str.strip().split('/')
        # Return in ISO format (YYYY-MM-DD)
        return f"{year}-{month}-{day}"
    except Exception as e:
        logger.error(f"Error converting date '{date_str}': {e}")
        return None

def get_day_of_week(day_abbr):
    """Convert French day abbreviation to full English day name."""
    day_mapping = {
        'LUNDI': 'Monday',
        'MARDI': 'Tuesday',
        'MERCREDI': 'Wednesday',
        'JEUDI': 'Thursday',
        'VENDREDI': 'Friday',
        'SAMEDI': 'Saturday',
        'DIMANCHE': 'Sunday'
    }
    
    # Strip whitespace and convert to title case to handle variations
    day_abbr = day_abbr.strip()
    
    for french_day, english_day in day_mapping.items():
        if day_abbr.startswith(french_day):
            return english_day
    
    return None

def import_nouveau_loto_csv(filename='attached_assets/nouveau_loto.csv', batch_size=25, max_rows=None, 
                           start_date=None, end_date=None):
    """
    Import data from the nouveau_loto.csv file for a specific date range

    Args:
        filename: Path to the CSV file
        batch_size: Number of records to insert in each batch
        max_rows: Maximum number of rows to process in total (None for all)
        start_date: Only import records on or after this date (YYYY-MM-DD format)
        end_date: Only import records on or before this date (YYYY-MM-DD format)
    
    Returns:
        int: Number of records imported
    """
    # Future date cutoff to prevent importing projections
    future_cutoff = date(2023, 1, 1)
    
    # Parse start and end dates if provided
    parsed_start_date = None
    parsed_end_date = None
    
    if start_date:
        try:
            parsed_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            logger.info(f"Filtering records on or after {parsed_start_date}")
        except ValueError:
            logger.warning(f"Invalid start_date format: {start_date}. Expected YYYY-MM-DD.")
    
    if end_date:
        try:
            parsed_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            logger.info(f"Filtering records on or before {parsed_end_date}")
        except ValueError:
            logger.warning(f"Invalid end_date format: {end_date}. Expected YYYY-MM-DD.")
            
    try:
        # Read the CSV file
        logger.info(f"Starting import from {filename}")
        df = pd.read_csv(filename, sep=';', encoding='utf-8')
        logger.info(f"Successfully read {len(df)} rows from {filename}")
        
        # Process the data
        records = []
        
        for _, row in df.iterrows():
            if len(records) == max_rows:
                break
            
            # Convert the date
            date_str = row['date_de_tirage'] if 'date_de_tirage' in row else None
            if not date_str:
                continue
                
            iso_date = convert_french_date(date_str)
            if not iso_date:
                continue
                
            # Check if date is in range
            record_date = datetime.strptime(iso_date, '%Y-%m-%d').date()
            
            # Skip records outside the specified date range
            if parsed_start_date and record_date < parsed_start_date:
                continue
                
            if parsed_end_date and record_date > parsed_end_date:
                continue
                
            # Skip future dates
            if record_date >= future_cutoff:
                continue
            
            # Extract numbers
            try:
                # The fixed positions for the numbers
                n1 = int(row['boule_1'])
                n2 = int(row['boule_2'])
                n3 = int(row['boule_3'])
                n4 = int(row['boule_4'])
                n5 = int(row['boule_5'])
                lucky = int(row['numero_chance'])
                
                # Default draw number (for multiple draws per day)
                draw_num = 1
                
                # Get day of week if available
                day_of_week = None
                if 'jour_de_tirage' in row:
                    day_of_week = get_day_of_week(row['jour_de_tirage'])
                
                # Get prize information if available
                winners_rank1 = int(row['nombre_de_gagnant_au_rang1']) if 'nombre_de_gagnant_au_rang1' in row and pd.notna(row['nombre_de_gagnant_au_rang1']) else 0
                prize_rank1 = float(str(row['rapport_du_rang1']).replace(',', '.')) if 'rapport_du_rang1' in row and pd.notna(row['rapport_du_rang1']) else 0.0
                
                # Add to records list
                records.append({
                    'date': iso_date,
                    'n1': n1,
                    'n2': n2,
                    'n3': n3,
                    'n4': n4,
                    'n5': n5,
                    'lucky': lucky,
                    'draw_num': draw_num,
                    'day_of_week': day_of_week,
                    'winners_rank1': winners_rank1,
                    'prize_rank1': prize_rank1
                })
            except Exception as e:
                logger.error(f"Error processing row: {e}")
                continue
        
        logger.info(f"Found {len(records)} valid records in specified date range")
        
        if max_rows:
            records = records[:max_rows]
            logger.info(f"Limiting to first {max_rows} records (out of {len(records)} total)")
        
        # Sort records by date (oldest first) to maintain chronological order
        records = sorted(records, key=lambda x: x['date'])
        
        # Insert records into the database
        conn = database.get_db_connection()
        if not conn:
            logger.error("Failed to connect to database")
            return 0
        
        # Insert in batches
        records_inserted = 0
        batches = [records[i:i+batch_size] for i in range(0, len(records), batch_size)]
        
        for batch_index, batch in enumerate(batches, 1):
            batch_inserted = 0
            
            for record in batch:
                try:
                    # Check if record already exists
                    query = text("""
                        SELECT COUNT(*) FROM french_loto_drawings 
                        WHERE date = :date AND draw_num = :draw_num
                    """)
                    
                    result = conn.execute(query, {
                        'date': record['date'],
                        'draw_num': record['draw_num']
                    })
                    
                    if result.scalar() > 0:
                        logger.info(f"Record for {record['date']} (draw #{record['draw_num']}) already exists, skipping")
                        continue
                    
                    # Insert the record
                    logger.info(f"Preparing to insert record for {record['date']} with numbers: {record['n1']}, {record['n2']}, {record['n3']}, {record['n4']}, {record['n5']}, {record['lucky']}")
                    
                    query = text("""
                        INSERT INTO french_loto_drawings 
                        (date, n1, n2, n3, n4, n5, lucky, draw_num) 
                        VALUES (:date, :n1, :n2, :n3, :n4, :n5, :lucky, :draw_num)
                        RETURNING id
                    """)
                    
                    params = {
                        'date': record['date'],
                        'n1': record['n1'],
                        'n2': record['n2'],
                        'n3': record['n3'],
                        'n4': record['n4'],
                        'n5': record['n5'],
                        'lucky': record['lucky'],
                        'draw_num': record['draw_num']
                    }
                    
                    logger.info(f"Running insert query with params: {params}")
                    result = conn.execute(query, params)
                    conn.commit()
                    
                    record_id = result.scalar()
                    logger.info(f"Successfully inserted record ID: {record_id}")
                    
                    records_inserted += 1
                    batch_inserted += 1
                    
                except Exception as e:
                    logger.error(f"Error inserting record: {e}")
                    conn.rollback()
            
            logger.info(f"Imported batch {batch_index}/{len(batches)}: {batch_inserted} records")
        
        conn.close()
        logger.info(f"Import completed. Total records inserted: {records_inserted}")
        return records_inserted
        
    except Exception as e:
        logger.error(f"Failed to import data from {filename}: {e}")
        return 0

def main():
    """Main function to import data from nouveau_loto.csv within a specific date range"""
    filename = 'attached_assets/nouveau_loto.csv'
    
    if not os.path.exists(filename):
        logger.error(f"File {filename} not found")
        return
    
    # Check the table structure to ensure we have the correct columns
    conn = database.get_db_connection()
    if conn is not None:
        try:
            query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'french_loto_drawings'
            """)
            result = conn.execute(query)
            columns = [row[0] for row in result.fetchall()]
            logger.info(f"Columns in french_loto_drawings table: {columns}")
            conn.close()
        except Exception as e:
            logger.error(f"Error checking table structure: {e}")
    
    # Import data for a specific date range (focus on 2012-2016 which is our gap)
    # Splitting into smaller chunks to avoid timeouts
    start_date = "2012-11-10"  # Continue from where we left off
    end_date = "2014-12-31"    # Next chunk
    
    batch_size = 25
    max_rows = None  # Import all records in the date range
    
    num_imported = import_nouveau_loto_csv(
        filename=filename, 
        batch_size=batch_size, 
        max_rows=max_rows,
        start_date=start_date,
        end_date=end_date
    )
    
    if num_imported > 0:
        logger.info(f"Successfully imported {num_imported} records from {start_date} to {end_date}")
    else:
        logger.error(f"Failed to import data from {filename} for date range {start_date} to {end_date}")

if __name__ == "__main__":
    main()