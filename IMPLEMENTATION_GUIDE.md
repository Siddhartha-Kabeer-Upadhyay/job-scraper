# Location Data Quality Fixes - Implementation Guide

## Overview

This implementation addresses critical data quality issues in the job scraper platform by adding comprehensive location validation, improving scraper reliability, and enhancing the dashboard with data quality metrics.

## Changes Made

### 1. Location Validation System (`utils/location_validator.py`)

**Purpose:** Ensure only Indian cities are stored in the database

**Features:**
- Comprehensive list of 100+ approved Indian cities
- Validation functions to check location validity
- Automatic rejection of US/international locations
- City name normalization for consistency
- Detailed validation reporting with rejection reasons

**Usage:**
```python
from utils.location_validator import is_indian_city, validate_location_data

# Simple validation
if is_indian_city("Bengaluru, Karnataka"):
    # Process the location
    pass

# Detailed validation with results
result = validate_location_data("Cincinnati, OH")
print(result['is_valid'])  # False
print(result['rejection_reason'])  # 'US location detected: OH'
```

### 2. Enhanced Scraper Manager (`scrapers/scraper_manager.py`)

**Improvements:**
- **Country Filters:** All portals (LinkedIn, Indeed, Glassdoor) now explicitly filter for India
- **Retry Logic:** Exponential backoff retry mechanism using `tenacity` library
- **Location Validation:** Scraped data validated before returning
- **Rate Limiting:** Improved delays between requests

**Key Changes:**
- Added `@retry` decorator for automatic retry on connection errors
- Location string now includes ", India" suffix for all portals
- New `_validate_scraped_data()` method filters out invalid locations
- Better error handling and logging

**Example:**
```bash
# Scraping will automatically retry on failures
python scrapers/scraper_manager.py --portals linkedin indeed glassdoor
```

### 3. Updated Data Cleaner (`data_processing/data_cleaner.py`)

**Enhancements:**
- **Location Validation:** Integrated location validator in cleaning pipeline
- **Quality Reporting:** Generates comprehensive data quality reports
- **Rejection Logging:** Logs all rejected entries with reasons

**New Methods:**
- `_validate_and_filter_locations()`: Validates and filters location data
- `_generate_quality_report()`: Creates detailed quality metrics

**Usage:**
```python
from data_processing.data_cleaner import JobDataCleaner

cleaner = JobDataCleaner()
df_clean = cleaner.clean_dataframe(df_raw)
# Automatically filters invalid locations and logs rejections
```

### 4. Database Validation Layer (`database/db_operations.py`)

**Additions:**
- **Pre-insertion Validation:** Validates locations before database insertion
- **Quality Check Functions:** New methods for data quality metrics
- **Validation Reporting:** Returns validation errors to caller

**New Methods:**
- `get_data_quality_stats()`: Returns comprehensive quality metrics
- `validate_database_locations()`: Validates existing locations in DB

**Usage:**
```python
from database.db_operations import JobDatabase

db = JobDatabase()

# Get quality statistics
stats = db.get_data_quality_stats()
print(f"Location coverage: {stats['location_coverage']}%")

# Validate existing data
validation = db.validate_database_locations()
print(f"Invalid locations: {validation['invalid_locations']}")
```

### 5. Enhanced Dashboard (`dashboard/app.py`)

**Improvements:**
- **Location Filtering:** Automatically filters out NaN/null locations
- **Data Quality Warnings:** Displays alerts for data quality issues
- **Coverage Metrics:** Shows data coverage percentages

**Key Changes:**
- Added data quality warning banner when coverage < 100%
- Enhanced location filtering in all queries
- New data coverage metrics display

### 6. Cleanup Script (`scripts/cleanup_bad_locations.py`)

**Purpose:** Remove existing bad data from the database

**Features:**
- Dry-run mode (default) to preview changes
- Comprehensive reporting of what will be removed
- Backup info before cleanup
- Support for report-only mode

**Usage:**
```bash
# Preview what would be cleaned (dry-run)
python scripts/cleanup_bad_locations.py

# Generate detailed report only
python scripts/cleanup_bad_locations.py --report-only

# Actually perform cleanup
python scripts/cleanup_bad_locations.py --execute
```

**Example Output:**
```
LOCATION VALIDATION REPORT
============================================================
Total locations: 1000
Valid Indian cities: 850 (85.0%)
Invalid locations: 150 (15.0%)
  - Null/Empty: 10
  - US locations: 120
  - International: 15
  - Unrecognized: 5

US Locations: 120 locations
  - Cincinnati, OH
  - West Chester, OH
  - New York, NY
  ... and 117 more

Total jobs that would be removed: 450
```

### 7. Enhanced Dashboard Files

#### `dashboard/app_enhanced.py`
Modern dashboard with improved UI/UX:
- Gradient metric cards with hover effects
- Better color schemes and styling
- Comprehensive data quality dashboard
- Modern navigation and layout

#### `dashboard/chart_utils.py`
Reusable chart creation utilities:
- `create_bar_chart()`: Styled bar charts
- `create_pie_chart()`: Donut/pie charts
- `create_line_chart()`: Line charts
- `create_treemap()`: Hierarchical visualizations
- And more...

