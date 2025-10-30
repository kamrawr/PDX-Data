# PDX-Data: Datasets

This directory contains information about the Portland Metro property assessment datasets.

## 📊 Available Datasets

### Complete Dataset
**`Portland_Assessor_AllNeighborhoods.csv`** (500MB+)
- **Records:** 1,698,076 properties
- **Neighborhoods:** 217
- **Coverage:** Complete Portland Metro area
- **Collection Date:** October 30, 2024

### Quality-Filtered Subsets

**`subsets/high_quality_80pct.csv`** (~479MB)
- Properties with 80%+ complete data fields
- Best for detailed analysis requiring comprehensive property information
- Excludes properties with significant missing data

**`subsets/medium_quality_60pct.csv`** (~508MB)
- Properties with 60%+ complete data fields
- Good balance between coverage and data completeness
- Suitable for most analytical purposes

**`subsets/portland_focused.csv`** (~178MB)
- Portland-only properties (high quality subset)
- 80%+ data completeness
- Focused on City of Portland proper

## 📋 Data Schema

Each property record includes the following fields:

| Field | Description | Example |
|-------|-------------|---------|
| `ADDRESS` | Street address | "1234 SE Main St" |
| `CITY` | City name | "Portland" |
| `STATE` | State abbreviation | "OR" |
| `ZIP_CODE` | ZIP code (numeric) | 97214 |
| `ZIP_CODE_STRING` | ZIP code (string format) | "97214" |
| `COUNTY` | County name | "Multnomah" |
| `NEIGHBORHOOD` | Neighborhood/district name | "Buckman" |
| `PROPERTY_ID` | Unique property identifier | "R123456" |
| `STATE_ID` | State tax lot ID | "1S1E02BA 12345" |
| `PARENT_STATE_ID` | Parent parcel ID (if applicable) | "1S1E02BA 00000" |
| `ALT_ACCOUNT_NUMBER` | Alternative account number | "12345678" |
| `OWNER` | Property owner name | "Smith, John & Jane" |
| `LEGAL_DESCRIPTION` | Legal property description | "LOT 1 BLOCK 2..." |
| `SQUARE_FEET` | Building square footage | 1500 |
| `MARKET_VALUE` | Assessed market value | 450000 |
| `SALE_DATE` | Most recent sale date | "2023-05-15" |
| `SALE_PRICE` | Most recent sale price | 425000 |
| `YEAR_BUILT` | Year constructed | 1925 |
| `X_STATE_PLANE` | X coordinate (state plane) | 7645123.45 |
| `Y_STATE_PLANE` | Y coordinate (state plane) | 685432.12 |

## 📥 Data Access

Due to file size limitations, the complete datasets are not stored in this repository. 

**Options for accessing the data:**

1. **Generate it yourself** - Use the tools in `/tools` to scrape fresh data
2. **Contact the maintainer** - Reach out for data sharing arrangements
3. **Cloud storage** - Check releases for download links (when available)

## 🔍 Data Quality Notes

- **Missing values:** Some properties may have incomplete information
- **Temporal accuracy:** Data represents a snapshot from the collection date
- **Geographic scope:** Includes Portland Metro (Multnomah, Clackamas, Washington counties)
- **Duplicates:** Minimal; primarily from pagination handling during collection

## 📈 Dataset Statistics

### Top 10 Neighborhoods by Property Count

1. CPO 4B Bull Mtn-Tigard: 143,734
2. Centennial: 111,628
3. CPO 4M Metzger: 109,950
4. Pearl District: 69,665
5. Oak Grove Community: 67,416
6. Hazelwood: 64,624
7. South Portland: 61,925
8. Powellhurst-Gilbert: 61,040
9. CPO 12 Forest Grove: 49,686
10. Sellwood-Moreland: 43,442

### Geographic Distribution
- **Multnomah County:** ~60% of records
- **Clackamas County:** ~25% of records
- **Washington County:** ~15% of records

## 🔄 Data Updates

This is a static dataset from October 2024. For current data:
- Re-run the scraping tools in `/tools`
- Visit the source: [PortlandMaps.com](https://www.portlandmaps.com/advanced/?action=assessor)

## ⚖️ Data Usage & Citation

This data is sourced from public records via PortlandMaps.com. When using this data, please cite:

```
PDX-Data: Portland Metro Property Assessment Dataset
Community Consulting Partners LLC
https://github.com/CommunityConsultingPartners/PDX-Data
Data sourced from: PortlandMaps.com
Collection Date: October 30, 2024
```

## 📧 Contact

Questions about the data? Open an issue or contact the maintainer.
