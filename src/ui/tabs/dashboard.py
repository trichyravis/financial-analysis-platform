
import streamlit as st
from src.core.utils import format_indian_currency
from src.analysis.financial import FinancialAnalyzer

def render_dashboard(data):
    """Renders the Executive Summary dashboard."""
    st.subheader("📊 Executive Summary")
    
    analyzer = FinancialAnalyzer(data)
    metrics = analyzer.get_profitability_metrics().iloc[-1] # Latest year
    solvency = analyzer.get_solvency_metrics().iloc[-1]
    
    # Branded Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Latest Revenue", format_indian_currency(data.iloc[-1]['Sales']))
    with col2:
        st.metric("Net Profit Margin", f"{metrics['Net Margin %']:.2f}%")
    with col3:
        st.metric("ROE %", f"{metrics['ROE %']:.2f}%")
    with col4:
        st.metric("Debt-to-Equity", f"{solvency['Debt-to-Equity']:.2f}x")

    st.divider()
    
    # Financial Trend Chart
    st.subheader("📈 Revenue & Profit Trend")
    chart_data = data[['Report Date', 'Sales', 'Net Profit']].set_index('Report Date')
    st.line_chart(chart_data)
