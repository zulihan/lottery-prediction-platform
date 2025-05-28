"""
Générer 5 nouveaux sets de combinaisons Euromillions pour le 30 mai 2025
en suivant exactement la même méthodologie que les 5 sets du 27 mai
SANS réutiliser les numéros du tirage d'hier (12, 30, 38, 40, 41)
"""
import psycopg2
import os
import pandas as pd
import numpy as np
import random
from collections import Counter

def load_historical_data():
    """Charger les données historiques depuis PostgreSQL"""
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        
        # Charger les 300 derniers tirages (excluant le 27 mai)
        query = """
        SELECT date, n1, n2, n3, n4, n5, s1, s2 
        FROM euromillions_drawings 
        WHERE date < '2025-05-27'
        ORDER BY date DESC 
        LIMIT 300
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print(f"✅ {len(df)} tirages historiques chargés (excluant 27 mai)")
        return df
        
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return None

def analyze_frequency_patterns(df):
    """Analyser les patterns de fréquence SANS les résultats du 27 mai"""
    
    all_numbers = []
    all_stars = []
    
    for _, row in df.iterrows():
        numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
        stars = [row['s1'], row['s2']]
        
        all_numbers.extend([int(n) for n in numbers if pd.notna(n)])
        all_stars.extend([int(s) for s in stars if pd.notna(s)])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Exclure explicitement les numéros du 27 mai
    excluded_numbers = {12, 30, 38, 40, 41}
    excluded_stars = {4, 12}
    
    # Créer des listes de numéros sans les exclus
    hot_numbers = [num for num, _ in number_freq.most_common(30) if num not in excluded_numbers]
    cold_numbers = [num for num, _ in number_freq.most_common()[-30:] if num not in excluded_numbers]
    hot_stars = [star for star, _ in star_freq.most_common(10) if star not in excluded_stars]
    
    print(f"🔥 Nouveaux numéros chauds: {hot_numbers[:15]}")
    print(f"❄️ Nouveaux numéros froids: {cold_numbers[:15]}")
    print(f"🌟 Nouvelles étoiles chaudes: {hot_stars}")
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'hot_stars': hot_stars,
        'number_freq': number_freq,
        'star_freq': star_freq,
        'excluded_numbers': excluded_numbers,
        'excluded_stars': excluded_stars
    }

def generate_set1_may30_optimized(patterns):
    """SET 1: May 30 Optimized - Style heavy high range SANS numéros d'hier"""
    
    combinations = []
    high_range = [n for n in range(35, 51) if n not in patterns['excluded_numbers']]
    mid_range = [n for n in range(18, 35) if n not in patterns['excluded_numbers']]
    
    # Sélectionner les meilleurs high range
    high_hot = [n for n in patterns['hot_numbers'] if n in high_range][:12]
    mid_hot = [n for n in patterns['hot_numbers'] if n in mid_range][:8]
    
    for i in range(10):
        # 3-4 numéros high range + équilibrage
        high_count = random.choice([3, 4])
        selected_high = random.sample(high_hot[:10], min(high_count, len(high_hot)))
        
        remaining = 5 - high_count
        if remaining > 0:
            selected_mid = random.sample(mid_hot[:6], min(remaining, len(mid_hot)))
        else:
            selected_mid = []
        
        numbers = sorted(selected_high + selected_mid)
        
        # Étoiles SANS 4 et 12
        available_stars = [s for s in patterns['hot_stars'] if s not in patterns['excluded_stars']]
        stars = sorted(random.sample(available_stars[:6], 2))
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'May 30 Heavy High Range V{i+1}'
        })
    
    return combinations

def generate_set2_backtesting_improved_v2(patterns):
    """SET 2: Backtesting Improved V2 - NOUVEAUX numéros gagnants potentiels"""
    
    combinations = []
    
    # Identifier de NOUVEAUX numéros avec fort potentiel
    potential_winners = [n for n in patterns['hot_numbers'][:20] if n not in patterns['excluded_numbers']]
    
    # Prendre les 2 plus prometteurs comme nouveaux "29" et "10"
    new_champion1 = potential_winners[0] if potential_winners else 35
    new_champion2 = potential_winners[1] if len(potential_winners) > 1 else 20
    
    print(f"🏆 Nouveaux champions identifiés: {new_champion1}, {new_champion2}")
    
    for i in range(10):
        # Inclure au moins un des nouveaux champions
        champion_count = random.choice([1, 2])
        selected_champions = [new_champion1] if champion_count == 1 else [new_champion1, new_champion2]
        
        # Compléter avec d'autres numéros prometteurs
        remaining_count = 5 - len(selected_champions)
        available_numbers = [n for n in patterns['hot_numbers'] if n not in selected_champions and n not in patterns['excluded_numbers']]
        selected_others = random.sample(available_numbers[:15], min(remaining_count, len(available_numbers)))
        
        numbers = sorted(selected_champions + selected_others)
        
        # Étoiles prioritaires SANS 4 et 12
        priority_stars = [s for s in patterns['hot_stars'][:4] if s not in patterns['excluded_stars']]
        stars = sorted(random.sample(priority_stars, 2))
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Backtesting Improved V2 #{i+1}'
        })
    
    return combinations

