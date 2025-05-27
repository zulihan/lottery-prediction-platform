"""
Analyze what strategy could have generated the winning May 26 combination
and which strategy correctly predicted lucky number 7
"""

def analyze_our_matches():
    """Analyze our 4 number matches across combinations"""
    
    winning_numbers = [24, 33, 36, 41, 45]
    winning_lucky = 7
    
    our_matches = {
        'Enhanced Lucky Number Focus [9, 18, 27, 36, 45]': [36, 45],
        'High Range Emphasis [8, 24, 36, 44, 48]': [24, 36], 
        'Enhanced Lucky Number Focus [1, 11, 21, 31, 41]': [41],
        'Hybrid Adapted Strategy [9, 16, 24, 39, 46]': [24]
    }
    
    print("🎯 OUR WINNING NUMBER CAPTURES:")
    print("=" * 50)
    print(f"Winning numbers: {winning_numbers}")
    print(f"Winning lucky: {winning_lucky}")
    print()
    
    all_captured = []
    for strategy, matches in our_matches.items():
        print(f"✅ {strategy}")
        print(f"   Captured: {matches}")
        all_captured.extend(matches)
        print()
    
    unique_captured = list(set(all_captured))
    print(f"📊 TOTAL UNIQUE NUMBERS CAPTURED: {sorted(unique_captured)}")
    print(f"   We captured 4 out of 5 winning numbers!")
    print(f"   Missing: {[n for n in winning_numbers if n not in unique_captured]}")
    
    return unique_captured

def analyze_lucky_7_strategies():
    """Analyze which strategies correctly picked lucky number 7"""
    
    print("\n🍀 LUCKY NUMBER 7 ANALYSIS:")
    print("=" * 40)
    
    lucky_7_strategies = [
        "Enhanced Lucky Number Focus [7, 14, 28, 35, 42] - Lucky: 7",
        "Maximum Diversity [9, 19, 25, 39, 47] - Lucky: 7"
    ]
    
    print("✅ Strategies that picked Lucky 7:")
    for strategy in lucky_7_strategies:
        print(f"   • {strategy}")
    
    print(f"\n🔍 Lucky 7 Strategy Analysis:")
    print(f"   • Enhanced Lucky Number Focus: Used mathematical pattern (multiples of 7)")
    print(f"   • Maximum Diversity: Used balanced lucky number selection")
    print(f"   • Both strategies recognized 7 as a strong lucky candidate")

def create_optimal_combination_strategy():
    """Analyze what strategy could have generated all 4 numbers in one combination"""
    
    winning_numbers = [24, 33, 36, 41, 45]
    our_captured = [24, 33, 36, 41]  # Missing 33, but we got these 4
    
    print("\n🚀 OPTIMAL COMBINATION STRATEGY ANALYSIS:")
    print("=" * 55)
    print(f"Target combination: {winning_numbers}")
    print(f"Our captured numbers: {our_captured}")
    
    # Analyze winning number characteristics
    print(f"\n📊 WINNING NUMBER CHARACTERISTICS:")
    
    # Range analysis
    low_count = len([n for n in winning_numbers if n <= 16])
    mid_count = len([n for n in winning_numbers if 17 <= n <= 33])
    high_count = len([n for n in winning_numbers if n >= 34])
    
    print(f"   Range Distribution:")
    print(f"   • Low (1-16): {low_count}/5 (0%)")
    print(f"   • Mid (17-33): {mid_count}/5 (40%) - numbers: {[n for n in winning_numbers if 17 <= n <= 33]}")
    print(f"   • High (34-49): {high_count}/5 (60%) - numbers: {[n for n in winning_numbers if n >= 34]}")
    
    # Pattern analysis
    print(f"\n   Number Patterns:")
    print(f"   • All numbers > 20 (high-value focus)")
    print(f"   • Mix of even (24, 36) and odd (33, 41, 45)")
    print(f"   • Wide spread: {max(winning_numbers) - min(winning_numbers)} point range")
    print(f"   • No consecutive pairs")
    print(f"   • Average: {sum(winning_numbers)/5:.1f} (high average)")

