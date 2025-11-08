"""
Navigation components for the dashboard
"""

import streamlit as st
from components.theme import get_theme_colors, toggle_theme, is_dark_mode


def sidebar_navigation(pages, current_page=None):
    """
    Create sidebar navigation with icons
    
    Args:
        pages: Dict of {page_name: icon_emoji}
        current_page: Currently selected page
        
    Returns:
        str: Selected page name
    """
    colors = get_theme_colors()
    
    st.markdown(f"""
    <style>
        .nav-item {{
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            color: var(--text-secondary);
            text-decoration: none;
        }}
        
        .nav-item:hover {{
            background: var(--card-secondary);
            color: var(--text-primary);
        }}
        
        .nav-item.active {{
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
            font-weight: 600;
        }}
        
        .nav-icon {{
            font-size: 1.2rem;
            margin-right: 0.75rem;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    selected = st.radio(
        "Navigation",
        list(pages.keys()),
        index=list(pages.keys()).index(current_page) if current_page in pages else 0,
        format_func=lambda x: f"{pages[x]} {x}",
        label_visibility="collapsed"
    )
    
    return selected


def theme_toggle():
    """
    Create a theme toggle button in sidebar
    
    Returns:
        bool: True if theme was toggled
    """
    colors = get_theme_colors()
    dark = is_dark_mode()
    
    st.markdown(f"""
    <style>
        .theme-toggle {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 1rem;
            background: var(--card-secondary);
            border-radius: 10px;
            margin: 1rem 0;
        }}
        
        .theme-label {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        .toggle-switch {{
            position: relative;
            width: 50px;
            height: 26px;
            background: var(--border);
            border-radius: 13px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .toggle-switch.active {{
            background: var(--accent-primary);
        }}
        
        .toggle-slider {{
            position: absolute;
            top: 3px;
            left: 3px;
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 50%;
            transition: all 0.3s ease;
        }}
        
        .toggle-switch.active .toggle-slider {{
            left: 27px;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    icon = "🌙" if dark else "☀️"
    label = "Dark Mode" if dark else "Light Mode"
    
    st.markdown(f"""
    <div class="theme-toggle">
        <span class="theme-label">{icon} {label}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Use checkbox for toggle
    toggled = st.checkbox(
        "Toggle Theme",
        value=dark,
        key="theme_toggle_checkbox",
        label_visibility="collapsed"
    )
    
    if toggled != dark:
        toggle_theme()
        return True
    
    return False


def breadcrumb(items):
    """
    Display breadcrumb navigation
    
    Args:
        items: List of breadcrumb items
    """
    colors = get_theme_colors()
    
    st.markdown(f"""
    <style>
        .breadcrumb {{
            display: flex;
            align-items: center;
            padding: 0.5rem 0;
            color: var(--text-tertiary);
            font-size: 0.9rem;
        }}
        
        .breadcrumb-item {{
            margin: 0 0.5rem;
        }}
        
        .breadcrumb-item:first-child {{
            margin-left: 0;
        }}
        
        .breadcrumb-separator {{
            margin: 0 0.5rem;
        }}
        
        .breadcrumb-item.active {{
            color: var(--text-primary);
            font-weight: 500;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    breadcrumb_html = '<div class="breadcrumb">'
    for idx, item in enumerate(items):
        active_class = " active" if idx == len(items) - 1 else ""
        breadcrumb_html += f'<span class="breadcrumb-item{active_class}">{item}</span>'
        if idx < len(items) - 1:
            breadcrumb_html += '<span class="breadcrumb-separator">/</span>'
    breadcrumb_html += '</div>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)


def tabs_navigation(tabs, key=None):
    """
    Create custom styled tabs
    
    Args:
        tabs: List of tab names
        key: Unique key
        
    Returns:
        str: Selected tab
    """
    colors = get_theme_colors()
    
    st.markdown(f"""
    <style>
        .custom-tabs {{
            display: flex;
            gap: 0.5rem;
            border-bottom: 2px solid var(--border);
            margin-bottom: 1.5rem;
        }}
        
        .custom-tab {{
            padding: 0.75rem 1.5rem;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            color: var(--text-secondary);
            transition: all 0.2s ease;
            font-weight: 500;
        }}
        
        .custom-tab:hover {{
            color: var(--text-primary);
        }}
        
        .custom-tab.active {{
            color: var(--accent-primary);
            border-bottom-color: var(--accent-primary);
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Use Streamlit's native tabs with custom styling
    return st.tabs(tabs)


def floating_action_button(icon, tooltip, key=None):
    """
    Create a floating action button
    
    Args:
        icon: Button icon (emoji or symbol)
        tooltip: Tooltip text
        key: Unique key
        
    Returns:
        bool: True if button was clicked
    """
    colors = get_theme_colors()
    
    st.markdown(f"""
    <style>
        .fab {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 8px 20px var(--shadow);
            cursor: pointer;
            transition: all 0.3s ease;
            z-index: 1000;
        }}
        
        .fab:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 30px var(--shadow);
        }}
        
        .fab:active {{
            transform: translateY(-2px);
        }}
    </style>
    """, unsafe_allow_html=True)
    
    return st.button(
        icon,
        key=key,
        help=tooltip,
        use_container_width=False
    )


def collapsible_section(title, content_func, default_expanded=True, icon=None):
    """
    Create a collapsible section
    
    Args:
        title: Section title
        content_func: Function that renders content
        default_expanded: Whether expanded by default
        icon: Optional icon
    """
    colors = get_theme_colors()
    
    icon_html = f"{icon} " if icon else ""
    
    with st.expander(f"{icon_html}{title}", expanded=default_expanded):
        content_func()


def progress_indicator(current_step, total_steps, step_labels=None):
    """
    Display a step progress indicator
    
    Args:
        current_step: Current step (1-indexed)
        total_steps: Total number of steps
        step_labels: Optional list of step labels
    """
    colors = get_theme_colors()
    
    st.markdown(f"""
    <style>
        .progress-steps {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 2rem 0;
        }}
        
        .progress-step {{
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
            position: relative;
        }}
        
        .progress-step-circle {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--card-secondary);
            border: 2px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            color: var(--text-tertiary);
            position: relative;
            z-index: 2;
        }}
        
        .progress-step.active .progress-step-circle {{
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            border-color: var(--accent-primary);
            color: white;
        }}
        
        .progress-step.completed .progress-step-circle {{
            background: var(--success);
            border-color: var(--success);
            color: white;
        }}
        
        .progress-step-label {{
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--text-tertiary);
        }}
        
        .progress-step.active .progress-step-label {{
            color: var(--text-primary);
            font-weight: 500;
        }}
        
        .progress-line {{
            position: absolute;
            top: 20px;
            left: 50%;
            right: -50%;
            height: 2px;
            background: var(--border);
            z-index: 1;
        }}
        
        .progress-step.completed .progress-line {{
            background: var(--success);
        }}
    </style>
    """, unsafe_allow_html=True)
    
    steps_html = '<div class="progress-steps">'
    for i in range(1, total_steps + 1):
        state_class = ""
        if i < current_step:
            state_class = "completed"
        elif i == current_step:
            state_class = "active"
        
        label = step_labels[i-1] if step_labels and len(step_labels) >= i else f"Step {i}"
        
        line_html = '<div class="progress-line"></div>' if i < total_steps else ''
        
        steps_html += f"""
        <div class="progress-step {state_class}">
            <div class="progress-step-circle">
                {i if i >= current_step else '✓'}
            </div>
            <div class="progress-step-label">{label}</div>
            {line_html}
        </div>
        """
    
    steps_html += '</div>'
    
    st.markdown(steps_html, unsafe_allow_html=True)
