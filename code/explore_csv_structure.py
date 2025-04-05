# explore_csv_structure.py
import pandas as pd
import os

data_dir = "data"
files = [
    "Leases.csv",
    "Major Market Occupancy Data.csv",
    "Price and Availability Data.csv",
    "Unemployment.csv"
]

def examine_csv_structure(filename, nrows=5):
    """Examine the structure of a CSV file"""
    filepath = os.path.join(data_dir, filename)
    print(f"\n===== Examining CSV file: {filename} =====")
    
    # Read just the header to get column names
    df_header = pd.read_csv(filepath, nrows=0)
    print(f"Number of columns: {len(df_header.columns)}")
    print("Column names:")
    for col in df_header.columns:
        print(f"- {col}")
    
    # Read a few rows to see the data
    print(f"\nReading {nrows} sample rows...")
    df_sample = pd.read_csv(filepath, nrows=nrows)
    print("\nData types:")
    print(df_sample.dtypes)
    print("\nSample data:")
    print(df_sample.head())
    
    return df_header.columns.tolist()

# Examine each CSV file
for file in files:
    try:
        examine_csv_structure(file)
    except Exception as e:
        print(f"Error examining {file}: {e}")