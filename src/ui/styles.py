
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* Main Background */
            .stApp {{
                background-color: {COLORS['background']};
            }}
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']};
            }}
            
            /* Header Styling */
            h1 {{
                color: {COLORS['primary_dark']};
                border-bottom: 2px solid {COLORS['accent_gold']};
            }}
            
            /* Tab Styling */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 24px;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                height: 50px;
                white-space: pre-wrap;
                background-color: #FFFFFF;
                border-radius: 4px 4px 0px 0px;
                gap: 1px;
                padding-top: 10px;
                color: {COLORS['text']};
            }}

            .stTabs [aria-selected="true"] {{
                background-color: {COLORS['accent_gold']} !important;
                color: {COLORS['primary_dark']} !important;
                font-weight: bold;
            }}
        </style>
    """, unsafe_allow_html=True)
