# Lottery Prediction Platform

## Overview

This is a comprehensive lottery prediction platform that uses advanced statistical analysis and machine learning techniques to generate optimized number combinations for Euromillions and French Loto. The application combines multiple prediction strategies including frequency analysis, Fibonacci sequences, risk/reward models, Markov chains, and time series analysis to provide users with data-driven lottery predictions.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based web application
- **UI Components**: Interactive dashboards with data visualizations using Plotly and Matplotlib
- **User Interface**: Multi-page application with sidebar navigation for different lottery types
- **Responsive Design**: Wide layout configuration for optimal viewing experience

### Backend Architecture
- **Database**: PostgreSQL 16 for persistent data storage
- **ORM**: SQLAlchemy for database operations with connection pooling and retry logic
- **Data Processing**: Pandas and NumPy for statistical analysis and data manipulation
- **Caching**: Local file-based caching system with pickle serialization for performance optimization

### Data Processing Pipeline
- **Historical Data Analysis**: Processes thousands of historical lottery drawings
- **Statistical Computing**: Frequency analysis, pattern recognition, and trend identification
- **Strategy Engine**: Multiple prediction algorithms working in parallel
- **Result Validation**: Backtesting against historical data for strategy optimization

## Key Components

### Strategy Modules
1. **Risk/Reward Balance Strategy** - Optimizes combinations based on probability distributions
2. **Frequency Analysis Strategy** - Analyzes hot and cold number patterns
3. **Fibonacci Enhanced Strategy** - Uses mathematical sequences for number selection
4. **Markov Chain Model** - Predicts based on sequential number relationships
5. **Time Series Analysis** - Identifies temporal patterns and seasonal trends
6. **Bayesian Inference** - Probabilistic modeling for prediction optimization

### Core Services
- **PredictionStrategies**: Main engine for generating Euromillions combinations
- **FrenchLotoStrategy**: Specialized algorithms for French Loto predictions
- **FrenchLotoStatistics**: Statistical analysis tools for French Loto data
- **FibonacciStrategy**: Mathematical sequence-based prediction methods
- **CombinationAnalysis**: Tools for analyzing and validating number combinations

### Database Schema
- **euromillions_drawings**: Historical Euromillions results (n1-n5, s1-s2, date)
- **french_loto_drawings**: Historical French Loto results (numbers + lucky number)
- **generated_combinations**: User-generated predictions with strategy metadata
- **french_loto_predictions**: French Loto specific predictions

## Data Flow

1. **Data Ingestion**: Historical lottery data is loaded from PostgreSQL database
2. **Statistical Processing**: Multiple analysis engines process the data in parallel
3. **Strategy Application**: Various prediction algorithms generate candidate combinations
4. **Optimization**: Results are filtered and optimized based on performance metrics
5. **Validation**: Backtesting against historical data validates strategy effectiveness
6. **Presentation**: Results are displayed through interactive Streamlit interface

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework for the user interface
- **PostgreSQL**: Primary database for data persistence
- **Pandas/NumPy**: Data analysis and numerical computing
- **Plotly/Matplotlib**: Data visualization and charting
- **SQLAlchemy**: Database ORM and connection management

### Python Libraries
- **psycopg2**: PostgreSQL database adapter
- **scikit-learn**: Machine learning algorithms (potential future use)
- **scipy**: Scientific computing functions
- **pickle**: Data serialization for caching

### System Dependencies
- **Python 3.11**: Runtime environment
- **Cairo/FFmpeg**: Graphics and media processing support
- **GTK3**: GUI toolkit dependencies

## Deployment Strategy

### Platform Configuration
- **Deployment Target**: Autoscale deployment on Replit
- **Runtime**: Python 3.11 with Nix package management
- **Port Configuration**: Main app on port 5000, secondary on port 5001
- **Process Management**: Parallel workflow execution with Streamlit server

### Workflow Management
- **Primary Workflow**: Euromillions Prediction App (port 5000)
- **Secondary Workflow**: Simple Fibonacci Test (port 5001)
- **Execution Mode**: Parallel task execution for multiple lottery types

### Performance Optimization
- **Caching Strategy**: Local file-based caching with 24-hour expiration
- **Connection Pooling**: Database connection management with retry logic
- **Resource Management**: Optimized for autoscale deployment environment

## Changelog

- June 24, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.