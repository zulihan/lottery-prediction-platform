# Results Analysis Documentation

## Overview

The Results Analysis feature allows you to track and analyze the performance of your lottery predictions by comparing them against actual draw results. This comprehensive analysis tool helps you understand which strategies work best and improve your prediction accuracy over time.

## Features

### 1. Add/Update Draw Results

Add actual draw results to the database for comparison with your predictions.

**How to use:**
1. Navigate to the **Results Analysis** tab
2. Click on **"➕ Add New Draw Result"** expander
3. Fill in the form:
   - **Draw Date**: Select the date of the draw
   - **Number 1-5**: Enter the 5 main numbers (1-49)
   - **Lucky Number**: Enter the lucky number (1-10)
4. Click **"✅ Add Draw Result"**

**Validation:**
- All 5 numbers must be unique
- Numbers must be between 1-49
- Lucky number must be between 1-10

### 2. Automatic Prediction Analysis

Once a draw result is added, the system automatically:
- Retrieves all predictions saved before or on the draw date
- Compares each prediction against the actual draw
- Calculates match scores and prize tiers
- Generates performance statistics

### 3. Performance Metrics

The analysis provides several key metrics:

#### Global Statistics
- **Total Predictions**: Number of predictions analyzed
- **Winners**: Number of predictions that won (any prize tier)
- **Win Rate**: Percentage of winning predictions
- **Average Number Matches**: Average number of correct numbers across all predictions
- **Best Result**: Highest match score achieved

#### Strategy Performance
For each strategy used, the system tracks:
- **Average Score**: Mean match score for this strategy
- **Best Score**: Highest match score achieved
- **Count**: Number of predictions using this strategy
- **Average Matches**: Average number of correct numbers
- **Lucky Hits**: Number of times the lucky number was correctly predicted

### 4. French Loto Scoring System

The system uses the official French Loto prize tier structure:

| Rank | Condition | Score | Description |
|------|-----------|-------|-------------|
| Rank 1 | 5 numbers + Lucky | 100 | Jackpot |
| Rank 2 | 5 numbers | 20 | Second tier |
| Rank 3 | 4 numbers + Lucky | 10 | Third tier |
| Rank 4 | 4 numbers | 5 | Fourth tier |
| Rank 5 | 3 numbers + Lucky | 3 | Fifth tier |
| Rank 6 | 3 numbers | 2 | Sixth tier |
| Rank 7 | 2 numbers + Lucky | 2 | Seventh tier |
| Rank 8 | 2 numbers | 1 | Eighth tier |
| Rank 9 | 1 number + Lucky | 1 | Ninth tier |
| No win | Less than above | 0 | No prize |

### 5. Detailed Results View

Each prediction is displayed with:
- **Prediction ID**: Unique identifier
- **Date Generated**: When the prediction was created
- **Predicted Numbers**: The 5 numbers you predicted
- **Predicted Lucky**: The lucky number you predicted
- **Strategy**: Which strategy was used
- **Prediction Score**: Original confidence score (0-100)
- **Number Matches**: How many numbers matched (0-5)
- **Lucky Match**: Whether the lucky number was correct (✅/❌)
- **Result Score**: Calculated match score
- **Prize Tier**: Which rank was achieved

### 6. Filtering Options

Filter results to focus on specific outcomes:

- **Minimum Number Matches**: Show only predictions with at least X number matches (0-5)
- **Show Only Winners**: Display only predictions that won a prize

## Workflow

### Step 1: Generate and Save Predictions

1. Go to **Strategy Generation** tab
2. Select **French Loto**
3. Generate combinations using your preferred strategy
4. Click **"💾 Save"** for each combination you want to track

**Tip**: Save multiple combinations from different strategies to compare their performance.

### Step 2: Wait for the Draw

After the official draw takes place, you'll have the actual winning numbers.

### Step 3: Add the Draw Result

1. Go to **Results Analysis** tab
2. Expand **"➕ Add New Draw Result"**
3. Enter the actual draw numbers
4. Click **"✅ Add Draw Result"**

### Step 4: Review Analysis

The system automatically:
- Compares all your saved predictions
- Calculates match scores
- Generates performance statistics
- Displays detailed results

### Step 5: Analyze Performance

1. Review **Global Statistics** to see overall performance
2. Check **Strategy Performance** to see which strategies work best
3. Use **Detailed Results** to examine individual predictions
4. Apply filters to focus on specific outcomes

## Best Practices

### 1. Save Predictions Before the Draw
- Always save your predictions before the draw date
- The system only analyzes predictions created on or before the draw date

### 2. Use Multiple Strategies
- Generate predictions using different strategies
- Compare their performance to find what works best for you

### 3. Track Over Time
- Add draw results regularly
- Monitor strategy performance trends
- Adjust your approach based on historical data

### 4. Review Strategy Performance
- Focus on strategies with higher average scores
- Consider the balance between average score and win rate
- Some strategies may have lower averages but higher win rates

## Example Use Case

**Scenario**: You want to test 3 different strategies for the next French Loto draw.

1. **Generate Predictions**:
   - Generate 2 combinations using "Risk/Reward Balance"
   - Generate 2 combinations using "Markov Chain Model"
   - Generate 2 combinations using "Frequency Analysis"
   - Save all 6 combinations

2. **Wait for Draw**: The draw happens on Saturday

3. **Add Result**: 
   - Winning numbers: 12, 18, 25, 33, 41
   - Lucky number: 7
   - Add this to the system

4. **Review Results**:
   - See that "Markov Chain Model" had the best average score
   - One prediction from "Risk/Reward Balance" got 4 numbers correct
   - Overall win rate was 50% (3 out of 6 predictions won prizes)

5. **Learn and Improve**:
   - Use "Markov Chain Model" more in future predictions
   - Consider mixing strategies based on performance

## Technical Details

### Database Tables Used

- **french_loto_drawings**: Stores actual draw results
- **french_loto_predictions**: Stores your saved predictions

### Analysis Logic

1. Retrieves the latest draw from `french_loto_drawings`
2. Finds all predictions from `french_loto_predictions` where `date_generated <= draw_date`
3. For each prediction:
   - Parses predicted numbers (stored as dash-separated string)
   - Compares with actual numbers using set intersection
   - Calculates match score based on French Loto rules
   - Determines prize tier

### Performance Considerations

- Analysis is performed on-demand when viewing the Results Analysis tab
- Up to 50 most recent predictions are analyzed by default
- Results are calculated in real-time for accuracy

## Future Enhancements

Planned features:
- **Euromillions Support**: Similar analysis for Euromillions draws
- **Historical Trends**: Track performance over multiple draws
- **Visual Charts**: Graphical representation of strategy performance
- **Export Functionality**: Export results to CSV/Excel
- **Prediction Recommendations**: AI-powered suggestions based on historical performance

## Troubleshooting

### No Draws Found
- **Problem**: "No drawings found in database"
- **Solution**: Add a draw result first using the "Add New Draw Result" form

### No Predictions to Analyze
- **Problem**: "No predictions found for analysis"
- **Solution**: Generate and save some predictions first in the Strategy Generation tab

### Predictions Not Showing
- **Problem**: Predictions not appearing in analysis
- **Solution**: Ensure predictions were saved before the draw date

## Support

For issues or questions:
1. Check that predictions were saved correctly
2. Verify draw results are added with correct date
3. Ensure database connection is working
4. Review error messages in the interface

---

**Last Updated**: 2024
**Version**: 1.0

