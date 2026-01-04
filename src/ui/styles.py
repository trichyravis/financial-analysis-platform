
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    """Injects custom CSS for Mountain Path branding."""
    st.markdown(f"""
        <style>
        /* Main Background and Text */
        .stApp {{
            background-color: {COLORS['background']};
            color: {COLORS['text']};
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background-color: {COLORS['primary_dark']} !important;
            border-right: 2px solid {COLORS['accent_gold']};
        }}
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        /* Custom Header Card */
        .hero-header {{
            background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, {COLORS['primary_light']} 100%);
            padding: 2.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            border-bottom: 6px solid {COLORS['accent_gold']};
        }}
        
        /* Metric Card Styling */
        div[data-testid="metric-container"] {{
            background-color: white;
            border-left: 5px solid {COLORS['primary_dark']};
            padding: 15px;
            border-radius: 8px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }}
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: #e1e1e1;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {COLORS['accent_gold']} !important;
            color: {COLORS['primary_dark']} !important;
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)
