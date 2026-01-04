
"""
app.py - Main Entry Point
🏔️ THE MOUNTAIN PATH - World of Finance
"""

import streamlit as st
import pandas as pd
from src.core.config import COLORS, TABS, FINANCIAL_DEFAULTS
from src.core.data_loader import UniversalScreenerLoader
from src.ui.styles import apply_custom_css
from src.ui.components import UIComponents
from src.ui.sidebar import render_sidebar

# 1. Page Configuration
st.set_page_config(
    page_title="Mountain Path | Financial Analysis",
    page_icon="🏔️",
    layout="wide"
)

# 2. Initialization
apply_custom_css()

def main():
    # 3. Sidebar UI (Branded)
    uploaded_file, settings = render_sidebar()

    # 4. Hero Header (Branded)
    UIComponents.header("Advanced Financial Analysis Platform")

    if uploaded_file:
        # 5. Data Processing
        with st.spinner("Processing Screener.in Data..."):
            loader = UniversalScreenerLoader(uploaded_file)
            data = loader.get_processed_data()

        if data is not None:
            # 6. Tabbed Interface (12 Tabs as requested)
            tab_objs = st.tabs(TABS)

            with tab_objs[0]: # Dashboard
                from src.ui.tabs.dashboard import render_dashboard
                render_dashboard(data)

            with tab_objs[1]: # Financials
                st.subheader("📋 Historical Financial Statements")
                st.dataframe(data.set_index('Report Date'), use_container_width=True)

            with tab_objs[2]: # Profitability
                from src.ui.tabs.profitability_tab import render_profitability_tab
                render_profitability_tab(data)

            with tab_objs[3]: # DCF Valuation
                from src.ui.tabs.dcf_tab import render_dcf_tab
                render_dcf_tab(data, settings)

            with tab_objs[4]: # EVA Analysis
                from src.analysis.eva import EVAAnalyzer
                eva_calc = EVAAnalyzer(data, settings['wacc'])
                st.dataframe(eva_calc.calculate_eva(), use_container_width=True)

            # ... Additional tabs (Solvency, Efficiency, Risk, etc.) 
            # would follow the same pattern of importing their respective UI logic

        else:
            st.error("Failed to parse the Excel file. Please ensure it is a standard Screener.in export.")
    
    else:
        # Welcome Screen for empty state
        st.info("👋 Welcome! Please upload a company Excel sheet from Screener.in to begin your analysis.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### How to use:
            1. Go to **Screener.in**
            2. Search for any Indian listed company.
            3. Click on **'Export to Excel'**.
            4. Upload that file here using the sidebar.
            """)
        with col2:
            st.markdown("### Analysis Features:")
            st.write("✔️ 2-Stage DCF Valuation")
            st.write("✔️ Economic Value Added (EVA)")
            st.write("✔️ 50+ Financial Ratios")
            st.write("✔️ Risk & Volatility Metrics")

    # 7. Branded Footer
    UIComponents.footer()

if __name__ == "__main__":
    main()
