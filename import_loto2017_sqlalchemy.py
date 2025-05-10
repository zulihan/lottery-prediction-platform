"""
Script to import loto2017.csv data into the French Loto database using SQLAlchemy.
This file contains French Loto data with a semicolon-separated format and covers more recent draws.
"""
import os
import sys
import pandas as pd
import datetime
import logging
import re
from sqlalchemy import text
from database import get_session, get_db_connection, FrenchLotoDrawing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_french_date(date_str):
    """Convert date from French format DD/MM/YYYY to ISO format YYYY-MM-DD"""
    if not date_str or pd.isna(date_str):
        return None
    
    try:
        day, month, year = date_str.split('/')
        return f"{year}-{month}-{day}"
    except Exception as e:
        logger.error(f"Error converting date '{date_str}': {e}")
        return None

def get_day_of_week(day_abbr):
    """Convert French day name to English day name."""
    day_mapping = {
        'LUNDI': 'Monday',
        'MARDI': 'Tuesday',
        'MERCREDI': 'Wednesday',
        'JEUDI': 'Thursday',
        'VENDREDI': 'Friday',
        'SAMEDI': 'Saturday',
        'DIMANCHE': 'Sunday'
    }
    
    # Remove extra spaces and return the mapped day name
    day_abbr = day_abbr.strip() if day_abbr else ''
    return day_mapping.get(day_abbr, day_abbr)

def check_table_columns():
    """
    Check the columns in the french_loto_drawings table
    """
    try:
        # Get a session from the connection
        conn = get_db_connection()
        if not conn:
            logger.error("Failed to get database connection")
            return []
            
        # Use SQLAlchemy to get column names
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'french_loto_drawings'"))
        columns = [row[0] for row in result]
        logger.info(f"Columns in french_loto_drawings table: {columns}")
        conn.close()
        return columns
    except Exception as e:
        logger.error(f"Error checking table structure: {e}")
        return []

