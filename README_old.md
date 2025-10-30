# PDX-Data: Portland Metro Property Assessment Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data: 1.7M+ Records](https://img.shields.io/badge/Records-1.7M+-blue.svg)](#)
[![Neighborhoods: 217](https://img.shields.io/badge/Neighborhoods-217-green.svg)](#)

A comprehensive dataset of **1.7 million property assessment records** from the Portland Metro area, covering 217 neighborhoods across Multnomah, Clackamas, and Washington counties.

🌐 **[View Project Website](https://communityconsultingpartners.github.io/PDX-Data)**

## 📊 Dataset Overview

This repository provides access to property assessment data for research, analysis, and urban planning. The data includes:

- **Property Characteristics**: Square footage, year built, location
- **Valuations**: Assessed market values from county assessors
- **Sales History**: Transaction dates and prices
- **Geographic Data**: Coordinates, neighborhoods, zip codes
- **Ownership**: Public record owner information

### Key Statistics

| Metric | Value |
|--------|-------|
| Total Properties | 1,698,076 |
| Neighborhoods | 217 |
| Data Fields | 20+ |
| Collection Date | October 30, 2024 |
| Geographic Coverage | 3 counties (Multnomah, Clackamas, Washington) |

## 🗂️ Available Datasets

### Quality-Filtered Subsets

**High Quality (80%+ complete)** - `subsets/high_quality_80pct.csv` (~479MB)
- Best for detailed analysis requiring comprehensive data
- Properties with at least 80% of fields populated

**Medium Quality (60%+ complete)** - `subsets/medium_quality_60pct.csv` (~508MB)
- Good balance between coverage and completeness
- Suitable for most analytical purposes

**Portland Focused** - `subsets/portland_focused.csv` (~178MB)
- City of Portland properties only
- High quality subset (80%+ complete)

**Complete Dataset** - `Portland_Assessor_AllNeighborhoods.csv` (500MB+)
- All 1.7M records
- Includes properties with sparse information

> **Note:** Due to file size, datasets are not included in the repository. See [Data Access](#-data-access) below.

## 📥 Data Access

### Option 1: Generate Fresh Data

Use the included scraping tools to collect current data:

```bash
# Install dependencies
pip install -r requirements.txt

# Run data collection (takes ~12 hours)
python tools/portlandmaps_scrape.py

# Process and filter data
python tools/create_quality_subsets.py
```

### Option 2: Request Access

Contact the maintainer for data sharing arrangements or check the [Releases](https://github.com/CommunityConsultingPartners/PDX-Data/releases) page for download links.

## 🚀 Quick Start

```python
import pandas as pd

# Load the Portland-focused dataset
df = pd.read_csv('subsets/portland_focused.csv')

# Basic exploration
print(f"Total properties: {len(df):,}")
print(f"Median value: ${df['MARKET_VALUE'].median():,.0f}")

# Filter to recent sales
recent_sales = df[
    (df['SALE_DATE'] >= '2023-01-01') & 
    (df['SALE_PRICE'] > 0)
]

# Analyze by neighborhood
neighborhood_stats = df.groupby('NEIGHBORHOOD').agg({
    'MARKET_VALUE': 'median',
    'SQUARE_FEET': 'mean'
}).round(0)
```

See [`examples/`](examples/) for more analysis examples.

## 📚 Documentation

- **[Data Dictionary](docs/DATA_DICTIONARY.md)** - Complete field definitions and schema
- **[Methodology](docs/METHODOLOGY.md)** - Data collection process and quality control
- **[Analysis Examples](examples/)** - Sample scripts and code snippets

## 🛠️ Repository Structure

```
PDX-Data/
├── index.html              # Project website
├── data/                   # Dataset information
│   └── README.md          # Data access and descriptions
├── docs/                   # Documentation
│   ├── DATA_DICTIONARY.md # Field definitions
│   └── METHODOLOGY.md     # Collection methodology
├── examples/               # Analysis examples
│   ├── basic_analysis.py  # Python analysis script
│   └── README.md          # Usage guide
├── tools/                  # Data collection tools
│   ├── portlandmaps_scrape.py
│   ├── create_quality_subsets.py
│   └── README.md
├── LICENSE                 # MIT License
├── CITATION.cff           # Citation information
└── README.md              # This file
```

## 📖 Use Cases

### Market Research
- Property valuation trends
- Neighborhood price comparisons
- Investment opportunity identification
- Market segmentation analysis

### Urban Planning
- Housing stock assessment
- Growth pattern analysis
- Demographic distribution
- Infrastructure planning

### Academic Research
- Real estate economics
- Urban development studies
- Gentrification analysis
- Property tax policy

### Data Science Projects
- Price prediction models
- Spatial analysis and mapping
- Time series forecasting
- Clustering and classification

## ⚖️ Citation

If you use this dataset in your research or project, please cite:

```bibtex
@dataset{pdx_data_2024,
  author = {Kamrar, Isaiah},
  title = {PDX-Data: Portland Metro Property Assessment Dataset},
  year = {2024},
  publisher = {Community Consulting Partners LLC},
  url = {https://github.com/CommunityConsultingPartners/PDX-Data},
  note = {Data sourced from PortlandMaps.com}
}
```

Or use the plain text citation:

```
Kamrar, I. (2024). PDX-Data: Portland Metro Property Assessment Dataset.
Community Consulting Partners LLC.
https://github.com/CommunityConsultingPartners/PDX-Data
Data sourced from PortlandMaps.com.
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The property data is sourced from public records via [PortlandMaps.com](https://www.portlandmaps.com) and is provided for research and analytical purposes.

## 🤝 Contributing

Contributions are welcome! Whether it's:

- 🐛 Bug reports
- 📊 New analysis examples
- 📝 Documentation improvements
- ✨ Feature suggestions

Please open an issue or submit a pull request.

## 🔄 Data Updates

This dataset represents a snapshot from **October 30, 2024**. Property values and ownership may have changed since collection.

To get current data:
1. Use the scraping tools in [`tools/`](tools/)
2. Visit [PortlandMaps.com](https://www.portlandmaps.com/advanced/?action=assessor) directly

## 📧 Contact

**Isaiah Kamrar**  
Community Consulting Partners LLC

- GitHub: [@CommunityConsultingPartners](https://github.com/CommunityConsultingPartners)
- Issues: [GitHub Issues](https://github.com/CommunityConsultingPartners/PDX-Data/issues)

## 🙏 Acknowledgments

- Data sourced from [PortlandMaps.com](https://www.portlandmaps.com)
- Original data provided by Multnomah, Clackamas, and Washington County Assessors
- Built with open-source tools: Python, Selenium, Pandas

---

⭐ **Star this repository** if you find it useful!
