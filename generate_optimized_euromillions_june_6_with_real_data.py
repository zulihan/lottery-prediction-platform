"""
Générer 10 combinaisons Euromillions optimisées pour le 6 juin 2025
Utilisant la vraie base de données avec 1845 tirages + analyse du 3 juin
"""
import os
from sqlalchemy import create_engine, text
import pandas as pd
from collections import Counter
import random
from datetime import datetime, timedelta

def connect_to_database():
    """Se connecter à la base de données PostgreSQL"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise Exception("DATABASE_URL not found")
        
        engine = create_engine(database_url)
        return engine
    except Exception as e:
        print(f"Erreur connexion base de données: {e}")
        return None

def load_euromillions_historical_data():
    """Charger les données historiques Euromillions depuis la vraie base"""
    engine = connect_to_database()
    if not engine:
        return None
    
    try:
        # First get the column names
        with engine.connect() as conn:
            columns_result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'euromillions_drawings'
                ORDER BY ordinal_position
            """))
            columns = [row[0] for row in columns_result.fetchall()]
            print(f"Colonnes de la table: {columns}")
        
        # Use the correct table without ORDER BY to avoid column name issues
        df = pd.read_sql_query("SELECT * FROM euromillions_drawings", engine)
        print(f"✅ Données chargées: {len(df)} tirages Euromillions historiques")
        return df
        
    except Exception as e:
        print(f"❌ Erreur chargement données: {e}")
        return None

def analyze_historical_frequencies(df):
    """Analyser les fréquences historiques réelles"""
    if df is None:
        return None
    
    try:
        all_numbers = []
        all_stars = []
        
        # Afficher la structure des données pour debug
        print(f"Colonnes disponibles: {df.columns.tolist()}")
        print(f"Premier échantillon: {df.iloc[0].to_dict()}")
        
        # Based on the sample: (1875, datetime.date(2004, 2, 13), 'Friday', 32, 16, 29, 41, 36, 9, 7)
        # Il semble que les colonnes soient: id, draw_date, day, n1, n2, n3, n4, n5, s1, s2
        
        # Identifier les colonnes par position (plus fiable)
        if len(df.columns) >= 8:
            # Colonnes 3-7 sont les numéros principaux (index 3,4,5,6,7)
            # Colonnes 8-9 sont les étoiles (index 8,9)
            number_cols = df.columns[3:8].tolist()  # 5 numéros
            star_cols = df.columns[8:10].tolist()   # 2 étoiles
        else:
            # Fallback: chercher par nom
            number_cols = [col for col in df.columns if col in ['n1', 'n2', 'n3', 'n4', 'n5'] or 'number' in str(col).lower()]
            star_cols = [col for col in df.columns if col in ['s1', 's2'] or 'star' in str(col).lower()]
        
        print(f"Colonnes numéros utilisées: {number_cols}")
        print(f"Colonnes étoiles utilisées: {star_cols}")
        
        # Extraire les numéros et étoiles
        for _, row in df.iterrows():
            # Numéros principaux
            for col in number_cols:
                if col in row and pd.notna(row[col]):
                    try:
                        num = int(row[col])
                        if 1 <= num <= 50:  # Validation range Euromillions
                            all_numbers.append(num)
                    except (ValueError, TypeError):
                        continue
            
            # Étoiles
            for col in star_cols:
                if col in row and pd.notna(row[col]):
                    try:
                        star = int(row[col])
                        if 1 <= star <= 12:  # Validation range étoiles Euromillions
                            all_stars.append(star)
                    except (ValueError, TypeError):
                        continue
        
        number_freq = Counter(all_numbers)
        star_freq = Counter(all_stars)
        
        # Analyser les 100 derniers tirages pour tendances récentes
        recent_numbers = []
        recent_stars = []
        
        for _, row in df.head(100).iterrows():
            for col in number_cols:
                if col in row and pd.notna(row[col]):
                    try:
                        num = int(row[col])
                        if 1 <= num <= 50:
                            recent_numbers.append(num)
                    except (ValueError, TypeError):
                        continue
            
            for col in star_cols:
                if col in row and pd.notna(row[col]):
                    try:
                        star = int(row[col])
                        if 1 <= star <= 12:
                            recent_stars.append(star)
                    except (ValueError, TypeError):
                        continue
        
        recent_number_freq = Counter(recent_numbers)
        recent_star_freq = Counter(recent_stars)
        
        print(f"Analyse terminée: {len(all_numbers)} numéros, {len(all_stars)} étoiles")
        print(f"Top 5 numéros: {number_freq.most_common(5)}")
        print(f"Top 5 étoiles: {star_freq.most_common(5)}")
        
        return {
            'all_numbers': number_freq,
            'all_stars': star_freq,
            'recent_numbers': recent_number_freq,
            'recent_stars': recent_star_freq,
            'total_draws': len(df),
            'hot_numbers': [num for num, _ in number_freq.most_common(15)],
            'cold_numbers': [num for num, _ in number_freq.most_common()[-15:]],
            'hot_stars': [star for star, _ in star_freq.most_common(6)],
            'cold_stars': [star for star, _ in star_freq.most_common()[-6:]]
        }
        
    except Exception as e:
        print(f"Erreur analyse fréquences: {e}")
        return None