def generate_set3_strategic_methods_v2(patterns):
    """SET 3: Strategic Methods V2 - Risk/Reward, Frequency, Markov, Time Series"""
    
    combinations = []
    
    # 2 Risk/Reward combinations
    for i in range(2):
        risk_level = 'High' if i == 0 else 'Moderate'
        if risk_level == 'High':
            # Plus de numéros froids
            cold_count = 2
            hot_count = 3
        else:
            cold_count = 1
            hot_count = 4
        
        selected_cold = random.sample(patterns['cold_numbers'][:15], cold_count)
        available_hot = [n for n in patterns['hot_numbers'] if n not in selected_cold and n not in patterns['excluded_numbers']]
        selected_hot = random.sample(available_hot[:12], hot_count)
        
        numbers = sorted(selected_cold + selected_hot)
        stars = sorted(random.sample([s for s in patterns['hot_stars'] if s not in patterns['excluded_stars']], 2))
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Risk/Reward Balance - {risk_level} Risk'
        })
    
    # 2 Frequency Analysis combinations
    for i in range(2):
        approach = 'Hot Focus' if i == 0 else 'Hot-Cold Balance'
        if approach == 'Hot Focus':
            selected_numbers = random.sample([n for n in patterns['hot_numbers'] if n not in patterns['excluded_numbers']][:15], 5)
        else:
            hot_nums = random.sample([n for n in patterns['hot_numbers'] if n not in patterns['excluded_numbers']][:12], 3)
            cold_nums = random.sample(patterns['cold_numbers'][:12], 2)
            selected_numbers = sorted(hot_nums + cold_nums)
        
        stars = sorted(random.sample([s for s in patterns['hot_stars'] if s not in patterns['excluded_stars']], 2))
        
        combinations.append({
            'numbers': selected_numbers,
            'stars': stars,
            'strategy': f'Frequency Analysis - {approach}'
        })
    
    # 2 Markov Chain combinations
    for i in range(2):
        # Séquences avec espacement logique
        base_num = random.choice([n for n in patterns['hot_numbers'] if n not in patterns['excluded_numbers']][:10])
        sequence = [base_num]
        
        for _ in range(4):
            next_num = sequence[-1] + random.choice([5, 7, 8, 10, 12])
            if next_num > 50:
                next_num = random.choice([n for n in range(1, 20) if n not in sequence and n not in patterns['excluded_numbers']])
            if next_num not in sequence and next_num not in patterns['excluded_numbers']:
                sequence.append(next_num)
        
        # Compléter si nécessaire
        while len(sequence) < 5:
            available = [n for n in range(1, 51) if n not in sequence and n not in patterns['excluded_numbers']]
            sequence.append(random.choice(available))
        
        numbers = sorted(sequence[:5])
        pattern_type = 'Sequential Patterns' if i == 0 else 'Transition Probability'
        stars = sorted(random.sample([s for s in patterns['hot_stars'] if s not in patterns['excluded_stars']], 2))
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Markov Chain - {pattern_type}'
        })
    
    # 2 Time Series combinations
    for i in range(2):
        analysis_type = 'Trend Analysis' if i == 0 else 'Seasonal Patterns'
        
        # Trend: numéros en progression
        if analysis_type == 'Trend Analysis':
            start_num = random.choice([n for n in patterns['hot_numbers'] if n not in patterns['excluded_numbers']][:8])
            numbers = []
            current = start_num
            for _ in range(5):
                if current <= 50 and current not in patterns['excluded_numbers']:
                    numbers.append(current)
                current += random.choice([3, 5, 7])
                if current > 50:
                    # Prendre un numéro aléatoire disponible
                    available = [n for n in range(1, 51) if n not in numbers and n not in patterns['excluded_numbers']]
                    if available:
                        numbers.append(random.choice(available))
            
            numbers = sorted(numbers[:5])
        else:
            # Seasonal: mix équilibré par range
            low_num = random.choice([n for n in range(1, 17) if n not in patterns['excluded_numbers']])
            mid_nums = random.sample([n for n in range(18, 34) if n not in patterns['excluded_numbers']], 2)
            high_nums = random.sample([n for n in range(35, 50) if n not in patterns['excluded_numbers']], 2)
            numbers = sorted([low_num] + mid_nums + high_nums)
        
        stars = sorted(random.sample([s for s in patterns['hot_stars'] if s not in patterns['excluded_stars']], 2))
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Time Series - {analysis_type}'
        })
    
    # 2 Coverage Optimization combinations
    for i in range(2):
        mix_type = 'Balanced Mix' if i == 0 else 'Diversified Mix'
        
        # Mélange équilibré de toutes les approches
        hot_nums = random.sample([n for n in patterns['hot_numbers'] if n not in patterns['excluded_numbers']][:10], 2)
        cold_nums = random.sample(patterns['cold_numbers'][:10], 1)
        mid_nums = random.sample([n for n in range(20, 35) if n not in patterns['excluded_numbers']], 2)
        
        numbers = sorted(hot_nums + cold_nums + mid_nums)
        stars = sorted(random.sample([s for s in patterns['hot_stars'] if s not in patterns['excluded_stars']], 2))
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Coverage Optimization - {mix_type}'
        })
    
    return combinations

