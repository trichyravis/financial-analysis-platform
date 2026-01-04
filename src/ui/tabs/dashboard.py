
import streamlit as st
from src.analysis.financial import FinancialAnalyzer

def render_dashboard(data):
    st.subheader("📊 Executive Summary")
    
    analyzer = FinancialAnalyzer(data)
    
    # These calls will now succeed
    prof_metrics = analyzer.get_profitability_metrics().iloc[-1]
    solv_metrics = analyzer.get_solvency_metrics().iloc[-1]
    
    # 🏔️ Mountain Path Branded Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Latest Sales", f"₹{data.iloc[-1].get('Sales', 0):,.0f} Cr")
    with col2:
        st.metric("Net Margin", f"{prof_metrics['Net Margin %']:.2f}%")
    with col3:
        st.metric("ROE", f"{prof_metrics['ROE %']:.2f}%")
    with col4:
        st.metric("Debt-to-Equity", f"{solv_metrics['Debt-to-Equity']:.2f}x")

    st.divider()
    
    # Visualizing the 10-year trend
    st.subheader("📈 Financial Performance Trend")
    chart_data = data[['Report Date', 'Sales', 'Net Profit']].set_index('Report Date')
    st.line_chart(chart_data)
