# profitability.py - FIXED VERSION
# Fix: Added error handling for missing 'Gross Profit' column

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def profitability_tab(data):
    """Profitability Analysis Tab - With Error Handling"""
    
    st.header("📉 Profitability Metrics")
    
    try:
        # FIXED: Check if required columns exist
        required_columns = ['Revenue', 'EBIT']
        missing_cols = [col for col in required_columns if col not in data.columns]
        
        if missing_cols:
            st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
            return
        
        # Check for optional 'Gross Profit' column
        has_gross_profit = 'Gross Profit' in data.columns
        
        if not has_gross_profit:
            st.warning("⚠️ Gross Profit data not available in the file")
            st.info("The following metrics cannot be calculated:")
            st.info("• Gross Profit Margin")
            st.info("App will display available metrics only.")
        
        # Create metrics columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Current Year")
            
            latest_year = data['Year'].max()
            latest_data = data[data['Year'] == latest_year].iloc[0]
            
            revenue = latest_data['Revenue']
            
            # Calculate EBIT Margin (always available)
            ebit = latest_data['EBIT']
            ebit_margin = (ebit / revenue) * 100
            
            st.metric("Revenue (Cr)", f"₹{revenue:,.0f}")
            st.metric("EBIT (Cr)", f"₹{ebit:,.0f}")
            st.metric("EBIT Margin %", f"{ebit_margin:.2f}%")
            
            # Only calculate Gross Profit Margin if data exists
            if has_gross_profit:
                gross_profit = latest_data['Gross Profit']
                gp_margin = (gross_profit / revenue) * 100
                st.metric("Gross Profit (Cr)", f"₹{gross_profit:,.0f}")
                st.metric("GP Margin %", f"{gp_margin:.2f}%")
        
        with col2:
            st.subheader("Trend (Last 5 Years)")
            
            # Get last 5 years of data
            data_last5 = data.tail(5).copy()
            data_last5['EBIT_Margin'] = (data_last5['EBIT'] / data_last5['Revenue']) * 100
            
            if has_gross_profit:
                data_last5['GP_Margin'] = (data_last5['Gross Profit'] / data_last5['Revenue']) * 100
                metrics_to_show = ['EBIT_Margin', 'GP_Margin']
                legend_labels = ['EBIT Margin %', 'Gross Profit Margin %']
            else:
                metrics_to_show = ['EBIT_Margin']
                legend_labels = ['EBIT Margin %']
            
            # Line chart for trends
            fig = go.Figure()
            
            for metric, label in zip(metrics_to_show, legend_labels):
                fig.add_trace(go.Scatter(
                    x=data_last5['Year'],
                    y=data_last5[metric],
                    mode='lines+markers',
                    name=label
                ))
            
            fig.update_layout(
                title="Profitability Trend",
                xaxis_title="Year",
                yaxis_title="Margin %",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.subheader("Year-on-Year Growth")
            
            # Calculate YoY changes
            if len(data) >= 2:
                latest_ebit = data['EBIT'].iloc[-1]
                previous_ebit = data['EBIT'].iloc[-2]
                ebit_growth = ((latest_ebit - previous_ebit) / abs(previous_ebit)) * 100
                
                st.metric("EBIT Growth YoY %", f"{ebit_growth:.2f}%")
                
                if has_gross_profit:
                    latest_gp = data['Gross Profit'].iloc[-1]
                    previous_gp = data['Gross Profit'].iloc[-2]
                    gp_growth = ((latest_gp - previous_gp) / abs(previous_gp)) * 100
                    st.metric("Gross Profit Growth %", f"{gp_growth:.2f}%")
            else:
                st.info("Need at least 2 years of data to calculate growth")
        
        # Detailed analysis table
        st.subheader("📊 Historical Profitability Analysis")
        
        analysis_data = data[['Year', 'Revenue', 'EBIT']].copy()
        analysis_data['EBIT Margin %'] = (analysis_data['EBIT'] / analysis_data['Revenue']) * 100
        
        if has_gross_profit:
            analysis_data['Gross Profit'] = data['Gross Profit']
            analysis_data['GP Margin %'] = (data['Gross Profit'] / analysis_data['Revenue']) * 100
        
        # Format for display
        for col in analysis_data.columns:
            if col != 'Year' and '%' not in col:
                analysis_data[col] = analysis_data[col].apply(lambda x: f"₹{x:,.0f}")
            elif '%' in col:
                analysis_data[col] = analysis_data[col].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(analysis_data, use_container_width=True)
        
        # Summary
        st.success("✅ Profitability metrics calculated successfully")
        if not has_gross_profit:
            st.caption("*Note: Some metrics excluded due to missing data in source file*")
    
    except KeyError as e:
        st.error(f"❌ Missing required column: {str(e)}")
        st.info("Please ensure Excel file includes: Year, Revenue, EBIT columns")
    except Exception as e:
        st.error(f"❌ Error in profitability calculation: {str(e)}")
        st.info("Check that all data is numeric and properly formatted")
