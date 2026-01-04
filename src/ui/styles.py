
import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            /* 1. MAIN HEADER: THE MOUNTAIN PATH */
            .main-header h1 {
                color: #FFD700 !important; /* PURE GOLD */
                font-size: 3.5rem !important;
                font-weight: 900 !important;
                text-shadow: 3px 3px 5px #000000 !important; /* Hard shadow for depth */
                letter-spacing: 1px;
            }

            /* 2. SIDEBAR: PURE BLACK TEXT ON WHITE BOX */
            [data-testid="stSidebar"] {
                background-color: #002b5b !important; /* Deep Navy */
            }
            
            /* File Uploader Box */
            [data-testid="stFileUploadDropzone"] {
                background-color: #FFFFFF !important; /* Pure White background */
                border: 2px solid #FFD700 !important;
            }
            
            /* Drag and Drop / Limit 200MB text */
            [data-testid="stFileUploadDropzone"] * {
                color: #000000 !important; /* FORCED PURE BLACK */
                font-weight: 800 !important;
            }

            /* 3. SIDEBAR SLIDER CONTRAST */
            [data-testid="stSidebar"] .stMarkdown p, 
            [data-testid="stSidebar"] label {
                color: #FFFFFF !important; /* PURE WHITE labels */
                font-weight: bold !important;
                font-size: 1.1rem !important;
            }
            
            /* Slider Numbers (5.0, 25.0) */
            [data-testid="stTickBar"] span {
                color: #FFFFFF !important;
                font-weight: 900 !important;
            }

            /* 4. FIXED FOOTER */
            .footer {
                position: fixed;
                bottom: 0;
                width: 100%;
                background-color: #002b5b !important;
                color: #FFD700 !important;
                border-top: 3px solid #FFD700;
                text-align: center;
                padding: 10px;
                font-weight: bold;
                z-index: 1000;
            }
        </style>
    """, unsafe_allow_html=True)
