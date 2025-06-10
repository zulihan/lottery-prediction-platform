"""
Generate an 11th fusion combination using a different mathematical approach
"""

def get_base_combinations():
    """Get the 10 existing combinations"""
    return [
        {'numbers': [9, 33, 47, 48, 49], 'stars': [5, 12], 'strategy': 'Time Series - Summer Seasonal'},
        {'numbers': [2, 13, 24, 35, 46], 'stars': [9, 12], 'strategy': 'Time Series - Mathematical Progression'},
        {'numbers': [1, 14, 21, 28, 41], 'stars': [2, 12], 'strategy': 'Time Series - Range Cycling'},
        {'numbers': [4, 20, 34, 41, 49], 'stars': [9, 12], 'strategy': 'Time Series - Temporal Extension'},
        {'numbers': [8, 9, 38, 46, 49], 'stars': [9, 12], 'strategy': 'Time Series - Cyclical Synthesis'},
        {'numbers': [9, 33, 41, 46, 49], 'stars': [9, 12], 'strategy': 'Frequency-Based Fusion'},
        {'numbers': [9, 14, 28, 47, 49], 'stars': [2, 5], 'strategy': 'Positional Alternating Fusion'},
        {'numbers': [1, 24, 28, 35, 49], 'stars': [2, 12], 'strategy': 'Extreme Selection Fusion'},  # Fixed to 5 numbers
        {'numbers': [1, 9, 21, 34, 46], 'stars': [2, 5], 'strategy': 'Mathematical Spacing Fusion'},
        {'numbers': [1, 2, 14, 20, 49], 'stars': [2, 5], 'strategy': 'Range Balanced Fusion'}
    ]

def generate_prime_harmonic_fusion():
    """Generate fusion using prime numbers and harmonic relationships"""
    
    base_combinations = get_base_combinations()
    
    # Extract all unique numbers and stars
    all_numbers = set()
    all_stars = set()
    
    for combo in base_combinations:
        all_numbers.update(combo['numbers'])
        all_stars.update(combo['stars'])
    
    all_numbers = sorted(list(all_numbers))
    all_stars = sorted(list(all_stars))
    
    print("Available numbers:", all_numbers)
    print("Available stars:", all_stars)
    
    # Prime numbers within our range
    primes_in_range = []
    for num in all_numbers:
        if is_prime(num):
            primes_in_range.append(num)
    
    print("Prime numbers in range:", primes_in_range)
    
    # If we have enough primes, use them
    if len(primes_in_range) >= 5:
        prime_numbers = primes_in_range[:5]
    else:
        # Fill with numbers that have harmonic relationships
        prime_numbers = primes_in_range.copy()
        
        # Find numbers with harmonic relationships (sum relationships)
        remaining_numbers = [n for n in all_numbers if n not in prime_numbers]
        
        # Add numbers that create good sum patterns
        target_sum = sum(prime_numbers) + (130 - sum(prime_numbers)) // (5 - len(prime_numbers))
        
        for num in remaining_numbers:
            if len(prime_numbers) < 5:
                current_sum = sum(prime_numbers) + num
                if current_sum <= 150:  # Reasonable sum range
                    prime_numbers.append(num)
    
    # For stars, use harmonic relationship
    # Take stars that complement each other mathematically
    harmonic_stars = []
    if 2 in all_stars and 12 in all_stars:  # 2 and 12 have 6x relationship
        harmonic_stars = [2, 12]
    elif 5 in all_stars and 9 in all_stars:  # Good mathematical relationship
        harmonic_stars = [5, 9]
    else:
        harmonic_stars = all_stars[:2]
    
    return {
        'numbers': sorted(prime_numbers[:5]),
        'stars': sorted(harmonic_stars),
        'strategy': 'Prime-Harmonic Fusion',
        'logic': 'Combines prime numbers with harmonic mathematical relationships'
    }

def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def validate_combination(combination):
    """Validate the combination format"""
    numbers = combination['numbers']
    stars = combination['stars']
    
    # Check numbers
    if len(numbers) != 5:
        print(f"❌ Numbers error: Expected 5, got {len(numbers)}")
        return False
    
    if not all(1 <= n <= 49 for n in numbers):
        print(f"❌ Numbers range error: All numbers must be 1-49")
        return False
    
    if len(set(numbers)) != 5:
        print(f"❌ Numbers uniqueness error: Duplicate numbers found")
        return False
    
    # Check stars
    if len(stars) != 2:
        print(f"❌ Stars error: Expected 2, got {len(stars)}")
        return False
    
    if not all(1 <= s <= 12 for s in stars):
        print(f"❌ Stars range error: All stars must be 1-12")
        return False
    
    if len(set(stars)) != 2:
        print(f"❌ Stars uniqueness error: Duplicate stars found")
        return False
    
    print("✅ Combination format is valid")
    return True

def main():
    print("GENERATING 11TH FUSION COMBINATION")
    print("=" * 33)
    
    # Generate the new fusion combination
    fusion_11 = generate_prime_harmonic_fusion()
    
    print("\n11TH COMBINATION:")
    print("-" * 16)
    print(f"11. {fusion_11['strategy']}")
    print(f"    Numbers: {fusion_11['numbers']} + Stars: {fusion_11['stars']}")
    print(f"    Logic: {fusion_11['logic']}")
    
    # Validate the combination
    print("\nVALIDATION:")
    print("-" * 11)
    validate_combination(fusion_11)
    
    # Show summary of all numbers and stars used
    base_combinations = get_base_combinations()
    base_combinations.append(fusion_11)
    
    all_unique_numbers = set()
    all_unique_stars = set()
    
    for combo in base_combinations:
        all_unique_numbers.update(combo['numbers'])  
        all_unique_stars.update(combo['stars'])
    
    print(f"\nTOTAL COVERAGE:")
    print(f"Unique numbers used across all 11 combinations: {len(all_unique_numbers)}")
    print(f"Unique stars used across all 11 combinations: {len(all_unique_stars)}")
    print(f"Numbers: {sorted(list(all_unique_numbers))}")
    print(f"Stars: {sorted(list(all_unique_stars))}")

if __name__ == "__main__":
    main()