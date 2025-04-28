import pandas as pd
import os
import sys
from datetime import datetime
from database import init_db, EuromillionsDrawing, session

def convert_french_date(date_str):
    """Convert date from French format to ISO format"""
    try:
        # Handle numeric format (YYYYMMDD)
        if len(date_str) == 8 and date_str.isdigit():
            return f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
        
        # Handle DD/MM/YYYY format
        elif '/' in date_str:
            parts = date_str.split('/')
            if len(parts) == 3:
                day, month, year = parts
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        # Handle DD-MM-YY format (like "16-09-23")
        elif '-' in date_str and len(date_str.split('-')) == 3:
            parts = date_str.split('-')
            if len(parts) == 3:
                day, month, year = parts
                # Handle two-digit year
                if len(year) == 2:
                    if int(year) > 50:  # Assume years > 50 are in the 1900s
                        year = "19" + year
                    else:  # Assume years <= 50 are in the 2000s
                        year = "20" + year
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        # Handle YYYYMMDD format without separators
        elif len(date_str) == 8:
            return f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
            
        # If all else fails, return as is
        return date_str
    except Exception as e:
        print(f"Error converting date {date_str}: {str(e)}")
        return date_str

def process_csv_files(directory):
    """Process all CSV files in the directory and load them into the database"""
    # Initialize the database
    init_db()
    
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    print(f"Found {len(csv_files)} CSV files in {directory}")
    
    total_records = 0
    processed_dates = set()
    
    # First, get all existing drawing dates from the database
    existing_drawings = session.query(EuromillionsDrawing.date).all()
    existing_dates = {str(date[0]) for date in existing_drawings}
    print(f"Found {len(existing_dates)} existing records in database")
    
    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        print(f"\nProcessing {file_path}...")
        
        # Try different encodings and separators
        encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']
        for encoding in encodings:
            try:
                # First, determine the separator
                with open(file_path, 'r', encoding=encoding) as f:
                    first_line = f.readline().strip()
                    separator = ';' if ';' in first_line else ','
                
                # Read only the first few rows to determine column names
                temp_df = pd.read_csv(file_path, sep=separator, encoding=encoding, nrows=5)
                
                # Identify the relevant columns
                date_col = None
                day_col = None
                n1_col = None
                n2_col = None
                n3_col = None
                n4_col = None
                n5_col = None
                s1_col = None
                s2_col = None
                
                # Check for French format columns
                if 'date_de_tirage' in temp_df.columns:
                    date_col = 'date_de_tirage'
                    day_col = 'jour_de_tirage' if 'jour_de_tirage' in temp_df.columns else None
                    n1_col, n2_col, n3_col, n4_col, n5_col = 'boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5'
                    s1_col, s2_col = 'etoile_1', 'etoile_2'
                else:
                    # Try to identify date column
                    date_candidates = [col for col in temp_df.columns if 'date' in col.lower()]
                    if date_candidates:
                        date_col = date_candidates[0]
                    
                    # Try to identify day column
                    day_candidates = [col for col in temp_df.columns if 'day' in col.lower() or 'jour' in col.lower()]
                    if day_candidates:
                        day_col = day_candidates[0]
                    
                    # Try to identify number columns
                    num_candidates = [col for col in temp_df.columns if 'n' in col.lower() or 'boule' in col.lower() or 'num' in col.lower()]
                    if len(num_candidates) >= 5:
                        n1_col, n2_col, n3_col, n4_col, n5_col = num_candidates[:5]
                    
                    # Try to identify star columns
                    star_candidates = [col for col in temp_df.columns if 's' in col.lower() or 'star' in col.lower() or 'etoile' in col.lower()]
                    if len(star_candidates) >= 2:
                        s1_col, s2_col = star_candidates[:2]
                
                # Continue only if we found all needed columns
                if not all([date_col, n1_col, n2_col, n3_col, n4_col, n5_col, s1_col, s2_col]):
                    print(f"Could not identify all required columns in {file_path}. Skipping file.")
                    print(f"Found: date_col={date_col}, n1_col={n1_col}, n2_col={n2_col}, n3_col={n3_col}, n4_col={n4_col}, n5_col={n5_col}, s1_col={s1_col}, s2_col={s2_col}")
                    break
                
                # Read only the needed columns
                usecols = [date_col, n1_col, n2_col, n3_col, n4_col, n5_col, s1_col, s2_col]
                if day_col:
                    usecols.append(day_col)
                
                df = pd.read_csv(file_path, sep=separator, encoding=encoding, usecols=usecols)
                print(f"Successfully read {len(df)} rows with encoding: {encoding}")
                
                # Process and insert records
                file_records = 0
                
                # Process in chunks to avoid timeouts
                chunk_size = 50
                for chunk_start in range(0, len(df), chunk_size):
                    chunk_end = min(chunk_start + chunk_size, len(df))
                    chunk = df.iloc[chunk_start:chunk_end]
                    
                    # Process each row in the chunk
                    for _, row in chunk.iterrows():
                        try:
                            # Convert date
                            date_str = str(row[date_col]).strip()
                            date = convert_french_date(date_str)
                            
                            # Skip if this date is already processed
                            if date in processed_dates or date in existing_dates:
                                continue
                            
                            # Get day of week if available
                            day_of_week = None
                            if day_col and day_col in row:
                                day_abbr = str(row[day_col]).strip()
                                day_mapping = {
                                    'LU': 'Monday',
                                    'MA': 'Tuesday',
                                    'ME': 'Wednesday',
                                    'JE': 'Thursday',
                                    'VE': 'Friday',
                                    'SA': 'Saturday',
                                    'DI': 'Sunday'
                                }
                                day_of_week = day_mapping.get(day_abbr)
                            
                            # Get numbers and stars
                            try:
                                # Check if the value is a string that starts with '-' 
                                # (like '-6-9-13-39-41-' from boules_gagnantes_en_ordre_croissant)
                                # and skip this row if so
                                for col in [n1_col, n2_col, n3_col, n4_col, n5_col, s1_col, s2_col]:
                                    val = str(row[col]).strip()
                                    if val.startswith('-') and val.count('-') > 1:
                                        raise ValueError(f"Column {col} contains formatted string '{val}' instead of a number")
                                
                                n1 = int(row[n1_col])
                                n2 = int(row[n2_col])
                                n3 = int(row[n3_col])
                                n4 = int(row[n4_col])
                                n5 = int(row[n5_col])
                                s1 = int(row[s1_col])
                                s2 = int(row[s2_col])
                            except (ValueError, TypeError) as e:
                                # Don't print detailed errors for the known issue
                                if "contains formatted string" not in str(e):
                                    print(f"Error converting numbers: {str(e)}")
                                continue
                            
                            # Create new record
                            drawing = EuromillionsDrawing(
                                date=date,
                                day_of_week=day_of_week,
                                n1=n1,
                                n2=n2,
                                n3=n3,
                                n4=n4,
                                n5=n5,
                                s1=s1,
                                s2=s2
                            )
                            
                            # Add to session
                            session.add(drawing)
                            file_records += 1
                            processed_dates.add(date)
                            
                        except Exception as e:
                            print(f"Error processing row: {str(e)}")
                            continue
                    
                    # Commit after each chunk
                    if file_records % chunk_size == 0:
                        try:
                            session.commit()
                        except Exception as e:
                            print(f"Error committing chunk: {str(e)}")
                            session.rollback()
                
                # Final commit for this file
                try:
                    session.commit()
                except Exception as e:
                    print(f"Error in final commit: {str(e)}")
                    session.rollback()
                
                print(f"Added {file_records} new records from {file_path}")
                total_records += file_records
                
                # Successfully processed the file, break out of the encoding loop
                break
                
            except Exception as e:
                print(f"Failed with encoding {encoding}: {str(e)}")
                continue
    
    print(f"\nTotal records added to database: {total_records}")
    
    # Create a processed CSV file for the app
    if total_records > 0:
        from database import get_all_drawings
        all_data = get_all_drawings()
        
        sample_path = 'sample_data/sample_euromillions.csv'
        all_data.to_csv(sample_path, index=False)
        print(f"Saved {len(all_data)} records to {sample_path} for app use")
        
        return True
    
    return False

