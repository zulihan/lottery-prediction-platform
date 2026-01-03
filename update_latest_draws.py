#!/usr/bin/env python3
"""
Script to download and import latest lottery drawings from FDJ API.

Downloads ZIP files from FDJ API endpoints and imports the latest drawings
into the SQLite database.
"""

import requests
import zipfile
import io
import pandas as pd
import sqlite3
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API endpoints
EUROMILLIONS_API_URL = "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afe6"
FRENCH_LOTO_API_URL = "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afp6"

DB_PATH = 'lottery_predictions.db'


def download_zip_from_url(url):
    """Download ZIP file from URL and return its content"""
    try:
        logger.info(f"Downloading from {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading from {url}: {e}")
        return None


def extract_csv_from_zip(zip_content, filename_pattern=None):
    """Extract CSV file from ZIP content"""
    try:
        zip_file = zipfile.ZipFile(io.BytesIO(zip_content))
        csv_files = [f for f in zip_file.namelist() if f.endswith('.csv')]
        
        if not csv_files:
            logger.warning("No CSV files found in ZIP")
            return None
        
        # If pattern specified, try to match it
        if filename_pattern:
            matching = [f for f in csv_files if filename_pattern in f.lower()]
            if matching:
                csv_files = matching
        
        # Use the first CSV file found
        csv_filename = csv_files[0]
        logger.info(f"Extracting {csv_filename} from ZIP")
        return zip_file.read(csv_filename)
    except Exception as e:
        logger.error(f"Error extracting CSV from ZIP: {e}")
        return None


def parse_euromillions_csv(csv_content):
    """Parse Euromillions CSV content and return DataFrame"""
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
            try:
                df = pd.read_csv(io.BytesIO(csv_content), encoding=encoding, sep=';')
                logger.info(f"Successfully parsed Euromillions CSV with encoding {encoding}")
                return df
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, try with error handling
        df = pd.read_csv(io.BytesIO(csv_content), encoding='utf-8', sep=';', encoding_errors='ignore')
        return df
    except Exception as e:
        logger.error(f"Error parsing Euromillions CSV: {e}")
        return None


def parse_french_loto_csv(csv_content):
    """Parse French Loto CSV content and return DataFrame"""
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
            try:
                df = pd.read_csv(io.BytesIO(csv_content), encoding=encoding, sep=';')
                logger.info(f"Successfully parsed French Loto CSV with encoding {encoding}")
                return df
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, try with error handling
        df = pd.read_csv(io.BytesIO(csv_content), encoding='utf-8', sep=';', encoding_errors='ignore')
        return df
    except Exception as e:
        logger.error(f"Error parsing French Loto CSV: {e}")
        return None


def normalize_euromillions_data(df):
    """Normalize Euromillions DataFrame to match database schema"""
    try:
        # Map column names (FDJ API uses French column names)
        column_mapping = {
            'date': 'date',
            'date_de_tirage': 'date',
            'jour': 'day_of_week',
            'jour_de_tirage': 'day_of_week',
            'day_of_week': 'day_of_week',
            'n1': 'n1',
            'n2': 'n2',
            'n3': 'n3',
            'n4': 'n4',
            'n5': 'n5',
            'boule_1': 'n1',
            'boule_2': 'n2',
            'boule_3': 'n3',
            'boule_4': 'n4',
            'boule_5': 'n5',
            'e1': 's1',
            'e2': 's2',
            'etoile_1': 's1',
            'etoile_2': 's2',
            'star_1': 's1',
            'star_2': 's2',
            's1': 's1',
            's2': 's2'
        }
        
        # Rename columns if they exist
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        # Ensure required columns exist
        required_cols = ['date', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            logger.warning(f"Missing columns in Euromillions data: {missing_cols}")
            logger.info(f"Available columns: {list(df.columns)}")
            return None
        
        # Convert date to string format (French format DD/MM/YYYY)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], dayfirst=True, format='mixed').dt.strftime('%Y-%m-%d')
        
        # Ensure numeric columns are integers
        for col in ['n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        
        return df[required_cols + ['day_of_week'] if 'day_of_week' in df.columns else required_cols]
    except Exception as e:
        logger.error(f"Error normalizing Euromillions data: {e}")
        return None


def normalize_french_loto_data(df):
    """Normalize French Loto DataFrame to match database schema"""
    try:
        # Map column names (FDJ API uses French column names)
        column_mapping = {
            'date': 'date',
            'date_de_tirage': 'date',
            'jour': 'day_of_week',
            'jour_de_tirage': 'day_of_week',
            'day_of_week': 'day_of_week',
            'numero_tirage': 'draw_num',
            'n1': 'n1',
            'n2': 'n2',
            'n3': 'n3',
            'n4': 'n4',
            'n5': 'n5',
            'boule_1': 'n1',
            'boule_2': 'n2',
            'boule_3': 'n3',
            'boule_4': 'n4',
            'boule_5': 'n5',
            'numero_chance': 'lucky',
            'numero_chance_1': 'lucky',
            'complementaire': 'lucky',
            'lucky': 'lucky'
        }
        
        # Rename columns if they exist
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        # Ensure required columns exist
        required_cols = ['date', 'n1', 'n2', 'n3', 'n4', 'n5']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            logger.warning(f"Missing columns in French Loto data: {missing_cols}")
            logger.info(f"Available columns: {list(df.columns)}")
            return None
        
        # Convert date to string format (French format DD/MM/YYYY)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], dayfirst=True, format='mixed').dt.strftime('%Y-%m-%d')
        
        # Ensure numeric columns are integers
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        
        # Set default values for optional columns
        if 'draw_num' not in df.columns:
            df['draw_num'] = 1
        if 'lucky' not in df.columns:
            df['lucky'] = None
        
        return df
    except Exception as e:
        logger.error(f"Error normalizing French Loto data: {e}")
        return None


def import_euromillions_to_db(df, db_path=DB_PATH):
    """Import Euromillions DataFrame to SQLite database"""
    if df is None or df.empty:
        logger.warning("No Euromillions data to import")
        return 0
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    count = 0
    for _, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO euromillions_drawings 
                (date, day_of_week, n1, n2, n3, n4, n5, s1, s2)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(row['date']),
                row.get('day_of_week', None),
                int(row['n1']), int(row['n2']), int(row['n3']), 
                int(row['n4']), int(row['n5']),
                int(row['s1']), int(row['s2'])
            ))
            if cursor.rowcount > 0:
                count += 1
        except Exception as e:
            logger.error(f"Error inserting Euromillions row: {e}")
            continue
    
    conn.commit()
    conn.close()
    logger.info(f"✅ Imported {count} new Euromillions drawings")
    return count


