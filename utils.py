# =============================================================================
# utils.py - Utility Functions
# =============================================================================

import pandas as pd
import numpy as np
from datetime import datetime

def format_currency(value, currency='₹'):
    """Format number as currency"""
    if pd.isna(value):
        return "N/A"
    if abs(value) >= 1e7:
        return f"{currency}{value/1e7:.1f}L"
    elif abs(value) >= 1e5:
        return f"{currency}{value/1e5:.1f}K"
    else:
        return f"{currency}{value:,.0f}"

def format_percentage(value, decimals=1):
    """Format number as percentage"""
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimals}f}%"

def format_ratio(value, decimals=2):
    """Format number as ratio"""
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimals}f}x"

def get_color_for_metric(value, threshold_good, threshold_bad):
    """Get color based on metric value"""
    if pd.isna(value):
        return "#999999"
    if value >= threshold_good:
        return "#00AA00"  # Green
    elif value <= threshold_bad:
        return "#AA0000"  # Red
    else:
        return "#FFB84D"  # Orange

def calculate_trend(series):
    """Calculate trend (up/down/stable)"""
    if len(series) < 2:
        return "Stable"
    
    recent = series.iloc[-1]
    previous = series.iloc[-2]
    
    if recent > previous * 1.05:
        return "📈 Up"
    elif recent < previous * 0.95:
        return "📉 Down"
    else:
        return "→ Stable"

def validate_dataframe(df, required_columns):
    """Validate dataframe has required columns"""
    missing = [col for col in required_columns if col not in df.columns]
    return len(missing) == 0, missing

def clean_numeric(value):
    """Clean and convert to numeric"""
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        value = value.replace(',', '').replace('₹', '')
    try:
        return float(value)
    except:
        return np.nan

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
