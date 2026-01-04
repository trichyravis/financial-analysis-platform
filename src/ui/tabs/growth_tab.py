
import streamlit as st
from src.analysis.growth import GrowthAnalyzer

def render_growth_tab(data):
    st.subheader("🚀 Growth Momentum")
    
    analyzer = GrowthAnalyzer(data)
    growth_df = analyzer.get_growth_summary()

    if not growth_df.empty:
        st.write("#### Compounded Annual Growth Rates (%)")
        st.table(growth_df.style.format("{:.2f}%"))
        
        st.divider()
        st.write("#### Historical Sales vs Profit Growth")
        # Plotting raw values to show scale of growth
        st.line_chart(data.set_index('Report Date')[['Sales', 'Net Profit']])
    else:
        st.warning("Insufficient historical data to calculate CAGR metrics.")
