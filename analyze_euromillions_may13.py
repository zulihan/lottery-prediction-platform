"""
Analyze how our combinations for the May 13 Euromillions drawing performed
and generate new combinations for the next draw.
"""
import random
import numpy as np
from collections import Counter
import json
from datetime import date, datetime, timedelta

# Define the actual result of May 13 drawing
actual_result = {
    'numbers': [6, 9, 25, 37, 46],
    'stars': [6, 12]
}

# Define our previous combinations for May 13
previous_combinations = [
    {'numbers': [7, 9, 15, 19, 44], 'stars': [2, 8], 'strategy': 'Risk-Reward (Low Risk 0.20)'},
    {'numbers': [9, 15, 20, 45, 50], 'stars': [1, 2], 'strategy': 'Risk-Reward (Medium-Low Risk 0.40)'},
    {'numbers': [3, 15, 17, 31, 47], 'stars': [8, 9], 'strategy': 'Risk-Reward (Medium-High Risk 0.60)'},
    {'numbers': [17, 28, 31, 38, 44], 'stars': [1, 6], 'strategy': 'Risk-Reward (High Risk 0.80)'},
    {'numbers': [3, 8, 27, 46, 47], 'stars': [1, 12], 'strategy': 'Overdue Numbers'},
    {'numbers': [3, 9, 19, 20, 47], 'stars': [2, 8], 'strategy': 'Frequency Analysis'},
    {'numbers': [9, 16, 19, 39, 44], 'stars': [1, 9], 'strategy': 'Wheel System'},
    {'numbers': [6, 7, 23, 39, 44], 'stars': [3, 10], 'strategy': 'Hot-Cold Balance'},
    {'numbers': [6, 7, 15, 42, 44], 'stars': [8, 9], 'strategy': 'Frequency Analysis (Alt)'},
    {'numbers': [1, 9, 13, 15, 27], 'stars': [2, 8], 'strategy': 'Frequency Analysis (Low Sum)'}
]

def analyze_combination_performance(combination, actual_result):
    """
    Analyze how well a combination performed against the actual result.
    
    Args:
        combination: Dictionary with 'numbers' and 'stars'
        actual_result: Dictionary with actual 'numbers' and 'stars'
        
    Returns:
        dict: Performance metrics
    """
    # Count matching numbers and stars
    matching_numbers = set(combination['numbers']).intersection(set(actual_result['numbers']))
    matching_stars = set(combination['stars']).intersection(set(actual_result['stars']))
    
    # Calculate score
    score = len(matching_numbers) * 2 + len(matching_stars)
    
    return {
        'matching_numbers': list(matching_numbers),
        'matching_stars': list(matching_stars),
        'num_matching_numbers': len(matching_numbers),
        'num_matching_stars': len(matching_stars),
        'score': score
    }

def analyze_all_combinations(combinations, actual_result):
    """
    Analyze the performance of all combinations.
    
    Returns:
        list: Performance data for each combination
    """
    results = []
    
    for combo in combinations:
        performance = analyze_combination_performance(combo, actual_result)
        results.append({
            'combination': combo,
            'performance': performance
        })
    
    # Sort by score (descending)
    results.sort(key=lambda x: x['performance']['score'], reverse=True)
    
    return results

def analyze_what_worked(analysis_results):
    """
    Analyze what strategies and approaches worked best.
    
    Args:
        analysis_results: List of analyzed combinations
        
    Returns:
        dict: Analysis of what worked
    """
    # Strategy performance
    strategy_performance = {}
    
    for result in analysis_results:
        strategy = result['combination']['strategy']
        
        if strategy not in strategy_performance:
            strategy_performance[strategy] = {
                'count': 0,
                'total_score': 0,
                'max_score': 0,
                'numbers_hit': [],
                'stars_hit': []
            }
        
        perf = strategy_performance[strategy]
        perf['count'] += 1
        perf['total_score'] += result['performance']['score']
        perf['max_score'] = max(perf['max_score'], result['performance']['score'])
        perf['numbers_hit'].extend(result['performance']['matching_numbers'])
        perf['stars_hit'].extend(result['performance']['matching_stars'])
    
    # Calculate average scores
    for strategy, perf in strategy_performance.items():
        if perf['count'] > 0:
            perf['avg_score'] = perf['total_score'] / perf['count']
        else:
            perf['avg_score'] = 0
        
        # Calculate most hit numbers and stars
        perf['numbers_hit_freq'] = Counter(perf['numbers_hit'])
        perf['stars_hit_freq'] = Counter(perf['stars_hit'])
    
    # Identify which numbers and stars were hit most often across all strategies
    all_hit_numbers = []
    all_hit_stars = []
    
    for result in analysis_results:
        all_hit_numbers.extend(result['performance']['matching_numbers'])
        all_hit_stars.extend(result['performance']['matching_stars'])
    
    number_hit_freq = Counter(all_hit_numbers)
    star_hit_freq = Counter(all_hit_stars)
    
    # Calculate average number of hits
    total_number_hits = sum(len(r['performance']['matching_numbers']) for r in analysis_results)
    total_star_hits = sum(len(r['performance']['matching_stars']) for r in analysis_results)
    
    avg_number_hits = total_number_hits / len(analysis_results) if analysis_results else 0
    avg_star_hits = total_star_hits / len(analysis_results) if analysis_results else 0
    
    return {
        'strategy_performance': strategy_performance,
        'number_hit_freq': number_hit_freq,
        'star_hit_freq': star_hit_freq,
        'avg_number_hits': avg_number_hits,
        'avg_star_hits': avg_star_hits
    }

