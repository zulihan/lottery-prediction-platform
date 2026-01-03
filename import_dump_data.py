#!/usr/bin/env python3
"""
Script to import data from SQL dumps into SQLite database.
Converts PostgreSQL SQL format to SQLite compatible format.
"""

import sqlite3
import re
import os
from datetime import datetime

def import_euromillions_data(db_path='lottery_predictions.db', sql_file='db_dump/euromillions_drawings.sql'):
    """Import Euromillions data from SQL dump to SQLite"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS euromillions_drawings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL UNIQUE,
            day_of_week VARCHAR(20),
            n1 INTEGER NOT NULL,
            n2 INTEGER NOT NULL,
            n3 INTEGER NOT NULL,
            n4 INTEGER NOT NULL,
            n5 INTEGER NOT NULL,
            s1 INTEGER NOT NULL,
            s2 INTEGER NOT NULL
        )
    ''')
    
    # Read SQL file and extract INSERT statements
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all INSERT statements
    insert_pattern = r"INSERT INTO euromillions_drawings \(date, day_of_week, n1, n2, n3, n4, n5, s1, s2\) VALUES \('([^']+)', '([^']+)', (\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\);"
    matches = re.findall(insert_pattern, content)
    
    count = 0
    for match in matches:
        try:
            date_str, day_of_week, n1, n2, n3, n4, n5, s1, s2 = match
            cursor.execute('''
                INSERT OR IGNORE INTO euromillions_drawings 
                (date, day_of_week, n1, n2, n3, n4, n5, s1, s2)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (date_str, day_of_week, int(n1), int(n2), int(n3), int(n4), int(n5), int(s1), int(s2)))
            count += 1
        except Exception as e:
            print(f"Error inserting row: {e}")
            continue
    
    conn.commit()
    conn.close()
    print(f"✅ Imported {count} Euromillions drawings")
    return count

def import_french_loto_data(db_path='lottery_predictions.db', sql_file='db_dump/french_loto_drawings.sql'):
    """Import French Loto data from SQL dump to SQLite"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS french_loto_drawings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            draw_num INTEGER DEFAULT 1,
            n1 INTEGER NOT NULL,
            n2 INTEGER NOT NULL,
            n3 INTEGER NOT NULL,
            n4 INTEGER NOT NULL,
            n5 INTEGER NOT NULL,
            lucky INTEGER,
            winners_rank1 INTEGER,
            winners_rank2 INTEGER,
            winners_rank3 INTEGER,
            winners_rank4 INTEGER,
            winners_rank5 INTEGER,
            winners_rank6 INTEGER,
            winners_rank7 INTEGER,
            prize_rank1 REAL,
            prize_rank2 REAL,
            prize_rank3 REAL,
            prize_rank4 REAL,
            prize_rank5 REAL,
            prize_rank6 REAL,
            prize_rank7 REAL,
            currency VARCHAR(10)
        )
    ''')
    
    # Read SQL file
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all INSERT statements - French Loto format is more complex
    # Pattern: INSERT INTO french_loto_drawings (...) VALUES (...);
    insert_pattern = r"INSERT INTO french_loto_drawings[^;]+;"
    insert_statements = re.findall(insert_pattern, content, re.DOTALL)
    
    count = 0
    for stmt in insert_statements:
        # Extract values from INSERT statement
        values_match = re.search(r"VALUES\s*\((.*?)\);", stmt, re.DOTALL)
        if values_match:
            values_str = values_match.group(1)
            # Parse values (handle NULL, strings, numbers)
            values = []
            current_value = ""
            in_quotes = False
            quote_char = None
            
            for char in values_str:
                if char in ("'", '"') and not in_quotes:
                    in_quotes = True
                    quote_char = char
                    current_value = ""
                elif char == quote_char and in_quotes:
                    in_quotes = False
                    values.append(current_value)
                    current_value = ""
                elif char == ',' and not in_quotes:
                    if current_value.strip():
                        val = current_value.strip()
                        if val.upper() == 'NULL':
                            values.append(None)
                        else:
                            values.append(val)
                    current_value = ""
                else:
                    current_value += char
            
            # Add last value
            if current_value.strip():
                val = current_value.strip()
                if val.upper() == 'NULL':
                    values.append(None)
                else:
                    values.append(val)
            
            # Convert values to proper types
            try:
                # Expected order: date, draw_num, n1-n5, lucky, winners_rank1-7, prize_rank1-7, currency
                date_val = values[0].strip("'\"")
                draw_num = int(values[1]) if values[1] and values[1] != 'NULL' else 1
                n1, n2, n3, n4, n5 = [int(v) for v in values[2:7]]
                lucky = int(values[7]) if values[7] and values[7] != 'NULL' else None
                
                # Winners and prizes (can be NULL)
                winners = [int(v) if v and v != 'NULL' else None for v in values[8:15]]
                prizes = [float(v) if v and v != 'NULL' else None for v in values[15:22]]
                currency = values[22].strip("'\"") if len(values) > 22 and values[22] else 'EUR'
                
                cursor.execute('''
                    INSERT OR IGNORE INTO french_loto_drawings 
                    (date, draw_num, n1, n2, n3, n4, n5, lucky,
                     winners_rank1, winners_rank2, winners_rank3, winners_rank4,
                     winners_rank5, winners_rank6, winners_rank7,
                     prize_rank1, prize_rank2, prize_rank3, prize_rank4,
                     prize_rank5, prize_rank6, prize_rank7, currency)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (date_val, draw_num, n1, n2, n3, n4, n5, lucky) + 
                    tuple(winners) + tuple(prizes) + (currency,))
                count += 1
            except Exception as e:
                print(f"Error inserting row: {e}")
                print(f"Values: {values[:10]}...")
                continue
    
    conn.commit()
    conn.close()
    print(f"✅ Imported {count} French Loto drawings")
    return count

if __name__ == "__main__":
    print("Starting data import...")
    print(f"Database: lottery_predictions.db")
    
    if os.path.exists('db_dump/euromillions_drawings.sql'):
        import_euromillions_data()
    else:
        print("⚠️  euromillions_drawings.sql not found")
    
    if os.path.exists('db_dump/french_loto_drawings.sql'):
        import_french_loto_data()
    else:
        print("⚠️  french_loto_drawings.sql not found")
    
    print("✅ Data import completed!")

