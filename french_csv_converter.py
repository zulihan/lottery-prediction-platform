#!/usr/bin/env python3
"""
Script to import French Loto data from the 2019 format CSV files
"""
import os
import sys
import process_french_csv
import database

def main():
    # Initialize the database
    database.init_db()
    
    # Check if a file path was provided
    if len(sys.argv) < 2:
        print("Usage: python french_csv_converter.py <file_path> [--skip-clear]")
        print("Example: python french_csv_converter.py attached_assets/loto_201902.csv")
        sys.exit(1)
    
    # Get the file path from command line arguments
    input_file = sys.argv[1]
    
    # Check if the --skip-clear flag is present
    skip_clear = "--skip-clear" in sys.argv
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)
    
    # Clear existing data if not skipped
    if not skip_clear:
        try:
            # Get a fresh connection
            conn = database.get_db_connection()
            # Delete all records
            from sqlalchemy import text
            result = conn.execute(text("DELETE FROM french_loto_drawings"))
            # Commit the transaction
            conn.commit()
            print(f"Deleted {result.rowcount} existing French Loto drawings from database")
            conn.close()
        except Exception as e:
            print(f"Error clearing French Loto data: {e}")
            sys.exit(1)
    
    print(f"Importing French Loto data from {input_file}...")
    
    # Import the data
    count = process_french_csv.import_french_loto_file(input_file)
    
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
            
        # Display a few sample records
        print("\nSample records:")
        samples = session.query(database.FrenchLotoDrawing).order_by(database.FrenchLotoDrawing.date.desc()).limit(5).all()
        for sample in samples:
            numbers = f"{sample.n1}-{sample.n2}-{sample.n3}-{sample.n4}-{sample.n5}"
            print(f"Date: {sample.date}, Draw: {sample.draw_num}, Numbers: {numbers}, Lucky: {sample.lucky}")
            
    except Exception as e:
        print(f"Error verifying import: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()