def identify_improvements(analysis_results, actual_result):
    """
    Identify how we could have improved our combinations.
    
    Args:
        analysis_results: List of analyzed combinations
        actual_result: Dictionary with actual 'numbers' and 'stars'
        
    Returns:
        dict: Improvement recommendations
    """
    # Check if any combination had 4+ numbers
    best_result = analysis_results[0]
    best_score = best_result['performance']['score']
    max_number_matches = max(r['performance']['num_matching_numbers'] for r in analysis_results)
    max_star_matches = max(r['performance']['num_matching_stars'] for r in analysis_results)
    
    # Identify missing numbers and stars
    all_selected_numbers = set()
    all_selected_stars = set()
    
    for result in analysis_results:
        all_selected_numbers.update(result['combination']['numbers'])
        all_selected_stars.update(result['combination']['stars'])
    
    missing_numbers = [n for n in actual_result['numbers'] if n not in all_selected_numbers]
    missing_stars = [s for s in actual_result['stars'] if s not in all_selected_stars]
    
    # Check which combinations came closest to the actual result
    closest_to_actual = []
    
    for result in analysis_results:
        if result['performance']['num_matching_numbers'] == max_number_matches:
            closest_to_actual.append(result)
    
    # Check patterns in the actual result
    actual_numbers = actual_result['numbers']
    actual_stars = actual_result['stars']
    
    # Check even/odd distribution
    even_numbers = len([n for n in actual_numbers if n % 2 == 0])
    odd_numbers = 5 - even_numbers
    
    # Check number ranges
    low_range = len([n for n in actual_numbers if 1 <= n <= 17])
    mid_range = len([n for n in actual_numbers if 18 <= n <= 34])
    high_range = len([n for n in actual_numbers if 35 <= n <= 50])
    
    # Check sum
    actual_sum = sum(actual_numbers)
    
    # Our best performing combinations
    best_combinations = analysis_results[:2]
    
    # Identify what our combinations missed
    combination_weaknesses = []
    
    # Check if our combinations matched the even/odd pattern
    avg_even_count = sum(len([n for n in r['combination']['numbers'] if n % 2 == 0]) 
                         for r in analysis_results) / len(analysis_results)
    
    if abs(avg_even_count - even_numbers) > 1:
        combination_weaknesses.append(
            f"Combinations had on average {avg_even_count:.1f} even numbers while actual had {even_numbers}"
        )
    
    # Check if our combinations matched the range distribution
    avg_low = sum(len([n for n in r['combination']['numbers'] if 1 <= n <= 17]) 
                  for r in analysis_results) / len(analysis_results)
    avg_mid = sum(len([n for n in r['combination']['numbers'] if 18 <= n <= 34]) 
                  for r in analysis_results) / len(analysis_results)
    avg_high = sum(len([n for n in r['combination']['numbers'] if 35 <= n <= 50]) 
                   for r in analysis_results) / len(analysis_results)
    
    if abs(avg_low - low_range) > 0.5:
        combination_weaknesses.append(
            f"Combinations had on average {avg_low:.1f} low range numbers while actual had {low_range}"
        )
    if abs(avg_high - high_range) > 0.5:
        combination_weaknesses.append(
            f"Combinations had on average {avg_high:.1f} high range numbers while actual had {high_range}"
        )
    
    # Check sum ranges
    avg_sum = sum(sum(r['combination']['numbers']) for r in analysis_results) / len(analysis_results)
    
    if abs(avg_sum - actual_sum) > 20:
        combination_weaknesses.append(
            f"Combinations had an average sum of {avg_sum:.1f} while actual had {actual_sum}"
        )
    
    return {
        'best_score': best_score,
        'max_number_matches': max_number_matches,
        'max_star_matches': max_star_matches,
        'missing_numbers': missing_numbers,
        'missing_stars': missing_stars,
        'closest_combinations': closest_to_actual,
        'actual_patterns': {
            'even_odd': [even_numbers, odd_numbers],
            'ranges': [low_range, mid_range, high_range],
            'sum': actual_sum
        },
        'combination_weaknesses': combination_weaknesses
    }

