#!/usr/bin/env python3
"""
Script to import a small sample of old French Loto data for testing
"""
import sys
import pandas as pd
import old_loto_importer
import database

def main():
    # Initialize the database
    database.init_db()
    
    print("Importing sample of old French Loto data for testing...")
    
    # Read the first 20 rows from the file
    input_file = "attached_assets/loto.csv"
    data = pd.read_csv(input_file, sep=';', encoding='utf-8', nrows=20)
    
    # Write sample to temporary file
    sample_file = "temp_data/loto_sample.csv"
    data.to_csv(sample_file, sep=';', index=False)
    
    # Process the sample file
    count = old_loto_importer.import_old_loto_file(sample_file)
    
    print(f"Successfully imported {count} records from sample file.")
    
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
        
        # Show a few sample records
        print("\nSample records:")
        records = session.query(database.FrenchLotoDrawing).order_by(database.FrenchLotoDrawing.date.desc()).limit(5).all()
        for record in records:
            print(f"Date: {record.date}, Numbers: {record.n1}-{record.n2}-{record.n3}-{record.n4}-{record.n5}, Lucky: {record.lucky}")
            
    except Exception as e:
        print(f"Error verifying import: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()