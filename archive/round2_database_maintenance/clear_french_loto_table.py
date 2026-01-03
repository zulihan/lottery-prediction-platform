"""
Script to clear all data from the French Loto table
"""

import database
from sqlalchemy import text

def clear_french_loto_table():
    """
    Delete all records from the french_loto_drawings table
    """
    # Get a database connection
    conn = database.get_db_connection()
    
    if conn is None:
        print("Error: Could not connect to database")
        return False
    
    try:
        # Delete all records
        result = conn.execute(text("DELETE FROM french_loto_drawings"))
        
        deleted_count = result.rowcount
        conn.commit()
        
        print(f"Successfully deleted {deleted_count} French Loto drawings from the table")
        return True
        
    except Exception as e:
        print(f"Error clearing French Loto table: {str(e)}")
        return False
    finally:
        conn.close()

def main():
    """Main function to clear the table"""
    print("Clearing French Loto table...")
    success = clear_french_loto_table()
    
    if success:
        print("Table cleared successfully")
    else:
        print("Failed to clear table")

if __name__ == "__main__":
    main()