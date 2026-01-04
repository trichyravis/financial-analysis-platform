
"""
app.py - Final Institutional Edition
🏔️ THE MOUNTAIN PATH
"""
import streamlit as st
import pandas as pd
from src.core.config import TABS, COMPANY_NAME, COLORS
from src.core.data_loader import UniversalScreenerLoader
from src.ui.sidebar import render_sidebar
from src.ui.styles import apply_custom_css
from src.ui.components import UIComponents

# Analysis Engines
from src.analysis.financial import FinancialAnalyzer
from src.analysis.eva import EVAAnalyzer
from src.analysis.thesis import ThesisEngine

# Tab Modules
from src.ui.tabs.dashboard import render_dashboard
from src.ui.tabs.profitability_tab import render_profitability_tab
from src.ui.tabs.dcf_tab import render_dcf_tab
from src.ui.tabs.efficiency_tab import render_efficiency_tab
from src.ui.tabs.growth_tab import render_growth_tab

st.set_page_config(page_title=COMPANY_NAME, layout="wide")

def main():
    apply_custom_css()
    uploaded_file, settings = render_sidebar()
    UIComponents.header("Institutional Financial Analytics")

    if uploaded_file:
        loader = UniversalScreenerLoader(uploaded_file)
        data, metadata = loader.get_processed_data()

        if data is not None:
            analyzer = FinancialAnalyzer(data)
            tab_objs = st.tabs(TABS)

            # --- TAB 1: DASHBOARD ---
            with tab_objs[0]: 
                render_dashboard(data, metadata)

            # --- TAB 2: FINANCIALS (With Arrow Fix) ---
            with tab_objs[1]: 
                st.subheader("📋 Historical Financial Statements")
                f_df = data.set_index('Report Date').T
                f_df.index = f_df.index.astype(str) # ARROW FIX
                st.dataframe(f_df, width='stretch')

            # --- TAB 3: PROFITABILITY ---
            with tab_objs[2]: 
                render_profitability_tab(data)

            # --- TAB 4: DCF VALUATION ---
            with tab_objs[3]: 
                render_dcf_tab(data, settings)

            # --- TAB 5: EVA ---
            with tab_objs[4]:
                wacc = settings.get('wacc', 12.0) / 100
                eva_df = EVAAnalyzer(data, wacc).calculate_eva()
                st.dataframe(eva_df.T, width='stretch')

            # --- TAB 6: SOLVENCY ---
            with tab_objs[5]: 
                solv = analyzer.get_solvency_metrics().T
                solv.index = solv.index.astype(str) # ARROW FIX
                st.dataframe(solv, width='stretch')

            # --- TAB 7: EFFICIENCY ---
            with tab_objs[6]: 
                render_efficiency_tab(data)

            # --- TAB 8: GROWTH ---
            with tab_objs[7]: 
                render_growth_tab(data)

            # --- TAB 9: THESIS (Dynamic Decision) ---
            with tab_objs[8]:
                st.subheader("📝 Final Investment Thesis")
                curr_price = metadata.get('current_price', 0)
                # Retrieves the value saved by the DCF Tab
                dcf_val = st.session_state.get('intrinsic_value', 0) 

                engine = ThesisEngine(data, dcf_val, curr_price)
                score, checks = engine.generate_verdict()

                c1, c2 = st.columns([1, 2])
                c1.metric("Mountain Score", f"{score} / 3")
                with c2:
                    for check in checks: st.write(check)

                if score >= 2:
                    st.success("🏔️ **VERDICT: INVESTABLE GRADE**")
                else:
                    st.error("🚨 **VERDICT: AVOID / WATCHLIST**")

    UIComponents.footer()

if __name__ == "__main__":
    main()
