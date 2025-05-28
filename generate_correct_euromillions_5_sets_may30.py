"""
Générer 5 nouveaux sets de combinaisons Euromillions pour le 30 mai 2025
en suivant la méthodologie des 5 sets du 27 mai
SANS exclure les numéros, mais en évitant qu'ils apparaissent tous ensemble
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
        
        # Charger les 300 derniers tirages
        query = """
        SELECT date, n1, n2, n3, n4, n5, s1, s2 
        FROM euromillions_drawings 
        ORDER BY date DESC 
        LIMIT 300
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print(f"✅ {len(df)} tirages historiques chargés")
        return df
        
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return None

def analyze_frequency_patterns(df):
    """Analyser les patterns de fréquence incluant TOUS les numéros"""
    
    all_numbers = []
    all_stars = []
    
    for _, row in df.iterrows():
        numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
        stars = [row['s1'], row['s2']]
        
        all_numbers.extend([int(n) for n in numbers if pd.notna(n)])
        all_stars.extend([int(s) for s in stars if pd.notna(s)])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Numéros du 27 mai pour éviter concentration excessive
    may27_numbers = {12, 30, 38, 40, 41}
    may27_stars = {4, 12}
    
    hot_numbers = [num for num, _ in number_freq.most_common(25)]
    cold_numbers = [num for num, _ in number_freq.most_common()[-25:]]
    hot_stars = [star for star, _ in star_freq.most_common(10)]
    
    print(f"🔥 Numéros chauds: {hot_numbers[:15]}")
    print(f"❄️ Numéros froids: {cold_numbers[:15]}")
    print(f"🌟 Étoiles chaudes: {hot_stars}")
    print(f"⚠️ Numéros du 27 mai à utiliser modérément: {may27_numbers}")
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'hot_stars': hot_stars,
        'number_freq': number_freq,
        'star_freq': star_freq,
        'may27_numbers': may27_numbers,
        'may27_stars': may27_stars
    }

def check_may27_concentration(numbers, stars, patterns):
    """Vérifier si une combinaison a trop de numéros du 27 mai"""
    may27_count = len([n for n in numbers if n in patterns['may27_numbers']])
    may27_star_count = len([s for s in stars if s in patterns['may27_stars']])
    
    # Limiter à maximum 2 numéros du 27 mai par combinaison
    return may27_count <= 2 and may27_star_count <= 1

def generate_set1_may30_optimized(patterns):
    """SET 1: May 30 Optimized - Style heavy high range"""
    
    combinations = []
    high_range = [n for n in range(35, 51)]
    mid_range = [n for n in range(18, 35)]
    
    # Sélectionner les meilleurs high range (incluant 38, 40, 41 si chauds)
    high_hot = [n for n in patterns['hot_numbers'] if n in high_range][:15]
    mid_hot = [n for n in patterns['hot_numbers'] if n in mid_range][:10]
    
    attempts = 0
    while len(combinations) < 10 and attempts < 50:
        # 3-4 numéros high range + équilibrage
        high_count = random.choice([3, 4])
        selected_high = random.sample(high_hot[:12], min(high_count, len(high_hot)))
        
        remaining = 5 - high_count
        if remaining > 0:
            selected_mid = random.sample(mid_hot[:8], min(remaining, len(mid_hot)))
        else:
            selected_mid = []
        
        numbers = sorted(selected_high + selected_mid)
        stars = sorted(random.sample(patterns['hot_stars'][:8], 2))
        
        # Vérifier la concentration May 27
        if check_may27_concentration(numbers, stars, patterns):
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': f'May 30 Heavy High Range V{len(combinations)+1}'
            })
        
        attempts += 1
    
    return combinations

