import json
import pandas as pd
from collections import Counter

# Actual draw results from May 6, 2025
actual_draw_numbers = [8, 23, 24, 47, 48]
actual_draw_stars = [4, 9]
actual_draw_date = "2025-05-06"

# Combinations played
combinations = [
    {
        "strategy": "Risk/Reward Strategy",
        "score": 96.42,
        "numbers": [3, 7, 15, 20, 50],
        "stars": [4, 9, 10]
    },
    {
        "strategy": "Ultimate Combined Strategy",
        "score": 95.0,
        "numbers": [15, 35, 40, 44, 48],
        "stars": [4, 10, 12]
    },
    {
        "strategy": "Risk/Reward Strategy",
        "score": 81.1,
        "numbers": [21, 30, 35, 39, 48],
        "stars": [4, 10, 11]
    },
    {
        "strategy": "Risk/Reward Strategy",
        "score": 76.17,
        "numbers": [15, 20, 31, 33, 39],
        "stars": [1, 4, 10]
    },
    {
        "strategy": "Frequency Strategy",
        "score": 9.57,
        "numbers": [11, 35, 40, 41, 48],
        "stars": [7, 10, 12]
    },
    {
        "strategy": "Frequency Strategy",
        "score": 8.69,
        "numbers": [29, 35, 40, 44, 48],
        "stars": [1, 6, 12]
    },
    {
        "strategy": "Frequency Strategy",
        "score": 7.95,
        "numbers": [2, 7, 40, 46, 47],
        "stars": [3, 4, 12]
    },
    {
        "strategy": "Frequency Strategy",
        "score": 6.3,
        "numbers": [9, 15, 25, 44, 47],
        "stars": [3, 7, 10]
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
    numbers_only_prize = get_prize_tier(len(matched_numbers), 0)
    with_stars_prize = get_prize_tier(len(matched_numbers), len(matched_stars))
    
    return {
        "strategy": combination["strategy"],
        "score": combination["score"],
        "matched_numbers": list(matched_numbers),
        "matched_stars": list(matched_stars),
        "total_matched": total_matched,
        "numbers_only_prize": numbers_only_prize,
        "with_stars_prize": with_stars_prize
    }

def get_prize_tier(num_matched, stars_matched):
    """Get prize tier based on matches"""
    # Simplified prize tier determination
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
    elif num_matched == 4 and stars_matched == 0:
        return "6th Prize"
    elif num_matched == 3 and stars_matched == 2:
        return "7th Prize"
    elif num_matched == 3 and stars_matched == 1:
        return "8th Prize"
    elif num_matched == 3 and stars_matched == 0:
        return "9th Prize"
    elif num_matched == 2 and stars_matched == 2:
        return "10th Prize"
    elif num_matched == 2 and stars_matched == 1:
        return "11th Prize"
    elif num_matched == 2 and stars_matched == 0:
        return "12th Prize"
    elif num_matched == 1 and stars_matched == 2:
        return "13th Prize"
    elif num_matched == 0 and stars_matched == 2:
        return "Small Prize"
    else:
        return "No Prize"

def strategy_performance_summary(results):
    """Summarize performance by strategy"""
    strategy_results = {}
    
    for result in results:
        strategy = result["strategy"]
        if strategy not in strategy_results:
            strategy_results[strategy] = {
                "combinations_count": 0,
                "total_matched": 0,
                "matched_numbers": 0,
                "matched_stars": 0,
                "prize_counts": Counter(),
                "combinations": []
            }
        
        sr = strategy_results[strategy]
        sr["combinations_count"] += 1
        sr["total_matched"] += result["total_matched"]
        sr["matched_numbers"] += len(result["matched_numbers"])
        sr["matched_stars"] += len(result["matched_stars"])
        sr["prize_counts"][result["with_stars_prize"]] += 1
        sr["combinations"].append(result)
    
    # Calculate averages
    for strategy, data in strategy_results.items():
        count = data["combinations_count"]
        data["avg_matched"] = data["total_matched"] / count
        data["avg_matched_numbers"] = data["matched_numbers"] / count
        data["avg_matched_stars"] = data["matched_stars"] / count
    
    return strategy_results

def analyze_all_combinations():
    """Analyze all combinations against actual results"""
    print(f"Analysis of combinations played for the {actual_draw_date} Euromillions draw")
    print(f"Actual draw numbers: {actual_draw_numbers}")
    print(f"Actual draw stars: {actual_draw_stars}")
    print("\n" + "="*80 + "\n")
    
    # Analyze each combination
    results = []
    for idx, combination in enumerate(combinations):
        result = analyze_combination(combination, actual_draw_numbers, actual_draw_stars)
        results.append(result)
        
        print(f"Combination {idx+1} ({combination['strategy']}, Score: {combination['score']}):")
        print(f"  Numbers played: {combination['numbers']}")
        print(f"  Stars played: {combination['stars']}")
        print(f"  Matched main numbers: {result['matched_numbers']} ({len(result['matched_numbers'])} of 5)")
        print(f"  Matched stars: {result['matched_stars']} ({len(result['matched_stars'])} of 2)")
        print(f"  Prize category: {result['with_stars_prize']}")
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
    
    # Strategy performance
    strategy_results = strategy_performance_summary(results)
    print("\nStrategy Performance Summary:")
    
    for strategy, data in strategy_results.items():
        print(f"  {strategy}:")
        print(f"    Combinations played: {data['combinations_count']}")
        print(f"    Average matched numbers: {data['avg_matched_numbers']:.2f}")
        print(f"    Average matched stars: {data['avg_matched_stars']:.2f}")
        
        # Best performing combination for this strategy
        best_combo = max(data["combinations"], key=lambda x: x["total_matched"])
        print(f"    Best combination had {len(best_combo['matched_numbers'])} numbers and {len(best_combo['matched_stars'])} stars")
        
        # Prize distribution
        prizes = data["prize_counts"]
        if "No Prize" in prizes:
            no_prize = prizes["No Prize"]
            prizes_won = data["combinations_count"] - no_prize
            print(f"    Combinations with prizes: {prizes_won} of {data['combinations_count']} ({prizes_won/data['combinations_count']*100:.1f}%)")
        
        print()
    
    # Score correlation analysis
    score_correlation = calculate_score_correlation(results)
    print("\nScore Correlation Analysis:")
    print(f"  Correlation between score and total matches: {score_correlation:.3f}")
    
    # Recommendations for future
    print("\nRecommendations for Future Draws:")
    future_recommendations()

def calculate_score_correlation(results):
    """Calculate correlation between score and matches"""
    if not results:
        return 0
    
    # Extract scores and total matches
    scores = [r["score"] for r in results]
    total_matches = [r["total_matched"] for r in results]
    
    # Calculate correlation if we have at least 2 data points
    if len(scores) < 2:
        return 0
    
    df = pd.DataFrame({"score": scores, "matches": total_matches})
    if df["score"].std() == 0 or df["matches"].std() == 0:
        return 0  # No correlation if no variation
        
    return df["score"].corr(df["matches"])

def future_recommendations():
    """Generate recommendations for future draws"""
    # Most common stars in actual draws
    print("  1. Continue using the stars 4 and 9 in future combinations as they appeared in this draw")
    print("  2. The number 47 and 48 appeared in both the draw and some of our combinations")
    print("  3. Consider using more balanced combinations of high and low numbers")
    print("  4. Both Risk/Reward and Frequency strategies had matches - continue using both")
    print("  5. Increase combinations that include numbers in the 20s range, as 23 and 24 appeared")

if __name__ == "__main__":
    analyze_all_combinations()