#!/usr/bin/env python3
"""
Process French Loto CSV files from 2019 format
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import database

def process_french_loto_csv(file_path, skip_future_dates=True):
    """
    Process French Loto CSV files with DD/MM/YYYY date format
    and specific column structure
    
    Args:
        file_path: Path to the CSV file
        skip_future_dates: If True, skip records with dates in the future
        
    Returns:
        Processed DataFrame ready for database import
    """
    print(f"Processing newer format French Loto file: {file_path}")
    
    # Try to read with different delimiters
    try:
        # First try with semicolon delimiter (common in French CSV)
        data = pd.read_csv(file_path, sep=';', encoding='utf-8')
    except:
        try:
            # Then try with comma delimiter
            data = pd.read_csv(file_path, sep=',', encoding='utf-8')
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return None
    
    # Print column names for debugging
    print(f"Columns in file: {data.columns.tolist()}")
    
    # Check if it's the expected format
    required_columns = ['date_de_tirage', 'boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5', 'numero_chance']
    for col in required_columns:
        if col not in data.columns:
            print(f"Missing required column: {col}")
            print(f"This doesn't appear to be a 2019 format French Loto file")
            return None
    
    # Convert dates
    try:
        # Try French format DD/MM/YYYY
        data['date'] = pd.to_datetime(data['date_de_tirage'], format='%d/%m/%Y')
        print("Successfully converted dates using format '%d/%m/%Y'")
    except:
        try:
            # Try alternate format MM/DD/YYYY
            data['date'] = pd.to_datetime(data['date_de_tirage'], format='%m/%d/%Y')
            print("Successfully converted dates using format '%m/%d/%Y'")
        except:
            try:
                # Try with pandas default parser
                data['date'] = pd.to_datetime(data['date_de_tirage'])
                print("Successfully converted dates using pandas default parser")
            except Exception as e:
                print(f"Error converting dates: {str(e)}")
                return None
                
    # Filter out future dates if requested
    if skip_future_dates:
        today = pd.Timestamp.now().normalize()  # Get today's date without time component
        future_dates_count = (data['date'] > today).sum()
        if future_dates_count > 0:
            print(f"Filtering out {future_dates_count} records with future dates")
            data = data[data['date'] <= today]
            if len(data) == 0:
                print("No records remaining after filtering out future dates")
                return None
            
    print(f"Processed {len(data)} records from {file_path}")
    
    # Create renamed dataframe with standardized column names
    renamed_data = pd.DataFrame()
    renamed_data['date'] = data['date']
    renamed_data['day_of_week'] = data['date'].dt.day_name()
    
    # Extract numbers
    renamed_data['n1'] = data['boule_1']
    renamed_data['n2'] = data['boule_2']
    renamed_data['n3'] = data['boule_3']
    renamed_data['n4'] = data['boule_4']
    renamed_data['n5'] = data['boule_5']
    renamed_data['lucky'] = data['numero_chance']
    
    # Set draw_num to 1 by default (assuming all are first draws unless specified)
    renamed_data['draw_num'] = 1
    
    # Add other columns if available
    if 'rapport_rang1' in data.columns:
        renamed_data['prize_rank1'] = data['rapport_rang1'].str.replace('€', '').str.replace(',', '.').str.replace(' ', '').astype(float)
    if 'nombre_de_gagnant_rang1' in data.columns:
        renamed_data['winners_rank1'] = data['nombre_de_gagnant_rang1']
    
    if 'rapport_rang2' in data.columns and 'nombre_de_gagnant_rang2' in data.columns:
        renamed_data['prize_rank2'] = data['rapport_rang2'].str.replace('€', '').str.replace(',', '.').str.replace(' ', '').astype(float)
        renamed_data['winners_rank2'] = data['nombre_de_gagnant_rang2']
    
    if 'rapport_rang3' in data.columns and 'nombre_de_gagnant_rang3' in data.columns:
        renamed_data['prize_rank3'] = data['rapport_rang3'].str.replace('€', '').str.replace(',', '.').str.replace(' ', '').astype(float)
        renamed_data['winners_rank3'] = data['nombre_de_gagnant_rang3']
    
    if 'rapport_rang4' in data.columns and 'nombre_de_gagnant_rang4' in data.columns:
        renamed_data['prize_rank4'] = data['rapport_rang4'].str.replace('€', '').str.replace(',', '.').str.replace(' ', '').astype(float)
        renamed_data['winners_rank4'] = data['nombre_de_gagnant_rang4']
    
    if 'rapport_rang5' in data.columns and 'nombre_de_gagnant_rang5' in data.columns:
        renamed_data['prize_rank5'] = data['rapport_rang5'].str.replace('€', '').str.replace(',', '.').str.replace(' ', '').astype(float)
        renamed_data['winners_rank5'] = data['nombre_de_gagnant_rang5']
    
    if 'rapport_rang6' in data.columns and 'nombre_de_gagnant_rang6' in data.columns:
        renamed_data['prize_rank6'] = data['rapport_rang6'].str.replace('€', '').str.replace(',', '.').str.replace(' ', '').astype(float)
        renamed_data['winners_rank6'] = data['nombre_de_gagnant_rang6']
    
    if 'rapport_rang7' in data.columns and 'nombre_de_gagnant_rang7' in data.columns:
        renamed_data['prize_rank7'] = data['rapport_rang7'].str.replace('€', '').str.replace(',', '.').str.replace(' ', '').astype(float)
        renamed_data['winners_rank7'] = data['nombre_de_gagnant_rang7']
    
    # Set currency to EUR for modern draws
    renamed_data['currency'] = 'EUR'
    
    print(f"Processed {len(renamed_data)} records")
    return renamed_data

def import_to_database(data):
    """
    Import the processed data to the database
    
    Args:
        data: Processed DataFrame
        
    Returns:
        Number of records imported
    """
    if data is None or len(data) == 0:
        print("No data to import")
        return 0
    
    count = 0
    for _, row in data.iterrows():
        try:
            # Extract data from the row
            numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            lucky = row['lucky']
            date = row['date'].date()  # Convert pandas timestamp to date
            day_of_week = row['day_of_week']
            draw_num = row['draw_num']
            
            # Prepare winners and prizes dictionaries
            winners = {}
            prizes = {}
            
            for i in range(1, 8):
                winners_key = f'winners_rank{i}'
                prize_key = f'prize_rank{i}'
                
                if winners_key in row and not pd.isna(row[winners_key]):
                    winners[f'rank{i}'] = int(row[winners_key])
                
                if prize_key in row and not pd.isna(row[prize_key]):
                    prizes[f'rank{i}'] = float(row[prize_key])
            
            # Prepare total amount if available
            total_amount = None
            if 'total_amount' in row and not pd.isna(row['total_amount']):
                total_amount = float(row['total_amount'])
            
            # Prepare currency
            currency = 'EUR'
            if 'currency' in row and not pd.isna(row['currency']):
                currency = row['currency']
            
            # Add to database
            success = database.add_french_loto_drawing_with_details(
                date=date,
                numbers=numbers,
                lucky=lucky,
                day_of_week=day_of_week,
                winners=winners,
                prizes=prizes,
                total_amount=total_amount,
                currency=currency,
                draw_num=draw_num
            )
            
            if success:
                count += 1
            
        except Exception as e:
            print(f"Error importing row: {str(e)}")
    
    print(f"Successfully imported {count} records")
    return count

def import_french_loto_file(file_path, skip_future_dates=True):
    """
    Main function to process and import a French Loto file
    
    Args:
        file_path: Path to the CSV file
        skip_future_dates: If True, skip records with dates in the future
        
    Returns:
        Number of records imported
    """
    # Process the data
    processed_data = process_french_loto_csv(file_path, skip_future_dates=skip_future_dates)
    
    # Import to database
    count = import_to_database(processed_data) if processed_data is not None else 0
    
    return count