def generate_set2_backtesting_improved_v2(patterns):
    """SET 2: Backtesting Improved V2 - Nouveaux champions avec contrôle"""
    
    combinations = []
    
    # Prendre les champions actuels (peut inclure numéros du 27 mai si vraiment chauds)
    potential_champions = patterns['hot_numbers'][:15]
    new_champion1 = potential_champions[0]
    new_champion2 = potential_champions[1] if len(potential_champions) > 1 else potential_champions[0]
    
    print(f"🏆 Champions identifiés: {new_champion1}, {new_champion2}")
    
    attempts = 0
    while len(combinations) < 10 and attempts < 50:
        # Inclure au moins un champion
        champion_count = random.choice([1, 2])
        if champion_count == 1:
            selected_champions = [random.choice([new_champion1, new_champion2])]
        else:
            selected_champions = [new_champion1, new_champion2]
        
        # Compléter avec d'autres numéros prometteurs
        remaining_count = 5 - len(selected_champions)
        available_numbers = [n for n in patterns['hot_numbers'] if n not in selected_champions]
        selected_others = random.sample(available_numbers[:20], min(remaining_count, len(available_numbers)))
        
        numbers = sorted(selected_champions + selected_others)
        stars = sorted(random.sample(patterns['hot_stars'][:8], 2))
        
        # Vérifier la concentration May 27
        if check_may27_concentration(numbers, stars, patterns):
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': f'Backtesting Improved V2 #{len(combinations)+1}'
            })
        
        attempts += 1
    
    return combinations

def generate_set3_strategic_methods_v2(patterns):
    """SET 3: Strategic Methods V2 - Risk/Reward, Frequency, Markov, Time Series"""
    
    combinations = []
    
    # 2 Risk/Reward combinations
    for i in range(2):
        attempts = 0
        while attempts < 20:
            risk_level = 'High' if i == 0 else 'Moderate'
            if risk_level == 'High':
                cold_count = 2
                hot_count = 3
            else:
                cold_count = 1
                hot_count = 4
            
            selected_cold = random.sample(patterns['cold_numbers'][:20], cold_count)
            available_hot = [n for n in patterns['hot_numbers'] if n not in selected_cold]
            selected_hot = random.sample(available_hot[:15], hot_count)
            
            numbers = sorted(selected_cold + selected_hot)
            stars = sorted(random.sample(patterns['hot_stars'][:8], 2))
            
            if check_may27_concentration(numbers, stars, patterns):
                combinations.append({
                    'numbers': numbers,
                    'stars': stars,
                    'strategy': f'Risk/Reward Balance - {risk_level} Risk'
                })
                break
            attempts += 1
    
    # 2 Frequency Analysis combinations
    for i in range(2):
        attempts = 0
        while attempts < 20:
            approach = 'Hot Focus' if i == 0 else 'Hot-Cold Balance'
            if approach == 'Hot Focus':
                selected_numbers = random.sample(patterns['hot_numbers'][:20], 5)
            else:
                hot_nums = random.sample(patterns['hot_numbers'][:15], 3)
                cold_nums = random.sample(patterns['cold_numbers'][:15], 2)
                selected_numbers = sorted(hot_nums + cold_nums)
            
            stars = sorted(random.sample(patterns['hot_stars'][:8], 2))
            
            if check_may27_concentration(selected_numbers, stars, patterns):
                combinations.append({
                    'numbers': selected_numbers,
                    'stars': stars,
                    'strategy': f'Frequency Analysis - {approach}'
                })
                break
            attempts += 1
    
    # 2 Markov Chain combinations
    for i in range(2):
        attempts = 0
        while attempts < 20:
            # Séquences avec espacement logique
            base_num = random.choice(patterns['hot_numbers'][:12])
            sequence = [base_num]
            
            for _ in range(4):
                next_num = sequence[-1] + random.choice([5, 7, 8, 10, 12])
                if next_num > 50:
                    next_num = random.choice(range(1, 20))
                if next_num not in sequence and next_num <= 50:
                    sequence.append(next_num)
            
            # Compléter si nécessaire
            while len(sequence) < 5:
                available = [n for n in range(1, 51) if n not in sequence]
                sequence.append(random.choice(available))
            
            numbers = sorted(sequence[:5])
            pattern_type = 'Sequential Patterns' if i == 0 else 'Transition Probability'
            stars = sorted(random.sample(patterns['hot_stars'][:8], 2))
            
            if check_may27_concentration(numbers, stars, patterns):
                combinations.append({
                    'numbers': numbers,
                    'stars': stars,
                    'strategy': f'Markov Chain - {pattern_type}'
                })
                break
            attempts += 1
    
    # 2 Time Series combinations
    for i in range(2):
        attempts = 0
        while attempts < 20:
            analysis_type = 'Trend Analysis' if i == 0 else 'Seasonal Patterns'
            
            if analysis_type == 'Trend Analysis':
                start_num = random.choice(patterns['hot_numbers'][:10])
                numbers = []
                current = start_num
                for _ in range(5):
                    if current <= 50:
                        numbers.append(current)
                    current += random.choice([3, 5, 7])
                    if current > 50:
                        available = [n for n in range(1, 51) if n not in numbers]
                        if available:
                            numbers.append(random.choice(available))
                numbers = sorted(numbers[:5])
            else:
                # Seasonal: mix équilibré par range
                low_num = random.choice(range(1, 17))
                mid_nums = random.sample(range(18, 34), 2)
                high_nums = random.sample(range(35, 50), 2)
                numbers = sorted([low_num] + mid_nums + high_nums)
            
            stars = sorted(random.sample(patterns['hot_stars'][:8], 2))
            
            if check_may27_concentration(numbers, stars, patterns):
                combinations.append({
                    'numbers': numbers,
                    'stars': stars,
                    'strategy': f'Time Series - {analysis_type}'
                })
                break
            attempts += 1
    
    # 2 Coverage Optimization combinations
    for i in range(2):
        attempts = 0
        while attempts < 20:
            mix_type = 'Balanced Mix' if i == 0 else 'Diversified Mix'
            
            # Mélange équilibré
            hot_nums = random.sample(patterns['hot_numbers'][:12], 2)
            cold_nums = random.sample(patterns['cold_numbers'][:12], 1)
            mid_nums = random.sample(range(20, 35), 2)
            
            numbers = sorted(hot_nums + cold_nums + mid_nums)
            stars = sorted(random.sample(patterns['hot_stars'][:8], 2))
            
            if check_may27_concentration(numbers, stars, patterns):
                combinations.append({
                    'numbers': numbers,
                    'stars': stars,
                    'strategy': f'Coverage Optimization - {mix_type}'
                })
                break
            attempts += 1
    
    return combinations

