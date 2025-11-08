"""
Setup script to initialize the entire project
Run this after cloning the repository
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from .env.example"""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✓ .env file created. Please update it with your database credentials.")
    else:
        print("✓ .env file already exists.")

def create_data_directory():
    """Create data directory for storing CSV files"""
    data_dir = Path('data')
    if not data_dir.exists():
        data_dir.mkdir()
        print("✓ Data directory created.")

def main():
    print("="*60)
    print("JOB INTELLIGENCE PLATFORM - SETUP")
    print("="*60)
    
    print("\n1. Setting up environment...")
    create_env_file()
    
    print("\n2. Creating directories...")
    create_data_directory()
    
    print("\n3. Next steps:")
    print("   a. Update .env file with your PostgreSQL credentials")
    print("   b. Install dependencies: pip install -r requirements.txt")
    print("   c. Initialize database: python database/db_operations.py")
    print("   d. Test scrapers: python scrapers/test_jobspy.py")
    print("   e. Run dashboard: streamlit run dashboard/app.py")
    
    print("\n" + "="*60)
    print("Setup complete! Follow the next steps above.")
    print("="*60)

if __name__ == "__main__":
    main()