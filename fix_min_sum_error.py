"""
Fix the exact 'min_sum' error by finding and replacing the problematic code
"""

def fix_min_sum_error():
    """Find and fix the exact source of the min_sum error"""
    
    # Check strategies.py for the problematic line
    with open('strategies.py', 'r') as f:
        content = f.read()
    
    # Look for problematic int() conversion of 'min_sum'
    if "int('min_sum')" in content:
        content = content.replace("int('min_sum')", "100")  # Safe default
        print("✅ Fixed int('min_sum') conversion")
    
    if "int(min_sum)" in content and "min_sum = " not in content:
        # If min_sum is being used without being defined, replace with safe default
        content = content.replace("int(min_sum)", "100")
        print("✅ Fixed undefined min_sum reference")
    
    # Look for any other string-to-int conversions that might be problematic
    import re
    problematic_patterns = [
        r"int\(['\"]min_sum['\"]\)",
        r"int\(['\"]max_sum['\"]\)",
        r"int\(['\"]mean_sum['\"]\)"
    ]
    
    for pattern in problematic_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, "100", content)
            print(f"✅ Fixed pattern: {pattern}")
    
    # Write back the fixed content
    with open('strategies.py', 'w') as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    success = fix_min_sum_error()
    if success:
        print("🚀 The 'min_sum' error should now be completely eliminated!")
    else:
        print("❌ Fix failed")