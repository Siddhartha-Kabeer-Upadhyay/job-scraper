"""
Analytics and insights generation for job intelligence platform
Provides high-level functions for data analysis and reporting
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config.database import get_db_connection, DatabaseManager
from database import queries
import pandas as pd
import logging
from typing import Dict, List, Tuple, Optional

import warnings
warnings.filterwarnings('ignore', message='pandas only supports SQLAlchemy')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobMarketAnalytics:
    """Generate insights from job market data"""
    
    def __init__(self):
        DatabaseManager.initialize_pool()
    
    def __del__(self):
        DatabaseManager.close_all_connections()
    
    def _execute_query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Execute a query and return results as DataFrame"""
        conn = None
        try:
            conn = get_db_connection()
            df = pd.read_sql_query(query, conn, params=params)
            return df
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
        finally:
            if conn:
                DatabaseManager.return_connection(conn)
    
    # ==================== SKILL ANALYTICS ====================
    
    def get_top_skills(self, limit: int = 20) -> pd.DataFrame:
        """
        Get top in-demand skills overall
        
        Returns:
            DataFrame with columns: skill_name, skill_category, job_count, percentage
        """
        logger.info(f"Fetching top {limit} skills...")
        df = self._execute_query(queries.TOP_SKILLS_OVERALL, (limit,))
        return df
    
    def get_top_skills_by_city(self, city: str, limit: int = 20) -> pd.DataFrame:
        """
        Get top skills for a specific city
        
        Args:
            city: City name (e.g., 'Bengaluru', 'Mumbai')
            limit: Number of top skills to return
            
        Returns:
            DataFrame with columns: city, skill_name, job_count
        """
        logger.info(f"Fetching top {limit} skills for {city}...")
        df = self._execute_query(queries.TOP_SKILLS_BY_LOCATION, (city, limit))
        return df
    
    def get_top_skills_by_role(self, role_keyword: str, limit: int = 20) -> pd.DataFrame:
        """
        Get top skills for a specific job role
        
        Args:
            role_keyword: Keyword to search in job titles (e.g., 'analyst', 'engineer')
            limit: Number of top skills to return
            
        Returns:
            DataFrame with columns: job_title, skill_name, frequency
        """
        logger.info(f"Fetching top {limit} skills for role: {role_keyword}...")
        df = self._execute_query(queries.TOP_SKILLS_BY_ROLE, (f'%{role_keyword}%', limit))
        return df
    
    def get_skill_cooccurrence(self, min_count: int = 10, limit: int = 50) -> pd.DataFrame:
        """
        Get skills that frequently appear together
        
        Args:
            min_count: Minimum co-occurrence count
            limit: Maximum number of pairs to return
            
        Returns:
            DataFrame with columns: skill_1, skill_2, co_occurrence_count
        """
        logger.info(f"Analyzing skill co-occurrence (min count: {min_count})...")
        df = self._execute_query(queries.SKILL_COOCCURRENCE, (min_count, limit))
        return df
    
    def compare_skills_across_cities(self, skills: List[str], cities: List[str] = None) -> pd.DataFrame:
        """
        Compare demand for specific skills across cities
        
        Args:
            skills: List of skill names to compare
            cities: List of cities to compare (None = all cities)
            
        Returns:
            DataFrame with skills as rows and cities as columns showing job counts
        """
        logger.info(f"Comparing {len(skills)} skills across cities...")
        
        if cities is None:
            cities = self.get_all_cities()['city'].tolist()
        
        comparison_data = []
        
        for skill in skills:
            row_data = {'skill': skill}
            for city in cities:
                df = self._execute_query(queries.TOP_SKILLS_BY_LOCATION, (city, 1000))
                count = df[df['skill_name'].str.lower() == skill.lower()]['job_count'].sum()
                row_data[city] = count
            comparison_data.append(row_data)
        
        return pd.DataFrame(comparison_data)
    
    # ==================== COMPANY ANALYTICS ====================
    
    def get_top_hiring_companies(self, limit: int = 20) -> pd.DataFrame:
        """
        Get companies with most job postings
        
        Returns:
            DataFrame with columns: company_name, industry, job_count, cities_hiring_in
        """
        logger.info(f"Fetching top {limit} hiring companies...")
        df = self._execute_query(queries.TOP_HIRING_COMPANIES, (limit,))
        return df
    
    def get_companies_by_city(self, city: str, limit: int = 20) -> pd.DataFrame:
        """
        Get top hiring companies in a specific city
        
        Args:
            city: City name
            limit: Number of companies to return
            
        Returns:
            DataFrame with columns: city, company_name, job_count
        """
        logger.info(f"Fetching top {limit} companies in {city}...")
        df = self._execute_query(queries.COMPANIES_BY_CITY, (city, limit))
        return df
    
    # ==================== LOCATION ANALYTICS ====================
    
    def get_jobs_by_city(self) -> pd.DataFrame:
        """
        Get job distribution across cities
        
        Returns:
            DataFrame with columns: city, state, job_count, company_count
        """
        logger.info("Fetching job distribution by city...")
        df = self._execute_query(queries.JOBS_BY_CITY)
        return df
    
    def get_all_cities(self) -> pd.DataFrame:
        """Get list of all cities with jobs"""
        df = self.get_jobs_by_city()
        return df[df['job_count'] > 0]
    
    # ==================== EXPERIENCE ANALYTICS ====================
    
    def get_experience_demand_by_skill(self, skill_name: str) -> pd.DataFrame:
        """
        Get experience level demand for a specific skill
        
        Args:
            skill_name: Skill to analyze
            
        Returns:
            DataFrame with columns: skill_name, experience_level, job_count
        """
        logger.info(f"Analyzing experience demand for {skill_name}...")
        df = self._execute_query(queries.EXPERIENCE_DEMAND_BY_SKILL, (skill_name,))
        return df
    
    def get_experience_distribution(self) -> pd.DataFrame:
        """
        Get overall distribution of experience levels
        
        Returns:
            DataFrame with columns: experience_level, job_count, percentage
        """
        logger.info("Fetching experience level distribution...")
        df = self._execute_query(queries.EXPERIENCE_DISTRIBUTION)
        return df
    
    # ==================== SALARY ANALYTICS ====================
    
    def get_salary_by_skill(self, min_jobs: int = 5, limit: int = 20) -> pd.DataFrame:
        """
        Get average salaries by skill
        
        Args:
            min_jobs: Minimum number of jobs required for a skill
            limit: Number of skills to return
            
        Returns:
            DataFrame with columns: skill_name, avg_min_salary, avg_max_salary, job_count
        """
        logger.info(f"Fetching salary data by skill (min {min_jobs} jobs)...")
        df = self._execute_query(queries.SALARY_BY_SKILL, (min_jobs, limit))
        return df
    
    def get_salary_by_city(self) -> pd.DataFrame:
        """
        Get average salaries by city
        
        Returns:
            DataFrame with columns: city, avg_min_salary, avg_max_salary, job_count
        """
        logger.info("Fetching salary data by city...")
        df = self._execute_query(queries.SALARY_BY_CITY)
        return df
    
    # ==================== FILTERED ANALYTICS ====================

    def get_jobs_with_salary(self) -> int:
        """Get count of jobs that have salary information"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM jobs 
                WHERE salary_min IS NOT NULL 
                  AND salary_max IS NOT NULL
                  AND salary_min > 0
                """
            )
            return cursor.fetchone()[0]
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)

    def get_jobs_by_experience_and_city(self, city: str) -> pd.DataFrame:
        """Get experience level distribution for a specific city"""
        query = """
            SELECT 
                j.experience_level,
                COUNT(*) as job_count
            FROM jobs j
            JOIN locations l ON j.location_id = l.location_id
            WHERE l.city = %s AND j.experience_level IS NOT NULL
            GROUP BY j.experience_level
            ORDER BY job_count DESC
        """
        return self._execute_query(query, (city,))

    def get_jobs_by_type_and_city(self, city: str) -> pd.DataFrame:
        """Get job type distribution for a specific city"""
        query = """
            SELECT 
                j.job_type,
                COUNT(*) as job_count
            FROM jobs j
            JOIN locations l ON j.location_id = l.location_id
            WHERE l.city = %s AND j.job_type IS NOT NULL
            GROUP BY j.job_type
            ORDER BY job_count DESC
        """
        return self._execute_query(query, (city,))

    def get_top_skills_by_experience(self, experience_level: str, limit: int = 20) -> pd.DataFrame:
        """Get top skills for a specific experience level"""
        query = """
            SELECT 
                s.skill_name,
                s.skill_category,
                COUNT(DISTINCT j.job_id) as job_count
            FROM skills s
            JOIN job_skills js ON s.skill_id = js.skill_id
            JOIN jobs j ON js.job_id = j.job_id
            WHERE j.experience_level = %s
            GROUP BY s.skill_id, s.skill_name, s.skill_category
            ORDER BY job_count DESC
            LIMIT %s
        """
        return self._execute_query(query, (experience_level, limit))

    def get_top_skills_by_job_type(self, job_type: str, limit: int = 20) -> pd.DataFrame:
        """Get top skills for a specific job type"""
        query = """
            SELECT 
                s.skill_name,
                s.skill_category,
                COUNT(DISTINCT j.job_id) as job_count
            FROM skills s
            JOIN job_skills js ON s.skill_id = js.skill_id
            JOIN jobs j ON js.job_id = j.job_id
            WHERE j.job_type = %s
            GROUP BY s.skill_id, s.skill_name, s.skill_category
            ORDER BY job_count DESC
            LIMIT %s
        """
        return self._execute_query(query, (job_type, limit))

    def get_companies_hiring_for_experience(self, experience_level: str, limit: int = 20) -> pd.DataFrame:
        """Get top companies hiring for a specific experience level"""
        query = """
            SELECT 
                c.company_name,
                COUNT(j.job_id) as job_count
            FROM companies c
            JOIN jobs j ON c.company_id = j.company_id
            WHERE j.experience_level = %s
            GROUP BY c.company_id, c.company_name
            ORDER BY job_count DESC
            LIMIT %s
        """
        return self._execute_query(query, (experience_level, limit))

    def search_jobs_by_filters(self, 
                               city: str = None, 
                               experience_level: str = None,
                               job_type: str = None,
                               skill_name: str = None,
                               limit: int = 100) -> pd.DataFrame:
        """
        Search jobs with multiple filters
        
        Args:
            city: Filter by city (optional)
            experience_level: Filter by experience level (optional)
            job_type: Filter by job type (optional)
            skill_name: Filter by skill (optional)
            limit: Maximum results
        """
        query = """
            SELECT DISTINCT
                j.job_id,
                j.job_title,
                c.company_name,
                l.city,
                j.experience_level,
                j.job_type,
                j.job_url,
                j.posted_date
            FROM jobs j
            LEFT JOIN companies c ON j.company_id = c.company_id
            LEFT JOIN locations l ON j.location_id = l.location_id
            LEFT JOIN job_skills js ON j.job_id = js.job_id
            LEFT JOIN skills s ON js.skill_id = s.skill_id
            WHERE 1=1
        """
        
        params = []
        
        if city:
            query += " AND l.city = %s"
            params.append(city)
        
        if experience_level:
            query += " AND j.experience_level = %s"
            params.append(experience_level)
        
        if job_type:
            query += " AND j.job_type = %s"
            params.append(job_type)
        
        if skill_name:
            query += " AND LOWER(s.skill_name) = LOWER(%s)"
            params.append(skill_name)
        
        query += " ORDER BY j.created_at DESC LIMIT %s"
        params.append(limit)
        
        return self._execute_query(query, tuple(params))
        
    # ==================== PORTAL ANALYTICS ====================
    
    def get_jobs_by_portal(self) -> pd.DataFrame:
        """
        Get job distribution by source portal
        
        Returns:
            DataFrame with columns: source_portal, job_count, percentage
        """
        logger.info("Fetching job distribution by portal...")
        df = self._execute_query(queries.JOBS_BY_PORTAL)
        return df
    
    def get_total_jobs(self) -> int:
        """Get total number of jobs in database"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM jobs")
            return cursor.fetchone()[0]
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)

    def get_jobs_with_salary(self) -> int:
        """Get count of jobs that have salary information"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM jobs 
                WHERE salary_min IS NOT NULL 
                  AND salary_max IS NOT NULL
                  AND salary_min > 0
                """
            )
            return cursor.fetchone()[0]
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    # ==================== COMPREHENSIVE REPORTS ====================
    
    def generate_market_overview(self) -> Dict:
        """
        Generate comprehensive market overview report
        
        Returns:
            Dictionary with various market statistics
        """
        logger.info("Generating market overview report...")
        
        overview = {}
        
        # Basic stats
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM jobs")
            overview['total_jobs'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM companies")
            overview['total_companies'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM skills")
            overview['total_skills'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT location_id) FROM jobs")
            overview['total_cities'] = cursor.fetchone()[0]
            
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
        
        # Top skills
        overview['top_10_skills'] = self.get_top_skills(10).to_dict('records')
        
        # Top companies
        overview['top_10_companies'] = self.get_top_hiring_companies(10).to_dict('records')
        
        # Job distribution by city
        overview['jobs_by_city'] = self.get_jobs_by_city().to_dict('records')
        
        # Experience distribution
        overview['experience_distribution'] = self.get_experience_distribution().to_dict('records')
        
        # Portal distribution
        overview['jobs_by_portal'] = self.get_jobs_by_portal().to_dict('records')
        
        logger.info("✓ Market overview generated")
        return overview
    
    def generate_city_report(self, city: str) -> Dict:
        """
        Generate detailed report for a specific city
        
        Args:
            city: City name
            
        Returns:
            Dictionary with city-specific statistics
        """
        logger.info(f"Generating report for {city}...")
        
        report = {
            'city': city,
            'top_skills': self.get_top_skills_by_city(city, 15).to_dict('records'),
            'top_companies': self.get_companies_by_city(city, 15).to_dict('records')
        }
        
        # Get total jobs in city
        jobs_df = self.get_jobs_by_city()
        city_data = jobs_df[jobs_df['city'] == city]
        if not city_data.empty:
            report['total_jobs'] = int(city_data.iloc[0]['job_count'])
            report['total_companies'] = int(city_data.iloc[0]['company_count'])
        
        logger.info(f"✓ Report generated for {city}")
        return report
    
    def generate_skill_report(self, skill_name: str) -> Dict:
        """
        Generate detailed report for a specific skill
        
        Args:
            skill_name: Skill to analyze
            
        Returns:
            Dictionary with skill-specific statistics
        """
        logger.info(f"Generating report for skill: {skill_name}...")
        
        report = {
            'skill': skill_name,
            'experience_demand': self.get_experience_demand_by_skill(skill_name).to_dict('records')
        }
        
        # Get total jobs with this skill
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT COUNT(DISTINCT js.job_id)
                FROM job_skills js
                JOIN skills s ON js.skill_id = s.skill_id
                WHERE LOWER(s.skill_name) = LOWER(%s)
                """,
                (skill_name,)
            )
            report['total_jobs'] = cursor.fetchone()[0]
            
            # Get top cities for this skill
            cursor.execute(
                """
                SELECT l.city, COUNT(j.job_id) as job_count
                FROM skills s
                JOIN job_skills js ON s.skill_id = js.skill_id
                JOIN jobs j ON js.job_id = j.job_id
                JOIN locations l ON j.location_id = l.location_id
                WHERE LOWER(s.skill_name) = LOWER(%s)
                GROUP BY l.city
                ORDER BY job_count DESC
                LIMIT 5
                """,
                (skill_name,)
            )
            report['top_cities'] = [{'city': row[0], 'job_count': row[1]} for row in cursor.fetchall()]
            
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
        
        logger.info(f"✓ Report generated for {skill_name}")
        return report
    
    # ==================== EXPORT FUNCTIONS ====================
    
    def export_report_to_csv(self, report_type: str, filename: str = None, **kwargs):
        """
        Export a report to CSV
        
        Args:
            report_type: Type of report ('top_skills', 'top_companies', 'jobs_by_city', etc.)
            filename: Output filename (auto-generated if None)
            **kwargs: Additional arguments for specific reports
        """
        from datetime import datetime
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{report_type}_{timestamp}.csv"
        
        report_functions = {
            'top_skills': lambda: self.get_top_skills(kwargs.get('limit', 50)),
            'top_companies': lambda: self.get_top_hiring_companies(kwargs.get('limit', 50)),
            'jobs_by_city': lambda: self.get_jobs_by_city(),
            'skill_cooccurrence': lambda: self.get_skill_cooccurrence(
                kwargs.get('min_count', 10),
                kwargs.get('limit', 100)
            ),
            'experience_distribution': lambda: self.get_experience_distribution(),
            'salary_by_skill': lambda: self.get_salary_by_skill(
                kwargs.get('min_jobs', 5),
                kwargs.get('limit', 50)
            )
        }
        
        if report_type not in report_functions:
            logger.error(f"Unknown report type: {report_type}")
            return
        
        try:
            df = report_functions[report_type]()
            df.to_csv(filename, index=False)
            logger.info(f"✓ Report exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting report: {e}")
            raise


