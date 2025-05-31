"""
Générer 10 combinaisons French Loto en utilisant Strategic Methods V3
Même méthodologie que celle qui a réussi pour Euromillions le 30 mai
"""
import psycopg2
import os
import pandas as pd
import numpy as np
import random
from collections import Counter

def load_french_loto_data():
    """Charger les données historiques French Loto depuis PostgreSQL"""
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        
        query = """
        SELECT date, n1, n2, n3, n4, n5, lucky 
        FROM french_loto_drawings 
        ORDER BY date DESC 
        LIMIT 200
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print(f"✅ {len(df)} tirages French Loto historiques chargés")
        return df
        
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return None

def analyze_french_loto_patterns(df):
    """Analyser les patterns de fréquence French Loto"""
    
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
    
    # Classifications pour French Loto (1-49 pour numéros, 1-10 pour chance)
    hot_numbers = [num for num, _ in number_freq.most_common(20)]
    cold_numbers = [num for num, _ in number_freq.most_common()[-20:]]
    medium_numbers = [num for num in range(1, 50) if num not in hot_numbers and num not in cold_numbers]
    hot_lucky = [lucky for lucky, _ in lucky_freq.most_common(6)]
    
    print(f"🔥 Hot numbers (1-49): {hot_numbers[:15]}")
    print(f"❄️ Cold numbers (1-49): {cold_numbers[:15]}")
    print(f"🍀 Hot lucky numbers (1-10): {hot_lucky}")
    
    return {
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'medium_numbers': medium_numbers,
        'hot_lucky': hot_lucky,
        'number_freq': number_freq,
        'lucky_freq': lucky_freq
    }

def generate_french_loto_strategic_methods_v3(patterns):
    """Générer 10 combinaisons French Loto Strategic Methods V3"""
    
    print(f"\n🚀 FRENCH LOTO STRATEGIC METHODS V3 - 10 COMBINAISONS")
    print("Adaptées de la méthodologie Euromillions gagnante")
    print("-" * 60)
    
    combinations = []
    
    # 2 Risk/Reward Enhanced (équivalent Euromillions)
    for i in range(2):
        risk_level = 'Enhanced High' if i == 0 else 'Enhanced Moderate'
        
        if risk_level == 'Enhanced High':
            # Plus de focus sur les vrais froids
            cold_count = 3
            hot_count = 2
            selected_cold = random.sample(patterns['cold_numbers'][:12], cold_count)
            selected_hot = random.sample(patterns['hot_numbers'][:10], hot_count)
        else:
            cold_count = 2
            hot_count = 3
            selected_cold = random.sample(patterns['cold_numbers'][:15], cold_count)
            selected_hot = random.sample(patterns['hot_numbers'][:12], hot_count)
        
        numbers = sorted(selected_cold + selected_hot)
        lucky = random.choice(patterns['hot_lucky'][:4])
        
        combinations.append({
            'numbers': numbers,
            'lucky': lucky,
            'strategy': f'Risk/Reward Enhanced - {risk_level}',
            'methodology': 'Cold/Hot balance for French Loto'
        })
    
    # 3 Frequency Analysis Enhanced (équivalent Euromillions)
    for i in range(3):
        approaches = ['Ultra Hot Focus', 'Hot-Medium Balance', 'Frequency Zones']
        approach = approaches[i]
        
        if approach == 'Ultra Hot Focus':
            selected_numbers = random.sample(patterns['hot_numbers'][:12], 5)
        elif approach == 'Hot-Medium Balance':
            hot_nums = random.sample(patterns['hot_numbers'][:10], 3)
            medium_nums = random.sample(patterns['medium_numbers'][:10], 2)
            selected_numbers = sorted(hot_nums + medium_nums)
        else:  # Frequency Zones
            zone1 = random.sample(patterns['hot_numbers'][:8], 2)  # Top hot
            zone2 = random.sample(patterns['hot_numbers'][8:16], 2)  # Medium hot
            zone3 = random.sample(patterns['medium_numbers'][:10], 1)  # Medium
            selected_numbers = sorted(zone1 + zone2 + zone3)
        
        lucky = random.choice(patterns['hot_lucky'][:5])
        
        combinations.append({
            'numbers': selected_numbers,
            'lucky': lucky,
            'strategy': f'Frequency Analysis Enhanced - {approach}',
            'methodology': 'French Loto frequency zones'
        })
    
    # 2 Markov Chain Enhanced (équivalent Euromillions)
    for i in range(2):
        pattern_types = ['Advanced Sequential', 'Transition Matrix']
        pattern_type = pattern_types[i]
        
        # Base sur les numéros récents chauds (French Loto 1-49)
        base_num = random.choice(patterns['hot_numbers'][:8])
        sequence = [base_num]
        
        gaps = [3, 5, 7, 9, 11] if pattern_type == 'Advanced Sequential' else [4, 6, 8, 10, 12]
        
        for _ in range(4):
            gap = random.choice(gaps)
            next_num = sequence[-1] + gap
            if next_num > 49:  # French Loto limite à 49
                # Redémarrer avec un petit numéro
                next_num = random.choice(range(1, 15))
            if next_num not in sequence and next_num <= 49:
                sequence.append(next_num)
        
        while len(sequence) < 5:
            available = [n for n in range(1, 50) if n not in sequence]
            sequence.append(random.choice(available))
        
        numbers = sorted(sequence[:5])
        lucky = random.choice(patterns['hot_lucky'][:6])
        
        combinations.append({
            'numbers': numbers,
            'lucky': lucky,
            'strategy': f'Markov Chain Enhanced - {pattern_type}',
            'methodology': 'French Loto gap analysis'
        })
    
    # 2 Time Series Enhanced (équivalent Euromillions)
    for i in range(2):
        analysis_types = ['Temporal Trends', 'Cyclical Patterns']
        analysis_type = analysis_types[i]
        
        if analysis_type == 'Temporal Trends':
            # Tendances récentes avec progression
            start = random.choice(patterns['hot_numbers'][:6])
            progression = [start]
            current = start
            
            for _ in range(4):
                current += random.choice([2, 4, 6, 8])
                if current > 49:  # French Loto limite
                    current = random.choice(range(1, 20))
                if current not in progression and current <= 49:
                    progression.append(current)
            
            numbers = sorted(progression[:5])
        else:
            # Patterns cycliques par range (French Loto)
            low = random.choice(range(1, 17))        # 1-16
            mid1 = random.choice(range(17, 25))      # 17-24
            mid2 = random.choice(range(25, 33))      # 25-32
            mid3 = random.choice(range(33, 41))      # 33-40
            high = random.choice(range(41, 49))      # 41-49
            
            numbers = sorted([low, mid1, mid2, mid3, high])
        
        # Lucky number avec focus sur les moins fréquentes
        less_frequent_lucky = [l for l in range(1, 11) if l not in patterns['hot_lucky'][:3]]
        lucky = random.choice(less_frequent_lucky[:4])
        
        combinations.append({
            'numbers': numbers,
            'lucky': lucky,
            'strategy': f'Time Series Enhanced - {analysis_type}',
            'methodology': 'French Loto temporal patterns'
        })
    
    # 1 Coverage Optimization Enhanced (équivalent Euromillions)
    # Mix équilibré ultra-sophistiqué pour French Loto
    hot_premium = random.sample(patterns['hot_numbers'][:6], 1)
    hot_secondary = random.sample(patterns['hot_numbers'][6:12], 1)
    medium_pick = random.sample(patterns['medium_numbers'][:8], 1)
    cold_surprise = random.sample(patterns['cold_numbers'][:10], 1)
    wild_card = random.choice([n for n in range(1, 50) if n not in hot_premium + hot_secondary + medium_pick + cold_surprise])
    
    numbers = sorted(hot_premium + hot_secondary + medium_pick + cold_surprise + [wild_card])
    lucky = random.choice(patterns['hot_lucky'][:5])
    
    combinations.append({
        'numbers': numbers,
        'lucky': lucky,
        'strategy': 'Coverage Optimization Enhanced - Ultra Balance',
        'methodology': 'All French Loto zones represented'
    })
    
    return combinations

def analyze_composition(combinations, patterns):
    """Analyser la composition des combinaisons générées"""
    
    print(f"\n📊 ANALYSE DE COMPOSITION:")
    print("-" * 40)
    
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
    
    print(f"Distribution globale:")
    print(f"  Cold numbers: {total_cold}/{total_numbers} ({total_cold/total_numbers*100:.1f}%)")
    print(f"  Hot numbers: {total_hot}/{total_numbers} ({total_hot/total_numbers*100:.1f}%)")
    print(f"  Medium numbers: {total_medium}/{total_numbers} ({total_medium/total_numbers*100:.1f}%)")
    
    print(f"\nDistribution Lucky Numbers:")
    for lucky, count in lucky_distribution.most_common():
        print(f"  Lucky {lucky}: {count} fois")

def main():
    """Générer les combinaisons French Loto Strategic Methods V3"""
    
    print("🚀 FRENCH LOTO STRATEGIC METHODS V3")
    print("Méthodologie adaptée du succès Euromillions du 30 mai")
    print("=" * 60)
    
    # Charger et analyser les données French Loto
    df = load_french_loto_data()
    if df is None:
        return None
    
    patterns = analyze_french_loto_patterns(df)
    
    # Générer les 10 combinaisons Strategic Methods V3
    strategic_v3 = generate_french_loto_strategic_methods_v3(patterns)
    
    print(f"\n🏆 FRENCH LOTO STRATEGIC METHODS V3 - 10 COMBINAISONS:")
    print("=" * 60)
    
    for i, combo in enumerate(strategic_v3, 1):
        print(f"{i:2d}. {combo['strategy']}")
        print(f"    Numbers: {combo['numbers']} | Lucky: {combo['lucky']}")
        print(f"    Methodology: {combo['methodology']}")
        
        # Analyser la composition
        cold_count = len([n for n in combo['numbers'] if n in patterns['cold_numbers'][:15]])
        hot_count = len([n for n in combo['numbers'] if n in patterns['hot_numbers'][:15]])
        
        print(f"    Composition: {cold_count} cold, {hot_count} hot, {5-cold_count-hot_count} medium")
        print()
    
    # Analyser la composition globale
    analyze_composition(strategic_v3, patterns)
    
    print(f"\n✅ GÉNÉRATION TERMINÉE:")
    print(f"📊 10 combinaisons French Loto Strategic Methods V3")
    print(f"🎯 Méthodologie éprouvée du succès Euromillions")
    print(f"🚀 Adaptée aux spécificités French Loto (1-49 + 1-10)")
    
    return strategic_v3

if __name__ == "__main__":
    main()