import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime
import io
import base64
import json
from data_processor import DataProcessor
from statistics import EuromillionsStatistics
from strategies import PredictionStrategies
from visualization import DataVisualization
from utils import get_download_link_csv, get_download_link_excel
import database
from strategy_testing import StrategyTester
from combination_analysis import analyze_full_combinations, analyze_number_combinations, analyze_star_combinations

# Initialize database tables if they don't exist
try:
    database.init_db()
except Exception as e:
    st.error(f"Error initializing database: {str(e)}")
    st.warning("Running in offline mode. Some database-dependent features will be disabled.")

# Create a flag to track database status
if 'db_available' not in st.session_state:
    st.session_state.db_available = database.DB_AVAILABLE

# Page configuration
st.set_page_config(
    page_title="Euromillions Prediction Application",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for data
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'euromillions_data' not in st.session_state:
    st.session_state.euromillions_data = None
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = None
if 'statistics' not in st.session_state:
    st.session_state.statistics = None
if 'strategies' not in st.session_state:
    st.session_state.strategies = None
if 'visualization' not in st.session_state:
    st.session_state.visualization = None
if 'generated_combinations' not in st.session_state:
    st.session_state.generated_combinations = {}
if 'combinations_loaded' not in st.session_state:
    st.session_state.combinations_loaded = False

# Title and introduction
st.title("Euromillions Advanced Prediction Application")
st.markdown("""
This application uses advanced statistical and mathematical models to analyze Euromillions drawing history
and generate optimized combinations. The app supports different prediction strategies based on frequency analysis,
Markov chains, Bayesian methods, and more.
""")

# Sidebar for data upload and configuration
with st.sidebar:
    st.header("Data Management")
    
    data_source = st.radio(
        "Choose data source:",
        ["Upload CSV file", "Use sample data"]
    )
    
    uploaded_file = None
    if data_source == "Upload CSV file":
        uploaded_file = st.file_uploader("Upload Euromillions historical data (CSV)", type=["csv"])
        
        if uploaded_file is not None:
            try:
                data = pd.read_csv(uploaded_file)
                st.session_state.data_processor = DataProcessor(data)
                st.session_state.euromillions_data = st.session_state.data_processor.get_processed_data()
                st.session_state.statistics = EuromillionsStatistics(st.session_state.euromillions_data)
                st.session_state.strategies = PredictionStrategies(st.session_state.statistics)
                st.session_state.visualization = DataVisualization(st.session_state.euromillions_data, st.session_state.statistics)
                st.session_state.data_loaded = True
                st.success("Data successfully loaded and processed!")
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
    else:
        data_option = st.radio(
            "Data source options:",
            ["Load from database", "Load sample CSV", "Load both (merge and save to database)"]
        )
        
        if st.button("Load Data"):
            try:
                if data_option == "Load from database":
                    # Try to load data from the database
                    db_data = database.get_all_drawings()
                    if not db_data.empty:
                        st.session_state.data_processor = DataProcessor(db_data)
                        st.session_state.euromillions_data = st.session_state.data_processor.get_processed_data()
                        st.session_state.statistics = EuromillionsStatistics(st.session_state.euromillions_data)
                        st.session_state.strategies = PredictionStrategies(st.session_state.statistics)
                        st.session_state.visualization = DataVisualization(st.session_state.euromillions_data, st.session_state.statistics)
                        st.session_state.data_loaded = True
                        st.success(f"Successfully loaded {len(db_data)} records from database!")
                    else:
                        st.warning("No data found in the database. Try loading the sample CSV data first.")
                
                elif data_option == "Load sample CSV":
                    # Load sample data from the sample_data directory
                    data = pd.read_csv("sample_data/sample_euromillions.csv")
                    st.session_state.data_processor = DataProcessor(data)
                    st.session_state.euromillions_data = st.session_state.data_processor.get_processed_data()
                    st.session_state.statistics = EuromillionsStatistics(st.session_state.euromillions_data)
                    st.session_state.strategies = PredictionStrategies(st.session_state.statistics)
                    st.session_state.visualization = DataVisualization(st.session_state.euromillions_data, st.session_state.statistics)
                    st.session_state.data_loaded = True
                    st.success(f"Successfully loaded {len(data)} records from sample CSV!")
                
                else:  # Load both
                    # Load sample data from CSV
                    csv_data = pd.read_csv("sample_data/sample_euromillions.csv")
                    
                    # Process the data
                    data_processor = DataProcessor(csv_data)
                    processed_data = data_processor.get_processed_data()
                    
                    # Load the data into the database
                    inserted_count = database.load_drawings_from_dataframe(processed_data)
                    
                    # Now load all data from the database
                    db_data = database.get_all_drawings()
                    
                    # Set up application state
                    st.session_state.data_processor = DataProcessor(db_data)
                    st.session_state.euromillions_data = st.session_state.data_processor.get_processed_data()
                    st.session_state.statistics = EuromillionsStatistics(st.session_state.euromillions_data)
                    st.session_state.strategies = PredictionStrategies(st.session_state.statistics)
                    st.session_state.visualization = DataVisualization(st.session_state.euromillions_data, st.session_state.statistics)
                    st.session_state.data_loaded = True
                    
                    if inserted_count > 0:
                        st.success(f"Added {inserted_count} new records to the database. Total records: {len(db_data)}")
                    else:
                        st.info(f"No new records added. Database already contains all {len(db_data)} records.")
                
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
    
    if st.session_state.data_loaded:
        st.header("Add New Draw")
        
        # Form for adding new draw
        with st.form("new_draw_form"):
            draw_date = st.date_input("Draw Date", datetime.datetime.now().date())
            st.markdown("**Main Numbers (1-50)**")
            col1, col2 = st.columns(2)
            with col1:
                num1 = st.number_input("Number 1", min_value=1, max_value=50, step=1)
                num2 = st.number_input("Number 2", min_value=1, max_value=50, step=1)
                num3 = st.number_input("Number 3", min_value=1, max_value=50, step=1)
            with col2:
                num4 = st.number_input("Number 4", min_value=1, max_value=50, step=1)
                num5 = st.number_input("Number 5", min_value=1, max_value=50, step=1)
            
            st.markdown("**Star Numbers (1-12)**")
            star1 = st.number_input("Star 1", min_value=1, max_value=12, step=1)
            star2 = st.number_input("Star 2", min_value=1, max_value=12, step=1)
            
            submitted = st.form_submit_button("Add New Draw")
            
            if submitted:
                # Check for duplicates
                numbers = [num1, num2, num3, num4, num5]
                stars = [star1, star2]
                
                if len(set(numbers)) != 5:
                    st.error("Main numbers must be unique!")
                elif len(set(stars)) != 2:
                    st.error("Star numbers must be unique!")
                else:
                    try:
                        # Add new draw to the dataset
                        st.session_state.data_processor.add_new_draw(
                            draw_date, numbers, stars
                        )
                        
                        # Also add to the database
                        day_name = draw_date.strftime("%A")  # Get day name from date
                        database.add_new_drawing(draw_date, numbers, stars, day_of_week=day_name)
                        
                        # Update all dependent objects
                        st.session_state.euromillions_data = st.session_state.data_processor.get_processed_data()
                        st.session_state.statistics = EuromillionsStatistics(st.session_state.euromillions_data)
                        st.session_state.strategies = PredictionStrategies(st.session_state.statistics)
                        st.session_state.visualization = DataVisualization(st.session_state.euromillions_data, st.session_state.statistics)
                        st.success("New draw added successfully to both application and database!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding new draw: {str(e)}")

# Main content area
if not st.session_state.data_loaded:
    st.info("Please upload Euromillions historical data or load sample data to start.")
else:
    # Create tabs for different functionalities
    tabs = st.tabs([
        "Data Overview", 
        "Statistical Analysis", 
        "Strategy Generation",
        "Visualizations",
        "Combination Analysis",
        "My Combinations",
        "All Generated Combinations",
        "Strategy Testing"
    ])
    
    # Data Overview tab
    with tabs[0]:
        st.header("Data Overview")
        
        # Display data summary
        st.subheader("Dataset Information")
        
        # Handle date range safely - convert to string format to avoid type comparison issues
        min_date = "N/A"
        max_date = "N/A"
        if not st.session_state.euromillions_data.empty:
            # First, ensure all date values are of the same type (convert timestamps to dates)
            try:
                date_column = st.session_state.euromillions_data['date'].copy()
                
                # Convert any Timestamp objects to datetime.date objects for consistency
                date_column = date_column.apply(lambda x: x.date() if hasattr(x, 'date') and callable(getattr(x, 'date')) else x)
                
                # Now safely get min and max dates
                if not date_column.empty:
                    min_date = str(min(date_column))
                    max_date = str(max(date_column))
            except Exception as e:
                # Fallback in case of any errors
                st.warning(f"Note: Could not determine exact date range due to mixed date types. Error: {str(e)}")
                min_date = "Unknown"
                max_date = "Present"
            
        data_info = {
            "Total number of draws": len(st.session_state.euromillions_data),
            "Date range": f"{min_date} to {max_date}",
            "Data columns": ", ".join(st.session_state.euromillions_data.columns)
        }
        
        for key, value in data_info.items():
            st.write(f"**{key}:** {value}")
        
        # Display recent draws
        st.subheader("Most Recent Draws")
        st.dataframe(st.session_state.euromillions_data.head(10))
        
        # Download options
        st.subheader("Download Data")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download as CSV",
                data=st.session_state.euromillions_data.to_csv(index=False),
                file_name="euromillions_data.csv",
                mime="text/csv"
            )
        with col2:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                st.session_state.euromillions_data.to_excel(writer, sheet_name='Euromillions Data', index=False)
            excel_data = buffer.getvalue()
            st.download_button(
                label="Download as Excel",
                data=excel_data,
                file_name="euromillions_data.xlsx",
                mime="application/vnd.ms-excel"
            )
    
    # Statistical Analysis tab
    with tabs[1]:
        st.header("Statistical Analysis")
        
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Number Frequency", "Star Frequency", "Pair Analysis", "Time Series Patterns", "Distribution Analysis"]
        )
        
        if analysis_type == "Number Frequency":
            st.subheader("Main Number Frequency Analysis")
            
            # Frequency weighting
            col1, col2 = st.columns(2)
            with col1:
                recent_weight = st.slider("Recent draws weight (%)", 0, 100, 60)
            with col2:
                historical_weight = 100 - recent_weight
                st.info(f"Historical draws weight: {historical_weight}%")
            
            # Get weighted frequency data
            weighted_freq = st.session_state.statistics.get_weighted_frequency(recent_weight/100)
            
            # Display frequency chart
            fig = st.session_state.visualization.plot_number_frequency(weighted_freq)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display top and bottom numbers
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 10 Most Frequent Numbers")
                top_numbers = weighted_freq.sort_values(ascending=False).head(10)
                for num, freq in top_numbers.items():
                    st.write(f"**Number {num}:** {freq:.4f}")
            
            with col2:
                st.subheader("Top 10 Least Frequent Numbers")
                bottom_numbers = weighted_freq.sort_values().head(10)
                for num, freq in bottom_numbers.items():
                    st.write(f"**Number {num}:** {freq:.4f}")
        
        elif analysis_type == "Star Frequency":
            st.subheader("Star Number Frequency Analysis")
            
            # Frequency weighting
            col1, col2 = st.columns(2)
            with col1:
                recent_weight = st.slider("Recent draws weight (%)", 0, 100, 60)
            with col2:
                historical_weight = 100 - recent_weight
                st.info(f"Historical draws weight: {historical_weight}%")
            
            # Get weighted frequency data
            weighted_freq = st.session_state.statistics.get_weighted_star_frequency(recent_weight/100)
            
            # Display frequency chart
            fig = st.session_state.visualization.plot_star_frequency(weighted_freq)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display all stars ranked
            st.subheader("Star Numbers Ranked by Frequency")
            ranked_stars = weighted_freq.sort_values(ascending=False)
            
            # Create columns for better display
            cols = st.columns(4)
            for i, (star, freq) in enumerate(ranked_stars.items()):
                cols[i % 4].write(f"**Star {star}:** {freq:.4f}")
        
        elif analysis_type == "Pair Analysis":
            st.subheader("Number Pair Analysis")
            
            # Get pair analysis data
            pair_data = st.session_state.statistics.get_number_pairs_frequency()
            
            # Display heatmap
            fig = st.session_state.visualization.plot_number_pairs_heatmap(pair_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show top pairs
            st.subheader("Top 15 Most Frequent Number Pairs")
            top_pairs = st.session_state.statistics.get_top_number_pairs(15)
            
            # Create columns for better display
            cols = st.columns(3)
            for i, (pair, count) in enumerate(top_pairs):
                cols[i % 3].write(f"**{pair}:** {count} occurrences")
            
            # Star pairs
            st.subheader("Star Pair Analysis")
            
            # Get star pair analysis data
            star_pair_data = st.session_state.statistics.get_star_pairs_frequency()
            
            # Display star pairs chart
            fig = st.session_state.visualization.plot_star_pairs_chart(star_pair_data)
            st.plotly_chart(fig, use_container_width=True)
            
        elif analysis_type == "Time Series Patterns":
            st.subheader("Time Series Analysis")
            
            # Select number to analyze
            number_to_analyze = st.selectbox(
                "Select number to analyze time pattern",
                list(range(1, 51))
            )
            
            # Get time series data
            time_series_data = st.session_state.statistics.get_number_time_series(number_to_analyze)
            
            # Plot time series
            fig = st.session_state.visualization.plot_number_time_series(number_to_analyze, time_series_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show statistics about the number
            stats = st.session_state.statistics.get_number_statistics(number_to_analyze)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Frequency", f"{stats['frequency']:.2f}%")
            col2.metric("Avg. Draws Between Appearances", f"{stats['avg_gap']:.1f}")
            col3.metric("Draws Since Last Appearance", stats['draws_since_last'])
            
            # Show cyclic patterns if identified
            if 'cyclic_pattern' in stats and stats['cyclic_pattern']:
                st.success(f"Potential cyclic pattern detected: appears approximately every {stats['cyclic_pattern']} draws")
            
            # Display occurrences by day of week
            dow_data = st.session_state.statistics.get_day_of_week_distribution(number_to_analyze)
            if dow_data is not None:
                fig = st.session_state.visualization.plot_day_of_week_distribution(number_to_analyze, dow_data)
                st.plotly_chart(fig, use_container_width=True)
            
        elif analysis_type == "Distribution Analysis":
            st.subheader("Distribution Analysis")
            
            dist_type = st.selectbox(
                "Select Distribution Type",
                ["Even/Odd Distribution", "Number Range Distribution", "Sum Distribution"]
            )
            
            if dist_type == "Even/Odd Distribution":
                # Get even/odd distribution
                even_odd_dist = st.session_state.statistics.get_even_odd_distribution()
                
                # Plot distribution
                fig = st.session_state.visualization.plot_even_odd_distribution(even_odd_dist)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show most common patterns
                st.subheader("Most Common Even/Odd Patterns")
                patterns = st.session_state.statistics.get_common_even_odd_patterns()
                
                for pattern, count in patterns.items():
                    st.write(f"**{pattern}** (even/odd): {count} occurrences")
            
            elif dist_type == "Number Range Distribution":
                # Get range distribution
                range_dist = st.session_state.statistics.get_number_range_distribution()
                
                # Plot distribution
                fig = st.session_state.visualization.plot_number_range_distribution(range_dist)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show distribution stats
                st.subheader("Number Range Distribution")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                ranges = ["1-10", "11-20", "21-30", "31-40", "41-50"]
                cols = [col1, col2, col3, col4, col5]
                
                for i, r in enumerate(ranges):
                    cols[i].metric(f"Range {r}", f"{range_dist[r]:.1f}%")
                
            elif dist_type == "Sum Distribution":
                # Get sum distribution
                sum_dist = st.session_state.statistics.get_sum_distribution()
                
                # Plot distribution
                fig = st.session_state.visualization.plot_sum_distribution(sum_dist)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show sum stats
                avg_sum = st.session_state.statistics.get_average_sum()
                most_common_sums = st.session_state.statistics.get_most_common_sums(5)
                
                st.metric("Average Sum of 5 Main Numbers", f"{avg_sum:.1f}")
                
                st.subheader("Most Common Sums")
                for sum_val, count in most_common_sums:
                    st.write(f"**Sum {sum_val}:** {count} occurrences")
    
    # Strategy Generation tab
    with tabs[2]:
        st.header("Strategy Generation")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Strategy Parameters")
            
            strategy_type = st.selectbox(
                "Select Strategy",
                ["Frequency Strategy", "Mixed Strategy", "Temporal Strategy", "Stratified Sampling", "Coverage Strategy", 
                 "Risk/Reward Optimization", "Bayesian Model", "Markov Chain Model", "Time Series Model", "Anti-Cognitive Bias",
                 "Multi-Strategy"]
            )
            
            num_combinations = st.number_input("Number of combinations to generate", 1, 20, 5)
            
            # Strategy-specific parameters
            if strategy_type == "Frequency Strategy":
                st.info("This strategy selects numbers based on their frequency in historical draws")
                recent_weight = st.slider("Recent draws importance (%)", 0, 100, 60, key="freq_weight")
                
            elif strategy_type == "Mixed Strategy":
                st.info("This strategy mixes high-frequency numbers with strategic outsiders")
                hot_ratio = st.slider("Hot numbers ratio (%)", 0, 100, 70, key="hot_ratio")
                
            elif strategy_type == "Temporal Strategy":
                st.info("This strategy considers temporal patterns and cycles")
                lookback_period = st.slider("Lookback period (draws)", 10, 100, 30, key="lookback")
                
            elif strategy_type == "Stratified Sampling":
                st.info("This strategy ensures balanced distribution across different number properties")
                
                # Add new stratification type options
                strata_type = st.selectbox(
                    "Stratification Type",
                    [
                        "range", "even_odd", "prime_composite", 
                        "hot_cold", "decade", "pattern"
                    ],
                    help="Choose how to stratify your number selection"
                )
                
                # Add balance factor slider
                balance_factor = st.slider(
                    "Balance Factor", 
                    min_value=0.0, 
                    max_value=1.0, 
                    value=0.7, 
                    step=0.1,
                    help="Higher values favor balanced distribution across strata, lower values favor historical frequencies",
                    key="stratified_balance_factor"
                )
                
                # Display explanations based on selection
                if strata_type == "range":
                    st.info("Range stratification divides the number range 1-50 into 5 equal parts and selects numbers from each part.")
                elif strata_type == "even_odd":
                    st.info("Even-Odd stratification balances the selection of even and odd numbers based on historical patterns.")
                elif strata_type == "prime_composite":
                    st.info("Prime-Composite stratification balances the selection between prime numbers and non-prime numbers.")
                elif strata_type == "hot_cold":
                    st.info("Hot-Cold stratification mixes frequently drawn numbers with less frequently drawn ones.")
                elif strata_type == "decade":
                    st.info("Decade stratification ensures numbers are selected from different decades (1-10, 11-20, etc.).")
                elif strata_type == "pattern":
                    st.info("Pattern stratification selects numbers based on their mathematical properties and patterns.")
                
            elif strategy_type == "Coverage Strategy":
                st.info("This strategy optimizes to cover as many possible winning combinations as possible")
                optimization_method = st.selectbox(
                    "Optimization Method",
                    ["Maximize Coverage", "Balanced Coverage"]
                )
                
            elif strategy_type == "Risk/Reward Optimization":
                st.info("This strategy focuses on combinations that might be less played by others")
                risk_level = st.slider("Risk level", 1, 10, 5, key="risk_level")
                
            elif strategy_type == "Bayesian Model":
                st.info("This strategy uses Bayesian probability theory to predict numbers based on prior probabilities and recent evidence.")
                
                # Extended Bayesian parameters
                st.subheader("Bayesian Inference Parameters")
                
                # Draws selection
                recent_draws_count = st.slider("Recent draws to consider", 5, 50, 20, key="bayes_draws")
                
                # Prior type selection
                prior_type = st.selectbox(
                    "Prior Distribution Type",
                    ["empirical", "uniform", "informative"],
                    help="Select the type of prior distribution to use",
                    key="bayes_prior"
                )
                
                # Update method selection
                update_method = st.selectbox(
                    "Probability Update Method",
                    ["standard", "sequential", "adaptive"],
                    help="Select the method for updating probabilities",
                    key="bayes_update"
                )
                
                # Smoothing factor
                smoothing_factor = st.slider(
                    "Smoothing Factor", 
                    0.01, 1.0, 0.1, 0.01,
                    help="Laplace smoothing factor to handle zero probabilities",
                    key="bayes_smoothing"
                )
                
                # Show explanation based on selections
                if prior_type == "empirical":
                    st.info("Empirical prior: Uses historical frequencies from past drawings as the basis for probabilities")
                elif prior_type == "uniform":
                    st.info("Uniform prior: Assumes all numbers have equal probability initially (useful when you believe past frequencies aren't predictive)")
                elif prior_type == "informative":
                    st.info("Informative prior: Incorporates external knowledge about number patterns and player psychology")
                    
                if update_method == "standard":
                    st.info("Standard update: Classic Bayesian update using all evidence at once")
                elif update_method == "sequential":
                    st.info("Sequential update: Updates probabilities draw by draw, which can better capture patterns of sequential changes")
                elif update_method == "adaptive":
                    st.info("Adaptive update: Gives more weight to recent draws, adapting to potential trends or shifts in drawing patterns")
                
            elif strategy_type == "Markov Chain Model":
                st.info("This strategy uses Markov chain transition probabilities to predict the next draw based on previous draws")
                lag = st.slider("Lag (number of previous draws to consider)", 1, 5, 1, key="markov_lag")
                
            elif strategy_type == "Time Series Model":
                st.info("This strategy analyzes time series patterns to find cycles and predict numbers due to appear")
                window_size = st.slider("Analysis window size", 5, 30, 10, key="ts_window")
                
            elif strategy_type == "Anti-Cognitive Bias":
                st.info("This strategy generates combinations that avoid common cognitive biases most players have when selecting numbers")
            elif strategy_type == "Multi-Strategy":
                st.info("This approach generates combinations using ALL strategies at once, giving you a diverse set of combinations based on different mathematical and statistical approaches.")
                st.warning("Note: This will generate 1 combination from each strategy!")
            
            generate_button = st.button("Generate Combinations")
            
            if generate_button:
                with st.spinner("Generating optimized combinations..."):
                    # Generate combinations based on the selected strategy
                    try:
                        if strategy_type == "Frequency Strategy":
                            combinations = st.session_state.strategies.frequency_strategy(
                                num_combinations=num_combinations,
                                recent_weight=recent_weight/100
                            )
                        elif strategy_type == "Mixed Strategy":
                            combinations = st.session_state.strategies.mixed_strategy(
                                num_combinations=num_combinations,
                                hot_ratio=hot_ratio/100
                            )
                        elif strategy_type == "Temporal Strategy":
                            combinations = st.session_state.strategies.temporal_strategy(
                                num_combinations=num_combinations,
                                lookback_period=lookback_period
                            )
                        elif strategy_type == "Stratified Sampling":
                            combinations = st.session_state.strategies.stratified_sampling_strategy(
                                num_combinations=num_combinations,
                                strata_type=strata_type,
                                balance_factor=balance_factor
                            )
                        elif strategy_type == "Coverage Strategy":
                            combinations = st.session_state.strategies.coverage_strategy(
                                num_combinations=num_combinations,
                                balanced=optimization_method == "Balanced Coverage"
                            )
                        elif strategy_type == "Risk/Reward Optimization":
                            combinations = st.session_state.strategies.risk_reward_strategy(
                                num_combinations=num_combinations,
                                risk_level=risk_level
                            )
                        elif strategy_type == "Bayesian Model":
                            combinations = st.session_state.strategies.bayesian_strategy(
                                num_combinations=num_combinations,
                                recent_draws_count=recent_draws_count,
                                prior_type=prior_type,
                                update_method=update_method,
                                smoothing_factor=smoothing_factor
                            )
                        elif strategy_type == "Markov Chain Model":
                            combinations = st.session_state.strategies.markov_strategy(
                                num_combinations=num_combinations,
                                lag=lag
                            )
                        elif strategy_type == "Time Series Model":
                            combinations = st.session_state.strategies.time_series_strategy(
                                num_combinations=num_combinations,
                                window_size=window_size
                            )
                        elif strategy_type == "Anti-Cognitive Bias":
                            combinations = st.session_state.strategies.cognitive_bias_strategy(
                                num_combinations=num_combinations
                            )
                        elif strategy_type == "Multi-Strategy":
                            # Generate combinations for each strategy
                            all_strategies = {
                                "Frequency Strategy": lambda: st.session_state.strategies.frequency_strategy(num_combinations=1, recent_weight=0.6),
                                "Mixed Strategy": lambda: st.session_state.strategies.mixed_strategy(num_combinations=1, hot_ratio=0.7),
                                "Temporal Strategy": lambda: st.session_state.strategies.temporal_strategy(num_combinations=1, lookback_period=30),
                                "Stratified Sampling": lambda: st.session_state.strategies.stratified_sampling_strategy(
                                    num_combinations=1,
                                    strata_type="pattern",  # Use pattern as default for multi-strategy approach
                                    balance_factor=0.7
                                ),
                                "Coverage Strategy": lambda: st.session_state.strategies.coverage_strategy(num_combinations=1, balanced=True),
                                "Risk/Reward Optimization": lambda: st.session_state.strategies.risk_reward_strategy(num_combinations=1, risk_level=5),
                                "Bayesian Model": lambda: st.session_state.strategies.bayesian_strategy(
                                    num_combinations=1, 
                                    recent_draws_count=20,
                                    prior_type="empirical", 
                                    update_method="sequential",
                                    smoothing_factor=0.1
                                ),
                                "Markov Chain Model": lambda: st.session_state.strategies.markov_strategy(num_combinations=1, lag=1),
                                "Time Series Model": lambda: st.session_state.strategies.time_series_strategy(num_combinations=1, window_size=10),
                                "Anti-Cognitive Bias": lambda: st.session_state.strategies.cognitive_bias_strategy(num_combinations=1)
                            }
                            
                            combinations = []
                            strategy_progress = st.progress(0.0)
                            
                            for i, (strategy_name, strategy_fn) in enumerate(all_strategies.items()):
                                try:
                                    st.write(f"Generating combinations using {strategy_name}...")
                                    strategy_combos = strategy_fn()
                                    
                                    # Add strategy name to each combination
                                    for combo in strategy_combos:
                                        combo['strategy'] = strategy_name
                                    
                                    combinations.extend(strategy_combos)
                                    
                                    # Store these combinations in their respective strategy too
                                    st.session_state.generated_combinations[strategy_name] = strategy_combos
                                    
                                    # Update progress
                                    strategy_progress.progress((i + 1) / len(all_strategies))
                                except Exception as e:
                                    st.warning(f"Error generating combinations for {strategy_name}: {str(e)}")
                        
                        # Store the generated combinations
                        st.session_state.generated_combinations[strategy_type] = combinations
                        
                        # Also save to the database
                        for combo in combinations:
                            numbers = combo['numbers']
                            stars = combo['stars']
                            score = combo.get('score', 0.0)
                            database.save_generated_combination(numbers, stars, strategy_type, score)
                        
                        st.success(f"Successfully generated {num_combinations} combinations and saved to database!")
                    except Exception as e:
                        st.error(f"Error generating combinations: {str(e)}")
        
        with col2:
            st.subheader("Generated Combinations")
            
            # Add Score/Confidence explanation
            with st.expander("What does Score/Confidence mean?"):
                st.markdown("""
                **Score/Confidence** represents how strongly the algorithm believes in this combination based on the strategy used:
                
                - **Higher values** indicate combinations more likely to appear according to the algorithm
                - **Different strategies** calculate scores differently:
                  - Frequency: Higher scores for more frequently drawn numbers
                  - Bayesian: Probability estimates based on prior observations
                  - Markov: Transition likelihood between consecutive states
                  - Time Series: Predictions based on temporal patterns
                  - Risk/Reward: Balance between common and rare numbers
                
                The score is not a true probability (0-100%), but a relative measure to compare combinations within the same strategy.
                """)
                
            # Automatically load generated combinations for the current strategy if not already loaded
            if not st.session_state.combinations_loaded:
                with st.spinner("Loading combinations from database..."):
                    try:
                        # Get combinations for the current strategy
                        db_combinations = database.get_generated_combinations(strategy=strategy_type)
                        
                        if db_combinations:
                            # Store in session state
                            st.session_state.generated_combinations[strategy_type] = db_combinations
                            st.success(f"Successfully loaded {len(db_combinations)} combinations for {strategy_type} strategy!")
                            st.session_state.combinations_loaded = True
                        else:
                            st.info(f"No previously generated combinations found for {strategy_type} strategy. Generate some now!")
                            st.session_state.combinations_loaded = True
                    except Exception as e:
                        st.error(f"Error loading combinations from database: {str(e)}")
                        
            # Add a refresh button to reload combinations from database
            if st.button("Refresh Combinations from Database", key="refresh_combinations"):
                with st.spinner("Refreshing combinations from database..."):
                    try:
                        # Get combinations for the current strategy
                        db_combinations = database.get_generated_combinations(strategy=strategy_type)
                        
                        if db_combinations:
                            # Store in session state
                            st.session_state.generated_combinations[strategy_type] = db_combinations
                            st.success(f"Successfully loaded {len(db_combinations)} combinations for {strategy_type} strategy!")
                            st.rerun()
                        else:
                            st.info(f"No saved combinations found for {strategy_type} strategy in the database.")
                    except Exception as e:
                        st.error(f"Error loading combinations from database: {str(e)}")
            
            if strategy_type in st.session_state.generated_combinations:
                combinations = st.session_state.generated_combinations[strategy_type]
                
                for i, combo in enumerate(combinations):
                    numbers = combo['numbers']
                    stars = combo['stars']
                    score = combo.get('score', 'N/A')
                    strategy_name = combo.get('strategy', strategy_type)
                    
                    # For Multi-Strategy, show which strategy generated each combination
                    if strategy_type == "Multi-Strategy":
                        st.markdown(f"### Combination {i+1} - {strategy_name}")
                    else:
                        st.markdown(f"### Combination {i+1}")
                    
                    # Display main numbers with colored balls
                    st.markdown("<div style='display:flex; gap:10px;'>", unsafe_allow_html=True)
                    for num in sorted(numbers):
                        st.markdown(
                            f"<div style='background-color:#1E88E5; color:white; width:40px; height:40px; "
                            f"border-radius:50%; display:flex; align-items:center; justify-content:center; "
                            f"font-weight:bold;'>{num}</div>",
                            unsafe_allow_html=True
                        )
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Display star numbers with yellow stars
                    st.markdown("<div style='display:flex; gap:10px; margin-top:10px;'>", unsafe_allow_html=True)
                    for star in sorted(stars):
                        st.markdown(
                            f"<div style='background-color:#FFD700; color:#333; width:40px; height:40px; "
                            f"border-radius:50%; display:flex; align-items:center; justify-content:center; "
                            f"font-weight:bold;'>{star}</div>",
                            unsafe_allow_html=True
                        )
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Display combination score/confidence
                    st.markdown(f"**Score/Confidence:** {score if score != 'N/A' else 'N/A'}")
                    
                    # Add delimiter between combinations
                    if i < len(combinations) - 1:
                        st.markdown("---")
                
                # Add export options
                st.subheader("Export Options")
                
                # Convert to DataFrame for easier export
                export_data = []
                for i, combo in enumerate(combinations):
                    numbers_str = ', '.join(map(str, sorted(combo['numbers'])))
                    stars_str = ', '.join(map(str, sorted(combo['stars'])))
                    
                    # For Multi-Strategy, include the strategy that generated each combination
                    if strategy_type == "Multi-Strategy":
                        export_data.append({
                            'Combination': i+1,
                            'Strategy': combo.get('strategy', 'Unknown'),
                            'Numbers': numbers_str,
                            'Stars': stars_str,
                            'Score': combo.get('score', 'N/A')
                        })
                    else:
                        export_data.append({
                            'Combination': i+1,
                            'Numbers': numbers_str,
                            'Stars': stars_str,
                            'Score': combo.get('score', 'N/A')
                        })
                
                export_df = pd.DataFrame(export_data)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download as CSV",
                        data=export_df.to_csv(index=False),
                        file_name=f"euromillions_{strategy_type.lower().replace('/', '_')}.csv",
                        mime="text/csv"
                    )
                with col2:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        export_df.to_excel(writer, sheet_name='Combinations', index=False)
                    excel_data = buffer.getvalue()
                    st.download_button(
                        label="Download as Excel",
                        data=excel_data,
                        file_name=f"euromillions_{strategy_type.lower().replace('/', '_')}.xlsx",
                        mime="application/vnd.ms-excel"
                    )
            else:
                st.info("Generate combinations using the form on the left to see them here.")
    
    # Visualizations tab
    with tabs[3]:
        st.header("Visualizations")
        
        viz_type = st.selectbox(
            "Select Visualization",
            ["Number Heatmap", "Evolution Over Time", "Correlation Analysis", "Winning Numbers Distribution", "Bayesian Probability Updates"]
        )
    
    # Combination Analysis tab
    with tabs[4]:
        st.header("Combination Analysis")
        
        analysis_options = st.selectbox(
            "Select Analysis Type",
            ["Repeated Combinations Check", "Frequent Number Groups", "Frequent Star Combinations"]
        )
        
        if analysis_options == "Repeated Combinations Check":
            st.subheader("Full Combination Repetition Analysis")
            st.write("This analysis checks if any complete Euromillions combination (5 numbers + 2 stars) has ever been repeated in the draw history.")
            
            with st.spinner("Analyzing combination repetitions..."):
                full_analysis = analyze_full_combinations()
                
                # Display results
                st.info(f"Total draws analyzed: {full_analysis['total_draws']}")
                st.info(f"Number of unique combinations: {full_analysis['unique_combinations']}")
                
                if full_analysis['repeated_combinations']:
                    st.success("Found repeated combinations!")
                    for combo, count in full_analysis['repeated_combinations'].items():
                        st.write(f"**{combo}** has appeared {count} times!")
                        repeat_dates = full_analysis['repeated_details'][combo]
                        st.write(f"Dates: {', '.join(str(date) for date in repeat_dates)}")
                else:
                    st.warning("No complete Euromillions combination (5 numbers + 2 stars) has ever repeated in the draw history.")
                    st.write("""
                    This is expected due to the extremely high number of possible combinations:
                    - For 5 numbers from 1-50: 2,118,760 possibilities
                    - Combined with 2 stars from 1-12: 25,425,120 possibilities
                    
                    Even with draws twice a week for decades, the probability of a repeat is extremely low.
                    """)
        
        elif analysis_options == "Frequent Number Groups":
            st.subheader("Frequent Number Group Analysis")
            st.write("This analysis identifies the most frequent number groups (2, 3, or 4 numbers that appear together).")
            
            group_size = st.radio("Select number group size to analyze", [2, 3, 4], horizontal=True)
            
            with st.spinner(f"Analyzing {group_size}-number groups..."):
                group_analysis = analyze_number_combinations(size=group_size)
                
                # Display results
                st.info(f"Total draws analyzed: {group_analysis['total_draws']}")
                
                # Create a table for the results
                data = []
                for combo, count in group_analysis['most_frequent_combinations'][:15]:  # Top 15 only
                    data.append({
                        "Numbers": ', '.join(str(n) for n in combo),
                        "Occurrences": count,
                        "Percentage": f"{(count / group_analysis['total_draws'] * 100):.2f}%"
                    })
                
                result_df = pd.DataFrame(data)
                st.table(result_df)
                
                # Create a bar chart
                fig = px.bar(
                    result_df, 
                    x="Numbers", 
                    y="Occurrences", 
                    title=f"Most Frequent {group_size}-Number Combinations",
                    color="Occurrences",
                    color_continuous_scale="Viridis"
                )
                fig.update_layout(xaxis_title="Number Combination", yaxis_title="Times Drawn Together")
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistical significance
                if group_size == 2:
                    expected_freq = 1 / (50 * 49 / 2) * (5 * 4 / 2) / 5
                elif group_size == 3:
                    expected_freq = 1 / (50 * 49 * 48 / 6) * (5 * 4 * 3 / 6) / 5
                elif group_size == 4:
                    expected_freq = 1 / (50 * 49 * 48 * 47 / 24) * (5 * 4 * 3 * 2 / 24) / 5
                
                expected_count = expected_freq * group_analysis['total_draws']
                
                st.subheader("Statistical Significance")
                st.write(f"If combinations were completely random, each {group_size}-number group would be expected to appear approximately **{expected_count:.2f}** times.")
                
                for combo, count in group_analysis['most_frequent_combinations'][:5]:  # Top 5 only
                    deviation = count / expected_count
                    st.write(f"The group **{', '.join(str(n) for n in combo)}** appears **{deviation:.2f}x** more often than expected by chance.")
        
        elif analysis_options == "Frequent Star Combinations":
            st.subheader("Frequent Star Combinations Analysis")
            st.write("This analysis identifies the most frequent star number combinations.")
            
            with st.spinner("Analyzing star combinations..."):
                star_analysis = analyze_star_combinations()
                
                # Display results
                st.info(f"Total draws analyzed: {star_analysis['total_draws']}")
                
                # Create a table for the results
                data = []
                for combo, count in star_analysis['most_frequent_star_combinations']:
                    data.append({
                        "Stars": ', '.join(str(s) for s in combo),
                        "Occurrences": count,
                        "Percentage": f"{(count / star_analysis['total_draws'] * 100):.2f}%"
                    })
                
                result_df = pd.DataFrame(data)
                st.table(result_df)
                
                # Create a bar chart
                fig = px.bar(
                    result_df.head(10), 
                    x="Stars", 
                    y="Occurrences", 
                    title=f"Most Frequent Star Combinations",
                    color="Occurrences",
                    color_continuous_scale="Reds"
                )
                fig.update_layout(xaxis_title="Star Combination", yaxis_title="Times Drawn Together")
                st.plotly_chart(fig, use_container_width=True)
                
                # Expected frequency
                expected_count = star_analysis['total_draws'] / 66  # 12 choose 2 = 66 combinations
                
                st.subheader("Statistical Significance")
                st.write(f"If combinations were completely random, each star pair would be expected to appear approximately **{expected_count:.2f}** times.")
                
                # Find the top star combo
                top_combo, top_count = star_analysis['most_frequent_star_combinations'][0]
                deviation = top_count / expected_count
                
                st.write(f"The star combination **{', '.join(str(s) for s in top_combo)}** appears **{deviation:.2f}x** more often than expected by chance.")
        
    # Visualizations tab continued
    with tabs[3]:  # Still the visualizations tab
        if viz_type == "Number Heatmap":
            st.subheader("Number Frequency Heatmap")
            
            fig = st.session_state.visualization.plot_number_heatmap()
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            This heatmap visualizes the frequency of each number in the Euromillions draws.
            Darker colors represent higher frequency.
            """)
            
        elif viz_type == "Evolution Over Time":
            st.subheader("Number Frequency Evolution Over Time")
            
            # Allow user to select numbers to visualize
            selected_numbers = st.multiselect(
                "Select numbers to visualize",
                list(range(1, 51)),
                default=[1, 10, 20, 30, 40, 50]
            )
            
            if selected_numbers:
                fig = st.session_state.visualization.plot_frequency_evolution(selected_numbers)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Please select at least one number to visualize its evolution.")
            
        elif viz_type == "Correlation Analysis":
            st.subheader("Number Correlation Analysis")
            
            fig = st.session_state.visualization.plot_number_correlation()
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            This correlation matrix shows relationships between different numbers.
            Positive values (blue) indicate numbers that tend to appear together,
            while negative values (red) indicate numbers that rarely appear together.
            """)
            
            # Show top correlated pairs
            st.subheader("Top Positively Correlated Number Pairs")
            pos_corr = st.session_state.statistics.get_top_correlated_pairs(5, positive=True)
            
            for (num1, num2), corr in pos_corr:
                st.write(f"Numbers **{num1}** and **{num2}**: Correlation = {corr:.3f}")
            
            st.subheader("Top Negatively Correlated Number Pairs")
            neg_corr = st.session_state.statistics.get_top_correlated_pairs(5, positive=False)
            
            for (num1, num2), corr in neg_corr:
                st.write(f"Numbers **{num1}** and **{num2}**: Correlation = {corr:.3f}")
            
        elif viz_type == "Winning Numbers Distribution":
            st.subheader("Winning Numbers Distribution")
            
            dist_subtype = st.radio(
                "Select Distribution Analysis",
                ["Sum Distribution", "Distance Distribution", "Pattern Distribution"]
            )
            
            if dist_subtype == "Sum Distribution":
                fig = st.session_state.visualization.plot_winning_sum_distribution()
                st.plotly_chart(fig, use_container_width=True)
                
                # Show average sum
                avg_sum = st.session_state.statistics.get_average_sum()
                st.metric("Average Sum of Winning Numbers", f"{avg_sum:.2f}")
                
            elif dist_subtype == "Distance Distribution":
                fig = st.session_state.visualization.plot_number_distance_distribution()
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                This chart shows the distribution of distances between consecutive winning numbers (when sorted).
                It helps identify if there are patterns in the spacing of winning numbers.
                """)
                
            elif dist_subtype == "Pattern Distribution":
                fig = st.session_state.visualization.plot_pattern_distribution()
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                This visualization shows the distribution of different patterns in the winning numbers,
                such as sequences, pairs, and isolated numbers.
                """)
                
        elif viz_type == "Bayesian Probability Updates":
            st.subheader("Bayesian Probability Updates Visualization")
            
            st.markdown("""
            This visualization shows how probabilities for selected numbers change through Bayesian updating.
            
            To generate this visualization:
            1. Go to the Prediction tab
            2. Select the Bayesian Model strategy
            3. Configure and generate combinations
            4. Return to this visualization
            """)
            
            # Check if Bayesian model was used
            if hasattr(st.session_state, 'strategies') and hasattr(st.session_state.strategies, 'current_bayesian_model'):
                # Get probability history
                prob_history = st.session_state.strategies.get_bayesian_probability_history()
                
                if prob_history:
                    # Allow user to select which numbers to visualize
                    st.subheader("Select numbers to visualize probability updates")
                    
                    # Number selection
                    number_selection = st.multiselect(
                        "Select main numbers",
                        options=list(range(1, 51)),
                        default=[1, 17, 23, 33, 50]
                    )
                    
                    # Star selection
                    star_selection = st.multiselect(
                        "Select star numbers",
                        options=list(range(1, 13)),
                        default=[2, 8]
                    )
                    
                    # Create figure for number probabilities
                    if number_selection:
                        st.subheader("Main Number Probability Updates")
                        
                        # Create dataframe for plotting
                        number_data = []
                        for num in number_selection:
                            if num in prob_history['numbers']:
                                history = prob_history['numbers'][num]
                                for i, prob in enumerate(history):
                                    number_data.append({
                                        'Step': i,
                                        'Number': f"Number {num}",
                                        'Probability': prob * 100  # Convert to percentage
                                    })
                        
                        if number_data:
                            number_df = pd.DataFrame(number_data)
                            fig = px.line(
                                number_df, 
                                x='Step', 
                                y='Probability', 
                                color='Number',
                                title='Probability Updates for Selected Numbers',
                                markers=True
                            )
                            fig.update_layout(
                                xaxis_title="Update Step (0=Prior, 1=Posterior)",
                                yaxis_title="Probability (%)",
                                yaxis=dict(range=[0, max(number_df['Probability']) * 1.1])
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Explanation based on model parameters
                            if hasattr(st.session_state.strategies.current_bayesian_model, 'prior_type'):
                                prior_type = st.session_state.strategies.current_bayesian_model.prior_type
                                update_method = st.session_state.strategies.current_bayesian_model.update_method
                                
                                st.info(f"This visualization shows how the probabilities change using a **{prior_type}** prior and **{update_method}** updating method.")
                                
                                if update_method == "sequential":
                                    st.markdown("Each step represents the probability after processing one draw in sequence.")
                                elif update_method == "adaptive":
                                    st.markdown("The probabilities are weighted by recency, with recent draws having more influence.")
                                else:
                                    st.markdown("The final probability is calculated using all evidence at once in a batch update.")
                        else:
                            st.warning("No probability history available for the selected numbers.")
                    
                    # Create figure for star probabilities
                    if star_selection:
                        st.subheader("Star Number Probability Updates")
                        
                        # Create dataframe for plotting
                        star_data = []
                        for star in star_selection:
                            if star in prob_history['stars']:
                                history = prob_history['stars'][star]
                                for i, prob in enumerate(history):
                                    star_data.append({
                                        'Step': i,
                                        'Star': f"Star {star}",
                                        'Probability': prob * 100  # Convert to percentage
                                    })
                        
                        if star_data:
                            star_df = pd.DataFrame(star_data)
                            fig = px.line(
                                star_df, 
                                x='Step', 
                                y='Probability', 
                                color='Star',
                                title='Probability Updates for Selected Stars',
                                markers=True
                            )
                            fig.update_layout(
                                xaxis_title="Update Step (0=Prior, 1=Posterior)",
                                yaxis_title="Probability (%)",
                                yaxis=dict(range=[0, max(star_df['Probability']) * 1.1])
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("No probability history available for the selected stars.")
                    
                else:
                    st.warning("No Bayesian probability history available. Generate combinations using the Bayesian model first.")
            else:
                st.warning("Please generate combinations using the Bayesian model strategy first to see probability updates.")
    
    # Generated Combinations tab
    with tabs[6]:  # This is now the correct index
        st.header("All Generated Combinations")
        
        if len(st.session_state.generated_combinations) > 0:
            # Create a tab for each strategy with combinations
            strategy_tabs = st.tabs(list(st.session_state.generated_combinations.keys()))
            
            for i, strategy in enumerate(st.session_state.generated_combinations.keys()):
                with strategy_tabs[i]:
                    st.subheader(f"{strategy} Combinations")
                    
                    combinations = st.session_state.generated_combinations[strategy]
                    
                    # Convert to DataFrame for easier display
                    display_data = []
                    for j, combo in enumerate(combinations):
                        numbers_str = ', '.join(map(str, sorted(combo['numbers'])))
                        stars_str = ', '.join(map(str, sorted(combo['stars'])))
                        display_data.append({
                            'Combination': j+1,
                            'Numbers': numbers_str,
                            'Stars': stars_str,
                            'Score': combo.get('score', 'N/A')
                        })
                    
                    display_df = pd.DataFrame(display_data)
                    st.dataframe(display_df, use_container_width=True)
                    
                    # Add export options
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download as CSV",
                            data=display_df.to_csv(index=False),
                            file_name=f"euromillions_{strategy.lower().replace('/', '_')}.csv",
                            mime="text/csv",
                            key=f"csv_{strategy}"
                        )
                    with col2:
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                            display_df.to_excel(writer, sheet_name='Combinations', index=False)
                        excel_data = buffer.getvalue()
                        st.download_button(
                            label="Download as Excel",
                            data=excel_data,
                            file_name=f"euromillions_{strategy.lower().replace('/', '_')}.xlsx",
                            mime="application/vnd.ms-excel",
                            key=f"excel_{strategy}"
                        )
        else:
            st.info("No combinations have been generated yet. Go to the Strategy Generation tab to create some.")
    
    # My Combinations tab
    with tabs[5]:  # This is the correct index for My Combinations
        st.header("My Combinations")
        
        # Initialize combinations loading state if not already done
        if 'my_combinations_loaded' not in st.session_state:
            st.session_state.my_combinations_loaded = False
        
        # Check if database is available before attempting to load
        if not st.session_state.db_available:
            st.warning("Database is not currently available. Combinations cannot be loaded.")
            st.session_state.my_combinations_loaded = True  # Prevent further loading attempts
            
        # Load all combinations from the database if not already loaded and DB is available
        elif not st.session_state.my_combinations_loaded:
            with st.spinner("Loading all combinations from database..."):
                try:
                    # Get all available strategies from the database
                    all_strategies = []
                    for strat in ['Frequency Strategy', 'Risk/Reward Strategy', 'Coverage Strategy', 'Bayesian Strategy', 'Mixed Strategy']:
                        combos = database.get_generated_combinations(strategy=strat)
                        if combos and len(combos) > 0:
                            all_strategies.append(strat)
                            st.session_state.generated_combinations[strat] = combos
                    
                    if all_strategies:
                        st.success(f"Successfully loaded combinations for {len(all_strategies)} strategies!")
                    st.session_state.my_combinations_loaded = True
                except Exception as e:
                    st.error(f"Error loading combinations: {str(e)}")
                    st.session_state.my_combinations_loaded = True  # Mark as loaded anyway to prevent repeated attempts
        
        # Create sub-tabs for different types of combinations
        my_tabs = st.tabs(["Generated Combinations", "Saved Combinations"])
        
        # Generated Combinations tab
        with my_tabs[0]:
            st.subheader("Generated Combinations")
            
            # Show available strategies that have generated combinations
            available_strategies = list(st.session_state.generated_combinations.keys())
            if available_strategies:
                strategy_selection = st.selectbox(
                    "Select Strategy to View",
                    available_strategies
                )
                
                # Automatically load generated combinations for the selected strategy if not already loaded
                if strategy_selection not in st.session_state.generated_combinations or len(st.session_state.generated_combinations[strategy_selection]) == 0:
                    with st.spinner(f"Loading combinations for {strategy_selection}..."):
                        try:
                            # Get combinations for the selected strategy
                            db_combinations = database.get_generated_combinations(strategy=strategy_selection)
                            
                            if db_combinations:
                                # Store in session state
                                st.session_state.generated_combinations[strategy_selection] = db_combinations
                                st.success(f"Successfully loaded {len(db_combinations)} combinations for {strategy_selection} strategy!")
                            else:
                                st.info(f"No combinations found for {strategy_selection} strategy in the database.")
                        except Exception as e:
                            st.error(f"Error loading combinations from database: {str(e)}")
                
                # Add a refresh button to reload combinations from database
                if st.button("Refresh Combinations from Database", key="refresh_generated"):
                    with st.spinner(f"Refreshing combinations for {strategy_selection}..."):
                        try:
                            # Get combinations for the selected strategy
                            db_combinations = database.get_generated_combinations(strategy=strategy_selection)
                            
                            if db_combinations:
                                # Store in session state
                                st.session_state.generated_combinations[strategy_selection] = db_combinations
                                st.success(f"Successfully loaded {len(db_combinations)} combinations for {strategy_selection} strategy!")
                                st.rerun()
                            else:
                                st.info(f"No combinations found for {strategy_selection} strategy in the database.")
                        except Exception as e:
                            st.error(f"Error loading combinations from database: {str(e)}")
                
                # Display the combinations
                if strategy_selection in st.session_state.generated_combinations and st.session_state.generated_combinations[strategy_selection]:
                    combinations = st.session_state.generated_combinations[strategy_selection]
                    
                    for i, combo in enumerate(combinations):
                        numbers = combo['numbers']
                        stars = combo['stars']
                        score = combo.get('score', 'N/A')
                        
                        st.markdown(f"### Combination {i+1}")
                        
                        # Display main numbers with colored balls
                        st.markdown("<div style='display:flex; gap:10px;'>", unsafe_allow_html=True)
                        for num in sorted(numbers):
                            st.markdown(
                                f"<div style='background-color:#1E88E5; color:white; width:40px; height:40px; "
                                f"border-radius:50%; display:flex; align-items:center; justify-content:center; "
                                f"font-weight:bold;'>{num}</div>",
                                unsafe_allow_html=True
                            )
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Display star numbers with yellow stars
                        st.markdown("<div style='display:flex; gap:10px; margin-top:10px;'>", unsafe_allow_html=True)
                        for star in sorted(stars):
                            st.markdown(
                                f"<div style='background-color:#FFD700; color:#333; width:40px; height:40px; "
                                f"border-radius:50%; display:flex; align-items:center; justify-content:center; "
                                f"font-weight:bold;'>{star}</div>",
                                unsafe_allow_html=True
                            )
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Display combination score/confidence
                        st.markdown(f"**Score/Confidence:** {score if score != 'N/A' else 'N/A'}")
                        
                        # Add delimiter between combinations
                        if i < len(combinations) - 1:
                            st.markdown("---")
                else:
                    st.info("No combinations found for this strategy. Generate some using the Strategy Generation tab.")
            else:
                st.info("You haven't generated any combinations yet. Use the Strategy Generation tab to create some.")
        
        # Saved Combinations tab
        with my_tabs[1]:
            st.subheader("Saved Combinations")
            
            # Initialize session state for saved combinations
            if 'saved_combinations_loaded' not in st.session_state:
                st.session_state.saved_combinations_loaded = False
                
            # Check if database is available before attempting to load
            if not st.session_state.db_available:
                st.warning("Database is not currently available. Saved combinations cannot be loaded.")
                st.session_state.saved_combinations_loaded = True  # Prevent further loading attempts
                if 'saved_combinations' not in st.session_state:
                    st.session_state.saved_combinations = []
            
            # Add a button to load saved combinations from database if DB is available
            elif not st.session_state.saved_combinations_loaded:
                if st.button("Load Saved Combinations from Database"):
                    try:
                        # Get saved combinations from database
                        saved_combos = database.get_user_saved_combinations()
                        if saved_combos:
                            st.session_state.saved_combinations = saved_combos
                            st.session_state.saved_combinations_loaded = True
                            st.success(f"Successfully loaded {len(saved_combos)} saved combinations!")
                        else:
                            st.session_state.saved_combinations = []
                            st.session_state.saved_combinations_loaded = True
                            st.info("No saved combinations found in the database.")
                    except Exception as e:
                        st.error(f"Error loading saved combinations: {str(e)}")
                        st.session_state.saved_combinations = []
                        st.session_state.saved_combinations_loaded = True  # Prevent repeated attempts
            
            # Display two columns: left for creating new saved combinations, right for displaying existing ones
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Save New Combination")
                
                # Form for adding a new saved combination
                with st.form("save_combination_form"):
                    st.markdown("**Main Numbers (1-50)**")
                    rows = 2
                    cols_per_row = 3
                    all_num_inputs = []
                    
                    for row in range(rows):
                        cols = st.columns(cols_per_row if row == 0 else cols_per_row - 1)
                        for i, col in enumerate(cols):
                            with col:
                                idx = row * cols_per_row + i
                                if idx < 5:  # We need 5 numbers total
                                    num = st.number_input(f"Number {idx+1}", min_value=1, max_value=50, key=f"save_num_{idx}")
                                    all_num_inputs.append(num)
                    
                    st.markdown("**Star Numbers (1-12)**")
                    col1, col2 = st.columns(2)
                    with col1:
                        star1 = st.number_input("Star 1", min_value=1, max_value=12, key="save_star_1")
                    with col2:
                        star2 = st.number_input("Star 2", min_value=1, max_value=12, key="save_star_2")
                    
                    # Additional fields
                    strategy = st.text_input("Strategy (optional)", "")
                    notes = st.text_area("Notes (optional)", "")
                    
                    submitted = st.form_submit_button("Save Combination")
                
                if submitted:
                    # First check if database is available
                    if not st.session_state.db_available:
                        st.error("Cannot save combination: Database is not available.")
                    else:
                        # Check for duplicates in the numbers
                        numbers = all_num_inputs
                        stars = [star1, star2]
                        
                        if len(set(numbers)) != 5:
                            st.error("Main numbers must be unique!")
                        elif len(set(stars)) != 2:
                            st.error("Star numbers must be unique!")
                        else:
                            try:
                                # Save to database
                                saved_id = database.save_user_combination(numbers, stars, strategy, notes)
                                
                                # Reload saved combinations to include the new one
                                saved_combos = database.get_user_saved_combinations()
                                st.session_state.saved_combinations = saved_combos
                                st.session_state.saved_combinations_loaded = True
                                
                                st.success("Combination saved successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error saving combination: {str(e)}")
        
        with col2:
            st.subheader("Your Saved Combinations")
            
            if st.session_state.saved_combinations_loaded:
                if hasattr(st.session_state, 'saved_combinations') and st.session_state.saved_combinations:
                    for i, combo in enumerate(st.session_state.saved_combinations):
                        with st.expander(f"Combination {i+1} - Saved on {combo['saved_at']}"):
                            # Display combination details
                            numbers = combo['numbers']
                            stars = combo['stars']
                            
                            # Display main numbers with colored balls
                            st.markdown("<h4>Numbers</h4>", unsafe_allow_html=True)
                            numbers_html = "<div style='display:flex; gap:10px;'>"
                            for num in sorted(numbers):
                                numbers_html += f"<div style='background-color:#1E88E5; color:white; width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold;'>{num}</div>"
                            numbers_html += "</div>"
                            st.markdown(numbers_html, unsafe_allow_html=True)
                                
                            # Display star numbers with yellow stars
                            st.markdown("<h4>Stars</h4>", unsafe_allow_html=True)
                            stars_html = "<div style='display:flex; gap:10px; margin-top:10px;'>"
                            for star in sorted(stars):
                                stars_html += f"<div style='background-color:#FFD700; color:#333; width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold;'>{star}</div>"
                            stars_html += "</div>"
                            st.markdown(stars_html, unsafe_allow_html=True)
                            
                            # Display if it was played and the result
                            played = combo.get('played', False)
                            result = combo.get('result', 'Not played yet')
                            
                            if played:
                                st.success("✓ Played")
                                st.write(f"Result: {result}")
                            else:
                                st.warning("⧖ Not played")
                            
                            # Display strategy and notes
                            if combo.get('strategy'):
                                st.write(f"**Strategy:** {combo['strategy']}")
                            
                            if combo.get('notes'):
                                st.write(f"**Notes:** {combo['notes']}")
                            
                            # Update combination status section
                            st.markdown("### Update Combination")
                            
                            with st.form(key=f"update_form_{combo['id']}"):
                                # Use individual input widgets inside a form
                                played_status = st.checkbox("Mark as Played", value=combo.get('played', False), key=f"played_{combo['id']}")
                                result_text = st.text_input("Result", value=combo.get('result', ''), key=f"result_{combo['id']}")
                                updated_notes = st.text_area("Update Notes", value=combo.get('notes', ''), key=f"notes_{combo['id']}")
                                
                                update_button = st.form_submit_button("Update Combination")
                            
                            if update_button:
                                # First check if database is available
                                if not st.session_state.db_available:
                                    st.error("Cannot update combination: Database is not available.")
                                else:
                                    try:
                                        # Update in database
                                        database.update_user_combination(
                                            combo['id'], 
                                            played=played_status, 
                                            result=result_text, 
                                            notes=updated_notes
                                        )
                                        
                                        # Reload saved combinations
                                        saved_combos = database.get_user_saved_combinations()
                                        st.session_state.saved_combinations = saved_combos
                                        
                                        st.success("Combination updated successfully!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error updating combination: {str(e)}")
                else:
                    st.info("You don't have any saved combinations yet. Use the form on the left to save your first combination.")
            else:
                st.info("Click the 'Load Saved Combinations from Database' button to view your saved combinations.")
                
    # Strategy Testing tab
    with tabs[7]:  # Updated for correct index
        st.header("Strategy A/B Testing")
        
        st.markdown("""
        This section allows you to scientifically compare different prediction strategies 
        to determine which ones perform better based on historical data. The system uses 
        backtesting to evaluate how well each strategy would have performed if used in the past.
        """)
        
        # Initialize session state for strategy testing
        if 'strategy_tester' not in st.session_state:
            st.session_state.strategy_tester = None
            
        if 'test_results' not in st.session_state:
            st.session_state.test_results = None
            
        # Create the tester object if not already created
        if st.session_state.strategy_tester is None and st.session_state.data_loaded:
            try:
                st.session_state.strategy_tester = StrategyTester(
                    data=st.session_state.euromillions_data,
                    statistics=st.session_state.statistics,
                    strategies=st.session_state.strategies
                )
                st.success("Strategy tester initialized successfully!")
            except Exception as e:
                st.error(f"Error initializing strategy tester: {str(e)}")
        
        # Create tabs for testing options
        test_tabs = st.tabs(["Run New Test", "View Test Results"])
        
        # Run New Test tab
        with test_tabs[0]:
            st.subheader("Run Strategy A/B Test")
            
            if st.session_state.strategy_tester is None:
                st.warning("Please load data first to enable strategy testing.")
            else:
                with st.form("ab_test_form"):
                    # Test parameters
                    st.markdown("### Test Configuration")
                    
                    # Time periods
                    col1, col2 = st.columns(2)
                    with col1:
                        test_period = st.slider("Test period (draws)", 10, 100, 30, 
                                               help="Number of most recent draws to use for testing")
                    with col2:
                        training_period = st.slider("Training period (draws)", 100, 500, 200, 
                                                  help="Number of draws to use for training the models")
                    
                    # Strategies to test
                    st.markdown("### Select Strategies to Test")
                    strategies = {
                        "frequency": st.checkbox("Frequency Analysis", value=True),
                        "time_series": st.checkbox("Time Series", value=True),
                        "markov_chain": st.checkbox("Markov Chain", value=True),
                        "stratified": st.checkbox("Stratified Sampling", value=True),
                        "bayesian": st.checkbox("Bayesian Model", value=True),
                        "balanced": st.checkbox("Balanced Mix", value=True),
                        "cognitive_bias": st.checkbox("Anti-Cognitive Bias", value=False),
                        "coverage": st.checkbox("Coverage Optimization", value=False),
                        "risk_reward": st.checkbox("Risk/Reward Optimization", value=False)
                    }
                    
                    # Evaluation metrics
                    st.markdown("### Select Evaluation Metrics")
                    metrics = {
                        "numbers_match_rate": st.checkbox("Number Match Rate", value=True, 
                                                      help="How well the strategies predict the main numbers"),
                        "stars_match_rate": st.checkbox("Star Match Rate", value=True,
                                                     help="How well the strategies predict the star numbers"),
                        "coverage_efficiency": st.checkbox("Coverage Efficiency", value=True,
                                                       help="How efficiently the combinations cover the number space"),
                        "diversity_score": st.checkbox("Diversity Score", value=True,
                                                   help="How diverse the generated combinations are"),
                        "historical_similarity": st.checkbox("Historical Pattern Similarity", value=True,
                                                         help="How similar the combinations are to historical patterns"),
                        "balance_factor": st.checkbox("Balance Factor", value=True,
                                                 help="How well-balanced the combinations are across different properties")
                    }
                    
                    # Test execution parameters
                    st.markdown("### Execution Parameters")
                    col1, col2 = st.columns(2)
                    with col1:
                        num_combinations = st.slider("Combinations per strategy", 5, 50, 10,
                                                  help="Number of combinations to generate for each strategy")
                    with col2:
                        iterations = st.slider("Test iterations", 1, 10, 3,
                                            help="Number of test iterations with different seeds")
                    
                    submitted = st.form_submit_button("Run A/B Test")
                    
                    if submitted:
                        # Get selected strategies and metrics
                        selected_strategies = [key for key, value in strategies.items() if value]
                        selected_metrics = [key for key, value in metrics.items() if value]
                        
                        if not selected_strategies:
                            st.error("Please select at least one strategy to test.")
                        elif not selected_metrics:
                            st.error("Please select at least one evaluation metric.")
                        else:
                            with st.spinner("Running A/B test. This may take a few minutes..."):
                                try:
                                    # Set up test environment
                                    st.session_state.strategy_tester.setup_test_environment(
                                        test_period=test_period,
                                        training_period=training_period
                                    )
                                    
                                    # Run the test
                                    results = st.session_state.strategy_tester.run_ab_test(
                                        strategies_to_test=selected_strategies,
                                        num_combinations=num_combinations,
                                        iterations=iterations,
                                        metrics=selected_metrics
                                    )
                                    
                                    # Store results
                                    st.session_state.test_results = results
                                    st.success("A/B test completed successfully!")
                                    
                                    # Show summary
                                    st.subheader("Test Summary")
                                    st.json(results['summary'])
                                    
                                    # Display rankings
                                    st.subheader("Strategy Rankings")
                                    
                                    # Create a DataFrame for better visualization
                                    ranking_data = []
                                    for strategy, ranks in results['rankings'].items():
                                        row = {
                                            'Strategy': strategy,
                                            'Overall Rank': ranks['overall_rank'],
                                            'Avg. Rank': f"{ranks['average_rank']:.2f}"
                                        }
                                        # Add metric-specific ranks
                                        for metric, rank in ranks['ranks_by_metric'].items():
                                            row[f"{metric}"] = rank
                                        
                                        ranking_data.append(row)
                                    
                                    ranking_df = pd.DataFrame(ranking_data).sort_values('Overall Rank')
                                    st.dataframe(ranking_df)
                                    
                                except Exception as e:
                                    st.error(f"Error running A/B test: {str(e)}")
        
        # View Test Results tab
        with test_tabs[1]:
            st.subheader("Previous Test Results")
            
            # Load results from database
            if st.button("Load Previous Test Results"):
                with st.spinner("Loading test results..."):
                    try:
                        results = database.get_strategy_test_results()
                        if results:
                            st.success(f"Loaded {len(results)} test results!")
                            
                            # Display results
                            for i, result in enumerate(results):
                                with st.expander(f"Test #{result['id']} - {result['test_date']}"):
                                    st.markdown(f"**Strategies Tested:** {', '.join(result['strategies_tested'])}")
                                    st.markdown(f"**Iterations:** {result['iterations']}")
                                    st.markdown(f"**Combinations per Strategy:** {result['num_combinations']}")
                                    
                                    # Create DataFrame for rankings
                                    if 'rankings' in result['results']:
                                        st.subheader("Strategy Rankings")
                                        ranking_data = []
                                        
                                        for strategy, ranks in result['results']['rankings'].items():
                                            row = {
                                                'Strategy': strategy,
                                                'Overall Rank': ranks['overall_rank'],
                                                'Avg. Rank': f"{ranks['average_rank']:.2f}"
                                            }
                                            
                                            # Add metric-specific ranks if available
                                            if 'ranks_by_metric' in ranks:
                                                for metric, rank in ranks['ranks_by_metric'].items():
                                                    row[f"{metric}"] = rank
                                            
                                            ranking_data.append(row)
                                        
                                        if ranking_data:
                                            ranking_df = pd.DataFrame(ranking_data).sort_values('Overall Rank')
                                            st.dataframe(ranking_df)
                                    
                                    # Show summary metrics
                                    if 'summary' in result['results']:
                                        st.subheader("Performance Summary")
                                        st.json(result['results']['summary'])
                        else:
                            st.info("No test results found in the database.")
                    except Exception as e:
                        st.error(f"Error loading test results: {str(e)}")
            
            # If there are results in session state, display them
            if st.session_state.test_results is not None:
                st.subheader("Current Test Results")
                
                # Create visualization for the current test results
                try:
                    results = st.session_state.test_results
                    
                    # Strategy performance by metric
                    st.subheader("Strategy Performance by Metric")
                    
                    # Extract metrics and strategies
                    metrics = results['metrics']
                    strategies = results['strategies_tested']
                    
                    # Show plots for each metric
                    for metric in metrics:
                        metric_data = []
                        
                        for strategy in strategies:
                            # Get mean and std for this strategy and metric
                            mean = results['summary'][strategy][metric]['mean']
                            std = results['summary'][strategy][metric]['std']
                            
                            metric_data.append({
                                'Strategy': strategy,
                                'Value': mean,
                                'Lower': mean - std,
                                'Upper': mean + std
                            })
                        
                        # Create DataFrame
                        df = pd.DataFrame(metric_data)
                        
                        # Display bar chart with error bars
                        st.markdown(f"#### {metric.replace('_', ' ').title()}")
                        
                        fig = px.bar(
                            df, 
                            x='Strategy', 
                            y='Value',
                            error_y=df['Upper'] - df['Value'],
                            error_y_minus=df['Value'] - df['Lower'],
                            title=f"{metric.replace('_', ' ').title()} by Strategy",
                            labels={'Value': 'Mean Value', 'Strategy': 'Strategy'},
                            color='Strategy'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error visualizing test results: {str(e)}")
