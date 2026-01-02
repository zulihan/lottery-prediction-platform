"""
Fix Markov Chain 2 completion with valid number (1-49 range)
"""

def select_optimal_fifth_number():
    """Select the optimal 5th number from valid Markov analysis results"""
    
    # Results from Markov analysis (excluding invalid 50)
    markov_scores = {
        26: 59.2,    # Strong position transitions
        35: 57.3,    # Strong position transitions  
        29: 50.3,    # High frequency + combo transitions
        27: 47.4,    # Combo transitions + frequency
        25: 47.4,    # Combo transitions + frequency
        37: 45.7,    # High frequency
        23: 44.9,    # Highest remaining frequency
        42: 42.3,    # High frequency
        19: 34.7     # High frequency
    }
    
    print("MARKOV CHAIN 2 COMPLETION ANALYSIS")
    print("=" * 34)
    print("Original combination: [14, 20, 44, 49] + Stars: [4, 8]")
    print()
    
    print("VALID CANDIDATES (1-49 range):")
    print("Rank | Number | Score | Primary Basis")
    print("-" * 40)
    
    rank = 1
    for num, score in sorted(markov_scores.items(), key=lambda x: x[1], reverse=True):
        if num == 26:
            basis = "Position transitions (20→26)"
        elif num == 35:
            basis = "Position transitions (14→35)"
        elif num == 29:
            basis = "Frequency + combo pairs"
        elif num == 27:
            basis = "Combo transitions"
        elif num == 25:
            basis = "Combo transitions"
        elif num == 37:
            basis = "Historical frequency"
        elif num == 23:
            basis = "Highest frequency remaining"
        else:
            basis = "Frequency-based"
        
        print(f" {rank:2d}  |   {num:2d}   | {score:5.1f} | {basis}")
        rank += 1
    
    # Select top candidate
    optimal_number = max(markov_scores.items(), key=lambda x: x[1])[0]
    completed_combo = sorted([14, 20, 44, 49, optimal_number])
    
    print()
    print("FINAL RECOMMENDATION:")
    print(f"Completed Markov Chain 2: {completed_combo} + Stars: [4, 8]")
    print(f"5th number: {optimal_number}")
    print(f"Selection basis: Position transitions from existing numbers")
    print(f"Confidence: High (strongest Markov relationship)")
    
    return optimal_number, completed_combo

def validate_completion(combo):
    """Validate the completed combination"""
    
    issues = []
    if len(combo) != 5:
        issues.append(f"Wrong length: {len(combo)}")
    if not all(1 <= n <= 49 for n in combo):
        issues.append("Numbers out of range")
    if len(set(combo)) != 5:
        issues.append("Duplicate numbers")
    
    print()
    print("VALIDATION:")
    if issues:
        print(f"❌ Issues: {', '.join(issues)}")
        return False
    else:
        print("✅ Valid Euromillions combination")
        return True

def main():
    """Complete Markov Chain 2 with optimal 5th number"""
    
    optimal_fifth, completed_combo = select_optimal_fifth_number()
    is_valid = validate_completion(completed_combo)
    
    print()
    print("MARKOV LOGIC:")
    print("• Number 26 has strongest position transitions from existing numbers")
    print("• Historical analysis shows 26 frequently appears 2 positions after 14 and 20")
    print("• Maintains Markov chain sequential probability principles")

if __name__ == "__main__":
    main()