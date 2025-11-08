"""
Styles and CSS for the dashboard
Includes glassmorphism, neumorphism, and modern UI components
"""

from components.theme import get_theme_colors, is_dark_mode


def get_base_styles():
    """Get base CSS styles with theme support"""
    colors = get_theme_colors()
    dark = is_dark_mode()
    
    return f"""
    <style>
        /* CSS Variables for theming */
        :root {{
            --bg-primary: {colors['background_primary']};
            --bg-secondary: {colors['background_secondary']};
            --card-primary: {colors['card_primary']};
            --card-secondary: {colors['card_secondary']};
            --card-elevated: {colors['card_elevated']};
            --text-primary: {colors['text_primary']};
            --text-secondary: {colors['text_secondary']};
            --text-tertiary: {colors['text_tertiary']};
            --accent-primary: {colors['accent_primary']};
            --accent-secondary: {colors['accent_secondary']};
            --success: {colors['success']};
            --warning: {colors['warning']};
            --error: {colors['error']};
            --info: {colors['info']};
            --border: {colors['border']};
            --shadow: {colors['shadow']};
        }}
        
        /* Global styles */
        .stApp {{
            background: var(--bg-primary);
            transition: background 0.3s ease;
        }}
        
        /* Remove default padding */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-primary) !important;
            font-weight: 600 !important;
        }}
        
        p, span, div {{
            color: var(--text-secondary) !important;
        }}
        
        /* Smooth transitions */
        * {{
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
    </style>
    """


def get_glassmorphism_style():
    """Get glassmorphism card styles"""
    colors = get_theme_colors()
    
    return f"""
    <style>
        .glass-card {{
            background: rgba(255, 255, 255, {'0.05' if is_dark_mode() else '0.7'});
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, {'0.1' if is_dark_mode() else '0.2'});
            padding: 1.5rem;
            box-shadow: 0 8px 32px 0 {colors['shadow']};
            transition: all 0.3s ease;
        }}
        
        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 40px 0 {colors['shadow']};
        }}
        
        .glass-metric {{
            background: rgba(255, 255, 255, {'0.03' if is_dark_mode() else '0.5'});
            backdrop-filter: blur(8px);
            border-radius: 12px;
            padding: 1.2rem;
            border: 1px solid rgba(255, 255, 255, {'0.08' if is_dark_mode() else '0.15'});
            text-align: center;
        }}
        
        .glass-metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-primary);
            margin: 0.5rem 0;
        }}
        
        .glass-metric-label {{
            font-size: 0.9rem;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
    </style>
    """


def get_card_styles():
    """Get modern card styles with elevation levels"""
    colors = get_theme_colors()
    
    return f"""
    <style>
        .modern-card {{
            background: var(--card-primary);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid var(--border);
            transition: all 0.3s ease;
        }}
        
        .modern-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px {colors['shadow']};
            border-color: var(--accent-primary);
        }}
        
        .card-elevated {{
            background: var(--card-elevated);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 20px {colors['shadow']};
            transition: all 0.3s ease;
        }}
        
        .card-flat {{
            background: var(--card-secondary);
            border-radius: 8px;
            padding: 1rem;
            border: none;
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--border);
        }}
        
        .card-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }}
        
        .card-subtitle {{
            font-size: 0.875rem;
            color: var(--text-tertiary);
            margin-top: 0.25rem;
        }}
        
        .card-body {{
            padding: 0.5rem 0;
        }}
        
        .card-footer {{
            margin-top: 1rem;
            padding-top: 0.75rem;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
    </style>
    """


def get_neumorphism_styles():
    """Get neumorphism button and input styles"""
    colors = get_theme_colors()
    
    shadow_light = 'rgba(255, 255, 255, 0.1)' if is_dark_mode() else 'rgba(255, 255, 255, 0.9)'
    shadow_dark = 'rgba(0, 0, 0, 0.3)' if is_dark_mode() else 'rgba(0, 0, 0, 0.1)'
    
    return f"""
    <style>
        .neuro-button {{
            background: var(--card-primary);
            border: none;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            cursor: pointer;
            box-shadow: 6px 6px 12px {shadow_dark},
                       -6px -6px 12px {shadow_light};
            transition: all 0.2s ease;
        }}
        
        .neuro-button:hover {{
            box-shadow: 4px 4px 8px {shadow_dark},
                       -4px -4px 8px {shadow_light};
        }}
        
        .neuro-button:active {{
            box-shadow: inset 4px 4px 8px {shadow_dark},
                       inset -4px -4px 8px {shadow_light};
        }}
        
        .neuro-input {{
            background: var(--card-primary);
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            color: var(--text-primary);
            box-shadow: inset 4px 4px 8px {shadow_dark},
                       inset -4px -4px 8px {shadow_light};
        }}
        
        .neuro-input:focus {{
            outline: none;
            box-shadow: inset 3px 3px 6px {shadow_dark},
                       inset -3px -3px 6px {shadow_light},
                       0 0 0 2px var(--accent-primary);
        }}
    </style>
    """


