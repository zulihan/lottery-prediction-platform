"""
Générer 10 combinaisons Euromillions optimisées pour le 6 juin 2025
Utilisant la base de données réelle avec accès direct via le module database
"""
import sys
import os
sys.path.append('.')

try:
    from database import get_database_connection
    import pandas as pd
    from collections import Counter
    import random
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def load_euromillions_from_database():
    """Charger les données Euromillions via le module database existant"""
    try:
        connection = get_database_connection()
        if not connection:
            print("Impossible de se connecter à la base de données")
            return None
        
        cursor = connection.cursor()
        
        # Obtenir d'abord la structure de la table
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'euromillions_drawings'
            ORDER BY ordinal_position
        """)
        columns_info = cursor.fetchall()
        print(f"Structure de la table: {columns_info}")
        
        # Charger toutes les données
        cursor.execute("SELECT * FROM euromillions_drawings LIMIT 10")
        sample_data = cursor.fetchall()
        print(f"Échantillon de données: {sample_data}")
        
        # Charger toutes les données
        cursor.execute("SELECT * FROM euromillions_drawings")
        data = cursor.fetchall()
        
        # Obtenir les noms de colonnes
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'euromillions_drawings'
            ORDER BY ordinal_position
        """)
        column_names = [row[0] for row in cursor.fetchall()]
        
        # Créer DataFrame
        df = pd.DataFrame(data, columns=column_names)
        
        connection.close()
        
        print(f"✅ Chargé {len(df)} tirages Euromillions depuis la base de données")
        return df
        
    except Exception as e:
        print(f"Erreur lors du chargement: {e}")
        return None

def analyze_real_frequencies(df):
    """Analyser les fréquences avec les vraies données"""
    if df is None:
        return None
    
    try:
        print(f"Colonnes disponibles: {list(df.columns)}")
        print(f"Premier échantillon:\n{df.iloc[0]}")
        
        all_numbers = []
        all_stars = []
        
        # Identifier les colonnes numériques (positions 3-9 based on sample data)
        # Sample: (1875, datetime.date(2004, 2, 13), 'Friday', 32, 16, 29, 41, 36, 9, 7)
        # Positions: 0=id, 1=date, 2=day, 3-7=numbers, 8-9=stars
        
        for _, row in df.iterrows():
            row_values = list(row)
            
            # Extraire les 5 numéros (positions 3-7)
            for i in range(3, 8):
                if i < len(row_values) and pd.notna(row_values[i]):
                    try:
                        num = int(row_values[i])
                        if 1 <= num <= 50:
                            all_numbers.append(num)
                    except (ValueError, TypeError):
                        continue
            
            # Extraire les 2 étoiles (positions 8-9)
            for i in range(8, 10):
                if i < len(row_values) and pd.notna(row_values[i]):
                    try:
                        star = int(row_values[i])
                        if 1 <= star <= 12:
                            all_stars.append(star)
                    except (ValueError, TypeError):
                        continue
        
        number_freq = Counter(all_numbers)
        star_freq = Counter(all_stars)
        
        # Analyser les 100 tirages les plus récents
        recent_numbers = []
        recent_stars = []
        
        for _, row in df.head(100).iterrows():
            row_values = list(row)
            
            for i in range(3, 8):
                if i < len(row_values) and pd.notna(row_values[i]):
                    try:
                        num = int(row_values[i])
                        if 1 <= num <= 50:
                            recent_numbers.append(num)
                    except (ValueError, TypeError):
                        continue
            
            for i in range(8, 10):
                if i < len(row_values) and pd.notna(row_values[i]):
                    try:
                        star = int(row_values[i])
                        if 1 <= star <= 12:
                            recent_stars.append(star)
                    except (ValueError, TypeError):
                        continue
        
        recent_number_freq = Counter(recent_numbers)
        recent_star_freq = Counter(recent_stars)
        
        print(f"📊 Analyse terminée:")
        print(f"   {len(all_numbers)} numéros analysés")
        print(f"   {len(all_stars)} étoiles analysées")
        print(f"   Top 10 numéros: {number_freq.most_common(10)}")
        print(f"   Top 6 étoiles: {star_freq.most_common(6)}")
        
        return {
            'all_numbers': number_freq,
            'all_stars': star_freq,
            'recent_numbers': recent_number_freq,
            'recent_stars': recent_star_freq,
            'total_draws': len(df),
            'hot_numbers': [num for num, _ in number_freq.most_common(20)],
            'cold_numbers': [num for num, _ in number_freq.most_common()[-15:]],
            'hot_stars': [star for star, _ in star_freq.most_common()],
            'cold_stars': [star for star, _ in star_freq.most_common()[-6:]]
        }
        
    except Exception as e:
        print(f"Erreur analyse: {e}")
        return None

