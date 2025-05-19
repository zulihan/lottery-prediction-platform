"""
Analyze how close our combinations came to the May 19, 2025 French Loto draw
and identify patterns for generating new combinations.
"""
import json
from database import get_session, GeneratedCombination, FrenchLotoDrawing
from sqlalchemy import desc
from datetime import date
from collections import Counter

def get_may19_combinations():
    """
    Get all combinations we generated for the May 19 draw
    """
    session = get_session()
    try:
        may19_combos = session.query(GeneratedCombination) \
            .filter(GeneratedCombination.created_at == date(2025, 5, 19)) \
            .all()
        
        combinations = []
        for combo in may19_combos:
            combinations.append({
                'id': combo.id,
                'numbers': json.loads(combo.numbers),
                'lucky_number': json.loads(combo.stars)[0],
                'strategy': combo.strategy,
                'score': combo.score
            })
        
        return combinations
    finally:
        session.close()

def get_may19_results():
    """
    Get the actual drawing results for May 19
    """
    return {
        'numbers': [8, 30, 33, 42, 43],
        'lucky_number': 4
    }

def analyze_match_performance(combinations, actual_results):
    """
    Analyze how well each combination performed against the actual results
    """
    results = []
    
    for combo in combinations:
        # Count matching numbers
        matching_numbers = set(combo['numbers']).intersection(set(actual_results['numbers']))
        lucky_match = 1 if combo['lucky_number'] == actual_results['lucky_number'] else 0
        
        results.append({
            'combo': combo,
            'matching_numbers': list(matching_numbers),
            'num_matches': len(matching_numbers),
            'lucky_match': lucky_match,
            'total_score': len(matching_numbers) * 2 + lucky_match
        })
    
    return sorted(results, key=lambda x: (x['num_matches'], x['lucky_match']), reverse=True)

def analyze_strategy_performance(analyzed_results):
    """
    Analyze which strategies performed best
    """
    strategy_performance = {}
    
    for result in analyzed_results:
        strategy = result['combo']['strategy']
        
        if strategy not in strategy_performance:
            strategy_performance[strategy] = {
                'combos': 0,
                'total_matches': 0,
                'max_matches': 0,
                'lucky_matches': 0
            }
        
        perf = strategy_performance[strategy]
        perf['combos'] += 1
        perf['total_matches'] += result['num_matches']
        perf['max_matches'] = max(perf['max_matches'], result['num_matches'])
        perf['lucky_matches'] += result['lucky_match']
    
    # Calculate average performance metrics
    for strategy, perf in strategy_performance.items():
        if perf['combos'] > 0:
            perf['avg_matches'] = perf['total_matches'] / perf['combos']
            perf['match_rate'] = perf['total_matches'] / (perf['combos'] * 5)  # 5 numbers per combo
            perf['lucky_hit_rate'] = perf['lucky_matches'] / perf['combos']
        else:
            perf['avg_matches'] = 0
            perf['match_rate'] = 0
            perf['lucky_hit_rate'] = 0
    
    return strategy_performance

