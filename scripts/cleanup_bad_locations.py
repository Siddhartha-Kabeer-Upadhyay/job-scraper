"""
Script to cleanup jobs with invalid locations from the database
Removes US cities, null locations, and other non-Indian locations
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config.database import get_db_connection, DatabaseManager
from utils.location_validator import is_indian_city, validate_location_data
import logging
from datetime import datetime
import argparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def backup_database():
    """
    Create a backup log of current database state
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get current counts
        cursor.execute("SELECT COUNT(*) FROM jobs")
        total_jobs = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM locations")
        total_locations = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM companies")
        total_companies = cursor.fetchone()[0]
        
        backup_info = {
            'timestamp': datetime.now().isoformat(),
            'total_jobs': total_jobs,
            'total_locations': total_locations,
            'total_companies': total_companies
        }
        
        logger.info("=" * 60)
        logger.info("DATABASE BACKUP INFO")
        logger.info("=" * 60)
        logger.info(f"Timestamp: {backup_info['timestamp']}")
        logger.info(f"Total Jobs: {backup_info['total_jobs']}")
        logger.info(f"Total Locations: {backup_info['total_locations']}")
        logger.info(f"Total Companies: {backup_info['total_companies']}")
        logger.info("=" * 60)
        
        return backup_info
        
    finally:
        if conn:
            cursor.close()
            DatabaseManager.return_connection(conn)


def identify_invalid_locations():
    """
    Identify all invalid locations in the database
    
    Returns:
        List of (location_id, city, state, reason) tuples
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all locations
        cursor.execute("""
            SELECT location_id, city, state
            FROM locations
        """)
        locations = cursor.fetchall()
        
        invalid_locations = []
        
        for location_id, city, state in locations:
            # Skip if city is null
            if not city:
                invalid_locations.append((location_id, city, state, 'Null city'))
                continue
            
            # Validate location
            location_str = f"{city}, {state}" if state else city
            validation = validate_location_data(location_str)
            
            if not validation['is_valid']:
                invalid_locations.append((
                    location_id,
                    city,
                    state,
                    validation['rejection_reason']
                ))
        
        return invalid_locations
        
    finally:
        if conn:
            cursor.close()
            DatabaseManager.return_connection(conn)


def get_jobs_with_invalid_locations(invalid_location_ids):
    """
    Get count of jobs associated with invalid locations
    
    Args:
        invalid_location_ids: List of location IDs to check
        
    Returns:
        Number of jobs that will be affected
    """
    if not invalid_location_ids:
        return 0
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get jobs with these locations
        placeholders = ','.join(['%s'] * len(invalid_location_ids))
        query = f"""
            SELECT COUNT(*)
            FROM jobs
            WHERE location_id IN ({placeholders})
        """
        
        cursor.execute(query, invalid_location_ids)
        count = cursor.fetchone()[0]
        
        return count
        
    finally:
        if conn:
            cursor.close()
            DatabaseManager.return_connection(conn)


def cleanup_invalid_locations(dry_run=True):
    """
    Remove jobs and locations with invalid data
    
    Args:
        dry_run: If True, only report what would be deleted
    """
    logger.info("\n" + "=" * 60)
    logger.info("STARTING LOCATION CLEANUP")
    logger.info("Mode: " + ("DRY RUN" if dry_run else "LIVE"))
    logger.info("=" * 60)
    
    # Step 1: Backup
    logger.info("\nStep 1: Creating backup...")
    backup_info = backup_database()
    
    # Step 2: Identify invalid locations
    logger.info("\nStep 2: Identifying invalid locations...")
    invalid_locations = identify_invalid_locations()
    
    if not invalid_locations:
        logger.info("✓ No invalid locations found! Database is clean.")
        return
    
    # Report findings
    logger.info(f"\nFound {len(invalid_locations)} invalid locations:")
    
    # Group by rejection reason
    reasons = {}
    for loc_id, city, state, reason in invalid_locations:
        if reason not in reasons:
            reasons[reason] = []
        reasons[reason].append(f"{city}, {state}" if state else city)
    
    for reason, locs in reasons.items():
        logger.info(f"\n{reason}: {len(locs)} locations")
        # Show first 5 examples
        for loc in locs[:5]:
            logger.info(f"  - {loc}")
        if len(locs) > 5:
            logger.info(f"  ... and {len(locs) - 5} more")
    
    # Step 3: Count affected jobs
    logger.info("\nStep 3: Counting affected jobs...")
    invalid_location_ids = [loc[0] for loc in invalid_locations]
    affected_jobs = get_jobs_with_invalid_locations(invalid_location_ids)
    
    logger.info(f"Jobs to be removed: {affected_jobs}")
    
    # Step 4: Perform cleanup (if not dry run)
    if not dry_run:
        logger.info("\nStep 4: Performing cleanup...")
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Delete jobs with invalid locations
            placeholders = ','.join(['%s'] * len(invalid_location_ids))
            
            # First delete job_skills relationships
            cursor.execute(f"""
                DELETE FROM job_skills
                WHERE job_id IN (
                    SELECT job_id FROM jobs
                    WHERE location_id IN ({placeholders})
                )
            """, invalid_location_ids)
            
            deleted_job_skills = cursor.rowcount
            logger.info(f"  Deleted {deleted_job_skills} job-skill relationships")
            
            # Delete jobs
            cursor.execute(f"""
                DELETE FROM jobs
                WHERE location_id IN ({placeholders})
            """, invalid_location_ids)
            
            deleted_jobs = cursor.rowcount
            logger.info(f"  Deleted {deleted_jobs} jobs")
            
            # Delete invalid locations
            cursor.execute(f"""
                DELETE FROM locations
                WHERE location_id IN ({placeholders})
            """, invalid_location_ids)
            
            deleted_locations = cursor.rowcount
            logger.info(f"  Deleted {deleted_locations} locations")
            
            conn.commit()
            
            logger.info("\n✓ Cleanup completed successfully!")
            
            # Show final stats
            cursor.execute("SELECT COUNT(*) FROM jobs")
            final_jobs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM locations")
            final_locations = cursor.fetchone()[0]
            
            logger.info("\n" + "=" * 60)
            logger.info("FINAL DATABASE STATE")
            logger.info("=" * 60)
            logger.info(f"Jobs: {backup_info['total_jobs']} → {final_jobs} ({backup_info['total_jobs'] - final_jobs} removed)")
            logger.info(f"Locations: {backup_info['total_locations']} → {final_locations} ({backup_info['total_locations'] - final_locations} removed)")
            logger.info("=" * 60)
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error during cleanup: {e}")
            raise
        finally:
            if conn:
                cursor.close()
                DatabaseManager.return_connection(conn)
    else:
        logger.info("\n" + "=" * 60)
        logger.info("DRY RUN COMPLETE")
        logger.info("=" * 60)
        logger.info("No changes made to database.")
        logger.info(f"To perform actual cleanup, run with --execute flag")
        logger.info("=" * 60)


def cleanup_null_locations(dry_run=True):
    """
    Remove jobs with null/empty locations
    
    Args:
        dry_run: If True, only report what would be deleted
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Find jobs with null location_id
        cursor.execute("""
            SELECT COUNT(*)
            FROM jobs
            WHERE location_id IS NULL
        """)
        null_location_jobs = cursor.fetchone()[0]
        
        if null_location_jobs > 0:
            logger.info(f"\nFound {null_location_jobs} jobs with null locations")
            
            if not dry_run:
                # Delete job_skills first
                cursor.execute("""
                    DELETE FROM job_skills
                    WHERE job_id IN (
                        SELECT job_id FROM jobs WHERE location_id IS NULL
                    )
                """)
                
                # Delete jobs
                cursor.execute("DELETE FROM jobs WHERE location_id IS NULL")
                conn.commit()
                
                logger.info(f"✓ Removed {null_location_jobs} jobs with null locations")
        else:
            logger.info("\n✓ No jobs with null locations found")
            
    finally:
        if conn:
            cursor.close()
            DatabaseManager.return_connection(conn)


