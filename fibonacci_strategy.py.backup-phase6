"""
Fibonacci Strategy Module for Euromillions
Integrates with the main Streamlit app
"""

import random
from collections import Counter
from datetime import datetime, timedelta

def get_fibonacci_numbers():
    """Get Fibonacci numbers in lottery range (1-50)"""
    fib = [1, 1]
    while fib[-1] < 50:
        fib.append(fib[-1] + fib[-2])
    
    # Remove duplicates and filter to lottery range
    fibonacci_in_range = sorted(list(set([f for f in fib if 1 <= f <= 50])))
    return fibonacci_in_range

def generate_fibonacci_combinations(strategy_variant="Mixed", num_combinations=5):
    """
    Generate Fibonacci-enhanced combinations for Euromillions
    
    Args:
        strategy_variant: Type of Fibonacci strategy
        num_combinations: Number of combinations to generate
    
    Returns:
        List of combination dictionaries
    """
    fibonacci_numbers = get_fibonacci_numbers()
    non_fibonacci = [i for i in range(1, 51) if i not in fibonacci_numbers]
    
    # May 20 successful Fibonacci numbers
    hot_fibonacci = [1, 8, 13]
    other_fibonacci = [2, 3, 5, 21, 34]
    
    # Hot stars (including May 20 winners)
    hot_stars = [2, 3, 5, 6, 8, 9, 11, 12]
    
    combinations = []
    number_usage = Counter()
    star_usage = Counter()
    
    for i in range(num_combinations):
        if strategy_variant == "Pure Fibonacci":
            # All Fibonacci numbers
            pool = fibonacci_numbers
            fib_target = 5
        elif strategy_variant == "Reverted Fibonacci":
            # Fibonacci in reverse order
            pool = fibonacci_numbers[::-1]
            fib_target = 5
        elif strategy_variant == "Mixed" or strategy_variant == "Fibonacci Enhanced":
            # Mix of Fibonacci and non-Fibonacci (like May 20 pattern)
            pool = fibonacci_numbers + non_fibonacci
            fib_target = 3
        elif strategy_variant == "Hot Fibonacci":
            # Focus on May 20 successful Fibonacci
            pool = hot_fibonacci + other_fibonacci + non_fibonacci[:10]
            fib_target = 3
        else:
            # Default to Mixed
            pool = fibonacci_numbers + non_fibonacci
            fib_target = 3
        
        # Generate numbers ensuring some Fibonacci presence
        combination_numbers = []
        fibonacci_included = 0
        
        # First, ensure we get some Fibonacci numbers
        available_fib = [n for n in fibonacci_numbers if number_usage[n] < 2]
        if available_fib and fibonacci_included < fib_target:
            # Include hot Fibonacci first
            for hot_fib in hot_fibonacci:
                if hot_fib in available_fib and len(combination_numbers) < 5:
                    combination_numbers.append(hot_fib)
                    number_usage[hot_fib] += 1
                    fibonacci_included += 1
                    available_fib.remove(hot_fib)
            
            # Fill remaining Fibonacci slots
            while len(combination_numbers) < min(fib_target, 5) and available_fib:
                num = random.choice(available_fib)
                combination_numbers.append(num)
                number_usage[num] += 1
                fibonacci_included += 1
                available_fib.remove(num)
        
        # Fill remaining slots from the pool
        remaining_slots = 5 - len(combination_numbers)
        available_pool = [n for n in pool 
                         if n not in combination_numbers and number_usage[n] < 2]
        
        while remaining_slots > 0 and available_pool:
            num = random.choice(available_pool)
            combination_numbers.append(num)
            number_usage[num] += 1
            remaining_slots -= 1
            available_pool.remove(num)
        
        # Fallback if we still need numbers
        while len(combination_numbers) < 5:
            num = random.randint(1, 50)
            if num not in combination_numbers:
                combination_numbers.append(num)
                number_usage[num] += 1
        
        combination_numbers.sort()
        
        # Generate stars with preference for hot stars
        available_stars = [s for s in hot_stars if star_usage[s] < 3]
        if len(available_stars) < 2:
            available_stars = list(range(1, 13))
        
        stars = sorted(random.sample(available_stars[:8], 2))
        for star in stars:
            star_usage[star] += 1
        
        # Calculate score based on Fibonacci content and patterns
        fib_count = len([n for n in combination_numbers if n in fibonacci_numbers])
        score = 75.0 + fib_count * 5  # Base score + Fibonacci bonus
        
        # Bonus for hot Fibonacci
        hot_fib_count = len([n for n in combination_numbers if n in hot_fibonacci])
        score += hot_fib_count * 3
        
        # Bonus for winning stars
        if 5 in stars or 6 in stars:
            score += 5
        
        combination = {
            'numbers': combination_numbers,
            'stars': stars,
            'strategy': f'Fibonacci: {strategy_variant}',
            'score': min(score, 100.0),
            'fibonacci_count': fib_count
        }
        
        combinations.append(combination)
    
    return combinations

def get_fibonacci_strategy_info():
    """Get information about Fibonacci strategies"""
    return {
        "Pure Fibonacci": "Uses only Fibonacci numbers (1, 2, 3, 5, 8, 13, 21, 34). Mathematical sequence approach.",
        "Reverted Fibonacci": "Fibonacci numbers in reverse order (34, 21, 13, 8, 5). Reversal pattern strategy.",
        "Mixed": "Combines Fibonacci with non-Fibonacci numbers. Balanced mathematical approach.",
        "Hot Fibonacci": "Prioritizes Fibonacci numbers that won on May 20 (1, 8, 13). Evidence-based selection.",
        "Fibonacci Enhanced": "Advanced mix optimizing Fibonacci patterns with winning insights. Recommended approach."
    }

def save_fibonacci_to_database(combinations, engine):
    """Save Fibonacci combinations to database"""
    import pandas as pd
    
    try:
        # Calculate target draw date
        today = datetime.now()
        days_until_friday = (4 - today.weekday()) % 7
        if days_until_friday == 0 and today.hour > 20:
            days_until_friday = 7
        next_draw_date = today + timedelta(days=days_until_friday)
        
        records = []
        for combo in combinations:
            record = {
                'numbers': str(combo['numbers']),
                'stars': str(combo['stars']),
                'strategy': combo['strategy'],
                'score': combo['score'],
                'target_draw_date': next_draw_date.date(),
                'created_at': datetime.now().date()
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        df.to_sql('generated_combinations', engine, if_exists='append', index=False)
        
        return True, len(combinations)
        
    except Exception as e:
        return False, str(e)