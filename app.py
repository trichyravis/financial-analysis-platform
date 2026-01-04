
"""
🏔️ THE MOUNTAIN PATH - World of Finance
Final Full Orchestrator: app.py
Project: Institutional Financial Analysis Platform
"""

import streamlit as st
import pandas as pd
import numpy as np

# 1. CORE CONFIG & UI COMPONENTS
from src.core.config import COLORS, TABS, COMPANY_NAME, FINANCIAL_DEFAULTS
from src.core.data_loader import UniversalScreenerLoader
from src.ui.styles import apply_custom_css
from src.ui.components import UIComponents
from src.ui.sidebar import render_sidebar

# 2. ANALYSIS ENGINES
from src.analysis.financial import FinancialAnalyzer
from src.analysis.eva import EVAAnalyzer
from src.analysis.growth import GrowthAnalyzer
from src.analysis.risk import RiskAnalyzer

# 3. TAB RENDERING MODULES
from src.ui.tabs.dashboard import render_dashboard
from src.ui.tabs.profitability_tab import render_profitability_tab
from src.ui.tabs.dcf_tab import render_dcf_tab
from src.ui.tabs.growth_tab import render_growth_tab
from src.ui.tabs.shareholding_tab import render_shareholding_tab
from src.ui.tabs.peers_tab import render_peers_tab
from src.ui.tabs.thesis_tab import render_thesis_tab

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title=f"{COMPANY_NAME} | Financial Analytics",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Apply Custom CSS Branding
    apply_custom_css()

    # RENDER SIDEBAR (Captures File and Valuation Inputs)
    uploaded_file, settings = render_sidebar()

    # RENDER BRANDED HEADER
    UIComponents.header("Advanced Institutional Financial Analysis")

    if uploaded_file:
        with st.spinner("🏔️ Scaling the Data Mountain..."):
            # INITIALIZE LOADER
            loader = UniversalScreenerLoader(uploaded_file)
            
            # UNPACK DATA & METADATA
            # Returns (DataFrame, MetaDict) to avoid TypeError
            data, metadata = loader.get_processed_data()

        if data is not None:
            # INITIALIZE MASTER ANALYZER (Shared across tabs for efficiency)
            analyzer = FinancialAnalyzer(data)
            
            # CREATE THE 12-TAB INTERFACE
            tab_objs = st.tabs(TABS)

            # --- TAB 1: EXECUTIVE DASHBOARD ---
            with tab_objs[0]:
                render_dashboard(data, metadata)

            # --- TAB 2: FINANCIAL STATEMENTS ---
            with tab_objs[1]:
                st.subheader("📋 Historical Financial Statements")
                # Transpose for institutional reading (Dates as Columns)
                st.dataframe(data.set_index('Report Date').T, width='stretch')

            # --- TAB 3: PROFITABILITY ANALYSIS ---
            with tab_objs[2]:
                render_profitability_tab(data)

            # --- TAB 4: DCF VALUATION ---
            with tab_objs[3]:
                render_dcf_tab(data, settings)

            # --- TAB 5: EVA ANALYSIS (Wealth Creation) ---
            with tab_objs[4]:
                st.subheader("💎 Economic Value Added (EVA)")
                eva_engine = EVAAnalyzer(data, settings.get('wacc', 0.12))
                st.dataframe(eva_engine.calculate_eva(), width='stretch')

            # --- TAB 6: SOLVENCY & CAPITAL STRUCTURE ---
            with tab_objs[5]:
                st.subheader("⚖️ Solvency Ratios")
                solvency_df = analyzer.get_solvency_metrics()
                st.line_chart(solvency_df[['Debt-to-Equity']])
                st.dataframe(solvency_df, width='stretch')

            # --- TAB 7: OPERATIONAL EFFICIENCY ---
            with tab_objs[6]:
                st.subheader("⚡ Efficiency & Asset Turnover")
                st.dataframe(analyzer.get_efficiency_metrics(), width='stretch')

            # --- TAB 8: GROWTH MOMENTUM ---
            with tab_objs[7]:
                render_growth_tab(data)

            # --- TAB 9: SHAREHOLDING & CAPITAL ---
            with tab_objs[8]:
                render_shareholding_tab(data)

            # --- TAB 10: RISK & VOLATILITY ---
            with tab_objs[9]:
                st.subheader("🛡️ Risk Metrics")
                risk_engine = RiskAnalyzer(data)
                st.table(risk_engine.get_risk_metrics())

            # --- TAB 11: PEER BENCHMARKING ---
            with tab_objs[10]:
                render_peers_tab(data)

            # --- TAB 12: INVESTMENT THESIS ---
            with tab_objs[11]:
                render_thesis_tab(data, settings)

        else:
            st.error("❌ Critical Error: Unable to process file. Ensure it is a standard Screener.in export.")
    
    else:
        # WELCOME STATE
        st.info("👋 Welcome! Please upload a company Excel sheet from Screener.in to begin.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Analysis Coverage:**
            - Intrinsic Value (DCF)
            - Economic Value Added (EVA)
            - 10-Year CAGR Growth
            - Solvency & Risk Profiles
            """)
        with col2:
            st.image("https://img.icons8.com/clouds/200/mountain.png")

    # GLOBAL FOOTER
    UIComponents.footer()

if __name__ == "__main__":
    main()
