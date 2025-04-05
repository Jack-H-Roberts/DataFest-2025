# market_analysis.py
import pandas as pd
import numpy as np
import os
from datetime import datetime

data_dir = "data"

def analyze_top_markets():
    """Analyze trends in the top markets"""
    print("\n===== TOP MARKET ANALYSIS =====")
    
    # Load price and availability data
    filepath = os.path.join(data_dir, "Price and Availability Data.csv")
    df = pd.read_csv(filepath)
    
    # Identify top markets by total RBA
    top_markets_by_size = df.groupby('market')['RBA'].sum().sort_values(ascending=False).head(10)
    print("Top 10 markets by size (total RBA):")
    for market, rba in top_markets_by_size.items():
        print(f"- {market}: {rba:,} sq ft")
    
    # Identify top markets by leasing activity
    top_markets_by_leasing = df.groupby('market')['leasing'].sum().sort_values(ascending=False).head(10)
    print("\nTop 10 markets by leasing activity:")
    for market, leasing in top_markets_by_leasing.items():
        print(f"- {market}: {leasing:,} sq ft")
    
    # Compare rent and availability in top 5 markets
    top_5_markets = top_markets_by_size.index[:5]
    
    # Get data for only the top 5 markets
    top_markets_df = df[df['market'].isin(top_5_markets)]
    
    # Analyze these markets over time
    market_trends = top_markets_df.groupby(['market', 'year']).agg({
        'internal_class_rent': 'mean',
        'availability_proportion': 'mean',
        'leasing': 'sum'
    }).reset_index()
    
    print("\nTrends in top 5 markets:")
    for market in top_5_markets:
        market_data = market_trends[market_trends['market'] == market]
        print(f"\n{market}:")
        print("Year | Avg Rent | Availability % | Leasing (M sq ft)")
        print("-" * 55)
        for _, row in market_data.iterrows():
            print(f"{row['year']}  | ${row['internal_class_rent']:.2f}    | {row['availability_proportion']:.1%}         | {row['leasing']/1000000:.1f}")

def analyze_covid_recovery():
    """Analyze COVID recovery patterns across markets"""
    print("\n===== COVID RECOVERY ANALYSIS =====")
    
    # Load price and availability data
    filepath = os.path.join(data_dir, "Price and Availability Data.csv")
    df = pd.read_csv(filepath)
    
    # Define periods
    pre_covid = df[(df['year'] == 2019) & (df['quarter'] == 'Q4')].copy()
    during_covid = df[(df['year'] == 2020) & (df['quarter'] == 'Q2')].copy()
    recent = df[(df['year'] == 2023) & (df['quarter'] == 'Q4')].copy()
    
    # Calculate metrics for each period
    pre_covid['period'] = 'Pre-COVID'
    during_covid['period'] = 'During COVID'
    recent['period'] = 'Recent'
    
    # Combine periods
    periods_df = pd.concat([pre_covid, during_covid, recent])
    
    # Calculate market-level metrics
    market_recovery = periods_df.groupby(['market', 'period']).agg({
        'leasing': 'sum',
        'internal_class_rent': 'mean',
        'availability_proportion': 'mean'
    }).reset_index()
    
    # Calculate recovery percentages
    recovery_metrics = []
    
    # Get unique markets
    markets = market_recovery['market'].unique()
    
    for market in markets:
        market_data = market_recovery[market_recovery['market'] == market]
        
        # Check if we have data for all periods
        if len(market_data) == 3:
            pre = market_data[market_data['period'] == 'Pre-COVID'].iloc[0]
            during = market_data[market_data['period'] == 'During COVID'].iloc[0]
            recent = market_data[market_data['period'] == 'Recent'].iloc[0]
            
            # Calculate recovery metrics
            leasing_drop = (during['leasing'] - pre['leasing']) / pre['leasing'] if pre['leasing'] > 0 else 0
            leasing_recovery = (recent['leasing'] - during['leasing']) / during['leasing'] if during['leasing'] > 0 else 0
            availability_increase = (during['availability_proportion'] - pre['availability_proportion'])
            recent_availability_change = (recent['availability_proportion'] - during['availability_proportion'])
            
            recovery_metrics.append({
                'market': market,
                'leasing_drop': leasing_drop,
                'leasing_recovery': leasing_recovery,
                'availability_increase': availability_increase,
                'recent_availability_change': recent_availability_change,
                'pre_covid_rent': pre['internal_class_rent'],
                'recent_rent': recent['internal_class_rent'],
                'rent_growth': (recent['internal_class_rent'] - pre['internal_class_rent']) / pre['internal_class_rent']
            })
    
    recovery_df = pd.DataFrame(recovery_metrics)
    
    # Sort by recovery strength
    recovery_df_sorted = recovery_df.sort_values('leasing_recovery', ascending=False)
    
    print("COVID impact and recovery by market:")
    print("\nTop 5 markets by leasing recovery:")
    for i, (_, row) in enumerate(recovery_df_sorted.head(5).iterrows()):
        print(f"{i+1}. {row['market']}:")
        print(f"   - Initial leasing drop: {row['leasing_drop']:.1%}")
        print(f"   - Leasing recovery: {row['leasing_recovery']:.1%}")
        print(f"   - Availability increase during COVID: {row['availability_increase']:.1%}")
        print(f"   - Availability change since COVID: {row['recent_availability_change']:.1%}")
        print(f"   - Rent growth since pre-COVID: {row['rent_growth']:.1%}")
    
    print("\nBottom 5 markets by leasing recovery:")
    for i, (_, row) in enumerate(recovery_df_sorted.tail(5).iterrows()):
        print(f"{i+1}. {row['market']}:")
        print(f"   - Initial leasing drop: {row['leasing_drop']:.1%}")
        print(f"   - Leasing recovery: {row['leasing_recovery']:.1%}")
        print(f"   - Availability increase during COVID: {row['availability_increase']:.1%}")
        print(f"   - Availability change since COVID: {row['recent_availability_change']:.1%}")
        print(f"   - Rent growth since pre-COVID: {row['rent_growth']:.1%}")