def generate_new_combinations(analysis_results, what_worked, improvements, num_combinations=10):
    """
    Generate new combinations based on analysis of previous performance.
    
    Args:
        analysis_results: List of analyzed combinations
        what_worked: Dictionary with analysis of what worked
        improvements: Dictionary with improvement recommendations
        num_combinations: Number of combinations to generate
        
    Returns:
        list: New combinations
    """
    # Best strategies based on performance
    strategy_performance = what_worked['strategy_performance']
    
    # Sort strategies by average score
    sorted_strategies = sorted(strategy_performance.items(), 
                              key=lambda x: x[1]['avg_score'], 
                              reverse=True)
    
    top_strategies = [s[0] for s in sorted_strategies[:3]]
    
    # Get actual patterns to match
    actual_patterns = improvements['actual_patterns']
    
    # New combinations to generate
    new_combinations = []
    
    # Generate combinations for each top strategy
    combinations_per_strategy = max(1, num_combinations // len(top_strategies))
    
    for strategy in top_strategies:
        for i in range(combinations_per_strategy):
            # Strategy-specific parameters
            if "Risk-Reward" in strategy:
                if "Low Risk" in strategy:
                    risk_level = 0.2
                elif "Medium-Low Risk" in strategy:
                    risk_level = 0.4
                elif "Medium-High Risk" in strategy:
                    risk_level = 0.6
                elif "High Risk" in strategy:
                    risk_level = 0.8
                else:
                    risk_level = 0.5
                
                combo = generate_risk_reward_combination(risk_level, actual_patterns)
                combo['strategy'] = f"Risk-Reward ({risk_level:.1f})"
            
            elif "Frequency Analysis" in strategy:
                combo = generate_frequency_analysis_combination(actual_patterns)
                combo['strategy'] = "Frequency Analysis"
                
                if "Alt" in strategy:
                    combo['strategy'] += " (Alt)"
                elif "Low Sum" in strategy:
                    combo['strategy'] += " (Low Sum)"
            
            elif "Overdue Numbers" in strategy:
                combo = generate_overdue_combination(actual_patterns)
                combo['strategy'] = "Overdue Numbers"
            
            elif "Hot-Cold" in strategy:
                combo = generate_hot_cold_combination(actual_patterns)
                combo['strategy'] = "Hot-Cold Balance"
            
            elif "Wheel" in strategy:
                combo = generate_wheel_combination(actual_patterns)
                combo['strategy'] = "Wheel System"
            
            else:
                # Default to balanced strategy
                combo = generate_balanced_combination(actual_patterns)
                combo['strategy'] = "Balanced Strategy"
            
            new_combinations.append(combo)
    
    # Fill any remaining slots with balanced combinations
    while len(new_combinations) < num_combinations:
        combo = generate_balanced_combination(actual_patterns)
        combo['strategy'] = "Balanced Strategy"
        new_combinations.append(combo)
    
    # Ensure uniqueness
    unique_combinations = ensure_unique_combinations(new_combinations)
    
    return unique_combinations

def generate_risk_reward_combination(risk_level, actual_patterns):
    """
    Generate a Risk-Reward combination with the specified risk level.
    
    Args:
        risk_level: Risk level (0-1), higher means more risky numbers
        actual_patterns: Patterns from the actual result to match
        
    Returns:
        dict: Generated combination
    """
    # Define safe and risky numbers based on historical frequency
    safe_numbers = [3, 9, 19, 21, 27, 37, 44]
    risky_numbers = [5, 7, 11, 25, 31, 33, 38, 45, 46, 50]
    
    # Define safe and risky stars
    safe_stars = [2, 3, 8, 9]
    risky_stars = [1, 4, 6, 7, 10, 11, 12]
    
    # Determine number of safe vs risky numbers based on risk level
    num_safe = int(5 * (1 - risk_level))
    num_risky = 5 - num_safe
    
    # Account for actual patterns - adjust for even/odd distribution
    even_odd = actual_patterns['even_odd']
    target_even = even_odd[0]
    
    # Categorize safe and risky by even/odd
    safe_even = [n for n in safe_numbers if n % 2 == 0]
    safe_odd = [n for n in safe_numbers if n % 2 == 1]
    risky_even = [n for n in risky_numbers if n % 2 == 0]
    risky_odd = [n for n in risky_numbers if n % 2 == 1]
    
    # Try to match actual even/odd distribution
    selected_numbers = []
    
    # Select safe numbers
    safe_even_needed = min(num_safe, target_even)
    safe_odd_needed = num_safe - safe_even_needed
    
    if safe_even and safe_even_needed > 0:
        selected_numbers.extend(random.sample(safe_even, min(safe_even_needed, len(safe_even))))
    
    if safe_odd and safe_odd_needed > 0:
        selected_numbers.extend(random.sample(safe_odd, min(safe_odd_needed, len(safe_odd))))
    
    # If we couldn't get enough safe numbers with the right distribution,
    # just get any safe numbers
    remaining_safe = num_safe - len(selected_numbers)
    if remaining_safe > 0:
        available_safe = [n for n in safe_numbers if n not in selected_numbers]
        if available_safe:
            selected_numbers.extend(random.sample(available_safe, min(remaining_safe, len(available_safe))))
    
    # Select risky numbers
    risky_even_needed = target_even - len([n for n in selected_numbers if n % 2 == 0])
    risky_odd_needed = num_risky - risky_even_needed
    
    if risky_even and risky_even_needed > 0:
        selected_numbers.extend(random.sample(risky_even, min(risky_even_needed, len(risky_even))))
    
    if risky_odd and risky_odd_needed > 0:
        selected_numbers.extend(random.sample(risky_odd, min(risky_odd_needed, len(risky_odd))))
    
    # If we couldn't get enough risky numbers with the right distribution,
    # just get any risky numbers
    remaining_risky = num_risky - (len(selected_numbers) - (num_safe - remaining_safe))
    if remaining_risky > 0:
        available_risky = [n for n in risky_numbers if n not in selected_numbers]
        if available_risky:
            selected_numbers.extend(random.sample(available_risky, min(remaining_risky, len(available_risky))))
    
    # If we still need more numbers, add random ones
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 51) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # Select stars (1 safe, 1 risky) - don't try to match patterns for stars
    # as they're too variable
    selected_stars = []
    
    if safe_stars:
        selected_stars.append(random.choice(safe_stars))
    
    if risky_stars:
        available_risky_stars = [s for s in risky_stars if s not in selected_stars]
        if available_risky_stars:
            selected_stars.append(random.choice(available_risky_stars))
    
    # If we need more stars, add random ones
    while len(selected_stars) < 2:
        available = [s for s in range(1, 13) if s not in selected_stars]
        selected_stars.append(random.choice(available))
    
    return {
        'numbers': sorted(selected_numbers),
        'stars': sorted(selected_stars)
    }

