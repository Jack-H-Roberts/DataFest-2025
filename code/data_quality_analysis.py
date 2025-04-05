# data_quality_analysis.py
import pandas as pd
import numpy as np
import os
from datetime import datetime

data_dir = "data"

def analyze_leases_sample(sample_size=10000):
    """Analyze a sample of the leases dataset"""
    print("\n===== LEASES DATASET ANALYSIS =====")
    
    filepath = os.path.join(data_dir, "Leases.csv")
    # Read a random sample to get a representative view
    df = pd.read_csv(filepath, nrows=sample_size)
    
    # Basic stats
    print(f"Sample size: {len(df):,} rows")
    
    # Check for missing values
    missing = df.isnull().sum()
    print("\nColumns with missing values:")
    for col in missing[missing > 0].index.sort_values():
        print(f"- {col}: {missing[col]:,} missing values ({missing[col]/len(df):.1%})")
    
    # Markets distribution
    print("\nTop 10 markets by number of leases:")
    market_counts = df['market'].value_counts().head(10)
    for market, count in market_counts.items():
        print(f"- {market}: {count:,} leases ({count/len(df):.1%})")
    
    # Building class distribution
    print("\nDistribution by building class:")
    class_counts = df['internal_class'].value_counts()
    for cls, count in class_counts.items():
        print(f"- Class {cls}: {count:,} leases ({count/len(df):.1%})")
    
    # Lease size distribution
    print("\nLease size statistics (square feet):")
    print(df['leasedSF'].describe())
    
    # Transaction type distribution
    print("\nTransaction types:")
    type_counts = df['transaction_type'].value_counts()
    for typ, count in type_counts.items():
        print(f"- {typ}: {count:,} ({count/len(df):.1%})")

def analyze_market_occupancy():
    """Analyze the market occupancy dataset"""
    print("\n===== MARKET OCCUPANCY DATASET ANALYSIS =====")
    
    filepath = os.path.join(data_dir, "Major Market Occupancy Data.csv")
    df = pd.read_csv(filepath)
    
    # Basic stats
    print(f"Total rows: {len(df):,}")
    
    # Check for missing values
    missing = df.isnull().sum()
    print("\nColumns with missing values:")
    for col in missing[missing > 0].index.sort_values():
        print(f"- {col}: {missing[col]:,} missing values ({missing[col]/len(df):.1%})")
    
    # Markets covered
    markets = df['market'].unique()
    print(f"\nNumber of unique markets: {len(markets)}")
    print("Markets covered:", ', '.join(sorted(markets)[:10]) + 
          (', ...' if len(markets) > 10 else ''))
    
    # Occupancy statistics
    print("\nOccupancy proportion statistics:")
    print(df['occupancy_proportion'].describe())

def analyze_price_availability():
    """Analyze the price and availability dataset"""
    print("\n===== PRICE AND AVAILABILITY DATASET ANALYSIS =====")
    
    filepath = os.path.join(data_dir, "Price and Availability Data.csv")
    df = pd.read_csv(filepath)
    
    # Basic stats
    print(f"Total rows: {len(df):,}")
    
    # Check for missing values
    missing = df.isnull().sum()
    print("\nColumns with missing values:")
    for col in missing[missing > 0].index.sort_values():
        print(f"- {col}: {missing[col]:,} missing values ({missing[col]/len(df):.1%})")
    
    # Markets and classes
    markets = df['market'].unique()
    print(f"\nNumber of unique markets: {len(markets)}")
    print("Markets covered:", ', '.join(sorted(markets)[:10]) + 
          (', ...' if len(markets) > 10 else ''))
    
    # Building class distribution
    print("\nDistribution by building class:")
    class_counts = df['internal_class'].value_counts()
    for cls, count in class_counts.items():
        print(f"- Class {cls}: {count:,} rows ({count/len(df):.1%})")
    
    # Rent statistics by class
    print("\nRent statistics by building class:")
    for cls in df['internal_class'].unique():
        rent_stats = df[df['internal_class'] == cls]['internal_class_rent'].describe()
        print(f"\nClass {cls} rent statistics:")
        print(f"- Average: ${rent_stats['mean']:.2f}")
        print(f"- Median: ${rent_stats['50%']:.2f}")
        print(f"- Min: ${rent_stats['min']:.2f}")
        print(f"- Max: ${rent_stats['max']:.2f}")

def analyze_unemployment():
    """Analyze the unemployment dataset"""
    print("\n===== UNEMPLOYMENT DATASET ANALYSIS =====")
    
    filepath = os.path.join(data_dir, "Unemployment.csv")
    df = pd.read_csv(filepath)
    
    # Basic stats
    print(f"Total rows: {len(df):,}")
    
    # Check for missing values
    missing = df.isnull().sum()
    print("\nColumns with missing values:")
    for col in missing[missing > 0].index.sort_values():
        print(f"- {col}: {missing[col]:,} missing values ({missing[col]/len(df):.1%})")
    
    # States covered
    states = df['state'].unique()
    print(f"\nNumber of states: {len(states)}")
    print("States covered:", ', '.join(sorted(states)[:10]) + 
          (', ...' if len(states) > 10 else ''))
    
    # Unemployment rate statistics
    print("\nUnemployment rate statistics:")
    print(df['unemployment_rate'].describe())
    
    # Evolution over time (yearly averages)
    print("\nYearly average unemployment rates:")
    yearly_avg = df.groupby('year')['unemployment_rate'].mean()
    for year, rate in yearly_avg.items():
        print(f"- {year}: {rate:.2f}%")

if __name__ == "__main__":
    print(f"Starting data quality analysis at {datetime.now()}")
    analyze_leases_sample()
    analyze_market_occupancy()
    analyze_price_availability()
    analyze_unemployment()
    print(f"\nCompleted analysis at {datetime.now()}")