"""
Chart utilities with dark mode support
"""

import plotly.graph_objects as go
import plotly.express as px
from components.theme import get_theme_colors, get_chart_colors, get_gradient_colors, is_dark_mode


def get_chart_layout(title=None, height=None):
    """
    Get base chart layout with theme support
    
    Args:
        title: Chart title
        height: Chart height
        
    Returns:
        dict: Layout configuration
    """
    colors = get_theme_colors()
    dark = is_dark_mode()
    
    layout = {
        'paper_bgcolor': colors['background_secondary'],
        'plot_bgcolor': colors['card_primary'],
        'font': {
            'color': colors['text_primary'],
            'family': 'Inter, system-ui, sans-serif'
        },
        'title': {
            'text': title,
            'font': {
                'size': 18,
                'color': colors['text_primary'],
                'family': 'Inter, system-ui, sans-serif'
            },
            'x': 0.5,
            'xanchor': 'center'
        } if title else None,
        'xaxis': {
            'gridcolor': colors['border'],
            'linecolor': colors['border'],
            'tickfont': {'color': colors['text_secondary']}
        },
        'yaxis': {
            'gridcolor': colors['border'],
            'linecolor': colors['border'],
            'tickfont': {'color': colors['text_secondary']}
        },
        'legend': {
            'font': {'color': colors['text_secondary']},
            'bgcolor': 'rgba(0,0,0,0)',
        },
        'margin': dict(l=40, r=40, t=60, b=40),
    }
    
    if height:
        layout['height'] = height
    
    return layout


def create_bar_chart(data, x, y, title=None, color=None, orientation='v', height=400):
    """
    Create a themed bar chart
    
    Args:
        data: DataFrame with data
        x: X-axis column
        y: Y-axis column
        title: Chart title
        color: Column for color grouping
        orientation: 'v' for vertical, 'h' for horizontal
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colors = get_chart_colors()
    
    fig = px.bar(
        data,
        x=x if orientation == 'v' else y,
        y=y if orientation == 'v' else x,
        color=color,
        orientation=orientation,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(**get_chart_layout(title, height))
    
    # Add gradient fill
    if not color:
        gradient_colors = get_gradient_colors()['primary']
        fig.update_traces(
            marker=dict(
                color=gradient_colors[0],
                line=dict(color=gradient_colors[1], width=1)
            )
        )
    
    return fig


def create_line_chart(data, x, y, title=None, color=None, height=400):
    """
    Create a themed line chart
    
    Args:
        data: DataFrame with data
        x: X-axis column
        y: Y-axis column
        title: Chart title
        color: Column for color grouping
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colors = get_chart_colors()
    
    fig = px.line(
        data,
        x=x,
        y=y,
        color=color,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(**get_chart_layout(title, height))
    
    # Add gradient fill under line with proper rgba color
    accent_color = get_theme_colors()['accent_primary']
    # Convert hex to rgba for fill (with low opacity)
    if accent_color.startswith('#'):
        # Simple approach: use the accent color with opacity
        fill_color = f"{accent_color}20"  # Add 20 for ~12% opacity in hex
    else:
        fill_color = 'rgba(102, 126, 234, 0.1)'
    
    fig.update_traces(
        fill='tozeroy',
        fillcolor=fill_color if not is_dark_mode() else f"{get_theme_colors()['accent_primary']}20",
        line=dict(width=3)
    )
    
    return fig


def create_pie_chart(data, values, names, title=None, hole=0.4, height=400):
    """
    Create a themed donut/pie chart
    
    Args:
        data: DataFrame with data
        values: Values column
        names: Names column
        title: Chart title
        hole: Hole size (0 for pie, >0 for donut)
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colors = get_chart_colors()
    
    fig = px.pie(
        data,
        values=values,
        names=names,
        hole=hole,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(**get_chart_layout(title, height))
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(color='white'),
        marker=dict(line=dict(color=get_theme_colors()['border'], width=2))
    )
    
    return fig


def create_scatter_chart(data, x, y, title=None, color=None, size=None, height=400):
    """
    Create a themed scatter plot
    
    Args:
        data: DataFrame with data
        x: X-axis column
        y: Y-axis column
        title: Chart title
        color: Column for color grouping
        size: Column for bubble size
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colors = get_chart_colors()
    
    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        size=size,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(**get_chart_layout(title, height))
    
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color=get_theme_colors()['border']),
            opacity=0.8
        )
    )
    
    return fig


