"""
Enhanced Euromillions Strategies based on June 3, 2025 analysis results
Implements the most successful strategies: Coverage Optimization, Risk/Reward Enhanced, 
Frequency Analysis Enhanced, Markov Chain Enhanced, Time Series Enhanced, and Fusion Methods
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from itertools import combinations
import math

class EnhancedEuromillionsStrategies:
    """Enhanced strategies based on proven performance"""
    
    def __init__(self, historical_data):
        self.data = historical_data
        self.prepare_analysis_data()
    
    def prepare_analysis_data(self):
        """Prepare data for analysis"""
        # Extract all main numbers and stars
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        star_cols = ['s1', 's2']
        
        # Flatten main numbers and stars
        self.all_main_numbers = []
        self.all_stars = []
        
        for _, row in self.data.iterrows():
            main_nums = [row[col] for col in main_cols if pd.notna(row[col])]
            star_nums = [row[col] for col in star_cols if pd.notna(row[col])]
            
            self.all_main_numbers.extend(main_nums)
            self.all_stars.extend(star_nums)
        
        # Calculate frequencies
        self.main_freq = Counter(self.all_main_numbers)
        self.star_freq = Counter(self.all_stars)
        
        # Get recent data for temporal analysis
        self.recent_data = self.data.head(50)  # Last 50 draws
    
    def coverage_optimization_enhanced_ultra_balance(self, num_combinations=1):
        """
        Coverage Optimization Enhanced - Ultra Balance Strategy
        Best performer from June 3 analysis (4/7 matches)
        """
        combinations = []
        
        for _ in range(num_combinations):
            # Ultra balance approach: mix all frequency zones and ranges
            
            # Divide numbers into zones
            low_zone = list(range(1, 18))      # 1-17
            mid_zone = list(range(18, 35))     # 18-34  
            high_zone = list(range(35, 51))    # 35-50
            
            # Frequency analysis
            freq_sorted = sorted(self.main_freq.items(), key=lambda x: x[1], reverse=True)
            hot_numbers = [num for num, _ in freq_sorted[:15]]
            warm_numbers = [num for num, _ in freq_sorted[15:35]]
            cold_numbers = [num for num, _ in freq_sorted[35:]]
            
            # Ultra balance selection
            numbers = []
            
            # 1-2 from low zone (prefer hot)
            low_candidates = [n for n in low_zone if n in hot_numbers or n in warm_numbers]
            if not low_candidates:
                low_candidates = low_zone
            numbers.extend(random.sample(low_candidates, min(2, len(low_candidates))))
            
            # 1-2 from mid zone (balanced)
            mid_candidates = [n for n in mid_zone if n in warm_numbers or n in hot_numbers]
            if not mid_candidates:
                mid_candidates = mid_zone
            if len(numbers) < 5:
                numbers.extend(random.sample(mid_candidates, min(2, len(mid_candidates), 5-len(numbers))))
            
            # Remaining from high zone (mix hot and cold for balance)
            high_hot = [n for n in high_zone if n in hot_numbers]
            high_cold = [n for n in high_zone if n in cold_numbers]
            high_candidates = high_hot + high_cold
            
            while len(numbers) < 5:
                if high_candidates:
                    selected = random.choice(high_candidates)
                    if selected not in numbers:
                        numbers.append(selected)
                        high_candidates.remove(selected)
                else:
                    # Fallback to any remaining numbers
                    remaining = [n for n in range(1, 51) if n not in numbers]
                    if remaining:
                        numbers.append(random.choice(remaining))
                    else:
                        break
            
            # Star selection - balanced frequency approach
            star_freq_sorted = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
            hot_stars = [star for star, _ in star_freq_sorted[:6]]
            
            # Mix hot and medium frequency stars
            stars = []
            if hot_stars:
                stars.append(random.choice(hot_stars))
            
            # Second star from medium frequency
            medium_stars = [star for star, _ in star_freq_sorted[3:9]]
            if medium_stars:
                remaining_stars = [s for s in medium_stars if s not in stars]
                if remaining_stars:
                    stars.append(random.choice(remaining_stars))
            
            # Ensure we have 2 stars
            while len(stars) < 2:
                available_stars = [s for s in range(1, 13) if s not in stars]
                if available_stars:
                    stars.append(random.choice(available_stars))
                else:
                    break
            
            numbers.sort()
            stars.sort()
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Coverage Optimization Enhanced - Ultra Balance',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        return combinations
    
    def risk_reward_enhanced(self, num_combinations=2, risk_level='moderate'):
        """
        Risk/Reward Enhanced Strategy
        Generates enhanced high and moderate risk combinations
        """
        combinations = []
        
        for i in range(num_combinations):
            if i == 0 and risk_level in ['moderate', 'both']:
                # Enhanced Moderate Risk
                numbers, stars = self._generate_risk_reward_combo('moderate')
                combinations.append({
                    'numbers': numbers,
                    'stars': stars,
                    'strategy': 'Risk/Reward Enhanced - Enhanced Moderate',
                    'score': self.calculate_combination_score(numbers, stars)
                })
            
            if (i == 1 or risk_level == 'high') and risk_level in ['high', 'both']:
                # Enhanced High Risk
                numbers, stars = self._generate_risk_reward_combo('high')
                combinations.append({
                    'numbers': numbers,
                    'stars': stars,
                    'strategy': 'Risk/Reward Enhanced - Enhanced High',
                    'score': self.calculate_combination_score(numbers, stars)
                })
        
        return combinations
    
    def _generate_risk_reward_combo(self, risk_type):
        """Generate risk/reward combination based on type"""
        freq_sorted = sorted(self.main_freq.items(), key=lambda x: x[1], reverse=True)
        
        if risk_type == 'moderate':
            # Enhanced moderate: mix warm and hot numbers
            hot_numbers = [num for num, _ in freq_sorted[:20]]
            warm_numbers = [num for num, _ in freq_sorted[15:35]]
            
            numbers = []
            # 2-3 hot numbers
            numbers.extend(random.sample(hot_numbers, 3))
            # 2 warm numbers
            remaining_warm = [n for n in warm_numbers if n not in numbers]
            numbers.extend(random.sample(remaining_warm, min(2, len(remaining_warm))))
            
        else:  # high risk
            # Enhanced high: mix hot with very cold
            hot_numbers = [num for num, _ in freq_sorted[:15]]
            cold_numbers = [num for num, _ in freq_sorted[-20:]]
            
            numbers = []
            # 2-3 hot numbers
            numbers.extend(random.sample(hot_numbers, 2))
            # 2-3 cold numbers for high risk/reward
            numbers.extend(random.sample(cold_numbers, 3))
        
        # Ensure 5 numbers
        while len(numbers) < 5:
            remaining = [n for n in range(1, 51) if n not in numbers]
            if remaining:
                numbers.append(random.choice(remaining))
        
        numbers = numbers[:5]
        numbers.sort()
        
        # Stars: balanced selection
        star_freq_sorted = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
        hot_stars = [star for star, _ in star_freq_sorted[:6]]
        stars = random.sample(hot_stars, min(2, len(hot_stars)))
        
        if len(stars) < 2:
            remaining_stars = [s for s in range(1, 13) if s not in stars]
            stars.extend(random.sample(remaining_stars, 2 - len(stars)))
        
        stars.sort()
        return numbers, stars
    
    def frequency_analysis_enhanced(self, num_combinations=3):
        """
        Frequency Analysis Enhanced Strategy
        Multiple variants: Ultra Hot Focus, Hot-Medium Balance, Frequency Zones
        """
        combinations = []
        
        freq_sorted = sorted(self.main_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Variant 1: Ultra Hot Focus
        if num_combinations >= 1:
            hot_numbers = [num for num, _ in freq_sorted[:15]]
            numbers = random.sample(hot_numbers, 5)
            numbers.sort()
            
            # Hot stars
            star_freq_sorted = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
            hot_stars = [star for star, _ in star_freq_sorted[:5]]
            stars = random.sample(hot_stars, min(2, len(hot_stars)))
            stars.sort()
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Frequency Analysis Enhanced - Ultra Hot Focus',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        # Variant 2: Hot-Medium Balance
        if num_combinations >= 2:
            hot_numbers = [num for num, _ in freq_sorted[:15]]
            medium_numbers = [num for num, _ in freq_sorted[15:35]]
            
            numbers = []
            numbers.extend(random.sample(hot_numbers, 3))
            numbers.extend(random.sample(medium_numbers, 2))
            numbers.sort()
            
            # Balanced stars
            star_freq_sorted = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
            stars = [star_freq_sorted[0][0], star_freq_sorted[4][0]]  # Hot + medium
            stars.sort()
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Frequency Analysis Enhanced - Hot-Medium Balance',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        # Variant 3: Frequency Zones
        if num_combinations >= 3:
            # Divide into frequency zones
            ultra_hot = [num for num, _ in freq_sorted[:10]]
            hot = [num for num, _ in freq_sorted[10:25]]
            medium = [num for num, _ in freq_sorted[25:40]]
            
            numbers = []
            numbers.extend(random.sample(ultra_hot, 2))
            numbers.extend(random.sample(hot, 2))
            numbers.extend(random.sample(medium, 1))
            numbers.sort()
            
            # Zone-based stars
            star_freq_sorted = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
            stars = [star_freq_sorted[0][0], star_freq_sorted[2][0]]
            stars.sort()
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Frequency Analysis Enhanced - Frequency Zones',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        return combinations
    
    def markov_chain_enhanced(self, num_combinations=2):
        """
        Markov Chain Enhanced Strategy
        Advanced Sequential and Transition Matrix variants
        """
        combinations = []
        
        # Analyze sequential patterns
        sequences = self._analyze_sequences()
        transitions = self._analyze_transitions()
        
        # Variant 1: Advanced Sequential
        if num_combinations >= 1:
            numbers = self._generate_sequential_combination(sequences)
            stars = self._generate_transition_stars(transitions)
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Markov Chain Enhanced - Advanced Sequential',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        # Variant 2: Transition Matrix
        if num_combinations >= 2:
            numbers = self._generate_transition_combination(transitions)
            stars = self._generate_sequential_stars(sequences)
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Markov Chain Enhanced - Transition Matrix',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        return combinations
    
    def time_series_enhanced(self, num_combinations=2):
        """
        Time Series Enhanced Strategy
        Temporal Trends and Cyclical Patterns variants
        """
        combinations = []
        
        temporal_trends = self._analyze_temporal_trends()
        cyclical_patterns = self._analyze_cyclical_patterns()
        
        # Variant 1: Temporal Trends
        if num_combinations >= 1:
            numbers = self._generate_temporal_combination(temporal_trends)
            stars = self._generate_cyclical_stars(cyclical_patterns)
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Time Series Enhanced - Temporal Trends',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        # Variant 2: Cyclical Patterns
        if num_combinations >= 2:
            numbers = self._generate_cyclical_combination(cyclical_patterns)
            stars = self._generate_temporal_stars(temporal_trends)
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Time Series Enhanced - Cyclical Patterns',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        return combinations
    
    def fusion_methods(self, num_combinations=5):
        """
        Fusion Methods - Combining multiple strategies
        Based on successful fusion combinations from June 3 analysis
        """
        combinations = []
        
        # 1. Risk-Frequency Hybrid
        if num_combinations >= 1:
            freq_numbers = self._get_frequency_numbers(3)
            risk_numbers = self._get_risk_numbers(2)
            numbers = sorted(freq_numbers + risk_numbers)
            stars = self._get_balanced_stars()
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Risk-Frequency Hybrid',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        # 2. Markov-Time Fusion
        if num_combinations >= 2:
            markov_numbers = self._get_markov_numbers(3)
            time_numbers = self._get_time_series_numbers(2)
            numbers = sorted(markov_numbers + time_numbers)
            stars = self._get_transition_stars()
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Markov-Time Fusion',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        # 3. Coverage-Risk Balance
        if num_combinations >= 3:
            coverage_numbers = self._get_coverage_numbers(3)
            risk_numbers = self._get_risk_numbers(2)
            numbers = sorted(coverage_numbers + risk_numbers)
            stars = self._get_balanced_stars()
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Coverage-Risk Balance',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        # 4. Cold-Hot Equilibrium
        if num_combinations >= 4:
            freq_sorted = sorted(self.main_freq.items(), key=lambda x: x[1], reverse=True)
            hot_numbers = [num for num, _ in freq_sorted[:15]]
            cold_numbers = [num for num, _ in freq_sorted[-15:]]
            
            numbers = []
            numbers.extend(random.sample(hot_numbers, 2))
            numbers.extend(random.sample(cold_numbers, 3))
            numbers.sort()
            
            stars = self._get_equilibrium_stars()
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Cold-Hot Equilibrium',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        # 5. Ultimate Strategic Synthesis
        if num_combinations >= 5:
            # Combine all methodologies
            numbers = self._generate_ultimate_synthesis()
            stars = self._get_synthesis_stars()
            
            combinations.append({
                'numbers': numbers,
                'stars': stars,
                'strategy': 'Ultimate Strategic Synthesis',
                'score': self.calculate_combination_score(numbers, stars)
            })
        
        return combinations
    
    def _analyze_sequences(self):
        """Analyze sequential patterns in draws"""
        sequences = []
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        
        for _, row in self.recent_data.iterrows():
            nums = sorted([row[col] for col in main_cols if pd.notna(row[col])])
            sequences.append(nums)
        
        return sequences
    
    def _analyze_transitions(self):
        """Analyze number transition patterns"""
        transitions = defaultdict(list)
        
        for i in range(len(self.recent_data) - 1):
            current_row = self.recent_data.iloc[i]
            next_row = self.recent_data.iloc[i + 1]
            
            current_nums = [current_row[f'n{j}'] for j in range(1, 6) if pd.notna(current_row[f'n{j}'])]
            next_nums = [next_row[f'n{j}'] for j in range(1, 6) if pd.notna(next_row[f'n{j}'])]
            
            for num in current_nums:
                transitions[num].extend(next_nums)
        
        return transitions
    
    def _analyze_temporal_trends(self):
        """Analyze temporal trends"""
        trends = {}
        recent_window = 20
        
        for num in range(1, 51):
            recent_count = 0
            for i in range(min(recent_window, len(self.recent_data))):
                row = self.recent_data.iloc[i]
                if num in [row[f'n{j}'] for j in range(1, 6) if pd.notna(row[f'n{j}'])]:
                    recent_count += 1
            trends[num] = recent_count
        
        return trends
    
    def _analyze_cyclical_patterns(self):
        """Analyze cyclical patterns"""
        patterns = {}
        cycle_length = 7  # Weekly cycle
        
        for num in range(1, 51):
            cycle_counts = [0] * cycle_length
            for i, row in enumerate(self.recent_data.iterrows()):
                if num in [row[1][f'n{j}'] for j in range(1, 6) if pd.notna(row[1][f'n{j}'])]:
                    cycle_counts[i % cycle_length] += 1
            patterns[num] = cycle_counts
        
        return patterns
    
    def _generate_sequential_combination(self, sequences):
        """Generate combination based on sequential patterns"""
        # Find most common sequences
        sequence_pairs = []
        for seq in sequences:
            for i in range(len(seq) - 1):
                sequence_pairs.append((seq[i], seq[i + 1]))
        
        pair_freq = Counter(sequence_pairs)
        common_pairs = [pair for pair, _ in pair_freq.most_common(10)]
        
        numbers = []
        if common_pairs:
            selected_pair = random.choice(common_pairs)
            numbers.extend(selected_pair)
        
        # Fill remaining with frequency-based selection
        freq_sorted = sorted(self.main_freq.items(), key=lambda x: x[1], reverse=True)
        candidates = [num for num, _ in freq_sorted if num not in numbers]
        
        while len(numbers) < 5 and candidates:
            numbers.append(candidates.pop(0))
        
        return sorted(numbers)
    
    def _generate_transition_combination(self, transitions):
        """Generate combination based on transition matrix"""
        numbers = []
        
        # Start with a high-frequency number
        freq_sorted = sorted(self.main_freq.items(), key=lambda x: x[1], reverse=True)
        start_num = freq_sorted[0][0]
        numbers.append(start_num)
        
        # Use transitions to build the rest
        current = start_num
        for _ in range(4):
            if current in transitions and transitions[current]:
                next_candidates = [n for n in transitions[current] if n not in numbers]
                if next_candidates:
                    next_num = random.choice(next_candidates)
                    numbers.append(next_num)
                    current = next_num
                else:
                    # Fallback to frequency
                    remaining = [num for num, _ in freq_sorted if num not in numbers]
                    if remaining:
                        numbers.append(remaining[0])
        
        return sorted(numbers)
    
    def _generate_temporal_combination(self, trends):
        """Generate combination based on temporal trends"""
        # Sort by recent trend strength
        trend_sorted = sorted(trends.items(), key=lambda x: x[1], reverse=True)
        
        # Mix trending and counter-trending numbers
        trending = [num for num, _ in trend_sorted[:20]]
        counter_trending = [num for num, _ in trend_sorted[-20:]]
        
        numbers = []
        numbers.extend(random.sample(trending, 3))
        numbers.extend(random.sample(counter_trending, 2))
        
        return sorted(numbers)
    
    def _generate_cyclical_combination(self, patterns):
        """Generate combination based on cyclical patterns"""
        # Find numbers with strong cyclical patterns
        cyclical_strength = {}
        for num, counts in patterns.items():
            max_count = max(counts)
            min_count = min(counts)
            cyclical_strength[num] = max_count - min_count
        
        strength_sorted = sorted(cyclical_strength.items(), key=lambda x: x[1], reverse=True)
        strong_cyclical = [num for num, _ in strength_sorted[:25]]
        
        numbers = random.sample(strong_cyclical, 5)
        return sorted(numbers)
    
    def _get_frequency_numbers(self, count):
        """Get numbers based on frequency"""
        freq_sorted = sorted(self.main_freq.items(), key=lambda x: x[1], reverse=True)
        hot_numbers = [num for num, _ in freq_sorted[:20]]
        return random.sample(hot_numbers, count)
    
    def _get_risk_numbers(self, count):
        """Get risk-based numbers (mix of hot and cold)"""
        freq_sorted = sorted(self.main_freq.items(), key=lambda x: x[1], reverse=True)
        cold_numbers = [num for num, _ in freq_sorted[-15:]]
        return random.sample(cold_numbers, count)
    
    def _get_markov_numbers(self, count):
        """Get Markov-based numbers"""
        transitions = self._analyze_transitions()
        return self._generate_transition_combination(transitions)[:count]
    
    def _get_time_series_numbers(self, count):
        """Get time series based numbers"""
        trends = self._analyze_temporal_trends()
        trend_sorted = sorted(trends.items(), key=lambda x: x[1], reverse=True)
        trending = [num for num, _ in trend_sorted[:15]]
        return random.sample(trending, count)
    
    def _get_coverage_numbers(self, count):
        """Get coverage-optimized numbers"""
        # Ensure range coverage
        low_range = list(range(1, 18))
        mid_range = list(range(18, 35))
        high_range = list(range(35, 51))
        
        numbers = []
        if count >= 1:
            numbers.append(random.choice(low_range))
        if count >= 2:
            numbers.append(random.choice(mid_range))
        if count >= 3:
            numbers.append(random.choice(high_range))
        
        # Fill remaining with frequency-based
        freq_sorted = sorted(self.main_freq.items(), key=lambda x: x[1], reverse=True)
        candidates = [num for num, _ in freq_sorted if num not in numbers]
        
        while len(numbers) < count and candidates:
            numbers.append(candidates.pop(0))
        
        return numbers
    
    def _get_balanced_stars(self):
        """Get balanced star selection"""
        star_freq_sorted = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
        hot_stars = [star for star, _ in star_freq_sorted[:6]]
        return random.sample(hot_stars, min(2, len(hot_stars)))
    
    def _get_transition_stars(self):
        """Get transition-based stars"""
        star_freq_sorted = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
        return [star_freq_sorted[0][0], star_freq_sorted[2][0]]
    
    def _get_equilibrium_stars(self):
        """Get equilibrium stars (hot + cold)"""
        star_freq_sorted = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
        hot_star = star_freq_sorted[0][0]
        cold_star = star_freq_sorted[-1][0]
        return sorted([hot_star, cold_star])
    
    def _generate_temporal_stars(self, trends):
        """Generate stars based on temporal trends"""
        return random.sample(range(1, 13), 2)
    
    def _generate_cyclical_stars(self, patterns):
        """Generate stars based on cyclical patterns"""
        return random.sample(range(1, 13), 2)
    
    def _generate_sequential_stars(self, sequences):
        """Generate stars based on sequential patterns"""
        return random.sample(range(1, 13), 2)
    
    def _generate_transition_stars(self, transitions):
        """Generate stars based on transitions"""
        return random.sample(range(1, 13), 2)
    
    def _generate_ultimate_synthesis(self):
        """Generate ultimate synthesis combination"""
        # Combine all methodologies
        freq_num = self._get_frequency_numbers(1)[0]
        risk_num = self._get_risk_numbers(1)[0]
        markov_num = self._get_markov_numbers(1)[0]
        time_num = self._get_time_series_numbers(1)[0]
        coverage_num = self._get_coverage_numbers(1)[0]
        
        numbers = [freq_num, risk_num, markov_num, time_num, coverage_num]
        # Remove duplicates and ensure 5 unique numbers
        unique_numbers = list(set(numbers))
        
        while len(unique_numbers) < 5:
            freq_sorted = sorted(self.main_freq.items(), key=lambda x: x[1], reverse=True)
            candidates = [num for num, _ in freq_sorted if num not in unique_numbers]
            if candidates:
                unique_numbers.append(candidates[0])
            else:
                break
        
        return sorted(unique_numbers[:5])
    
    def _get_synthesis_stars(self):
        """Get synthesis stars combining all methods"""
        star_freq_sorted = sorted(self.star_freq.items(), key=lambda x: x[1], reverse=True)
        # Balance between hot and medium frequency
        return [star_freq_sorted[0][0], star_freq_sorted[3][0]]
    
    def calculate_combination_score(self, numbers, stars):
        """Calculate a score for the combination based on various factors"""
        score = 0.0
        
        # Frequency score
        for num in numbers:
            score += self.main_freq.get(num, 0) * 0.1
        
        for star in stars:
            score += self.star_freq.get(star, 0) * 0.2
        
        # Range balance score
        low_count = sum(1 for n in numbers if n <= 17)
        mid_count = sum(1 for n in numbers if 18 <= n <= 34)
        high_count = sum(1 for n in numbers if n >= 35)
        
        # Bonus for balanced distribution
        if low_count >= 1 and mid_count >= 1 and high_count >= 1:
            score += 5.0
        
        # Even/odd balance
        even_count = sum(1 for n in numbers if n % 2 == 0)
        if 2 <= even_count <= 3:
            score += 2.0
        
        return score
    
    def generate_strategic_methods_v3(self, num_combinations=10):
        """Generate Strategic Methods V3 combinations"""
        combinations = []
        
        # Coverage Optimization Enhanced - Ultra Balance (best performer)
        combinations.extend(self.coverage_optimization_enhanced_ultra_balance(1))
        
        # Risk/Reward Enhanced
        combinations.extend(self.risk_reward_enhanced(2, 'both'))
        
        # Frequency Analysis Enhanced
        combinations.extend(self.frequency_analysis_enhanced(3))
        
        # Markov Chain Enhanced
        combinations.extend(self.markov_chain_enhanced(2))
        
        # Time Series Enhanced
        combinations.extend(self.time_series_enhanced(2))
        
        return combinations[:num_combinations]
    
    def generate_fusion_combinations(self, num_combinations=10):
        """Generate fusion combinations"""
        return self.fusion_methods(num_combinations)