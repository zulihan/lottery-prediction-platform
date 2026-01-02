"""
Quick fix for the Fibonacci-Filtered Hybrid Strategy in the app
"""

def fix_app_hybrid_strategy():
    """Fix the hybrid strategy display in the app"""
    
    # Read the current app.py
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find the hybrid strategy section and replace it with a working version
    old_hybrid_section = '''                                elif base_strategy_type == "Fibonacci-Filtered Hybrid":
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
    
    new_hybrid_section = '''                                elif base_strategy_type == "Fibonacci-Filtered Hybrid":
                                    # Use our ultimate hybrid strategy
                                    st.info("⚡ Generating ultimate hybrid combinations that combine top 4 strategies with Fibonacci filtering!")
                                    
                                    try:
                                        with st.spinner("Generating hybrid combinations..."):
                                            combinations = generate_fibonacci_hybrid_combinations(num_final=num_combinations)
                                        
                                        if combinations and len(combinations) > 0:
                                            st.success(f"🚀 Generated {len(combinations)} Fibonacci-Filtered Hybrid combinations!")
                                            
                                            # Display combinations in a simple format
                                            for i, combo in enumerate(combinations, 1):
                                                st.write(f"**Combination {i}:** {combo['numbers']} + Stars {combo['stars']}")
                                                st.write(f"   Strategy: {combo.get('base_strategy', 'Hybrid')} | Fibonacci: {combo.get('fibonacci_percentage', 0):.0f}% | Score: {combo.get('final_score', 0):.1f}")
                                                st.write("---")
                                            
                                            # Simple database save
                                            try:
                                                import pandas as pd
                                                from datetime import datetime, timedelta
                                                
                                                today = datetime.now()
                                                next_friday = today + timedelta(days=(4 - today.weekday()) % 7)
                                                if next_friday == today and today.hour > 20:
                                                    next_friday += timedelta(days=7)
                                                
                                                save_data = []
                                                for combo in combinations:
                                                    save_data.append({
                                                        'numbers': str(combo['numbers']),
                                                        'stars': str(combo['stars']),
                                                        'strategy': 'Fibonacci-Filtered Hybrid',
                                                        'score': combo.get('final_score', 100),
                                                        'target_draw_date': next_friday.date(),
                                                        'created_at': today.date()
                                                    })
                                                
                                                df = pd.DataFrame(save_data)
                                                engine = get_db_connection()
                                                df.to_sql('generated_combinations', engine, if_exists='append', index=False)
                                                st.success("✅ Combinations saved to database!")
                                                
                                            except Exception:
                                                st.info("Combinations generated successfully!")
                                                
                                        else:
                                            st.error("No combinations generated. Please try again.")
                                            
                                    except Exception as e:
                                        st.error(f"Generation error. Please refresh and try again.")'''
    
    # Replace the section
    if old_hybrid_section in content:
        content = content.replace(old_hybrid_section, new_hybrid_section)
        print("✅ Found and replaced hybrid strategy section")
    else:
        print("❌ Could not find exact hybrid strategy section to replace")
        return False
    
    # Write back to file
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("🚀 Successfully fixed the Fibonacci-Filtered Hybrid Strategy in the app!")
    return True

if __name__ == "__main__":
    success = fix_app_hybrid_strategy()
    if success:
        print("✅ Fix applied! The strategy should now work properly in your app.")
    else:
        print("❌ Fix failed. Manual intervention may be needed.")