#!/usr/bin/env python3
import database
import datetime
import json

"""
Script to save the combinations for the May 6, 2025 draw to the database
"""

# Target draw date
target_date = datetime.date(2025, 5, 6)  # May 6, 2025 - Tuesday

# Combinations from the user
combinations = [
    {
        "numbers": [3, 7, 15, 20, 50],
        "stars": [4, 9, 10],
        "strategy": "Risk/Reward Strategy",
        "score": 96.42
    },
    {
        "numbers": [15, 35, 40, 44, 48],
        "stars": [4, 10, 12],
        "strategy": "Ultimate Combined Strategy",
        "score": 95.0
    },
    {
        "numbers": [21, 30, 35, 39, 48],
        "stars": [4, 10, 11],
        "strategy": "Risk/Reward Strategy",
        "score": 81.1
    },
    {
        "numbers": [15, 20, 31, 33, 39],
        "stars": [1, 4, 10],
        "strategy": "Risk/Reward Strategy",
        "score": 76.17
    },
    {
        "numbers": [11, 35, 40, 41, 48],
        "stars": [7, 10, 12],
        "strategy": "Frequency Strategy",
        "score": 9.57
    },
    {
        "numbers": [29, 35, 40, 44, 48],
        "stars": [1, 6, 12],
        "strategy": "Frequency Strategy",
        "score": 8.69
    },
    {
        "numbers": [2, 7, 40, 46, 47],
        "stars": [3, 4, 12],
        "strategy": "Frequency Strategy",
        "score": 7.95
    },
    {
        "numbers": [9, 15, 25, 44, 47],
        "stars": [3, 7, 10],
        "strategy": "Frequency Strategy",
        "score": 6.3
    }
]

def save_combinations():
    """Save all combinations to the database"""
    total_saved = 0
    
    for combo in combinations:
        try:
            combo_id = database.save_generated_combination(
                numbers=combo["numbers"],
                stars=combo["stars"],
                strategy=combo["strategy"],
                score=combo["score"],
                target_draw_date=target_date
            )
            if combo_id:
                total_saved += 1
                print(f"Saved combination {total_saved}: {combo['strategy']} (Score: {combo['score']})")
                print(f"  Numbers: {sorted(combo['numbers'])}")
                print(f"  Stars: {sorted(combo['stars'])}")
                print(f"  ID: {combo_id}")
                print("--------------------")
        except Exception as e:
            print(f"Error saving combination: {str(e)}")
    
    print(f"Saved {total_saved} out of {len(combinations)} combinations for May 6, 2025 draw")

if __name__ == "__main__":
    # Initialize database
    database.init_db()
    
    # Save combinations
    save_combinations()
