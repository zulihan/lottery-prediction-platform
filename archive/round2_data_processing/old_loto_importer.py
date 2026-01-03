#!/usr/bin/env python3
"""
Import data from old French Loto CSV format (1976-2008)
"""
import pandas as pd
import datetime
import database
from dateutil.parser import parse
import re

def process_old_loto_csv(file_path):
    """Process old format French Loto CSV files with semicolon separators"""
    print(f"Processing old Loto file: {file_path}")
    
    # Read the CSV with ; as separator
    try:
        data = pd.read_csv(file_path, sep=';', encoding='utf-8')
        print(f"Read {len(data)} rows from {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return 0
    
    # Map the columns to our database schema
    # The old format has columns:
    # 'annee_numero_de_tirage', '1er_ou_2eme_tirage', 'jour_de_tirage', 'date_de_tirage', etc.
    
    # First, convert dates
    # The date_de_tirage seems to be in format YYYYMMDD (e.g., 20081004)
    # Direct extraction from this field
    
    try:
        # First try to extract date directly from date_de_tirage field
        # Format appears to be YYYYMMDD with no separators
        data['date'] = pd.to_datetime(data['date_de_tirage'], format='%Y%m%d')
        print("Successfully converted dates using format '%Y%m%d'")
    except Exception as e:
        print(f"Error converting dates with specific format: {str(e)}")
        
        try:
            # Try with default pandas parsing as a fallback
            data['date'] = pd.to_datetime(data['date_de_tirage'])
            print("Successfully converted dates using pandas default parsing")
        except Exception as e:
            print(f"Error converting dates with pandas default: {str(e)}")
            print("Falling back to manual date parsing...")
            
            # Extract year from annee_numero_de_tirage as a last resort
            data['year'] = data['annee_numero_de_tirage'].astype(str).str[:4].astype(int)
            
            # If everything fails, manually parse each date with our custom function
            data['date'] = data.apply(
                lambda row: parse_french_date(row['date_de_tirage'], row['year']), 
                axis=1
            )
    
    # Get day of week from abbreviations
    day_of_week_map = {
        'LU': 'Monday',
        'MA': 'Tuesday',
        'ME': 'Wednesday',
        'JE': 'Thursday',
        'VE': 'Friday',
        'SA': 'Saturday',
        'DI': 'Sunday'
    }
    data['day_of_week'] = data['jour_de_tirage'].apply(lambda x: day_of_week_map.get(x, ''))
    
    # Map the drawing numbers
    # In old format, they're called 'boule_1', 'boule_2', etc.
    renamed_data = pd.DataFrame()
    renamed_data['date'] = data['date']
    renamed_data['day_of_week'] = data['day_of_week']
    
    # Add draw number (1er_ou_2eme_tirage) - 1=first, 2=second draw of the day
    renamed_data['draw_num'] = data['1er_ou_2eme_tirage'].astype(int)
    
    # Standardize the ball columns
    renamed_data['n1'] = data['boule_1'].astype(int)
    renamed_data['n2'] = data['boule_2'].astype(int)
    renamed_data['n3'] = data['boule_3'].astype(int)
    renamed_data['n4'] = data['boule_4'].astype(int)
    renamed_data['n5'] = data['boule_5'].astype(int)
    renamed_data['lucky'] = data['boule_complementaire'].astype(int)
    
    # Map winner information and prize amounts
    renamed_data['winners_rank1'] = data['nombre_de_gagnant_au_rang1']
    renamed_data['winners_rank2'] = data['nombre_de_gagnant_au_rang2']
    renamed_data['winners_rank3'] = data['nombre_de_gagnant_au_rang3']
    renamed_data['winners_rank4'] = data['nombre_de_gagnant_au_rang4']
    renamed_data['winners_rank5'] = data['nombre_de_gagnant_au_rang5']
    renamed_data['winners_rank6'] = data['nombre_de_gagnant_au_rang6']
    renamed_data['winners_rank7'] = data['nombre_de_gagnant_au_rang7']
    
    # Clean and convert prize amounts
    for i in range(1, 8):
        prize_col = f'rapport_du_rang{i}'
        if prize_col in data.columns:
            try:
                # Try to convert directly first
                renamed_data[f'prize_rank{i}'] = pd.to_numeric(data[prize_col].str.replace(',', '.'), errors='coerce')
            except:
                # If that fails, try more complex cleaning
                renamed_data[f'prize_rank{i}'] = data[prize_col].apply(lambda x: clean_amount(x))
    
    # Set currency
    renamed_data['currency'] = data['devise']
    
    # Add column for total amount if available
    if 'total' in data.columns:
        renamed_data['total_amount'] = data['total'].apply(lambda x: clean_amount(x))
    else:
        # Estimate total jackpot if not available
        renamed_data['total_amount'] = renamed_data['prize_rank1'] * 1.5
    
    # Sort by date
    renamed_data = renamed_data.sort_values(by='date').reset_index(drop=True)
    
    return renamed_data

def parse_french_date(date_str, year=None):
    """
    Parse date string in various French formats
    
    Args:
        date_str: Date string in French format
        year: Known year to use if not present in date string (extracted from annee_numero_de_tirage)
    """
    try:
        # Try basic date parsing
        parsed_date = parse(date_str, dayfirst=True)
        # If the extracted year is provided and doesn't match, override it
        if year and parsed_date.year != year:
            return datetime.date(year, parsed_date.month, parsed_date.day)
        return parsed_date
    except:
        # Try with regex patterns for various formats
        patterns = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
            r'(\d{1,2})-(\d{1,2})-(\d{4})',  # DD-MM-YYYY
            r'(\d{1,2})\.(\d{1,2})\.(\d{4})',  # DD.MM.YYYY
            r'(\d{1,2})/(\d{1,2})',  # DD/MM (year missing)
            r'(\d{1,2})-(\d{1,2})',  # DD-MM (year missing)
            r'(\d{1,2})\.(\d{1,2})'  # DD.MM (year missing)
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_str)
            if match:
                groups = match.groups()
                # If we have DD/MM/YYYY format
                if len(groups) == 3:
                    day, month, extracted_year = groups
                    # Use the provided year if it conflicts with the extracted one
                    use_year = year if year and int(extracted_year) != year else int(extracted_year)
                    return datetime.date(use_year, int(month), int(day))
                # If we have DD/MM format and year is provided
                elif len(groups) == 2 and year:
                    day, month = groups
                    return datetime.date(year, int(month), int(day))
        
        # If all else fails and we have a year, use it with January 1
        if year:
            print(f"Warning: Could not parse date '{date_str}', using January 1 of year {year}")
            return datetime.date(year, 1, 1)
        
        # Absolute fallback
        print(f"Warning: Could not parse date '{date_str}', using today's date")
        return datetime.date.today()

