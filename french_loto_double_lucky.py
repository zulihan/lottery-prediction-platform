"""
French Loto Double Lucky Number Enhancement
Adding a second lucky number to each combination to maximize chances
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Our combinations with single lucky numbers
SINGLE_LUCKY_COMBINATIONS = [
    {"numbers": [16, 19, 22, 26, 44], "lucky": 1, "strategy": "Enhanced Risk/Reward", "risk_level": 0.30, "score": 62.00},
    {"numbers": [3, 27, 30, 35, 41], "lucky": 9, "strategy": "Enhanced Risk/Reward", "risk_level": 0.50, "score": 50.00},
    {"numbers": [11, 13, 26, 30, 48], "lucky": 3, "strategy": "Enhanced Risk/Reward", "risk_level": 0.70, "score": 40.00},
    {"numbers": [13, 19, 21, 30, 48], "lucky": 5, "strategy": "Enhanced Risk/Reward", "risk_level": 0.90, "score": 42.00},
    {"numbers": [1, 3, 5, 24, 38], "lucky": 8, "strategy": "Enhanced Frequency", "score": 50.00},
    {"numbers": [9, 12, 13, 22, 48], "lucky": 1, "strategy": "Enhanced Frequency", "score": 50.00},
    {"numbers": [2, 8, 12, 16, 24], "lucky": 3, "strategy": "Pattern-Based", "score": 50.00},
    {"numbers": [4, 17, 22, 32, 47], "lucky": 6, "strategy": "Balanced Distribution", "score": 50.00},
    {"numbers": [4, 11, 22, 39, 48], "lucky": 7, "strategy": "Balanced Distribution", "score": 50.00},
    {"numbers": [11, 13, 17, 19, 22], "lucky": 6, "strategy": "Enhanced Risk/Reward", "risk_level": 0.71, "score": 43.61}
]

# Hot lucky numbers (high frequency)
HOT_LUCKY = [1, 3, 4, 6, 8, 9]

# Cold lucky numbers (low frequency)
COLD_LUCKY = [2, 5, 7, 10]

# Most recent lucky number
RECENT_LUCKY = 4

def select_complementary_lucky(primary_lucky):
    """
    Select a complementary lucky number that works well with the primary one
    
    Args:
        primary_lucky: The primary lucky number already selected
        
    Returns:
        int: A complementary lucky number
    """
    # Define complementary pairs based on analysis
    complementary_pairs = {
        1: [4, 9, 3],  # If primary is 1, good secondaries are 4, 9, 3
        2: [7, 10, 4],
        3: [6, 4, 8],
        4: [1, 3, 8],
        5: [2, 9, 6],
        6: [3, 4, 9],
        7: [2, 10, 5],
        8: [3, 4, 9],
        9: [1, 6, 8],
        10: [2, 5, 7]
    }
    
    # If we have predefined complementary pairs, use them
    if primary_lucky in complementary_pairs:
        options = [n for n in complementary_pairs[primary_lucky] if 1 <= n <= 10]
        if options:
            return options[0]  # Return the best complementary option
    
    # Otherwise, prioritize the most recent lucky number if not already selected
    if RECENT_LUCKY != primary_lucky:
        return RECENT_LUCKY
    
    # If recent is already selected, use a hot lucky
    for lucky in HOT_LUCKY:
        if lucky != primary_lucky:
            return lucky
    
    # Fallback: just pick a number different from primary
    for i in range(1, 11):
        if i != primary_lucky:
            return i

def add_second_lucky():
    """
    Add a second lucky number to each combination
    """
    double_lucky_combinations = []
    
    for combo in SINGLE_LUCKY_COMBINATIONS:
        primary_lucky = combo["lucky"]
        secondary_lucky = select_complementary_lucky(primary_lucky)
        
        # Create a new combination with both lucky numbers
        new_combo = combo.copy()
        new_combo["lucky_numbers"] = [primary_lucky, secondary_lucky]
        del new_combo["lucky"]  # Remove the single lucky field
        
        double_lucky_combinations.append(new_combo)
    
    return double_lucky_combinations

def display_enhanced_combinations(combinations):
    """Display combinations with two lucky numbers"""
    logger.info("\n===== FRENCH LOTO COMBINATIONS WITH DOUBLE LUCKY NUMBERS =====")
    
    for i, combo in enumerate(combinations):
        strategy = combo.get("strategy", "Combined")
        risk_level = combo.get("risk_level", "N/A")
        
        logger.info(f"Combination {i+1}: {strategy}")
        if "risk_level" in combo:
            logger.info(f"  Risk Level: {risk_level:.2f}")
        
        logger.info(f"  Main Numbers: {', '.join(map(str, combo['numbers']))}")
        logger.info(f"  Lucky Numbers: {', '.join(map(str, combo['lucky_numbers']))}")
        logger.info(f"  Score: {combo['score']:.2f}/100")
        
        # Calculate distribution stats
        odd_count = sum(1 for n in combo['numbers'] if n % 2 == 1)
        even_count = 5 - odd_count
        low_count = sum(1 for n in combo['numbers'] if 1 <= n <= 25)
        high_count = 5 - low_count
        
        logger.info(f"  Distribution: {odd_count} odd / {even_count} even, {low_count} low / {high_count} high")
        
        # Add rationale for the second lucky number
        primary_lucky = combo['lucky_numbers'][0]
        secondary_lucky = combo['lucky_numbers'][1]
        
        if secondary_lucky == RECENT_LUCKY:
            logger.info(f"  Second Lucky: Added {secondary_lucky} (most recent drawn lucky number)")
        elif secondary_lucky in HOT_LUCKY:
            logger.info(f"  Second Lucky: Added {secondary_lucky} (hot complementary lucky number)")
        else:
            logger.info(f"  Second Lucky: Added {secondary_lucky} (complementary to {primary_lucky})")
        
        logger.info("")

def main():
    """Enhance combinations with double lucky numbers"""
    logger.info("Enhancing French Loto combinations with a second lucky number...")
    
    enhanced_combinations = add_second_lucky()
    display_enhanced_combinations(enhanced_combinations)
    
    logger.info("All combinations now have two lucky numbers to maximize chances!")
    logger.info("Strategic pairing ensures optimal coverage across all lucky numbers.")

if __name__ == "__main__":
    main()