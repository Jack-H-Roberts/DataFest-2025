import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def space_utlization_bar(market, is_premium_quality):
    # Output filename based on market and quality
    output_filename = f"visualizations/pngs/stacked_bars/{market.replace(' ', '')}{'Premium' if is_premium_quality == 1 else 'Standard'}.png"

    # Read the main CSV file
    file_path = 'data/Cleaned PAD.csv'
    df = pd.read_csv(file_path)

    # Read the inflation data
    inflation_path = 'data/Inflation Q over Q 2019-2024.csv'
    inflation_df = pd.read_csv(inflation_path)

    # Convert numeric columns to appropriate types in main dataframe
    numeric_columns = ['total_space', 'available_space', 'direct_available_space', 
                    'sublet_available_space', 'internal_class_rent', 
                    'direct_internal_class_rent', 'sublet_internal_class_rent']
                    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Make sure is_premium_quality is numeric
    df['is_premium_quality'] = pd.to_numeric(df['is_premium_quality'], errors='coerce')

    # Ensure year columns are integers
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    inflation_df['year'] = pd.to_numeric(inflation_df['year'], errors='coerce').astype('Int64')

    # Handle quarter format differences - ensure both are integers
    df['quarter'] = pd.to_numeric(df['quarter'].astype(str).str.replace('Q', ''), errors='coerce').astype('Int64')
    inflation_df['quarter'] = pd.to_numeric(inflation_df['quarter'], errors='coerce').astype('Int64')

    # Convert inflation data to numeric
    inflation_df['inflation_rate'] = pd.to_numeric(inflation_df['inflation_rate'], errors='coerce')

    # Filter data for selected market and quality
    market_df = df[(df['market'] == market) & (df['is_premium_quality'] == is_premium_quality)].copy()

    # Check if we have data
    if market_df.empty:
        print(f"No data available for {market} with premium quality = {is_premium_quality}")
        exit(0)

    # Sort by year and quarter
    market_df['year_quarter'] = market_df['year'].astype(str) + ' Q' + market_df['quarter'].astype(str)
    market_df = market_df.sort_values(by=['year', 'quarter'])

    # Calculate "Used Space"
    market_df['used_space'] = market_df['total_space'] - market_df['available_space']

    # Fill NaN values with 0 for bar chart data
    for col in ['used_space', 'direct_available_space', 'sublet_available_space']:
        market_df[col] = market_df[col].fillna(0)
        
    # Convert square feet to millions for better display
    mil_factor = 1000000
    for col in ['used_space', 'direct_available_space', 'sublet_available_space', 'total_space', 'available_space']:
        market_df[col] = market_df[col] / mil_factor

    # Calculate "Used Space"
    market_df['used_space'] = market_df['total_space'] - market_df['available_space']

    # Fill NaN values with 0 for bar chart data
    for col in ['used_space', 'direct_available_space', 'sublet_available_space']:
        market_df[col] = market_df[col].fillna(0)
        
    # Merge with inflation data
    market_df = pd.merge(market_df, inflation_df, on=['year', 'quarter'], how='left')

    # Fill any missing inflation rates with 0
    market_df['inflation_rate'] = market_df['inflation_rate'].fillna(0)

    # Apply inflation adjustment to rent prices
    # Create a baseline for inflation adjustment (100% at start)
    # We'll adjust all periods to account for cumulative inflation
    base_inflation = 100.0
    market_df['cumulative_inflation'] = float(base_inflation)  # Properly initialized as float

    # Sort by year and quarter to ensure proper sequence
    market_df = market_df.sort_values(by=['year', 'quarter'])

    # Calculate cumulative inflation factor (convert percentage to multiplicative factor)
    for i in range(1, len(market_df)):
        prev_inflation = market_df['cumulative_inflation'].iloc[i-1]
        current_rate = market_df['inflation_rate'].iloc[i] / 100.0  # Convert % to decimal
        market_df.loc[market_df.index[i], 'cumulative_inflation'] = float(prev_inflation * (1 + current_rate))

    # Apply the inflation adjustment to rent prices
    # Adjust to current period values
    market_df['inflation_factor'] = base_inflation / market_df['cumulative_inflation']
    market_df['direct_rent_adjusted'] = market_df['direct_internal_class_rent'] * market_df['inflation_factor']
    market_df['sublet_rent_adjusted'] = market_df['sublet_internal_class_rent'] * market_df['inflation_factor']

    # Calculate percentages for stacked bar segments
    market_df['total_stacked'] = market_df['used_space'] + market_df['direct_available_space'] + market_df['sublet_available_space']
    market_df['used_space_pct'] = (market_df['used_space'] / market_df['total_stacked'] * 100).round(1)
    market_df['direct_space_pct'] = (market_df['direct_available_space'] / market_df['total_stacked'] * 100).round(1)
    market_df['sublet_space_pct'] = (market_df['sublet_available_space'] / market_df['total_stacked'] * 100).round(1)

    # Create figure and primary axis for bars
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Set up x-axis positions
    x = np.arange(len(market_df['year_quarter']))

    # Create the stacked bar chart with updated colors
    bar_width = 0.8
    p1 = ax1.bar(x, market_df['used_space'], bar_width, label='Used Space', color='#808080',  # Medium gray
                edgecolor='white', linewidth=0.5)
    p2 = ax1.bar(x, market_df['direct_available_space'], bar_width, bottom=market_df['used_space'], 
                label='Direct Space', color='#ADD8E6',  # Light blue
                edgecolor='white', linewidth=0.5)
    bottom_values = market_df['used_space'] + market_df['direct_available_space']
    p3 = ax1.bar(x, market_df['sublet_available_space'], bar_width, bottom=bottom_values, 
                label='Sublet Space', color='#FFCCCB',  # Light red
                edgecolor='white', linewidth=0.5)

    # Add percentage labels to each segment of the bars (now rotated)
    for i, value in enumerate(market_df['used_space']):
        if value > 0:  # Only add labels if the space has a value
            height = value / 2  # Position label in middle of segment
            ax1.text(i, height, f"{market_df['used_space_pct'].iloc[i]}%", 
                    ha='center', va='center', color='white', fontweight='bold', rotation=90)
            
    for i, value in enumerate(market_df['direct_available_space']):
        if value > 0:
            height = market_df['used_space'].iloc[i] + value / 2
            ax1.text(i, height, f"{market_df['direct_space_pct'].iloc[i]}%", 
                    ha='center', va='center', color='white', fontweight='bold', rotation=90)
            
    for i, value in enumerate(market_df['sublet_available_space']):
        if value > 0:
            height = bottom_values.iloc[i] + value / 2
            ax1.text(i, height, f"{market_df['sublet_space_pct'].iloc[i]}%", 
                    ha='center', va='center', color='white', fontweight='bold', rotation=90)

    # Create secondary axis for line charts
    ax2 = ax1.twinx()

    # Plot the line charts with updated colors
    ln1 = ax2.plot(x, market_df['direct_rent_adjusted'], marker='o', linestyle='-', 
                color='#00008B', linewidth=2, label='Direct Rent Price (Inflation Adj.)')  # Dark blue
    ln2 = ax2.plot(x, market_df['sublet_rent_adjusted'], marker='s', linestyle='--', 
                color='#8B0000', linewidth=2, label='Sublet Rent Price (Inflation Adj.)')  # Dark red

    # Set labels and title
    ax1.set_xlabel('Year-Quarter', fontsize=12, labelpad=20)  # Added more padding
    ax1.set_ylabel('Space (Million Square Feet)', fontsize=12)  # Updated to millions
    ax2.set_ylabel('Rent ($ per Square Foot)', fontsize=12)
    quality_text = "Premium Quality" if is_premium_quality == 1 else "Standard Quality"
    plt.title(f'{market} {quality_text} Space Utilization and Inflation-Adjusted Rental Prices', fontsize=14)

    # Set x-axis tick labels to year-quarter
    ax1.set_xticks(x)
    ax1.set_xticklabels(market_df['year_quarter'], rotation=45, ha='right')

    # Format y-axis to use comma separators for thousands
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.2f}'))  # Show 2 decimal places for millions
    ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:.2f}'))

    # Add gridlines for better readability
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Ensure both axes start at 0
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)

    # Combine legends from both axes
    bars = [p1, p2, p3]
    lines = ln1 + ln2
    labels = [b.get_label() for b in bars] + [l.get_label() for l in lines]
    ax1.legend(bars + lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.22),  # Added more space
            fancybox=True, shadow=True, ncol=5)

    # Combine legends from both axes
    bars = [p1, p2, p3]
    lines = ln1 + ln2
    labels = [b.get_label() for b in bars] + [l.get_label() for l in lines]
    ax1.legend(bars + lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
            fancybox=True, shadow=True, ncol=5)

    # Adjust layout
    plt.tight_layout()

    # Save the figure
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Chart has been created and saved as '{output_filename}'")