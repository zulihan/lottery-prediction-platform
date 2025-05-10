"""
Script to import all French Loto data from attached_assets/loto.csv
This script processes the file in small batches from the earliest date
to ensure complete import of the entire historical dataset
"""

import pandas as pd
import database
from sqlalchemy import text
import os
from datetime import datetime
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_current_import_status():
    """
    Get the current status of the French Loto data import
    
    Returns:
        tuple: (count, earliest_date, latest_date)
    """
    conn = database.get_db_connection()
    
    if conn is None:
        print("Error: Could not connect to database")
        return 0, None, None
    
    try:
        result = conn.execute(text("""
            SELECT 
                COUNT(*) AS count,
                MIN(date) AS earliest_date,
                MAX(date) AS latest_date
            FROM french_loto_drawings
        """))
        row = result.fetchone()
        
        if row:
            count = row[0] if row[0] is not None else 0
            earliest_date = row[1]
            latest_date = row[2]
            
            print(f"Current French Loto database status:")
            print(f"Total drawings: {count}")
            if earliest_date and latest_date:
                print(f"Date range: {earliest_date} to {latest_date}")
            
            return count, earliest_date, latest_date
        else:
            print("No drawings found in the database")
            return 0, None, None
    except Exception as e:
        print(f"Error getting database status: {e}")
        return 0, None, None
    finally:
        conn.close()

def import_loto_csv_in_batches(filename='attached_assets/loto.csv', batch_size=20, start_row=0, total_rows=None):
    """
    Import all data from the loto.csv file in small batches
    
    Args:
        filename: Path to the CSV file
        batch_size: Number of records to process in each batch
        start_row: Row to start processing from (to resume interrupted imports)
        total_rows: Total number of rows to process (default: all rows)
        
    Returns:
        int: Number of records imported
    """
    print(f"Reading French Loto file: {filename}")
    
    try:
        # Read the CSV file
        df = pd.read_csv(filename, sep=';', dtype=str, encoding='utf-8')
        record_count = len(df)
        print(f"Found {record_count} records in {filename}")
        
        # Get columns
        number_cols = ['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']
        lucky_col = 'boule_complementaire'
        date_col = 'date_de_tirage'
        draw_col = '1er_ou_2eme_tirage'
        
        # Limit rows to process if specified
        if total_rows is not None:
            end_row = min(start_row + total_rows, record_count)
        else:
            end_row = record_count
        
        # Sort by date (assuming date is in YYYYMMDD format)
        df['date_value'] = pd.to_datetime(df[date_col], format='%Y%m%d', errors='coerce')
        df = df.sort_values('date_value')
        
        print(f"Processing rows {start_row} to {end_row} of {record_count}")
        
        # Track progress
        successful_imports = 0
        errors = 0
        
        # Process in batches from the beginning of the file
        for i in range(start_row, end_row, batch_size):
            batch_end = min(i + batch_size, end_row)
            batch = df.iloc[i:batch_end]
            print(f"Processing batch {i+1} to {batch_end} of {end_row}")
            
            for _, row in batch.iterrows():
                try:
                    # Parse date - format is YYYYMMDD
                    date_str = str(row[date_col]).strip()
                    try:
                        draw_date = datetime.strptime(date_str, '%Y%m%d').date()
                    except ValueError:
                        print(f"Invalid date format: {date_str}, skipping")
                        errors += 1
                        continue
                    
                    # Get numbers
                    numbers = []
                    for col in number_cols:
                        num_str = str(row[col]).strip()
                        if not num_str or not num_str.isdigit():
                            raise ValueError(f"Invalid number: '{num_str}' in column {col}")
                        numbers.append(int(num_str))
                    
                    # Get lucky number
                    lucky_str = str(row[lucky_col]).strip()
                    if not lucky_str or not lucky_str.isdigit():
                        raise ValueError(f"Invalid lucky number: '{lucky_str}'")
                    lucky = int(lucky_str)
                    
                    # Determine draw number (1=1st draw, 2=2nd draw)
                    draw_num = 1
                    if draw_col in row:
                        draw_value = str(row[draw_col]).strip()
                        if draw_value == '2':
                            draw_num = 2
                    
                    # Add to database
                    success = database.add_french_loto_drawing_with_details(
                        date=draw_date,
                        numbers=numbers,
                        lucky=lucky,
                        draw_num=draw_num
                    )
                    
                    if success:
                        successful_imports += 1
                    else:
                        errors += 1
                        
                except Exception as e:
                    errors += 1
                    print(f"Error processing row: {e}")
            
            # After each batch, show progress
            print(f"Progress: {successful_imports} records imported successfully, {errors} errors")
            time.sleep(0.1)  # Small pause to avoid timeouts
        
        print(f"Import batch completed. Successful: {successful_imports}, Errors: {errors}")
        return successful_imports
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return 0