def generate_frequency_analysis_combination(actual_patterns):
    """
    Generate a combination based on frequency analysis.
    
    Args:
        actual_patterns: Patterns from the actual result to match
        
    Returns:
        dict: Generated combination
    """
    # Define frequency tiers based on historical data
    high_freq = [5, 9, 15, 19, 20, 23, 27, 37, 44, 50]
    medium_freq = [6, 8, 11, 17, 21, 25, 29, 33, 39, 42, 46, 48]
    low_freq = [1, 2, 3, 7, 10, 13, 14, 16, 22, 24, 26, 28, 30, 34, 35, 38, 40, 41, 43, 45, 47, 49]
    
    # Star frequency
    high_freq_stars = [2, 3, 8, 9]
    low_freq_stars = [1, 4, 5, 6, 7, 10, 11, 12]
    
    # Account for actual patterns - adjust for even/odd distribution
    even_odd = actual_patterns['even_odd']
    target_even = even_odd[0]
    
    # Define distribution based on frequency
    num_high = random.randint(2, 3)
    num_medium = random.randint(1, 2)
    num_low = 5 - num_high - num_medium
    
    # Categorize by even/odd
    high_even = [n for n in high_freq if n % 2 == 0]
    high_odd = [n for n in high_freq if n % 2 == 1]
    medium_even = [n for n in medium_freq if n % 2 == 0]
    medium_odd = [n for n in medium_freq if n % 2 == 1]
    low_even = [n for n in low_freq if n % 2 == 0]
    low_odd = [n for n in low_freq if n % 2 == 1]
    
    # Try to match actual even/odd distribution
    selected_numbers = []
    
    # Select high frequency numbers
    high_even_needed = min(num_high, target_even)
    high_odd_needed = num_high - high_even_needed
    
    if high_even and high_even_needed > 0:
        selected_numbers.extend(random.sample(high_even, min(high_even_needed, len(high_even))))
    
    if high_odd and high_odd_needed > 0:
        selected_numbers.extend(random.sample(high_odd, min(high_odd_needed, len(high_odd))))
    
    # If we couldn't get enough high frequency numbers with the right distribution,
    # just get any high frequency numbers
    remaining_high = num_high - len(selected_numbers)
    if remaining_high > 0:
        available_high = [n for n in high_freq if n not in selected_numbers]
        if available_high:
            selected_numbers.extend(random.sample(available_high, min(remaining_high, len(available_high))))
    
    # Select medium frequency numbers
    current_even = len([n for n in selected_numbers if n % 2 == 0])
    medium_even_needed = min(num_medium, target_even - current_even)
    medium_odd_needed = num_medium - medium_even_needed
    
    if medium_even and medium_even_needed > 0:
        selected_numbers.extend(random.sample(medium_even, min(medium_even_needed, len(medium_even))))
    
    if medium_odd and medium_odd_needed > 0:
        selected_numbers.extend(random.sample(medium_odd, min(medium_odd_needed, len(medium_odd))))
    
    # If we couldn't get enough medium frequency numbers with the right distribution,
    # just get any medium frequency numbers
    remaining_medium = num_medium - (len(selected_numbers) - (num_high - remaining_high))
    if remaining_medium > 0:
        available_medium = [n for n in medium_freq if n not in selected_numbers]
        if available_medium:
            selected_numbers.extend(random.sample(available_medium, min(remaining_medium, len(available_medium))))
    
    # Select low frequency numbers
    current_even = len([n for n in selected_numbers if n % 2 == 0])
    low_even_needed = target_even - current_even
    low_odd_needed = num_low - low_even_needed
    
    if low_even and low_even_needed > 0:
        selected_numbers.extend(random.sample(low_even, min(low_even_needed, len(low_even))))
    
    if low_odd and low_odd_needed > 0:
        selected_numbers.extend(random.sample(low_odd, min(low_odd_needed, len(low_odd))))
    
    # If we couldn't get enough low frequency numbers with the right distribution,
    # just get any low frequency numbers
    remaining_low = num_low - (len(selected_numbers) - (num_high - remaining_high + num_medium - remaining_medium))
    if remaining_low > 0:
        available_low = [n for n in low_freq if n not in selected_numbers]
        if available_low:
            selected_numbers.extend(random.sample(available_low, min(remaining_low, len(available_low))))
    
    # If we still need more numbers, add random ones
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 51) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # Select 1 high frequency star and 1 low frequency star
    selected_stars = []
    
    if high_freq_stars:
        selected_stars.append(random.choice(high_freq_stars))
    
    if low_freq_stars:
        available_low_stars = [s for s in low_freq_stars if s not in selected_stars]
        if available_low_stars:
            selected_stars.append(random.choice(available_low_stars))
    
    # If we need more stars, add random ones
    while len(selected_stars) < 2:
        available = [s for s in range(1, 13) if s not in selected_stars]
        selected_stars.append(random.choice(available))
    
    return {
        'numbers': sorted(selected_numbers),
        'stars': sorted(selected_stars)
    }

