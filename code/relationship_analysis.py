# relationship_analysis.py
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime

data_dir = "data"

def load_unemployment_data():
    """Load and aggregate unemployment data by state and quarter"""
    filepath = os.path.join(data_dir, "Unemployment.csv")
    unemployment = pd.read_csv(filepath)
    
    # Aggregate to quarterly level (average of months in quarter)
    quarterly_unemployment = unemployment.groupby(['year', 'quarter', 'state'])['unemployment_rate'].mean().reset_index()
    
    return quarterly_unemployment

def analyze_market_unemployment_relation():
    """Analyze the relationship between market metrics and unemployment"""
    print("\n===== MARKET AND UNEMPLOYMENT RELATION =====")
    
    # Load unemployment data
    unemployment = load_unemployment_data()
    
    # Load price and availability data
    price_filepath = os.path.join(data_dir, "Price and Availability Data.csv")
    price_data = pd.read_csv(price_filepath)
    
    # Get state from market (for matching with unemployment)
    # Create a mapping of markets to states - this is approximate and may need refinement
    market_to_state = {
        'Atlanta': 'GA',
        'Austin': 'TX',
        'Baltimore': 'MD',
        'Boston': 'MA',
        'Charlotte': 'NC',
        'Chicago': 'IL',
        'Chicago Suburbs': 'IL',
        'Dallas/Ft Worth': 'TX',
        'Dallas-Ft. Worth': 'TX',
        'Denver': 'CO',
        'Denver-Boulder': 'CO',
        'Houston': 'TX',
        'Los Angeles': 'CA',
        'Manhattan': 'NY',
        'Miami': 'FL',
        'Orange County': 'CA',
        'Philadelphia': 'PA',
        'Phoenix': 'AZ',
        'San Francisco': 'CA',
        'Seattle': 'WA',
        'South Bay/San Jose': 'CA',
        'South Florida': 'FL',
        'Washington D.C.': 'DC'
    }
    
    # Map markets to states where possible
    price_data['state'] = price_data['market'].map(market_to_state)
    
    # Filter to only data with state mappings
    price_data_with_state = price_data[~price_data['state'].isna()]
    
    # Merge price data with unemployment
    merged_data = price_data_with_state.merge(
        unemployment,
        on=['year', 'quarter', 'state'],
        how='inner'
    )
    
    print(f"Successfully merged {len(merged_data)} rows")
    
    # Analyze relationship between rent and unemployment
    print("\nCorrelation between unemployment and rent metrics:")
    correlations = merged_data[['unemployment_rate', 'internal_class_rent', 'overall_rent']].corr()
    print(correlations.loc['unemployment_rate', ['internal_class_rent', 'overall_rent']])
    
    # Analyze by building class
    print("\nAverage metrics by building class:")
    class_metrics = merged_data.groupby('internal_class').agg({
        'internal_class_rent': 'mean',
        'unemployment_rate': 'mean',
        'availability_proportion': 'mean'
    }).reset_index()
    print(class_metrics)
    
    # Analyze by year
    print("\nYearly trends (average across all markets):")
    year_metrics = merged_data.groupby('year').agg({
        'internal_class_rent': 'mean',
        'unemployment_rate': 'mean',
        'availability_proportion': 'mean'
    }).reset_index()
    print(year_metrics)

def analyze_lease_activity():
    """Analyze the trends in leasing activity over time"""
    print("\n===== LEASE ACTIVITY TRENDS =====")
    
    # Load price and availability data (which has aggregated leasing activity)
    filepath = os.path.join(data_dir, "Price and Availability Data.csv")
    pa_data = pd.read_csv(filepath)
    
    # Group by year and quarter to see trends
    leasing_by_time = pa_data.groupby(['year', 'quarter']).agg({
        'leasing': 'sum',
        'available_space': 'sum',
        'RBA': 'sum'  # Rentable Building Area
    }).reset_index()
    
    # Calculate proportion of space leased relative to available and total
    leasing_by_time['leasing_to_available_ratio'] = leasing_by_time['leasing'] / leasing_by_time['available_space']
    leasing_by_time['leasing_to_total_ratio'] = leasing_by_time['leasing'] / leasing_by_time['RBA']
    
    print("\nQuarterly leasing activity:")
    print(leasing_by_time[['year', 'quarter', 'leasing', 'leasing_to_available_ratio', 'leasing_to_total_ratio']])
    
    # Analyze by building class
    class_leasing = pa_data.groupby(['internal_class']).agg({
        'leasing': 'sum',
        'available_space': 'sum',
        'RBA': 'sum'
    }).reset_index()
    
    class_leasing['leasing_to_available_ratio'] = class_leasing['leasing'] / class_leasing['available_space']
    class_leasing['leasing_to_total_ratio'] = class_leasing['leasing'] / class_leasing['RBA']
    
    print("\nLeasing activity by building class:")
    print(class_leasing)
    
    # COVID impact analysis - Compare pre-COVID, COVID, and post-COVID
    print("\nCOVID impact analysis (yearly averages):")
    pa_data['period'] = pa_data['year'].apply(
        lambda y: 'Pre-COVID' if y < 2020 else ('COVID' if y == 2020 else 'Post-COVID')
    )
    
    period_metrics = pa_data.groupby('period').agg({
        'leasing': 'mean',
        'availability_proportion': 'mean',
        'internal_class_rent': 'mean'
    }).reset_index()
    
    print(period_metrics)

if __name__ == "__main__":
    print(f"Starting relationship analysis at {datetime.now()}")
    try:
        analyze_market_unemployment_relation()
    except Exception as e:
        print(f"Error in market-unemployment analysis: {e}")
    
    try:
        analyze_lease_activity()
    except Exception as e:
        print(f"Error in lease activity analysis: {e}")
    
    print(f"\nCompleted analysis at {datetime.now()}")