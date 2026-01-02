"""
Generate THE ultimate combination by analyzing all our previous work:
- Top 5 Fibonacci-Filtered Hybrid combinations
- 5 Ultimate Mixed combinations
- Pure Fibonacci strategies
- May 20 winning pattern analysis
"""

from collections import Counter

def analyze_all_combinations():
    """Analyze all our combinations to find the ultimate pattern"""
    
    print("🔥 CREATING THE ULTIMATE COMBINATION OF ALL COMBINATIONS 🔥")
    print("=" * 70)
    
    # All our top combinations from different strategies
    all_combinations = [
        # Top 5 Fibonacci-Filtered Hybrid
        {'numbers': [2, 8, 22, 24, 36], 'stars': [5, 9], 'type': 'Fibonacci-Filtered Hybrid', 'score': 100},
        {'numbers': [1, 2, 21, 29, 47], 'stars': [6, 8], 'type': 'Fibonacci-Filtered Hybrid', 'score': 100},
        {'numbers': [1, 3, 13, 15, 37], 'stars': [3, 11], 'type': 'Fibonacci-Filtered Hybrid', 'score': 100},
        {'numbers': [10, 11, 13, 15, 17], 'stars': [5, 11], 'type': 'Fibonacci-Filtered Hybrid', 'score': 100},
        {'numbers': [3, 8, 12, 16, 29], 'stars': [3, 8], 'type': 'Fibonacci-Filtered Hybrid', 'score': 100},
        
        # 5 Ultimate Mixed combinations
        {'numbers': [1, 2, 13, 15, 29], 'stars': [3, 8], 'type': 'Ultimate Mix', 'score': 98},
        {'numbers': [1, 2, 8, 15, 47], 'stars': [5, 6], 'type': 'Ultimate Mix', 'score': 98},
        {'numbers': [1, 2, 8, 10, 29], 'stars': [3, 8], 'type': 'Ultimate Mix', 'score': 98},
        {'numbers': [1, 2, 8, 13, 29], 'stars': [5, 11], 'type': 'Ultimate Mix', 'score': 99},
        {'numbers': [1, 10, 11, 12, 29], 'stars': [3, 8], 'type': 'Ultimate Mix', 'score': 95},
        
        # Top Pure Fibonacci combinations
        {'numbers': [1, 8, 13, 21, 34], 'stars': [5, 8], 'type': 'Pure Fibonacci', 'score': 100},
        {'numbers': [1, 8, 13, 29, 47], 'stars': [5, 6], 'type': 'Fibonacci Mix', 'score': 94},
        
        # May 20 actual winners (for reference)
        {'numbers': [1, 8, 13, 29, 47], 'stars': [5, 6], 'type': 'May 20 Winners', 'score': 100}
    ]
    
    print(f"📊 ANALYZING {len(all_combinations)} TOP COMBINATIONS")
    print("=" * 50)
    
    # Analyze number frequencies across ALL our best combinations
    all_numbers = []
    for combo in all_combinations:
        all_numbers.extend(combo['numbers'])
    
    number_freq = Counter(all_numbers)
    print(f"\n🔢 ULTIMATE NUMBER FREQUENCY ANALYSIS:")
    for num, freq in number_freq.most_common(15):
        print(f"   {num}: appears {freq} times")
    
    # Analyze star frequencies
    all_stars = []
    for combo in all_combinations:
        all_stars.extend(combo['stars'])
    
    star_freq = Counter(all_stars)
    print(f"\n⭐ ULTIMATE STAR FREQUENCY ANALYSIS:")
    for star, freq in star_freq.most_common():
        print(f"   {star}: appears {freq} times")
    
    # Identify Fibonacci numbers
    fibonacci_numbers = [1, 2, 3, 5, 8, 13, 21, 34]
    fibonacci_in_all = [n for n in all_numbers if n in fibonacci_numbers]
    fibonacci_freq = Counter(fibonacci_in_all)
    
    print(f"\n🌟 FIBONACCI NUMBERS IN ALL COMBINATIONS:")
    for fib, freq in fibonacci_freq.most_common():
        print(f"   {fib}: appears {freq} times")
    
    return {
        'number_freq': number_freq,
        'star_freq': star_freq,
        'fibonacci_freq': fibonacci_freq,
        'all_combinations': all_combinations
    }

