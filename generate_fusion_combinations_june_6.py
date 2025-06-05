"""
Générer 10 combinaisons fusion pour le 6 juin 2025
Mixing strategy: Fusionner les 10 combinaisons optimisées en nouvelles combinaisons hybrides
"""
import os
from sqlalchemy import create_engine, text
import pandas as pd
from collections import Counter
import random

def get_base_combinations():
    """Les 10 combinaisons optimisées de base à fusionner"""
    
    base_combinations = [
        {
            'name': 'Coverage Optimization Enhanced',
            'numbers': [12, 15, 38, 47, 49],
            'stars': [5, 7],
            'strategy_type': 'coverage',
            'strength': 'extreme_high_focus'
        },
        {
            'name': 'Frequency Analysis Ultimate',
            'numbers': [23, 44, 19, 50],
            'stars': [3, 7],
            'strategy_type': 'frequency',
            'strength': 'high_frequency'
        },
        {
            'name': 'Recent Trends Analysis',
            'numbers': [47, 29, 15, 49],
            'stars': [5, 12],
            'strategy_type': 'recent',
            'strength': 'trend_based'
        },
        {
            'name': 'High-Range Pattern',
            'numbers': [10, 44, 50, 42, 37],
            'stars': [7, 2],
            'strategy_type': 'range',
            'strength': 'high_concentration'
        },
        {
            'name': 'Star 7 Priority',
            'numbers': [15, 38, 23, 44, 19],
            'stars': [7, 3],
            'strategy_type': 'star_focus',
            'strength': 'star_optimization'
        },
        {
            'name': 'Extreme High Focus',
            'numbers': [23, 44, 50, 45],
            'stars': [5, 7],
            'strategy_type': 'extreme',
            'strength': 'extreme_numbers'
        },
        {
            'name': 'Hot-Cold Balance',
            'numbers': [23, 44, 19, 16, 48],
            'stars': [7, 8],
            'strategy_type': 'balance',
            'strength': 'balanced_approach'
        },
        {
            'name': 'Time Series Pattern',
            'numbers': [23, 32, 39, 42, 46],
            'stars': [5, 7],
            'strategy_type': 'pattern',
            'strength': 'mathematical_progression'
        },
        {
            'name': 'Coverage Maximizer',
            'numbers': [23, 44, 19, 10],
            'stars': [7, 3],
            'strategy_type': 'coverage',
            'strength': 'range_diversity'
        },
        {
            'name': 'Ultimate Synthesis',
            'numbers': [12, 38, 23, 44, 19],
            'stars': [5, 7],
            'strategy_type': 'synthesis',
            'strength': 'multi_strategy'
        }
    ]
    
    return base_combinations

def analyze_fusion_opportunities(base_combinations):
    """Analyser les opportunités de fusion entre stratégies"""
    
    print(f"🔬 ANALYSE DES OPPORTUNITÉS DE FUSION")
    print("=" * 40)
    
    # Analyser la distribution des numéros
    all_numbers = []
    all_stars = []
    
    for combo in base_combinations:
        all_numbers.extend(combo['numbers'])
        all_stars.extend(combo['stars'])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    print(f"📊 FRÉQUENCES DANS LES 10 COMBINAISONS DE BASE:")
    print(f"Top numéros: {number_freq.most_common(10)}")
    print(f"Étoiles: {star_freq.most_common()}")
    
    # Identifier les gaps
    all_possible_numbers = set(range(1, 51))
    used_numbers = set(all_numbers)
    missing_numbers = all_possible_numbers - used_numbers
    
    all_possible_stars = set(range(1, 13))
    used_stars = set(all_stars)
    missing_stars = all_possible_stars - used_stars
    
    print(f"\n🎯 GAPS À COMBLER:")
    print(f"Numéros manquants: {sorted(missing_numbers)}")
    print(f"Étoiles manquantes: {sorted(missing_stars)}")
    
    return {
        'number_freq': number_freq,
        'star_freq': star_freq,
        'missing_numbers': missing_numbers,
        'missing_stars': missing_stars,
        'high_freq_numbers': [num for num, count in number_freq.most_common(15)],
        'high_freq_stars': [star for star, count in star_freq.most_common(6)]
    }

