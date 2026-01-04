
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* 1. MAIN HEADER: THE MOUNTAIN PATH TITLE */
            header[data-testid="stHeader"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            
            .main-header {{
                background-color: {COLORS['primary_dark']} !important;
                padding: 2.5rem !important;
                border-bottom: 6px solid {COLORS['accent_gold']} !important;
                text-align: left;
            }}
            
            .main-header h1 {{
                color: #FFD700 !important; /* Vivid Gold */
                font-size: 3.5rem !important;
                font-weight: 900 !important;
                text-shadow: 3px 3px 5px #000000 !important; /* Black shadow for visibility */
                margin: 0 !important;
            }}

            /* 2. SIDEBAR: FILE UPLOADER & TEXT */
            section[data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']} !important;
                border-right: 3px solid {COLORS['accent_gold']} !important;
            }}
            
            /* Sidebar Labels & Captions */
            section[data-testid="stSidebar"] .stMarkdown p, 
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] h2 {{
                color: #FFFFFF !important; /* Pure White */
                font-weight: 700 !important;
                font-size: 1.1rem !important;
                opacity: 1 !important;
            }}

            /* FILE UPLOADER TEXT FIX (Drag and Drop / 200MB) */
            [data-testid="stFileUploadDropzone"] {{
                background-color: #FFFFFF !important; /* Pure White Box */
                border: 2px dashed #000000 !important;
            }}
            
            /* Forces "Drag and drop file here" and "Limit 200MB" to PURE BLACK */
            [data-testid="stFileUploadDropzone"] div, 
            [data-testid="stFileUploadDropzone"] span, 
            [data-testid="stFileUploadDropzone"] small {{
                color: #000000 !important;
                font-weight: 800 !important;
                opacity: 1 !important;
            }}

            /* 3. SLIDER CONTRAST */
            [data-testid="stTickBar"] span {{
                color: #FFFFFF !important; /* White numbers (5.00, 25.00) */
                font-weight: bold !important;
            }}

            /* 4. FIXED FOOTER */
            .footer {{
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: {COLORS['primary_dark']} !important;
                color: #FFD700 !important; /* Gold Text */
                text-align: center;
                padding: 15px;
                font-weight: bold;
                border-top: 3px solid {COLORS['accent_gold']} !important;
                z-index: 1000;
            }}
        </style>
    """, unsafe_allow_html=True)
