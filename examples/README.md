# Analysis Examples

This directory contains example scripts and notebooks demonstrating how to analyze the PDX-Data property assessment datasets.

## Available Examples

### `basic_analysis.py`

Comprehensive Python script showcasing common analysis patterns:

- **Dataset Overview** - Basic statistics and data completeness
- **Market Value Analysis** - Value distributions and percentiles
- **Neighborhood Rankings** - Top neighborhoods by various metrics
- **Sales Activity** - Recent sales trends and patterns
- **Property Characteristics** - Square footage and age distributions
- **Price per Square Foot** - Valuation efficiency metrics

**Usage:**
```bash
python basic_analysis.py
```

**Requirements:**
```bash
pip install pandas matplotlib seaborn
```

## Analysis Ideas

### Market Research
- **Price Trends**: Track median values over time by neighborhood
- **Affordability Analysis**: Identify price ranges and availability
- **Market Segmentation**: Cluster neighborhoods by characteristics
- **Investment Opportunities**: Find undervalued properties

### Geographic Analysis
- **Spatial Patterns**: Map property values across the metro area
- **Proximity Analysis**: Distance to transit, parks, schools
- **Neighborhood Boundaries**: Explore assessment differences at borders
- **Growth Patterns**: Identify areas of development

### Temporal Analysis
- **Building Age Trends**: Construction booms and historical patterns
- **Sales Velocity**: How quickly properties turn over
- **Value Appreciation**: Calculate growth rates by area
- **Seasonal Patterns**: Sales activity by time of year

### Statistical Modeling
- **Price Prediction**: Build models for property valuation
- **Feature Importance**: What drives property values?
- **Anomaly Detection**: Find underpriced or overpriced properties
- **Clustering**: Group similar properties or neighborhoods

## Sample Analysis Snippets

### Load and Filter Data
```python
import pandas as pd

# Load Portland-focused dataset
df = pd.read_csv('subsets/portland_focused.csv')

# Filter to recent sales
recent_sales = df[
    (df['SALE_DATE'] >= '2023-01-01') & 
    (df['SALE_PRICE'] > 0)
]

# Filter to specific neighborhood
pearl = df[df['NEIGHBORHOOD'] == 'PEARL DISTRICT']
```

### Calculate Metrics
```python
# Price per square foot
df['PRICE_PER_SQFT'] = df['MARKET_VALUE'] / df['SQUARE_FEET']

# Property age
df['AGE'] = 2024 - df['YEAR_BUILT']

# Value appreciation (requires historical data)
df['APPRECIATION'] = (df['MARKET_VALUE'] - df['SALE_PRICE']) / df['SALE_PRICE']
```

### Aggregations
```python
# Average values by neighborhood
neighborhood_stats = df.groupby('NEIGHBORHOOD').agg({
    'MARKET_VALUE': ['mean', 'median', 'count'],
    'SQUARE_FEET': 'mean',
    'YEAR_BUILT': 'median'
}).round(0)

# Sales volume by year
sales_by_year = df[df['SALE_PRICE'] > 0].groupby(
    pd.to_datetime(df['SALE_DATE']).dt.year
).size()
```

### Visualizations
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Value distribution
plt.figure(figsize=(10, 6))
df['MARKET_VALUE'].hist(bins=50, edgecolor='black')
plt.xlabel('Market Value ($)')
plt.ylabel('Count')
plt.title('Distribution of Property Values')
plt.show()

# Price by neighborhood (top 10)
top_hoods = df.groupby('NEIGHBORHOOD')['MARKET_VALUE'].median().nlargest(10)
plt.figure(figsize=(12, 6))
top_hoods.plot(kind='barh')
plt.xlabel('Median Market Value ($)')
plt.title('Top 10 Neighborhoods by Median Value')
plt.tight_layout()
plt.show()

# Scatter: Size vs. Value
plt.figure(figsize=(10, 6))
plt.scatter(df['SQUARE_FEET'], df['MARKET_VALUE'], alpha=0.3)
plt.xlabel('Square Feet')
plt.ylabel('Market Value ($)')
plt.title('Property Size vs. Market Value')
plt.show()
```

### Geographic Mapping
```python
import folium
from pyproj import Transformer

# Convert State Plane to Lat/Long
transformer = Transformer.from_crs("EPSG:6557", "EPSG:4326")

df_map = df[df['X_STATE_PLANE'].notna()].head(1000)  # Sample for performance
df_map['LAT'], df_map['LON'] = transformer.transform(
    df_map['X_STATE_PLANE'], 
    df_map['Y_STATE_PLANE']
)

# Create map
m = folium.Map(location=[45.5152, -122.6784], zoom_start=12)

for idx, row in df_map.iterrows():
    folium.CircleMarker(
        location=[row['LAT'], row['LON']],
        radius=3,
        popup=f"{row['ADDRESS']}<br>${row['MARKET_VALUE']:,}",
        color='blue',
        fill=True
    ).add_to(m)

m.save('property_map.html')
```

## Data Exploration Tips

1. **Start Small**: Use `.head()`, `.sample()`, or `nrows` parameter when loading
2. **Check Data Quality**: Use `.info()`, `.describe()`, `.isna().sum()`
3. **Filter Intelligently**: Remove outliers and invalid values
4. **Visualize First**: Plots reveal patterns that statistics might miss
5. **Document Assumptions**: Note any filters or transformations applied

## Contributing Examples

Have an interesting analysis? We'd love to include it!

1. Fork the repository
2. Add your example script or notebook
3. Include comments and documentation
4. Submit a pull request

## Resources

- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/
- **Seaborn Tutorial**: https://seaborn.pydata.org/tutorial.html
- **Folium Docs**: https://python-visualization.github.io/folium/

## Questions?

Open an issue on GitHub or check the main documentation in `/docs`.
