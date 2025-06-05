"""
Check the actual database structure to find the correct table names and columns
"""
import sqlite3
import pandas as pd

def check_database_structure():
    """Check what tables and columns exist in the database"""
    try:
        conn = sqlite3.connect('euromillions_predictions.db')
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("Available tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check each table structure
        for table in tables:
            table_name = table[0]
            print(f"\n{table_name} structure:")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
            
            # Show sample data
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  Rows: {count}")
            
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample = cursor.fetchall()
                print("  Sample data:")
                for row in sample:
                    print(f"    {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_database_structure()