"""
Location validation utility for ensuring only Indian cities are stored in the database
"""

import logging
import re
from typing import Optional, Tuple

# Import pandas for null checking (if available)
try:
    import pandas as pd
except ImportError:
    # Fallback implementation
    class pd:
        @staticmethod
        def isna(val):
            return val is None or (isinstance(val, float) and val != val) or str(val).lower() == 'nan'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Comprehensive list of approved Indian cities and their aliases
APPROVED_INDIAN_CITIES = {
    'Bengaluru', 'Bangalore', 'Mumbai', 'Pune', 'Delhi', 'New Delhi',
    'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad', 'Gurugram', 'Gurgaon',
    'Noida', 'Greater Noida', 'Kochi', 'Cochin', 'Thiruvananthapuram',
    'Trivandrum', 'Chandigarh', 'Jaipur', 'Indore', 'Lucknow', 'Bhopal',
    'Nagpur', 'Visakhapatnam', 'Vizag', 'Surat', 'Coimbatore', 'Vadodara',
    'Mysore', 'Mysuru', 'Mangalore', 'Mangaluru', 'Patna', 'Ranchi',
    'Bhubaneswar', 'Guwahati', 'Dehradun', 'Nashik', 'Rajkot', 'Kanpur',
    'Ludhiana', 'Agra', 'Madurai', 'Varanasi', 'Meerut', 'Faridabad',
    'Ghaziabad', 'Amritsar', 'Allahabad', 'Prayagraj', 'Vijayawada',
    'Jabalpur', 'Jodhpur', 'Raipur', 'Kota', 'Gwalior', 'Aurangabad',
    'Thiruvananthapuram', 'Tiruchirappalli', 'Trichy', 'Salem', 'Udaipur',
    'Jammu', 'Srinagar', 'Tirupati', 'Erode', 'Bhilai', 'Warangal',
    'Bhiwandi', 'Guntur', 'Nellore', 'Belgaum', 'Belagavi', 'Durgapur',
    'Kolhapur', 'Ajmer', 'Bikaner', 'Jalandhar', 'Siliguri', 'Thrissur',
    'Tirunelveli', 'Saharanpur', 'Moradabad', 'Gandhinagar', 'Shimla',
    'Tiruppur', 'Panipat', 'Rourkela', 'Rajahmundry', 'Bokaro', 'Malappuram'
}

# Normalize city names for consistent storage
CITY_NAME_MAPPING = {
    'bangalore': 'Bengaluru',
    'bengaluru': 'Bengaluru',
    'bombay': 'Mumbai',
    'mumbai': 'Mumbai',
    'pune': 'Pune',
    'delhi': 'Delhi',
    'new delhi': 'Delhi',
    'hyderabad': 'Hyderabad',
    'chennai': 'Chennai',
    'madras': 'Chennai',
    'kolkata': 'Kolkata',
    'calcutta': 'Kolkata',
    'gurgaon': 'Gurugram',
    'gurugram': 'Gurugram',
    'noida': 'Noida',
    'greater noida': 'Greater Noida',
    'cochin': 'Kochi',
    'kochi': 'Kochi',
    'trivandrum': 'Thiruvananthapuram',
    'thiruvananthapuram': 'Thiruvananthapuram',
    'vizag': 'Visakhapatnam',
    'visakhapatnam': 'Visakhapatnam',
    'mysore': 'Mysuru',
    'mysuru': 'Mysuru',
    'mangalore': 'Mangaluru',
    'mangaluru': 'Mangaluru',
    'trichy': 'Tiruchirappalli',
    'tiruchirappalli': 'Tiruchirappalli',
    'belagavi': 'Belgaum',
    'belgaum': 'Belgaum',
    'allahabad': 'Prayagraj',
    'prayagraj': 'Prayagraj',
}

# List of known US cities/states to reject
US_LOCATIONS = {
    'Cincinnati', 'OH', 'Ohio', 'West Chester', 'New York', 'NY',
    'California', 'CA', 'San Francisco', 'Los Angeles', 'Seattle',
    'Washington', 'WA', 'Austin', 'Texas', 'TX', 'Boston', 'MA',
    'Massachusetts', 'Chicago', 'Illinois', 'IL', 'Denver', 'Colorado',
    'CO', 'Portland', 'Oregon', 'OR', 'Miami', 'Florida', 'FL',
    'Atlanta', 'Georgia', 'GA', 'Dallas', 'Philadelphia', 'PA',
    'Pennsylvania', 'San Diego', 'Phoenix', 'Arizona', 'AZ',
    'Las Vegas', 'Nevada', 'NV', 'Detroit', 'Michigan', 'MI',
    'Minneapolis', 'Minnesota', 'MN', 'Tampa', 'Charlotte',
    'North Carolina', 'NC', 'Indianapolis', 'Indiana', 'IN',
    'Columbus', 'Kansas City', 'Missouri', 'MO', 'Nashville',
    'Tennessee', 'TN', 'Milwaukee', 'Wisconsin', 'WI', 'Raleigh',
    'Virginia', 'VA', 'Richmond', 'Salt Lake City', 'Utah', 'UT',
    'USA', 'United States', 'US', 'America'
}

