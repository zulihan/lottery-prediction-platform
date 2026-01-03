"""
Script to import French Loto data from multiple CSV files
This script handles batch imports to avoid timeout issues
"""

import argparse
import pandas as pd
import database
from sqlalchemy import text
import os
from datetime import datetime

def import_old_format(filename, batch_size=100):
    """
    Import data from the old format CSV file (YYYYMMDD dates)
    
    Args:
        filename: Path to the CSV file
        batch_size: Number of records to process in each batch
        
    Returns:
        int: Number of successfully imported records
    """
    print(f"Processing old Loto file: {filename}")
    
    try:
        # Read the file
        df = pd.read_csv(filename, sep=';', encoding='utf-8')
        print(f"Read {len(df)} rows from {filename}")
        
        # Check if the file has the expected columns
        required_cols = ['date_de_tirage', 'boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5', 'numero_chance']
        
        # Map columns if needed
        # This is where we handle different column names in different file formats
        col_mapping = {}
        
        # Get actual columns in file
        actual_cols = df.columns.tolist()
        
        # Try to find date column
        date_cols = [col for col in actual_cols if 'date' in col.lower()]
        if date_cols:
            col_mapping['date_de_tirage'] = date_cols[0]
        
        # Try to find number columns
        for i in range(1, 6):
            num_cols = [col for col in actual_cols if f'boule_{i}' in col.lower()]
            if num_cols:
                col_mapping[f'boule_{i}'] = num_cols[0]
            else:
                num_cols = [col for col in actual_cols if f'b{i}' in col.lower()]
                if num_cols:
                    col_mapping[f'boule_{i}'] = num_cols[0]
        
        # Try to find lucky number column
        lucky_cols = [col for col in actual_cols if 'chance' in col.lower()]
        if lucky_cols:
            col_mapping['numero_chance'] = lucky_cols[0]
        
        # Apply column mapping if needed
        if col_mapping:
            df = df.rename(columns=col_mapping)
        
        # Check for date format
        date_formats = ['%Y%m%d', '%d/%m/%Y']
        date_format = None
        
        # Try to determine date format
        sample_date = str(df['date_de_tirage'].iloc[0])
        for fmt in date_formats:
            try:
                datetime.strptime(sample_date, fmt)
                date_format = fmt
                print(f"Successfully converted dates using format '{fmt}'")
                break
            except ValueError:
                continue
        
        if date_format is None:
            print(f"ERROR: Could not determine date format for {filename}")
            return 0
        
        # Process in batches
        imported_count = 0
        
        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i+batch_size]
            
            for _, row in batch_df.iterrows():
                # Convert date
                try:
                    date_str = str(row['date_de_tirage'])
                    draw_date = datetime.strptime(date_str, date_format).date()
                except ValueError:
                    print(f"Warning: Invalid date format: {row['date_de_tirage']}")
                    continue
                
                # Get numbers
                try:
                    numbers = [
                        int(row['boule_1']), 
                        int(row['boule_2']), 
                        int(row['boule_3']), 
                        int(row['boule_4']), 
                        int(row['boule_5'])
                    ]
                    lucky = int(row['numero_chance'])
                except (ValueError, KeyError) as e:
                    print(f"Warning: Invalid number format in row: {e}")
                    continue
                
                # Determine draw number (default to 1)
                draw_num = 1
                if 'tirage' in row:
                    if row['tirage'] == '2ème tirage':
                        draw_num = 2
                
                # Add to database
                success = database.add_french_loto_drawing(
                    draw_date, 
                    numbers[0], numbers[1], numbers[2], numbers[3], numbers[4],
                    lucky,
                    draw_num=draw_num
                )
                
                if success:
                    imported_count += 1
            
            print(f"Imported {imported_count} records so far")
        
        return imported_count
                
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
        return 0

