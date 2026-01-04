
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* HEADER: THE MOUNTAIN PATH */
            header[data-testid="stHeader"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            .main-header {{
                background-color: {COLORS['primary_dark']} !important;
                padding: 2.5rem !important;
                border-bottom: 5px solid #FFD700 !important;
            }}
            .main-header h1 {{
                color: #FFD700 !important; /* PURE GOLD */
                font-size: 3.5rem !important;
                font-weight: 900 !important;
                text-shadow: 3px 3px 2px #000000 !important;
            }}

            /* SIDEBAR: UPLOADER TEXT & LABELS */
            section[data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            
            /* The Uploader Box text */
            [data-testid="stFileUploadDropzone"] {{
                background-color: #FFFFFF !important;
                border: 2px dashed #000000 !important;
            }}
            [data-testid="stFileUploadDropzone"] * {{
                color: #000000 !important; /* PURE BLACK */
                font-weight: bold !important;
            }}

            /* Sidebar general labels */
            section[data-testid="stSidebar"] label p {{
                color: #FFFFFF !important; /* PURE WHITE */
                font-size: 1.1rem !important;
                font-weight: bold !important;
            }}

            /* FOOTER */
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
