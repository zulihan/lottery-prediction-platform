"""
Générer 4 combinaisons spécialisées en utilisant Strategic Methods:
1 Risk/Reward Balance
1 Frequency Analysis  
1 Markov Chain Model
1 Time Series Analysis
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
        
        query = """
        SELECT date, n1, n2, n3, n4, n5, s1, s2 
        FROM euromillions_drawings 
        ORDER BY date DESC 
        LIMIT 150
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print(f"✅ {len(df)} tirages historiques chargés")
        return df
        
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return None

def analyze_patterns(df):
    """Analyser les patterns pour les 4 stratégies"""
    
    all_numbers = []
    all_stars = []
    
    for _, row in df.iterrows():
        numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
        stars = [row['s1'], row['s2']]
        
        all_numbers.extend([int(n) for n in numbers if pd.notna(n)])
        all_stars.extend([int(s) for s in stars if pd.notna(s)])
    
    number_freq = Counter(all_numbers)
    star_freq = Counter(all_stars)
    
    hot_numbers = [num for num, _ in number_freq.most_common(20)]
    cold_numbers = [num for num, _ in number_freq.most_common()[-20:]]
    medium_numbers = [num for num in range(1, 51) if num not in hot_numbers and num not in cold_numbers]
    hot_stars = [star for star, _ in star_freq.most_common(8)]
    
    print(f"🔥 Hot numbers: {hot_numbers[:12]}")
    print(f"❄️ Cold numbers: {cold_numbers[:12]}")
    print(f"🌟 Hot stars: {hot_stars[:6]}")
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'medium_numbers': medium_numbers,
        'hot_stars': hot_stars,
        'number_freq': number_freq,
        'star_freq': star_freq,
        'df': df
    }

def generate_risk_reward_combination(patterns):
    """Stratégie Risk/Reward Balance - Équilibre risque/récompense optimisé"""
    
    print("\n🎯 RISK/REWARD BALANCE STRATEGY")
    print("Équilibre optimisé entre sécurité et potentiel")
    print("-" * 50)
    
    # Distribution optimisée: 40% cold (risque élevé), 60% hot (sécurité)
    cold_count = 2
    hot_count = 3
    
    # Sélectionner des numéros froids avec potentiel
    priority_cold = [n for n in patterns['cold_numbers'][:15] if patterns['number_freq'][n] >= 3]
    if len(priority_cold) < cold_count:
        priority_cold.extend(patterns['cold_numbers'][:cold_count])
    
    selected_cold = random.sample(priority_cold[:12], cold_count)
    
    # Sélectionner des numéros chauds fiables
    selected_hot = random.sample(patterns['hot_numbers'][:12], hot_count)
    
    numbers = sorted(selected_cold + selected_hot)
    
    # Étoiles: équilibrer risque/sécurité
    safe_star = patterns['hot_stars'][0]
    risk_star = random.choice([s for s in range(1, 13) if s not in patterns['hot_stars'][:3]])
    stars = sorted([safe_star, risk_star])
    
    # Calculer les métriques
    risk_score = (cold_count / 5) * 100
    safety_score = (hot_count / 5) * 100
    
    combination = {
        'numbers': numbers,
        'stars': stars,
        'strategy': 'Risk/Reward Balance Optimized',
        'cold_numbers': selected_cold,
        'hot_numbers': selected_hot,
        'risk_score': risk_score,
        'safety_score': safety_score
    }
    
    print(f"Numbers: {numbers} | Stars: {stars}")
    print(f"Cold (risque): {selected_cold} - Potentiel élevé")
    print(f"Hot (sécurité): {selected_hot} - Fiabilité")
    print(f"Risk Score: {risk_score}% | Safety Score: {safety_score}%")
    
    return combination

