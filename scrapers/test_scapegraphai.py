"""
Test script for ScrapeGraphAI
Alternative if JobSpy doesn't work
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_scrapegraphai():
    """Test ScrapeGraphAI capabilities"""
    logger.info("Testing ScrapeGraphAI...")
    
    try:
        # Note: ScrapeGraphAI requires API key and different setup
        # This is a placeholder for testing
        logger.warning("ScrapeGraphAI requires API keys and additional setup")
        logger.info("Visit: https://scrapegraphai.com for setup instructions")
        return False, "Not configured"
        
    except ImportError:
        logger.error("ScrapeGraphAI not installed")
        logger.info("Install with: pip install scrapegraphai")
        return False, "Not installed"
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False, str(e)

if __name__ == "__main__":
    test_scrapegraphai()