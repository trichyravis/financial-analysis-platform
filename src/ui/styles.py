
import streamlit as st
from src.core.config import COLORS

def apply_custom_css():
    st.markdown(f"""
        <style>
            /* 1. Global App & Sidebar */
            [data-testid="stSidebar"] {{
                background-color: {COLORS['primary_dark']} !important;
            }}
            
            /* General Sidebar Text remains White for contrast against Navy */
            [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {{
                color: #FFFFFF !important;
            }}

            /* 2. FILE UPLOADER FIX: Force Text to BLACK inside the frame */
            [data-testid="stFileUploadDropzone"] {{
                background-color: #FFFFFF !important; /* White background for the box */
                border: 2px dashed {COLORS['accent_gold']} !important;
                border-radius: 10px !important;
            }}

            /* Targets the "Browse files" text and "Drag and drop" instructions */
            [data-testid="stFileUploadDropzone"] * {{
                color: #000000 !important; /* PURE BLACK TEXT */
                font-weight: 500 !important;
            }}
            
            /* Specific fix for the 'Limit 200MB' small text */
            [data-testid="stFileUploadDropzone"] small {{
                color: #333333 !important;
            }}

            /* 3. Sidebar Slider Fix (Already discussed) */
            [data-testid="stSidebar"] [data-baseweb="slider"] {{
                background-color: transparent !important;
            }}

            /* 4. Main Header and Footer Branding (As per your design) */
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
