import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime
import io
import base64
from data_processor import DataProcessor
from statistics import EuromillionsStatistics
from strategies import PredictionStrategies
from visualization import DataVisualization
from utils import get_download_link_csv, get_download_link_excel

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
        if st.button("Load Sample Data"):
            try:
                # Load sample data from the sample_data directory
                data = pd.read_csv("sample_data/sample_euromillions.csv")
                st.session_state.data_processor = DataProcessor(data)
                st.session_state.euromillions_data = st.session_state.data_processor.get_processed_data()
                st.session_state.statistics = EuromillionsStatistics(st.session_state.euromillions_data)
                st.session_state.strategies = PredictionStrategies(st.session_state.statistics)
                st.session_state.visualization = DataVisualization(st.session_state.euromillions_data, st.session_state.statistics)
                st.session_state.data_loaded = True
                st.success("Sample data successfully loaded!")
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
    
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
                        # Update all dependent objects
                        st.session_state.euromillions_data = st.session_state.data_processor.get_processed_data()
                        st.session_state.statistics = EuromillionsStatistics(st.session_state.euromillions_data)
                        st.session_state.strategies = PredictionStrategies(st.session_state.statistics)
                        st.session_state.visualization = DataVisualization(st.session_state.euromillions_data, st.session_state.statistics)
                        st.success("New draw added successfully!")
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
        "Generated Combinations"
    ])
    
    # Data Overview tab
    with tabs[0]:
        st.header("Data Overview")
        
        # Display data summary
        st.subheader("Dataset Information")
        data_info = {
            "Total number of draws": len(st.session_state.euromillions_data),
            "Date range": f"{st.session_state.euromillions_data['date'].min()} to {st.session_state.euromillions_data['date'].max()}",
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
                 "Risk/Reward Optimization", "Bayesian Model", "Markov Chain Model", "Time Series Model", "Anti-Cognitive Bias"]
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
                st.info("This strategy ensures balanced distribution across different number ranges")
                # No specific parameters needed
                
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
                st.info("This strategy uses Bayesian probability theory to predict numbers based on prior probabilities and recent evidence")
                recent_draws_count = st.slider("Recent draws to consider", 5, 50, 20, key="bayes_draws")
                
            elif strategy_type == "Markov Chain Model":
                st.info("This strategy uses Markov chain transition probabilities to predict the next draw based on previous draws")
                lag = st.slider("Lag (number of previous draws to consider)", 1, 5, 1, key="markov_lag")
                
            elif strategy_type == "Time Series Model":
                st.info("This strategy analyzes time series patterns to find cycles and predict numbers due to appear")
                window_size = st.slider("Analysis window size", 5, 30, 10, key="ts_window")
                
            elif strategy_type == "Anti-Cognitive Bias":
                st.info("This strategy generates combinations that avoid common cognitive biases most players have when selecting numbers")
            
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
                                num_combinations=num_combinations
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
                                recent_draws_count=recent_draws_count
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
                        
                        # Store the generated combinations
                        st.session_state.generated_combinations[strategy_type] = combinations
                        st.success(f"Successfully generated {num_combinations} combinations!")
                    except Exception as e:
                        st.error(f"Error generating combinations: {str(e)}")
        
        with col2:
            st.subheader("Generated Combinations")
            
            if strategy_type in st.session_state.generated_combinations:
                combinations = st.session_state.generated_combinations[strategy_type]
                
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
                
                # Add export options
                st.subheader("Export Options")
                
                # Convert to DataFrame for easier export
                export_data = []
                for i, combo in enumerate(combinations):
                    numbers_str = ', '.join(map(str, sorted(combo['numbers'])))
                    stars_str = ', '.join(map(str, sorted(combo['stars'])))
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
            ["Number Heatmap", "Evolution Over Time", "Correlation Analysis", "Winning Numbers Distribution"]
        )
        
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
    
    # Generated Combinations tab
    with tabs[4]:
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
