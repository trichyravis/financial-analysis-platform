import streamlit as st
from src.analysis.shareholding import CapitalAnalyzer

def render_shareholding_tab(data):
    st.subheader("🏦 Capital Structure & Equity Dilution")
    
    analyzer = CapitalAnalyzer(data)
    metrics = analyzer.get_dilution_metrics()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("#### Share Count Trend")
        st.area_chart(metrics['No. of Shares'])
    
    with col2:
        latest_change = metrics['Share Count Change %'].iloc[-1]
        if latest_change > 0:
            st.warning(f"⚠️ Equity Dilution: Share count increased by {latest_change:.2f}% last year.")
        elif latest_change < 0:
            st.success(f"💎 Buyback Alert: Share count reduced by {abs(latest_change):.2f}% last year.")
        else:
            st.info("⚖️ Stable Capital: No change in share count.")

    st.write("#### Historical Capital Base")
    st.dataframe(metrics, width='stretch')
