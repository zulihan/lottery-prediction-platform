"""
Add debugging to identify exactly where the 'min_sum' error is coming from
"""

def add_debugging():
    """Add debugging to trace the exact source of the error"""
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find the Risk/Reward strategy section and add extensive debugging
    old_section = '''                                    try:
                                        # Convert risk_level from 0.0-1.0 slider to 1-10 integer expected by function
                                        risk_level_int = max(1, min(10, int(risk_level * 10)))
                                        combinations = strategies.risk_reward_strategy(
                                            num_combinations=num_combinations,
                                            risk_level=risk_level_int
                                        )'''
    
    new_section = '''                                    try:
                                        # DEBUG: Add extensive debugging
                                        st.write("🔍 DEBUG: Starting Risk/Reward strategy")
                                        st.write(f"🔍 DEBUG: Original risk_level = {risk_level} (type: {type(risk_level)})")
                                        
                                        # Convert risk_level from 0.0-1.0 slider to 1-10 integer expected by function
                                        risk_level_int = max(1, min(10, int(risk_level * 10)))
                                        st.write(f"🔍 DEBUG: Converted risk_level_int = {risk_level_int} (type: {type(risk_level_int)})")
                                        st.write(f"🔍 DEBUG: num_combinations = {num_combinations} (type: {type(num_combinations)})")
                                        
                                        st.write("🔍 DEBUG: About to call strategies.risk_reward_strategy...")
                                        combinations = strategies.risk_reward_strategy(
                                            num_combinations=num_combinations,
                                            risk_level=risk_level_int
                                        )
                                        st.write("🔍 DEBUG: Successfully called strategy function!")'''
    
    if old_section in content:
        content = content.replace(old_section, new_section)
        print("✅ Added debugging to Risk/Reward strategy")
        
        with open('app.py', 'w') as f:
            f.write(content)
        
        return True
    else:
        print("❌ Could not find the exact section to debug")
        return False

if __name__ == "__main__":
    success = add_debugging()
    if success:
        print("🔍 Debugging added! Now we can see exactly where the error occurs.")
    else:
        print("❌ Failed to add debugging")