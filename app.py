
"""
app.py - Final Orchestrator
🏔️ THE MOUNTAIN PATH
"""
import streamlit as st
from src.core.config import TABS, COMPANY_NAME
from src.core.data_loader import UniversalScreenerLoader
from src.ui.sidebar import render_sidebar
from src.ui.styles import apply_custom_css
from src.ui.components import UIComponents

# Analysis Engines
from src.analysis.financial import FinancialAnalyzer
from src.analysis.eva import EVAAnalyzer
from src.analysis.thesis import ThesisEngine # Ensure this file exists!

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

            # TABS 0 - 7 (Previously implemented)
            with tab_objs[0]: render_dashboard(data, metadata)
            with tab_objs[1]: st.dataframe(data.set_index('Report Date').T, width='stretch')
            with tab_objs[2]: render_profitability_tab(data)
            with tab_objs[3]: render_dcf_tab(data, settings)
            with tab_objs[4]:
                wacc = settings.get('wacc', 12.0) / 100
                eva_df = EVAAnalyzer(data, wacc).calculate_eva()
                st.dataframe(eva_df.T, width='stretch')
            with tab_objs[5]: 
                st.subheader("⚖️ Solvency")
                st.dataframe(analyzer.get_solvency_metrics().T, width='stretch')
            with tab_objs[6]: render_efficiency_tab(data)
            with tab_objs[7]: render_growth_tab(data)

            # --- TAB 8: THE INVESTMENT THESIS ---
            with tab_objs[8]:
                st.subheader("📝 Final Investment Thesis")
                
                # Logic: Use Metadata for Price and Analyzer for Fundamentals
                curr_price = metadata.get('current_price', 0)
                # Note: dcf_value should be calculated in your DCF module
                dcf_value = st.session_state.get('intrinsic_value', 0) 

                engine = ThesisEngine(data, dcf_value, curr_price)
                score, checks = engine.generate_verdict()

                # Scorecard UI
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric("Mountain Quality Score", f"{score} / 3")
                
                with col2:
                    for check in checks:
                        st.write(check)

                st.divider()
                if score >= 2:
                    st.success("🏔️ **VERDICT: INVESTABLE GRADE** - Company meets high-quality criteria.")
                else:
                    st.error("🚨 **VERDICT: AVOID / MONITOR** - Fundamental or Valuation red flags detected.")

    UIComponents.footer()

if __name__ == "__main__":
    main()
