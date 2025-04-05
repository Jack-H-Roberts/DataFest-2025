import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# File path 
file_path = 'data/Major Market Occupancy Data.csv'

# Read the CSV file
df = pd.read_csv(file_path)

# Print information about the data for verification
print(f"Data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Number of markets (cities): {df['market'].nunique()}")
print(f"Years range: {df['year'].min()} to {df['year'].max()}")

# Create a time label for x-axis by combining year and quarter
df['time_label'] = df['year'].astype(str) + ' Q' + df['quarter'].astype(str)

# Sort the data by year and quarter to ensure proper timeline
df = df.sort_values(['year', 'quarter'])

# Get unique time labels for x-axis
time_labels = df['time_label'].unique()

# Create a figure with a larger size for better readability
plt.figure(figsize=(14, 8))

# Plot a line for each city with different colors
markets = df['market'].unique()
colors = plt.cm.tab10(np.linspace(0, 1, len(markets)))  # Generate distinct colors

for i, market in enumerate(markets):
    market_data = df[df['market'] == market]
    plt.plot(
        market_data['time_label'], 
        market_data['starting_occupancy_proportion'] * 100,  # Convert to percentage
        marker='o',
        linestyle='-',
        color=colors[i],
        linewidth=2,
        markersize=5,
        label=market
    )

# Set chart title and labels
plt.title('Occupancy Percentage by City Over Time', fontsize=16)
plt.xlabel('Time Period', fontsize=12)
plt.ylabel('Occupancy Percentage (%)', fontsize=12)

# Add a grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Format x-axis labels to be vertical if there are many time periods
if len(time_labels) > 8:
    plt.xticks(rotation=90)

# Add a legend with the city names
plt.legend(title='Cities', bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout to make room for the legend
plt.tight_layout()

# Create directory if it doesn't exist
import os
output_dir = os.path.join('visualizations', 'pngs')
os.makedirs(output_dir, exist_ok=True)

# Save the figure to the specified directory
output_path = os.path.join(output_dir, 'city_occupancy_trend.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"Plot saved successfully to {output_path}")