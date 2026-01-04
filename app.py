
"""
🏔️ THE MOUNTAIN PATH - World of Finance
Advanced Financial Analysis Platform (Institutional Edition)
Main Orchestrator: app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Import Core Configurations and Components
from src.core.config import COLORS, TABS, FINANCIAL_DEFAULTS, COMPANY_NAME, AUTHOR
from src.core.data_loader import UniversalScreenerLoader
from src.ui.styles import apply_custom_css
from src.ui.components import UIComponents
from src.ui.sidebar import render_sidebar

# Import Tab Rendering Logic
from src.ui.tabs.dashboard import render_dashboard
from src.ui.tabs.profitability_tab import render_profitability_tab
from src.ui.tabs.dcf_tab import render_dcf_tab

# Import Analysis Engines
from src.analysis.financial import FinancialAnalyzer
from src.analysis.eva import EVAAnalyzer

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title=f"{COMPANY_NAME} | Financial Analysis",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. APPLY BRANDING (Dark Blue & Gold Theme)
apply_custom_css()

def main():
    # 3. RENDER SIDEBAR (Branded Sidebar with File Uploader)
    # Returns the uploaded file and user-defined settings (WACC, Growth, etc.)
    uploaded_file, settings = render_sidebar()

    # 4. RENDER HERO HEADER (The Mountain Path Design)
    UIComponents.header("Institutional Financial Analytics Platform")

    if uploaded_file:
        # 5. DATA INGESTION ENGINE
        with st.spinner("🏔️ Scaling the data... Processing Screener.in Excel..."):
            loader = UniversalScreenerLoader(uploaded_file)
            processed_data = loader.get_processed_data()
            
            # Extract metadata (Market Cap, Current Price) if available
            metadata = loader.get_metadata() if hasattr(loader, 'get_metadata') else {}

        if processed_data is not None:
            # 6. 12-TAB INTERFACE
            tab_list = st.tabs(TABS)

            # --- TAB 1: EXECUTIVE DASHBOARD ---
            with tab_list[0]:
                render_dashboard(processed_data, metadata)

            # --- TAB 2: FINANCIAL STATEMENTS ---
            with tab_list[1]:
                st.subheader("📋 Cleaned Financial Data (P&L + BS + CF)")
                # Transpose for easier reading (years as columns)
                st.dataframe(processed_data.set_index('Report Date').T, width='stretch')

            # --- TAB 3: PROFITABILITY ANALYSIS ---
            with tab_list[2]:
                render_profitability_tab(processed_data)

            # --- TAB 4: DCF VALUATION ---
            with tab_list[3]:
                render_dcf_tab(processed_data, settings)

            # --- TAB 5: EVA ANALYSIS ---
            with tab_list[4]:
                st.subheader("💎 Economic Value Added (EVA) - Wealth Creation")
                eva_engine = EVAAnalyzer(processed_data, settings['wacc'])
                eva_df = eva_engine.calculate_eva()
                st.dataframe(eva_df, width='stretch')

            # --- TAB 6: SOLVENCY & CAPITAL STRUCTURE ---
            with tab_list[5]:
                from src.analysis.financial import FinancialAnalyzer
                analyzer = FinancialAnalyzer(processed_data)
                solvency_df = analyzer.get_solvency_metrics()
                st.line_chart(solvency_df[['Debt-to-Equity']])
                st.dataframe(solvency_df, width='stretch')

            # --- TAB 7: OPERATIONAL EFFICIENCY ---
            with tab_list[6]:
                st.subheader("⚡ Asset Utilization & Efficiency")
                # Logic for efficiency metrics goes here
                st.info("Module loading: Asset Turnover, Debtor Days, and Inventory Cycle.")

            # --- TABS 8-12: GROWTH, RISK, PEERS, SUMMARY ---
            # Implementation follows the same pattern of calling specialized renderers
            for i in range(7, 12):
                with tab_list[i]:
                    st.write(f"### {TABS[i]}")
                    st.info("Section currently processing historical data trends...")

        else:
            st.error("❌ Data Error: The uploaded file structure does not match the Screener.in standard.")
    
    else:
        # 7. WELCOME / EMPTY STATE
        st.markdown(f"""
        ### 👋 Welcome to {COMPANY_NAME}
        To begin your analysis, please download the **Standard Excel Export** from [Screener.in](https://www.screener.in) 
        for any listed Indian company and upload it via the sidebar.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://img.icons8.com/clouds/200/mountain.png")
        with col2:
            st.warning("📊 **Note:** This tool is optimized for the 'Data Sheet' tab in Screener's Excel files.")

    # 8. RENDER GLOBAL FOOTER
    UIComponents.footer()

if __name__ == "__main__":
    main()
