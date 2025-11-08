"""
Modern Design System - Color schemes and design tokens for the job scraper dashboard.
This module provides a comprehensive design system with professional color palettes,
typography scales, spacing system, and theme configurations.
"""

# ============================================================================
# COLOR PALETTE - Modern SaaS Design
# ============================================================================

LIGHT_THEME = {
    # Primary Colors - Professional Blues
    'primary': {
        '50': '#eff6ff',
        '100': '#dbeafe',
        '200': '#bfdbfe',
        '300': '#93c5fd',
        '400': '#60a5fa',
        '500': '#3b82f6',  # Main primary
        '600': '#2563eb',
        '700': '#1d4ed8',
        '800': '#1e40af',
        '900': '#1e3a8a',
    },
    
    # Secondary Colors - Purple Accent
    'secondary': {
        '50': '#faf5ff',
        '100': '#f3e8ff',
        '200': '#e9d5ff',
        '300': '#d8b4fe',
        '400': '#c084fc',
        '500': '#a855f7',  # Main secondary
        '600': '#9333ea',
        '700': '#7e22ce',
        '800': '#6b21a8',
        '900': '#581c87',
    },
    
    # Neutral Colors - Grays
    'neutral': {
        '50': '#fafafa',
        '100': '#f4f4f5',
        '200': '#e4e4e7',
        '300': '#d4d4d8',
        '400': '#a1a1aa',
        '500': '#71717a',
        '600': '#52525b',
        '700': '#3f3f46',
        '800': '#27272a',
        '900': '#18181b',
    },
    
    # Semantic Colors
    'success': {
        'light': '#d1fae5',
        'main': '#10b981',
        'dark': '#059669',
    },
    'warning': {
        'light': '#fef3c7',
        'main': '#f59e0b',
        'dark': '#d97706',
    },
    'error': {
        'light': '#fee2e2',
        'main': '#ef4444',
        'dark': '#dc2626',
    },
    'info': {
        'light': '#dbeafe',
        'main': '#3b82f6',
        'dark': '#2563eb',
    },
    
    # Background Colors
    'background': {
        'default': '#fafbfc',
        'paper': '#ffffff',
        'elevated': '#ffffff',
        'overlay': 'rgba(0, 0, 0, 0.5)',
    },
    
    # Text Colors
    'text': {
        'primary': '#1f2937',
        'secondary': '#4b5563',
        'tertiary': '#6b7280',
        'disabled': '#9ca3af',
        'inverse': '#ffffff',
    },
    
    # Border Colors
    'border': {
        'light': '#f3f4f6',
        'main': '#e5e7eb',
        'dark': '#d1d5db',
    },
    
    # Shadow Colors
    'shadow': {
        'sm': 'rgba(0, 0, 0, 0.05)',
        'md': 'rgba(0, 0, 0, 0.1)',
        'lg': 'rgba(0, 0, 0, 0.15)',
        'xl': 'rgba(0, 0, 0, 0.2)',
    },
}

DARK_THEME = {
    # Primary Colors - Softer Blues for Dark Mode
    'primary': {
        '50': '#1e3a8a',
        '100': '#1e40af',
        '200': '#1d4ed8',
        '300': '#2563eb',
        '400': '#3b82f6',
        '500': '#60a5fa',  # Main primary
        '600': '#93c5fd',
        '700': '#bfdbfe',
        '800': '#dbeafe',
        '900': '#eff6ff',
    },
    
    # Secondary Colors - Purple Accent
    'secondary': {
        '50': '#581c87',
        '100': '#6b21a8',
        '200': '#7e22ce',
        '300': '#9333ea',
        '400': '#a855f7',
        '500': '#c084fc',  # Main secondary
        '600': '#d8b4fe',
        '700': '#e9d5ff',
        '800': '#f3e8ff',
        '900': '#faf5ff',
    },
    
    # Neutral Colors - Dark Grays
    'neutral': {
        '50': '#18181b',
        '100': '#27272a',
        '200': '#3f3f46',
        '300': '#52525b',
        '400': '#71717a',
        '500': '#a1a1aa',
        '600': '#d4d4d8',
        '700': '#e4e4e7',
        '800': '#f4f4f5',
        '900': '#fafafa',
    },
    
    # Semantic Colors - Adjusted for Dark Mode
    'success': {
        'light': '#064e3b',
        'main': '#34d399',
        'dark': '#6ee7b7',
    },
    'warning': {
        'light': '#78350f',
        'main': '#fbbf24',
        'dark': '#fcd34d',
    },
    'error': {
        'light': '#7f1d1d',
        'main': '#f87171',
        'dark': '#fca5a5',
    },
    'info': {
        'light': '#1e3a8a',
        'main': '#60a5fa',
        'dark': '#93c5fd',
    },
    
    # Background Colors
    'background': {
        'default': '#0f172a',
        'paper': '#1e293b',
        'elevated': '#334155',
        'overlay': 'rgba(0, 0, 0, 0.7)',
    },
    
    # Text Colors
    'text': {
        'primary': '#f1f5f9',
        'secondary': '#cbd5e1',
        'tertiary': '#94a3b8',
        'disabled': '#64748b',
        'inverse': '#1f2937',
    },
    
    # Border Colors
    'border': {
        'light': '#1e293b',
        'main': '#334155',
        'dark': '#475569',
    },
    
    # Shadow Colors
    'shadow': {
        'sm': 'rgba(0, 0, 0, 0.2)',
        'md': 'rgba(0, 0, 0, 0.3)',
        'lg': 'rgba(0, 0, 0, 0.4)',
        'xl': 'rgba(0, 0, 0, 0.5)',
    },
}