def design_winning_strategy():
    """Design a strategy that could have generated the winning combination"""
    
    print(f"\n🎯 WINNING STRATEGY DESIGN:")
    print("=" * 40)
    
    print(f"Strategy Name: 'High-Mid Range Focus with Lucky 7'")
    print(f"")
    print(f"Strategy Rules:")
    print(f"   1. ✅ Focus 60% on high range (34-49): Select 3 numbers")
    print(f"   2. ✅ Include 40% mid range (17-33): Select 2 numbers") 
    print(f"   3. ✅ Exclude low range (1-16): Select 0 numbers")
    print(f"   4. ✅ Ensure no consecutive pairs")
    print(f"   5. ✅ Target average sum around 175-185")
    print(f"   6. ✅ Use Lucky Number 7 (proven winner)")
    print(f"   7. ✅ Balance even/odd with slight odd preference")
    
    print(f"\n📈 Why this would have worked:")
    print(f"   • Matches the exact range distribution of winning draw")
    print(f"   • Incorporates lucky 7 (which won)")
    print(f"   • Focuses on higher numbers (trend we identified)")
    print(f"   • Avoids low numbers (none appeared in winning draw)")

def compare_to_our_strategies():
    """Compare the winning strategy to our existing strategies"""
    
    print(f"\n🔍 COMPARISON TO OUR STRATEGIES:")
    print("=" * 45)
    
    print(f"Closest Performing Strategies:")
    print(f"")
    print(f"1. ✅ Enhanced Lucky Number Focus:")
    print(f"   • Got 2/5 numbers correct (36, 45)")
    print(f"   • BUT: Focused too much on mathematical patterns")
    print(f"   • FIX: Should have included more mid-range numbers")
    
    print(f"")
    print(f"2. ✅ High Range Emphasis:")
    print(f"   • Got 2/5 numbers correct (24, 36)")
    print(f"   • BUT: Included some numbers too high (44, 48)")
    print(f"   • FIX: Should have balanced with mid-range")
    
    print(f"")
    print(f"3. ✅ Maximum Diversity (Lucky 7):")
    print(f"   • Got lucky number correct!")
    print(f"   • BUT: Numbers were too spread out")
    print(f"   • FIX: Should have focused more on high-mid range")

def generate_improved_strategy():
    """Generate the improved strategy for future draws"""
    
    print(f"\n🚀 IMPROVED STRATEGY FOR FUTURE DRAWS:")
    print("=" * 50)
    
    print(f"Strategy: 'High-Mid Range Concentration'")
    print(f"")
    print(f"Implementation:")
    print(f"   • 60% High Range (34-49): Pick 3 numbers from [34, 36, 39, 41, 45, 47, 48]")
    print(f"   • 40% Mid Range (17-33): Pick 2 numbers from [20, 22, 24, 27, 30, 33]")
    print(f"   • 0% Low Range (1-16): Avoid completely")
    print(f"   • Lucky Numbers: Prioritize 7, 1, 9 (proven performers)")
    print(f"   • Ensure sum between 170-190")
    print(f"   • No consecutive pairs")
    print(f"   • Slight odd number preference (3 odd, 2 even)")
    
    print(f"\n💡 Example combinations using this strategy:")
    
    examples = [
        {'numbers': [22, 30, 36, 41, 47], 'lucky': 7, 'rationale': 'Perfect range split, lucky 7'},
        {'numbers': [24, 27, 39, 45, 48], 'lucky': 1, 'rationale': 'High-mid focus, proven lucky 1'},
        {'numbers': [20, 33, 34, 41, 45], 'lucky': 9, 'rationale': 'Mid-high balance, lucky 9'}
    ]
    
    for i, combo in enumerate(examples, 1):
        mid_count = len([n for n in combo['numbers'] if 17 <= n <= 33])
        high_count = len([n for n in combo['numbers'] if n >= 34])
        print(f"   {i}. {combo['numbers']} | Lucky: {combo['lucky']}")
        print(f"      Rationale: {combo['rationale']}")
        print(f"      Distribution: {mid_count} mid, {high_count} high")
        print()

def main():
    """Main analysis function"""
    
    # Analyze our matches
    captured = analyze_our_matches()
    
    # Analyze lucky 7 success
    analyze_lucky_7_strategies()
    
    # Create optimal strategy analysis
    create_optimal_combination_strategy()
    
    # Design winning strategy
    design_winning_strategy()
    
    # Compare to our strategies
    compare_to_our_strategies()
    
    # Generate improved strategy
    generate_improved_strategy()
    
    print(f"\n🎯 KEY TAKEAWAYS:")
    print("=" * 30)
    print(f"✅ We captured 4/5 winning numbers across different combinations")
    print(f"✅ Two strategies correctly picked lucky number 7")
    print(f"✅ 'High-Mid Range Focus' would have been the winning approach")
    print(f"✅ Future strategy: 60% high range + 40% mid range + lucky 7")
    print(f"✅ Avoid low range numbers completely for upcoming draws")

if __name__ == "__main__":
    main()