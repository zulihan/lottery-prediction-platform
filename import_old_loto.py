#!/usr/bin/env python3
"""
Script to import old French Loto data from the CSV file for 1976-2008
"""
import sys
import old_loto_importer
import database

def main():
    # Initialize the database
    database.init_db()
    
    print("Importing old French Loto data from 1976-2008...")
    
    # Import the file
    input_file = "attached_assets/loto.csv"
    count = old_loto_importer.import_old_loto_file(input_file)
    
    print(f"Successfully imported {count} records from the old French Loto data.")
    
    # Verify the import
    session = database.get_session()
    try:
        count = session.query(database.FrenchLotoDrawing).count()
        print(f"Total French Loto drawings in database: {count}")
        
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