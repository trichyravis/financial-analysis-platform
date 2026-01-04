
"""
🏔️ THE MOUNTAIN PATH - World of Finance
Advanced Financial Analysis Platform (Institutional Edition)
Main Orchestrator: app.py
"""

import streamlit as st
import pandas as pd
from src.core.config import COLORS, TABS, FINANCIAL_DEFAULTS, COMPANY_NAME
from src.core.data_loader import UniversalScreenerLoader
from src.ui.styles import apply_custom_css
from src.ui.components import UIComponents
from src.ui.sidebar import render_sidebar

# Import Tab Renderers
from src.ui.tabs.dashboard import render_dashboard
from src.ui.tabs.profitability_tab import render_profitability_tab
from src.ui.tabs.dcf_tab import render_dcf_tab
from src.ui.tabs.growth_tab import render_growth_tab
from src.ui.tabs.shareholding_tab import render_shareholding_tab

# Import Analysis Engines
from src.analysis.financial import FinancialAnalyzer
from src.analysis.eva import EVAAnalyzer

st.set_page_config(page_title=f"{COMPANY_NAME} | Analysis", page_icon="🏔️", layout="wide")
apply_custom_css()

def main():
    uploaded_file, settings = render_sidebar()
    UIComponents.header("Institutional Financial Analytics Platform")

    if uploaded_file:
        with st.spinner("🏔️ Scaling the data..."):
            loader = UniversalScreenerLoader(uploaded_file)
            processed_data, metadata = loader.get_processed_data()

        if processed_data is not None:
            # Initialize the master analyzer once for efficiency
            analyzer = FinancialAnalyzer(processed_data)
            tab_list = st.tabs(TABS)

            # --- TABS 1-3: CORE VIEW ---
            with tab_list[0]: render_dashboard(processed_data, metadata)
            with tab_list[1]: 
                st.subheader("📋 Historical Financial Statements")
                st.dataframe(processed_data.set_index('Report Date').T, width='stretch')
            with tab_list[2]: render_profitability_tab(processed_data)

            # --- TABS 4-5: VALUATION & WEALTH ---
            with tab_list[3]: render_dcf_tab(processed_data, settings)
            with tab_list[4]:
                st.subheader("💎 Economic Value Added (EVA)")
                eva_engine = EVAAnalyzer(processed_data, settings.get('wacc', 0.10))
                st.dataframe(eva_engine.calculate_eva(), width='stretch')

            # --- TABS 6-7: OPERATIONAL HEALTH ---
            with tab_list[5]:
                st.subheader("⚖️ Solvency & Capital Structure")
                st.line_chart(analyzer.get_solvency_metrics()[['Debt-to-Equity']])
                st.dataframe(analyzer.get_solvency_metrics(), width='stretch')
            with tab_list[6]:
                st.subheader("⚡ Operational Efficiency")
                st.dataframe(analyzer.get_efficiency_metrics(), width='stretch')

            # --- TABS 8-9: MOMENTUM & OWNERSHIP ---
            with tab_list[7]: 
                render_growth_tab(processed_data)
            with tab_list[8]: 
                render_shareholding_tab(processed_data)

            # --- TAB 10: RISK METRICS ---
            with tab_list[9]:
                st.subheader("🛡️ Risk & Volatility Analysis")
                from src.analysis.risk import RiskAnalyzer
                risk_engine = RiskAnalyzer(processed_data)
                st.dataframe(risk_engine.get_risk_metrics(), width='stretch')

            # --- TAB 11: PEER COMPARISON ---
            with tab_list[10]:
                st.subheader("💹 Peer Benchmarking")
                st.info("Upload multiple Screener files in the future to compare. Currently showing internal benchmarks.")
                st.bar_chart(processed_data.set_index('Report Date')['Net Margin %'])

            # --- TAB 12: EXECUTIVE SUMMARY ---
            with tab_list[11]:
                st.subheader("📝 Final Investment Thesis")
                st.write("Based on the data, here is the automated summary:")
                if processed_data['Net Profit'].iloc[-1] > processed_data['Net Profit'].iloc[-2]:
                    st.success("✅ Positive Earnings Momentum detected.")
                else:
                    st.warning("⚠️ Earnings deceleration observed in the latest period.")

        else:
            st.error("❌ Data Error: Structure mismatch.")
    else:
        st.info("👋 Please upload a Screener.in Excel file to begin.")

    UIComponents.footer()

if __name__ == "__main__":
    main()