# Other international cities/countries to reject
INTERNATIONAL_LOCATIONS = {
    'London', 'UK', 'United Kingdom', 'England', 'Manchester', 'Birmingham',
    'Toronto', 'Canada', 'Vancouver', 'Montreal', 'Singapore', 'Dubai',
    'UAE', 'Sydney', 'Australia', 'Melbourne', 'Berlin', 'Germany',
    'Munich', 'Paris', 'France', 'Amsterdam', 'Netherlands', 'Tokyo',
    'Japan', 'Beijing', 'China', 'Shanghai', 'Hong Kong', 'Seoul',
    'South Korea', 'Bangkok', 'Thailand', 'Manila', 'Philippines',
    'Jakarta', 'Indonesia', 'Kuala Lumpur', 'Malaysia', 'Remote',
    'Worldwide', 'Global', 'International'
}


def normalize_city_name(city: str) -> str:
    """
    Normalize city name to standard format
    
    Args:
        city: Raw city name
        
    Returns:
        Normalized city name
    """
    if not city:
        return None
    
    city_lower = city.strip().lower()
    return CITY_NAME_MAPPING.get(city_lower, city.strip())


def is_indian_city(location: str) -> bool:
    """
    Check if location is a valid Indian city
    
    Args:
        location: Location string (may contain city, state, country)
        
    Returns:
        True if location is in India, False otherwise
    """
    if not location or pd.isna(location) or location == 'nan' or location == '':
        return False
    
    location_str = str(location).strip()
    location_lower = location_str.lower()
    
    # First check if it explicitly mentions India - if yes, it's likely valid
    if 'india' in location_lower:
        # But still reject if it's clearly a US/International location
        us_keywords = ['united states', 'usa', 'u.s.a', 'america']
        for keyword in us_keywords:
            if keyword in location_lower:
                logger.debug(f"Rejected US location: {location}")
                return False
        # It's in India, continue to validate
    
    # Check for US locations (use word boundaries to avoid false positives)
    for us_loc in US_LOCATIONS:
        us_loc_lower = us_loc.lower()
        # Use word boundaries for short state codes to avoid matching inside words
        if len(us_loc) <= 2:
            # For state codes, check if it appears as a separate word
            pattern = r'\b' + re.escape(us_loc_lower) + r'\b'
            if re.search(pattern, location_lower):
                # Additional check: make sure it's not part of an Indian location
                if 'india' not in location_lower:
                    logger.debug(f"Rejected US location: {location}")
                    return False
        else:
            # For longer names, check if present
            if us_loc_lower in location_lower and 'india' not in location_lower:
                logger.debug(f"Rejected US location: {location}")
                return False
    
    # Check for other international locations
    for intl_loc in INTERNATIONAL_LOCATIONS:
        intl_loc_lower = intl_loc.lower()
        if intl_loc_lower in location_lower:
            # Make sure it's not a false positive (e.g., "Remote" in other words)
            if len(intl_loc) <= 4:
                pattern = r'\b' + re.escape(intl_loc_lower) + r'\b'
                if re.search(pattern, location_lower):
                    logger.debug(f"Rejected international location: {location}")
                    return False
            else:
                logger.debug(f"Rejected international location: {location}")
                return False
    
    # Extract city name (usually first part before comma)
    city_parts = location_str.split(',')
    city = city_parts[0].strip()
    
    # Normalize and check against approved cities
    normalized_city = normalize_city_name(city)
    
    # Check if normalized city is in approved list
    if normalized_city in APPROVED_INDIAN_CITIES:
        return True
    
    # Check if original city (case-insensitive) is in approved list
    for approved_city in APPROVED_INDIAN_CITIES:
        if approved_city.lower() == city.lower():
            return True
    
    # Check if location explicitly mentions India
    if 'india' in location_lower:
        # If it mentions India but we don't recognize the city, still accept it
        # but log for review
        logger.debug(f"Accepted unrecognized Indian city: {location}")
        return True
    
    # Default: reject unknown locations
    logger.debug(f"Rejected unknown location: {location}")
    return False


def extract_and_validate_city(location: str) -> Tuple[Optional[str], Optional[str], bool]:
    """
    Extract city and state from location string and validate
    
    Args:
        location: Location string
        
    Returns:
        Tuple of (city, state, is_valid)
    """
    if not location or pd.isna(location):
        return None, None, False
    
    location_str = str(location).strip()
    
    # Check if location is valid Indian city
    if not is_indian_city(location_str):
        return None, None, False
    
    # Extract city and state
    parts = location_str.split(',')
    
    city = parts[0].strip() if len(parts) > 0 else None
    state = parts[1].strip() if len(parts) > 1 else None
    
    # Normalize city name
    if city:
        city = normalize_city_name(city)
    
    return city, state, True


