"""
Analyser les résultats du tirage Euromillions du 27 mai 2025
contre toutes nos combinaisons générées
Résultats: 12, 30, 38, 40, 41 / étoiles: 4, 12
"""

def get_may27_actual_results():
    """Obtenir les résultats réels du 27 mai 2025"""
    return {
        'numbers': [12, 30, 38, 40, 41],
        'stars': [4, 12]
    }

def get_all_generated_combinations():
    """Obtenir toutes nos combinaisons générées"""
    
    # Set 1: May 23 Optimized (10 combinations)
    may23_optimized = [
        {'numbers': [25, 29, 35, 38, 39], 'stars': [6, 12], 'strategy': 'Heavy High Range Focus', 'set': 'May 23 Optimized'},
        {'numbers': [29, 35, 39, 45, 48], 'stars': [5, 7], 'strategy': 'May 23 Pattern Adaptation', 'set': 'May 23 Optimized'},
        {'numbers': [29, 36, 40, 43, 48], 'stars': [7, 12], 'strategy': 'Fibonacci High-Range Hybrid', 'set': 'May 23 Optimized'},
        {'numbers': [29, 34, 40, 44, 45], 'stars': [6, 12], 'strategy': 'Successful Numbers Enhanced', 'set': 'May 23 Optimized'},
        {'numbers': [26, 31, 34, 38, 44], 'stars': [7, 10], 'strategy': 'Ultra High Range Strategy', 'set': 'May 23 Optimized'},
        {'numbers': [5, 29, 34, 40, 48], 'stars': [1, 12], 'strategy': 'Balanced High-Mid Approach', 'set': 'May 23 Optimized'},
        {'numbers': [14, 22, 29, 40, 45], 'stars': [4, 5], 'strategy': 'Priority Stars Emphasis', 'set': 'May 23 Optimized'},
        {'numbers': [10, 29, 32, 37, 38], 'stars': [3, 4], 'strategy': 'Mathematical High Precision', 'set': 'May 23 Optimized'},
        {'numbers': [10, 22, 26, 35, 46], 'stars': [8, 9], 'strategy': 'May 23 Winners Extended', 'set': 'May 23 Optimized'},
        {'numbers': [10, 19, 26, 36, 45], 'stars': [1, 4], 'strategy': 'Ultimate High Range Fusion', 'set': 'May 23 Optimized'}
    ]
    
    # Set 2: Backtesting Improved (10 combinations)
    backtesting_improved = [
        {'numbers': [10, 26, 29, 43, 47], 'stars': [1, 7], 'strategy': 'Enhanced Star Priority Strategy', 'set': 'Backtesting Improved'},
        {'numbers': [10, 26, 29, 43, 47], 'stars': [1, 2], 'strategy': 'Backtesting Winner Replication', 'set': 'Backtesting Improved'},
        {'numbers': [10, 26, 29, 43, 47], 'stars': [2, 12], 'strategy': 'Historical Pattern Adaptation', 'set': 'Backtesting Improved'},
        {'numbers': [20, 29, 37, 48, 50], 'stars': [7, 12], 'strategy': 'Diversified High Range Focus', 'set': 'Backtesting Improved'},
        {'numbers': [6, 19, 29, 41, 48], 'stars': [2, 7], 'strategy': 'Star-Number Balance Optimization', 'set': 'Backtesting Improved'},
        {'numbers': [16, 29, 32, 38, 45], 'stars': [8, 12], 'strategy': 'Proven Winners Concentration', 'set': 'Backtesting Improved'},
        {'numbers': [10, 29, 35, 36, 49], 'stars': [6, 8], 'strategy': 'Wide Range Coverage Strategy', 'set': 'Backtesting Improved'},
        {'numbers': [10, 12, 13, 29, 36], 'stars': [7, 10], 'strategy': 'Mathematical Balance Approach', 'set': 'Backtesting Improved'},
        {'numbers': [10, 29, 31, 36, 44], 'stars': [4, 9], 'strategy': 'Hybrid Concentration Method', 'set': 'Backtesting Improved'},
        {'numbers': [10, 26, 29, 36, 46], 'stars': [5, 9], 'strategy': 'Ultimate Backtesting Fusion', 'set': 'Backtesting Improved'}
    ]
    
    # Set 3: Strategic Methods (10 combinations)
    strategic_methods = [
        {'numbers': [3, 17, 29, 41, 47], 'stars': [7, 11], 'strategy': 'Risk/Reward Balance - High Risk', 'set': 'Strategic Methods'},
        {'numbers': [10, 22, 29, 36, 44], 'stars': [5, 12], 'strategy': 'Risk/Reward Balance - Moderate Risk', 'set': 'Strategic Methods'},
        {'numbers': [7, 10, 23, 29, 42], 'stars': [3, 7], 'strategy': 'Frequency Analysis - Hot Numbers', 'set': 'Strategic Methods'},
        {'numbers': [4, 19, 29, 35, 48], 'stars': [9, 12], 'strategy': 'Frequency Analysis - Hot-Cold Balance', 'set': 'Strategic Methods'},
        {'numbers': [8, 15, 29, 36, 43], 'stars': [4, 7], 'strategy': 'Markov Chain - Sequential Patterns', 'set': 'Strategic Methods'},
        {'numbers': [5, 18, 29, 40, 46], 'stars': [6, 12], 'strategy': 'Markov Chain - Transition Probability', 'set': 'Strategic Methods'},
        {'numbers': [12, 24, 29, 38, 45], 'stars': [2, 7], 'strategy': 'Time Series - Trend Analysis', 'set': 'Strategic Methods'},
        {'numbers': [9, 21, 29, 33, 49], 'stars': [8, 12], 'strategy': 'Time Series - Seasonal Patterns', 'set': 'Strategic Methods'},
        {'numbers': [4, 10, 29, 36, 44], 'stars': [7, 12], 'strategy': 'Coverage Optimization - Balanced Mix', 'set': 'Strategic Methods'},
        {'numbers': [3, 17, 22, 41, 47], 'stars': [5, 11], 'strategy': 'Coverage Optimization - Diversified Mix', 'set': 'Strategic Methods'}
    ]
    
    # Set 4: Ultimate Mix (3 combinations)
    ultimate_mix = [
        {'numbers': [10, 26, 29, 36, 45], 'stars': [7, 12], 'strategy': 'Ultimate Mix - Frequency Champions', 'set': 'Ultimate Mix'},
        {'numbers': [29, 35, 39, 40, 48], 'stars': [6, 12], 'strategy': 'Ultimate Mix - High Performance Fusion', 'set': 'Ultimate Mix'},
        {'numbers': [10, 26, 29, 36, 45], 'stars': [1, 2], 'strategy': 'Ultimate Mix - Strategic Balance Supreme', 'set': 'Ultimate Mix'}
    ]
    
    # Set 5: Mixed Strategy (10 combinations)
    mixed_strategy = [
        {'numbers': [2, 8, 15, 36, 41], 'stars': [9, 12], 'strategy': 'Mixed Strategy - Balanced', 'set': 'Mixed Strategy'},
        {'numbers': [15, 29, 30, 31, 43], 'stars': [11, 12], 'strategy': 'Mixed Strategy - Hot Emphasis', 'set': 'Mixed Strategy'},
        {'numbers': [17, 25, 30, 41, 49], 'stars': [5, 8], 'strategy': 'Mixed Strategy - Cold Balance', 'set': 'Mixed Strategy'},
        {'numbers': [10, 14, 16, 24, 36], 'stars': [1, 3], 'strategy': 'Mixed Strategy - Frequency Optimized', 'set': 'Mixed Strategy'},
        {'numbers': [3, 9, 25, 40, 46], 'stars': [7, 11], 'strategy': 'Mixed Strategy - Diversity Focus', 'set': 'Mixed Strategy'},
        {'numbers': [9, 19, 27, 33, 50], 'stars': [2, 6], 'strategy': 'Mixed Strategy - Strategic Balance', 'set': 'Mixed Strategy'},
        {'numbers': [4, 10, 15, 21, 40], 'stars': [1, 10], 'strategy': 'Mixed Strategy - Pattern Variation', 'set': 'Mixed Strategy'},
        {'numbers': [6, 30, 33, 38, 44], 'stars': [3, 6], 'strategy': 'Mixed Strategy - Adaptive Mix', 'set': 'Mixed Strategy'},
        {'numbers': [13, 20, 24, 25, 43], 'stars': [6, 9], 'strategy': 'Mixed Strategy - Range Optimized', 'set': 'Mixed Strategy'},
        {'numbers': [11, 30, 31, 41, 48], 'stars': [3, 7], 'strategy': 'Mixed Strategy - Ultimate Balance', 'set': 'Mixed Strategy'}
    ]
    
    # Combiner tous les sets
    all_combinations = may23_optimized + backtesting_improved + strategic_methods + ultimate_mix + mixed_strategy
    
    return all_combinations

