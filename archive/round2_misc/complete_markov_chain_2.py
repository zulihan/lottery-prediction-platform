"""
Determine the optimal 5th number for Markov Chain 2: [14, 20, 44, 49] + Stars: [4, 8]
Using transition analysis from historical data
"""

import psycopg2
import os
from collections import defaultdict, Counter

def connect_to_database():
    """Connect to the PostgreSQL database"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    else:
        raise Exception("No database connection available")

def get_historical_data():
    """Get all historical Euromillions data for transition analysis"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = """
    SELECT date, n1, n2, n3, n4, n5, s1, s2 
    FROM euromillions_drawings 
    ORDER BY date DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.close()
    return results

def build_markov_transitions(historical_data):
    """Build comprehensive Markov transition matrices"""
    
    # Multiple transition types
    direct_transitions = defaultdict(Counter)  # number -> next number
    position_transitions = defaultdict(Counter)  # number -> number 2 positions later
    combination_transitions = defaultdict(Counter)  # (num1, num2) -> num3
    
    all_numbers = []
    
    for row in historical_data:
        date, n1, n2, n3, n4, n5, s1, s2 = row
        numbers = sorted([n1, n2, n3, n4, n5])
        all_numbers.extend(numbers)
        
        # Direct transitions (adjacent in sorted order)
        for i in range(len(numbers) - 1):
            current = numbers[i]
            next_num = numbers[i + 1]
            direct_transitions[current][next_num] += 1
        
        # Position-based transitions (every 2nd number)
        for i in range(len(numbers) - 2):
            current = numbers[i]
            next_num = numbers[i + 2]
            position_transitions[current][next_num] += 1
        
        # Combination transitions (pair -> next)
        for i in range(len(numbers) - 2):
            pair = (numbers[i], numbers[i + 1])
            next_num = numbers[i + 2]
            combination_transitions[pair][next_num] += 1
    
    return direct_transitions, position_transitions, combination_transitions, Counter(all_numbers)

