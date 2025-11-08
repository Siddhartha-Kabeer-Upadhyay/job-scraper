"""
Database operations for job intelligence platform
Handles CRUD operations for all tables with location validation
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config.database import get_db_connection, DatabaseManager
import logging
from typing import Optional, List, Dict, Tuple
import pandas as pd
from utils.location_validator import is_indian_city, validate_location_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobDatabase:
    """Handles all database operations for job data"""
    
    def __init__(self):
        DatabaseManager.initialize_pool()
    
    def __del__(self):
        DatabaseManager.close_all_connections()
    
    # ==================== COMPANY OPERATIONS ====================
    
    def insert_company(self, company_name: str) -> int:
        """Insert a company and return its ID"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if company exists
            cursor.execute(
                "SELECT company_id FROM companies WHERE company_name = %s",
                (company_name,)
            )
            result = cursor.fetchone()
            
            if result:
                return result[0]
            
            # Insert new company
            cursor.execute(
                """
                INSERT INTO companies (company_name)
                VALUES (%s)
                RETURNING company_id
                """,
                (company_name,)
            )
            company_id = cursor.fetchone()[0]
            conn.commit()
            
            return company_id
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error inserting company: {e}")
            raise
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    # ==================== LOCATION OPERATIONS ====================
    
    def insert_location(self, city: str, state: Optional[str] = None) -> int:
        """
        Insert a location and return its ID (with validation)
        
        Args:
            city: City name
            state: State name (optional)
            
        Returns:
            Location ID if valid, None if invalid
        """
        conn = None
        try:
            # Validate location first
            location_str = f"{city}, {state}" if state else city
            if not is_indian_city(location_str):
                logger.warning(f"Attempted to insert invalid location: {location_str}")
                return None
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if location exists
            cursor.execute(
                "SELECT location_id FROM locations WHERE city = %s",
                (city,)
            )
            result = cursor.fetchone()
            
            if result:
                return result[0]
            
            # Insert new location
            cursor.execute(
                """
                INSERT INTO locations (city, state)
                VALUES (%s, %s)
                RETURNING location_id
                """,
                (city, state)
            )
            location_id = cursor.fetchone()[0]
            conn.commit()
            
            return location_id
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error inserting location: {e}")
            raise
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    # ==================== SKILL OPERATIONS ====================
    
    def insert_skill(self, skill_name: str, skill_category: Optional[str] = None) -> int:
        """Insert a skill and return its ID"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if skill exists
            cursor.execute(
                "SELECT skill_id FROM skills WHERE LOWER(skill_name) = LOWER(%s)",
                (skill_name,)
            )
            result = cursor.fetchone()
            
            if result:
                return result[0]
            
            # Insert new skill
            cursor.execute(
                """
                INSERT INTO skills (skill_name, skill_category)
                VALUES (%s, %s)
                RETURNING skill_id
                """,
                (skill_name, skill_category)
            )
            skill_id = cursor.fetchone()[0]
            conn.commit()
            
            return skill_id
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error inserting skill: {e}")
            raise
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    def bulk_insert_skills(self, skills_dict: Dict[str, List[str]]):
        """Bulk insert skills from skill_keywords.json"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            total_inserted = 0
            
            for category, skills in skills_dict.items():
                # Clean category name
                category_clean = category.replace('_', ' ').title()
                
                for skill in skills:
                    try:
                        cursor.execute(
                            """
                            INSERT INTO skills (skill_name, skill_category)
                            VALUES (%s, %s)
                            ON CONFLICT (skill_name) DO NOTHING
                            """,
                            (skill, category_clean)
                        )
                        if cursor.rowcount > 0:
                            total_inserted += 1
                    except Exception as e:
                        logger.warning(f"Could not insert skill '{skill}': {e}")
                        continue
            
            conn.commit()
            logger.info(f"✓ Bulk inserted {total_inserted} skills")
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error in bulk skill insert: {e}")
            raise
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    # ==================== JOB OPERATIONS ====================
    
    def insert_job(self, job_data: Dict) -> Optional[int]:
        """
        Insert a job posting and return its ID (with location validation)
        
        Args:
            job_data: Dictionary with job information
            
        Returns:
            Job ID if successful, None if validation fails
        """
        conn = None
        try:
            # Validate location before insertion
            if job_data.get('city'):
                location_str = f"{job_data['city']}, {job_data.get('state', '')}"
                validation = validate_location_data(location_str)
                
                if not validation['is_valid']:
                    logger.warning(f"Skipping job with invalid location: {location_str} - {validation['rejection_reason']}")
                    return None
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if job URL already exists (avoid duplicates)
            if job_data.get('job_url'):
                cursor.execute(
                    "SELECT job_id FROM jobs WHERE job_url = %s",
                    (job_data['job_url'],)
                )
                result = cursor.fetchone()
                if result:
                    logger.debug(f"Job already exists: {job_data['job_url']}")
                    return result[0]
            
            # Get or create company
            company_id = None
            if job_data.get('company_name'):
                company_id = self.insert_company(job_data['company_name'])
            
            # Get or create location (will validate again)
            location_id = None
            if job_data.get('city'):
                location_id = self.insert_location(
                    job_data['city'],
                    job_data.get('state')
                )
                
                # If location validation fails, skip this job
                if location_id is None:
                    logger.warning(f"Cannot insert job - invalid location: {job_data.get('city')}")
                    return None
            
            # Insert job
            cursor.execute(
                """
                INSERT INTO jobs (
                    job_title, company_id, location_id, job_description,
                    job_url, experience_level, job_type, salary_min,
                    salary_max, posted_date, source_portal
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING job_id
                """,
                (
                    job_data.get('job_title'),
                    company_id,
                    location_id,
                    job_data.get('job_description'),
                    job_data.get('job_url'),
                    job_data.get('experience_level'),
                    job_data.get('job_type'),
                    job_data.get('salary_min'),
                    job_data.get('salary_max'),
                    job_data.get('posted_date'),
                    job_data.get('source_portal')
                )
            )
            job_id = cursor.fetchone()[0]
            conn.commit()
            
            return job_id
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error inserting job: {e}")
            return None
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    # ==================== JOB-SKILL MAPPING ====================
    
    def link_job_skills(self, job_id: int, skill_ids: List[int]):
        """Link a job with multiple skills"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for skill_id in skill_ids:
                cursor.execute(
                    """
                    INSERT INTO job_skills (job_id, skill_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (job_id, skill_id)
                )
            
            conn.commit()
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error linking job skills: {e}")
            raise
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    # ==================== BULK OPERATIONS ====================
    
    def bulk_insert_jobs(self, jobs_df: pd.DataFrame, skills_extracted: Dict[int, List[str]]):
        """
        Bulk insert jobs from a DataFrame
        
        Args:
            jobs_df: DataFrame with job data
            skills_extracted: Dictionary mapping DataFrame index to list of skill names
        """
        logger.info(f"Starting bulk insert of {len(jobs_df)} jobs...")
        
        inserted_count = 0
        skipped_count = 0
        error_count = 0
        
        for idx, row in jobs_df.iterrows():
            try:
                # Prepare job data
                job_data = {
                    'job_title': row.get('title'),
                    'company_name': row.get('company'),
                    'city': row.get('location'),
                    'job_description': row.get('description'),
                    'job_url': row.get('job_url'),
                    'source_portal': row.get('source_portal'),
                    'posted_date': row.get('date_posted'),
                    'job_type': row.get('job_type'),
                    'experience_level': row.get('job_level')
                }
                
                # Extract salary if available
                if 'min_amount' in row and pd.notna(row['min_amount']):
                    job_data['salary_min'] = row['min_amount']
                if 'max_amount' in row and pd.notna(row['max_amount']):
                    job_data['salary_max'] = row['max_amount']
                
                # Insert job
                job_id = self.insert_job(job_data)
                
                if job_id:
                    # Link skills if extracted
                    if idx in skills_extracted and skills_extracted[idx]:
                        skill_ids = []
                        for skill_name in skills_extracted[idx]:
                            skill_id = self.insert_skill(skill_name)
                            skill_ids.append(skill_id)
                        
                        if skill_ids:
                            self.link_job_skills(job_id, skill_ids)
                    
                    inserted_count += 1
                else:
                    skipped_count += 1
                
                # Progress update every 100 jobs
                if (inserted_count + skipped_count) % 100 == 0:
                    logger.info(f"Progress: {inserted_count} inserted, {skipped_count} skipped")
                    
            except Exception as e:
                error_count += 1
                logger.error(f"Error processing row {idx}: {e}")
                continue
        
        logger.info(f"\n{'='*50}")
        logger.info(f"Bulk insert complete!")
        logger.info(f"✓ Inserted: {inserted_count}")
        logger.info(f"⊘ Skipped: {skipped_count}")
        logger.info(f"✗ Errors: {error_count}")
        logger.info(f"{'='*50}")
    
    # ==================== QUERY OPERATIONS ====================
    
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
    
    def get_total_companies(self) -> int:
        """Get total number of companies"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM companies")
            return cursor.fetchone()[0]
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    def get_total_skills(self) -> int:
        """Get total number of unique skills"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM skills")
            return cursor.fetchone()[0]
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    def get_jobs_by_city(self) -> List[Tuple]:
        """Get job count by city"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT l.city, COUNT(j.job_id) as job_count
                FROM locations l
                LEFT JOIN jobs j ON l.location_id = j.location_id
                GROUP BY l.city
                ORDER BY job_count DESC
                """
            )
            return cursor.fetchall()
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    def get_database_stats(self) -> Dict:
        """Get overall database statistics"""
        return {
            'total_jobs': self.get_total_jobs(),
            'total_companies': self.get_total_companies(),
            'total_skills': self.get_total_skills(),
            'jobs_by_city': self.get_jobs_by_city()
        }
    
    def get_data_quality_stats(self) -> Dict:
        """
        Get data quality statistics
        
        Returns:
            Dictionary with quality metrics
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Total jobs
            cursor.execute("SELECT COUNT(*) FROM jobs")
            total_jobs = cursor.fetchone()[0]
            
            # Jobs with valid locations
            cursor.execute("""
                SELECT COUNT(*) FROM jobs j
                JOIN locations l ON j.location_id = l.location_id
                WHERE l.city IS NOT NULL AND l.city != ''
            """)
            jobs_with_location = cursor.fetchone()[0]
            
            # Jobs with salary info
            cursor.execute("""
                SELECT COUNT(*) FROM jobs
                WHERE salary_min IS NOT NULL OR salary_max IS NOT NULL
            """)
            jobs_with_salary = cursor.fetchone()[0]
            
            # Jobs with descriptions
            cursor.execute("""
                SELECT COUNT(*) FROM jobs
                WHERE job_description IS NOT NULL AND job_description != ''
            """)
            jobs_with_description = cursor.fetchone()[0]
            
            # Unique locations
            cursor.execute("SELECT COUNT(DISTINCT city) FROM locations")
            unique_cities = cursor.fetchone()[0]
            
            return {
                'total_jobs': total_jobs,
                'jobs_with_valid_location': jobs_with_location,
                'jobs_with_salary': jobs_with_salary,
                'jobs_with_description': jobs_with_description,
                'unique_cities': unique_cities,
                'location_coverage': round(jobs_with_location / total_jobs * 100, 2) if total_jobs > 0 else 0,
                'salary_coverage': round(jobs_with_salary / total_jobs * 100, 2) if total_jobs > 0 else 0,
                'description_coverage': round(jobs_with_description / total_jobs * 100, 2) if total_jobs > 0 else 0
            }
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    
    def validate_database_locations(self) -> Dict:
        """
        Validate all locations in the database
        
        Returns:
            Dictionary with validation results
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get all locations
            cursor.execute("SELECT location_id, city, state FROM locations")
            locations = cursor.fetchall()
            
            valid_count = 0
            invalid_count = 0
            invalid_locations = []
            
            for location_id, city, state in locations:
                location_str = f"{city}, {state}" if state else city
                if is_indian_city(location_str):
                    valid_count += 1
                else:
                    invalid_count += 1
                    invalid_locations.append({
                        'location_id': location_id,
                        'city': city,
                        'state': state
                    })
            
            return {
                'total_locations': len(locations),
                'valid_locations': valid_count,
                'invalid_locations': invalid_count,
                'invalid_location_details': invalid_locations[:10]  # Show first 10
            }
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)


