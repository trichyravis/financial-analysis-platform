
"""
app.py - Institutional Financial Analysis Platform
🏔️ THE MOUNTAIN PATH - World of Finance
"""

import streamlit as st
import pandas as pd
from src.core.config import COLORS, TABS, COMPANY_NAME
from src.core.data_loader import UniversalScreenerLoader
from src.ui.styles import apply_custom_css
from src.ui.components import UIComponents
from src.ui.sidebar import render_sidebar

# Import Analysis Engines
from src.analysis.financial import FinancialAnalyzer
from src.analysis.eva import EVAAnalyzer

# Import Specialized Tab Renderers
from src.ui.tabs.dashboard import render_dashboard
from src.ui.tabs.profitability_tab import render_profitability_tab
from src.ui.tabs.dcf_tab import render_dcf_tab

# 1. Page Configuration
st.set_page_config(
    page_title=f"{COMPANY_NAME} | Analysis",
    page_icon="🏔️",
    layout="wide"
)
apply_custom_css()

def main():
    # 2. Sidebar & File Upload
    uploaded_file, settings = render_sidebar()
    UIComponents.header("Institutional Financial Analytics Platform")

    if uploaded_file:
        with st.spinner("🏔️ Scaling the Data Mountain..."):
            loader = UniversalScreenerLoader(uploaded_file)
            # Unpacking the tuple (DataFrame, Metadata)
            data, metadata = loader.get_processed_data()

        if data is not None:
            # Initialize Master Analyzer
            analyzer = FinancialAnalyzer(data)
            tab_objs = st.tabs(TABS)

            # --- TAB 1: DASHBOARD ---
            with tab_objs[0]: 
                render_dashboard(data, metadata)

            # --- TAB 2: FINANCIALS ---
            with tab_objs[1]: 
                st.subheader("📋 Historical Financial Statements")
                st.dataframe(data.set_index('Report Date').T, width='stretch')

            # --- TAB 3: PROFITABILITY ---
            with tab_objs[2]: 
                render_profitability_tab(data)

            # --- TAB 4: DCF VALUATION ---
            with tab_objs[3]: 
                render_dcf_tab(data, settings)

            # --- TAB 5: EVA ANALYSIS ---
            with tab_objs[4]: 
                st.subheader("💎 Economic Value Added (EVA)")
                # Convert WACC percentage from sidebar to decimal
                wacc_decimal = settings.get('wacc', 12.0) / 100
                
                eva_engine = EVAAnalyzer(data, wacc_decimal)
                eva_results = eva_engine.calculate_eva()
                
                # Metrics Row
                e1, e2 = st.columns(2)
                latest_eva = eva_results['EVA'].iloc[-1]
                e1.metric("Latest EVA", f"₹{latest_eva:,.2f} Cr", 
                          delta="Wealth Creator" if latest_eva > 0 else "Wealth Destroyer")
                e2.metric("Latest ROIC %", f"{eva_results['ROIC %'].iloc[-1]:.2f}%")
                
                # Charts & Tables
                st.bar_chart(eva_results.set_index('Report Date')['EVA'])
                st.dataframe(eva_results.set_index('Report Date').T, width='stretch')

            # --- TAB 6: SOLVENCY ---
            with tab_objs[5]: 
                st.subheader("⚖️ Solvency & Capital Structure")
                solv = analyzer.get_solvency_metrics()
                st.line_chart(solv[['Debt-to-Equity']])
                st.dataframe(solv.T, width='stretch')

            # --- TAB 7-12: Placeholder logic ---
            # (Implemented as per previous module logic)
            for i in range(6, 12):
                with tab_objs[i]:
                    st.write(f"### {TABS[i]}")
                    st.info("Analysis module loading from processed historical data...")

        else:
            st.error("❌ Data Error: Structure mismatch. Please ensure you uploaded a Screener.in Excel.")
    else:
        st.info("👋 Welcome! Please upload a company Excel sheet from the sidebar to begin.")

    UIComponents.footer()

if __name__ == "__main__":
    main()
