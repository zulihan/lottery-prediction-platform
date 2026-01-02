"""
Analyze the logic behind integrating June 3 winning numbers into new combinations
Question: On what basis should we integrate recent winning numbers?
"""
import os
from sqlalchemy import create_engine, text
import pandas as pd
from collections import Counter

def analyze_winning_number_patterns():
    """Analyze if recent winning numbers have any predictive value"""
    
    try:
        database_url = os.getenv('DATABASE_URL')
        engine = create_engine(database_url)
        
        # Get recent draws to analyze winning number patterns
        df = pd.read_sql_query("""
            SELECT id, date, n1, n2, n3, n4, n5, s1, s2 
            FROM euromillions_drawings 
            ORDER BY date DESC
            LIMIT 100
        """, engine)
        
        print(f"🔍 WINNING NUMBER INTEGRATION ANALYSIS")
        print("=" * 45)
        
        # June 3 winning numbers
        june_3_numbers = [12, 15, 38, 47, 48]
        june_3_stars = [5, 7]
        
        print(f"June 3 winners: {june_3_numbers} / {june_3_stars}")
        
        # Analyze if winning numbers appear again in subsequent draws
        winning_reappearance_analysis = []
        
        for i in range(len(df) - 5):  # Analyze 5 draws after each draw
            current_draw = df.iloc[i]
            current_numbers = [current_draw['n1'], current_draw['n2'], current_draw['n3'], 
                             current_draw['n4'], current_draw['n5']]
            
            # Check next 5 draws
            for j in range(1, 6):
                if i + j < len(df):
                    next_draw = df.iloc[i + j]
                    next_numbers = [next_draw['n1'], next_draw['n2'], next_draw['n3'], 
                                  next_draw['n4'], next_draw['n5']]
                    
                    # Count overlapping numbers
                    overlap = len(set(current_numbers) & set(next_numbers))
                    winning_reappearance_analysis.append({
                        'draws_apart': j,
                        'overlap': overlap,
                        'current_date': current_draw['date'],
                        'next_date': next_draw['date']
                    })
        
        # Calculate statistics
        avg_overlap_by_distance = {}
        for distance in range(1, 6):
            overlaps = [x['overlap'] for x in winning_reappearance_analysis if x['draws_apart'] == distance]
            if overlaps:
                avg_overlap_by_distance[distance] = sum(overlaps) / len(overlaps)
        
        print(f"\n📊 WINNING NUMBER REAPPEARANCE ANALYSIS:")
        print(f"Average overlapping numbers in subsequent draws:")
        for distance, avg_overlap in avg_overlap_by_distance.items():
            print(f"   {distance} draw(s) later: {avg_overlap:.2f} numbers on average")
        
        # Random baseline calculation
        # If numbers were completely random, what overlap would we expect?
        total_numbers = 50
        numbers_per_draw = 5
        expected_random_overlap = (numbers_per_draw * numbers_per_draw) / total_numbers
        
        print(f"\n🎲 RANDOM BASELINE:")
        print(f"   Expected overlap if random: {expected_random_overlap:.2f} numbers")
        print(f"   Actual overlap (1 draw later): {avg_overlap_by_distance.get(1, 0):.2f} numbers")
        
        if avg_overlap_by_distance.get(1, 0) > expected_random_overlap:
            print(f"   ✅ Recent winners appear MORE than random chance")
            integration_justified = "MATHEMATICAL"
        elif avg_overlap_by_distance.get(1, 0) < expected_random_overlap:
            print(f"   ❌ Recent winners appear LESS than random chance")
            integration_justified = "NOT_MATHEMATICAL"
        else:
            print(f"   ⚖️  Recent winners appear at random chance level")
            integration_justified = "NEUTRAL"
        
        return integration_justified, avg_overlap_by_distance, expected_random_overlap
        
    except Exception as e:
        print(f"Analysis error: {e}")
        return None, None, None

