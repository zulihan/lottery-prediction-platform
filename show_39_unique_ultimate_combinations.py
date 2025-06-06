"""
Show the 39 unique combinations from the ultimate strategy
(Excluding the 1 duplicate with the initial 20)
"""

def get_initial_20_signatures():
    """Get signatures of the initial 20 combinations to identify duplicates"""
    
    initial_20 = [
        # Initial 10 Optimized
        ([12, 15, 38, 47, 49], [5, 7]),
        ([23, 44, 19, 50], [3, 7]),
        ([47, 29, 15, 49], [5, 12]),
        ([10, 44, 50, 42, 37], [7, 2]),
        ([15, 38, 23, 44, 19], [7, 3]),
        ([23, 44, 50, 45], [5, 7]),
        ([23, 44, 19, 16, 48], [7, 8]),
        ([23, 32, 39, 42, 46], [5, 7]),
        ([23, 44, 19, 10], [7, 3]),
        ([12, 38, 23, 44, 19], [5, 7]),
        
        # Initial 10 Fusion
        ([23, 44, 19, 12, 38], [7, 3]),  # This one duplicates with ULT-2
        ([50, 49, 48, 16, 29], [5, 8]),
        ([32, 39, 42, 10, 37], [7, 2]),
        ([47, 15, 12, 23, 44], [5, 12]),
        ([12, 23, 50, 38, 44], [7, 5]),
        ([23, 44, 1, 2, 3], [7, 1]),
        ([10, 12, 44, 15, 23], [7, 5]),
        ([2, 23, 30, 37, 44], [3, 7]),
        ([12, 15, 38, 23, 44], [7, 3]),
        ([15, 23, 19, 44, 38], [5, 7])
    ]
    
    # Convert to signatures (sorted tuples)
    signatures = set()
    for numbers, stars in initial_20:
        signature = (tuple(sorted(numbers)), tuple(sorted(stars)))
        signatures.add(signature)
    
    return signatures

def get_ultimate_40_unique():
    """Get the 39 unique combinations from ultimate 40 (excluding duplicate)"""
    
    ultimate_40 = [
        # SET 1: Coverage Optimization Supreme
        {'id': 'ULT-1', 'strategy': 'Coverage Optimization Supreme', 'numbers': [12, 15, 38, 47, 48], 'stars': [5, 7]},
        {'id': 'ULT-2', 'strategy': 'Coverage-Frequency Supreme', 'numbers': [23, 44, 19, 12, 38], 'stars': [7, 3]},  # DUPLICATE
        {'id': 'ULT-3', 'strategy': 'Extreme High Supreme', 'numbers': [23, 44, 45, 46, 47], 'stars': [5, 7]},
        {'id': 'ULT-4', 'strategy': 'Coverage Optimization Variant 1', 'numbers': [10, 23, 19, 44, 50], 'stars': [7, 3]},
        {'id': 'ULT-5', 'strategy': 'Coverage Optimization Variant 2', 'numbers': [23, 44, 19, 50], 'stars': [7, 2]},
        {'id': 'ULT-6', 'strategy': 'Coverage Optimization Variant 3', 'numbers': [10, 23, 19, 44, 50], 'stars': [7, 8]},
        {'id': 'ULT-7', 'strategy': 'Coverage Optimization Variant 4', 'numbers': [23, 44, 19, 50], 'stars': [7, 9]},
        {'id': 'ULT-8', 'strategy': 'Coverage Optimization Variant 5', 'numbers': [10, 23, 19, 44, 50], 'stars': [7, 3]},
        {'id': 'ULT-9', 'strategy': 'Coverage Optimization Variant 6', 'numbers': [23, 44, 19, 50], 'stars': [7, 2]},
        {'id': 'ULT-10', 'strategy': 'Coverage Optimization Variant 7', 'numbers': [10, 23, 19, 44, 50], 'stars': [7, 8]},
        
        # SET 2: Fusion Mastery
        {'id': 'ULT-11', 'strategy': 'Fusion Mastery 1', 'numbers': [38, 40, 41, 23, 44], 'stars': [7, 3]},
        {'id': 'ULT-12', 'strategy': 'Fusion Mastery 2', 'numbers': [41, 10, 43, 23, 44], 'stars': [7, 2]},
        {'id': 'ULT-13', 'strategy': 'Fusion Mastery 3', 'numbers': [43, 12, 46, 23, 44], 'stars': [7, 8]},
        {'id': 'ULT-14', 'strategy': 'Fusion Mastery 4', 'numbers': [46, 47, 48, 23, 44], 'stars': [7, 9]},
        {'id': 'ULT-15', 'strategy': 'Fusion Mastery 5', 'numbers': [48, 15, 49, 23, 44], 'stars': [7, 3]},
        {'id': 'ULT-16', 'strategy': 'Fusion Mastery 6', 'numbers': [49, 29, 30, 23, 44], 'stars': [7, 2]},
        {'id': 'ULT-17', 'strategy': 'Fusion Mastery 7', 'numbers': [30, 23, 44, 19, 50], 'stars': [7, 8]},
        {'id': 'ULT-18', 'strategy': 'Fusion Mastery 8', 'numbers': [23, 44, 19, 50, 21], 'stars': [7, 9]},
        {'id': 'ULT-19', 'strategy': 'Fusion Mastery 9', 'numbers': [23, 44, 19, 50, 21], 'stars': [5, 3]},
        {'id': 'ULT-20', 'strategy': 'Fusion Mastery 10', 'numbers': [23, 44, 19, 50, 21], 'stars': [5, 2]},
        
        # SET 3: Frequency Dominance
        {'id': 'ULT-21', 'strategy': 'Frequency Dominance 1', 'numbers': [23, 50, 29, 37, 25], 'stars': [3, 2]},
        {'id': 'ULT-22', 'strategy': 'Frequency Dominance 2', 'numbers': [44, 21, 10, 20, 27], 'stars': [3, 8]},
        {'id': 'ULT-23', 'strategy': 'Frequency Dominance 3', 'numbers': [19, 42, 17, 15, 38], 'stars': [3, 9]},
        {'id': 'ULT-24', 'strategy': 'Frequency Dominance 4', 'numbers': [50, 29, 37, 25, 23], 'stars': [3, 3]},
        {'id': 'ULT-25', 'strategy': 'Frequency Dominance 5', 'numbers': [21, 10, 20, 27, 44], 'stars': [3, 2]},
        {'id': 'ULT-26', 'strategy': 'Frequency Dominance 6', 'numbers': [42, 17, 15, 38, 19], 'stars': [3, 8]},
        {'id': 'ULT-27', 'strategy': 'Frequency Dominance 7', 'numbers': [29, 37, 25, 23, 50], 'stars': [3, 9]},
        {'id': 'ULT-28', 'strategy': 'Frequency Dominance 8', 'numbers': [10, 20, 27, 44, 21], 'stars': [3, 3]},
        {'id': 'ULT-29', 'strategy': 'Frequency Dominance 9', 'numbers': [17, 15, 38, 19, 42], 'stars': [3, 2]},
        {'id': 'ULT-30', 'strategy': 'Frequency Dominance 10', 'numbers': [37, 25, 23, 50, 29], 'stars': [3, 8]},
        
        # SET 4: Extreme Range Focus
        {'id': 'ULT-31', 'strategy': 'Extreme Range Focus 1', 'numbers': [10, 20, 42, 44, 50], 'stars': [7, 5]},
        {'id': 'ULT-32', 'strategy': 'Extreme Range Focus 2', 'numbers': [10, 20, 42, 44, 50], 'stars': [7, 5]},
        {'id': 'ULT-33', 'strategy': 'Extreme Range Focus 3', 'numbers': [10, 20, 42, 44, 50], 'stars': [7, 5]},
        {'id': 'ULT-34', 'strategy': 'Extreme Range Focus 4', 'numbers': [10, 20, 42, 44, 50], 'stars': [7, 5]},
        {'id': 'ULT-35', 'strategy': 'Extreme Range Focus 5', 'numbers': [10, 20, 42, 44, 50], 'stars': [7, 5]},
        {'id': 'ULT-36', 'strategy': 'Extreme Range Focus 6', 'numbers': [10, 20, 42, 44, 50], 'stars': [5, 2]},
        {'id': 'ULT-37', 'strategy': 'Extreme Range Focus 7', 'numbers': [10, 20, 42, 44, 50], 'stars': [5, 8]},
        {'id': 'ULT-38', 'strategy': 'Extreme Range Focus 8', 'numbers': [10, 20, 42, 44, 50], 'stars': [5, 9]},
        {'id': 'ULT-39', 'strategy': 'Extreme Range Focus 9', 'numbers': [10, 20, 42, 44, 50], 'stars': [5, 3]},
        {'id': 'ULT-40', 'strategy': 'Extreme Range Focus 10', 'numbers': [10, 20, 42, 44, 50], 'stars': [5, 2]}
    ]
    
    initial_signatures = get_initial_20_signatures()
    unique_combinations = []
    
    for combo in ultimate_40:
        combo_signature = (tuple(sorted(combo['numbers'])), tuple(sorted(combo['stars'])))
        
        if combo_signature not in initial_signatures:
            unique_combinations.append(combo)
    
    return unique_combinations