def generate_overdue_combination(actual_patterns):
    """
    Generate a combination focusing on overdue numbers.
    
    Args:
        actual_patterns: Patterns from the actual result to match
        
    Returns:
        dict: Generated combination
    """
    # Define overdue numbers (those that haven't appeared in a long time)
    # In a real implementation, this would be calculated from historical data
    overdue_numbers = [2, 11, 13, 14, 29, 35, 40, 41, 45, 47, 49]
    regular_numbers = [n for n in range(1, 51) if n not in overdue_numbers]
    
    # Star frequency
    overdue_stars = [4, 5, 7, 10, 11]
    regular_stars = [s for s in range(1, 13) if s not in overdue_stars]
    
    # Account for actual patterns - adjust for even/odd distribution
    even_odd = actual_patterns['even_odd']
    target_even = even_odd[0]
    
    # Mix overdue and regular numbers
    num_overdue = random.randint(2, 3)
    num_regular = 5 - num_overdue
    
    # Categorize by even/odd
    overdue_even = [n for n in overdue_numbers if n % 2 == 0]
    overdue_odd = [n for n in overdue_numbers if n % 2 == 1]
    regular_even = [n for n in regular_numbers if n % 2 == 0]
    regular_odd = [n for n in regular_numbers if n % 2 == 1]
    
    # Try to match actual even/odd distribution
    selected_numbers = []
    
    # Select overdue numbers
    overdue_even_needed = min(num_overdue, target_even)
    overdue_odd_needed = num_overdue - overdue_even_needed
    
    if overdue_even and overdue_even_needed > 0:
        selected_numbers.extend(random.sample(overdue_even, min(overdue_even_needed, len(overdue_even))))
    
    if overdue_odd and overdue_odd_needed > 0:
        selected_numbers.extend(random.sample(overdue_odd, min(overdue_odd_needed, len(overdue_odd))))
    
    # If we couldn't get enough overdue numbers with the right distribution,
    # just get any overdue numbers
    remaining_overdue = num_overdue - len(selected_numbers)
    if remaining_overdue > 0:
        available_overdue = [n for n in overdue_numbers if n not in selected_numbers]
        if available_overdue:
            selected_numbers.extend(random.sample(available_overdue, min(remaining_overdue, len(available_overdue))))
    
    # Select regular numbers
    current_even = len([n for n in selected_numbers if n % 2 == 0])
    regular_even_needed = target_even - current_even
    regular_odd_needed = num_regular - regular_even_needed
    
    if regular_even and regular_even_needed > 0:
        selected_numbers.extend(random.sample(regular_even, min(regular_even_needed, len(regular_even))))
    
    if regular_odd and regular_odd_needed > 0:
        selected_numbers.extend(random.sample(regular_odd, min(regular_odd_needed, len(regular_odd))))
    
    # If we couldn't get enough regular numbers with the right distribution,
    # just get any regular numbers
    remaining_regular = num_regular - (len(selected_numbers) - (num_overdue - remaining_overdue))
    if remaining_regular > 0:
        available_regular = [n for n in regular_numbers if n not in selected_numbers]
        if available_regular:
            selected_numbers.extend(random.sample(available_regular, min(remaining_regular, len(available_regular))))
    
    # If we still need more numbers, add random ones
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 51) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # Select 1 overdue star and 1 regular star
    selected_stars = []
    
    if overdue_stars:
        selected_stars.append(random.choice(overdue_stars))
    
    if regular_stars:
        available_regular_stars = [s for s in regular_stars if s not in selected_stars]
        if available_regular_stars:
            selected_stars.append(random.choice(available_regular_stars))
    
    # If we need more stars, add random ones
    while len(selected_stars) < 2:
        available = [s for s in range(1, 13) if s not in selected_stars]
        selected_stars.append(random.choice(available))
    
    return {
        'numbers': sorted(selected_numbers),
        'stars': sorted(selected_stars)
    }

