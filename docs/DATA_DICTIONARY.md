# Data Dictionary

Complete reference for all fields in the PDX-Data property assessment datasets.

## Field Definitions

### Address & Location Fields

#### `ADDRESS`
- **Type:** String
- **Description:** Full street address of the property
- **Example:** `"1234 SE Main St"`
- **Completeness:** ~95%
- **Notes:** May include unit numbers for condos/apartments

#### `CITY`
- **Type:** String
- **Description:** Municipality name
- **Example:** `"Portland"`, `"Gresham"`, `"Beaverton"`
- **Completeness:** ~99%
- **Unique Values:** ~50 cities

#### `STATE`
- **Type:** String (2 characters)
- **Description:** State abbreviation
- **Example:** `"OR"`
- **Completeness:** ~99%
- **Notes:** Almost exclusively "OR"

#### `ZIP_CODE`
- **Type:** Integer
- **Description:** Postal ZIP code (numeric format)
- **Example:** `97214`
- **Completeness:** ~98%
- **Range:** 97001-97299

#### `ZIP_CODE_STRING`
- **Type:** String
- **Description:** Postal ZIP code (string format, may include ZIP+4)
- **Example:** `"97214"`, `"97214-1234"`
- **Completeness:** ~98%

#### `COUNTY`
- **Type:** String
- **Description:** County name
- **Example:** `"Multnomah"`, `"Clackamas"`, `"Washington"`
- **Completeness:** 100%
- **Unique Values:** 3 primary counties

#### `NEIGHBORHOOD`
- **Type:** String
- **Description:** Neighborhood or district name
- **Example:** `"Pearl District"`, `"Sellwood-Moreland"`
- **Completeness:** 100%
- **Unique Values:** 217 neighborhoods
- **Notes:** Some neighborhoods cross city boundaries

### Property Identification Fields

#### `PROPERTY_ID`
- **Type:** String
- **Description:** Internal property identifier used by assessor's office
- **Example:** `"R123456"`, `"M345678"`
- **Completeness:** ~99%
- **Format:** Usually starts with R (residential), M (multi-family), or C (commercial)
- **Uniqueness:** Primary key for properties

#### `STATE_ID`
- **Type:** String
- **Description:** Oregon state tax lot identification number
- **Example:** `"1S1E02BA 12345"`
- **Completeness:** ~95%
- **Format:** Township-Range-Section-TaxLot
- **Notes:** Official legal identifier for tax purposes

#### `PARENT_STATE_ID`
- **Type:** String
- **Description:** Parent parcel state ID (for subdivided properties)
- **Example:** `"1S1E02BA 00000"`
- **Completeness:** ~40%
- **Notes:** Empty for standalone parcels

#### `ALT_ACCOUNT_NUMBER`
- **Type:** String
- **Description:** Alternative account number (legacy or cross-reference)
- **Example:** `"12345678"`
- **Completeness:** ~60%

### Ownership Fields

#### `OWNER`
- **Type:** String
- **Description:** Name(s) of property owner(s) on record
- **Example:** `"Smith, John & Jane"`, `"ABC Properties LLC"`
- **Completeness:** ~98%
- **Privacy:** Public record data
- **Notes:** Format varies (individuals, trusts, corporations)

#### `LEGAL_DESCRIPTION`
- **Type:** String (long text)
- **Description:** Legal description of property boundaries
- **Example:** `"LOT 1 BLOCK 2 OF SUBDIVISION XYZ"`
- **Completeness:** ~85%
- **Notes:** Can be very lengthy for complex parcels

### Property Characteristics

#### `SQUARE_FEET`
- **Type:** Integer
- **Description:** Total finished square footage of buildings
- **Example:** `1500`, `2400`
- **Completeness:** ~75%
- **Range:** 100 - 50,000+ (residential), larger for commercial
- **Notes:** Excludes garages/unfinished basements unless finished

