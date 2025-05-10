import os
import sys
import random
import logging
import numpy as np
from datetime import datetime, date, timedelta
from collections import Counter
import json
import pandas as pd

# Add relative import support
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import database

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FrenchLotoStrategy:
    """
    Strategy for French Loto predictions.
    French Loto draws 5 numbers from 1-49 and 1 lucky number from 1-10.
    """
    
    def __init__(self, historical_data=None):
        """
        Initialize with historical data if available
        
        Args:
            historical_data: DataFrame with historical draws or path to CSV file
        """
        # Game parameters
        self.num_range = (1, 49)  # Main numbers range
        self.lucky_range = (1, 10)  # Lucky number range
        self.main_count = 5  # Number of main numbers to select
        self.lucky_count = 1  # Number of lucky numbers to select
        
        # Number group ranges
        self.number_groups = {
            'low': list(range(1, 17)),     # 1-16
            'mid': list(range(17, 33)),    # 17-32
            'high': list(range(33, 50))    # 33-49
        }
        
        # Optimal balanced distribution
        self.optimal_distribution = {
            'low': 2,   # 2 numbers from low range
            'mid': 2,   # 2 numbers from mid range
            'high': 1   # 1 number from high range
        }
        
        # Load and prepare historical data
        self.historical_data = self.load_historical_data(historical_data)
        
        # Initialize frequency weights
        self.number_weights, self.lucky_weights = self.calculate_weights()
    
    def load_historical_data(self, data_source=None):
        """
        Load historical data from various sources
        
        Args:
            data_source: DataFrame or path to CSV file
            
        Returns:
            DataFrame with historical data
        """
        # Try to load data from given source
        if data_source is not None:
            if isinstance(data_source, pd.DataFrame):
                logger.info(f"Using provided DataFrame with {len(data_source)} records")
                return data_source
            elif isinstance(data_source, str) and os.path.exists(data_source):
                try:
                    df = pd.read_csv(data_source)
                    logger.info(f"Loaded data from {data_source} with {len(df)} records")
                    return df
                except Exception as e:
                    logger.error(f"Failed to load data from {data_source}: {e}")
        
        # Try to create table if it doesn't exist
        self.create_loto_table_if_not_exists()
        
        # Try to load from database
        try:
            df = self.get_loto_draws_from_db()
            if df is not None and len(df) > 0:
                logger.info(f"Loaded {len(df)} records from database")
                return df
        except Exception as e:
            logger.error(f"Failed to load data from database: {e}")
        
        # If no data is available, create empty DataFrame with correct structure
        logger.warning("No historical data available. Creating empty DataFrame")
        return pd.DataFrame(columns=['date', 'n1', 'n2', 'n3', 'n4', 'n5', 'lucky'])
    
    def create_loto_table_if_not_exists(self):
        """Create French Loto table in database if it doesn't exist"""
        try:
            from sqlalchemy import Column, Integer, Date, String, Float, Boolean, create_engine, inspect
            from sqlalchemy.ext.declarative import declarative_base
            from sqlalchemy.orm import sessionmaker
            import os
            
            # Get database URL from environment
            database_url = os.environ.get('DATABASE_URL')
            if not database_url:
                logger.error("No DATABASE_URL environment variable found")
                return
            
            # Create engine and base
            engine = create_engine(database_url)
            Base = declarative_base()
            
            # Define FrenchLotoDrawing model
            class FrenchLotoDrawing(Base):
                __tablename__ = 'french_loto_drawings'
                
                id = Column(Integer, primary_key=True)
                date = Column(Date, nullable=False, unique=True)
                day_of_week = Column(String(20))
                n1 = Column(Integer, nullable=False)
                n2 = Column(Integer, nullable=False)
                n3 = Column(Integer, nullable=False)
                n4 = Column(Integer, nullable=False)
                n5 = Column(Integer, nullable=False)
                lucky = Column(Integer, nullable=False)
            
            # Check if table exists
            inspector = inspect(engine)
            if not inspector.has_table('french_loto_drawings'):
                # Create table
                Base.metadata.create_all(engine)
                logger.info("Created french_loto_drawings table")
        
        except Exception as e:
            logger.error(f"Failed to create French Loto table: {e}")
    
    def get_loto_draws_from_db(self):
        """
        Get French Loto drawings from database
        
        Returns:
            DataFrame with drawings
        """
        try:
            from sqlalchemy import create_engine
            import os
            
            # Get database URL from environment
            database_url = os.environ.get('DATABASE_URL')
            if not database_url:
                logger.error("No DATABASE_URL environment variable found")
                return None
            
            # Create engine
            engine = create_engine(database_url)
            
            # Query all drawings
            query = "SELECT * FROM french_loto_drawings ORDER BY date"
            df = pd.read_sql(query, engine)
            
            return df
        
        except Exception as e:
            logger.error(f"Failed to get Loto drawings from database: {e}")
            return None
    
    def save_loto_draw_to_db(self, date, numbers, lucky, day_of_week=None):
        """
        Save a French Loto draw to the database
        
        Args:
            date: Date of the draw
            numbers: List of 5 main numbers
            lucky: Lucky number
            day_of_week: Day of the week
            
        Returns:
            bool: True if saved successfully
        """
        try:
            from sqlalchemy import create_engine, text
            import os
            from datetime import datetime
            
            # Validate inputs
            if not isinstance(numbers, list) or len(numbers) != 5:
                logger.error(f"Invalid numbers: {numbers}. Expected list of 5 integers")
                return False
            
            # Ensure date is in correct format
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Get database URL from environment
            database_url = os.environ.get('DATABASE_URL')
            if not database_url:
                logger.error("No DATABASE_URL environment variable found")
                return False
            
            # Create engine
            engine = create_engine(database_url)
            
            # Check if this date already exists
            check_query = text("SELECT id FROM french_loto_drawings WHERE date = :date")
            with engine.connect() as conn:
                result = conn.execute(check_query, {"date": date})
                if result.fetchone():
                    logger.warning(f"Draw for date {date} already exists in database")
                    return False
            
            # Insert new draw
            insert_query = text("""
                INSERT INTO french_loto_drawings (date, day_of_week, n1, n2, n3, n4, n5, lucky)
                VALUES (:date, :day_of_week, :n1, :n2, :n3, :n4, :n5, :lucky)
            """)
            
            with engine.connect() as conn:
                conn.execute(insert_query, {
                    "date": date,
                    "day_of_week": day_of_week,
                    "n1": numbers[0],
                    "n2": numbers[1],
                    "n3": numbers[2],
                    "n4": numbers[3],
                    "n5": numbers[4],
                    "lucky": lucky
                })
                conn.commit()
            
            logger.info(f"Saved draw for date {date} to database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save Loto draw to database: {e}")
            return False
    
    def save_generated_combination(self, numbers, lucky, strategy, score, target_draw_date=None):
        """
        Save a generated combination to the database
        
        Args:
            numbers: List of 5 main numbers
            lucky: Lucky number or list of lucky numbers
            strategy: Strategy used to generate
            score: Confidence score
            target_draw_date: Target draw date
        
        Returns:
            int: ID of saved combination or None if failed
        """
        try:
            # Ensure lucky is a list
            if not isinstance(lucky, list):
                lucky = [lucky]
                
            # Convert to string format for saving
            numbers_str = json.dumps(numbers)
            lucky_str = json.dumps(lucky)
            
            # Use existing save_generated_combination function but mark as French Loto
            strategy = f"French Loto - {strategy}"
            
            # Call database function
            combination_id = database.save_generated_combination(
                numbers=numbers,
                stars=lucky,  # Use stars field for lucky numbers
                strategy=strategy,
                score=score,
                target_draw_date=target_draw_date
            )
            
            return combination_id
            
        except Exception as e:
            logger.error(f"Failed to save generated combination: {e}")
            return None
    
    def calculate_weights(self):
        """
        Calculate weights for numbers and lucky numbers based on historical frequency
        
        Returns:
            tuple: (number_weights, lucky_weights)
        """
        # Initialize with equal weights
        number_weights = {n: 1.0 for n in range(self.num_range[0], self.num_range[1] + 1)}
        lucky_weights = {n: 1.0 for n in range(self.lucky_range[0], self.lucky_range[1] + 1)}
        
        # If no historical data, return equal weights
        if self.historical_data is None or len(self.historical_data) == 0:
            return number_weights, lucky_weights
        
        # Count frequencies
        number_counts = {}
        lucky_counts = {}
        
        for _, row in self.historical_data.iterrows():
            # Skip rows with missing data
            if any(pd.isna(row[f'n{i}']) for i in range(1, 6)) or pd.isna(row['lucky']):
                continue
                
            # Count main numbers
            for i in range(1, 6):
                num = int(row[f'n{i}'])
                number_counts[num] = number_counts.get(num, 0) + 1
            
            # Count lucky numbers
            lucky = int(row['lucky'])
            lucky_counts[lucky] = lucky_counts.get(lucky, 0) + 1
        
        # Calculate normalized weights based on frequency
        if number_counts:
            max_num_count = max(number_counts.values())
            for num, count in number_counts.items():
                # Scale between 0.5 and 1.5
                number_weights[num] = 0.5 + (count / max_num_count)
        
        if lucky_counts:
            max_lucky_count = max(lucky_counts.values())
            for num, count in lucky_counts.items():
                # Scale between 0.5 and 1.5
                lucky_weights[num] = 0.5 + (count / max_lucky_count)
        
        return number_weights, lucky_weights
    
    def get_hot_cold_numbers(self):
        """
        Identify hot and cold numbers
        
        Returns:
            dict: Hot and cold numbers and lucky numbers
        """
        result = {
            'hot_numbers': [],
            'cold_numbers': [],
            'hot_lucky': [],
            'cold_lucky': []
        }
        
        # Sort by weight
        sorted_numbers = sorted(self.number_weights.items(), key=lambda x: x[1], reverse=True)
        sorted_lucky = sorted(self.lucky_weights.items(), key=lambda x: x[1], reverse=True)
        
        # Get top 20% as hot, bottom 20% as cold
        hot_count = max(int(len(sorted_numbers) * 0.2), 5)
        cold_count = max(int(len(sorted_numbers) * 0.2), 5)
        
        result['hot_numbers'] = [n for n, _ in sorted_numbers[:hot_count]]
        result['cold_numbers'] = [n for n, _ in sorted_numbers[-cold_count:]]
        
        # For lucky numbers, get top 30% as hot, bottom 30% as cold
        hot_lucky_count = max(int(len(sorted_lucky) * 0.3), 2)
        cold_lucky_count = max(int(len(sorted_lucky) * 0.3), 2)
        
        result['hot_lucky'] = [n for n, _ in sorted_lucky[:hot_lucky_count]]
        result['cold_lucky'] = [n for n, _ in sorted_lucky[-cold_lucky_count:]]
        
        return result
    
    def generate_balanced_combination(self, risk_level=0.5):
        """
        Generate a balanced combination
        
        Args:
            risk_level: Risk level (0-1)
            
        Returns:
            tuple: (numbers, lucky, score)
        """
        # Adjust weights based on risk level
        adjusted_weights = self.number_weights.copy()
        
        # For higher risk, add randomness
        if risk_level > 0.5:
            for n in adjusted_weights:
                # Add random factor proportional to risk
                random_factor = 1.0 + ((random.random() - 0.5) * risk_level)
                adjusted_weights[n] *= random_factor
        
        # Select numbers according to optimal distribution
        selected_numbers = []
        
        # Select from low range
        low_nums = self.number_groups['low']
        low_weights = [adjusted_weights.get(n, 1.0) for n in low_nums]
        sum_weights = sum(low_weights)
        low_probs = [w/sum_weights for w in low_weights] if sum_weights > 0 else None
        
        if low_nums and low_probs:
            chosen_low = np.random.choice(
                low_nums, 
                size=min(self.optimal_distribution['low'], len(low_nums)),
                replace=False,
                p=low_probs
            )
            selected_numbers.extend(chosen_low)
        
        # Select from mid range
        mid_nums = self.number_groups['mid']
        mid_weights = [adjusted_weights.get(n, 1.0) for n in mid_nums]
        sum_weights = sum(mid_weights)
        mid_probs = [w/sum_weights for w in mid_weights] if sum_weights > 0 else None
        
        if mid_nums and mid_probs:
            chosen_mid = np.random.choice(
                mid_nums, 
                size=min(self.optimal_distribution['mid'], len(mid_nums)),
                replace=False,
                p=mid_probs
            )
            selected_numbers.extend(chosen_mid)
        
        # Select from high range
        high_nums = self.number_groups['high']
        high_weights = [adjusted_weights.get(n, 1.0) for n in high_nums]
        sum_weights = sum(high_weights)
        high_probs = [w/sum_weights for w in high_weights] if sum_weights > 0 else None
        
        if high_nums and high_probs:
            chosen_high = np.random.choice(
                high_nums, 
                size=min(self.optimal_distribution['high'], len(high_nums)),
                replace=False,
                p=high_probs
            )
            selected_numbers.extend(chosen_high)
        
        # Ensure we have exactly 5 numbers
        selected_numbers = list(set(selected_numbers))
        
        # Fill remaining slots if needed
        while len(selected_numbers) < 5:
            remaining = [n for n in range(self.num_range[0], self.num_range[1] + 1) 
                         if n not in selected_numbers]
            if remaining:
                remaining_weights = [adjusted_weights.get(n, 1.0) for n in remaining]
                sum_weights = sum(remaining_weights)
                remaining_probs = [w/sum_weights for w in remaining_weights] if sum_weights > 0 else None
                
                if remaining_probs:
                    chosen = np.random.choice(remaining, p=remaining_probs)
                    selected_numbers.append(chosen)
                else:
                    selected_numbers.append(random.choice(remaining))
            else:
                break
        
        # Select 1 lucky number
        lucky_nums = list(range(self.lucky_range[0], self.lucky_range[1] + 1))
        lucky_weights = [self.lucky_weights.get(n, 1.0) for n in lucky_nums]
        sum_weights = sum(lucky_weights)
        lucky_probs = [w/sum_weights for w in lucky_weights] if sum_weights > 0 else None
        
        if lucky_probs:
            selected_lucky = int(np.random.choice(lucky_nums, p=lucky_probs))
        else:
            selected_lucky = random.choice(lucky_nums)
        
        # Sort the numbers
        selected_numbers.sort()
        
        # Calculate score
        score = self.calculate_score(selected_numbers, selected_lucky)
        
        return selected_numbers, selected_lucky, score
    
    def generate_pattern_combination(self, pattern_type="consecutive"):
        """
        Generate a combination with a specific pattern
        
        Args:
            pattern_type: Pattern type ("consecutive", "even_odd", "sum_range")
            
        Returns:
            tuple: (numbers, lucky, score)
        """
        selected_numbers = []
        
        if pattern_type == "consecutive":
            # Include at least one pair of consecutive numbers
            start = random.randint(self.num_range[0], self.num_range[1] - 1)
            selected_numbers.append(start)
            selected_numbers.append(start + 1)
            
            # Select remaining numbers normally
            remaining = 5 - len(selected_numbers)
            candidates = [n for n in range(self.num_range[0], self.num_range[1] + 1) 
                          if n not in selected_numbers]
            
            # Weight by frequency
            weights = [self.number_weights.get(n, 1.0) for n in candidates]
            sum_weights = sum(weights)
            probs = [w/sum_weights for w in weights] if sum_weights > 0 else None
            
            if probs and candidates:
                additional = list(np.random.choice(
                    candidates, 
                    size=min(remaining, len(candidates)),
                    replace=False,
                    p=probs
                ))
                selected_numbers.extend(additional)
        
        elif pattern_type == "even_odd":
            # Create a specific even/odd pattern
            # Decide on even/odd count
            even_count = random.choice([2, 3])
            odd_count = 5 - even_count
            
            # Get even and odd candidates
            even_candidates = [n for n in range(self.num_range[0], self.num_range[1] + 1) if n % 2 == 0]
            odd_candidates = [n for n in range(self.num_range[0], self.num_range[1] + 1) if n % 2 == 1]
            
            # Weight by frequency
            even_weights = [self.number_weights.get(n, 1.0) for n in even_candidates]
            sum_even = sum(even_weights)
            even_probs = [w/sum_even for w in even_weights] if sum_even > 0 else None
            
            odd_weights = [self.number_weights.get(n, 1.0) for n in odd_candidates]
            sum_odd = sum(odd_weights)
            odd_probs = [w/sum_odd for w in odd_weights] if sum_odd > 0 else None
            
            # Select even numbers
            if even_probs and even_candidates:
                even_selection = list(np.random.choice(
                    even_candidates, 
                    size=min(even_count, len(even_candidates)),
                    replace=False,
                    p=even_probs
                ))
                selected_numbers.extend(even_selection)
            
            # Select odd numbers
            if odd_probs and odd_candidates:
                odd_selection = list(np.random.choice(
                    odd_candidates, 
                    size=min(odd_count, len(odd_candidates)),
                    replace=False,
                    p=odd_probs
                ))
                selected_numbers.extend(odd_selection)
        
        elif pattern_type == "sum_range":
            # Create a combination with a specific sum range
            # Choose a target sum range
            # French Loto (5 numbers from 1-49) has a min sum of 15 and max sum of 245
            # Divide into low (15-90), medium (91-170), high (171-245)
            sum_ranges = [
                (15, 90),    # Low sum
                (91, 170),   # Medium sum
                (171, 245)   # High sum
            ]
            target_range = random.choice(sum_ranges)
            
            # Start with a random number
            candidates = list(range(self.num_range[0], self.num_range[1] + 1))
            weights = [self.number_weights.get(n, 1.0) for n in candidates]
            sum_weights = sum(weights)
            probs = [w/sum_weights for w in weights] if sum_weights > 0 else None
            
            if probs:
                first_num = int(np.random.choice(candidates, p=probs))
            else:
                first_num = random.choice(candidates)
                
            selected_numbers.append(first_num)
            current_sum = first_num
            
            # Add numbers until we have 5 or reach target range
            while len(selected_numbers) < 5:
                remaining = 5 - len(selected_numbers)
                min_needed = target_range[0] - current_sum
                max_allowed = target_range[1] - current_sum
                
                min_per_num = max(1, min_needed // remaining)
                max_per_num = min(49, max_allowed // remaining)
                
                # If min > max, adjust to allow some flexibility
                if min_per_num > max_per_num:
                    min_per_num = max(1, max_per_num - 5)
                    max_per_num = min(49, min_per_num + 10)
                
                # Get candidates in range that aren't already selected
                range_candidates = [n for n in range(min_per_num, max_per_num + 1) 
                                   if n not in selected_numbers 
                                   and self.num_range[0] <= n <= self.num_range[1]]
                
                if not range_candidates:
                    # If no candidates in range, just get any unselected number
                    range_candidates = [n for n in range(self.num_range[0], self.num_range[1] + 1) 
                                       if n not in selected_numbers]
                
                if range_candidates:
                    # Weight by frequency
                    weights = [self.number_weights.get(n, 1.0) for n in range_candidates]
                    sum_weights = sum(weights)
                    probs = [w/sum_weights for w in weights] if sum_weights > 0 else None
                    
                    if probs:
                        next_num = int(np.random.choice(range_candidates, p=probs))
                    else:
                        next_num = random.choice(range_candidates)
                        
                    selected_numbers.append(next_num)
                    current_sum += next_num
                else:
                    break
        
        else:  # Default to basic frequency selection
            candidates = list(range(self.num_range[0], self.num_range[1] + 1))
            weights = [self.number_weights.get(n, 1.0) for n in candidates]
            sum_weights = sum(weights)
            probs = [w/sum_weights for w in weights] if sum_weights > 0 else None
            
            if probs:
                selected_numbers = list(np.random.choice(
                    candidates, 
                    size=min(5, len(candidates)),
                    replace=False,
                    p=probs
                ))
            else:
                selected_numbers = random.sample(candidates, min(5, len(candidates)))
        
        # Ensure we have exactly 5 numbers
        selected_numbers = list(set(selected_numbers))
        
        # Fill remaining slots if needed
        while len(selected_numbers) < 5:
            remaining = [n for n in range(self.num_range[0], self.num_range[1] + 1) 
                         if n not in selected_numbers]
            if remaining:
                weights = [self.number_weights.get(n, 1.0) for n in remaining]
                sum_weights = sum(weights)
                probs = [w/sum_weights for w in weights] if sum_weights > 0 else None
                
                if probs:
                    chosen = int(np.random.choice(remaining, p=probs))
                else:
                    chosen = random.choice(remaining)
                    
                selected_numbers.append(chosen)
            else:
                break
        
        # Select 1 lucky number
        lucky_nums = list(range(self.lucky_range[0], self.lucky_range[1] + 1))
        lucky_weights = [self.lucky_weights.get(n, 1.0) for n in lucky_nums]
        sum_weights = sum(lucky_weights)
        lucky_probs = [w/sum_weights for w in lucky_weights] if sum_weights > 0 else None
        
        if lucky_probs:
            selected_lucky = int(np.random.choice(lucky_nums, p=lucky_probs))
        else:
            selected_lucky = random.choice(lucky_nums)
        
        # Sort the numbers
        selected_numbers.sort()
        
        # Calculate score
        score = self.calculate_score(selected_numbers, selected_lucky)
        
        return selected_numbers, selected_lucky, score
    
    def generate_coverage_combination(self, existing_combinations):
        """
        Generate a combination that provides good coverage with existing combinations
        
        Args:
            existing_combinations: List of existing combinations [(numbers, lucky, score), ...]
            
        Returns:
            tuple: (numbers, lucky, score)
        """
        # Count which numbers and lucky numbers are already covered
        covered_numbers = Counter()
        covered_lucky = Counter()
        
        for numbers, lucky, _ in existing_combinations:
            for num in numbers:
                covered_numbers[num] += 1
            covered_lucky[lucky] += 1
        
        # Create inverse weights (less covered = higher weight)
        inverse_weights = {}
        for n in range(self.num_range[0], self.num_range[1] + 1):
            # Combine inverse coverage with frequency weight
            base_weight = self.number_weights.get(n, 1.0)
            coverage_factor = 1.0 / (covered_numbers.get(n, 0) + 1)
            inverse_weights[n] = base_weight * coverage_factor
        
        # Normalize weights
        total_weight = sum(inverse_weights.values())
        probs = {n: w/total_weight for n, w in inverse_weights.items()}
        
        # Select 5 numbers using the inverse weights
        candidates = list(range(self.num_range[0], self.num_range[1] + 1))
        probs_list = [probs.get(n, 0) for n in candidates]
        
        selected_numbers = list(np.random.choice(
            candidates, 
            size=min(5, len(candidates)),
            replace=False,
            p=probs_list
        ))
        
        # Do the same for lucky number
        inverse_lucky_weights = {}
        for n in range(self.lucky_range[0], self.lucky_range[1] + 1):
            base_weight = self.lucky_weights.get(n, 1.0)
            coverage_factor = 1.0 / (covered_lucky.get(n, 0) + 1)
            inverse_lucky_weights[n] = base_weight * coverage_factor
        
        # Normalize lucky weights
        total_lucky_weight = sum(inverse_lucky_weights.values())
        lucky_probs = {n: w/total_lucky_weight for n, w in inverse_lucky_weights.items()}
        
        # Select 1 lucky number
        lucky_candidates = list(range(self.lucky_range[0], self.lucky_range[1] + 1))
        lucky_probs_list = [lucky_probs.get(n, 0) for n in lucky_candidates]
        
        selected_lucky = int(np.random.choice(
            lucky_candidates, 
            p=lucky_probs_list
        ))
        
        # Sort numbers
        selected_numbers.sort()
        
        # Calculate score
        score = self.calculate_score(selected_numbers, selected_lucky)
        
        return selected_numbers, selected_lucky, score
    
    def calculate_score(self, numbers, lucky):
        """
        Calculate a confidence score for the combination
        
        Args:
            numbers: List of selected main numbers
            lucky: Selected lucky number
            
        Returns:
            float: Confidence score (0-100)
        """
        score = 75.0  # Base score
        
        # Calculate weighted scores based on frequencies
        number_score = sum(self.number_weights.get(n, 1.0) for n in numbers) / len(numbers)
        lucky_score = self.lucky_weights.get(lucky, 1.0)
        
        # Normalize scores
        max_num_weight = max(self.number_weights.values())
        max_lucky_weight = max(self.lucky_weights.values())
        
        normalized_number_score = (number_score / max_num_weight) * 15  # Up to 15 points
        normalized_lucky_score = (lucky_score / max_lucky_weight) * 5  # Up to 5 points
        
        score += normalized_number_score + normalized_lucky_score
        
        # Check distribution
        low_count = len([n for n in numbers if n in self.number_groups['low']])
        mid_count = len([n for n in numbers if n in self.number_groups['mid']])
        high_count = len([n for n in numbers if n in self.number_groups['high']])
        
        # Bonus for balanced distribution
        distribution_match = 0
        if low_count == self.optimal_distribution['low']:
            distribution_match += 1
        if mid_count == self.optimal_distribution['mid']:
            distribution_match += 1
        if high_count == self.optimal_distribution['high']:
            distribution_match += 1
        
        score += distribution_match * 2.0  # Up to 6 points
        
        # Bonus for even/odd balance (ideally 2/3 or 3/2)
        even_count = len([n for n in numbers if n % 2 == 0])
        odd_count = 5 - even_count
        
        if (even_count == 2 and odd_count == 3) or (even_count == 3 and odd_count == 2):
            score += 2.0
        
        # Cap score at 100
        return min(score, 100)
    
    def generate_combinations(self, count=5, include_multiple_strategies=True):
        """
        Generate multiple combinations
        
        Args:
            count: Number of combinations to generate
            include_multiple_strategies: Whether to use multiple strategies
            
        Returns:
            list: List of combinations [(numbers, lucky, score, strategy), ...]
        """
        combinations = []
        
        # List of strategies to use
        strategies = ["balanced"]
        if include_multiple_strategies:
            strategies.extend(["consecutive", "even_odd", "sum_range", "coverage"])
        
        # Generate combinations using different strategies
        for i in range(count):
            # Choose strategy (cycling through available strategies)
            strategy_name = strategies[i % len(strategies)]
            
            # Generate using appropriate strategy
            if strategy_name == "balanced":
                # Vary risk level for diversity
                risk_level = 0.4 + (i * 0.1)
                numbers, lucky, score = self.generate_balanced_combination(risk_level=risk_level)
                strategy_desc = f"Balanced (Risk: {risk_level:.2f})"
            
            elif strategy_name == "consecutive":
                numbers, lucky, score = self.generate_pattern_combination("consecutive")
                strategy_desc = "Pattern (Consecutive)"
            
            elif strategy_name == "even_odd":
                numbers, lucky, score = self.generate_pattern_combination("even_odd")
                strategy_desc = "Pattern (Even-Odd)"
            
            elif strategy_name == "sum_range":
                numbers, lucky, score = self.generate_pattern_combination("sum_range")
                strategy_desc = "Pattern (Sum Range)"
            
            elif strategy_name == "coverage":
                # This needs existing combinations
                if combinations:
                    numbers, lucky, score = self.generate_coverage_combination(combinations)
                    strategy_desc = "Coverage Optimization"
                else:
                    numbers, lucky, score = self.generate_balanced_combination()
                    strategy_desc = "Balanced (Default)"
            
            else:
                # Default to balanced
                numbers, lucky, score = self.generate_balanced_combination()
                strategy_desc = "Balanced (Default)"
            
            # Add to results
            combinations.append((numbers, lucky, score, strategy_desc))
        
        return combinations
    
    def save_combinations_to_db(self, combinations, target_date=None):
        """
        Save combinations to database
        
        Args:
            combinations: List of combinations [(numbers, lucky, score, strategy), ...]
            target_date: Target draw date (None for next draw)
            
        Returns:
            list: List of saved combination IDs
        """
        saved_ids = []
        
        # Set default target date if not provided (next Monday or Wednesday)
        if target_date is None:
            today = date.today()
            days_to_monday = (0 - today.weekday()) % 7
            days_to_wednesday = (2 - today.weekday()) % 7
            
            if days_to_monday == 0:
                # If today is Monday, use next Wednesday
                target_date = today + timedelta(days=days_to_wednesday)
            elif days_to_wednesday == 0:
                # If today is Wednesday, use next Monday
                target_date = today + timedelta(days=days_to_monday + 7)
            else:
                # Use next closest draw day
                if days_to_monday < days_to_wednesday:
                    target_date = today + timedelta(days=days_to_monday)
                else:
                    target_date = today + timedelta(days=days_to_wednesday)
        
        # Convert date to string if needed
        if isinstance(target_date, date):
            target_date = target_date.strftime('%Y-%m-%d')
        
        # Save each combination
        for numbers, lucky, score, strategy in combinations:
            combination_id = self.save_generated_combination(
                numbers=numbers,
                lucky=lucky,
                strategy=strategy,
                score=score,
                target_draw_date=target_date
            )
            
            if combination_id:
                saved_ids.append(combination_id)
                logger.info(f"Saved combination {numbers} - {lucky} to database with ID {combination_id}")
        
        return saved_ids

def main():
    """Test the French Loto strategy"""
    print("Generating French Loto combinations...")
    
    # Initialize strategy
    strategy = FrenchLotoStrategy()
    
    # Generate combinations
    combinations = strategy.generate_combinations(count=10, include_multiple_strategies=True)
    
    # Display results
    print("\nGenerated French Loto Combinations:\n")
    
    for i, (numbers, lucky, score, strategy_name) in enumerate(combinations):
        print(f"Combination {i+1}:")
        print(f"  Strategy: {strategy_name}")
        print(f"  Main Numbers: {', '.join(map(str, numbers))}")
        print(f"  Lucky Number: {lucky}")
        print(f"  Score: {score:.2f}\n")
    
    # Ask if user wants to save to database
    save_choice = input("Save these combinations to database? (y/n): ")
    if save_choice.lower().startswith('y'):
        target_date = input("Enter target draw date (YYYY-MM-DD) or leave blank for next draw: ")
        target_date = target_date if target_date else None
        
        saved_ids = strategy.save_combinations_to_db(combinations, target_date)
        print(f"Saved {len(saved_ids)} combinations to database.")

if __name__ == "__main__":
    main()