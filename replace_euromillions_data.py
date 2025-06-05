"""
Script to replace all Euromillions draws in the database with data from the CSV file
"""
import pandas as pd
import os
from datetime import datetime
from database import init_db, EuromillionsDrawing, get_session, DB_AVAILABLE
from sqlalchemy import text

def parse_date(date_str):
    """Parse date from YYYYMMDD format to datetime.date"""
    try:
        return datetime.strptime(str(date_str), '%Y%m%d').date()
    except:
        return None

def map_day_abbreviation(day_abbrev):
    """Map French day abbreviations to full English day names"""
    day_mapping = {
        'LU': 'Monday',
        'MA': 'Tuesday', 
        'ME': 'Wednesday',
        'JE': 'Thursday',
        'VE': 'Friday',
        'SA': 'Saturday',
        'DI': 'Sunday'
    }
    return day_mapping.get(day_abbrev, day_abbrev)

def clear_existing_draws():
    """Remove all existing Euromillions draws from database"""
    if not DB_AVAILABLE:
        print("Database not available")
        return False
        
    session = get_session()
    try:
        # Delete all existing records
        deleted_count = session.query(EuromillionsDrawing).delete()
        session.commit()
        print(f"Deleted {deleted_count} existing Euromillions draws")
        return True
    except Exception as e:
        session.rollback()
        print(f"Error clearing existing draws: {str(e)}")
        return False
    finally:
        session.close()

def load_csv_data(csv_path):
    """Load and parse the CSV data"""
    try:
        # Read CSV with semicolon separator
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        print(f"Loaded {len(df)} records from CSV")
        
        # Extract required columns
        draws_data = []
        for _, row in df.iterrows():
            try:
                # Parse date
                draw_date = parse_date(row['date_de_tirage'])
                if not draw_date:
                    continue
                
                # Map day of week
                day_of_week = map_day_abbreviation(row['jour_de_tirage'])
                
                # Extract numbers and stars
                n1 = int(row['boule_1'])
                n2 = int(row['boule_2'])
                n3 = int(row['boule_3'])
                n4 = int(row['boule_4'])
                n5 = int(row['boule_5'])
                s1 = int(row['etoile_1'])
                s2 = int(row['etoile_2'])
                
                # Validate ranges
                if all(1 <= n <= 50 for n in [n1, n2, n3, n4, n5]) and all(1 <= s <= 12 for s in [s1, s2]):
                    draws_data.append({
                        'date': draw_date,
                        'day_of_week': day_of_week,
                        'n1': n1,
                        'n2': n2,
                        'n3': n3,
                        'n4': n4,
                        'n5': n5,
                        's1': s1,
                        's2': s2
                    })
                else:
                    print(f"Invalid number ranges for date {draw_date}: numbers={[n1,n2,n3,n4,n5]}, stars={[s1,s2]}")
                    
            except Exception as e:
                print(f"Error processing row: {str(e)}")
                continue
        
        print(f"Successfully parsed {len(draws_data)} valid draws")
        return draws_data
        
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")
        return []

def insert_draws(draws_data):
    """Insert the new draws into the database"""
    if not DB_AVAILABLE:
        print("Database not available")
        return False
        
    session = get_session()
    try:
        inserted_count = 0
        batch_size = 100
        
        for i in range(0, len(draws_data), batch_size):
            batch = draws_data[i:i + batch_size]
            
            for draw_data in batch:
                # Check if draw already exists (shouldn't happen after clearing, but safety check)
                existing = session.query(EuromillionsDrawing).filter_by(date=draw_data['date']).first()
                if existing:
                    continue
                
                # Create new draw
                new_draw = EuromillionsDrawing(
                    date=draw_data['date'],
                    day_of_week=draw_data['day_of_week'],
                    n1=draw_data['n1'],
                    n2=draw_data['n2'],
                    n3=draw_data['n3'],
                    n4=draw_data['n4'],
                    n5=draw_data['n5'],
                    s1=draw_data['s1'],
                    s2=draw_data['s2']
                )
                session.add(new_draw)
                inserted_count += 1
            
            # Commit batch
            session.commit()
            print(f"Inserted batch {i//batch_size + 1}: {len(batch)} draws")
        
        print(f"Successfully inserted {inserted_count} Euromillions draws")
        return True
        
    except Exception as e:
        session.rollback()
        print(f"Error inserting draws: {str(e)}")
        return False
    finally:
        session.close()

def verify_data():
    """Verify the inserted data"""
    if not DB_AVAILABLE:
        print("Database not available for verification")
        return
        
    session = get_session()
    try:
        # Count total records
        total_count = session.query(EuromillionsDrawing).count()
        print(f"Total Euromillions draws in database: {total_count}")
        
        # Show date range
        oldest = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date.asc()).first()
        newest = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date.desc()).first()
        
        if oldest and newest:
            print(f"Date range: {oldest.date} to {newest.date}")
            print(f"Oldest draw: {oldest.date} - Numbers: {oldest.n1},{oldest.n2},{oldest.n3},{oldest.n4},{oldest.n5} Stars: {oldest.s1},{oldest.s2}")
            print(f"Newest draw: {newest.date} - Numbers: {newest.n1},{newest.n2},{newest.n3},{newest.n4},{newest.n5} Stars: {newest.s1},{newest.s2}")
        
    except Exception as e:
        print(f"Error verifying data: {str(e)}")
    finally:
        session.close()

def main():
    """Main function to replace all Euromillions data"""
    print("Starting Euromillions data replacement...")
    
    # Initialize database
    init_db()
    
    if not DB_AVAILABLE:
        print("Database connection failed. Cannot proceed.")
        return
    
    # CSV file path
    csv_path = "attached_assets/euromillion_all_1749131576125.csv"
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return
    
    # Step 1: Clear existing data
    print("\n1. Clearing existing Euromillions draws...")
    if not clear_existing_draws():
        print("Failed to clear existing data. Aborting.")
        return
    
    # Step 2: Load CSV data
    print("\n2. Loading data from CSV...")
    draws_data = load_csv_data(csv_path)
    
    if not draws_data:
        print("No valid data found in CSV. Aborting.")
        return
    
    # Step 3: Insert new data
    print("\n3. Inserting new Euromillions draws...")
    if not insert_draws(draws_data):
        print("Failed to insert new data.")
        return
    
    # Step 4: Verify data
    print("\n4. Verifying inserted data...")
    verify_data()
    
    print("\n✅ Euromillions data replacement completed successfully!")

if __name__ == "__main__":
    main()