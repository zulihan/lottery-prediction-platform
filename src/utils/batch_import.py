"""
Batch Import Utilities

Utilities for importing large datasets with date filtering and batch processing
to prevent database timeouts and rate limits.
"""

import csv
import pandas as pd
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)


def import_csv_in_batches(filename, insert_function, batch_size=25,
                          start_date=None, end_date=None,
                          date_column='date', date_format='%Y-%m-%d'):
    """
    Import CSV in date-filtered batches to prevent timeouts.

    Args:
        filename: Path to CSV file
        insert_function: Function to call for batch insertion (receives list of records)
        batch_size: Number of records per batch (default 25)
        start_date: Start date filter (YYYY-MM-DD string or datetime)
        end_date: End date filter (YYYY-MM-DD string or datetime)
        date_column: Name of date column in CSV
        date_format: Date format string for parsing

    Returns:
        dict: Import statistics
    """
    logger.info(f"Starting batch import from {filename}")
    logger.info(f"Batch size: {batch_size}, Date range: {start_date} to {end_date}")

    # Parse date filters
    parsed_start = None
    parsed_end = None

    if start_date:
        if isinstance(start_date, str):
            parsed_start = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            parsed_start = start_date

    if end_date:
        if isinstance(end_date, str):
            parsed_end = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            parsed_end = end_date

    batch = []
    total_imported = 0
    total_skipped = 0
    total_errors = 0

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row_num, row in enumerate(reader, 1):
                try:
                    # Parse and filter by date
                    if date_column in row:
                        record_date = datetime.strptime(row[date_column], date_format)

                        # Apply date filters
                        if parsed_start and record_date < parsed_start:
                            total_skipped += 1
                            continue
                        if parsed_end and record_date > parsed_end:
                            total_skipped += 1
                            continue

                    batch.append(row)

                    # Process batch when it reaches size limit
                    if len(batch) >= batch_size:
                        success = insert_function(batch)
                        if success:
                            total_imported += len(batch)
                            logger.info(f"Imported {total_imported} records (skipped {total_skipped})...")
                        else:
                            total_errors += len(batch)
                            logger.error(f"Failed to import batch at row {row_num}")

                        batch = []

                        # Small delay to avoid rate limits
                        time.sleep(0.1)

                except Exception as e:
                    logger.error(f"Error processing row {row_num}: {e}")
                    total_errors += 1

            # Process remaining records
            if batch:
                success = insert_function(batch)
                if success:
                    total_imported += len(batch)
                    logger.info(f"Imported final batch. Total: {total_imported} records")
                else:
                    total_errors += len(batch)
                    logger.error("Failed to import final batch")

    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return {
            'success': False,
            'error': 'File not found',
            'total_imported': 0
        }
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return {
            'success': False,
            'error': str(e),
            'total_imported': total_imported
        }

    return {
        'success': True,
        'total_imported': total_imported,
        'total_skipped': total_skipped,
        'total_errors': total_errors,
        'filename': filename
    }


def import_dataframe_in_batches(df, insert_function, batch_size=25,
                                start_date=None, end_date=None,
                                date_column='date'):
    """
    Import pandas DataFrame in batches with date filtering.

    Args:
        df: pandas DataFrame
        insert_function: Function to call for batch insertion
        batch_size: Number of records per batch
        start_date: Start date filter
        end_date: End date filter
        date_column: Name of date column

    Returns:
        dict: Import statistics
    """
    logger.info(f"Starting batch import from DataFrame ({len(df)} rows)")

    # Apply date filters
    if start_date or end_date:
        # Ensure date column is datetime
        if date_column in df.columns:
            df[date_column] = pd.to_datetime(df[date_column])

            if start_date:
                start_dt = pd.to_datetime(start_date)
                df = df[df[date_column] >= start_dt]

            if end_date:
                end_dt = pd.to_datetime(end_date)
                df = df[df[date_column] <= end_dt]

    total_imported = 0
    total_errors = 0

    # Process in batches
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i+batch_size]
        batch_records = batch_df.to_dict('records')

        try:
            success = insert_function(batch_records)
            if success:
                total_imported += len(batch_records)
                logger.info(f"Imported {total_imported}/{len(df)} records...")
            else:
                total_errors += len(batch_records)
                logger.error(f"Failed to import batch {i//batch_size + 1}")

            # Small delay to avoid rate limits
            time.sleep(0.1)

        except Exception as e:
            logger.error(f"Error importing batch: {e}")
            total_errors += len(batch_records)

    return {
        'success': True,
        'total_imported': total_imported,
        'total_errors': total_errors,
        'total_rows': len(df)
    }


def validate_csv_structure(filename, required_columns, max_rows_to_check=10):
    """
    Validate CSV file structure before importing.

    Args:
        filename: Path to CSV file
        required_columns: List of required column names
        max_rows_to_check: Maximum rows to read for validation

    Returns:
        dict: Validation results
    """
    try:
        # Read first few rows
        df = pd.read_csv(filename, nrows=max_rows_to_check)

        # Check for required columns (case-insensitive)
        df_columns_lower = [col.lower() for col in df.columns]
        required_lower = [col.lower() for col in required_columns]

        missing_columns = [col for col in required_lower if col not in df_columns_lower]

        if missing_columns:
            return {
                'valid': False,
                'error': f"Missing required columns: {missing_columns}",
                'found_columns': list(df.columns),
                'row_count': len(df)
            }

        return {
            'valid': True,
            'found_columns': list(df.columns),
            'row_count': len(df),
            'sample_data': df.head(3).to_dict('records')
        }

    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }


def estimate_import_time(file_size_mb, batch_size=25, avg_batch_time=0.5):
    """
    Estimate time required for import based on file size.

    Args:
        file_size_mb: File size in megabytes
        batch_size: Batch size
        avg_batch_time: Average time per batch in seconds

    Returns:
        dict: Time estimates
    """
    # Rough estimate: 1MB ≈ 10,000 rows for CSV
    estimated_rows = file_size_mb * 10000
    estimated_batches = estimated_rows / batch_size
    estimated_time_seconds = estimated_batches * avg_batch_time

    return {
        'estimated_rows': int(estimated_rows),
        'estimated_batches': int(estimated_batches),
        'estimated_time_seconds': estimated_time_seconds,
        'estimated_time_minutes': round(estimated_time_seconds / 60, 1),
        'recommended_batch_size': batch_size
    }


# Example insert function (for reference)
def example_insert_function(batch_records):
    """
    Example insert function signature.

    Args:
        batch_records: List of dict records to insert

    Returns:
        bool: Success status
    """
    # Example implementation:
    # for record in batch_records:
    #     db.insert(record)
    # return True
    logger.info(f"Inserting {len(batch_records)} records...")
    return True


# Example usage
if __name__ == "__main__":
    # Validate CSV
    validation = validate_csv_structure(
        'example.csv',
        required_columns=['date', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']
    )
    print(f"Validation: {validation}")

    # Import with date filtering
    if validation['valid']:
        results = import_csv_in_batches(
            'example.csv',
            insert_function=example_insert_function,
            batch_size=25,
            start_date='2024-01-01',
            end_date='2024-12-31'
        )
        print(f"Import results: {results}")
