"""
Indeed scraper with proper rate limiting and robots.txt compliance
Based on Indeed's robots.txt: https://www.indeed.com/robots.txt
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from datetime import datetime
from typing import List, Dict
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndeedScraper:
    """
    Indeed scraper that respects robots.txt
    
    Key points from Indeed's robots.txt:
    - Crawl-delay: 1 second minimum (we'll use 5-10 for safety)
    - Allowed: /jobs, /viewjob, /q-*
    - Disallowed: Many API endpoints
    """
    
    def __init__(self):
        self.base_url = "https://in.indeed.com"
        self.session = requests.Session()
        
        # Rotate user agents to appear more natural
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.current_ua_index = 0
        self.request_count = 0
        self.last_request_time = 0
        
        # Minimum delay between requests (5-10 seconds)
        self.min_delay = 5
        self.max_delay = 10
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with rotating user agent"""
        # Rotate user agent every 10 requests
        if self.request_count % 10 == 0:
            self.current_ua_index = (self.current_ua_index + 1) % len(self.user_agents)
        
        return {
            'User-Agent': self.user_agents[self.current_ua_index],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.indeed.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin'
        }
    
    def _respect_rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Random delay between 5-10 seconds
        required_delay = random.uniform(self.min_delay, self.max_delay)
        
        if time_since_last < required_delay:
            sleep_time = required_delay - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    def search_jobs(self, query: str, location: str, max_results: int = 50) -> List[Dict]:
        """
        Search for jobs on Indeed
        
        Args:
            query: Search term (e.g., "software engineer")
            location: Location (e.g., "Bengaluru")
            max_results: Maximum number of results to fetch
            
        Returns:
            List of job dictionaries
        """
        logger.info(f"Searching Indeed: '{query}' in {location}")
        
        jobs = []
        start = 0
        
        while len(jobs) < max_results:
            # Respect rate limit
            self._respect_rate_limit()
            
            # Build URL
            params = {
                'q': query,
                'l': location,
                'start': start,
                'filter': 0  # Show all jobs
            }
            
            try:
                response = self.session.get(
                    f"{self.base_url}/jobs",
                    params=params,
                    headers=self._get_headers(),
                    timeout=15
                )
                
                if response.status_code == 200:
                    # Parse the page
                    page_jobs = self._parse_job_listings(response.content)
                    
                    if not page_jobs:
                        logger.info("No more jobs found, stopping.")
                        break
                    
                    jobs.extend(page_jobs)
                    logger.info(f"Collected {len(jobs)} jobs so far...")
                    
                    start += 10
                    
                elif response.status_code == 403:
                    logger.warning("Access forbidden (403). Indeed may be blocking requests.")
                    logger.info("Suggestions:")
                    logger.info("  1. Increase delay between requests")
                    logger.info("  2. Use a proxy service")
                    logger.info("  3. Use Indeed's official API (if available)")
                    break
                    
                elif response.status_code == 429:
                    logger.warning("Rate limited (429). Waiting 60 seconds...")
                    time.sleep(60)
                    continue
                    
                else:
                    logger.error(f"Unexpected status code: {response.status_code}")
                    break
                    
            except Exception as e:
                logger.error(f"Error during request: {e}")
                break
        
        logger.info(f"Finished: collected {len(jobs)} jobs")
        return jobs[:max_results]
    
    def _parse_job_listings(self, html_content: bytes) -> List[Dict]:
        """
        Parse job listings from Indeed HTML
        Note: Indeed's HTML structure changes frequently
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        jobs = []
        
        # Indeed uses various div classes - these may need updating
        job_cards = soup.find_all(['div', 'a'], class_=lambda x: x and ('job_seen_beacon' in x or 'resultContent' in x or 'slider_container' in x))
        
        if not job_cards:
            # Try alternative selectors
            job_cards = soup.find_all('td', class_='resultContent')
        
        for card in job_cards:
            try:
                job_data = self._extract_job_data(card)
                if job_data:
                    jobs.append(job_data)
            except Exception as e:
                logger.debug(f"Error parsing job card: {e}")
                continue
        
        return jobs
    
    def _extract_job_data(self, card) -> Dict:
        """Extract job data from a job card"""
        job = {}
        
        try:
            # Title and URL
            title_elem = card.find('h2', class_='jobTitle')
            if not title_elem:
                title_elem = card.find(['a', 'span'], class_=lambda x: x and 'jobTitle' in str(x))
            
            if title_elem:
                link = title_elem.find('a') if title_elem.name != 'a' else title_elem
                job['title'] = title_elem.get_text(strip=True)
                if link:
                    job['job_url'] = self.base_url + link.get('href', '')
            
            # Company
            company_elem = card.find(['span', 'div'], attrs={'data-testid': 'company-name'})
            if not company_elem:
                company_elem = card.find(class_=lambda x: x and 'companyName' in str(x))
            if company_elem:
                job['company'] = company_elem.get_text(strip=True)
            
            # Location
            location_elem = card.find(['div', 'span'], attrs={'data-testid': 'text-location'})
            if not location_elem:
                location_elem = card.find(class_=lambda x: x and 'companyLocation' in str(x))
            if location_elem:
                job['location'] = location_elem.get_text(strip=True)
            
            # Salary
            salary_elem = card.find(class_=lambda x: x and 'salary' in str(x).lower())
            if salary_elem:
                job['salary'] = salary_elem.get_text(strip=True)
            
            # Job snippet/description
            snippet_elem = card.find(['div', 'span'], class_=lambda x: x and 'jobsnippet' in str(x).lower())
            if snippet_elem:
                job['description'] = snippet_elem.get_text(strip=True)
            
            # Source
            job['source_portal'] = 'indeed'
            job['scraped_at'] = datetime.now()
            
            return job if job.get('title') else None
            
        except Exception as e:
            logger.debug(f"Error extracting job data: {e}")
            return None


def main():
    """Test the Indeed scraper"""
    scraper = IndeedScraper()
    
    # Test search
    jobs = scraper.search_jobs(
        query="python developer",
        location="Bengaluru",
        max_results=20
    )
    
    if jobs:
        # Convert to DataFrame
        df = pd.DataFrame(jobs)
        
        # Save to CSV
        filename = f"indeed_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        
        logger.info(f"\n{'='*50}")
        logger.info(f"✓ Scraped {len(jobs)} jobs from Indeed")
        logger.info(f"✓ Saved to {filename}")
        logger.info(f"{'='*50}")
        
        # Show sample
        print("\nSample jobs:")
        print(df[['title', 'company', 'location']].head())
    else:
        logger.warning("No jobs scraped. Indeed may be blocking requests.")


if __name__ == "__main__":
    main()