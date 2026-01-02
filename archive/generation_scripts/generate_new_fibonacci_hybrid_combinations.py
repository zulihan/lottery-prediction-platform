"""
Generate 5 new combinations using the proven Fibonacci-Filtered Hybrid strategy
with different parameters and approaches for fresh winning possibilities
"""

import random
from collections import Counter
from database import get_db_connection

def generate_fresh_fibonacci_hybrid_combinations():
    """Generate 5 new combinations using validated methodology with fresh parameters"""
    
    print("🚀 GENERATING FRESH FIBONACCI-FILTERED HYBRID COMBINATIONS 🚀")
    print("Using your proven methodology with new parameters for fresh results!")
    print("=" * 75)
    
    # Validated elements from your research
    fibonacci_numbers = [1, 2, 3, 5, 8, 13, 21, 34]
    hot_numbers = [1, 8, 13, 29, 47]  # Proven from May 20
    frequent_from_analysis = [1, 2, 8, 13, 15, 29, 47]  # From your ultimate analysis
    
    # Extended number pools for fresh combinations
    mid_range_numbers = list(range(15, 35))
    high_range_numbers = list(range(35, 51))
    low_range_numbers = list(range(1, 15))
    
    # Proven star patterns
    winning_stars = [5, 6]  # May 20 winners
    frequent_stars = [3, 5, 8, 11]  # From your analysis
    
    fresh_combinations = []
    
    # Combination 1: Enhanced Fibonacci Focus
    print("\n1️⃣ ENHANCED FIBONACCI FOCUS")
    print("   Strategy: Maximum Fibonacci with fresh non-Fibonacci additions")
    
    # Take 3 different Fibonacci numbers (not the May 20 ones)
    fresh_fibonacci = [fib for fib in fibonacci_numbers if fib not in [1, 8, 13]]
    selected_fib = random.sample(fresh_fibonacci, 3)
    
    # Add 2 fresh numbers from different ranges
    fresh_numbers = random.sample(mid_range_numbers, 1) + random.sample(high_range_numbers, 1)
    combo1_numbers = sorted(selected_fib + fresh_numbers)
    combo1_stars = sorted(random.sample([2, 4, 7, 9, 12], 2))
    
    fib_count1 = len([n for n in combo1_numbers if n in fibonacci_numbers])
    combo1 = {
        'numbers': combo1_numbers,
        'stars': combo1_stars,
        'strategy': 'Enhanced Fibonacci Focus',
        'fibonacci_percentage': (fib_count1/5) * 100,
        'description': 'Fresh Fibonacci numbers with strategic range distribution'
    }
    fresh_combinations.append(combo1)
    
    print(f"   Numbers: {combo1_numbers} (Fibonacci: {fib_count1}/5 = {combo1['fibonacci_percentage']:.0f}%)")
    print(f"   Stars: {combo1_stars}")
    
    # Combination 2: Frequency Shift Strategy
    print("\n2️⃣ FREQUENCY SHIFT STRATEGY")
    print("   Strategy: Use proven frequency logic but shift to unexplored numbers")
    
    # Take 1-2 from proven frequent, rest from unexplored but mathematically sound
    proven_sample = random.sample(frequent_from_analysis[:4], 2)
    
    # Fibonacci that haven't been overused
    unexplored_fib = [21, 34]  # Less used Fibonacci
    other_unexplored = [4, 6, 7, 9, 14, 16, 22, 23, 31, 32, 38, 39, 41, 43]
    
    remaining_numbers = random.sample(unexplored_fib, 1) + random.sample(other_unexplored, 2)
    combo2_numbers = sorted(proven_sample + remaining_numbers)
    combo2_stars = [5, 9]  # Mix proven (5) with fresh (9)
    
    fib_count2 = len([n for n in combo2_numbers if n in fibonacci_numbers])
    combo2 = {
        'numbers': combo2_numbers,
        'stars': combo2_stars,
        'strategy': 'Frequency Shift Strategy',
        'fibonacci_percentage': (fib_count2/5) * 100,
        'description': 'Proven frequency logic applied to fresh number territory'
    }
    fresh_combinations.append(combo2)
    
    print(f"   Numbers: {combo2_numbers} (Fibonacci: {fib_count2}/5 = {combo2['fibonacci_percentage']:.0f}%)")
    print(f"   Stars: {combo2_stars}")
    
    # Combination 3: Balanced Range Fibonacci
    print("\n3️⃣ BALANCED RANGE FIBONACCI")
    print("   Strategy: Distribute Fibonacci across low, mid, high ranges")
    
    # Strategic distribution: 1 low Fibonacci, 1 mid Fibonacci, 1 high, 2 others
    low_fib = [1, 2, 3, 5, 8]
    mid_fib = [13, 21]
    high_fib = [34]
    
    combo3_numbers = []
    combo3_numbers.append(random.choice(low_fib))  # Low range Fibonacci
    combo3_numbers.append(random.choice(mid_fib))  # Mid range Fibonacci
    
    # Add strategic non-Fibonacci from different ranges
    combo3_numbers.append(random.choice(range(10, 20)))  # Mid-low
    combo3_numbers.append(random.choice(range(25, 35)))  # Mid-high  
    combo3_numbers.append(random.choice(range(40, 50)))  # High
    
    combo3_numbers = sorted(list(set(combo3_numbers))[:5])  # Remove duplicates if any
    while len(combo3_numbers) < 5:  # Fill if needed
        combo3_numbers.append(random.choice(range(1, 51)))
        combo3_numbers = sorted(list(set(combo3_numbers)))
    
    combo3_stars = [3, 11]  # Frequent from analysis but not May 20
    
    fib_count3 = len([n for n in combo3_numbers if n in fibonacci_numbers])
    combo3 = {
        'numbers': combo3_numbers[:5],
        'stars': combo3_stars,
        'strategy': 'Balanced Range Fibonacci',
        'fibonacci_percentage': (fib_count3/5) * 100,
        'description': 'Strategic Fibonacci distribution across number ranges'
    }
    fresh_combinations.append(combo3)
    
    print(f"   Numbers: {combo3_numbers[:5]} (Fibonacci: {fib_count3}/5 = {combo3['fibonacci_percentage']:.0f}%)")
    print(f"   Stars: {combo3_stars}")
    
    # Combination 4: Mathematical Gap Pattern
    print("\n4️⃣ MATHEMATICAL GAP PATTERN")
    print("   Strategy: Use Fibonacci-inspired gaps between numbers")
    
    # Start with a Fibonacci number, then use Fibonacci sequence as gaps
    start_num = random.choice([2, 3, 5])
    gaps = [2, 3, 5, 8]  # Fibonacci gaps
    
    combo4_numbers = [start_num]
    current = start_num
    
    for gap in gaps:
        current += gap
        if current <= 50:
            combo4_numbers.append(current)
        else:
            # Wrap around or adjust
            combo4_numbers.append(current - 20)
    
    combo4_numbers = sorted(list(set(combo4_numbers))[:5])
    while len(combo4_numbers) < 5:
        combo4_numbers.append(random.choice(fibonacci_numbers))
        combo4_numbers = sorted(list(set(combo4_numbers)))
    
    combo4_stars = [6, 8]  # Mix May 20 winner (6) with frequent (8)
    
    fib_count4 = len([n for n in combo4_numbers if n in fibonacci_numbers])
    combo4 = {
        'numbers': combo4_numbers[:5],
        'stars': combo4_stars,
        'strategy': 'Mathematical Gap Pattern',
        'fibonacci_percentage': (fib_count4/5) * 100,
        'description': 'Fibonacci-inspired mathematical spacing pattern'
    }
    fresh_combinations.append(combo4)
    
    print(f"   Numbers: {combo4_numbers[:5]} (Fibonacci: {fib_count4}/5 = {combo4['fibonacci_percentage']:.0f}%)")
    print(f"   Stars: {combo4_stars}")
    
    # Combination 5: Inverse Frequency Power
    print("\n5️⃣ INVERSE FREQUENCY POWER")
    print("   Strategy: Apply proven methodology to less frequent but mathematically sound numbers")
    
    # Take numbers that didn't appear much in analysis but are mathematically interesting
    less_frequent_but_valid = [4, 6, 7, 9, 14, 17, 18, 19, 23, 24, 26, 27, 31, 33, 37, 39, 41, 42, 44, 46, 48, 49]
    
    # Mix with 1-2 Fibonacci for mathematical foundation
    combo5_numbers = random.sample([3, 5, 21], 2)  # Less used Fibonacci
    combo5_numbers.extend(random.sample(less_frequent_but_valid, 3))
    combo5_numbers = sorted(combo5_numbers)
    
    combo5_stars = [2, 12]  # Unexplored but mathematically valid
    
    fib_count5 = len([n for n in combo5_numbers if n in fibonacci_numbers])
    combo5 = {
        'numbers': combo5_numbers,
        'stars': combo5_stars,
        'strategy': 'Inverse Frequency Power',
        'fibonacci_percentage': (fib_count5/5) * 100,
        'description': 'Proven methodology applied to unexplored number territory'
    }
    fresh_combinations.append(combo5)
    
    print(f"   Numbers: {combo5_numbers} (Fibonacci: {fib_count5}/5 = {combo5['fibonacci_percentage']:.0f}%)")
    print(f"   Stars: {combo5_stars}")
    
    return fresh_combinations

