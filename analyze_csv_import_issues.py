"""
Analyze why only 378 out of 1846 CSV records were imported
"""
import pandas as pd
import os
from datetime import datetime

def parse_date(date_str):
    """Parse date from YYYYMMDD format to datetime.date"""
    try:
        return datetime.strptime(str(date_str), '%Y%m%d').date()
    except:
        return None

def analyze_csv_data():
    """Analyze the CSV data to understand filtering issues"""
    csv_path = "attached_assets/euromillion_all_1749131576125.csv"
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return
    
    try:
        # Read CSV with semicolon separator
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        print(f"Total records in CSV: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        
        # Analyze each filtering step
        valid_dates = 0
        invalid_dates = 0
        valid_numbers = 0
        invalid_numbers = 0
        valid_stars = 0
        invalid_stars = 0
        final_valid = 0
        
        date_issues = []
        number_issues = []
        star_issues = []
        
        for idx, row in df.iterrows():
            # Check date parsing
            draw_date = parse_date(row['date_de_tirage'])
            if draw_date:
                valid_dates += 1
            else:
                invalid_dates += 1
                date_issues.append(f"Row {idx}: date_de_tirage = {row['date_de_tirage']}")
                continue
            
            try:
                # Check numbers
                n1 = int(row['boule_1'])
                n2 = int(row['boule_2'])
                n3 = int(row['boule_3'])
                n4 = int(row['boule_4'])
                n5 = int(row['boule_5'])
                
                if all(1 <= n <= 50 for n in [n1, n2, n3, n4, n5]):
                    valid_numbers += 1
                else:
                    invalid_numbers += 1
                    number_issues.append(f"Row {idx}: numbers = {[n1,n2,n3,n4,n5]}")
                    continue
                
                # Check stars
                s1 = int(row['etoile_1'])
                s2 = int(row['etoile_2'])
                
                if all(1 <= s <= 12 for s in [s1, s2]):
                    valid_stars += 1
                    final_valid += 1
                else:
                    invalid_stars += 1
                    star_issues.append(f"Row {idx}: stars = {[s1,s2]}")
                    
            except Exception as e:
                number_issues.append(f"Row {idx}: conversion error = {str(e)}")
                continue
        
        print(f"\n=== Analysis Results ===")
        print(f"Valid dates: {valid_dates}")
        print(f"Invalid dates: {invalid_dates}")
        print(f"Valid main numbers: {valid_numbers}")
        print(f"Invalid main numbers: {invalid_numbers}")
        print(f"Valid star numbers: {valid_stars}")
        print(f"Invalid star numbers: {invalid_stars}")
        print(f"Final valid records: {final_valid}")
        
        # Show sample issues
        if date_issues:
            print(f"\nSample date issues (first 5):")
            for issue in date_issues[:5]:
                print(f"  {issue}")
        
        if number_issues:
            print(f"\nSample number issues (first 5):")
            for issue in number_issues[:5]:
                print(f"  {issue}")
        
        if star_issues:
            print(f"\nSample star issues (first 5):")
            for issue in star_issues[:5]:
                print(f"  {issue}")
        
        # Check for star number range evolution
        print(f"\n=== Star Number Range Analysis ===")
        star_max_values = []
        for _, row in df.iterrows():
            try:
                s1 = int(row['etoile_1'])
                s2 = int(row['etoile_2'])
                star_max_values.append(max(s1, s2))
            except:
                continue
        
        if star_max_values:
            print(f"Maximum star number found: {max(star_max_values)}")
            print(f"Star numbers > 12: {sum(1 for s in star_max_values if s > 12)}")
            print(f"Star numbers distribution (max per draw):")
            for i in range(1, max(star_max_values) + 1):
                count = sum(1 for s in star_max_values if s == i)
                if count > 0:
                    print(f"  Max star {i}: {count} draws")
        
        # Check date range
        print(f"\n=== Date Range Analysis ===")
        dates = []
        for _, row in df.iterrows():
            date = parse_date(row['date_de_tirage'])
            if date:
                dates.append(date)
        
        if dates:
            dates.sort()
            print(f"Date range: {dates[0]} to {dates[-1]}")
            
            # Count by year
            year_counts = {}
            for date in dates:
                year = date.year
                year_counts[year] = year_counts.get(year, 0) + 1
            
            print(f"Records by year:")
            for year in sorted(year_counts.keys()):
                print(f"  {year}: {year_counts[year]} draws")
        
    except Exception as e:
        print(f"Error analyzing CSV: {str(e)}")

if __name__ == "__main__":
    analyze_csv_data()