def generate_cleanup_report():
    """
    Generate a comprehensive cleanup report
    """
    logger.info("\n" + "=" * 60)
    logger.info("CLEANUP REPORT GENERATION")
    logger.info("=" * 60)
    
    invalid_locations = identify_invalid_locations()
    
    if not invalid_locations:
        logger.info("\n✓ Database is clean! No invalid locations found.")
        return
    
    # Group by category
    us_locations = []
    international_locations = []
    null_locations = []
    other_invalid = []
    
    for loc_id, city, state, reason in invalid_locations:
        location_str = f"{city}, {state}" if state else city
        
        if 'US location' in reason:
            us_locations.append(location_str)
        elif 'International location' in reason:
            international_locations.append(location_str)
        elif 'null' in reason.lower() or 'empty' in reason.lower():
            null_locations.append(location_str)
        else:
            other_invalid.append(location_str)
    
    logger.info(f"\nTotal invalid locations: {len(invalid_locations)}")
    logger.info(f"  - US locations: {len(us_locations)}")
    logger.info(f"  - International locations: {len(international_locations)}")
    logger.info(f"  - Null/Empty: {len(null_locations)}")
    logger.info(f"  - Other invalid: {len(other_invalid)}")
    
    # Show examples
    if us_locations:
        logger.info(f"\nUS Locations (showing up to 10):")
        for loc in us_locations[:10]:
            logger.info(f"  - {loc}")
    
    if international_locations:
        logger.info(f"\nInternational Locations (showing up to 10):")
        for loc in international_locations[:10]:
            logger.info(f"  - {loc}")
    
    # Count affected jobs
    invalid_location_ids = [loc[0] for loc in invalid_locations]
    affected_jobs = get_jobs_with_invalid_locations(invalid_location_ids)
    
    logger.info(f"\nTotal jobs that would be removed: {affected_jobs}")
    logger.info("=" * 60)


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description='Cleanup invalid locations from job database'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually perform the cleanup (default is dry-run)'
    )
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Only generate a report, no cleanup'
    )
    
    args = parser.parse_args()
    
    try:
        if args.report_only:
            generate_cleanup_report()
        else:
            # Cleanup invalid locations
            cleanup_invalid_locations(dry_run=not args.execute)
            
            # Also cleanup null locations
            cleanup_null_locations(dry_run=not args.execute)
        
        logger.info("\n✓ Script completed successfully!")
        
    except Exception as e:
        logger.error(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
