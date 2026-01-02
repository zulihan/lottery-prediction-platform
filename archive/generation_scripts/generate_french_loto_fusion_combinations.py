"""
Générer 10 combinaisons fusion French Loto 
basées sur les 10 Strategic Methods V3 French Loto
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
        LIMIT 100
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print(f"✅ {len(df)} tirages French Loto chargés")
        return df
        
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return None

def analyze_patterns(df):
    """Analyser les patterns French Loto"""
    
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
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'medium_numbers': medium_numbers,
        'hot_lucky': hot_lucky,
        'number_freq': number_freq,
        'lucky_freq': lucky_freq
    }

def get_strategic_v3_combinations():
    """Les 10 combinaisons Strategic Methods V3 French Loto générées"""
    return [
        {'numbers': [9, 11, 20, 29, 30], 'lucky': 9, 'strategy': 'Risk/Reward Enhanced - Enhanced High'},
        {'numbers': [19, 20, 24, 31, 35], 'lucky': 2, 'strategy': 'Risk/Reward Enhanced - Enhanced Moderate'},
        {'numbers': [30, 28, 3, 24, 13], 'lucky': 9, 'strategy': 'Frequency Analysis Enhanced - Ultra Hot Focus'},
        {'numbers': [3, 4, 10, 24, 30], 'lucky': 2, 'strategy': 'Frequency Analysis Enhanced - Hot-Medium Balance'},
        {'numbers': [3, 10, 12, 20, 39], 'lucky': 8, 'strategy': 'Frequency Analysis Enhanced - Frequency Zones'},
        {'numbers': [3, 14, 21, 30, 41], 'lucky': 7, 'strategy': 'Markov Chain Enhanced - Advanced Sequential'},
        {'numbers': [3, 7, 28, 36, 40], 'lucky': 5, 'strategy': 'Markov Chain Enhanced - Transition Matrix'},
        {'numbers': [24, 30, 34, 42, 48], 'lucky': 1, 'strategy': 'Time Series Enhanced - Temporal Trends'},
        {'numbers': [1, 23, 31, 37, 48], 'lucky': 5, 'strategy': 'Time Series Enhanced - Cyclical Patterns'},
        {'numbers': [16, 26, 28, 39, 41], 'lucky': 7, 'strategy': 'Coverage Optimization Enhanced - Ultra Balance'}
    ]

def analyze_strategic_v3_patterns():
    """Analyser les patterns dans les combinaisons Strategic V3"""
    
    strategic_combos = get_strategic_v3_combinations()
    
    all_strategic_numbers = []
    all_strategic_lucky = []
    
    for combo in strategic_combos:
        all_strategic_numbers.extend(combo['numbers'])
        all_strategic_lucky.append(combo['lucky'])
    
    strategic_freq = Counter(all_strategic_numbers)
    strategic_lucky_freq = Counter(all_strategic_lucky)
    
    most_used_numbers = [num for num, _ in strategic_freq.most_common(15)]
    most_used_lucky = [lucky for lucky, _ in strategic_lucky_freq.most_common(8)]
    
    print(f"📊 Numéros les plus utilisés dans Strategic V3: {most_used_numbers[:10]}")
    print(f"🍀 Lucky numbers les plus utilisés: {most_used_lucky}")
    
    return {
        'most_used_numbers': most_used_numbers,
        'most_used_lucky': most_used_lucky,
        'strategic_freq': strategic_freq,
        'strategic_lucky_freq': strategic_lucky_freq
    }

def generate_french_loto_fusion_combinations(patterns, strategic_patterns):
    """Générer 10 combinaisons fusion French Loto"""
    
    print(f"\n🎯 FRENCH LOTO FUSION COMBINATIONS - 10 COMBINAISONS")
    print("Mélanges intelligents des 10 Strategic Methods V3")
    print("-" * 60)
    
    fusion_combinations = []
    
    fusion_strategies = [
        'Perfect Strategic Fusion',
        'Risk-Frequency Hybrid',
        'Markov-Time Fusion',
        'Coverage-Risk Balance',
        'Hot Numbers Concentration',
        'Strategic Diversity Mix',
        'Pattern Recognition Fusion',
        'Trend-Frequency Hybrid',
        'Cold-Hot Equilibrium',
        'Ultimate Strategic Synthesis'
    ]
    
    for i, strategy_name in enumerate(fusion_strategies):
        
        if strategy_name == 'Perfect Strategic Fusion':
            # Fusion basée sur les numéros les plus utilisés
            core_numbers = random.sample(strategic_patterns['most_used_numbers'][:8], 3)
            complement_numbers = random.sample(patterns['hot_numbers'][:12], 2)
            numbers = sorted(core_numbers + complement_numbers)
            lucky = random.choice(strategic_patterns['most_used_lucky'][:4])
            
        elif strategy_name == 'Risk-Frequency Hybrid':
            # 40% Risk (cold) + 60% Frequency (hot)
            risk_numbers = random.sample(patterns['cold_numbers'][:12], 2)
            freq_numbers = random.sample(patterns['hot_numbers'][:10], 3)
            numbers = sorted(risk_numbers + freq_numbers)
            lucky = random.choice(strategic_patterns['most_used_lucky'][:5])
            
        elif strategy_name == 'Markov-Time Fusion':
            # Fusion des approches Markov et Time Series
            base_num = random.choice(strategic_patterns['most_used_numbers'][:6])
            sequence = [base_num]
            
            # Progression Markov-Time
            current = base_num
            for _ in range(4):
                gap = random.choice([4, 6, 8, 10])
                current += gap
                if current > 49:
                    current = random.choice(range(1, 20))
                if current not in sequence and current <= 49:
                    sequence.append(current)
            
            while len(sequence) < 5:
                available = [n for n in range(1, 50) if n not in sequence]
                sequence.append(random.choice(available))
            
            numbers = sorted(sequence[:5])
            lucky = random.choice([1, 5, 7, 9])  # Lucky numbers des Time Series
            
        elif strategy_name == 'Coverage-Risk Balance':
            # Équilibre coverage et risk
            coverage_picks = random.sample(strategic_patterns['most_used_numbers'][:10], 2)
            risk_picks = random.sample(patterns['cold_numbers'][:10], 1)
            balance_picks = random.sample(patterns['medium_numbers'][:10], 2)
            
            numbers = sorted(coverage_picks + risk_picks + balance_picks)
            lucky = random.choice(patterns['hot_lucky'][:4])
            
        elif strategy_name == 'Hot Numbers Concentration':
            # Concentration sur les numéros chauds
            strategic_hot = random.sample(strategic_patterns['most_used_numbers'][:8], 3)
            historical_hot = random.sample(patterns['hot_numbers'][:8], 2)
            
            numbers = sorted(strategic_hot + historical_hot)
            lucky = strategic_patterns['most_used_lucky'][0]  # Le plus utilisé
            
        elif strategy_name == 'Strategic Diversity Mix':
            # Mix diversifié des différentes stratégies
            risk_pick = random.choice(patterns['cold_numbers'][:8])
            freq_pick = random.choice(patterns['hot_numbers'][:6])
            markov_pick = random.choice(strategic_patterns['most_used_numbers'][:6])
            time_pick = random.choice(range(25, 45))  # Time series range
            coverage_pick = random.choice(patterns['medium_numbers'][:8])
            
            numbers = sorted([risk_pick, freq_pick, markov_pick, time_pick, coverage_pick])
            lucky = random.choice(strategic_patterns['most_used_lucky'][:6])
            
        elif strategy_name == 'Pattern Recognition Fusion':
            # Reconnaissance de patterns avancée
            pattern_base = strategic_patterns['most_used_numbers'][:6]
            selected_pattern = random.sample(pattern_base, 2)
            
            # Compléter avec logique de progression
            complement = []
            for base in selected_pattern:
                next_num = base + random.choice([7, 9, 12])
                if next_num <= 49 and next_num not in selected_pattern + complement:
                    complement.append(next_num)
            
            while len(complement) < 3:
                available = [n for n in range(1, 50) if n not in selected_pattern + complement]
                complement.append(random.choice(available))
            
            numbers = sorted(selected_pattern + complement[:3])
            lucky = random.choice([2, 5, 7, 8, 9])
            
        elif strategy_name == 'Trend-Frequency Hybrid':
            # Tendances + fréquences
            trend_numbers = random.sample(strategic_patterns['most_used_numbers'][:8], 2)
            freq_numbers = random.sample(patterns['hot_numbers'][:10], 3)
            
            numbers = sorted(trend_numbers + freq_numbers)
            lucky = random.choice(strategic_patterns['most_used_lucky'][:4])
            
        elif strategy_name == 'Cold-Hot Equilibrium':
            # Équilibre parfait cold/hot
            cold_selection = random.sample(patterns['cold_numbers'][:10], 2)
            hot_selection = random.sample(patterns['hot_numbers'][:8], 2)
            strategic_selection = random.sample(strategic_patterns['most_used_numbers'][:6], 1)
            
            numbers = sorted(cold_selection + hot_selection + strategic_selection)
            lucky = random.choice(strategic_patterns['most_used_lucky'][:5])
            
        else:  # Ultimate Strategic Synthesis
            # Synthèse ultime de toutes les approches
            synthesis_pool = strategic_patterns['most_used_numbers'][:10]
            selected = random.sample(synthesis_pool, 5)
            numbers = sorted(selected)
            lucky = strategic_patterns['most_used_lucky'][0] if strategic_patterns['most_used_lucky'] else 7
        
        fusion_combinations.append({
            'numbers': numbers,
            'lucky': lucky,
            'strategy': strategy_name,
            'methodology': 'French Loto Strategic Fusion'
        })
    
    return fusion_combinations

def analyze_fusion_composition(combinations, patterns):
    """Analyser la composition des combinaisons fusion"""
    
    print(f"\n📊 ANALYSE DE COMPOSITION FUSION:")
    print("-" * 45)
    
    total_cold = 0
    total_hot = 0
    total_medium = 0
    lucky_distribution = Counter()
    
    for combo in combinations:
        cold_count = len([n for n in combo['numbers'] if n in patterns['cold_numbers'][:15]])
        hot_count = len([n for n in combo['numbers'] if n in patterns['hot_numbers'][:15]])
        medium_count = 5 - cold_count - hot_count
        
        total_cold += cold_count
        total_hot += hot_count
        total_medium += medium_count
        
        lucky_distribution[combo['lucky']] += 1
    
    total_numbers = len(combinations) * 5
    
    print(f"Distribution fusion globale:")
    print(f"  Cold numbers: {total_cold}/{total_numbers} ({total_cold/total_numbers*100:.1f}%)")
    print(f"  Hot numbers: {total_hot}/{total_numbers} ({total_hot/total_numbers*100:.1f}%)")
    print(f"  Medium numbers: {total_medium}/{total_numbers} ({total_medium/total_numbers*100:.1f}%)")
    
    print(f"\nDistribution Lucky Numbers Fusion:")
    for lucky, count in lucky_distribution.most_common():
        print(f"  Lucky {lucky}: {count} fois")

def main():
    """Générer les combinaisons fusion French Loto"""
    
    print("🚀 FRENCH LOTO FUSION COMBINATIONS")
    print("Basées sur Strategic Methods V3 French Loto")
    print("=" * 50)
    
    # Charger et analyser les données
    df = load_french_loto_data()
    if df is None:
        return None
    
    patterns = analyze_patterns(df)
    
    # Analyser les patterns Strategic V3
    strategic_patterns = analyze_strategic_v3_patterns()
    
    # Générer les 10 combinaisons fusion
    fusion_combos = generate_french_loto_fusion_combinations(patterns, strategic_patterns)
    
    print(f"\n🏆 FRENCH LOTO FUSION COMBINATIONS - 10 COMBINAISONS:")
    print("=" * 60)
    
    for i, combo in enumerate(fusion_combos, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        
        # Analyser la composition
        cold_count = len([n for n in combo['numbers'] if n in patterns['cold_numbers'][:15]])
        hot_count = len([n for n in combo['numbers'] if n in patterns['hot_numbers'][:15]])
        
        print(f"    Composition: {cold_count} cold, {hot_count} hot, {5-cold_count-hot_count} medium")
        print()
    
    # Analyser la composition globale
    analyze_fusion_composition(fusion_combos, patterns)
    
    print(f"\n✅ GÉNÉRATION TERMINÉE:")
    print(f"📊 10 combinaisons French Loto Fusion")
    print(f"🎯 Basées sur Strategic Methods V3 success patterns")
    print(f"🚀 Total: 20 combinaisons French Loto optimisées")
    
    return fusion_combos

if __name__ == "__main__":
    main()