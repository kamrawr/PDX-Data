import pandas as pd
import numpy as np
import os

print("📊 Analyzing data quality...\n")

# Load the full dataset
df = pd.read_csv("Portland_Assessor_AllNeighborhoods.csv", low_memory=False)
print(f"Loaded {len(df):,} total properties\n")

# Analyze completeness by column
print("=" * 70)
print("COLUMN COMPLETENESS ANALYSIS")
print("=" * 70)

completeness = {}
for col in df.columns:
    non_null_count = df[col].notna().sum()
    pct_complete = (non_null_count / len(df)) * 100
    completeness[col] = {
        'non_null': non_null_count,
        'pct_complete': pct_complete
    }

# Sort by completeness
sorted_cols = sorted(completeness.items(), key=lambda x: x[1]['pct_complete'], reverse=True)

print(f"\n{'Column':<40} {'Complete':<12} {'% Complete':<12}")
print("-" * 70)
for col, stats in sorted_cols:
    print(f"{col:<40} {stats['non_null']:>10,}  {stats['pct_complete']:>10.1f}%")

# Identify key structural columns for Portland property data (using actual column names)
key_columns = [
    'PROPERTY_ID', 'STATE_ID', 'ADDRESS', 'OWNER',
    'YEAR_BUILT', 'MARKET_VALUE', 'SALE_PRICE', 'SALE_DATE',
    'SQUARE_FEET', 'LEGAL_DESCRIPTION', 'CITY', 'ZIP_CODE',
    'LATITUDE', 'LONGITUDE', 'neighborhood'
]

# Find which key columns exist in the dataset
existing_key_cols = [col for col in key_columns if col in df.columns]
print(f"\n\n{'='*70}")
print(f"KEY COLUMNS FOUND: {len(existing_key_cols)}")
print(f"{'='*70}")
print(", ".join(existing_key_cols))

# Calculate completeness score for each row
print("\n\n" + "=" * 70)
print("CALCULATING ROW-LEVEL COMPLETENESS SCORES")
print("=" * 70)

# Score based on existing key columns
df['completeness_score'] = df[existing_key_cols].notna().sum(axis=1) / len(existing_key_cols) * 100

# Analyze by neighborhood
print("\nCompleteness by Neighborhood (Top 30):\n")
neighborhood_quality = df.groupby('neighborhood').agg({
    'completeness_score': 'mean',
    'PROPERTY_ID': 'count'
}).rename(columns={'PROPERTY_ID': 'count'})
neighborhood_quality = neighborhood_quality.sort_values('completeness_score', ascending=False)

print(f"{'Neighborhood':<40} {'Avg Complete %':<15} {'Properties':<12}")
print("-" * 70)
for hood, row in neighborhood_quality.head(30).iterrows():
    print(f"{hood:<40} {row['completeness_score']:>13.1f}%  {int(row['count']):>10,}")

# Create quality-filtered subsets
print("\n\n" + "=" * 70)
print("CREATING QUALITY-FILTERED DATASETS")
print("=" * 70)

# Subset 1: High Quality (>= 80% complete)
high_quality = df[df['completeness_score'] >= 80].copy()
print(f"\n✓ High Quality (≥80% complete): {len(high_quality):,} properties")

# Subset 2: Medium Quality (>= 60% complete)
medium_quality = df[df['completeness_score'] >= 60].copy()
print(f"✓ Medium Quality (≥60% complete): {len(medium_quality):,} properties")

# Subset 3: Portland-specific (city name filtering)
if 'CITY' in df.columns:
    portland_only = df[df['CITY'].str.upper().str.contains('PORTLAND', na=False)].copy()
    print(f"✓ Portland City Only: {len(portland_only):,} properties")
else:
    # Try to identify Portland by neighborhood names
    portland_neighborhoods = neighborhood_quality.head(50).index.tolist()
    portland_only = df[df['neighborhood'].isin(portland_neighborhoods)].copy()
    print(f"✓ Portland Area (top neighborhoods): {len(portland_only):,} properties")

# Subset 4: Complete key fields only
required_fields = [col for col in ['PROPERTY_ID', 'ADDRESS', 'OWNER', 'MARKET_VALUE', 'YEAR_BUILT'] if col in df.columns]
complete_required = df.dropna(subset=required_fields).copy()
print(f"✓ Complete Core Fields: {len(complete_required):,} properties")

# Subset 5: Residential with structure details (has year built and square feet)
residential_filter = (df['completeness_score'] >= 70) & (df['YEAR_BUILT'].notna()) & (df['SQUARE_FEET'].notna())
residential_complete = df[residential_filter].copy()
print(f"✓ Residential High Quality (with structure data): {len(residential_complete):,} properties")

# Save subsets
print("\n\n" + "=" * 70)
print("SAVING SUBSETS")
print("=" * 70)

os.makedirs("subsets", exist_ok=True)

datasets = {
    "high_quality_80pct": high_quality,
    "medium_quality_60pct": medium_quality,
    "portland_focused": portland_only,
    "complete_core_fields": complete_required,
    "residential_high_quality": residential_complete
}

for name, data in datasets.items():
    if len(data) > 0:
        filepath = f"subsets/{name}.csv"
        data.to_csv(filepath, index=False)
        print(f"✓ Saved: {filepath} ({len(data):,} rows)")

# Create quality summary report
report_file = "subsets/quality_report.txt"
with open(report_file, "w") as f:
    f.write("PDX Data Quality Analysis Report\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Original Dataset: {len(df):,} properties\n\n")
    
    f.write("Quality-Filtered Subsets:\n")
    f.write("-" * 70 + "\n")
    for name, data in datasets.items():
        pct = (len(data) / len(df)) * 100
        f.write(f"{name:<30} {len(data):>10,} properties ({pct:.1f}%)\n")
    
    f.write("\n\nTop 20 Highest Quality Neighborhoods:\n")
    f.write("-" * 70 + "\n")
    for hood, row in neighborhood_quality.head(20).iterrows():
        f.write(f"{hood:<40} {row['completeness_score']:>6.1f}%  ({int(row['count']):,} properties)\n")
    
    f.write("\n\nColumn Completeness (All Columns):\n")
    f.write("-" * 70 + "\n")
    for col, stats in sorted_cols:
        f.write(f"{col:<40} {stats['pct_complete']:>6.1f}%\n")

print(f"\n✓ Saved: {report_file}")

print("\n\n🎉 Complete! Check the 'subsets/' folder for quality-filtered datasets.")
print(f"\nRecommendation: Start with 'high_quality_80pct.csv' or 'portland_focused.csv'")
