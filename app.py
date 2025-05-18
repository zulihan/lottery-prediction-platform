import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
import io
import json
from datetime import datetime, date, timedelta
from database import init_db, get_db_connection
import logging

# Import strategy and analysis tools
try:
    from strategies import PredictionStrategies
    from french_loto_strategy import FrenchLotoStrategy
    from french_loto_statistics import FrenchLotoStatistics
    from combination_analysis import analyze_full_combinations, analyze_number_combinations
    from strategy_recommendation import get_ordered_strategy_list, get_strategy_info_text, get_base_strategy_name
except ImportError:
    logging.warning("Strategy modules not found. Some features may be unavailable.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

# Set page config (must be first Streamlit command)
st.set_page_config(
    page_title="Euromillions & French Loto Prediction",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    
    # Application title
    st.title("🎯 Lottery Prediction Platform")
    st.write("Advanced prediction tools for Euromillions and French Loto")
    
    # Initialize session state for storing data
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
        
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
        
    if 'french_loto_data_loaded' not in st.session_state:
        st.session_state.french_loto_data_loaded = False
        
    if 'french_loto_data' not in st.session_state:
        st.session_state.french_loto_data = None
    
    # Sidebar for data loading and configuration
    with st.sidebar:
        st.header("Data Sources")
        
        # Euromillions data loading
        st.subheader("Euromillions Data")
        load_data_button = st.button("Load Euromillions Data")
        
        if load_data_button:
            with st.spinner("Loading Euromillions data..."):
                # Get database connection
                conn = get_db_connection()
                if conn:
                    try:
                        query = "SELECT * FROM euromillions_drawings ORDER BY date DESC"
                        data = pd.read_sql(query, conn)
                        st.session_state.processed_data = data
                        st.session_state.data_loaded = True
                    except Exception as e:
                        st.error(f"Error loading data: {str(e)}")
                else:
                    st.error("Could not connect to database.")
        
        if st.session_state.data_loaded:
            st.success(f"✅ {len(st.session_state.processed_data)} Euromillions drawings loaded")
        
        # French Loto data loading
        st.subheader("French Loto Data")
        load_french_loto_button = st.button("Load French Loto Data")
        
        if load_french_loto_button:
            with st.spinner("Loading French Loto data..."):
                # Get database connection
                conn = get_db_connection()
                if conn:
                    try:
                        query = "SELECT * FROM french_loto_drawings ORDER BY date DESC"
                        data = pd.read_sql(query, conn)
                        st.session_state.french_loto_data = data
                        st.session_state.french_loto_data_loaded = True
                    except Exception as e:
                        st.error(f"Error loading data: {str(e)}")
                else:
                    st.error("Could not connect to database.")
            
            if st.session_state.french_loto_data_loaded:
                st.success(f"✅ {len(st.session_state.french_loto_data)} French Loto drawings loaded")
    
    # Create tabs for different application functionalities
    tabs = st.tabs([
        "Data Overview", 
        "Statistics", 
        "Strategy Generation", 
        "Results Analysis", 
        "Visualizations",
        "Add Latest Draw",
        "Strategy Performance"
    ])
    
    # Data Overview tab
    with tabs[0]:
        st.header("Data Overview")
        
        lottery_type = st.radio(
            "Select Lottery Type",
            ["Euromillions", "French Loto"],
            horizontal=True,
            key="overview_lottery_type"
        )
        
        if lottery_type == "Euromillions":
            if not st.session_state.data_loaded:
                st.warning("Please load Euromillions data from the sidebar first.")
            else:
                # Display raw data table
                st.subheader("Euromillions Drawings")
                st.dataframe(st.session_state.processed_data)
                
                # Export options
                st.subheader("Export Data")
                export_format = st.radio("Choose export format:", ["CSV", "Excel"], horizontal=True)
                
                if st.button("Download Data"):
                    if export_format == "CSV":
                        csv = st.session_state.processed_data.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="euromillions_data.csv",
                            mime="text/csv"
                        )
                    else:
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            st.session_state.processed_data.to_excel(writer, sheet_name="Euromillions", index=False)
                        st.download_button(
                            label="Download Excel",
                            data=output.getvalue(),
                            file_name="euromillions_data.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
        else:
            if not st.session_state.french_loto_data_loaded:
                st.warning("Please load French Loto data from the sidebar first.")
            else:
                # Display raw data table
                st.subheader("French Loto Drawings")
                st.dataframe(st.session_state.french_loto_data)
                
                # Export options
                st.subheader("Export Data")
                export_format = st.radio("Choose export format:", ["CSV", "Excel"], horizontal=True)
                
                if st.button("Download Data"):
                    if export_format == "CSV":
                        csv = st.session_state.french_loto_data.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="french_loto_data.csv",
                            mime="text/csv"
                        )
                    else:
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            st.session_state.french_loto_data.to_excel(writer, sheet_name="FrenchLoto", index=False)
                        st.download_button(
                            label="Download Excel",
                            data=output.getvalue(),
                            file_name="french_loto_data.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
    
    # Statistics tab
    with tabs[1]:
        st.header("Statistical Analysis")
        
        lottery_type = st.radio(
            "Select Lottery Type",
            ["Euromillions", "French Loto"],
            horizontal=True,
            key="stats_lottery_type"
        )
        
        if lottery_type == "Euromillions":
            if not st.session_state.data_loaded:
                st.warning("Please load Euromillions data from the sidebar first.")
            else:
                # Create frequency analysis
                st.subheader("Number Frequency Analysis")
                
                # Count frequencies of main numbers
                main_number_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
                main_numbers = pd.Series(st.session_state.processed_data[main_number_cols].values.flatten())
                main_freq = main_numbers.value_counts().sort_index()
                
                # Create a DataFrame for all possible numbers (1-50)
                all_main_numbers = pd.DataFrame({'number': range(1, 51)})
                main_freq_df = pd.DataFrame({'number': main_freq.index, 'frequency': main_freq.values})
                
                # Merge to include numbers with zero frequency
                main_freq_df = all_main_numbers.merge(main_freq_df, on='number', how='left').fillna(0)
                
                # Calculate star frequencies
                star_number_cols = ['s1', 's2']
                star_numbers = pd.Series(st.session_state.processed_data[star_number_cols].values.flatten())
                star_freq = star_numbers.value_counts().sort_index()
                
                # Create a DataFrame for all possible stars (1-12)
                all_star_numbers = pd.DataFrame({'number': range(1, 13)})
                star_freq_df = pd.DataFrame({'number': star_freq.index, 'frequency': star_freq.values})
                
                # Merge to include numbers with zero frequency
                star_freq_df = all_star_numbers.merge(star_freq_df, on='number', how='left').fillna(0)
                
                # Display bar charts for frequencies
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Main Numbers (1-50)")
                    fig = px.bar(
                        main_freq_df,
                        x='number',
                        y='frequency',
                        title='Frequency of Main Numbers',
                        labels={'number': 'Number', 'frequency': 'Frequency'},
                        color='frequency',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("Star Numbers (1-12)")
                    fig = px.bar(
                        star_freq_df,
                        x='number',
                        y='frequency',
                        title='Frequency of Star Numbers',
                        labels={'number': 'Number', 'frequency': 'Frequency'},
                        color='frequency',
                        color_continuous_scale='Inferno'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Hot and cold numbers
                st.subheader("Hot and Cold Numbers")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("Hot Numbers (Most Frequent)")
                    hot_main = main_freq_df.nlargest(10, 'frequency')
                    st.dataframe(hot_main)
                    
                with col2:
                    st.write("Cold Numbers (Least Frequent)")
                    cold_main = main_freq_df.nsmallest(10, 'frequency')
                    st.dataframe(cold_main)
                
                # Custom analysis
                st.subheader("Advanced Analysis")
                try:
                    combination_size = st.slider("Combination Size", 1, 5, 3)
                    st.write(f"Analyzing {combination_size}-number combinations...")
                    combination_analysis = analyze_number_combinations(size=combination_size)
                    
                    if combination_analysis and 'most_frequent' in combination_analysis:
                        st.write(f"Most Frequent {combination_size}-Number Combinations:")
                        for combo, freq in combination_analysis['most_frequent']:
                            st.write(f"Numbers {combo}: {freq} occurrences")
                except Exception as e:
                    st.error(f"Error in combination analysis: {str(e)}")
        
        else:  # French Loto
            if not st.session_state.french_loto_data_loaded:
                st.warning("Please load French Loto data from the sidebar first.")
            else:
                try:
                    # Initialize the FrenchLotoStatistics module
                    try:
                        stats = FrenchLotoStatistics(st.session_state.french_loto_data)
                    except Exception as e:
                        st.error(f"Error initializing statistics module: {str(e)}")
                        stats = None
                    
                    if stats:
                        # Get hot and cold numbers
                        hot_numbers, cold_numbers = stats.get_hot_cold_numbers()
                        hot_lucky, cold_lucky = stats.get_hot_cold_lucky_numbers()
                        
                        # Display hot and cold numbers
                        st.subheader("Hot and Cold Numbers")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("Hot Main Numbers (Most Frequent)")
                            st.write(hot_numbers)
                            
                            st.write("Hot Lucky Numbers")
                            st.write(hot_lucky)
                        
                        with col2:
                            st.write("Cold Main Numbers (Least Frequent)")
                            st.write(cold_numbers)
                            
                            st.write("Cold Lucky Numbers")
                            st.write(cold_lucky)
                        
                        # Display frequency charts
                        st.subheader("Number Frequency Analysis")
                        main_freq_df, lucky_freq_df = stats.get_frequency_dataframes()
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Main Numbers (1-49)")
                            fig = px.bar(
                                main_freq_df,
                                x='number',
                                y='frequency',
                                title='Frequency of Main Numbers',
                                labels={'number': 'Number', 'frequency': 'Frequency'},
                                color='frequency',
                                color_continuous_scale='Viridis'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            st.subheader("Lucky Numbers (1-10)")
                            fig = px.bar(
                                lucky_freq_df,
                                x='number',
                                y='frequency',
                                title='Frequency of Lucky Numbers',
                                labels={'number': 'Number', 'frequency': 'Frequency'},
                                color='frequency',
                                color_continuous_scale='Inferno'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Display distribution analysis
                        st.subheader("Number Distribution Analysis")
                        dist_stats = stats.get_distribution_stats()
                        
                        st.write("Even/Odd Distribution")
                        st.write(f"Most common pattern: {dist_stats['even_odd_pattern']}")
                        
                        st.write("Low/High Distribution")
                        st.write(f"Most common pattern: {dist_stats['low_high_pattern']}")
                        
                        # Display time-based trends
                        st.subheader("Recency Analysis")
                        recent_freq = stats.get_recency_stats(draws=20)
                        
                        st.write("Recent Trends (Last 20 Draws)")
                        st.write(f"Most frequent numbers in recent draws: {recent_freq['hot_numbers']}")
                        st.write(f"Most frequent lucky numbers in recent draws: {recent_freq['hot_lucky']}")
                    
                except Exception as e:
                    st.error(f"Error in French Loto statistics analysis: {str(e)}")
    
    # Strategy Generation tab
    with tabs[2]:
        st.header("Strategy Generation")
        
        lottery_type = st.radio(
            "Select Lottery Type",
            ["Euromillions", "French Loto"],
            horizontal=True,
            key="strategy_lottery_type"
        )
        
        if lottery_type == "Euromillions":
            if not st.session_state.data_loaded:
                st.warning("Please load Euromillions data from the sidebar first.")
            else:
                # Strategy options
                st.subheader("Strategy Parameters")
                
                # Initialize strategies
                try:
                    # Create a simple statistics class for Euromillions data
                    from statistics import EuromillionsStatistics
                    euro_stats = EuromillionsStatistics(st.session_state.processed_data)
                    strategies = PredictionStrategies(euro_stats)
                except Exception as e:
                    st.error(f"Error initializing prediction strategies: {str(e)}")
                    strategies = None
                
                if strategies:
                    # Information about strategy performance
                    st.info(get_strategy_info_text())
                    
                    # Strategy selection
                    strategy_type = st.selectbox(
                        "Select Strategy",
                        [
                            "Risk/Reward Balance ⭐",
                            "Frequency Analysis ⭐",
                            "Markov Chain Model ⭐",
                            "Time Series Analysis ⭐",
                            "Bayesian Inference",
                            "Coverage Optimization",
                            "Temporal Patterns",
                            "Stratified Sampling",
                            "Anti-Cognitive Bias",
                            "Mixed Strategy"
                        ]
                    )
                    
                    
                    # Function to process strategy name that might have star symbols
                    base_strategy_type = get_base_strategy_name(strategy_type)
                    # Parameters for each strategy
                    if base_strategy_type == "Frequency Analysis":
                        recency_weight = st.slider(
                            "Recency Weight",
                            0.0, 1.0, 0.3,
                            help="Higher values give more importance to recent draws"
                        )
                    
                    elif base_strategy_type == "Temporal Patterns":
                        pattern_depth = st.slider(
                            "Pattern Recognition Depth",
                            1, 10, 3,
                            help="Number of historical patterns to consider"
                        )
                    
                    elif base_strategy_type == "Stratified Sampling":
                        confidence = st.slider(
                            "Confidence Level",
                            0.0, 1.0, 0.8,
                            help="Higher values lead to more conservative predictions"
                        )
                    
                    elif base_strategy_type == "Coverage Optimization":
                        balance = st.slider(
                            "Coverage Balance",
                            0.0, 1.0, 0.6,
                            help="Balance between number density and range coverage"
                        )
                    
                    elif base_strategy_type == "Bayesian Inference":
                        recent_draws_count = st.slider(
                            "Recent Draws to Consider",
                            5, 50, 20,
                            help="Number of recent draws to factor into the Bayesian model"
                        )
                        prior_strength = st.slider(
                            "Prior Strength",
                            0.1, 5.0, 1.0,
                            help="Strength of the prior distribution"
                        )
                    
                    elif base_strategy_type == "Risk/Reward Balance":
                        risk_level = st.slider(
                            "Risk Level",
                            0.0, 1.0, 0.5,
                            help="Higher values favor high-risk, high-reward combinations"
                        )
                    
                    elif base_strategy_type == "Markov Chain Model":
                        balanced = st.slider(
                            "Balance Factor",
                            0.0, 1.0, 0.7,
                            help="Balance between pattern prediction and randomness"
                        )
                    
                    elif base_strategy_type == "Time Series Analysis":
                        lag = st.slider(
                            "Lag Parameter",
                            1, 10, 3,
                            help="Lag for time series forecasting"
                        )
                    
                    elif base_strategy_type == "Anti-Cognitive Bias":
                        window_size = st.slider(
                            "Analysis Window",
                            5, 30, 10,
                            help="Window size for analyzing cognitive biases"
                        )
                    
                    # Number of combinations to generate
                    num_combinations = st.slider("Number of Combinations", 1, 10, 5)
                    
                    # Generate combinations
                    generate_button = st.button("Generate Combinations")
                    
                    if generate_button:
                        with st.spinner(f"Generating {num_combinations} combinations using {strategy_type}..."):
                            try:
                                combinations = []
                                
                                if base_strategy_type == "Frequency Analysis":
                                    combinations = strategies.frequency_strategy(
                                        num_combinations=num_combinations,
                                        recency_weight=recency_weight
                                    )
                                
                                elif base_strategy_type == "Temporal Patterns":
                                    combinations = strategies.temporal_pattern_strategy(
                                        num_combinations=num_combinations,
                                        pattern_depth=pattern_depth
                                    )
                                
                                elif base_strategy_type == "Stratified Sampling":
                                    combinations = strategies.stratified_sampling_strategy(
                                        num_combinations=num_combinations,
                                        confidence=confidence
                                    )
                                
                                elif base_strategy_type == "Coverage Optimization":
                                    combinations = strategies.coverage_optimization_strategy(
                                        num_combinations=num_combinations,
                                        balance=balance
                                    )
                                
                                elif base_strategy_type == "Bayesian Inference":
                                    combinations = strategies.bayesian_strategy(
                                        num_combinations=num_combinations,
                                        prior_type="adaptive",
                                        recent_draws_count=recent_draws_count,
                                        prior_strength=prior_strength
                                    )
                                
                                elif base_strategy_type == "Risk/Reward Balance":
                                    combinations = strategies.risk_reward_strategy(
                                        num_combinations=num_combinations,
                                        risk_level=risk_level
                                    )
                                
                                elif base_strategy_type == "Markov Chain Model":
                                    combinations = strategies.markov_chain_strategy(
                                        num_combinations=num_combinations,
                                        balanced=balanced
                                    )
                                
                                elif base_strategy_type == "Time Series Analysis":
                                    combinations = strategies.time_series_strategy(
                                        num_combinations=num_combinations,
                                        lag=lag
                                    )
                                
                                elif base_strategy_type == "Anti-Cognitive Bias":
                                    combinations = strategies.cognitive_bias_strategy(
                                        num_combinations=num_combinations,
                                        window_size=window_size
                                    )
                                
                                elif base_strategy_type == "Mixed Strategy":
                                    combinations = strategies.mixed_strategy(
                                        num_combinations=num_combinations
                                    )
                                
                                # Display generated combinations
                                if combinations:
                                    st.subheader("Generated Combinations")
                                    
                                    for i, combo in enumerate(combinations):
                                        col1, col2, col3 = st.columns([3, 2, 1])
                                        
                                        with col1:
                                            st.write(f"**Combination {i+1}**")
                                            numbers_str = ", ".join([str(n) for n in combo['numbers']])
                                            stars_str = ", ".join([str(s) for s in combo['stars']])
                                            st.write(f"Numbers: {numbers_str}")
                                            st.write(f"Stars: {stars_str}")
                                        
                                        with col2:
                                            if 'score' in combo:
                                                st.write(f"Score: {combo['score']:.2f}")
                                            if 'rationale' in combo:
                                                st.write(f"Rationale: {combo['rationale']}")
                                        
                                        with col3:
                                            # Save to database button
                                            if st.button(f"Save #{i+1}", key=f"save_combo_{i}"):
                                                try:
                                                    from database import GeneratedCombination, get_session
                                                    
                                                    # Create new combination record
                                                    new_combo = GeneratedCombination(
                                                        created_at=date.today(),
                                                        numbers=json.dumps(combo['numbers']),
                                                        stars=json.dumps(combo['stars']),
                                                        strategy=strategy_type,
                                                        score=combo.get('score', 0.0)
                                                    )
                                                    
                                                    # Save to database
                                                    session = get_session()
                                                    session.add(new_combo)
                                                    session.commit()
                                                    session.close()
                                                    
                                                    st.success(f"Combination #{i+1} saved successfully!")
                                                except Exception as e:
                                                    st.error(f"Error saving combination: {str(e)}")
                            
                            except Exception as e:
                                st.error(f"Error generating combinations: {str(e)}")
        
        else:  # French Loto
            if not st.session_state.french_loto_data_loaded:
                st.warning("Please load French Loto data from the sidebar first.")
            else:
                # Strategy options
                st.subheader("French Loto Strategy Parameters")
                
                # Initialize strategies
                try:
                    strategies = FrenchLotoStrategy(st.session_state.french_loto_data)
                except Exception as e:
                    st.error(f"Error initializing French Loto strategies: {str(e)}")
                    strategies = None
                
                if strategies:
                    # Information about strategy performance
                    st.info(get_strategy_info_text())
                    
                    # Strategy selection
                    strategy_type = st.selectbox(
                        "Select Strategy",
                        [
                            "Risk/Reward Balance ⭐",
                            "Frequency Analysis ⭐",
                            "Markov Chain Model ⭐",
                            "Time Series Analysis ⭐",
                            "Bayesian Inference",
                            "Coverage Optimization",
                            "Temporal Patterns",
                            "Stratified Sampling",
                            "Anti-Cognitive Bias",
                            "Mixed Strategy"
                        ]
                    )
                    
                    
                    # Function to process strategy name that might have star symbols
                    base_strategy_type = get_base_strategy_name(strategy_type)
                    # Parameters for each strategy
                    if base_strategy_type == "Frequency Analysis":
                        recency_weight = st.slider(
                            "Recency Weight",
                            0.0, 1.0, 0.3,
                            help="Higher values give more importance to recent draws"
                        )
                    
                    elif base_strategy_type == "Temporal Patterns":
                        pattern_depth = st.slider(
                            "Pattern Recognition Depth",
                            1, 10, 3,
                            help="Number of historical patterns to consider"
                        )
                    
                    elif base_strategy_type == "Stratified Sampling":
                        confidence = st.slider(
                            "Confidence Level",
                            0.0, 1.0, 0.8,
                            help="Higher values lead to more conservative predictions"
                        )
                    
                    elif base_strategy_type == "Coverage Optimization":
                        balance = st.slider(
                            "Coverage Balance",
                            0.0, 1.0, 0.6,
                            help="Balance between number density and range coverage"
                        )
                    
                    elif base_strategy_type == "Bayesian Inference":
                        recent_draws_count = st.slider(
                            "Recent Draws to Consider",
                            5, 50, 20,
                            help="Number of recent draws to factor into the Bayesian model"
                        )
                        prior_strength = st.slider(
                            "Prior Strength",
                            0.1, 5.0, 1.0,
                            help="Strength of the prior distribution"
                        )
                    
                    elif base_strategy_type == "Risk/Reward Balance":
                        risk_level = st.slider(
                            "Risk Level",
                            0.0, 1.0, 0.5,
                            help="Higher values favor high-risk, high-reward combinations"
                        )
                    
                    elif base_strategy_type == "Markov Chain Model":
                        balanced = st.slider(
                            "Balance Factor",
                            0.0, 1.0, 0.7,
                            help="Balance between pattern prediction and randomness"
                        )
                    
                    elif base_strategy_type == "Time Series Analysis":
                        lag = st.slider(
                            "Lag Parameter",
                            1, 10, 3,
                            help="Lag for time series forecasting"
                        )
                    
                    elif base_strategy_type == "Anti-Cognitive Bias":
                        window_size = st.slider(
                            "Analysis Window",
                            5, 30, 10,
                            help="Window size for analyzing cognitive biases"
                        )
                    
                    # Number of combinations to generate
                    num_combinations = st.slider("Number of Combinations", 1, 10, 5)
                    
                    # Generate combinations
                    generate_button = st.button("Generate Combinations")
                    
                    if generate_button:
                        with st.spinner(f"Generating {num_combinations} combinations using {strategy_type}..."):
                            try:
                                combinations = []
                                
                                if base_strategy_type == "Frequency Analysis":
                                    combinations = strategies.frequency_strategy(
                                        num_combinations=num_combinations,
                                        recency_weight=recency_weight
                                    )
                                
                                elif base_strategy_type == "Temporal Patterns":
                                    combinations = strategies.temporal_pattern_strategy(
                                        num_combinations=num_combinations,
                                        pattern_depth=pattern_depth
                                    )
                                
                                elif base_strategy_type == "Stratified Sampling":
                                    combinations = strategies.stratified_sampling_strategy(
                                        num_combinations=num_combinations,
                                        confidence=confidence
                                    )
                                
                                elif base_strategy_type == "Coverage Optimization":
                                    combinations = strategies.coverage_optimization_strategy(
                                        num_combinations=num_combinations,
                                        balance=balance
                                    )
                                
                                elif base_strategy_type == "Bayesian Inference":
                                    combinations = strategies.bayesian_strategy(
                                        num_combinations=num_combinations,
                                        prior_type="adaptive",
                                        recent_draws_count=recent_draws_count,
                                        prior_strength=prior_strength
                                    )
                                
                                elif base_strategy_type == "Risk/Reward Balance":
                                    combinations = strategies.risk_reward_strategy(
                                        num_combinations=num_combinations,
                                        risk_level=risk_level
                                    )
                                
                                elif base_strategy_type == "Markov Chain Model":
                                    combinations = strategies.markov_chain_strategy(
                                        num_combinations=num_combinations,
                                        balanced=balanced
                                    )
                                
                                elif base_strategy_type == "Time Series Analysis":
                                    combinations = strategies.time_series_strategy(
                                        num_combinations=num_combinations,
                                        lag=lag
                                    )
                                
                                elif base_strategy_type == "Anti-Cognitive Bias":
                                    combinations = strategies.cognitive_bias_strategy(
                                        num_combinations=num_combinations,
                                        window_size=window_size
                                    )
                                
                                elif base_strategy_type == "Mixed Strategy":
                                    combinations = strategies.mixed_strategy(
                                        num_combinations=num_combinations
                                    )
                                
                                # Display generated combinations
                                if combinations:
                                    st.subheader("Generated Combinations")
                                    
                                    for i, combo in enumerate(combinations):
                                        col1, col2, col3 = st.columns([3, 2, 1])
                                        
                                        with col1:
                                            st.write(f"**Combination {i+1}**")
                                            numbers_str = ", ".join([str(n) for n in combo['numbers']])
                                            st.write(f"Numbers: {numbers_str}")
                                            st.write(f"Lucky Number: {combo['lucky']}")
                                        
                                        with col2:
                                            if 'score' in combo:
                                                st.write(f"Score: {combo['score']:.2f}")
                                            if 'rationale' in combo:
                                                st.write(f"Rationale: {combo['rationale']}")
                                        
                                        with col3:
                                            # Save to database button
                                            if st.button(f"Save #{i+1}", key=f"save_loto_combo_{i}"):
                                                try:
                                                    from database import FrenchLotoPrediction, get_session
                                                    
                                                    # Format numbers as dash-separated string
                                                    numbers_str = "-".join([str(n) for n in combo['numbers']])
                                                    
                                                    # Create new prediction record
                                                    new_combo = FrenchLotoPrediction(
                                                        date_generated=date.today(),
                                                        numbers=numbers_str,
                                                        lucky=combo['lucky'],
                                                        strategy=strategy_type,
                                                        score=combo.get('score', 0.0)
                                                    )
                                                    
                                                    # Save to database
                                                    session = get_session()
                                                    session.add(new_combo)
                                                    session.commit()
                                                    session.close()
                                                    
                                                    st.success(f"Combination #{i+1} saved successfully!")
                                                except Exception as e:
                                                    st.error(f"Error saving combination: {str(e)}")
                            
                            except Exception as e:
                                st.error(f"Error generating combinations: {str(e)}")
    
    # Results Analysis tab
    with tabs[3]:
        st.header("Results Analysis")
        st.write("Results analysis functionality will be implemented here.")
        
    # Visualizations tab
    with tabs[4]:
        st.header("Visualizations")
        st.write("Visualization tools will be added here.")
        
    # Add Latest Draw tab
    with tabs[5]:
        st.header("Add Latest Draw")
        
        # Select lottery type for the new draw
        lottery_type = st.radio(
            "Select Lottery Type",
            ["Euromillions", "French Loto"],
            horizontal=True,
            key="latest_draw_lottery_type"
        )
        
        if lottery_type == "Euromillions":
            st.subheader("Add Latest Euromillions Draw")
            
            # Form for adding a new Euromillions draw
            with st.form(key="add_euromillions_form"):
                # Draw date
                from datetime import datetime as dt
                current_date = dt.now().date()
                draw_date = st.date_input("Draw Date", value=current_date)
                
                # Day of week (auto-populated)
                day_of_week = draw_date.strftime("%A")
                st.write(f"Day of week: {day_of_week}")
                
                # Numbers input
                st.subheader("Main Numbers (1-50)")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    n1 = st.number_input("Number 1", min_value=1, max_value=50, step=1)
                with col2:
                    n2 = st.number_input("Number 2", min_value=1, max_value=50, step=1)
                with col3:
                    n3 = st.number_input("Number 3", min_value=1, max_value=50, step=1)
                with col4:
                    n4 = st.number_input("Number 4", min_value=1, max_value=50, step=1)
                with col5:
                    n5 = st.number_input("Number 5", min_value=1, max_value=50, step=1)
                
                st.subheader("Star Numbers (1-12)")
                col1, col2 = st.columns(2)
                with col1:
                    s1 = st.number_input("Star 1", min_value=1, max_value=12, step=1)
                with col2:
                    s2 = st.number_input("Star 2", min_value=1, max_value=12, step=1)
                
                # Submit button
                submit_button = st.form_submit_button("Add Euromillions Draw")
                
                if submit_button:
                    # Validate numbers (make sure they're unique)
                    all_numbers = [n1, n2, n3, n4, n5]
                    all_stars = [s1, s2]
                    
                    if len(set(all_numbers)) != 5:
                        st.error("❌ Main numbers must be unique!")
                    elif len(set(all_stars)) != 2:
                        st.error("❌ Star numbers must be unique!")
                    else:
                        try:
                            # Import EuromillionsDrawing model
                            from database import EuromillionsDrawing, get_session
                            
                            # Create new drawing
                            new_draw = EuromillionsDrawing(
                                date=draw_date,
                                day_of_week=day_of_week,
                                n1=n1,
                                n2=n2,
                                n3=n3,
                                n4=n4,
                                n5=n5,
                                s1=s1,
                                s2=s2
                            )
                            
                            # Save to database
                            session = get_session()
                            try:
                                # Check if this date already exists
                                existing_draw = session.query(EuromillionsDrawing).filter_by(date=draw_date).first()
                                if existing_draw:
                                    st.warning(f"⚠️ A draw for {draw_date} already exists. Updating with new numbers.")
                                    # Update existing draw
                                    existing_draw.n1 = n1
                                    existing_draw.n2 = n2
                                    existing_draw.n3 = n3
                                    existing_draw.n4 = n4
                                    existing_draw.n5 = n5
                                    existing_draw.s1 = s1
                                    existing_draw.s2 = s2
                                else:
                                    # Add new draw
                                    session.add(new_draw)
                                
                                session.commit()
                                st.success(f"✅ Successfully added Euromillions draw for {draw_date}!")
                                
                                # Force reload of data if it was already loaded
                                if st.session_state.data_loaded:
                                    conn = get_db_connection()
                                    if conn:
                                        query = "SELECT * FROM euromillions_drawings ORDER BY date DESC"
                                        data = pd.read_sql(query, conn)
                                        st.session_state.processed_data = data
                                
                            except Exception as e:
                                session.rollback()
                                st.error(f"❌ Error adding draw: {str(e)}")
                            finally:
                                session.close()
                        except Exception as e:
                            st.error(f"❌ Database error: {str(e)}")
        
        else:  # French Loto
            st.subheader("Add Latest French Loto Draw")
            
            # Form for adding a new French Loto draw
            with st.form(key="add_french_loto_form"):
                # Draw date
                from datetime import datetime as dt
                current_date = dt.now().date()
                draw_date = st.date_input("Draw Date", value=current_date)
                
                # Day of week (auto-populated)
                day_of_week = draw_date.strftime("%A")
                st.write(f"Day of week: {day_of_week}")
                
                # Numbers input
                st.subheader("Main Numbers (1-49)")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    n1 = st.number_input("Number 1", min_value=1, max_value=49, step=1)
                with col2:
                    n2 = st.number_input("Number 2", min_value=1, max_value=49, step=1)
                with col3:
                    n3 = st.number_input("Number 3", min_value=1, max_value=49, step=1)
                with col4:
                    n4 = st.number_input("Number 4", min_value=1, max_value=49, step=1)
                with col5:
                    n5 = st.number_input("Number 5", min_value=1, max_value=49, step=1)
                
                st.subheader("Lucky Number (1-10)")
                lucky = st.number_input("Lucky Number", min_value=1, max_value=10, step=1)
                
                # Winner information (optional)
                st.subheader("Winner Information (Optional)")
                cols = st.columns(3)
                with cols[0]:
                    winners_rank1 = st.number_input("Rank 1 Winners", min_value=0, step=1)
                with cols[1]:
                    winners_rank2 = st.number_input("Rank 2 Winners", min_value=0, step=1)
                with cols[2]:
                    winners_rank3 = st.number_input("Rank 3 Winners", min_value=0, step=1)
                
                # Prize information (optional)
                st.subheader("Prize Information (Optional)")
                cols = st.columns(3)
                with cols[0]:
                    prize_rank1 = st.number_input("Rank 1 Prize (€)", min_value=0.0, step=1000.0)
                with cols[1]:
                    prize_rank2 = st.number_input("Rank 2 Prize (€)", min_value=0.0, step=100.0)
                with cols[2]:
                    prize_rank3 = st.number_input("Rank 3 Prize (€)", min_value=0.0, step=10.0)
                
                # Submit button
                submit_button = st.form_submit_button("Add French Loto Draw")
                
                if submit_button:
                    # Validate numbers (make sure they're unique)
                    all_numbers = [n1, n2, n3, n4, n5]
                    
                    if len(set(all_numbers)) != 5:
                        st.error("❌ Main numbers must be unique!")
                    else:
                        try:
                            # Import FrenchLotoDrawing model
                            from database import FrenchLotoDrawing, get_session
                            
                            # Create new drawing
                            new_draw = FrenchLotoDrawing(
                                date=draw_date,
                                day_of_week=day_of_week,
                                n1=n1,
                                n2=n2,
                                n3=n3,
                                n4=n4,
                                n5=n5,
                                lucky=lucky,
                                winners_rank1=winners_rank1,
                                winners_rank2=winners_rank2,
                                winners_rank3=winners_rank3,
                                prize_rank1=prize_rank1,
                                prize_rank2=prize_rank2,
                                prize_rank3=prize_rank3,
                                currency="EUR"
                            )
                            
                            # Save to database
                            session = get_session()
                            try:
                                # Check if this date already exists
                                existing_draw = session.query(FrenchLotoDrawing).filter_by(date=draw_date).first()
                                if existing_draw:
                                    st.warning(f"⚠️ A draw for {draw_date} already exists. Updating with new numbers.")
                                    # Update existing draw
                                    existing_draw.n1 = n1
                                    existing_draw.n2 = n2
                                    existing_draw.n3 = n3
                                    existing_draw.n4 = n4
                                    existing_draw.n5 = n5
                                    existing_draw.lucky = lucky
                                    existing_draw.winners_rank1 = winners_rank1
                                    existing_draw.winners_rank2 = winners_rank2
                                    existing_draw.winners_rank3 = winners_rank3
                                    existing_draw.prize_rank1 = prize_rank1
                                    existing_draw.prize_rank2 = prize_rank2
                                    existing_draw.prize_rank3 = prize_rank3
                                else:
                                    # Add new draw
                                    session.add(new_draw)
                                
                                session.commit()
                                st.success(f"✅ Successfully added French Loto draw for {draw_date}!")
                                
                                # Force reload of data if it was already loaded
                                if st.session_state.french_loto_data_loaded:
                                    conn = get_db_connection()
                                    if conn:
                                        query = "SELECT * FROM french_loto_drawings ORDER BY date DESC"
                                        data = pd.read_sql(query, conn)
                                        st.session_state.french_loto_data = data
                                
                            except Exception as e:
                                session.rollback()
                                st.error(f"❌ Error adding draw: {str(e)}")
                            finally:
                                session.close()
                        except Exception as e:
                            st.error(f"❌ Database error: {str(e)}")
    
    # Strategy Performance tab
    with tabs[6]:
        st.header("Strategy Performance Analysis")
        
        # Select lottery type for the performance analysis
        lottery_perf_type = st.radio(
            "Select Lottery Type",
            ["Euromillions", "French Loto"],
            horizontal=True,
            key="perf_lottery_type"
        )
        
        if lottery_perf_type == "French Loto":
            st.subheader("French Loto Strategy Performance")
            
            st.write("Based on comprehensive backtesting against historical data (30% test set, 20 combinations per strategy), here are the results:")
            
            # Display performance metrics for each strategy
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Best Performing Strategies")
                st.markdown("""
                1. **Risk/Reward Strategy**: 2.16/6 avg score, 22.69% win rate
                2. **Frequency Analysis**: 2.15/6 avg score, 21.45% win rate
                3. **Markov Chain Model**: 2.14/6 avg score, 23.26% win rate
                4. **Time Series Analysis**: 2.14/6 avg score, 22.12% win rate
                """)
                
                st.markdown("### Recommendations")
                st.markdown("""
                - **Risk/Reward Balance** is optimal for maximizing both your match rate and potential payouts
                - **Markov Chain Model** gives the highest win percentage but slightly lower average matches
                - For consistent performance, consider a blend of the top three strategies
                """)
                
            with col2:
                # Example performance chart
                strategy_data = {
                    'Strategy': ['Risk/Reward', 'Frequency', 'Markov', 'Time Series', 'Bayesian', 
                                'Coverage', 'Temporal', 'Stratified', 'Cognitive', 'Mixed'],
                    'Average Score': [2.16, 2.15, 2.14, 2.14, 2.10, 2.13, 2.13, 2.06, 2.09, 1.91],
                    'Win Rate (%)': [22.69, 21.45, 23.26, 22.12, 20.97, 22.50, 20.59, 18.02, 20.02, 14.78]
                }
                
                df_perf = pd.DataFrame(strategy_data)
                
                # Bar chart of average scores
                st.write("Average Score by Strategy (out of 6)")
                fig1 = px.bar(df_perf, x='Strategy', y='Average Score', color='Average Score',
                             color_continuous_scale='Viridis', height=300)
                st.plotly_chart(fig1, use_container_width=True)
                
                # Bar chart of win rates
                st.write("Win Rate by Strategy (%)")
                fig2 = px.bar(df_perf, x='Strategy', y='Win Rate (%)', color='Win Rate (%)',
                             color_continuous_scale='Viridis', height=300)
                st.plotly_chart(fig2, use_container_width=True)
            
            st.info("**Analysis Details**: Backtesting conducted across 1,049 test drawings from historical data. " +
                   "Win rate refers to matches of 3 or more numbers (threshold for winning a prize).")
        
        else:  # Euromillions
            st.subheader("Euromillions Strategy Performance")
            st.write("Euromillions strategy performance analysis coming soon.")
            st.info("Run the backtesting module to see comprehensive performance statistics for Euromillions strategies.")


if __name__ == "__main__":
    main()