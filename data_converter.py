import pandas as pd
import sys
import re
from datetime import datetime

def convert_french_date(date_str):
    """Convert date from French format DD/MM/YYYY to ISO format YYYY-MM-DD"""
    if isinstance(date_str, str) and re.match(r'\d{2}/\d{2}/\d{4}', date_str):
        day, month, year = date_str.split('/')
        return f"{year}-{month}-{day}"
    return date_str

def get_day_of_week(day_abbr):
    """Convert French day abbreviation to full English day name."""
    mapping = {
        'VE': 'Friday',
        'MA': 'Tuesday',
        'VENDREDI': 'Friday',
        'MARDI': 'Tuesday'
    }
    return mapping.get(day_abbr, day_abbr)

def convert_euromillions_data(input_file, output_file):
    """Convert Euromillions data from French format to application format."""
    # Read the data
    data = pd.read_csv(input_file, sep=';')
    
    # Select relevant columns and rename
    try:
        if 'boule_1' in data.columns:
            # Format with 'boule_' prefix
            cols = {
                'date_de_tirage': 'date',
                'jour_de_tirage': 'day_of_week',
                'boule_1': 'n1',
                'boule_2': 'n2',
                'boule_3': 'n3',
                'boule_4': 'n4',
                'boule_5': 'n5',
                'etoile_1': 's1',
                'etoile_2': 's2'
            }
        else:
            # Try alternative format
            possible_cols = [
                ['date', 'day_of_week', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2'],
                ['date_de_tirage', 'jour_de_tirage', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']
            ]
            
            for col_set in possible_cols:
                if all(col in data.columns for col in col_set):
                    cols = {col: col for col in col_set}
                    break
            else:
                # If no match found, use generic column indices
                print("Couldn't match column names, using generic indices")
                cols = {
                    data.columns[2]: 'date',
                    data.columns[1]: 'day_of_week',
                    data.columns[4]: 'n1',
                    data.columns[5]: 'n2',
                    data.columns[6]: 'n3',
                    data.columns[7]: 'n4',
                    data.columns[8]: 'n5',
                    data.columns[9]: 's1',
                    data.columns[10]: 's2'
                }
    
        # Select and rename columns
        df = data[list(cols.keys())].rename(columns=cols)
        
        # Convert date format
        df['date'] = df['date'].apply(convert_french_date)
        
        # Convert day of week
        df['day_of_week'] = df['day_of_week'].apply(get_day_of_week)
        
        # Ensure numerical columns are integers
        for col in ['n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']:
            df[col] = df[col].astype(int)
        
        # Sort by date (descending) to have newest draws first
        df = df.sort_values('date', ascending=False)
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"Successfully converted {len(df)} records to {output_file}")
        
    except Exception as e:
        print(f"Error converting data: {str(e)}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python data_converter.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_euromillions_data(input_file, output_file)