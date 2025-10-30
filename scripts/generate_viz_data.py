import pandas as pd
import json

print("Generating visualization data for interactive page...")

df = pd.read_csv("subsets/complete_core_fields.csv", low_memory=False)

# Prepare data
df['YEAR_BUILT'] = pd.to_numeric(df['YEAR_BUILT'], errors='coerce')
df['MARKET_VALUE'] = pd.to_numeric(df['MARKET_VALUE'], errors='coerce')
df['SQUARE_FEET'] = pd.to_numeric(df['SQUARE_FEET'], errors='coerce')
df['price_per_sqft'] = df['MARKET_VALUE'] / df['SQUARE_FEET']
df['building_age'] = 2025 - df['YEAR_BUILT']

# 1. Top/Bottom neighborhoods by value
neighborhood_values = df.groupby('neighborhood')['MARKET_VALUE'].agg(['median', 'count'])
neighborhood_values = neighborhood_values[neighborhood_values['count'] >= 300].sort_values('median', ascending=False)

top_hoods = neighborhood_values.head(15).reset_index()
bottom_hoods = neighborhood_values.tail(15).reset_index()

top_neighborhoods = [{
    'neighborhood': row['neighborhood'],
    'value': int(row['median']),
    'count': int(row['count'])
} for _, row in top_hoods.iterrows()]

bottom_neighborhoods = [{
    'neighborhood': row['neighborhood'],
    'value': int(row['median']),
    'count': int(row['count'])
} for _, row in bottom_hoods.iterrows()]

# 2. Affordability tiers
affordability_tiers = pd.cut(df['MARKET_VALUE'], 
                              bins=[0, 300000, 500000, 750000, 1000000, float('inf')],
                              labels=['<300K', '300-500K', '500-750K', '750K-1M', '>1M'])
tier_counts = affordability_tiers.value_counts().sort_index()

affordability_data = [{
    'tier': str(tier),
    'count': int(count),
    'percentage': round(count / len(df) * 100, 1)
} for tier, count in tier_counts.items()]

