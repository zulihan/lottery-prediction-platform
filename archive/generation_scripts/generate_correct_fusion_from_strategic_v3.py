"""
Générer des combinaisons fusion CORRECTES en utilisant UNIQUEMENT 
les numéros qui apparaissent dans les 10 Strategic Methods V3 originales
"""
from collections import Counter
import random

def get_original_strategic_v3_combinations():
    """Les 10 combinaisons Strategic Methods V3 originales"""
    return [
        {'numbers': [7, 17, 28, 34, 36], 'stars': [9, 12], 'strategy': 'Risk/Reward Enhanced - Enhanced High'},
        {'numbers': [4, 23, 33, 35, 39], 'stars': [1, 12], 'strategy': 'Risk/Reward Enhanced - Enhanced Moderate'},
        {'numbers': [33, 44, 21, 35, 20], 'stars': [5, 8], 'strategy': 'Frequency Analysis Enhanced - Ultra Hot Focus'},
        {'numbers': [14, 23, 29, 37, 44], 'stars': [8, 12], 'strategy': 'Frequency Analysis Enhanced - Hot-Medium Balance'},
        {'numbers': [16, 20, 21, 29, 50], 'stars': [5, 8], 'strategy': 'Frequency Analysis Enhanced - Frequency Zones'},
        {'numbers': [9, 18, 23, 35, 44], 'stars': [5, 9], 'strategy': 'Markov Chain Enhanced - Advanced Sequential'},
        {'numbers': [7, 23, 31, 37, 45], 'stars': [1, 3], 'strategy': 'Markov Chain Enhanced - Transition Matrix'},
        {'numbers': [12, 29, 37, 39, 47], 'stars': [3, 4], 'strategy': 'Time Series Enhanced - Temporal Trends'},
        {'numbers': [10, 25, 31, 33, 42], 'stars': [1, 6], 'strategy': 'Time Series Enhanced - Cyclical Patterns'},
        {'numbers': [7, 12, 15, 29, 38], 'stars': [5, 8], 'strategy': 'Coverage Optimization Enhanced - Ultra Balance'}
    ]

def analyze_strategic_v3_pool():
    """Analyser les numéros et étoiles disponibles dans les 10 combinaisons originales"""
    
    strategic_combos = get_original_strategic_v3_combinations()
    
    all_numbers = []
    all_stars = []
    
    for combo in strategic_combos:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    # Compter les fréquences
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Pool disponible (tous les numéros/étoiles qui apparaissent)
    available_numbers = list(set(all_numbers))
    available_stars = list(set(all_stars))
    
    # Les plus fréquents
    most_frequent_numbers = [num for num, _ in number_freq.most_common()]
    most_frequent_stars = [star for star, _ in star_freq.most_common()]
    
    print("📊 ANALYSE DU POOL STRATEGIC V3 ORIGINAL:")
    print(f"Numéros disponibles: {sorted(available_numbers)}")
    print(f"Étoiles disponibles: {sorted(available_stars)}")
    print(f"Numéros par fréquence: {most_frequent_numbers[:10]}")
    print(f"Étoiles par fréquence: {most_frequent_stars}")
    
    return {
        'available_numbers': available_numbers,
        'available_stars': available_stars,
        'most_frequent_numbers': most_frequent_numbers,
        'most_frequent_stars': most_frequent_stars,
        'number_freq': number_freq,
        'star_freq': star_freq
    }