def main():
    """Generate sample reports"""
    analytics = JobMarketAnalytics()
    
    print("\n" + "="*60)
    print("JOB MARKET ANALYTICS - SAMPLE REPORTS")
    print("="*60)
    
    # Market Overview
    print("\n📊 MARKET OVERVIEW")
    print("-"*60)
    overview = analytics.generate_market_overview()
    print(f"Total Jobs: {overview['total_jobs']}")
    print(f"Total Companies: {overview['total_companies']}")
    print(f"Total Skills: {overview['total_skills']}")
    print(f"Total Cities: {overview['total_cities']}")
    
    # Top Skills
    print("\n🔧 TOP 10 SKILLS")
    print("-"*60)
    top_skills_df = analytics.get_top_skills(10)
    for idx, row in top_skills_df.iterrows():
        print(f"{idx+1}. {row['skill_name']} ({row['skill_category']}) - {row['job_count']} jobs ({row['percentage']}%)")
    
    # Top Companies
    print("\n🏢 TOP 10 HIRING COMPANIES")
    print("-"*60)
    top_companies_df = analytics.get_top_hiring_companies(10)
    for idx, row in top_companies_df.iterrows():
        print(f"{idx+1}. {row['company_name']} - {row['job_count']} jobs")
    
    # Jobs by City
    print("\n📍 JOBS BY CITY")
    print("-"*60)
    jobs_by_city_df = analytics.get_jobs_by_city()
    for idx, row in jobs_by_city_df.iterrows():
        if row['job_count'] > 0:
            print(f"{row['city']}: {row['job_count']} jobs, {row['company_count']} companies")
    
    # Skill Co-occurrence
    print("\n🔗 TOP SKILL COMBINATIONS")
    print("-"*60)
    cooccurrence_df = analytics.get_skill_cooccurrence(min_count=5, limit=10)
    for idx, row in cooccurrence_df.iterrows():
        print(f"{row['skill_1']} + {row['skill_2']}: {row['co_occurrence_count']} times")
    
    # Experience Distribution
    print("\n📈 EXPERIENCE LEVEL DISTRIBUTION")
    print("-"*60)
    exp_dist_df = analytics.get_experience_distribution()
    for idx, row in exp_dist_df.iterrows():
        print(f"{row['experience_level']}: {row['job_count']} jobs ({row['percentage']}%)")
    
    print("\n" + "="*60)
    print("✓ Analytics complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()