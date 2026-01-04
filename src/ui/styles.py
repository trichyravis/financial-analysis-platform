
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* 1. GLOBAL RESET - Force Backgrounds */
            .stApp {{
                background-color: #F8F9FA;
            }}
            
            /* 2. HEADER: Deep Navy Background + Gold Text */
            header[data-testid="stHeader"] {{
                background-color: {COLORS['primary_dark']} !important;
                height: 4rem;
            }}
            
            .main-header {{
                background-color: {COLORS['primary_dark']};
                padding: 2.5rem;
                border-radius: 12px;
                border-bottom: 5px solid {COLORS['accent_gold']};
                margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            }}
            
            .main-header h1 {{
                color: {COLORS['accent_gold']} !important;
                font-size: 3rem !important;
                font-weight: 800 !important;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin: 0;
            }}

            /* 3. SIDEBAR: Solid Navy + Pure White Text */
            section[data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']} !important;
                border-right: 2px solid {COLORS['accent_gold']};
            }}
            
            /* Force all Sidebar text, headers, and labels to High-Contrast White */
            section[data-testid="stSidebar"] * {{
                color: #FFFFFF !important;
            }}

            /* 4. SLIDER CONTRAST FIX */
            /* This makes the "active" part of the slider Gold and the text Bold White */
            div[data-testid="stSlider"] [data-baseweb="slider"] {{
                margin-top: 15px;
            }}
            
            /* Slider handle and track */
            div[data-st-thumb] {{
                background-color: {COLORS['accent_gold']} !important;
            }}
            
            /* The numbers at the ends of the slider (5.0, 25.0) */
            div[data-testid="stTickBar"] span {{
                color: #FFFFFF !important;
                font-weight: bold !important;
                font-size: 0.9rem !important;
            }}

            /* 5. FOOTER: Fixed, Deep Navy, High Visibility */
            .footer {{
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: {COLORS['primary_dark']} !important;
                color: #FFFFFF !important;
                text-align: center;
                padding: 15px 0;
                font-weight: 500;
                border-top: 3px solid {COLORS['accent_gold']};
                z-index: 1000;
                font-size: 0.9rem;
            }}
            
            .footer b {{
                color: {COLORS['accent_gold']};
            }}

            /* 6. FILE UPLOADER: White Box / Black Text */
            [data-testid="stFileUploadDropzone"] {{
                background-color: #FFFFFF !important;
                border: 2px dashed {COLORS['accent_gold']} !important;
            }}
            [data-testid="stFileUploadDropzone"] * {{
                color: #000000 !important; /* Force Black text in White box */
            }}
        </style>
    """, unsafe_allow_html=True)
