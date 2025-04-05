from space_utilization_and_rent_trends import space_utlization_bar

def main():
    # List of all markets to process
    markets = [
        "Atlanta",
        "Austin",
        "Baltimore",
        "Boston",
        "Charlotte",
        "Chicago Suburbs",
        "Dallas-Ft. Worth",
        "Denver-Boulder",
        "Detroit",
        "Houston",
        "Los Angeles",
        "Nashville",
        "Manhattan",
        "Northern New Jersey",
        "Northern Virginia",
        "Orange County (CA)",
        "Philadelphia",
        "Phoenix",
        "Raleigh-Durham",
        "Salt Lake City",
        "San Diego",
        "San Francisco",
        "Seattle",
        "South Bay",
        "South Florida",
        "Suburban Maryland",
        "Tampa"
    ]
    
    # Quality levels: 0 for standard, 1 for premium
    quality_levels = [0, 1]
    
    # Calculate total number of charts to generate
    total_charts = len(markets) * len(quality_levels)
    processed = 0
    
    print(f"Starting to generate {total_charts} visualizations...")
    
    # Process each market with both quality levels
    for market in markets:
        for quality in quality_levels:
            # Create a descriptive string for the quality level
            quality_str = "Premium" if quality == 1 else "Standard"
            
            # Show progress
            processed += 1
            print(f"[{processed}/{total_charts}] Processing {market} ({quality_str})")
            
            try:
                # Call the visualization function
                space_utlization_bar(market, quality)
                print(f"✓ Successfully created visualization for {market} ({quality_str})")
            except Exception as e:
                print(f"✗ Error creating visualization for {market} ({quality_str}): {str(e)}")
    
    print(f"\nCompleted generating {processed}/{total_charts} visualizations.")

if __name__ == "__main__":
    main()