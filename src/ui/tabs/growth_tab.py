
import streamlit as st
from src.analysis.growth import GrowthAnalyzer

def render_growth_tab(data):
    st.subheader("🚀 Growth Momentum")
    analyzer = GrowthAnalyzer(data)
    growth_df = analyzer.get_growth_summary()

    # CAGR Summary Cards
    c1, c2, c3 = st.columns(3)
    c1.metric("3Y Sales CAGR", f"{growth_df.loc['Sales', '3Y CAGR']:.2f}%")
    c2.metric("5Y Sales CAGR", f"{growth_df.loc['Sales', '5Y CAGR']:.2f}%")
    c3.metric("10Y Sales CAGR", f"{growth_df.loc['Sales', '10Y CAGR']:.2f}%")

    st.divider()
    
    # Historical Sales & Profit Growth
    st.write("#### Revenue vs. Profit Growth (YoY)")
    growth_plot = data.set_index('Report Date')[['Sales', 'Net Profit']].pct_change() * 100
    st.line_chart(growth_plot)
