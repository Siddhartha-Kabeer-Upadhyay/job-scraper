"""
Enhanced scraper manager with Indeed and Glassdoor support
Uses JobSpy with proper error handling, retries, and location validation
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime
import time
import logging
from config.settings import SCRAPING_CONFIG
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from utils.location_validator import is_indian_city, validate_location_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JobScraperManager:
    """Enhanced job scraper with multiple portal support"""
    
    def __init__(self):
        self.cities = SCRAPING_CONFIG['cities']
        self.search_terms = SCRAPING_CONFIG['search_terms']
        self.delay = SCRAPING_CONFIG['delay']
        self.max_jobs_per_city = SCRAPING_CONFIG['max_jobs_per_city']
        self.all_jobs = []
        
        # Portals to scrape
        self.portals = ['linkedin', 'indeed', 'glassdoor']
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True
    )
    def _scrape_with_retry(self, portal: str, search_term: str, city: str, results_wanted: int):
        """
        Inner scraping function with retry logic
        
        Args:
            portal: Job portal name
            search_term: Search query
            city: City name
            results_wanted: Number of results
            
        Returns:
            DataFrame with scraped jobs
        """
        try:
            logger.info(f"Scraping {portal.upper()}: '{search_term}' in {city}")
            
            # Different configurations per portal
            kwargs = {
                'site_name': [portal],
                'search_term': search_term,
                'location': f"{city}, India",  # Always append India
                'results_wanted': results_wanted,
                'hours_old': 720,  # Last 30 days
                'country_indeed': 'India',  # Force India for all portals
            }
            
            # Portal-specific settings
            if portal == 'indeed':
                kwargs['country_indeed'] = 'India'
                kwargs['hours_old'] = 168  # Last 7 days for Indeed (more reliable)
            
            elif portal == 'glassdoor':
                # Glassdoor is more restrictive
                kwargs['results_wanted'] = min(results_wanted, 30)  # Limit to 30
                kwargs['hours_old'] = 168  # Last 7 days
                # Glassdoor-specific: use full location string
                kwargs['location'] = f"{city}, India"
            
            elif portal == 'linkedin':
                # LinkedIn works better with specific locations
                kwargs['hours_old'] = 720  # Last 30 days
                kwargs['location'] = f"{city}, India"
            
            # Scrape with timeout
            jobs = scrape_jobs(**kwargs)
            
            if jobs is not None and not jobs.empty:
                # Add metadata
                jobs['source_portal'] = portal
                jobs['search_term_used'] = search_term
                jobs['scraped_at'] = datetime.now()
                
                return jobs
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"✗ Error scraping {portal}: {str(e)}")
            # Let retry decorator handle retries for connection errors
            if isinstance(e, (ConnectionError, TimeoutError)):
                raise
            # For other errors, return empty dataframe
            return pd.DataFrame()
    
    def scrape_portal(self, portal: str, search_term: str, city: str, results_wanted: int = 50):
        """
        Scrape jobs from a specific portal with error handling and retry logic
        
        Args:
            portal: 'linkedin', 'indeed', or 'glassdoor'
            search_term: Job search query
            city: City name
            results_wanted: Number of jobs to fetch
        """
        try:
            jobs_df = self._scrape_with_retry(portal, search_term, city, results_wanted)
            
            if not jobs_df.empty:
                # Validate locations before returning
                initial_count = len(jobs_df)
                jobs_df = self._validate_scraped_data(jobs_df, city)
                valid_count = len(jobs_df)
                
                if valid_count < initial_count:
                    logger.warning(f"⚠ Filtered out {initial_count - valid_count} jobs with invalid locations")
                
                if not jobs_df.empty:
                    logger.info(f"✓ Found {len(jobs_df)} valid jobs from {portal}")
                    return jobs_df
                else:
                    logger.warning(f"✗ No valid jobs after location filtering from {portal}")
                    return pd.DataFrame()
            else:
                logger.warning(f"✗ No jobs found on {portal}")
                return pd.DataFrame()
        
        except Exception as e:
            logger.error(f"✗ All retry attempts failed for {portal}: {str(e)}")
            return pd.DataFrame()
    
    def _validate_scraped_data(self, jobs_df: pd.DataFrame, expected_city: str) -> pd.DataFrame:
        """
        Validate scraped job data and filter out invalid entries
        
        Args:
            jobs_df: DataFrame with scraped jobs
            expected_city: City we expected to scrape from
            
        Returns:
            Filtered DataFrame with only valid jobs
        """
        if jobs_df.empty:
            return jobs_df
        
        # Track validation statistics
        initial_count = len(jobs_df)
        invalid_locations = []
        
        # Validate each job's location
        valid_indices = []
        for idx, row in jobs_df.iterrows():
            location = row.get('location', '')
            
            # Validate location
            if is_indian_city(location):
                valid_indices.append(idx)
            else:
                invalid_locations.append(location)
                logger.debug(f"Rejected job with invalid location: {location}")
        
        # Filter to valid jobs only
        if valid_indices:
            validated_df = jobs_df.loc[valid_indices].copy()
        else:
            validated_df = pd.DataFrame()
        
        # Log validation results
        rejected_count = initial_count - len(validated_df)
        if rejected_count > 0:
            logger.info(f"Data validation: {len(validated_df)}/{initial_count} jobs passed location validation")
            # Show some examples of rejected locations
            unique_invalid = list(set(invalid_locations))[:5]
            if unique_invalid:
                logger.debug(f"Examples of rejected locations: {unique_invalid}")
        
        return validated_df
    
    def scrape_city(self, city: str, search_term: str):
        """
        Scrape all portals for a specific city and search term
        
        Args:
            city: City name
            search_term: Job search query
            
        Returns:
            Combined DataFrame from all portals
        """
        city_jobs = []
        
        for portal in self.portals:
            try:
                jobs_df = self.scrape_portal(
                    portal=portal,
                    search_term=search_term,
                    city=city,
                    results_wanted=self.max_jobs_per_city // len(self.portals)
                )
                
                if not jobs_df.empty:
                    city_jobs.append(jobs_df)
                
                # Rate limiting between portals
                time.sleep(self.delay)
                
            except Exception as e:
                logger.error(f"Error with {portal} in {city}: {e}")
                continue
        
        if city_jobs:
            combined = pd.concat(city_jobs, ignore_index=True)
            logger.info(f"✓ {city}: Total {len(combined)} jobs from all portals")
            return combined
        else:
            logger.warning(f"✗ {city}: No jobs found from any portal")
            return pd.DataFrame()
    
    def scrape_all(self):
        """
        Scrape jobs from all configured cities, search terms, and portals
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"STARTING BULK SCRAPING OPERATION")
        logger.info(f"{'='*60}")
        logger.info(f"Cities: {self.cities}")
        logger.info(f"Search terms: {self.search_terms}")
        logger.info(f"Portals: {self.portals}")
        logger.info(f"Delay between requests: {self.delay}s")
        logger.info(f"{'='*60}\n")
        
        total_scraped = 0
        
        for city in self.cities:
            logger.info(f"\n{'='*60}")
            logger.info(f"PROCESSING: {city.upper()}")
            logger.info(f"{'='*60}")
            
            city_all_jobs = []
            
            for search_term in self.search_terms:
                logger.info(f"\nSearch term: '{search_term}'")
                
                jobs_df = self.scrape_city(city, search_term)
                
                if not jobs_df.empty:
                    city_all_jobs.append(jobs_df)
                    total_scraped += len(jobs_df)
                
                # Rate limiting between search terms
                time.sleep(self.delay)
            
            if city_all_jobs:
                city_combined = pd.concat(city_all_jobs, ignore_index=True)
                self.all_jobs.append(city_combined)
                logger.info(f"\n✓ {city}: Collected {len(city_combined)} total jobs")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"SCRAPING COMPLETE!")
        logger.info(f"{'='*60}")
        logger.info(f"Total jobs scraped: {total_scraped}")
        logger.info(f"{'='*60}\n")
        
        return self.combine_results()
    
    def combine_results(self):
        """Combine all scraped jobs and remove duplicates"""
        if not self.all_jobs:
            logger.warning("No jobs scraped!")
            return pd.DataFrame()
        
        combined = pd.concat(self.all_jobs, ignore_index=True)
        
        # Remove duplicates based on job_url
        initial_count = len(combined)
        combined = combined.drop_duplicates(subset=['job_url'], keep='first')
        final_count = len(combined)
        
        duplicates_removed = initial_count - final_count
        
        logger.info(f"\n{'='*60}")
        logger.info(f"DATA PROCESSING")
        logger.info(f"{'='*60}")
        logger.info(f"Initial jobs: {initial_count}")
        logger.info(f"Duplicates removed: {duplicates_removed}")
        logger.info(f"Final unique jobs: {final_count}")
        logger.info(f"{'='*60}\n")
        
        # Show breakdown by portal
        if 'source_portal' in combined.columns:
            portal_counts = combined['source_portal'].value_counts()
            logger.info("Jobs by Portal:")
            for portal, count in portal_counts.items():
                logger.info(f"  • {portal.capitalize()}: {count}")
        
        return combined
    
    def save_results(self, filename=None):
        """Save scraped jobs to CSV"""
        if not self.all_jobs:
            logger.warning("No data to save!")
            return None
        
        df = self.combine_results()
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"scraped_jobs_{timestamp}.csv"
        
        # Ensure description column exists
        if 'description' not in df.columns:
            df['description'] = df.get('job_description', '')
        
        # Save with UTF-8 BOM for Excel compatibility
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        logger.info(f"\n{'='*60}")
        logger.info(f"DATA SAVED")
        logger.info(f"{'='*60}")
        logger.info(f"Filename: {filename}")
        logger.info(f"Total jobs: {len(df)}")
        logger.info(f"File size: {Path(filename).stat().st_size / 1024:.1f} KB")
        logger.info(f"{'='*60}\n")
        
        # Show sample
        logger.info("Sample Jobs:")
        for idx in range(min(3, len(df))):
            job = df.iloc[idx]
            logger.info(f"\n  {idx+1}. {job.get('title', 'N/A')}")
            logger.info(f"     Company: {job.get('company', 'N/A')}")
            logger.info(f"     Location: {job.get('location', 'N/A')}")
            logger.info(f"     Portal: {job.get('source_portal', 'N/A')}")
        
        return filename


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Job Scraper - LinkedIn, Indeed, Glassdoor'
    )
    parser.add_argument(
        '--portals',
        nargs='+',
        choices=['linkedin', 'indeed', 'glassdoor'],
        default=['linkedin', 'indeed', 'glassdoor'],
        help='Portals to scrape (default: all)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode - scrape only 10 jobs from one city'
    )
    
    args = parser.parse_args()
    
    scraper = JobScraperManager()
    
    # Override portals if specified
    if args.portals:
        scraper.portals = args.portals
        logger.info(f"Using portals: {scraper.portals}")
    
    # Test mode
    if args.test:
        logger.info("TEST MODE: Scraping limited data...")
        scraper.cities = [scraper.cities[0]]  # First city only
        scraper.search_terms = [scraper.search_terms[0]]  # First search term only
        scraper.max_jobs_per_city = 10
    
    # Run scraper
    try:
        scraper.scrape_all()
        filename = scraper.save_results()
        
        if filename:
            logger.info(f"\n SUCCESS! Data saved to: {filename}")
            logger.info(f"\nNext steps:")
            logger.info(f"1. Process the data:")
            logger.info(f"   python data_processing/data_cleaner.py {filename}")
            logger.info(f"\n2. Run the dashboard:")
            logger.info(f"   streamlit run dashboard/app.py")
        
    except KeyboardInterrupt:
        logger.info("\n\n⚠ Scraping interrupted by user")
        if scraper.all_jobs:
            logger.info("Saving partial results...")
            scraper.save_results()
    except Exception as e:
        logger.error(f"\n Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
