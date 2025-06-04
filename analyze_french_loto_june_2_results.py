"""
Analyser les résultats du French Loto du 2 juin 2025
contre les 10 combinaisons fusion jouées
Résultats: 8, 13, 25, 29, 36 / Lucky 2
"""

def get_played_combinations():
    """Les 10 combinaisons French Loto Fusion jouées"""
    return [
        {'numbers': [3, 20, 21, 30, 41], 'lucky': 5, 'strategy': 'Perfect Strategic Fusion'},
        {'numbers': [4, 6, 8, 11, 40], 'lucky': 8, 'strategy': 'Risk-Frequency Hybrid'},
        {'numbers': [24, 30, 34, 38, 42], 'lucky': 5, 'strategy': 'Markov-Time Fusion'},
        {'numbers': [3, 7, 32, 39, 45], 'lucky': 5, 'strategy': 'Coverage-Risk Balance'},
        {'numbers': [3, 8, 13, 28, 31], 'lucky': 9, 'strategy': 'Hot Numbers Concentration'},
        {'numbers': [13, 24, 26, 29, 33], 'lucky': 1, 'strategy': 'Strategic Diversity Mix'},
        {'numbers': [3, 10, 20, 29, 30], 'lucky': 8, 'strategy': 'Pattern Recognition Fusion'},
        {'numbers': [6, 8, 10, 31, 36], 'lucky': 5, 'strategy': 'Trend-Frequency Hybrid'},
        {'numbers': [4, 10, 21, 30, 36], 'lucky': 8, 'strategy': 'Cold-Hot Equilibrium'},
        {'numbers': [10, 20, 28, 41, 48], 'lucky': 9, 'strategy': 'Ultimate Strategic Synthesis'}
    ]

def get_june_2_results():
    """Résultats du tirage du 2 juin 2025"""
    return {
        'numbers': [8, 13, 25, 29, 36],
        'lucky': 2
    }

def analyze_combination_performance(combo, results):
    """Analyser la performance d'une combinaison"""
    
    number_matches = len([n for n in combo['numbers'] if n in results['numbers']])
    lucky_match = 1 if combo['lucky'] == results['lucky'] else 0
    
    return {
        'number_matches': number_matches,
        'lucky_match': lucky_match,
        'matched_numbers': [n for n in combo['numbers'] if n in results['numbers']],
        'total_score': number_matches + lucky_match
    }

def analyze_all_combinations():
    """Analyser toutes les combinaisons contre les résultats"""
    
    played_combos = get_played_combinations()
    results = get_june_2_results()
    
    print("🎯 ANALYSE FRENCH LOTO - 2 JUIN 2025")
    print(f"Résultats: {results['numbers']} / Lucky {results['lucky']}")
    print("=" * 60)
    
    analysis_results = []
    
    for i, combo in enumerate(played_combos, 1):
        performance = analyze_combination_performance(combo, results)
        
        analysis_results.append({
            'combo_num': i,
            'strategy': combo['strategy'],
            'combination': combo,
            'performance': performance
        })
        
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Combinaison: {combo['numbers']} + Lucky {combo['lucky']}")
        print(f"    Numéros gagnants: {performance['matched_numbers']} ({performance['number_matches']}/5)")
        print(f"    Lucky match: {'✅' if performance['lucky_match'] else '❌'}")
        print(f"    Score total: {performance['total_score']}/6")
        print()
    
    return analysis_results

def find_best_performers(analysis_results):
    """Identifier les meilleures performances"""
    
    print("🏆 MEILLEURES PERFORMANCES:")
    print("-" * 35)
    
    # Trier par score total
    sorted_results = sorted(analysis_results, key=lambda x: x['performance']['total_score'], reverse=True)
    
    best_performers = []
    for result in sorted_results:
        if result['performance']['number_matches'] >= 2:  # Au moins 2 numéros
            best_performers.append(result)
    
    for i, result in enumerate(best_performers, 1):
        perf = result['performance']
        print(f"{i}. {result['strategy']}")
        print(f"   Numéros capturés: {perf['matched_numbers']} ({perf['number_matches']}/5)")
        print(f"   Score: {perf['total_score']}/6")
        print()
    
    return best_performers

