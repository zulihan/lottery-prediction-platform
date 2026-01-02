"""
Generate improved French Loto combinations based on May 21, 2025 analysis insights
Key learnings: Low range focus, consecutive pairs, cold numbers, odd-dominant patterns
"""

import random

def generate_insight_based_combinations():
    """Generate combinations incorporating May 21 analysis insights"""
    
    print("🚀 IMPROVED FRENCH LOTO COMBINATIONS")
    print("Based on May 21, 2025 analysis insights")
    print("=" * 55)
    
    # May 21 insights
    print("📊 INCORPORATING KEY INSIGHTS:")
    print("✓ Low range focus (1-16) was dominant")
    print("✓ Consecutive pairs appeared (10-11)")
    print("✓ Cold numbers performed better")
    print("✓ Odd numbers dominated (3 odd vs 2 even)")
    print("✓ Lucky number was very low (3)")
    print()
    
    combinations = []
    
    # Strategy 1: Low Range Consecutive Focus
    print("1️⃣ LOW RANGE CONSECUTIVE FOCUS")
    print("   Strategy: Emphasize 1-16 range with consecutive pairs")
    
    # Build around consecutive pairs in low range
    consecutive_options = [(4,5), (6,7), (8,9), (12,13), (14,15)]
    chosen_consecutive = random.choice(consecutive_options)
    
    combo1_numbers = list(chosen_consecutive)
    # Add 3 more from low range (1-16)
    low_range = [n for n in range(1, 17) if n not in combo1_numbers]
    combo1_numbers.extend(random.sample(low_range, 3))
    combo1_numbers = sorted(combo1_numbers)
    combo1_lucky = random.choice([1, 2, 3, 4, 5])  # Low lucky numbers
    
    combo1 = {
        'numbers': combo1_numbers,
        'lucky': combo1_lucky,
        'strategy': 'Low Range Consecutive Focus',
        'description': f'Consecutive pair {chosen_consecutive} + low range dominance'
    }
    combinations.append(combo1)
    
    print(f"   Numbers: {combo1_numbers} | Lucky: {combo1_lucky}")
    print(f"   Features: Consecutive {chosen_consecutive}, all numbers ≤16")
    
    # Strategy 2: Cold Numbers Enhanced
    print("\n2️⃣ COLD NUMBERS ENHANCED")
    print("   Strategy: Focus on historically less frequent numbers")
    
    # Cold numbers (historically less frequent)
    cold_numbers = [1, 4, 9, 15, 16, 23, 26, 31, 32, 35, 39, 41, 45, 46, 48]
    combo2_numbers = sorted(random.sample(cold_numbers, 5))
    combo2_lucky = random.choice([2, 3, 6, 7])  # Mix of low-mid lucky
    
    combo2 = {
        'numbers': combo2_numbers,
        'lucky': combo2_lucky,
        'strategy': 'Cold Numbers Enhanced',
        'description': 'Focus on historically underrepresented numbers'
    }
    combinations.append(combo2)
    
    print(f"   Numbers: {combo2_numbers} | Lucky: {combo2_lucky}")
    print(f"   Features: All numbers from cold/infrequent pool")
    
    # Strategy 3: Odd-Dominant Pattern
    print("\n3️⃣ ODD-DOMINANT PATTERN")
    print("   Strategy: 3-4 odd numbers following May 21 pattern")
    
    # Build with 3-4 odd numbers, 1-2 even
    odd_candidates = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49]
    even_candidates = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48]
    
    combo3_numbers = random.sample(odd_candidates, 4) + random.sample(even_candidates, 1)
    combo3_numbers = sorted(combo3_numbers)
    combo3_lucky = random.choice([1, 3, 5, 7, 9])  # Odd lucky number
    
    combo3 = {
        'numbers': combo3_numbers,
        'lucky': combo3_lucky,
        'strategy': 'Odd-Dominant Pattern',
        'description': '4 odd + 1 even numbers with odd lucky'
    }
    combinations.append(combo3)
    
    print(f"   Numbers: {combo3_numbers} | Lucky: {combo3_lucky}")
    
    odd_count = len([n for n in combo3_numbers if n % 2 == 1])
    even_count = len([n for n in combo3_numbers if n % 2 == 0])
    print(f"   Features: {odd_count} odd, {even_count} even numbers")
    
    # Strategy 4: Low-Mid-High Balanced
    print("\n4️⃣ LOW-MID-HIGH BALANCED")
    print("   Strategy: Strategic distribution but emphasizing low range")
    
    # 3 from low (1-16), 1 from mid (17-33), 1 from high (34-49)
    low_pool = list(range(1, 17))
    mid_pool = list(range(17, 34))
    high_pool = list(range(34, 50))
    
    combo4_numbers = random.sample(low_pool, 3) + random.sample(mid_pool, 1) + random.sample(high_pool, 1)
    combo4_numbers = sorted(combo4_numbers)
    combo4_lucky = random.choice([2, 4, 6, 8])  # Even lucky for balance
    
    combo4 = {
        'numbers': combo4_numbers,
        'lucky': combo4_lucky,
        'strategy': 'Low-Mid-High Balanced',
        'description': '3 low + 1 mid + 1 high range distribution'
    }
    combinations.append(combo4)
    
    print(f"   Numbers: {combo4_numbers} | Lucky: {combo4_lucky}")
    
    low_count = len([n for n in combo4_numbers if n <= 16])
    mid_count = len([n for n in combo4_numbers if 17 <= n <= 33])
    high_count = len([n for n in combo4_numbers if n >= 34])
    print(f"   Features: Low({low_count}) Mid({mid_count}) High({high_count})")
    
    # Strategy 5: Sequential Pattern Advanced
    print("\n5️⃣ SEQUENTIAL PATTERN ADVANCED")
    print("   Strategy: Multiple consecutive elements and patterns")
    
    # Create a combination with multiple consecutive elements
    combo5_numbers = [6, 7]  # One consecutive pair
    combo5_numbers.extend([12, 13])  # Another consecutive pair
    # Add one more strategic number
    combo5_numbers.append(random.choice([3, 9, 19, 25, 31]))
    combo5_numbers = sorted(combo5_numbers)
    combo5_lucky = 3  # Use the winning lucky number
    
    combo5 = {
        'numbers': combo5_numbers,
        'lucky': combo5_lucky,
        'strategy': 'Sequential Pattern Advanced',
        'description': 'Two consecutive pairs (6-7, 12-13) + strategic fifth'
    }
    combinations.append(combo5)
    
    print(f"   Numbers: {combo5_numbers} | Lucky: {combo5_lucky}")
    print(f"   Features: Two consecutive pairs + May 21 winning lucky number")
    
    return combinations