#### `YEAR_BUILT`
- **Type:** Integer
- **Description:** Year the primary structure was constructed
- **Example:** `1925`, `2005`
- **Completeness:** ~80%
- **Range:** 1850-2024
- **Notes:** May represent most recent major reconstruction

### Valuation Fields

#### `MARKET_VALUE`
- **Type:** Integer
- **Description:** Assessed market value (county assessor determination)
- **Example:** `450000`, `625000`
- **Completeness:** ~90%
- **Currency:** USD
- **Notes:** 
  - Used for property tax calculation
  - Updated periodically by assessor
  - May differ from actual market price
  - Represents value at time of assessment

#### `SALE_DATE`
- **Type:** String (date)
- **Description:** Date of most recent arm's-length sale
- **Example:** `"2023-05-15"`, `"2020-11-03"`
- **Completeness:** ~60%
- **Format:** ISO 8601 (YYYY-MM-DD)
- **Notes:** 
  - Only reflects recorded sales
  - Inherited/gifted properties may have old or no sale date
  - Empty if never sold or pre-digital records

#### `SALE_PRICE`
- **Type:** Integer
- **Description:** Price of most recent arm's-length sale
- **Example:** `425000`, `575000`
- **Completeness:** ~60%
- **Currency:** USD
- **Notes:**
  - Matches `SALE_DATE` when present
  - Public record from deed recordings
  - May not reflect seller concessions

### Geographic Coordinates

#### `X_STATE_PLANE`
- **Type:** Float
- **Description:** X coordinate in Oregon State Plane North projection
- **Example:** `7645123.45`
- **Completeness:** ~85%
- **Units:** US Survey Feet
- **Projection:** NAD83(2011) Oregon State Plane North (EPSG:6557)

#### `Y_STATE_PLANE`
- **Type:** Float
- **Description:** Y coordinate in Oregon State Plane North projection
- **Example:** `685432.12`
- **Completeness:** ~85%
- **Units:** US Survey Feet
- **Projection:** NAD83(2011) Oregon State Plane North (EPSG:6557)
- **Notes:** Can be converted to lat/long for mapping

## Data Quality Tiers

### High Quality (80%+)
Properties with at least 80% of all fields populated. Suitable for:
- Detailed market analysis
- Statistical modeling
- Property comparison studies

### Medium Quality (60%+)
Properties with at least 60% of fields populated. Suitable for:
- General trends analysis
- Neighborhood overviews
- Price range studies

### All Data
Complete dataset including properties with sparse information. Suitable for:
- Coverage analysis
- Finding specific properties
- Data validation studies

## Common Data Patterns

### Missing Values
- Older properties more likely to have missing `YEAR_BUILT`
- Never-sold properties lack `SALE_DATE` and `SALE_PRICE`
- Vacant land often missing `SQUARE_FEET`
- Rural/county properties may have limited detail

### Value Ranges by Property Type
- **Single-family:** $200K-$800K (typical)
- **Condos:** $150K-$600K (typical)
- **Multi-family:** $500K-$3M+ (typical)
- **Commercial:** Highly variable

## Using the Data

### Filtering Recommendations
```python
# High-value residential
df[(df['MARKET_VALUE'] > 500000) & (df['SQUARE_FEET'] > 2000)]

# Recent sales
df[df['SALE_DATE'] >= '2023-01-01']

# Specific neighborhood
df[df['NEIGHBORHOOD'] == 'Pearl District']

# Complete records
df[df.notna().sum(axis=1) >= 16]  # at least 80% complete
```

### Coordinate Conversion
To convert State Plane to Lat/Long:
```python
from pyproj import Transformer

transformer = Transformer.from_crs("EPSG:6557", "EPSG:4326")
lat, lon = transformer.transform(df['X_STATE_PLANE'], df['Y_STATE_PLANE'])
```

## Data Source

All field definitions based on:
- Portland Maps assessor database structure
- Multnomah, Clackamas, and Washington County records
- Oregon Department of Revenue property tax standards

Last Updated: October 30, 2024
