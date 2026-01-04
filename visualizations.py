# =============================================================================
# visualizations.py - Chart Generation & Visualization Utilities
# =============================================================================

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_line_chart(x_data, y_data, trace_name, title, y_axis_title="Value"):
    """Create Plotly line chart"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        name=trace_name,
        mode='lines+markers',
        line=dict(color='#003366', width=2),
        marker=dict(size=6)
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title=y_axis_title,
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    return fig

def create_bar_chart(x_data, y_data, y_axis_title, title):
    """Create Plotly bar chart"""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x_data,
        y=y_data,
        marker=dict(color='#FFD700', line=dict(color='#003366', width=1.5))
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title=y_axis_title,
        height=400,
        template='plotly_white',
        showlegend=False
    )
    return fig

def create_metric_card(metric_name, value, color="#003366"):
    """Create styled metric card"""
    return f"""
    <div style='background-color: #f0f2f6; padding: 15px; 
                border-left: 4px solid {color}; border-radius: 5px; margin: 10px 0;'>
        <p style='color: #666; margin: 0; font-size: 12px;'>{metric_name}</p>
        <p style='color: {color}; margin: 0; font-size: 20px; font-weight: bold;'>{value}</p>
    </div>
    """

def create_heatmap(data, title, x_label, y_label):
    """Create Plotly heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale='RdYlGn'
    ))
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=400
    )
    return fig

def create_pie_chart(labels, values, title):
    """Create Plotly pie chart"""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=['#003366', '#ADD8E6', '#FFD700', '#666666'])
    )])
    fig.update_layout(title=title, height=400)
    return fig

def create_waterfall_chart(categories, values, title):
    """Create Plotly waterfall chart"""
    fig = go.Figure(go.Waterfall(
        name="Value Bridge",
        orientation="v",
        x=categories,
        textposition="outside",
        y=values,
        connector={"line": {"color": "rgba(63, 63, 63, 0.5)"}}
    ))
    fig.update_layout(title=title, height=400, showlegend=False)
    return fig