#### `dashboard/styles.py`
Complete CSS styling system:
- Modern gradient designs
- Responsive layouts
- Hover effects and animations
- Consistent color schemes

**Usage:**
```bash
# Run the enhanced dashboard
streamlit run dashboard/app_enhanced.py
```

### 8. Updated Dependencies (`requirements.txt`)

**Added:**
- `tenacity>=8.2.0` - For retry logic with exponential backoff

## Implementation Workflow

### For Fresh Scraping

1. **Configure Cities** (in `config/settings.py`):
```python
SCRAPING_CONFIG = {
    'cities': ['Bengaluru', 'Mumbai', 'Pune', 'Delhi'],
    # ... other config
}
```

2. **Run Scraper**:
```bash
python scrapers/scraper_manager.py
```
- Automatically applies country filters
- Validates locations before returning
- Retries on failures

3. **Process Data**:
```bash
python data_processing/data_cleaner.py scraped_jobs_20251106.csv
```
- Validates and filters locations
- Generates quality report
- Loads to database with validation

4. **View Dashboard**:
```bash
streamlit run dashboard/app_enhanced.py
```

### For Existing Data Cleanup

1. **Generate Report**:
```bash
python scripts/cleanup_bad_locations.py --report-only
```

2. **Preview Cleanup** (dry-run):
```bash
python scripts/cleanup_bad_locations.py
```

3. **Execute Cleanup**:
```bash
python scripts/cleanup_bad_locations.py --execute
```

4. **Verify Results**:
```bash
streamlit run dashboard/app_enhanced.py
# Navigate to "Data Quality" page
```

## Testing

### Test Location Validator
```bash
python utils/location_validator.py
```

### Test Cleanup Script
```bash
# Help
python scripts/cleanup_bad_locations.py --help

# Report only
python scripts/cleanup_bad_locations.py --report-only
```

### Test Dashboard
```bash
# Original dashboard
streamlit run dashboard/app.py

# Enhanced dashboard
streamlit run dashboard/app_enhanced.py
```

## Key Features

### ✅ Data Quality Improvements
- Only Indian cities appear in dashboard
- No NaN/null locations visible
- Automatic rejection of US/international cities
- Comprehensive validation at all stages

### ✅ Scraper Reliability
- Retry logic handles network failures
- Exponential backoff prevents rate limiting
- Country filters ensure correct data
- Better error handling and logging

### ✅ Dashboard Enhancements
- Data quality warnings
- Coverage metrics
- Modern UI with gradients
- Better visualizations

### ✅ Monitoring & Reporting
- Quality metrics at each stage
- Detailed rejection reasons
- Comprehensive cleanup reports
- Database validation functions

## Configuration

### Approved Cities

To add more cities, edit `utils/location_validator.py`:

```python
APPROVED_INDIAN_CITIES = {
    'Bengaluru', 'Mumbai', 'Pune', 
    # Add more cities here
}

CITY_NAME_MAPPING = {
    'bangalore': 'Bengaluru',
    # Add more mappings here
}
```

### Scraper Settings

Edit `config/settings.py`:

```python
SCRAPING_CONFIG = {
    'delay': 3,  # Seconds between requests
    'max_jobs_per_city': 750,
    'cities': ['Bengaluru', 'Mumbai'],  # Cities to scrape
    'search_terms': ['software engineer', 'developer'],
}
```

## Troubleshooting

### Issue: Dashboard shows no data
**Solution:** 
- Check database connection
- Verify data was loaded: `python database/db_operations.py`
- Check data quality: Run cleanup script with `--report-only`

### Issue: Scraper getting blocked
**Solution:**
- Increase delay in settings
- Use fewer concurrent requests
- Check if IP is rate-limited

### Issue: Too many jobs rejected
**Solution:**
- Review rejected locations in logs
- Add city to APPROVED_INDIAN_CITIES if valid
- Check if city name normalization needed

## File Structure

```
job-scraper/
├── utils/
│   └── location_validator.py          # NEW: Location validation
├── scrapers/
│   └── scraper_manager.py             # MODIFIED: Added retry & validation
├── data_processing/
│   └── data_cleaner.py                # MODIFIED: Added location validation
├── database/
│   └── db_operations.py               # MODIFIED: Added validation layer
├── dashboard/
│   ├── app.py                         # MODIFIED: Added quality warnings
│   ├── app_enhanced.py                # NEW: Enhanced dashboard
│   ├── chart_utils.py                 # NEW: Chart utilities
│   └── styles.py                      # NEW: CSS styling
├── scripts/
│   └── cleanup_bad_locations.py       # NEW: Cleanup script
└── requirements.txt                   # MODIFIED: Added tenacity
```

## Next Steps

1. **Deploy**: Push changes to production
2. **Monitor**: Watch quality metrics in dashboard
3. **Cleanup**: Run cleanup script on existing data
4. **Validate**: Check that only Indian cities appear
5. **Iterate**: Add more cities as needed

## Support

For issues or questions:
- Check logs for detailed error messages
- Review validation reports
- Use dry-run mode to test changes
- Consult inline documentation in code

## Version History

- **v2.0.0** (2025-11-06): Major data quality improvements
  - Added location validation system
  - Enhanced scraper reliability
  - Improved dashboard with quality metrics
  - Created cleanup utilities
