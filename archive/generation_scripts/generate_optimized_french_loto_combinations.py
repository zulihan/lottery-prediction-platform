"""
Générer 10 combinaisons optimisées pour le prochain tirage French Loto
Basées sur l'analyse des résultats du 2 juin 2025 et les insights stratégiques
"""
import psycopg2
import os
import pandas as pd
import numpy as np
import random
from collections import Counter

def load_french_loto_data():
    """Charger les données historiques French Loto"""
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        
        query = """
        SELECT date, n1, n2, n3, n4, n5, lucky 
        FROM french_loto_drawings 
        ORDER BY date DESC 
        LIMIT 150
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print(f"✅ {len(df)} tirages French Loto chargés")
        return df
        
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return None

def analyze_current_patterns(df):
    """Analyser les patterns actuels incluant les résultats récents"""
    
    all_numbers = []
    all_lucky = []
    
    for _, row in df.iterrows():
        numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
        lucky = row['lucky']
        
        all_numbers.extend([int(n) for n in numbers if pd.notna(n)])
        if pd.notna(lucky):
            all_lucky.append(int(lucky))
    
    number_freq = Counter(all_numbers)
    lucky_freq = Counter(all_lucky)
    
    hot_numbers = [num for num, _ in number_freq.most_common(20)]
    cold_numbers = [num for num, _ in number_freq.most_common()[-20:]]
    medium_numbers = [num for num in range(1, 50) if num not in hot_numbers and num not in cold_numbers]
    hot_lucky = [lucky for lucky, _ in lucky_freq.most_common(6)]
    
    print(f"🔥 Hot numbers: {hot_numbers[:12]}")
    print(f"❄️ Cold numbers: {cold_numbers[:12]}")
    print(f"🍀 Hot lucky: {hot_lucky}")
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'medium_numbers': medium_numbers,
        'hot_lucky': hot_lucky,
        'number_freq': number_freq,
        'lucky_freq': lucky_freq
    }

def get_june_2_insights():
    """Insights du tirage du 2 juin 2025"""
    return {
        'winning_numbers': [8, 13, 25, 29, 36],
        'lucky': 2,
        'successful_strategies': ['Hot Numbers Concentration', 'Strategic Diversity Mix', 'Trend-Frequency Hybrid'],
        'well_covered_numbers': [8, 13, 29, 36],  # Numbers that appeared in multiple combos
        'missed_number': 25,  # Number not in any combination
        'range_distribution': {'low': 2, 'mid': 2, 'high': 1},  # Winning pattern
        'lucky_insight': 'Very low lucky number (2) not anticipated'
    }

def generate_optimized_combinations(patterns):
    """Générer 10 combinaisons optimisées basées sur les insights"""
    
    insights = get_june_2_insights()
    combinations = []
    
    print(f"\n🚀 GÉNÉRATION DE 10 COMBINAISONS OPTIMISÉES")
    print("Basées sur l'analyse du succès du 2 juin 2025")
    print("-" * 55)
    
    # 1. Hot Numbers Enhanced (meilleure stratégie du 2 juin)
    hot_enhanced = random.sample(patterns['hot_numbers'][:10], 4) + random.sample(patterns['medium_numbers'][:8], 1)
    combinations.append({
        'numbers': sorted(hot_enhanced),
        'lucky': random.choice([1, 2, 3]),  # Lucky numbers bas comme insight
        'strategy': 'Hot Numbers Enhanced V2'
    })
    
    # 2. Strategic Diversity Improved (2ème meilleure du 2 juin)
    diversity_mix = (
        random.sample(patterns['hot_numbers'][:8], 2) +
        random.sample(patterns['medium_numbers'][:10], 2) +
        random.sample(range(20, 30), 1)  # Focus mid-range pour capturer des 25-like
    )
    combinations.append({
        'numbers': sorted(diversity_mix),
        'lucky': random.choice([2, 5, 7]),
        'strategy': 'Strategic Diversity Improved'
    })
    
    # 3. Trend-Frequency Improved (3ème meilleure du 2 juin)
    trend_freq = (
        random.sample(patterns['hot_numbers'][:6], 2) +
        random.sample(patterns['cold_numbers'][:8], 1) +
        random.sample(range(30, 40), 2)  # Range 30-40 pour capturer 36-like
    )
    combinations.append({
        'numbers': sorted(trend_freq),
        'lucky': random.choice([1, 8, 9]),
        'strategy': 'Trend-Frequency Improved'
    })
    
    # 4. Range Balance Optimized (pour corriger le déséquilibre de range)
    range_balanced = (
        random.sample(range(1, 17), 2) +    # 2 low (comme pattern gagnant)
        random.sample(range(17, 34), 2) +   # 2 mid (comme pattern gagnant)  
        random.sample(range(34, 50), 1)     # 1 high (comme pattern gagnant)
    )
    combinations.append({
        'numbers': sorted(range_balanced),
        'lucky': random.choice([2, 4, 6]),
        'strategy': 'Range Balance Optimized'
    })
    
    # 5. Missing Number Focus (pour capturer les 25-like)
    missing_focus = (
        [25] +  # Include explicit 25 or similar
        random.sample([n for n in range(20, 30) if n != 25], 2) +
        random.sample(patterns['hot_numbers'][:8], 2)
    )
    combinations.append({
        'numbers': sorted(missing_focus),
        'lucky': random.choice([1, 3, 5]),
        'strategy': 'Missing Number Focus'
    })
    
    # 6. Low Lucky Strategy (pour capturer lucky 2-like)
    low_lucky_combo = random.sample(patterns['hot_numbers'][:12], 3) + random.sample(patterns['medium_numbers'][:8], 2)
    combinations.append({
        'numbers': sorted(low_lucky_combo),
        'lucky': random.choice([1, 2, 3]),  # Focus sur lucky très bas
        'strategy': 'Low Lucky Strategy'
    })
    
    # 7. Pattern Replication (répliquer le pattern gagnant du 2 juin)
    pattern_replica = []
    # 2 low range
    pattern_replica.extend(random.sample([n for n in range(1, 17) if n in patterns['hot_numbers']], 2))
    # 2 mid range  
    pattern_replica.extend(random.sample([n for n in range(17, 34) if n in patterns['hot_numbers']], 2))
    # 1 high range
    pattern_replica.extend(random.sample([n for n in range(34, 50) if n in patterns['hot_numbers']], 1))
    
    combinations.append({
        'numbers': sorted(pattern_replica),
        'lucky': 2,  # Exact lucky du pattern gagnant
        'strategy': 'Pattern Replication'
    })
    
    # 8. Coverage Enhancement (améliorer la couverture des numéros manqués)
    coverage_enhanced = (
        [n for n in [24, 25, 26, 27] if n not in [combo['numbers'] for combo in combinations]] +
        random.sample(patterns['hot_numbers'][:8], 3)
    )[:5]
    while len(coverage_enhanced) < 5:
        available = [n for n in range(1, 50) if n not in coverage_enhanced]
        coverage_enhanced.append(random.choice(available))
    
    combinations.append({
        'numbers': sorted(coverage_enhanced),
        'lucky': random.choice([4, 7, 9]),
        'strategy': 'Coverage Enhancement'
    })
    
    # 9. Risk-Reward Refined (équilibrer risque et sécurité)
    risk_reward = (
        random.sample(patterns['hot_numbers'][:6], 3) +  # Sécurité
        random.sample(patterns['cold_numbers'][:10], 2)   # Risque
    )
    combinations.append({
        'numbers': sorted(risk_reward),
        'lucky': random.choice([1, 5, 8]),
        'strategy': 'Risk-Reward Refined'
    })
    
    # 10. Ultimate Fusion V2 (synthèse de tous les insights)
    ultimate_fusion = (
        [n for n in insights['well_covered_numbers'] if n in patterns['hot_numbers']][:2] +
        [25] +  # Include the missed number type
        random.sample([n for n in range(1, 17)], 1) +  # Low range
        random.sample([n for n in range(34, 50)], 1)   # High range
    )
    combinations.append({
        'numbers': sorted(ultimate_fusion[:5]),
        'lucky': 2,  # Lucky du pattern gagnant
        'strategy': 'Ultimate Fusion V2'
    })
    
    return combinations

def display_combinations(combinations):
    """Afficher les 10 combinaisons optimisées"""
    
    print(f"\n🎯 10 COMBINAISONS OPTIMISÉES POUR CE SOIR:")
    print("=" * 50)
    
    for i, combo in enumerate(combinations, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        
        # Analyser la composition
        low = len([n for n in combo['numbers'] if n <= 16])
        mid = len([n for n in combo['numbers'] if 17 <= n <= 33])
        high = len([n for n in combo['numbers'] if n >= 34])
        
        print(f"    Répartition: {low} bas, {mid} mid, {high} high")
        print()

def analyze_optimization_strategy(combinations):
    """Analyser la stratégie d'optimisation"""
    
    print(f"📊 ANALYSE DE L'OPTIMISATION:")
    print("-" * 35)
    
    # Lucky numbers distribution
    lucky_dist = Counter([combo['lucky'] for combo in combinations])
    print(f"Distribution Lucky Numbers:")
    for lucky, count in sorted(lucky_dist.items()):
        print(f"  Lucky {lucky}: {count} fois")
    
    # Range analysis
    total_low = sum(len([n for n in combo['numbers'] if n <= 16]) for combo in combinations)
    total_mid = sum(len([n for n in combo['numbers'] if 17 <= n <= 33]) for combo in combinations)
    total_high = sum(len([n for n in combo['numbers'] if n >= 34]) for combo in combinations)
    total_numbers = len(combinations) * 5
    
    print(f"\nDistribution globale des ranges:")
    print(f"  Bas (1-16): {total_low}/{total_numbers} ({total_low/total_numbers*100:.1f}%)")
    print(f"  Mid (17-33): {total_mid}/{total_numbers} ({total_mid/total_numbers*100:.1f}%)")
    print(f"  Haut (34-49): {total_high}/{total_numbers} ({total_high/total_numbers*100:.1f}%)")
    
    # Coverage du numéro manqué (25)
    includes_25_area = sum(1 for combo in combinations if any(20 <= n <= 30 for n in combo['numbers']))
    print(f"\nCouverture zone 20-30: {includes_25_area}/10 combinaisons")

def main():
    """Générer les combinaisons optimisées pour ce soir"""
    
    print("🚀 COMBINAISONS FRENCH LOTO OPTIMISÉES POUR CE SOIR")
    print("Basées sur l'analyse des succès du 2 juin 2025")
    print("=" * 60)
    
    # Charger et analyser les données
    df = load_french_loto_data()
    if df is None:
        return None
    
    patterns = analyze_current_patterns(df)
    
    # Générer les combinaisons optimisées
    combinations = generate_optimized_combinations(patterns)
    
    # Afficher les combinaisons
    display_combinations(combinations)
    
    # Analyser la stratégie d'optimisation
    analyze_optimization_strategy(combinations)
    
    print(f"\n✅ GÉNÉRATION TERMINÉE:")
    print(f"📊 10 combinaisons optimisées pour ce soir")
    print(f"🎯 Intègrent les insights du succès du 2 juin")
    print(f"🚀 Focus: hot numbers, range balance, lucky bas")
    
    return combinations

if __name__ == "__main__":
    main()