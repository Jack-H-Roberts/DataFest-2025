# explore_codebook.py
import pandas as pd
import os

data_dir = "data"
codebook_path = os.path.join(data_dir, "Data Set and Variable Codebook.xlsx")

print(f"Exploring Excel codebook: {codebook_path}")

# List all sheets in the Excel file
xlsx = pd.ExcelFile(codebook_path)
print(f"Available sheets: {xlsx.sheet_names}")

# Examine each sheet
for sheet in xlsx.sheet_names:
    print(f"\n===== Sheet: {sheet} =====")
    df = pd.read_excel(codebook_path, sheet_name=sheet, nrows=5)
    print(f"Shape: {df.shape}")
    print("Columns:")
    print(df.columns.tolist())
    print("\nSample data:")
    print(df.head())