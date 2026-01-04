import streamlit as st
import pandas as pd
import plotly.express as px
from src.analysis.growth import GrowthAnalyzer

def render_growth_tab(data):
    st.subheader("📈 Compounded Growth Analysis (CAGR)")
    
    analyzer = GrowthAnalyzer(data)
    growth_df = analyzer.get_growth_summary()
    
    # 1. Growth Metric Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("3Y Sales CAGR", f"{growth_df.loc['Sales', '3Y CAGR']:.2f}%")
    with col2:
        st.metric("5Y Sales CAGR", f"{growth_df.loc['Sales', '5Y CAGR']:.2f}%")
    with col3:
        st.metric("10Y Sales CAGR", f"{growth_df.loc['Sales', '10Y CAGR']:.2f}%")

    st.divider()

    # 2. Detailed Growth Table
    st.write("#### Detailed Historical CAGR Summary")
    st.table(growth_df.style.format("{:.2f}%", na_rep="-"))

    # 3. Growth Momentum Chart
    st.write("#### Sales & Profit Momentum")
    momentum_df = data.set_index('Report Date')[['Sales', 'Net Profit']]
    st.line_chart(momentum_df)
