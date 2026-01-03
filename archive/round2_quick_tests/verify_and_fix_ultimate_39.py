"""
Verify and fix the 39 ultimate strategy combinations to ensure all have exactly 5 numbers
"""

def get_ultimate_39_corrected():
    """Get the corrected 39 ultimate combinations with exactly 5 numbers each"""
    
    combinations = [
        # SET 1: Coverage Optimization Supreme (8 combinations)
        {'id': 'ULT-1', 'numbers': [12, 15, 38, 47, 48], 'stars': [5, 7], 'strategy': 'Coverage Optimization Supreme'},
        {'id': 'ULT-2', 'numbers': [10, 23, 19, 44, 50], 'stars': [7, 3], 'strategy': 'Coverage Optimization Variant 1'},
        {'id': 'ULT-3', 'numbers': [23, 44, 19, 50, 42], 'stars': [7, 2], 'strategy': 'Coverage Optimization Variant 2'},  # FIXED: Added 42
        {'id': 'ULT-4', 'numbers': [15, 23, 38, 44, 47], 'stars': [7, 8], 'strategy': 'Coverage Optimization Variant 3'},
        {'id': 'ULT-5', 'numbers': [12, 19, 23, 44, 49], 'stars': [7, 9], 'strategy': 'Coverage Optimization Variant 4'},
        {'id': 'ULT-6', 'numbers': [10, 15, 38, 44, 50], 'stars': [5, 3], 'strategy': 'Coverage Optimization Variant 5'},
        {'id': 'ULT-7', 'numbers': [19, 23, 47, 48, 50], 'stars': [7, 1], 'strategy': 'Coverage Optimization Variant 6'},
        {'id': 'ULT-8', 'numbers': [12, 23, 38, 44, 47], 'stars': [5, 8], 'strategy': 'Coverage Optimization Variant 7'},
        
        # SET 2: Fusion Mastery (10 combinations)
        {'id': 'ULT-9', 'numbers': [38, 40, 41, 23, 44], 'stars': [7, 3], 'strategy': 'Fusion Mastery 1'},
        {'id': 'ULT-10', 'numbers': [41, 10, 43, 23, 44], 'stars': [7, 2], 'strategy': 'Fusion Mastery 2'},
        {'id': 'ULT-11', 'numbers': [43, 12, 46, 23, 44], 'stars': [7, 8], 'strategy': 'Fusion Mastery 3'},
        {'id': 'ULT-12', 'numbers': [46, 47, 48, 23, 44], 'stars': [7, 9], 'strategy': 'Fusion Mastery 4'},
        {'id': 'ULT-13', 'numbers': [48, 15, 49, 23, 44], 'stars': [7, 3], 'strategy': 'Fusion Mastery 5'},
        {'id': 'ULT-14', 'numbers': [49, 29, 30, 23, 44], 'stars': [7, 2], 'strategy': 'Fusion Mastery 6'},
        {'id': 'ULT-15', 'numbers': [30, 23, 44, 19, 50], 'stars': [7, 8], 'strategy': 'Fusion Mastery 7'},
        {'id': 'ULT-16', 'numbers': [23, 44, 19, 50, 21], 'stars': [7, 9], 'strategy': 'Fusion Mastery 8'},
        {'id': 'ULT-17', 'numbers': [23, 44, 19, 50, 21], 'stars': [5, 3], 'strategy': 'Fusion Mastery 9'},
        {'id': 'ULT-18', 'numbers': [23, 44, 19, 50, 21], 'stars': [5, 2], 'strategy': 'Fusion Mastery 10'},
        
        # SET 3: Frequency Dominance (10 combinations)
        {'id': 'ULT-19', 'numbers': [23, 50, 29, 37, 25], 'stars': [3, 2], 'strategy': 'Frequency Dominance 1'},
        {'id': 'ULT-20', 'numbers': [44, 21, 10, 20, 27], 'stars': [3, 8], 'strategy': 'Frequency Dominance 2'},
        {'id': 'ULT-21', 'numbers': [19, 42, 17, 15, 38], 'stars': [3, 9], 'strategy': 'Frequency Dominance 3'},
        {'id': 'ULT-22', 'numbers': [50, 29, 37, 25, 23], 'stars': [3, 3], 'strategy': 'Frequency Dominance 4'},
        {'id': 'ULT-23', 'numbers': [21, 10, 20, 27, 44], 'stars': [3, 2], 'strategy': 'Frequency Dominance 5'},
        {'id': 'ULT-24', 'numbers': [42, 17, 15, 38, 19], 'stars': [3, 8], 'strategy': 'Frequency Dominance 6'},
        {'id': 'ULT-25', 'numbers': [29, 37, 25, 23, 50], 'stars': [3, 9], 'strategy': 'Frequency Dominance 7'},
        {'id': 'ULT-26', 'numbers': [10, 20, 27, 44, 21], 'stars': [3, 3], 'strategy': 'Frequency Dominance 8'},
        {'id': 'ULT-27', 'numbers': [17, 15, 38, 19, 42], 'stars': [3, 2], 'strategy': 'Frequency Dominance 9'},
        {'id': 'ULT-28', 'numbers': [37, 25, 23, 50, 29], 'stars': [3, 8], 'strategy': 'Frequency Dominance 10'},
        
        # SET 4: Extreme Range Focus (11 combinations)
        {'id': 'ULT-29', 'numbers': [10, 20, 42, 44, 50], 'stars': [7, 5], 'strategy': 'Extreme Range Focus 1'},
        {'id': 'ULT-30', 'numbers': [15, 25, 40, 45, 49], 'stars': [7, 2], 'strategy': 'Extreme Range Focus 2'},
        {'id': 'ULT-31', 'numbers': [12, 22, 41, 46, 48], 'stars': [5, 8], 'strategy': 'Extreme Range Focus 3'},
        {'id': 'ULT-32', 'numbers': [8, 18, 43, 47, 50], 'stars': [7, 9], 'strategy': 'Extreme Range Focus 4'},
        {'id': 'ULT-33', 'numbers': [14, 24, 39, 44, 49], 'stars': [5, 3], 'strategy': 'Extreme Range Focus 5'},
        {'id': 'ULT-34', 'numbers': [11, 21, 40, 45, 48], 'stars': [7, 1], 'strategy': 'Extreme Range Focus 6'},
        {'id': 'ULT-35', 'numbers': [16, 26, 42, 46, 50], 'stars': [5, 6], 'strategy': 'Extreme Range Focus 7'},
        {'id': 'ULT-36', 'numbers': [9, 19, 41, 47, 49], 'stars': [7, 4], 'strategy': 'Extreme Range Focus 8'},
        {'id': 'ULT-37', 'numbers': [13, 23, 43, 45, 48], 'stars': [5, 11], 'strategy': 'Extreme Range Focus 9'},
        {'id': 'ULT-38', 'numbers': [17, 27, 39, 44, 50], 'stars': [7, 12], 'strategy': 'Extreme Range Focus 10'},
        {'id': 'ULT-39', 'numbers': [6, 28, 38, 46, 49], 'stars': [5, 10], 'strategy': 'Extreme Range Focus 11'}
    ]
    
    return combinations

