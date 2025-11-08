"""
Redesigned Job Intelligence Platform Dashboard
Modern, professional UI/UX with comprehensive features
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings

# Import analytics and database
from analytics.insights import JobMarketAnalytics
from database.db_operations import JobDatabase

# Import theme system
from theme import (
    get_theme, create_design_tokens, get_gradient,
    LIGHT_THEME, DARK_THEME, TYPOGRAPHY, SPACING
)

# Import configuration
from config import TEAM_MEMBERS, PLOTLY_CONFIG, CACHE_TTL, UI_CONFIG

# Suppress warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='The keyword arguments have been deprecated')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Job Intelligence Platform | Modern Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state=UI_CONFIG['sidebar_default_state']
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'light'

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Overview'

# ============================================================================
# THEME FUNCTIONS
# ============================================================================

def toggle_theme():
    """Toggle between light and dark theme"""
    st.session_state.theme_mode = 'dark' if st.session_state.theme_mode == 'light' else 'light'
    st.rerun()

def get_current_theme():
    """Get current theme colors"""
    return get_theme(st.session_state.theme_mode)

def apply_theme_styles():
    """Apply theme-specific CSS styles"""
    theme = get_current_theme()
    tokens = create_design_tokens(st.session_state.theme_mode)
    
    # Load external CSS
    css_path = Path(__file__).parent / "styles_v2.css"
    try:
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
        else:
            css_content = ""
    except Exception as e:
        st.warning(f"Could not load CSS file: {e}")
        css_content = ""
    
    # Generate CSS variables
    css_vars = ":root {\n"
    for key, value in tokens.items():
        css_vars += f"    {key}: {value};\n"
    css_vars += "}\n\n"
    
    # Add theme data attribute
    theme_attr = f'<div data-theme="{st.session_state.theme_mode}"></div>'
    
    # Combine all styles
    st.markdown(f"<style>{css_vars}{css_content}</style>{theme_attr}", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_resource
def get_analytics():
    """Initialize analytics instance"""
    return JobMarketAnalytics()

@st.cache_resource
def get_database():
    """Initialize database instance"""
    return JobDatabase()

@st.cache_data(ttl=CACHE_TTL)
def load_market_overview():
    analytics = get_analytics()
    return analytics.generate_market_overview()

@st.cache_data(ttl=CACHE_TTL)
def load_data_quality():
    """Load data quality statistics"""
    db = get_database()
    return db.get_data_quality_stats()

@st.cache_data(ttl=CACHE_TTL)
def load_top_skills(limit=20):
    analytics = get_analytics()
    return analytics.get_top_skills(limit)

@st.cache_data(ttl=CACHE_TTL)
def load_top_companies(limit=20):
    analytics = get_analytics()
    return analytics.get_top_hiring_companies(limit)

@st.cache_data(ttl=CACHE_TTL)
def load_jobs_by_city():
    analytics = get_analytics()
    return analytics.get_jobs_by_city()

@st.cache_data(ttl=CACHE_TTL)
def load_skill_cooccurrence(min_count=10, limit=50):
    analytics = get_analytics()
    return analytics.get_skill_cooccurrence(min_count, limit)

@st.cache_data(ttl=CACHE_TTL)
def load_experience_distribution():
    analytics = get_analytics()
    return analytics.get_experience_distribution()

@st.cache_data(ttl=CACHE_TTL)
def load_top_skills_by_city(city, limit=20):
    analytics = get_analytics()
    return analytics.get_top_skills_by_city(city, limit)

@st.cache_data(ttl=CACHE_TTL)
def load_companies_by_city(city, limit=20):
    analytics = get_analytics()
    return analytics.get_companies_by_city(city, limit)

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_header():
    """Render modern dashboard header"""
    theme = get_current_theme()
    gradient = get_gradient(theme, ['primary', 'secondary'], '135deg')
    
    header_html = f"""
    <div class="hero-section" style="background: {gradient};">
        <div class="hero-content">
            <h1 class="hero-title">🚀 Job Intelligence Platform</h1>
            <p class="hero-subtitle">Tech Job Market Analytics for India - Powered by Modern Data Science</p>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_metric_card(label, value, icon="📊", delta=None, delta_color="success"):
    """Render a modern metric card"""
    theme = get_current_theme()
    
    delta_html = ""
    if delta:
        delta_class = "positive" if delta_color == "success" else "negative"
        delta_html = f'<div class="metric-delta {delta_class}">{delta}</div>'
    
    card_html = f"""
    <div class="metric-card">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_sidebar():
    """Render modern sidebar with navigation"""
    with st.sidebar:
        # Theme toggle button
        theme_icon = "🌙" if st.session_state.theme_mode == 'light' else "☀️"
        theme_label = "Dark Mode" if st.session_state.theme_mode == 'light' else "Light Mode"
        
        if st.button(f"{theme_icon} {theme_label}", use_container_width=True):
            toggle_theme()
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📊 Navigation")
        
        pages = [
            ("🏠 Overview", "Overview"),
            ("🎯 Skills Analysis", "Skills"),
            ("🏢 Company Insights", "Companies"),
            ("📍 Location Analysis", "Locations"),
            ("📈 Experience Trends", "Experience"),
            ("💰 Salary Analysis", "Salary"),
        ]
        
        for icon_label, page_key in pages:
            if st.button(icon_label, use_container_width=True, 
                        type="primary" if st.session_state.current_page == page_key else "secondary"):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        # Data refresh
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.success("Data refreshed!")
            st.rerun()
        
        st.markdown("---")
        
        # Project info
        st.markdown("### 📋 Project Info")
        st.markdown("**DBMS Course Project**")
        st.markdown(f"**Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        if UI_CONFIG['show_team_info']:
            st.markdown("---")
            st.markdown("### 👥 Team")
            for member in TEAM_MEMBERS:
                st.markdown(f"{member['icon']} **{member['name']}**  \n*{member['role']}*")

def create_modern_chart(data, chart_type, **kwargs):
    """Create a modern styled chart"""
    theme = get_current_theme()
    
    # Common layout settings
    layout_args = {
        'template': 'plotly_white' if st.session_state.theme_mode == 'light' else 'plotly_dark',
        'font': {'family': TYPOGRAPHY['font_family']['sans']},
        'paper_bgcolor': theme['background']['paper'],
        'plot_bgcolor': theme['background']['paper'],
        'margin': dict(l=20, r=20, t=40, b=20),
    }
    
    if chart_type == 'bar':
        fig = px.bar(data, **kwargs)
    elif chart_type == 'pie':
        fig = px.pie(data, **kwargs)
    elif chart_type == 'line':
        fig = px.line(data, **kwargs)
    elif chart_type == 'scatter':
        fig = px.scatter(data, **kwargs)
    else:
        fig = px.bar(data, **kwargs)
    
    fig.update_layout(**layout_args)
    return fig

# ============================================================================
# PAGE VIEWS
# ============================================================================

def show_overview():
    """Market Overview Page - Completely Redesigned"""
    st.markdown("## 📊 Market Overview")
    st.caption("High-level statistics of the tech job market in India")
    
    try:
        with st.spinner("Loading market data..."):
            overview = load_market_overview()
            quality_stats = load_data_quality()
        
        # Data quality warning
        if quality_stats['location_coverage'] < 100:
            st.warning(
                f"⚠️ **Data Quality Notice:** {quality_stats['location_coverage']:.1f}% of jobs have valid location data. "
                f"Jobs without valid Indian locations are excluded."
            )
        
        st.markdown("---")
        
        # Key metrics in cards
        st.markdown("### 🎯 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_metric_card("Total Jobs", f"{overview['total_jobs']:,}", "💼")
        
        with col2:
            render_metric_card("Companies Hiring", f"{overview['total_companies']:,}", "🏢")
        
        with col3:
            render_metric_card("Unique Skills", f"{overview['total_skills']:,}", "🎯")
        
        with col4:
            render_metric_card("Cities Covered", f"{overview['total_cities']:,}", "📍")
        
        st.markdown("---")
        
        # Data coverage metrics
        st.markdown("### 📈 Data Coverage")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_metric_card("Location Data", f"{quality_stats['location_coverage']:.1f}%", "📍")
        
        with col2:
            render_metric_card("Salary Data", f"{quality_stats['salary_coverage']:.1f}%", "💰")
        
        with col3:
            render_metric_card("Description Data", f"{quality_stats['description_coverage']:.1f}%", "📝")
        
        st.markdown("---")
        
        # Charts section
        st.markdown("### 📊 Market Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Top 10 In-Demand Skills")
            top_skills_df = pd.DataFrame(overview['top_10_skills'])
            
            if not top_skills_df.empty:
                fig = create_modern_chart(
                    top_skills_df,
                    'bar',
                    x='job_count',
                    y='skill_name',
                    orientation='h',
                    color='skill_category',
                    labels={'job_count': 'Job Count', 'skill_name': 'Skill'}
                )
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("No skills data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("#### 🏢 Top 10 Hiring Companies")
            top_companies_df = pd.DataFrame(overview['top_10_companies'])
            
            if not top_companies_df.empty:
                fig = create_modern_chart(
                    top_companies_df,
                    'bar',
                    x='job_count',
                    y='company_name',
                    orientation='h',
                    labels={'job_count': 'Job Count', 'company_name': 'Company'}
                )
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("No company data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("#### 📍 Job Distribution by City")
            jobs_by_city_df = pd.DataFrame(overview['jobs_by_city'])
            jobs_by_city_df = jobs_by_city_df[
                (jobs_by_city_df['city'].notna()) & 
                (jobs_by_city_df['city'] != '') & 
                (jobs_by_city_df['job_count'] > 0)
            ]
            
            if not jobs_by_city_df.empty:
                fig = create_modern_chart(
                    jobs_by_city_df,
                    'pie',
                    values='job_count',
                    names='city',
                    hole=0.4
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("No location data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("#### 📈 Experience Level Distribution")
            exp_dist_df = pd.DataFrame(overview['experience_distribution'])
            
            if not exp_dist_df.empty:
                fig = create_modern_chart(
                    exp_dist_df,
                    'pie',
                    values='job_count',
                    names='experience_level',
                    hole=0.4
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("No experience data available")
            st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.info("Ensure database is populated with job data.")

def show_skills_analysis():
    """Skills Analysis Page - Redesigned"""
    st.markdown("## 🎯 Skills Analysis")
    st.caption("Deep dive into skill demand across the job market")
    
    tab1, tab2, tab3 = st.tabs(["📊 Overall Demand", "📍 By Location", "🔗 Co-occurrence"])
    
    with tab1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Most In-Demand Skills")
        
        num_skills = st.slider("Number of skills to display", 10, 50, 20, 5)
        
        try:
            with st.spinner("Loading skills data..."):
                skills_df = load_top_skills(num_skills)
            
            if not skills_df.empty:
                fig = create_modern_chart(
                    skills_df,
                    'bar',
                    x='job_count',
                    y='skill_name',
                    orientation='h',
                    color='skill_category',
                    labels={'job_count': 'Job Count', 'skill_name': 'Skill'},
                    hover_data=['percentage']
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                st.markdown("### 📋 Detailed Data")
                st.dataframe(skills_df, use_container_width=True, hide_index=True)
                
                csv = skills_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"top_skills_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No skills data available")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### 📍 Skills by City")
        
        try:
            cities_df = load_jobs_by_city()
            cities_df_filtered = cities_df[
                (cities_df['city'].notna()) & 
                (cities_df['city'] != '') & 
                (cities_df['job_count'] > 0)
            ]
            cities = cities_df_filtered['city'].tolist()
            
            if cities:
                selected_city = st.selectbox("Select City", cities)
                num_skills_city = st.slider("Number of skills", 10, 30, 15, 5, key="city_skills")
                
                with st.spinner(f"Loading skills data for {selected_city}..."):
                    city_skills_df = load_top_skills_by_city(selected_city, num_skills_city)
                
                if not city_skills_df.empty:
                    fig = create_modern_chart(
                        city_skills_df,
                        'bar',
                        x='job_count',
                        y='skill_name',
                        orientation='h',
                        labels={'job_count': 'Job Count', 'skill_name': 'Skill'}
                    )
                    fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                    
                    st.dataframe(city_skills_df, use_container_width=True, hide_index=True)
                else:
                    st.warning(f"No skills data for {selected_city}")
            else:
                st.warning("No city data available")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### 🔗 Skill Co-occurrence")
        st.caption("Discover which skills are frequently requested together")
        
        col1, col2 = st.columns(2)
        with col1:
            min_count = st.number_input("Minimum occurrences", 5, 50, 10, 5)
        with col2:
            limit = st.number_input("Number of pairs", 10, 100, 30, 10)
        
        try:
            with st.spinner("Analyzing skill combinations..."):
                cooccurrence_df = load_skill_cooccurrence(min_count, limit)
            
            if not cooccurrence_df.empty:
                cooccurrence_df['skill_pair'] = cooccurrence_df['skill_1'] + ' + ' + cooccurrence_df['skill_2']
                
                fig = create_modern_chart(
                    cooccurrence_df,
                    'bar',
                    x='co_occurrence_count',
                    y='skill_pair',
                    orientation='h',
                    labels={'co_occurrence_count': 'Job Count', 'skill_pair': 'Skill Pair'}
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                st.dataframe(
                    cooccurrence_df[['skill_1', 'skill_2', 'co_occurrence_count']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No co-occurrence data with current filters")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_company_insights():
    """Company Insights Page - Redesigned"""
    st.markdown("## 🏢 Company Insights")
    st.caption("Explore which companies are hiring and where")
    
    tab1, tab2 = st.tabs(["🏆 Top Companies", "📍 By Location"])
    
    with tab1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### 🏆 Top Hiring Companies")
        
        num_companies = st.slider("Number of companies", 10, 50, 20, 5)
        
        try:
            with st.spinner("Loading company data..."):
                companies_df = load_top_companies(num_companies)
            
            if not companies_df.empty:
                fig = create_modern_chart(
                    companies_df,
                    'bar',
                    x='job_count',
                    y='company_name',
                    orientation='h',
                    color='cities_hiring_in',
                    labels={'job_count': 'Job Count', 'company_name': 'Company', 'cities_hiring_in': 'Cities'}
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                st.markdown("### 📋 Detailed Data")
                st.dataframe(companies_df, use_container_width=True, hide_index=True)
                
                csv = companies_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"top_companies_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No company data available")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### 📍 Companies by City")
        
        try:
            cities_df = load_jobs_by_city()
            cities_df_filtered = cities_df[
                (cities_df['city'].notna()) & 
                (cities_df['city'] != '') & 
                (cities_df['job_count'] > 0)
            ]
            cities = cities_df_filtered['city'].tolist()
            
            if cities:
                selected_city = st.selectbox("Select City", cities, key="company_city")
                num_companies_city = st.slider("Number of companies", 10, 30, 15, 5, key="city_companies")
                
                with st.spinner(f"Loading companies in {selected_city}..."):
                    city_companies_df = load_companies_by_city(selected_city, num_companies_city)
                
                if not city_companies_df.empty:
                    fig = create_modern_chart(
                        city_companies_df,
                        'bar',
                        x='job_count',
                        y='company_name',
                        orientation='h',
                        labels={'job_count': 'Job Count', 'company_name': 'Company'}
                    )
                    fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                    
                    st.dataframe(city_companies_df, use_container_width=True, hide_index=True)
                else:
                    st.warning(f"No company data for {selected_city}")
            else:
                st.warning("No city data available")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_location_analysis():
    """Location Analysis Page - Redesigned"""
    st.markdown("## 📍 Location Analysis")
    st.caption("Geographic distribution of job opportunities")
    
    try:
        with st.spinner("Loading location data..."):
            locations_df = load_jobs_by_city()
            locations_df = locations_df[
                (locations_df['city'].notna()) & 
                (locations_df['city'] != '') & 
                (locations_df['job_count'] > 0)
            ]
        
        if not locations_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.markdown("### 📊 Jobs by City")
                fig = create_modern_chart(
                    locations_df,
                    'bar',
                    x='city',
                    y='job_count',
                    labels={'job_count': 'Job Count', 'city': 'City'},
                    color='job_count',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.markdown("### 🥧 Market Distribution")
                fig = create_modern_chart(
                    locations_df,
                    'pie',
                    values='job_count',
                    names='city',
                    hole=0.4
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Location Statistics")
            st.dataframe(locations_df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### 🔄 City Comparison")
            
            selected_cities = st.multiselect(
                "Select cities to compare",
                locations_df['city'].tolist(),
                default=locations_df['city'].tolist()[:3]
            )
            
            if selected_cities:
                comparison_df = locations_df[locations_df['city'].isin(selected_cities)]
                
                fig = go.Figure(data=[
                    go.Bar(name='Jobs', x=comparison_df['city'], y=comparison_df['job_count']),
                    go.Bar(name='Companies', x=comparison_df['city'], y=comparison_df['company_count'])
                ])
                fig.update_layout(
                    barmode='group',
                    xaxis_title="City",
                    yaxis_title="Count",
                    height=400,
                    template='plotly_white' if st.session_state.theme_mode == 'light' else 'plotly_dark'
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No location data available")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def show_experience_analysis():
    """Experience Analysis Page - Redesigned"""
    st.markdown("## 📈 Experience Level Analysis")
    st.caption("Distribution of job opportunities by experience level")
    
    try:
        with st.spinner("Loading experience data..."):
            exp_df = load_experience_distribution()
        
        if not exp_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.markdown("### 🥧 Distribution")
                fig = create_modern_chart(
                    exp_df,
                    'pie',
                    values='job_count',
                    names='experience_level',
                    hole=0.4
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.markdown("### 📊 Demand by Level")
                fig = create_modern_chart(
                    exp_df,
                    'bar',
                    x='experience_level',
                    y='job_count',
                    labels={'job_count': 'Job Count', 'experience_level': 'Experience Level'},
                    color='job_count',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Statistics")
            st.dataframe(exp_df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No experience data available")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def show_salary_analysis():
    """Salary Analysis Page - Redesigned"""
    st.markdown("## 💰 Salary Analysis")
    st.caption("Compensation insights across skills and locations")
    
    try:
        analytics = get_analytics()
        
        total_jobs = analytics.get_total_jobs()
        jobs_with_salary = analytics.get_jobs_with_salary()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            render_metric_card("Total Jobs", f"{total_jobs:,}", "💼")
        with col2:
            render_metric_card("Jobs with Salary", f"{jobs_with_salary:,}", "💰")
        with col3:
            percentage = round(jobs_with_salary / total_jobs * 100, 1) if total_jobs > 0 else 0
            render_metric_card("Data Availability", f"{percentage}%", "📊")
        
        if jobs_with_salary == 0:
            st.warning("⚠️ No salary data available in current dataset")
            st.info("Most job postings in India don't publicly disclose salary ranges. This is normal.")
            return
        
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["🎯 By Skill", "📍 By City"])
        
        with tab1:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### 💰 Average Salary by Skill")
            
            min_jobs = st.slider("Minimum jobs required", 3, 20, 5)
            
            with st.spinner("Analyzing salary data..."):
                salary_df = analytics.get_salary_by_skill(min_jobs=min_jobs, limit=20)
            
            if not salary_df.empty:
                salary_df['avg_min_display'] = salary_df['avg_min_salary'].apply(
                    lambda x: f"₹{x/100000:.1f}L" if pd.notna(x) else "N/A"
                )
                salary_df['avg_max_display'] = salary_df['avg_max_salary'].apply(
                    lambda x: f"₹{x/100000:.1f}L" if pd.notna(x) else "N/A"
                )
                
                fig = create_modern_chart(
                    salary_df,
                    'bar',
                    x='avg_max_salary',
                    y='skill_name',
                    orientation='h',
                    labels={'avg_max_salary': 'Average Max Salary', 'skill_name': 'Skill'},
                    hover_data=['avg_min_display', 'avg_max_display', 'job_count']
                )
                fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                display_df = salary_df[['skill_name', 'avg_min_display', 'avg_max_display', 'job_count']]
                display_df.columns = ['Skill', 'Avg Min', 'Avg Max', 'Jobs']
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info("Not enough data to display salary by skill")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### 💰 Average Salary by City")
            
            with st.spinner("Analyzing salary data by city..."):
                city_salary_df = analytics.get_salary_by_city()
            
            if not city_salary_df.empty:
                city_salary_df['avg_min_display'] = city_salary_df['avg_min_salary'].apply(
                    lambda x: f"₹{x/100000:.1f}L" if pd.notna(x) else "N/A"
                )
                city_salary_df['avg_max_display'] = city_salary_df['avg_max_salary'].apply(
                    lambda x: f"₹{x/100000:.1f}L" if pd.notna(x) else "N/A"
                )
                
                fig = create_modern_chart(
                    city_salary_df,
                    'bar',
                    x='city',
                    y='avg_max_salary',
                    labels={'avg_max_salary': 'Average Max Salary', 'city': 'City'},
                    hover_data=['avg_min_display', 'avg_max_display', 'job_count']
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                display_df = city_salary_df[['city', 'avg_min_display', 'avg_max_display', 'job_count']]
                display_df.columns = ['City', 'Avg Min', 'Avg Max', 'Jobs']
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info("Not enough data to display salary by city")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    # Apply theme styles
    apply_theme_styles()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area with padding
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Route to appropriate page
    if st.session_state.current_page == "Overview":
        show_overview()
    elif st.session_state.current_page == "Skills":
        show_skills_analysis()
    elif st.session_state.current_page == "Companies":
        show_company_insights()
    elif st.session_state.current_page == "Locations":
        show_location_analysis()
    elif st.session_state.current_page == "Experience":
        show_experience_analysis()
    elif st.session_state.current_page == "Salary":
        show_salary_analysis()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: var(--color-text-tertiary); font-size: 0.875rem;">'
        '🚀 Job Intelligence Platform | Built with ❤️ by Team DBMS | © 2025'
        '</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