def generate_data_driven_combinations(frequencies):
    """Générer combinaisons basées sur les vraies données + insights June 3"""
    
    if frequencies is None:
        print("❌ Pas de données de fréquence disponibles")
        return []
    
    print(f"🎯 Génération avec {frequencies['total_draws']} tirages historiques")
    
    combinations = []
    
    # June 3 insights
    june_3_insights = {
        'winning_numbers': [12, 15, 38, 47, 48],
        'winning_stars': [5, 7],
        'best_strategy': 'Coverage Optimization Enhanced',
        'pattern': {'low': 2, 'mid': 0, 'high': 3}  # 60% high range
    }
    
    # 1. Coverage Optimization Data-Driven
    hot_nums = frequencies['hot_numbers'][:10]
    extreme_high = [n for n in range(45, 51) if n in hot_nums]
    if len(extreme_high) < 2:
        extreme_high.extend([47, 49])  # From June 3 pattern
    
    combo1 = {
        'numbers': [12, 15] + extreme_high[:3],  # Winning pattern + data extreme high
        'stars': [5, 7],  # June 3 winning stars
        'strategy': 'Coverage Optimization Data-Driven V1',
        'method': f'Real data hot numbers + June 3 winning pattern + extreme high focus'
    }
    combinations.append(combo1)
    
    # 2. Frequency Analysis Ultimate
    top_frequent = frequencies['hot_numbers'][:8]
    selected_freq = [n for n in top_frequent if n >= 35][:3]  # High range preferred
    if len(selected_freq) < 3:
        selected_freq.extend([38, 44])  # Fill with known hot high numbers
    
    combo2 = {
        'numbers': [frequencies['hot_numbers'][0], frequencies['hot_numbers'][2]] + selected_freq[:3],
        'stars': [frequencies['hot_stars'][0], 7],  # Most frequent + missing star 7
        'strategy': 'Frequency Analysis Ultimate Data-Driven',
        'method': f'Top frequent numbers from {frequencies["total_draws"]} draws + star 7 gap'
    }
    combinations.append(combo2)
    
    # 3. Recent Trends Analysis
    recent_hot = [num for num, _ in frequencies['recent_numbers'].most_common(10)]
    recent_high = [n for n in recent_hot if n >= 35]
    
    combo3 = {
        'numbers': recent_hot[:2] + recent_high[:3],
        'stars': [5, frequencies['recent_stars'].most_common()[0][0]],
        'strategy': 'Recent Trends Analysis Data-Driven',
        'method': 'Recent 100 draws hot numbers + June 3 winning star 5'
    }
    combinations.append(combo3)
    
    # 4. Cold Numbers Contrarian Strategy
    cold_nums = frequencies['cold_numbers']
    cold_extreme = [n for n in cold_nums if n >= 45]
    
    combo4 = {
        'numbers': [15, 38] + cold_extreme[:3],  # June 3 winners + cold extreme
        'stars': [7, frequencies['cold_stars'][0]],
        'strategy': 'Cold Numbers Contrarian Data-Driven',
        'method': 'Cold extreme high numbers + June 3 elements'
    }
    combinations.append(combo4)
    
    # 5. Balanced Hot-Cold Fusion
    hot_selection = frequencies['hot_numbers'][:5]
    cold_selection = frequencies['cold_numbers'][:5]
    
    combo5 = {
        'numbers': hot_selection[:3] + cold_selection[:2],
        'stars': [5, 7],
        'strategy': 'Hot-Cold Fusion Data-Driven',
        'method': 'Balanced hot-cold from real data + winning stars'
    }
    combinations.append(combo5)
    
    # 6-10: Generate more combinations with variations
    for i in range(5):
        # Vary the approach
        if i % 2 == 0:
            # High range focus
            nums = random.sample(frequencies['hot_numbers'], 2) + random.sample([n for n in range(35, 51)], 3)
        else:
            # Balanced approach
            nums = random.sample(frequencies['hot_numbers'], 3) + random.sample(frequencies['cold_numbers'], 2)
        
        stars = [7, random.choice(frequencies['hot_stars'])] if i < 3 else [5, random.choice(frequencies['hot_stars'])]
        
        combo = {
            'numbers': sorted(nums),
            'stars': sorted(stars),
            'strategy': f'Data-Driven Variation {i+6}',
            'method': f'Algorithm variation based on {frequencies["total_draws"]} historical draws'
        }
        combinations.append(combo)
    
    return combinations

