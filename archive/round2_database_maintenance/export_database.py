import os
import json
from datetime import datetime
from database import get_session, EuromillionsDrawing, FrenchLotoDrawing, GeneratedCombination, UserSavedCombination, FrenchLotoPrediction, FrenchLotoPlayedCombination, StrategyTestResult

def export_euromillions():
    session = get_session()
    drawings = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date).all()
    
    with open('db_dump/euromillions_drawings.sql', 'w') as f:
        f.write("-- Euromillions Drawings Dump\n")
        f.write("-- Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
        f.write("CREATE TABLE IF NOT EXISTS euromillions_drawings (\n")
        f.write("    id SERIAL PRIMARY KEY,\n")
        f.write("    date DATE NOT NULL UNIQUE,\n")
        f.write("    day_of_week VARCHAR(20),\n")
        f.write("    n1 INTEGER NOT NULL,\n")
        f.write("    n2 INTEGER NOT NULL,\n")
        f.write("    n3 INTEGER NOT NULL,\n")
        f.write("    n4 INTEGER NOT NULL,\n")
        f.write("    n5 INTEGER NOT NULL,\n")
        f.write("    s1 INTEGER NOT NULL,\n")
        f.write("    s2 INTEGER NOT NULL\n")
        f.write(");\n\n")
        
        for d in drawings:
            day = d.day_of_week if d.day_of_week else 'NULL'
            day_val = f"'{day}'" if day != 'NULL' else 'NULL'
            f.write(f"INSERT INTO euromillions_drawings (date, day_of_week, n1, n2, n3, n4, n5, s1, s2) VALUES ('{d.date}', {day_val}, {d.n1}, {d.n2}, {d.n3}, {d.n4}, {d.n5}, {d.s1}, {d.s2});\n")
    
    print(f"Exported {len(drawings)} Euromillions drawings")
    session.close()

def export_french_loto():
    session = get_session()
    drawings = session.query(FrenchLotoDrawing).order_by(FrenchLotoDrawing.date).all()
    
    with open('db_dump/french_loto_drawings.sql', 'w') as f:
        f.write("-- French Loto Drawings Dump\n")
        f.write("-- Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
        f.write("CREATE TABLE IF NOT EXISTS french_loto_drawings (\n")
        f.write("    id SERIAL PRIMARY KEY,\n")
        f.write("    date DATE NOT NULL,\n")
        f.write("    draw_num INTEGER DEFAULT 1,\n")
        f.write("    day_of_week VARCHAR(20),\n")
        f.write("    n1 INTEGER NOT NULL,\n")
        f.write("    n2 INTEGER NOT NULL,\n")
        f.write("    n3 INTEGER NOT NULL,\n")
        f.write("    n4 INTEGER NOT NULL,\n")
        f.write("    n5 INTEGER NOT NULL,\n")
        f.write("    lucky INTEGER NOT NULL,\n")
        f.write("    winners_rank1 INTEGER,\n")
        f.write("    winners_rank2 INTEGER,\n")
        f.write("    winners_rank3 INTEGER,\n")
        f.write("    winners_rank4 INTEGER,\n")
        f.write("    winners_rank5 INTEGER,\n")
        f.write("    winners_rank6 INTEGER,\n")
        f.write("    winners_rank7 INTEGER,\n")
        f.write("    prize_rank1 FLOAT,\n")
        f.write("    prize_rank2 FLOAT,\n")
        f.write("    prize_rank3 FLOAT,\n")
        f.write("    prize_rank4 FLOAT,\n")
        f.write("    prize_rank5 FLOAT,\n")
        f.write("    prize_rank6 FLOAT,\n")
        f.write("    prize_rank7 FLOAT,\n")
        f.write("    total_amount FLOAT,\n")
        f.write("    currency VARCHAR(10),\n")
        f.write("    UNIQUE(date, draw_num)\n")
        f.write(");\n\n")
        
        for d in drawings:
            day = d.day_of_week if d.day_of_week else 'NULL'
            day_val = f"'{day}'" if day != 'NULL' else 'NULL'
            curr = d.currency if d.currency else 'EUR'
            f.write(f"INSERT INTO french_loto_drawings (date, draw_num, day_of_week, n1, n2, n3, n4, n5, lucky, currency) VALUES ('{d.date}', {d.draw_num or 1}, {day_val}, {d.n1}, {d.n2}, {d.n3}, {d.n4}, {d.n5}, {d.lucky}, '{curr}');\n")
    
    print(f"Exported {len(drawings)} French Loto drawings")
    session.close()

def export_csv():
    session = get_session()
    
    # Euromillions CSV
    drawings = session.query(EuromillionsDrawing).order_by(EuromillionsDrawing.date).all()
    with open('db_dump/euromillions_drawings.csv', 'w') as f:
        f.write("date,n1,n2,n3,n4,n5,s1,s2\n")
        for d in drawings:
            f.write(f"{d.date},{d.n1},{d.n2},{d.n3},{d.n4},{d.n5},{d.s1},{d.s2}\n")
    print(f"Exported {len(drawings)} Euromillions to CSV")
    
    # French Loto CSV
    drawings = session.query(FrenchLotoDrawing).order_by(FrenchLotoDrawing.date).all()
    with open('db_dump/french_loto_drawings.csv', 'w') as f:
        f.write("date,n1,n2,n3,n4,n5,lucky\n")
        for d in drawings:
            f.write(f"{d.date},{d.n1},{d.n2},{d.n3},{d.n4},{d.n5},{d.lucky}\n")
    print(f"Exported {len(drawings)} French Loto to CSV")
    
    session.close()

if __name__ == '__main__':
    os.makedirs('db_dump', exist_ok=True)
    export_euromillions()
    export_french_loto()
    export_csv()
    print("\nDatabase dump complete! Files in db_dump/ folder")