def generate_data_driven_combinations(frequencies):
    """Générer 10 combinaisons basées sur les vraies données + insights June 3"""
    
    if not frequencies:
        print("Pas de données de fréquence disponibles")
        return []
    
    print(f"🎯 Génération avec {frequencies['total_draws']} tirages historiques")
    
    combinations = []
    
    # June 3 insights: Coverage Optimization was best, need star 7, extreme high focus
    june_3_winners = [12, 15, 38, 47, 48]
    june_3_stars = [5, 7]
    
    # 1. Coverage Optimization Data-Driven (Best strategy from June 3)
    hot_nums = frequencies['hot_numbers'][:15]
    extreme_high = [n for n in hot_nums if n >= 45]
    if len(extreme_high) < 3:
        extreme_high.extend([47, 48, 49])
    
    combo1 = {
        'numbers': [15, 38] + extreme_high[:3],  # June 3 winners + extreme high
        'stars': [5, 7],  # June 3 winning stars
        'strategy': 'Coverage Optimization Data-Driven',
        'method': f'June 3 winners + real data extreme high from {frequencies["total_draws"]} draws'
    }
    combinations.append(combo1)
    
    # 2. Frequency Analysis Ultimate
    top_5_numbers = [num for num, _ in frequencies['all_numbers'].most_common(5)]
    
    combo2 = {
        'numbers': top_5_numbers,
        'stars': [frequencies['hot_stars'][0], 7],  # Most frequent + missing star 7
        'strategy': 'Frequency Analysis Ultimate',
        'method': f'Top 5 most frequent from {frequencies["total_draws"]} historical draws'
    }
    combinations.append(combo2)
    
    # 3. Recent Trends Enhanced
    recent_top = [num for num, _ in frequencies['recent_numbers'].most_common(8)]
    recent_high = [n for n in recent_top if n >= 35][:3]
    recent_low = [n for n in recent_top if n <= 17][:2]
    
    combo3 = {
        'numbers': recent_low + recent_high,
        'stars': [5, frequencies['recent_stars'].most_common()[0][0]],
        'strategy': 'Recent Trends Enhanced',
        'method': 'Recent 100 draws patterns + June 3 winning star'
    }
    combinations.append(combo3)
    
    # 4. High-Range Concentration (60% like June 3)
    high_range_hot = [n for n in frequencies['hot_numbers'] if n >= 35][:3]
    low_range_hot = [n for n in frequencies['hot_numbers'] if n <= 17][:2]
    
    combo4 = {
        'numbers': low_range_hot + high_range_hot,
        'stars': [7, frequencies['hot_stars'][1]],  # Star 7 priority
        'strategy': 'High-Range Concentration',
        'method': 'June 3 pattern: 2 low + 3 high with real data frequencies'
    }
    combinations.append(combo4)
    
    # 5. Star 7 Priority Ultimate
    balanced_nums = frequencies['hot_numbers'][:3] + [38, 47]  # Include June 3 winners
    
    combo5 = {
        'numbers': balanced_nums,
        'stars': [7, 3],  # Star 7 maximum priority
        'strategy': 'Star 7 Priority Ultimate',
        'method': 'Star 7 focus + June 3 winning elements + hot numbers'
    }
    combinations.append(combo5)
    
    # 6-10: Generate variations with different approaches
    variation_strategies = [
        'Hot-Cold Balance',
        'Extreme High Focus',
        'Mathematical Progression',
        'Time Series Pattern',
        'Ultimate Synthesis'
    ]
    
    for i, strategy in enumerate(variation_strategies):
        if i < 3:
            # High range focus variations
            nums = random.sample(frequencies['hot_numbers'][:10], 2) + random.sample([n for n in range(40, 51)], 3)
        else:
            # Balanced variations
            nums = random.sample(frequencies['hot_numbers'][:8], 3) + random.sample(frequencies['cold_numbers'][:8], 2)
        
        stars = [7, random.choice(frequencies['hot_stars'][:4])] if i % 2 == 0 else [5, random.choice(frequencies['hot_stars'][:4])]
        
        combo = {
            'numbers': sorted(nums),
            'stars': sorted(stars),
            'strategy': f'{strategy} Data-Driven',
            'method': f'Real data variation from {frequencies["total_draws"]} draws'
        }
        combinations.append(combo)
    
    return combinations