def generate_set4_ultimate_mix_v2(patterns):
    """SET 4: Ultimate Mix V2 - Fusion des 3 premiers sets"""
    
    combinations = []
    
    # Analyser les numéros les plus prometteurs des sets précédents
    top_candidates = [n for n in patterns['hot_numbers'][:15] if n not in patterns['excluded_numbers']]
    
    for i in range(3):
        # Fusion intelligente des méthodologies
        if i == 0:  # Frequency Champions
            selected_numbers = random.sample(top_candidates[:10], 5)
            strategy_name = 'Ultimate Mix - Frequency Champions V2'
        elif i == 1:  # High Performance Fusion
            high_range_candidates = [n for n in top_candidates if n >= 35]
            mid_range_candidates = [n for n in top_candidates if 20 <= n <= 34]
            selected_numbers = random.sample(high_range_candidates[:6], 3) + random.sample(mid_range_candidates[:6], 2)
            selected_numbers = sorted(selected_numbers)
            strategy_name = 'Ultimate Mix - High Performance Fusion V2'
        else:  # Strategic Balance Supreme
            # Équilibre parfait entre tous les ranges
            low_candidates = [n for n in range(1, 18) if n not in patterns['excluded_numbers'] and patterns['number_freq'].get(n, 0) > 0]
            mid_candidates = [n for n in range(18, 35) if n not in patterns['excluded_numbers'] and n in patterns['hot_numbers']]
            high_candidates = [n for n in range(35, 51) if n not in patterns['excluded_numbers'] and n in patterns['hot_numbers']]
            
            selected_numbers = (
                random.sample(low_candidates[:8], 1) +
                random.sample(mid_candidates[:8], 2) +
                random.sample(high_candidates[:8], 2)
            )
            selected_numbers = sorted(selected_numbers)
            strategy_name = 'Ultimate Mix - Strategic Balance Supreme V2'
        
        # Étoiles optimales
        optimal_stars = [s for s in patterns['hot_stars'][:3] if s not in patterns['excluded_stars']]
        stars = sorted(random.sample(optimal_stars, 2))
        
        combinations.append({
            'numbers': selected_numbers,
            'stars': stars,
            'strategy': strategy_name
        })
    
    return combinations

