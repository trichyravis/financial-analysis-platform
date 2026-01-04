
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* 1. GLOBAL SIDEBAR OVERRIDE */
            /* Forces the Navy Blue background and sets a base white color */
            section[data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']} !important;
                color: #FFFFFF !important;
            }}

            /* 2. FORCE TEXT COLORS FOR ALL SIDEBAR ELEMENTS */
            /* This ensures Headers, Labels, and normal text are always White */
            section[data-testid="stSidebar"] h1, 
            section[data-testid="stSidebar"] h2, 
            section[data-testid="stSidebar"] h3, 
            section[data-testid="stSidebar"] label, 
            section[data-testid="stSidebar"] p, 
            section[data-testid="stSidebar"] span {{
                color: #FFFFFF !important;
                font-weight: 500 !important;
            }}

            /* 3. FILE UPLOADER CONTRAST FIX */
            /* We make the box white so the black text inside it stands out */
            [data-testid="stFileUploadDropzone"] {{
                background-color: #FFFFFF !important;
                border: 2px dashed {COLORS['accent_gold']} !important;
            }}
            
            /* Forces the "Drag and drop", "Browse files", and "Limit" text to BLACK */
            [data-testid="stFileUploadDropzone"] * {{
                color: #000000 !important;
            }}

            /* 4. SLIDER VISIBILITY */
            /* Ensures the slider numbers and labels at the ends (5.0, 25.0) are White */
            [data-testid="stSidebar"] [data-testid="stTickBarMin"],
            [data-testid="stSidebar"] [data-testid="stTickBarMax"],
            [data-testid="stSidebar"] [data-testid="stSliderTick"] {{
                color: #FFFFFF !important;
            }}
            
            /* Changes the Slider handle to Gold for branding */
            [data-testid="stSidebar"] .st-eb {{
                background-color: {COLORS['accent_gold']} !important;
            }}

            /* 5. HEADER & FOOTER (Matches your previous design) */
            [data-testid="stHeader"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            
            .main-header {{
                background-color: {COLORS['primary_dark']};
                padding: 1.5rem;
                border-radius: 8px;
                border-left: 10px solid {COLORS['accent_gold']};
                margin-bottom: 2rem;
            }}
            
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
                z-index: 999;
            }}
        </style>
    """, unsafe_allow_html=True)
