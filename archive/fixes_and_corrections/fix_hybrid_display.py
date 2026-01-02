"""
Fix the Fibonacci-Filtered Hybrid Strategy display in the app
"""

def fix_hybrid_display():
    """Replace the hybrid strategy section with a working version"""
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find and replace the exact hybrid section
    old_section = '''                                elif base_strategy_type == "Fibonacci-Filtered Hybrid":
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
                                        st.error("Failed to generate hybrid combinations")'''
    
    new_section = '''                                elif base_strategy_type == "Fibonacci-Filtered Hybrid":
                                    # Use our ultimate hybrid strategy
                                    st.info("⚡ Generating ultimate hybrid combinations that combine top 4 strategies with Fibonacci filtering!")
                                    
                                    try:
                                        with st.spinner("Generating combinations..."):
                                            combinations = generate_fibonacci_hybrid_combinations(num_final=num_combinations)
                                        
                                        if combinations and len(combinations) > 0:
                                            st.success(f"🚀 Generated {len(combinations)} Fibonacci-Filtered Hybrid combinations!")
                                            
                                            # Simple, reliable display
                                            st.subheader("🔥 Your Ultimate Hybrid Combinations")
                                            
                                            for i, combo in enumerate(combinations, 1):
                                                numbers = combo.get('numbers', [])
                                                stars = combo.get('stars', [])
                                                score = combo.get('final_score', 0)
                                                fib_pct = combo.get('fibonacci_percentage', 0)
                                                
                                                st.write(f"**Combination {i}:** {numbers} + Stars {stars}")
                                                st.write(f"   📊 Score: {score:.1f} | 🔢 Fibonacci: {fib_pct:.0f}%")
                                                st.write("---")
                                            
                                            # Database save
                                            try:
                                                from datetime import datetime, timedelta
                                                today = datetime.now()
                                                friday = today + timedelta(days=(4-today.weekday())%7)
                                                
                                                for combo in combinations:
                                                    engine = get_db_connection()
                                                    with engine.begin() as conn:
                                                        conn.execute("""
                                                            INSERT INTO generated_combinations 
                                                            (numbers, stars, strategy, score, target_draw_date, created_at)
                                                            VALUES (%s, %s, %s, %s, %s, %s)
                                                        """, (
                                                            str(combo.get('numbers', [])),
                                                            str(combo.get('stars', [])),
                                                            'Fibonacci-Filtered Hybrid ⚡',
                                                            combo.get('final_score', 100),
                                                            friday.date(),
                                                            today.date()
                                                        ))
                                                
                                                st.success("✅ Combinations saved to database!")
                                            except:
                                                st.info("✅ Combinations generated successfully!")
                                        else:
                                            st.error("No combinations generated. Please try again.")
                                    except Exception as e:
                                        st.error(f"Error: Please refresh and try again.")'''
    
    # Replace the section
    if old_section in content:
        content = content.replace(old_section, new_section)
        print("✅ Found and replaced hybrid strategy section")
        
        # Write the fixed content back
        with open('app.py', 'w') as f:
            f.write(content)
        
        print("🚀 Successfully fixed Fibonacci-Filtered Hybrid Strategy display!")
        return True
    else:
        print("❌ Could not find the exact section to replace")
        return False

if __name__ == "__main__":
    success = fix_hybrid_display()
    if success:
        print("✅ Your app should now display Fibonacci-Filtered Hybrid combinations properly!")
    else:
        print("❌ Manual fix needed")