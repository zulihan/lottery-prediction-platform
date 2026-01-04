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
from src.core.database import init_db, get_db_connection
import logging

# Import strategy and analysis tools
try:
    from src.core.strategies import PredictionStrategies
    from src.core.french_loto_strategy import FrenchLotoStrategy
    from src.core.french_loto_statistics import FrenchLotoStatistics
    from src.utils.combination_analysis import analyze_full_combinations, analyze_number_combinations
    from src.utils.strategy_recommendation import get_ordered_strategy_list, get_strategy_info_text, get_base_strategy_name
    from src.core.fibonacci_strategy import generate_fibonacci_combinations, get_fibonacci_strategy_info, save_fibonacci_to_database

    # NEW: Import ensemble strategies and analysis tools
    from src.core.ensemble import EnsembleStrategies
    from src.utils.evaluation import FailureAnalyzer
    from src.utils.visualizations import (
        plot_number_pairs_heatmap,
        plot_number_frequency_chart,
        plot_hot_cold_numbers,
        plot_range_distribution,
        plot_star_frequency,
        plot_trend_over_time,
        create_all_visualizations
    )
except ImportError as e:
    logging.warning(f"Strategy modules not found. Some features may be unavailable. Error: {str(e)}")
    # Define fallback functions
    def get_strategy_info_text():
        return "Strategy information not available."
    def get_ordered_strategy_list():
        return []
    def get_base_strategy_name(strategy):
        return strategy
    # Define fallback for combination analysis
    def analyze_number_combinations(size=3):
        return {"error": "Combination analysis not available"}
    def analyze_full_combinations():
        return {"error": "Combination analysis not available"}
    # Define fallback for new modules
    EnsembleStrategies = None
    FailureAnalyzer = None

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
        
        # Update Euromillions from FDJ API
        st.subheader("Update from FDJ API")
        update_euromillions_button = st.button("🔄 Update Euromillions", help="Download latest drawings from FDJ API")
        
        if update_euromillions_button:
            with st.spinner("Updating Euromillions from FDJ API..."):
                try:
                    from update_latest_draws import update_euromillions
                    count = update_euromillions()
                    if count > 0:
                        st.success(f"✅ {count} new Euromillions drawings imported!")
                        # Reload data
                        conn = get_db_connection()
                        if conn:
                            query = "SELECT * FROM euromillions_drawings ORDER BY date DESC"
                            data = pd.read_sql(query, conn)
                            st.session_state.processed_data = data
                            st.session_state.data_loaded = True
                    else:
                        st.info("No new Euromillions drawings found (all already imported)")
                except Exception as e:
                    st.error(f"Error updating Euromillions: {str(e)}")
        
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
            
        # Update French Loto from FDJ API
            if st.session_state.french_loto_data_loaded:
                st.success(f"✅ {len(st.session_state.french_loto_data)} French Loto drawings loaded")
        
        update_french_loto_button = st.button("🔄 Update French Loto", help="Download latest drawings from FDJ API")
        
        if update_french_loto_button:
            with st.spinner("Updating French Loto from FDJ API..."):
                try:
                    from update_latest_draws import update_french_loto
                    count = update_french_loto()
                    if count > 0:
                        st.success(f"✅ {count} new French Loto drawings imported!")
                        # Reload data
                        conn = get_db_connection()
                        if conn:
                            query = "SELECT * FROM french_loto_drawings ORDER BY date DESC"
                            data = pd.read_sql(query, conn)
                            st.session_state.french_loto_data = data
                            st.session_state.french_loto_data_loaded = True
                    else:
                        st.info("No new French Loto drawings found (all already imported)")
                except Exception as e:
                    st.error(f"Error updating French Loto: {str(e)}")
    
    # Create tabs for different application functionalities
    tabs = st.tabs([
        "Data Overview",
        "Statistics",
        "Strategy Generation",
        "Results Analysis",
        "Visualizations",
        "Failure Analysis",  # NEW
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
                    # Pass the data to the analysis function
                    if 'analyze_number_combinations' in globals():
                        combination_analysis = analyze_number_combinations(
                            data=st.session_state.processed_data,
                            size=combination_size
                        )
                        
                        if combination_analysis and 'most_frequent_combinations' in combination_analysis:
                            st.write(f"Most Frequent {combination_size}-Number Combinations:")
                            for combo, freq in combination_analysis['most_frequent_combinations']:
                                st.write(f"Numbers {combo}: {freq} occurrences")
                        elif combination_analysis and 'error' in combination_analysis:
                            st.warning(combination_analysis['error'])
                    else:
                        st.warning("Combination analysis function not available")
                except Exception as e:
                    st.error(f"Error in combination analysis: {str(e)}")
        
        else:  # French Loto
            if not st.session_state.french_loto_data_loaded:
                st.warning("Please load French Loto data from the sidebar first.")
            else:
                try:
                    # Initialize the FrenchLotoStatistics module
                    try:
                        # Import here to ensure it's available even if global import failed
                        from src.core.french_loto_statistics import FrenchLotoStatistics
                        stats = FrenchLotoStatistics(st.session_state.french_loto_data)
                    except Exception as e:
                        st.error(f"Error initializing statistics module: {str(e)}")
                        import traceback
                        st.error(f"Traceback: {traceback.format_exc()}")
                        stats = None
                    
                    if stats:
                        # Get hot and cold numbers (returns a dict)
                        hot_cold = stats.get_hot_cold_numbers()
                        hot_numbers = hot_cold.get('hot_numbers', [])
                        cold_numbers = hot_cold.get('cold_numbers', [])
                        hot_lucky = hot_cold.get('hot_lucky', [])
                        cold_lucky = hot_cold.get('cold_lucky', [])
                        
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
                    from src.core.statistics import EuromillionsStatistics
                    euro_stats = EuromillionsStatistics(st.session_state.processed_data)
                    strategies = PredictionStrategies(euro_stats)

                    # Initialize ensemble strategies
                    ensemble_strategies = EnsembleStrategies(
                        base_strategies=strategies,
                        historical_data=st.session_state.processed_data
                    )
                except Exception as e:
                    st.error(f"Error initializing prediction strategies: {str(e)}")
                    strategies = None
                    ensemble_strategies = None
                
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
                            "Fibonacci-Filtered Hybrid ⭐⭐",
                            "Strategic Fusion Ensemble ⭐⭐",
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

                    elif base_strategy_type == "Fibonacci-Filtered Hybrid":
                        num_per_strategy = st.slider(
                            "Candidates per Strategy",
                            4, 12, 8,
                            help="Number of candidates to generate from each base strategy before filtering"
                        )

                    elif base_strategy_type == "Strategic Fusion Ensemble":
                        fusion_types = st.multiselect(
                            "Fusion Types",
                            ["cross_strategy", "averaging", "frequency_weighted"],
                            default=["cross_strategy", "averaging"],
                            help="Select which fusion methods to use"
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

                                elif base_strategy_type == "Fibonacci-Filtered Hybrid":
                                    if ensemble_strategies:
                                        combinations = ensemble_strategies.fibonacci_filtered_hybrid_strategy(
                                            num_combinations=num_combinations,
                                            num_per_strategy=num_per_strategy
                                        )
                                    else:
                                        st.error("Ensemble strategies not available")
                                        combinations = []

                                elif base_strategy_type == "Strategic Fusion Ensemble":
                                    if ensemble_strategies:
                                        # Use fusion_types from multiselect, or default if empty
                                        selected_fusion = fusion_types if fusion_types else ["cross_strategy", "averaging"]
                                        combinations = ensemble_strategies.strategic_fusion_ensemble(
                                            num_combinations=num_combinations,
                                            fusion_types=selected_fusion
                                        )
                                    else:
                                        st.error("Ensemble strategies not available")
                                        combinations = []

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
                                                    from src.core.database import GeneratedCombination, get_session
                                                    
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
                # Initialize strategies
                try:
                    # Create a statistics class for French Loto data
                    from src.core.french_loto_statistics import FrenchLotoStatistics
                    loto_stats = FrenchLotoStatistics(st.session_state.french_loto_data)
                    strategies = FrenchLotoStrategy(loto_stats)
                except Exception as e:
                    st.error(f"Error initializing French Loto strategies: {str(e)}")
                    strategies = None
                
                if strategies:
                    # Intelligent Recommendations Section
                    st.subheader("🎯 Intelligent Strategy Recommendations")
                    
                    # Display performance analysis
                    with st.expander("📊 Strategy Performance Analysis", expanded=True):
                        st.markdown("""
                        **Based on comprehensive backtesting against historical data (30% test set, 20 combinations per strategy):**
                        
                        **Best Performing Strategies:**
                        - 🥇 **Risk/Reward Strategy**: 2.16/6 avg score, 22.69% win rate
                        - 🥈 **Frequency Analysis**: 2.15/6 avg score, 21.45% win rate
                        - 🥉 **Markov Chain Model**: 2.14/6 avg score, 23.26% win rate
                        - ⭐ **Time Series Analysis**: 2.14/6 avg score, 22.12% win rate
                        
                        **Recommendations:**
                        - ✅ **Risk/Reward Balance** is optimal for maximizing both your match rate and potential payouts
                        - ✅ **Markov Chain Model** gives the highest win percentage but slightly lower average matches
                        - ✅ For consistent performance, consider a **blend of the top three strategies**
                        
                        *Analysis Details: Backtesting conducted across 1,049 test drawings from historical data. Win rate refers to matches of 3 or more numbers (threshold for winning a prize).*
                        """)
                    
                    # Quick Generate Section
                    st.subheader("🚀 Quick Generate Optimal Combinations")
                    
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        num_combos = st.number_input("Number of combinations", min_value=1, max_value=10, value=2, key="loto_quick_num")
                    
                    with col2:
                        strategy_choice = st.selectbox(
                            "Recommended Strategy",
                            [
                                "Risk/Reward Balance ⭐ (Best Overall)",
                                "Markov Chain Model ⭐ (Highest Win Rate)",
                                "Frequency Analysis ⭐ (Consistent)",
                                "Time Series Analysis ⭐ (Balanced)",
                                "Mixed Strategy (Blend of Top 3)"
                            ],
                            key="loto_quick_strategy"
                        )
                    
                    with col3:
                        st.write("")  # Spacing
                        st.write("")  # Spacing
                        quick_generate = st.button("✨ Generate", type="primary", key="loto_quick_generate")
                    
                    if quick_generate:
                        with st.spinner(f"Generating {num_combos} optimal combinations using {strategy_choice}..."):
                            try:
                                # Extract base strategy name
                                if "Risk/Reward" in strategy_choice:
                                    base_strategy = "Risk/Reward Balance"
                                    risk_level = 0.5  # Balanced risk
                                    combinations = strategies.risk_reward_strategy(
                                        num_combinations=num_combos,
                                        risk_level=risk_level
                                    )
                                elif "Markov" in strategy_choice:
                                    base_strategy = "Markov Chain Model"
                                    lag = 3
                                    combinations = strategies.markov_strategy(
                                        num_combinations=num_combos,
                                        lag=lag
                                    )
                                elif "Frequency" in strategy_choice:
                                    base_strategy = "Frequency Analysis"
                                    recency_weight = 0.3
                                    combinations = strategies.frequency_strategy(
                                        num_combinations=num_combos,
                                        recent_weight=recency_weight
                                    )
                                elif "Time Series" in strategy_choice:
                                    base_strategy = "Time Series Analysis"
                                    window_size = 10
                                    combinations = strategies.time_series_strategy(
                                        num_combinations=num_combos,
                                        window_size=window_size
                                    )
                                else:  # Mixed Strategy
                                    base_strategy = "Mixed Strategy"
                                    combinations = strategies.mixed_strategy(
                                        num_combinations=num_combos
                                    )
                                
                                if combinations:
                                    st.success(f"✅ Generated {len(combinations)} optimal combinations using {base_strategy}!")
                                    st.subheader("🎲 Your Optimal Combinations")
                                    
                                    for i, combo in enumerate(combinations):
                                        with st.container():
                                            col1, col2, col3 = st.columns([3, 2, 1])
                                            
                                            with col1:
                                                st.markdown(f"### Combination {i+1}")
                                                if 'main_numbers' in combo:
                                                    numbers_str = ", ".join([str(n) for n in combo['main_numbers']])
                                                    st.markdown(f"**Numbers:** {numbers_str}")
                                                    st.markdown(f"**Lucky Number:** {combo.get('lucky_number', 'N/A')}")
                                                else:
                                                    numbers_str = ", ".join([str(n) for n in combo.get('numbers', [])])
                                                    stars_str = ", ".join([str(s) for s in combo.get('stars', [])])
                                                    st.markdown(f"**Numbers:** {numbers_str}")
                                                    st.markdown(f"**Stars:** {stars_str}")
                                            
                                            with col2:
                                                if 'score' in combo:
                                                    st.metric("Score", f"{combo['score']:.2f}")
                                                if 'strategy' in combo:
                                                    st.caption(f"Strategy: {combo['strategy']}")
                                            
                                            with col3:
                                                # Save to database button
                                                if st.button(f"💾 Save", key=f"loto_quick_save_{i}"):
                                                    try:
                                                        from src.core.database import FrenchLotoPrediction, get_session
                                                        from datetime import date
                                                        
                                                        if 'main_numbers' in combo:
                                                            numbers_list = combo['main_numbers']
                                                            lucky = combo.get('lucky_number', None)
                                                        else:
                                                            numbers_list = combo.get('numbers', [])
                                                            lucky = combo.get('lucky', None)
                                                        
                                                        numbers_str = "-".join([str(n) for n in numbers_list])
                                                        
                                                        new_combo = FrenchLotoPrediction(
                                                            date_generated=date.today(),
                                                            numbers=numbers_str,
                                                            lucky=lucky,
                                                            strategy=base_strategy,
                                                            score=combo.get('score', 0.0)
                                                        )
                                                        
                                                        session = get_session()
                                                        session.add(new_combo)
                                                        session.commit()
                                                        session.close()
                                                        
                                                        st.success(f"✅ Combination {i+1} saved!")
                                                    except Exception as e:
                                                        st.error(f"Error saving: {str(e)}")
                                            
                                            st.divider()
                                
                                # Store combinations in session state for mixing (append, don't replace)
                                if 'loto_generated_combinations' not in st.session_state:
                                    st.session_state.loto_generated_combinations = []
                                # Add new combinations to existing ones
                                st.session_state.loto_generated_combinations.extend(combinations)
                                st.info(f"💾 {len(combinations)} combination(s) added to mixing pool (Total: {len(st.session_state.loto_generated_combinations)})")
                                
                            except Exception as e:
                                st.error(f"Error generating combinations: {str(e)}")
                                import traceback
                                st.error(f"Traceback: {traceback.format_exc()}")
                    
                    # Mix Combinations Section
                    st.divider()
                    st.subheader("🔀 Mix Combinations for Maximum Score")
                    st.markdown("Combine multiple combinations to create an optimal new combination with the highest possible score.")
                    
                    # Initialize session state if needed
                    if 'loto_generated_combinations' not in st.session_state:
                        st.session_state.loto_generated_combinations = []
                    
                    # Always get fresh reference to session state
                    available_combos = st.session_state.loto_generated_combinations.copy() if st.session_state.loto_generated_combinations else []
                    
                    # Management buttons
                    col_reset, col_add_manual, col_count = st.columns([1, 1, 2])
                    
                    with col_reset:
                        if st.button("🗑️ Reset All", key="loto_reset_combos", help="Clear all combinations from mixing pool"):
                            st.session_state.loto_generated_combinations = []
                            st.rerun()
                    
                    with col_add_manual:
                        # Use session state to keep form open
                        if 'loto_show_manual_form' not in st.session_state:
                            st.session_state.loto_show_manual_form = False
                        
                        if st.button("➕ Add Manual Combination", key="loto_show_manual", help="Add a combination manually"):
                            st.session_state.loto_show_manual_form = not st.session_state.loto_show_manual_form
                            st.rerun()
                    
                    with col_count:
                        # Get fresh count
                        current_count = len(st.session_state.loto_generated_combinations)
                        st.caption(f"**Total combinations in pool:** {current_count}")
                    
                    # Manual combination input form
                    if st.session_state.loto_show_manual_form:
                        with st.expander("➕ Add Manual Combination", expanded=True):
                            with st.form(key="loto_manual_combo_form"):
                                st.markdown("Enter a combination manually:")
                                
                                col1, col2, col3, col4, col5 = st.columns(5)
                                with col1:
                                    n1 = st.number_input("Number 1", min_value=1, max_value=49, value=1, key="manual_n1")
                                with col2:
                                    n2 = st.number_input("Number 2", min_value=1, max_value=49, value=2, key="manual_n2")
                                with col3:
                                    n3 = st.number_input("Number 3", min_value=1, max_value=49, value=3, key="manual_n3")
                                with col4:
                                    n4 = st.number_input("Number 4", min_value=1, max_value=49, value=4, key="manual_n4")
                                with col5:
                                    n5 = st.number_input("Number 5", min_value=1, max_value=49, value=5, key="manual_n5")
                                
                                lucky = st.number_input("Lucky Number", min_value=1, max_value=10, value=1, key="manual_lucky")
                                
                                manual_score = st.slider("Score (optional)", min_value=0.0, max_value=100.0, value=75.0, key="manual_score")
                                
                                manual_strategy = st.text_input("Strategy Name (optional)", value="Manual Entry", key="manual_strategy")
                                
                                col_submit, col_close = st.columns([1, 1])
                                with col_submit:
                                    submit_manual = st.form_submit_button("✅ Add to Pool", type="primary")
                                with col_close:
                                    if st.form_submit_button("❌ Close"):
                                        st.session_state.loto_show_manual_form = False
                                        st.rerun()
                                
                                if submit_manual:
                                    # Validate numbers are unique
                                    numbers = [int(n1), int(n2), int(n3), int(n4), int(n5)]
                                    if len(set(numbers)) != 5:
                                        st.error("❌ All 5 numbers must be unique!")
                                    else:
                                        manual_combo = {
                                            'main_numbers': sorted(numbers),
                                            'lucky_number': int(lucky),
                                            'score': float(manual_score),
                                            'strategy': manual_strategy,
                                            'date_generated': datetime.now().strftime('%Y-%m-%d')
                                        }
                                        st.session_state.loto_generated_combinations.append(manual_combo)
                                        st.success(f"✅ Added manual combination: {sorted(numbers)} (Lucky: {lucky})")
                                        # Keep form open for adding more
                                        st.rerun()
                    
                    # Always show available combinations (even if less than 2)
                    current_combos = st.session_state.loto_generated_combinations
                    if len(current_combos) > 0:
                        # Display available combinations
                        st.markdown("**Available Combinations to Mix:**")
                        
                        # Create checkboxes for selection with delete option
                        selected_indices = []
                        
                        # Group combinations in rows of 3
                        for row_start in range(0, len(current_combos), 3):
                            cols = st.columns(3)
                            row_combos = current_combos[row_start:row_start+3]
                            
                            for col_idx, (i, combo) in enumerate(zip(range(row_start, row_start+len(row_combos)), row_combos)):
                                with cols[col_idx]:
                                    if 'main_numbers' in combo:
                                        numbers_str = ", ".join([str(n) for n in combo['main_numbers']])
                                        lucky_str = str(combo.get('lucky_number', 'N/A'))
                                        score = combo.get('score', 0)
                                        strategy = combo.get('strategy', 'Unknown')
                                    else:
                                        numbers_str = ", ".join([str(n) for n in combo.get('numbers', [])])
                                        lucky_str = "N/A"
                                        score = combo.get('score', 0)
                                        strategy = combo.get('strategy', 'Unknown')
                                    
                                    # Container for each combo
                                    with st.container():
                                        # Checkbox for selection
                                        if st.checkbox(
                                            f"Combo {i+1}",
                                            key=f"loto_mix_select_{i}",
                                            value=(i < 2 and row_start == 0)  # Pre-select first 2
                                        ):
                                            selected_indices.append(i)
                                        
                                        # Display combo info
                                        st.markdown(f"**Score:** {score:.1f}")
                                        st.caption(f"Numbers: {numbers_str}")
                                        st.caption(f"Lucky: {lucky_str}")
                                        st.caption(f"Strategy: {strategy}")
                                        
                                        # Delete button
                                        if st.button("🗑️", key=f"loto_delete_{i}", help="Remove this combination"):
                                            if i < len(st.session_state.loto_generated_combinations):
                                                st.session_state.loto_generated_combinations.pop(i)
                                                st.rerun()
                                        
                                        st.divider()
                        
                        # Show mix button if at least 2 combinations are selected
                        if len(selected_indices) >= 2:
                            mix_button = st.button("✨ Mix Selected Combinations", type="primary", key="loto_mix_button")
                            
                            if mix_button:
                                with st.spinner("Mixing combinations to find optimal solution..."):
                                    try:
                                        selected_combos = [current_combos[i] for i in selected_indices if i < len(current_combos)]
                                        mixed_combo = strategies.mix_combinations(selected_combos, max_iterations=200)
                                        
                                        if mixed_combo:
                                            st.success(f"✅ Created optimal mixed combination with score {mixed_combo.get('score', 0):.2f}!")
                                            st.subheader("🎯 Your Optimized Mixed Combination")
                                            
                                            col1, col2, col3 = st.columns([3, 2, 1])
                                            
                                            with col1:
                                                st.markdown("### 🏆 Best Mixed Combination")
                                                numbers_str = ", ".join([str(n) for n in mixed_combo['main_numbers']])
                                                st.markdown(f"**Numbers:** {numbers_str}")
                                                st.markdown(f"**Lucky Number:** {mixed_combo.get('lucky_number', 'N/A')}")
                                                st.caption(f"Mixed from {len(selected_indices)} combinations")
                                            
                                            with col2:
                                                st.metric("Optimized Score", f"{mixed_combo.get('score', 0):.2f}")
                                                st.caption("Based on frequency, hot/cold analysis, and balance")
                                            
                                            with col3:
                                                if st.button("💾 Save Mixed", key="loto_save_mixed", type="primary"):
                                                    try:
                                                        from src.core.database import FrenchLotoPrediction, get_session
                                                        from datetime import date
                                                        
                                                        numbers_str = "-".join([str(n) for n in mixed_combo['main_numbers']])
                                                        
                                                        new_combo = FrenchLotoPrediction(
                                                            date_generated=date.today(),
                                                            numbers=numbers_str,
                                                            lucky=mixed_combo.get('lucky_number'),
                                                            strategy=f"Mixed from {len(selected_indices)} combos",
                                                            score=mixed_combo.get('score', 0.0)
                                                        )
                                                        
                                                        session = get_session()
                                                        session.add(new_combo)
                                                        session.commit()
                                                        session.close()
                                                        
                                                        st.success("✅ Mixed combination saved!")
                                                    except Exception as e:
                                                        st.error(f"Error saving: {str(e)}")
                                            
                                            # Show what was mixed
                                            with st.expander("📊 Mixing Details"):
                                                st.write(f"**Combined {len(selected_indices)} combinations:**")
                                                for idx in selected_indices:
                                                    if idx < len(current_combos):
                                                        combo = current_combos[idx]
                                                    if 'main_numbers' in combo:
                                                        nums = ", ".join([str(n) for n in combo['main_numbers']])
                                                        st.write(f"- Combo {idx+1}: {nums} (Score: {combo.get('score', 0):.1f})")
                                                
                                                st.write(f"\n**Optimization factors considered:**")
                                                st.write("- Frequency of numbers across input combinations")
                                                st.write("- Original scores of source combinations")
                                                st.write("- Hot/cold number analysis")
                                                st.write("- Historical frequency patterns")
                                                st.write("- Even/odd balance")
                                                st.write("- Range distribution")
                                                st.write("- Sum optimization")
                                        
                                    except Exception as e:
                                        st.error(f"Error mixing combinations: {str(e)}")
                                        import traceback
                                        st.error(f"Traceback: {traceback.format_exc()}")
                        else:
                            if len(current_combos) < 2:
                                st.warning(f"⚠️ You need at least 2 combinations to mix. Currently have {len(current_combos)}. Add more combinations above.")
                            else:
                                st.info(f"👆 Select at least 2 combinations to mix (currently selected: {len(selected_indices)})")
                    else:
                        st.info("👆 Generate some combinations first, or add them manually using the 'Add Manual Combination' button above.")
                    
                    st.divider()
                    
                    # Advanced Strategy Options
                    st.subheader("⚙️ Advanced Strategy Parameters")
                    
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
                    
                    elif base_strategy_type == "Risk/Reward Balance":
                        risk_level = st.slider(
                            "Risk Level",
                            0.0, 1.0, 0.5,
                            help="Higher values favor high-risk, high-reward combinations"
                        )
                    
                    elif base_strategy_type == "Markov Chain Model":
                        lag = st.slider(
                            "Lag Parameter",
                            1, 10, 3,
                            help="Lag for Markov chain transitions"
                        )
                    
                    elif base_strategy_type == "Time Series Analysis":
                        window_size = st.slider(
                            "Window Size",
                            5, 30, 10,
                            help="Window size for time series analysis"
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
                                        recent_weight=recency_weight
                                    )
                                
                                elif base_strategy_type == "Temporal Patterns":
                                    combinations = strategies.temporal_strategy(
                                        num_combinations=num_combinations,
                                        lookback_period=pattern_depth * 10
                                    )
                                
                                elif base_strategy_type == "Stratified Sampling":
                                    combinations = strategies.stratified_sampling_strategy(
                                        num_combinations=num_combinations,
                                        balance_factor=confidence
                                    )
                                
                                elif base_strategy_type == "Coverage Optimization":
                                    combinations = strategies.coverage_strategy(
                                        num_combinations=num_combinations,
                                        balanced=(balance > 0.5)
                                    )
                                
                                elif base_strategy_type == "Bayesian Inference":
                                    combinations = strategies.bayesian_strategy(
                                        num_combinations=num_combinations,
                                        recent_draws_count=recent_draws_count
                                    )
                                
                                elif base_strategy_type == "Risk/Reward Balance":
                                    combinations = strategies.risk_reward_strategy(
                                        num_combinations=num_combinations,
                                        risk_level=risk_level
                                    )
                                
                                elif base_strategy_type == "Markov Chain Model":
                                    combinations = strategies.markov_strategy(
                                        num_combinations=num_combinations,
                                        lag=lag
                                    )
                                
                                elif base_strategy_type == "Time Series Analysis":
                                    combinations = strategies.time_series_strategy(
                                        num_combinations=num_combinations,
                                        window_size=window_size
                                    )
                                
                                elif base_strategy_type == "Anti-Cognitive Bias":
                                    combinations = strategies.cognitive_bias_strategy(
                                        num_combinations=num_combinations
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
                                            # French Loto uses 'main_numbers' and 'lucky_number', Euromillions uses 'numbers' and 'stars'
                                            if 'main_numbers' in combo:
                                                # French Loto format
                                                numbers_str = ", ".join([str(n) for n in combo['main_numbers']])
                                                st.write(f"Numbers: {numbers_str}")
                                                st.write(f"Lucky Number: {combo.get('lucky_number', 'N/A')}")
                                            else:
                                                # Euromillions format
                                                numbers_str = ", ".join([str(n) for n in combo.get('numbers', [])])
                                                stars_str = ", ".join([str(s) for s in combo.get('stars', [])])
                                                st.write(f"Numbers: {numbers_str}")
                                                st.write(f"Stars: {stars_str}")
                                        
                                        with col2:
                                            if 'score' in combo:
                                                st.write(f"Score: {combo['score']:.2f}")
                                            if 'rationale' in combo:
                                                st.write(f"Rationale: {combo['rationale']}")
                                        
                                        with col3:
                                            # Save to database button
                                            if st.button(f"Save #{i+1}", key=f"save_loto_combo_{i}"):
                                                try:
                                                    from src.core.database import FrenchLotoPrediction, get_session
                                                    
                                                    # Format numbers as dash-separated string
                                                    # French Loto uses 'main_numbers', Euromillions uses 'numbers'
                                                    if 'main_numbers' in combo:
                                                        numbers_list = combo['main_numbers']
                                                        lucky = combo.get('lucky_number', None)
                                                    else:
                                                        numbers_list = combo.get('numbers', [])
                                                        lucky = combo.get('lucky', None)
                                                    
                                                    numbers_str = "-".join([str(n) for n in numbers_list])
                                                    
                                                    # Create new prediction record
                                                    new_combo = FrenchLotoPrediction(
                                                        date_generated=date.today(),
                                                        numbers=numbers_str,
                                                        lucky=lucky,
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
        st.header("📊 Results Analysis")
        st.markdown("Compare your saved predictions against actual draw results and analyze performance.")
        
        # Lottery type selection
        lottery_type = st.radio(
            "Select Lottery Type",
            ["French Loto", "Euromillions"],
            horizontal=True,
            key="results_lottery_type"
        )
        
        if lottery_type == "French Loto":
            st.subheader("French Loto Results Analysis")
            
            # Get latest drawing date
            conn = get_db_connection()
            if conn:
                try:
                    latest_drawing_query = "SELECT MAX(date) as latest_date FROM french_loto_drawings"
                    latest_drawing = pd.read_sql(latest_drawing_query, conn)
                    latest_date = latest_drawing['latest_date'].iloc[0] if not latest_drawing.empty and latest_drawing['latest_date'].iloc[0] else None
                    
                    if latest_date:
                        st.info(f"📅 Latest draw in database: {latest_date}")
                    else:
                        st.warning("⚠️ No drawings found in database. Add a drawing first.")
                except Exception as e:
                    st.error(f"Error checking latest drawing: {str(e)}")
                    latest_date = None
            else:
                latest_date = None
                st.error("Could not connect to database.")
            
            # Section 1: Add/Update Draw Result
            st.subheader("1️⃣ Add or Update Draw Result")
            with st.expander("➕ Add New Draw Result", expanded=False):
                with st.form(key="add_draw_result_form"):
                    draw_date = st.date_input("Draw Date", value=datetime.now().date(), key="result_draw_date")
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        n1 = st.number_input("Number 1", min_value=1, max_value=49, value=1, key="result_n1")
                    with col2:
                        n2 = st.number_input("Number 2", min_value=1, max_value=49, value=2, key="result_n2")
                    with col3:
                        n3 = st.number_input("Number 3", min_value=1, max_value=49, value=3, key="result_n3")
                    with col4:
                        n4 = st.number_input("Number 4", min_value=1, max_value=49, value=4, key="result_n4")
                    with col5:
                        n5 = st.number_input("Number 5", min_value=1, max_value=49, value=5, key="result_n5")
                    
                    lucky = st.number_input("Lucky Number", min_value=1, max_value=10, value=1, key="result_lucky")
                    
                    submit_draw = st.form_submit_button("✅ Add Draw Result", type="primary")
                    
                    if submit_draw:
                        # Validate numbers are unique
                        numbers = [int(n1), int(n2), int(n3), int(n4), int(n5)]
                        if len(set(numbers)) != 5:
                            st.error("❌ All 5 numbers must be unique!")
                        else:
                            try:
                                from src.core.database import add_french_loto_drawing_with_details
                                success = add_french_loto_drawing_with_details(
                                    date=draw_date,
                                    numbers=sorted(numbers),
                                    lucky=int(lucky),
                                    draw_num=1
                                )
                                if success:
                                    st.success(f"✅ Draw result added for {draw_date}!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to add draw result. It may already exist.")
                            except Exception as e:
                                st.error(f"Error adding draw: {str(e)}")
            
            # Section 2: Analyze Predictions vs Results
            st.subheader("2️⃣ Analyze Predictions Against Latest Draw")
            
            if latest_date:
                # Get latest drawing
                try:
                    latest_draw_query = f"""
                        SELECT date, n1, n2, n3, n4, n5, lucky 
                        FROM french_loto_drawings 
                        WHERE date = '{latest_date}'
                        ORDER BY draw_num DESC
                        LIMIT 1
                    """
                    latest_draw_df = pd.read_sql(latest_draw_query, conn)
                    
                    if not latest_draw_df.empty:
                        draw = latest_draw_df.iloc[0]
                        actual_numbers = sorted([int(draw['n1']), int(draw['n2']), int(draw['n3']), int(draw['n4']), int(draw['n5'])])
                        actual_lucky = int(draw['lucky'])
                        
                        st.markdown(f"**Latest Draw: {draw['date']}**")
                        st.markdown(f"**Numbers:** {', '.join(map(str, actual_numbers))}")
                        st.markdown(f"**Lucky Number:** {actual_lucky}")
                        
                        # Get predictions for this date or before
                        predictions_query = f"""
                            SELECT id, date_generated, numbers, lucky, strategy, score
                            FROM french_loto_predictions
                            WHERE date_generated <= '{latest_date}'
                            ORDER BY date_generated DESC, score DESC
                            LIMIT 50
                        """
                        predictions_df = pd.read_sql(predictions_query, conn)
                        
                        if not predictions_df.empty:
                            st.markdown(f"**Found {len(predictions_df)} predictions to analyze**")
                            
                            # Analyze each prediction
                            results = []
                            for idx, pred in predictions_df.iterrows():
                                pred_numbers = [int(n) for n in pred['numbers'].split('-')]
                                pred_lucky = int(pred['lucky'])
                                
                                # Count matches
                                number_matches = len(set(pred_numbers) & set(actual_numbers))
                                lucky_match = 1 if pred_lucky == actual_lucky else 0
                                
                                # Calculate score (French Loto scoring)
                                if number_matches == 5 and lucky_match == 1:
                                    match_score = 100  # Jackpot
                                    prize_tier = "Rank 1 (Jackpot)"
                                elif number_matches == 5 and lucky_match == 0:
                                    match_score = 20
                                    prize_tier = "Rank 2"
                                elif number_matches == 4 and lucky_match == 1:
                                    match_score = 10
                                    prize_tier = "Rank 3"
                                elif number_matches == 4 and lucky_match == 0:
                                    match_score = 5
                                    prize_tier = "Rank 4"
                                elif number_matches == 3 and lucky_match == 1:
                                    match_score = 3
                                    prize_tier = "Rank 5"
                                elif number_matches == 3 and lucky_match == 0:
                                    match_score = 2
                                    prize_tier = "Rank 6"
                                elif number_matches == 2 and lucky_match == 1:
                                    match_score = 2
                                    prize_tier = "Rank 7"
                                elif number_matches == 2 and lucky_match == 0:
                                    match_score = 1
                                    prize_tier = "Rank 8"
                                elif number_matches == 1 and lucky_match == 1:
                                    match_score = 1
                                    prize_tier = "Rank 9"
                                else:
                                    match_score = 0
                                    prize_tier = "No win"
                                
                                results.append({
                                    'id': pred['id'],
                                    'date_generated': pred['date_generated'],
                                    'predicted_numbers': pred_numbers,
                                    'predicted_lucky': pred_lucky,
                                    'strategy': pred['strategy'],
                                    'prediction_score': pred['score'],
                                    'number_matches': number_matches,
                                    'lucky_match': lucky_match,
                                    'match_score': match_score,
                                    'prize_tier': prize_tier
                                })
                            
                            # Display results
                            results_df = pd.DataFrame(results)
                            
                            # Summary statistics
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Predictions", len(results_df))
                            with col2:
                                winners = len(results_df[results_df['match_score'] > 0])
                                st.metric("Winners", winners, f"{winners/len(results_df)*100:.1f}%")
                            with col3:
                                avg_matches = results_df['number_matches'].mean()
                                st.metric("Avg Number Matches", f"{avg_matches:.2f}")
                            with col4:
                                best_score = results_df['match_score'].max()
                                st.metric("Best Result", best_score)
                            
                            # Strategy performance
                            st.subheader("📈 Strategy Performance")
                            strategy_stats = results_df.groupby('strategy').agg({
                                'match_score': ['mean', 'max', 'count'],
                                'number_matches': 'mean',
                                'lucky_match': 'sum'
                            }).round(2)
                            strategy_stats.columns = ['Avg Score', 'Best Score', 'Count', 'Avg Matches', 'Lucky Hits']
                            strategy_stats = strategy_stats.sort_values('Avg Score', ascending=False)
                            st.dataframe(strategy_stats, use_container_width=True)
                            
                            # Detailed results table
                            st.subheader("📋 Detailed Results")
                            
                            # Filter options
                            col_filter1, col_filter2 = st.columns(2)
                            with col_filter1:
                                min_matches = st.slider("Minimum number matches", 0, 5, 0, key="min_matches_filter")
                            with col_filter2:
                                show_only_winners = st.checkbox("Show only winners", value=False, key="winners_only")
                            
                            filtered_results = results_df[
                                (results_df['number_matches'] >= min_matches) &
                                ((results_df['match_score'] > 0) if show_only_winners else True)
                            ]
                            
                            # Display filtered results
                            for idx, result in filtered_results.iterrows():
                                with st.container():
                                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                                    
                                    with col1:
                                        pred_nums_str = ", ".join(map(str, result['predicted_numbers']))
                                        st.markdown(f"**Prediction #{result['id']}** ({result['date_generated']})")
                                        st.caption(f"Numbers: {pred_nums_str} | Lucky: {result['predicted_lucky']}")
                                        st.caption(f"Strategy: {result['strategy']} | Predicted Score: {result['prediction_score']:.1f}")
                                    
                                    with col2:
                                        st.markdown(f"**Matches:** {result['number_matches']}/5 numbers")
                                        st.markdown(f"**Lucky:** {'✅' if result['lucky_match'] else '❌'}")
                                    
                                    with col3:
                                        st.metric("Result Score", result['match_score'])
                                        st.caption(result['prize_tier'])
                                    
                                    with col4:
                                        if result['match_score'] >= 10:
                                            st.success("🏆")
                                        elif result['match_score'] > 0:
                                            st.info("🎯")
                                        else:
                                            st.write("")
                                    
                                    st.divider()
                        else:
                            st.info("No predictions found for analysis. Generate and save some predictions first!")
                    else:
                        st.warning("Could not retrieve latest draw from database.")
                except Exception as e:
                    st.error(f"Error analyzing predictions: {str(e)}")
                    import traceback
                    st.error(f"Traceback: {traceback.format_exc()}")
            else:
                st.warning("⚠️ No drawings found in database. Add a draw result first to analyze predictions.")
        
        else:  # Euromillions
            st.subheader("Euromillions Results Analysis")
            st.info("Euromillions results analysis will be implemented similarly. Coming soon!")
        
    # Visualizations tab
    with tabs[4]:
        st.header("📊 Interactive Visualizations")

        # Lottery type selection
        viz_lottery_type = st.radio(
            "Select Lottery Type for Visualizations",
            ["Euromillions", "French Loto"],
            key="viz_lottery_type",
            horizontal=True
        )

        if viz_lottery_type == "Euromillions":
            if not st.session_state.data_loaded:
                st.warning("⚠️ Please load Euromillions data from the sidebar first.")
            else:
                try:
                    from src.core.statistics import EuromillionsStatistics

                    # Initialize statistics
                    euro_stats = EuromillionsStatistics(st.session_state.processed_data)

                    # Visualization selection
                    viz_type = st.selectbox(
                        "Select Visualization Type",
                        [
                            "Number Pairs Heatmap",
                            "Number Frequency Chart",
                            "Hot vs Cold Numbers",
                            "Range Distribution",
                            "Star Frequency",
                            "Trends Over Time",
                            "All Visualizations"
                        ]
                    )

                    if viz_type == "Number Pairs Heatmap":
                        st.subheader("Number Pairs Frequency Heatmap")
                        st.markdown("Interactive heatmap showing how often number pairs appear together")
                        with st.spinner("Generating heatmap..."):
                            fig = plot_number_pairs_heatmap(
                                historical_data=st.session_state.processed_data.to_dict('records')
                            )
                            st.plotly_chart(fig, use_container_width=True)

                    elif viz_type == "Number Frequency Chart":
                        st.subheader("Number Frequency Analysis")
                        top_n = st.slider("Show Top N Numbers", 10, 50, 20, key="freq_top_n")
                        chart_type = st.radio("Chart Type", ["bar", "line"], horizontal=True, key="freq_chart_type")

                        number_freq = euro_stats.get_frequency()
                        fig = plot_number_frequency_chart(number_freq, top_n=top_n, chart_type=chart_type)
                        st.plotly_chart(fig, use_container_width=True)

                    elif viz_type == "Hot vs Cold Numbers":
                        st.subheader("Hot vs Cold Numbers Comparison")
                        max_display = st.slider("Numbers to Display per Category", 5, 15, 10, key="hotcold_display")

                        hot_numbers = euro_stats.get_hot_numbers(max_display)
                        cold_numbers = euro_stats.get_cold_numbers(max_display)

                        # Convert to (number, frequency) tuples
                        hot_freq = [(n, euro_stats.get_frequency(n)) for n in hot_numbers]
                        cold_freq = [(n, euro_stats.get_frequency(n)) for n in cold_numbers]

                        fig = plot_hot_cold_numbers(hot_freq, cold_freq, max_display=max_display)
                        st.plotly_chart(fig, use_container_width=True)

                    elif viz_type == "Range Distribution":
                        st.subheader("Number Range Distribution")
                        st.markdown("Distribution of numbers across different ranges (1-10, 11-20, etc.)")

                        range_dist = euro_stats.get_number_range_distribution()
                        fig = plot_range_distribution(range_dist)
                        st.plotly_chart(fig, use_container_width=True)

                    elif viz_type == "Star Frequency":
                        st.subheader("Lucky Star Frequency Distribution")

                        star_freq = euro_stats.get_star_frequency()
                        fig = plot_star_frequency(star_freq)
                        st.plotly_chart(fig, use_container_width=True)

                    elif viz_type == "Trends Over Time":
                        st.subheader("Number Frequency Trends Over Time")

                        trend_option = st.radio(
                            "Track",
                            ["Top 5 Numbers", "Specific Number"],
                            horizontal=True,
                            key="trend_option"
                        )

                        if trend_option == "Specific Number":
                            specific_num = st.number_input(
                                "Enter number to track (1-50)",
                                min_value=1,
                                max_value=50,
                                value=7,
                                key="trend_specific_num"
                            )
                            fig = plot_trend_over_time(
                                st.session_state.processed_data.to_dict('records'),
                                number=specific_num
                            )
                        else:
                            fig = plot_trend_over_time(
                                st.session_state.processed_data.to_dict('records'),
                                number=None
                            )

                        st.plotly_chart(fig, use_container_width=True)

                    elif viz_type == "All Visualizations":
                        st.subheader("Comprehensive Dashboard")
                        st.markdown("Generating all visualizations...")

                        with st.spinner("Generating comprehensive dashboard..."):
                            figures = create_all_visualizations(
                                st.session_state.processed_data.to_dict('records'),
                                euro_stats
                            )

                            # Display each figure
                            if 'pairs_heatmap' in figures:
                                st.plotly_chart(figures['pairs_heatmap'], use_container_width=True)

                            col1, col2 = st.columns(2)
                            with col1:
                                if 'number_frequency' in figures:
                                    st.plotly_chart(figures['number_frequency'], use_container_width=True)
                                if 'range_distribution' in figures:
                                    st.plotly_chart(figures['range_distribution'], use_container_width=True)

                            with col2:
                                if 'hot_cold' in figures:
                                    st.plotly_chart(figures['hot_cold'], use_container_width=True)
                                if 'star_frequency' in figures:
                                    st.plotly_chart(figures['star_frequency'], use_container_width=True)

                            if 'trends' in figures:
                                st.plotly_chart(figures['trends'], use_container_width=True)

                except Exception as e:
                    st.error(f"Error generating visualizations: {str(e)}")
                    import traceback
                    st.error(f"Traceback: {traceback.format_exc()}")

        else:  # French Loto
            if not st.session_state.french_loto_data_loaded:
                st.warning("⚠️ Please load French Loto data from the sidebar first.")
            else:
                st.info("French Loto visualizations coming soon! The visualization framework supports it, just needs implementation.")


    # Failure Analysis tab (NEW)
    with tabs[5]:
        st.header("🔍 Failure Analysis")
        st.markdown("Analyze why your predictions didn't match the winning numbers and get actionable recommendations.")

        if FailureAnalyzer is None:
            st.error("Failure Analysis module not available.")
        else:
            # Lottery type selection
            analysis_lottery_type = st.radio(
                "Select Lottery Type for Analysis",
                ["Euromillions", "French Loto"],
                key="analysis_lottery_type",
                horizontal=True
            )

            st.subheader("📋 Your Predictions")

            # Manual entry of predictions
            num_predictions = st.number_input(
                "Number of combinations to analyze",
                min_value=1,
                max_value=20,
                value=5,
                key="num_predictions_to_analyze"
            )

            predictions = []
            if analysis_lottery_type == "Euromillions":
                st.write("Enter your predicted combinations:")
                for i in range(num_predictions):
                    with st.expander(f"Combination {i+1}"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            numbers = st.multiselect(
                                "Numbers (select 5)",
                                list(range(1, 51)),
                                key=f"pred_numbers_{i}",
                                max_selections=5
                            )
                        with col2:
                            stars = st.multiselect(
                                "Stars (select 2)",
                                list(range(1, 13)),
                                key=f"pred_stars_{i}",
                                max_selections=2
                            )

                        if len(numbers) == 5 and len(stars) == 2:
                            predictions.append({
                                'numbers': sorted(numbers),
                                'stars': sorted(stars)
                            })

                st.subheader("🎯 Actual Winning Numbers")
                col1, col2 = st.columns([3, 1])
                with col1:
                    winning_numbers = st.multiselect(
                        "Winning Numbers (select 5)",
                        list(range(1, 51)),
                        key="winning_numbers_analysis",
                        max_selections=5
                    )
                with col2:
                    winning_stars = st.multiselect(
                        "Winning Stars (select 2)",
                        list(range(1, 13)),
                        key="winning_stars_analysis",
                        max_selections=2
                    )

            else:  # French Loto
                st.write("Enter your predicted combinations:")
                for i in range(num_predictions):
                    with st.expander(f"Combination {i+1}"):
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            numbers = st.multiselect(
                                "Numbers (select 5)",
                                list(range(1, 50)),
                                key=f"pred_loto_numbers_{i}",
                                max_selections=5
                            )
                        with col2:
                            lucky = st.selectbox(
                                "Lucky Number",
                                list(range(1, 11)),
                                key=f"pred_loto_lucky_{i}"
                            )

                        if len(numbers) == 5:
                            predictions.append({
                                'numbers': sorted(numbers),
                                'stars': []  # Not used for Loto but keep structure consistent
                            })

                st.subheader("🎯 Actual Winning Numbers")
                col1, col2 = st.columns([4, 1])
                with col1:
                    winning_numbers = st.multiselect(
                        "Winning Numbers (select 5)",
                        list(range(1, 50)),
                        key="winning_loto_numbers_analysis",
                        max_selections=5
                    )
                with col2:
                    winning_lucky = st.selectbox(
                        "Winning Lucky Number",
                        list(range(1, 11)),
                        key="winning_loto_lucky_analysis"
                    )
                winning_stars = []  # Not used for Loto

            # Analyze button
            if st.button("🔍 Analyze Predictions", type="primary"):
                if len(predictions) > 0 and len(winning_numbers) == 5:
                    with st.spinner("Analyzing predictions..."):
                        try:
                            analyzer = FailureAnalyzer()
                            results = analyzer.analyze_predictions(
                                predictions,
                                winning_numbers,
                                winning_stars if analysis_lottery_type == "Euromillions" else []
                            )

                            # Display results
                            st.success("✅ Analysis Complete!")

                            # Summary metrics
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric(
                                    "Overused Numbers",
                                    len(results['overused_numbers']['numbers'])
                                )
                            with col2:
                                st.metric(
                                    "Missing Numbers",
                                    results['missing_numbers']['count']
                                )
                            with col3:
                                st.metric(
                                    "Missing %",
                                    f"{results['missing_numbers']['percentage']:.0f}%"
                                )
                            with col4:
                                if analysis_lottery_type == "Euromillions":
                                    st.metric(
                                        "Star Hit Rate",
                                        f"{results['star_analysis']['hit_rate']:.0f}%"
                                    )

                            # Detailed Analysis
                            st.subheader("📊 Detailed Analysis")

                            # Overused numbers
                            if results['overused_numbers']['numbers']:
                                with st.expander("⚠️ Overused Numbers"):
                                    st.write("These numbers appeared too many times in your predictions:")
                                    for num, count in sorted(
                                        results['overused_numbers']['numbers'].items(),
                                        key=lambda x: x[1],
                                        reverse=True
                                    ):
                                        won = "✓ WON" if num in winning_numbers else "✗ LOST"
                                        st.write(f"- Number **{num}**: used {count} times - {won}")

                            # Missing numbers
                            if results['missing_numbers']['numbers']:
                                with st.expander("❌ Missing Winning Numbers"):
                                    st.write("These winning numbers were not in any of your predictions:")
                                    missing_nums = ", ".join([f"**{n}**" for n in sorted(results['missing_numbers']['numbers'])])
                                    st.write(missing_nums)

                            # Range distribution
                            with st.expander("📍 Range Distribution Analysis"):
                                st.write("Comparison of number ranges:")
                                range_df = pd.DataFrame({
                                    'Range': list(results['range_analysis']['winning_distribution'].keys()),
                                    'Winning': list(results['range_analysis']['winning_distribution'].values()),
                                    'Your Predictions': list(results['range_analysis']['our_distribution'].values())
                                })
                                st.dataframe(range_df, use_container_width=True)

                                if results['range_analysis']['underrepresented_ranges']:
                                    st.warning("⚠️ Underrepresented ranges:")
                                    for gap in results['range_analysis']['underrepresented_ranges']:
                                        st.write(f"- **{gap['range']}**: needed {gap['winning_count']}, had {gap['our_count']}")

                            # Recommendations
                            st.subheader("💡 Recommendations")
                            for i, rec in enumerate(results['recommendations'], 1):
                                st.info(f"**{i}.** {rec}")

                        except Exception as e:
                            st.error(f"Error during analysis: {str(e)}")
                            logger.error(f"Failure analysis error: {e}")
                else:
                    st.warning("Please enter at least one complete prediction and the winning numbers.")

    # Add Latest Draw tab
    with tabs[6]:
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
                            from src.core.database import EuromillionsDrawing, get_session
                            
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
                            from src.core.database import FrenchLotoDrawing, get_session
                            
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
    with tabs[7]:
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