def verify_all_combinations(combinations):
    """Verify all combinations have exactly 5 numbers and 2 stars"""
    
    errors = []
    
    for combo in combinations:
        if len(combo['numbers']) != 5:
            errors.append(f"{combo['id']}: {len(combo['numbers'])} numbers instead of 5: {combo['numbers']}")
        
        if len(combo['stars']) != 2:
            errors.append(f"{combo['id']}: {len(combo['stars'])} stars instead of 2")
        
        # Check for valid ranges
        for num in combo['numbers']:
            if not (1 <= num <= 50):
                errors.append(f"{combo['id']}: Number {num} out of range (1-50)")
        
        for star in combo['stars']:
            if not (1 <= star <= 12):
                errors.append(f"{combo['id']}: Star {star} out of range (1-12)")
    
    return errors

def check_uniqueness(combinations):
    """Check for duplicate combinations"""
    signatures = set()
    duplicates = []
    
    for combo in combinations:
        signature = (tuple(sorted(combo['numbers'])), tuple(sorted(combo['stars'])))
        if signature in signatures:
            duplicates.append(combo['id'])
        else:
            signatures.add(signature)
    
    return duplicates

def display_verification_results():
    """Display verification results for the ultimate 39"""
    
    combinations = get_ultimate_39_corrected()
    errors = verify_all_combinations(combinations)
    duplicates = check_uniqueness(combinations)
    
    print("🔧 VERIFICATION: ULTIMATE 39 COMBINATIONS")
    print("=" * 45)
    
    if errors:
        print("❌ ERRORS FOUND:")
        for error in errors:
            print(f"   {error}")
        print()
    else:
        print("✅ ALL COMBINATIONS VALID: 5 numbers + 2 stars each")
        print()
    
    if duplicates:
        print("❌ DUPLICATES FOUND:")
        for dup in duplicates:
            print(f"   {dup}")
        print()
    else:
        print("✅ ALL COMBINATIONS UNIQUE")
        print()
    
    # Display summary by sets
    sets = [
        ("SET 1: COVERAGE OPTIMIZATION SUPREME", combinations[0:8]),
        ("SET 2: FUSION MASTERY", combinations[8:18]),
        ("SET 3: FREQUENCY DOMINANCE", combinations[18:28]),
        ("SET 4: EXTREME RANGE FOCUS", combinations[28:39])
    ]
    
    print("SUMMARY BY SETS:")
    print("-" * 20)
    
    for set_name, set_combos in sets:
        print(f"{set_name}: {len(set_combos)} combinations")
        
        # Check if any in this set have issues
        set_errors = [e for e in errors if any(combo['id'] in e for combo in set_combos)]
        if set_errors:
            print(f"   ❌ Issues found in this set")
        else:
            print(f"   ✅ All valid")
    
    print(f"\n📊 FINAL STATUS:")
    print(f"    Total combinations: {len(combinations)}")
    print(f"    All valid: {'YES' if not errors else 'NO'}")
    print(f"    All unique: {'YES' if not duplicates else 'NO'}")
    print(f"    Ready for play: {'YES' if not errors and not duplicates else 'NO'}")
    
    if not errors and not duplicates:
        print(f"\n✅ ULTIMATE 39 COMBINATIONS ARE READY")
        print(f"Combined with corrected initial 20 = 59 total combinations")
    
    return combinations, not errors and not duplicates

def main():
    display_verification_results()

if __name__ == "__main__":
    main()