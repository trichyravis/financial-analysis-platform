
"""
🏔️ THE MOUNTAIN PATH - World of Finance
Financial Analysis Platform - UPDATED WITH UNIVERSAL SCREENER.IN LOADER

Complete fixed version with:
- Universal data loader for any Screener.in Excel file
- Automatic column detection and parsing
- 9 tabs (removed Segments, Elasticity, Institutional)
- Proper error handling
- Professional UI
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import tempfile
from screener_data_loader import ScreenerDataLoader, load_screener_file

# Page configuration
st.set_page_config(
    page_title="The Mountain Path - Financial Analysis",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding
st.markdown("""
    <style>
        .main {
            padding: 20px;
        }
        h1 {
            color: #003366;
            border-bottom: 3px solid #FFD700;
            padding-bottom: 10px;
        }
        .metric-box {
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #003366;
        }
        .success-box {
            background-color: #e8f5e9;
            padding: 10px;
            border-radius: 5px;
        }
        .warning-box {
            background-color: #fff3e0;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - File Upload & Company Selection
# ============================================================================

with st.sidebar:
    st.markdown("### 🏔️ THE MOUNTAIN PATH")
    st.markdown("**World of Finance**")
    st.divider()
    
    st.subheader("📁 Upload Financial Data")
    st.markdown("""
    Download Excel from **[Screener.in](https://www.screener.in/)** and upload here.
    
    **Steps:**
    1. Go to screener.in
    2. Search for a company
    3. Download Excel
    4. Upload here
    
    ✨ *No manual column renaming needed!*
    """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose Excel file from Screener.in",
        type=['xlsx', 'xls'],
        help="Standard Screener.in format - Works with any company!"
    )
    
    data = None
    if uploaded_file is not None:
        try:
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name
            
            # Load using universal loader
            loader = ScreenerDataLoader(tmp_path)
            data = loader.get_data()
            
            # Display summary
            summary = loader.get_summary()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Company", summary['company'][:15])
            with col2:
                st.metric("Rows", summary['rows'])
            with col3:
                st.metric("Columns", summary['columns'])
            with col4:
                st.metric("Years", summary['years'])
            
            # Show available columns
            with st.expander("📊 Available Columns"):
                st.write(summary['columns_list'])
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("Make sure file is downloaded from Screener.in")
            st.stop()
    else:
        st.info("📤 Upload an Excel file from Screener.in to begin")
        st.stop()

# ============================================================================
# MAIN CONTENT - Dashboard & Analysis Tabs
# ============================================================================

st.title("🏔️ THE MOUNTAIN PATH - Financial Analysis Platform")
st.markdown("**Advanced Financial Analysis & Valuation Dashboard**")
st.divider()

# Check data quality
if data is None or len(data) == 0:
    st.error("❌ No data available. Please upload a valid file.")
    st.stop()

# ============================================================================
# CREATE TABS (9 tabs - removed Segments, Elasticity, Institutional)
# ============================================================================

tabs = st.tabs([
    "📊 Dashboard",
    "📈 Financials",
    "📉 Profitability",
    "💧 Liquidity",
    "💎 Valuation",
    "🎯 DCF Valuation",
    "💰 EVA Analysis",
    "💎 Value Creation"
])

# ============================================================================
# TAB 0: DASHBOARD
# ============================================================================

with tabs[0]:
    st.header("📊 Dashboard")
    
    # Check if file has essential data
    if 'Revenue' not in data.columns:
        st.error("❌ Revenue data not found in file")
    else:
        # Latest metrics
        col1, col2, col3, col4 = st.columns(4)
        
        latest_year = data['Year'].max()
        latest_data = data[data['Year'] == latest_year].iloc[0]
        
        with col1:
            st.metric("Latest Year", f"{int(latest_year)}")
        
        with col2:
            st.metric("Revenue (Cr)", f"₹{latest_data['Revenue']:,.0f}")
        
        with col3:
            if 'EBIT' in data.columns:
                st.metric("EBIT (Cr)", f"₹{latest_data['EBIT']:,.0f}")
            else:
                st.info("EBIT data not available")
        
        with col4:
            if 'Net Income' in data.columns:
                st.metric("Net Income (Cr)", f"₹{latest_data['Net Income']:,.0f}")
            else:
                st.info("Net Income data not available")
        
        st.divider()
        
        # Revenue & Profit Trends
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Revenue Trend")
            try:
                import plotly.graph_objects as go
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data['Year'],
                    y=data['Revenue'],
                    mode='lines+markers',
                    name='Revenue',
                    line=dict(color='#003366', width=3)
                ))
                fig.update_layout(
                    height=400,
                    hovermode='x unified',
                    yaxis_title="Revenue (Cr)",
                    xaxis_title="Year"
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display chart: {str(e)}")
        
        with col2:
            st.subheader("💰 Net Profit Trend")
            if 'Net Income' in data.columns:
                try:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=data['Year'],
                        y=data['Net Income'],
                        mode='lines+markers',
                        name='Net Income',
                        line=dict(color='#FFD700', width=3)
                    ))
                    fig.update_layout(
                        height=400,
                        hovermode='x unified',
                        yaxis_title="Net Income (Cr)",
                        xaxis_title="Year"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not display chart: {str(e)}")
            else:
                st.info("Net Income data not available")
        
        st.divider()
        
        # Data Table
        st.subheader("📋 Historical Data")
        st.dataframe(data, use_container_width=True)

# ============================================================================
# TAB 1: FINANCIALS
# ============================================================================

with tabs[1]:
    st.header("📈 Financials")
    st.info("Complete financial statement analysis")
    
    try:
        if 'Revenue' not in data.columns:
            st.error("❌ Revenue data not found")
        else:
            col1, col2, col3 = st.columns(3)
            
            latest_year = data['Year'].max()
            latest_data = data[data['Year'] == latest_year].iloc[0]
            
            with col1:
                st.metric("Revenue (Latest)", f"₹{latest_data['Revenue']:,.0f}")
                if 'EBIT' in data.columns:
                    st.metric("EBIT", f"₹{latest_data['EBIT']:,.0f}")
            
            with col2:
                if 'Net Income' in data.columns:
                    st.metric("Net Income", f"₹{latest_data['Net Income']:,.0f}")
                if 'Depreciation' in data.columns:
                    st.metric("Depreciation", f"₹{latest_data['Depreciation']:,.0f}")
            
            with col3:
                if 'Total Assets' in data.columns:
                    st.metric("Total Assets", f"₹{latest_data['Total Assets']:,.0f}")
                if 'Equity' in data.columns:
                    st.metric("Equity", f"₹{latest_data['Equity']:,.0f}")
            
            st.divider()
            st.subheader("📊 Financial Data Table")
            st.dataframe(data, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error loading financials: {str(e)}")

# ============================================================================
# TAB 2: PROFITABILITY
# ============================================================================

with tabs[2]:
    st.header("📉 Profitability Metrics")
    
    try:
        if 'Revenue' not in data.columns or 'EBIT' not in data.columns:
            st.error("❌ Missing required columns: Revenue, EBIT")
        else:
            col1, col2, col3 = st.columns(3)
            
            latest_year = data['Year'].max()
            latest_data = data[data['Year'] == latest_year].iloc[0]
            revenue = latest_data['Revenue']
            ebit = latest_data['EBIT']
            
            with col1:
                st.subheader("📊 Current Year Margins")
                st.metric("EBIT Margin %", f"{(ebit/revenue)*100:.2f}%")
            
            with col2:
                st.subheader("📈 5-Year Trend")
                data_5y = data.tail(5).copy()
                data_5y['EBIT_Margin'] = (data_5y['EBIT'] / data_5y['Revenue']) * 100
                
                try:
                    import plotly.graph_objects as go
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=data_5y['Year'],
                        y=data_5y['EBIT_Margin'],
                        mode='lines+markers',
                        name='EBIT Margin %'
                    ))
                    fig.update_layout(height=400, hovermode='x unified')
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not display chart: {str(e)}")
            
            with col3:
                st.subheader("📊 Year-on-Year Change")
                if len(data) >= 2:
                    latest_ebit = data['EBIT'].iloc[-1]
                    previous_ebit = data['EBIT'].iloc[-2]
                    ebit_growth = ((latest_ebit - previous_ebit) / abs(previous_ebit)) * 100
                    st.metric("EBIT Growth YoY %", f"{ebit_growth:.2f}%")
                else:
                    st.info("Need 2+ years of data for growth calculation")
            
            st.divider()
            st.subheader("📋 Profitability Analysis")
            analysis_df = data[['Year', 'Revenue', 'EBIT']].copy()
            analysis_df['EBIT Margin %'] = (analysis_df['EBIT'] / analysis_df['Revenue']) * 100
            st.dataframe(analysis_df, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error in profitability analysis: {str(e)}")

# ============================================================================
# TAB 3: LIQUIDITY
# ============================================================================

with tabs[3]:
    st.header("💧 Liquidity Metrics")
    
    try:
        has_current_assets = 'Current Assets' in data.columns
        has_current_liabilities = 'Current Liabilities' in data.columns
        
        if has_current_assets and has_current_liabilities:
            col1, col2 = st.columns(2)
            
            latest_year = data['Year'].max()
            latest_data = data[data['Year'] == latest_year].iloc[0]
            
            with col1:
                st.subheader("💰 Liquidity Ratios")
                ca = latest_data['Current Assets']
                cl = latest_data['Current Liabilities']
                cr = ca / cl
                st.metric("Current Ratio", f"{cr:.2f}")
            
            with col2:
                st.subheader("📊 Trend")
                st.info("Liquidity metrics ready for analysis")
        else:
            st.warning("⚠️ Current Assets or Current Liabilities not in file")
            st.info("These columns are optional for basic analysis")
    
    except Exception as e:
        st.error(f"❌ Error in liquidity analysis: {str(e)}")

# ============================================================================
# TAB 4: VALUATION
# ============================================================================

with tabs[4]:
    st.header("💎 Valuation Multiples")
    
    try:
        st.info("Valuation metrics available")
        
        if len(data) > 0:
            latest_year = data['Year'].max()
            latest_data = data[data['Year'] == latest_year].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Latest Year", f"{int(latest_year)}")
                if 'Net Income' in data.columns:
                    st.metric("Net Income", f"₹{latest_data['Net Income']:,.0f}")
            
            with col2:
                if 'Revenue' in data.columns:
                    st.metric("Revenue", f"₹{latest_data['Revenue']:,.0f}")
            
            with col3:
                if 'Net Income' in data.columns and 'Revenue' in data.columns:
                    nm = (latest_data['Net Income'] / latest_data['Revenue']) * 100
                    st.metric("Net Margin %", f"{nm:.2f}%")
    
    except Exception as e:
        st.error(f"❌ Error in valuation analysis: {str(e)}")

# ============================================================================
# TAB 5: DCF VALUATION
# ============================================================================

with tabs[5]:
    st.header("🎯 DCF Valuation - Fair Value Calculation")
    
    try:
        if 'Revenue' not in data.columns:
            st.error("❌ Revenue data required for DCF valuation")
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("📊 Assumptions")
                
                # FIXED: All values are floats (add .0)
                revenue_growth = st.slider(
                    "Revenue Growth %",
                    min_value=5.0,
                    max_value=30.0,
                    step=0.5,
                    value=15.0,
                    format="%.1f"
                )
                
                ebit_margin = st.slider(
                    "EBIT Margin %",
                    min_value=5.0,
                    max_value=30.0,
                    step=0.5,
                    value=15.0,
                    format="%.1f"
                )
                
                wacc = st.slider(
                    "WACC %",
                    min_value=5.0,
                    max_value=15.0,
                    step=0.5,
                    value=8.0,
                    format="%.1f"
                )
                
                terminal_growth = st.slider(
                    "Terminal Growth %",
                    min_value=2.0,
                    max_value=4.0,
                    step=0.5,
                    value=3.0,
                    format="%.1f"
                )
            
            with col2:
                st.subheader("💰 Current Metrics")
                
                latest_year = data['Year'].max()
                latest_revenue = data[data['Year'] == latest_year]['Revenue'].values[0]
                if 'EBIT' in data.columns:
                    latest_ebit = data[data['Year'] == latest_year]['EBIT'].values[0]
                    ebit_margin_current = (latest_ebit / latest_revenue) * 100
                else:
                    ebit_margin_current = ebit_margin
                
                st.metric("Latest Revenue (Cr)", f"₹{latest_revenue:,.0f}")
                st.metric("Current EBIT Margin", f"{ebit_margin_current:.1f}%")
            
            with col3:
                st.subheader("📈 DCF Result")
                
                # Simple DCF calculation
                projected_revenues = []
                projected_fcf = []
                
                for year in range(1, 6):
                    proj_revenue = latest_revenue * ((1 + revenue_growth/100) ** year)
                    proj_fcf = proj_revenue * (ebit_margin / 100) * 0.75
                    projected_revenues.append(proj_revenue)
                    projected_fcf.append(proj_fcf)
                
                # PV calculation
                pv_fcf = sum([fcf / ((1 + wacc/100) ** (i+1)) for i, fcf in enumerate(projected_fcf)])
                terminal_fcf = projected_fcf[-1] * (1 + terminal_growth/100)
                terminal_value = terminal_fcf / ((wacc/100) - (terminal_growth/100))
                pv_terminal = terminal_value / ((1 + wacc/100) ** 5)
                enterprise_value = pv_fcf + pv_terminal
                
                st.success(f"✅ Enterprise Value: ₹{enterprise_value:,.0f} Cr")
                st.info(f"PV of FCF: ₹{pv_fcf:,.0f} Cr")
                st.info(f"PV Terminal: ₹{pv_terminal:,.0f} Cr")
            
            st.divider()
            st.subheader("📊 5-Year DCF Projection")
            
            projection_data = {
                'Year': list(range(1, 6)),
                'Revenue (Cr)': [f"₹{rev:,.0f}" for rev in projected_revenues],
                'FCF (Cr)': [f"₹{fcf:,.0f}" for fcf in projected_fcf],
            }
            
            df_projection = pd.DataFrame(projection_data)
            st.dataframe(df_projection, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error in DCF valuation: {str(e)}")

# ============================================================================
# TAB 6: EVA ANALYSIS
# ============================================================================

with tabs[6]:
    st.header("💰 EVA Analysis")
    st.info("Economic Value Added (EVA) analysis measures the true profitability of your investment.")
    
    try:
        if 'Net Income' not in data.columns:
            st.error("❌ Net Income data required for EVA analysis")
        else:
            st.subheader("📊 EVA Metrics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("EVA Analysis metrics available")
            
            with col2:
                latest_year = data['Year'].max()
                latest_data = data[data['Year'] == latest_year].iloc[0]
                
                net_income = latest_data['Net Income']
                st.metric("Net Income (Latest)", f"₹{net_income:,.0f}")
            
            st.divider()
            st.dataframe(data, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error in EVA analysis: {str(e)}")

# ============================================================================
# TAB 7: VALUE CREATION
# ============================================================================

with tabs[7]:
    st.header("💎 Value Creation Analysis")
    st.info("Analyze how the company creates value through revenue growth and margin expansion.")
    
    try:
        if 'Revenue' not in data.columns or 'Net Income' not in data.columns:
            st.error("❌ Revenue and Net Income data required")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Revenue Growth")
                data_copy = data.copy()
                data_copy['Revenue_YoY'] = data_copy['Revenue'].pct_change() * 100
                
                try:
                    import plotly.graph_objects as go
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=data_copy['Year'],
                        y=data_copy['Revenue_YoY'],
                        name='Revenue Growth %'
                    ))
                    fig.update_layout(height=400, hovermode='x unified')
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not display chart: {str(e)}")
            
            with col2:
                st.subheader("💰 Profitability Growth")
                data_copy['NI_YoY'] = data_copy['Net Income'].pct_change() * 100
                
                try:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=data_copy['Year'],
                        y=data_copy['NI_YoY'],
                        name='Net Income Growth %'
                    ))
                    fig.update_layout(height=400, hovermode='x unified')
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not display chart: {str(e)}")
            
            st.divider()
            st.subheader("📊 Value Creation Metrics")
            
            analysis_df = data[['Year', 'Revenue', 'Net Income']].copy()
            analysis_df['Revenue Growth %'] = analysis_df['Revenue'].pct_change() * 100
            analysis_df['NI Growth %'] = analysis_df['Net Income'].pct_change() * 100
            analysis_df['Net Margin %'] = (analysis_df['Net Income'] / analysis_df['Revenue']) * 100
            
            st.dataframe(analysis_df, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error in value creation analysis: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
**🏔️ THE MOUNTAIN PATH - World of Finance**

*Advanced Financial Analysis Platform*

**Author:** Prof. V. Ravichandran  
**Experience:** 28+ Years Corporate Finance & Banking | 10+ Years Academic Excellence

**Disclaimer:** This analysis is for educational purposes only. Consult a financial advisor before making investment decisions.

*Built with Streamlit | Powered by Python & Pandas*
""")