def display_final_combinations(combinations, frequencies):
    """Afficher les combinaisons finales avec métriques"""
    
    total_draws = frequencies['total_draws'] if frequencies else "N/A"
    
    print(f"\n🎯 10 COMBINAISONS OPTIMISÉES - EUROMILLIONS 6 JUIN 2025")
    print(f"Basées sur {total_draws} tirages historiques + analyse June 3")
    print("=" * 70)
    
    for i, combo in enumerate(combinations, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print(f"    Method: {combo['method']}")
        
        # Analyse de composition
        low = len([n for n in combo['numbers'] if n <= 17])
        mid = len([n for n in combo['numbers'] if 18 <= n <= 34])
        high = len([n for n in combo['numbers'] if n >= 35])
        extreme_high = len([n for n in combo['numbers'] if n >= 45])
        has_star_7 = 7 in combo['stars']
        has_star_5 = 5 in combo['stars']
        
        print(f"    Composition: {low} bas, {mid} mid, {high} haut ({extreme_high} extrême)")
        print(f"    Stars: 7: {'✓' if has_star_7 else '✗'} | 5: {'✓' if has_star_5 else '✗'}")
        print()
    
    if frequencies:
        # Métriques d'optimisation
        star_7_count = sum(1 for combo in combinations if 7 in combo['stars'])
        star_5_count = sum(1 for combo in combinations if 5 in combo['stars'])
        extreme_high_coverage = set()
        for combo in combinations:
            extreme_high_coverage.update([n for n in combo['numbers'] if n >= 45])
        
        print(f"📊 MÉTRIQUES D'OPTIMISATION:")
        print(f"    Données historiques: {frequencies['total_draws']} tirages")
        print(f"    Étoile 7 coverage: {star_7_count}/10 ({star_7_count*10}%)")
        print(f"    Étoile 5 coverage: {star_5_count}/10 ({star_5_count*10}%)")
        print(f"    Nombres extrême haut: {len(extreme_high_coverage)}/6 couverts")
        print(f"    Couverture: {sorted(extreme_high_coverage)}")

def main():
    """Fonction principale"""
    
    print("🚀 EUROMILLIONS - COMBINAISONS OPTIMISÉES 6 JUIN 2025")
    print("Données historiques complètes + insights June 3")
    print("=" * 65)
    
    # Charger les données depuis la base
    df = load_euromillions_from_database()
    
    # Analyser les fréquences
    frequencies = analyze_real_frequencies(df)
    
    # Générer les combinaisons
    combinations = generate_data_driven_combinations(frequencies)
    
    # Afficher les résultats
    display_final_combinations(combinations, frequencies)
    
    print(f"\n✅ GÉNÉRATION TERMINÉE:")
    print(f"🎯 Coverage Optimization prioritisé (meilleure stratégie June 3)")
    print(f"📊 Star 7 gap comblé (0% → optimisé)")
    print(f"🔢 Focus extrême haut 45-50 renforcé")
    print(f"🏆 Prêt pour le tirage du 6 juin 2025")
    
    return combinations

if __name__ == "__main__":
    main()