def generate_set5_mixed_strategy_v2(patterns):
    """SET 5: Mixed Strategy V2 - Hot-Cold Balance SANS numéros d'hier"""
    
    combinations = []
    
    # Hot-Cold balancing 70% hot, 30% cold
    hot_pool = [n for n in patterns['hot_numbers'][:20] if n not in patterns['excluded_numbers']]
    cold_pool = [n for n in patterns['cold_numbers'][:20] if n not in patterns['excluded_numbers']]
    
    strategies = [
        'Hot Emphasis', 'Balanced', 'Cold Balance', 'Frequency Optimized',
        'Diversity Focus', 'Strategic Balance', 'Pattern Variation',
        'Adaptive Mix', 'Range Optimized', 'Ultimate Balance'
    ]
    
    for i in range(10):
        strategy_name = strategies[i]
        
        # Varier le ratio hot/cold selon la stratégie
        if 'Hot' in strategy_name:
            hot_count = 4
            cold_count = 1
        elif 'Cold' in strategy_name:
            hot_count = 2
            cold_count = 3
        else:
            hot_count = 3
            cold_count = 2
        
        selected_hot = random.sample(hot_pool[:15], min(hot_count, len(hot_pool)))
        selected_cold = random.sample(cold_pool[:15], min(cold_count, len(cold_pool)))
        
        numbers = sorted(selected_hot + selected_cold)
        
        # Étoiles avec balance hot/cold
        hot_stars = [s for s in patterns['hot_stars'][:4] if s not in patterns['excluded_stars']]
        cold_stars = [s for s in range(1, 13) if s not in hot_stars and s not in patterns['excluded_stars']]
        
        star1 = random.choice(hot_stars[:3])
        star2 = random.choice(cold_stars[:3])
        stars = sorted([star1, star2])
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Mixed Strategy - {strategy_name}'
        })
    
    return combinations

def main():
    """Générer les 5 nouveaux sets pour le 30 mai 2025"""
    
    print("🚀 GÉNÉRATION DES 5 NOUVEAUX SETS EUROMILLIONS - 30 MAI 2025")
    print("EXCLUSION TOTALE des numéros du 27 mai: 12, 30, 38, 40, 41")
    print("=" * 75)
    
    # Charger les données (sans le 27 mai)
    df = load_historical_data()
    if df is None:
        return None
    
    # Analyser les nouveaux patterns
    print("\n📊 ANALYSE DES NOUVEAUX PATTERNS (SANS 27 MAI):")
    patterns = analyze_frequency_patterns(df)
    
    print(f"\n🚀 GÉNÉRATION DES 5 SETS COMPLETS:")
    print("-" * 50)
    
    all_sets = []
    
    # SET 1: May 30 Optimized
    print("✅ SET 1: May 30 Optimized (10 combinaisons)")
    set1 = generate_set1_may30_optimized(patterns)
    all_sets.append(('SET 1: May 30 Optimized', set1))
    
    # SET 2: Backtesting Improved V2
    print("✅ SET 2: Backtesting Improved V2 (10 combinaisons)")
    set2 = generate_set2_backtesting_improved_v2(patterns)
    all_sets.append(('SET 2: Backtesting Improved V2', set2))
    
    # SET 3: Strategic Methods V2
    print("✅ SET 3: Strategic Methods V2 (10 combinaisons)")
    set3 = generate_set3_strategic_methods_v2(patterns)
    all_sets.append(('SET 3: Strategic Methods V2', set3))
    
    # SET 4: Ultimate Mix V2
    print("✅ SET 4: Ultimate Mix V2 (3 combinaisons)")
    set4 = generate_set4_ultimate_mix_v2(patterns)
    all_sets.append(('SET 4: Ultimate Mix V2', set4))
    
    # SET 5: Mixed Strategy V2
    print("✅ SET 5: Mixed Strategy V2 (10 combinaisons)")
    set5 = generate_set5_mixed_strategy_v2(patterns)
    all_sets.append(('SET 5: Mixed Strategy V2', set5))
    
    # Afficher tous les sets
    total_combinations = 0
    for set_name, combinations in all_sets:
        print(f"\n🎯 {set_name}")
        print("=" * len(set_name) + "====")
        
        for i, combo in enumerate(combinations, 1):
            print(f"{total_combinations + i:2d}. {combo['strategy']}")
            print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
            
            # Vérifier qu'aucun numéro exclu n'est présent
            excluded_found = [n for n in combo['numbers'] if n in patterns['excluded_numbers']]
            excluded_stars = [s for s in combo['stars'] if s in patterns['excluded_stars']]
            
            if excluded_found or excluded_stars:
                print(f"    ⚠️ ERREUR: Contient des numéros exclus!")
            else:
                print(f"    ✅ Nouvelle combinaison valide")
            print()
        
        total_combinations += len(combinations)
    
    print(f"\n🎯 RÉCAPITULATIF:")
    print(f"✅ {total_combinations} nouvelles combinaisons générées")
    print(f"✅ AUCUN numéro du 27 mai inclus: {patterns['excluded_numbers']}")
    print(f"✅ AUCUNE étoile du 27 mai incluse: {patterns['excluded_stars']}")
    print(f"✅ Méthodologie identique aux 5 sets précédents")
    print(f"🚀 Prêt pour le tirage du 30 mai 2025!")
    
    return all_sets

if __name__ == "__main__":
    main()