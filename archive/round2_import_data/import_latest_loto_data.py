"""
Script to import the latest French Loto data from attached_assets/loto_201911.csv
to update the database with new drawings through 2025
"""
import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import text
from database import get_session, FrenchLotoDrawing, init_db

def convert_french_date(date_str):
    """Convert date from French format DD/MM/YYYY to ISO format YYYY-MM-DD"""
    try:
        day, month, year = date_str.split('/')
        return f"{year}-{month}-{day}"
    except Exception as e:
        print(f"Error converting date {date_str}: {str(e)}")
        return None

def get_latest_date_in_db():
    """Get the latest date in the database to know from where to start importing"""
    session = get_session()
    try:
        result = session.execute(text("SELECT MAX(date) FROM french_loto_drawings")).scalar()
        return result
    except Exception as e:
        print(f"Error getting latest date: {str(e)}")
        return None
    finally:
        session.close()

def import_loto_201911_data(filename='attached_assets/loto_201911.csv', batch_size=25):
    """
    Import French Loto data from the loto_201911.csv file
    
    Args:
        filename: Path to the CSV file
        batch_size: Number of records to process in each batch
    """
    print(f"Starting import from {filename}...")
    
    # Get the latest date in the database
    latest_date = get_latest_date_in_db()
    print(f"Latest date in database: {latest_date}")
    
    try:
        # Read the CSV file with semicolon as delimiter
        df = pd.read_csv(filename, sep=';', encoding='utf-8')
        print(f"Loaded {len(df)} records from CSV file")
        
        # Convert date format
        df['date'] = df['date_de_tirage'].apply(convert_french_date)
        
        # If we have a latest date, filter to only newer records
        if latest_date:
            # Convert to datetime for comparison
            df['date_obj'] = pd.to_datetime(df['date'])
            latest_date_obj = pd.to_datetime(latest_date)
            
            # Filter for newer records
            df = df[df['date_obj'] > latest_date_obj]
            print(f"Filtered to {len(df)} records newer than {latest_date}")
        
        # Skip if no new records
        if len(df) == 0:
            print("No new records to import.")
            return 0
        
        # Process in batches
        total_imported = 0
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            print(f"Processing batch {i//batch_size + 1} ({len(batch)} records)...")
            
            # Process each batch
            session = get_session()
            try:
                for _, row in batch.iterrows():
                    try:
                        # Extract data
                        date_str = convert_french_date(row['date_de_tirage'])
                        if not date_str:
                            continue
                            
                        # Create new record
                        drawing = FrenchLotoDrawing(
                            date=date_str,
                            day_of_week=row['jour_de_tirage'].capitalize(),
                            n1=int(row['boule_1']),
                            n2=int(row['boule_2']),
                            n3=int(row['boule_3']),
                            n4=int(row['boule_4']),
                            n5=int(row['boule_5']),
                            lucky=int(row['numero_chance']),
                            winners_rank1=int(row['nombre_de_gagnant_au_rang1']) if not pd.isna(row['nombre_de_gagnant_au_rang1']) else 0,
                            winners_rank2=int(row['nombre_de_gagnant_au_rang2']) if not pd.isna(row['nombre_de_gagnant_au_rang2']) else 0,
                            winners_rank3=int(row['nombre_de_gagnant_au_rang3']) if not pd.isna(row['nombre_de_gagnant_au_rang3']) else 0,
                            winners_rank4=int(row['nombre_de_gagnant_au_rang4']) if not pd.isna(row['nombre_de_gagnant_au_rang4']) else 0,
                            winners_rank5=int(row['nombre_de_gagnant_au_rang5']) if not pd.isna(row['nombre_de_gagnant_au_rang5']) else 0,
                            winners_rank6=int(row['nombre_de_gagnant_au_rang6']) if not pd.isna(row['nombre_de_gagnant_au_rang6']) else 0,
                            winners_rank7=int(row['nombre_de_gagnant_au_rang7']) if not pd.isna(row['nombre_de_gagnant_au_rang7']) else 0,
                            prize_rank1=float(str(row['rapport_du_rang1']).replace(',', '.')) if not pd.isna(row['rapport_du_rang1']) else 0,
                            prize_rank2=float(str(row['rapport_du_rang2']).replace(',', '.')) if not pd.isna(row['rapport_du_rang2']) else 0,
                            prize_rank3=float(str(row['rapport_du_rang3']).replace(',', '.')) if not pd.isna(row['rapport_du_rang3']) else 0,
                            prize_rank4=float(str(row['rapport_du_rang4']).replace(',', '.')) if not pd.isna(row['rapport_du_rang4']) else 0,
                            prize_rank5=float(str(row['rapport_du_rang5']).replace(',', '.')) if not pd.isna(row['rapport_du_rang5']) else 0,
                            prize_rank6=float(str(row['rapport_du_rang6']).replace(',', '.')) if not pd.isna(row['rapport_du_rang6']) else 0,
                            prize_rank7=float(str(row['rapport_du_rang7']).replace(',', '.')) if not pd.isna(row['rapport_du_rang7']) else 0,
                            currency='EUR'
                        )
                        
                        # Add to session
                        session.add(drawing)
                        total_imported += 1
                    except Exception as e:
                        print(f"Error processing row: {str(e)}")
                        continue
                
                # Commit batch
                session.commit()
                print(f"Committed batch {i//batch_size + 1} ({total_imported} records total)")
                
            except Exception as e:
                print(f"Error processing batch: {str(e)}")
                session.rollback()
            finally:
                session.close()
        
        print(f"Import complete. Added {total_imported} new records.")
        return total_imported
        
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return 0

def check_data_quality():
    """Verify the data quality after import"""
    session = get_session()
    try:
        # Get latest 5 records
        latest = session.execute(text("SELECT date, day_of_week, n1, n2, n3, n4, n5, lucky FROM french_loto_drawings ORDER BY date DESC LIMIT 5")).fetchall()
        
        print("\nLatest 5 records:")
        for draw in latest:
            print(f"{draw[0]} ({draw[1]}): {draw[2]}-{draw[3]}-{draw[4]}-{draw[5]}-{draw[6]} + {draw[7]}")
            
        # Get count by year
        year_counts = session.execute(text("SELECT EXTRACT(YEAR FROM date) as year, COUNT(*) FROM french_loto_drawings GROUP BY year ORDER BY year DESC")).fetchall()
        
        print("\nRecords by year:")
        for year, count in year_counts[:10]:  # Show last 10 years
            print(f"{int(year)}: {count} drawings")
            
        # Check for duplicates
        dupes = session.execute(text("SELECT date, COUNT(*) FROM french_loto_drawings GROUP BY date HAVING COUNT(*) > 1")).fetchall()
        
        if dupes:
            print("\nWarning: Duplicate dates found:")
            for date, count in dupes:
                print(f"{date}: {count} records")
        else:
            print("\nNo duplicate dates found.")
            
    except Exception as e:
        print(f"Error checking data quality: {str(e)}")
    finally:
        session.close()

def main():
    """Main function to import latest data and verify it"""
    # Initialize database if needed
    init_db()
    
    # Import latest data
    imported = import_loto_201911_data()
    
    if imported > 0:
        # Check data quality
        check_data_quality()
    else:
        print("No new data imported.")

if __name__ == "__main__":
    main()