def analyze_winning_patterns(results):
    """Analyser les patterns des numéros gagnants"""
    
    print("📊 ANALYSE DES PATTERNS GAGNANTS:")
    print("-" * 40)
    
    winning_numbers = results['numbers']
    
    # Analyse par range
    low_range = [n for n in winning_numbers if n <= 16]
    mid_range = [n for n in winning_numbers if 17 <= n <= 33]
    high_range = [n for n in winning_numbers if n >= 34]
    
    print(f"Distribution par range:")
    print(f"  Bas (1-16): {low_range} ({len(low_range)}/5)")
    print(f"  Mid (17-33): {mid_range} ({len(mid_range)}/5)")
    print(f"  Haut (34-49): {high_range} ({len(high_range)}/5)")
    
    # Analyse des caractéristiques
    even_numbers = [n for n in winning_numbers if n % 2 == 0]
    odd_numbers = [n for n in winning_numbers if n % 2 == 1]
    
    print(f"\nCaractéristiques:")
    print(f"  Pairs: {even_numbers} ({len(even_numbers)}/5)")
    print(f"  Impairs: {odd_numbers} ({len(odd_numbers)}/5)")
    print(f"  Somme: {sum(winning_numbers)}")
    print(f"  Lucky number: {results['lucky']} (très bas)")
    
    return {
        'range_distribution': {'low': len(low_range), 'mid': len(mid_range), 'high': len(high_range)},
        'parity': {'even': len(even_numbers), 'odd': len(odd_numbers)},
        'sum': sum(winning_numbers),
        'lucky': results['lucky']
    }

def analyze_strategy_effectiveness(analysis_results):
    """Analyser l'efficacité des différentes stratégies"""
    
    print("🎯 EFFICACITÉ DES STRATÉGIES:")
    print("-" * 35)
    
    strategy_performance = {}
    
    for result in analysis_results:
        strategy = result['strategy']
        score = result['performance']['total_score']
        matches = result['performance']['number_matches']
        
        if 'Hot Numbers' in strategy:
            category = 'Hot Focus'
        elif 'Risk' in strategy or 'Cold' in strategy:
            category = 'Risk/Cold Focus'
        elif 'Markov' in strategy or 'Time' in strategy:
            category = 'Pattern/Sequence'
        else:
            category = 'Fusion/Balance'
        
        if category not in strategy_performance:
            strategy_performance[category] = {'total_score': 0, 'total_matches': 0, 'count': 0}
        
        strategy_performance[category]['total_score'] += score
        strategy_performance[category]['total_matches'] += matches
        strategy_performance[category]['count'] += 1
    
    for category, data in strategy_performance.items():
        avg_score = data['total_score'] / data['count']
        avg_matches = data['total_matches'] / data['count']
        
        print(f"{category}:")
        print(f"  Score moyen: {avg_score:.1f}/6")
        print(f"  Matches moyens: {avg_matches:.1f}/5")
        print()

def identify_successful_numbers(analysis_results):
    """Identifier quels numéros de nos combinaisons étaient gagnants"""
    
    print("🎯 NUMÉROS GAGNANTS DANS NOS COMBINAISONS:")
    print("-" * 45)
    
    results = get_june_2_results()
    winning_numbers = results['numbers']  # [8, 13, 25, 29, 36]
    
    number_appearances = {}
    
    for result in analysis_results:
        combo = result['combination']
        for num in combo['numbers']:
            if num not in number_appearances:
                number_appearances[num] = []
            number_appearances[num].append(result['strategy'])
    
    print("Numéros gagnants et leur présence dans nos combinaisons:")
    for winning_num in winning_numbers:
        if winning_num in number_appearances:
            strategies = number_appearances[winning_num]
            print(f"  {winning_num}: {len(strategies)} combinaisons")
            for strategy in strategies:
                print(f"    - {strategy}")
        else:
            print(f"  {winning_num}: 0 combinaisons ❌")
        print()

def main():
    """Analyse complète des résultats"""
    
    print("🚀 ANALYSE COMPLÈTE FRENCH LOTO - 2 JUIN 2025")
    print("=" * 55)
    
    # Analyser toutes les combinaisons
    analysis_results = analyze_all_combinations()
    
    # Identifier les meilleures performances
    best_performers = find_best_performers(analysis_results)
    
    # Analyser les patterns gagnants
    patterns = analyze_winning_patterns(get_june_2_results())
    
    # Analyser l'efficacité des stratégies
    analyze_strategy_effectiveness(analysis_results)
    
    # Identifier les numéros gagnants dans nos combinaisons
    identify_successful_numbers(analysis_results)
    
    print("📊 RÉSUMÉ:")
    print(f"✅ {len(best_performers)} combinaisons avec 2+ numéros gagnants")
    print(f"🎯 Distribution gagnante: {patterns['range_distribution']['low']} bas, {patterns['range_distribution']['mid']} mid, {patterns['range_distribution']['high']} haut")
    print(f"📈 Lucky number 2 était très bas (non anticipé)")
    
    return analysis_results, best_performers, patterns

if __name__ == "__main__":
    main()