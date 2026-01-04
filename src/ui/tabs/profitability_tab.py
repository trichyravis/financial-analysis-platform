
import streamlit as st
import pandas as pd
from src.analysis.financial import FinancialAnalyzer

def render_profitability_tab(data):
    st.subheader("📊 Profitability & Margin Analysis")
    
    analyzer = FinancialAnalyzer(data)
    metrics_df = analyzer.get_profitability_metrics()
    
    # --- 1. Top Level Metrics (Latest Year) ---
    latest = metrics_df.iloc[-1]
    m1, m2, m3 = st.columns(3)
    
    # Net Margin metric with Delta (YoY change)
    if len(metrics_df) > 1:
        prev_margin = metrics_df['Net Margin %'].iloc[-2]
        margin_delta = latest['Net Margin %'] - prev_margin
        m1.metric("Latest Net Margin", f"{latest['Net Margin %']:.2f}%", delta=f"{margin_delta:.2f}%")
    else:
        m1.metric("Latest Net Margin", f"{latest['Net Margin %']:.2f}%")
        
    m2.metric("Latest ROE", f"{latest['ROE %']:.2f}%")
    
    if 'EBITDA Margin %' in latest:
        m3.metric("Latest EBITDA Margin", f"{latest['EBITDA Margin %']:.2f}%")

    st.divider()

    # --- 2. Margin Trends Chart ---
    st.write("#### Margin Trends Over Time (%)")
    target_cols = ['Gross Margin %', 'EBITDA Margin %', 'Net Margin %']
    available_cols = [col for col in target_cols if col in metrics_df.columns]
    
    if available_cols:
        # Use 'Year' for x-axis indexing
        chart_data = metrics_df.set_index('Year')[available_cols]
        st.area_chart(chart_data)
    else:
        st.warning("⚠️ Margin data is missing or improperly formatted in the Analysis Layer.")

    st.divider()

    # --- 3. Return Ratios Table (Institutional Layout) ---
    st.write("#### Historical Return Ratios & Efficiency")
    
    display_cols = ['Year', 'ROE %', 'Net Margin %']
    # Filter only existing columns
    valid_display = [c for c in display_cols if c in metrics_df.columns]
        
    # Transpose so years are columns (Screener.in style)
    st.dataframe(metrics_df[valid_display].set_index('Year').T, width='stretch')

    # --- 4. Institutional Insight (DuPont Perspective) ---
    with st.expander("🔍 Institutional Insight: The DuPont Analysis"):
        st.write("""
        Professional investors break down **Return on Equity (ROE)** into three levers:
        1. **Profit Margin**: How much profit is kept from every dollar of sales?
        2. **Asset Turnover**: How efficiently are assets used to generate sales?
        3. **Financial Leverage**: How much debt is used to amplify returns?
        """)
        
        # This is how you correctly include the diagram in the UI
        st.markdown("---")
        st.write("### DuPont Analysis Framework")
        # The tag below will be processed by the system to show the diagram
        #