def import_french_loto_to_db(df, db_path=DB_PATH):
    """Import French Loto DataFrame to SQLite database"""
    if df is None or df.empty:
        logger.warning("No French Loto data to import")
        return 0
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    count = 0
    for _, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO french_loto_drawings 
                (date, draw_num, n1, n2, n3, n4, n5, lucky)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(row['date']),
                int(row.get('draw_num', 1)),
                int(row['n1']), int(row['n2']), int(row['n3']), 
                int(row['n4']), int(row['n5']),
                int(row['lucky']) if pd.notna(row.get('lucky')) else None
            ))
            if cursor.rowcount > 0:
                count += 1
        except Exception as e:
            logger.error(f"Error inserting French Loto row: {e}")
            continue
    
    conn.commit()
    conn.close()
    logger.info(f"✅ Imported {count} new French Loto drawings")
    return count


def update_euromillions():
    """Download and import latest Euromillions drawings"""
    logger.info("=" * 60)
    logger.info("Updating Euromillions drawings")
    logger.info("=" * 60)
    
    # Download ZIP
    zip_content = download_zip_from_url(EUROMILLIONS_API_URL)
    if not zip_content:
        logger.error("Failed to download Euromillions data")
        return 0
    
    # Extract CSV
    csv_content = extract_csv_from_zip(zip_content, 'euromillions')
    if not csv_content:
        logger.error("Failed to extract Euromillions CSV")
        return 0
    
    # Parse CSV
    df = parse_euromillions_csv(csv_content)
    if df is None:
        logger.error("Failed to parse Euromillions CSV")
        return 0
    
    # Normalize data
    df = normalize_euromillions_data(df)
    if df is None:
        logger.error("Failed to normalize Euromillions data")
        return 0
    
    # Import to database
    count = import_euromillions_to_db(df)
    return count


def update_french_loto():
    """Download and import latest French Loto drawings"""
    logger.info("=" * 60)
    logger.info("Updating French Loto drawings")
    logger.info("=" * 60)
    
    # Download ZIP
    zip_content = download_zip_from_url(FRENCH_LOTO_API_URL)
    if not zip_content:
        logger.error("Failed to download French Loto data")
        return 0
    
    # Extract CSV
    csv_content = extract_csv_from_zip(zip_content, 'loto')
    if not csv_content:
        logger.error("Failed to extract French Loto CSV")
        return 0
    
    # Parse CSV
    df = parse_french_loto_csv(csv_content)
    if df is None:
        logger.error("Failed to parse French Loto CSV")
        return 0
    
    # Normalize data
    df = normalize_french_loto_data(df)
    if df is None:
        logger.error("Failed to normalize French Loto data")
        return 0
    
    # Import to database
    count = import_french_loto_to_db(df)
    return count


def main():
    """Main function"""
    logger.info("Starting lottery drawings update from FDJ API")
    logger.info(f"Database: {DB_PATH}")
    
    euromillions_count = update_euromillions()
    french_loto_count = update_french_loto()
    
    logger.info("=" * 60)
    logger.info("Update completed!")
    logger.info(f"   - Euromillions: {euromillions_count} new drawings")
    logger.info(f"   - French Loto: {french_loto_count} new drawings")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

