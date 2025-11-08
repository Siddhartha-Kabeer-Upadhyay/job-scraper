"""
Theme management for the dashboard
Handles dark/light mode switching and theme persistence
"""

import streamlit as st


def init_theme():
    """Initialize theme in session state"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'


def get_theme():
    """Get current theme"""
    init_theme()
    return st.session_state.theme


def toggle_theme():
    """Toggle between dark and light theme"""
    init_theme()
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'


def is_dark_mode():
    """Check if dark mode is active"""
    return get_theme() == 'dark'


def get_theme_colors():
    """
    Get color palette based on current theme
    
    Returns:
        dict: Color palette with the following keys:
            - background_primary: Main background color
            - background_secondary: Secondary background color
            - card_primary: Primary card background
            - card_secondary: Secondary card background
            - card_elevated: Elevated card background
            - text_primary: Primary text color
            - text_secondary: Secondary text color
            - text_tertiary: Tertiary/muted text color
            - accent_primary: Primary accent color
            - accent_secondary: Secondary accent color
            - success: Success state color
            - warning: Warning state color
            - error: Error state color
            - info: Info state color
            - border: Border color
            - shadow: Shadow color (with alpha)
    """
    if is_dark_mode():
        return {
            'background_primary': '#0e1117',
            'background_secondary': '#1a1d24',
            'card_primary': '#262730',
            'card_secondary': '#2e2e38',
            'card_elevated': '#363844',
            'text_primary': '#fafafa',
            'text_secondary': '#cbd5e1',
            'text_tertiary': '#94a3b8',
            'accent_primary': '#8b9dff',
            'accent_secondary': '#a29dff',
            'success': '#34d399',
            'warning': '#fbbf24',
            'error': '#f87171',
            'info': '#60a5fa',
            'border': '#404252',
            'shadow': 'rgba(0, 0, 0, 0.3)',
        }
    else:
        return {
            'background_primary': '#fafbfc',
            'background_secondary': '#ffffff',
            'card_primary': '#ffffff',
            'card_secondary': '#f8f9fa',
            'card_elevated': '#ffffff',
            'text_primary': '#1e293b',
            'text_secondary': '#475569',
            'text_tertiary': '#64748b',
            'accent_primary': '#667eea',
            'accent_secondary': '#764ba2',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'info': '#3b82f6',
            'border': '#e2e8f0',
            'shadow': 'rgba(0, 0, 0, 0.1)',
        }


def get_chart_colors():
    """
    Get chart color palette based on current theme
    
    Returns:
        list: List of colors suitable for charts
    """
    if is_dark_mode():
        return [
            '#8b9dff', '#a29dff', '#34d399', '#fbbf24', '#f87171',
            '#60a5fa', '#c084fc', '#fb923c', '#4ade80', '#38bdf8',
            '#a78bfa', '#fb7185', '#fcd34d', '#86efac', '#7dd3fc'
        ]
    else:
        return [
            '#667eea', '#764ba2', '#10b981', '#f59e0b', '#ef4444',
            '#3b82f6', '#a855f7', '#f97316', '#22c55e', '#0ea5e9',
            '#8b5cf6', '#ec4899', '#eab308', '#16a34a', '#0284c7'
        ]


def get_gradient_colors():
    """
    Get gradient color combinations based on theme
    
    Returns:
        dict: Dictionary of gradient combinations
    """
    if is_dark_mode():
        return {
            'primary': ['#8b9dff', '#a29dff'],
            'success': ['#059669', '#34d399'],
            'warning': ['#d97706', '#fbbf24'],
            'purple': ['#7c3aed', '#a78bfa'],
            'blue': ['#2563eb', '#60a5fa'],
        }
    else:
        return {
            'primary': ['#667eea', '#764ba2'],
            'success': ['#059669', '#10b981'],
            'warning': ['#d97706', '#f59e0b'],
            'purple': ['#7c3aed', '#a855f7'],
            'blue': ['#2563eb', '#3b82f6'],
        }
