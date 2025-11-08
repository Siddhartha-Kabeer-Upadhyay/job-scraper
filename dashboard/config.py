"""
Configuration constants for the dashboard
"""

# Team Information
TEAM_MEMBERS = [
    {
        "name": "Siddhartha Kabeer Upadhyay",
        "role": "Backend & Database",
        "icon": "💻"
    },
    {
        "name": "Adrika Srivastava",
        "role": "Frontend Development",
        "icon": "🎨"
    },
    {
        "name": "Vibhor Saini",
        "role": "Data Processing & NLP",
        "icon": "📊"
    },
    {
        "name": "Nelly",
        "role": "Quality Assurance & Documentation",
        "icon": "✅"
    }
]

# Project Information
PROJECT_NAME = "Job Intelligence Platform"
PROJECT_DESCRIPTION = "Tech Job Market Analytics for India"

# Cache Settings
CACHE_TTL = 3600  # 1 hour in seconds

# Pagination Settings
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Chart Settings
DEFAULT_CHART_HEIGHT = 400
PLOTLY_CONFIG = {'displayModeBar': False}

# Theme Settings
THEME_OPTIONS = ['light', 'dark', 'auto']
DEFAULT_THEME = 'light'

# UI Configuration
UI_CONFIG = {
    'enable_animations': True,
    'enable_glassmorphism': True,
    'show_team_info': True,
    'compact_mode': False,
    'sidebar_default_state': 'expanded',
}