def analyze_fresh_combinations(combinations):
    """Analyze the fresh combinations for patterns and scoring"""
    
    print(f"\n📊 FRESH COMBINATIONS ANALYSIS")
    print("=" * 50)
    
    fibonacci_numbers = [1, 2, 3, 5, 8, 13, 21, 34]
    
    for i, combo in enumerate(combinations, 1):
        print(f"\n{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']}")
        print(f"   Stars: {combo['stars']}")
        print(f"   Fibonacci Content: {combo['fibonacci_percentage']:.0f}%")
        
        # Identify which numbers are Fibonacci
        fib_in_combo = [n for n in combo['numbers'] if n in fibonacci_numbers]
        if fib_in_combo:
            print(f"   Fibonacci Numbers: {fib_in_combo}")
        
        # Calculate range distribution
        low_count = len([n for n in combo['numbers'] if n <= 17])
        mid_count = len([n for n in combo['numbers'] if 18 <= n <= 34])
        high_count = len([n for n in combo['numbers'] if n >= 35])
        
        print(f"   Range Distribution: Low({low_count}) Mid({mid_count}) High({high_count})")
        print(f"   Description: {combo['description']}")

def main():
    """Generate and analyze fresh Fibonacci-Filtered Hybrid combinations"""
    
    # Generate fresh combinations
    fresh_combinations = generate_fresh_fibonacci_hybrid_combinations()
    
    # Analyze them
    analyze_fresh_combinations(fresh_combinations)
    
    print(f"\n🎯 FRESH COMBINATIONS SUMMARY")
    print("=" * 60)
    print(f"✅ Generated 5 fresh combinations using your proven methodology")
    print(f"✅ Applied Fibonacci-Filtered Hybrid strategy with new parameters")
    print(f"✅ Balanced mathematical precision with fresh number exploration")
    print(f"✅ Maintained validated framework while creating new possibilities")
    
    print(f"\n🚀 Your fresh Fibonacci-Filtered Hybrid combinations are ready!")
    print(f"These represent new winning possibilities using your proven mathematical framework!")
    
    return fresh_combinations

if __name__ == "__main__":
    main()