import pandas as pd
import numpy as np
import base64
import io

def get_download_link_csv(df, filename, link_text="Download CSV"):
    """
    Generate a download link for a pandas DataFrame as a CSV file.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be downloaded
    filename : str
        The name of the file to be downloaded
    link_text : str
        The text to display in the download link
    
    Returns:
    --------
    str
        HTML code for a download link
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def get_download_link_excel(df, filename, link_text="Download Excel"):
    """
    Generate a download link for a pandas DataFrame as an Excel file.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be downloaded
    filename : str
        The name of the file to be downloaded
    link_text : str
        The text to display in the download link
    
    Returns:
    --------
    str
        HTML code for a download link
    """
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.close()
    output.seek(0)
    excel_data = output.read()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def calculate_probability_score(numbers, stars, freq_data, star_freq_data):
    """
    Calculate a probability score for a combination based on frequency data.
    
    Parameters:
    -----------
    numbers : list
        List of main numbers (1-50)
    stars : list
        List of star numbers (1-12)
    freq_data : pandas.Series
        Frequency data for main numbers
    star_freq_data : pandas.Series
        Frequency data for star numbers
    
    Returns:
    --------
    float
        Probability score (0-100)
    """
    # Calculate average frequency for numbers
    num_avg_freq = sum(freq_data[n] for n in numbers) / len(numbers)
    
    # Calculate average frequency for stars
    star_avg_freq = sum(star_freq_data[s] for s in stars) / len(stars)
    
    # Combine with a 70/30 weight (arbitrary but reasonable)
    combined_score = (0.7 * num_avg_freq) + (0.3 * star_avg_freq)
    
    # Normalize to 0-100 scale
    normalized_score = combined_score * 100
    
    return round(normalized_score, 2)

def calculate_markov_score(numbers, transition_matrix):
    """
    Calculate a score based on Markov transition probabilities.
    
    Parameters:
    -----------
    numbers : list
        List of main numbers (1-50)
    transition_matrix : pandas.DataFrame
        Markov transition matrix
    
    Returns:
    --------
    float
        Markov score (0-100)
    """
    # Sort numbers to check transitions
    sorted_numbers = sorted(numbers)
    
    # Calculate transition probabilities
    transition_probs = []
    for i in range(len(sorted_numbers) - 1):
        from_num = sorted_numbers[i]
        to_num = sorted_numbers[i + 1]
        transition_probs.append(transition_matrix.loc[from_num, to_num])
    
    # Average transition probability
    avg_prob = sum(transition_probs) / len(transition_probs) if transition_probs else 0
    
    # Normalize to 0-100 scale
    normalized_score = avg_prob * 100
    
    return round(normalized_score, 2)

def validate_euromillions_numbers(numbers, stars):
    """
    Validate if a set of numbers is valid for Euromillions.
    
    Parameters:
    -----------
    numbers : list
        List of main numbers (should be 5 unique numbers between 1-50)
    stars : list
        List of star numbers (should be 2 unique numbers between 1-12)
    
    Returns:
    --------
    bool
        True if valid, False otherwise
    """
    # Check length
    if len(numbers) != 5 or len(stars) != 2:
        return False
    
    # Check uniqueness
    if len(set(numbers)) != 5 or len(set(stars)) != 2:
        return False
    
    # Check ranges
    if not all(1 <= n <= 50 for n in numbers) or not all(1 <= s <= 12 for s in stars):
        return False
    
    return True

def get_number_statistics_summary(statistics, number):
    """
    Get a summary of statistics for a specific number.
    
    Parameters:
    -----------
    statistics : EuromillionsStatistics
        Statistics object
    number : int
        The number to analyze (1-50)
    
    Returns:
    --------
    dict
        Dictionary with statistical summary
    """
    # Get basic statistics
    stats = statistics.get_number_statistics(number)
    
    # Get frequency data
    freq_data = statistics.get_frequency()
    frequency_rank = sorted(freq_data.items(), key=lambda x: x[1], reverse=True)
    rank = next(i for i, (num, _) in enumerate(frequency_rank) if num == number) + 1
    
    # Get day of week distribution
    dow_data = statistics.get_day_of_week_distribution(number)
    best_day = dow_data.idxmax() if dow_data is not None else "N/A"
    
    # Create summary
    summary = {
        "number": number,
        "frequency": stats["frequency"],
        "rank": rank,
        "occurrences": stats["occurrences"],
        "average_gap": stats["avg_gap"],
        "draws_since_last": stats["draws_since_last"],
        "best_day": best_day
    }
    
    # Add cyclic pattern if identified
    if stats.get("cyclic_pattern"):
        summary["cyclic_pattern"] = stats["cyclic_pattern"]
    
    return summary