def generate_frequency_analysis_combination(patterns):
    """Stratégie Frequency Analysis - Analyse statistique des fréquences"""
    
    print("\n📊 FREQUENCY ANALYSIS STRATEGY")
    print("Optimisation basée sur les fréquences statistiques")
    print("-" * 50)
    
    # Segmentation par quartiles de fréquence
    total_numbers = len(patterns['number_freq'])
    quartile_size = total_numbers // 4
    
    sorted_by_freq = [num for num, _ in patterns['number_freq'].most_common()]
    
    quartiles = {
        'ultra_hot': sorted_by_freq[:quartile_size],
        'hot': sorted_by_freq[quartile_size:quartile_size*2],
        'medium': sorted_by_freq[quartile_size*2:quartile_size*3],
        'cold': sorted_by_freq[quartile_size*3:]
    }
    
    # Distribution optimale: 60% ultra_hot+hot, 40% medium+cold
    ultra_hot_pick = random.sample(quartiles['ultra_hot'][:8], 2)
    hot_pick = random.sample(quartiles['hot'][:8], 1)
    medium_pick = random.sample(quartiles['medium'][:8], 1)
    cold_pick = random.sample(quartiles['cold'][:8], 1)
    
    numbers = sorted(ultra_hot_pick + hot_pick + medium_pick + cold_pick)
    
    # Étoiles basées sur fréquence optimisée
    stars = sorted(random.sample(patterns['hot_stars'][:4], 2))
    
    # Calculer la fréquence moyenne
    avg_frequency = sum(patterns['number_freq'][n] for n in numbers) / len(numbers)
    
    combination = {
        'numbers': numbers,
        'stars': stars,
        'strategy': 'Frequency Analysis Optimized',
        'ultra_hot': ultra_hot_pick,
        'hot': hot_pick,
        'medium': medium_pick,
        'cold': cold_pick,
        'avg_frequency': avg_frequency
    }
    
    print(f"Numbers: {numbers} | Stars: {stars}")
    print(f"Ultra hot: {ultra_hot_pick} | Hot: {hot_pick}")
    print(f"Medium: {medium_pick} | Cold: {cold_pick}")
    print(f"Average frequency: {avg_frequency:.1f}")
    
    return combination

def generate_markov_chain_combination(patterns):
    """Stratégie Markov Chain Model - Transitions et séquences"""
    
    print("\n🔗 MARKOV CHAIN MODEL STRATEGY")
    print("Analyse des transitions et patterns séquentiels")
    print("-" * 50)
    
    df = patterns['df']
    
    # Construire matrice de transition
    transitions = {}
    
    for _, row in df.head(50).iterrows():
        numbers = sorted([row['n1'], row['n2'], row['n3'], row['n4'], row['n5']])
        for i in range(len(numbers)-1):
            current = numbers[i]
            next_num = numbers[i+1]
            if current not in transitions:
                transitions[current] = []
            transitions[current].append(next_num)
    
    # Commencer avec un numéro chaud prometteur
    start_number = random.choice(patterns['hot_numbers'][:8])
    sequence = [start_number]
    
    # Construire séquence avec transitions
    current = start_number
    for _ in range(4):
        if current in transitions and transitions[current]:
            # Utiliser les transitions observées
            candidates = transitions[current]
            next_num = random.choice(candidates)
            
            if next_num not in sequence and next_num <= 50:
                sequence.append(next_num)
                current = next_num
            else:
                # Fallback avec gap logique
                gap = random.choice([4, 6, 8, 11, 13])
                next_num = current + gap
                if next_num > 50:
                    next_num = random.choice(range(1, 20))
                if next_num not in sequence:
                    sequence.append(next_num)
                    current = next_num
        else:
            # Gap progression si pas de transition
            gap = random.choice([5, 7, 9, 12])
            next_num = current + gap
            if next_num > 50:
                next_num = random.choice(range(1, 25))
            if next_num not in sequence:
                sequence.append(next_num)
                current = next_num
    
    # Compléter si nécessaire
    while len(sequence) < 5:
        available = [n for n in range(1, 51) if n not in sequence]
        sequence.append(random.choice(available))
    
    numbers = sorted(sequence[:5])
    
    # Étoiles avec logique de transition
    star_transitions = {}
    for _, row in df.head(30).iterrows():
        stars = sorted([row['s1'], row['s2']])
        if len(stars) == 2:
            if stars[0] not in star_transitions:
                star_transitions[stars[0]] = []
            star_transitions[stars[0]].append(stars[1])
    
    start_star = patterns['hot_stars'][0]
    if start_star in star_transitions:
        second_star = random.choice(star_transitions[start_star])
    else:
        second_star = random.choice([s for s in patterns['hot_stars'][1:5] if s != start_star])
    
    stars = sorted([start_star, second_star])
    
    combination = {
        'numbers': numbers,
        'stars': stars,
        'strategy': 'Markov Chain Model Optimized',
        'start_number': start_number,
        'sequence_chain': sequence,
        'transition_method': 'Statistical transitions + gap logic'
    }
    
    print(f"Numbers: {numbers} | Stars: {stars}")
    print(f"Start: {start_number}")
    print(f"Chain: {' → '.join(map(str, sequence))}")
    print(f"Method: Statistical transitions with gap logic")
    
    return combination

