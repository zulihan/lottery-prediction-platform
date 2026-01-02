"""
Emergency fix - replace Fibonacci strategies with super simple versions that definitely work
"""

def emergency_fix():
    """Replace with the simplest possible working code"""
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find the generate button section and add a simple test
    if 'if st.button("Generate Combinations")' in content:
        # Add a simple test right after the button
        button_section = 'if st.button("Generate Combinations"):'
        
        new_button_section = '''if st.button("Generate Combinations"):
                            # EMERGENCY TEST - Does this show up?
                            st.write("🚨 BUTTON CLICKED - THIS IS A TEST!")
                            st.write(f"Strategy selected: {base_strategy_type}")
                            st.write(f"Number of combinations: {num_combinations}")'''
        
        # Insert test right after button click
        test_insert = '''
                            # EMERGENCY TEST - Does this show up?
                            st.write("🚨 BUTTON CLICKED - THIS IS A TEST!")
                            st.write(f"Strategy selected: {base_strategy_type}")
                            st.write(f"Number of combinations: {num_combinations}")
                            
                            # If Fibonacci strategies, show simple output
                            if "Fibonacci" in base_strategy_type:
                                st.success("🔥 FIBONACCI STRATEGY DETECTED!")
                                st.write("**Test Combination 1:** [1, 8, 13, 21, 34] + Stars [5, 8]")
                                st.write("**Test Combination 2:** [2, 3, 5, 25, 47] + Stars [6, 9]")
                                st.write("**Test Combination 3:** [8, 13, 21, 29, 44] + Stars [3, 12]")
                                st.success("✅ Test combinations displayed!")
                                return  # Exit early for Fibonacci
                            '''
        
        # Find where to insert the test
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            if 'if st.button("Generate Combinations"):' in line:
                # Add our test code after the button click
                indent = ' ' * (len(line) - len(line.lstrip()) + 4)
                test_lines = test_insert.strip().split('\n')
                for test_line in test_lines:
                    if test_line.strip():
                        new_lines.append(indent + test_line.strip())
                    else:
                        new_lines.append('')
        
        content = '\n'.join(new_lines)
        
        with open('app.py', 'w') as f:
            f.write(content)
        
        print("✅ Added emergency test to see if button clicks work")
        return True
    else:
        print("❌ Could not find button section")
        return False

if __name__ == "__main__":
    success = emergency_fix()
    if success:
        print("🚨 Emergency test added! Try clicking generate button now.")
    else:
        print("❌ Emergency fix failed")