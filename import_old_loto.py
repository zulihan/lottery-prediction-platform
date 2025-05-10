#!/usr/bin/env python3
"""
Script to import old French Loto data from the CSV file for 1976-2008
"""
import os
import sys
import pandas as pd
import old_loto_importer
import database
from sqlalchemy import text

def clear_existing_data():
    """Clear existing French Loto data from the database"""
    try:
        conn = database.get_db_connection()
        with conn.begin():
            result = conn.execute(text("DELETE FROM french_loto_drawings"))
            print(f"Deleted {result.rowcount} existing French Loto drawings from database")
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing French Loto data: {e}")
        return False

def main():
    # Initialize the database
    database.init_db()
    
    # Check if input file exists
    input_file = "attached_assets/loto.csv"
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)
    
    # Ask for confirmation before clearing data
    confirm = input("This will clear all existing French Loto data. Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Import cancelled")
        sys.exit(0)
    
    # Clear existing data
    if not clear_existing_data():
        sys.exit(1)
    
    print(f"Importing French Loto data from {input_file}...")
    
    # Import the data
    count = old_loto_importer.import_old_loto_file(input_file)
    
    print(f"Successfully imported {count} records from {input_file}")
    
    # Verify the import
    session = database.get_session()
    try:
        total_count = session.query(database.FrenchLotoDrawing).count()
        print(f"Total French Loto drawings in database: {total_count}")
        
        # Get the date range
        min_date = session.query(database.FrenchLotoDrawing.date).order_by(database.FrenchLotoDrawing.date.asc()).first()
        max_date = session.query(database.FrenchLotoDrawing.date).order_by(database.FrenchLotoDrawing.date.desc()).first()
        
        if min_date and max_date:
            print(f"Date range: {min_date[0]} to {max_date[0]}")
            
    except Exception as e:
        print(f"Error verifying import: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()