# ============================================================================
# TYPOGRAPHY SCALE
# ============================================================================

TYPOGRAPHY = {
    'font_family': {
        'sans': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        'mono': 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace',
    },
    'font_size': {
        'xs': '0.75rem',      # 12px
        'sm': '0.875rem',     # 14px
        'base': '1rem',       # 16px
        'lg': '1.125rem',     # 18px
        'xl': '1.25rem',      # 20px
        '2xl': '1.5rem',      # 24px
        '3xl': '1.875rem',    # 30px
        '4xl': '2.25rem',     # 36px
        '5xl': '3rem',        # 48px
    },
    'font_weight': {
        'light': '300',
        'normal': '400',
        'medium': '500',
        'semibold': '600',
        'bold': '700',
        'extrabold': '800',
    },
    'line_height': {
        'tight': '1.25',
        'normal': '1.5',
        'relaxed': '1.75',
    },
    'letter_spacing': {
        'tight': '-0.025em',
        'normal': '0',
        'wide': '0.025em',
    },
}

# ============================================================================
# SPACING SYSTEM (8px base)
# ============================================================================

SPACING = {
    '0': '0',
    '1': '0.25rem',   # 4px
    '2': '0.5rem',    # 8px
    '3': '0.75rem',   # 12px
    '4': '1rem',      # 16px
    '5': '1.25rem',   # 20px
    '6': '1.5rem',    # 24px
    '8': '2rem',      # 32px
    '10': '2.5rem',   # 40px
    '12': '3rem',     # 48px
    '16': '4rem',     # 64px
    '20': '5rem',     # 80px
    '24': '6rem',     # 96px
}

# ============================================================================
# BORDER RADIUS
# ============================================================================

BORDER_RADIUS = {
    'none': '0',
    'sm': '0.25rem',   # 4px
    'base': '0.5rem',  # 8px
    'md': '0.75rem',   # 12px
    'lg': '1rem',      # 16px
    'xl': '1.5rem',    # 24px
    '2xl': '2rem',     # 32px
    'full': '9999px',
}

# ============================================================================
# SHADOWS
# ============================================================================

SHADOWS = {
    'light': {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'base': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    },
    'dark': {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
        'base': '0 1px 3px 0 rgba(0, 0, 0, 0.4), 0 1px 2px 0 rgba(0, 0, 0, 0.3)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.4)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.6)',
    },
}

# ============================================================================
# TRANSITIONS
# ============================================================================

TRANSITIONS = {
    'duration': {
        'fast': '150ms',
        'normal': '300ms',
        'slow': '500ms',
    },
    'timing': {
        'ease': 'ease',
        'ease-in': 'ease-in',
        'ease-out': 'ease-out',
        'ease-in-out': 'ease-in-out',
    },
}

# ============================================================================
# BREAKPOINTS (Responsive Design)
# ============================================================================