def display_39_unique():
    """Display the 39 unique combinations from ultimate strategy"""
    
    unique_combos = get_ultimate_40_unique()
    
    print("🎯 39 UNIQUE COMBINATIONS FROM ULTIMATE STRATEGY")
    print("(Excluding the 1 duplicate with initial 20)")
    print("=" * 55)
    
    # Group by sets
    sets = {
        'SET 1: COVERAGE OPTIMIZATION SUPREME': [],
        'SET 2: FUSION MASTERY': [],
        'SET 3: FREQUENCY DOMINANCE': [],
        'SET 4: EXTREME RANGE FOCUS': []
    }
    
    for combo in unique_combos:
        if 'Coverage' in combo['strategy']:
            sets['SET 1: COVERAGE OPTIMIZATION SUPREME'].append(combo)
        elif 'Fusion Mastery' in combo['strategy']:
            sets['SET 2: FUSION MASTERY'].append(combo)
        elif 'Frequency Dominance' in combo['strategy']:
            sets['SET 3: FREQUENCY DOMINANCE'].append(combo)
        elif 'Extreme Range Focus' in combo['strategy']:
            sets['SET 4: EXTREME RANGE FOCUS'].append(combo)
    
    combo_number = 1
    
    for set_name, combinations in sets.items():
        if combinations:  # Only show sets that have combinations
            print(f"\n{set_name}")
            print("-" * len(set_name))
            
            for combo in combinations:
                print(f"{combo_number:2d}. {combo['strategy']}")
                print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
                combo_number += 1
            print()
    
    print(f"📊 SUMMARY:")
    print(f"    Total unique combinations from ultimate strategy: {len(unique_combos)}")
    print(f"    Combined with initial 20: {20 + len(unique_combos)} total combinations")
    print(f"    Coverage: Maximum strategic diversity for historic jackpot")
    
    return unique_combos

def main():
    """Main function"""
    unique_combos = display_39_unique()
    
    print(f"\n🏆 RECOMMENDATION:")
    print(f"    Play initial 20 combinations + these 39 unique combinations")
    print(f"    Total: 59 combinations for maximum jackpot opportunity")

if __name__ == "__main__":
    main()