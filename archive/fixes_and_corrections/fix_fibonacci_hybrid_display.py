"""
Add debugging to the Fibonacci-Filtered Hybrid strategy to identify display issues
"""

def add_fibonacci_hybrid_debugging():
    """Add comprehensive debugging to trace the Fibonacci-Filtered Hybrid execution"""
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find the Fibonacci-Filtered Hybrid section and add debugging
    old_start = '''                                elif base_strategy_type == "Fibonacci-Filtered Hybrid":
                                    # Simple Hybrid strategy
                                    st.info("⚡ Generating ultimate hybrid combinations...")'''
    
    new_start = '''                                elif base_strategy_type == "Fibonacci-Filtered Hybrid":
                                    # DEBUG: Comprehensive debugging for Fibonacci-Filtered Hybrid
                                    st.write("🔍 DEBUG: Fibonacci-Filtered Hybrid strategy STARTED!")
                                    st.write(f"🔍 DEBUG: num_combinations = {num_combinations}")
                                    st.write(f"🔍 DEBUG: base_strategy_type = '{base_strategy_type}'")
                                    
                                    # Simple Hybrid strategy
                                    st.info("⚡ Generating ultimate hybrid combinations...")
                                    st.write("🔍 DEBUG: Info message displayed, continuing...")'''
    
    # Also add debugging at key points in the generation process
    old_generation = '''                                    # Generate hybrid combinations
                                    import random
                                    combinations = []'''
    
    new_generation = '''                                    # Generate hybrid combinations
                                    st.write("🔍 DEBUG: About to start generating combinations...")
                                    import random
                                    combinations = []
                                    st.write("🔍 DEBUG: Empty combinations list created")'''
    
    old_loop = '''                                    for i in range(num_combinations):'''
    new_loop = '''                                    st.write(f"🔍 DEBUG: Starting loop for {num_combinations} combinations...")
                                    for i in range(num_combinations):
                                        st.write(f"🔍 DEBUG: Generating combination {i+1}...")'''
    
    old_display = '''                                    # Display results
                                    st.success(f"⚡ Generated {len(combinations)} Fibonacci-Filtered Hybrid combinations!")'''
    
    new_display = '''                                    # Display results
                                    st.write(f"🔍 DEBUG: About to display {len(combinations)} combinations...")
                                    st.write(f"🔍 DEBUG: combinations = {combinations}")
                                    st.success(f"⚡ Generated {len(combinations)} Fibonacci-Filtered Hybrid combinations!")
                                    st.write("🔍 DEBUG: Success message displayed")'''
    
    # Apply all debugging additions
    if old_start in content:
        content = content.replace(old_start, new_start)
        print("✅ Added debugging to strategy start")
    
    if old_generation in content:
        content = content.replace(old_generation, new_generation)
        print("✅ Added debugging to generation start")
    
    if old_loop in content:
        content = content.replace(old_loop, new_loop)
        print("✅ Added debugging to combination loop")
    
    if old_display in content:
        content = content.replace(old_display, new_display)
        print("✅ Added debugging to results display")
    
    # Write the updated content
    with open('app.py', 'w') as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    success = add_fibonacci_hybrid_debugging()
    if success:
        print("🔍 Debugging added to Fibonacci-Filtered Hybrid strategy!")
        print("Now you can see exactly where the execution stops or fails.")
    else:
        print("❌ Failed to add debugging")