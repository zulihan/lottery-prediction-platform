"""
Script to add the Fibonacci-Filtered Hybrid Strategy to the main app.py
"""

def add_hybrid_strategy():
    """Add the hybrid strategy to the app"""
    
    # Read the current app.py file
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Add the hybrid strategy to the strategy list in Euromillions section
    euromillions_strategies = '''                        [
                            "Risk/Reward Balance ⭐",
                            "Frequency Analysis ⭐",
                            "Markov Chain Model ⭐",
                            "Time Series Analysis ⭐",
                            "Fibonacci Enhanced 🔥",
                            "Bayesian Inference",'''
    
    new_euromillions_strategies = '''                        [
                            "Risk/Reward Balance ⭐",
                            "Frequency Analysis ⭐",
                            "Markov Chain Model ⭐",
                            "Time Series Analysis ⭐",
                            "Fibonacci Enhanced 🔥",
                            "Fibonacci-Filtered Hybrid ⚡",
                            "Bayesian Inference",'''
    
    # Replace the first occurrence (Euromillions section)
    if euromillions_strategies in content:
        content = content.replace(euromillions_strategies, new_euromillions_strategies, 1)
        print("✅ Added Fibonacci-Filtered Hybrid Strategy to Euromillions section")
    
    # Add the hybrid strategy to French Loto section too
    french_loto_strategies = '''                        [
                            "Risk/Reward Balance ⭐",
                            "Frequency Analysis ⭐",
                            "Markov Chain Model ⭐",
                            "Time Series Analysis ⭐",
                            "Fibonacci Enhanced 🔥",
                            "Bayesian Inference",'''
    
    new_french_loto_strategies = '''                        [
                            "Risk/Reward Balance ⭐",
                            "Frequency Analysis ⭐",
                            "Markov Chain Model ⭐",
                            "Time Series Analysis ⭐",
                            "Fibonacci Enhanced 🔥",
                            "Fibonacci-Filtered Hybrid ⚡",
                            "Bayesian Inference",'''
    
    # Replace the second occurrence (French Loto section)
    if french_loto_strategies in content:
        content = content.replace(french_loto_strategies, new_french_loto_strategies, 1)
        print("✅ Added Fibonacci-Filtered Hybrid Strategy to French Loto section")
    
    # Add the code to handle the hybrid strategy in Euromillions generation
    fibonacci_enhanced_code = '''                                elif base_strategy_type == "Fibonacci Enhanced":
                                    # Use our new Fibonacci strategy
                                    combinations = generate_fibonacci_combinations(
                                        strategy_variant=fibonacci_variant,
                                        num_combinations=num_combinations
                                    )
                                    
                                    # Save to database
                                    try:
                                        engine = get_db_connection()
                                        success, result = save_fibonacci_to_database(combinations, engine)
                                        if success:
                                            st.success(f"✅ Saved {result} Fibonacci combinations to database!")
                                    except Exception as e:
                                        st.info("Combinations generated successfully (database save optional)")
                                
                                elif base_strategy_type == "Anti-Cognitive Bias":'''
    
    new_fibonacci_code = '''                                elif base_strategy_type == "Fibonacci Enhanced":
                                    # Use our new Fibonacci strategy
                                    combinations = generate_fibonacci_combinations(
                                        strategy_variant=fibonacci_variant,
                                        num_combinations=num_combinations
                                    )
                                    
                                    # Save to database
                                    try:
                                        engine = get_db_connection()
                                        success, result = save_fibonacci_to_database(combinations, engine)
                                        if success:
                                            st.success(f"✅ Saved {result} Fibonacci combinations to database!")
                                    except Exception as e:
                                        st.info("Combinations generated successfully (database save optional)")
                                
                                elif base_strategy_type == "Fibonacci-Filtered Hybrid":
                                    # Use our ultimate hybrid strategy
                                    st.info("⚡ Generating ultimate hybrid combinations that combine top 4 strategies with Fibonacci filtering!")
                                    combinations = generate_fibonacci_hybrid_combinations(num_final=num_combinations)
                                    
                                    # Display the hybrid combinations
                                    if combinations:
                                        st.success(f"🚀 Generated {len(combinations)} Fibonacci-Filtered Hybrid combinations!")
                                        
                                        # Create display DataFrame
                                        display_data = []
                                        for i, combo in enumerate(combinations, 1):
                                            display_data.append({
                                                'Combination': i,
                                                'Numbers': str(combo['numbers']),
                                                'Stars': str(combo['stars']),
                                                'Strategy': combo['base_strategy'],
                                                'Fibonacci %': f"{combo['fibonacci_percentage']:.0f}%",
                                                'Score': f"{combo['final_score']:.1f}"
                                            })
                                        
                                        df_display = pd.DataFrame(display_data)
                                        st.dataframe(df_display, use_container_width=True)
                                        
                                        st.success("✅ All combinations automatically saved to database for tracking!")
                                    else:
                                        st.error("Failed to generate hybrid combinations")
                                
                                elif base_strategy_type == "Anti-Cognitive Bias":'''
    
    # Replace the Fibonacci Enhanced handling code
    if fibonacci_enhanced_code in content:
        content = content.replace(fibonacci_enhanced_code, new_fibonacci_code)
        print("✅ Added Fibonacci-Filtered Hybrid Strategy generation code to Euromillions")
    
    # Write the updated content back to app.py
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("🚀 Successfully added Fibonacci-Filtered Hybrid Strategy to app.py!")
    print("The hybrid strategy is now available in both Euromillions and French Loto sections!")

if __name__ == "__main__":
    add_hybrid_strategy()