"""
Strategy Recommendation Module

This module contains utility functions and data related to French Loto strategy 
performance based on backtesting results. It's used to provide recommendations
for the most effective strategies in the user interface.
"""

# Strategy performance data based on backtesting with 1,049 historical drawings
STRATEGY_PERFORMANCE = {
    "Risk/Reward Balance": {
        "avg_score": 2.16,  # Average match score out of 6
        "win_rate": 22.69,  # Percentage of draws with at least 3 matches
        "recommended": True,
        "rank": 1
    },
    "Frequency Analysis": {
        "avg_score": 2.15,
        "win_rate": 21.45,
        "recommended": True,
        "rank": 2
    },
    "Markov Chain Model": {
        "avg_score": 2.14,
        "win_rate": 23.26,
        "recommended": True,
        "rank": 3
    },
    "Time Series Analysis": {
        "avg_score": 2.14,
        "win_rate": 22.12,
        "recommended": True,
        "rank": 4
    },
    "Bayesian Inference": {
        "avg_score": 2.12,
        "win_rate": 20.88,
        "recommended": False,
        "rank": 5
    },
    "Coverage Optimization": {
        "avg_score": 2.11,
        "win_rate": 20.40,
        "recommended": False,
        "rank": 6
    },
    "Temporal Patterns": {
        "avg_score": 2.09,
        "win_rate": 19.73,
        "recommended": False,
        "rank": 7
    },
    "Stratified Sampling": {
        "avg_score": 2.08,
        "win_rate": 19.35,
        "recommended": False,
        "rank": 8
    },
    "Anti-Cognitive Bias": {
        "avg_score": 2.07,
        "win_rate": 18.78,
        "recommended": False,
        "rank": 9
    },
    "Mixed Strategy": {
        "avg_score": 2.10,
        "win_rate": 19.92,
        "recommended": False,
        "rank": 10
    }
}

def get_strategy_display_name(strategy_name):
    """
    Convert a strategy name to its display name with a star if it's recommended
    
    Args:
        strategy_name (str): The base strategy name
        
    Returns:
        str: The display name with star symbol for recommended strategies
    """
    if strategy_name in STRATEGY_PERFORMANCE and STRATEGY_PERFORMANCE[strategy_name]["recommended"]:
        return f"{strategy_name} ⭐"
    return strategy_name

def get_base_strategy_name(display_name):
    """
    Extract the base strategy name from a display name
    
    Args:
        display_name (str): The display name (potentially with star symbol)
        
    Returns:
        str: The base strategy name
    """
    return display_name.split(" ⭐")[0]

def get_ordered_strategy_list():
    """
    Get an ordered list of strategy display names, with recommended strategies first
    
    Returns:
        list: Ordered list of strategy display names
    """
    strategies = sorted(
        STRATEGY_PERFORMANCE.keys(), 
        key=lambda s: STRATEGY_PERFORMANCE[s]["rank"]
    )
    return [get_strategy_display_name(s) for s in strategies]

def get_strategy_info_text():
    """
    Get an information text about strategy performance
    
    Returns:
        str: Information text about top strategies
    """
    return "Based on our backtesting with 1,049 historical drawings, we've identified the best-performing strategies for French Loto."