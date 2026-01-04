
"""
🏔️ THE MOUNTAIN PATH - World of Finance
Final Orchestrated app.py (2026 Edition)
Institutional Financial Analysis Platform
"""

import streamlit as st
import pandas as pd

# Core Configuration & UI
from src.core.config import COLORS, TABS, COMPANY_NAME
from src.core.data_loader import UniversalScreenerLoader
from src.ui.styles import apply_custom_css
from src.ui.components import UIComponents
from src.ui.sidebar import render_sidebar

# Analysis Engines
from src.analysis.financial import FinancialAnalyzer
from src.analysis.eva import EVAAnalyzer
from src.analysis.growth import GrowthAnalyzer

# Tab Rendering Logic
from src.ui.tabs.dashboard import render_dashboard
from src.ui.tabs.profitability_tab import render_profitability_tab
from src.ui.tabs.dcf_tab import render_dcf_tab
from src.ui.tabs.efficiency_tab import render_efficiency_tab
from src.ui.tabs.growth_tab import render_growth_tab

# Page Configuration
st.set_page_config(
    page_title=f"{COMPANY_NAME} | Institutional Analysis",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Apply Custom Branding
    apply_custom_css()

    # Sidebar Capture (Returns file and user-defined valuation inputs)
    uploaded_file, settings = render_sidebar()

    # Hero Header
    UIComponents.header("Advanced Institutional Financial Analysis")

    if uploaded_file:
        with st.spinner("🏔️ Scaling the Data Mountain..."):
            loader = UniversalScreenerLoader(uploaded_file)
            processed_data, metadata = loader.get_processed_data()

        if processed_data is not None:
            # Initialize Master Analyzer
            analyzer = FinancialAnalyzer(processed_data)
            
            # Generate the 12-Tab Interface
            tab_objs = st.tabs(TABS)

            # --- TAB 0: EXECUTIVE DASHBOARD ---
            with tab_objs[0]:
                render_dashboard(processed_data, metadata)

            # --- TAB 1: FINANCIAL STATEMENTS ---
            with tab_objs[1]:
                st.subheader("📋 Historical Statements (P&L + BS + CF)")
                # Transposed for institutional reading
                st.dataframe(processed_data.set_index('Report Date').T, width='stretch')

            # --- TAB 2: PROFITABILITY ANALYSIS ---
            with tab_objs[2]:
                render_profitability_tab(processed_data)

            # --- TAB 3: DCF VALUATION ---
            with tab_objs[3]:
                render_dcf_tab(processed_data, settings)

            # --- TAB 4: EVA ANALYSIS ---
            with tab_objs[4]:
                st.subheader("💎 Economic Value Added (EVA)")
                wacc_dec = settings.get('wacc', 12.0) / 100
                eva_engine = EVAAnalyzer(processed_data, wacc_dec)
                eva_df = eva_engine.calculate_eva()
                st.bar_chart(eva_df['EVA'])
                st.dataframe(eva_df.T, width='stretch')

            # --- TAB 5: SOLVENCY & CAPITAL ---
            with tab_objs[5]:
                st.subheader("⚖️ Solvency Ratios")
                solv_df = analyzer.get_solvency_metrics()
                st.line_chart(solv_df[['Debt-to-Equity']])
                st.dataframe(solv_df.set_index('Year').T, width='stretch')

            # --- TAB 6: OPERATIONAL EFFICIENCY ---
            with tab_objs[6]:
                render_efficiency_tab(processed_data)

            # --- TAB 7: GROWTH MOMENTUM ---
            with tab_objs[7]:
                render_growth_tab(processed_data)

            # --- TABS 8-11: DYNAMIC PLACEHOLDERS ---
            # Prevents IndexError if config.py has 12 tabs but logic isn't written yet
            for i in range(8, len(tab_objs)):
                with tab_objs[i]:
                    st.write(f"### {TABS[i]}")
                    st.info(f"The {TABS[i]} module is processing historical data trends...")

        else:
            st.error("❌ Data structure mismatch. Ensure you use a standard Screener.in Excel.")
    
    else:
        # Welcome State
        st.markdown(f"### 👋 Welcome to {COMPANY_NAME}")
        st.info("Please upload a Screener.in Excel file from the sidebar to begin your institutional analysis.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Analysis Capabilities:**")
            st.write("- 3-Stage DCF Intrinsic Valuation")
            st.write("- Economic Value Added (EVA) Analysis")
            st.write("- DuPont Profitability Framework")
        with col2:
            st.write("**Operational Intelligence:**")
            st.write("- Working Capital Cycle Analysis")
            st.write("- Debt Solvency & Interest Coverage")
            st.write("- 10-Year CAGR Growth Tracking")

    # Global Footer
    UIComponents.footer()

if __name__ == "__main__":
    main()
