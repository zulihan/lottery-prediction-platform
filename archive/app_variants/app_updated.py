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
                        
                        st.write("Distribution of Numbers by Position:")
                        st.json(dist_stats)
                        
                except Exception as e:
                    st.error(f"Error in French Loto statistics: {str(e)}")
    
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
                    strategies = PredictionStrategies(st.session_state.processed_data)
                except Exception as e:
                    st.error(f"Error initializing strategies: {str(e)}")
                    strategies = None
                
                if strategies:
                    # Strategy selection
                    strategy_type = st.selectbox(
                        "Select Strategy",
                        [
                            "Frequency Analysis",
                            "Mixed Strategy",
                            "Temporal Patterns",
                            "Stratified Sampling",
                            "Coverage Optimization",
                            "Risk/Reward Balance",
                            "Bayesian Inference",
                            "Markov Chain Model",
                            "Time Series Analysis",
                            "Anti-Cognitive Bias"
                        ]
                    )
                    
                    # Parameters for each strategy
                    if strategy_type == "Frequency Analysis":
                        recency_weight = st.slider(
                            "Recency Weight",
                            0.0, 1.0, 0.3,
                            help="Higher values give more importance to recent draws"
                        )
                    
                    elif strategy_type == "Temporal Patterns":
                        pattern_depth = st.slider(
                            "Pattern Recognition Depth",
                            1, 10, 3,
                            help="Number of historical patterns to consider"
                        )
                    
                    elif strategy_type == "Stratified Sampling":
                        confidence = st.slider(
                            "Confidence Level",
                            0.1, 0.99, 0.8,
                            help="Statistical confidence level for sampling"
                        )
                    
                    elif strategy_type == "Coverage Optimization":
                        balance = st.slider(
                            "Coverage Balance",
                            0.0, 1.0, 0.5,
                            help="Balance between full coverage and frequency-based optimization"
                        )
                    
                    elif strategy_type == "Bayesian Inference":
                        recent_draws_count = st.slider(
                            "Recent Draws to Consider",
                            5, 100, 20,
                            help="Number of recent draws to use for Bayesian prior"
                        )
                        
                        prior_strength = st.slider(
                            "Prior Strength",
                            0.1, 5.0, 1.0, 0.1,
                            help="Weight given to prior beliefs vs. observed data"
                        )
                    
                    elif strategy_type == "Risk/Reward Balance":
                        risk_level = st.slider(
                            "Risk Level",
                            0.0, 1.0, 0.5,
                            help="Higher values favor riskier combinations with potentially higher rewards"
                        )
                    
                    elif strategy_type == "Markov Chain Model":
                        balanced = st.slider(
                            "Balance Factor",
                            0.0, 1.0, 0.5,
                            help="Balance between pure Markov predictions and frequency analysis"
                        )
                    
                    elif strategy_type == "Time Series Analysis":
                        lag = st.slider(
                            "Lag Parameter",
                            1, 10, 3,
                            help="Number of previous draws to consider for time series analysis"
                        )
                    
                    elif strategy_type == "Anti-Cognitive Bias":
                        window_size = st.slider(
                            "Analysis Window",
                            5, 100, 20,
                            help="Number of past draws to analyze for cognitive biases"
                        )
                    
                    # Number of combinations to generate
                    num_combinations = st.slider("Number of Combinations", 1, 10, 5)
                    
                    # Generate combinations
                    generate_button = st.button("Generate Combinations")
                    
                    if generate_button:
                        with st.spinner(f"Generating {num_combinations} combinations using {strategy_type}..."):
                            try:
                                combinations = []
                                
                                if strategy_type == "Frequency Analysis":
                                    combinations = strategies.frequency_strategy(
                                        num_combinations=num_combinations,
                                        recency_weight=recency_weight
                                    )
                                
                                elif strategy_type == "Temporal Patterns":
                                    combinations = strategies.temporal_pattern_strategy(
                                        num_combinations=num_combinations,
                                        pattern_depth=pattern_depth
                                    )
                                
                                elif strategy_type == "Stratified Sampling":
                                    combinations = strategies.stratified_sampling_strategy(
                                        num_combinations=num_combinations,
                                        confidence=confidence
                                    )
                                
                                elif strategy_type == "Coverage Optimization":
                                    combinations = strategies.coverage_optimization_strategy(
                                        num_combinations=num_combinations,
                                        balance=balance
                                    )
                                
                                elif strategy_type == "Bayesian Inference":
                                    combinations = strategies.bayesian_strategy(
                                        num_combinations=num_combinations,
                                        recent_draws_count=recent_draws_count,
                                        prior_strength=prior_strength
                                    )
                                
                                elif strategy_type == "Risk/Reward Balance":
                                    combinations = strategies.risk_reward_strategy(
                                        num_combinations=num_combinations,
                                        risk_level=risk_level
                                    )
                                
                                elif strategy_type == "Markov Chain Model":
                                    combinations = strategies.markov_chain_strategy(
                                        num_combinations=num_combinations,
                                        balanced=balanced
                                    )
                                
                                elif strategy_type == "Time Series Analysis":
                                    combinations = strategies.time_series_strategy(
                                        num_combinations=num_combinations,
                                        lag=lag
                                    )
                                
                                elif strategy_type == "Anti-Cognitive Bias":
                                    combinations = strategies.cognitive_bias_strategy(
                                        num_combinations=num_combinations,
                                        window_size=window_size
                                    )
                                
                                elif strategy_type == "Mixed Strategy":
                                    combinations = strategies.mixed_strategy(
                                        num_combinations=num_combinations
                                    )
                                
                                # Display combinations
                                st.subheader("Generated Combinations")
                                
                                for i, combo in enumerate(combinations):
                                    st.write(f"**Combination {i+1}:**")
                                    
                                    col1, col2, col3 = st.columns([3, 2, 3])
                                    
                                    with col1:
                                        st.write(f"Main Numbers: {', '.join(map(str, combo['numbers']))}")
                                    
                                    with col2:
                                        st.write(f"Stars: {', '.join(map(str, combo['stars']))}")
                                    
                                    with col3:
                                        if 'score' in combo:
                                            st.write(f"Score: {combo['score']:.2f}/100")
                                
                                # Save combinations to database
                                save_option = st.radio(
                                    "Would you like to save these combinations?",
                                    ["Yes", "No"],
                                    horizontal=True
                                )
                                
                                if save_option == "Yes":
                                    save_name = st.text_input("Enter a name for this set of combinations:")
                                    
                                    if save_name and st.button("Save Combinations"):
                                        conn = get_db_connection()
                                        if conn:
                                            try:
                                                # Convert combinations to JSON
                                                combos_json = json.dumps({
                                                    'strategy': strategy_type,
                                                    'timestamp': datetime.now().isoformat(),
                                                    'combinations': combinations
                                                })
                                                
                                                # Save to database
                                                cur = conn.cursor()
                                                cur.execute(
                                                    "INSERT INTO saved_combinations (name, lottery_type, combinations) VALUES (%s, %s, %s)",
                                                    (save_name, "Euromillions", combos_json)
                                                )
                                                conn.commit()
                                                conn.close()
                                                
                                                st.success(f"Successfully saved {len(combinations)} combinations as '{save_name}'")
                                            except Exception as e:
                                                st.error(f"Error saving combinations: {str(e)}")
                                        else:
                                            st.error("Could not connect to database.")
                            
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
                    st.info("Based on our backtesting with 1,049 historical drawings, we've identified the best-performing strategies for French Loto.")
                    
                    # Strategy selection
                    strategy_type = st.selectbox(
                        "Select Strategy",
                        [
                            "Risk/Reward Balance ⭐",  # Top performer (2.16/6 score, 22.69% win rate)
                            "Frequency Analysis ⭐",   # Second best (2.15/6 score, 21.45% win rate)
                            "Markov Chain Model ⭐",   # Third best (2.14/6 score, 23.26% win rate)
                            "Time Series Analysis ⭐", # Fourth best (2.14/6 score, 22.12% win rate)
                            "Bayesian Inference",
                            "Coverage Optimization",
                            "Temporal Patterns",
                            "Stratified Sampling",
                            "Anti-Cognitive Bias",
                            "Mixed Strategy"
                        ]
                    )
                    
                    # Function to map displayed strategy names to internal names
                    def get_strategy_name(display_name):
                        # Remove star symbol if present
                        return display_name.split(" ⭐")[0]
                        
                    # Get the base strategy name without stars
                    base_strategy_type = get_strategy_name(strategy_type)
                    
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
                            0.1, 0.99, 0.8,
                            help="Statistical confidence level for sampling"
                        )
                    
                    elif base_strategy_type == "Coverage Optimization":
                        balance = st.slider(
                            "Coverage Balance",
                            0.0, 1.0, 0.5,
                            help="Balance between full coverage and frequency-based optimization"
                        )
                    
                    elif base_strategy_type == "Bayesian Inference":
                        recent_draws_count = st.slider(
                            "Recent Draws to Consider",
                            5, 100, 20,
                            help="Number of recent draws to use for Bayesian prior"
                        )
                        
                        prior_strength = st.slider(
                            "Prior Strength",
                            0.1, 5.0, 1.0, 0.1,
                            help="Weight given to prior beliefs vs. observed data"
                        )
                    
                    elif base_strategy_type == "Risk/Reward Balance":
                        risk_level = st.slider(
                            "Risk Level",
                            0.0, 1.0, 0.5,
                            help="Higher values favor riskier combinations with potentially higher rewards"
                        )
                    
                    elif base_strategy_type == "Markov Chain Model":
                        balanced = st.slider(
                            "Balance Factor",
                            0.0, 1.0, 0.5,
                            help="Balance between pure Markov predictions and frequency analysis"
                        )
                    
                    elif base_strategy_type == "Time Series Analysis":
                        lag = st.slider(
                            "Lag Parameter",
                            1, 10, 3,
                            help="Number of previous draws to consider for time series analysis"
                        )
                    
                    elif base_strategy_type == "Anti-Cognitive Bias":
                        window_size = st.slider(
                            "Analysis Window",
                            5, 100, 20,
                            help="Number of past draws to analyze for cognitive biases"
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
                                
                                # Display combinations
                                st.subheader("Generated Combinations")
                                
                                for i, combo in enumerate(combinations):
                                    st.write(f"**Combination {i+1}:**")
                                    
                                    col1, col2, col3 = st.columns([3, 2, 3])
                                    
                                    with col1:
                                        if 'numbers' in combo:
                                            st.write(f"Main Numbers: {', '.join(map(str, combo['numbers']))}")
                                        elif 'main_numbers' in combo:
                                            st.write(f"Main Numbers: {', '.join(map(str, combo['main_numbers']))}")
                                    
                                    with col2:
                                        if 'lucky' in combo:
                                            st.write(f"Lucky Number: {combo['lucky']}")
                                        elif 'lucky_number' in combo:
                                            st.write(f"Lucky Number: {combo['lucky_number']}")
                                    
                                    with col3:
                                        if 'score' in combo:
                                            st.write(f"Score: {combo['score']:.2f}/100")
                                
                                # Save combinations to database
                                save_option = st.radio(
                                    "Would you like to save these combinations?",
                                    ["Yes", "No"],
                                    horizontal=True
                                )
                                
                                if save_option == "Yes":
                                    save_name = st.text_input("Enter a name for this set of combinations:")
                                    
                                    if save_name and st.button("Save Combinations"):
                                        conn = get_db_connection()
                                        if conn:
                                            try:
                                                # Convert combinations to JSON
                                                combos_json = json.dumps({
                                                    'strategy': strategy_type,
                                                    'timestamp': datetime.now().isoformat(),
                                                    'combinations': combinations
                                                })
                                                
                                                # Save to database
                                                cur = conn.cursor()
                                                cur.execute(
                                                    "INSERT INTO saved_combinations (name, lottery_type, combinations) VALUES (%s, %s, %s)",
                                                    (save_name, "French Loto", combos_json)
                                                )
                                                conn.commit()
                                                conn.close()
                                                
                                                st.success(f"Successfully saved {len(combinations)} combinations as '{save_name}'")
                                            except Exception as e:
                                                st.error(f"Error saving combinations: {str(e)}")
                                        else:
                                            st.error("Could not connect to database.")
                            
                            except Exception as e:
                                st.error(f"Error generating combinations: {str(e)}")

# Additional tabs and code continue here...

if __name__ == "__main__":
    main()