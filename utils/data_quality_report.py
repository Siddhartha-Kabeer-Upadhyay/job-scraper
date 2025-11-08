"""
Generate data quality report for scraped jobs
Shows completeness of each field
"""

import pandas as pd
import sys
from pathlib import Path

def generate_quality_report(csv_file: str):
    """Generate comprehensive data quality report"""
    
    print(f"\n{'='*60}")
    print(f"DATA QUALITY REPORT: {Path(csv_file).name}")
    print(f"{'='*60}\n")
    
    df = pd.read_csv(csv_file)
    total_jobs = len(df)
    
    print(f"Total Jobs: {total_jobs}\n")
    
    # Field completeness
    print(f"{'Field':<25} {'Present':<10} {'Missing':<10} {'%Complete':<12}")
    print("-" * 60)
    
    field_stats = []
    
    for col in df.columns:
        present = df[col].notna().sum()
        missing = df[col].isna().sum()
        percentage = round(present / total_jobs * 100, 1)
        
        field_stats.append({
            'field': col,
            'present': present,
            'missing': missing,
            'percentage': percentage
        })
        
        print(f"{col:<25} {present:<10} {missing:<10} {percentage:<12}%")
    
    # Sort by completeness
    field_stats.sort(key=lambda x: x['percentage'], reverse=True)
    
    print(f"\n{'='*60}")
    print("FIELD QUALITY TIERS")
    print(f"{'='*60}\n")
    
    excellent = [f['field'] for f in field_stats if f['percentage'] >= 90]
    good = [f['field'] for f in field_stats if 70 <= f['percentage'] < 90]
    fair = [f['field'] for f in field_stats if 50 <= f['percentage'] < 70]
    poor = [f['field'] for f in field_stats if f['percentage'] < 50]
    
    print(f"✓ EXCELLENT (≥90%): {len(excellent)} fields")
    for field in excellent:
        print(f"  - {field}")
    
    print(f"\n○ GOOD (70-89%): {len(good)} fields")
    for field in good:
        print(f"  - {field}")
    
    print(f"\n△ FAIR (50-69%): {len(fair)} fields")
    for field in fair:
        print(f"  - {field}")
    
    print(f"\n✗ POOR (<50%): {len(poor)} fields")
    for field in poor:
        print(f"  - {field}")
    
    print(f"\n{'='*60}")
    print("RECOMMENDATIONS")
    print(f"{'='*60}\n")
    
    if poor:
        print(f"⚠ Consider removing or marking optional these fields:")
        for field in poor:
            print(f"  - {field}")
    
    # Check critical fields
    critical_fields = ['title', 'company', 'location', 'description', 'job_url']
    critical_missing = []
    
    for field in critical_fields:
        if field in df.columns:
            if (df[field].isna().sum() / total_jobs * 100) > 10:
                critical_missing.append(field)
    
    if critical_missing:
        print(f"\n⚠ WARNING: Critical fields with >10% missing:")
        for field in critical_missing:
            print(f"  - {field}")
    else:
        print(f"\n✓ All critical fields have good data quality")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python data_quality_report.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not Path(csv_file).exists():
        print(f"Error: File not found: {csv_file}")
        sys.exit(1)
    
    generate_quality_report(csv_file)