import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class FrenchLotoVisualization:
    """
    Class for creating visualizations of French Loto data.
    """
    
    def __init__(self, data, statistics):
        """
        Initialize with data and statistics.
        
        Args:
            data: DataFrame with French Loto data
            statistics: FrenchLotoStatistics object
        """
        self.data = data
        self.statistics = statistics
    
    def plot_number_frequency(self, weighted_freq=None):
        """
        Plot frequency of main numbers.
        
        Args:
            weighted_freq: Optional weighted frequency Series
            
        Returns:
            Plotly figure
        """
        if weighted_freq is None:
            weighted_freq = self.statistics.number_frequency
        
        # Create a DataFrame for plotting
        df = pd.DataFrame({
            'Number': weighted_freq.index,
            'Frequency': weighted_freq.values
        })
        
        # Create the figure with Plotly
        fig = px.bar(
            df,
            x='Number',
            y='Frequency',
            title='French Loto Number Frequency',
            color='Frequency',
            color_continuous_scale='Viridis'
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title='Number (1-49)',
            yaxis_title='Frequency',
            xaxis=dict(tickmode='linear', dtick=5),
            yaxis=dict(tickformat='.3f'),
            height=500
        )
        
        return fig
    
    def plot_lucky_frequency(self, weighted_freq=None):
        """
        Plot frequency of lucky numbers.
        
        Args:
            weighted_freq: Optional weighted frequency Series
            
        Returns:
            Plotly figure
        """
        if weighted_freq is None:
            weighted_freq = self.statistics.lucky_frequency
        
        # Create a DataFrame for plotting
        df = pd.DataFrame({
            'Lucky Number': weighted_freq.index,
            'Frequency': weighted_freq.values
        })
        
        # Create the figure with Plotly
        fig = px.bar(
            df,
            x='Lucky Number',
            y='Frequency',
            title='French Loto Lucky Number Frequency',
            color='Frequency',
            color_continuous_scale='Reds'
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title='Lucky Number (1-10)',
            yaxis_title='Frequency',
            xaxis=dict(tickmode='linear', dtick=1),
            yaxis=dict(tickformat='.3f'),
            height=400
        )
        
        return fig
    
    def plot_number_heatmap(self, recent_draws=100):
        """
        Create a heatmap of number occurrences in recent draws.
        
        Args:
            recent_draws: Number of recent draws to include
            
        Returns:
            Plotly figure
        """
        if self.data.empty:
            # Return empty figure if no data
            return go.Figure()
        
        # Get recent draws
        recent_data = self.data.sort_values('date', ascending=False).head(recent_draws)
        
        # Create a matrix for the heatmap
        matrix = np.zeros((10, 5))  # 10 rows, 5 columns for numbers
        
        # Fill the matrix with occurrence counts
        for _, row in recent_data.iterrows():
            for i, col in enumerate(['n1', 'n2', 'n3', 'n4', 'n5']):
                num = row[col]
                # Map number to position in matrix (1-49 -> 0-9 × 0-4)
                r = (num - 1) // 5
                c = i
                if r < 10:  # Ensure we're within matrix bounds
                    matrix[r, c] += 1
        
        # Create x and y labels
        y_labels = [f"{i*5+1}-{i*5+5}" for i in range(10)]
        x_labels = ["First", "Second", "Third", "Fourth", "Fifth"]
        
        # Create the heatmap
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=x_labels,
            y=y_labels,
            colorscale='Viridis',
            zmin=0,
            zmax=matrix.max(),
            hoverongaps=False,
            showscale=True,
            colorbar=dict(title='Occurrences')
        ))
        
        # Update layout
        fig.update_layout(
            title=f'Number Occurrence Heatmap (Last {recent_draws} Draws)',
            xaxis_title='Position in Draw',
            yaxis_title='Number Range',
            height=600
        )
        
        return fig
    
    def plot_even_odd_distribution(self):
        """
        Plot distribution of even/odd numbers.
        
        Returns:
            Plotly figure
        """
        if not hasattr(self.statistics, 'even_odd_distribution') or not self.statistics.even_odd_distribution:
            # Return empty figure if no data
            return go.Figure()
        
        # Create a DataFrame for plotting
        df = pd.DataFrame({
            'Even Count': list(self.statistics.even_odd_distribution.keys()),
            'Percentage': [v * 100 for v in self.statistics.even_odd_distribution.values()]
        })
        
        # Create the figure with Plotly
        fig = px.bar(
            df,
            x='Even Count',
            y='Percentage',
            title='Distribution of Even Numbers in French Loto Draws',
            color='Percentage',
            color_continuous_scale='Blues'
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title='Number of Even Numbers in Draw',
            yaxis_title='Percentage of Draws',
            xaxis=dict(tickmode='linear', dtick=1),
            yaxis=dict(tickformat='.1f', suffix='%'),
            height=400
        )
        
        return fig
    
    def plot_sum_distribution(self):
        """
        Plot distribution of sum of numbers.
        
        Returns:
            Plotly figure
        """
        if not hasattr(self.statistics, 'sum_distribution') or not self.statistics.sum_distribution:
            # Return empty figure if no data
            return go.Figure()
        
        # Create a DataFrame for plotting
        df = pd.DataFrame({
            'Sum Range': list(self.statistics.sum_distribution.keys()),
            'Percentage': [v * 100 for v in self.statistics.sum_distribution.values()]
        })
        
        # Create the figure with Plotly
        fig = px.bar(
            df,
            x='Sum Range',
            y='Percentage',
            title='Distribution of Sum of Numbers in French Loto Draws',
            color='Percentage',
            color_continuous_scale='Greens'
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title='Sum Range',
            yaxis_title='Percentage of Draws',
            yaxis=dict(tickformat='.1f', suffix='%'),
            height=400
        )
        
        return fig
    
    def plot_range_distribution(self):
        """
        Plot distribution of range between min and max number.
        
        Returns:
            Plotly figure
        """
        if not hasattr(self.statistics, 'range_distribution') or not self.statistics.range_distribution:
            # Return empty figure if no data
            return go.Figure()
        
        # Create a DataFrame for plotting
        df = pd.DataFrame({
            'Range': list(self.statistics.range_distribution.keys()),
            'Percentage': [v * 100 for v in self.statistics.range_distribution.values()]
        })
        
        # Create the figure with Plotly
        fig = px.bar(
            df,
            x='Range',
            y='Percentage',
            title='Distribution of Range between Min and Max Number',
            color='Percentage',
            color_continuous_scale='Purples'
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title='Range',
            yaxis_title='Percentage of Draws',
            yaxis=dict(tickformat='.1f', suffix='%'),
            height=400
        )
        
        return fig
    
    def plot_draws_by_day(self):
        """
        Plot number of draws by day of the week.
        
        Returns:
            Plotly figure
        """
        if self.data.empty or 'day_of_week' not in self.data.columns:
            # Return empty figure if no data
            return go.Figure()
        
        # Create a DataFrame for plotting
        day_counts = self.data['day_of_week'].value_counts()
        
        # Define order of days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Reindex to ensure all days are included and in correct order
        day_counts = day_counts.reindex(day_order, fill_value=0)
        
        # Create the figure with Plotly
        fig = px.bar(
            x=day_counts.index,
            y=day_counts.values,
            title='Number of French Loto Draws by Day of Week',
            color=day_counts.values,
            color_continuous_scale='Oranges'
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title='Day of Week',
            yaxis_title='Number of Draws',
            height=400
        )
        
        return fig
    
    def plot_timeline(self, metric='winning_numbers'):
        """
        Plot timeline of draws with selected metric.
        
        Args:
            metric: What to visualize ('winning_numbers' or 'lucky_numbers')
            
        Returns:
            Plotly figure
        """
        if self.data.empty:
            # Return empty figure if no data
            return go.Figure()
        
        # Sort data by date
        sorted_data = self.data.sort_values('date')
        
        if metric == 'winning_numbers':
            # Create a figure with 5 scatter traces, one for each number
            fig = go.Figure()
            
            for i, col in enumerate(['n1', 'n2', 'n3', 'n4', 'n5']):
                fig.add_trace(go.Scatter(
                    x=sorted_data['date'],
                    y=sorted_data[col],
                    mode='markers',
                    name=f'Number {i+1}',
                    marker=dict(size=8)
                ))
            
            title = 'Timeline of Winning Numbers'
            y_title = 'Number (1-49)'
            
        else:  # lucky_numbers
            # Create a figure with 1 scatter trace for lucky numbers
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=sorted_data['date'],
                y=sorted_data['lucky'],
                mode='markers',
                name='Lucky Number',
                marker=dict(size=8, color='red')
            ))
            
            title = 'Timeline of Lucky Numbers'
            y_title = 'Lucky Number (1-10)'
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title=y_title,
            height=500,
            showlegend=True
        )
        
        return fig