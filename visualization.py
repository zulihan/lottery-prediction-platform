import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import math

class DataVisualization:
    """
    Class for creating visualizations of Euromillions data.
    """
    
    def __init__(self, data, statistics):
        """
        Initialize the visualization class with data and statistics.
        
        Parameters:
        -----------
        data : pandas.DataFrame
            The processed Euromillions data
        statistics : EuromillionsStatistics
            The statistics object with calculated metrics
        """
        self.data = data
        self.stats = statistics
    
    def plot_number_frequency(self, freq_data=None):
        """
        Plot the frequency of each number.
        
        Parameters:
        -----------
        freq_data : pandas.Series, optional
            Frequency data to plot. If None, uses the basic frequency.
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        if freq_data is None:
            freq_data = self.stats.get_frequency()
        
        # Convert to percentage
        freq_percent = freq_data * 100
        
        # Create figure
        fig = go.Figure(data=[
            go.Bar(
                x=list(freq_percent.index),
                y=list(freq_percent.values),
                marker_color='royalblue'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title='Main Number Frequency (%)',
            xaxis_title='Number',
            yaxis_title='Frequency (%)',
            xaxis=dict(
                tickmode='linear',
                tick0=1,
                dtick=1
            ),
            yaxis=dict(
                range=[0, max(freq_percent.values) * 1.1]
            )
        )
        
        return fig
    
    def plot_star_frequency(self, freq_data=None):
        """
        Plot the frequency of each star number.
        
        Parameters:
        -----------
        freq_data : pandas.Series, optional
            Frequency data to plot. If None, uses the basic frequency.
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        if freq_data is None:
            freq_data = self.stats.get_star_frequency()
        
        # Convert to percentage
        freq_percent = freq_data * 100
        
        # Create figure
        fig = go.Figure(data=[
            go.Bar(
                x=list(freq_percent.index),
                y=list(freq_percent.values),
                marker_color='gold'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title='Star Number Frequency (%)',
            xaxis_title='Star Number',
            yaxis_title='Frequency (%)',
            xaxis=dict(
                tickmode='linear',
                tick0=1,
                dtick=1
            ),
            yaxis=dict(
                range=[0, max(freq_percent.values) * 1.1]
            )
        )
        
        return fig
    
    def plot_number_pairs_heatmap(self, pairs_data=None):
        """
        Plot a heatmap of number pair frequencies.
        
        Parameters:
        -----------
        pairs_data : dict, optional
            Number pairs frequency data. If None, uses the calculated pairs.
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        if pairs_data is None:
            pairs_data = self.stats.get_number_pairs_frequency()
        
        # Create a matrix for heatmap
        matrix = np.zeros((50, 50))
        
        for (i, j), freq in pairs_data.items():
            matrix[i-1, j-1] = freq * 100  # Convert to percentage
            matrix[j-1, i-1] = freq * 100  # Mirror for symmetry
        
        # Create figure
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=list(range(1, 51)),
            y=list(range(1, 51)),
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Frequency (%)')
        ))
        
        # Update layout
        fig.update_layout(
            title='Number Pair Frequency',
            xaxis_title='Number',
            yaxis_title='Number',
            xaxis=dict(
                tickmode='linear',
                tick0=1,
                dtick=5
            ),
            yaxis=dict(
                autorange='reversed',  # To have (1,1) at the top left
                tickmode='linear',
                tick0=1,
                dtick=5
            )
        )
        
        return fig
    
    def plot_star_pairs_chart(self, star_pairs=None):
        """
        Plot a chart of star pair frequencies.
        
        Parameters:
        -----------
        star_pairs : dict, optional
            Star pairs frequency data. If None, uses the calculated pairs.
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        if star_pairs is None:
            star_pairs = self.stats.get_star_pairs_frequency()
        
        # Convert to a list of (pair, frequency) tuples
        pair_freq = [(f"{pair[0]}-{pair[1]}", freq * 100) for pair, freq in star_pairs.items()]
        
        # Sort by frequency
        pair_freq.sort(key=lambda x: x[1], reverse=True)
        
        # Create figure
        fig = go.Figure(data=[
            go.Bar(
                x=[p[0] for p in pair_freq],
                y=[p[1] for p in pair_freq],
                marker_color='gold'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title='Star Pair Frequency (%)',
            xaxis_title='Star Pair',
            yaxis_title='Frequency (%)',
            xaxis=dict(
                categoryorder='total descending'
            ),
            yaxis=dict(
                range=[0, max(p[1] for p in pair_freq) * 1.1]
            )
        )
        
        return fig
    
    def plot_number_time_series(self, number, time_series_data=None):
        """
        Plot time series data for a specific number.
        
        Parameters:
        -----------
        number : int
            The number to plot (1-50)
        time_series_data : pandas.DataFrame, optional
            Time series data. If None, generates it for the given number.
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        if time_series_data is None:
            time_series_data = self.stats.get_number_time_series(number)
        
        # Create figure with two y-axes
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add occurrence data
        fig.add_trace(
            go.Scatter(
                x=time_series_data['date'],
                y=time_series_data['occurrence'],
                mode='markers',
                name='Occurrence',
                marker=dict(
                    color='royalblue',
                    size=8
                )
            ),
            secondary_y=False,
        )
        
        # Add rolling average
        fig.add_trace(
            go.Scatter(
                x=time_series_data['date'],
                y=time_series_data['rolling_avg'],
                mode='lines',
                name='10-draw Rolling Average',
                line=dict(
                    color='red',
                    width=2
                )
            ),
            secondary_y=False,
        )
        
        # Add cumulative sum
        fig.add_trace(
            go.Scatter(
                x=time_series_data['date'],
                y=time_series_data['cumulative'],
                mode='lines',
                name='Cumulative Occurrences',
                line=dict(
                    color='green',
                    width=2,
                    dash='dash'
                )
            ),
            secondary_y=True,
        )
        
        # Update layout
        fig.update_layout(
            title=f'Time Series Analysis for Number {number}',
            xaxis_title='Date',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Update y-axes
        fig.update_yaxes(title_text="Occurrence / Rolling Average", secondary_y=False)
        fig.update_yaxes(title_text="Cumulative Occurrences", secondary_y=True)
        
        return fig
    
    def plot_day_of_week_distribution(self, number, dow_data):
        """
        Plot the distribution of a number by day of week.
        
        Parameters:
        -----------
        number : int
            The number to plot (1-50)
        dow_data : pandas.Series
            Day of week distribution data
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        # Create figure
        fig = go.Figure(data=[
            go.Bar(
                x=dow_data.index,
                y=dow_data.values,
                marker_color='royalblue'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title=f'Day of Week Distribution for Number {number} (%)',
            xaxis_title='Day of Week',
            yaxis_title='Occurrence Rate (%)',
            yaxis=dict(
                range=[0, max(dow_data.values) * 1.1]
            )
        )
        
        return fig
    
    def plot_even_odd_distribution(self, dist_data):
        """
        Plot the distribution of even/odd numbers.
        
        Parameters:
        -----------
        dist_data : dict
            Even/odd distribution data
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        # Create figure
        fig = go.Figure(data=[
            go.Bar(
                x=[f"{k} even, {5-k} odd" for k in sorted(dist_data.keys())],
                y=[dist_data[k] for k in sorted(dist_data.keys())],
                marker_color='royalblue'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title='Even/Odd Number Distribution (%)',
            xaxis_title='Pattern',
            yaxis_title='Percentage (%)',
            yaxis=dict(
                range=[0, max(dist_data.values()) * 1.1]
            )
        )
        
        return fig
    
    def plot_number_range_distribution(self, dist_data):
        """
        Plot the distribution of numbers across different ranges.
        
        Parameters:
        -----------
        dist_data : dict
            Number range distribution data
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        # Create figure
        fig = go.Figure(data=[
            go.Bar(
                x=list(dist_data.keys()),
                y=list(dist_data.values()),
                marker_color='royalblue'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title='Number Range Distribution (%)',
            xaxis_title='Range',
            yaxis_title='Percentage (%)',
            yaxis=dict(
                range=[0, max(dist_data.values()) * 1.1]
            )
        )
        
        return fig
    
    def plot_sum_distribution(self, dist_data):
        """
        Plot the distribution of the sum of winning numbers.
        
        Parameters:
        -----------
        dist_data : dict
            Sum distribution data
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        # Sort ranges by their lower bound
        sorted_ranges = sorted(dist_data.keys(), key=lambda x: int(x.split('-')[0]))
        
        # Create figure
        fig = go.Figure(data=[
            go.Bar(
                x=sorted_ranges,
                y=[dist_data[k] for k in sorted_ranges],
                marker_color='royalblue'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title='Sum Distribution (%)',
            xaxis_title='Sum Range',
            yaxis_title='Percentage (%)',
            yaxis=dict(
                range=[0, max(dist_data.values()) * 1.1]
            )
        )
        
        return fig
    
    def plot_number_heatmap(self):
        """
        Plot a heatmap of number frequencies.
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        # Get frequency data
        freq_data = self.stats.get_frequency()
        
        # Create a 5x10 matrix for the numbers 1-50
        matrix = np.zeros((5, 10))
        
        for num, freq in freq_data.items():
            row = (num - 1) // 10
            col = (num - 1) % 10
            matrix[row, col] = freq * 100  # Convert to percentage
        
        # Create figure
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=list(range(1, 11)),
            y=list(range(1, 6)),
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Frequency (%)')
        ))
        
        # Add number annotations
        annotations = []
        for i in range(5):
            for j in range(10):
                num = i * 10 + j + 1
                
                if num <= 50:  # Only for valid numbers 1-50
                    annotations.append(dict(
                        x=j+1,
                        y=i+1,
                        text=str(num),
                        showarrow=False,
                        font=dict(
                            color='white' if matrix[i, j] > 1.5 else 'black'  # Adjust threshold as needed
                        )
                    ))
        
        # Update layout
        fig.update_layout(
            title='Number Frequency Heatmap',
            xaxis_title='Column',
            yaxis_title='Row',
            annotations=annotations,
            xaxis=dict(
                tickmode='linear',
                tick0=1,
                dtick=1
            ),
            yaxis=dict(
                autorange='reversed',  # To have row 1 at the top
                tickmode='linear',
                tick0=1,
                dtick=1
            )
        )
        
        return fig
    
    def plot_frequency_evolution(self, numbers):
        """
        Plot the evolution of frequencies for selected numbers over time.
        
        Parameters:
        -----------
        numbers : list
            List of numbers to plot
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        # Create figure
        fig = go.Figure()
        
        # Define a color palette
        colors = px.colors.qualitative.Plotly
        
        # Get data for each number
        for i, number in enumerate(numbers):
            time_series = self.stats.get_number_time_series(number)
            
            # Calculate rolling frequency (10-draw window)
            rolling_freq = time_series['rolling_avg'] * 100  # Convert to percentage
            
            fig.add_trace(
                go.Scatter(
                    x=time_series['date'],
                    y=rolling_freq,
                    mode='lines',
                    name=f'Number {number}',
                    line=dict(
                        color=colors[i % len(colors)],
                        width=2
                    )
                )
            )
        
        # Update layout
        fig.update_layout(
            title='Number Frequency Evolution Over Time',
            xaxis_title='Date',
            yaxis_title='Rolling Frequency (%)',
            legend_title="Numbers"
        )
        
        return fig
    
    def plot_number_correlation(self):
        """
        Plot a correlation matrix for numbers.
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        # Create a matrix to track occurrences of each number
        num_draws = len(self.data)
        occurrences = np.zeros((51, num_draws))
        
        for draw_idx, (_, row) in enumerate(self.data.iterrows()):
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                num = row[col]
                occurrences[num, draw_idx] = 1
        
        # Calculate correlation matrix
        corr_matrix = np.zeros((50, 50))
        for i in range(1, 51):
            for j in range(1, 51):
                corr_matrix[i-1, j-1] = np.corrcoef(occurrences[i], occurrences[j])[0, 1]
        
        # Create figure
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=list(range(1, 51)),
            y=list(range(1, 51)),
            colorscale='RdBu',
            showscale=True,
            zmid=0,  # Center the color scale at 0
            colorbar=dict(title='Correlation')
        ))
        
        # Update layout
        fig.update_layout(
            title='Number Correlation Matrix',
            xaxis_title='Number',
            yaxis_title='Number',
            xaxis=dict(
                tickmode='linear',
                tick0=1,
                dtick=5
            ),
            yaxis=dict(
                autorange='reversed',
                tickmode='linear',
                tick0=1,
                dtick=5
            )
        )
        
        return fig
    
    def plot_winning_sum_distribution(self):
        """
        Plot the distribution of the sum of winning numbers.
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        # Calculate sums for all draws
        sums = []
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in ['n1', 'n2', 'n3', 'n4', 'n5']]
            sums.append(sum(numbers))
        
        # Create histogram
        fig = go.Figure(data=[
            go.Histogram(
                x=sums,
                nbinsx=20,
                marker_color='royalblue'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title='Distribution of Winning Number Sums',
            xaxis_title='Sum of 5 Main Numbers',
            yaxis_title='Frequency'
        )
        
        return fig
    
    def plot_number_distance_distribution(self):
        """
        Plot the distribution of distances between consecutive winning numbers.
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        # Calculate distances for all draws
        distances = []
        for _, row in self.data.iterrows():
            numbers = sorted([row[col] for col in ['n1', 'n2', 'n3', 'n4', 'n5']])
            for i in range(len(numbers) - 1):
                distances.append(numbers[i+1] - numbers[i])
        
        # Create histogram
        fig = go.Figure(data=[
            go.Histogram(
                x=distances,
                nbinsx=15,
                marker_color='royalblue'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title='Distribution of Distances Between Consecutive Numbers',
            xaxis_title='Distance',
            yaxis_title='Frequency'
        )
        
        return fig
    
    def plot_pattern_distribution(self):
        """
        Plot the distribution of different patterns in winning numbers.
        
        Returns:
        --------
        plotly.graph_objects.Figure
            The plotly figure
        """
        # Define patterns to look for
        patterns = {
            'Consecutive Pair': 0,
            'Consecutive Triplet': 0,
            'Two Consecutive Pairs': 0,
            'Even Distribution': 0,
            'Clustered': 0,
            'Other': 0
        }
        
        # Analyze all draws
        for _, row in self.data.iterrows():
            numbers = sorted([row[col] for col in ['n1', 'n2', 'n3', 'n4', 'n5']])
            
            # Check for consecutive numbers
            consecutive_count = 0
            consecutive_pairs = 0
            for i in range(len(numbers) - 1):
                if numbers[i+1] - numbers[i] == 1:
                    consecutive_count += 1
                    consecutive_pairs += 1 if consecutive_count == 1 else 0
                else:
                    consecutive_count = 0
            
            # Check distances between all numbers
            distances = [numbers[i+1] - numbers[i] for i in range(len(numbers) - 1)]
            avg_distance = sum(distances) / len(distances)
            std_distance = np.std(distances)
            
            # Classify pattern
            if consecutive_count >= 2:
                patterns['Consecutive Triplet'] += 1
            elif consecutive_pairs >= 2:
                patterns['Two Consecutive Pairs'] += 1
            elif consecutive_pairs == 1:
                patterns['Consecutive Pair'] += 1
            elif std_distance < 3:  # Threshold for even distribution
                patterns['Even Distribution'] += 1
            elif std_distance > 8:  # Threshold for clustering
                patterns['Clustered'] += 1
            else:
                patterns['Other'] += 1
        
        # Convert to percentages
        total = sum(patterns.values())
        percentages = {k: (v / total) * 100 for k, v in patterns.items()}
        
        # Create figure
        fig = go.Figure(data=[
            go.Bar(
                x=list(percentages.keys()),
                y=list(percentages.values()),
                marker_color='royalblue'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title='Distribution of Number Patterns (%)',
            xaxis_title='Pattern',
            yaxis_title='Percentage (%)',
            yaxis=dict(
                range=[0, max(percentages.values()) * 1.1]
            )
        )
        
        return fig
