
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* 1. HEADER: THE MOUNTAIN PATH TITLE */
            .main-header h1 {{
                color: #FFD700 !important; /* Pure Gold */
                font-size: 3.5rem !important;
                font-weight: 900 !important;
                text-shadow: 3px 3px 0px #000000 !important; /* High contrast shadow */
                margin: 0 !important;
            }}

            /* 2. SIDEBAR: UPLOADER CONTRAST */
            /* Forces the uploader box to white so we can see black text inside */
            [data-testid="stFileUploadDropzone"] {{
                background-color: #FFFFFF !important;
                border: 3px dashed {COLORS['accent_gold']} !important;
            }}
            
            /* Target 'Drag and drop', 'Limit 200MB', and 'XLSX' */
            [data-testid="stFileUploadDropzone"] * {{
                color: #000000 !important; /* FORCE BLACK */
                font-weight: 800 !important;
            }}

            /* 3. SIDEBAR LABELS & TITLES */
            section[data-testid="stSidebar"] label p, 
            section[data-testid="stSidebar"] h1, 
            section[data-testid="stSidebar"] h2 {{
                color: #FFFFFF !important; /* FORCE WHITE */
                font-weight: 700 !important;
                font-size: 1.2rem !important;
                text-shadow: 1px 1px 2px #000000;
            }}

            /* 4. SLIDER NUMBERS (5.0, 25.0) */
            [data-testid="stTickBar"] span {{
                color: #FFFFFF !important;
                font-weight: bold !important;
            }}

            /* 5. STICKY FOOTER */
            .footer {{
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: {COLORS['primary_dark']} !important;
                color: #FFD700 !important;
                border-top: 4px solid {COLORS['accent_gold']} !important;
                padding: 10px;
                text-align: center;
                z-index: 1000;
            }}
        </style>
    """, unsafe_allow_html=True)
