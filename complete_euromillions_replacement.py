"""
Complete the Euromillions data replacement with optimized batch processing
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

def get_existing_dates():
    """Get all existing draw dates to avoid duplicates"""
    if not DB_AVAILABLE:
        return set()
        
    session = get_session()
    try:
        existing_dates = session.query(EuromillionsDrawing.date).all()
        return {date[0] for date in existing_dates}
    except Exception as e:
        print(f"Error getting existing dates: {str(e)}")
        return set()
    finally:
        session.close()

def bulk_insert_remaining_data():
    """Complete the data insertion with bulk operations"""
    if not DB_AVAILABLE:
        print("Database not available")
        return False
        
    # Load CSV data
    csv_path = "attached_assets/euromillion_all_1749131576125.csv"
    
    try:
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        print(f"Loaded {len(df)} records from CSV")
        
        # Get existing dates to avoid duplicates
        existing_dates = get_existing_dates()
        print(f"Found {len(existing_dates)} existing draws in database")
        
        # Prepare data for bulk insert
        bulk_data = []
        for _, row in df.iterrows():
            try:
                draw_date = parse_date(row['date_de_tirage'])
                if not draw_date or draw_date in existing_dates:
                    continue
                
                # Validate and extract data
                n1, n2, n3, n4, n5 = int(row['boule_1']), int(row['boule_2']), int(row['boule_3']), int(row['boule_4']), int(row['boule_5'])
                s1, s2 = int(row['etoile_1']), int(row['etoile_2'])
                
                # Validate ranges
                if all(1 <= n <= 50 for n in [n1, n2, n3, n4, n5]) and all(1 <= s <= 12 for s in [s1, s2]):
                    bulk_data.append({
                        'date': draw_date,
                        'day_of_week': map_day_abbreviation(row['jour_de_tirage']),
                        'n1': n1, 'n2': n2, 'n3': n3, 'n4': n4, 'n5': n5,
                        's1': s1, 's2': s2
                    })
                    
            except Exception as e:
                continue
        
        print(f"Prepared {len(bulk_data)} new draws for insertion")
        
        if not bulk_data:
            print("No new data to insert")
            return True
        
        # Bulk insert using SQLAlchemy core for speed
        session = get_session()
        try:
            session.bulk_insert_mappings(EuromillionsDrawing, bulk_data)
            session.commit()
            print(f"Successfully inserted {len(bulk_data)} new draws")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error during bulk insert: {str(e)}")
            return False
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error processing CSV: {str(e)}")
        return False

def verify_final_data():
    """Verify the final database state"""
    if not DB_AVAILABLE:
        return
        
    session = get_session()
    try:
        total_count = session.query(EuromillionsDrawing).count()
        oldest = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date.asc()).first()
        newest = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date.desc()).first()
        
        print(f"\n=== Final Database State ===")
        print(f"Total Euromillions draws: {total_count}")
        if oldest and newest:
            print(f"Date range: {oldest.date} to {newest.date}")
            print(f"Oldest: {oldest.date} - {oldest.n1},{oldest.n2},{oldest.n3},{oldest.n4},{oldest.n5} / {oldest.s1},{oldest.s2}")
            print(f"Newest: {newest.date} - {newest.n1},{newest.n2},{newest.n3},{newest.n4},{newest.n5} / {newest.s1},{newest.s2}")
        
    except Exception as e:
        print(f"Error verifying data: {str(e)}")
    finally:
        session.close()

def main():
    """Complete the Euromillions data replacement"""
    print("Completing Euromillions data replacement...")
    
    init_db()
    
    if not DB_AVAILABLE:
        print("Database connection failed")
        return
    
    # Complete the data insertion
    if bulk_insert_remaining_data():
        verify_final_data()
        print("\n✅ Euromillions data replacement completed successfully!")
    else:
        print("❌ Failed to complete data replacement")

if __name__ == "__main__":
    main()