def analyze_existing_numbers(existing_numbers, transitions, number_freq):
    """Analyze what 5th number would best complete the Markov chain"""
    
    direct_trans, position_trans, combo_trans, freq = transitions
    
    print(f"ANALYZING MARKOV CHAIN: {existing_numbers}")
    print("=" * 40)
    
    # Method 1: Direct transitions from last number
    last_num = existing_numbers[-1]  # 49
    print(f"1. DIRECT TRANSITIONS FROM {last_num}:")
    if last_num in direct_trans:
        candidates_direct = direct_trans[last_num]
        available_direct = {num: count for num, count in candidates_direct.items() 
                          if num not in existing_numbers}
        sorted_direct = sorted(available_direct.items(), key=lambda x: x[1], reverse=True)
        print(f"   Available candidates: {dict(sorted_direct[:5])}")
    else:
        available_direct = {}
        print(f"   No direct transitions found from {last_num}")
    
    # Method 2: Position transitions from numbers 2 positions back
    print(f"\n2. POSITION TRANSITIONS:")
    available_position = {}
    for i, num in enumerate(existing_numbers[:-2]):  # 14, 20
        if num in position_trans:
            candidates = position_trans[num]
            for candidate, count in candidates.items():
                if candidate not in existing_numbers:
                    if candidate not in available_position:
                        available_position[candidate] = 0
                    available_position[candidate] += count
    
    if available_position:
        sorted_position = sorted(available_position.items(), key=lambda x: x[1], reverse=True)
        print(f"   Available candidates: {dict(sorted_position[:5])}")
    else:
        print(f"   No position transitions found")
    
    # Method 3: Combination transitions from pairs
    print(f"\n3. COMBINATION TRANSITIONS FROM PAIRS:")
    available_combo = {}
    
    # Check all possible pairs in existing numbers
    for i in range(len(existing_numbers) - 1):
        for j in range(i + 1, len(existing_numbers)):
            pair = (existing_numbers[i], existing_numbers[j])
            reverse_pair = (existing_numbers[j], existing_numbers[i])
            
            for test_pair in [pair, reverse_pair]:
                if test_pair in combo_trans:
                    candidates = combo_trans[test_pair]
                    for candidate, count in candidates.items():
                        if candidate not in existing_numbers:
                            if candidate not in available_combo:
                                available_combo[candidate] = 0
                            available_combo[candidate] += count
    
    if available_combo:
        sorted_combo = sorted(available_combo.items(), key=lambda x: x[1], reverse=True)
        print(f"   Available candidates: {dict(sorted_combo[:5])}")
    else:
        print(f"   No combination transitions found")
    
    # Method 4: Frequency-based completion
    print(f"\n4. FREQUENCY-BASED COMPLETION:")
    remaining_numbers = [n for n in range(1, 50) if n not in existing_numbers]
    freq_candidates = {num: freq[num] for num in remaining_numbers}
    sorted_freq = sorted(freq_candidates.items(), key=lambda x: x[1], reverse=True)
    print(f"   Top frequent remaining: {dict(sorted_freq[:10])}")
    
    # Combine all methods for final recommendation
    print(f"\n5. COMBINED SCORING:")
    combined_scores = {}
    
    # Weight the different methods
    for num, score in available_direct.items():
        combined_scores[num] = combined_scores.get(num, 0) + score * 3  # Direct transitions weighted 3x
    
    for num, score in available_position.items():
        combined_scores[num] = combined_scores.get(num, 0) + score * 2  # Position transitions weighted 2x
    
    for num, score in available_combo.items():
        combined_scores[num] = combined_scores.get(num, 0) + score * 2  # Combo transitions weighted 2x
    
    # Add frequency bonus for top numbers
    top_freq_nums = [num for num, count in sorted_freq[:15]]
    for num in top_freq_nums:
        if num in combined_scores:
            combined_scores[num] += freq[num] * 0.1  # Small frequency bonus
        else:
            combined_scores[num] = freq[num] * 0.1
    
    if combined_scores:
        final_ranking = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        print(f"   Final ranking (top 10): {dict(final_ranking[:10])}")
        return final_ranking[0][0]  # Return top candidate
    else:
        # Fallback to most frequent remaining number
        return sorted_freq[0][0]

def validate_completion(existing_numbers, fifth_number):
    """Validate the completed combination"""
    
    complete_combo = existing_numbers + [fifth_number]
    complete_combo.sort()
    
    print(f"\nCOMPLETED COMBINATION VALIDATION:")
    print(f"Original: {existing_numbers} + [?]")
    print(f"Completed: {complete_combo}")
    
    # Check for issues
    issues = []
    if len(complete_combo) != 5:
        issues.append(f"Wrong length: {len(complete_combo)}")
    if not all(1 <= n <= 49 for n in complete_combo):
        issues.append("Numbers out of range")
    if len(set(complete_combo)) != 5:
        issues.append("Duplicate numbers")
    
    if issues:
        print(f"❌ Issues found: {', '.join(issues)}")
        return False
    else:
        print(f"✅ Valid combination")
        return True

def main():
    """Determine the optimal 5th number for Markov Chain 2"""
    
    print("COMPLETING MARKOV CHAIN 2 COMBINATION")
    print("=" * 37)
    
    # Get data and build transitions
    historical_data = get_historical_data()
    print(f"Analyzing {len(historical_data)} historical draws")
    
    transitions = build_markov_transitions(historical_data)
    
    # Existing combination
    existing_numbers = [14, 20, 44, 49]
    
    # Find optimal 5th number
    optimal_fifth = analyze_existing_numbers(existing_numbers, transitions, transitions[3])
    
    # Validate
    is_valid = validate_completion(existing_numbers, optimal_fifth)
    
    print(f"\n" + "="*50)
    print(f"RECOMMENDATION:")
    print(f"Markov Chain 2: {sorted(existing_numbers + [optimal_fifth])} + Stars: [4, 8]")
    print(f"5th number: {optimal_fifth}")
    print(f"Confidence: {'High' if is_valid else 'Low'} (based on historical Markov transitions)")
    print(f"="*50)

if __name__ == "__main__":
    main()