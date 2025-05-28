"""
Générer de VRAIES combinaisons pour le prochain tirage Euromillions
en utilisant les scripts de stratégies existants et les données historiques
"""
import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def load_historical_data():
    """Charger les données historiques depuis la base"""
    try:
        conn = sqlite3.connect('lottery_predictions.db')
        
        # Charger les données Euromillions
        query = """
        SELECT draw_date, number1, number2, number3, number4, number5, star1, star2 
        FROM euromillions_draws 
        WHERE draw_date IS NOT NULL 
        ORDER BY draw_date DESC 
        LIMIT 500
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if len(df) == 0:
            print("⚠️ Aucune donnée trouvée dans la base")
            return None
            
        print(f"✅ {len(df)} tirages historiques chargés")
        return df
        
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return None

def analyze_frequency_patterns(df):
    """Analyser les patterns de fréquence dans les données historiques"""
    
    # Analyser les numéros
    all_numbers = []
    for _, row in df.iterrows():
        numbers = [row['number1'], row['number2'], row['number3'], row['number4'], row['number5']]
        all_numbers.extend([n for n in numbers if pd.notna(n)])
    
    # Analyser les étoiles
    all_stars = []
    for _, row in df.iterrows():
        stars = [row['star1'], row['star2']]
        all_stars.extend([s for s in stars if pd.notna(s)])
    
    # Calculer les fréquences
    from collections import Counter
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    # Trier par fréquence
    hot_numbers = [num for num, _ in number_freq.most_common(20)]
    cold_numbers = [num for num, _ in number_freq.most_common()[-20:]]
    hot_stars = [star for star, _ in star_freq.most_common(6)]
    cold_stars = [star for star, _ in star_freq.most_common()[-6:]]
    
    print(f"🔥 Numéros chauds: {hot_numbers[:10]}")
    print(f"❄️ Numéros froids: {cold_numbers[:10]}")
    print(f"🌟 Étoiles chaudes: {hot_stars}")
    print(f"⭐ Étoiles froides: {cold_stars}")
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'hot_stars': hot_stars,
        'cold_stars': cold_stars,
        'all_freq': number_freq,
        'star_freq': star_freq
    }

def generate_high_range_strategy(patterns, num_combos=10):
    """Stratégie High Range basée sur les données réelles"""
    
    combinations = []
    high_range = [n for n in range(35, 51)]
    mid_range = [n for n in range(18, 35)]
    
    for i in range(num_combos):
        # 3-4 numéros high range, 1-2 mid range
        high_count = random.choice([3, 4])
        mid_count = 5 - high_count
        
        # Sélectionner des numéros high range chauds
        available_high = [n for n in high_range if n in patterns['hot_numbers'][:25]]
        if len(available_high) < high_count:
            available_high.extend([n for n in high_range if n not in available_high])
        
        selected_high = random.sample(available_high[:15], min(high_count, len(available_high)))
        
        # Sélectionner des numéros mid range
        available_mid = [n for n in mid_range]
        selected_mid = random.sample(available_mid, min(mid_count, len(available_mid)))
        
        numbers = sorted(selected_high + selected_mid)
        
        # Sélectionner les étoiles (prioriser les chaudes)
        star1 = random.choice(patterns['hot_stars'][:4])
        star2 = random.choice([s for s in patterns['hot_stars'] if s != star1])
        stars = sorted([star1, star2])
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'High Range Strategy V{i+1}'
        })
    
    return combinations

def generate_mixed_balance_strategy(patterns, num_combos=10):
    """Stratégie Mixed Balance basée sur les données réelles"""
    
    combinations = []
    
    for i in range(num_combos):
        # Distribution équilibrée: 1 bas, 2 mid, 2 high
        low_range = [n for n in range(1, 18)]
        mid_range = [n for n in range(18, 35)]
        high_range = [n for n in range(35, 51)]
        
        # 1 numéro bas (souvent froid)
        selected_low = random.sample(low_range, 1)
        
        # 2 numéros mid (mix chaud/froid)
        hot_mid = [n for n in mid_range if n in patterns['hot_numbers'][:20]]
        cold_mid = [n for n in mid_range if n in patterns['cold_numbers'][:20]]
        
        selected_mid = []
        if hot_mid:
            selected_mid.append(random.choice(hot_mid))
        if cold_mid and len(selected_mid) < 2:
            selected_mid.append(random.choice([n for n in cold_mid if n not in selected_mid]))
        while len(selected_mid) < 2:
            selected_mid.append(random.choice([n for n in mid_range if n not in selected_mid]))
        
        # 2 numéros high (principalement chauds)
        hot_high = [n for n in high_range if n in patterns['hot_numbers'][:15]]
        selected_high = random.sample(hot_high[:10], min(2, len(hot_high)))
        
        numbers = sorted(selected_low + selected_mid + selected_high)
        
        # Étoiles: mix chaud/froid
        star1 = random.choice(patterns['hot_stars'][:3])
        star2 = random.choice(patterns['cold_stars'][:3])
        if star1 == star2:
            star2 = random.choice([s for s in range(1, 13) if s != star1])
        stars = sorted([star1, star2])
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Mixed Balance Strategy V{i+1}'
        })
    
    return combinations

def generate_frequency_focus_strategy(patterns, num_combos=10):
    """Stratégie basée sur les fréquences réelles"""
    
    combinations = []
    
    for i in range(num_combos):
        # 60% de numéros chauds, 40% d'équilibre
        hot_count = 3
        balance_count = 2
        
        # Sélectionner 3 numéros très chauds
        very_hot = patterns['hot_numbers'][:12]
        selected_hot = random.sample(very_hot, hot_count)
        
        # Sélectionner 2 numéros pour équilibrer
        remaining_numbers = [n for n in range(1, 51) if n not in selected_hot]
        selected_balance = random.sample(remaining_numbers, balance_count)
        
        numbers = sorted(selected_hot + selected_balance)
        
        # Étoiles: favoriser la plus chaude
        hottest_star = patterns['hot_stars'][0]
        other_star = random.choice([s for s in patterns['hot_stars'][1:4] if s != hottest_star])
        stars = sorted([hottest_star, other_star])
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Frequency Focus Strategy V{i+1}'
        })
    
    return combinations

def generate_surprise_strategy(patterns, num_combos=10):
    """Stratégie incluant des numéros surprise (froids)"""
    
    combinations = []
    
    for i in range(num_combos):
        # 1-2 numéros froids + 3-4 numéros chauds/moyens
        cold_count = random.choice([1, 2])
        hot_count = 5 - cold_count
        
        # Sélectionner des numéros froids
        cold_numbers = patterns['cold_numbers'][:15]
        selected_cold = random.sample(cold_numbers, cold_count)
        
        # Sélectionner des numéros chauds/moyens
        hot_medium = patterns['hot_numbers'][:25]
        available_hot = [n for n in hot_medium if n not in selected_cold]
        selected_hot = random.sample(available_hot, hot_count)
        
        numbers = sorted(selected_cold + selected_hot)
        
        # Étoiles: mix équilibré
        star1 = random.choice(patterns['hot_stars'][:4])
        star2 = random.choice([s for s in range(1, 13) if s != star1])
        stars = sorted([star1, star2])
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Surprise Strategy V{i+1}'
        })
    
    return combinations

def generate_mathematical_progression_strategy(patterns, num_combos=5):
    """Stratégie basée sur des progressions mathématiques réalistes"""
    
    combinations = []
    
    for i in range(num_combos):
        # Générer une base avec des numéros chauds
        base_numbers = random.sample(patterns['hot_numbers'][:20], 3)
        
        # Ajouter 2 numéros avec des écarts réalistes
        additional = []
        for _ in range(2):
            # Écarts de 5-15 positions
            base = random.choice(base_numbers)
            offset = random.choice([-12, -8, -5, 5, 8, 12])
            new_num = base + offset
            if 1 <= new_num <= 50 and new_num not in base_numbers + additional:
                additional.append(new_num)
            else:
                # Fallback sur un numéro chaud disponible
                available = [n for n in patterns['hot_numbers'] if n not in base_numbers + additional]
                if available:
                    additional.append(random.choice(available[:15]))
        
        while len(additional) < 2:
            available = [n for n in range(1, 51) if n not in base_numbers + additional]
            additional.append(random.choice(available))
        
        numbers = sorted(base_numbers + additional)
        
        # Étoiles avec logique mathématique simple
        star1 = random.choice(patterns['hot_stars'][:3])
        star2 = (star1 + random.choice([3, 5, 7])) % 12 + 1
        if star2 == star1:
            star2 = random.choice([s for s in patterns['hot_stars'] if s != star1])
        stars = sorted([star1, star2])
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': f'Mathematical Progression V{i+1}'
        })
    
    return combinations

def main():
    """Générer les vraies combinaisons pour le prochain tirage"""
    
    print("🎯 GÉNÉRATION DE VRAIES COMBINAISONS EUROMILLIONS")
    print("Basées sur les données historiques et stratégies calculées")
    print("=" * 65)
    
    # Charger les données historiques
    df = load_historical_data()
    if df is None:
        print("❌ Impossible de générer sans données historiques")
        return
    
    # Analyser les patterns
    print("\n📊 ANALYSE DES PATTERNS HISTORIQUES:")
    patterns = analyze_frequency_patterns(df)
    
    print(f"\n🚀 GÉNÉRATION DES 45 COMBINAISONS RÉELLES:")
    print("-" * 50)
    
    all_combinations = []
    
    # Set 1: High Range Strategy (10 combos)
    print("SET 1: High Range Strategy (10 combinaisons)")
    set1 = generate_high_range_strategy(patterns, 10)
    all_combinations.extend(set1)
    
    # Set 2: Mixed Balance Strategy (10 combos)  
    print("SET 2: Mixed Balance Strategy (10 combinaisons)")
    set2 = generate_mixed_balance_strategy(patterns, 10)
    all_combinations.extend(set2)
    
    # Set 3: Frequency Focus Strategy (10 combos)
    print("SET 3: Frequency Focus Strategy (10 combinaisons)")
    set3 = generate_frequency_focus_strategy(patterns, 10)
    all_combinations.extend(set3)
    
    # Set 4: Surprise Strategy (10 combos)
    print("SET 4: Surprise Strategy (10 combinaisons)")
    set4 = generate_surprise_strategy(patterns, 10)
    all_combinations.extend(set4)
    
    # Set 5: Mathematical Progression (5 combos)
    print("SET 5: Mathematical Progression (5 combinaisons)")
    set5 = generate_mathematical_progression_strategy(patterns, 5)
    all_combinations.extend(set5)
    
    # Afficher toutes les combinaisons
    print(f"\n🎯 TOUTES LES 45 COMBINAISONS CALCULÉES:")
    print("=" * 55)
    
    for i, combo in enumerate(all_combinations, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        
        # Analyser la composition
        low = len([n for n in combo['numbers'] if n <= 17])
        mid = len([n for n in combo['numbers'] if 18 <= n <= 34])
        high = len([n for n in combo['numbers'] if n >= 35])
        
        print(f"    Répartition: {low} bas, {mid} mid, {high} high")
        print()
    
    print(f"✅ {len(all_combinations)} combinaisons générées avec succès!")
    print("🎯 Basées sur vos données historiques réelles!")
    
    return all_combinations

if __name__ == "__main__":
    main()