def create_heatmap(data, x, y, z, title=None, height=400):
    """
    Create a themed heatmap
    
    Args:
        data: DataFrame with data
        x: X-axis column
        y: Y-axis column
        z: Values for heatmap
        title: Chart title
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colorscale = 'Viridis' if is_dark_mode() else 'Blues'
    
    fig = px.density_heatmap(
        data,
        x=x,
        y=y,
        z=z,
        color_continuous_scale=colorscale
    )
    
    fig.update_layout(**get_chart_layout(title, height))
    
    return fig


def create_sparkline(values, color=None, height=50, width=100):
    """
    Create a mini sparkline chart
    
    Args:
        values: List of values
        color: Line color
        height: Chart height
        width: Chart width
        
    Returns:
        Plotly figure
    """
    theme_colors = get_theme_colors()
    if not color:
        color = theme_colors['accent_primary']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=values,
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba({color}, 0.2)',
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        margin=dict(l=0, r=0, t=0, b=0),
        height=height,
        width=width,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_gauge_chart(value, max_value, title=None, height=300):
    """
    Create a themed gauge chart
    
    Args:
        value: Current value
        max_value: Maximum value
        title: Chart title
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colors = get_theme_colors()
    gradient = get_gradient_colors()['primary']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'color': colors['text_primary']}},
        gauge={
            'axis': {'range': [None, max_value], 'tickcolor': colors['text_tertiary']},
            'bar': {'color': gradient[0]},
            'bgcolor': colors['card_secondary'],
            'borderwidth': 2,
            'bordercolor': colors['border'],
            'steps': [
                {'range': [0, max_value * 0.33], 'color': colors['card_elevated']},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': colors['card_primary']},
                {'range': [max_value * 0.66, max_value], 'color': colors['card_secondary']}
            ],
            'threshold': {
                'line': {'color': colors['error'], 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor=colors['background_secondary'],
        font={'color': colors['text_primary']},
        height=height
    )
    
    return fig


def create_treemap(data, path, values, title=None, height=400):
    """
    Create a themed treemap
    
    Args:
        data: DataFrame with data
        path: Hierarchical path columns
        values: Values column
        title: Chart title
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colors = get_chart_colors()
    
    fig = px.treemap(
        data,
        path=path,
        values=values,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(**get_chart_layout(title, height))
    
    fig.update_traces(
        textfont=dict(color='white', size=14),
        marker=dict(line=dict(color=get_theme_colors()['border'], width=2))
    )
    
    return fig


def create_funnel_chart(data, x, y, title=None, height=400):
    """
    Create a themed funnel chart
    
    Args:
        data: DataFrame with data
        x: X-axis column (values)
        y: Y-axis column (stages)
        title: Chart title
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colors = get_chart_colors()
    
    fig = px.funnel(
        data,
        x=x,
        y=y,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(**get_chart_layout(title, height))
    
    return fig


def create_timeline_chart(data, x_start, x_end, y, title=None, color=None, height=400):
    """
    Create a timeline/gantt chart
    
    Args:
        data: DataFrame with data
        x_start: Start time column
        x_end: End time column
        y: Category column
        title: Chart title
        color: Column for color grouping
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colors = get_chart_colors()
    
    fig = px.timeline(
        data,
        x_start=x_start,
        x_end=x_end,
        y=y,
        color=color,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(**get_chart_layout(title, height))
    
    return fig


def create_bubble_chart(data, x, y, size, title=None, color=None, height=400):
    """
    Create an interactive bubble chart
    
    Args:
        data: DataFrame with data
        x: X-axis column
        y: Y-axis column
        size: Bubble size column
        title: Chart title
        color: Column for color grouping
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colors = get_chart_colors()
    
    fig = px.scatter(
        data,
        x=x,
        y=y,
        size=size,
        color=color,
        color_discrete_sequence=colors,
        size_max=60
    )
    
    fig.update_layout(**get_chart_layout(title, height))
    
    fig.update_traces(
        marker=dict(
            line=dict(width=2, color=get_theme_colors()['border']),
            opacity=0.7
        )
    )
    
    return fig


def create_sunburst_chart(data, path, values, title=None, height=400):
    """
    Create a sunburst chart for hierarchical data
    
    Args:
        data: DataFrame with data
        path: Hierarchical path columns
        values: Values column
        title: Chart title
        height: Chart height
        
    Returns:
        Plotly figure
    """
    colors = get_chart_colors()
    
    fig = px.sunburst(
        data,
        path=path,
        values=values,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(**get_chart_layout(title, height))
    
    fig.update_traces(
        textfont=dict(color='white'),
        marker=dict(line=dict(color=get_theme_colors()['border'], width=2))
    )
    
    return fig