def analyze_combination_performance(combination, actual_results):
    """Analyser la performance d'une combinaison contre les résultats réels"""
    
    combo_numbers = set(combination['numbers'])
    actual_numbers = set(actual_results['numbers'])
    
    combo_stars = set(combination['stars'])
    actual_stars = set(actual_results['stars'])
    
    # Compter les correspondances
    number_matches = len(combo_numbers.intersection(actual_numbers))
    matched_numbers = sorted(list(combo_numbers.intersection(actual_numbers)))
    
    star_matches = len(combo_stars.intersection(actual_stars))
    matched_stars = sorted(list(combo_stars.intersection(actual_stars)))
    
    # Calculer le score de performance
    performance_score = (number_matches * 2) + (star_matches * 3)
    max_possible = 16  # 5 nombres * 2 + 2 étoiles * 3
    percentage = (performance_score / max_possible) * 100
    
    return {
        'combination': combination,
        'number_matches': number_matches,
        'matched_numbers': matched_numbers,
        'star_matches': star_matches,
        'matched_stars': matched_stars,
        'performance_score': performance_score,
        'percentage': round(percentage, 1),
        'won_prize': performance_score > 0
    }

def analyze_all_combinations():
    """Analyser toutes les combinaisons contre les résultats du 27 mai"""
    
    actual_results = get_may27_actual_results()
    all_combinations = get_all_generated_combinations()
    
    print("🎯 ANALYSE DES RÉSULTATS EUROMILLIONS - 27 MAI 2025")
    print("=" * 65)
    print(f"Résultats réels: {actual_results['numbers']} / Étoiles: {actual_results['stars']}")
    print("=" * 65)
    
    all_results = []
    
    # Analyser chaque combinaison
    for combination in all_combinations:
        result = analyze_combination_performance(combination, actual_results)
        all_results.append(result)
    
    return all_results, actual_results