def generate_set4_ultimate_mix_v2(patterns):
    """SET 4: Ultimate Mix V2 - Fusion des méthodologies"""
    
    combinations = []
    top_candidates = patterns['hot_numbers'][:20]
    
    strategies = [
        'Ultimate Mix - Frequency Champions V2',
        'Ultimate Mix - High Performance Fusion V2', 
        'Ultimate Mix - Strategic Balance Supreme V2'
    ]
    
    for i, strategy_name in enumerate(strategies):
        attempts = 0
        while attempts < 20:
            if i == 0:  # Frequency Champions
                selected_numbers = random.sample(top_candidates[:12], 5)
            elif i == 1:  # High Performance Fusion
                high_range_candidates = [n for n in top_candidates if n >= 35]
                mid_range_candidates = [n for n in top_candidates if 20 <= n <= 34]
                selected_numbers = random.sample(high_range_candidates[:8], 3) + random.sample(mid_range_candidates[:8], 2)
                selected_numbers = sorted(selected_numbers)
            else:  # Strategic Balance Supreme
                low_candidates = [n for n in range(1, 18) if patterns['number_freq'].get(n, 0) > 0]
                mid_candidates = [n for n in range(18, 35) if n in patterns['hot_numbers']]
                high_candidates = [n for n in range(35, 51) if n in patterns['hot_numbers']]
                
                selected_numbers = (
                    random.sample(low_candidates[:10], 1) +
                    random.sample(mid_candidates[:10], 2) +
                    random.sample(high_candidates[:10], 2)
                )
                selected_numbers = sorted(selected_numbers)
            
            stars = sorted(random.sample(patterns['hot_stars'][:6], 2))
            
            if check_may27_concentration(selected_numbers, stars, patterns):
                combinations.append({
                    'numbers': selected_numbers,
                    'stars': stars,
                    'strategy': strategy_name
                })
                break
            attempts += 1
    
    return combinations