def create_fusion_combinations(base_combinations, analysis):
    """Créer 10 combinaisons fusion innovantes"""
    
    print(f"\n🧬 GÉNÉRATION DES COMBINAISONS FUSION")
    print("=" * 42)
    
    fusion_combinations = []
    
    # 1. Fusion Frequency + Coverage
    freq_nums = [23, 44, 19]  # Les plus fréquents
    coverage_nums = [12, 38]  # De Coverage Optimization
    
    fusion1 = {
        'numbers': freq_nums + coverage_nums,
        'stars': [7, 3],  # Star 7 prioritaire + étoile fréquente
        'strategy': 'Frequency-Coverage Fusion',
        'method': 'Top fréquents + gagnants June 3 optimaux',
        'parent_strategies': ['Frequency Analysis', 'Coverage Optimization']
    }
    fusion_combinations.append(fusion1)
    
    # 2. Fusion Extreme + Balance
    extreme_nums = [50, 49, 48]  # Extreme high
    balance_nums = [16, 29]      # De Hot-Cold Balance
    
    fusion2 = {
        'numbers': extreme_nums + balance_nums,
        'stars': [5, 8],
        'strategy': 'Extreme-Balance Fusion',
        'method': 'Extreme high + équilibrage froid',
        'parent_strategies': ['Extreme High Focus', 'Hot-Cold Balance']
    }
    fusion_combinations.append(fusion2)
    
    # 3. Fusion Pattern + Range
    pattern_nums = [32, 39, 42]  # De Time Series
    range_nums = [10, 37]        # De High-Range Pattern
    
    fusion3 = {
        'numbers': pattern_nums + range_nums,
        'stars': [7, 2],
        'strategy': 'Pattern-Range Fusion',
        'method': 'Progression mathématique + distribution range',
        'parent_strategies': ['Time Series Pattern', 'High-Range Pattern']
    }
    fusion_combinations.append(fusion3)
    
    # 4. Fusion Recent + Synthesis
    recent_nums = [47, 15]       # De Recent Trends
    synthesis_nums = [12, 23, 44]  # De Ultimate Synthesis
    
    fusion4 = {
        'numbers': recent_nums + synthesis_nums,
        'stars': [5, 12],
        'strategy': 'Recent-Synthesis Fusion',
        'method': 'Tendances récentes + synthèse multi-stratégies',
        'parent_strategies': ['Recent Trends', 'Ultimate Synthesis']
    }
    fusion_combinations.append(fusion4)
    
    # 5. Fusion Triple Strategy (Coverage + Frequency + Extreme)
    triple_nums = [12, 23, 50, 38, 44]  # Mix des 3 stratégies
    
    fusion5 = {
        'numbers': triple_nums,
        'stars': [7, 5],  # Les 2 stars les plus importantes
        'strategy': 'Triple Strategy Fusion',
        'method': 'Coverage + Frequency + Extreme unified',
        'parent_strategies': ['Coverage', 'Frequency', 'Extreme']
    }
    fusion_combinations.append(fusion5)
    
    # 6. Fusion Gap Coverage (utiliser les numéros manquants)
    gap_nums = list(analysis['missing_numbers'])[:3]
    frequent_nums = analysis['high_freq_numbers'][:2]
    
    fusion6 = {
        'numbers': frequent_nums + gap_nums,
        'stars': [7, list(analysis['missing_stars'])[0] if analysis['missing_stars'] else 11],
        'strategy': 'Gap Coverage Fusion',
        'method': 'Numéros fréquents + gaps non couverts',
        'parent_strategies': ['Coverage Maximizer', 'Gap Analysis']
    }
    fusion_combinations.append(fusion6)
    
    # 7. Fusion Star Optimization
    star_7_combos = [combo for combo in base_combinations if 7 in combo['stars']]
    selected_nums = []
    for combo in star_7_combos[:3]:
        selected_nums.extend(combo['numbers'][:2])
    selected_nums = list(set(selected_nums))[:5]
    
    fusion7 = {
        'numbers': selected_nums,
        'stars': [7, 5],  # Focus total sur stars gagnantes June 3
        'strategy': 'Star Optimization Fusion',
        'method': 'Numéros des combinaisons avec star 7',
        'parent_strategies': ['Star 7 Priority', 'Coverage Optimization']
    }
    fusion_combinations.append(fusion7)
    
    # 8. Fusion Mathematical Progression Enhanced
    progression_base = 23  # Numéro le plus fréquent
    progression_nums = [progression_base]
    for i in range(4):
        next_num = progression_base + (i + 1) * 7  # Progression par 7
        if next_num > 50:
            next_num = next_num - 50 + random.choice([1, 2, 3])
        if next_num not in progression_nums and 1 <= next_num <= 50:
            progression_nums.append(next_num)
    
    while len(progression_nums) < 5:
        add_num = random.choice(analysis['high_freq_numbers'])
        if add_num not in progression_nums:
            progression_nums.append(add_num)
    
    fusion8 = {
        'numbers': sorted(progression_nums[:5]),
        'stars': [3, 7],  # Mix des étoiles fréquentes
        'strategy': 'Mathematical Progression Enhanced',
        'method': 'Progression par 7 depuis numéro le plus fréquent',
        'parent_strategies': ['Time Series Pattern', 'Frequency Analysis']
    }
    fusion_combinations.append(fusion8)
    
    # 9. Fusion High Performance Mix
    # Combiner les numéros des stratégies qui ont eu les meilleurs scores
    high_perf_nums = [12, 15, 38, 23, 44]  # Des meilleures stratégies
    
    fusion9 = {
        'numbers': high_perf_nums,
        'stars': [7, 3],
        'strategy': 'High Performance Mix',
        'method': 'Numéros des stratégies les plus performantes June 3',
        'parent_strategies': ['Coverage Optimization', 'Frequency Analysis']
    }
    fusion_combinations.append(fusion9)
    
    # 10. Fusion Ultimate Diversity
    # Maximiser la diversité en prenant 1 numéro de chaque range
    low_range = [num for num in analysis['high_freq_numbers'] if num <= 17][:1]
    mid_range = [num for num in analysis['high_freq_numbers'] if 18 <= num <= 34][:2]
    high_range = [num for num in analysis['high_freq_numbers'] if num >= 35][:2]
    
    fusion10 = {
        'numbers': low_range + mid_range + high_range,
        'stars': [5, 7],  # Stars gagnantes June 3
        'strategy': 'Ultimate Diversity Fusion',
        'method': 'Diversité maximale avec numéros fréquents',
        'parent_strategies': ['Coverage Maximizer', 'Hot-Cold Balance']
    }
    fusion_combinations.append(fusion10)
    
    return fusion_combinations