def display_combinations(combinations, frequencies):
    """Afficher les combinaisons avec métriques"""
    
    total_draws = frequencies['total_draws'] if frequencies else "N/A"
    
    print(f"\n🚀 10 COMBINAISONS OPTIMISÉES - EUROMILLIONS 6 JUIN:")
    print(f"Basées sur {total_draws} tirages historiques + analyse June 3")
    print("=" * 65)
    
    for i, combo in enumerate(combinations, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        print(f"    Method: {combo['method']}")
        
        # Analyser la composition
        low = len([n for n in combo['numbers'] if n <= 17])
        mid = len([n for n in combo['numbers'] if 18 <= n <= 34])
        high = len([n for n in combo['numbers'] if n >= 35])
        extreme_high = len([n for n in combo['numbers'] if n >= 45])
        has_star_7 = 7 in combo['stars']
        has_star_5 = 5 in combo['stars']
        
        print(f"    Composition: {low} bas, {mid} mid, {high} haut ({extreme_high} extrême)")
        print(f"    Stars: Étoile 7: {'✅' if has_star_7 else '❌'} | Étoile 5: {'✅' if has_star_5 else '❌'}")
        print()

def main():
    """Fonction principale"""
    
    print("🚀 EUROMILLIONS - COMBINAISONS OPTIMISÉES 6 JUIN 2025")
    print("Données historiques réelles + analyse performance June 3")
    print("=" * 65)
    
    # Charger les données historiques
    df = load_euromillions_historical_data()
    
    # Analyser les fréquences
    frequencies = analyze_historical_frequencies(df)
    
    # Générer les combinaisons
    combinations = generate_data_driven_combinations(frequencies)
    
    # Afficher les résultats
    display_combinations(combinations, frequencies)
    
    if frequencies:
        # Métriques finales
        star_7_coverage = sum(1 for combo in combinations if 7 in combo['stars'])
        star_5_coverage = sum(1 for combo in combinations if 5 in combo['stars'])
        
        print(f"📊 MÉTRIQUES FINALES:")
        print(f"✅ Données historiques: {frequencies['total_draws']} tirages")
        print(f"⭐ Étoile 7 coverage: {star_7_coverage}/10 ({star_7_coverage*10}%)")
        print(f"🏆 Étoile 5 coverage: {star_5_coverage}/10 ({star_5_coverage*10}%)")
        print(f"🎯 Prêt pour le tirage du 6 juin 2025")
    
    return combinations

if __name__ == "__main__":
    main()