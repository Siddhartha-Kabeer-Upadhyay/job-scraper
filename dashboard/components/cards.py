"""
Reusable card components for the dashboard
"""

import streamlit as st
from components.theme import get_theme_colors


def metric_card(label, value, delta=None, icon=None):
    """
    Display a metric in a glassmorphism card
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional change/delta value
        icon: Optional icon (emoji or symbol)
    """
    colors = get_theme_colors()
    
    icon_html = f'<span style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</span>' if icon else ''
    delta_html = ''
    if delta:
        delta_color = colors['success'] if str(delta).startswith('+') else colors['error']
        delta_html = f'<div style="font-size: 0.9rem; color: {delta_color}; margin-top: 0.5rem;">{delta}</div>'
    
    card_html = f"""
    <div class="glass-metric fade-in">
        {icon_html}
        <div class="glass-metric-label">{label}</div>
        <div class="glass-metric-value">{value}</div>
        {delta_html}
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def info_card(title, content, subtitle=None, icon=None):
    """
    Display an information card with title and content
    
    Args:
        title: Card title
        content: Card content (can be HTML)
        subtitle: Optional subtitle
        icon: Optional icon
    """
    icon_html = f'<span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>' if icon else ''
    subtitle_html = f'<div class="card-subtitle">{subtitle}</div>' if subtitle else ''
    
    card_html = f"""
    <div class="modern-card fade-in">
        <div class="card-header">
            <div>
                <div style="display: flex; align-items: center;">
                    {icon_html}
                    <h3 class="card-title">{title}</h3>
                </div>
                {subtitle_html}
            </div>
        </div>
        <div class="card-body">
            {content}
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def stat_card(title, stats_dict, colors_dict=None):
    """
    Display a card with multiple statistics
    
    Args:
        title: Card title
        stats_dict: Dictionary of stat_name: stat_value
        colors_dict: Optional dictionary of stat_name: color
    """
    colors = get_theme_colors()
    
    stats_html = ''
    for key, value in stats_dict.items():
        color = colors_dict.get(key, colors['text_primary']) if colors_dict else colors['text_primary']
        stats_html += f"""
        <div style="margin: 0.75rem 0;">
            <div style="font-size: 0.9rem; color: {colors['text_tertiary']};">{key}</div>
            <div style="font-size: 1.5rem; font-weight: 600; color: {color};">{value}</div>
        </div>
        """
    
    card_html = f"""
    <div class="card-elevated fade-in">
        <h3 class="card-title" style="margin-bottom: 1rem;">{title}</h3>
        {stats_html}
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def company_card(company_name, job_count, locations=None, logo_url=None):
    """
    Display a company card with stats
    
    Args:
        company_name: Name of the company
        job_count: Number of job openings
        locations: List of locations
        logo_url: URL to company logo (optional)
    """
    colors = get_theme_colors()
    
    logo_html = ''
    if logo_url:
        logo_html = f'<img src="{logo_url}" alt="{company_name}" style="width: 50px; height: 50px; border-radius: 8px; margin-right: 1rem;" />'
    else:
        # Use initials as placeholder
        initials = ''.join([word[0] for word in company_name.split()[:2]]).upper()
        logo_html = f'''
        <div style="width: 50px; height: 50px; border-radius: 8px; 
                    background: linear-gradient(135deg, {colors['accent_primary']}, {colors['accent_secondary']});
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.2rem; font-weight: 700; color: white; margin-right: 1rem;">
            {initials}
        </div>
        '''
    
    locations_html = ''
    if locations:
        locations_str = ', '.join(locations[:3])
        if len(locations) > 3:
            locations_str += f' +{len(locations) - 3} more'
        locations_html = f'<div style="font-size: 0.85rem; color: {colors["text_tertiary"]}; margin-top: 0.5rem;">📍 {locations_str}</div>'
    
    card_html = f"""
    <div class="modern-card">
        <div style="display: flex; align-items: center;">
            {logo_html}
            <div style="flex: 1;">
                <h4 style="margin: 0; color: {colors['text_primary']};">{company_name}</h4>
                <div style="font-size: 1.2rem; font-weight: 600; color: {colors['accent_primary']}; margin-top: 0.25rem;">
                    {job_count} openings
                </div>
                {locations_html}
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def job_card(job_title, company, location, salary=None, skills=None, posted_date=None, job_url=None):
    """
    Display a job posting card
    
    Args:
        job_title: Job title (required, will be HTML-escaped)
        company: Company name (required, will be HTML-escaped)
        location: Job location (required, will be HTML-escaped)
        salary: Salary range (optional, will be HTML-escaped)
        skills: List of required skills (optional, will be HTML-escaped)
        posted_date: Date posted (optional, will be HTML-escaped)
        job_url: URL to job posting (optional, will be validated)
    """
    import html
    
    # Sanitize inputs
    job_title = html.escape(str(job_title))
    company = html.escape(str(company))
    location = html.escape(str(location))
    
    colors = get_theme_colors()
    
    salary_html = ''
    if salary:
        salary_html = f'<div style="font-size: 1.1rem; font-weight: 600; color: {colors["success"]}; margin-top: 0.5rem;">{html.escape(str(salary))}</div>'
    
    skills_html = ''
    if skills:
        skills_badges = ' '.join([f'<span class="badge badge-outline">{html.escape(str(skill))}</span>' for skill in skills[:5]])
        skills_html = f'<div style="margin-top: 1rem;">{skills_badges}</div>'
    
    posted_html = ''
    if posted_date:
        posted_html = f'<span style="color: {colors["text_tertiary"]}; font-size: 0.85rem;">Posted: {html.escape(str(posted_date))}</span>'
    
    apply_button = ''
    if job_url:
        # Basic URL validation
        url = str(job_url).strip()
        if url.startswith(('http://', 'https://')):
            # HTML escape the URL for safety
            safe_url = html.escape(url)
            apply_button = f'<a href="{safe_url}" target="_blank" rel="noopener noreferrer" style="text-decoration: none;"><button class="neuro-button">Apply Now</button></a>'
    
    card_html = f"""
    <div class="modern-card">
        <h3 style="margin: 0 0 0.5rem 0; color: {colors['text_primary']};">{job_title}</h3>
        <div style="font-size: 1rem; color: {colors['text_secondary']};">{company}</div>
        <div style="font-size: 0.9rem; color: {colors['text_tertiary']}; margin-top: 0.25rem;">📍 {location}</div>
        {salary_html}
        {skills_html}
        <div class="card-footer">
            {posted_html}
            {apply_button}
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def skill_badge(skill_name, count=None, category=None):
    """
    Display a skill as an interactive badge
    
    Args:
        skill_name: Name of the skill
        count: Number of jobs requiring this skill (optional)
        category: Skill category for color coding (optional)
    """
    colors = get_theme_colors()
    
    # Color based on category
    category_colors = {
        'Programming Language': colors['accent_primary'],
        'Framework': colors['info'],
        'Tool': colors['warning'],
        'Database': colors['success'],
        'Cloud': colors['accent_secondary'],
    }
    
    color = category_colors.get(category, colors['text_secondary'])
    
    count_html = ''
    if count:
        count_html = f' <span style="background: rgba(255,255,255,0.2); padding: 0.1rem 0.4rem; border-radius: 10px; font-size: 0.75rem;">{count}</span>'
    
    badge_html = f"""
    <span class="badge" style="background: {color}; color: white;">
        {skill_name}{count_html}
    </span>
    """
    
    return badge_html


def progress_card(title, current, total, label=None):
    """
    Display a progress card with a progress bar
    
    Args:
        title: Card title
        current: Current value
        total: Total/target value
        label: Optional label
    """
    colors = get_theme_colors()
    percentage = (current / total * 100) if total > 0 else 0
    
    label_html = f'<div style="color: {colors["text_tertiary"]}; font-size: 0.9rem;">{label}</div>' if label else ''
    
    card_html = f"""
    <div class="modern-card">
        <h4 style="margin: 0 0 1rem 0; color: {colors['text_primary']};">{title}</h4>
        {label_html}
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-size: 1.2rem; font-weight: 600; color: {colors['accent_primary']};">{current}</span>
            <span style="color: {colors['text_tertiary']};">/ {total}</span>
        </div>
        <div style="background: {colors['card_secondary']}; height: 8px; border-radius: 4px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, {colors['accent_primary']}, {colors['accent_secondary']}); 
                        height: 100%; width: {percentage}%; transition: width 0.5s ease;"></div>
        </div>
        <div style="text-align: right; margin-top: 0.25rem; color: {colors['text_tertiary']}; font-size: 0.85rem;">
            {percentage:.1f}%
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def empty_state(message, icon="📭", action_text=None, action_callback=None):
    """
    Display an empty state when no data is available
    
    Args:
        message: Message to display
        icon: Icon to display
        action_text: Optional action button text
        action_callback: Optional action callback
    """
    colors = get_theme_colors()
    
    action_html = ''
    if action_text:
        action_html = f'<button class="neuro-button" style="margin-top: 1rem;">{action_text}</button>'
    
    empty_html = f"""
    <div style="text-align: center; padding: 3rem 2rem; background: var(--card-primary); border-radius: 12px; border: 2px dashed var(--border);">
        <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">{icon}</div>
        <div style="font-size: 1.2rem; color: {colors['text_secondary']}; margin-bottom: 1rem;">{message}</div>
        {action_html}
    </div>
    """
    
    st.markdown(empty_html, unsafe_allow_html=True)


def loading_skeleton(height="100px", count=1):
    """
    Display loading skeleton placeholders
    
    Args:
        height: Height of skeleton
        count: Number of skeletons
    """
    for _ in range(count):
        st.markdown(
            f'<div class="skeleton" style="height: {height}; margin-bottom: 1rem;"></div>',
            unsafe_allow_html=True
        )