# ==================== HELPER FUNCTIONS ====================

def initialize_database():
    """Initialize database with schema"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Read and execute schema
        schema_path = Path(__file__).parent / 'schema.sql'
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        cursor.execute(schema_sql)
        conn.commit()
        
        logger.info("✓ Database schema initialized successfully")
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        if conn:
            cursor.close()
            DatabaseManager.return_connection(conn)

def load_initial_skills():
    """Load skills from skill_keywords.json into database"""
    import json
    
    try:
        skills_path = Path(__file__).parent.parent / 'data_processing' / 'skill_keywords.json'
        with open(skills_path, 'r') as f:
            skills_dict = json.load(f)
        
        db = JobDatabase()
        db.bulk_insert_skills(skills_dict)
        
        logger.info("✓ Initial skills loaded successfully")
        
    except Exception as e:
        logger.error(f"Error loading initial skills: {e}")
        raise


def main():
    """Test database operations"""
    try:
        # Initialize database
        logger.info("Initializing database...")
        initialize_database()
        
        # Load initial skills
        logger.info("Loading initial skills...")
        load_initial_skills()
        
        # Get stats
        db = JobDatabase()
        stats = db.get_database_stats()
        
        logger.info("\n" + "="*50)
        logger.info("Database Statistics:")
        logger.info(f"Total Jobs: {stats['total_jobs']}")
        logger.info(f"Total Companies: {stats['total_companies']}")
        logger.info(f"Total Skills: {stats['total_skills']}")
        logger.info("="*50)
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    main()
