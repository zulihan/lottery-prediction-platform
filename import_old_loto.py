"""
Script to specifically import the old French Loto data file (loto.csv)
"""

import pandas as pd
import database
from sqlalchemy import text
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_french_loto_table():
    """
    Delete all records from the french_loto_drawings table
    """
    conn = database.get_db_connection()
    
    if conn is None:
        print("Error: Could not connect to database")
        return False
    
    try:
        # Delete all records
        result = conn.execute(text("DELETE FROM french_loto_drawings"))
        
        deleted_count = result.rowcount
        conn.commit()
        
        print(f"Successfully deleted {deleted_count} French Loto drawings from the table")
        return True
        
    except Exception as e:
        print(f"Error clearing French Loto table: {str(e)}")
        return False
    finally:
        conn.close()

def import_loto_csv(filename='attached_assets/loto.csv', batch_size=50):
    """
    Import data from the loto.csv file
    """
    print(f"Processing French Loto file: {filename}")
    
    try:
        # Read the CSV file
        df = pd.read_csv(filename, sep=';', dtype=str, encoding='utf-8')
        record_count = len(df)
        print(f"Read {record_count} records from {filename}")
        
        # Get columns
        columns = df.columns.tolist()
        print(f"Columns: {', '.join(columns[:10])}...")
        
        number_cols = ['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']
        lucky_col = 'boule_complementaire'
        date_col = 'date_de_tirage'
        draw_col = '1er_ou_2eme_tirage'
        
        # Check if columns exist
        for col in number_cols + [lucky_col, date_col]:
            if col not in columns:
                print(f"ERROR: Required column {col} not found in the file")
                return 0
        
        print(f"Using column mapping: numbers={number_cols}, lucky={lucky_col}, date={date_col}")
        
        # Process in batches
        successful_imports = 0
        errors = 0
        
        for i in range(0, record_count, batch_size):
            end_idx = min(i + batch_size, record_count)
            batch = df.iloc[i:end_idx]
            print(f"Processing batch {i+1} to {end_idx} of {record_count}")
            
            for _, row in batch.iterrows():
                try:
                    # Parse date - format is YYYYMMDD
                    date_str = str(row[date_col]).strip()
                    draw_date = datetime.strptime(date_str, '%Y%m%d').date()
                    
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
                        if successful_imports % 100 == 0:
                            print(f"Successfully imported {successful_imports} records")
                    else:
                        errors += 1
                        
                except Exception as e:
                    errors += 1
                    if errors < 10:  # Limit error messages
                        print(f"Error processing row: {e}")
        
        print(f"Import completed. Successful: {successful_imports}, Errors: {errors}")
        return successful_imports
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return 0

def verify_import():
    """
    Verify the import by showing basic statistics
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
        
        print("\nFrench Loto Import Summary:")
        print("-------------------------")
        for row in result:
            print(f"{row.era}: {row.draw_count} drawings from {row.earliest_date} to {row.latest_date}")
        
        # Get total count
        result = conn.execute(text("SELECT COUNT(*) AS total FROM french_loto_drawings"))
        total = result.fetchone().total
        
        print(f"\nTotal French Loto drawings in database: {total}")
        
    except Exception as e:
        print(f"Error verifying import: {e}")
    finally:
        conn.close()

def main():
    """
    Main function: clear table and import loto.csv
    """
    print("Clearing French Loto table...")
    if clear_french_loto_table():
        print("Table cleared successfully")
    else:
        print("Failed to clear table")
        return
    
    print("\nImporting loto.csv...")
    imported = import_loto_csv()
    
    print(f"\nImported {imported} records from loto.csv")
    
    if imported > 0:
        verify_import()

if __name__ == "__main__":
    main()