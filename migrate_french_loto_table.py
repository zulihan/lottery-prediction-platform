#!/usr/bin/env python3
"""
Script to migrate the french_loto_drawings table to add draw_num column
and update the unique constraint
"""
import sys
import database
from sqlalchemy import text

def migrate_table():
    """
    Add draw_num column to french_loto_drawings table and 
    update the unique constraint
    """
    # Get database connection
    try:
        conn = database.get_db_connection()
        
        # Check if column already exists (avoid errors if script is run multiple times)
        check_sql = """
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'french_loto_drawings' AND column_name = 'draw_num';
        """
        result = conn.execute(text(check_sql))
        if result.rowcount > 0:
            print("Column draw_num already exists, skipping creation")
        else:
            # Add draw_num column with default value 1
            add_column_sql = """
            ALTER TABLE french_loto_drawings 
            ADD COLUMN draw_num INTEGER NOT NULL DEFAULT 1;
            """
            conn.execute(text(add_column_sql))
            print("Added draw_num column")
        
        # Check if unique constraint exists and drop it
        check_constraint_sql = """
        SELECT constraint_name FROM information_schema.table_constraints
        WHERE table_name = 'french_loto_drawings' 
        AND constraint_type = 'UNIQUE';
        """
        result = conn.execute(text(check_constraint_sql))
        constraints = result.fetchall()
        
        # Drop existing unique constraint(s) if any
        for constraint in constraints:
            drop_constraint_sql = f"""
            ALTER TABLE french_loto_drawings
            DROP CONSTRAINT {constraint[0]};
            """
            conn.execute(text(drop_constraint_sql))
            print(f"Dropped constraint: {constraint[0]}")
        
        # Add new unique constraint on (date, draw_num)
        add_constraint_sql = """
        ALTER TABLE french_loto_drawings
        ADD CONSTRAINT unique_french_loto_drawing UNIQUE (date, draw_num);
        """
        conn.execute(text(add_constraint_sql))
        print("Added new unique constraint on (date, draw_num)")
        
        # Commit changes
        conn.commit()
        print("Migration completed successfully")
        return True
        
    except Exception as e:
        print(f"Error migrating table: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    # Initialize the database
    database.init_db()
    
    print("Migrating french_loto_drawings table...")
    
    # Perform the migration
    success = migrate_table()
    
    if success:
        print("Migration completed successfully.")
        
        # Verify the structure
        conn = database.get_db_connection()
        try:
            # Check column exists
            check_sql = """
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'french_loto_drawings'
            ORDER BY ordinal_position;
            """
            result = conn.execute(text(check_sql))
            columns = result.fetchall()
            
            print("\nTable structure:")
            for col in columns:
                print(f"  {col[0]} ({col[1]})")
                
            # Check constraint exists
            check_constraint_sql = """
            SELECT constraint_name, constraint_type
            FROM information_schema.table_constraints
            WHERE table_name = 'french_loto_drawings';
            """
            result = conn.execute(text(check_constraint_sql))
            constraints = result.fetchall()
            
            print("\nTable constraints:")
            for constraint in constraints:
                print(f"  {constraint[0]} ({constraint[1]})")
                
        except Exception as e:
            print(f"Error verifying structure: {str(e)}")
        finally:
            conn.close()
    else:
        print("Migration failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()