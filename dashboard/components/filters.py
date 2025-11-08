"""
Filter and search components for the dashboard
"""

import streamlit as st
from components.theme import get_theme_colors


def search_bar(placeholder="Search...", key=None):
    """
    Display a search bar with custom styling
    
    Args:
        placeholder: Placeholder text
        key: Unique key for the widget
        
    Returns:
        str: Search query
    """
    colors = get_theme_colors()
    
    st.markdown(f"""
    <style>
        .search-container {{
            background: var(--card-primary);
            border-radius: 12px;
            padding: 0.5rem 1rem;
            border: 2px solid var(--border);
            display: flex;
            align-items: center;
            transition: all 0.3s ease;
        }}
        
        .search-container:focus-within {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .search-icon {{
            color: var(--text-tertiary);
            margin-right: 0.5rem;
            font-size: 1.2rem;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    return st.text_input(
        "Search",
        placeholder=placeholder,
        label_visibility="collapsed",
        key=key
    )


def chip_selector(options, selected=None, key=None, multi=True):
    """
    Display options as selectable chips
    
    Args:
        options: List of options
        selected: Currently selected option(s)
        key: Unique key
        multi: Allow multiple selection
        
    Returns:
        Selected option(s)
    """
    colors = get_theme_colors()
    
    if selected is None:
        selected = [] if multi else None
    
    st.markdown("""
    <style>
        .chip-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chip-container">', unsafe_allow_html=True)
    
    if multi:
        # Multiple selection
        cols = st.columns(min(len(options), 5))
        result = []
        for idx, option in enumerate(options):
            with cols[idx % len(cols)]:
                if st.checkbox(option, value=option in selected, key=f"{key}_{option}" if key else None):
                    result.append(option)
        st.markdown('</div>', unsafe_allow_html=True)
        return result
    else:
        # Single selection
        result = st.radio(
            "Select option",
            options,
            index=options.index(selected) if selected in options else 0,
            key=key,
            label_visibility="collapsed",
            horizontal=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        return result


def filter_panel(filters_config, key_prefix="filter"):
    """
    Display a collapsible filter panel
    
    Args:
        filters_config: Dict of filter_name: filter_options
        key_prefix: Prefix for widget keys
        
    Returns:
        dict: Selected filters
    """
    colors = get_theme_colors()
    
    with st.expander("🔍 Filters", expanded=False):
        st.markdown(f"""
        <style>
            .filter-section {{
                background: var(--card-secondary);
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1rem;
            }}
            
            .filter-label {{
                color: var(--text-primary);
                font-weight: 600;
                margin-bottom: 0.5rem;
            }}
        </style>
        """, unsafe_allow_html=True)
        
        selected_filters = {}
        
        for filter_name, filter_options in filters_config.items():
            st.markdown(f'<div class="filter-section">', unsafe_allow_html=True)
            st.markdown(f'<div class="filter-label">{filter_name}</div>', unsafe_allow_html=True)
            
            if isinstance(filter_options, dict):
                # Handle different filter types
                filter_type = filter_options.get('type', 'multiselect')
                options = filter_options.get('options', [])
                default = filter_options.get('default', None)
                
                if filter_type == 'multiselect':
                    selected_filters[filter_name] = st.multiselect(
                        filter_name,
                        options,
                        default=default,
                        key=f"{key_prefix}_{filter_name}",
                        label_visibility="collapsed"
                    )
                elif filter_type == 'select':
                    selected_filters[filter_name] = st.selectbox(
                        filter_name,
                        options,
                        index=options.index(default) if default and default in options else 0,
                        key=f"{key_prefix}_{filter_name}",
                        label_visibility="collapsed"
                    )
                elif filter_type == 'slider':
                    min_val = filter_options.get('min', 0)
                    max_val = filter_options.get('max', 100)
                    selected_filters[filter_name] = st.slider(
                        filter_name,
                        min_val,
                        max_val,
                        (min_val, max_val),
                        key=f"{key_prefix}_{filter_name}",
                        label_visibility="collapsed"
                    )
                elif filter_type == 'checkbox':
                    selected_filters[filter_name] = st.checkbox(
                        filter_name,
                        value=default or False,
                        key=f"{key_prefix}_{filter_name}",
                        label_visibility="collapsed"
                    )
            else:
                # Simple list of options (multiselect)
                selected_filters[filter_name] = st.multiselect(
                    filter_name,
                    filter_options,
                    key=f"{key_prefix}_{filter_name}",
                    label_visibility="collapsed"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Reset filters button
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Reset Filters", key=f"{key_prefix}_reset"):
                st.rerun()
        with col2:
            if st.button("Apply Filters", key=f"{key_prefix}_apply", type="primary"):
                pass  # Filters are already applied
        
        return selected_filters


def sort_selector(options, default=None, key=None):
    """
    Display a sort selector
    
    Args:
        options: Dict of {display_name: value}
        default: Default sort option
        key: Unique key
        
    Returns:
        Selected sort value
    """
    colors = get_theme_colors()
    
    st.markdown(f"""
    <style>
        .sort-container {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem;
            background: var(--card-secondary);
            border-radius: 8px;
        }}
        
        .sort-label {{
            color: var(--text-tertiary);
            font-size: 0.9rem;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sort-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown('<span class="sort-label">Sort by:</span>', unsafe_allow_html=True)
    with col2:
        selected = st.selectbox(
            "Sort",
            options=list(options.keys()),
            index=list(options.keys()).index(default) if default in options.keys() else 0,
            key=key,
            label_visibility="collapsed"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return options[selected]


def quick_filters(filters, key_prefix="quick"):
    """
    Display quick filter buttons
    
    Args:
        filters: List of filter names
        key_prefix: Prefix for keys
        
    Returns:
        Selected filter
    """
    colors = get_theme_colors()
    
    st.markdown("""
    <style>
        .quick-filter-btn {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            border: 2px solid var(--border);
            background: var(--card-primary);
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s ease;
            margin: 0.25rem;
        }
        
        .quick-filter-btn:hover {
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }
        
        .quick-filter-btn.active {
            background: var(--accent-primary);
            color: white;
            border-color: var(--accent-primary);
        }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(filters))
    selected = None
    
    for idx, filter_name in enumerate(filters):
        with cols[idx]:
            if st.button(filter_name, key=f"{key_prefix}_{filter_name}"):
                selected = filter_name
    
    return selected


def range_slider(label, min_val, max_val, default_range=None, key=None):
    """
    Display a styled range slider
    
    Args:
        label: Slider label
        min_val: Minimum value
        max_val: Maximum value
        default_range: Default range (tuple)
        key: Unique key
        
    Returns:
        tuple: Selected range
    """
    if default_range is None:
        default_range = (min_val, max_val)
    
    st.markdown(f"""
    <style>
        .range-label {{
            color: var(--text-primary);
            font-weight: 500;
            margin-bottom: 0.5rem;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="range-label">{label}</div>', unsafe_allow_html=True)
    
    return st.slider(
        label,
        min_val,
        max_val,
        default_range,
        key=key,
        label_visibility="collapsed"
    )