def generate_correct_fusion_combinations(pool_data):
    """Générer 10 combinaisons fusion CORRECTES en utilisant uniquement le pool original"""
    
    print(f"\n🎯 FUSION COMBINATIONS CORRECTES - 10 COMBINAISONS")
    print("Utilisant UNIQUEMENT les numéros des 10 Strategic Methods V3 originales")
    print("-" * 70)
    
    fusion_combinations = []
    
    fusion_strategies = [
        'Frequency Champions Fusion',
        'Risk-Frequency Hybrid', 
        'Markov-Time Fusion',
        'Coverage-Risk Balance',
        'Hot Numbers Concentration',
        'Strategic Diversity Mix',
        'Pattern Recognition Fusion',
        'Trend-Frequency Hybrid',
        'Cold-Hot Equilibrium',
        'Ultimate Strategic Synthesis'
    ]
    
    for i, strategy_name in enumerate(fusion_strategies):
        
        if strategy_name == 'Frequency Champions Fusion':
            # Utiliser les 5 numéros les plus fréquents du pool
            selected_numbers = pool_data['most_frequent_numbers'][:5]
            selected_stars = pool_data['most_frequent_stars'][:2]
            
        elif strategy_name == 'Risk-Frequency Hybrid':
            # Mix des plus fréquents et moins fréquents
            frequent = pool_data['most_frequent_numbers'][:3]
            less_frequent = pool_data['most_frequent_numbers'][-2:]
            selected_numbers = sorted(frequent + less_frequent)
            selected_stars = pool_data['most_frequent_stars'][:2]
            
        elif strategy_name == 'Markov-Time Fusion':
            # Numéros des strategies Markov et Time Series seulement
            markov_time_numbers = [7, 23, 31, 37, 45, 12, 29, 39, 47, 10, 25, 33, 42]
            available_markov_time = [n for n in markov_time_numbers if n in pool_data['available_numbers']]
            selected_numbers = sorted(random.sample(available_markov_time, 5))
            selected_stars = [1, 3]  # Étoiles des Markov/Time Series
            
        elif strategy_name == 'Coverage-Risk Balance':
            # Mix équilibré de différentes fréquences
            high_freq = pool_data['most_frequent_numbers'][:2]
            mid_freq = pool_data['most_frequent_numbers'][5:7]
            low_freq = [pool_data['most_frequent_numbers'][-1]]
            selected_numbers = sorted(high_freq + mid_freq + low_freq)
            selected_stars = sorted(random.sample(pool_data['available_stars'], 2))
            
        elif strategy_name == 'Hot Numbers Concentration':
            # Concentration sur les numéros très fréquents
            selected_numbers = pool_data['most_frequent_numbers'][:5]
            selected_stars = pool_data['most_frequent_stars'][:2]
            
        elif strategy_name == 'Strategic Diversity Mix':
            # Un numéro de chaque stratégie principale
            risk_reward_nums = [7, 17, 28, 34, 36, 4, 23, 33, 35, 39]
            freq_analysis_nums = [20, 21, 29, 44, 14, 37, 16, 50]
            markov_nums = [9, 18, 31, 45]
            time_nums = [12, 47, 10, 25, 42]
            coverage_nums = [15, 38]
            
            diversity_pick = [
                random.choice([n for n in risk_reward_nums if n in pool_data['available_numbers']]),
                random.choice([n for n in freq_analysis_nums if n in pool_data['available_numbers']]),
                random.choice([n for n in markov_nums if n in pool_data['available_numbers']]),
                random.choice([n for n in time_nums if n in pool_data['available_numbers']]),
                random.choice([n for n in coverage_nums if n in pool_data['available_numbers']])
            ]
            selected_numbers = sorted(diversity_pick)
            selected_stars = [5, 9]  # Mix des étoiles
            
        elif strategy_name == 'Pattern Recognition Fusion':
            # Pattern basé sur les numéros qui apparaissent ensemble
            # Numéros qui apparaissent dans plusieurs combinaisons
            multi_appearance = [n for n, freq in pool_data['number_freq'].items() if freq >= 2]
            selected_numbers = sorted(random.sample(multi_appearance, 5))
            selected_stars = [1, 12]  # Étoiles fréquentes
            
        elif strategy_name == 'Trend-Frequency Hybrid':
            # Mix tendance et fréquence
            trend_nums = pool_data['most_frequent_numbers'][:3]
            freq_nums = random.sample([n for n in pool_data['available_numbers'] if n not in trend_nums], 2)
            selected_numbers = sorted(trend_nums + freq_nums)
            selected_stars = [5, 8]  # Étoiles populaires
            
        elif strategy_name == 'Cold-Hot Equilibrium':
            # Équilibre entre fréquents et moins fréquents
            hot = pool_data['most_frequent_numbers'][:2]
            cold = pool_data['most_frequent_numbers'][-2:]
            medium = pool_data['most_frequent_numbers'][len(pool_data['most_frequent_numbers'])//2:len(pool_data['most_frequent_numbers'])//2+1]
            selected_numbers = sorted(hot + cold + medium)
            selected_stars = [9, 12]  # Étoiles équilibrées
            
        else:  # Ultimate Strategic Synthesis
            # Synthèse des numéros les plus strategiques
            ultimate_pick = pool_data['most_frequent_numbers'][:5]
            selected_numbers = sorted(ultimate_pick)
            selected_stars = pool_data['most_frequent_stars'][:2]
        
        # Vérifier que tous les numéros sont dans le pool
        if all(n in pool_data['available_numbers'] for n in selected_numbers) and \
           all(s in pool_data['available_stars'] for s in selected_stars):
            
            fusion_combinations.append({
                'numbers': selected_numbers,
                'stars': selected_stars,
                'strategy': strategy_name,
                'methodology': 'Strategic V3 Pool Fusion'
            })
        else:
            print(f"⚠️ Erreur dans {strategy_name}: numéros hors pool")
    
    return fusion_combinations

def verify_fusion_validity(fusion_combos, pool_data):
    """Vérifier que toutes les combinaisons fusion utilisent uniquement le pool original"""
    
    print(f"\n✅ VÉRIFICATION DE VALIDITÉ:")
    print("-" * 35)
    
    valid_count = 0
    
    for combo in fusion_combos:
        numbers_valid = all(n in pool_data['available_numbers'] for n in combo['numbers'])
        stars_valid = all(s in pool_data['available_stars'] for s in combo['stars'])
        
        if numbers_valid and stars_valid:
            valid_count += 1
            print(f"✅ {combo['strategy']}: VALIDE")
        else:
            print(f"❌ {combo['strategy']}: INVALIDE")
            if not numbers_valid:
                invalid_nums = [n for n in combo['numbers'] if n not in pool_data['available_numbers']]
                print(f"   Numéros invalides: {invalid_nums}")
            if not stars_valid:
                invalid_stars = [s for s in combo['stars'] if s not in pool_data['available_stars']]
                print(f"   Étoiles invalides: {invalid_stars}")
    
    print(f"\n📊 Résultat: {valid_count}/{len(fusion_combos)} combinaisons valides")
    return valid_count == len(fusion_combos)

def main():
    """Générer les combinaisons fusion CORRECTES"""
    
    print("🚀 GÉNÉRATION FUSION COMBINATIONS CORRECTES")
    print("Basées UNIQUEMENT sur les 10 Strategic Methods V3 originales")
    print("=" * 70)
    
    # Analyser le pool des 10 combinaisons originales
    pool_data = analyze_strategic_v3_pool()
    
    # Générer les fusions correctes
    fusion_combos = generate_correct_fusion_combinations(pool_data)
    
    print(f"\n🏆 FUSION COMBINATIONS CORRECTES:")
    print("=" * 40)
    
    for i, combo in enumerate(fusion_combos, 11):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print()
    
    # Vérifier la validité
    is_valid = verify_fusion_validity(fusion_combos, pool_data)
    
    if is_valid:
        print(f"\n✅ SUCCÈS: Toutes les combinations fusion utilisent uniquement le pool Strategic V3!")
    else:
        print(f"\n❌ ERREUR: Certaines combinations utilisent des numéros externes!")
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"• Pool disponible: {len(pool_data['available_numbers'])} numéros, {len(pool_data['available_stars'])} étoiles")
    print(f"• {len(fusion_combos)} combinaisons fusion générées")
    print(f"• Toutes basées sur Strategic Methods V3 originales")
    
    return fusion_combos, pool_data

if __name__ == "__main__":
    main()