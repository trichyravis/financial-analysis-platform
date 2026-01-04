
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* 1. SIDEBAR GLOBAL FIX */
            [data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}

            /* Force all text, headers, and paragraphs in sidebar to WHITE */
            [data-testid="stSidebar"] *, 
            [data-testid="stSidebar"] h1, 
            [data-testid="stSidebar"] h2, 
            [data-testid="stSidebar"] h3, 
            [data-testid="stSidebar"] p, 
            [data-testid="stSidebar"] span, 
            [data-testid="stSidebar"] label {{
                color: #FFFFFF !important;
            }}

            /* 2. SLIDER & INPUT FIXES (Specific for Sidebar) */
            /* Makes the slider track and numbers visible */
            [data-testid="stSidebar"] [data-baseweb="slider"] {{
                background-color: transparent !important;
            }}
            
            /* Change slider handle and active track to Gold for contrast */
            [data-testid="stSidebar"] .st-eb {{
                background-color: {COLORS['accent_gold']} !important;
            }}

            /* 3. FILE UPLOADER CONTRAST */
            [data-testid="stSidebar"] section[data-testid="stFileUploadDropzone"] {{
                background-color: rgba(255, 255, 255, 0.1) !important;
                border: 1px dashed {COLORS['accent_gold']} !important;
            }}

            /* 4. HEADER BRANDING FIX */
            header[data-testid="stHeader"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            
            /* 5. MAIN CONTENT HEADER */
            .main-header {{
                background-color: {COLORS['primary_dark']};
                padding: 1.5rem;
                border-radius: 8px;
                border-left: 12px solid {COLORS['accent_gold']};
                margin-bottom: 2rem;
            }}
            .main-header h1 {{
                color: {COLORS['accent_gold']} !important;
                margin: 0;
            }}
        </style>
    """, unsafe_allow_html=True)