def clean_amount(amount_str):
    """Clean and convert prize amount strings to float values"""
    if pd.isna(amount_str):
        return 0.0
    
    # Convert to string if it's not already
    amount_str = str(amount_str)
    
    # Remove any currency symbols or text
    amount_str = re.sub(r'[^\d,.]', '', amount_str)
    
    # Replace comma with dot for decimal
    amount_str = amount_str.replace(',', '.')
    
    # Try to convert to float
    try:
        return float(amount_str)
    except:
        return 0.0

def import_to_database(data):
    """Import the processed data to the database"""
    count = 0
    
    for _, row in data.iterrows():
        # Prepare data for database
        date = row['date'].date() if hasattr(row['date'], 'date') else row['date']
        numbers = [int(row['n1']), int(row['n2']), int(row['n3']), int(row['n4']), int(row['n5'])]
        lucky = int(row['lucky'])
        day_of_week = row.get('day_of_week', '')
        draw_num = int(row.get('draw_num', 1))  # Default to 1 if not provided
        
        # Prepare winner data
        winners = {
            'rank1': int(row.get('winners_rank1', 0)),
            'rank2': int(row.get('winners_rank2', 0)),
            'rank3': int(row.get('winners_rank3', 0)),
            'rank4': int(row.get('winners_rank4', 0)),
            'rank5': int(row.get('winners_rank5', 0)),
            'rank6': int(row.get('winners_rank6', 0)),
            'rank7': int(row.get('winners_rank7', 0))
        }
        
        # Prepare prize data
        prizes = {
            'rank1': float(row.get('prize_rank1', 0)),
            'rank2': float(row.get('prize_rank2', 0)),
            'rank3': float(row.get('prize_rank3', 0)),
            'rank4': float(row.get('prize_rank4', 0)),
            'rank5': float(row.get('prize_rank5', 0)),
            'rank6': float(row.get('prize_rank6', 0)),
            'rank7': float(row.get('prize_rank7', 0))
        }
        
        # Add currency if available
        currency = row.get('currency', 'EUR')
        
        # Total amount 
        total_amount = float(row.get('total_amount', 0))
        
        # Add to database using the advanced import function
        success = database.add_french_loto_drawing_with_details(
            date,
            numbers,
            lucky,
            day_of_week,
            winners,
            prizes,
            total_amount,
            currency,
            draw_num
        )
        
        if success:
            count += 1
    
    return count

def import_old_loto_file(file_path):
    """Main function to import an old Loto file"""
    processed_data = process_old_loto_csv(file_path)
    
    if isinstance(processed_data, pd.DataFrame) and not processed_data.empty:
        count = import_to_database(processed_data)
        print(f"Successfully imported {count} records from {file_path}")
        return count
    else:
        print(f"No valid data to import from {file_path}")
        return 0

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        import_old_loto_file(file_path)
    else:
        print("Please provide a file path as argument")