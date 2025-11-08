import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'job_intelligence_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Scraping Configuration
SCRAPING_CONFIG = {
    'delay': int(os.getenv('SCRAPING_DELAY', 3)),
    'max_jobs_per_city': int(os.getenv('MAX_JOBS_PER_CITY', 750)),
    'cities': ['Bengaluru', 'Mumbai', 'Pune', 'Delhi'],
    'search_terms': ['software engineer', 'developer', 'data analyst', 'tech'],
    'portals': ['indeed', 'linkedin'], 
}

# Skill Extraction Configuration
SKILL_EXTRACTION_CONFIG = {
    'min_skill_length': 2,
    'max_skill_length': 30,
    'case_sensitive': False
}