def get_hero_styles():
    """Get hero section styles with gradient background"""
    colors = get_theme_colors()
    
    gradient = f"linear-gradient(135deg, {colors['accent_primary']} 0%, {colors['accent_secondary']} 100%)"
    
    return f"""
    <style>
        .hero-section {{
            background: {gradient};
            border-radius: 20px;
            padding: 3rem 2rem;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 40px {colors['shadow']};
        }}
        
        .hero-section::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                       radial-gradient(circle at 70% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
            pointer-events: none;
        }}
        
        .hero-content {{
            position: relative;
            z-index: 1;
        }}
        
        .hero-title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: white !important;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }}
        
        .hero-subtitle {{
            font-size: 1.1rem;
            color: rgba(255, 255, 255, 0.9) !important;
            margin-bottom: 2rem;
        }}
        
        .hero-metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }}
    </style>
    """


def get_animation_styles():
    """Get animation and transition styles"""
    return """
    <style>
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }
        
        @keyframes shimmer {
            0% {
                background-position: -1000px 0;
            }
            100% {
                background-position: 1000px 0;
            }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        
        .slide-in {
            animation: slideIn 0.5s ease-out;
        }
        
        .pulse {
            animation: pulse 2s ease-in-out infinite;
        }
        
        .skeleton {
            background: linear-gradient(90deg, 
                        var(--card-secondary) 0%, 
                        var(--card-elevated) 50%, 
                        var(--card-secondary) 100%);
            background-size: 1000px 100%;
            animation: shimmer 2s infinite;
            border-radius: 8px;
        }
        
        .loading-bar {
            height: 4px;
            background: linear-gradient(90deg, 
                        var(--accent-primary) 0%, 
                        var(--accent-secondary) 100%);
            border-radius: 2px;
            position: relative;
            overflow: hidden;
        }
        
        .loading-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            background: linear-gradient(90deg, 
                        transparent 0%, 
                        rgba(255, 255, 255, 0.3) 50%, 
                        transparent 100%);
            animation: shimmer 1.5s infinite;
        }
    </style>
    """


def get_badge_styles():
    """Get badge and chip styles"""
    return """
    <style>
        .badge {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 500;
            margin: 0.25rem;
            transition: all 0.2s ease;
        }
        
        .badge:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px var(--shadow);
        }
        
        .badge-primary {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
        }
        
        .badge-success {
            background: var(--success);
            color: white;
        }
        
        .badge-warning {
            background: var(--warning);
            color: white;
        }
        
        .badge-info {
            background: var(--info);
            color: white;
        }
        
        .badge-outline {
            background: transparent;
            border: 2px solid var(--accent-primary);
            color: var(--accent-primary);
        }
        
        .chip {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            background: var(--card-secondary);
            border: 1px solid var(--border);
            font-size: 0.9rem;
            margin: 0.25rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .chip:hover {
            background: var(--card-elevated);
            border-color: var(--accent-primary);
            transform: translateY(-1px);
        }
        
        .chip.active {
            background: var(--accent-primary);
            color: white;
            border-color: var(--accent-primary);
        }
    </style>
    """


def get_responsive_styles():
    """Get responsive design styles"""
    return """
    <style>
        /* Grid system */
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
        }
        
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }
        
        .grid-4 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
        }
        
        /* Responsive breakpoints */
        @media (max-width: 1200px) {
            .grid-4 {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .grid-2, .grid-3, .grid-4 {
                grid-template-columns: 1fr;
            }
            
            .hero-title {
                font-size: 2rem !important;
            }
            
            .hero-subtitle {
                font-size: 1rem !important;
            }
        }
        
        /* Flexbox utilities */
        .flex {
            display: flex;
        }
        
        .flex-col {
            flex-direction: column;
        }
        
        .items-center {
            align-items: center;
        }
        
        .justify-between {
            justify-content: space-between;
        }
        
        .justify-center {
            justify-content: center;
        }
        
        .gap-1 {
            gap: 0.5rem;
        }
        
        .gap-2 {
            gap: 1rem;
        }
        
        .gap-3 {
            gap: 1.5rem;
        }
    </style>
    """


def get_all_styles():
    """Get all styles combined"""
    return (
        get_base_styles() +
        get_glassmorphism_style() +
        get_card_styles() +
        get_neumorphism_styles() +
        get_hero_styles() +
        get_animation_styles() +
        get_badge_styles() +
        get_responsive_styles()
    )
