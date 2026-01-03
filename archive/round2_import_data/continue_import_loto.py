"""
Script to continue importing the old French Loto data file (loto.csv) from where it left off
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

def get_latest_imported_date():
    """
    Get the date of the most recently imported French Loto drawing
    """
    conn = database.get_db_connection()
    
    if conn is None:
        print("Error: Could not connect to database")
        return None
    
    try:
        result = conn.execute(text("SELECT MIN(date) AS earliest_date FROM french_loto_drawings"))
        row = result.fetchone()
        if row and row.earliest_date:
            earliest_date = row.earliest_date
            print(f"Earliest imported date: {earliest_date}")
            
            # Get the row count
            result = conn.execute(text("SELECT COUNT(*) AS count FROM french_loto_drawings"))
            count = result.fetchone().count
            print(f"Current count of French Loto drawings: {count}")
            
            return earliest_date
        else:
            print("No drawings found in the database")
            return None
    except Exception as e:
        print(f"Error getting latest date: {e}")
        return None
    finally:
        conn.close()

def continue_import_loto_csv(filename='attached_assets/loto.csv', batch_size=100, earliest_date=None):
    """
    Continue importing data from the loto.csv file, starting from before the earliest date in the database
    """
    print(f"Processing French Loto file: {filename}")
    
    try:
        # Read the CSV file
        df = pd.read_csv(filename, sep=';', dtype=str, encoding='utf-8')
        record_count = len(df)
        print(f"Read {record_count} records from {filename}")
        
        # Get columns
        number_cols = ['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']
        lucky_col = 'boule_complementaire'
        date_col = 'date_de_tirage'
        draw_col = '1er_ou_2eme_tirage'
        
        # Filter by date if needed
        if earliest_date:
            # Convert dates in dataframe
            df['parsed_date'] = pd.to_datetime(df[date_col], format='%Y%m%d')
            
            # Filter to only include dates before the earliest date
            cutoff_date = pd.Timestamp(earliest_date)
            df = df[df['parsed_date'] < cutoff_date]
            print(f"Filtered to {len(df)} records before {earliest_date}")
        
        # Process in batches
        successful_imports = 0
        errors = 0
        
        # Skip header row if present
        start_row = 1 if df.columns[0] == 'annee_numero_de_tirage' else 0
        
        for i in range(start_row, len(df), batch_size):
            end_idx = min(i + batch_size, len(df))
            batch = df.iloc[i:end_idx]
            print(f"Processing batch {i+1} to {end_idx} of {len(df)}")
            
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
            
            # After each batch, show progress
            print(f"Progress: {successful_imports} records imported successfully")
        
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
        
        # Get number frequency
        result = conn.execute(text("""
            WITH number_data AS (
                SELECT n1 as num FROM french_loto_drawings
                UNION ALL SELECT n2 FROM french_loto_drawings
                UNION ALL SELECT n3 FROM french_loto_drawings
                UNION ALL SELECT n4 FROM french_loto_drawings
                UNION ALL SELECT n5 FROM french_loto_drawings
            )
            SELECT num, COUNT(*) as frequency
            FROM number_data
            GROUP BY num
            ORDER BY frequency DESC
            LIMIT 10
        """))
        
        print("\nMost frequent numbers:")
        print("--------------------")
        for row in result:
            print(f"Number {row.num}: {row.frequency} occurrences")
            
        # Get lucky number frequency
        result = conn.execute(text("""
            SELECT lucky, COUNT(*) as frequency
            FROM french_loto_drawings
            GROUP BY lucky
            ORDER BY frequency DESC
            LIMIT 10
        """))
        
        print("\nMost frequent lucky numbers:")
        print("-------------------------")
        for row in result:
            print(f"Lucky {row.lucky}: {row.frequency} occurrences")
        
    except Exception as e:
        print(f"Error verifying import: {e}")
    finally:
        conn.close()

def main():
    """
    Main function: continue importing from loto.csv
    """
    # Get the earliest date currently in the database
    earliest_date = get_latest_imported_date()
    
    print("\nContinuing import of loto.csv...")
    imported = continue_import_loto_csv(earliest_date=earliest_date)
    
    print(f"\nImported {imported} additional records from loto.csv")
    
    if imported > 0:
        verify_import()

if __name__ == "__main__":
    main()