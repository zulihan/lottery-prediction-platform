import pandas as pd
import os
import sys
from datetime import datetime
from database import init_db, EuromillionsDrawing, session
from data_converter import convert_french_date

def process_french_csv(file_path):
    """
    Process a CSV file in French format and extract the relevant Euromillions data.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame with processed data
    """
    try:
        # Read the CSV file with semicolons as separators
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        
        # Map the French column names to our format
        column_mapping = {
            'date_de_tirage': 'date',
            'jour_de_tirage': 'day_abbr',
            'boule_1': 'n1',
            'boule_2': 'n2',
            'boule_3': 'n3',
            'boule_4': 'n4',
            'boule_5': 'n5',
            'etoile_1': 's1',
            'etoile_2': 's2'
        }
        
        # Select only the columns we need
        needed_columns = list(column_mapping.keys())
        
        # Check if all needed columns exist in the dataframe
        missing_columns = [col for col in needed_columns if col not in df.columns]
        if missing_columns:
            print(f"Error: The following columns are missing from the CSV file: {', '.join(missing_columns)}")
            print(f"Available columns: {', '.join(df.columns)}")
            return None
        
        # Select and rename columns
        processed_df = df[needed_columns].rename(columns=column_mapping)
        
        # Convert date format
        processed_df['date'] = processed_df['date'].apply(convert_french_date)
        
        # Map day abbreviations to full English day names
        day_mapping = {
            'LU': 'Monday',
            'MA': 'Tuesday',
            'ME': 'Wednesday',
            'JE': 'Thursday',
            'VE': 'Friday',
            'SA': 'Saturday',
            'DI': 'Sunday'
        }
        processed_df['day_of_week'] = processed_df['day_abbr'].map(day_mapping)
        
        # Drop the day_abbr column
        processed_df = processed_df.drop('day_abbr', axis=1)
        
        return processed_df
        
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")
        return None

def load_data_to_db(file_path):
    """
    Load Euromillions data from a CSV file to the database.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Number of records inserted
    """
    try:
        # Process the CSV file
        df = process_french_csv(file_path)
        if df is None:
            return 0
        
        count = 0
        for _, row in df.iterrows():
            # Check if this drawing already exists
            existing = session.query(EuromillionsDrawing).filter_by(date=row['date']).first()
            if existing:
                continue
                
            # Create new drawing record
            drawing = EuromillionsDrawing(
                date=row['date'],
                day_of_week=row['day_of_week'],
                n1=int(row['n1']),
                n2=int(row['n2']),
                n3=int(row['n3']),
                n4=int(row['n4']),
                n5=int(row['n5']),
                s1=int(row['s1']),
                s2=int(row['s2'])
            )
            
            # Add to the database
            session.add(drawing)
            count += 1
        
        # Commit changes
        if count > 0:
            session.commit()
            
        return count
    
    except Exception as e:
        print(f"Error loading data to database: {str(e)}")
        session.rollback()
        return 0

def main():
    # Initialize the database
    init_db()
    
    # Process all CSV files in attached_assets directory
    csv_files = [f for f in os.listdir('attached_assets') if f.endswith('.csv')]
    
    total_records = 0
    for csv_file in csv_files:
        file_path = os.path.join('attached_assets', csv_file)
        print(f"Processing {file_path}...")
        records = load_data_to_db(file_path)
        total_records += records
        print(f"Added {records} new records from {csv_file}")
    
    print(f"Total new records added to database: {total_records}")
    
    # Also copy a processed version to sample_data for the app to use
    if total_records > 0:
        # Get all data from database
        from database import get_all_drawings
        all_data = get_all_drawings()
        
        # Save to sample_data directory
        sample_path = 'sample_data/sample_euromillions.csv'
        all_data.to_csv(sample_path, index=False)
        print(f"Saved {len(all_data)} records to {sample_path}")

if __name__ == "__main__":
    main()