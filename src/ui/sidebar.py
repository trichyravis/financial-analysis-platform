
import streamlit as st
from src.core.config import COMPANY_NAME

def render_sidebar():
    """Renders sidebar for file upload and global settings."""
    st.sidebar.title(f"🏔️ {COMPANY_NAME}")
    
    # 1. Initialize the settings dictionary
    settings = {}
    
    st.sidebar.header("📁 Data Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Screener.in Excel", 
        type=["xlsx"],
        help="Download the 'Data Sheet' from Screener.in and upload here."
    )
    
    st.sidebar.divider()
    
    st.sidebar.header("⚙️ Valuation Assumptions")
    
    # 2. WACC Input (Default 10.0%)
    # We display it as a whole number for user comfort
    wacc_pct = st.sidebar.slider(
        "Cost of Capital (WACC %)", 
        min_value=5.0, 
        max_value=25.0, 
        value=10.0,
        step=0.5,
        help="The required rate of return for investors."
    )
    
    # Store in settings (The DCF tab will divide this by 100 later)
    settings['wacc'] = wacc_pct 
    
    # 3. Tax Rate Input
    tax_rate = st.sidebar.number_input(
        "Effective Tax Rate (%)", 
        min_value=0, 
        max_value=50, 
        value=25
    )
    settings['tax_rate'] = tax_rate / 100

    st.sidebar.divider()
    
    # Sidebar Branding
    st.sidebar.info(
        "Institutional Grade Financial Analysis Platform\n\n"
        "Developed by Prof. V. Ravichandran"
    )
    
    return uploaded_file, settings
