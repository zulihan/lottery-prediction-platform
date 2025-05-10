"""
Script to clean up future dates from the French Loto database.
This is needed to handle the problem where our environment has a future date
but we want to keep only real historical data.
"""

import database
from sqlalchemy import text
from datetime import datetime

def clean_french_loto_future_dates():
    """
    Remove all French Loto drawings with dates after January 1, 2023
    which are likely future projections rather than actual historical data.
    """
    # Reference date for what we consider "historical" vs "future"
    reference_date = datetime(2023, 1, 1).date()
    
    # Get a database connection
    conn = database.get_db_connection()
    
    if conn is None:
        print("Error: Could not connect to database")
        return False
    
    try:
        # Delete all records with dates after our reference date
        result = conn.execute(
            text("DELETE FROM french_loto_drawings WHERE date > :ref_date"),
            {"ref_date": reference_date}
        )
        
        deleted_count = result.rowcount
        conn.commit()
        
        print(f"Successfully deleted {deleted_count} French Loto drawings with dates after {reference_date}")
        return True
        
    except Exception as e:
        print(f"Error cleaning future dates: {str(e)}")
        return False
    finally:
        conn.close()

def main():
    """Main function to run the clean-up"""
    print("Cleaning future dates from French Loto database...")
    success = clean_french_loto_future_dates()
    
    if success:
        print("Clean-up completed successfully")
    else:
        print("Clean-up failed")

if __name__ == "__main__":
    main()