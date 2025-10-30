# Data Collection Methodology

Documentation of how the PDX-Data property assessment dataset was collected and processed.

## Overview

This dataset was created through automated web scraping of the PortlandMaps.com public assessor database, followed by data consolidation and quality filtering.

## Collection Process

### Source System
- **Website:** https://www.portlandmaps.com/advanced/?action=assessor
- **Authority:** City of Portland Bureau of Technology Services
- **Data Provider:** Multnomah, Clackamas, and Washington County Assessors
- **Access:** Public database, no authentication required

### Scraping Methodology

#### Tool: Selenium WebDriver
- **Browser:** Chrome (automated)
- **Language:** Python 3.x
- **Key Libraries:** Selenium, Pandas, webdriver-manager

#### Collection Strategy

**1. Neighborhood-Based Extraction**
- The source system provides a dropdown menu of 217 neighborhoods
- Each neighborhood is queried individually to retrieve all properties
- This approach ensures complete coverage without API rate limits

**2. Pagination Handling**
- System automatically detects multi-page result sets
- Iterates through all pages for neighborhoods with >100 properties
- Each page downloads separately to avoid data loss

**3. Resume Capability**
- Tracks already-downloaded neighborhoods
- Skips completed neighborhoods on restart
- Enables multi-session collection for large datasets

**4. File Naming Convention**
```
{NEIGHBORHOOD}_page{N}_{TIMESTAMP}.csv
```
- Prevents overwrites
- Maintains provenance
- Enables incremental updates

### Collection Timeline

**Date:** October 29-30, 2024  
**Duration:** ~12 hours (automated)  
**Neighborhoods Processed:** 217  
**Files Downloaded:** 419 CSV files  
**Total Records:** 1,698,076

### Quality Control During Collection

- **Wait Times:** 2-3 second delays between requests to avoid server overload
- **Error Handling:** Try/catch blocks for missing/empty results
- **Verification:** File existence checks before proceeding
- **Logging:** Console output tracks progress and errors

## Data Processing

### Phase 1: Consolidation

**Script:** `cleanup_and_merge.py`

**Process:**
1. Scan `raw_downloads/` directory for all CSV files
2. Load each CSV with pandas
3. Extract neighborhood from filename
4. Add `NEIGHBORHOOD` column to each dataframe
5. Concatenate all dataframes
6. Export unified dataset

**Output:** `Portland_Assessor_AllNeighborhoods.csv` (1.7M records)

### Phase 2: Quality Filtering

**Script:** `create_quality_subsets.py`

**Metrics:**
- Calculate completeness percentage per record
- Count non-null values across all fields
- Apply threshold filters

**Subsets Created:**

**High Quality (80%+)**
- Threshold: ≥80% of fields populated
- Records: ~1.2M properties
- Use Case: Detailed analysis, modeling

**Medium Quality (60%+)**
- Threshold: ≥60% of fields populated  
- Records: ~1.4M properties
- Use Case: General analysis, trends

**Portland Focused**
- City filter: `CITY == "Portland"`
- Quality filter: ≥80% completeness
- Records: ~400K properties
- Use Case: City-specific research

## Data Validation

### Completeness Checks
- Record count per neighborhood matches source system
- No duplicate records within neighborhoods
- Field types match expected schema

### Geographic Validation
- All coordinates within Oregon State Plane bounds
- Counties match expected values (Multnomah, Clackamas, Washington)
- ZIP codes within Portland Metro range (97001-97299)

### Value Range Validation
- `YEAR_BUILT`: 1850-2024
- `MARKET_VALUE`: >$0, <$50M (flagged outliers reviewed)
- `SQUARE_FEET`: >0, <100,000 for residential

### Deduplication
- Minimal duplicates found (<0.1%)
- Duplicates primarily from:
  - Properties appearing in multiple pagination pages
  - Properties at neighborhood boundaries
- Duplicates retained to preserve source data fidelity

## Limitations & Considerations

### Temporal Snapshot
- Data represents a point-in-time capture (Oct 2024)
- Property values and ownership may have changed since collection
- Recommend periodic re-collection for current data

### Missing Data
- Not all properties have complete information
- Older properties tend to have more missing fields
- Vacant land often lacks building characteristics
- Never-sold properties missing sale information

### Geographic Coverage
- Focused on Portland Metro (3-county area)
- Some peripheral areas may have incomplete coverage
- Neighborhood boundaries based on assessor definitions

### Data Accuracy
- Sourced directly from official county records
- Accuracy dependent on county assessor data quality
- Assessor values may differ from market prices
- Manual data entry errors from source system preserved

## Reproducibility

### Requirements
- Chrome browser
- Python 3.x with dependencies (see `requirements.txt`)
- Stable internet connection
- ~12 hours processing time
- ~2GB disk space for raw downloads

### Replication Steps
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run scraper: `python tools/portlandmaps_scrape.py`
4. Merge data: `python tools/cleanup_and_merge.py`
5. Filter subsets: `python tools/create_quality_subsets.py`

### Expected Variations
- Record counts may vary slightly (+/- 1-2%) from current collection
- New properties added/removed since Oct 2024
- Updated assessor values
- Ownership changes

## Ethical Considerations

### Public Data
- All data sourced from public records
- No authentication bypass or terms violation
- Respectful scraping with delays
- Data already publicly accessible

### Privacy
- Owner names are public record
- No personal contact information collected
- Data used for research/analysis purposes
- Follows standard property data research practices

### Attribution
- Data sourced from PortlandMaps.com
- County assessors are original data authorities
- Scraping methodology documented for transparency

## Future Improvements

### Planned Enhancements
- Parallel processing to reduce collection time
- Automated change detection for incremental updates
- Historical snapshots for trend analysis
- Enhanced error handling and retry logic
- Progress bars and better status reporting

### Data Enrichment Opportunities
- Property type classification
- School district mapping
- Transit proximity calculations
- Historical sales trends
- Neighborhood market statistics

## Version History

**v1.0 (October 2024)**
- Initial collection of 1.7M records
- 217 neighborhoods across 3 counties
- Quality filtering implementation
- Documentation and tooling

## Contact

Questions about methodology? Open an issue on GitHub or contact the maintainer.

---

**Last Updated:** October 30, 2024  
**Collection Version:** 1.0  
**Methodology Document Version:** 1.0
