
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* SIDEBAR: Deep Navy with White Text */
            [data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            [data-testid="stSidebar"] * {{
                color: #FFFFFF !important;
            }}
            /* Sidebar Sliders & Inputs */
            [data-testid="stSidebar"] .stSlider {{
                padding-bottom: 20px;
            }}
            
            /* HEADER: Deep Navy Branding */
            header[data-testid="stHeader"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            
            /* INSTITUTIONAL BANNER */
            .main-header {{
                background-color: {COLORS['primary_dark']};
                padding: 2rem;
                border-radius: 10px;
                border-left: 12px solid {COLORS['accent_gold']};
                margin-bottom: 2rem;
                color: white;
            }}
            .main-header h1 {{
                color: {COLORS['accent_gold']} !important;
                margin-bottom: 0px;
            }}

            /* FOOTER: Professional Branding */
            .footer {{
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: {COLORS['primary_dark']};
                color: white;
                text-align: center;
                padding: 10px;
                font-size: 0.8rem;
                border-top: 2px solid {COLORS['accent_gold']};
                z-index: 100;
            }}
        </style>
    """, unsafe_allow_html=True)
