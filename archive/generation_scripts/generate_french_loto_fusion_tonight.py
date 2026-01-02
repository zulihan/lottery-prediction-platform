"""
Générer une combinaison fusion basée sur les 10 combinaisons optimisées
pour le tirage French Loto de ce soir
"""
from collections import Counter
import random

def get_tonight_optimized_combinations():
    """Les 10 combinaisons optimisées pour ce soir"""
    return [
        {'numbers': [3, 6, 10, 24, 31], 'lucky': 3, 'strategy': 'Hot Numbers Enhanced V2'},
        {'numbers': [13, 22, 24, 46, 49], 'lucky': 5, 'strategy': 'Strategic Diversity Improved'},
        {'numbers': [6, 8, 31, 35, 36], 'lucky': 8, 'strategy': 'Trend-Frequency Improved'},
        {'numbers': [6, 15, 26, 32, 38], 'lucky': 2, 'strategy': 'Range Balance Optimized'},
        {'numbers': [3, 21, 25, 27, 31], 'lucky': 1, 'strategy': 'Missing Number Focus'},
        {'numbers': [11, 12, 21, 24, 29], 'lucky': 1, 'strategy': 'Low Lucky Strategy'},
        {'numbers': [3, 7, 28, 31, 36], 'lucky': 2, 'strategy': 'Pattern Replication'},
        {'numbers': [24, 25, 26, 27, 28], 'lucky': 4, 'strategy': 'Coverage Enhancement'},
        {'numbers': [3, 15, 24, 28, 40], 'lucky': 5, 'strategy': 'Risk-Reward Refined'},
        {'numbers': [2, 8, 13, 25, 38], 'lucky': 2, 'strategy': 'Ultimate Fusion V2'}
    ]

def analyze_combination_patterns():
    """Analyser les patterns dans les 10 combinaisons optimisées"""
    
    combinations = get_tonight_optimized_combinations()
    
    all_numbers = []
    all_lucky = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_lucky.append(combo['lucky'])
    
    # Compter les fréquences
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    # Identifier les numéros les plus fréquents
    most_frequent_numbers = [num for num, freq in number_freq.most_common() if freq >= 2]
    single_appearance = [num for num, freq in number_freq.most_common() if freq == 1]
    
    print("📊 ANALYSE DES 10 COMBINAISONS OPTIMISÉES:")
    print(f"Numéros multiples: {most_frequent_numbers}")
    print(f"Fréquences: {[(num, freq) for num, freq in number_freq.most_common() if freq >= 2]}")
    print(f"Lucky par fréquence: {[(lucky, freq) for lucky, freq in lucky_freq.most_common()]}")
    
    return {
        'all_numbers': list(set(all_numbers)),
        'all_lucky': list(set(all_lucky)),
        'most_frequent_numbers': most_frequent_numbers,
        'single_appearance': single_appearance,
        'number_freq': number_freq,
        'lucky_freq': lucky_freq
    }

