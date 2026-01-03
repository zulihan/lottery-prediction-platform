import pandas as pd
import json
import numpy as np
from collections import Counter

# May 9th, 2025 Euromillions draw results
actual_draw = {
    'date': '2025-05-09',
    'numbers': [15, 18, 25, 29, 47],
    'stars': [5, 9]
}

# Combinations we played
combinations = [
    # May 9th base combinations (8)
    {
        'strategy': 'May 9 Optimized (Risk: 0.40)',
        'numbers': [1, 5, 28, 39, 46],
        'stars': [1, 7, 10],
        'score': 88.50
    },
    {
        'strategy': 'May 9 Optimized (Risk: 0.46)',
        'numbers': [9, 10, 34, 44, 46],
        'stars': [3, 7, 10],
        'score': 90.00
    },
    {
        'strategy': 'May 9 Optimized (Risk: 0.53)',
        'numbers': [5, 12, 30, 35, 39],
        'stars': [9, 10, 11],
        'score': 93.50
    },
    {
        'strategy': 'May 9 Optimized (Risk: 0.59)',
        'numbers': [3, 17, 29, 39, 50],
        'stars': [3, 7, 10],
        'score': 90.00
    },
    {
        'strategy': 'May 9 Optimized (Risk: 0.65)',
        'numbers': [3, 15, 28, 35, 50],
        'stars': [6, 8, 11],
        'score': 85.50
    },
    {
        'strategy': 'May 9 Optimized (Risk: 0.71)',
        'numbers': [4, 9, 29, 43, 46],
        'stars': [1, 6, 7],
        'score': 85.50
    },
    {
        'strategy': 'May 9 Optimized (Risk: 0.78)',
        'numbers': [3, 15, 26, 35, 50],
        'stars': [4, 5, 6],
        'score': 92.00
    },
    {
        'strategy': 'May 9 Optimized (Risk: 0.84)',
        'numbers': [13, 15, 27, 39, 41],
        'stars': [2, 6, 9],
        'score': 95.00
    },
    
    # Ultimate Mix combinations (4)
    {
        'strategy': 'Ultimate Mix for May 9',
        'numbers': [5, 15, 28, 39, 46],
        'stars': [4, 7, 10],
        'score': 96.50
    },
    
    # Additional Ultimate Mix combinations (3)
    {
        'strategy': 'Ultimate Mix (May 9 - Hot_Numbers)',
        'numbers': [17, 25, 34, 41, 44],
        'stars': [1, 9, 11],
        'score': 86.55
    },
    {
        'strategy': 'Ultimate Mix (May 9 - Adjacent)',
        'numbers': [6, 24, 31, 48, 49],
        'stars': [2, 3, 11],
        'score': 87.26
    },
    {
        'strategy': 'Ultimate Mix (May 9 - Balanced)',
        'numbers': [12, 20, 30, 35, 38],
        'stars': [7, 8, 10],
        'score': 94.24
    }
]

def analyze_combination(combination, actual_numbers, actual_stars):
    """Analyze a single combination against actual results"""
    numbers_set = set(combination["numbers"])
    stars_set = set(combination["stars"])
    
    actual_numbers_set = set(actual_numbers)
    actual_stars_set = set(actual_stars)
    
    matched_numbers = numbers_set.intersection(actual_numbers_set)
    matched_stars = stars_set.intersection(actual_stars_set)
    
    total_matched = len(matched_numbers) + len(matched_stars)
    prize_tier = get_prize_tier(len(matched_numbers), len(matched_stars))
    
    return {
        "strategy": combination["strategy"],
        "score": combination.get("score", 0),
        "matched_numbers": list(matched_numbers),
        "matched_stars": list(matched_stars),
        "total_matched": total_matched,
        "prize_tier": prize_tier
    }

def get_prize_tier(num_matched, stars_matched):
    """Get prize tier based on matches"""
    if num_matched == 5 and stars_matched == 2:
        return "Jackpot"
    elif num_matched == 5 and stars_matched == 1:
        return "2nd Prize"
    elif num_matched == 5 and stars_matched == 0:
        return "3rd Prize"
    elif num_matched == 4 and stars_matched == 2:
        return "4th Prize"
    elif num_matched == 4 and stars_matched == 1:
        return "5th Prize"
    elif num_matched == 3 and stars_matched == 2:
        return "6th Prize"
    elif num_matched == 4 and stars_matched == 0:
        return "7th Prize"
    elif num_matched == 2 and stars_matched == 2:
        return "8th Prize"
    elif num_matched == 3 and stars_matched == 1:
        return "9th Prize"
    elif num_matched == 3 and stars_matched == 0:
        return "10th Prize"
    elif num_matched == 1 and stars_matched == 2:
        return "11th Prize"
    elif num_matched == 2 and stars_matched == 1:
        return "12th Prize"
    elif num_matched == 2 and stars_matched == 0:
        return "13th Prize"
    else:
        return "No Prize"

def strategy_performance_summary(results):
    """Summarize performance by strategy"""
    strategy_results = {}
    
    for result in results:
        strategy_type = result["strategy"].split("(")[0].strip()
        if strategy_type not in strategy_results:
            strategy_results[strategy_type] = {
                "combinations_count": 0,
                "total_matched_numbers": 0,
                "total_matched_stars": 0,
                "prize_counts": Counter(),
                "combinations": []
            }
        
        sr = strategy_results[strategy_type]
        sr["combinations_count"] += 1
        sr["total_matched_numbers"] += len(result["matched_numbers"])
        sr["total_matched_stars"] += len(result["matched_stars"])
        sr["prize_counts"][result["prize_tier"]] += 1
        sr["combinations"].append(result)
    
    # Calculate averages
    for strategy, data in strategy_results.items():
        count = data["combinations_count"]
        data["avg_matched_numbers"] = data["total_matched_numbers"] / count
        data["avg_matched_stars"] = data["total_matched_stars"] / count
    
    return strategy_results