def analyze_number_patterns(winning_numbers):
    """
    Analyze patterns in the winning numbers
    """
    # Basic statistics
    numbers = winning_numbers['numbers']
    lucky = winning_numbers['lucky_number']
    
    # Even/odd distribution
    even_count = len([n for n in numbers if n % 2 == 0])
    odd_count = 5 - even_count
    
    # Sum and average
    total_sum = sum(numbers)
    average = total_sum / 5
    
    # Range distribution
    ranges = {
        '1-10': len([n for n in numbers if 1 <= n <= 10]),
        '11-20': len([n for n in numbers if 11 <= n <= 20]),
        '21-30': len([n for n in numbers if 21 <= n <= 30]),
        '31-40': len([n for n in numbers if 31 <= n <= 40]),
        '41-49': len([n for n in numbers if 41 <= n <= 49])
    }
    
    # Check for sequential numbers
    numbers_sorted = sorted(numbers)
    sequential_pairs = 0
    for i in range(len(numbers_sorted) - 1):
        if numbers_sorted[i+1] - numbers_sorted[i] == 1:
            sequential_pairs += 1
    
    # Analyze number distribution compared to historical data
    session = get_session()
    try:
        # Get frequency of winning numbers in historical data
        historical_drawings = session.query(FrenchLotoDrawing) \
            .filter(FrenchLotoDrawing.date < date(2025, 5, 19)) \
            .all()
        
        historical_numbers = []
        for drawing in historical_drawings:
            historical_numbers.extend([drawing.n1, drawing.n2, drawing.n3, drawing.n4, drawing.n5])
        
        number_freq = Counter(historical_numbers)
        
        # Check if winning numbers were historically hot or cold
        number_ranks = {}
        for num in range(1, 50):
            number_ranks[num] = {
                'frequency': number_freq.get(num, 0),
                'rank': 0  # Will be calculated below
            }
        
        # Rank numbers by frequency
        sorted_numbers = sorted(number_ranks.keys(), key=lambda x: number_ranks[x]['frequency'], reverse=True)
        for i, num in enumerate(sorted_numbers):
            number_ranks[num]['rank'] = i + 1
        
        # Check if winning numbers were hot or cold
        winning_ranks = [number_ranks[n]['rank'] for n in numbers]
        avg_rank = sum(winning_ranks) / len(winning_ranks)
        
        # Categorize numbers as hot, medium, or cold
        hot_cutoff = 16  # Top third
        cold_cutoff = 33  # Bottom third
        
        winning_categories = {
            'hot': len([n for n in numbers if number_ranks[n]['rank'] <= hot_cutoff]),
            'medium': len([n for n in numbers if hot_cutoff < number_ranks[n]['rank'] < cold_cutoff]),
            'cold': len([n for n in numbers if number_ranks[n]['rank'] >= cold_cutoff])
        }
        
        lucky_rank = number_ranks.get(lucky, {}).get('rank', 0)
        lucky_category = 'hot' if lucky_rank <= hot_cutoff else ('cold' if lucky_rank >= cold_cutoff else 'medium')
        
        return {
            'even_odd': {'even': even_count, 'odd': odd_count},
            'sum': total_sum,
            'average': average,
            'ranges': ranges,
            'sequential_pairs': sequential_pairs,
            'avg_rank': avg_rank,
            'categories': winning_categories,
            'lucky_category': lucky_category
        }
    finally:
        session.close()

def analyze_missed_opportunities(winning_numbers, analyzed_results):
    """
    Analyze what we missed and how we could have generated the winning combination
    """
    # Check if any of our pairs appeared in the winning combination
    winning_set = set(winning_numbers['numbers'])
    
    # Collect all pairs from our combinations
    all_pairs = []
    for result in analyzed_results:
        combo_numbers = result['combo']['numbers']
        for i in range(len(combo_numbers)):
            for j in range(i+1, len(combo_numbers)):
                all_pairs.append((combo_numbers[i], combo_numbers[j]))
    
    # Count pair frequencies
    pair_counter = Counter(all_pairs)
    
    # Check which winning pairs we included in our combinations
    winning_pairs = []
    for i in range(len(winning_numbers['numbers'])):
        for j in range(i+1, len(winning_numbers['numbers'])):
            pair = (winning_numbers['numbers'][i], winning_numbers['numbers'][j])
            sorted_pair = tuple(sorted(pair))
            winning_pairs.append(sorted_pair)
    
    included_pairs = {}
    for pair in winning_pairs:
        sorted_pair = tuple(sorted(pair))
        included_pairs[sorted_pair] = pair_counter.get(sorted_pair, 0)
    
    # Check if the winning numbers appeared in our combinations and how frequently
    number_counter = Counter()
    for result in analyzed_results:
        number_counter.update(result['combo']['numbers'])
    
    winning_frequencies = {num: number_counter.get(num, 0) for num in winning_numbers['numbers']}
    
    # Check if lucky number appeared in our combinations
    lucky_counter = Counter()
    for result in analyzed_results:
        lucky_counter.update([result['combo']['lucky_number']])
    
    lucky_frequency = lucky_counter.get(winning_numbers['lucky_number'], 0)
    
    return {
        'included_pairs': included_pairs,
        'winning_frequencies': winning_frequencies,
        'lucky_frequency': lucky_frequency
    }

