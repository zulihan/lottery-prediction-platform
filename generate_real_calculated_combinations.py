"""
Générer de VRAIES combinaisons calculées pour le prochain tirage Euromillions
en utilisant les données historiques réelles de la base PostgreSQL
"""
import psycopg2
import os
import pandas as pd
import numpy as np
import random
from collections import Counter
from datetime import datetime

def load_historical_data():
    """Charger les données historiques depuis PostgreSQL"""
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        
        # Charger les 200 derniers tirages
        query = """
        SELECT date, n1, n2, n3, n4, n5, s1, s2 
        FROM euromillions_drawings 
        ORDER BY date DESC 
        LIMIT 200
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print(f"✅ {len(df)} tirages historiques chargés depuis PostgreSQL")
        return df
        
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return None

def analyze_real_frequency_patterns(df):
    """Analyser les vrais patterns de fréquence"""
    
    # Collecter tous les numéros
    all_numbers = []
    all_stars = []
    
    for _, row in df.iterrows():
        numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
        stars = [row['s1'], row['s2']]
        
        all_numbers.extend([int(n) for n in numbers if pd.notna(n)])
        all_stars.extend([int(s) for s in stars if pd.notna(s)])
    
    # Calculer les fréquences réelles
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Analyser par ranges
    low_range = [n for n in range(1, 18)]
    mid_range = [n for n in range(18, 35)]
    high_range = [n for n in range(35, 51)]
    
    low_freq = {n: number_freq.get(n, 0) for n in low_range}
    mid_freq = {n: number_freq.get(n, 0) for n in mid_range}
    high_freq = {n: number_freq.get(n, 0) for n in high_range}
    
    # Trier par fréquence
    hot_numbers = [num for num, _ in number_freq.most_common(25)]
    cold_numbers = [num for num, _ in number_freq.most_common()[-25:]]
    hot_stars = [star for star, _ in star_freq.most_common(8)]
    
    print(f"🔥 Top 10 numéros chauds: {hot_numbers[:10]}")
    print(f"❄️ Top 10 numéros froids: {cold_numbers[:10]}")
    print(f"🌟 Étoiles chaudes: {hot_stars[:6]}")
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'hot_stars': hot_stars,
        'number_freq': number_freq,
        'star_freq': star_freq,
        'low_freq': low_freq,
        'mid_freq': mid_freq,
        'high_freq': high_freq
    }

def generate_high_range_focused_set(patterns):
    """SET 1: High Range Focused (basé sur succès du 27 mai)"""
    
    combinations = []
    
    # Les numéros high range les plus fréquents
    high_hot = [n for n in patterns['hot_numbers'] if n >= 35][:12]
    mid_support = [n for n in patterns['hot_numbers'] if 20 <= n <= 34][:8]
    
    for i in range(10):
        # 3-4 numéros high range + 1-2 mid range
        high_count = random.choice([3, 4])
        selected_high = random.sample(high_hot[:10], min(high_count, len(high_hot)))
        
        remaining = 5 - high_count
        selected_mid = random.sample(mid_support, min(remaining, len(mid_support)))
        
        numbers = sorted(selected_high + selected_mid)
        
        # Étoiles: prioriser les plus fréquentes
        star1 = patterns['hot_stars'][0] if patterns['hot_stars'] else 12
        star2 = random.choice(patterns['hot_stars'][1:4]) if len(patterns['hot_stars']) > 1 else 4
        stars = sorted([star1, star2])
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'High Range Focused V{i+1}'
        })
    
    return combinations

def generate_mixed_balance_set(patterns):
    """SET 2: Mixed Balance (succès avec numéro 30)"""
    
    combinations = []
    
    # Distribution qui a fonctionné: 1 bas, 1 mid, 3 high
    low_nums = [n for n in range(1, 18) if patterns['number_freq'].get(n, 0) > 0]
    mid_nums = [n for n in range(18, 35) if n in patterns['hot_numbers'][:20]]
    high_nums = [n for n in range(35, 51) if n in patterns['hot_numbers'][:15]]
    
    for i in range(10):
        # 1 numéro bas (potentiel surprise comme 12)
        selected_low = random.sample(low_nums, 1)
        
        # 1-2 numéros mid (incluant des candidats comme 30)
        mid_count = random.choice([1, 2])
        selected_mid = random.sample(mid_nums[:12], min(mid_count, len(mid_nums)))
        
        # Le reste en high
        high_count = 5 - len(selected_low) - len(selected_mid)
        selected_high = random.sample(high_nums[:10], min(high_count, len(high_nums)))
        
        numbers = sorted(selected_low + selected_mid + selected_high)
        
        # Étoiles avec les plus performantes
        stars = sorted(random.sample(patterns['hot_stars'][:6], 2))
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Mixed Balance V{i+1}'
        })
    
    return combinations

def generate_frequency_champions_set(patterns):
    """SET 3: Champions de fréquence"""
    
    combinations = []
    
    # Les 15 numéros les plus fréquents
    champions = patterns['hot_numbers'][:15]
    
    for i in range(10):
        # 4 champions + 1 équilibrage
        selected_champions = random.sample(champions, 4)
        
        # 1 numéro pour équilibrer (peut être cold ou différent range)
        remaining_nums = [n for n in range(1, 51) if n not in selected_champions]
        balance_num = random.choice(remaining_nums)
        
        numbers = sorted(selected_champions + [balance_num])
        
        # Étoiles: les 2 plus fréquentes avec variation
        if i % 3 == 0:
            stars = sorted(patterns['hot_stars'][:2])
        else:
            star1 = patterns['hot_stars'][0]
            star2 = random.choice(patterns['hot_stars'][1:5])
            stars = sorted([star1, star2])
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Frequency Champions V{i+1}'
        })
    
    return combinations

def generate_surprise_inclusion_set(patterns):
    """SET 4: Inclusion des surprises (comme le 12 du 27 mai)"""
    
    combinations = []
    
    # Numéros moins fréquents mais pas les plus froids
    surprise_candidates = [n for n in range(1, 20) if patterns['number_freq'].get(n, 0) < 8]
    hot_support = patterns['hot_numbers'][:20]
    
    for i in range(10):
        # 1-2 surprises + 3-4 numéros chauds
        surprise_count = random.choice([1, 2])
        selected_surprises = random.sample(surprise_candidates, min(surprise_count, len(surprise_candidates)))
        
        # Compléter avec des chauds
        hot_count = 5 - surprise_count
        available_hot = [n for n in hot_support if n not in selected_surprises]
        selected_hot = random.sample(available_hot, min(hot_count, len(available_hot)))
        
        numbers = sorted(selected_surprises + selected_hot)
        
        # Étoiles: mix équilibré
        star1 = patterns['hot_stars'][0] if patterns['hot_stars'] else 12
        star2 = random.choice([s for s in patterns['hot_stars'][1:] if s != star1]) if len(patterns['hot_stars']) > 1 else 4
        stars = sorted([star1, star2])
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Surprise Inclusion V{i+1}'
        })
    
    return combinations

def generate_strategic_fusion_set(patterns):
    """SET 5: Fusion stratégique optimale"""
    
    combinations = []
    
    # Basé sur l'analyse des 74.4% de succès
    # Mix des numéros qui sont sortis le plus souvent dans nos combinaisons gagnantes
    priority_numbers = [40, 38, 41, 30]  # Les champions du 27 mai
    support_numbers = patterns['hot_numbers'][:20]
    
    for i in range(5):
        # Inclure 2-3 numéros prioritaires
        priority_count = random.choice([2, 3])
        selected_priority = random.sample(priority_numbers, min(priority_count, len(priority_numbers)))
        
        # Compléter avec des numéros chauds
        remaining_count = 5 - priority_count
        available_support = [n for n in support_numbers if n not in selected_priority]
        selected_support = random.sample(available_support, min(remaining_count, len(available_support)))
        
        numbers = sorted(selected_priority + selected_support)
        
        # Étoiles: priorité aux performantes (12 et 4)
        priority_stars = [12, 4]
        if i < 3:
            stars = sorted(random.sample(priority_stars, 2))
        else:
            star1 = random.choice(priority_stars)
            star2 = random.choice([s for s in patterns['hot_stars'] if s != star1])
            stars = sorted([star1, star2])
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Strategic Fusion V{i+1}'
        })
    
    return combinations

def main():
    """Générer les vraies combinaisons calculées"""
    
    print("🎯 GÉNÉRATION DE VRAIES COMBINAISONS CALCULÉES")
    print("Basées sur les données PostgreSQL réelles")
    print("=" * 55)
    
    # Charger les vraies données
    df = load_historical_data()
    if df is None:
        return None
    
    # Analyser les vrais patterns
    print("\n📊 ANALYSE DES PATTERNS RÉELS:")
    patterns = analyze_real_frequency_patterns(df)
    
    print(f"\n🚀 GÉNÉRATION DES 45 COMBINAISONS CALCULÉES:")
    print("-" * 50)
    
    all_combinations = []
    
    # Générer les 5 sets
    print("✅ SET 1: High Range Focused (10 combinaisons)")
    set1 = generate_high_range_focused_set(patterns)
    all_combinations.extend(set1)
    
    print("✅ SET 2: Mixed Balance (10 combinaisons)")
    set2 = generate_mixed_balance_set(patterns)
    all_combinations.extend(set2)
    
    print("✅ SET 3: Frequency Champions (10 combinaisons)")
    set3 = generate_frequency_champions_set(patterns)
    all_combinations.extend(set3)
    
    print("✅ SET 4: Surprise Inclusion (10 combinaisons)")
    set4 = generate_surprise_inclusion_set(patterns)
    all_combinations.extend(set4)
    
    print("✅ SET 5: Strategic Fusion (5 combinaisons)")
    set5 = generate_strategic_fusion_set(patterns)
    all_combinations.extend(set5)
    
    # Afficher toutes les combinaisons
    print(f"\n🎯 LES 45 COMBINAISONS CALCULÉES:")
    print("=" * 45)
    
    for i, combo in enumerate(all_combinations, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        
        # Analyser la composition
        low = len([n for n in combo['numbers'] if n <= 17])
        mid = len([n for n in combo['numbers'] if 18 <= n <= 34])
        high = len([n for n in combo['numbers'] if n >= 35])
        
        print(f"    Répartition: {low} bas | {mid} mid | {high} high")
        
        # Vérifier si contient des numéros champions
        champions = [n for n in combo['numbers'] if n in [40, 38, 41, 30]]
        if champions:
            print(f"    ⭐ Champions: {champions}")
        print()
    
    print(f"✅ {len(all_combinations)} combinaisons calculées avec vos vraies données!")
    return all_combinations

if __name__ == "__main__":
    main()