def generate_fusion_combination(patterns):
    """Générer la combinaison fusion optimale"""
    
    print(f"\n🎯 FUSION DES 10 COMBINAISONS OPTIMISÉES")
    print("Combinaison ultime pour ce soir")
    print("-" * 45)
    
    combinations = get_tonight_optimized_combinations()
    
    # Stratégie de fusion intelligente
    fusion_numbers = []
    
    # 1. Prendre les 3 numéros les plus fréquents
    top_frequent = [num for num, freq in patterns['number_freq'].most_common()[:10] if freq >= 3]
    if len(top_frequent) >= 3:
        fusion_numbers.extend(top_frequent[:3])
    else:
        # Compléter avec les plus fréquents
        top_5_frequent = [num for num, _ in patterns['number_freq'].most_common()[:5]]
        fusion_numbers.extend(top_5_frequent[:3])
    
    # 2. Ajouter 1 numéro de chaque stratégie la plus performante
    priority_strategies = ['Hot Numbers Enhanced V2', 'Strategic Diversity Improved', 'Missing Number Focus']
    
    for strategy_name in priority_strategies:
        strategy_combo = next((combo for combo in combinations if combo['strategy'] == strategy_name), None)
        if strategy_combo:
            available_nums = [n for n in strategy_combo['numbers'] if n not in fusion_numbers]
            if available_nums:
                fusion_numbers.append(random.choice(available_nums))
    
    # 3. Compléter jusqu'à 5 numéros avec les mieux représentés
    while len(fusion_numbers) < 5:
        candidates = [num for num, freq in patterns['number_freq'].most_common() 
                     if num not in fusion_numbers and freq >= 2]
        if candidates:
            fusion_numbers.append(candidates[0])
        else:
            # Fallback sur tous les disponibles
            available = [n for n in patterns['all_numbers'] if n not in fusion_numbers]
            if available:
                fusion_numbers.append(random.choice(available))
    
    numbers = sorted(fusion_numbers[:5])
    
    # Lucky: prendre le plus fréquent
    most_frequent_lucky = patterns['lucky_freq'].most_common()[0][0]
    lucky = most_frequent_lucky
    
    # Analyser les contributions par stratégie
    strategy_contributions = {}
    for combo in combinations:
        matches = [n for n in numbers if n in combo['numbers']]
        if matches:
            strategy_contributions[combo['strategy']] = matches
    
    fusion_combination = {
        'numbers': numbers,
        'lucky': lucky,
        'strategy': 'Optimized Strategic Fusion Tonight',
        'methodology': 'Fusion des 10 combinaisons optimisées',
        'contributions': strategy_contributions
    }
    
    print(f"Numbers: {numbers} | Lucky: {lucky}")
    print(f"Strategy: Optimized Strategic Fusion Tonight")
    print(f"")
    print(f"Contributions par stratégie:")
    for strategy, nums in strategy_contributions.items():
        short_name = strategy.split()[0]
        print(f"  {short_name}: {nums}")
    
    # Analyser la composition
    low = len([n for n in numbers if n <= 16])
    mid = len([n for n in numbers if 17 <= n <= 33])
    high = len([n for n in numbers if n >= 34])
    
    print(f"")
    print(f"Composition:")
    print(f"  Répartition: {low} bas, {mid} mid, {high} high")
    print(f"  Lucky number: {lucky} (fréquence dans les 10 combos: {patterns['lucky_freq'][lucky]})")
    
    return fusion_combination

def validate_fusion_coverage(fusion_combo, patterns):
    """Valider la couverture de la fusion"""
    
    print(f"\n✅ VALIDATION DE LA FUSION:")
    print("-" * 30)
    
    combinations = get_tonight_optimized_combinations()
    
    # Vérifier la représentation de chaque stratégie
    strategy_representation = {}
    for combo in combinations:
        matches = len([n for n in fusion_combo['numbers'] if n in combo['numbers']])
        strategy_representation[combo['strategy']] = matches
    
    print("Représentation par stratégie:")
    for strategy, count in strategy_representation.items():
        short_name = strategy.split()[0]
        print(f"  {short_name}: {count}/5 numéros")
    
    # Score de qualité
    total_representation = sum(strategy_representation.values())
    quality_score = (total_representation / 50) * 100  # 50 = max possible
    
    print(f"")
    print(f"Score de qualité fusion: {quality_score:.1f}%")
    
    # Vérifier l'équilibre
    represented_strategies = sum(1 for count in strategy_representation.values() if count >= 1)
    print(f"Stratégies représentées: {represented_strategies}/10")
    
    # Vérifier la couverture des numéros les plus fréquents
    top_frequent = [num for num, _ in patterns['number_freq'].most_common()[:8]]
    covered_frequent = len([n for n in fusion_combo['numbers'] if n in top_frequent])
    print(f"Couverture top frequent: {covered_frequent}/5")
    
    return quality_score >= 50

def main():
    """Générer la combinaison fusion pour ce soir"""
    
    print("🚀 FUSION COMBINAISON FRENCH LOTO - CE SOIR")
    print("Basée sur les 10 combinaisons optimisées")
    print("=" * 50)
    
    # Analyser les patterns des 10 combinaisons
    patterns = analyze_combination_patterns()
    
    # Générer la fusion
    fusion_combo = generate_fusion_combination(patterns)
    
    # Valider la qualité
    is_valid = validate_fusion_coverage(fusion_combo, patterns)
    
    print(f"\n🎯 COMBINAISON FUSION FINALE POUR CE SOIR:")
    print("=" * 45)
    print(f"Numbers: {fusion_combo['numbers']} | Lucky: {fusion_combo['lucky']}")
    print(f"Strategy: {fusion_combo['strategy']}")
    print(f"Quality: {'✅ EXCELLENTE' if is_valid else '⚠️ ACCEPTABLE'}")
    
    print(f"\n✅ FUSION TERMINÉE:")
    print(f"📊 1 combinaison fusion ultime générée")
    print(f"🎯 Synthèse des 10 combinaisons optimisées")
    print(f"🚀 Prête pour le tirage de ce soir")
    
    return fusion_combo

if __name__ == "__main__":
    main()