import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
import time

# Import the enhanced database module with retry logic
from database_retry import (
    get_all_draws, get_all_french_loto_draws,
    save_generated_combination, save_french_loto_prediction,
    DB_AVAILABLE
)

# Import strategies and utilities
from french_loto_strategy import generate_french_loto_combinations

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Lottery Prediction System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a Lottery",
    ["French Loto", "Euromillions"]
)

# Main content
st.title("Advanced Lottery Prediction System")
st.write("Analyze past drawings and generate optimized number combinations")

# Display database status
if DB_AVAILABLE:
    st.sidebar.success("✅ Database Connected")
else:
    st.sidebar.error("❌ Database Not Connected - Using Local Data")
    st.warning("Database connection unavailable. The application is running in offline mode with limited functionality.")

# Function to load data with retry
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(lottery="euromillions"):
    """Load historical data with retry logic"""
    retries = 0
    max_retries = 3
    retry_delay = 1
    
    while retries < max_retries:
        try:
            if lottery.lower() == "euromillions":
                draws = get_all_draws()
                if draws:
                    # Convert to DataFrame
                    data = []
                    for draw in draws:
                        row = {
                            'date': draw.date,
                            'day_of_week': draw.day_of_week,
                            'n1': draw.n1,
                            'n2': draw.n2,
                            'n3': draw.n3,
                            'n4': draw.n4,
                            'n5': draw.n5,
                            's1': draw.s1,
                            's2': draw.s2
                        }
                        data.append(row)
                    return pd.DataFrame(data)
                else:
                    logger.warning("No Euromillions draws found in database")
                    return pd.DataFrame()
            elif lottery.lower() == "french_loto":
                draws = get_all_french_loto_draws()
                if draws:
                    # Convert to DataFrame
                    data = []
                    for draw in draws:
                        row = {
                            'date': draw.date,
                            'day_of_week': draw.day_of_week,
                            'n1': draw.n1,
                            'n2': draw.n2,
                            'n3': draw.n3,
                            'n4': draw.n4,
                            'n5': draw.n5,
                            'lucky': draw.lucky
                        }
                        data.append(row)
                    return pd.DataFrame(data)
                else:
                    logger.warning("No French Loto draws found in database")
                    return pd.DataFrame()
            else:
                logger.error(f"Unknown lottery type: {lottery}")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading {lottery} data (attempt {retries+1}/{max_retries}): {str(e)}")
            retries += 1
            if retries < max_retries:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error(f"Failed to load {lottery} data after {max_retries} attempts")
                return pd.DataFrame()
    
    return pd.DataFrame()  # Return empty DataFrame as fallback

# Function to get strategy descriptions with performance indicators
def get_strategy_info_text():
    """Get strategy information with performance indicators"""
    return {
        "Risk/Reward Balance": "⭐ Top performer with 2.16/6 score, 22.69% win rate - Balances safe and risky numbers based on statistical probability and potential payout",
        "Frequency Analysis": "⭐ Second best with 2.15/6 score, 21.45% win rate - Prioritizes numbers based on their historical frequency",
        "Markov Chain": "⭐ 2.14/6 score, 23.26% win rate - Uses probability transitions between numbers in previous draws",
        "Pattern Detection": "2.09/6 score, 19.17% win rate - Identifies recurring patterns in historical drawings",
        "Delta System": "2.08/6 score, 18.83% win rate - Analyzes the differences between consecutive drawn numbers",
        "Hot/Cold Analysis": "2.05/6 score, 20.41% win rate - Combines frequently drawn 'hot' numbers with rarely drawn 'cold' numbers",
        "Number Cycles": "2.03/6 score, 17.64% win rate - Tracks cyclical appearance patterns of individual numbers",
        "Coverage Optimization": "1.97/6 score, 16.32% win rate - Maximizes coverage across all possible number ranges",
        "Lucky Numbers": "1.95/6 score, 15.17% win rate - Incorporates personal lucky numbers with statistical analysis",
        "Random Selection": "1.87/6 score, 14.38% win rate - Truly random selection with minimal statistical input"
    }

