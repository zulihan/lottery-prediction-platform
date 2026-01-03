"""
Plotly Visualizations for Lottery Analysis

Interactive visualizations using Plotly for better data exploration:
- Number pairs heatmap
- Frequency charts
- Trend analysis
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from collections import Counter
import logging

logger = logging.getLogger(__name__)


def plot_number_pairs_heatmap(pairs_data=None, historical_data=None, max_number=50):
    """
    Create interactive heatmap showing frequency of number pairs.

    Args:
        pairs_data: dict of {(num1, num2): frequency} (optional)
        historical_data: List of draws with 'numbers' key (used if pairs_data not provided)
        max_number: Maximum number in range (default 50 for Euromillions)

    Returns:
        Plotly figure object
    """
    if pairs_data is None and historical_data is None:
        raise ValueError("Either pairs_data or historical_data must be provided")

    # Build pairs data from historical data if not provided
    if pairs_data is None:
        pairs_counter = Counter()
        for draw in historical_data:
            numbers = sorted(draw['numbers'])
            # Count all pairs in this draw
            for i in range(len(numbers)):
                for j in range(i+1, len(numbers)):
                    pair = (numbers[i], numbers[j])
                    pairs_counter[pair] += 1
        pairs_data = dict(pairs_counter)

    # Create matrix
    matrix = np.zeros((max_number, max_number))

    # Total draws for percentage calculation
    total_pairs = sum(pairs_data.values())

    for (i, j), freq in pairs_data.items():
        if 1 <= i <= max_number and 1 <= j <= max_number:
            # Convert frequency to percentage
            percentage = (freq / total_pairs * 100) if total_pairs > 0 else 0
            matrix[i-1, j-1] = percentage
            matrix[j-1, i-1] = percentage  # Mirror for symmetry

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=list(range(1, max_number+1)),
        y=list(range(1, max_number+1)),
        colorscale='YlOrRd',
        hoverongaps=False,
        hovertemplate='Numbers: %{y} & %{x}<br>Frequency: %{z:.2f}%<extra></extra>',
        colorbar=dict(title="Frequency %")
    ))

    fig.update_layout(
        title='Number Pair Frequency Heatmap',
        xaxis_title='Number',
        yaxis_title='Number',
        width=800,
        height=800,
        xaxis=dict(dtick=5),
        yaxis=dict(dtick=5)
    )

    return fig


def plot_number_frequency_chart(number_frequency, top_n=20, chart_type='bar'):
    """
    Create interactive frequency chart for numbers.

    Args:
        number_frequency: dict of {number: frequency}
        top_n: Show top N most frequent numbers
        chart_type: 'bar' or 'line'

    Returns:
        Plotly figure object
    """
    # Sort by frequency and get top N
    sorted_freq = sorted(number_frequency.items(), key=lambda x: x[1], reverse=True)[:top_n]
    numbers, frequencies = zip(*sorted_freq)

    if chart_type == 'bar':
        fig = go.Figure(data=[
            go.Bar(
                x=list(numbers),
                y=list(frequencies),
                marker_color='indianred',
                hovertemplate='Number: %{x}<br>Frequency: %{y}<extra></extra>'
            )
        ])
    else:  # line
        fig = go.Figure(data=[
            go.Scatter(
                x=list(numbers),
                y=list(frequencies),
                mode='lines+markers',
                line=dict(color='indianred', width=2),
                marker=dict(size=8),
                hovertemplate='Number: %{x}<br>Frequency: %{y}<extra></extra>'
            )
        ])

    fig.update_layout(
        title=f'Top {top_n} Most Frequent Numbers',
        xaxis_title='Number',
        yaxis_title='Frequency',
        width=900,
        height=500,
        hovermode='x unified'
    )

    return fig


def plot_hot_cold_numbers(hot_numbers, cold_numbers, max_display=10):
    """
    Create visualization comparing hot vs cold numbers.

    Args:
        hot_numbers: List of (number, frequency) tuples for hot numbers
        cold_numbers: List of (number, frequency) tuples for cold numbers
        max_display: Maximum numbers to display in each category

    Returns:
        Plotly figure object
    """
    # Prepare data
    hot_nums, hot_freqs = zip(*hot_numbers[:max_display])
    cold_nums, cold_freqs = zip(*cold_numbers[:max_display])

    fig = go.Figure()

    # Hot numbers
    fig.add_trace(go.Bar(
        name='Hot Numbers',
        x=list(hot_nums),
        y=list(hot_freqs),
        marker_color='crimson',
        hovertemplate='Number: %{x}<br>Frequency: %{y}<extra></extra>'
    ))

    # Cold numbers
    fig.add_trace(go.Bar(
        name='Cold Numbers',
        x=list(cold_nums),
        y=list(cold_freqs),
        marker_color='steelblue',
        hovertemplate='Number: %{x}<br>Frequency: %{y}<extra></extra>'
    ))

    fig.update_layout(
        title='Hot vs Cold Numbers',
        xaxis_title='Number',
        yaxis_title='Frequency',
        barmode='group',
        width=900,
        height=500,
        hovermode='x unified',
        legend=dict(x=0.7, y=1)
    )

    return fig


def plot_range_distribution(range_distribution):
    """
    Create pie chart showing number range distribution.

    Args:
        range_distribution: dict of {range_label: count}

    Returns:
        Plotly figure object
    """
    labels = list(range_distribution.keys())
    values = list(range_distribution.values())

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        hovertemplate='Range: %{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])

    fig.update_layout(
        title='Number Range Distribution',
        width=700,
        height=500
    )

    return fig


def plot_star_frequency(star_frequency):
    """
    Create bar chart for star number frequencies.

    Args:
        star_frequency: dict of {star: frequency}

    Returns:
        Plotly figure object
    """
    stars = sorted(star_frequency.keys())
    frequencies = [star_frequency[s] for s in stars]

    fig = go.Figure(data=[
        go.Bar(
            x=stars,
            y=frequencies,
            marker_color='gold',
            hovertemplate='Star: %{x}<br>Frequency: %{y}<extra></extra>'
        )
    ])

    fig.update_layout(
        title='Star Number Frequency Distribution',
        xaxis_title='Star Number',
        yaxis_title='Frequency',
        width=700,
        height=500,
        xaxis=dict(dtick=1)
    )

    return fig


def plot_trend_over_time(historical_data, number=None):
    """
    Plot frequency trend of a specific number or all numbers over time.

    Args:
        historical_data: List of draws with 'date' and 'numbers' keys
        number: Specific number to track (optional, if None shows top 5)

    Returns:
        Plotly figure object
    """
    # Sort by date
    sorted_data = sorted(historical_data, key=lambda x: x['date'])

    if number is not None:
        # Track specific number
        dates = []
        running_count = 0
        counts = []

        for draw in sorted_data:
            dates.append(draw['date'])
            if number in draw['numbers']:
                running_count += 1
            counts.append(running_count)

        fig = go.Figure(data=[
            go.Scatter(
                x=dates,
                y=counts,
                mode='lines+markers',
                name=f'Number {number}',
                line=dict(width=2),
                hovertemplate='Date: %{x}<br>Cumulative: %{y}<extra></extra>'
            )
        ])

        fig.update_layout(
            title=f'Number {number} Frequency Over Time',
            xaxis_title='Date',
            yaxis_title='Cumulative Frequency'
        )
    else:
        # Track top 5 most frequent numbers
        all_numbers = []
        for draw in sorted_data:
            all_numbers.extend(draw['numbers'])
        number_freq = Counter(all_numbers)
        top_5 = [num for num, _ in number_freq.most_common(5)]

        fig = go.Figure()

        for num in top_5:
            dates = []
            running_count = 0
            counts = []

            for draw in sorted_data:
                dates.append(draw['date'])
                if num in draw['numbers']:
                    running_count += 1
                counts.append(running_count)

            fig.add_trace(go.Scatter(
                x=dates,
                y=counts,
                mode='lines',
                name=f'Number {num}',
                line=dict(width=2),
                hovertemplate='Date: %{x}<br>Cumulative: %{y}<extra></extra>'
            ))

        fig.update_layout(
            title='Top 5 Numbers Frequency Trends',
            xaxis_title='Date',
            yaxis_title='Cumulative Frequency',
            hovermode='x unified'
        )

    fig.update_layout(
        width=1000,
        height=500
    )

    return fig


# Helper function to create all visualizations at once
def create_all_visualizations(historical_data, statistics):
    """
    Create a comprehensive set of visualizations.

    Args:
        historical_data: List of historical draws
        statistics: Statistics object with frequency data

    Returns:
        dict: Dictionary of figure objects
    """
    figures = {}

    try:
        # Number pairs heatmap
        figures['pairs_heatmap'] = plot_number_pairs_heatmap(historical_data=historical_data)
    except Exception as e:
        logger.error(f"Error creating pairs heatmap: {e}")

    try:
        # Number frequency
        number_freq = statistics.get_frequency()
        figures['number_frequency'] = plot_number_frequency_chart(number_freq)
    except Exception as e:
        logger.error(f"Error creating frequency chart: {e}")

    try:
        # Hot vs Cold
        hot_numbers = statistics.get_hot_numbers(10)
        cold_numbers = statistics.get_cold_numbers(10)
        hot_freq = [(n, statistics.get_frequency(n)) for n in hot_numbers]
        cold_freq = [(n, statistics.get_frequency(n)) for n in cold_numbers]
        figures['hot_cold'] = plot_hot_cold_numbers(hot_freq, cold_freq)
    except Exception as e:
        logger.error(f"Error creating hot/cold chart: {e}")

    try:
        # Range distribution
        range_dist = statistics.get_number_range_distribution()
        figures['range_distribution'] = plot_range_distribution(range_dist)
    except Exception as e:
        logger.error(f"Error creating range distribution: {e}")

    try:
        # Star frequency
        star_freq = statistics.get_star_frequency()
        figures['star_frequency'] = plot_star_frequency(star_freq)
    except Exception as e:
        logger.error(f"Error creating star frequency: {e}")

    try:
        # Trends over time
        figures['trends'] = plot_trend_over_time(historical_data)
    except Exception as e:
        logger.error(f"Error creating trends: {e}")

    return figures
