"""
Script to import French Loto data from multiple CSV files
This script properly handles different file formats and ensures correct database import
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

def process_old_format(filename, batch_size=100):
    """
    Process old format French Loto file (YYYYMMDD dates)
    """
    print(f"\nProcessing old Loto file: {filename}")
    
    try:
        # Read CSV file
        df = pd.read_csv(filename, sep=';', encoding='utf-8', dtype=str)
        row_count = len(df)
        print(f"Read {row_count} rows from {filename}")
        
        # Get column names
        columns = df.columns.tolist()
        print(f"File contains columns: {', '.join(columns)}")
        
        # Find date column
        date_col = next((col for col in columns if 'date' in col.lower()), None)
        if not date_col:
            print(f"ERROR: Could not find date column in {filename}")
            return 0
            
        # Find number columns
        number_cols = []
        for i in range(1, 6):
            # Try common column naming patterns
            patterns = [f'boule_{i}', f'b{i}', f'n{i}', f'numero_{i}']
            for pattern in patterns:
                col = next((c for c in columns if pattern.lower() in c.lower()), None)
                if col:
                    number_cols.append(col)
                    break
        
        if len(number_cols) != 5:
            print(f"ERROR: Could not find all 5 number columns in {filename}")
            return 0
            
        # Find lucky number column
        lucky_col = next((col for col in columns if 'chance' in col.lower() or 'comp' in col.lower()), None)
        if not lucky_col:
            print(f"ERROR: Could not find lucky number column in {filename}")
            return 0
            
        print(f"Using columns: Date={date_col}, Numbers={number_cols}, Lucky={lucky_col}")
        
        # Determine date format
        sample_date = str(df[date_col].iloc[0])
        date_format = None
        for fmt in ['%Y%m%d', '%d/%m/%Y']:
            try:
                datetime.strptime(sample_date, fmt)
                date_format = fmt
                print(f"Using date format: {fmt}")
                break
            except ValueError:
                continue
                
        if not date_format:
            print(f"ERROR: Could not determine date format for {filename}")
            return 0
            
        # Process rows
        imported_count = 0
        errors = 0
        
        for _, row in df.iterrows():
            try:
                # Parse date
                date_str = str(row[date_col]).strip()
                draw_date = datetime.strptime(date_str, date_format).date()
                
                # Get numbers
                numbers = []
                for col in number_cols:
                    num_str = str(row[col]).strip()
                    if not num_str or not num_str.isdigit():
                        raise ValueError(f"Invalid number: '{num_str}'")
                    numbers.append(int(num_str))
                
                # Get lucky number
                lucky_str = str(row[lucky_col]).strip()
                if not lucky_str or not lucky_str.isdigit():
                    raise ValueError(f"Invalid lucky number: '{lucky_str}'")
                lucky = int(lucky_str)
                
                # Default draw number is 1
                draw_num = 1
                
                # Look for draw number indicator
                for col in columns:
                    if 'tirage' in col.lower():
                        tirage_value = str(row[col]).lower()
                        if '2' in tirage_value:
                            draw_num = 2
                            break
                
                # Add to database
                success = database.add_french_loto_drawing_with_details(
                    date=draw_date,
                    numbers=numbers,
                    lucky=lucky,
                    draw_num=draw_num
                )
                
                if success:
                    imported_count += 1
                    if imported_count % 100 == 0:
                        print(f"Imported {imported_count} records...")
                else:
                    errors += 1
                    
            except Exception as e:
                errors += 1
                if errors < 10:  # Limit the number of error messages
                    print(f"Error on row: {e}")
        
        print(f"Finished importing from {filename}")
        print(f"Successful imports: {imported_count}")
        print(f"Errors: {errors}")
        return imported_count
        
    except Exception as e:
        print(f"Error processing file {filename}: {e}")
        return 0

def process_newer_format(filename, batch_size=100):
    """
    Process newer format French Loto file (DD/MM/YYYY dates)
    """
    print(f"\nProcessing newer Loto file: {filename}")
    
    try:
        # Read CSV file
        df = pd.read_csv(filename, sep=';', encoding='utf-8', dtype=str)
        row_count = len(df)
        print(f"Read {row_count} rows from {filename}")
        
        # Get column names
        columns = df.columns.tolist()
        print(f"File contains columns: {', '.join(columns)}")
        
        # Find date column - try different naming patterns
        date_patterns = ['date', 'jour', 'date_de_tirage']
        date_col = None
        for pattern in date_patterns:
            date_col = next((col for col in columns if pattern.lower() in col.lower()), None)
            if date_col:
                break
                
        if not date_col:
            print(f"ERROR: Could not find date column in {filename}")
            return 0
            
        # Find number columns
        number_cols = []
        for i in range(1, 6):
            # Try common column naming patterns
            patterns = [f'boule_{i}', f'b{i}', f'n{i}']
            for pattern in patterns:
                col = next((c for c in columns if pattern.lower() in c.lower()), None)
                if col:
                    number_cols.append(col)
                    break
        
        if len(number_cols) != 5:
            print(f"ERROR: Could not find all 5 number columns in {filename}")
            return 0
            
        # Find lucky number column
        lucky_patterns = ['chance', 'complementaire', 'comp']
        lucky_col = None
        for pattern in lucky_patterns:
            lucky_col = next((col for col in columns if pattern.lower() in col.lower()), None)
            if lucky_col:
                break
                
        if not lucky_col:
            print(f"ERROR: Could not find lucky number column in {filename}")
            return 0
            
        print(f"Using columns: Date={date_col}, Numbers={number_cols}, Lucky={lucky_col}")
        
        # Process rows
        imported_count = 0
        errors = 0
        
        for i, row in df.iterrows():
            try:
                # Parse date - handle different formats
                date_str = str(row[date_col]).strip()
                
                # Skip weekday-only entries
                if date_str.upper() in ['LUNDI', 'MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI', 'DIMANCHE']:
                    continue
                    
                # Try different date formats
                draw_date = None
                for fmt in ['%d/%m/%Y', '%Y%m%d']:
                    try:
                        draw_date = datetime.strptime(date_str, fmt).date()
                        break
                    except ValueError:
                        continue
                        
                if not draw_date:
                    errors += 1
                    if errors < 10:
                        print(f"Could not parse date: '{date_str}'")
                    continue
                
                # Get numbers
                numbers = []
                for col in number_cols:
                    num_str = str(row[col]).strip()
                    if not num_str or not num_str.isdigit():
                        raise ValueError(f"Invalid number: '{num_str}'")
                    numbers.append(int(num_str))
                
                # Get lucky number
                lucky_str = str(row[lucky_col]).strip()
                if not lucky_str or not lucky_str.isdigit():
                    raise ValueError(f"Invalid lucky number: '{lucky_str}'")
                lucky = int(lucky_str)
                
                # Default draw number is 1
                draw_num = 1
                
                # Look for draw number indicator
                for col in columns:
                    if 'tirage' in col.lower():
                        tirage_value = str(row[col]).lower()
                        if '2' in tirage_value:
                            draw_num = 2
                            break
                
                # Add to database
                success = database.add_french_loto_drawing_with_details(
                    date=draw_date,
                    numbers=numbers,
                    lucky=lucky,
                    draw_num=draw_num
                )
                
                if success:
                    imported_count += 1
                    if imported_count % 100 == 0:
                        print(f"Imported {imported_count} records...")
                else:
                    errors += 1
                    
            except Exception as e:
                errors += 1
                if errors < 10:  # Limit the number of error messages
                    print(f"Error on row {i}: {e}")
        
        print(f"Finished importing from {filename}")
        print(f"Successful imports: {imported_count}")
        print(f"Errors: {errors}")
        return imported_count
        
    except Exception as e:
        print(f"Error processing file {filename}: {e}")
        return 0

def verify_import():
    """
    Verify French Loto data in database
    """
    conn = database.get_db_connection()
    
    if conn is None:
        print("Error: Could not connect to database")
        return
    
    try:
        # Get count by era
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
        print(f"Error verifying import: {str(e)}")
    finally:
        conn.close()

def main():
    """
    Main function to import French Loto data
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Import French Loto data')
    parser.add_argument('--clear', action='store_true', help='Clear the table before importing')
    parser.add_argument('--file', type=str, help='Specific file to import')
    parser.add_argument('--type', type=str, choices=['old', 'new'], help='File format type (old or new)')
    parser.add_argument('--verify', action='store_true', help='Only verify the data without importing')
    args = parser.parse_args()
    
    if args.verify:
        print("Verifying French Loto data in database...")
        verify_import()
        return
    
    if args.clear:
        print("Clearing French Loto table...")
        clear_french_loto_table()
    
    # Define available files
    all_files = [
        ('attached_assets/loto.csv', 'old'),           # Oldest data
        ('attached_assets/loto2017.csv', 'new'),       # 2017 data
        ('attached_assets/loto_201902.csv', 'new'),    # 2019 Feb data
        ('attached_assets/loto_201911.csv', 'new')     # 2019 Nov data
    ]
    
    # Import single file if specified, otherwise list available files
    if args.file:
        file_type = args.type if args.type else 'old'
        
        if file_type == 'old':
            imported = process_old_format(args.file)
        else:
            imported = process_newer_format(args.file)
            
        print(f"\nImported {imported} records from {args.file}")
        verify_import()
    else:
        print("\nAvailable files to import:")
        for i, (filename, file_type) in enumerate(all_files):
            print(f"{i+1}. {filename} (type: {file_type})")
        print("\nTo import a file, run:")
        print("python3 import_french_loto.py --file FILENAME --type TYPE")
        print("Example: python3 import_french_loto.py --file attached_assets/loto.csv --type old")

if __name__ == "__main__":
    main()