def process_single_file(file_path):
    """Process a single CSV file and load it into the database"""
    init_db()
    
    total_records = 0
    processed_dates = set()
    
    # Get all existing drawing dates from the database
    existing_drawings = session.query(EuromillionsDrawing.date).all()
    existing_dates = {str(date[0]) for date in existing_drawings}
    print(f"Found {len(existing_dates)} existing records in database")
    
    print(f"\nProcessing {file_path}...")
    
    # Try different encodings and separators
    encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            # First, determine the separator
            with open(file_path, 'r', encoding=encoding) as f:
                first_line = f.readline().strip()
                separator = ';' if ';' in first_line else ','
            
            # Read only the first few rows to determine column names
            temp_df = pd.read_csv(file_path, sep=separator, encoding=encoding, nrows=5)
            
            # Identify the relevant columns
            date_col = None
            day_col = None
            n1_col = None
            n2_col = None
            n3_col = None
            n4_col = None
            n5_col = None
            s1_col = None
            s2_col = None
            
            # Check for French format columns
            if 'date_de_tirage' in temp_df.columns:
                date_col = 'date_de_tirage'
                day_col = 'jour_de_tirage' if 'jour_de_tirage' in temp_df.columns else None
                n1_col, n2_col, n3_col, n4_col, n5_col = 'boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5'
                s1_col, s2_col = 'etoile_1', 'etoile_2'
            else:
                # Try to identify date column
                date_candidates = [col for col in temp_df.columns if 'date' in col.lower()]
                if date_candidates:
                    date_col = date_candidates[0]
                
                # Try to identify day column
                day_candidates = [col for col in temp_df.columns if 'day' in col.lower() or 'jour' in col.lower()]
                if day_candidates:
                    day_col = day_candidates[0]
                
                # Try to identify number columns
                num_candidates = [col for col in temp_df.columns if 'n' in col.lower() or 'boule' in col.lower() or 'num' in col.lower()]
                if len(num_candidates) >= 5:
                    n1_col, n2_col, n3_col, n4_col, n5_col = num_candidates[:5]
                
                # Try to identify star columns
                star_candidates = [col for col in temp_df.columns if 's' in col.lower() or 'star' in col.lower() or 'etoile' in col.lower()]
                if len(star_candidates) >= 2:
                    s1_col, s2_col = star_candidates[:2]
            
            # Continue only if we found all needed columns
            if not all([date_col, n1_col, n2_col, n3_col, n4_col, n5_col, s1_col, s2_col]):
                print(f"Could not identify all required columns. Skipping file.")
                print(f"Found: date_col={date_col}, n1_col={n1_col}, n2_col={n2_col}, n3_col={n3_col}, n4_col={n4_col}, n5_col={n5_col}, s1_col={s1_col}, s2_col={s2_col}")
                break
            
            # Read only the needed columns
            usecols = [date_col, n1_col, n2_col, n3_col, n4_col, n5_col, s1_col, s2_col]
            if day_col:
                usecols.append(day_col)
            
            df = pd.read_csv(file_path, sep=separator, encoding=encoding, usecols=usecols)
            print(f"Successfully read {len(df)} rows with encoding: {encoding}")
            
            # Process and insert records
            file_records = 0
            
            # Process in chunks to avoid timeouts
            chunk_size = 50
            for chunk_start in range(0, len(df), chunk_size):
                chunk_end = min(chunk_start + chunk_size, len(df))
                chunk = df.iloc[chunk_start:chunk_end]
                
                # Process each row in the chunk
                for _, row in chunk.iterrows():
                    try:
                        # Convert date
                        date_str = str(row[date_col]).strip()
                        date = convert_french_date(date_str)
                        
                        # Skip if this date is already processed
                        if date in processed_dates or date in existing_dates:
                            continue
                        
                        # Get day of week if available
                        day_of_week = None
                        if day_col and day_col in row:
                            day_abbr = str(row[day_col]).strip()
                            day_mapping = {
                                'LU': 'Monday',
                                'MA': 'Tuesday',
                                'ME': 'Wednesday',
                                'JE': 'Thursday',
                                'VE': 'Friday',
                                'SA': 'Saturday',
                                'DI': 'Sunday'
                            }
                            day_of_week = day_mapping.get(day_abbr)
                        
                        # Get numbers and stars
                        try:
                            # Check if the value is a string that starts with '-' 
                            # (like '-6-9-13-39-41-' from boules_gagnantes_en_ordre_croissant)
                            # and skip this row if so
                            for col in [n1_col, n2_col, n3_col, n4_col, n5_col, s1_col, s2_col]:
                                val = str(row[col]).strip()
                                if val.startswith('-') and val.count('-') > 1:
                                    raise ValueError(f"Column {col} contains formatted string '{val}' instead of a number")
                            
                            n1 = int(row[n1_col])
                            n2 = int(row[n2_col])
                            n3 = int(row[n3_col])
                            n4 = int(row[n4_col])
                            n5 = int(row[n5_col])
                            s1 = int(row[s1_col])
                            s2 = int(row[s2_col])
                        except (ValueError, TypeError) as e:
                            # Don't print detailed errors for the known issue
                            if "contains formatted string" not in str(e):
                                print(f"Error converting numbers: {str(e)}")
                            continue
                        
                        # Create new record
                        drawing = EuromillionsDrawing(
                            date=date,
                            day_of_week=day_of_week,
                            n1=n1,
                            n2=n2,
                            n3=n3,
                            n4=n4,
                            n5=n5,
                            s1=s1,
                            s2=s2
                        )
                        
                        # Add to session
                        session.add(drawing)
                        file_records += 1
                        processed_dates.add(date)
                        
                    except Exception as e:
                        print(f"Error processing row: {str(e)}")
                        continue
                
                # Commit after each chunk
                if file_records % chunk_size == 0:
                    try:
                        session.commit()
                    except Exception as e:
                        print(f"Error committing chunk: {str(e)}")
                        session.rollback()
            
            # Final commit for this file
            try:
                session.commit()
            except Exception as e:
                print(f"Error in final commit: {str(e)}")
                session.rollback()
            
            print(f"Added {file_records} new records from {file_path}")
            total_records += file_records
            
            # Successfully processed the file, break out of the encoding loop
            break
            
        except Exception as e:
            print(f"Failed with encoding {encoding}: {str(e)}")
            continue
    
    print(f"\nTotal records added to database: {total_records}")
    
    # Create a processed CSV file for the app
    if total_records > 0:
        from database import get_all_drawings
        all_data = get_all_drawings()
        
        sample_path = 'sample_data/sample_euromillions.csv'
        all_data.to_csv(sample_path, index=False)
        print(f"Saved {len(all_data)} records to {sample_path} for app use")
        
        return True
    
    return False

if __name__ == "__main__":
    # Get path from command line or use default directory
    path = sys.argv[1] if len(sys.argv) > 1 else 'attached_assets'
    
    if os.path.isdir(path):
        # Process all CSV files in the directory
        success = process_csv_files(path)
    else:
        # Process a single file
        success = process_single_file(path)
    
    if success:
        print("Database loading completed successfully!")
    else:
        print("Failed to load data into database.")