"""
Générer 10 combinaisons fusion supplémentaires 
basées sur l'analyse Strategic Methods du 30 mai
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
        LIMIT 100
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print(f"✅ {len(df)} tirages historiques chargés")
        return df
        
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return None

def analyze_patterns(df):
    """Analyser les patterns actuels"""
    
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
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'medium_numbers': medium_numbers,
        'hot_stars': hot_stars,
        'number_freq': number_freq,
        'star_freq': star_freq
    }

def get_strategic_successful_numbers():
    """Les numéros qui ont eu du succès dans Strategic Methods"""
    # Basé sur l'analyse précédente
    return {
        'risk_reward_winners': [4, 7, 14],  # Numéros capturés par Risk/Reward
        'frequency_winners': [33],           # Numéros capturés par Frequency Analysis
        'time_series_winners': [36],         # Numéros capturés par Time Series
        'most_used_strategic': [23, 29, 7, 33, 35, 44, 37, 39, 21, 20],
        'successful_stars': [1, 5, 9, 12, 3, 8]
    }

def generate_10_additional_fusion_combinations(patterns):
    """Générer 10 nouvelles combinaisons fusion avancées"""
    
    strategic_data = get_strategic_successful_numbers()
    
    combinations = []
    
    fusion_strategies = [
        'Perfect Fusion Replica',
        'Risk-Dominant Fusion',
        'Frequency-Dominant Fusion', 
        'Time Series-Dominant Fusion',
        'Hybrid Strategic Balance',
        'Enhanced Pattern Recognition',
        'Multi-Zone Convergence',
        'Strategic Amplification',
        'Optimal Distribution Fusion',
        'Ultimate Strategic Synthesis'
    ]
    
    for i, strategy_name in enumerate(fusion_strategies):
        
        if strategy_name == 'Perfect Fusion Replica':
            # Réplique exacte de la formule gagnante
            risk_nums = random.sample(patterns['cold_numbers'][:12], 2)  # 40% (2 nums)
            freq_nums = random.sample(patterns['hot_numbers'][:8], 1)    # 20% (1 num)
            time_nums = random.sample(strategic_data['most_used_strategic'][:10], 2)  # 40% (2 nums)
            numbers = sorted(risk_nums + freq_nums + time_nums)
            stars = sorted(random.sample([1, 5] + patterns['hot_stars'][:3], 2))
            
        elif strategy_name == 'Risk-Dominant Fusion':
            # 60% Risk/Reward, 40% autres
            risk_nums = random.sample(patterns['cold_numbers'][:15], 3)
            other_nums = random.sample(patterns['hot_numbers'][:10], 2)
            numbers = sorted(risk_nums + other_nums)
            stars = sorted(random.sample(strategic_data['successful_stars'][:4], 2))
            
        elif strategy_name == 'Frequency-Dominant Fusion':
            # 60% Frequency Analysis, 40% autres
            freq_nums = random.sample(patterns['hot_numbers'][:12], 3)
            other_nums = random.sample(patterns['medium_numbers'][:12], 2)
            numbers = sorted(freq_nums + other_nums)
            stars = sorted(random.sample(patterns['hot_stars'][:5], 2))
            
        elif strategy_name == 'Time Series-Dominant Fusion':
            # 60% Time Series patterns, 40% autres
            # Séquences temporelles
            base = random.choice(patterns['hot_numbers'][:8])
            sequence = [base]
            current = base
            for _ in range(2):
                current += random.choice([5, 7, 9, 11])
                if current > 50:
                    current = random.choice(range(1, 20))
                if current not in sequence:
                    sequence.append(current)
            
            # Compléter avec strategic numbers
            remaining = 5 - len(sequence)
            if remaining > 0:
                available = [n for n in strategic_data['most_used_strategic'] if n not in sequence]
                sequence.extend(random.sample(available[:8], min(remaining, len(available))))
            
            numbers = sorted(sequence[:5])
            stars = sorted(random.sample([1, 5, 3, 6], 2))
            
        elif strategy_name == 'Hybrid Strategic Balance':
            # Équilibre parfait des 3 méthodes
            risk_num = random.choice(patterns['cold_numbers'][:10])
            freq_num = random.choice(patterns['hot_numbers'][:8])
            time_num = random.choice(strategic_data['time_series_winners'] + [n for n in range(30, 45)])
            strategic_nums = random.sample(strategic_data['most_used_strategic'][:8], 2)
            
            numbers = sorted([risk_num, freq_num, time_num] + strategic_nums)
            stars = sorted(random.sample(strategic_data['successful_stars'][:6], 2))
            
        elif strategy_name == 'Enhanced Pattern Recognition':
            # Pattern basé sur les succès précédents
            pattern_base = strategic_data['risk_reward_winners'] + strategic_data['frequency_winners']
            selected_pattern = random.sample(pattern_base, 2)
            
            # Compléter avec logique de progression
            complement = []
            for base in selected_pattern:
                next_num = base + random.choice([8, 12, 16])
                if next_num <= 50 and next_num not in selected_pattern + complement:
                    complement.append(next_num)
            
            while len(complement) < 3:
                available = [n for n in range(1, 51) if n not in selected_pattern + complement]
                complement.append(random.choice(available))
            
            numbers = sorted(selected_pattern + complement[:3])
            stars = sorted(random.sample(patterns['hot_stars'][:6], 2))
            
        elif strategy_name == 'Multi-Zone Convergence':
            # Convergence des zones de fréquence
            zones = {
                'ultra_hot': patterns['hot_numbers'][:5],
                'hot': patterns['hot_numbers'][5:12],
                'medium': patterns['medium_numbers'][:10],
                'cold': patterns['cold_numbers'][:8]
            }
            
            selection = (
                random.sample(zones['ultra_hot'], 1) +
                random.sample(zones['hot'], 2) +
                random.sample(zones['medium'], 1) +
                random.sample(zones['cold'], 1)
            )
            
            numbers = sorted(selection)
            stars = sorted(random.sample(strategic_data['successful_stars'][:5], 2))
            
        elif strategy_name == 'Strategic Amplification':
            # Amplification des numéros strategic les plus utilisés
            core_strategic = random.sample(strategic_data['most_used_strategic'][:6], 3)
            amplification = []
            
            for num in core_strategic:
                # Numéros proches par amplitude
                nearby = [n for n in range(max(1, num-5), min(51, num+6)) if n != num]
                if nearby:
                    amplification.append(random.choice(nearby))
            
            numbers = sorted(core_strategic + amplification[:2])
            stars = sorted(random.sample(strategic_data['successful_stars'][:6], 2))
            
        elif strategy_name == 'Optimal Distribution Fusion':
            # Distribution optimale basée sur les succès
            distribution = {
                'low_range': random.sample(range(1, 17), 1),
                'mid_range': random.sample(range(18, 34), 2),
                'high_range': random.sample(range(35, 50), 2)
            }
            
            numbers = sorted(sum(distribution.values(), []))
            
            # Étoiles avec distribution similaire
            low_stars = [s for s in range(1, 5)]
            high_stars = [s for s in range(8, 13)]
            stars = sorted([random.choice(low_stars), random.choice(high_stars)])
            
        else:  # Ultimate Strategic Synthesis
            # Synthèse ultime de tous les insights
            synthesis_pool = (
                strategic_data['risk_reward_winners'][:2] +
                strategic_data['frequency_winners'] +
                strategic_data['most_used_strategic'][:5]
            )
            
            selected = random.sample(synthesis_pool, 5)
            numbers = sorted(selected)
            stars = sorted(random.sample([1, 5] + strategic_data['successful_stars'][:4], 2))
        
        combinations.append({
            'numbers': numbers,
            'stars': stars,
            'strategy': strategy_name,
            'methodology': 'Advanced Strategic Fusion'
        })
    
    return combinations

def main():
    """Générer les 10 combinaisons fusion supplémentaires"""
    
    print("🚀 GÉNÉRATION DE 10 COMBINAISONS FUSION SUPPLÉMENTAIRES")
    print("Basées sur l'analyse Strategic Methods du 30 mai")
    print("=" * 65)
    
    # Charger et analyser les données
    df = load_historical_data()
    if df is None:
        return None
    
    patterns = analyze_patterns(df)
    
    # Générer les 10 combinaisons fusion supplémentaires
    additional_fusion = generate_10_additional_fusion_combinations(patterns)
    
    print(f"\n🎯 10 COMBINAISONS FUSION SUPPLÉMENTAIRES:")
    print("-" * 50)
    
    for i, combo in enumerate(additional_fusion, 31):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Stars: {combo['stars']}")
        
        # Analyser la composition selon la formule gagnante
        cold_count = len([n for n in combo['numbers'] if n in patterns['cold_numbers'][:15]])
        hot_count = len([n for n in combo['numbers'] if n in patterns['hot_numbers'][:15]])
        
        print(f"    Composition: {cold_count} cold, {hot_count} hot")
        print()
    
    print(f"✅ 10 combinaisons fusion supplémentaires générées!")
    print(f"🎯 Total avec les précédentes: 40 combinaisons optimisées")
    print(f"📊 Basées sur la formule gagnante: 40% Risk/Reward + 20% Frequency + 40% Time Series")
    
    return additional_fusion

if __name__ == "__main__":
    main()