def analyze_june_3_frequency_basis():
    """Analyze if June 3 numbers were already frequent historically"""
    
    try:
        database_url = os.getenv('DATABASE_URL')
        engine = create_engine(database_url)
        
        # Get all historical data
        df = pd.read_sql_query("""
            SELECT n1, n2, n3, n4, n5 
            FROM euromillions_drawings 
            ORDER BY date DESC
        """, engine)
        
        # Count all number frequencies
        all_numbers = []
        for _, row in df.iterrows():
            numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            for num in numbers:
                if pd.notna(num) and 1 <= int(num) <= 50:
                    all_numbers.append(int(num))
        
        number_freq = Counter(all_numbers)
        total_positions = len(all_numbers)
        
        june_3_numbers = [12, 15, 38, 47, 48]
        
        print(f"\n🎯 JUNE 3 NUMBERS - HISTORICAL FREQUENCY BASIS:")
        print(f"Analyzing if these numbers were already statistically significant:")
        
        frequencies = []
        for num in june_3_numbers:
            count = number_freq[num]
            percentage = (count / total_positions) * 100
            rank = sorted(number_freq.values(), reverse=True).index(count) + 1
            frequencies.append({
                'number': num,
                'count': count,
                'percentage': percentage,
                'rank': rank
            })
            print(f"   Number {num:2d}: {count:3d} times ({percentage:5.2f}%) - Rank {rank:2d}/50")
        
        # Calculate average rank of June 3 numbers
        avg_rank = sum(f['rank'] for f in frequencies) / len(frequencies)
        avg_percentage = sum(f['percentage'] for f in frequencies) / len(frequencies)
        expected_percentage = 100 / 50  # 2% if perfectly random
        
        print(f"\n📊 JUNE 3 NUMBERS STATISTICAL PROFILE:")
        print(f"   Average rank: {avg_rank:.1f}/50")
        print(f"   Average frequency: {avg_percentage:.2f}%")
        print(f"   Expected if random: {expected_percentage:.2f}%")
        print(f"   Deviation: {avg_percentage - expected_percentage:+.2f}%")
        
        if avg_rank <= 25:
            print(f"   Status: ABOVE AVERAGE frequency numbers")
            frequency_justification = "HIGH_FREQUENCY"
        else:
            print(f"   Status: BELOW AVERAGE frequency numbers")
            frequency_justification = "LOW_FREQUENCY"
        
        return frequency_justification, frequencies, avg_rank
        
    except Exception as e:
        print(f"Frequency analysis error: {e}")
        return None, None, None

def evaluate_integration_logic():
    """Evaluate the different reasons for integrating June 3 numbers"""
    
    print(f"\n🧠 INTEGRATION LOGIC EVALUATION:")
    print("=" * 35)
    
    print(f"POSSIBLE JUSTIFICATIONS FOR INTEGRATING JUNE 3 NUMBERS:")
    print(f"")
    print(f"1️⃣ MATHEMATICAL REAPPEARANCE:")
    print(f"   Theory: Winning numbers statistically reappear")
    print(f"   Basis: Historical overlap analysis")
    
    print(f"")
    print(f"2️⃣ HIGH HISTORICAL FREQUENCY:")
    print(f"   Theory: June 3 numbers were already frequent")
    print(f"   Basis: Historical frequency rankings")
    
    print(f"")
    print(f"3️⃣ STRATEGIC PATTERN LEARNING:")
    print(f"   Theory: Learn from successful combinations")
    print(f"   Basis: June 3 had optimal range distribution")
    
    print(f"")
    print(f"4️⃣ RECENCY BIAS (QUESTIONABLE):")
    print(f"   Theory: Recent results influence future draws")
    print(f"   Basis: Gambler's fallacy territory")
    
    print(f"")
    print(f"5️⃣ COVERAGE OPTIMIZATION:")
    print(f"   Theory: Maintain representation of proven winners")
    print(f"   Basis: Risk management approach")
    
    # Run the analyses
    reappearance_result, overlap_data, random_baseline = analyze_winning_number_patterns()
    frequency_result, freq_data, avg_rank = analyze_june_3_frequency_basis()
    
    print(f"\n📋 ANALYSIS RESULTS:")
    if reappearance_result == "MATHEMATICAL":
        print(f"   ✅ Mathematical reappearance: SUPPORTED")
    elif reappearance_result == "NOT_MATHEMATICAL":
        print(f"   ❌ Mathematical reappearance: NOT SUPPORTED")
    else:
        print(f"   ⚖️  Mathematical reappearance: NEUTRAL")
    
    if frequency_result == "HIGH_FREQUENCY":
        print(f"   ✅ High historical frequency: SUPPORTED")
        print(f"   📊 June 3 numbers rank {avg_rank:.1f}/50 on average")
    elif frequency_result == "LOW_FREQUENCY":
        print(f"   ❌ High historical frequency: NOT SUPPORTED")
        print(f"   📊 June 3 numbers rank {avg_rank:.1f}/50 on average")
    
    print(f"\n💡 RECOMMENDED INTEGRATION APPROACH:")
    
    if frequency_result == "HIGH_FREQUENCY":
        print(f"   ✅ JUSTIFIED: June 3 numbers are historically frequent")
        print(f"   📋 Primary reason: Historical frequency basis")
        print(f"   🎯 Integration level: Selective (high-frequency numbers)")
    elif reappearance_result == "MATHEMATICAL":
        print(f"   ✅ JUSTIFIED: Mathematical reappearance pattern exists")
        print(f"   📋 Primary reason: Statistical reappearance evidence")
        print(f"   🎯 Integration level: Moderate")
    else:
        print(f"   ⚠️  QUESTIONABLE: Limited mathematical justification")
        print(f"   📋 Primary reason: Coverage optimization only")
        print(f"   🎯 Integration level: Minimal (avoid recency bias)")

def main():
    """Main analysis"""
    evaluate_integration_logic()

if __name__ == "__main__":
    main()