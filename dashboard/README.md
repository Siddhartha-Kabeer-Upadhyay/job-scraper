# Running the Enhanced Dashboard

## Quick Start

### Option 1: Run Enhanced Dashboard (Recommended)
```bash
streamlit run dashboard/app_enhanced.py
```

### Option 2: Run Original Dashboard
```bash
streamlit run dashboard/app.py
```

## Features Comparison

### Enhanced Dashboard (`app_enhanced.py`)
✅ Dark/Light mode toggle  
✅ Modern card-based layout  
✅ Glass-morphism effects  
✅ Interactive charts  
✅ No tables as primary view  
✅ Responsive design  
✅ Advanced filtering  
✅ Smooth animations  

### Original Dashboard (`app.py`)
✅ Basic theme  
✅ Table-based views  
✅ Standard charts  
✅ Simple layout  

## What's New in Enhanced Dashboard

### 1. **Dark Mode Support** 🌙
- Toggle between light and dark themes in the sidebar
- Automatic color adjustments for all components
- Eye-friendly for extended use

### 2. **Modern UI Components** 🎨
- **Glass-morphism cards**: Frosted glass effect with transparency
- **Neumorphism buttons**: Soft, tactile UI elements
- **Interactive badges**: Colored skill and category tags
- **Progress cards**: Visual progress indicators
- **Empty states**: Friendly placeholders when no data

### 3. **Enhanced Navigation** 🧭
- Icon-based sidebar navigation
- Breadcrumb trails
- Quick action buttons
- Collapsible sections

### 4. **Better Data Visualization** 📊
- All charts adapt to theme (light/dark)
- Gradient fills and modern styling
- Interactive tooltips
- Sparklines for quick insights
- Multiple chart types (bar, pie, scatter, bubble, etc.)

### 5. **Card-Based Layout** 📇
- No tables as primary view
- Information presented in scannable cards
- Grid layouts with proper spacing
- Hover effects and animations

## Pages Overview

### 📊 Dashboard (Home)
- Hero section with gradient background
- Key metrics in glass cards
- Top skills and companies
- Geographic and experience distribution

### 💡 Skills Analysis
- Search and filter skills
- View as charts, cards, or list
- Skills by location
- Skill co-occurrence analysis

### 🏢 Company Insights
- Top hiring companies
- Company profile cards
- Filter by location
- Company statistics

### 🌍 Location Analysis
- City overview cards
- Job distribution charts
- Market share analysis
- Side-by-side city comparison

### 🔍 Job Explorer
- Advanced job search (placeholder)
- Job listing cards
- Filter and sort options
- Coming soon: Full job browsing

## Theme Colors

### Light Mode
- Clean, professional appearance
- Purple accent colors (#667eea)
- High contrast for readability

### Dark Mode
- Modern, eye-friendly colors
- Lighter purple accents (#8b9dff)
- Reduced eye strain

## Requirements

All dependencies are already in `requirements.txt`:
- streamlit >= 1.29.0
- plotly >= 5.18.0
- pandas >= 2.1.0
- psycopg2-binary (for database)

## Troubleshooting

### Dashboard doesn't load
- Ensure database is set up and populated
- Check `.env` file for correct credentials
- Verify all dependencies are installed

### Charts not showing
- Clear cache: Click "Refresh Data" button
- Check if data exists in database
- Look for error messages in console

### Theme toggle not working
- Theme persists in session state
- Refresh the page to see changes
- Check browser console for errors

## Development

### File Structure
```
dashboard/
├── app.py                  # Original dashboard
├── app_enhanced.py         # Enhanced dashboard ⭐
├── chart_utils.py          # Chart utilities
├── styles.py               # CSS and styling
├── ENHANCED_DASHBOARD.md   # Full documentation
├── components/
│   ├── theme.py           # Theme management
│   ├── cards.py           # Card components
│   ├── filters.py         # Filter components
│   └── navigation.py      # Navigation components
└── pages/
    └── __init__.py
```

### Adding New Features

1. **Add a new card type**: Edit `components/cards.py`
2. **Add new filters**: Edit `components/filters.py`
3. **Add new charts**: Edit `chart_utils.py`
4. **Modify theme colors**: Edit `components/theme.py`
5. **Add CSS styles**: Edit `styles.py`

## Team

1. **Siddhartha Kabeer Upadhyay** - Backend & Database
2. **Adrika Srivastava** - Frontend Development
3. **Vibhor Saini** - Data Processing & NLP
4. **Nelly** - Quality Assurance & Documentation

## Support

For detailed documentation, see `ENHANCED_DASHBOARD.md`

For issues, contact the development team.
