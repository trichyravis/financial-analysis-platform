
"""
🏔️ THE MOUNTAIN PATH - World of Finance
Final Orchestrated app.py
Institutional Financial Analysis Platform
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
from src.analysis.growth import GrowthAnalyzer
from src.analysis.risk import RiskAnalyzer

# Import Specialized Tab Renderers
from src.ui.tabs.dashboard import render_dashboard
from src.ui.tabs.profitability_tab import render_profitability_tab
from src.ui.tabs.dcf_tab import render_dcf_tab
from src.ui.tabs.growth_tab import render_growth_tab
from src.ui.tabs.shareholding_tab import render_shareholding_tab

# 1. Page Configuration
st.set_page_config(page_title=f"{COMPANY_NAME} | Analysis", page_icon="🏔️", layout="wide")
apply_custom_css()

def main():
    # 2. Sidebar & File Upload
    uploaded_file, settings = render_sidebar()
    UIComponents.header("Institutional Financial Analytics Platform")

    if uploaded_file:
        with st.spinner("🏔️ Scaling the Data Mountain..."):
            loader = UniversalScreenerLoader(uploaded_file)
            # Standard Unpacking of (DataFrame, Metadata)
            data, metadata = loader.get_processed_data()

        if data is not None:
            # 3. Initialize Master Analyzer
            analyzer = FinancialAnalyzer(data)
            tab_objs = st.tabs(TABS)

            # --- TABS 1-3: CORE METRICS ---
            with tab_objs[0]: 
                render_dashboard(data, metadata)
            with tab_objs[1]: 
                st.subheader("📋 Historical Financial Statements")
                st.dataframe(data.set_index('Report Date').T, width='stretch')
            with tab_objs[2]: 
                render_profitability_tab(data)

            # --- TABS 4-5: VALUATION & WEALTH ---
            with tab_objs[3]: 
                render_dcf_tab(data, settings)
            with tab_objs[4]: 
                st.subheader("💎 Economic Value Added (EVA)")
                eva_calc = EVAAnalyzer(data, settings.get('wacc', 0.12))
                st.dataframe(eva_calc.calculate_eva(), width='stretch')

            # --- TABS 6-7: OPERATIONAL HEALTH ---
            with tab_objs[5]: 
                st.subheader("⚖️ Solvency & Capital Structure")
                solv = analyzer.get_solvency_metrics()
                st.line_chart(solv[['Debt-to-Equity']])
                st.dataframe(solv, width='stretch')
            with tab_objs[6]: 
                st.subheader("⚡ Operational Efficiency")
                st.dataframe(analyzer.get_efficiency_metrics(), width='stretch')

            # --- TABS 8-9: GROWTH & CAPITAL ---
            with tab_objs[7]: 
                render_growth_tab(data)
            with tab_objs[8]: 
                render_shareholding_tab(data)

            # --- TAB 10: RISK ASSESSMENT ---
            with tab_objs[9]:
                st.subheader("🛡️ Risk & Volatility Profile")
                risk_engine = RiskAnalyzer(data)
                st.table(risk_engine.get_risk_metrics())

            # --- TAB 11: PEER BENCHMARKING ---
            with tab_objs[10]:
                st.subheader("💹 Peer Comparison")
                # Showing internal Margin vs ROE scatter
                prof = analyzer.get_profitability_metrics()
                st.scatter_chart(prof, x='Net Margin %', y='ROE %')

            # --- TAB 12: INVESTMENT THESIS ---
            with tab_objs[11]:
                st.subheader("📝 Summary Thesis")
                latest_pate = data['Net Profit'].iloc[-1]
                avg_pat = data['Net Profit'].mean()
                if latest_pat > avg_pat:
                    st.success(f"🏔️ The company is currently performing above its historical average. Wealth creation potential is High.")
                else:
                    st.warning(f"⚠️ Performance is lagging historical averages. Caution advised.")

        else:
            st.error("❌ Data structure mismatch. Please use a standard Screener.in export.")
    else:
        st.info("👋 Welcome! Please upload a company Excel sheet to begin your journey.")

    UIComponents.footer()

if __name__ == "__main__":
    main()
