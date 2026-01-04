
import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            /* 1. FORCE THE MOUNTAIN PATH TITLE TO BRIGHT GOLD */
            .main-header h1 {
                color: #FFD700 !important; /* Pure Vivid Gold */
                font-size: 3.8rem !important; /* Larger for impact */
                font-weight: 900 !important;
                text-shadow: 4px 4px 0px #000000 !important; /* Thick black shadow */
                margin-bottom: 0 !important;
            }
            .main-header p {
                color: #FFFFFF !important; /* Pure white subtitle */
                font-size: 1.2rem;
            }

            /* 2. SIDEBAR FILE UPLOADER CONTRAST */
            [data-testid="stSidebar"] {
                background-color: #001f3f !important; /* Deep Midnight Navy */
            }
            
            /* File Uploader Box: White Background for Black Text */
            [data-testid="stFileUploadDropzone"] {
                background-color: #FFFFFF !important;
                border: 3px solid #FFD700 !important; /* Gold border */
            }
            
            /* The "Drag and Drop" and "Limit 200MB" text forced to BLACK */
            [data-testid="stFileUploadDropzone"] * {
                color: #000000 !important; 
                font-weight: 900 !important;
                font-size: 1rem !important;
            }

            /* 3. SIDEBAR LABELS (WACC, Tax Rate, etc) */
            section[data-testid="stSidebar"] label p {
                color: #FFFFFF !important; /* High contrast White */
                font-size: 1.15rem !important;
                font-weight: bold !important;
            }

            /* 4. FOOTER: GOLD ON NAVY */
            .footer {
                position: fixed;
                bottom: 0;
                width: 100%;
                background-color: #001f3f !important;
                color: #FFD700 !important;
                text-align: center;
                padding: 12px;
                border-top: 4px solid #FFD700;
                font-weight: bold;
                z-index: 1000;
            }
        </style>
    """, unsafe_allow_html=True)
