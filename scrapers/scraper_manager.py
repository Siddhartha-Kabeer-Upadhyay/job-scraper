"""
Main scraper manager - handles bulk scraping operations
Now supports both LinkedIn (via JobSpy) and Indeed (custom scraper)
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

# Import custom Indeed scraper
try:
    from indeed_scraper import IndeedScraper
    INDEED_AVAILABLE = True
except ImportError:
    INDEED_AVAILABLE = False
    logging.warning("Custom Indeed scraper not available")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JobScraperManager:
    """Manages job scraping operations across multiple portals and cities"""
    
    def __init__(self, use_indeed=True):
        self.cities = SCRAPING_CONFIG['cities']
        self.search_terms = SCRAPING_CONFIG['search_terms']
        self.delay = SCRAPING_CONFIG['delay']
        self.max_jobs_per_city = SCRAPING_CONFIG['max_jobs_per_city']
        self.all_jobs = []
        self.use_indeed = use_indeed and INDEED_AVAILABLE
        
        if self.use_indeed:
            self.indeed_scraper = IndeedScraper()
            logger.info("Custom Indeed scraper initialized")
    
    def scrape_linkedin(self, search_term: str, city: str, results_wanted: int = 50):
        """Scrape jobs from LinkedIn using JobSpy"""
        try:
            logger.info(f"Scraping LinkedIn: '{search_term}' in {city}")
            
            jobs = scrape_jobs(
                site_name=['linkedin'],
                search_term=search_term,
                location=city,
                results_wanted=results_wanted,
                country_indeed='India',
                hours_old=720  # Last 30 days
            )
            
            if jobs is not None and not jobs.empty:
                jobs['source_portal'] = 'linkedin'
                jobs['search_term_used'] = search_term
                jobs['scraped_at'] = datetime.now()
                logger.info(f"✓ Found {len(jobs)} jobs")
                return jobs
            else:
                logger.warning(f"✗ No jobs found")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"✗ Error scraping LinkedIn: {str(e)}")
            return pd.DataFrame()
    
    def scrape_indeed_custom(self, search_term: str, city: str, max_results: int = 50):
        """Scrape jobs from Indeed using custom scraper"""
        if not self.use_indeed:
            logger.warning("Indeed scraper not available, skipping")
            return pd.DataFrame()
        
        try:
            logger.info(f"Scraping Indeed (custom): '{search_term}' in {city}")
            
            jobs = self.indeed_scraper.search_jobs(
                query=search_term,
                location=city,
                max_results=max_results
            )
            
            if jobs:
                df = pd.DataFrame(jobs)
                df['search_term_used'] = search_term
                logger.info(f"✓ Found {len(jobs)} jobs")
                return df
            else:
                logger.warning(f"✗ No jobs found")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"✗ Error scraping Indeed: {str(e)}")
            return pd.DataFrame()
    
    def scrape_all(self, use_linkedin=True, use_indeed=True):
        """
        Scrape jobs from all configured portals and cities
        
        Args:
            use_linkedin: Whether to scrape LinkedIn (default: True)
            use_indeed: Whether to scrape Indeed (default: True)
        """
        logger.info(f"Starting bulk scraping operation")
        logger.info(f"Cities: {self.cities}")
        logger.info(f"Search terms: {self.search_terms}")
        logger.info(f"Portals: LinkedIn={use_linkedin}, Indeed={use_indeed and self.use_indeed}")
        logger.info(f"Delay between requests: {self.delay}s")
        
        total_scraped = 0
        
        for city in self.cities:
            city_jobs = []
            
            for search_term in self.search_terms:
                
                # LinkedIn via JobSpy
                if use_linkedin:
                    jobs_df = self.scrape_linkedin(
                        search_term=search_term,
                        city=city,
                        results_wanted=100
                    )
                    
                    if not jobs_df.empty:
                        city_jobs.append(jobs_df)
                        total_scraped += len(jobs_df)
                    
                    time.sleep(self.delay)
                
                # Indeed via custom scraper
                if use_indeed and self.use_indeed:
                    jobs_df = self.scrape_indeed_custom(
                        search_term=search_term,
                        city=city,
                        max_results=50  # Smaller batch for Indeed
                    )
                    
                    if not jobs_df.empty:
                        city_jobs.append(jobs_df)
                        total_scraped += len(jobs_df)
                    
                    # Longer delay for Indeed (respecting robots.txt)
                    time.sleep(self.delay * 2)
            
            if city_jobs:
                city_df = pd.concat(city_jobs, ignore_index=True)
                self.all_jobs.append(city_df)
                logger.info(f"✓ {city}: Collected {len(city_df)} jobs")
        
        logger.info(f"\n{'='*50}")
        logger.info(f"Scraping complete! Total jobs: {total_scraped}")
        logger.info(f"{'='*50}")
        
        return self.combine_results()
    
    def combine_results(self):
        """Combine all scraped jobs into a single DataFrame"""
        if not self.all_jobs:
            logger.warning("No jobs scraped!")
            return pd.DataFrame()
        
        combined = pd.concat(self.all_jobs, ignore_index=True)
        
        # Remove duplicates based on job URL
        initial_count = len(combined)
        combined = combined.drop_duplicates(subset=['job_url'], keep='first')
        final_count = len(combined)
        
        logger.info(f"Removed {initial_count - final_count} duplicates")
        logger.info(f"Final dataset: {final_count} unique jobs")
        
        return combined
    
    def save_results(self, filename=None):
        """Save scraped jobs to CSV"""
        if not self.all_jobs:
            logger.warning("No data to save!")
            return
        
        df = self.combine_results()
        
        if filename is None:
            filename = f"scraped_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df.to_csv(filename, index=False)
        logger.info(f"✓ Data saved to {filename}")
        return filename


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Job Intelligence Platform Scraper')
    parser.add_argument('--linkedin-only', action='store_true', help='Scrape only LinkedIn')
    parser.add_argument('--indeed-only', action='store_true', help='Scrape only Indeed')
    parser.add_argument('--no-indeed', action='store_true', help='Skip Indeed scraping')
    
    args = parser.parse_args()
    
    # Determine which portals to use
    use_linkedin = not args.indeed_only
    use_indeed = not args.linkedin_only and not args.no_indeed
    
    scraper = JobScraperManager(use_indeed=use_indeed)
    scraper.scrape_all(use_linkedin=use_linkedin, use_indeed=use_indeed)
    scraper.save_results()


if __name__ == "__main__":
    main()