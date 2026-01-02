"""
Fix the exact 'min_sum' error in Risk/Reward strategy
"""

def fix_risk_reward_error():
    """Fix the parameter conversion error"""
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find and replace the exact problematic line
    old_line = "risk_level=float(risk_level)"
    new_line = "risk_level=max(1, min(10, int(risk_level * 10)))"
    
    # Replace in Euromillions section only (first occurrence)
    lines = content.split('\n')
    found_euromillions = False
    
    for i, line in enumerate(lines):
        # Look for the Euromillions section
        if 'elif base_strategy_type == "Risk/Reward Balance":' in line and not found_euromillions:
            found_euromillions = True
            # Find the risk_level parameter line within the next 10 lines
            for j in range(i, min(i+10, len(lines))):
                if old_line in lines[j]:
                    lines[j] = lines[j].replace(old_line, new_line)
                    print(f"✅ Fixed Risk/Reward parameter on line {j+1}")
                    break
            break
    
    # Write back the fixed content
    content = '\n'.join(lines)
    with open('app.py', 'w') as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    success = fix_risk_reward_error()
    if success:
        print("🚀 Risk/Reward 'min_sum' error should now be fixed!")
    else:
        print("❌ Fix failed")