"""
Fix the initial 20 combinations - ensure all have exactly 5 numbers + 2 stars
"""

def get_corrected_initial_20():
    """Get the corrected initial 20 combinations with exactly 5 numbers each"""
    
    # FIRST 10 - OPTIMIZED (CORRECTED)
    optimized_10 = [
        {
            'id': 'OPT-1',
            'strategy': 'Coverage Optimization Enhanced',
            'numbers': [12, 15, 38, 47, 49],  # Already 5 numbers
            'stars': [5, 7],
            'method': 'June 3 winning pattern + extreme high coverage'
        },
        {
            'id': 'OPT-2',
            'strategy': 'Frequency Analysis Ultimate',
            'numbers': [23, 44, 19, 50, 21],  # FIXED: Added 21 (frequent)
            'stars': [3, 7],
            'method': 'Most frequent numbers from 1845 draws + star 7 gap'
        },
        {
            'id': 'OPT-3',
            'strategy': 'Recent Trends Analysis',
            'numbers': [47, 29, 15, 49, 23],  # FIXED: Added 23 (frequent)
            'stars': [5, 12],
            'method': 'Hot numbers from recent 100 draws'
        },
        {
            'id': 'OPT-4',
            'strategy': 'High-Range Pattern',
            'numbers': [10, 44, 50, 42, 37],  # Already 5 numbers
            'stars': [7, 2],
            'method': 'June 3 range distribution (1 low + 4 high)'
        },
        {
            'id': 'OPT-5',
            'strategy': 'Star 7 Priority',
            'numbers': [15, 38, 23, 44, 19],  # Already 5 numbers
            'stars': [7, 3],
            'method': 'Critical star 7 focus + June 3 winners'
        },
        {
            'id': 'OPT-6',
            'strategy': 'Extreme High Focus',
            'numbers': [23, 44, 50, 45, 47],  # FIXED: Added 47 (extreme high)
            'stars': [5, 7],
            'method': 'Address 45-50 range under-representation'
        },
        {
            'id': 'OPT-7',
            'strategy': 'Hot-Cold Balance',
            'numbers': [23, 44, 19, 16, 48],  # Already 5 numbers
            'stars': [7, 8],
            'method': 'Balanced approach with star 7 coverage'
        },
        {
            'id': 'OPT-8',
            'strategy': 'Time Series Pattern',
            'numbers': [23, 32, 39, 42, 46],  # Already 5 numbers
            'stars': [5, 7],
            'method': 'Mathematical progression with winning stars'
        },
        {
            'id': 'OPT-9',
            'strategy': 'Coverage Maximizer',
            'numbers': [23, 44, 19, 10, 37],  # FIXED: Added 37 (frequent)
            'stars': [7, 3],
            'method': 'Maximum range coverage + priority star 7'
        },
        {
            'id': 'OPT-10',
            'strategy': 'Ultimate Synthesis',
            'numbers': [12, 38, 23, 44, 19],  # Already 5 numbers
            'stars': [5, 7],
            'method': 'Best strategies + complete June 3 insights'
        }
    ]
    
    # SECOND 10 - FUSION (CORRECTED)
    fusion_10 = [
        {
            'id': 'FUS-1',
            'strategy': 'Frequency-Coverage Fusion',
            'numbers': [23, 44, 19, 12, 38],  # Already 5 numbers
            'stars': [7, 3],
            'method': 'Top frequent + June 3 optimal'
        },
        {
            'id': 'FUS-2',
            'strategy': 'Extreme-Balance Fusion',
            'numbers': [50, 49, 48, 16, 29],  # Already 5 numbers
            'stars': [5, 8],
            'method': 'Extreme high + cold number balance'
        },
        {
            'id': 'FUS-3',
            'strategy': 'Pattern-Range Fusion',
            'numbers': [32, 39, 42, 10, 37],  # Already 5 numbers
            'stars': [7, 2],
            'method': 'Mathematical progression + range distribution'
        },
        {
            'id': 'FUS-4',
            'strategy': 'Recent-Synthesis Fusion',
            'numbers': [47, 15, 12, 23, 44],  # Already 5 numbers
            'stars': [5, 12],
            'method': 'Recent trends + multi-strategy synthesis'
        },
        {
            'id': 'FUS-5',
            'strategy': 'Triple Strategy Fusion',
            'numbers': [12, 23, 50, 38, 44],  # Already 5 numbers
            'stars': [7, 5],
            'method': 'Coverage + Frequency + Extreme unified'
        },
        {
            'id': 'FUS-6',
            'strategy': 'Gap Coverage Fusion',
            'numbers': [23, 44, 1, 2, 3],  # Already 5 numbers
            'stars': [7, 1],
            'method': 'Frequent numbers + gap coverage'
        },
        {
            'id': 'FUS-7',
            'strategy': 'Star Optimization Fusion',
            'numbers': [10, 12, 44, 15, 23],  # Already 5 numbers
            'stars': [7, 5],
            'method': 'Numbers from best star 7 combinations'
        },
        {
            'id': 'FUS-8',
            'strategy': 'Mathematical Progression Enhanced',
            'numbers': [2, 23, 30, 37, 44],  # Already 5 numbers
            'stars': [3, 7],
            'method': 'Progression by 7 from most frequent number'
        },
        {
            'id': 'FUS-9',
            'strategy': 'High Performance Mix',
            'numbers': [12, 15, 38, 23, 44],  # Already 5 numbers
            'stars': [7, 3],
            'method': 'Numbers from top-performing June 3 strategies'
        },
        {
            'id': 'FUS-10',
            'strategy': 'Ultimate Diversity Fusion',
            'numbers': [15, 23, 19, 44, 38],  # Already 5 numbers
            'stars': [5, 7],
            'method': 'Maximum range diversity with frequent numbers'
        }
    ]
    
    return optimized_10 + fusion_10

def verify_combinations(combinations):
    """Verify all combinations have exactly 5 numbers and 2 stars"""
    
    errors = []
    
    for combo in combinations:
        if len(combo['numbers']) != 5:
            errors.append(f"{combo['id']}: {len(combo['numbers'])} numbers instead of 5")
        
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

def display_corrected_initial_20():
    """Display the corrected initial 20 combinations"""
    
    combinations = get_corrected_initial_20()
    errors = verify_combinations(combinations)
    
    print("🔧 CORRECTED INITIAL 20 COMBINATIONS")
    print("All combinations now have exactly 5 numbers + 2 stars")
    print("=" * 55)
    
    if errors:
        print("❌ ERRORS FOUND:")
        for error in errors:
            print(f"   {error}")
        print()
    else:
        print("✅ VERIFICATION PASSED: All combinations valid")
        print()
    
    print("FIRST 10 - OPTIMIZED COMBINATIONS:")
    print("-" * 35)
    
    for i, combo in enumerate(combinations[:10], 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print(f"    Method: {combo['method']}")
        print()
    
    print("SECOND 10 - FUSION COMBINATIONS:")
    print("-" * 32)
    
    for i, combo in enumerate(combinations[10:], 11):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print(f"    Method: {combo['method']}")
        print()
    
    print("📊 SUMMARY:")
    print(f"    Total combinations: {len(combinations)}")
    print(f"    All have 5 numbers: {'YES' if not errors else 'NO'}")
    print(f"    All have 2 stars: {'YES' if not errors else 'NO'}")
    print(f"    Ready for play: {'YES' if not errors else 'NO'}")
    
    return combinations

def main():
    display_corrected_initial_20()

if __name__ == "__main__":
    main()