"""
Script to remove duplicate French Loto drawings from the database.
For any dates with multiple records, we'll keep the one with the highest ID.
"""
import pandas as pd
from sqlalchemy import text
from database import get_session, init_db, FrenchLotoDrawing

def identify_duplicates(limit=None):
    """
    Identify all dates that have duplicate records in the french_loto_drawings table.
    
    Args:
        limit: Optional limit on the number of duplicate dates to process
        
    Returns:
        list: List of dates that have duplicates
    """
    session = get_session()
    try:
        query = """
            SELECT date
            FROM french_loto_drawings
            GROUP BY date
            HAVING COUNT(*) > 1
            ORDER BY date DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
            
        duplicate_dates = session.execute(text(query)).fetchall()
        
        # Convert to simple list of dates
        return [str(d[0]) for d in duplicate_dates]
    except Exception as e:
        print(f"Error identifying duplicates: {str(e)}")
        return []
    finally:
        session.close()

def remove_duplicates(duplicate_dates, batch_size=50):
    """
    Remove duplicate records, keeping only the one with the highest ID for each date.
    
    Args:
        duplicate_dates: List of dates that have duplicate records
        batch_size: Number of dates to process in a single transaction
        
    Returns:
        int: Number of records removed
    """
    if not duplicate_dates:
        return 0
        
    total_removed = 0
    
    # Process in batches
    for i in range(0, len(duplicate_dates), batch_size):
        batch = duplicate_dates[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1} of {len(duplicate_dates)//batch_size + 1} ({len(batch)} dates)")
        
        session = get_session()
        removed_count = 0
        
        try:
            for date in batch:
                try:
                    # Get all records for this date
                    records = session.query(FrenchLotoDrawing).filter(
                        FrenchLotoDrawing.date == date
                    ).order_by(FrenchLotoDrawing.id).all()
                    
                    if len(records) <= 1:
                        continue
                        
                    # Keep the record with the highest ID (most recently added)
                    highest_id = -1
                    record_to_keep = None
                    for record in records:
                        if record.id > highest_id:
                            highest_id = record.id
                            record_to_keep = record
                    
                    # Delete all other records for this date
                    for record in records:
                        if record.id != record_to_keep.id:
                            session.delete(record)
                            removed_count += 1
                            
                    print(f"Processed date {date}: keeping record ID {record_to_keep.id}, removing {len(records) - 1} duplicates")
                    
                except Exception as e:
                    print(f"Error processing date {date}: {str(e)}")
                    continue
                    
            # Commit batch
            session.commit()
            total_removed += removed_count
            print(f"Committed batch {i//batch_size + 1}: removed {removed_count} duplicates, {total_removed} total")
            
        except Exception as e:
            print(f"Error processing batch: {str(e)}")
            session.rollback()
        finally:
            session.close()
            
    return total_removed

def verify_no_duplicates():
    """
    Verify that no duplicate dates remain in the database.
    
    Returns:
        bool: True if no duplicates remain, False otherwise
    """
    session = get_session()
    try:
        remaining_duplicates = session.execute(text("""
            SELECT COUNT(*) as duplicate_count
            FROM (
                SELECT date
                FROM french_loto_drawings
                GROUP BY date
                HAVING COUNT(*) > 1
            ) as duplicates
        """)).scalar()
        
        return remaining_duplicates == 0
    except Exception as e:
        print(f"Error verifying duplicates: {str(e)}")
        return False
    finally:
        session.close()

def count_records():
    """
    Count the total number of records in the french_loto_drawings table.
    
    Returns:
        int: Total record count
    """
    session = get_session()
    try:
        count = session.query(FrenchLotoDrawing).count()
        return count
    except Exception as e:
        print(f"Error counting records: {str(e)}")
        return 0
    finally:
        session.close()

def main():
    """Main function to remove duplicate records"""
    # Initialize database
    init_db()
    
    # Count records before
    record_count_before = count_records()
    print(f"Record count before: {record_count_before}")
    
    # Process in smaller batches to avoid timeouts
    batch_limit = 25  # Process only 25 duplicate dates at a time
    
    total_removed = 0
    batch_num = 1
    max_batches = 5  # Limit to 5 batches per run to avoid timeouts
    
    while batch_num <= max_batches:
        # Identify next batch of duplicates
        duplicate_dates = identify_duplicates(limit=batch_limit)
        if not duplicate_dates:
            print("No more duplicates to remove")
            break
            
        print(f"Processing batch {batch_num}: Found {len(duplicate_dates)} dates with duplicate records")
        
        # Remove duplicates in this batch
        removed_count = remove_duplicates(duplicate_dates, batch_size=25)
        total_removed += removed_count
        print(f"Batch {batch_num} complete: Removed {removed_count} duplicate records (Total removed: {total_removed})")
        
        # Check if we need to continue
        if len(duplicate_dates) < batch_limit:
            print("Processed all duplicates")
            break
            
        batch_num += 1
    
    print(f"Run complete. Processed {batch_num} batches, removed {total_removed} duplicate records.")
    print("To continue removing duplicates, run this script again.")
    
    # Count records after
    record_count_after = count_records()
    print(f"\nFinal results:")
    print(f"Record count before: {record_count_before}")
    print(f"Record count after: {record_count_after}")
    print(f"Total removed: {record_count_before - record_count_after}")
    
    # Verify no duplicates remain
    if verify_no_duplicates():
        print("Success: No duplicate dates remain in the database")
    else:
        print("Warning: Some duplicate dates still remain in the database")

if __name__ == "__main__":
    main()