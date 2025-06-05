"""
Check the actual database using the same connection method as the Streamlit app
"""
import os
from sqlalchemy import create_engine, text
import pandas as pd

def check_database_with_sqlalchemy():
    """Check database using SQLAlchemy like the Streamlit app"""
    try:
        # Use the same DATABASE_URL as the Streamlit app
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("No DATABASE_URL found")
            return
        
        engine = create_engine(database_url)
        
        # Check what tables exist
        with engine.connect() as conn:
            # PostgreSQL way to list tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            
            print(f"Available tables:")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Check each table
            for table in tables:
                table_name = table[0]
                print(f"\n{table_name}:")
                
                # Get row count
                count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = count_result.fetchone()[0]
                print(f"  Rows: {count}")
                
                if count > 0:
                    # Get column info
                    cols_result = conn.execute(text(f"""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_name = '{table_name}'
                        ORDER BY ordinal_position
                    """))
                    columns = cols_result.fetchall()
                    print("  Columns:")
                    for col in columns:
                        print(f"    {col[0]} ({col[1]})")
                    
                    # Sample data
                    sample_result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 3"))
                    sample = sample_result.fetchall()
                    print("  Sample data:")
                    for row in sample:
                        print(f"    {row}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_database_with_sqlalchemy()