def find_anomalies():
    """Find markets with unusual patterns or outliers"""
    print("\n===== MARKET ANOMALIES =====")
    
    # Load price and availability data
    filepath = os.path.join(data_dir, "Price and Availability Data.csv")
    df = pd.read_csv(filepath)
    
    # Aggregate to market level
    market_metrics = df.groupby('market').agg({
        'internal_class_rent': ['mean', 'std'],
        'availability_proportion': ['mean', 'std'],
        'leasing': ['sum', 'mean', 'std']
    })
    
    # Flatten column names
    market_metrics.columns = ['_'.join(col).strip() for col in market_metrics.columns.values]
    market_metrics = market_metrics.reset_index()
    
    # Calculate coefficient of variation for key metrics
    market_metrics['rent_cv'] = market_metrics['internal_class_rent_std'] / market_metrics['internal_class_rent_mean']
    market_metrics['availability_cv'] = market_metrics['availability_proportion_std'] / market_metrics['availability_proportion_mean']
    market_metrics['leasing_cv'] = market_metrics['leasing_std'] / market_metrics['leasing_mean']
    
    # Find markets with highest variability
    print("Markets with highest rent variability:")
    for market, cv in market_metrics.sort_values('rent_cv', ascending=False)['market'].head(5).items():
        print(f"- {cv}")
    
    print("\nMarkets with highest availability variability:")
    for market, cv in market_metrics.sort_values('availability_cv', ascending=False)['market'].head(5).items():
        print(f"- {cv}")
    
    print("\nMarkets with highest leasing variability:")
    for market, cv in market_metrics.sort_values('leasing_cv', ascending=False)['market'].head(5).items():
        print(f"- {cv}")
    
    # Look for markets with unusual relationships between metrics
    # Calculate correlations between rent and availability for each market
    correlations = []
    
    for market in df['market'].unique():
        market_data = df[df['market'] == market]
        if len(market_data) >= 8:  # Ensure we have enough data points
            corr = market_data['internal_class_rent'].corr(market_data['availability_proportion'])
            correlations.append({
                'market': market,
                'rent_availability_correlation': corr
            })
    
    corr_df = pd.DataFrame(correlations)
    
    print("\nMarkets with strongest positive correlation between rent and availability:")
    for i, (_, row) in enumerate(corr_df.sort_values('rent_availability_correlation', ascending=False).head(5).iterrows()):
        print(f"{i+1}. {row['market']}: {row['rent_availability_correlation']:.2f}")
    
    print("\nMarkets with strongest negative correlation between rent and availability:")
    for i, (_, row) in enumerate(corr_df.sort_values('rent_availability_correlation').head(5).iterrows()):
        print(f"{i+1}. {row['market']}: {row['rent_availability_correlation']:.2f}")

if __name__ == "__main__":
    print(f"Starting market analysis at {datetime.now()}")
    try:
        analyze_top_markets()
    except Exception as e:
        print(f"Error in top markets analysis: {e}")
    
    try:
        analyze_covid_recovery()
    except Exception as e:
        print(f"Error in COVID recovery analysis: {e}")
    
    try:
        find_anomalies()
    except Exception as e:
        print(f"Error in anomalies analysis: {e}")
    
    print(f"\nCompleted analysis at {datetime.now()}")