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
    # Handle the case where modules aren't available yet
    pass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

# Initialize session state for consistent state management
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'french_loto_data_loaded' not in st.session_state:
    st.session_state.french_loto_data_loaded = False
if 'active_lottery' not in st.session_state:
    st.session_state.active_lottery = "Euromillions"
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'french_loto_data' not in st.session_state:
    st.session_state.french_loto_data = None

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="Lottery Prediction Platform",
        page_icon="🎲",
        layout="wide"
    )
    
    # Application header
    st.title("Advanced Lottery Prediction Platform")
    
    # Sidebar for global controls and data management
    with st.sidebar:
        st.header("Data Management")
        
        # Lottery selector
        lottery_type = st.radio(
            "Select Lottery Type",
            ["Euromillions", "French Loto"],
            horizontal=True
        )
        st.session_state.active_lottery = lottery_type
        
        st.divider()
        
        # Euromillions data management
        if lottery_type == "Euromillions":
            st.subheader("Euromillions Data")
            
            if st.button("Load Euromillions Data"):
                try:
                    # Get database connection
                    conn = get_db_connection()
                    if conn is None:
                        st.error("❌ Could not connect to database!")
                        return
                    
                    query = "SELECT * FROM euromillions_drawings ORDER BY date DESC"
                    data = pd.read_sql(query, conn)
                    
                    if data is not None and not data.empty:
                        st.session_state.processed_data = data
                        st.session_state.data_loaded = True
                        st.success(f"✅ Successfully loaded {len(data)} Euromillions drawings!")
                    else:
                        st.error("❌ No Euromillions data found in the database!")
                except Exception as e:
                    st.error(f"❌ Error loading Euromillions data: {e}")
            
            if st.session_state.data_loaded:
                st.success(f"✅ {len(st.session_state.processed_data)} Euromillions drawings loaded")
        
        # French Loto data management
        else:
            st.subheader("French Loto Data")
            
            if st.button("Load French Loto Data"):
                try:
                    # Get database connection
                    conn = get_db_connection()
                    if conn is None:
                        st.error("❌ Could not connect to database!")
                        return
                    
                    query = "SELECT * FROM french_loto_drawings ORDER BY date DESC"
                    data = pd.read_sql(query, conn)
                    
                    if data is not None and not data.empty:
                        st.session_state.french_loto_data = data
                        st.session_state.french_loto_data_loaded = True
                        st.success(f"✅ Successfully loaded {len(data)} French Loto drawings!")
                    else:
                        st.error("❌ No French Loto data found in the database!")
                except Exception as e:
                    st.error(f"❌ Error loading French Loto data: {e}")
            
            if st.session_state.french_loto_data_loaded:
                st.success(f"✅ {len(st.session_state.french_loto_data)} French Loto drawings loaded")
    
    # Create tabs for different application functionalities
    tabs = st.tabs([
        "Data Overview", 
        "Statistics", 
        "Strategy Generation", 
        "Results Analysis", 
        "Visualizations"
    ])
    
    # Data Overview tab
    with tabs[0]:
        st.header("Data Overview")
        
        if st.session_state.active_lottery == "Euromillions":
            if not st.session_state.data_loaded:
                st.warning("⚠️ Please load Euromillions data from the sidebar first!")
            else:
                data = st.session_state.processed_data
                st.write("### Latest Euromillions Drawings")
                st.dataframe(data.head(10))
                
                # Add export options
                st.subheader("Export Data")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Export to CSV"):
                        csv = data.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="euromillions_data.csv",
                            mime="text/csv"
                        )
                with col2:
                    if st.button("Export to Excel"):
                        # Convert DataFrame to Excel
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            data.to_excel(writer, index=False, sheet_name='Euromillions')
                            writer.close()
                            
                        # Prepare for download
                        excel_data = output.getvalue()
                        st.download_button(
                            label="Download Excel",
                            data=excel_data,
                            file_name="euromillions_data.xlsx",
                            mime="application/vnd.ms-excel"
                        )
        else:
            if not st.session_state.french_loto_data_loaded:
                st.warning("⚠️ Please load French Loto data from the sidebar first!")
            else:
                data = st.session_state.french_loto_data
                st.write("### Latest French Loto Drawings")
                st.dataframe(data.head(10))
                
                # Add export options
                st.subheader("Export Data")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Export to CSV"):
                        csv = data.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="french_loto_data.csv",
                            mime="text/csv"
                        )
                with col2:
                    if st.button("Export to Excel"):
                        # Convert DataFrame to Excel
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            data.to_excel(writer, index=False, sheet_name='FrenchLoto')
                            writer.close()
                            
                        # Prepare for download
                        excel_data = output.getvalue()
                        st.download_button(
                            label="Download Excel",
                            data=excel_data,
                            file_name="french_loto_data.xlsx",
                            mime="application/vnd.ms-excel"
                        )
    
    # Statistics tab
    with tabs[1]:
        st.header("Statistical Analysis")
        
        if st.session_state.active_lottery == "Euromillions":
            if not st.session_state.data_loaded:
                st.warning("⚠️ Please load Euromillions data first from the Data Management sidebar!")
            else:
                st.write("Euromillions statistics will be displayed here")
                # Stats will be implemented in future updates
        else:
            if not st.session_state.french_loto_data_loaded:
                st.warning("⚠️ Please load French Loto data first from the Data Management sidebar!")
            else:
                st.write("French Loto statistics will be displayed here")
                # Stats will be implemented in future updates
    
    # Strategy Generation tab
    with tabs[2]:
        st.header("Strategy Generation")
        
        # Check which lottery is active and ensure data is loaded
        if st.session_state.active_lottery == "French Loto":
            if not st.session_state.french_loto_data_loaded:
                st.warning("⚠️ Please load French Loto data first from the Data Management sidebar!")
            else:
                # Data is loaded, show French Loto strategy generator
                st.subheader("French Loto Strategy Generator")
                
                # Strategy selection
                strategy_choice = st.selectbox(
                    "Select Strategy",
                    ["Frequency-Based", "Pattern-Based", "Statistical", "Balanced", 
                     "Bayesian", "Risk/Reward", "Coverage", "Markov Chain", "Time Series", 
                     "Anti-Cognitive Bias"],
                    key="french_loto_strategy_choice"
                )
                
                # Number of combinations to generate
                num_combinations = st.number_input("Number of combinations", 1, 10, 3, key="french_loto_num_combinations")
                
                # Description based on selected strategy
                if strategy_choice == "Frequency-Based":
                    st.info("This strategy selects numbers based on their historical frequency")
                    recency_weight = st.slider("Recent draws importance", 0, 100, 50, key="french_loto_recency_weight") / 100.0
                
                elif strategy_choice == "Pattern-Based":
                    st.info("This strategy analyzes patterns in the historical data")
                    pattern_depth = st.slider("Pattern recognition depth", 1, 10, 5, key="french_loto_pattern_depth")
                
                elif strategy_choice == "Statistical":
                    st.info("This strategy uses statistical models to predict likely numbers")
                    confidence = st.slider("Confidence level", 60, 99, 90, key="french_loto_confidence")
                
                elif strategy_choice == "Balanced":
                    st.info("This strategy balances between hot and cold numbers")
                    balance = st.slider("Hot/Cold balance", 0, 100, 50, key="french_loto_balance") / 100.0
                
                elif strategy_choice == "Bayesian":
                    st.info("This strategy uses Bayesian inference to estimate probabilities based on historical data and prior knowledge")
                    recent_draws_count = st.slider("Number of recent draws to analyze", 5, 50, 20, key="french_loto_recent_draws")
                    prior_strength = st.slider("Prior knowledge strength", 1, 10, 5, key="french_loto_prior_strength")
                
                elif strategy_choice == "Risk/Reward":
                    st.info("This strategy balances between risk and potential reward")
                    risk_level = st.slider("Risk level (1-10)", 1, 10, 5, key="french_loto_risk_level")
                    st.info("Higher risk level = more unusual number combinations with potentially higher rewards")
                
                elif strategy_choice == "Coverage":
                    st.info("This strategy maximizes coverage of potential winning combinations")
                    balanced = st.checkbox("Use balanced coverage", True, key="french_loto_balanced_coverage")
                    st.info("Balanced coverage ensures more even distribution across the number space")
                
                elif strategy_choice == "Markov Chain":
                    st.info("This strategy uses Markov Chain models to predict numbers based on transition probabilities")
                    lag = st.slider("Lag (order of the Markov model)", 1, 3, 1, key="french_loto_markov_lag")
                
                elif strategy_choice == "Time Series":
                    st.info("This strategy uses time series analysis to identify cyclical patterns")
                    window_size = st.slider("Window size for analysis", 5, 20, 10, key="french_loto_window_size")
                
                elif strategy_choice == "Anti-Cognitive Bias":
                    st.info("This strategy avoids common cognitive biases in number selection")
                    st.write("This strategy purposely avoids patterns that are commonly selected due to cognitive biases, such as birthday numbers, lucky numbers, visual patterns, etc.")
                
                # Generate button
                if st.button("Generate Combinations", key="french_loto_generate"):
                    with st.spinner("Generating optimized combinations..."):
                        # Display sample results
                        st.subheader("Generated Combinations")
                        
                        for i in range(num_combinations):
                            # These are just placeholder values for demonstration
                            numbers = sorted([i+1, i+10, i+17, i+24, i+34])
                            lucky = i+5
                            
                            # Display as a formatted string
                            st.write(f"**Combination {i+1}:** Numbers {numbers}, Lucky {lucky}")
                
        elif st.session_state.active_lottery == "Euromillions":
            if not st.session_state.data_loaded:
                st.warning("⚠️ Please load Euromillions data first from the Data Management sidebar!")
            else:
                # Data is loaded, show Euromillions strategy generator
                st.subheader("Euromillions Strategy Generator")
                
                # Strategy selection
                strategy_choice = st.selectbox(
                    "Select Strategy",
                    ["Frequency-Based", "Pattern-Based", "Statistical", "Balanced", 
                     "Bayesian", "Risk/Reward", "Coverage", "Markov Chain", "Time Series", 
                     "Anti-Cognitive Bias"],
                    key="euromillions_strategy_choice"
                )
                
                # Number of combinations to generate
                num_combinations = st.number_input("Number of combinations", 1, 10, 3, key="euromillions_num_combinations")
                
                # Description based on selected strategy
                if strategy_choice == "Frequency-Based":
                    st.info("This strategy selects numbers based on their historical frequency")
                    recency_weight = st.slider("Recent draws importance", 0, 100, 50, key="euromillions_recency_weight") / 100.0
                
                elif strategy_choice == "Pattern-Based":
                    st.info("This strategy analyzes patterns in the historical data")
                    pattern_depth = st.slider("Pattern recognition depth", 1, 10, 5, key="euromillions_pattern_depth")
                
                elif strategy_choice == "Statistical":
                    st.info("This strategy uses statistical models to predict likely numbers")
                    confidence = st.slider("Confidence level", 60, 99, 90, key="euromillions_confidence")
                
                elif strategy_choice == "Balanced":
                    st.info("This strategy balances between hot and cold numbers")
                    balance = st.slider("Hot/Cold balance", 0, 100, 50, key="euromillions_balance") / 100.0
                
                elif strategy_choice == "Bayesian":
                    st.info("This strategy uses Bayesian inference to estimate probabilities based on historical data and prior knowledge")
                    recent_draws_count = st.slider("Number of recent draws to analyze", 5, 50, 20, key="euromillions_recent_draws")
                    prior_strength = st.slider("Prior knowledge strength", 1, 10, 5, key="euromillions_prior_strength")
                
                elif strategy_choice == "Risk/Reward":
                    st.info("This strategy balances between risk and potential reward")
                    risk_level = st.slider("Risk level (1-10)", 1, 10, 5, key="euromillions_risk_level")
                    st.info("Higher risk level = more unusual number combinations with potentially higher rewards")
                
                elif strategy_choice == "Coverage":
                    st.info("This strategy maximizes coverage of potential winning combinations")
                    balanced = st.checkbox("Use balanced coverage", True, key="euromillions_balanced_coverage")
                    st.info("Balanced coverage ensures more even distribution across the number space")
                
                elif strategy_choice == "Markov Chain":
                    st.info("This strategy uses Markov Chain models to predict numbers based on transition probabilities")
                    lag = st.slider("Lag (order of the Markov model)", 1, 3, 1, key="euromillions_markov_lag")
                
                elif strategy_choice == "Time Series":
                    st.info("This strategy uses time series analysis to identify cyclical patterns")
                    window_size = st.slider("Window size for analysis", 5, 20, 10, key="euromillions_window_size")
                
                elif strategy_choice == "Anti-Cognitive Bias":
                    st.info("This strategy avoids common cognitive biases in number selection")
                    st.write("This strategy purposely avoids patterns that are commonly selected due to cognitive biases, such as birthday numbers, lucky numbers, visual patterns, etc.")
                
                # Generate button
                if st.button("Generate Combinations", key="euromillions_generate"):
                    with st.spinner("Generating optimized combinations..."):
                        try:
                            # Check if we have the statistics and strategies objects
                            if 'euromillions_stats' not in st.session_state:
                                from statistics import EuromillionsStatistics
                                st.session_state.euromillions_stats = EuromillionsStatistics(st.session_state.processed_data)
                            
                            if 'euromillions_strategies' not in st.session_state:
                                from strategies import PredictionStrategies
                                st.session_state.euromillions_strategies = PredictionStrategies(st.session_state.euromillions_stats)
                            
                            # Call the appropriate strategy based on selection
                            strategies = st.session_state.euromillions_strategies
                            
                            if strategy_choice == "Frequency-Based":
                                combinations = strategies.frequency_strategy(num_combinations, recency_weight)
                            
                            elif strategy_choice == "Pattern-Based":
                                # Map to temporal strategy
                                combinations = strategies.temporal_strategy(num_combinations, pattern_depth * 5)
                            
                            elif strategy_choice == "Statistical":
                                # Map to stratified strategy
                                combinations = strategies.stratified_sampling_strategy(num_combinations, "range", confidence / 100.0)
                            
                            elif strategy_choice == "Balanced":
                                # Map to mixed strategy
                                combinations = strategies.mixed_strategy(num_combinations, balance)
                            
                            elif strategy_choice == "Bayesian":
                                combinations = strategies.bayesian_strategy(num_combinations, recent_draws_count, prior_strength)
                            
                            elif strategy_choice == "Risk/Reward":
                                combinations = strategies.risk_reward_strategy(num_combinations, risk_level)
                            
                            elif strategy_choice == "Coverage":
                                combinations = strategies.coverage_strategy(num_combinations, balanced)
                            
                            elif strategy_choice == "Markov Chain":
                                combinations = strategies.markov_strategy(num_combinations, lag)
                            
                            elif strategy_choice == "Time Series":
                                combinations = strategies.time_series_strategy(num_combinations, window_size)
                            
                            elif strategy_choice == "Anti-Cognitive Bias":
                                combinations = strategies.cognitive_bias_strategy(num_combinations)
                            
                            else:
                                # Default to frequency strategy
                                combinations = strategies.frequency_strategy(num_combinations)
                            
                            # Display the generated combinations
                            st.subheader("Generated Combinations")
                            
                            for i, combo in enumerate(combinations):
                                # Format numbers and stars for display
                                numbers = combo['numbers'] if isinstance(combo['numbers'], list) else sorted([int(n) for n in combo['numbers'].strip('[]').split(',')])
                                stars = combo['stars'] if isinstance(combo['stars'], list) else sorted([int(s) for s in combo['stars'].strip('[]').split(',')])
                                
                                # Style for the numbers and stars
                                numbers_html = ' '.join([f'<span style="background-color:#f0f0f0; padding:5px; margin:2px; border-radius:50%;">{n}</span>' for n in sorted(numbers)])
                                stars_html = ' '.join([f'<span style="background-color:#ffe066; padding:5px; margin:2px; border-radius:50%;">★{s}</span>' for s in sorted(stars)])
                                
                                # Display score
                                score = combo.get('score', 0)
                                score_text = f"<span style='color:{'green' if score > 70 else 'orange' if score > 50 else 'red'}'>{score:.1f}</span>"
                                
                                # Display combination with HTML
                                st.markdown(f"**Combination {i+1}** (Score: {score_text}):<br> {numbers_html} | {stars_html}", unsafe_allow_html=True)
                                
                            # Option to save combinations
                            if 'generated_combinations' not in st.session_state:
                                st.session_state.generated_combinations = combinations
                            else:
                                st.session_state.generated_combinations = combinations
                                
                            if st.button("Save These Combinations to Database"):
                                try:
                                    import json
                                    from database import get_session
                                    from database import GeneratedCombination
                                    from datetime import datetime
                                    
                                    session = get_session()
                                    saved_count = 0
                                    
                                    for combo in combinations:
                                        # Convert to proper format
                                        numbers_str = json.dumps(sorted(combo['numbers'])) if isinstance(combo['numbers'], list) else json.dumps(sorted([int(n) for n in combo['numbers'].strip('[]').split(',')]))
                                        stars_str = json.dumps(sorted(combo['stars'])) if isinstance(combo['stars'], list) else json.dumps(sorted([int(s) for s in combo['stars'].strip('[]').split(',')]))
                                        
                                        # Create new record
                                        new_combo = GeneratedCombination(
                                            created_at=datetime.now().date(),
                                            numbers=numbers_str,
                                            stars=stars_str,
                                            strategy=strategy_choice,
                                            score=float(combo.get('score', 0))
                                        )
                                        
                                        session.add(new_combo)
                                        saved_count += 1
                                    
                                    session.commit()
                                    st.success(f"✅ Successfully saved {saved_count} combinations to database!")
                                    
                                except Exception as e:
                                    st.error(f"❌ Error saving combinations: {str(e)}")
                                finally:
                                    session.close()
                        except Exception as e:
                            st.error(f"❌ Error generating combinations: {str(e)}")
                            st.error("Please check that you have loaded data correctly and try again.")

    # Results Analysis tab
    with tabs[3]:
        st.header("Results Analysis")
        st.write("Results analysis functionality will be implemented here.")
        
    # Visualizations tab
    with tabs[4]:
        st.header("Visualizations")
        st.write("Visualization tools will be added here.")


if __name__ == "__main__":
    main()