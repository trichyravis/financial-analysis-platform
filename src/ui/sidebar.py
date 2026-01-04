
import streamlit as st
from src.core.config import COMPANY_NAME

def render_sidebar():
    """Handles sidebar branding, file uploads, and global settings."""
    with st.sidebar:
        st.image("https://img.icons8.com/ios-filled/100/ffffff/mountain.png", width=80)
        st.title(f"{COMPANY_NAME}")
        st.subheader("Data Ingestion")
        
        uploaded_file = st.file_uploader(
            "Upload Screener.in Excel", 
            type=["xlsx"], 
            help="Download the 'Standard' Excel export from any company page on Screener.in"
        )
        
        st.divider()
        
        st.subheader("Analysis Parameters")
        wacc = st.slider("Cost of Capital (WACC %)", 5.0, 20.0, 10.0, step=0.5) / 100
        tax = st.number_input("Marginal Tax Rate", 0.0, 0.4, 0.25)
        
        st.sidebar.success("✅ System Ready" if uploaded_file else "⏳ Awaiting Data")
        
        return uploaded_file, {"wacc": wacc, "tax": tax}
