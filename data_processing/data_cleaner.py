"""
Data cleaning and preprocessing for scraped job data
Includes location validation and quality reporting
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
import re
import logging
from datetime import datetime
from typing import Optional, Dict, List
from skill_extractor import SkillExtractor
from database.db_operations import JobDatabase
from utils.location_validator import is_indian_city, validate_location_data, get_location_statistics

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JobDataCleaner:
    """Clean and preprocess scraped job data"""
    
    def __init__(self):
        self.city_mapping = {
            'bangalore': 'Bengaluru',
            'bengaluru': 'Bengaluru',
            'mumbai': 'Mumbai',
            'pune': 'Pune',
            'delhi': 'Delhi',
            'new delhi': 'Delhi',
            'hyderabad': 'Hyderabad',
            'chennai': 'Chennai',
            'noida': 'Noida',
            'gurugram': 'Gurugram',
            'gurgaon': 'Gurugram'
        }
        
        self.experience_mapping = {
            'entry': 'Entry Level',
            'junior': 'Entry Level',
            'mid': 'Mid Level',
            'senior': 'Senior Level',
            'lead': 'Senior Level',
            'principal': 'Senior Level',
            'staff': 'Senior Level',
            'intern': 'Internship',
            'internship': 'Internship'
        }
        
        self.job_type_mapping = {
            'full time': 'Full-time',
            'full-time': 'Full-time',
            'fulltime': 'Full-time',
            'part time': 'Part-time',
            'part-time': 'Part-time',
            'parttime': 'Part-time',
            'contract': 'Contract',
            'temporary': 'Contract',
            'remote': 'Remote',
            'hybrid': 'Hybrid',
            'onsite': 'On-site',
            'on-site': 'On-site'
        }
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the entire DataFrame with location validation
        
        Args:
            df: Raw scraped DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info(f"Starting data cleaning for {len(df)} rows...")
        
        df_clean = df.copy()
        
        # Remove completely empty rows
        df_clean = df_clean.dropna(how='all')
        
        # Validate and filter locations FIRST (most critical)
        logger.info("Validating locations...")
        df_clean = self._validate_and_filter_locations(df_clean)
        
        # Handle missing data with defaults
        df_clean = self._handle_missing_data(df_clean)
        
        # Clean each column
        df_clean = self._clean_titles(df_clean)
        df_clean = self._clean_companies(df_clean)
        df_clean = self._clean_locations(df_clean)
        df_clean = self._clean_descriptions(df_clean)
        df_clean = self._clean_urls(df_clean)
        df_clean = self._clean_dates(df_clean)
        df_clean = self._clean_experience_levels(df_clean)
        df_clean = self._clean_job_types(df_clean)
        df_clean = self._clean_salaries(df_clean)
        
        # Remove duplicates based on job URL
        initial_count = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=['job_url'], keep='first')
        duplicates_removed = initial_count - len(df_clean)
        
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate jobs")
        
        # Remove rows without essential information
        df_clean = df_clean[
            df_clean['title'].notna() & 
            (df_clean['title'] != '') &
            df_clean['description'].notna()
        ]
        
        logger.info(f"Cleaning complete! {len(df_clean)} rows remaining")
        
        # Generate data quality report
        self._generate_quality_report(df, df_clean)
        
        return df_clean
    
    def _validate_and_filter_locations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate locations and filter out non-Indian cities
        
        Args:
            df: DataFrame with location data
            
        Returns:
            Filtered DataFrame with only valid Indian locations
        """
        if 'location' not in df.columns:
            logger.warning("No location column found in DataFrame")
            return df
        
        initial_count = len(df)
        
        # Get location statistics for reporting
        locations_list = df['location'].tolist()
        stats = get_location_statistics(locations_list)
        
        logger.info("=" * 60)
        logger.info("LOCATION VALIDATION REPORT")
        logger.info("=" * 60)
        logger.info(f"Total locations: {stats['total_locations']}")
        logger.info(f"Valid Indian cities: {stats['valid_locations']} ({stats.get('valid_percentage', 0)}%)")
        logger.info(f"Invalid locations: {stats['invalid_locations']} ({stats.get('invalid_percentage', 0)}%)")
        logger.info(f"  - Null/Empty: {stats['null_locations']}")
        logger.info(f"  - US locations: {stats['us_locations']}")
        logger.info(f"  - International: {stats['international_locations']}")
        logger.info(f"  - Unrecognized: {stats['unrecognized_locations']}")
        
        # Show rejection reasons
        if stats['rejection_reasons']:
            logger.info("\nTop rejection reasons:")
            for reason, count in list(stats['rejection_reasons'].items())[:5]:
                logger.info(f"  - {reason}: {count}")
        logger.info("=" * 60)
        
        # Filter to only valid Indian locations
        valid_mask = df['location'].apply(lambda x: is_indian_city(x))
        df_valid = df[valid_mask].copy()
        
        rejected_count = initial_count - len(df_valid)
        logger.info(f"\n✓ Kept {len(df_valid)} jobs with valid Indian locations")
        logger.info(f"✗ Rejected {rejected_count} jobs with invalid locations")
        
        # Log some examples of rejected locations for review
        if rejected_count > 0:
            rejected_df = df[~valid_mask]
            rejected_locations = rejected_df['location'].value_counts().head(5)
            logger.info("\nExamples of rejected locations:")
            for loc, count in rejected_locations.items():
                logger.info(f"  - {loc}: {count} jobs")
        
        return df_valid
    
    def _generate_quality_report(self, df_original: pd.DataFrame, df_cleaned: pd.DataFrame):
        """
        Generate a data quality report
        
        Args:
            df_original: Original DataFrame before cleaning
            df_cleaned: Cleaned DataFrame
        """
        report = {
            'original_rows': len(df_original),
            'cleaned_rows': len(df_cleaned),
            'rows_removed': len(df_original) - len(df_cleaned),
            'removal_percentage': round((len(df_original) - len(df_cleaned)) / len(df_original) * 100, 2) if len(df_original) > 0 else 0
        }
        
        logger.info("\n" + "=" * 60)
        logger.info("DATA QUALITY SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Original rows: {report['original_rows']}")
        logger.info(f"Cleaned rows: {report['cleaned_rows']}")
        logger.info(f"Rows removed: {report['rows_removed']} ({report['removal_percentage']}%)")
        logger.info("=" * 60)
    
    def _handle_missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing data with appropriate defaults"""
        
        # Default values for missing fields
        defaults = {
            'experience_level': 'Entry Level',
            'job_type': 'Full-time',
            'currency': 'INR',
            'is_remote': False,
            'num_urgent_words': 0
        }
        
        for col, default in defaults.items():
            if col in df.columns:
                df[col] = df[col].fillna(default)
        
        # Salary handling - set to None (will show as "Not Specified" in UI)
        salary_cols = ['salary_min', 'salary_max', 'min_amount', 'max_amount']
        for col in salary_cols:
            if col in df.columns:
                df[col] = df[col].replace(0, np.nan)  # Replace 0 with NaN
        
        return df
    
    def _clean_titles(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean job titles"""
        if 'title' in df.columns:
            df['title'] = df['title'].astype(str)
            df['title'] = df['title'].str.strip()
            df['title'] = df['title'].str.replace(r'\s+', ' ', regex=True)
            df['title'] = df['title'].str[:255]
        return df
    
    def _clean_companies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean company names"""
        if 'company' in df.columns:
            df['company'] = df['company'].astype(str)
            df['company'] = df['company'].str.strip()
            df['company'] = df['company'].str.replace(r'\s+', ' ', regex=True)
            df['company'] = df['company'].str.replace(r'\s+(Pvt\.?|Ltd\.?|Private Limited|Limited)$', '', regex=True, flags=re.IGNORECASE)
            df['company'] = df['company'].str[:255]
        return df
    
    def _clean_locations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize location names"""
        if 'location' in df.columns:
            df['location'] = df['location'].astype(str)
            df['location'] = df['location'].str.strip()
            
            # Extract city name
            df['city'] = df['location'].apply(self._extract_city)
            df['state'] = df['location'].apply(self._extract_state)
            
            # Standardize city names
            df['city'] = df['city'].str.lower().map(self.city_mapping).fillna(df['city'])
            
        return df
    
    def _extract_city(self, location: str) -> str:
        """Extract city from location string"""
        if not location or location == 'nan':
            return None
        
        parts = location.split(',')
        city = parts[0].strip()
        
        return city
    
    def _extract_state(self, location: str) -> Optional[str]:
        """Extract state from location string"""
        if not location or location == 'nan':
            return None
        
        parts = location.split(',')
        if len(parts) > 1:
            state = parts[1].strip()
            return state
        
        return None
    
    def _clean_descriptions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean job descriptions"""
        if 'description' in df.columns:
            df['description'] = df['description'].astype(str)
            df['description'] = df['description'].str.strip()
            df['description'] = df['description'].str.replace(r'\s+', ' ', regex=True)
            df['description'] = df['description'].str.replace(r'<[^>]+>', '', regex=True)
        return df
    
    def _clean_urls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean job URLs"""
        if 'job_url' in df.columns:
            df['job_url'] = df['job_url'].astype(str)
            df['job_url'] = df['job_url'].str.strip()
            df['job_url'] = df['job_url'].str[:500]
        return df
    
    def _clean_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and parse dates"""
        date_columns = ['date_posted', 'posted_date']
        
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Use posted_date as standard column
        if 'date_posted' in df.columns:
            df['posted_date'] = df['date_posted']
            df = df.drop(columns=['date_posted'])
        
        return df
    
    def _clean_experience_levels(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize experience level values"""
        exp_columns = ['job_level', 'experience_level', 'seniority']
        
        for col in exp_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower()
                df[col] = df[col].map(self.experience_mapping).fillna('Entry Level')
        
        # Use experience_level as standard column
        if 'job_level' in df.columns:
            df['experience_level'] = df['job_level']
            df = df.drop(columns=['job_level'])
        elif 'experience_level' not in df.columns:
            df['experience_level'] = 'Entry Level'
        
        return df
    
    def _clean_job_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize job type values"""
        if 'job_type' in df.columns:
            df['job_type'] = df['job_type'].astype(str).str.lower()
            df['job_type'] = df['job_type'].map(self.job_type_mapping).fillna('Full-time')
        else:
            df['job_type'] = 'Full-time'
        
        return df
    
    def _clean_salaries(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize salary information"""
        salary_cols = ['min_amount', 'max_amount', 'salary_min', 'salary_max']
        
        for col in salary_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Remove unrealistic salaries
                df.loc[df[col] < 1000, col] = np.nan
                df.loc[df[col] > 10000000, col] = np.nan
        
        # Standardize column names
        if 'min_amount' in df.columns:
            df['salary_min'] = df['min_amount']
            df = df.drop(columns=['min_amount'])
        
        if 'max_amount' in df.columns:
            df['salary_max'] = df['max_amount']
            df = df.drop(columns=['max_amount'])
        
        # Set currency to INR for all Indian jobs
        if 'currency' in df.columns:
            df['currency'] = df['currency'].fillna('INR')
        
        return df
    
    def prepare_for_database(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare cleaned data for database insertion
        Maps DataFrame columns to database schema
        """
        column_mapping = {
            'title': 'job_title',
            'company': 'company_name',
            'description': 'job_description',
            'job_url': 'job_url',
            'city': 'city',
            'state': 'state',
            'experience_level': 'experience_level',
            'job_type': 'job_type',
            'salary_min': 'salary_min',
            'salary_max': 'salary_max',
            'posted_date': 'posted_date',
            'source_portal': 'source_portal'
        }
        
        # Keep only relevant columns and rename
        available_columns = {k: v for k, v in column_mapping.items() if k in df.columns}
        df_db = df[list(available_columns.keys())].copy()
        df_db = df_db.rename(columns=available_columns)
        
        return df_db


def process_and_load_data(csv_file: str, extract_skills: bool = True):
    """
    Complete pipeline: Load CSV -> Clean -> Extract Skills -> Load to DB
    
    Args:
        csv_file: Path to CSV file with scraped jobs
        extract_skills: Whether to extract skills from descriptions
    """
    logger.info("="*50)
    logger.info("Starting data processing pipeline")
    logger.info("="*50)
    
    # Step 1: Load data
    logger.info(f"\n1. Loading data from {csv_file}...")
    try:
        df = pd.read_csv(csv_file)
        logger.info(f"✓ Loaded {len(df)} rows")
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        return
    
    # Step 2: Clean data
    logger.info("\n2. Cleaning data...")
    cleaner = JobDataCleaner()
    df_clean = cleaner.clean_dataframe(df)
    logger.info(f"✓ Cleaned data: {len(df_clean)} rows")
    
    # Step 3: Extract skills
    skills_by_job = {}
    if extract_skills:
        logger.info("\n3. Extracting skills...")
        extractor = SkillExtractor()
        skills_by_job = extractor.extract_skills_from_dataframe(df_clean)
        logger.info(f"✓ Extracted skills from {len(skills_by_job)} jobs")
    else:
        logger.info("\n3. Skipping skill extraction")
    
    # Step 4: Prepare for database
    logger.info("\n4. Preparing data for database...")
    df_db = cleaner.prepare_for_database(df_clean)
    
    # Step 5: Load to database
    logger.info("\n5. Loading data to database...")
    try:
        db = JobDatabase()
        db.bulk_insert_jobs(df_clean, skills_by_job)
        logger.info("✓ Data loaded successfully!")
        
        # Show stats
        stats = db.get_database_stats()
        logger.info("\n" + "="*50)
        logger.info("DATABASE STATISTICS")
        logger.info("="*50)
        logger.info(f"Total Jobs: {stats['total_jobs']}")
        logger.info(f"Total Companies: {stats['total_companies']}")
        logger.info(f"Total Skills: {stats['total_skills']}")
        logger.info("="*50)
        
    except Exception as e:
        logger.error(f"Error loading to database: {e}")
        raise
    
    logger.info("\n✓ Pipeline complete!")


def main():
    """Main execution"""
    import sys
    
    if len(sys.argv) < 2:
        logger.error("Usage: python data_cleaner.py <csv_file>")
        logger.info("Example: python data_cleaner.py scraped_jobs_20251005.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not Path(csv_file).exists():
        logger.error(f"File not found: {csv_file}")
        sys.exit(1)
    
    process_and_load_data(csv_file, extract_skills=True)


if __name__ == "__main__":
    main()