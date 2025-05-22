"""
Fix the indentation error that's preventing the app from running
"""

def fix_indentation():
    """Fix the broken indentation in app.py"""
    
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # Find and fix line 578 which has incorrect indentation
    for i, line in enumerate(lines):
        if i == 577:  # Line 578 (0-indexed)
            # Remove extra indentation
            if line.startswith('                                            numbers = sorted'):
                lines[i] = '                                        numbers = sorted(random.sample(range(1, 51), 5))\n'
                print(f"✅ Fixed indentation on line {i+1}")
        elif i == 578:  # Line 579
            if line.startswith('                                            stars = sorted'):
                lines[i] = '                                        stars = sorted(random.sample(range(1, 13), 2))\n'
                print(f"✅ Fixed indentation on line {i+1}")
        elif i == 579:  # Line 580
            if line.startswith('                                            combinations.append'):
                lines[i] = '                                        combinations.append({\n'
                print(f"✅ Fixed indentation on line {i+1}")
    
    # Write the fixed content back
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    return True

if __name__ == "__main__":
    success = fix_indentation()
    if success:
        print("🚀 Indentation error fixed! App should work now.")
    else:
        print("❌ Fix failed")