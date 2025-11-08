# Enhanced Dashboard Documentation

## Overview

The enhanced dashboard (`app_enhanced.py`) is a modern, card-based UI with dark mode support, designed to provide a premium user experience for job market analytics.

## Key Features

### 1. Dark/Light Mode Toggle
- **Location**: Sidebar
- **Persistence**: Uses Streamlit session state
- **Usage**: Click the theme toggle in the sidebar to switch between light and dark modes
- **Implementation**: `components/theme.py`

### 2. Modern Card-Based Layout
- **Glass-morphism cards**: Frosted glass effect with blur
- **Neumorphism buttons**: Soft UI design with shadows
- **Elevated cards**: Different elevation levels for hierarchy
- **Interactive cards**: Hover effects and smooth transitions

### 3. Component Library

#### Cards (`components/cards.py`)
- `metric_card()`: Display key metrics with icons
- `info_card()`: Information cards with title and content
- `stat_card()`: Cards with multiple statistics
- `company_card()`: Company profile cards
- `job_card()`: Job posting cards
- `skill_badge()`: Interactive skill badges
- `progress_card()`: Progress bars in cards
- `empty_state()`: Empty state placeholders
- `loading_skeleton()`: Loading placeholders

#### Filters (`components/filters.py`)
- `search_bar()`: Styled search input
- `chip_selector()`: Chip-based filters
- `filter_panel()`: Collapsible filter panel
- `sort_selector()`: Sort options
- `quick_filters()`: Quick filter buttons
- `range_slider()`: Range selection

#### Navigation (`components/navigation.py`)
- `sidebar_navigation()`: Icon-based navigation
- `theme_toggle()`: Dark/light mode toggle
- `breadcrumb()`: Breadcrumb navigation
- `tabs_navigation()`: Custom styled tabs
- `collapsible_section()`: Expandable sections
- `progress_indicator()`: Step progress

### 4. Enhanced Charts (`chart_utils.py`)
All charts support dark mode with automatic color adjustments:
- `create_bar_chart()`: Horizontal/vertical bar charts
- `create_line_chart()`: Line charts with gradient fills
- `create_pie_chart()`: Donut/pie charts
- `create_scatter_chart()`: Scatter plots
- `create_heatmap()`: Heatmaps
- `create_sparkline()`: Mini sparkline charts
- `create_gauge_chart()`: Gauge indicators
- `create_treemap()`: Hierarchical treemaps
- `create_funnel_chart()`: Funnel charts
- `create_timeline_chart()`: Timeline/Gantt charts
- `create_bubble_chart()`: Bubble charts
- `create_sunburst_chart()`: Sunburst charts

### 5. Styling System (`styles.py`)
- **CSS Variables**: Theme-aware custom properties
- **Glass-morphism**: Frosted glass effects
- **Neumorphism**: Soft UI elements
- **Animations**: Fade in, slide in, pulse, shimmer
- **Responsive**: Mobile-friendly grid system
- **Badges**: Colored badge/chip components

## Color Palettes

### Light Mode
- Background: `#fafbfc`, `#ffffff`
- Cards: `#ffffff` with subtle shadows
- Text: `#1e293b`, `#475569`
- Accent: `#667eea`, `#764ba2` (purple gradient)
- Success: `#10b981`
- Warning: `#f59e0b`

### Dark Mode
- Background: `#0e1117`, `#1a1d24`
- Cards: `#262730`, `#2e2e38` (elevated)
- Text: `#fafafa`, `#cbd5e1`
- Accent: `#8b9dff`, `#a29dff` (lighter purple)
- Success: `#34d399`
- Warning: `#fbbf24`

## Pages

### 1. Dashboard (Overview)
- **Hero Section**: Large gradient header with key metrics
- **Glass Metric Cards**: 4 main statistics (Jobs, Companies, Skills, Cities)
- **Top Skills Chart**: Bar chart with skill badges
- **Top Companies Chart**: Bar chart with company mini-cards
- **Geographic Distribution**: Donut chart
- **Experience Distribution**: Donut chart with progress bars

### 2. Skills Analysis
- **Search Bar**: Filter skills by name
- **View Modes**: Chart, Cards, or List view
- **Overall Demand Tab**: Most in-demand skills with category colors
- **By Location Tab**: Skills filtered by city
- **Co-occurrence Tab**: Skill pairs that appear together

### 3. Company Insights
- **Company Search**: Filter companies by name
- **Top Companies**: Bar chart and grid of company cards
- **By Location**: Companies filtered by city

### 4. Location Analysis
- **City Overview Cards**: Grid of city statistics
- **Job Distribution**: Bar chart by city
- **Market Share**: Donut chart
- **City Comparison**: Side-by-side comparison with progress cards

### 5. Job Explorer
- **Search & Filters**: Advanced job search (placeholder)
- **Sample Job Cards**: Demo job listing cards
- **Coming Soon**: Full job browsing capability

## Usage

### Running the Enhanced Dashboard

```bash
# Navigate to the project directory
cd /path/to/job-scraper

# Run the enhanced dashboard
streamlit run dashboard/app_enhanced.py

# Or run the original dashboard
streamlit run dashboard/app.py
```

### Accessing Features

1. **Toggle Dark Mode**: Click the theme toggle in the sidebar
2. **Navigate**: Use the sidebar navigation menu
3. **Search**: Use search bars to filter data
4. **Download**: Click download buttons to export CSV data
5. **Refresh**: Click "Refresh Data" to clear cache and reload

## Technical Implementation

### Theme Management
```python
from components.theme import init_theme, get_theme_colors, toggle_theme

# Initialize theme in session state
init_theme()

# Get current theme colors
colors = get_theme_colors()

# Toggle between light and dark
toggle_theme()
```

### Creating Cards
```python
from components.cards import metric_card, stat_card

# Display a metric card
metric_card("Total Jobs", "1,234", delta="+10%", icon="💼")

# Display a stat card
stat_card("Company Stats", {
    "Jobs": "100",
    "Locations": "5",
    "Active Since": "2020"
})
```

### Creating Charts
```python
from chart_utils import create_bar_chart

# Create a themed bar chart
fig = create_bar_chart(
    data=df,
    x='count',
    y='name',
    orientation='h',
    height=400
)
st.plotly_chart(fig, use_container_width=True)
```

## Accessibility

- **Color Contrast**: WCAG AA compliant in both themes
- **Keyboard Navigation**: Full keyboard support
- **Screen Readers**: ARIA labels (planned)
- **Responsive**: Works on desktop, tablet, and mobile

## Performance

- **Caching**: All data loading functions are cached (1 hour TTL)
- **Lazy Loading**: Components load on demand
- **Optimized Re-rendering**: Minimal state changes

## Future Enhancements

- [ ] Persist theme in browser localStorage
- [ ] Export data from any view
- [ ] Share specific views via URL
- [ ] Print-friendly layouts
- [ ] Keyboard shortcuts
- [ ] Multi-language support
- [ ] Advanced job filtering in Job Explorer
- [ ] Bookmark/save functionality
- [ ] Email alerts for new jobs
- [ ] Custom dashboard widgets

## Team

1. **Siddhartha Kabeer Upadhyay** - Backend & Database
2. **Adrika Srivastava** - Frontend Development
3. **Vibhor Saini** - Data Processing & NLP
4. **Nelly** - Quality Assurance & Documentation

## Support

For issues or questions, please contact the development team or create an issue in the repository.