def generate_hot_cold_combination(actual_patterns):
    """
    Generate a combination balancing hot and cold numbers.
    
    Args:
        actual_patterns: Patterns from the actual result to match
        
    Returns:
        dict: Generated combination
    """
    # Define hot (recently drawn) and cold (not recently drawn) numbers
    hot_numbers = [6, 9, 15, 19, 20, 25, 27, 37, 44, 46]
    cold_numbers = [1, 2, 3, 7, 10, 11, 13, 14, 21, 26, 28, 29, 31, 32, 33, 38, 39, 40, 41, 43, 48, 49]
    
    # Star temperature
    hot_stars = [2, 6, 8, 9, 12]
    cold_stars = [1, 3, 4, 5, 7, 10, 11]
    
    # Account for actual patterns - adjust for even/odd distribution
    even_odd = actual_patterns['even_odd']
    target_even = even_odd[0]
    
    # Balance hot and cold numbers
    num_hot = random.randint(2, 3)
    num_cold = 5 - num_hot
    
    # Categorize by even/odd
    hot_even = [n for n in hot_numbers if n % 2 == 0]
    hot_odd = [n for n in hot_numbers if n % 2 == 1]
    cold_even = [n for n in cold_numbers if n % 2 == 0]
    cold_odd = [n for n in cold_numbers if n % 2 == 1]
    
    # Try to match actual even/odd distribution
    selected_numbers = []
    
    # Select hot numbers
    hot_even_needed = min(num_hot, target_even)
    hot_odd_needed = num_hot - hot_even_needed
    
    if hot_even and hot_even_needed > 0:
        selected_numbers.extend(random.sample(hot_even, min(hot_even_needed, len(hot_even))))
    
    if hot_odd and hot_odd_needed > 0:
        selected_numbers.extend(random.sample(hot_odd, min(hot_odd_needed, len(hot_odd))))
    
    # If we couldn't get enough hot numbers with the right distribution,
    # just get any hot numbers
    remaining_hot = num_hot - len(selected_numbers)
    if remaining_hot > 0:
        available_hot = [n for n in hot_numbers if n not in selected_numbers]
        if available_hot:
            selected_numbers.extend(random.sample(available_hot, min(remaining_hot, len(available_hot))))
    
    # Select cold numbers
    current_even = len([n for n in selected_numbers if n % 2 == 0])
    cold_even_needed = target_even - current_even
    cold_odd_needed = num_cold - cold_even_needed
    
    if cold_even and cold_even_needed > 0:
        selected_numbers.extend(random.sample(cold_even, min(cold_even_needed, len(cold_even))))
    
    if cold_odd and cold_odd_needed > 0:
        selected_numbers.extend(random.sample(cold_odd, min(cold_odd_needed, len(cold_odd))))
    
    # If we couldn't get enough cold numbers with the right distribution,
    # just get any cold numbers
    remaining_cold = num_cold - (len(selected_numbers) - (num_hot - remaining_hot))
    if remaining_cold > 0:
        available_cold = [n for n in cold_numbers if n not in selected_numbers]
        if available_cold:
            selected_numbers.extend(random.sample(available_cold, min(remaining_cold, len(available_cold))))
    
    # If we still need more numbers, add random ones
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 51) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # Select 1 hot star and 1 cold star
    selected_stars = []
    
    if hot_stars:
        selected_stars.append(random.choice(hot_stars))
    
    if cold_stars:
        available_cold_stars = [s for s in cold_stars if s not in selected_stars]
        if available_cold_stars:
            selected_stars.append(random.choice(available_cold_stars))
    
    # If we need more stars, add random ones
    while len(selected_stars) < 2:
        available = [s for s in range(1, 13) if s not in selected_stars]
        selected_stars.append(random.choice(available))
    
    return {
        'numbers': sorted(selected_numbers),
        'stars': sorted(selected_stars)
    }

def generate_wheel_combination(actual_patterns):
    """
    Generate a combination using a wheel system.
    
    Args:
        actual_patterns: Patterns from the actual result to match
        
    Returns:
        dict: Generated combination
    """
    # Define core numbers (frequently appearing)
    core_numbers = [6, 9, 15, 19, 20, 25, 27, 37, 44, 46]
    
    # Define supplementary numbers (less frequently appearing)
    supplementary_numbers = [n for n in range(1, 51) if n not in core_numbers]
    
    # Star pools
    core_stars = [2, 6, 8, 9, 12]
    supplementary_stars = [s for s in range(1, 13) if s not in core_stars]
    
    # Account for actual patterns - adjust for even/odd distribution
    even_odd = actual_patterns['even_odd']
    target_even = even_odd[0]
    
    # Select 3 core numbers and 2 supplementary numbers
    num_core = 3
    num_supplementary = 5 - num_core
    
    # Categorize by even/odd
    core_even = [n for n in core_numbers if n % 2 == 0]
    core_odd = [n for n in core_numbers if n % 2 == 1]
    supplementary_even = [n for n in supplementary_numbers if n % 2 == 0]
    supplementary_odd = [n for n in supplementary_numbers if n % 2 == 1]
    
    # Try to match actual even/odd distribution
    selected_numbers = []
    
    # Select core numbers
    core_even_needed = min(num_core, target_even)
    core_odd_needed = num_core - core_even_needed
    
    if core_even and core_even_needed > 0:
        selected_numbers.extend(random.sample(core_even, min(core_even_needed, len(core_even))))
    
    if core_odd and core_odd_needed > 0:
        selected_numbers.extend(random.sample(core_odd, min(core_odd_needed, len(core_odd))))
    
    # If we couldn't get enough core numbers with the right distribution,
    # just get any core numbers
    remaining_core = num_core - len(selected_numbers)
    if remaining_core > 0:
        available_core = [n for n in core_numbers if n not in selected_numbers]
        if available_core:
            selected_numbers.extend(random.sample(available_core, min(remaining_core, len(available_core))))
    
    # Select supplementary numbers
    current_even = len([n for n in selected_numbers if n % 2 == 0])
    supplementary_even_needed = target_even - current_even
    supplementary_odd_needed = num_supplementary - supplementary_even_needed
    
    if supplementary_even and supplementary_even_needed > 0:
        selected_numbers.extend(random.sample(supplementary_even, min(supplementary_even_needed, len(supplementary_even))))
    
    if supplementary_odd and supplementary_odd_needed > 0:
        selected_numbers.extend(random.sample(supplementary_odd, min(supplementary_odd_needed, len(supplementary_odd))))
    
    # If we couldn't get enough supplementary numbers with the right distribution,
    # just get any supplementary numbers
    remaining_supplementary = num_supplementary - (len(selected_numbers) - (num_core - remaining_core))
    if remaining_supplementary > 0:
        available_supplementary = [n for n in supplementary_numbers if n not in selected_numbers]
        if available_supplementary:
            selected_numbers.extend(random.sample(available_supplementary, min(remaining_supplementary, len(available_supplementary))))
    
    # If we still need more numbers, add random ones
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 51) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # Select 1 core star and 1 supplementary star
    selected_stars = []
    
    if core_stars:
        selected_stars.append(random.choice(core_stars))
    
    if supplementary_stars:
        available_supplementary_stars = [s for s in supplementary_stars if s not in selected_stars]
        if available_supplementary_stars:
            selected_stars.append(random.choice(available_supplementary_stars))
    
    # If we need more stars, add random ones
    while len(selected_stars) < 2:
        available = [s for s in range(1, 13) if s not in selected_stars]
        selected_stars.append(random.choice(available))
    
    return {
        'numbers': sorted(selected_numbers),
        'stars': sorted(selected_stars)
    }

