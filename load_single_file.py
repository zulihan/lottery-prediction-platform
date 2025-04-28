import pandas as pd
import os
import sys
from datetime import datetime
from database import init_db, EuromillionsDrawing, session

def convert_french_date(date_str):
    """Convert date from French format DD/MM/YYYY to ISO format YYYY-MM-DD"""
    try:
        if len(date_str) == 8:  # Format like "20110506"
            return f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
        elif '/' in date_str:  # Format like "DD/MM/YYYY"
            day, month, year = date_str.split('/')
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            return date_str
    except Exception as e:
        print(f"Error converting date {date_str}: {str(e)}")
        return date_str

def process_file(file_path):
    """Process a single CSV file and load it into the database"""
    try:
        print(f"Reading file: {file_path}")
        
        # Try different encodings
        encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']
        separator = None
        df = None
        
        for encoding in encodings:
            try:
                # Determine the separator by examining the first line
                with open(file_path, 'r', encoding=encoding) as f:
                    first_line = f.readline().strip()
                    separator = ';' if ';' in first_line else ','
                
                # Read the CSV file
                df = pd.read_csv(file_path, sep=separator, encoding=encoding)
                print(f"Successfully read file with encoding: {encoding}")
                print(f"Using separator: {separator}")
                break
            except Exception as e:
                print(f"Failed with encoding {encoding}: {str(e)}")
        
        if df is None:
            raise Exception("Could not read file with any encoding")
        
        print(f"File columns: {', '.join(df.columns)}")
        print(f"File shape: {df.shape}")
        
        # Determine the format and extract relevant columns
        if 'date_de_tirage' in df.columns:
            # French format
            print("Detected French format")
            date_col = 'date_de_tirage'
            day_col = 'jour_de_tirage' if 'jour_de_tirage' in df.columns else None
            n1_col, n2_col, n3_col, n4_col, n5_col = 'boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5'
            s1_col, s2_col = 'etoile_1', 'etoile_2'
        else:
            # Try to identify columns
            print("Attempting to identify columns...")
            
            # Find date column
            date_candidates = [col for col in df.columns if 'date' in col.lower()]
            date_col = date_candidates[0] if date_candidates else None
            
            # Find day column
            day_col = next((col for col in df.columns if 'day' in col.lower() or 'jour' in col.lower()), None)
            
            # Find number columns
            num_cols = [col for col in df.columns if 'n' in col.lower() or 'number' in col.lower() or 'boule' in col.lower()]
            if len(num_cols) >= 5:
                n1_col, n2_col, n3_col, n4_col, n5_col = num_cols[:5]
            else:
                print(f"Could not identify number columns. Available columns: {', '.join(df.columns)}")
                return 0
            
            # Find star columns
            star_cols = [col for col in df.columns if 's' in col.lower() or 'star' in col.lower() or 'etoile' in col.lower()]
            if len(star_cols) >= 2:
                s1_col, s2_col = star_cols[:2]
            else:
                print(f"Could not identify star columns. Available columns: {', '.join(df.columns)}")
                return 0
        
        # Check if we have all required columns
        if not all([date_col, n1_col, n2_col, n3_col, n4_col, n5_col, s1_col, s2_col]):
            print("Missing required columns")
            return 0
        
        # Add new records to the database
        count = 0
        for i, row in df.iterrows():
            try:
                # Get date and convert if needed
                date_str = str(row[date_col]).strip()
                date = convert_french_date(date_str)
                
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
                
                # Check if this drawing already exists
                existing = session.query(EuromillionsDrawing).filter_by(date=date).first()
                if existing:
                    continue
                
                # Get numbers and stars
                n1 = int(row[n1_col])
                n2 = int(row[n2_col])
                n3 = int(row[n3_col])
                n4 = int(row[n4_col])
                n5 = int(row[n5_col])
                s1 = int(row[s1_col])
                s2 = int(row[s2_col])
                
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
                count += 1
                
                # Commit every 100 records to avoid timeouts
                if count % 100 == 0:
                    session.commit()
                    print(f"Committed {count} records so far...")
                
            except Exception as e:
                print(f"Error processing row {i}: {str(e)}")
                continue
        
        # Final commit
        if count % 100 != 0:
            session.commit()
        
        print(f"Successfully added {count} new records from {file_path}")
        return count
        
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        session.rollback()
        return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_single_file.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
        
    # Initialize database
    init_db()
    
    # Process the file
    count = process_file(file_path)
    print(f"Added {count} new records to the database")