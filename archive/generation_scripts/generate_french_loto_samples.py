"""
Generate sample French Loto combinations using top-performing strategies.
This script will generate combinations using Risk/Reward strategy and Frequency Analysis.
"""

import pandas as pd
from database import get_db_connection
from french_loto_strategy import FrenchLotoStrategy
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_french_loto_data():
    """Load French Loto data from the database."""
    try:
        conn = get_db_connection()
        if conn:
            query = "SELECT * FROM french_loto_drawings ORDER BY date DESC"
            data = pd.read_sql(query, conn)
            logger.info(f"Loaded {len(data)} French Loto drawings")
            return data
        else:
            logger.error("Could not connect to database.")
            return None
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return None

def generate_combinations():
    """Generate French Loto combinations using top-performing strategies."""
    # Load data
    data = load_french_loto_data()
    if data is None:
        logger.error("No data available. Cannot generate combinations.")
        return
    
    # Initialize statistics and strategies
    try:
        from french_loto_statistics import FrenchLotoStatistics
        stats = FrenchLotoStatistics(data)
        strategies = FrenchLotoStrategy(stats)
    except Exception as e:
        logger.error(f"Error initializing strategies: {str(e)}")
        return
    
    # Generate 2 combinations using Risk/Reward strategy
    logger.info("Generating combinations using Risk/Reward strategy...")
    risk_reward_combos = strategies.risk_reward_strategy(
        num_combinations=2,
        risk_level=6  # Moderate-high risk (must be integer)
    )
    
    # Generate 1 combination using Frequency Analysis strategy
    logger.info("Generating combinations using Frequency Analysis strategy...")
    frequency_combos = strategies.frequency_strategy(
        num_combinations=1,
        recent_weight=0.4  # Give some weight to recent draws
    )
    
    # Display combinations
    logger.info("\n=== RISK/REWARD STRATEGY COMBINATIONS ===")
    for i, combo in enumerate(risk_reward_combos):
        if 'numbers' in combo:
            numbers = combo['numbers']
        elif 'main_numbers' in combo:
            numbers = combo['main_numbers']
        else:
            numbers = []
            
        lucky = combo.get('lucky', combo.get('lucky_number', 0))
        score = combo.get('score', 0)
        
        logger.info(f"Combination {i+1}:")
        logger.info(f"  Main Numbers: {', '.join(map(str, numbers))}")
        logger.info(f"  Lucky Number: {lucky}")
        if score:
            logger.info(f"  Score: {score:.2f}/100")
        logger.info("")
    
    logger.info("\n=== FREQUENCY ANALYSIS STRATEGY COMBINATIONS ===")
    for i, combo in enumerate(frequency_combos):
        if 'numbers' in combo:
            numbers = combo['numbers']
        elif 'main_numbers' in combo:
            numbers = combo['main_numbers']
        else:
            numbers = []
            
        lucky = combo.get('lucky', combo.get('lucky_number', 0))
        score = combo.get('score', 0)
        
        logger.info(f"Combination {i+1}:")
        logger.info(f"  Main Numbers: {', '.join(map(str, numbers))}")
        logger.info(f"  Lucky Number: {lucky}")
        if score:
            logger.info(f"  Score: {score:.2f}/100")
        logger.info("")
    
    return risk_reward_combos, frequency_combos

if __name__ == "__main__":
    generate_combinations()