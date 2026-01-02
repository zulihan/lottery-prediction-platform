"""
Générer 4 combinaisons spécialisées pour le 30 mai 2025:
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
        LIMIT 200
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
    
    # Classifications pour les stratégies
    hot_numbers = [num for num, _ in number_freq.most_common(15)]
    cold_numbers = [num for num, _ in number_freq.most_common()[-15:]]
    medium_numbers = [num for num in range(1, 51) if num not in hot_numbers and num not in cold_numbers]
    
    hot_stars = [star for star, _ in star_freq.most_common(6)]
    
    print(f"🔥 Hot numbers: {hot_numbers}")
    print(f"❄️ Cold numbers: {cold_numbers}")
    print(f"🌟 Hot stars: {hot_stars}")
    
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
    """Stratégie Risk/Reward Balance - Équilibre risque/récompense"""
    
    print("\n🎯 RISK/REWARD BALANCE STRATEGY")
    print("Équilibre entre numéros sûrs (chauds) et risqués (froids)")
    print("-" * 50)
    
    # 60% numéros chauds (sûrs), 40% numéros froids (risqués)
    hot_count = 3
    cold_count = 2
    
    # Sélectionner les numéros les plus chauds pour la sécurité
    selected_hot = random.sample(patterns['hot_numbers'][:10], hot_count)
    
    # Sélectionner des numéros froids pour le potentiel
    selected_cold = random.sample(patterns['cold_numbers'][:12], cold_count)
    
    numbers = sorted(selected_hot + selected_cold)
    
    # Étoiles: 1 chaude + 1 moins fréquente pour équilibrer
    hot_star = patterns['hot_stars'][0]
    balance_star = random.choice([s for s in range(1, 13) if s not in patterns['hot_stars'][:3]])
    stars = sorted([hot_star, balance_star])
    
    # Calculer le score de risque
    risk_score = (len(selected_cold) * 0.4 + len(selected_hot) * 0.6) * 20
    
    combination = {
        'numbers': numbers,
        'stars': stars,
        'strategy': 'Risk/Reward Balance',
        'risk_level': 'Moderate',
        'hot_numbers': selected_hot,
        'cold_numbers': selected_cold,
        'risk_score': risk_score
    }
    
    print(f"Numbers: {numbers} | Stars: {stars}")
    print(f"Hot numbers (sûrs): {selected_hot}")
    print(f"Cold numbers (risqués): {selected_cold}")
    print(f"Risk Score: {risk_score:.1f}/100")
    
    return combination

def generate_frequency_analysis_combination(patterns):
    """Stratégie Frequency Analysis - Basée sur les fréquences historiques"""
    
    print("\n📊 FREQUENCY ANALYSIS STRATEGY")
    print("Basée sur l'analyse statistique des fréquences")
    print("-" * 50)
    
    # Analyser les fréquences par quartiles
    freq_quartiles = {
        'very_hot': patterns['hot_numbers'][:5],      # Top 5
        'hot': patterns['hot_numbers'][5:10],         # 6-10
        'medium': patterns['medium_numbers'][:10],    # Medium freq
        'cold': patterns['cold_numbers'][:8]          # Low freq
    }
    
    # Distribution optimale: 40% very hot, 40% hot, 20% medium
    selected_numbers = (
        random.sample(freq_quartiles['very_hot'], 2) +
        random.sample(freq_quartiles['hot'], 2) +
        random.sample(freq_quartiles['medium'], 1)
    )
    
    numbers = sorted(selected_numbers)
    
    # Étoiles basées sur fréquence
    stars = sorted(random.sample(patterns['hot_stars'][:4], 2))
    
    # Calculer le score de fréquence
    freq_score = sum(patterns['number_freq'][n] for n in numbers) / len(numbers)
    
    combination = {
        'numbers': numbers,
        'stars': stars,
        'strategy': 'Frequency Analysis',
        'distribution': '40% very hot, 40% hot, 20% medium',
        'avg_frequency': freq_score,
        'quartile_breakdown': {
            'very_hot': [n for n in numbers if n in freq_quartiles['very_hot']],
            'hot': [n for n in numbers if n in freq_quartiles['hot']],
            'medium': [n for n in numbers if n in freq_quartiles['medium']]
        }
    }
    
    print(f"Numbers: {numbers} | Stars: {stars}")
    print(f"Very hot (top 5): {combination['quartile_breakdown']['very_hot']}")
    print(f"Hot (6-10): {combination['quartile_breakdown']['hot']}")
    print(f"Medium freq: {combination['quartile_breakdown']['medium']}")
    print(f"Average frequency: {freq_score:.1f}")
    
    return combination

def generate_markov_chain_combination(patterns):
    """Stratégie Markov Chain Model - Séquences et transitions"""
    
    print("\n🔗 MARKOV CHAIN MODEL STRATEGY")
    print("Basée sur les patterns de transition entre numéros")
    print("-" * 50)
    
    # Analyser les transitions dans les tirages récents
    df = patterns['df']
    transitions = {}
    
    # Construire la matrice de transition
    for _, row in df.head(50).iterrows():  # 50 derniers tirages
        numbers = sorted([row['n1'], row['n2'], row['n3'], row['n4'], row['n5']])
        for i in range(len(numbers)-1):
            current = numbers[i]
            next_num = numbers[i+1]
            if current not in transitions:
                transitions[current] = []
            transitions[current].append(next_num)
    
    # Commencer avec un numéro chaud
    start_number = random.choice(patterns['hot_numbers'][:8])
    sequence = [start_number]
    
    # Construire la séquence avec les transitions
    current = start_number
    attempts = 0
    while len(sequence) < 5 and attempts < 20:
        if current in transitions and transitions[current]:
            # Choisir le prochain numéro basé sur les transitions
            next_candidates = transitions[current]
            next_num = random.choice(next_candidates)
            if next_num not in sequence and next_num <= 50:
                sequence.append(next_num)
                current = next_num
            else:
                # Fallback: numéro aléatoire avec logique d'espacement
                gap = random.choice([5, 7, 8, 10, 12])
                next_num = current + gap
                if next_num > 50:
                    next_num = random.choice([n for n in range(1, 20) if n not in sequence])
                if next_num not in sequence:
                    sequence.append(next_num)
                    current = next_num
        else:
            # Pas de transition connue, utiliser logique d'espacement
            gap = random.choice([6, 8, 9, 11])
            next_num = current + gap
            if next_num > 50:
                available = [n for n in range(1, 51) if n not in sequence]
                next_num = random.choice(available)
            if next_num not in sequence:
                sequence.append(next_num)
                current = next_num
        attempts += 1
    
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
        second_star = random.choice([s for s in patterns['hot_stars'][1:4] if s != start_star])
    
    stars = sorted([start_star, second_star])
    
    combination = {
        'numbers': numbers,
        'stars': stars,
        'strategy': 'Markov Chain Model',
        'start_number': start_number,
        'transition_pattern': 'Sequential probability based',
        'chain_length': len(sequence)
    }
    
    print(f"Numbers: {numbers} | Stars: {stars}")
    print(f"Start number: {start_number}")
    print(f"Transition chain: {' → '.join(map(str, sequence))}")
    print(f"Chain methodology: Sequential probability transitions")
    
    return combination

def generate_time_series_combination(patterns):
    """Stratégie Time Series Analysis - Tendances temporelles"""
    
    print("\n📈 TIME SERIES ANALYSIS STRATEGY")
    print("Basée sur l'analyse des tendances temporelles")
    print("-" * 50)
    
    df = patterns['df']
    
    # Analyser les tendances des 20 derniers tirages
    recent_numbers = []
    for _, row in df.head(20).iterrows():
        numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
        recent_numbers.extend([int(n) for n in numbers if pd.notna(n)])
    
    recent_freq = Counter(recent_numbers)
    
    # Identifier les tendances montantes (numéros en hausse)
    trending_up = [num for num, freq in recent_freq.most_common(15)]
    
    # Analyser les cycles (numéros qui reviennent cycliquement)
    cycle_analysis = {}
    for num in range(1, 51):
        appearances = []
        for i, (_, row) in enumerate(df.head(50).iterrows()):
            numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            if num in numbers:
                appearances.append(i)
        
        if len(appearances) >= 2:
            # Calculer l'intervalle moyen
            intervals = [appearances[i] - appearances[i+1] for i in range(len(appearances)-1)]
            if intervals:
                cycle_analysis[num] = np.mean(intervals)
    
    # Sélectionner des numéros avec cycles courts (plus susceptibles de revenir)
    cycle_candidates = sorted(cycle_analysis.items(), key=lambda x: x[1])[:10]
    cycle_numbers = [num for num, _ in cycle_candidates]
    
    # Construction de la combinaison: 60% trending, 40% cycle
    trending_selection = random.sample(trending_up[:12], 3)
    cycle_selection = random.sample(cycle_numbers[:8], 2)
    
    numbers = sorted(trending_selection + cycle_selection)
    
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
        'strategy': 'Time Series Analysis',
        'trending_numbers': trending_selection,
        'cycle_numbers': cycle_selection,
        'trend_analysis': '60% trending up, 40% cycle return',
        'time_window': '20 recent draws analysis'
    }
    
    print(f"Numbers: {numbers} | Stars: {stars}")
    print(f"Trending up: {trending_selection}")
    print(f"Cycle return: {cycle_selection}")
    print(f"Analysis window: Last 20 draws")
    print(f"Methodology: 60% trend + 40% cycle")
    
    return combination

def main():
    """Générer les 4 combinaisons stratégiques"""
    
    print("🚀 GÉNÉRATION DE 4 COMBINAISONS STRATÉGIQUES")
    print("Euromillions - 30 mai 2025")
    print("=" * 55)
    
    # Charger et analyser les données
    df = load_historical_data()
    if df is None:
        return None
    
    patterns = analyze_patterns(df)
    
    # Générer les 4 combinaisons
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
    print("🎯 RÉSUMÉ DES 4 COMBINAISONS STRATÉGIQUES")
    print("="*60)
    
    for i, combo in enumerate(combinations, 1):
        print(f"\n{i}. {combo['strategy']}")
        print(f"   Numbers: {combo['numbers']} | Stars: {combo['stars']}")
    
    print(f"\n✅ 4 combinaisons spécialisées générées avec succès!")
    print(f"🎯 Chaque stratégie utilise une méthodologie unique")
    print(f"📊 Basées sur {len(df)} tirages historiques authentiques")
    
    return combinations

if __name__ == "__main__":
    main()