import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# Set up dark mode theme
plt.style.use('dark_background')
dark_bg_color = '#1C1C1E'  # Discord/Dracula-like dark background
text_color = 'white'

# Load the data
df = pd.read_csv("data/Cleaned PAD.csv")

# Filter for premium quality properties
premium_df = df[df['is_premium_quality'] == 1].copy()

# Create a new column for year_quarter for easier grouping
premium_df.loc[:, 'year_quarter'] = premium_df['year'].astype(str) + '-Q' + premium_df['quarter'].astype(str)

# Create a list of all year_quarter combinations for sorting
year_quarters = sorted(premium_df['year_quarter'].unique())

# Print available date range in dataset
print(f"Available date range in dataset: {year_quarters[0]} to {year_quarters[-1]}")

# Calculate the weighted average national direct rent for each quarter and year
national_avg_results = []
for yq in year_quarters:
    subset = premium_df[premium_df['year_quarter'] == yq]
    numerator = np.sum(subset['direct_available_space'] * subset['direct_internal_class_rent'])
    denominator = np.sum(subset['direct_available_space'])
    avg = numerator / denominator if denominator > 0 else np.nan
    national_avg_results.append({'year_quarter': yq, 'avg_national_direct_rent': avg})

national_avg_df = pd.DataFrame(national_avg_results)

# Merge the national average back to the premium dataframe
premium_df = pd.merge(premium_df, national_avg_df, on='year_quarter')

# Calculate each market's direct rent relative to the national average
premium_df['relative_direct_rent'] = premium_df['direct_internal_class_rent'] / premium_df['avg_national_direct_rent']

# List of all markets
markets = [
    "Atlanta", "Austin", "Baltimore", "Boston", "Charlotte", "Chicago Suburbs",
    "Dallas-Ft. Worth", "Denver-Boulder", "Detroit", "Houston", "Los Angeles",
    "Nashville", "Manhattan", "Northern New Jersey", "Northern Virginia", 
    "Orange County (CA)", "Philadelphia", "Phoenix", "Raleigh-Durham", 
    "Salt Lake City", "San Diego", "San Francisco", "Seattle", "South Bay", 
    "South Florida", "Suburban Maryland", "Tampa"
]

# Updated list of highlighted markets
highlighted_markets = ["Manhattan", "San Francisco", "Detroit", "Baltimore", "South Bay", "Boston", "South Florida"]

# Filter for only the markets we want to plot
plot_df = premium_df[premium_df['market'].isin(markets)]

# Create the plot with dark background
plt.figure(figsize=(18, 10))
fig = plt.gcf()
ax = plt.gca()
fig.patch.set_facecolor(dark_bg_color)
ax.set_facecolor(dark_bg_color)

# Define color palette for highlighted markets
highlighted_colors = ['#FF5555', '#50FA7B', '#8BE9FD', '#FF79C6', '#BD93F9']

# Add a horizontal line at y=1 (national average)
plt.axhline(y=1, color='#F8F8F2', linestyle='-', linewidth=2.5, alpha=0.8, label='National Average')

# Plot all non-highlighted markets in grey first (so they're in the background)
for market in markets:
    if market not in highlighted_markets:
        market_data = plot_df[plot_df['market'] == market]
        
        # Skip if market has no data
        if market_data.empty:
            continue
        
        # Sort by year_quarter to ensure proper line connectivity
        market_data = market_data.sort_values('year_quarter')
        
        # Convert year_quarter to numeric indices for plotting
        x_indices = [year_quarters.index(yq) for yq in market_data['year_quarter']]
        
        # Plot in light grey, without adding to legend
        plt.plot(x_indices, market_data['relative_direct_rent'].values, 
                 color='#666666', alpha=0.3, linewidth=1.0)

# Now plot highlighted markets with distinct colors
for i, market in enumerate(highlighted_markets):
    market_data = plot_df[plot_df['market'] == market]
    
    # Skip if market has no data
    if market_data.empty:
        continue
    
    # Sort by year_quarter to ensure proper line connectivity
    market_data = market_data.sort_values('year_quarter')
    
    # Convert year_quarter to numeric indices for plotting
    x_indices = [year_quarters.index(yq) for yq in market_data['year_quarter']]
    
    # Plot with a distinct color from our palette
    plt.plot(x_indices, market_data['relative_direct_rent'].values, 
             color=highlighted_colors[i % len(highlighted_colors)], 
             linewidth=2.0, 
             label=market)

# Add a vertical line for COVID-19 (around Q1 2020)
if '2020-Q1' in year_quarters:
    idx = year_quarters.index('2020-Q1')
    plt.axvline(x=idx, color='#FF5555', linestyle='--', 
                linewidth=1.5, alpha=0.7, label='COVID-19 Start (Q1 2020)')

# Customize the plot
plt.title('Market Direct Rent Relative to National Average (Premium Properties)', 
          fontsize=16, color=text_color)
plt.xlabel('Year-Quarter', fontsize=14, color=text_color)
plt.ylabel('Relative Direct Rent (National Avg = 1)', fontsize=14, color=text_color)

# Set grid for horizontal lines only
plt.grid(True, axis='y', linestyle='--', alpha=0.3, color='#666666')
plt.grid(False, axis='x')

# Update tick colors to white
plt.tick_params(axis='both', colors=text_color)
for spine in ax.spines.values():
    spine.set_color(text_color)

# Fix the quarter format - Convert from YYYY-QQ# to YYYY-Q#
formatted_labels = []
for yq in year_quarters:
    # Check if the format is YYYY-QQ#
    if "QQ" in yq:
        year, quarter = yq.split('-QQ')
        formatted_labels.append(f"{year}-Q{quarter}")
    else:
        # If already in YYYY-Q# format or some other format
        formatted_labels.append(yq)

plt.xticks(range(len(year_quarters)), 
           formatted_labels, 
           rotation=45, ha='right', color=text_color)

# Add legend - only include highlighted markets and national average
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles, labels, loc='upper left', bbox_to_anchor=(1.01, 1), 
           borderaxespad=0., fontsize=12, facecolor=dark_bg_color, edgecolor='gray',
           labelcolor=text_color)

# Adjust layout
plt.tight_layout()

# Save the figure to the specified path
plt.savefig('visualizations/pngs/relative_direct_rent.png', 
            dpi=300, bbox_inches='tight', facecolor=dark_bg_color)

# Show plot
plt.show()