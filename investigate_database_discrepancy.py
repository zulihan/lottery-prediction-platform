"""
Investigate the discrepancy between expected 1845 draws and observed 1875 rows
"""
import os
from sqlalchemy import create_engine, text
import pandas as pd

def investigate_euromillions_data():
    """Investigate the database content to understand the row count discrepancy"""
    
    try:
        database_url = os.getenv('DATABASE_URL')
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Get total row count
            count_result = conn.execute(text("SELECT COUNT(*) FROM euromillions_drawings"))
            total_rows = count_result.fetchone()[0]
            print(f"Total rows in euromillions_drawings: {total_rows}")
            
            # Get column structure
            columns_result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'euromillions_drawings'
                ORDER BY ordinal_position
            """))
            columns = columns_result.fetchall()
            print(f"Table structure: {columns}")
            
            # Get date range
            date_result = conn.execute(text("""
                SELECT MIN(id), MAX(id) FROM euromillions_drawings
            """))
            min_id, max_id = date_result.fetchone()
            print(f"ID range: {min_id} to {max_id}")
            
            # Check for duplicate IDs
            duplicate_result = conn.execute(text("""
                SELECT id, COUNT(*) as count 
                FROM euromillions_drawings 
                GROUP BY id 
                HAVING COUNT(*) > 1
                ORDER BY count DESC
                LIMIT 10
            """))
            duplicates = duplicate_result.fetchall()
            if duplicates:
                print(f"Duplicate IDs found: {duplicates}")
            else:
                print("No duplicate IDs found")
            
            # Get sample of first and last few rows to understand the data
            sample_result = conn.execute(text("""
                SELECT * FROM euromillions_drawings 
                ORDER BY id DESC 
                LIMIT 5
            """))
            recent_samples = sample_result.fetchall()
            print(f"5 most recent entries:")
            for row in recent_samples:
                print(f"  {row}")
            
            # Get oldest entries
            oldest_result = conn.execute(text("""
                SELECT * FROM euromillions_drawings 
                ORDER BY id ASC 
                LIMIT 5
            """))
            oldest_samples = oldest_result.fetchall()
            print(f"5 oldest entries:")
            for row in oldest_samples:
                print(f"  {row}")
            
            # Check if there are any rows with null values in key columns
            null_check = conn.execute(text("""
                SELECT 
                    COUNT(*) as total_rows,
                    COUNT(CASE WHEN id IS NULL THEN 1 END) as null_ids,
                    COUNT(CASE WHEN date_column IS NULL THEN 1 END) as null_dates
                FROM euromillions_drawings
            """))
            null_counts = null_check.fetchone()
            print(f"Null value analysis: {null_counts}")
            
            # Check unique date values if there's a date column
            try:
                unique_dates = conn.execute(text("""
                    SELECT COUNT(DISTINCT date_column) as unique_dates
                    FROM euromillions_drawings
                """))
                unique_count = unique_dates.fetchone()[0]
                print(f"Unique dates: {unique_count}")
            except:
                print("No date_column found or accessible")
            
            # Try to identify the actual data structure
            sample_full = conn.execute(text("SELECT * FROM euromillions_drawings LIMIT 1"))
            sample_row = sample_full.fetchone()
            if sample_row:
                print(f"Sample row with all values: {sample_row}")
                print(f"Number of columns: {len(sample_row)}")
                
                # Based on previous output: (1875, datetime.date(2004, 2, 13), 'Friday', 32, 16, 29, 41, 36, 9, 7)
                # This suggests: id, date, day, n1, n2, n3, n4, n5, s1, s2
                if len(sample_row) >= 10:
                    id_val = sample_row[0]
                    date_val = sample_row[1] 
                    day_val = sample_row[2]
                    numbers = sample_row[3:8]  # positions 3-7
                    stars = sample_row[8:10]   # positions 8-9
                    
                    print(f"Parsed structure:")
                    print(f"  ID: {id_val}")
                    print(f"  Date: {date_val}")
                    print(f"  Day: {day_val}")
                    print(f"  Numbers: {numbers}")
                    print(f"  Stars: {stars}")
        
        return total_rows
        
    except Exception as e:
        print(f"Investigation error: {e}")
        return None

def main():
    """Main investigation function"""
    print("🔍 INVESTIGATING DATABASE DISCREPANCY")
    print("Expected: 1845 draws | Observed: 1875 rows")
    print("=" * 50)
    
    total_rows = investigate_euromillions_data()
    
    if total_rows:
        difference = total_rows - 1845
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"Actual rows: {total_rows}")
        print(f"Expected rows: 1845")
        print(f"Difference: +{difference} rows")
        
        if difference > 0:
            print(f"\nPossible explanations for +{difference} extra rows:")
            print("- Duplicate entries in the dataset")
            print("- Test/sample data mixed with real data")
            print("- Different Euromillions variants (e.g., different countries)")
            print("- Data import included header rows or metadata")
            print("- Recent draws added after the original 1845 count")
    
    return total_rows

if __name__ == "__main__":
    main()