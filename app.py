
"""
🏔️ THE MOUNTAIN PATH - World of Finance
Institutional Financial Analysis Platform
Final Orchestrated app.py
"""

import streamlit as st
import pandas as pd

# Core Configuration & UI
from src.core.config import COLORS, TABS, COMPANY_NAME, TAGLINE
from src.core.data_loader import UniversalScreenerLoader
from src.ui.styles import apply_custom_css
from src.ui.components import UIComponents
from src.ui.sidebar import render_sidebar

# Analysis Engines
from src.analysis.financial import FinancialAnalyzer
from src.analysis.eva import EVAAnalyzer
from src.analysis.growth import GrowthAnalyzer
from src.analysis.thesis import ThesisEngine

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

def format_df_for_streamlit(df):
    """Fixes ArrowTypeError by ensuring string indices and columns."""
    temp_df = df.copy()
    temp_df.index = temp_df.index.astype(str)
    temp_df.columns = temp_df.columns.astype(str)
    return temp_df

def main():
    # 1. Apply UI Branding
    apply_custom_css()

    # 2. Sidebar Implementation
    uploaded_file, settings = render_sidebar()

    # 3. Main Hero Header (Dark Blue Background Fix)
    st.markdown(f'''
        <div class="main-header">
            <h1>{COMPANY_NAME}</h1>
            <p style="color:white; opacity: 0.9;">{TAGLINE} | Prof. V. Ravichandran</p>
        </div>
    ''', unsafe_allow_html=True)

    if uploaded_file:
        with st.spinner("🏔️ Scaling the Data..."):
            loader = UniversalScreenerLoader(uploaded_file)
            data, metadata = loader.get_processed_data()

        if data is not None:
            analyzer = FinancialAnalyzer(data)
            tab_objs = st.tabs(TABS)

            # --- TAB 0: DASHBOARD ---
            with tab_objs[0]:
                render_dashboard(data, metadata)

            # --- TAB 1: FINANCIALS (Arrow Fix) ---
            with tab_objs[1]:
                st.subheader("📋 Historical Financial Statements")
                f_df = data.set_index('Report Date').T
                st.dataframe(format_df_for_streamlit(f_df), width='stretch')

            # --- TAB 2: PROFITABILITY ---
            with tab_objs[2]:
                render_profitability_tab(data)

            # --- TAB 3: DCF VALUATION ---
            with tab_objs[3]:
                render_dcf_tab(data, settings)

            # --- TAB 4: EVA ANALYSIS (Arrow Fix) ---
            with tab_objs[4]:
                st.subheader("💎 Economic Value Added (EVA)")
                wacc_dec = settings.get('wacc', 12.0) / 100
                eva_engine = EVAAnalyzer(data, wacc_dec)
                eva_df = eva_engine.calculate_eva()
                
                st.bar_chart(eva_df.set_index('Report Date')['EVA'])
                st.dataframe(format_df_for_streamlit(eva_df.set_index('Report Date').T), width='stretch')

            # --- TAB 5: SOLVENCY ---
            with tab_objs[5]:
                st.subheader("⚖️ Solvency Ratios")
                solv_df = analyzer.get_solvency_metrics()
                st.line_chart(solv_df.set_index('Year')['Debt-to-Equity'])
                st.dataframe(format_df_for_streamlit(solv_df.set_index('Year').T), width='stretch')

            # --- TAB 6: EFFICIENCY ---
            with tab_objs[6]:
                render_efficiency_tab(data)

            # --- TAB 7: GROWTH ---
            with tab_objs[7]:
                render_growth_tab(data)

            # --- TAB 8: FINAL THESIS ---
            with tab_objs[8]:
                st.subheader("📝 Final Investment Thesis")
                curr_price = metadata.get('current_price', 0)
                dcf_val = st.session_state.get('intrinsic_value', 0)

                engine = ThesisEngine(data, dcf_val, curr_price)
                score, checks = engine.generate_verdict()

                c1, c2 = st.columns([1, 2])
                c1.metric("Mountain Score", f"{score} / 3")
                with c2:
                    for check in checks:
                        st.write(check)

                st.divider()
                if score >= 2:
                    st.success("🏔️ **VERDICT: INVESTABLE GRADE**")
                else:
                    st.error("🚨 **VERDICT: AVOID / MONITOR**")

        else:
            st.error("❌ Data error: Structure mismatch.")
    else:
        # Welcome Screen
        st.info("👋 Welcome! Please upload a company Excel sheet from the sidebar to begin.")

    UIComponents.footer()

if __name__ == "__main__":
    main()
