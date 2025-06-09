"""
Correctly fuse the original 5 Time Series combinations using only their existing numbers
"""

def get_original_5_combinations():
    """Get the exact original 5 Time Series combinations"""
    return [
        {'numbers': [9, 28, 35, 41, 47], 'lucky': 1, 'strategy': 'Time Series - Summer Seasonal'},
        {'numbers': [5, 13, 31, 39, 44], 'lucky': 6, 'strategy': 'Time Series - Mathematical Progression'},
        {'numbers': [12, 26, 34, 42, 48], 'lucky': 2, 'strategy': 'Time Series - Range Cycling'},
        {'numbers': [8, 22, 33, 38, 46], 'lucky': 4, 'strategy': 'Time Series - Temporal Extension'},
        {'numbers': [6, 19, 29, 36, 43], 'lucky': 8, 'strategy': 'Time Series - Cyclical Synthesis'}
    ]

def extract_all_unique_numbers():
    """Extract all unique numbers from the 5 original combinations"""
    original_combos = get_original_5_combinations()
    
    all_numbers = set()
    all_lucky = []
    
    for combo in original_combos:
        all_numbers.update(combo['numbers'])
        all_lucky.append(combo['lucky'])
    
    print("AVAILABLE NUMBERS FROM ORIGINAL 5 COMBINATIONS:")
    print("=" * 50)
    print(f"All unique numbers: {sorted(list(all_numbers))}")
    print(f"Total unique numbers available: {len(all_numbers)}")
    print(f"Lucky numbers available: {all_lucky}")
    print()
    
    return sorted(list(all_numbers)), all_lucky

def frequency_based_fusion():
    """Select numbers based on frequency across the 5 original combinations"""
    original_combos = get_original_5_combinations()
    
    frequency_count = {}
    for combo in original_combos:
        for num in combo['numbers']:
            frequency_count[num] = frequency_count.get(num, 0) + 1
    
    # Sort by frequency, then by value
    sorted_by_freq = sorted(frequency_count.items(), key=lambda x: (x[1], x[0]), reverse=True)
    
    # Take top 5 most frequent
    top_5_numbers = [num for num, freq in sorted_by_freq[:5]]
    
    return sorted(top_5_numbers)

def positional_fusion(combo1_idx, combo2_idx):
    """Fuse two combinations by alternating positions"""
    original_combos = get_original_5_combinations()
    
    combo1 = original_combos[combo1_idx]
    combo2 = original_combos[combo2_idx]
    
    fused_numbers = []
    
    # Alternate taking numbers from each combination
    for i in range(5):
        if i % 2 == 0:  # Even positions from combo1
            fused_numbers.append(combo1['numbers'][i])
        else:  # Odd positions from combo2
            fused_numbers.append(combo2['numbers'][i])
    
    # Remove duplicates and sort
    fused_numbers = sorted(list(set(fused_numbers)))
    
    # If we have duplicates and less than 5, fill from remaining numbers
    if len(fused_numbers) < 5:
        remaining_numbers = []
        for num in combo1['numbers'] + combo2['numbers']:
            if num not in fused_numbers:
                remaining_numbers.append(num)
        
        remaining_numbers = sorted(list(set(remaining_numbers)))
        fused_numbers.extend(remaining_numbers[:5-len(fused_numbers)])
    
    return sorted(fused_numbers[:5])