BREAKPOINTS = {
    'xs': '480px',
    'sm': '640px',
    'md': '768px',
    'lg': '1024px',
    'xl': '1280px',
    '2xl': '1536px',
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_theme(mode='light'):
    """
    Get theme colors for the specified mode.
    
    Args:
        mode (str): Theme mode - 'light' or 'dark'
        
    Returns:
        dict: Theme color palette
    """
    return DARK_THEME if mode == 'dark' else LIGHT_THEME


def get_color(theme, category, shade='500'):
    """
    Get a specific color from the theme.
    
    Args:
        theme (dict): Theme dictionary
        category (str): Color category (e.g., 'primary', 'neutral')
        shade (str): Color shade (e.g., '500', 'main')
        
    Returns:
        str: Color hex code
    """
    # Determine theme-appropriate fallback
    fallback = '#1f2937' if theme.get('background', {}).get('default', '#ffffff').startswith('#fa') else '#f1f5f9'
    
    if category in theme and isinstance(theme[category], dict):
        return theme[category].get(shade, theme[category].get('main', fallback))
    return fallback


def get_gradient(theme, colors=['primary', 'secondary'], direction='135deg'):
    """
    Generate a gradient CSS string.
    
    Args:
        theme (dict): Theme dictionary
        colors (list): List of color categories
        direction (str): Gradient direction
        
    Returns:
        str: CSS gradient string
    """
    color_values = [get_color(theme, color, '500') for color in colors]
    return f"linear-gradient({direction}, {', '.join(color_values)})"


def get_shadow(mode='light', size='md'):
    """
    Get shadow CSS for the specified mode and size.
    
    Args:
        mode (str): Theme mode - 'light' or 'dark'
        size (str): Shadow size - 'sm', 'base', 'md', 'lg', 'xl', '2xl'
        
    Returns:
        str: CSS shadow string
    """
    shadows = SHADOWS['dark'] if mode == 'dark' else SHADOWS['light']
    return shadows.get(size, shadows['base'])


def create_design_tokens(mode='light'):
    """
    Create a comprehensive design token dictionary for CSS variables.
    
    Args:
        mode (str): Theme mode - 'light' or 'dark'
        
    Returns:
        dict: Design tokens
    """
    theme = get_theme(mode)
    
    return {
        # Colors
        '--color-primary': get_color(theme, 'primary', '500'),
        '--color-primary-light': get_color(theme, 'primary', '400'),
        '--color-primary-dark': get_color(theme, 'primary', '600'),
        
        '--color-secondary': get_color(theme, 'secondary', '500'),
        '--color-secondary-light': get_color(theme, 'secondary', '400'),
        '--color-secondary-dark': get_color(theme, 'secondary', '600'),
        
        '--color-success': theme['success']['main'],
        '--color-warning': theme['warning']['main'],
        '--color-error': theme['error']['main'],
        '--color-info': theme['info']['main'],
        
        '--color-bg-default': theme['background']['default'],
        '--color-bg-paper': theme['background']['paper'],
        '--color-bg-elevated': theme['background']['elevated'],
        '--color-bg-overlay': theme['background']['overlay'],
        
        '--color-text-primary': theme['text']['primary'],
        '--color-text-secondary': theme['text']['secondary'],
        '--color-text-tertiary': theme['text']['tertiary'],
        '--color-text-disabled': theme['text']['disabled'],
        
        '--color-border': theme['border']['main'],
        '--color-border-light': theme['border']['light'],
        '--color-border-dark': theme['border']['dark'],
        
        # Typography
        '--font-sans': TYPOGRAPHY['font_family']['sans'],
        '--font-mono': TYPOGRAPHY['font_family']['mono'],
        
        '--text-xs': TYPOGRAPHY['font_size']['xs'],
        '--text-sm': TYPOGRAPHY['font_size']['sm'],
        '--text-base': TYPOGRAPHY['font_size']['base'],
        '--text-lg': TYPOGRAPHY['font_size']['lg'],
        '--text-xl': TYPOGRAPHY['font_size']['xl'],
        '--text-2xl': TYPOGRAPHY['font_size']['2xl'],
        '--text-3xl': TYPOGRAPHY['font_size']['3xl'],
        '--text-4xl': TYPOGRAPHY['font_size']['4xl'],
        
        '--font-normal': TYPOGRAPHY['font_weight']['normal'],
        '--font-medium': TYPOGRAPHY['font_weight']['medium'],
        '--font-semibold': TYPOGRAPHY['font_weight']['semibold'],
        '--font-bold': TYPOGRAPHY['font_weight']['bold'],
        
        # Spacing
        '--space-1': SPACING['1'],
        '--space-2': SPACING['2'],
        '--space-3': SPACING['3'],
        '--space-4': SPACING['4'],
        '--space-6': SPACING['6'],
        '--space-8': SPACING['8'],
        
        # Border Radius
        '--radius-sm': BORDER_RADIUS['sm'],
        '--radius-base': BORDER_RADIUS['base'],
        '--radius-md': BORDER_RADIUS['md'],
        '--radius-lg': BORDER_RADIUS['lg'],
        '--radius-xl': BORDER_RADIUS['xl'],
        '--radius-full': BORDER_RADIUS['full'],
        
        # Shadows
        '--shadow-sm': get_shadow(mode, 'sm'),
        '--shadow-base': get_shadow(mode, 'base'),
        '--shadow-md': get_shadow(mode, 'md'),
        '--shadow-lg': get_shadow(mode, 'lg'),
        '--shadow-xl': get_shadow(mode, 'xl'),
        
        # Transitions
        '--transition-fast': f"{TRANSITIONS['duration']['fast']} {TRANSITIONS['timing']['ease-out']}",
        '--transition-normal': f"{TRANSITIONS['duration']['normal']} {TRANSITIONS['timing']['ease-in-out']}",
        '--transition-slow': f"{TRANSITIONS['duration']['slow']} {TRANSITIONS['timing']['ease-in-out']}",
    }