def generate_balanced_combination(actual_patterns):
    """
    Generate a balanced combination that matches actual patterns.
    
    Args:
        actual_patterns: Patterns from the actual result to match
        
    Returns:
        dict: Generated combination
    """
    # Account for actual patterns
    even_odd = actual_patterns['even_odd']
    ranges = actual_patterns['ranges']
    
    target_even = even_odd[0]
    target_odd = even_odd[1]
    
    target_low = ranges[0]
    target_mid = ranges[1]
    target_high = ranges[2]
    
    # Generate a balanced combination
    # First determine how many numbers to select from each range
    low_range = list(range(1, 18))
    mid_range = list(range(18, 35))
    high_range = list(range(35, 51))
    
    # Determine how many even and odd numbers to select
    num_even = target_even
    num_odd = 5 - num_even
    
    # Determine how many numbers to select from each range
    num_low = target_low
    num_mid = target_mid
    num_high = 5 - num_low - num_mid
    
    # Categorize by even/odd and range
    low_even = [n for n in low_range if n % 2 == 0]
    low_odd = [n for n in low_range if n % 2 == 1]
    mid_even = [n for n in mid_range if n % 2 == 0]
    mid_odd = [n for n in mid_range if n % 2 == 1]
    high_even = [n for n in high_range if n % 2 == 0]
    high_odd = [n for n in high_range if n % 2 == 1]
    
    # Try to match both even/odd and range distributions
    selected_numbers = []
    
    # Select low range numbers
    low_even_needed = min(num_low, num_even)
    low_odd_needed = num_low - low_even_needed
    
    if low_even and low_even_needed > 0:
        selected_numbers.extend(random.sample(low_even, min(low_even_needed, len(low_even))))
    
    if low_odd and low_odd_needed > 0:
        selected_numbers.extend(random.sample(low_odd, min(low_odd_needed, len(low_odd))))
    
    # If we couldn't get enough low range numbers with the right distribution,
    # just get any low range numbers
    remaining_low = num_low - len(selected_numbers)
    if remaining_low > 0:
        available_low = [n for n in low_range if n not in selected_numbers]
        if available_low:
            selected_numbers.extend(random.sample(available_low, min(remaining_low, len(available_low))))
    
    # Update counts
    current_even = len([n for n in selected_numbers if n % 2 == 0])
    current_odd = len(selected_numbers) - current_even
    
    # Select mid range numbers
    mid_even_needed = min(num_mid, num_even - current_even)
    mid_odd_needed = num_mid - mid_even_needed
    
    if mid_even and mid_even_needed > 0:
        selected_numbers.extend(random.sample(mid_even, min(mid_even_needed, len(mid_even))))
    
    if mid_odd and mid_odd_needed > 0:
        selected_numbers.extend(random.sample(mid_odd, min(mid_odd_needed, len(mid_odd))))
    
    # If we couldn't get enough mid range numbers with the right distribution,
    # just get any mid range numbers
    remaining_mid = num_mid - (len(selected_numbers) - (num_low - remaining_low))
    if remaining_mid > 0:
        available_mid = [n for n in mid_range if n not in selected_numbers]
        if available_mid:
            selected_numbers.extend(random.sample(available_mid, min(remaining_mid, len(available_mid))))
    
    # Update counts
    current_even = len([n for n in selected_numbers if n % 2 == 0])
    current_odd = len(selected_numbers) - current_even
    
    # Select high range numbers
    high_even_needed = num_even - current_even
    high_odd_needed = num_odd - current_odd
    
    if high_even and high_even_needed > 0:
        selected_numbers.extend(random.sample(high_even, min(high_even_needed, len(high_even))))
    
    if high_odd and high_odd_needed > 0:
        selected_numbers.extend(random.sample(high_odd, min(high_odd_needed, len(high_odd))))
    
    # If we couldn't get the right distribution, just fill the remaining slots
    while len(selected_numbers) < 5:
        available = [n for n in range(1, 51) if n not in selected_numbers]
        selected_numbers.append(random.choice(available))
    
    # Select stars
    selected_stars = []
    
    # Balance between high and low stars
    low_stars = list(range(1, 7))
    high_stars = list(range(7, 13))
    
    selected_stars.append(random.choice(low_stars))
    selected_stars.append(random.choice(high_stars))
    
    # Ensure uniqueness
    if selected_stars[0] == selected_stars[1]:
        available = [s for s in range(1, 13) if s != selected_stars[0]]
        selected_stars[1] = random.choice(available)
    
    return {
        'numbers': sorted(selected_numbers),
        'stars': sorted(selected_stars)
    }

