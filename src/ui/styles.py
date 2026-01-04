
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* 1. Global App Background */
            .stApp {{
                background-color: {COLORS['background']};
            }}
            
            /* 2. Sidebar Background & Text Color Fix */
            [data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            
            /* Ensures all text, labels, and icons in sidebar are White/Visible */
            [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
                color: #FFFFFF !important;
            }}

            /* 3. Header / Top Bar Branding */
            [data-testid="stHeader"] {{
                background-color: {COLORS['primary_dark']} !important;
                color: #FFFFFF !important;
            }}

            /* 4. Custom Header Styling (The Title) */
            .main-header {{
                background-color: {COLORS['primary_dark']};
                color: {COLORS['accent_gold']};
                padding: 1.5rem;
                border-radius: 10px;
                border-bottom: 4px solid {COLORS['accent_gold']};
                margin-bottom: 2rem;
                text-align: center;
            }}
            
            /* 5. Modern Tab Styling */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
                background-color: transparent;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                background-color: #E1E4E8;
                border-radius: 4px 4px 0px 0px;
                padding: 10px 20px;
                color: {COLORS['primary_dark']};
            }}

            .stTabs [aria-selected="true"] {{
                background-color: {COLORS['accent_gold']} !important;
                font-weight: bold;
                color: {COLORS['primary_dark']} !important;
            }}

            /* 6. Metric Card Styling */
            [data-testid="stMetricValue"] {{
                color: {COLORS['primary_dark']};
            }}
        </style>
    """, unsafe_allow_html=True)
