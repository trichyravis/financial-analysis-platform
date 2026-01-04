
import streamlit as st
import pandas as pd
from src.analysis.growth import GrowthAnalyzer

def render_growth_tab(data):
    st.subheader("📈 Compounded Growth Analysis")
    
    analyzer = GrowthAnalyzer(data)
    growth_df = analyzer.get_growth_summary()
    
    if not growth_df.empty:
        st.write("#### CAGR Performance (%)")
        st.table(growth_df.style.format("{:.2f}%", na_rep="-"))
        
        st.write("#### Growth Visualizer")
        st.line_chart(data.set_index('Report Date')[['Sales', 'Net Profit']])
    else:
        st.warning("Insufficient historical data to calculate CAGR.")
