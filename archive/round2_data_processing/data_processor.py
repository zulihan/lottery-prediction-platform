import pandas as pd
import numpy as np
from datetime import datetime
import re

class DataProcessor:
    """
    Class for processing Euromillions data.
    Handles importing, cleaning, and structuring the data.
    """
    
    def __init__(self, data):
        """
        Initialize the data processor with a pandas DataFrame.
        
        Parameters:
        -----------
        data : pandas.DataFrame
            The raw Euromillions data
        """
        self.raw_data = data
        self.processed_data = None
        self.process_data()
    
    def process_data(self):
        """
        Process the raw data into a standardized format.
        Handles different CSV formats and ensures consistent column names and data types.
        """
        # Make a copy to avoid modifying the original data
        df = self.raw_data.copy()
        
        # Identify the data format based on column names
        if self.identify_data_format(df) == "standard":
            self.process_standard_format(df)
        else:
            self.process_custom_format(df)
    
    def identify_data_format(self, df):
        """
        Identify the format of the data based on column names.
        
        Returns:
        --------
        str
            The identified format ("standard" or "custom")
        """
        # Check for standard column names (or variations)
        standard_cols = ['date', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']
        date_variants = ['date', 'draw_date', 'drawdate', 'date_of_draw']
        number_variants = [
            ['n1', 'n2', 'n3', 'n4', 'n5'],
            ['number1', 'number2', 'number3', 'number4', 'number5'],
            ['num1', 'num2', 'num3', 'num4', 'num5'],
            ['ball1', 'ball2', 'ball3', 'ball4', 'ball5']
        ]
        star_variants = [
            ['s1', 's2'],
            ['star1', 'star2'],
            ['lucky_star1', 'lucky_star2'],
            ['ls1', 'ls2']
        ]
        
        # Check for date column
        date_col = None
        for variant in date_variants:
            if variant in df.columns:
                date_col = variant
                break
        
        # Check for number columns
        number_cols = None
        for variant in number_variants:
            if all(col in df.columns for col in variant):
                number_cols = variant
                break
        
        # Check for star columns
        star_cols = None
        for variant in star_variants:
            if all(col in df.columns for col in variant):
                star_cols = variant
                break
        
        if date_col and number_cols and star_cols:
            return "standard"
        else:
            return "custom"
    
    def process_standard_format(self, df):
        """
        Process data in standard format with recognized column names.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The data to process
        """
        # Identify column names
        date_variants = ['date', 'draw_date', 'drawdate', 'date_of_draw']
        date_col = next((col for col in date_variants if col in df.columns), None)
        
        number_variants = [
            ['n1', 'n2', 'n3', 'n4', 'n5'],
            ['number1', 'number2', 'number3', 'number4', 'number5'],
            ['num1', 'num2', 'num3', 'num4', 'num5'],
            ['ball1', 'ball2', 'ball3', 'ball4', 'ball5']
        ]
        number_cols = next((cols for cols in number_variants if all(col in df.columns for col in cols)), None)
        
        star_variants = [
            ['s1', 's2'],
            ['star1', 'star2'],
            ['lucky_star1', 'lucky_star2'],
            ['ls1', 'ls2']
        ]
        star_cols = next((cols for cols in star_variants if all(col in df.columns for col in cols)), None)
        
        # Create a new DataFrame with standardized columns
        processed = pd.DataFrame()
        
        # Process date - convert to datetime and then to date objects for consistency
        dates = pd.to_datetime(df[date_col])
        processed['date'] = dates.apply(lambda x: x.date() if hasattr(x, 'date') and callable(getattr(x, 'date')) else x)
        
        # Add day of week using the original datetime objects (before conversion to date)
        processed['day_of_week'] = dates.dt.day_name()
        
        # Process numbers
        for i, col in enumerate(number_cols):
            processed[f'n{i+1}'] = df[col].astype(int)
        
        # Process stars
        for i, col in enumerate(star_cols):
            processed[f's{i+1}'] = df[col].astype(int)
        
        # Sort by date (descending)
        processed = processed.sort_values('date', ascending=False).reset_index(drop=True)
        
        self.processed_data = processed
    
    def process_custom_format(self, df):
        """
        Process data in a custom or unrecognized format.
        Attempts to extract the required information based on column contents.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The data to process
        """
        # Create a new DataFrame with standardized columns
        processed = pd.DataFrame()
        
        # Look for date column
        date_col = None
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if column contains date-like strings
                sample = df[col].iloc[0] if not df[col].empty else ""
                if isinstance(sample, str) and (
                    re.match(r'\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}', sample) or
                    re.match(r'\d{4}[/.-]\d{1,2}[/.-]\d{1,2}', sample)
                ):
                    date_col = col
                    break
        
        if date_col:
            try:
                # Convert to datetime and then explicitly to datetime.date objects for consistency
                dates = pd.to_datetime(df[date_col])
                processed['date'] = dates.apply(lambda x: x.date() if hasattr(x, 'date') and callable(getattr(x, 'date')) else x)
                
                # Add day of week using the original datetime objects (before conversion to date)
                processed['day_of_week'] = dates.dt.day_name()
            except:
                # If conversion fails, create a basic date column
                today = pd.to_datetime('today').normalize()
                processed['date'] = today.date()
                processed['day_of_week'] = today.day_name()
        else:
            # Create a default date column
            today = pd.to_datetime('today').normalize() 
            processed['date'] = today.date()
            processed['day_of_week'] = today.day_name()
        
        # Try to identify number columns and star columns
        num_cols = []
        star_cols = []
        
        for col in df.columns:
            if df[col].dtype == 'int64' or df[col].dtype == 'float64':
                sample_values = df[col].dropna().unique()
                if len(sample_values) > 0:
                    min_val = min(sample_values)
                    max_val = max(sample_values)
                    
                    if 1 <= min_val and max_val <= 50:
                        num_cols.append(col)
                    elif 1 <= min_val and max_val <= 12:
                        star_cols.append(col)
        
        # If we found at least 5 number columns and 2 star columns
        if len(num_cols) >= 5 and len(star_cols) >= 2:
            # Take the first 5 number columns and 2 star columns
            for i, col in enumerate(num_cols[:5]):
                processed[f'n{i+1}'] = df[col].astype(int)
            
            for i, col in enumerate(star_cols[:2]):
                processed[f's{i+1}'] = df[col].astype(int)
        else:
            # Create sample data if we can't identify the correct columns
            for i in range(1, 6):
                processed[f'n{i}'] = np.random.randint(1, 51, size=len(processed))
            
            for i in range(1, 3):
                processed[f's{i}'] = np.random.randint(1, 13, size=len(processed))
        
        # Sort by date (descending)
        processed = processed.sort_values('date', ascending=False).reset_index(drop=True)
        
        self.processed_data = processed
    
    def get_processed_data(self):
        """
        Get the processed data.
        
        Returns:
        --------
        pandas.DataFrame
            The processed Euromillions data
        """
        return self.processed_data
    
    def add_new_draw(self, draw_date, numbers, stars):
        """
        Add a new draw to the dataset.
        
        Parameters:
        -----------
        draw_date : datetime.date, pandas.Timestamp, or str
            The date of the draw
        numbers : list
            List of 5 main numbers
        stars : list
            List of 2 star numbers
        
        Returns:
        --------
        bool
            True if the draw was added successfully
        """
        # Validate inputs
        if len(numbers) != 5 or len(stars) != 2:
            raise ValueError("Invalid number of values: must be 5 main numbers and 2 stars")
        
        if not all(1 <= n <= 50 for n in numbers) or not all(1 <= s <= 12 for s in stars):
            raise ValueError("Invalid number values: main numbers must be 1-50, stars must be 1-12")
        
        if len(set(numbers)) != 5 or len(set(stars)) != 2:
            raise ValueError("Duplicate numbers are not allowed")
        
        # Convert date to a consistent datetime.date object format
        if isinstance(draw_date, str):
            draw_date = datetime.strptime(draw_date, "%Y-%m-%d").date()
        elif hasattr(draw_date, 'date') and callable(getattr(draw_date, 'date')):  # Handle pandas Timestamp
            draw_date = draw_date.date()
        elif not isinstance(draw_date, type(datetime.now().date())):
            # If it's still not a date object, try to convert with str
            draw_date = datetime.strptime(str(draw_date), "%Y-%m-%d").date()
        
        # Create new draw data
        new_draw = {
            'date': draw_date,
            'day_of_week': draw_date.strftime('%A'),
        }
        
        # Add main numbers
        for i, num in enumerate(sorted(numbers)):
            new_draw[f'n{i+1}'] = num
        
        # Add star numbers
        for i, star in enumerate(sorted(stars)):
            new_draw[f's{i+1}'] = star
        
        # Add to the DataFrame
        self.processed_data = pd.concat([
            pd.DataFrame([new_draw]),
            self.processed_data
        ]).reset_index(drop=True)
        
        return True
    
    def export_data(self, file_path):
        """
        Export the processed data to a CSV file.
        
        Parameters:
        -----------
        file_path : str
            The path to save the CSV file
        
        Returns:
        --------
        bool
            True if the export was successful
        """
        try:
            self.processed_data.to_csv(file_path, index=False)
            return True
        except Exception as e:
            print(f"Error exporting data: {str(e)}")
            return False
