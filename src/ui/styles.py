
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* 1. Force the Header Background */
            header[data-testid="stHeader"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}

            /* 2. Force the Sidebar Background and Text Color */
            section[data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            
            /* Target all text elements in sidebar to be white */
            section[data-testid="stSidebar"] span, 
            section[data-testid="stSidebar"] p, 
            section[data-testid="stSidebar"] label {{
                color: white !important;
            }}

            /* 3. Main Title Branding */
            .main-header {{
                background-color: {COLORS['primary_dark']};
                padding: 20px;
                border-radius: 8px;
                border-left: 10px solid {COLORS['accent_gold']};
                margin-bottom: 30px;
            }}
            .main-header h1 {{
                color: {COLORS['accent_gold']} !important;
                margin: 0;
            }}

            /* 4. Fix Tab Headers */
            .stTabs [data-baseweb="tab-list"] button {{
                color: {COLORS['primary_dark']};
            }}
            .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
                background-color: {COLORS['accent_gold']} !important;
                border-radius: 5px;
            }}
        </style>
    """, unsafe_allow_html=True)