def generate_set5_mixed_strategy_v2(patterns):
    """SET 5: Mixed Strategy V2 - Hot-Cold Balance"""
    
    combinations = []
    hot_pool = patterns['hot_numbers'][:25]
    cold_pool = patterns['cold_numbers'][:25]
    
    strategies = [
        'Hot Emphasis', 'Balanced', 'Cold Balance', 'Frequency Optimized',
        'Diversity Focus', 'Strategic Balance', 'Pattern Variation',
        'Adaptive Mix', 'Range Optimized', 'Ultimate Balance'
    ]
    
    for i, strategy_name in enumerate(strategies):
        attempts = 0
        while attempts < 20:
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
            
            selected_hot = random.sample(hot_pool[:20], min(hot_count, len(hot_pool)))
            selected_cold = random.sample(cold_pool[:20], min(cold_count, len(cold_pool)))
            
            numbers = sorted(selected_hot + selected_cold)
            
            # Étoiles avec balance hot/cold
            hot_stars = patterns['hot_stars'][:6]
            cold_stars = [s for s in range(1, 13) if s not in hot_stars[:4]]
            
            star1 = random.choice(hot_stars[:4])
            star2 = random.choice(cold_stars[:4])
            stars = sorted([star1, star2])
            
            if check_may27_concentration(numbers, stars, patterns):
                combinations.append({
                    'numbers': numbers,
                    'stars': stars,
                    'strategy': f'Mixed Strategy - {strategy_name}'
                })
                break
            attempts += 1
    
    return combinations

def main():
    """Générer les 5 sets corrigés pour le 30 mai 2025"""
    
    print("🚀 GÉNÉRATION CORRIGÉE DES 5 SETS EUROMILLIONS - 30 MAI 2025")
    print("Inclusion naturelle des numéros selon calculs, limitation concentration 27 mai")
    print("=" * 80)
    
    # Charger les données complètes
    df = load_historical_data()
    if df is None:
        return None
    
    # Analyser tous les patterns
    print("\n📊 ANALYSE COMPLÈTE DES PATTERNS:")
    patterns = analyze_frequency_patterns(df)
    
    print(f"\n🚀 GÉNÉRATION DES 5 SETS AVEC CONTRÔLE DE CONCENTRATION:")
    print("-" * 60)
    
    all_sets = []
    
    # Générer tous les sets
    print("✅ SET 1: May 30 Optimized")
    set1 = generate_set1_may30_optimized(patterns)
    all_sets.append(('SET 1: May 30 Optimized', set1))
    
    print("✅ SET 2: Backtesting Improved V2")
    set2 = generate_set2_backtesting_improved_v2(patterns)
    all_sets.append(('SET 2: Backtesting Improved V2', set2))
    
    print("✅ SET 3: Strategic Methods V2")
    set3 = generate_set3_strategic_methods_v2(patterns)
    all_sets.append(('SET 3: Strategic Methods V2', set3))
    
    print("✅ SET 4: Ultimate Mix V2")
    set4 = generate_set4_ultimate_mix_v2(patterns)
    all_sets.append(('SET 4: Ultimate Mix V2', set4))
    
    print("✅ SET 5: Mixed Strategy V2")
    set5 = generate_set5_mixed_strategy_v2(patterns)
    all_sets.append(('SET 5: Mixed Strategy V2', set5))
    
    # Afficher et analyser tous les sets
    total_combinations = 0
    may27_usage = Counter()
    
    for set_name, combinations in all_sets:
        print(f"\n🎯 {set_name}")
        print("=" * len(set_name) + "====")
        
        for i, combo in enumerate(combinations, 1):
            print(f"{total_combinations + i:2d}. {combo['strategy']}")
            print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
            
            # Analyser l'usage des numéros du 27 mai
            may27_nums = [n for n in combo['numbers'] if n in patterns['may27_numbers']]
            may27_stars_found = [s for s in combo['stars'] if s in patterns['may27_stars']]
            
            if may27_nums or may27_stars_found:
                print(f"    📊 Numéros 27 mai: {may27_nums} | Étoiles: {may27_stars_found}")
                for num in may27_nums:
                    may27_usage[f'N{num}'] += 1
                for star in may27_stars_found:
                    may27_usage[f'S{star}'] += 1
            else:
                print(f"    ✅ Aucun numéro du 27 mai")
            print()
        
        total_combinations += len(combinations)
    
    # Statistiques finales
    print(f"\n🎯 STATISTIQUES FINALES:")
    print(f"✅ {total_combinations} combinaisons générées")
    print(f"📊 Usage des numéros/étoiles du 27 mai:")
    for item, count in may27_usage.most_common():
        print(f"   {item}: {count} fois")
    
    print(f"\n✅ Méthodologie respectée avec contrôle intelligent!")
    print(f"🚀 Prêt pour le tirage du 30 mai 2025!")
    
    return all_sets

if __name__ == "__main__":
    main()