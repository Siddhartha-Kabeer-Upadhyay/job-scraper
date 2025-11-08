"""
Enhanced Job Intelligence Platform Dashboard
Modern card-based UI with dark mode support
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime
import warnings

# Import components
from components.theme import init_theme, get_theme_colors, is_dark_mode
from components.cards import (
    metric_card, info_card, stat_card, company_card, 
    job_card, skill_badge, progress_card, empty_state, loading_skeleton
)
from components.filters import search_bar, chip_selector, filter_panel, sort_selector
from components.navigation import sidebar_navigation, theme_toggle, breadcrumb, collapsible_section
from styles import get_all_styles
from chart_utils import (
    create_bar_chart, create_pie_chart, create_line_chart,
    create_scatter_chart, create_sparkline, create_bubble_chart
)

# Import analytics
from analytics.insights import JobMarketAnalytics
from config import TEAM_MEMBERS, PLOTLY_CONFIG, CACHE_TTL

# Suppress warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='The keyword arguments have been deprecated')

# Page configuration
st.set_page_config(
    page_title="Job Intelligence Platform - Enhanced",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme
init_theme()

# Apply custom styles
st.markdown(get_all_styles(), unsafe_allow_html=True)

# Plotly configuration
# PLOTLY_CONFIG imported from config


# Cache functions
@st.cache_resource
def get_analytics():
    """Initialize analytics instance"""
    return JobMarketAnalytics()


@st.cache_data(ttl=CACHE_TTL)
def load_market_overview():
    analytics = get_analytics()
    return analytics.generate_market_overview()


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


def main():
    """Main application"""
    colors = get_theme_colors()
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
            <h2 style="margin: 0; background: linear-gradient(135deg, {colors['accent_primary']}, {colors['accent_secondary']});
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       background-clip: text;">
                🚀 Job Intel
            </h2>
            <p style="margin: 0.25rem 0 0 0; color: {colors['text_tertiary']}; font-size: 0.85rem;">
                Tech Job Market Analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Theme toggle
        if theme_toggle():
            st.rerun()
        
        st.markdown("---")
        
        # Navigation
        pages = {
            "Dashboard": "📊",
            "Skills Analysis": "💡",
            "Company Insights": "🏢",
            "Location Analysis": "🌍",
            "Job Explorer": "🔍",
        }
        
        page = sidebar_navigation(pages)
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### Quick Actions")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        if st.button("📥 Export Data", use_container_width=True):
            st.info("Export feature coming soon!")
        
        st.markdown("---")
        
        # Project info
        st.markdown("### About")
        st.markdown(f"""
        <div style="background: var(--card-secondary); padding: 1rem; border-radius: 8px; font-size: 0.85rem;">
            <p style="margin: 0 0 0.5rem 0; color: {colors['text_tertiary']};">
                <strong>DBMS Course Project</strong>
            </p>
            <p style="margin: 0; color: {colors['text_tertiary']};">
                Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Team
        st.markdown("### Team")
        
        for member in TEAM_MEMBERS:
            st.markdown(f"""
            <div style="margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: {colors['text_primary']};">{member['icon']} {member['name']}</div>
                <div style="font-size: 0.8rem; color: {colors['text_tertiary']}; margin-top: 0.25rem;">{member['role']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Skills Analysis":
        show_skills_analysis()
    elif page == "Company Insights":
        show_company_insights()
    elif page == "Location Analysis":
        show_location_analysis()
    elif page == "Job Explorer":
        show_job_explorer()


def show_dashboard():
    """Dashboard/Overview Page - Modern card-based layout"""
    colors = get_theme_colors()
    
    # Hero Section
    st.markdown(f"""
    <div class="hero-section fade-in">
        <div class="hero-content">
            <h1 class="hero-title">Job Market Intelligence</h1>
            <p class="hero-subtitle">Real-time analytics of India's tech job landscape</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with st.spinner("Loading market data..."):
            overview = load_market_overview()
        
        # Key Metrics in Glass Cards
        st.markdown("### 📈 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            metric_card("Total Jobs", f"{overview['total_jobs']:,}", icon="💼")
        
        with col2:
            metric_card("Companies", f"{overview['total_companies']:,}", icon="🏢")
        
        with col3:
            metric_card("Unique Skills", f"{overview['total_skills']:,}", icon="⚡")
        
        with col4:
            metric_card("Cities", f"{overview['total_cities']:,}", icon="🌍")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts in card grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔥 Top Skills in Demand")
            top_skills_df = pd.DataFrame(overview['top_10_skills'])
            
            if not top_skills_df.empty:
                fig = create_bar_chart(
                    top_skills_df,
                    x='job_count',
                    y='skill_name',
                    color='skill_category',
                    orientation='h',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                # Show top 5 as badges
                st.markdown("**Most Popular:**")
                badges_html = ""
                for _, row in top_skills_df.head(5).iterrows():
                    badges_html += skill_badge(row['skill_name'], row['job_count'], row['skill_category'])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                empty_state("No skills data available", "📊")
        
        with col2:
            st.markdown("### 🏆 Top Hiring Companies")
            top_companies_df = pd.DataFrame(overview['top_10_companies'])
            
            if not top_companies_df.empty:
                fig = create_bar_chart(
                    top_companies_df,
                    x='job_count',
                    y='company_name',
                    orientation='h',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                # Show top companies as mini cards
                st.markdown("**Top Recruiters:**")
                for _, row in top_companies_df.head(3).iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div style="background: var(--card-secondary); padding: 0.75rem; border-radius: 8px; 
                                    margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 600; color: {colors['text_primary']};">{row['company_name']}</span>
                            <span style="color: {colors['accent_primary']}; font-weight: 700;">{row['job_count']} jobs</span>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                empty_state("No company data available", "🏢")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Second row
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📍 Geographic Distribution")
            jobs_by_city_df = pd.DataFrame(overview['jobs_by_city'])
            jobs_by_city_df = jobs_by_city_df[jobs_by_city_df['job_count'] > 0]
            
            if not jobs_by_city_df.empty:
                fig = create_pie_chart(
                    jobs_by_city_df,
                    values='job_count',
                    names='city',
                    hole=0.5,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                empty_state("No location data", "🗺️")
        
        with col2:
            st.markdown("### 👨‍💼 Experience Level Breakdown")
            exp_dist_df = pd.DataFrame(overview['experience_distribution'])
            
            if not exp_dist_df.empty:
                fig = create_pie_chart(
                    exp_dist_df,
                    values='job_count',
                    names='experience_level',
                    hole=0.5,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                # Experience stats
                st.markdown("**Job Distribution:**")
                for _, row in exp_dist_df.iterrows():
                    percentage = (row['job_count'] / overview['total_jobs'] * 100) if overview['total_jobs'] > 0 else 0
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span style="color: {colors['text_secondary']};">{row['experience_level']}</span>
                            <span style="color: {colors['accent_primary']}; font-weight: 600;">{percentage:.1f}%</span>
                        </div>
                        <div style="background: {colors['card_secondary']}; height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, {colors['accent_primary']}, {colors['accent_secondary']}); 
                                        height: 100%; width: {percentage}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                empty_state("No experience data", "💼")
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Ensure database is populated with job data.")


def show_skills_analysis():
    """Skills Analysis Page - Card-based with interactive filters"""
    colors = get_theme_colors()
    
    breadcrumb(["Home", "Skills Analysis"])
    
    st.markdown(f"""
    <div class="fade-in">
        <h1 style="color: {colors['text_primary']};">💡 Skills Analysis</h1>
        <p style="color: {colors['text_secondary']};">Explore the most in-demand technical skills</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search and filters
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = search_bar("Search skills...", key="skill_search")
    with col2:
        view_mode = st.selectbox("View", ["Chart", "Cards", "List"], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Overall Demand", "🌍 By Location", "🔗 Co-occurrence"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### Most In-Demand Skills")
        with col2:
            num_skills = st.slider("Top", 10, 50, 20, 5, label_visibility="collapsed")
        
        try:
            with st.spinner("Loading skills..."):
                skills_df = load_top_skills(num_skills)
            
            if not skills_df.empty:
                # Filter by search
                if search_query:
                    skills_df = skills_df[skills_df['skill_name'].str.contains(search_query, case=False, na=False)]
                
                if skills_df.empty:
                    empty_state(f"No skills found matching '{search_query}'", "🔍")
                else:
                    if view_mode == "Chart":
                        fig = create_bar_chart(
                            skills_df,
                            x='job_count',
                            y='skill_name',
                            color='skill_category',
                            orientation='h',
                            height=600
                        )
                        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                    
                    elif view_mode == "Cards":
                        # Show as cards
                        cols_per_row = 3
                        for i in range(0, len(skills_df), cols_per_row):
                            cols = st.columns(cols_per_row)
                            for j, col in enumerate(cols):
                                if i + j < len(skills_df):
                                    row = skills_df.iloc[i + j]
                                    with col:
                                        stat_card(
                                            row['skill_name'],
                                            {
                                                "Job Count": row['job_count'],
                                                "Category": row['skill_category'],
                                                "Percentage": f"{row['percentage']:.1f}%"
                                            }
                                        )
                    
                    else:  # List view
                        st.dataframe(
                            skills_df[['skill_name', 'skill_category', 'job_count', 'percentage']],
                            use_container_width=True,
                            hide_index=True
                        )
                    
                    # Download button
                    st.markdown("<br>", unsafe_allow_html=True)
                    csv = skills_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        f"top_skills_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv",
                        key='download-skills'
                    )
            else:
                empty_state("No skills data available", "📊")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab2:
        st.markdown("### Skills by Location")
        
        try:
            cities_df = load_jobs_by_city()
            cities = cities_df[cities_df['job_count'] > 0]['city'].tolist()
            
            if cities:
                col1, col2 = st.columns([2, 1])
                with col1:
                    selected_city = st.selectbox("Select City", cities, key="city_skills_select")
                with col2:
                    num_skills_city = st.slider("Top Skills", 10, 30, 15, 5, key="city_skills_slider")
                
                with st.spinner("Loading city skills..."):
                    city_skills_df = load_top_skills_by_city(selected_city, num_skills_city)
                
                if not city_skills_df.empty:
                    fig = create_bar_chart(
                        city_skills_df,
                        x='job_count',
                        y='skill_name',
                        orientation='h',
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                    
                    # Show top 10 as badges
                    st.markdown(f"**Top Skills in {selected_city}:**")
                    badges_html = ""
                    for _, row in city_skills_df.head(10).iterrows():
                        badges_html += skill_badge(row['skill_name'], row['job_count'])
                    st.markdown(badges_html, unsafe_allow_html=True)
                else:
                    empty_state(f"No skill data for {selected_city}", "📍")
            else:
                empty_state("No city data available", "🌍")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab3:
        st.markdown("### Skill Co-occurrence Analysis")
        st.caption("Skills frequently requested together in job postings")
        
        col1, col2 = st.columns(2)
        with col1:
            min_count = st.number_input("Minimum occurrences", 5, 50, 10, 5)
        with col2:
            limit = st.number_input("Number of pairs", 10, 100, 30, 10)
        
        try:
            with st.spinner("Analyzing skill pairs..."):
                cooccurrence_df = load_skill_cooccurrence(min_count, limit)
            
            if not cooccurrence_df.empty:
                cooccurrence_df['skill_pair'] = cooccurrence_df['skill_1'] + ' + ' + cooccurrence_df['skill_2']
                
                fig = create_bar_chart(
                    cooccurrence_df,
                    x='co_occurrence_count',
                    y='skill_pair',
                    orientation='h',
                    height=600
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                # Show as cards
                st.markdown("**Common Skill Combinations:**")
                cols_per_row = 2
                for i in range(0, min(6, len(cooccurrence_df)), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        if i + j < len(cooccurrence_df):
                            row = cooccurrence_df.iloc[i + j]
                            with col:
                                st.markdown(f"""
                                <div class="modern-card">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <div>
                                            <span class="badge badge-primary">{row['skill_1']}</span>
                                            <span style="margin: 0 0.5rem; color: {colors['text_tertiary']};">+</span>
                                            <span class="badge badge-info">{row['skill_2']}</span>
                                        </div>
                                        <div style="font-size: 1.5rem; font-weight: 700; color: {colors['accent_primary']};">
                                            {row['co_occurrence_count']}
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
            else:
                empty_state("No co-occurrence data with current filters", "🔗")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")


def show_company_insights():
    """Company Insights Page - Card grid layout"""
    colors = get_theme_colors()
    
    breadcrumb(["Home", "Company Insights"])
    
    st.markdown(f"""
    <div class="fade-in">
        <h1 style="color: {colors['text_primary']};">🏢 Company Insights</h1>
        <p style="color: {colors['text_secondary']};">Discover top recruiters and hiring trends</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar
    search_query = search_bar("Search companies...", key="company_search")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2 = st.tabs(["🏆 Top Companies", "🌍 By Location"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### Top Hiring Companies")
        with col2:
            num_companies = st.slider("Show", 10, 50, 20, 5, label_visibility="collapsed")
        
        try:
            with st.spinner("Loading companies..."):
                companies_df = load_top_companies(num_companies)
            
            if not companies_df.empty:
                # Filter by search
                if search_query:
                    companies_df = companies_df[companies_df['company_name'].str.contains(search_query, case=False, na=False)]
                
                if companies_df.empty:
                    empty_state(f"No companies found matching '{search_query}'", "🔍")
                else:
                    # Show chart
                    fig = create_bar_chart(
                        companies_df,
                        x='job_count',
                        y='company_name',
                        orientation='h',
                        height=600
                    )
                    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                    
                    # Show as company cards
                    st.markdown("### Company Profiles")
                    cols_per_row = 3
                    for i in range(0, min(12, len(companies_df)), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for j, col in enumerate(cols):
                            if i + j < len(companies_df):
                                row = companies_df.iloc[i + j]
                                with col:
                                    company_card(
                                        row['company_name'],
                                        row['job_count'],
                                        None  # We don't have locations in this view
                                    )
                    
                    # Download
                    st.markdown("<br>", unsafe_allow_html=True)
                    csv = companies_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        f"top_companies_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv"
                    )
            else:
                empty_state("No company data available", "🏢")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab2:
        st.markdown("### Companies by City")
        
        try:
            cities_df = load_jobs_by_city()
            cities = cities_df[cities_df['job_count'] > 0]['city'].tolist()
            
            if cities:
                col1, col2 = st.columns([2, 1])
                with col1:
                    selected_city = st.selectbox("Select City", cities, key="company_city")
                with col2:
                    num_companies_city = st.slider("Top Companies", 10, 30, 15, 5, key="city_companies")
                
                with st.spinner("Loading city companies..."):
                    city_companies_df = load_companies_by_city(selected_city, num_companies_city)
                
                if not city_companies_df.empty:
                    fig = create_bar_chart(
                        city_companies_df,
                        x='job_count',
                        y='company_name',
                        orientation='h',
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                    
                    # Show as cards
                    st.markdown(f"**Top Recruiters in {selected_city}:**")
                    cols_per_row = 3
                    for i in range(0, min(9, len(city_companies_df)), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for j, col in enumerate(cols):
                            if i + j < len(city_companies_df):
                                row = city_companies_df.iloc[i + j]
                                with col:
                                    company_card(row['company_name'], row['job_count'])
                else:
                    empty_state(f"No company data for {selected_city}", "📍")
            else:
                empty_state("No city data available", "🌍")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")


def show_location_analysis():
    """Location Analysis Page - Interactive comparison"""
    colors = get_theme_colors()
    
    breadcrumb(["Home", "Location Analysis"])
    
    st.markdown(f"""
    <div class="fade-in">
        <h1 style="color: {colors['text_primary']};">🌍 Location Analysis</h1>
        <p style="color: {colors['text_secondary']};">Compare job markets across Indian cities</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with st.spinner("Loading location data..."):
            locations_df = load_jobs_by_city()
            locations_df = locations_df[locations_df['job_count'] > 0]
        
        if not locations_df.empty:
            # City cards at top
            st.markdown("### City Overview")
            cols_per_row = 4
            for i in range(0, len(locations_df), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(locations_df):
                        row = locations_df.iloc[i + j]
                        with col:
                            stat_card(
                                f"📍 {row['city']}",
                                {
                                    "Jobs": f"{row['job_count']:,}",
                                    "Companies": f"{row['company_count']:,}",
                                }
                            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Job Distribution")
                fig = create_bar_chart(
                    locations_df,
                    x='city',
                    y='job_count',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            
            with col2:
                st.markdown("### Market Share")
                fig = create_pie_chart(
                    locations_df,
                    values='job_count',
                    names='city',
                    hole=0.5,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            
            # City comparison
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🔄 Compare Cities")
            
            selected_cities = st.multiselect(
                "Select cities to compare",
                locations_df['city'].tolist(),
                default=locations_df['city'].tolist()[:min(3, len(locations_df))],
                key="city_comparison"
            )
            
            if selected_cities:
                comparison_df = locations_df[locations_df['city'].isin(selected_cities)]
                
                # Side-by-side comparison cards
                cols = st.columns(len(selected_cities))
                for idx, city in enumerate(selected_cities):
                    city_data = comparison_df[comparison_df['city'] == city].iloc[0]
                    with cols[idx]:
                        progress_card(
                            city,
                            city_data['job_count'],
                            locations_df['job_count'].max(),
                            f"{city_data['company_count']} companies"
                        )
            
        else:
            empty_state("No location data available", "🗺️")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


def show_job_explorer():
    """Job Explorer - Browse individual job postings (placeholder)"""
    colors = get_theme_colors()
    
    breadcrumb(["Home", "Job Explorer"])
    
    st.markdown(f"""
    <div class="fade-in">
        <h1 style="color: {colors['text_primary']};">🔍 Job Explorer</h1>
        <p style="color: {colors['text_secondary']};">Browse and discover job opportunities</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search and filters
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_query = search_bar("Search jobs by title, company, or skills...", key="job_search")
    with col2:
        sort_by = st.selectbox("Sort", ["Recent", "Relevant", "Salary"], label_visibility="collapsed")
    with col3:
        view_type = st.selectbox("View", ["Cards", "List"], label_visibility="collapsed")
    
    # Filters panel
    with st.expander("🔧 Advanced Filters"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.multiselect("Experience Level", ["Entry Level", "Mid Level", "Senior Level", "Lead"])
        with col2:
            st.multiselect("Job Type", ["Full-time", "Part-time", "Contract", "Remote"])
        with col3:
            st.slider("Salary Range (LPA)", 0, 50, (0, 50))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Placeholder message
    st.info("💡 **Coming Soon!** The Job Explorer feature will allow you to browse individual job postings with advanced filtering and bookmarking capabilities.")
    
    # Demo job cards
    st.markdown("### 📋 Sample Job Listings")
    
    sample_jobs = [
        {
            "title": "Senior Software Engineer",
            "company": "Tech Corp India",
            "location": "Bangalore",
            "salary": "₹15L - ₹25L",
            "skills": ["Python", "Django", "AWS", "Docker"],
            "posted": "2 days ago"
        },
        {
            "title": "Data Scientist",
            "company": "Analytics Pro",
            "location": "Mumbai",
            "salary": "₹12L - ₹20L",
            "skills": ["Python", "Machine Learning", "SQL", "TensorFlow"],
            "posted": "1 week ago"
        },
        {
            "title": "Frontend Developer",
            "company": "Digital Solutions",
            "location": "Delhi",
            "salary": "₹8L - ₹15L",
            "skills": ["React", "JavaScript", "TypeScript", "CSS"],
            "posted": "3 days ago"
        },
    ]
    
    cols_per_row = 2
    for i in range(0, len(sample_jobs), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(sample_jobs):
                job = sample_jobs[i + j]
                with col:
                    job_card(
                        job["title"],
                        job["company"],
                        job["location"],
                        job["salary"],
                        job["skills"],
                        job["posted"]
                    )


if __name__ == "__main__":
    main()
