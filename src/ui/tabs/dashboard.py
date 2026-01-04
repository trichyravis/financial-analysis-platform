
import streamlit as st
from src.analysis.financial import FinancialAnalyzer

def render_dashboard(data, meta):
    st.subheader("📊 Executive Dashboard")
    
    # Metadata Row (Branded)
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Market Cap", f"₹{meta.get('Market Cap', 0):,.0f} Cr")
    with m2: st.metric("Current Price", f"₹{meta.get('Current Price', 0):,.2f}")
    with m3: st.metric("Total Shares", f"{meta.get('Total Shares', 0):,.2f} Cr")

    st.divider()
    
    analyzer = FinancialAnalyzer(data)
    prof = analyzer.get_profitability_metrics().iloc[-1]
    
    # 🏔️ Institutional Metric Display
    cols = st.columns(4)
    cols[0].metric("ROE %", f"{prof.get('ROE %', 0):.2f}%")
    cols[1].metric("Net Margin %", f"{prof.get('Net Margin %', 0):.2f}%")
    cols[2].metric("Sales Growth (YoY)", f"{data['Sales'].pct_change().iloc[-1]*100:.1f}%")
    cols[3].metric("Debt/Equity", f"{(data['Borrowings']/ (data['Equity Share Capital']+data['Reserves'])).iloc[-1]:.2f}x")

    st.line_chart(data.set_index('Report Date')[['Sales', 'Net Profit']])