def analyze_new_combinations(combinations):
    """Analyze the new combinations for key characteristics"""
    
    print(f"\n📊 NEW COMBINATIONS ANALYSIS")
    print("=" * 45)
    
    for i, combo in enumerate(combinations, 1):
        print(f"\n{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        
        # Range analysis
        low_count = len([n for n in combo['numbers'] if n <= 16])
        mid_count = len([n for n in combo['numbers'] if 17 <= n <= 33])
        high_count = len([n for n in combo['numbers'] if n >= 34])
        
        # Odd/even analysis
        odd_count = len([n for n in combo['numbers'] if n % 2 == 1])
        even_count = len([n for n in combo['numbers'] if n % 2 == 0])
        
        # Consecutive analysis
        consecutive_pairs = []
        sorted_numbers = sorted(combo['numbers'])
        for j in range(len(sorted_numbers)-1):
            if sorted_numbers[j+1] - sorted_numbers[j] == 1:
                consecutive_pairs.append((sorted_numbers[j], sorted_numbers[j+1]))
        
        print(f"   Range: Low({low_count}) Mid({mid_count}) High({high_count})")
        print(f"   Parity: Odd({odd_count}) Even({even_count})")
        if consecutive_pairs:
            print(f"   Consecutive: {consecutive_pairs}")
        print(f"   Description: {combo['description']}")

def main():
    """Generate and analyze improved French Loto combinations"""
    
    # Generate combinations
    combinations = generate_insight_based_combinations()
    
    # Analyze them
    analyze_new_combinations(combinations)
    
    print(f"\n🎯 IMPROVED STRATEGY SUMMARY")
    print("=" * 50)
    print("✅ Applied May 21 analysis insights")
    print("✅ Emphasized low range numbers (1-16)")
    print("✅ Included consecutive pair strategies")
    print("✅ Focused on cold/infrequent numbers")
    print("✅ Implemented odd-dominant patterns")
    print("✅ Used low lucky number preferences")
    
    print(f"\n🚀 These combinations incorporate all key learnings!")
    print("Ready for the next French Loto draw!")
    
    return combinations

if __name__ == "__main__":
    main()