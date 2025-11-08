
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from analytics.insights import JobMarketAnalytics
from database.db_operations import JobDatabase
from datetime import datetime

import warnings

# Suppress deprecation warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='The keyword arguments have been deprecated')

# Page configuration
st.set_page_config(
    page_title="Job Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modern theme system
try:
    from theme import create_design_tokens
    from pathlib import Path
    
    # Load modern CSS
    css_path = Path(__file__).parent / "styles_v2.css"
    if css_path.exists():
        with open(css_path) as f:
            modern_css = f.read()
        
        # Create CSS variables for light theme
        tokens = create_design_tokens('light')
        css_vars = ":root {\n"
        for key, value in tokens.items():
            css_vars += f"    {key}: {value};\n"
        css_vars += "}\n\n"
        
        # Apply modern styles
        st.markdown(f"<style>{css_vars}{modern_css}</style>", unsafe_allow_html=True)
    else:
        # Fallback to original styles if modern CSS not found
        st.markdown("""
        <style>
            .main-header {
                font-size: 2.2rem;
                font-weight: 600;
                color: #1f2937;
                margin-bottom: 1rem;
            }
            .sub-header {
                font-size: 1.1rem;
                color: #6b7280;
                margin-bottom: 2rem;
            }
            .metric-container {
                background-color: #f9fafb;
                padding: 1.5rem;
                border-radius: 0.5rem;
                border-left: 4px solid #3b82f6;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 1rem;
            }
            .stTabs [data-baseweb="tab"] {
                padding: 0.5rem 1.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
except ImportError:
    # Fallback to basic styles if modern theme module is not available
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #6b7280;
            margin-bottom: 2rem;
        }
        .metric-container {
            background-color: #f9fafb;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #3b82f6;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Plotly configuration
PLOTLY_CONFIG = {'displayModeBar': False}

# Helper functions
def format_salary(min_sal, max_sal, currency='INR'):
    """Format salary for display"""
    if pd.isna(min_sal) and pd.isna(max_sal):
        return "Not Specified"
    
    def format_amount(amount):
        if amount >= 100000:
            return f"₹{amount/100000:.1f}L"
        else:
            return f"₹{amount/1000:.0f}K"
    
    if pd.notna(min_sal) and pd.notna(max_sal):
        return f"{format_amount(min_sal)} - {format_amount(max_sal)}"
    elif pd.notna(min_sal):
        return f"{format_amount(min_sal)}+"
    elif pd.notna(max_sal):
        return f"Up to {format_amount(max_sal)}"
    
    return "Not Specified"

# Initialize analytics
@st.cache_resource
def get_analytics():
    """Initialize analytics instance"""
    return JobMarketAnalytics()

@st.cache_resource
def get_database():
    """Initialize database instance"""
    return JobDatabase()

# Cache data loading
@st.cache_data(ttl=3600)
def load_market_overview():
    analytics = get_analytics()
    return analytics.generate_market_overview()

@st.cache_data(ttl=3600)
def load_data_quality():
    """Load data quality statistics"""
    db = get_database()
    return db.get_data_quality_stats()

@st.cache_data(ttl=3600)
def load_top_skills(limit=20):
    analytics = get_analytics()
    return analytics.get_top_skills(limit)

@st.cache_data(ttl=3600)
def load_top_companies(limit=20):
    analytics = get_analytics()
    return analytics.get_top_hiring_companies(limit)

@st.cache_data(ttl=3600)
def load_jobs_by_city():
    analytics = get_analytics()
    return analytics.get_jobs_by_city()

@st.cache_data(ttl=3600)
def load_skill_cooccurrence(min_count=10, limit=50):
    analytics = get_analytics()
    return analytics.get_skill_cooccurrence(min_count, limit)

@st.cache_data(ttl=3600)
def load_experience_distribution():
    analytics = get_analytics()
    return analytics.get_experience_distribution()

@st.cache_data(ttl=3600)
def load_top_skills_by_city(city, limit=20):
    analytics = get_analytics()
    return analytics.get_top_skills_by_city(city, limit)

@st.cache_data(ttl=3600)
def load_companies_by_city(city, limit=20):
    analytics = get_analytics()
    return analytics.get_companies_by_city(city, limit)


def main():
    # Header
    st.markdown('<h1 class="main-header">Job Intelligence Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tech Job Market Analytics for India</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        
        page = st.radio(
            "Select Analysis View:",
            ["Market Overview", "Skills Analysis", "Company Insights", 
             "Location Analysis", "Experience Trends", "Salary Analysis"],
            label_visibility="visible"
        )
        
        st.markdown("---")
        
        # Data refresh
        if st.button("Refresh Data", width='stretch'):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Project info
        st.markdown("### Project Information")
        st.markdown("**DBMS Course Project**")
        st.markdown("**Last Updated:** " + datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        st.markdown("---")
        
        # Team
        st.markdown("### Team Members")
        st.markdown("""
        **Siddhartha Kabeer Upadhyay**  
        Backend & Database
        
        **Adrika Srivastava**  
        Frontend Development
        
        **Vibhor Saini**  
        Data Processing & NLP
        
        **Nelly**  
        Quality Assurance & Documentation
        """)
    
    # Route to appropriate page
    if page == "Market Overview":
        show_overview()
    elif page == "Skills Analysis":
        show_skills_analysis()
    elif page == "Company Insights":
        show_company_insights()
    elif page == "Location Analysis":
        show_location_analysis()
    elif page == "Experience Trends":
        show_experience_analysis()
    elif page == "Salary Analysis":
        show_salary_analysis()


def show_overview():
    """Market Overview Page"""
    st.header("Market Overview")
    st.markdown("High-level statistics of the tech job market")
    
    try:
        with st.spinner("Loading data..."):
            overview = load_market_overview()
            quality_stats = load_data_quality()
        
        # Data Quality Alert
        if quality_stats['location_coverage'] < 100:
            st.warning(f"⚠️ Data Quality Notice: {quality_stats['location_coverage']:.1f}% of jobs have valid location data. "
                      f"Jobs without valid Indian locations are excluded from this dashboard.")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Jobs", f"{overview['total_jobs']:,}")
        with col2:
            st.metric("Companies", f"{overview['total_companies']:,}")
        with col3:
            st.metric("Unique Skills", f"{overview['total_skills']:,}")
        with col4:
            st.metric("Cities Covered", f"{overview['total_cities']:,}")
        
        # Data Coverage Metrics
        st.markdown("---")
        st.subheader("Data Coverage")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Location Data", f"{quality_stats['location_coverage']:.1f}%")
        with col2:
            st.metric("Salary Data", f"{quality_stats['salary_coverage']:.1f}%")
        with col3:
            st.metric("Description Data", f"{quality_stats['description_coverage']:.1f}%")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Skills")
            top_skills_df = pd.DataFrame(overview['top_10_skills'])
            
            if not top_skills_df.empty:
                fig = px.bar(
                    top_skills_df,
                    x='job_count',
                    y='skill_name',
                    orientation='h',
                    color='skill_category',
                    labels={'job_count': 'Job Count', 'skill_name': 'Skill'}
                )
                fig.update_layout(
                    height=400,
                    showlegend=True,
                    yaxis={'categoryorder':'total ascending'},
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        
        with col2:
            st.subheader("Top 10 Hiring Companies")
            top_companies_df = pd.DataFrame(overview['top_10_companies'])
            
            if not top_companies_df.empty:
                fig = px.bar(
                    top_companies_df,
                    x='job_count',
                    y='company_name',
                    orientation='h',
                    labels={'job_count': 'Job Count', 'company_name': 'Company'}
                )
                fig.update_layout(
                    height=400,
                    yaxis={'categoryorder':'total ascending'},
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Job Distribution by City")
            jobs_by_city_df = pd.DataFrame(overview['jobs_by_city'])
            # Filter out null/NaN locations and ensure only valid data
            jobs_by_city_df = jobs_by_city_df[
                (jobs_by_city_df['city'].notna()) & 
                (jobs_by_city_df['city'] != '') & 
                (jobs_by_city_df['job_count'] > 0)
            ]
            
            if not jobs_by_city_df.empty:
                fig = px.pie(
                    jobs_by_city_df,
                    values='job_count',
                    names='city',
                    hole=0.4
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        
        with col2:
            st.subheader("Experience Level Distribution")
            exp_dist_df = pd.DataFrame(overview['experience_distribution'])
            
            if not exp_dist_df.empty:
                fig = px.pie(
                    exp_dist_df,
                    values='job_count',
                    names='experience_level',
                    hole=0.4
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Ensure database is populated with job data.")


def show_skills_analysis():
    """Skills Analysis Page"""
    st.header("Skills Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Overall Demand", "By Location", "Co-occurrence"])
    
    with tab1:
        st.subheader("Most In-Demand Skills")
        
        num_skills = st.slider("Number of skills", 10, 50, 20, 5)
        
        try:
            with st.spinner("Loading..."):
                skills_df = load_top_skills(num_skills)
            
            if not skills_df.empty:
                fig = px.bar(
                    skills_df,
                    x='job_count',
                    y='skill_name',
                    orientation='h',
                    color='skill_category',
                    labels={'job_count': 'Job Count', 'skill_name': 'Skill'},
                    hover_data=['percentage']
                )
                fig.update_layout(
                    height=600,
                    yaxis={'categoryorder':'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                st.subheader("Detailed Data")
                st.dataframe(skills_df, width='stretch', hide_index=True)
                
                csv = skills_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"top_skills_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data available")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab2:
        st.subheader("Skills by City")
        
        try:
            cities_df = load_jobs_by_city()
            # Filter to only valid cities with jobs
            cities_df_filtered = cities_df[
                (cities_df['city'].notna()) & 
                (cities_df['city'] != '') & 
                (cities_df['job_count'] > 0)
            ]
            cities = cities_df_filtered['city'].tolist()
            
            if not cities:
                st.warning("No city data available")
                return
            
            selected_city = st.selectbox("Select City", cities)
            num_skills_city = st.slider("Number of skills", 10, 30, 15, 5, key="city_skills")
            
            with st.spinner("Loading..."):
                city_skills_df = load_top_skills_by_city(selected_city, num_skills_city)
            
            if not city_skills_df.empty:
                fig = px.bar(
                    city_skills_df,
                    x='job_count',
                    y='skill_name',
                    orientation='h',
                    labels={'job_count': 'Job Count', 'skill_name': 'Skill'}
                )
                fig.update_layout(
                    height=500,
                    yaxis={'categoryorder':'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                st.dataframe(city_skills_df, width='stretch', hide_index=True)
            else:
                st.warning(f"No data for {selected_city}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab3:
        st.subheader("Skill Co-occurrence")
        st.caption("Skills frequently requested together")
        
        col1, col2 = st.columns(2)
        with col1:
            min_count = st.number_input("Minimum occurrences", 5, 50, 10, 5)
        with col2:
            limit = st.number_input("Number of pairs", 10, 100, 30, 10)
        
        try:
            with st.spinner("Analyzing..."):
                cooccurrence_df = load_skill_cooccurrence(min_count, limit)
            
            if not cooccurrence_df.empty:
                cooccurrence_df['skill_pair'] = cooccurrence_df['skill_1'] + ' + ' + cooccurrence_df['skill_2']
                
                fig = px.bar(
                    cooccurrence_df,
                    x='co_occurrence_count',
                    y='skill_pair',
                    orientation='h',
                    labels={'co_occurrence_count': 'Job Count', 'skill_pair': 'Skill Pair'}
                )
                fig.update_layout(
                    height=600,
                    yaxis={'categoryorder':'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                st.dataframe(
                    cooccurrence_df[['skill_1', 'skill_2', 'co_occurrence_count']],
                    width='stretch',
                    hide_index=True
                )
            else:
                st.warning("No co-occurrence data with current filters")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")


def show_company_insights():
    """Company Insights Page"""
    st.header("Company Insights")
    
    tab1, tab2 = st.tabs(["Top Companies", "By Location"])
    
    with tab1:
        st.subheader("Top Hiring Companies")
        
        num_companies = st.slider("Number of companies", 10, 50, 20, 5)
        
        try:
            with st.spinner("Loading..."):
                companies_df = load_top_companies(num_companies)
            
            if not companies_df.empty:
                fig = px.bar(
                    companies_df,
                    x='job_count',
                    y='company_name',
                    orientation='h',
                    color='cities_hiring_in',
                    labels={'job_count': 'Job Count', 'company_name': 'Company', 'cities_hiring_in': 'Cities'},
                )
                fig.update_layout(
                    height=600,
                    yaxis={'categoryorder':'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                st.dataframe(companies_df, width='stretch', hide_index=True)
                
                csv = companies_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"top_companies_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data available")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab2:
        st.subheader("Companies by City")
        
        try:
            cities_df = load_jobs_by_city()
            # Filter to only valid cities with jobs
            cities_df_filtered = cities_df[
                (cities_df['city'].notna()) & 
                (cities_df['city'] != '') & 
                (cities_df['job_count'] > 0)
            ]
            cities = cities_df_filtered['city'].tolist()
            
            if not cities:
                st.warning("No city data available")
                return
            
            selected_city = st.selectbox("Select City", cities, key="company_city")
            num_companies_city = st.slider("Number of companies", 10, 30, 15, 5, key="city_companies")
            
            with st.spinner("Loading..."):
                city_companies_df = load_companies_by_city(selected_city, num_companies_city)
            
            if not city_companies_df.empty:
                fig = px.bar(
                    city_companies_df,
                    x='job_count',
                    y='company_name',
                    orientation='h',
                    labels={'job_count': 'Job Count', 'company_name': 'Company'}
                )
                fig.update_layout(
                    height=500,
                    yaxis={'categoryorder':'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                st.dataframe(city_companies_df, width='stretch', hide_index=True)
            else:
                st.warning(f"No data for {selected_city}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")


def show_location_analysis():
    """Location Analysis Page"""
    st.header("Location Analysis")
    
    try:
        with st.spinner("Loading..."):
            locations_df = load_jobs_by_city()
            # Filter out null/NaN locations
            locations_df = locations_df[
                (locations_df['city'].notna()) & 
                (locations_df['city'] != '') & 
                (locations_df['job_count'] > 0)
            ]
        
        if not locations_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Jobs by City")
                fig = px.bar(
                    locations_df,
                    x='city',
                    y='job_count',
                    labels={'job_count': 'Job Count', 'city': 'City'},
                    color='job_count',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            
            with col2:
                st.subheader("Market Distribution")
                fig = px.pie(
                    locations_df,
                    values='job_count',
                    names='city',
                    hole=0.4
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            
            st.subheader("Location Statistics")
            st.dataframe(locations_df, width='stretch', hide_index=True)
            
            st.markdown("---")
            st.subheader("City Comparison")
            
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
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        else:
            st.warning("No location data available")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")


def show_experience_analysis():
    """Experience Analysis Page"""
    st.header("Experience Level Analysis")
    
    try:
        with st.spinner("Loading..."):
            exp_df = load_experience_distribution()
        
        if not exp_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Distribution")
                fig = px.pie(
                    exp_df,
                    values='job_count',
                    names='experience_level',
                    hole=0.4
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            
            with col2:
                st.subheader("Demand by Level")
                fig = px.bar(
                    exp_df,
                    x='experience_level',
                    y='job_count',
                    labels={'job_count': 'Job Count', 'experience_level': 'Experience Level'},
                    color='job_count',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            
            st.subheader("Statistics")
            st.dataframe(exp_df, width='stretch', hide_index=True)
            
        else:
            st.warning("No experience data available")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")


def show_salary_analysis():
    """Salary Analysis Page"""
    st.header("Salary Analysis")
    st.caption("Note: Only showing jobs with disclosed salary information")
    
    try:
        analytics = get_analytics()
        
        # Get stats
        total_jobs = analytics.get_total_jobs()
        jobs_with_salary = analytics.get_jobs_with_salary()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Jobs", f"{total_jobs:,}")
        with col2:
            st.metric("Jobs with Salary", f"{jobs_with_salary:,}")
        with col3:
            percentage = round(jobs_with_salary / total_jobs * 100, 1) if total_jobs > 0 else 0
            st.metric("Data Availability", f"{percentage}%")
        
        if jobs_with_salary == 0:
            st.warning("No salary data available in current dataset")
            st.info("Most job postings in India don't publicly disclose salary ranges. This is normal.")
            return
        
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["By Skill", "By City"])
        
        with tab1:
            st.subheader("Average Salary by Skill")
            
            min_jobs = st.slider("Minimum jobs required", 3, 20, 5)
            
            with st.spinner("Loading..."):
                salary_df = analytics.get_salary_by_skill(min_jobs=min_jobs, limit=20)
            
            if not salary_df.empty:
                # Format salary for display
                salary_df['avg_min_display'] = salary_df['avg_min_salary'].apply(
                    lambda x: f"₹{x/100000:.1f}L" if pd.notna(x) else "N/A"
                )
                salary_df['avg_max_display'] = salary_df['avg_max_salary'].apply(
                    lambda x: f"₹{x/100000:.1f}L" if pd.notna(x) else "N/A"
                )
                
                # Bar chart
                fig = px.bar(
                    salary_df,
                    x='avg_max_salary',
                    y='skill_name',
                    orientation='h',
                    labels={'avg_max_salary': 'Average Max Salary', 'skill_name': 'Skill'},
                    hover_data=['avg_min_display', 'avg_max_display', 'job_count']
                )
                fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                # Data table
                display_df = salary_df[['skill_name', 'avg_min_display', 'avg_max_display', 'job_count']]
                display_df.columns = ['Skill', 'Avg Min', 'Avg Max', 'Jobs']
                st.dataframe(display_df, width='stretch', hide_index=True)
            else:
                st.info("Not enough data to display salary by skill")
        
        with tab2:
            st.subheader("Average Salary by City")
            
            with st.spinner("Loading..."):
                city_salary_df = analytics.get_salary_by_city()
            
            if not city_salary_df.empty:
                # Format salary
                city_salary_df['avg_min_display'] = city_salary_df['avg_min_salary'].apply(
                    lambda x: f"₹{x/100000:.1f}L" if pd.notna(x) else "N/A"
                )
                city_salary_df['avg_max_display'] = city_salary_df['avg_max_salary'].apply(
                    lambda x: f"₹{x/100000:.1f}L" if pd.notna(x) else "N/A"
                )
                
                # Bar chart
                fig = px.bar(
                    city_salary_df,
                    x='city',
                    y='avg_max_salary',
                    labels={'avg_max_salary': 'Average Max Salary', 'city': 'City'},
                    hover_data=['avg_min_display', 'avg_max_display', 'job_count']
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
                
                # Data table
                display_df = city_salary_df[['city', 'avg_min_display', 'avg_max_display', 'job_count']]
                display_df.columns = ['City', 'Avg Min', 'Avg Max', 'Jobs']
                st.dataframe(display_df, width='stretch', hide_index=True)
            else:
                st.info("Not enough data to display salary by city")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