def main():
    """Analyze the May 19 results and print findings"""
    print("Analyzing May 19, 2025 French Loto results...")
    
    # Get our generated combinations
    combinations = get_may19_combinations()
    
    if not combinations:
        print("No combinations found for May 19, 2025.")
        return
    
    print(f"Found {len(combinations)} combinations generated for May 19.")
    
    # Get actual drawing results
    actual_results = get_may19_results()
    print(f"Actual drawing: {actual_results['numbers']} / Lucky: {actual_results['lucky_number']}")
    
    # Analyze match performance
    analyzed_results = analyze_match_performance(combinations, actual_results)
    
    # Show best-performing combinations
    print("\nBest-performing combinations:")
    for i, result in enumerate(analyzed_results[:5], 1):
        combo = result['combo']
        print(f"{i}. Numbers: {combo['numbers']} / Lucky: {combo['lucky_number']} ({combo['strategy']})")
        print(f"   Matches: {result['matching_numbers']} ({result['num_matches']}/5) + "
              f"Lucky: {'Yes' if result['lucky_match'] else 'No'}")
    
    # Analyze strategy performance
    strategy_performance = analyze_strategy_performance(analyzed_results)
    
    print("\nStrategy Performance:")
    for strategy, perf in sorted(strategy_performance.items(), 
                                key=lambda x: x[1]['avg_matches'], 
                                reverse=True):
        print(f"{strategy}: Avg matches: {perf['avg_matches']:.2f}, "
              f"Max matches: {perf['max_matches']}, "
              f"Lucky hits: {perf['lucky_matches']}/{perf['combos']}")
    
    # Analyze number patterns
    patterns = analyze_number_patterns(actual_results)
    
    print("\nWinning Number Patterns:")
    print(f"Even/Odd: {patterns['even_odd']['even']}/{patterns['even_odd']['odd']}")
    print(f"Sum: {patterns['sum']}, Average: {patterns['average']:.2f}")
    print(f"Range distribution: {patterns['ranges']}")
    print(f"Sequential pairs: {patterns['sequential_pairs']}")
    print(f"Number categories: Hot: {patterns['categories']['hot']}, "
          f"Medium: {patterns['categories']['medium']}, "
          f"Cold: {patterns['categories']['cold']}")
    print(f"Lucky number category: {patterns['lucky_category']}")
    
    # Analyze missed opportunities
    missed = analyze_missed_opportunities(actual_results, analyzed_results)
    
    print("\nMissed Opportunities Analysis:")
    print("Winning pairs in our combinations:")
    for pair, count in missed['included_pairs'].items():
        print(f"{pair}: {count} occurrences")
    
    print("\nWinning number frequencies in our combinations:")
    for num, freq in missed['winning_frequencies'].items():
        print(f"Number {num}: {freq} occurrences")
    
    print(f"\nLucky number {actual_results['lucky_number']} appeared in {missed['lucky_frequency']} combinations")
    
    # Identify what we missed
    print("\nWhat we missed:")
    
    # Check if we had combinations with 4 matching numbers
    best_combo = analyzed_results[0]
    if best_combo['num_matches'] >= 4:
        print("- We had combinations with 4+ matching numbers but missed the complete set")
    else:
        print("- Our combinations didn't contain enough of the winning numbers together")
    
    # Check frequency of winning numbers in our combinations
    low_freq_numbers = [num for num, freq in missed['winning_frequencies'].items() if freq <= 2]
    if low_freq_numbers:
        print(f"- Numbers {low_freq_numbers} appeared in few of our combinations")
    
    # Check lucky number
    if missed['lucky_frequency'] == 0:
        print(f"- We didn't include lucky number {actual_results['lucky_number']} in any combination")
    elif missed['lucky_frequency'] < 3:
        print(f"- Lucky number {actual_results['lucky_number']} appeared in only {missed['lucky_frequency']} combinations")
    
    # Recommendations for next draw
    print("\nRecommendations for next draw:")
    
    # Best strategies
    top_strategies = [s for s, p in sorted(strategy_performance.items(), 
                                          key=lambda x: x[1]['avg_matches'], 
                                          reverse=True)[:3]]
    print(f"- Focus on these strategies: {', '.join(top_strategies)}")
    
    # Number patterns
    if patterns['even_odd']['even'] >= 3:
        print("- Include more even numbers (majority of winning numbers were even)")
    else:
        print("- Include more odd numbers (majority of winning numbers were odd)")
    
    # Range focus
    top_ranges = sorted(patterns['ranges'].items(), key=lambda x: x[1], reverse=True)
    if top_ranges[0][1] >= 2:
        print(f"- Focus on the {top_ranges[0][0]} range which had {top_ranges[0][1]} winning numbers")
    
    # Sequential patterns
    if patterns['sequential_pairs'] >= 1:
        print(f"- Include some sequential pairs (winning numbers had {patterns['sequential_pairs']} sequential pairs)")
    
    # Hot/cold patterns
    if patterns['categories']['hot'] >= 3:
        print("- Include more hot numbers (majority of winning numbers were hot)")
    elif patterns['categories']['cold'] >= 3:
        print("- Include more cold numbers (majority of winning numbers were cold)")
    
    # Lucky number
    print(f"- Pay attention to {patterns['lucky_category']} lucky numbers")
    
    # Include winning numbers
    print("- Include these hot numbers from the last draw: " + 
          ", ".join(map(str, sorted(actual_results['numbers']))))
    
    return {
        'winning_numbers': actual_results,
        'analyzed_results': analyzed_results,
        'strategy_performance': strategy_performance,
        'patterns': patterns,
        'missed': missed
    }

if __name__ == "__main__":
    main()