def find_best_performers(results):
    """Trouver les meilleures performances"""
    
    # Trier par score de performance
    sorted_results = sorted(results, key=lambda x: x['performance_score'], reverse=True)
    
    print("\n🏆 TOP PERFORMANCES:")
    print("=" * 35)
    
    # Trouver les gagnants
    winners = [r for r in sorted_results if r['performance_score'] > 0]
    
    if not winners:
        print("❌ Aucune combinaison n'a obtenu de correspondances avec les numéros gagnants.")
        print("\n🔍 COMBINAISONS LES PLUS PROCHES:")
        top_5 = sorted_results[:5]
    else:
        print(f"✅ {len(winners)} combinaisons ont obtenu des correspondances!")
        top_5 = winners[:10] if len(winners) >= 10 else winners
    
    for i, result in enumerate(top_5, 1):
        combo = result['combination']
        print(f"{i:2d}. {combo['strategy']} ({combo['set']})")
        print(f"    Numéros: {combo['numbers']} | Étoiles: {combo['stars']}")
        print(f"    Correspondances: {result['number_matches']} numéros {result['matched_numbers']}")
        if result['star_matches'] > 0:
            print(f"    Étoiles: {result['star_matches']} étoiles {result['matched_stars']} ⭐")
        print(f"    Score: {result['performance_score']}/16 ({result['percentage']}%)")
        print()
    
    return top_5