def import_loto2017_csv(filename='attached_assets/loto2017.csv', batch_size=25, max_rows=None, 
                       start_date=None, end_date=None, start_row=0):
    """
    Import data from the loto2017.csv file using SQLAlchemy

    Args:
        filename: Path to the CSV file
        batch_size: Number of records to insert in each batch
        max_rows: Maximum number of rows to process in total (None for all)
        start_date: Only import records on or after this date (YYYY-MM-DD format)
        end_date: Only import records on or before this date (YYYY-MM-DD format)
        start_row: Row to start processing from (for resuming interrupted imports)
    
    Returns:
        int: Number of records imported
    """
    try:
        logger.info(f"Starting import from {filename}")
        
        # Check if the file exists
        if not os.path.exists(filename):
            logger.error(f"File {filename} not found")
            return 0
        
        # Read the CSV file with semicolon delimiter
        df = pd.read_csv(filename, sep=';', encoding='utf-8')
        
        # Print first few columns to help debug
        logger.info(f"Successfully read {len(df)} rows from {filename}")
        logger.info(f"First row column names: {list(df.columns)[:10]}...")
        logger.info(f"Sample values from first row: {dict(df.iloc[0].head(10))}")
        
        # Filter by date range if specified
        if start_date:
            logger.info(f"Filtering records on or after {start_date}")
            # Convert French dates to ISO format for comparison
            df['date_iso'] = df['date_de_tirage'].apply(convert_french_date)
            df = df[df['date_iso'] >= start_date]
        
        if end_date:
            logger.info(f"Filtering records on or before {end_date}")
            if 'date_iso' not in df.columns:
                df['date_iso'] = df['date_de_tirage'].apply(convert_french_date)
            df = df[df['date_iso'] <= end_date]
        
        # Skip rows if specified
        if start_row > 0:
            logger.info(f"Starting from row {start_row}")
            df = df.iloc[start_row:]
        
        # Limit rows if specified
        if max_rows:
            logger.info(f"Processing up to {max_rows} rows")
            df = df.head(max_rows)
        
        logger.info(f"Found {len(df)} valid records to process")
        
        # Get a database session
        session = get_session()
        if not session:
            logger.error("Failed to get database session")
            return 0
        
        # Prepare for batch processing
        total_imported = 0
        batches = (len(df) + batch_size - 1) // batch_size
        
        for batch_num in range(batches):
            if max_rows and total_imported >= max_rows:
                break
                
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(df))
            batch_df = df.iloc[start_idx:end_idx]
            
            batch_imported = 0
            
            for _, row in batch_df.iterrows():
                try:
                    # Convert date from French to ISO format
                    draw_date = convert_french_date(row['date_de_tirage'])
                    if not draw_date:
                        logger.warning(f"Invalid date format: {row['date_de_tirage']}, skipping")
                        continue
                    
                    # Check for future dates (beyond Jan 1, 2023)
                    reference_date = "2023-01-01"
                    if draw_date > reference_date:
                        logger.warning(f"Skipping future date: {draw_date}")
                        continue
                    
                    # Extract values
                    n1 = int(row['boule_1'])
                    n2 = int(row['boule_2'])
                    n3 = int(row['boule_3'])
                    n4 = int(row['boule_4'])
                    n5 = int(row['boule_5'])
                    lucky = int(row['numero_chance'])
                    day_of_week = get_day_of_week(row['jour_de_tirage'])
                    
                    # Get winners and prize data if available
                    try:
                        winners_rank1 = int(row['nombre_de_gagnant_au_rang1']) if pd.notna(row.get('nombre_de_gagnant_au_rang1', None)) else None
                    except (ValueError, TypeError):
                        winners_rank1 = None
                        
                    try:
                        prize_rank1 = row['rapport_du_rang1'] if pd.notna(row.get('rapport_du_rang1', None)) else None
                        if isinstance(prize_rank1, str):
                            prize_rank1 = prize_rank1.replace(',', '.')
                    except (ValueError, TypeError):
                        prize_rank1 = None
                    
                    try:
                        winners_rank2 = int(row['nombre_de_gagnant_au_rang2']) if pd.notna(row.get('nombre_de_gagnant_au_rang2', None)) else None
                    except (ValueError, TypeError):
                        winners_rank2 = None
                        
                    try:
                        prize_rank2 = row['rapport_du_rang2'] if pd.notna(row.get('rapport_du_rang2', None)) else None
                        if isinstance(prize_rank2, str):
                            prize_rank2 = prize_rank2.replace(',', '.')
                    except (ValueError, TypeError):
                        prize_rank2 = None
                    
                    try:
                        winners_rank3 = int(row['nombre_de_gagnant_au_rang3']) if pd.notna(row.get('nombre_de_gagnant_au_rang3', None)) else None
                    except (ValueError, TypeError):
                        winners_rank3 = None
                        
                    try:
                        prize_rank3 = row['rapport_du_rang3'] if pd.notna(row.get('rapport_du_rang3', None)) else None
                        if isinstance(prize_rank3, str):
                            prize_rank3 = prize_rank3.replace(',', '.')
                    except (ValueError, TypeError):
                        prize_rank3 = None
                    
                    try:
                        winners_rank4 = int(row['nombre_de_gagnant_au_rang4']) if pd.notna(row.get('nombre_de_gagnant_au_rang4', None)) else None
                    except (ValueError, TypeError):
                        winners_rank4 = None
                        
                    try:
                        prize_rank4 = row['rapport_du_rang4'] if pd.notna(row.get('rapport_du_rang4', None)) else None
                        if isinstance(prize_rank4, str):
                            prize_rank4 = prize_rank4.replace(',', '.')
                    except (ValueError, TypeError):
                        prize_rank4 = None
                    
                    try:
                        winners_rank5 = int(row['nombre_de_gagnant_au_rang5']) if pd.notna(row.get('nombre_de_gagnant_au_rang5', None)) else None
                    except (ValueError, TypeError):
                        winners_rank5 = None
                        
                    try:
                        prize_rank5 = row['rapport_du_rang5'] if pd.notna(row.get('rapport_du_rang5', None)) else None
                        if isinstance(prize_rank5, str):
                            prize_rank5 = prize_rank5.replace(',', '.')
                    except (ValueError, TypeError):
                        prize_rank5 = None
                    
                    try:
                        winners_rank6 = int(row['nombre_de_gagnant_au_rang6']) if pd.notna(row.get('nombre_de_gagnant_au_rang6', None)) else None
                    except (ValueError, TypeError):
                        winners_rank6 = None
                        
                    try:
                        prize_rank6 = row['rapport_du_rang6'] if pd.notna(row.get('rapport_du_rang6', None)) else None
                        if isinstance(prize_rank6, str):
                            prize_rank6 = prize_rank6.replace(',', '.')
                    except (ValueError, TypeError):
                        prize_rank6 = None
                    
                    try:
                        winners_rank7 = int(row['nombre_de_gagnant_au_rang7']) if pd.notna(row.get('nombre_de_gagnant_au_rang7', None)) else None
                    except (ValueError, TypeError):
                        winners_rank7 = None
                        
                    try:
                        prize_rank7 = row['rapport_du_rang7'] if pd.notna(row.get('rapport_du_rang7', None)) else None
                        if isinstance(prize_rank7, str):
                            prize_rank7 = prize_rank7.replace(',', '.')
                    except (ValueError, TypeError):
                        prize_rank7 = None
                    
                    # Add currency if available
                    currency = row.get('devise', 'EUR') if pd.notna(row.get('devise', None)) else 'EUR'
                    
                    # Total prize amount if available (replace comma with dot for proper decimal)
                    total_amount = None
                    try:
                        # Try different potential column names
                        for col_name in ['prix_total', 'cagnotte', 'mises']:
                            if col_name in row and pd.notna(row[col_name]):
                                amount_value = row[col_name]
                                if isinstance(amount_value, str):
                                    amount_str = amount_value.replace(',', '.')
                                    # Remove any non-numeric characters except for the decimal point
                                    amount_str = re.sub(r'[^\d.]', '', amount_str)
                                    try:
                                        total_amount = float(amount_str)
                                        break
                                    except ValueError:
                                        pass
                                elif isinstance(amount_value, (int, float)):
                                    total_amount = float(amount_value)
                                    break
                    except Exception as e:
                        logger.warning(f"Error processing total amount: {e}")
                        total_amount = None
                    
                    # Check for existing record for this date and draw number
                    draw_num = 1  # Default
                    
                    # Query using SQLAlchemy
                    existing_record = session.query(FrenchLotoDrawing).filter_by(
                        date=datetime.datetime.strptime(draw_date, '%Y-%m-%d').date(),
                        draw_num=draw_num
                    ).first()
                    
                    if existing_record:
                        logger.info(f"Record for {draw_date} (draw #{draw_num}) already exists, skipping")
                        continue
                    
                    logger.info(f"Preparing to insert record for {draw_date} with numbers: {n1}, {n2}, {n3}, {n4}, {n5}, {lucky}")
                    
                    # Create a new FrenchLotoDrawing object
                    drawing = FrenchLotoDrawing(
                        date=datetime.datetime.strptime(draw_date, '%Y-%m-%d').date(),
                        draw_num=draw_num,
                        day_of_week=day_of_week,
                        n1=n1,
                        n2=n2,
                        n3=n3,
                        n4=n4,
                        n5=n5,
                        lucky=lucky,
                        winners_rank1=winners_rank1,
                        prize_rank1=prize_rank1,
                        winners_rank2=winners_rank2,
                        prize_rank2=prize_rank2,
                        winners_rank3=winners_rank3,
                        prize_rank3=prize_rank3,
                        winners_rank4=winners_rank4,
                        prize_rank4=prize_rank4,
                        winners_rank5=winners_rank5,
                        prize_rank5=prize_rank5,
                        winners_rank6=winners_rank6,
                        prize_rank6=prize_rank6,
                        winners_rank7=winners_rank7,
                        prize_rank7=prize_rank7,
                        total_amount=total_amount,
                        currency=currency
                    )
                    
                    # Add to session
                    session.add(drawing)
                    
                    # Commit after each record to avoid losing progress if there's an error
                    session.commit()
                    logger.info(f"Successfully inserted record for date {draw_date}")
                    
                    batch_imported += 1
                    total_imported += 1
                    
                except Exception as e:
                    logger.error(f"Error processing row: {e}")
                    session.rollback()
                    # Continue with the next row
                    continue
            
            logger.info(f"Imported batch {batch_num+1}/{batches}: {batch_imported} records")
        
        session.close()
        return total_imported
        
    except Exception as e:
        logger.error(f"Error importing data: {e}")
        if 'session' in locals() and session:
            session.close()
        return 0

def verify_import():
    """
    Verify the import by showing basic statistics
    """
    try:
        session = get_session()
        if not session:
            logger.error("Failed to get database session")
            return
        
        # Get total count
        total_count = session.query(FrenchLotoDrawing).count()
        logger.info(f"Total records in database: {total_count}")
        
        # Get count by year using SQLAlchemy
        from sqlalchemy import extract, func
        result = session.query(
            extract('year', FrenchLotoDrawing.date).label('year'),
            func.count('*').label('count')
        ).group_by('year').order_by('year').all()
        
        logger.info("Records by year:")
        for year, count in result:
            logger.info(f"  {int(year)}: {count} records")
            
        session.close()
        
    except Exception as e:
        logger.error(f"Error verifying import: {e}")
        if 'session' in locals() and session:
            session.close()

def main():
    """
    Main function to import the loto2017.csv file
    """
    # Check table structure
    check_table_columns()
    
    # Import data (use smaller batch size to avoid timeouts)
    imported = import_loto2017_csv(
        filename='attached_assets/loto2017.csv',
        batch_size=25,
        max_rows=None  # Import all records
    )
    
    logger.info(f"Successfully imported {imported} records")
    
    # Verify the import
    verify_import()

if __name__ == "__main__":
    main()