def display_fusion_results(fusion_combinations, analysis):
    """Afficher les résultats des combinaisons fusion"""
    
    print(f"\n🎯 10 COMBINAISONS FUSION - EUROMILLIONS 6 JUIN 2025")
    print(f"Stratégie: Fusion intelligente des 10 combinaisons optimisées")
    print("=" * 65)
    
    for i, combo in enumerate(fusion_combinations, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print(f"    Method: {combo['method']}")
        print(f"    Parents: {', '.join(combo['parent_strategies'])}")
        
        # Analyse de la distribution
        low = len([n for n in combo['numbers'] if n <= 17])
        mid = len([n for n in combo['numbers'] if 18 <= n <= 34])
        high = len([n for n in combo['numbers'] if n >= 35])
        extreme_high = len([n for n in combo['numbers'] if n >= 45])
        has_star_7 = 7 in combo['stars']
        has_star_5 = 5 in combo['stars']
        
        print(f"    Distribution: {low} low, {mid} mid, {high} high ({extreme_high} extreme)")
        print(f"    Stars: 7: {'✓' if has_star_7 else '✗'} | 5: {'✓' if has_star_5 else '✗'}")
        print()
    
    # Métriques finales
    all_fusion_numbers = set()
    all_fusion_stars = set()
    star_7_count = 0
    star_5_count = 0
    
    for combo in fusion_combinations:
        all_fusion_numbers.update(combo['numbers'])
        all_fusion_stars.update(combo['stars'])
        if 7 in combo['stars']:
            star_7_count += 1
        if 5 in combo['stars']:
            star_5_count += 1
    
    extreme_coverage = [n for n in all_fusion_numbers if n >= 45]
    
    print(f"📊 MÉTRIQUES FUSION FINALES:")
    print(f"    Numéros uniques couverts: {len(all_fusion_numbers)}/50")
    print(f"    Étoiles uniques couvertes: {len(all_fusion_stars)}/12")
    print(f"    Étoile 7 coverage: {star_7_count}/10 ({star_7_count*10}%)")
    print(f"    Étoile 5 coverage: {star_5_count}/10 ({star_5_count*10}%)")
    print(f"    Extreme high coverage: {len(extreme_coverage)}/6 numbers")
    print(f"    Ranges: {sorted(extreme_coverage)}")

def main():
    """Fonction principale de génération fusion"""
    
    print("🧬 EUROMILLIONS FUSION STRATEGY - 6 JUIN 2025")
    print("Fusion intelligente des 10 combinaisons optimisées")
    print("=" * 55)
    
    # Récupérer les combinaisons de base
    base_combinations = get_base_combinations()
    
    # Analyser les opportunités de fusion
    analysis = analyze_fusion_opportunities(base_combinations)
    
    # Créer les combinaisons fusion
    fusion_combinations = create_fusion_combinations(base_combinations, analysis)
    
    # Afficher les résultats
    display_fusion_results(fusion_combinations, analysis)
    
    print(f"\n✅ AVANTAGES DE LA STRATÉGIE FUSION:")
    print(f"   Diversité maximisée: Combine les forces de chaque stratégie")
    print(f"   Gaps comblés: Couvre les numéros/étoiles manquants")
    print(f"   Équilibrage optimal: Balance fréquence + couverture + patterns")
    print(f"   Innovation: Nouvelles combinaisons non présentes dans les sets originaux")
    print(f"   Total combinaisons: 20 (10 optimisées + 10 fusion)")
    
    return fusion_combinations

if __name__ == "__main__":
    main()