def validate_location_data(location: str) -> dict:
    """
    Comprehensive location validation with detailed results
    
    Args:
        location: Location string to validate
        
    Returns:
        Dictionary with validation results
    """
    result = {
        'original_location': location,
        'is_valid': False,
        'city': None,
        'state': None,
        'normalized_city': None,
        'rejection_reason': None
    }
    
    if not location or pd.isna(location) or str(location).strip() == '':
        result['rejection_reason'] = 'Empty or null location'
        return result
    
    location_str = str(location).strip()
    location_lower = location_str.lower()
    
    # First check if it explicitly mentions India
    has_india = 'india' in location_lower
    
    # Check for US locations (with word boundary consideration)
    for us_loc in US_LOCATIONS:
        us_loc_lower = us_loc.lower()
        if len(us_loc) <= 2:
            # For state codes, check word boundaries
            pattern = r'\b' + re.escape(us_loc_lower) + r'\b'
            if re.search(pattern, location_lower) and not has_india:
                result['rejection_reason'] = f'US location detected: {us_loc}'
                return result
        else:
            if us_loc_lower in location_lower and not has_india:
                result['rejection_reason'] = f'US location detected: {us_loc}'
                return result
    
    # Check for international locations
    for intl_loc in INTERNATIONAL_LOCATIONS:
        intl_loc_lower = intl_loc.lower()
        if len(intl_loc) <= 4:
            pattern = r'\b' + re.escape(intl_loc_lower) + r'\b'
            if re.search(pattern, location_lower):
                result['rejection_reason'] = f'International location detected: {intl_loc}'
                return result
        else:
            if intl_loc_lower in location_lower:
                result['rejection_reason'] = f'International location detected: {intl_loc}'
                return result
    
    # Extract city and state
    city, state, is_valid = extract_and_validate_city(location_str)
    
    if is_valid and city:
        result['is_valid'] = True
        result['city'] = city
        result['state'] = state
        result['normalized_city'] = normalize_city_name(city)
    else:
        result['rejection_reason'] = 'Location not in approved Indian cities list'
    
    return result


def get_location_statistics(locations: list) -> dict:
    """
    Get statistics about location data quality
    
    Args:
        locations: List of location strings
        
    Returns:
        Dictionary with statistics
    """
    stats = {
        'total_locations': len(locations),
        'valid_locations': 0,
        'invalid_locations': 0,
        'null_locations': 0,
        'us_locations': 0,
        'international_locations': 0,
        'unrecognized_locations': 0,
        'rejection_reasons': {}
    }
    
    for location in locations:
        validation = validate_location_data(location)
        
        if validation['is_valid']:
            stats['valid_locations'] += 1
        else:
            stats['invalid_locations'] += 1
            
            reason = validation['rejection_reason']
            if reason:
                if 'null' in reason.lower() or 'empty' in reason.lower():
                    stats['null_locations'] += 1
                elif 'US location' in reason:
                    stats['us_locations'] += 1
                elif 'International location' in reason:
                    stats['international_locations'] += 1
                else:
                    stats['unrecognized_locations'] += 1
                
                # Count rejection reasons
                stats['rejection_reasons'][reason] = stats['rejection_reasons'].get(reason, 0) + 1
    
    # Calculate percentages
    if stats['total_locations'] > 0:
        stats['valid_percentage'] = round(stats['valid_locations'] / stats['total_locations'] * 100, 2)
        stats['invalid_percentage'] = round(stats['invalid_locations'] / stats['total_locations'] * 100, 2)
    
    return stats


def main():
    """Test location validation"""
    test_locations = [
        'Bengaluru, Karnataka, India',
        'Mumbai, Maharashtra',
        'Cincinnati, OH, United States',
        'West Chester, OH',
        'Pune, India',
        'London, UK',
        'Hyderabad',
        None,
        '',
        'Remote',
        'Delhi, India'
    ]
    
    print("=" * 60)
    print("LOCATION VALIDATION TEST")
    print("=" * 60)
    
    for location in test_locations:
        result = validate_location_data(location)
        print(f"\nLocation: {location}")
        print(f"Valid: {result['is_valid']}")
        if result['is_valid']:
            print(f"City: {result['city']}")
            print(f"State: {result['state']}")
        else:
            print(f"Reason: {result['rejection_reason']}")
    
    print("\n" + "=" * 60)
    print("LOCATION STATISTICS")
    print("=" * 60)
    
    stats = get_location_statistics(test_locations)
    print(f"Total: {stats['total_locations']}")
    print(f"Valid: {stats['valid_locations']} ({stats.get('valid_percentage', 0)}%)")
    print(f"Invalid: {stats['invalid_locations']} ({stats.get('invalid_percentage', 0)}%)")
    print(f"  - Null/Empty: {stats['null_locations']}")
    print(f"  - US: {stats['us_locations']}")
    print(f"  - International: {stats['international_locations']}")
    print(f"  - Unrecognized: {stats['unrecognized_locations']}")


if __name__ == "__main__":
    main()
