
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* 1. MAIN HEADER TEXT VISIBILITY */
            .main-header h1 {{
                color: {COLORS['accent_gold']} !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5); /* Adds depth for visibility */
                font-weight: 800 !important;
                margin: 0 !important;
            }}
            .main-header p {{
                color: #FFFFFF !important;
                font-weight: 500 !important;
            }}

            /* 2. SIDEBAR FILE UPLOADER VISIBILITY */
            /* We force the dropzone box to be White so Black text inside is clear */
            [data-testid="stFileUploadDropzone"] {{
                background-color: #FFFFFF !important;
                border: 2px dashed {COLORS['accent_gold']} !important;
                padding: 10px !important;
            }}
            
            /* Target 'Drag and drop', 'Limit 200MB', and 'XLSX' text */
            [data-testid="stFileUploadDropzone"] * {{
                color: #000000 !important; /* FORCED BLACK */
                font-family: sans-serif !important;
            }}
            
            /* Target the small 'Limit' text specifically */
            [data-testid="stFileUploadDropzone"] small {{
                color: #444444 !important;
                font-weight: bold !important;
            }}

            /* 3. SIDEBAR BRANDING TITLE (The Mountain Path in Sidebar) */
            [data-testid="stSidebarNav"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            section[data-testid="stSidebar"] .stMarkdown h1 {{
                color: #FFFFFF !important;
                padding-top: 20px;
            }}

            /* 4. SYSTEM HEADER OVERRIDE */
            header[data-testid="stHeader"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
        </style>
    """, unsafe_allow_html=True)