def extreme_selection_fusion():
    """Select extreme numbers (highest and lowest) from all 5 combinations"""
    all_numbers, _ = extract_all_unique_numbers()
    
    # Take 2 lowest, 1 middle, 2 highest
    sorted_nums = sorted(all_numbers)
    
    fusion_numbers = []
    fusion_numbers.extend(sorted_nums[:2])  # 2 lowest
    fusion_numbers.append(sorted_nums[len(sorted_nums)//2])  # 1 middle
    fusion_numbers.extend(sorted_nums[-2:])  # 2 highest
    
    return sorted(fusion_numbers)

def mathematical_spacing_fusion():
    """Create fusion based on mathematical spacing from original numbers"""
    all_numbers, _ = extract_all_unique_numbers()
    
    # Find numbers that create good mathematical spacing
    sorted_nums = sorted(all_numbers)
    
    # Try to find 5 numbers with roughly equal spacing
    target_spacing = (max(sorted_nums) - min(sorted_nums)) // 4
    
    fusion_numbers = [sorted_nums[0]]  # Start with lowest
    
    for i in range(1, 5):
        target = fusion_numbers[0] + (i * target_spacing)
        # Find closest available number to target
        closest = min(sorted_nums, key=lambda x: abs(x - target))
        if closest not in fusion_numbers:
            fusion_numbers.append(closest)
    
    # If we don't have 5, fill with remaining numbers
    while len(fusion_numbers) < 5:
        for num in sorted_nums:
            if num not in fusion_numbers:
                fusion_numbers.append(num)
                break
    
    return sorted(fusion_numbers[:5])

def range_balanced_fusion():
    """Create fusion ensuring balanced range representation"""
    all_numbers, _ = extract_all_unique_numbers()
    
    # Categorize by ranges
    low_range = [n for n in all_numbers if 1 <= n <= 16]
    mid_range = [n for n in all_numbers if 17 <= n <= 33]
    high_range = [n for n in all_numbers if 34 <= n <= 49]
    
    fusion_numbers = []
    
    # Take 1-2 from each range to ensure balance
    if low_range:
        fusion_numbers.extend(sorted(low_range)[:2])
    if mid_range:
        fusion_numbers.extend(sorted(mid_range)[:2])
    if high_range:
        fusion_numbers.extend(sorted(high_range)[:2])
    
    # Trim to 5 numbers
    return sorted(fusion_numbers[:5])

def generate_correct_fusion_combinations():
    """Generate 5 fusion combinations using only numbers from original 5"""
    
    all_numbers, all_lucky = extract_all_unique_numbers()
    original_combos = get_original_5_combinations()
    
    fusion_combinations = []
    
    # 1. Frequency-Based Fusion
    freq_numbers = frequency_based_fusion()
    fusion_combinations.append({
        'numbers': freq_numbers,
        'lucky': 1,  # Most frequent lucky from originals
        'strategy': 'Frequency-Based Fusion',
        'logic': 'Selects 5 most frequent numbers across all original combinations'
    })
    
    # 2. Positional Fusion (Combos 1 & 3)
    pos_numbers = positional_fusion(0, 2)  # Summer Seasonal + Range Cycling
    fusion_combinations.append({
        'numbers': pos_numbers,
        'lucky': 6,  # Average of lucky 1 and 2
        'strategy': 'Positional Alternating Fusion',
        'logic': 'Alternates positions between Summer Seasonal and Range Cycling combinations'
    })
    
    # 3. Extreme Selection Fusion
    extreme_numbers = extreme_selection_fusion()
    fusion_combinations.append({
        'numbers': extreme_numbers,
        'lucky': 4,  # Median lucky number
        'strategy': 'Extreme Selection Fusion',
        'logic': 'Combines highest and lowest numbers from all 5 original combinations'
    })
    
    # 4. Mathematical Spacing Fusion
    spacing_numbers = mathematical_spacing_fusion()
    fusion_combinations.append({
        'numbers': spacing_numbers,
        'lucky': 8,  # Highest lucky from originals
        'strategy': 'Mathematical Spacing Fusion',
        'logic': 'Creates equal spacing pattern using available numbers from originals'
    })
    
    # 5. Range Balanced Fusion
    balanced_numbers = range_balanced_fusion()
    fusion_combinations.append({
        'numbers': balanced_numbers,
        'lucky': 2,  # Second most frequent lucky
        'strategy': 'Range Balanced Fusion',
        'logic': 'Ensures balanced representation across low, mid, and high ranges'
    })
    
    return fusion_combinations

def main():
    print("CORRECTED FUSION: USING ONLY ORIGINAL 5 COMBINATION NUMBERS")
    print("=" * 62)
    
    all_numbers, all_lucky = extract_all_unique_numbers()
    
    fusion_combinations = generate_correct_fusion_combinations()
    
    print("5 CORRECTED FUSION COMBINATIONS:")
    print("-" * 32)
    
    for i, combo in enumerate(fusion_combinations, 1):
        print(f"{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        print(f"   Logic: {combo['logic']}")
        print()
    
    # Verify all numbers come from originals
    print("VERIFICATION:")
    print("=" * 12)
    
    all_fusion_numbers = set()
    for combo in fusion_combinations:
        all_fusion_numbers.update(combo['numbers'])
    
    original_numbers = set()
    original_combos = get_original_5_combinations()
    for combo in original_combos:
        original_numbers.update(combo['numbers'])
    
    unauthorized_numbers = all_fusion_numbers - original_numbers
    
    if not unauthorized_numbers:
        print("✓ All fusion numbers come from original 5 combinations")
    else:
        print(f"✗ Unauthorized numbers found: {unauthorized_numbers}")
    
    print(f"✓ Total original numbers available: {len(original_numbers)}")
    print(f"✓ Total fusion numbers used: {len(all_fusion_numbers)}")

if __name__ == "__main__":
    main()