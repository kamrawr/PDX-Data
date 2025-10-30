"""
PDX-Data: Basic Analysis Examples
==================================

This script demonstrates common analysis patterns for the Portland property dataset.

Requirements:
    pip install pandas matplotlib seaborn

Usage:
    python basic_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
DATA_DIR = Path(__file__).parent.parent / "subsets"
HIGH_QUALITY_FILE = DATA_DIR / "high_quality_80pct.csv"
PORTLAND_FILE = DATA_DIR / "portland_focused.csv"

def load_data(filepath=PORTLAND_FILE, sample_size=None):
    """
    Load property data from CSV file.
    
    Args:
        filepath: Path to CSV file
        sample_size: Optional number of rows to sample (for faster testing)
    
    Returns:
        pandas DataFrame
    """
    print(f"Loading data from {filepath.name}...")
    
    if sample_size:
        df = pd.read_csv(filepath, nrows=sample_size)
        print(f"Loaded {len(df):,} rows (sample)")
    else:
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df):,} rows")
    
    return df


def basic_statistics(df):
    """Print basic dataset statistics."""
    print("\n" + "="*60)
    print("DATASET OVERVIEW")
    print("="*60)
    
    print(f"\nTotal Properties: {len(df):,}")
    print(f"Unique Neighborhoods: {df['NEIGHBORHOOD'].nunique()}")
    print(f"Cities Covered: {df['CITY'].nunique()}")
    print(f"Date Range: {df.shape}")
    
    print("\n" + "-"*60)
    print("DATA COMPLETENESS")
    print("-"*60)
    completeness = (df.notna().sum() / len(df) * 100).sort_values(ascending=False)
    for field, pct in completeness.items():
        print(f"{field:25s} {pct:5.1f}%")


def market_value_analysis(df):
    """Analyze market value distributions."""
    print("\n" + "="*60)
    print("MARKET VALUE ANALYSIS")
    print("="*60)
    
    # Filter to valid market values
    df_valid = df[df['MARKET_VALUE'] > 0].copy()
    
    print(f"\nProperties with Market Value: {len(df_valid):,}")
    print(f"Mean Market Value: ${df_valid['MARKET_VALUE'].mean():,.0f}")
    print(f"Median Market Value: ${df_valid['MARKET_VALUE'].median():,.0f}")
    print(f"Min Market Value: ${df_valid['MARKET_VALUE'].min():,.0f}")
    print(f"Max Market Value: ${df_valid['MARKET_VALUE'].max():,.0f}")
    
    print("\nMarket Value Percentiles:")
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    for p in percentiles:
        value = df_valid['MARKET_VALUE'].quantile(p/100)
        print(f"  {p}th percentile: ${value:,.0f}")


def neighborhood_rankings(df, top_n=15):
    """Rank neighborhoods by various metrics."""
    print("\n" + "="*60)
    print(f"TOP {top_n} NEIGHBORHOODS")
    print("="*60)
    
    # By count
    print("\n📊 Most Properties:")
    counts = df['NEIGHBORHOOD'].value_counts().head(top_n)
    for i, (hood, count) in enumerate(counts.items(), 1):
        print(f"  {i:2d}. {hood:35s} {count:6,d} properties")
    
    # By median value
    print(f"\n💰 Highest Median Values:")
    df_valid = df[df['MARKET_VALUE'] > 0].copy()
    medians = df_valid.groupby('NEIGHBORHOOD')['MARKET_VALUE'].median().sort_values(ascending=False).head(top_n)
    for i, (hood, value) in enumerate(medians.items(), 1):
        print(f"  {i:2d}. {hood:35s} ${value:9,.0f}")
    
    # By age
    print(f"\n🏛️ Oldest Average Building Age:")
    df_built = df[df['YEAR_BUILT'] > 0].copy()
    df_built['AGE'] = 2024 - df_built['YEAR_BUILT']
    ages = df_built.groupby('NEIGHBORHOOD')['AGE'].mean().sort_values(ascending=False).head(top_n)
    for i, (hood, age) in enumerate(ages.items(), 1):
        print(f"  {i:2d}. {hood:35s} {age:5.1f} years avg")


def sales_analysis(df):
    """Analyze recent sales activity."""
    print("\n" + "="*60)
    print("SALES ACTIVITY ANALYSIS")
    print("="*60)
    
    # Filter to properties with sale data
    df_sales = df[df['SALE_PRICE'].notna() & (df['SALE_PRICE'] > 0)].copy()
    
    print(f"\nProperties with Sale Data: {len(df_sales):,}")
    print(f"Mean Sale Price: ${df_sales['SALE_PRICE'].mean():,.0f}")
    print(f"Median Sale Price: ${df_sales['SALE_PRICE'].median():,.0f}")
    
    # Parse dates
    df_sales['SALE_DATE'] = pd.to_datetime(df_sales['SALE_DATE'], errors='coerce')
    df_sales['SALE_YEAR'] = df_sales['SALE_DATE'].dt.year
    
    # Recent sales (2020+)
    recent = df_sales[df_sales['SALE_YEAR'] >= 2020]
    print(f"\nSales Since 2020: {len(recent):,}")
    
    if len(recent) > 0:
        print("\nSales by Year (2020+):")
        sales_by_year = recent.groupby('SALE_YEAR').agg({
            'SALE_PRICE': ['count', 'median']
        }).round(0)
        for year, row in sales_by_year.iterrows():
            count = int(row['SALE_PRICE']['count'])
            median = int(row['SALE_PRICE']['median'])
            print(f"  {year}: {count:5,d} sales, median ${median:,}")


def property_characteristics(df):
    """Analyze property characteristics."""
    print("\n" + "="*60)
    print("PROPERTY CHARACTERISTICS")
    print("="*60)
    
    # Square footage
    df_sqft = df[df['SQUARE_FEET'] > 0].copy()
    print(f"\nSquare Footage Statistics:")
    print(f"  Mean: {df_sqft['SQUARE_FEET'].mean():,.0f} sq ft")
    print(f"  Median: {df_sqft['SQUARE_FEET'].median():,.0f} sq ft")
    print(f"  25th percentile: {df_sqft['SQUARE_FEET'].quantile(0.25):,.0f} sq ft")
    print(f"  75th percentile: {df_sqft['SQUARE_FEET'].quantile(0.75):,.0f} sq ft")
    
    # Year built
    df_built = df[df['YEAR_BUILT'] > 0].copy()
    print(f"\nYear Built Statistics:")
    print(f"  Oldest: {df_built['YEAR_BUILT'].min():.0f}")
    print(f"  Newest: {df_built['YEAR_BUILT'].max():.0f}")
    print(f"  Median: {df_built['YEAR_BUILT'].median():.0f}")
    print(f"  Average Age: {(2024 - df_built['YEAR_BUILT'].mean()):,.1f} years")
    
    # Decade distribution
    df_built['DECADE'] = (df_built['YEAR_BUILT'] // 10) * 10
    print(f"\nProperties by Decade:")
    decades = df_built['DECADE'].value_counts().sort_index(ascending=False).head(10)
    for decade, count in decades.items():
        print(f"  {int(decade)}s: {count:6,d} properties")


def price_per_sqft_analysis(df):
    """Calculate price per square foot metrics."""
    print("\n" + "="*60)
    print("PRICE PER SQUARE FOOT ANALYSIS")
    print("="*60)
    
    # Filter to valid data
    df_calc = df[
        (df['MARKET_VALUE'] > 0) & 
        (df['SQUARE_FEET'] > 0) & 
        (df['SQUARE_FEET'] < 10000)  # Filter outliers
    ].copy()
    
    df_calc['PRICE_PER_SQFT'] = df_calc['MARKET_VALUE'] / df_calc['SQUARE_FEET']
    
    print(f"\nProperties with both value & sqft: {len(df_calc):,}")
    print(f"Mean Price/SqFt: ${df_calc['PRICE_PER_SQFT'].mean():,.2f}")
    print(f"Median Price/SqFt: ${df_calc['PRICE_PER_SQFT'].median():,.2f}")
    
    # Top neighborhoods by price/sqft
    print(f"\n💎 Top 10 Neighborhoods by Median Price/SqFt:")
    top_price_sqft = df_calc.groupby('NEIGHBORHOOD')['PRICE_PER_SQFT'].agg(['median', 'count'])
    top_price_sqft = top_price_sqft[top_price_sqft['count'] >= 10]  # Min 10 properties
    top_price_sqft = top_price_sqft.sort_values('median', ascending=False).head(10)
    
    for i, (hood, row) in enumerate(top_price_sqft.iterrows(), 1):
        print(f"  {i:2d}. {hood:35s} ${row['median']:6.2f}/sqft ({int(row['count'])} properties)")


def main():
    """Run all analysis examples."""
    
    # Check if data files exist
    if not PORTLAND_FILE.exists():
        print(f"❌ Data file not found: {PORTLAND_FILE}")
        print("\nPlease generate the data using:")
        print("  python tools/create_quality_subsets.py")
        return
    
    # Load data
    df = load_data(PORTLAND_FILE)
    
    # Run analyses
    basic_statistics(df)
    market_value_analysis(df)
    neighborhood_rankings(df)
    sales_analysis(df)
    property_characteristics(df)
    price_per_sqft_analysis(df)
    
    print("\n" + "="*60)
    print("✅ Analysis Complete!")
    print("="*60)


if __name__ == "__main__":
    main()
