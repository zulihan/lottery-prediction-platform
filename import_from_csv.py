#!/usr/bin/env python3
"""
Script to import data from CSV files into SQLite database.
"""

import sqlite3
import pandas as pd
import os

def import_euromillions_from_csv(db_path='lottery_predictions.db', csv_file='db_dump/euromillions_drawings.csv'):
    """Import Euromillions data from CSV to SQLite"""
    if not os.path.exists(csv_file):
        print(f"⚠️  {csv_file} not found")
        return 0
    
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
    
    # Read CSV
    df = pd.read_csv(csv_file)
    
    # Insert data
    count = 0
    for _, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO euromillions_drawings 
                (date, day_of_week, n1, n2, n3, n4, n5, s1, s2)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['date'],
                row.get('day_of_week', None),
                int(row['n1']), int(row['n2']), int(row['n3']), 
                int(row['n4']), int(row['n5']),
                int(row['s1']), int(row['s2'])
            ))
            count += 1
        except Exception as e:
            print(f"Error inserting row: {e}")
            continue
    
    conn.commit()
    conn.close()
    print(f"✅ Imported {count} Euromillions drawings from CSV")
    return count

def import_french_loto_from_csv(db_path='lottery_predictions.db', csv_file='db_dump/french_loto_drawings.csv'):
    """Import French Loto data from CSV to SQLite"""
    if not os.path.exists(csv_file):
        print(f"⚠️  {csv_file} not found")
        return 0
    
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
    
    # Read CSV
    df = pd.read_csv(csv_file)
    
    # Insert data
    count = 0
    for _, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO french_loto_drawings 
                (date, draw_num, n1, n2, n3, n4, n5, lucky,
                 winners_rank1, winners_rank2, winners_rank3, winners_rank4,
                 winners_rank5, winners_rank6, winners_rank7,
                 prize_rank1, prize_rank2, prize_rank3, prize_rank4,
                 prize_rank5, prize_rank6, prize_rank7, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['date'],
                int(row.get('draw_num', 1)),
                int(row['n1']), int(row['n2']), int(row['n3']), 
                int(row['n4']), int(row['n5']),
                int(row.get('lucky', 0)) if pd.notna(row.get('lucky')) else None,
                int(row.get('winners_rank1', 0)) if pd.notna(row.get('winners_rank1')) else None,
                int(row.get('winners_rank2', 0)) if pd.notna(row.get('winners_rank2')) else None,
                int(row.get('winners_rank3', 0)) if pd.notna(row.get('winners_rank3')) else None,
                int(row.get('winners_rank4', 0)) if pd.notna(row.get('winners_rank4')) else None,
                int(row.get('winners_rank5', 0)) if pd.notna(row.get('winners_rank5')) else None,
                int(row.get('winners_rank6', 0)) if pd.notna(row.get('winners_rank6')) else None,
                int(row.get('winners_rank7', 0)) if pd.notna(row.get('winners_rank7')) else None,
                float(row.get('prize_rank1', 0)) if pd.notna(row.get('prize_rank1')) else None,
                float(row.get('prize_rank2', 0)) if pd.notna(row.get('prize_rank2')) else None,
                float(row.get('prize_rank3', 0)) if pd.notna(row.get('prize_rank3')) else None,
                float(row.get('prize_rank4', 0)) if pd.notna(row.get('prize_rank4')) else None,
                float(row.get('prize_rank5', 0)) if pd.notna(row.get('prize_rank5')) else None,
                float(row.get('prize_rank6', 0)) if pd.notna(row.get('prize_rank6')) else None,
                float(row.get('prize_rank7', 0)) if pd.notna(row.get('prize_rank7')) else None,
                str(row.get('currency', 'EUR'))
            ))
            count += 1
        except Exception as e:
            print(f"Error inserting row {count}: {e}")
            print(f"Row data: {row.to_dict()}")
            continue
    
    conn.commit()
    conn.close()
    print(f"✅ Imported {count} French Loto drawings from CSV")
    return count

if __name__ == "__main__":
    print("Starting CSV data import...")
    print(f"Database: lottery_predictions.db")
    
    euromillions_count = import_euromillions_from_csv()
    french_loto_count = import_french_loto_from_csv()
    
    print(f"\n✅ Data import completed!")
    print(f"   - Euromillions: {euromillions_count} drawings")
    print(f"   - French Loto: {french_loto_count} drawings")