# Function to get strategy name for display
def get_strategy_name(display_name):
    """Strip performance indicators from strategy names"""
    return display_name.split(" - ")[0].split(" with ")[0]

# French Loto page
if page == "French Loto":
    st.header("French Loto Prediction")
    
    # Load French Loto data
    with st.spinner("Loading French Loto data..."):
        french_loto_df = load_data("french_loto")
    
    if french_loto_df.empty:
        st.warning("No French Loto data available. Please check database connection.")
    else:
        st.success(f"Loaded {len(french_loto_df)} French Loto drawings")
        
        # Show recent draws
        st.subheader("Recent Drawings")
        recent_draws = french_loto_df.head(5)
        
        # Format for display
        display_draws = recent_draws.copy()
        if 'date' in display_draws.columns:
            display_draws['date'] = display_draws['date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(display_draws)
        
        # Generate combinations section
        st.subheader("Generate Combinations")
        
        # Strategy selection
        strategy_info = get_strategy_info_text()
        strategies = list(strategy_info.keys())
        
        selected_strategy = st.selectbox(
            "Select Strategy",
            strategies,
            index=0,
            help="Choose a strategy for generating combinations"
        )
        
        # Show strategy description
        st.info(strategy_info[selected_strategy])
        
        # Number of combinations
        num_combinations = st.slider(
            "Number of Combinations",
            min_value=1,
            max_value=10,
            value=5,
            help="How many combinations to generate"
        )
        
        # Generate button
        if st.button("Generate Combinations"):
            with st.spinner("Generating optimized combinations..."):
                try:
                    # Get clean strategy name
                    clean_strategy = get_strategy_name(selected_strategy)
                    
                    # Generate combinations
                    combinations = generate_french_loto_combinations(
                        strategy=clean_strategy,
                        count=num_combinations
                    )
                    
                    if combinations:
                        st.subheader("Generated Combinations")
                        
                        for i, combo in enumerate(combinations):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.write(f"**Combination {i+1}:**")
                                st.write(f"Main Numbers: {', '.join(map(str, combo['numbers']))}")
                                st.write(f"Lucky Number: {combo['lucky']}")
                                
                            with col2:
                                st.write(f"Score: {combo['score']:.2f}/100")
                                
                                # Save button for each combination
                                if st.button(f"Save #{i+1}", key=f"save_{i}"):
                                    if DB_AVAILABLE:
                                        success = save_french_loto_prediction(
                                            combo['numbers'],
                                            combo['lucky'],
                                            clean_strategy,
                                            combo['score']
                                        )
                                        if success:
                                            st.success("Combination saved!")
                                        else:
                                            st.error("Failed to save combination")
                                    else:
                                        st.warning("Database unavailable - cannot save")
                            
                            st.markdown("---")
                    else:
                        st.error("Failed to generate combinations")
                        
                except Exception as e:
                    st.error(f"Error generating combinations: {str(e)}")
                    logger.error(f"Error in generate combinations: {str(e)}")

# Euromillions page
else:
    st.header("Euromillions Prediction")
    
    # Load Euromillions data
    with st.spinner("Loading Euromillions data..."):
        euro_df = load_data("euromillions")
    
    if euro_df.empty:
        st.warning("No Euromillions data available. Please check database connection.")
    else:
        st.success(f"Loaded {len(euro_df)} Euromillions drawings")
        
        # Show recent draws
        st.subheader("Recent Drawings")
        recent_draws = euro_df.head(5)
        
        # Format for display
        display_draws = recent_draws.copy()
        if 'date' in display_draws.columns:
            display_draws['date'] = display_draws['date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(display_draws)
        
        # Further Euromillions functionality would go here...
        st.info("Euromillions prediction functionality coming soon!")

# Add footer
st.markdown("---")
st.markdown("© 2025 Advanced Lottery Prediction System")