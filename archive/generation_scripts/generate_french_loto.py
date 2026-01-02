import os
import sys
import argparse
from datetime import datetime, date, timedelta
from french_loto_strategy import FrenchLotoStrategy

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Generate French Loto combinations')
    parser.add_argument('--count', '-c', type=int, default=10, 
                        help='Number of combinations to generate (default: 10)')
    parser.add_argument('--target-date', '-d', type=str, default=None,
                        help='Target draw date (YYYY-MM-DD). Default is next draw date.')
    parser.add_argument('--save', '-s', action='store_true', 
                        help='Save combinations to database')
    parser.add_argument('--strategies', '-t', action='store_true',
                        help='Use multiple strategies (default: True)')
    parser.add_argument('--format', '-f', choices=['table', 'list'], default='table',
                        help='Output format (default: table)')
    return parser.parse_args()

def format_as_table(combinations):
    """Format combinations as a table"""
    # Print header
    print(f"{'No.':<4}{'Strategy':<25}{'Main Numbers':<25}{'Lucky':<6}{'Score':<7}")
    print("-" * 70)
    
    # Print each combination
    for i, (numbers, lucky, score, strategy) in enumerate(combinations):
        numbers_str = ', '.join(str(n) for n in numbers)
        print(f"{i+1:<4}{strategy[:22]+'...' if len(strategy) > 25 else strategy:<25}"
              f"{numbers_str:<25}{lucky:<6}{score:<7.2f}")

def format_as_list(combinations):
    """Format combinations as a detailed list"""
    for i, (numbers, lucky, score, strategy) in enumerate(combinations):
        print(f"Combination {i+1}:")
        print(f"  Strategy: {strategy}")
        print(f"  Main Numbers: {', '.join(map(str, numbers))}")
        print(f"  Lucky Number: {lucky}")
        print(f"  Score: {score:.2f}\n")

def get_next_draw_date():
    """Calculate the next French Loto draw date (Monday or Wednesday)"""
    today = date.today()
    days_to_monday = (0 - today.weekday()) % 7
    days_to_wednesday = (2 - today.weekday()) % 7
    
    if days_to_monday == 0:
        # If today is Monday, use next Wednesday
        next_draw = today + timedelta(days=days_to_wednesday)
    elif days_to_wednesday == 0:
        # If today is Wednesday, use next Monday
        next_draw = today + timedelta(days=days_to_monday + 7)
    else:
        # Use next closest draw day
        if days_to_monday < days_to_wednesday:
            next_draw = today + timedelta(days=days_to_monday)
        else:
            next_draw = today + timedelta(days=days_to_wednesday)
    
    return next_draw.strftime('%Y-%m-%d')

def main():
    """Generate French Loto combinations"""
    args = parse_arguments()
    
    # Calculate target date if not provided
    target_date = args.target_date if args.target_date else get_next_draw_date()
    
    print(f"Generating {args.count} French Loto combinations for draw on {target_date}...")
    
    # Initialize strategy
    strategy = FrenchLotoStrategy()
    
    # Generate combinations
    combinations = strategy.generate_combinations(
        count=args.count, 
        include_multiple_strategies=args.strategies
    )
    
    # Display results
    print("\nGenerated French Loto Combinations:\n")
    
    if args.format == 'table':
        format_as_table(combinations)
    else:
        format_as_list(combinations)
    
    # Save to database if requested
    if args.save:
        saved_ids = strategy.save_combinations_to_db(combinations, target_date)
        print(f"\nSaved {len(saved_ids)} combinations to database for draw on {target_date}.")
    else:
        print("\nCombinations were not saved to database. Use --save flag to save.")

if __name__ == "__main__":
    main()