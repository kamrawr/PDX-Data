# PDX-Data Tools

This directory contains the scraping and data processing tools used to collect and prepare the Portland property assessment data.

## Tools Overview

### 🕷️ Scraping Tools

- **`portlandmaps_scrape.py`** - Main scraper that collects property data from PortlandMaps.com
  - Iterates through all 217 neighborhoods
  - Handles pagination automatically
  - Downloads CSV files for each neighborhood
  - Resumes from where it left off if interrupted
  
- **`portlandmaps_scrape_reverse.py`** - Alternative scraper with reverse order processing

### 🧹 Data Processing Tools

- **`cleanup_and_merge.py`** - Merges individual neighborhood CSVs into unified dataset
  - Combines all downloaded CSV files
  - Adds neighborhood labels
  - Creates `Portland_Assessor_AllNeighborhoods.csv`

- **`create_quality_subsets.py`** - Generates filtered data subsets
  - **High quality (80%)**: Properties with 80%+ complete data fields
  - **Medium quality (60%)**: Properties with 60%+ complete data fields  
  - **Portland focused**: Portland-only properties (high quality)

### 🧪 Testing Tools

- **`test_alameda.py`** - Test scraper for Alameda neighborhood (development/debugging)

## Usage

### Initial Data Collection

```bash
# Install dependencies
pip install -r ../requirements.txt

# Run the main scraper (takes several hours)
python portlandmaps_scrape.py
```

### Process Downloaded Data

```bash
# Merge all CSVs into unified dataset
python cleanup_and_merge.py

# Create quality-filtered subsets
python create_quality_subsets.py
```

## Technical Details

**Dependencies:**
- Selenium WebDriver
- Pandas
- Chrome Browser
- webdriver-manager

**Output Locations:**
- `../raw_downloads/` - Individual neighborhood CSV files
- `../Portland_Assessor_AllNeighborhoods.csv` - Complete unified dataset
- `../subsets/` - Quality-filtered datasets

## Notes

- The scraper respects the source website's pagination structure
- Downloads are timestamped to avoid overwriting
- Smart resume feature skips already-downloaded neighborhoods
- Pagination detection handles both single-page and multi-page results

## Data Source

All data is collected from: https://www.portlandmaps.com/advanced/?action=assessor