def import_whole_file(batch_size=20, max_rows_per_run=200):
    """
    Import the entire file in multiple runs with small batches
    
    Args:
        batch_size: Size of each batch to process
        max_rows_per_run: Maximum rows to process in a single run
    """
    filename = 'attached_assets/loto.csv'
    
    # Get the total number of records in the file
    try:
        df = pd.read_csv(filename, sep=';', nrows=1)
        total_records = sum(1 for _ in open(filename, 'r')) - 1  # Subtract header
        print(f"Total records in file: {total_records}")
    except Exception as e:
        print(f"Error getting file info: {e}")
        return
    
    # Get current import status
    current_count, earliest_date, latest_date = get_current_import_status()
    
    # Calculate how many records we still need to process
    remaining = total_records - current_count
    if remaining <= 0:
        print("All records have already been imported.")
        return
    
    print(f"Remaining records to import: {remaining}")
    
    # Import in chunks from the oldest records first
    start_row = 1  # Skip header
    
    while start_row < total_records:
        print(f"\n--- Importing batch starting at row {start_row} ---")
        imported = import_loto_csv_in_batches(
            batch_size=batch_size,
            start_row=start_row,
            total_rows=max_rows_per_run
        )
        
        if imported == 0:
            print("No records imported in this batch, stopping")
            break
        
        # Update starting point for next batch
        start_row += max_rows_per_run
        
        # Show current status
        get_current_import_status()
    
    print("Import process completed!")

def get_era_statistics():
    """
    Get statistics about the data by era
    """
    conn = database.get_db_connection()
    
    if conn is None:
        print("Error: Could not connect to database")
        return
    
    try:
        # Get era statistics
        result = conn.execute(text("""
            SELECT 
            CASE 
                WHEN EXTRACT(YEAR FROM date) < 1980 THEN '1976-1979'
                WHEN EXTRACT(YEAR FROM date) < 1990 THEN '1980-1989'
                WHEN EXTRACT(YEAR FROM date) < 2000 THEN '1990-1999'
                WHEN EXTRACT(YEAR FROM date) < 2010 THEN '2000-2009'
                WHEN EXTRACT(YEAR FROM date) < 2020 THEN '2010-2019'
                ELSE '2020+'
            END AS era,
            COUNT(*) AS draw_count,
            MIN(date) AS earliest_date,
            MAX(date) AS latest_date
            FROM french_loto_drawings
            GROUP BY era
            ORDER BY earliest_date
        """))
        
        print("\nFrench Loto Import Summary by Era:")
        print("----------------------------------")
        for row in result:
            print(f"{row.era}: {row.draw_count} drawings from {row.earliest_date} to {row.latest_date}")
        
        # Get total count
        result = conn.execute(text("SELECT COUNT(*) AS total FROM french_loto_drawings"))
        total = result.fetchone().total
        
        print(f"\nTotal French Loto drawings in database: {total}")
        
    except Exception as e:
        print(f"Error getting statistics: {e}")
    finally:
        conn.close()

def calculate_top_numbers():
    """
    Calculate and display the most frequent numbers and lucky numbers
    """
    conn = database.get_db_connection()
    
    if conn is None:
        print("Error: Could not connect to database")
        return
    
    try:
        # Create temp table with all numbers
        conn.execute(text("""
            WITH all_numbers AS (
                SELECT number1 as number FROM french_loto_drawings
                UNION ALL
                SELECT number2 FROM french_loto_drawings
                UNION ALL
                SELECT number3 FROM french_loto_drawings
                UNION ALL
                SELECT number4 FROM french_loto_drawings
                UNION ALL
                SELECT number5 FROM french_loto_drawings
            )
            SELECT 
                number, 
                COUNT(*) as frequency
            FROM all_numbers
            GROUP BY number
            ORDER BY frequency DESC
            LIMIT 10
        """))
        
        # Get top 10 main numbers
        result = conn.execute(text("""
            WITH all_numbers AS (
                SELECT number1 as number FROM french_loto_drawings
                UNION ALL
                SELECT number2 FROM french_loto_drawings
                UNION ALL
                SELECT number3 FROM french_loto_drawings
                UNION ALL
                SELECT number4 FROM french_loto_drawings
                UNION ALL
                SELECT number5 FROM french_loto_drawings
            )
            SELECT 
                number, 
                COUNT(*) as frequency
            FROM all_numbers
            GROUP BY number
            ORDER BY frequency DESC
            LIMIT 10
        """))
        
        print("\nTop 10 Most Frequent Main Numbers:")
        for i, row in enumerate(result):
            print(f"{i+1}. Number {row.number}: {row.frequency} occurrences")
        
        # Get top 5 lucky numbers
        result = conn.execute(text("""
            SELECT 
                lucky_number, 
                COUNT(*) as frequency
            FROM french_loto_drawings
            GROUP BY lucky_number
            ORDER BY frequency DESC
            LIMIT 5
        """))
        
        print("\nTop 5 Most Frequent Lucky Numbers:")
        for i, row in enumerate(result):
            print(f"{i+1}. Lucky Number {row.lucky_number}: {row.frequency} occurrences")
        
    except Exception as e:
        print(f"Error calculating top numbers: {e}")
    finally:
        conn.close()

def main():
    """
    Main function to import all French Loto data
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Import French Loto data')
    parser.add_argument('--start', type=int, default=1, help='Starting row in the CSV file (default: 1)')
    parser.add_argument('--batch', type=int, default=20, help='Batch size (default: 20)')
    parser.add_argument('--max', type=int, default=100, help='Maximum rows to process in this run (default: 100)')
    args = parser.parse_args()
    
    # Get current status
    get_current_import_status()
    
    # Import data from the specified starting point
    print(f"\n--- Importing batch starting at row {args.start} ---")
    imported = import_loto_csv_in_batches(
        batch_size=args.batch,
        start_row=args.start,
        total_rows=args.max
    )
    
    print(f"Imported {imported} records in this batch")
    
    # Get statistics
    get_era_statistics()
    
    # Calculate top numbers
    calculate_top_numbers()

if __name__ == "__main__":
    main()