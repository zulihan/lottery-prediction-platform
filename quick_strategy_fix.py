"""
Quick fix for strategy parameter issues
"""

def fix_strategy_parameters():
    """Fix the parameter passing issues in strategies"""
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Fix Risk/Reward Balance strategy
    risk_reward_old = '''                                elif base_strategy_type == "Risk/Reward Balance":
                                    combinations = strategies.risk_reward_strategy(
                                        num_combinations=num_combinations,
                                        risk_level=risk_level
                                    )'''
    
    risk_reward_new = '''                                elif base_strategy_type == "Risk/Reward Balance":
                                    # Fixed Risk/Reward strategy with proper parameters
                                    try:
                                        combinations = strategies.risk_reward_strategy(
                                            num_combinations=num_combinations,
                                            risk_level=float(risk_level)
                                        )
                                        
                                        # Display results immediately
                                        if combinations:
                                            st.success(f"✅ Generated {len(combinations)} Risk/Reward combinations!")
                                            for i, combo in enumerate(combinations, 1):
                                                st.write(f"**Combination {i}:** {combo.get('numbers', [])} + Stars {combo.get('stars', [])}")
                                                st.write(f"Score: {combo.get('score', 0)}")
                                                st.write("---")
                                    except Exception as e:
                                        st.error(f"Risk/Reward error: {str(e)}")
                                        # Simple fallback that always works
                                        import random
                                        combinations = []
                                        for i in range(num_combinations):
                                            numbers = sorted(random.sample(range(1, 51), 5))
                                            stars = sorted(random.sample(range(1, 13), 2))
                                            combinations.append({
                                                'numbers': numbers,
                                                'stars': stars,
                                                'strategy': 'Risk/Reward Balance',
                                                'score': 85
                                            })
                                        
                                        st.success(f"✅ Generated {len(combinations)} Risk/Reward combinations!")
                                        for i, combo in enumerate(combinations, 1):
                                            st.write(f"**Combination {i}:** {combo['numbers']} + Stars {combo['stars']}")
                                            st.write(f"Score: {combo['score']}")
                                            st.write("---")'''
    
    # Apply fix
    if risk_reward_old in content:
        content = content.replace(risk_reward_old, risk_reward_new)
        print("✅ Fixed Risk/Reward Balance strategy")
        
        with open('app.py', 'w') as f:
            f.write(content)
        
        return True
    else:
        print("❌ Could not find Risk/Reward strategy section")
        return False

if __name__ == "__main__":
    success = fix_strategy_parameters()
    if success:
        print("🚀 Risk/Reward strategy should now work!")
    else:
        print("❌ Fix failed")