# 3. Building age distribution by decade
df['decade'] = (df['YEAR_BUILT'] // 10) * 10
decade_counts = df[df['YEAR_BUILT'] >= 1900].groupby('decade').agg({
    'PROPERTY_ID': 'count',
    'MARKET_VALUE': 'median'
}).round(0)

decade_data = [{
    'decade': int(decade),
    'count': int(row['PROPERTY_ID']),
    'median_value': int(row['MARKET_VALUE'])
} for decade, row in decade_counts.iterrows()]

# 4. Corporate vs Individual ownership
corporate_keywords = ['LLC', 'INC', 'CORP', 'LP', 'COMPANY', 'CO ', 'TRUST', 'PROPERTIES']
df['is_corporate'] = df['OWNER'].str.upper().str.contains('|'.join(corporate_keywords), na=False)

ownership_data = [{
    'type': 'Corporate/Institutional',
    'count': int(df['is_corporate'].sum()),
    'total_value': int(df[df['is_corporate']]['MARKET_VALUE'].sum()),
    'median_value': int(df[df['is_corporate']]['MARKET_VALUE'].median())
}, {
    'type': 'Individual/Family',
    'count': int((~df['is_corporate']).sum()),
    'total_value': int(df[~df['is_corporate']]['MARKET_VALUE'].sum()),
    'median_value': int(df[~df['is_corporate']]['MARKET_VALUE'].median())
}]

# 5. Displacement risk neighborhoods
neighborhood_gent = df.groupby('neighborhood').agg({
    'MARKET_VALUE': ['median', 'std', 'mean'],
    'price_per_sqft': 'median',
    'building_age': 'median',
    'PROPERTY_ID': 'count'
})
neighborhood_gent.columns = ['_'.join(col).strip() for col in neighborhood_gent.columns.values]
neighborhood_gent = neighborhood_gent[neighborhood_gent['PROPERTY_ID_count'] >= 500]

neighborhood_gent['price_variance'] = neighborhood_gent['MARKET_VALUE_std'] / neighborhood_gent['MARKET_VALUE_mean']
neighborhood_gent['risk_score'] = (
    neighborhood_gent['price_variance'].rank(pct=True) * 0.3 +
    (neighborhood_gent['building_age_median'] / 100).rank(pct=True) * 0.2 +
    (1 / (neighborhood_gent['MARKET_VALUE_median'] / 1000000)).rank(pct=True) * 0.3 +
    (neighborhood_gent['price_per_sqft_median'] / 100).rank(pct=True) * 0.2
) * 100

displacement_risk = neighborhood_gent.sort_values('risk_score', ascending=False).head(20).reset_index()
displacement_data = [{
    'neighborhood': row['neighborhood'],
    'risk_score': round(row['risk_score'], 1),
    'median_value': int(row['MARKET_VALUE_median']),
    'building_age': int(row['building_age_median']),
    'variance': round(row['price_variance'], 2)
} for _, row in displacement_risk.iterrows()]

# 6. Value concentration (top 8 neighborhoods)
value_by_hood = df.groupby('neighborhood')['MARKET_VALUE'].sum().sort_values(ascending=False).head(8)
total_value = df['MARKET_VALUE'].sum()

concentration_data = [{
    'neighborhood': hood,
    'total_value': int(value),
    'percentage': round(value / total_value * 100, 1)
} for hood, value in value_by_hood.items()]

# 7. Ultra-luxury concentration ($2M+)
ultra_luxury = df[df['MARKET_VALUE'] >= 2000000]
ultra_by_hood = ultra_luxury.groupby('neighborhood').agg({
    'PROPERTY_ID': 'count',
    'MARKET_VALUE': ['max', 'median']
})
ultra_by_hood.columns = ['count', 'max_value', 'median_value']
ultra_by_hood = ultra_by_hood[ultra_by_hood['count'] >= 5].sort_values('count', ascending=False).head(15).reset_index()

ultra_luxury_data = [{
    'neighborhood': row['neighborhood'],
    'count': int(row['count']),
    'max_value': int(row['max_value']),
    'median_value': int(row['median_value'])
} for _, row in ultra_by_hood.iterrows()]

# 8. Most corporatized neighborhoods
corp_by_hood = df.groupby('neighborhood')['is_corporate'].agg(['sum', 'count'])
corp_by_hood['corp_pct'] = (corp_by_hood['sum'] / corp_by_hood['count'] * 100)
corp_by_hood = corp_by_hood[corp_by_hood['count'] >= 300].sort_values('corp_pct', ascending=False).head(15).reset_index()

corporate_concentration_data = [{
    'neighborhood': row['neighborhood'],
    'corporate_pct': round(row['corp_pct'], 1),
    'corporate_count': int(row['sum']),
    'total_count': int(row['count'])
} for _, row in corp_by_hood.iterrows()]

# Compile all data
viz_data = {
    'metadata': {
        'total_properties': len(df),
        'total_market_value': int(df['MARKET_VALUE'].sum()),
        'median_value': int(df['MARKET_VALUE'].median()),
        'neighborhoods': int(df['neighborhood'].nunique()),
        'analysis_date': '2025-10-30'
    },
    'top_neighborhoods': top_neighborhoods,
    'bottom_neighborhoods': bottom_neighborhoods,
    'affordability_tiers': affordability_data,
    'building_decades': decade_data,
    'ownership_breakdown': ownership_data,
    'displacement_risk': displacement_data,
    'value_concentration': concentration_data,
    'ultra_luxury': ultra_luxury_data,
    'corporate_concentration': corporate_concentration_data
}

# Save to JSON
with open('viz_data.json', 'w') as f:
    json.dump(viz_data, f, indent=2)

print("✅ Data exported to viz_data.json")
print(f"   - {len(df):,} properties analyzed")
print(f"   - {len(viz_data)} visualization datasets created")
