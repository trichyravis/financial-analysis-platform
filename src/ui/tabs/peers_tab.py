import streamlit as st
import pandas as pd
import plotly.express as px

def render_peers_tab(data):
    st.subheader("💹 Peer & Historical Benchmarking")
    
    # 1. Historical Median Comparison
    metrics = ['Net Margin %', 'ROE %', 'Sales']
    latest = data.iloc[-1]
    median = data[metrics].median()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Current vs. 10Y Median")
        comp_df = pd.DataFrame({
            'Metric': metrics,
            'Current': [latest['Net Margin %'], latest['ROE %'], "Latest"],
            '10Y Median': [median['Net Margin %'], median['ROE %'], "Average"]
        })
        st.table(comp_df)

    with col2:
        st.write("#### Margin Consistency")
        fig = px.box(data, y="Net Margin %", points="all", title="Margin Dispersion (10 Years)")
        st.plotly_chart(fig, theme="streamlit")

    st.info("💡 Note: For direct competitor comparison, upload a 'Peer Comparison' CSV from Screener.in.")
