
# DCF Valuation Module - FIXED VERSION
# Fix: All slider values changed from int to float to match step parameter

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def dcf_valuation_tab(data):
    """DCF Valuation - Fair Value Calculation"""
    
    st.header("🎯 DCF Valuation - Fair Value Calculation")
    
    try:
        # Validate required columns
        required_cols = ['Revenue', 'EBIT', 'Net Income']
        missing_cols = [col for col in required_cols if col not in data.columns]
        
        if missing_cols:
            st.warning(f"⚠️ Missing columns: {', '.join(missing_cols)}")
            st.info("DCF valuation requires: Revenue, EBIT, Net Income")
            return
        
        # Create three columns for inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📊 Assumptions")
            
            # FIXED: Changed all values from int to float (add .0)
            revenue_growth = st.slider(
                "Revenue Growth %",
                min_value=5.0,      # Changed from 5 to 5.0
                max_value=30.0,     # Changed from 30 to 30.0
                step=0.5,
                value=15.0,         # Changed from 15 to 15.0
                format="%.1f"
            )
            
            ebit_margin = st.slider(
                "EBIT Margin %",
                min_value=5.0,      # Changed from 5 to 5.0
                max_value=30.0,     # Changed from 30 to 30.0
                step=0.5,
                value=15.0,         # Changed from 15 to 15.0
                format="%.1f"
            )
            
            wacc = st.slider(
                "WACC %",
                min_value=5.0,      # Changed from 5 to 5.0
                max_value=15.0,     # Changed from 15 to 15.0
                step=0.5,
                value=8.0,          # Changed from 8 to 8.0
                format="%.1f"
            )
            
            nwc_change_percent = st.slider(
                "NWC Change %",
                min_value=1.0,      # Changed from 1 to 1.0
                max_value=5.0,      # Changed from 5 to 5.0
                step=0.5,
                value=2.0,          # Changed from 2 to 2.0
                format="%.1f"
            )
            
            terminal_growth = st.slider(
                "Terminal Growth %",
                min_value=2.0,      # Changed from 2 to 2.0
                max_value=4.0,      # Changed from 4 to 4.0
                step=0.5,
                value=3.0,          # Changed from 3 to 3.0
                format="%.1f"
            )
        
        with col2:
            st.subheader("💰 Current Metrics")
            
            # Get latest year data
            latest_year = data['Year'].max()
            latest_revenue = data[data['Year'] == latest_year]['Revenue'].values[0]
            latest_ebit = data[data['Year'] == latest_year]['EBIT'].values[0]
            
            st.metric("Latest Revenue (Cr)", f"₹{latest_revenue:,.0f}")
            st.metric("Latest EBIT (Cr)", f"₹{latest_ebit:,.0f}")
            st.metric("EBIT Margin", f"{(latest_ebit/latest_revenue)*100:.1f}%")
        
        with col3:
            st.subheader("📈 Projections")
            
            # Simple DCF calculation
            if latest_revenue > 0:
                projected_revenues = []
                projected_fcf = []
                
                for year in range(1, 6):
                    proj_revenue = latest_revenue * ((1 + revenue_growth/100) ** year)
                    proj_ebit = proj_revenue * (ebit_margin / 100)
                    proj_fcf = proj_ebit * 0.75  # Simplified FCF
                    
                    projected_revenues.append(proj_revenue)
                    projected_fcf.append(proj_fcf)
                
                # Calculate PV of FCFs
                pv_fcf = sum([fcf / ((1 + wacc/100) ** (i+1)) for i, fcf in enumerate(projected_fcf)])
                
                # Terminal value
                terminal_fcf = projected_fcf[-1] * (1 + terminal_growth/100)
                terminal_value = terminal_fcf / ((wacc/100) - (terminal_growth/100))
                pv_terminal = terminal_value / ((1 + wacc/100) ** 5)
                
                # Enterprise value
                enterprise_value = pv_fcf + pv_terminal
                
                st.metric("Year 1 Revenue", f"₹{projected_revenues[0]:,.0f}")
                st.metric("PV of FCFs", f"₹{pv_fcf:,.0f}")
                st.metric("PV Terminal Value", f"₹{pv_terminal:,.0f}")
                st.metric("Enterprise Value", f"₹{enterprise_value:,.0f}")
        
        # Detailed projection table
        st.subheader("📊 5-Year DCF Projection")
        
        projection_data = {
            'Year': list(range(1, 6)),
            'Revenue (Cr)': [f"₹{rev:,.0f}" for rev in projected_revenues],
            'EBIT Margin %': [f"{ebit_margin:.1f}%"] * 5,
            'EBIT (Cr)': [f"₹{rev * (ebit_margin/100):,.0f}" for rev in projected_revenues],
            'FCF (Cr)': [f"₹{fcf:,.0f}" for fcf in projected_fcf],
        }
        
        df_projection = pd.DataFrame(projection_data)
        st.dataframe(df_projection, use_container_width=True)
        
        # Summary section
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"✅ **Enterprise Value: ₹{enterprise_value:,.0f} Cr**")
            st.info(f"Based on {revenue_growth}% revenue growth and {wacc}% WACC")
        
        with col2:
            # Fair value per share (simplified)
            if latest_revenue > 0:
                fair_value = enterprise_value / (latest_revenue / 1000)  # Simplified
                st.warning(f"⚠️ **Fair Value (Estimated): ₹{fair_value:,.0f}**")
                st.caption("*Simplified calculation - consult financial advisor*")
    
    except KeyError as e:
        st.error(f"❌ Missing required column: {str(e)}")
        st.info("Please ensure Excel has: Revenue, EBIT, Net Income columns")
    except Exception as e:
        st.error(f"❌ Error in DCF calculation: {str(e)}")
        st.info("Check that all data is numeric and valid")
