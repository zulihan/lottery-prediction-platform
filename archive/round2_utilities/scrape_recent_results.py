#!/usr/bin/env python3
"""
Script to scrape recent Euromillions results and add them to the database.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import logging
import re
from database import init_db, EuromillionsDrawing, get_all_drawings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import engine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_euromillions_results(start_year=2014, end_year=2025):
    """
    Scrape Euromillions results from the Euro-Millions.com website.
    
    Args:
        start_year: The year to start scraping results from
        end_year: The year to end scraping results at
        
    Returns:
        DataFrame containing the scraped results
    """
    all_results = []
    
    for year in range(start_year, end_year + 1):
        logger.info(f"Scraping results for year {year}...")
        
        # URL for the year's results
        url = f"https://www.euro-millions.com/results-history-{year}"
        
        # Send a request to the website
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find result tables
            result_tables = soup.find_all('table', class_='table table-striped table-bordered table-condensed')
            
            if not result_tables:
                logger.warning(f"No result tables found for year {year}")
                continue
                
            # Process each table (usually one per month)
            for table in result_tables:
                # Find all result rows
                rows = table.find_all('tr')
                
                # Skip header row
                for row in rows[1:]:
                    try:
                        # Extract date
                        date_cell = row.find('td', class_='date')
                        if not date_cell:
                            continue
                            
                        date_str = date_cell.text.strip()
                        date_match = re.search(r'(\d{1,2})(?:st|nd|rd|th)? ([A-Za-z]+) (\d{4})', date_str)
                        if date_match:
                            day, month_name, year = date_match.groups()
                            # Convert month name to number
                            month_dict = {
                                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                                'September': 9, 'October': 10, 'November': 11, 'December': 12
                            }
                            month = month_dict.get(month_name, 1)
                            date = datetime.date(int(year), month, int(day))
                            
                            # Extract day of week
                            day_of_week = row.find('td', class_='day').text.strip() if row.find('td', class_='day') else None
                            
                            # Extract numbers
                            number_cells = row.find_all('li', class_='ball')
                            if len(number_cells) >= 5:
                                main_numbers = [int(num.text.strip()) for num in number_cells[:5]]
                                
                                # Extract star numbers
                                star_cells = row.find_all('li', class_='lucky-star')
                                if len(star_cells) >= 2:
                                    star_numbers = [int(star.text.strip()) for star in star_cells[:2]]
                                    
                                    # Add to results
                                    result = {
                                        'date': date,
                                        'day_of_week': day_of_week,
                                        'n1': main_numbers[0],
                                        'n2': main_numbers[1],
                                        'n3': main_numbers[2],
                                        'n4': main_numbers[3],
                                        'n5': main_numbers[4],
                                        's1': star_numbers[0],
                                        's2': star_numbers[1]
                                    }
                                    all_results.append(result)
                    except Exception as e:
                        logger.error(f"Error processing row: {e}")
                        continue
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching results for year {year}: {e}")
            continue
            
    # Convert to DataFrame
    df = pd.DataFrame(all_results)
    
    # Sort by date
    if not df.empty:
        df = df.sort_values('date', ascending=False)
        
    return df

def add_to_database(df):
    """
    Add scraped results to the database.
    
    Args:
        df: DataFrame containing the results
        
    Returns:
        int: Number of records added
    """
    logger.info(f"Adding {len(df)} results to database...")
    
    # Initialize the database
    init_db()
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Get existing dates in the database
    try:
        existing_df = get_all_drawings()
        existing_dates = set(pd.to_datetime(existing_df['date']).dt.date.tolist())
        logger.info(f"Found {len(existing_dates)} existing dates in database")
    except Exception as e:
        logger.warning(f"Could not fetch existing dates: {e}")
        existing_dates = set()
    
    # Add new records
    count = 0
    for _, row in df.iterrows():
        try:
            # Skip if date already exists
            if row['date'] in existing_dates:
                continue
                
            # Create a new drawing
            drawing = EuromillionsDrawing(
                date=row['date'],
                day_of_week=row['day_of_week'],
                n1=row['n1'],
                n2=row['n2'],
                n3=row['n3'],
                n4=row['n4'],
                n5=row['n5'],
                s1=row['s1'],
                s2=row['s2']
            )
            
            # Add to session
            session.add(drawing)
            count += 1
            
        except Exception as e:
            logger.error(f"Error adding record for {row['date']}: {e}")
            session.rollback()
            continue
    
    # Commit session
    try:
        session.commit()
        logger.info(f"Successfully added {count} new records")
    except Exception as e:
        logger.error(f"Error committing session: {e}")
        session.rollback()
        count = 0
        
    return count

def verify_database():
    """
    Verify the database has a complete set of data.
    """
    try:
        drawings = get_all_drawings()
        logger.info(f"Total drawings in database: {len(drawings)}")
        logger.info(f"Date range: {drawings['date'].min()} to {drawings['date'].max()}")
        
        # Calculate frequency
        drawings['date'] = pd.to_datetime(drawings['date'])
        drawings = drawings.sort_values('date')
        
        # Count drawings per year
        year_counts = drawings.groupby(drawings['date'].dt.year).size()
        logger.info("Drawings per year:")
        for year, count in year_counts.items():
            logger.info(f"  {year}: {count}")
            
        return len(drawings)
    except Exception as e:
        logger.error(f"Error verifying database: {e}")
        return 0

def main():
    """
    Main function to scrape results and add to database.
    """
    # Scrape results
    df = scrape_euromillions_results()
    
    # Check if any results were scraped
    if df.empty:
        logger.error("No results were scraped")
        return
        
    logger.info(f"Scraped {len(df)} results from {df['date'].min()} to {df['date'].max()}")
    
    # Add to database
    count = add_to_database(df)
    
    # Verify database
    total = verify_database()
    
    logger.info(f"Added {count} new records. Total records in database: {total}")

if __name__ == "__main__":
    main()