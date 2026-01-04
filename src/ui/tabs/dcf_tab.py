
import streamlit as st
import pandas as pd
import plotly.express as px
from src.analysis.valuation import calculate_dcf, get_sensitivity_matrix

def render_dcf_tab(data, settings):
    """Renders the DCF Valuation interface with safety guardrails."""
    st.subheader("🎯 Intrinsic Value Estimation (DCF)")
    
    # --- 1. Inputs & Parameters ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Valuation Assumptions")
        
        # Pull WACC from sidebar settings
        wacc = settings.get('wacc', 12.0) / 100
        st.info(f"Current WACC (from sidebar): **{wacc*100:.1f}%**")

        # Growth Inputs
        growth_rate = st.slider("Step 1: 5Y Growth Rate (%)", 0.0, 50.0, 15.0) / 100
        
        # Terminal Growth should ideally be < Risk-Free Rate
        t_growth = st.slider("Step 2: Terminal Growth (%)", 0.0, 6.0, 4.0) / 100
        
        # Validation to prevent negative infinity math
        if wacc <= t_growth:
            st.error("⚠️ Error: WACC must be strictly higher than Terminal Growth to calculate Terminal Value.")
            fair_value = 0.0
        else:
            # Stage 0: FCF Proxy (Net Profit adjusted for non-cash items)
            latest_pat = data.iloc[-1].get('Net Profit', 0)
            depreciation = data.iloc[-1].get('Depreciation', 0)
            # Conservative Institutional FCF Proxy
            latest_fcf = latest_pat + (depreciation * 0.3)
            
            # --- 2. Calculation ---
            fair_value = calculate_dcf(latest_fcf, growth_rate, wacc, t_growth)

    # --- 3. Save to Session State for Thesis Tab ---
    st.session_state['intrinsic_value'] = fair_value

    with col2:
        if fair_value > 0:
            st.success(f"### Estimated Intrinsic Value: ₹{fair_value:,.2f} Cr")
            
            # Market Gap Logic
            curr_price = st.session_state.get('current_price', 0)
            if curr_price > 0:
                upside = ((fair_value / curr_price) - 1) * 100
                color = "green" if upside > 0 else "red"
                st.markdown(f"**Potential Upside:** :{color}[{upside:.1f}%]")
        else:
            st.warning("### Valuation Unavailable")
            st.write("Adjust your WACC or Growth rates to valid institutional ranges.")

        st.divider()

        # --- 4. Sensitivity Matrix ---
        st.write("#### Sensitivity Matrix (WACC vs. Growth)")
        
        # Generate ranges centered around user inputs
        wacc_range = [round(wacc + i, 3) for i in [-0.02, -0.01, 0, 0.01, 0.02]]
        growth_range = [round(growth_rate + i, 3) for i in [-0.04, -0.02, 0, 0.02, 0.04]]
        
        # Filter ranges to ensure no matrix cell breaks the math
        wacc_range = [w for w in wacc_range if w > t_growth]

        if wacc_range:
            matrix_df = get_sensitivity_matrix(latest_fcf, growth_range, wacc_range, t_growth)
            
            # Format the matrix for display (Convert to Strings for Arrow Compatibility)
            matrix_df.index = [f"{i*100:.1f}%" for i in matrix_df.index]
            matrix_df.columns = [f"{i*100:.1f}%" for i in matrix_df.columns]

            fig = px.imshow(
                matrix_df,
                text_auto=".0f",
                color_continuous_scale='RdYlGn',
                labels=dict(x="Growth Rate", y="WACC", color="Fair Value")
            )
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Sensitivity matrix hidden: WACC assumptions are too low.")

    with st.expander("📚 Understanding the DCF Math"):
        st.write("""
        The intrinsic value is calculated using a **Two-Stage Gordon Growth Model**:
        1. **Stage 1**: Free Cash Flows (FCF) are projected for 5 years and discounted.
        2. **Stage 2**: A Terminal Value is calculated to represent all flows beyond year 5.
        
        If the **WACC** (your discount rate) is lower than **Terminal Growth**, the model assumes the company grows faster than the economy forever, which results in a negative/infinite value. Professional analysts cap Terminal Growth at the Risk-Free Rate.
        """)
