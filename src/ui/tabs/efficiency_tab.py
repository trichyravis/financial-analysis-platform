import streamlit as st
from src.analysis.financial import FinancialAnalyzer

def render_efficiency_tab(data):
    st.subheader("⚡ Operational Efficiency")
    
    analyzer = FinancialAnalyzer(data)
    eff_df = analyzer.get_efficiency_metrics()

    # Metric Cards for latest year
    latest = eff_df.iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("Asset Turnover", f"{latest['Asset Turnover']:.2f}x")
    c2.metric("Inventory Turnover", f"{latest['Inventory Turnover']:.2f}x")
    c3.metric("Debtor Days", f"{int(latest['Debtor Days'])} Days")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.write("#### Asset Utilization Trend")
        # Ensure 'Year' is the index for the chart
        st.line_chart(eff_df.set_index('Year')['Asset Turnover'])
    
    with col2:
        st.write("#### Working Capital Cycle (Days)")
        st.bar_chart(eff_df.set_index('Year')['Debtor Days'])

    st.write("#### Efficiency Data Table")
    st.dataframe(eff_df.set_index('Year').T, width='stretch')
