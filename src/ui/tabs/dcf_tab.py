
import streamlit as st
import pandas as pd
import plotly.express as px
from src.analysis.valuation import calculate_dcf, get_sensitivity_matrix

def render_dcf_tab(data, settings):
    """Renders the DCF Valuation interface with Sensitivity Analysis."""
    st.subheader("🎯 Intrinsic Value Estimation (DCF)")
    
    # 1. VALUATION INPUTS
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Valuation Inputs")
        # Growth and Terminal assumptions
        growth_input = st.slider("Next 5Y Growth Rate (%)", 0.0, 40.0, 15.0) / 100
        t_growth = st.slider("Terminal Growth (%)", 0.0, 7.0, 4.0) / 100
        
        # Pull WACC from sidebar settings (provided via app.py)
        wacc = settings.get('wacc', 12.0) / 100

    # 2. FCF LOGIC
    # Institutional approach: FCF = Net Profit + Depreciation - CapEx
    # If CapEx is not available, we fall back to a conservative Net Profit proxy
    latest_pat = data.iloc[-1].get('Net Profit', 0)
    depreciation = data.iloc[-1].get('Depreciation', 0)
    # Standard assumption: CapEx ≈ Depreciation for steady-state, or use actuals
    latest_fcf = latest_pat + (depreciation * 0.2) # 20% add-back proxy for conservative FCF

    # 3. CALCULATION
    fair_value = calculate_dcf(latest_fcf, growth_input, wacc, t_growth)
    
    # --- CRITICAL: Save to Session State for Thesis Tab ---
    st.session_state['intrinsic_value'] = fair_value

    with col2:
        st.success(f"### Estimated Intrinsic Value: ₹{fair_value:,.2f} Cr")
        
        # Dynamic Market Gap Analysis
        curr_price = st.session_state.get('current_price', 0) 
        if curr_price > 0:
            upside = ((fair_value / curr_price) - 1) * 100
            color = "green" if upside > 0 else "red"
            st.markdown(f"**Market Gap:** :{color}[{upside:.1f}% Upside/Downside]")

        # 4. SENSITIVITY MATRIX
        st.write("#### Sensitivity Analysis (WACC vs Growth)")
        
        # Generate ranges around the current inputs
        wacc_range = [round(wacc + i, 3) for i in [-0.02, -0.01, 0, 0.01, 0.02]]
        growth_range = [round(growth_input + i, 3) for i in [-0.04, -0.02, 0, 0.02, 0.04]]
        
        matrix_df = get_sensitivity_matrix(latest_fcf, growth_range, wacc_range, t_growth)
        
        # Plotly Heatmap
        fig = px.imshow(
            matrix_df, 
            text_auto=".0f", 
            color_continuous_scale='RdYlGn',
            labels=dict(x="Growth Rate (%)", y="WACC (%)", color="Fair Value")
        )
        # 2026 Compliance: width='stretch' instead of use_container_width
        st.plotly_chart(fig, width='stretch')

    st.info("💡 **Institutional Note:** The DCF value is highly sensitive to WACC and Terminal Growth. Use the Sensitivity Matrix to find a 'Margin of Safety'.")
