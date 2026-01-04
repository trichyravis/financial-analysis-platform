
import streamlit as st
import pandas as pd
from src.analysis.valuation import calculate_dcf, get_sensitivity_matrix
import plotly.express as px

def render_dcf_tab(data, settings):
    """Renders the DCF Valuation interface with Sensitivity Analysis."""
    st.subheader("🎯 Intrinsic Value Estimation (DCF)")
    
    # Input parameters
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Valuation Inputs")
        growth = st.slider("5Y Growth Rate (%)", 0.0, 30.0, 15.0) / 100
        t_growth = st.slider("Terminal Growth (%)", 0.0, 7.0, 4.0) / 100
        
    latest_fcf = data.iloc[-1]['Net Profit'] # Simplified FCF for example
    fair_value = calculate_dcf(latest_fcf, growth, settings['wacc'], t_growth)
    
    with col2:
        st.success(f"### Estimated Intrinsic Value: {fair_value:,.2f} Cr")
        
        # Sensitivity Matrix Visualization
        st.write("#### Sensitivity Analysis (WACC vs Growth)")
        wacc_range = [0.08, 0.09, 0.10, 0.11, 0.12]
        growth_range = [0.10, 0.12, 0.15, 0.18, 0.20]
        
        matrix_df = get_sensitivity_matrix(latest_fcf, growth_range, wacc_range, t_growth)
        fig = px.imshow(matrix_df, text_auto=True, color_continuous_scale='RdYlGn',
                        labels=dict(x="Growth Rate", y="WACC", color="Fair Value"))
        st.plotly_chart(fig, use_container_width=True)
