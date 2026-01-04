
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* 1. MAIN HEADER: THE MOUNTAIN PATH */
            header[data-testid="stHeader"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            .main-header {{
                background-color: {COLORS['primary_dark']} !important;
                padding: 2rem !important;
                border-bottom: 6px solid #FFD700 !important;
                margin-bottom: 25px !important;
            }}
            .main-header h1 {{
                color: #FFD700 !important; /* PURE GOLD */
                font-size: 3.5rem !important;
                font-weight: 900 !important;
                text-shadow: 2px 2px 4px #000000 !important; /* Makes it pop */
                margin: 0 !important;
            }}

            /* 2. SIDEBAR: UPLOADER CONTRAST */
            [data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            
            /* Forces the uploader box to be white so black text is visible */
            [data-testid="stFileUploadDropzone"] {{
                background-color: #FFFFFF !important;
                border: 2px dashed #000000 !important;
            }}
            
            /* FORCE BLACK TEXT for "Drag and Drop" and "Limit 200MB" */
            [data-testid="stFileUploadDropzone"] * {{
                color: #000000 !important; 
                font-weight: 800 !important;
            }}

            /* 3. SIDEBAR LABELS (WACC, Tax Rate) */
            section[data-testid="stSidebar"] label p {{
                color: #FFFFFF !important; /* PURE WHITE */
                font-size: 1.1rem !important;
                font-weight: bold !important;
            }}

            /* 4. FIXED FOOTER */
            .footer {{
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: {COLORS['primary_dark']} !important;
                color: #FFD700 !important;
                text-align: center;
                padding: 10px;
                border-top: 3px solid #FFD700;
                z-index: 999;
            }}
        </style>
    """, unsafe_allow_html=True)