def ensure_unique_combinations(combinations):
    """
    Ensure all combinations are unique.
    
    Args:
        combinations: List of combination dictionaries
        
    Returns:
        list: List of unique combinations
    """
    # Extract number and star sets
    number_sets = []
    star_sets = []
    
    for combo in combinations:
        number_sets.append(frozenset(combo['numbers']))
        star_sets.append(frozenset(combo['stars']))
    
    # Check for duplicates
    for i in range(len(combinations)):
        # Check if this combination is a duplicate of any previous one
        for j in range(i):
            if number_sets[i] == number_sets[j] and star_sets[i] == star_sets[j]:
                # Found a duplicate, modify it
                combo = combinations[i]
                
                # Replace one number
                numbers = list(combo['numbers'])
                to_replace = random.choice(numbers)
                available = [n for n in range(1, 51) if n not in numbers]
                
                if available:
                    new_number = random.choice(available)
                    numbers[numbers.index(to_replace)] = new_number
                    combo['numbers'] = sorted(numbers)
                    
                    # Update the set
                    number_sets[i] = frozenset(combo['numbers'])
                
                # If there's still a duplicate, replace a star too
                if number_sets[i] == number_sets[j] and star_sets[i] == star_sets[j]:
                    stars = list(combo['stars'])
                    to_replace = random.choice(stars)
                    available = [s for s in range(1, 13) if s not in stars]
                    
                    if available:
                        new_star = random.choice(available)
                        stars[stars.index(to_replace)] = new_star
                        combo['stars'] = sorted(stars)
                        
                        # Update the set
                        star_sets[i] = frozenset(combo['stars'])
    
    return combinations

def main():
    """Analyze previous combinations and generate new ones for the next Euromillions draw"""
    print("Analyzing previous combinations for May 13, 2025 Euromillions...")
    
    # Analyze the performance of previous combinations
    analysis_results = analyze_all_combinations(previous_combinations, actual_result)
    
    # Print the results
    print("\nPerformance of previous combinations:")
    for i, result in enumerate(analysis_results):
        combo = result['combination']
        perf = result['performance']
        
        print(f"{i+1}. Strategy: {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']}, Stars: {combo['stars']}")
        print(f"   Matching numbers: {perf['matching_numbers']} ({perf['num_matching_numbers']}/5)")
        print(f"   Matching stars: {perf['matching_stars']} ({perf['num_matching_stars']}/2)")
        print(f"   Score: {perf['score']}")
    
    # Analyze what worked
    what_worked = analyze_what_worked(analysis_results)
    
    print("\nStrategy Performance:")
    for strategy, perf in sorted(what_worked['strategy_performance'].items(), 
                                key=lambda x: x[1]['avg_score'], 
                                reverse=True):
        print(f"{strategy}: Avg score: {perf['avg_score']:.2f}, Max score: {perf['max_score']}")
    
    print("\nNumber Hit Frequencies:")
    for num, freq in what_worked['number_hit_freq'].most_common():
        print(f"Number {num}: {freq} hits")
    
    print("\nStar Hit Frequencies:")
    for star, freq in what_worked['star_hit_freq'].most_common():
        print(f"Star {star}: {freq} hits")
    
    # Identify potential improvements
    improvements = identify_improvements(analysis_results, actual_result)
    
    print("\nImprovement Recommendations:")
    print(f"Best score: {improvements['best_score']}")
    print(f"Max number matches: {improvements['max_number_matches']}/5")
    print(f"Max star matches: {improvements['max_star_matches']}/2")
    
    if improvements['missing_numbers']:
        print(f"Missing numbers (not in any combination): {improvements['missing_numbers']}")
    
    if improvements['missing_stars']:
        print(f"Missing stars (not in any combination): {improvements['missing_stars']}")
    
    print("\nActual Result Patterns:")
    print(f"Even/Odd: {improvements['actual_patterns']['even_odd']}")
    print(f"Ranges: {improvements['actual_patterns']['ranges']}")
    print(f"Sum: {improvements['actual_patterns']['sum']}")
    
    if improvements['combination_weaknesses']:
        print("\nCombination Weaknesses:")
        for weakness in improvements['combination_weaknesses']:
            print(f"- {weakness}")
    
    # Generate new combinations for the next draw
    print("\nGenerating new combinations for the next Euromillions draw...")
    new_combinations = generate_new_combinations(
        analysis_results, what_worked, improvements, num_combinations=10
    )
    
    # Print the new combinations
    print("\n10 Optimized Combinations for the Next Euromillions Drawing (May 20, 2025):")
    for i, combo in enumerate(new_combinations):
        print(f"{i+1}. Strategy: {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']}")
        print(f"   Stars: {combo['stars']}")
        print()
    
    return new_combinations

if __name__ == "__main__":
    main()