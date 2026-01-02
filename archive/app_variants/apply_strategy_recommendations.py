"""
Script to apply strategy recommendations to the main app.py file

This script will modify the app.py file to add strategy recommendations
based on our backtesting results.
"""

import re
import shutil
import os
from strategy_recommendation import get_ordered_strategy_list, get_strategy_info_text

# Create a backup of the original file
print("Creating backup of app.py...")
shutil.copy("app.py", "app.py.backup")

# Read the content of the app.py file
with open("app.py", "r") as f:
    content = f.read()

# Add import for the strategy recommendation module
if "from strategy_recommendation import" not in content:
    import_pattern = r"from combination_analysis import analyze_full_combinations, analyze_number_combinations"
    new_import = (
        "from combination_analysis import analyze_full_combinations, analyze_number_combinations\n"
        "from strategy_recommendation import get_ordered_strategy_list, get_strategy_info_text, get_base_strategy_name"
    )
    content = content.replace(import_pattern, new_import)

# Add info text after strategies initialization for French Loto section
french_loto_strategy_pattern = r"(\s+if strategies:\s+)# Strategy selection"
info_text_replacement = r"\1# Information about strategy performance\n                    st.info(get_strategy_info_text())\n                    \n                    # Strategy selection"
content = re.sub(french_loto_strategy_pattern, info_text_replacement, content)

# Replace the strategy list with the ordered list from our recommendations
strategy_list_pattern = r'                        "Select Strategy",\s+\[\s+(".*?"),\s+(".*?"),\s+(".*?"),\s+(".*?"),\s+(".*?"),\s+(".*?"),\s+(".*?"),\s+(".*?"),\s+(".*?"),\s+(".*?")\s+\]'
ordered_strategies = get_ordered_strategy_list()
formatted_strategies = ',\n                            '.join([f'"{s}"' for s in ordered_strategies])
strategy_list_replacement = f'                        "Select Strategy",\n                        [\n                            {formatted_strategies}\n                        ]'
content = re.sub(strategy_list_pattern, strategy_list_replacement, content)

# Add the strategy name mapping function right after the strategy selection
mapping_function_code = """
                    # Function to process strategy name that might have star symbols
                    base_strategy_type = get_base_strategy_name(strategy_type)
                    """
strategy_type_pattern = r'(\s+strategy_type = st\.selectbox\([^)]+\)\s+)'
content = re.sub(strategy_type_pattern, r'\1' + mapping_function_code, content)

# Replace strategy_type with base_strategy_type in strategy parameter sections
content = content.replace("if strategy_type ==", "if base_strategy_type ==")
content = content.replace("elif strategy_type ==", "elif base_strategy_type ==")

# Write the modified content back to app.py
with open("app.py.updated", "w") as f:
    f.write(content)

print("Updated app.py.updated successfully!")
print("The original file was backed up to app.py.backup")
print("To apply the changes, run: mv app.py.updated app.py")