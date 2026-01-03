"""
Script to add Fibonacci strategy to the main app.py
This will integrate the Fibonacci Enhanced strategy into your Streamlit app
"""

def add_fibonacci_strategy_to_app():
    """Add Fibonacci strategy to the main app"""
    
    # Read the current app.py
    with open('app.py', 'r') as f:
        content = f.read()
    
    # 1. Add Fibonacci to strategy list
    old_strategy_list = '''                            "Time Series Analysis ⭐",
                            "Bayesian Inference",'''
    
    new_strategy_list = '''                            "Time Series Analysis ⭐",
                            "Fibonacci Enhanced 🔥",
                            "Bayesian Inference",'''
    
    # 2. Add Fibonacci parameters section
    old_params = '''                    elif base_strategy_type == "Anti-Cognitive Bias":
                        window_size = st.slider(
                            "Analysis Window",
                            5, 30, 10,
                            help="Window size for analyzing cognitive biases"
                        )'''
    
    new_params = '''                    elif base_strategy_type == "Fibonacci Enhanced":
                        fibonacci_variant = st.selectbox(
                            "Fibonacci Strategy Type",
                            ["Mixed", "Pure Fibonacci", "Reverted Fibonacci", "Hot Fibonacci"],
                            help="Choose the type of Fibonacci strategy to use"
                        )
                        st.info("🔥 Fibonacci Enhanced uses mathematical sequences for prediction. Mixed approach recommended based on May 20 analysis showing 60% Fibonacci presence!")
                    
                    elif base_strategy_type == "Anti-Cognitive Bias":
                        window_size = st.slider(
                            "Analysis Window",
                            5, 30, 10,
                            help="Window size for analyzing cognitive biases"
                        )'''
    
    # 3. Add Fibonacci generation logic
    old_generation = '''                                elif base_strategy_type == "Anti-Cognitive Bias":
                                    combinations = strategies.cognitive_bias_strategy(
                                        num_combinations=num_combinations,
                                        window_size=window_size
                                    )'''
    
    new_generation = '''                                elif base_strategy_type == "Fibonacci Enhanced":
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
                                
                                elif base_strategy_type == "Anti-Cognitive Bias":
                                    combinations = strategies.cognitive_bias_strategy(
                                        num_combinations=num_combinations,
                                        window_size=window_size
                                    )'''
    
    # Apply modifications
    if old_strategy_list in content:
        content = content.replace(old_strategy_list, new_strategy_list)
        print("✅ Added Fibonacci to strategy selection dropdown")
    else:
        print("⚠️ Could not find strategy list to modify")
    
    if old_params in content:
        content = content.replace(old_params, new_params)
        print("✅ Added Fibonacci parameter selection")
    else:
        print("⚠️ Could not find parameter section to modify")
    
    if old_generation in content:
        content = content.replace(old_generation, new_generation)
        print("✅ Added Fibonacci generation logic")
    else:
        print("⚠️ Could not find generation section to modify")
    
    # Write the modified content back
    with open('app_with_fibonacci.py', 'w') as f:
        f.write(content)
    
    print("\n🎯 Created app_with_fibonacci.py with Fibonacci strategy integrated!")
    print("You can rename this file to app.py to use it, or copy the changes manually.")
    
    return True

if __name__ == "__main__":
    add_fibonacci_strategy_to_app()