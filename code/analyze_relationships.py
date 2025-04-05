# analyze_relationships.py
import pandas as pd
import os

data_dir = "data"
files = [
    "Leases.csv",
    "Major Market Occupancy Data.csv",
    "Price and Availability Data.csv",
    "Unemployment.csv"
]

# Function to count rows in a CSV file efficiently
def count_rows(filepath, chunk_size=100000):
    print(f"Counting rows in {filepath}...")
    total_rows = 0
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        total_rows += len(chunk)
    return total_rows

# Count rows in each file
file_counts = {}
for file in files:
    filepath = os.path.join(data_dir, file)
    try:
        count = count_rows(filepath)
        file_counts[file] = count
        print(f"Total rows in {file}: {count:,}")
    except Exception as e:
        print(f"Error counting rows in {file}: {e}")

print("\n===== COMMON COLUMNS BETWEEN FILES =====")
# Find common columns between files
file_columns = {}
for file in files:
    filepath = os.path.join(data_dir, file)
    df_header = pd.read_csv(filepath, nrows=0)
    file_columns[file] = set(df_header.columns)
    
# Print common columns
for i, (file1, cols1) in enumerate(file_columns.items()):
    for file2, cols2 in list(file_columns.items())[i+1:]:
        common = cols1 & cols2
        if common:
            print(f"\n{file1} and {file2} share {len(common)} columns:")
            for col in sorted(common):
                print(f"- {col}")

# Explore time periods in each dataset
print("\n===== TIME PERIODS COVERED =====")
for file in files:
    filepath = os.path.join(data_dir, file)
    try:
        if 'year' in file_columns[file] and 'quarter' in file_columns[file]:
            # Use chunks to handle large files
            time_data = []
            for chunk in pd.read_csv(filepath, usecols=['year', 'quarter'], chunksize=100000):
                chunk_time = chunk.groupby(['year', 'quarter']).size().reset_index()
                time_data.append(chunk_time)
            
            if time_data:
                time_df = pd.concat(time_data).groupby(['year', 'quarter']).size().reset_index()
                time_df.columns = ['year', 'quarter', 'count']
                
                print(f"\nTime periods in {file}:")
                print(f"Min year: {time_df['year'].min()}, Max year: {time_df['year'].max()}")
                print(f"Number of year-quarter combinations: {len(time_df)}")
                print("First 5 year-quarters:")
                print(time_df.sort_values(['year', 'quarter']).head())
    except Exception as e:
        print(f"Error analyzing time periods in {file}: {e}")