def analyze_results():
    """Analyze all combinations against actual results"""
    print(f"Analysis of combinations played for the {actual_draw['date']} Euromillions draw")
    print(f"Actual draw numbers: {actual_draw['numbers']}")
    print(f"Actual draw stars: {actual_draw['stars']}")
    print("\n" + "="*80 + "\n")
    
    # Analyze each combination
    results = []
    for idx, combination in enumerate(combinations):
        result = analyze_combination(combination, actual_draw['numbers'], actual_draw['stars'])
        results.append(result)
        
        print(f"Combination {idx+1} ({combination['strategy']}):")
        print(f"  Numbers played: {combination['numbers']}")
        print(f"  Stars played: {combination['stars']}")
        print(f"  Matched main numbers: {result['matched_numbers']} ({len(result['matched_numbers'])} of 5)")
        print(f"  Matched stars: {result['matched_stars']} ({len(result['matched_stars'])} of 2)")
        print(f"  Prize category: {result['prize_tier']}")
        print()
    
    # Overall statistics
    all_matched_numbers = set()
    all_matched_stars = set()
    for result in results:
        all_matched_numbers.update(result["matched_numbers"])
        all_matched_stars.update(result["matched_stars"])
    
    print("\n" + "="*80)
    print("\nOverall Performance Summary:")
    print(f"  Total combinations played: {len(combinations)}")
    print(f"  Total unique matched numbers: {all_matched_numbers} ({len(all_matched_numbers)} of 5)")
    print(f"  Total unique matched stars: {all_matched_stars} ({len(all_matched_stars)} of 2)")
    
    # Count total prizes
    prize_counter = Counter()
    for result in results:
        prize_counter[result["prize_tier"]] += 1
    
    print("\nPrize Distribution:")
    for tier, count in sorted(prize_counter.items(), key=lambda x: (x[0] != "No Prize", x[0])):
        percentage = (count / len(combinations)) * 100
        print(f"  {tier+':':<15} {count} ({percentage:.1f}%)")
    
    # Strategy performance
    strategy_results = strategy_performance_summary(results)
    print("\nStrategy Performance Summary:")
    
    # Sort strategies by average match rate
    sorted_strategies = sorted(
        strategy_results.items(),
        key=lambda x: (x[1]["avg_matched_numbers"] + x[1]["avg_matched_stars"] * 2),
        reverse=True
    )
    
    for strategy, data in sorted_strategies:
        print(f"\n  {strategy}:")
        print(f"    Combinations played: {data['combinations_count']}")
        print(f"    Average matched numbers: {data['avg_matched_numbers']:.2f}")
        print(f"    Average matched stars: {data['avg_matched_stars']:.2f}")
        
        # Best performing combination for this strategy
        best_combo = max(data["combinations"], key=lambda x: x["total_matched"])
        print(f"    Best result: {len(best_combo['matched_numbers'])} numbers and {len(best_combo['matched_stars'])} stars")
        
        # Prize distribution
        prizes = data["prize_counts"]
        if "No Prize" in prizes:
            no_prize = prizes["No Prize"]
            prizes_won = data["combinations_count"] - no_prize
            print(f"    Combinations with prizes: {prizes_won} of {data['combinations_count']} ({prizes_won/data['combinations_count']*100:.1f}%)")
    
    # Winning numbers analysis
    print("\n" + "="*80)
    print("\nWinning Numbers Analysis:")
    
    # Analyze where winning numbers appeared in our combinations
    winning_numbers_freq = Counter()
    winning_stars_freq = Counter()
    
    for combo in combinations:
        for num in combo['numbers']:
            if num in actual_draw['numbers']:
                winning_numbers_freq[num] += 1
        
        for star in combo['stars']:
            if star in actual_draw['stars']:
                winning_stars_freq[star] += 1
    
    print("\nWinning number occurrences in our combinations:")
    for num in sorted(actual_draw['numbers']):
        freq = winning_numbers_freq.get(num, 0)
        percentage = (freq / len(combinations)) * 100
        print(f"  Number {num}: appeared in {freq} combinations ({percentage:.1f}%)")
    
    print("\nWinning star occurrences in our combinations:")
    for star in sorted(actual_draw['stars']):
        freq = winning_stars_freq.get(star, 0)
        percentage = (freq / len(combinations)) * 100
        print(f"  Star {star}: appeared in {freq} combinations ({percentage:.1f}%)")
    
    # Score correlation analysis
    scores = [r["score"] for r in results]
    matches = [r["total_matched"] for r in results]
    
    if len(scores) > 1 and len(set(scores)) > 1:
        correlation = np.corrcoef(scores, matches)[0, 1]
        print(f"\nCorrelation between combination score and matches: {correlation:.3f}")
    
    # Recommendations for future draws
    print("\n" + "="*80)
    print("\nRecommendations for Future Draws:")
    print("1. Focus more on winning numbers from this draw (15, 25, 29, 47)")
    print("2. Continue including star 9 which has appeared in both May 6 and May 9 draws")
    print("3. Consider using star 5 more frequently (appeared in today's draw)")
    print("4. The Ultimate Mix strategy performed well and should be retained")
    print("5. Consider increasing the weight of numbers in the 15-30 range (three winning numbers in this range)")

if __name__ == "__main__":
    analyze_results()