#!/usr/bin/env python3

import database

def main():
    # View Risk/Reward Strategy combinations
    print("\nRisk/Reward Strategy Combinations:")
    risk_reward_combos = database.get_generated_combinations(strategy="Risk/Reward Strategy", limit=7)
    for i, combo in enumerate(risk_reward_combos):
        print(f"\nCombination {i+1}:")
        print(f"  Main Numbers: {', '.join(map(str, sorted(combo['numbers'])))}")
        print(f"  Stars: {', '.join(map(str, sorted(combo['stars'])))}")
        print(f"  Score: {combo['score']}")
    
    # View Ultimate Combined Strategy combinations
    print("\nUltimate Combined Strategy:")
    ultimate_combos = database.get_generated_combinations(strategy="Ultimate Combined Strategy", limit=3)
    for i, combo in enumerate(ultimate_combos):
        print(f"\nCombination {i+1}:")
        print(f"  Main Numbers: {', '.join(map(str, sorted(combo['numbers'])))}")
        print(f"  Stars: {', '.join(map(str, sorted(combo['stars'])))}")
        print(f"  Score: {combo['score']}")

if __name__ == "__main__":
    main()