def analyze_by_strategy_set(results):
    """Analyser les performances par ensemble de stratégies"""
    
    print("📊 ANALYSE PAR ENSEMBLE DE STRATÉGIES:")
    print("=" * 45)
    
    # Grouper par ensemble
    sets_performance = {}
    
    for result in results:
        set_name = result['combination']['set']
        if set_name not in sets_performance:
            sets_performance[set_name] = {
                'total_score': 0,
                'combinations': 0,
                'winners': 0,
                'best_score': 0
            }
        
        sets_performance[set_name]['total_score'] += result['performance_score']
        sets_performance[set_name]['combinations'] += 1
        sets_performance[set_name]['best_score'] = max(
            sets_performance[set_name]['best_score'], 
            result['performance_score']
        )
        if result['won_prize']:
            sets_performance[set_name]['winners'] += 1
    
    # Trier par performance moyenne
    sorted_sets = sorted(sets_performance.items(), 
                        key=lambda x: x[1]['total_score']/x[1]['combinations'], 
                        reverse=True)
    
    for set_name, stats in sorted_sets:
        avg_score = stats['total_score'] / stats['combinations']
        success_rate = (stats['winners'] / stats['combinations']) * 100
        
        print(f"{set_name}:")
        print(f"   Score moyen: {avg_score:.1f}/16")
        print(f"   Meilleur score: {stats['best_score']}/16")
        print(f"   Taux de succès: {stats['winners']}/{stats['combinations']} ({success_rate:.1f}%)")
        print()

def analyze_winning_patterns(actual_results):
    """Analyser les patterns des numéros gagnants du 27 mai"""
    
    numbers = actual_results['numbers']
    stars = actual_results['stars']
    
    print("🔍 ANALYSE DES PATTERNS GAGNANTS - 27 MAI:")
    print("=" * 50)
    
    # Analyse des ranges
    low_count = len([n for n in numbers if n <= 17])
    mid_count = len([n for n in numbers if 18 <= n <= 34])
    high_count = len([n for n in numbers if n >= 35])
    
    print(f"Distribution des ranges:")
    print(f"   Bas (1-17): {low_count}/5 ({low_count/5*100:.0f}%) → {[n for n in numbers if n <= 17]}")
    print(f"   Moyen (18-34): {mid_count}/5 ({mid_count/5*100:.0f}%) → {[n for n in numbers if 18 <= n <= 34]}")
    print(f"   Haut (35-50): {high_count}/5 ({high_count/5*100:.0f}%) → {[n for n in numbers if n >= 35]}")
    
    # Analyse pair/impair
    even_count = len([n for n in numbers if n % 2 == 0])
    odd_count = len([n for n in numbers if n % 2 == 1])
    
    print(f"\nDistribution pair/impair:")
    print(f"   Pairs: {even_count}/5 ({even_count/5*100:.0f}%) → {[n for n in numbers if n % 2 == 0]}")
    print(f"   Impairs: {odd_count}/5 ({odd_count/5*100:.0f}%) → {[n for n in numbers if n % 2 == 1]}")
    
    # Caractéristiques des numéros
    print(f"\nCaractéristiques des numéros:")
    print(f"   Numéros: {numbers}")
    print(f"   Somme: {sum(numbers)}")
    print(f"   Moyenne: {sum(numbers)/5:.1f}")
    print(f"   Écart: {max(numbers) - min(numbers)}")
    print(f"   Étoiles: {stars}")
    
    # Analyse des intervalles
    intervals = []
    for i in range(len(numbers)-1):
        intervals.append(numbers[i+1] - numbers[i])
    
    print(f"   Intervalles: {intervals}")
    print(f"   Intervalle moyen: {sum(intervals)/len(intervals):.1f}")

def main():
    """Fonction principale d'analyse"""
    
    # Analyser toutes les combinaisons
    results, actual_results = analyze_all_combinations()
    
    # Trouver les meilleures performances
    best_performers = find_best_performers(results)
    
    # Analyser par ensemble de stratégies
    analyze_by_strategy_set(results)
    
    # Analyser les patterns gagnants
    analyze_winning_patterns(actual_results)
    
    print("\n🚀 ANALYSE TERMINÉE!")
    print("=" * 25)
    print("Vos combinaisons ont été analysées contre les résultats du 27 mai!")

if __name__ == "__main__":
    main()