"""
Quick status check for the project
"""
from database.db_operations import JobDatabase

db = JobDatabase()
stats = db.get_database_stats()

print("\n" + "="*50)
print("PROJECT STATUS")
print("="*50)
print(f"Jobs in DB: {stats['total_jobs']}")
print(f"Companies: {stats['total_companies']}")
print(f"Skills: {stats['total_skills']}")
print("\nJobs by City:")
for city, count in stats['jobs_by_city']:
    if count > 0:
        print(f"  {city}: {count}")
print("="*50 + "\n")