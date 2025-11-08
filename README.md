# Open Source Job Intelligence Platform

A comprehensive platform that scrapes job postings from Indian job portals, analyzes skill demand, and provides market insights for tech roles.

## Features

- **Multi-Portal Scraping**: Scrape jobs from LinkedIn, Indeed, and Naukri
- **Skill Extraction**: Automatic skill detection from job descriptions using NLP
- **Analytics Dashboard**: Interactive visualizations for job market trends
- **Database Management**: Normalized PostgreSQL database with efficient querying
- **Market Insights**: 
  - Top in-demand skills by location
  - Company hiring trends
  - Skill co-occurrence analysis
  - Experience level demand

## Tech Stack

- **Backend**: Python 3.9+
- **Database**: PostgreSQL
- **Scraping**: JobSpy, BeautifulSoup, Selenium
- **NLP**: spaCy, NLTK
- **Dashboard**: Streamlit
- **Visualization**: Plotly, Matplotlib

## Project Structure

```
job-intelligence-platform/
├── config/              # Configuration and database connection
├── scrapers/            # Web scraping modules
├── data_processing/     # Data cleaning and skill extraction
├── database/            # Database operations and queries
├── analytics/           # Analytics and insights
├── dashboard/           # Streamlit dashboard
└── utils/              # Helper utilities
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Siddhartha-Kabeer-Upadhyay/job-intelligence-platform.git
cd job-intelligence-platform
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_intelligence_db
DB_USER=postgres
DB_PASSWORD=your_password
```

### 5. Initialize Database

```bash
python database/db_operations.py
```

This will:
- Create all tables
- Set up indexes
- Load initial skill keywords

### 6. Test Scrapers

```bash
# Test JobSpy
python scrapers/test_jobspy.py

# If JobSpy doesn't work, test alternatives
python scrapers/test_scrapegraphai.py
```

### 7. Scrape Jobs

```bash
python scrapers/scraper_manager.py
```

This will scrape jobs from configured portals and cities.

### 8. Process and Load Data

```bash
python data_processing/data_cleaner.py
```

### 9. Run Dashboard

```bash
streamlit run dashboard/app.py
```

## 📊 Database Schema

```sql
companies (company_id, company_name, industry)
locations (location_id, city, state)
jobs (job_id, job_title, company_id, location_id, description, url, ...)
skills (skill_id, skill_name, skill_category)
job_skills (job_id, skill_id)  -- Many-to-many relationship
```

## Configuration

Edit `config/settings.py` to customize:

- Target cities
- Search terms
- Scraping delay
- Maximum jobs per city

## Analytics Features

- **Skill Analysis**: Top skills overall and by location/role
- **Company Insights**: Top hiring companies and their job distribution
- **Location Trends**: Jobs by city comparison
- **Skill Co-occurrence**: Which skills are requested together
- **Experience Demand**: Experience level requirements for skills

## License

MIT License

## Team

1. **Siddhartha Kabeer Upadhyay** - Backend & Database
2. **Adrika Srivastava** - Frontend Development
3. **Vibhor Saini** - Data Processing & NLP
4. **Nelly** - Quality Assurance & Documentation

**Note**: This project is for educational purposes. Please respect the Terms of Service of job portals when scraping data.