"""
Complete Euromillions import with proper date parsing for all 1846 records
"""
import pandas as pd
import os
from datetime import datetime
from database import init_db, EuromillionsDrawing, get_session, DB_AVAILABLE
from sqlalchemy import text

def parse_date_flexible(date_str):
    """Parse date from multiple formats"""
    try:
        date_str = str(date_str).strip()
        
        # Try YYYYMMDD format first
        if len(date_str) == 8 and date_str.isdigit():
            return datetime.strptime(date_str, '%Y%m%d').date()
        
        # Try DD/MM/YYYY format
        if '/' in date_str:
            return datetime.strptime(date_str, '%d/%m/%Y').date()
        
        # Try other common formats
        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y']:
            try:
                return datetime.strptime(date_str, fmt).date()
            except:
                continue
                
        return None
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

def clear_all_draws():
    """Remove all existing Euromillions draws from database"""
    if not DB_AVAILABLE:
        print("Database not available")
        return False
        
    session = get_session()
    try:
        deleted_count = session.query(EuromillionsDrawing).delete()
        session.commit()
        print(f"Cleared {deleted_count} existing Euromillions draws")
        return True
    except Exception as e:
        session.rollback()
        print(f"Error clearing draws: {str(e)}")
        return False
    finally:
        session.close()

def import_all_euromillions_data():
    """Import all 1846 Euromillions records with proper date parsing"""
    csv_path = "attached_assets/euromillion_all_1749131576125.csv"
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return False
    
    try:
        # Read CSV
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        print(f"Loaded {len(df)} records from CSV")
        
        # Process all records
        valid_draws = []
        skipped_records = []
        
        for idx, row in df.iterrows():
            try:
                # Parse date with flexible parser
                draw_date = parse_date_flexible(row['date_de_tirage'])
                if not draw_date:
                    skipped_records.append(f"Row {idx}: Invalid date '{row['date_de_tirage']}'")
                    continue
                
                # Extract and validate numbers
                n1 = int(row['boule_1'])
                n2 = int(row['boule_2'])
                n3 = int(row['boule_3'])
                n4 = int(row['boule_4'])
                n5 = int(row['boule_5'])
                
                # Extract and validate stars
                s1 = int(row['etoile_1'])
                s2 = int(row['etoile_2'])
                
                # Validate number ranges
                if not all(1 <= n <= 50 for n in [n1, n2, n3, n4, n5]):
                    skipped_records.append(f"Row {idx}: Invalid main numbers {[n1,n2,n3,n4,n5]}")
                    continue
                    
                if not all(1 <= s <= 12 for s in [s1, s2]):
                    skipped_records.append(f"Row {idx}: Invalid stars {[s1,s2]}")
                    continue
                
                # Map day of week
                day_of_week = map_day_abbreviation(row['jour_de_tirage'])
                
                # Add to valid draws
                valid_draws.append({
                    'date': draw_date,
                    'day_of_week': day_of_week,
                    'n1': n1, 'n2': n2, 'n3': n3, 'n4': n4, 'n5': n5,
                    's1': s1, 's2': s2
                })
                
            except Exception as e:
                skipped_records.append(f"Row {idx}: Processing error - {str(e)}")
                continue
        
        print(f"Successfully processed {len(valid_draws)} valid draws")
        print(f"Skipped {len(skipped_records)} records")
        
        if skipped_records and len(skipped_records) <= 10:
            print("Skipped records:")
            for record in skipped_records:
                print(f"  {record}")
        
        # Bulk insert all valid draws
        if valid_draws:
            session = get_session()
            try:
                session.bulk_insert_mappings(EuromillionsDrawing, valid_draws)
                session.commit()
                print(f"Successfully inserted {len(valid_draws)} Euromillions draws")
                return True
                
            except Exception as e:
                session.rollback()
                print(f"Error during bulk insert: {str(e)}")
                return False
            finally:
                session.close()
        else:
            print("No valid draws to insert")
            return False
            
    except Exception as e:
        print(f"Error processing CSV: {str(e)}")
        return False

def verify_complete_data():
    """Verify the complete database state"""
    if not DB_AVAILABLE:
        return
        
    session = get_session()
    try:
        total_count = session.query(EuromillionsDrawing).count()
        oldest = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date.asc()).first()
        newest = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date.desc()).first()
        
        print(f"\n=== Complete Database Verification ===")
        print(f"Total Euromillions draws: {total_count}")
        
        if oldest and newest:
            print(f"Date range: {oldest.date} to {newest.date}")
            print(f"Oldest: {oldest.date} - {oldest.n1},{oldest.n2},{oldest.n3},{oldest.n4},{oldest.n5} / {oldest.s1},{oldest.s2}")
            print(f"Newest: {newest.date} - {newest.n1},{newest.n2},{newest.n3},{newest.n4},{newest.n5} / {newest.s1},{newest.s2}")
        
        # Count by year
        year_counts = {}
        all_draws = session.query(EuromillionsDrawing).all()
        for draw in all_draws:
            year = draw.date.year
            year_counts[year] = year_counts.get(year, 0) + 1
        
        print(f"Draws by year:")
        for year in sorted(year_counts.keys()):
            print(f"  {year}: {year_counts[year]} draws")
        
    except Exception as e:
        print(f"Error verifying data: {str(e)}")
    finally:
        session.close()

def main():
    """Complete import of all Euromillions data"""
    print("Starting complete Euromillions data import...")
    
    init_db()
    
    if not DB_AVAILABLE:
        print("Database connection failed")
        return
    
    # Clear existing data
    print("\n1. Clearing existing data...")
    if not clear_all_draws():
        print("Failed to clear existing data")
        return
    
    # Import all data with proper date parsing
    print("\n2. Importing all 1846 records...")
    if not import_all_euromillions_data():
        print("Failed to import data")
        return
    
    # Verify complete import
    print("\n3. Verifying complete import...")
    verify_complete_data()
    
    print("\n✅ Complete Euromillions data import finished!")

if __name__ == "__main__":
    main()