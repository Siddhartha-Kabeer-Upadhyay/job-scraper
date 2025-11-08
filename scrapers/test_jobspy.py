"""
Test script for JobSpy library
Tests scraping capabilities for Indian job portals
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_jobspy_scraping():
    """Test JobSpy with Indian job portals"""
    
    test_configs = [
        {
            'site_name': ['indeed'],
            'search_term': 'software engineer',
            'location': 'Bengaluru',
            'results_wanted': 10,
            'country_indeed': 'India'
        },
        {
            'site_name': ['linkedin'],
            'search_term': 'data analyst',
            'location': 'Mumbai',
            'results_wanted': 10,
            'country_indeed': 'India'
        }
    ]
    
    for i, config in enumerate(test_configs, 1):
        logger.info(f"\n{'='*50}")
        logger.info(f"Test {i}: {config['site_name'][0].upper()} - {config['search_term']} in {config['location']}")
        logger.info(f"{'='*50}")
        
        try:
            jobs = scrape_jobs(**config)
            
            if jobs is not None and not jobs.empty:
                logger.info(f"✓ Successfully scraped {len(jobs)} jobs")
                logger.info(f"\nColumns available: {list(jobs.columns)}")
                logger.info(f"\nSample job:")
                logger.info(f"Title: {jobs.iloc[0]['title'] if 'title' in jobs.columns else 'N/A'}")
                logger.info(f"Company: {jobs.iloc[0]['company'] if 'company' in jobs.columns else 'N/A'}")
                logger.info(f"Location: {jobs.iloc[0]['location'] if 'location' in jobs.columns else 'N/A'}")
                
                # Save sample
                filename = f"jobspy_test_{config['site_name'][0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                jobs.to_csv(filename, index=False)
                logger.info(f"✓ Sample saved to {filename}")
                
                return True, "JobSpy works!"
            else:
                logger.warning(f"✗ No jobs found for this configuration")
                
        except Exception as e:
            logger.error(f"✗ Error: {str(e)}")
            return False, str(e)
    
    return False, "All tests failed"

if __name__ == "__main__":
    logger.info("Testing JobSpy library...")
    success, message = test_jobspy_scraping()
    
    if success:
        logger.info(f"\n{'='*50}")
        logger.info(f"✓ JobSpy is working! {message}")
        logger.info(f"{'='*50}")
    else:
        logger.error(f"\n{'='*50}")
        logger.error(f"✗ JobSpy test failed: {message}")
        logger.error(f"Recommendation: Try ScrapeGraphAI or custom scraper")
        logger.error(f"{'='*50}")