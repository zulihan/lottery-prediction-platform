"""
Visualizations for French Loto data
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FrenchLotoVisualization:
    """
    Class for creating visualizations of French Loto data
    """
    
    def __init__(self, data, statistics):
        """
        Initialize with data and statistics
        
        Args:
            data: pandas DataFrame containing French Loto data
            statistics: FrenchLotoStatistics object
        """
        self.data = data
        self.statistics = statistics
        self.main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        self.lucky_col = 'lucky'
        
        # Check if we need to use alternative column names
        if 'n1' not in self.data.columns and 'number1' in self.data.columns:
            self.main_cols = ['number1', 'number2', 'number3', 'number4', 'number5']
            
        if 'lucky' not in self.data.columns and 'lucky_number' in self.data.columns:
            self.lucky_col = 'lucky_number'
    
    def plot_number_frequency(self):
        """
        Create a bar chart of number frequencies
        
        Returns:
            plotly.graph_objects.Figure
        """
        if not hasattr(self.statistics, 'main_number_freq'):
            self.statistics.analyze_frequencies()
            
        # Get frequency data
        main_freq = self.statistics.main_number_freq
        
        # Create dataframe for plotting
        freq_df = pd.DataFrame({
            'Number': list(main_freq.keys()),
            'Frequency': list(main_freq.values())
        })
        
        # Sort by number for this visualization
        freq_df = freq_df.sort_values('Number')
        
        # Create figure
        fig = px.bar(
            freq_df, 
            x='Number', 
            y='Frequency',
            title='French Loto Number Frequency (1-49)',
            labels={'Number': 'Number', 'Frequency': 'Times Drawn'},
            color='Frequency',
            color_continuous_scale='Viridis'
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title='Number',
            yaxis_title='Frequency',
            hovermode='closest',
            coloraxis_showscale=True,
            height=500,
            width=800
        )
        
        return fig
    
    def plot_lucky_number_frequency(self):
        """
        Create a bar chart of lucky number frequencies
        
        Returns:
            plotly.graph_objects.Figure
        """
        if not hasattr(self.statistics, 'lucky_number_freq'):
            self.statistics.analyze_frequencies()
            
        # Get frequency data
        lucky_freq = self.statistics.lucky_number_freq
        
        # Create dataframe for plotting
        freq_df = pd.DataFrame({
            'Lucky Number': list(lucky_freq.keys()),
            'Frequency': list(lucky_freq.values())
        })
        
        # Sort by number for this visualization
        freq_df = freq_df.sort_values('Lucky Number')
        
        # Create figure
        fig = px.bar(
            freq_df, 
            x='Lucky Number', 
            y='Frequency',
            title='French Loto Lucky Number Frequency (1-10)',
            labels={'Lucky Number': 'Lucky Number', 'Frequency': 'Times Drawn'},
            color='Frequency',
            color_continuous_scale='Inferno'
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title='Lucky Number',
            yaxis_title='Frequency',
            hovermode='closest',
            height=400,
            width=800
        )
        
        return fig
    
    def plot_hot_cold_numbers(self):
        """
        Create a visualization of hot and cold numbers
        
        Returns:
            plotly.graph_objects.Figure
        """
        hot_cold = self.statistics.hot_cold_numbers
        
        # Create a DataFrame with all numbers
        all_numbers = pd.DataFrame({'Number': range(1, 50)})
        
        # Label hot and cold numbers
        all_numbers['Status'] = 'Neutral'
        all_numbers.loc[all_numbers['Number'].isin(hot_cold['hot_numbers']), 'Status'] = 'Hot'
        all_numbers.loc[all_numbers['Number'].isin(hot_cold['cold_numbers']), 'Status'] = 'Cold'
        
        # Create color mapping
        color_map = {'Hot': 'red', 'Cold': 'blue', 'Neutral': 'gray'}
        
        # Create figure
        fig = px.scatter(
            all_numbers,
            x='Number',
            y=[1] * len(all_numbers),  # All points at same y level
            color='Status',
            color_discrete_map=color_map,
            title=f'Hot and Cold Numbers ({hot_cold["recent_period"]})',
            size_max=15,
            size=[10 if status == 'Neutral' else 15 for status in all_numbers['Status']],
            hover_data={'Number': True, 'Status': True}
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title='Number',
            yaxis_visible=False,
            yaxis_showticklabels=False,
            height=300,
            width=800,
            showlegend=True
        )
        
        # Update traces
        fig.update_traces(
            marker=dict(
                line=dict(width=1, color='DarkSlateGrey')
            )
        )
        
        return fig
    
    def plot_hot_cold_lucky(self):
        """
        Create a visualization of hot and cold lucky numbers
        
        Returns:
            plotly.graph_objects.Figure
        """
        hot_cold = self.statistics.hot_cold_numbers
        
        # Create a DataFrame with all lucky numbers
        all_numbers = pd.DataFrame({'Lucky Number': range(1, 11)})
        
        # Label hot and cold numbers
        all_numbers['Status'] = 'Neutral'
        all_numbers.loc[all_numbers['Lucky Number'].isin(hot_cold['hot_lucky']), 'Status'] = 'Hot'
        all_numbers.loc[all_numbers['Lucky Number'].isin(hot_cold['cold_lucky']), 'Status'] = 'Cold'
        
        # Create color mapping
        color_map = {'Hot': 'red', 'Cold': 'blue', 'Neutral': 'gray'}
        
        # Create figure
        fig = px.scatter(
            all_numbers,
            x='Lucky Number',
            y=[1] * len(all_numbers),  # All points at same y level
            color='Status',
            color_discrete_map=color_map,
            title=f'Hot and Cold Lucky Numbers ({hot_cold["recent_period"]})',
            size_max=15,
            size=[10 if status == 'Neutral' else 15 for status in all_numbers['Status']],
            hover_data={'Lucky Number': True, 'Status': True}
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title='Lucky Number',
            yaxis_visible=False,
            yaxis_showticklabels=False,
            height=300,
            width=800,
            showlegend=True
        )
        
        # Update traces
        fig.update_traces(
            marker=dict(
                line=dict(width=1, color='DarkSlateGrey')
            )
        )
        
        return fig
    
    def plot_monthly_trends(self):
        """
        Plot trends over time by month
        
        Returns:
            plotly.graph_objects.Figure
        """
        # Ensure date is datetime
        if self.data['date'].dtype != 'datetime64[ns]':
            self.data['date'] = pd.to_datetime(self.data['date'])
        
        # Create month and year columns
        self.data['year'] = self.data['date'].dt.year
        self.data['month'] = self.data['date'].dt.month
        
        # Group by year-month and count
        monthly_counts = self.data.groupby(['year', 'month']).size().reset_index(name='count')
        
        # Create date column for x-axis
        monthly_counts['date'] = pd.to_datetime(monthly_counts['year'].astype(str) + '-' + 
                                             monthly_counts['month'].astype(str) + '-01')
        
        # Sort by date
        monthly_counts = monthly_counts.sort_values('date')
        
        # Create figure
        fig = px.line(
            monthly_counts,
            x='date',
            y='count',
            title='French Loto Drawings per Month',
            labels={'count': 'Number of Drawings', 'date': 'Date'}
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Number of Drawings',
            height=400,
            width=800
        )
        
        return fig
    
    def plot_number_heatmap(self):
        """
        Create a heatmap showing which numbers appear together
        
        Returns:
            plotly.graph_objects.Figure
        """
        # Create an empty 49x49 matrix
        matrix = np.zeros((49, 49))
        
        # Count co-occurrences
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in self.main_cols]
            for i, num1 in enumerate(numbers):
                for j, num2 in enumerate(numbers):
                    if i != j:  # Avoid counting a number with itself
                        matrix[num1-1, num2-1] += 1
        
        # Create figure
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=list(range(1, 50)),
            y=list(range(1, 50)),
            colorscale='Viridis',
            showscale=True,
            hoverongaps=False
        ))
        
        # Customize layout
        fig.update_layout(
            title='Number Co-occurrence Heatmap',
            xaxis_title='Number',
            yaxis_title='Number',
            height=700,
            width=700
        )
        
        return fig
    
    def plot_pair_frequency(self):
        """
        Plot the frequency of number pairs
        
        Returns:
            plotly.graph_objects.Figure
        """
        # Get the top pairs
        top_pairs = self.statistics.pair_analysis
        
        # Create dataframe for plotting
        pair_df = pd.DataFrame({
            'Pair': [f"{pair[0]}-{pair[1]}" for pair in top_pairs.keys()],
            'Count': list(top_pairs.values())
        })
        
        # Sort by frequency
        pair_df = pair_df.sort_values('Count', ascending=False).head(15)
        
        # Create figure
        fig = px.bar(
            pair_df,
            x='Pair',
            y='Count',
            title='Most Frequent Number Pairs',
            labels={'Pair': 'Number Pair', 'Count': 'Times Appeared Together'},
            color='Count',
            color_continuous_scale='Viridis'
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title='Number Pair',
            yaxis_title='Frequency',
            height=500,
            width=800
        )
        
        return fig
    
    def plot_combination_dashboard(self, combinations):
        """
        Create a dashboard visualization for generated combinations
        
        Args:
            combinations: List of combination dictionaries
            
        Returns:
            plotly.graph_objects.Figure
        """
        # Create subplots
        fig = make_subplots(
            rows=len(combinations), 
            cols=1,
            subplot_titles=[f"Combination {i+1}: {combo['strategy']}" for i, combo in enumerate(combinations)],
            vertical_spacing=0.1
        )
        
        # Color map for strategies
        strategy_colors = {
            "Frequency-based": "blue",
            "Hot-Cold Balance": "purple",
            "Balanced Range": "green",
            "Pattern Analysis": "orange"
        }
        
        # Add combinations to the plot
        for i, combo in enumerate(combinations):
            main_nums = combo['main_numbers']
            lucky = combo['lucky_number']
            score = combo['score']
            strategy = combo['strategy']
            
            # Background color for each combination based on score
            score_color = f"rgba(255, {255 - int(score*2)}, 0, 0.1)"
            
            # Main numbers
            for num in main_nums:
                fig.add_trace(
                    go.Scatter(
                        x=[num],
                        y=[0],
                        mode='markers',
                        marker=dict(
                            symbol='circle',
                            size=30,
                            color=strategy_colors.get(strategy, 'blue'),
                            line=dict(color='black', width=1)
                        ),
                        text=f"{num}",
                        textposition="middle center",
                        name=f"Main {num}",
                        showlegend=False,
                        hoverinfo='text',
                        hovertext=f"Number: {num}"
                    ),
                    row=i+1, col=1
                )
            
            # Lucky number
            fig.add_trace(
                go.Scatter(
                    x=[lucky],
                    y=[0],
                    mode='markers',
                    marker=dict(
                        symbol='star',
                        size=35,
                        color='gold',
                        line=dict(color='black', width=1)
                    ),
                    text=f"{lucky}",
                    textposition="middle center",
                    name=f"Lucky {lucky}",
                    showlegend=False,
                    hoverinfo='text',
                    hovertext=f"Lucky Number: {lucky}"
                ),
                row=i+1, col=1
            )
            
            # Score text
            fig.add_annotation(
                x=35,
                y=0,
                text=f"Score: {score}/100",
                showarrow=False,
                font=dict(size=14, color="black"),
                row=i+1, col=1
            )
            
            # Add a background for each combination
            fig.add_shape(
                type="rect",
                x0=0,
                y0=-0.5,
                x1=50,
                y1=0.5,
                fillcolor=score_color,
                line=dict(width=0),
                row=i+1, col=1
            )
            
            # Update axes for each subplot
            fig.update_xaxes(
                title="Numbers",
                range=[0, 50],
                row=i+1, col=1
            )
            fig.update_yaxes(
                visible=False,
                range=[-0.5, 0.5],
                row=i+1, col=1
            )
        
        # Customize overall layout
        fig.update_layout(
            title="French Loto Optimized Combinations",
            height=200 * len(combinations),
            width=800,
            showlegend=False,
            margin=dict(t=50, l=50, r=50, b=50),
        )
        
        return fig