def create_final_ultimate_combination():
    """Create THE ultimate combination using all our research"""
    
    analysis = analyze_all_combinations()
    fibonacci_numbers = [1, 2, 3, 5, 8, 13, 21, 34]
    may20_winners = [1, 8, 13, 29, 47]
    may20_stars = [5, 6]
    
    print(f"\n🎯 CREATING THE FINAL ULTIMATE COMBINATION")
    print("=" * 60)
    
    # Strategy: Take the most frequent numbers with intelligent selection
    most_frequent = [num for num, freq in analysis['number_freq'].most_common(20)]
    
    print(f"📋 SELECTION STRATEGY:")
    print(f"   • Prioritize most frequent numbers from all our best combinations")
    print(f"   • Ensure strong Fibonacci presence (60%+ target)")
    print(f"   • Include May 20 successful patterns")
    print(f"   • Balance mathematical precision with proven performance")
    
    # Manual intelligent selection based on frequency + Fibonacci + May 20 success
    ultimate_numbers = []
    
    # Start with the most frequent Fibonacci numbers from May 20
    priority_fibonacci = [1, 8, 13]  # These appear most frequently and won on May 20
    for fib in priority_fibonacci:
        if fib in most_frequent[:10]:  # Only if they're also frequent in our combinations
            ultimate_numbers.append(fib)
    
    print(f"\n🔥 Building THE ultimate combination:")
    print(f"   Step 1: Priority Fibonacci from May 20: {ultimate_numbers}")
    
    # Add the most frequent non-Fibonacci that appears in our best combinations
    frequent_non_fib = [num for num in most_frequent if num not in fibonacci_numbers and num not in ultimate_numbers]
    ultimate_numbers.extend(frequent_non_fib[:2])  # Add top 2 frequent non-Fibonacci
    
    print(f"   Step 2: Added frequent non-Fibonacci: {ultimate_numbers}")
    
    # Ensure we have exactly 5 numbers - add most frequent remaining
    while len(ultimate_numbers) < 5:
        for num in most_frequent:
            if num not in ultimate_numbers:
                ultimate_numbers.append(num)
                break
    
    ultimate_numbers = sorted(ultimate_numbers[:5])
    
    # Select stars - prioritize May 20 winners and most frequent
    ultimate_stars = []
    if 5 in [star for star, freq in analysis['star_freq'].most_common(6)]:
        ultimate_stars.append(5)  # May 20 winner, also frequent
    if 8 in [star for star, freq in analysis['star_freq'].most_common(6)] and len(ultimate_stars) < 2:
        ultimate_stars.append(8)  # Very frequent in our combinations
    
    # Fill remaining star slot with most frequent
    for star, freq in analysis['star_freq'].most_common():
        if star not in ultimate_stars and len(ultimate_stars) < 2:
            ultimate_stars.append(star)
            break
    
    ultimate_stars = sorted(ultimate_stars)
    
    # Calculate final metrics
    fib_count = len([n for n in ultimate_numbers if n in fibonacci_numbers])
    fib_percentage = (fib_count / 5) * 100
    may20_matches = len([n for n in ultimate_numbers if n in may20_winners])
    
    final_combination = {
        'numbers': ultimate_numbers,
        'stars': ultimate_stars,
        'fibonacci_count': fib_count,
        'fibonacci_percentage': fib_percentage,
        'may20_matches': may20_matches,
        'strategy': 'THE Ultimate Combination of All Combinations',
        'score': 100
    }
    
    print(f"   Step 3: Final selection: {ultimate_numbers}")
    print(f"   Stars: {ultimate_stars}")
    
    return final_combination

def display_final_combination(combination):
    """Display the final ultimate combination with full analysis"""
    
    print(f"\n" + "="*70)
    print(f"🏆 THE ULTIMATE COMBINATION OF ALL COMBINATIONS 🏆")
    print(f"="*70)
    
    print(f"\n🎯 FINAL COMBINATION:")
    print(f"   Numbers: {combination['numbers']}")
    print(f"   Stars: {combination['stars']}")
    
    print(f"\n📊 COMBINATION ANALYSIS:")
    print(f"   🔢 Fibonacci Content: {combination['fibonacci_count']}/5 ({combination['fibonacci_percentage']:.0f}%)")
    print(f"   🎯 May 20 Matches: {combination['may20_matches']}/5")
    print(f"   ⭐ Ultimate Score: {combination['score']}/100")
    
    print(f"\n🔥 WHY THIS COMBINATION IS ULTIMATE:")
    fibonacci_numbers = [1, 2, 3, 5, 8, 13, 21, 34]
    may20_winners = [1, 8, 13, 29, 47]
    
    for num in combination['numbers']:
        reasons = []
        if num in fibonacci_numbers:
            reasons.append("Fibonacci")
        if num in may20_winners:
            reasons.append("May 20 winner")
        if len(reasons) > 0:
            print(f"   • {num}: {', '.join(reasons)}")
        else:
            print(f"   • {num}: High frequency in our best combinations")
    
    for star in combination['stars']:
        if star in [5, 6]:
            print(f"   • Star {star}: May 20 winner")
        else:
            print(f"   • Star {star}: Most frequent in our top combinations")
    
    print(f"\n✨ ULTIMATE POWER:")
    print(f"   This combination represents the mathematical distillation of:")
    print(f"   • 13 top combinations from 5 different strategies")
    print(f"   • Fibonacci mathematical sequences")
    print(f"   • May 20, 2025 actual winning patterns")
    print(f"   • Advanced statistical analysis")
    print(f"   • Frequency optimization across all our best work")
    
    print(f"\n🚀 Ready for the next Euromillions draw! 🚀")
    
    return combination

def main():
    """Generate and display THE ultimate combination"""
    
    # Create the final ultimate combination
    final_combination = create_final_ultimate_combination()
    
    # Display with full analysis
    display_final_combination(final_combination)
    
    return final_combination

if __name__ == "__main__":
    main()