def import_newer_format(filename, batch_size=100):
    """
    Import data from newer format CSV file (DD/MM/YYYY dates)
    
    Args:
        filename: Path to the CSV file
        batch_size: Number of records to process in each batch
        
    Returns:
        int: Number of successfully imported records
    """
    print(f"Processing newer Loto file: {filename}")
    
    try:
        # Read the file
        df = pd.read_csv(filename, sep=';', encoding='utf-8')
        print(f"Read {len(df)} rows from {filename}")
        
        # Look for column names in newer formats
        date_col = None
        for col in df.columns:
            if 'date' in col.lower() or 'jour' in col.lower():
                date_col = col
                break
        
        if date_col is None:
            print(f"ERROR: Could not find date column in {filename}")
            return 0
        
        # Find number columns
        number_cols = []
        for i in range(1, 6):
            found = False
            for col in df.columns:
                if f'boule_{i}' in col.lower() or f'b{i}' in col.lower() or f'n{i}' in col.lower():
                    number_cols.append(col)
                    found = True
                    break
            if not found:
                print(f"WARNING: Could not find column for number {i}")
                return 0
        
        # Find lucky number column
        lucky_col = None
        for col in df.columns:
            if 'chance' in col.lower() or 'complementaire' in col.lower():
                lucky_col = col
                break
        
        if lucky_col is None:
            print(f"ERROR: Could not find lucky number column in {filename}")
            return 0
        
        # Find draw number column (for multiple draws per day)
        draw_col = None
        for col in df.columns:
            if 'tirage' in col.lower():
                draw_col = col
                break
        
        # Process in batches
        imported_count = 0
        
        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i+batch_size]
            
            for _, row in batch_df.iterrows():
                # Convert date
                try:
                    date_str = str(row[date_col])
                    
                    # Try different date formats
                    for fmt in ['%d/%m/%Y', '%Y%m%d']:
                        try:
                            draw_date = datetime.strptime(date_str, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        print(f"Warning: Invalid date format: {date_str}")
                        continue
                        
                except ValueError:
                    print(f"Warning: Invalid date format: {row[date_col]}")
                    continue
                
                # Get numbers
                try:
                    numbers = [int(row[col]) for col in number_cols]
                    lucky = int(row[lucky_col])
                except (ValueError, KeyError) as e:
                    print(f"Warning: Invalid number format in row: {e}")
                    continue
                
                # Determine draw number (default to 1)
                draw_num = 1
                if draw_col is not None and draw_col in row:
                    draw_value = row[draw_col]
                    if isinstance(draw_value, str) and '2' in draw_value.lower():
                        draw_num = 2
                
                # Add to database
                success = database.add_french_loto_drawing(
                    draw_date, 
                    numbers[0], numbers[1], numbers[2], numbers[3], numbers[4],
                    lucky,
                    draw_num=draw_num
                )
                
                if success:
                    imported_count += 1
            
            print(f"Imported {imported_count} records so far")
        
        return imported_count
                
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
        return 0

def verify_import():
    """
    Verify data was imported correctly
    """
    conn = database.get_db_connection()
    
    if conn is None:
        print("Error: Could not connect to database")
        return
    
    try:
        # Get count by decade
        result = conn.execute(text("""
            SELECT 
            CASE 
                WHEN EXTRACT(YEAR FROM date) < 1980 THEN '1976-1979'
                WHEN EXTRACT(YEAR FROM date) < 1990 THEN '1980-1989'
                WHEN EXTRACT(YEAR FROM date) < 2000 THEN '1990-1999'
                WHEN EXTRACT(YEAR FROM date) < 2010 THEN '2000-2009'
                WHEN EXTRACT(YEAR FROM date) < 2020 THEN '2010-2019'
                ELSE '2020+'
            END AS decade,
            COUNT(*) AS draw_count,
            MIN(date) AS earliest_date,
            MAX(date) AS latest_date
            FROM french_loto_drawings
            GROUP BY decade
            ORDER BY earliest_date
        """))
        
        print("\nImport Summary by Decade:")
        print("-------------------------")
        for row in result:
            print(f"{row.decade}: {row.draw_count} drawings from {row.earliest_date} to {row.latest_date}")
        
        # Get total count
        result = conn.execute(text("SELECT COUNT(*) AS total FROM french_loto_drawings"))
        total = result.fetchone().total
        
        print(f"\nTotal French Loto drawings in database: {total}")
        
    except Exception as e:
        print(f"Error verifying import: {str(e)}")
    finally:
        conn.close()

def main():
    """
    Main function to import all French Loto data
    """
    parser = argparse.ArgumentParser(description='Import French Loto data from CSV files')
    parser.add_argument('--clear', action='store_true', help='Clear the table before importing')
    parser.add_argument('--files', nargs='+', help='CSV files to import')
    args = parser.parse_args()
    
    # Clear the table if requested
    if args.clear:
        print("Clearing French Loto table...")
        conn = database.get_db_connection()
        
        if conn is None:
            print("Error: Could not connect to database")
            return
        
        try:
            result = conn.execute(text("DELETE FROM french_loto_drawings"))
            deleted_count = result.rowcount
            conn.commit()
            print(f"Successfully deleted {deleted_count} existing French Loto drawings from database")
        except Exception as e:
            print(f"Error clearing French Loto table: {str(e)}")
            return
        finally:
            conn.close()
    
    # Define all files to import if not specified
    files = args.files if args.files else [
        'attached_assets/loto.csv',
        'attached_assets/loto2017.csv',
        'attached_assets/loto_201902.csv',
        'attached_assets/loto_201911.csv'
    ]
    
    # Import each file
    total_imported = 0
    
    for filename in files:
        print(f"\nImporting French Loto data from {filename}...")
        
        # Determine format based on filename
        if '2019' in filename:
            imported = import_newer_format(filename)
        else:
            imported = import_old_format(filename)
        
        total_imported += imported
        print(f"Imported {imported} records from {filename}")
    
    print(f"\nTotal records imported: {total_imported}")
    
    # Verify the import
    verify_import()

if __name__ == "__main__":
    main()