def generate_time_series_combination(patterns):
    """Stratégie Time Series Analysis - Tendances temporelles"""
    
    print("\n📈 TIME SERIES ANALYSIS STRATEGY")
    print("Analyse des tendances et cycles temporels")
    print("-" * 50)
    
    df = patterns['df']
    
    # Analyser les tendances récentes (derniers 25 tirages)
    recent_numbers = []
    trend_weights = []
    
    for i, (_, row) in enumerate(df.head(25).iterrows()):
        numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
        weight = 25 - i  # Plus récent = plus de poids
        
        for num in numbers:
            if pd.notna(num):
                recent_numbers.append(int(num))
                trend_weights.append(weight)
    
    # Calculer score de tendance pondéré
    weighted_freq = {}
    for num, weight in zip(recent_numbers, trend_weights):
        if num not in weighted_freq:
            weighted_freq[num] = 0
        weighted_freq[num] += weight
    
    # Identifier cycles et patterns
    cycle_analysis = {}
    for num in range(1, 51):
        appearances = []
        for i, (_, row) in enumerate(df.head(50).iterrows()):
            numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            if num in numbers:
                appearances.append(i)
        
        if len(appearances) >= 2:
            intervals = [appearances[i] - appearances[i+1] for i in range(len(appearances)-1)]
            if intervals:
                cycle_analysis[num] = np.mean(intervals)
    
    # Sélection basée sur tendances et cycles
    trending_candidates = sorted(weighted_freq.items(), key=lambda x: x[1], reverse=True)[:15]
    cycle_candidates = sorted(cycle_analysis.items(), key=lambda x: x[1])[:10]  # Cycles courts
    
    # Mix tendances et cycles
    trending_picks = random.sample([num for num, _ in trending_candidates[:12]], 3)
    cycle_picks = random.sample([num for num, _ in cycle_candidates[:8]], 2)
    
    numbers = sorted(trending_picks + cycle_picks)
    
    # Étoiles avec analyse temporelle
    recent_stars = []
    for _, row in df.head(15).iterrows():
        stars = [row['s1'], row['s2']]
        recent_stars.extend([int(s) for s in stars if pd.notna(s)])
    
    recent_star_freq = Counter(recent_stars)
    trending_stars = [star for star, _ in recent_star_freq.most_common(4)]
    stars = sorted(random.sample(trending_stars, 2))
    
    combination = {
        'numbers': numbers,
        'stars': stars,
        'strategy': 'Time Series Analysis Optimized',
        'trending_numbers': trending_picks,
        'cycle_numbers': cycle_picks,
        'analysis_window': '25 recent draws',
        'method': 'Weighted trends + cycle analysis'
    }
    
    print(f"Numbers: {numbers} | Stars: {stars}")
    print(f"Trending: {trending_picks}")
    print(f"Cycle return: {cycle_picks}")
    print(f"Analysis: 25 draws weighted + cycle patterns")
    
    return combination

def main():
    """Générer les 4 combinaisons spécialisées"""
    
    print("🚀 GÉNÉRATION DE 4 COMBINAISONS SPÉCIALISÉES")
    print("Strategic Methods pour Euromillions")
    print("=" * 55)
    
    # Charger et analyser les données
    df = load_historical_data()
    if df is None:
        return None
    
    patterns = analyze_patterns(df)
    
    # Générer les 4 combinaisons spécialisées
    combinations = []
    
    print("\n" + "="*60)
    combo1 = generate_risk_reward_combination(patterns)
    combinations.append(combo1)
    
    print("\n" + "="*60)
    combo2 = generate_frequency_analysis_combination(patterns)
    combinations.append(combo2)
    
    print("\n" + "="*60)
    combo3 = generate_markov_chain_combination(patterns)
    combinations.append(combo3)
    
    print("\n" + "="*60)
    combo4 = generate_time_series_combination(patterns)
    combinations.append(combo4)
    
    # Résumé final
    print("\n" + "="*60)
    print("🎯 RÉSUMÉ DES 4 COMBINAISONS SPÉCIALISÉES")
    print("="*60)
    
    for i, combo in enumerate(combinations, 1):
        print(f"\n{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} | Stars: {combo['stars']}")
    
    print(f"\n✅ 4 combinaisons spécialisées générées avec succès!")
    print(f"🎯 Chaque stratégie utilise sa méthodologie optimisée")
    print(f"📊 Basées sur {len(df)} tirages historiques authentiques")
    
    return combinations

if __name__ == "__main__":
    main()