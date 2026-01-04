
import streamlit as st
from src.analysis.financial import FinancialAnalyzer

def render_profitability_tab(data):
    st.subheader("📊 Profitability & Margin Analysis")
    
    analyzer = FinancialAnalyzer(data)
    metrics_df = analyzer.get_profitability_metrics()
    
    # --- Margin Trends ---
    st.write("#### Margin Trends (%)")
    
    # List of columns we WANT to show
    target_cols = ['Gross Margin %', 'EBITDA Margin %', 'Net Margin %']
    
    # Safety Check: Only use columns that actually exist in metrics_df
    available_cols = [col for col in target_cols if col in metrics_df.columns]
    
    if available_cols:
        # Use metrics_df['Year'] for the x-axis
        chart_data = metrics_df.set_index('Year')[available_cols]
        st.area_chart(chart_data)
    else:
        st.error("Could not find required margin columns in processed data.")

    st.divider()
    
    # --- Return Ratios ---
    st.write("#### Historical Return Ratios")
    st.dataframe(metrics_df[['Year', 'ROE %']].set_index('Year').T, width='stretch')
