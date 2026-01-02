"""
Générer 9 combinaisons fusion supplémentaires basées sur les 10 combinaisons optimisées
en utilisant différentes stratégies de fusion
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

def analyze_patterns():
    """Analyser les patterns des 10 combinaisons"""
    combinations = get_tonight_optimized_combinations()
    
    all_numbers = []
    all_lucky = []
    
    for combo in combinations:
        all_numbers.extend(combo['numbers'])
        all_lucky.append(combo['lucky'])
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    return {
        'combinations': combinations,
        'number_freq': number_freq,
        'lucky_freq': lucky_freq,
        'all_numbers': list(set(all_numbers)),
        'all_lucky': list(set(all_lucky))
    }

def generate_9_fusion_combinations(patterns):
    """Générer 9 combinaisons fusion avec différentes stratégies"""
    
    print("🎯 GÉNÉRATION DE 9 COMBINAISONS FUSION SUPPLÉMENTAIRES")
    print("Différentes stratégies de fusion des 10 combinaisons optimisées")
    print("-" * 65)
    
    fusion_combinations = []
    combinations = patterns['combinations']
    
    # 1. Frequency Champions Fusion V2
    top_frequent = [num for num, _ in patterns['number_freq'].most_common()[:7]]
    selected = sorted(random.sample(top_frequent, 5))
    lucky = patterns['lucky_freq'].most_common()[0][0]
    
    fusion_combinations.append({
        'numbers': selected,
        'lucky': lucky,
        'strategy': 'Frequency Champions Fusion V2',
        'method': 'Top 5 most frequent numbers'
    })
    
    # 2. Strategy Diversity Fusion
    # Un numéro de chaque stratégie différente
    diverse_pick = []
    strategy_groups = [
        combinations[0]['numbers'],  # Hot Numbers
        combinations[1]['numbers'],  # Strategic Diversity
        combinations[2]['numbers'],  # Trend-Frequency
        combinations[4]['numbers'],  # Missing Number
        combinations[7]['numbers']   # Coverage Enhancement
    ]
    
    for group in strategy_groups:
        available = [n for n in group if n not in diverse_pick]
        if available:
            diverse_pick.append(random.choice(available))
    
    fusion_combinations.append({
        'numbers': sorted(diverse_pick[:5]),
        'lucky': random.choice([1, 2, 5]),
        'strategy': 'Strategy Diversity Fusion',
        'method': 'One number per strategy type'
    })
    
    # 3. Range Balancer Fusion
    # Équilibrer les ranges selon le pattern gagnant (2 bas, 2 mid, 1 haut)
    low_numbers = [n for n in patterns['all_numbers'] if n <= 16]
    mid_numbers = [n for n in patterns['all_numbers'] if 17 <= n <= 33]
    high_numbers = [n for n in patterns['all_numbers'] if n >= 34]
    
    range_balanced = (
        random.sample(low_numbers, 2) +
        random.sample(mid_numbers, 2) +
        random.sample(high_numbers, 1)
    )
    
    fusion_combinations.append({
        'numbers': sorted(range_balanced),
        'lucky': 2,  # Lucky du pattern gagnant
        'strategy': 'Range Balancer Fusion',
        'method': '2 low + 2 mid + 1 high (winning pattern)'
    })
    
    # 4. Hot-Cold Equilibrium Fusion
    # Mix des numéros les plus et moins fréquents
    hot_picks = [num for num, _ in patterns['number_freq'].most_common()[:8]]
    cold_picks = [num for num, _ in patterns['number_freq'].most_common()[-8:]]
    
    equilibrium = sorted(random.sample(hot_picks, 3) + random.sample(cold_picks, 2))
    
    fusion_combinations.append({
        'numbers': equilibrium,
        'lucky': random.choice([1, 3, 8]),
        'strategy': 'Hot-Cold Equilibrium Fusion',
        'method': '3 hot + 2 cold numbers'
    })
    
    # 5. Lucky Priority Fusion
    # Focus sur les lucky numbers les plus fréquents
    lucky_priority_combos = [combo for combo in combinations if combo['lucky'] in [1, 2, 5]]
    lucky_numbers = []
    for combo in lucky_priority_combos[:3]:
        available = [n for n in combo['numbers'] if n not in lucky_numbers]
        if available:
            lucky_numbers.extend(random.sample(available, min(2, len(available))))
    
    while len(lucky_numbers) < 5:
        available = [n for n in patterns['all_numbers'] if n not in lucky_numbers]
        lucky_numbers.append(random.choice(available))
    
    fusion_combinations.append({
        'numbers': sorted(lucky_numbers[:5]),
        'lucky': 1,  # Lucky le plus fréquent après 2
        'strategy': 'Lucky Priority Fusion',
        'method': 'From combinations with priority lucky numbers'
    })
    
    # 6. Sequential Pattern Fusion
    # Numéros en progression logique
    base_num = random.choice([num for num, freq in patterns['number_freq'].most_common()[:5]])
    sequential = [base_num]
    current = base_num
    
    for _ in range(4):
        next_num = current + random.choice([3, 5, 7, 9])
        if next_num > 49:
            next_num = random.choice(range(1, 20))
        if next_num not in sequential and next_num in patterns['all_numbers']:
            sequential.append(next_num)
            current = next_num
    
    while len(sequential) < 5:
        available = [n for n in patterns['all_numbers'] if n not in sequential]
        sequential.append(random.choice(available))
    
    fusion_combinations.append({
        'numbers': sorted(sequential[:5]),
        'lucky': random.choice([2, 4, 8]),
        'strategy': 'Sequential Pattern Fusion',
        'method': 'Progressive number sequence'
    })
    
    # 7. Coverage Maximizer Fusion
    # Couvrir le maximum de stratégies
    coverage_numbers = []
    for combo in combinations:
        available = [n for n in combo['numbers'] if n not in coverage_numbers]
        if available and len(coverage_numbers) < 5:
            coverage_numbers.append(available[0])
    
    fusion_combinations.append({
        'numbers': sorted(coverage_numbers[:5]),
        'lucky': patterns['lucky_freq'].most_common()[1][0],  # 2ème plus fréquent
        'strategy': 'Coverage Maximizer Fusion',
        'method': 'One number from each combination'
    })
    
    # 8. Balanced Distribution Fusion
    # Distribution équilibrée par fréquence
    ultra_frequent = [num for num, freq in patterns['number_freq'].most_common() if freq >= 4]
    frequent = [num for num, freq in patterns['number_freq'].most_common() if 2 <= freq < 4]
    single = [num for num, freq in patterns['number_freq'].most_common() if freq == 1]
    
    balanced = (
        random.sample(ultra_frequent[:4], min(2, len(ultra_frequent))) +
        random.sample(frequent[:8], min(2, len(frequent))) +
        random.sample(single[:5], min(1, len(single)))
    )
    
    fusion_combinations.append({
        'numbers': sorted(balanced[:5]),
        'lucky': random.choice([2, 5]),
        'strategy': 'Balanced Distribution Fusion',
        'method': 'Frequency-balanced selection'
    })
    
    # 9. Ultimate Synthesis Fusion
    # Synthèse ultime de tous les meilleurs éléments
    best_elements = []
    
    # Les 3 numéros les plus fréquents
    best_elements.extend([num for num, _ in patterns['number_freq'].most_common()[:3]])
    
    # 1 numéro de la meilleure stratégie (Hot Numbers)
    hot_strategy_nums = [n for n in combinations[0]['numbers'] if n not in best_elements]
    if hot_strategy_nums:
        best_elements.append(random.choice(hot_strategy_nums))
    
    # 1 numéro pour équilibrer les ranges
    if not any(n >= 34 for n in best_elements):
        high_candidates = [n for n in patterns['all_numbers'] if n >= 34 and n not in best_elements]
        if high_candidates:
            best_elements.append(random.choice(high_candidates))
    
    fusion_combinations.append({
        'numbers': sorted(best_elements[:5]),
        'lucky': 2,  # Lucky du pattern gagnant
        'strategy': 'Ultimate Synthesis Fusion',
        'method': 'Best elements synthesis'
    })
    
    return fusion_combinations

def display_fusion_combinations(fusion_combos):
    """Afficher les 9 combinaisons fusion"""
    
    print(f"\n🏆 9 COMBINAISONS FUSION SUPPLÉMENTAIRES:")
    print("=" * 55)
    
    for i, combo in enumerate(fusion_combos, 2):  # Commencer à 2 car on a déjà la #1
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        print(f"    Method: {combo['method']}")
        
        # Analyser la composition
        low = len([n for n in combo['numbers'] if n <= 16])
        mid = len([n for n in combo['numbers'] if 17 <= n <= 33])
        high = len([n for n in combo['numbers'] if n >= 34])
        
        print(f"    Répartition: {low} bas, {mid} mid, {high} high")
        print()

def analyze_fusion_distribution(fusion_combos):
    """Analyser la distribution globale des fusions"""
    
    print("📊 ANALYSE GLOBALE DES 9 FUSIONS:")
    print("-" * 40)
    
    all_fusion_numbers = []
    all_fusion_lucky = []
    
    for combo in fusion_combos:
        all_fusion_numbers.extend(combo['numbers'])
        all_fusion_lucky.append(combo['lucky'])
    
    fusion_number_freq = Counter(all_fusion_numbers)
    fusion_lucky_freq = Counter(all_fusion_lucky)
    
    print("Distribution Lucky Numbers:")
    for lucky, count in sorted(fusion_lucky_freq.items()):
        print(f"  Lucky {lucky}: {count} fois")
    
    print(f"\nTop 5 numéros dans les fusions:")
    for num, count in fusion_number_freq.most_common()[:5]:
        print(f"  {num}: {count} fois")

def main():
    """Générer les 9 combinaisons fusion supplémentaires"""
    
    print("🚀 GÉNÉRATION 9 FUSIONS SUPPLÉMENTAIRES - FRENCH LOTO")
    print("Basées sur les 10 combinaisons optimisées pour ce soir")
    print("=" * 60)
    
    # Analyser les patterns
    patterns = analyze_patterns()
    
    # Générer les 9 fusions
    fusion_combos = generate_9_fusion_combinations(patterns)
    
    # Afficher les combinaisons
    display_fusion_combinations(fusion_combos)
    
    # Analyser la distribution
    analyze_fusion_distribution(fusion_combos)
    
    print(f"\n✅ GÉNÉRATION TERMINÉE:")
    print(f"📊 9 combinaisons fusion supplémentaires créées")
    print(f"🎯 Total avec la première: 10 fusions différentes")
    print(f"🚀 Variété de stratégies pour maximiser les chances")
    
    return fusion_combos

if __name__ == "__main__":
    main()