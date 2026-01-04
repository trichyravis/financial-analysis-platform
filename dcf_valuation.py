# =============================================================================
# DCF Valuation Module - Free Cash Flow to Firm Valuation
# =============================================================================

import pandas as pd
import numpy as np

class DCFValuation:
    """
    Complete DCF valuation using Free Cash Flow to Firm (FCFF) method.
    
    DCF Value = Σ(FCF / (1+WACC)^t) + Terminal Value / (1+WACC)^n
    
    Where:
    FCF = Free Cash Flow = NOPAT + Depreciation - CapEx - Change in WC
    WACC = Discount rate
    Terminal Value = FCF_terminal × (1 + g) / (WACC - g)
    """
    
    def __init__(self, annual_data, quarterly_data=None):
        """Initialize with financial data"""
        self.data = annual_data
        self.quarterly = quarterly_data
        self.projections = None
        
    # ========== HISTORICAL CALCULATIONS ==========
    
    def calculate_historical_fcf(self):
        """
        Calculate historical Free Cash Flow
        FCF = Operating Cash Flow - Capital Expenditure
        Or: FCF = NOPAT + D&A - CapEx - Change in WC
        """
        # Method 1: Using cash flow statement (preferred)
        try:
            ocf = self.data['Cash from Operating Activity']
            
            # CapEx estimated from investing activity
            investing = self.data['Cash from Investing Activity']
            capex = -investing.clip(upper=0)  # Only positive investing outflows are CapEx
            
            fcf = ocf - capex
            return fcf
        
        except:
            # Method 2: Calculate from components
            try:
                # NOPAT
                ebit = self.data['Profit before tax'] + self.data['Interest']
                tax_rate = (self.data['Tax'] / (self.data['Profit before tax'] + 0.1)).mean()
                nopat = ebit * (1 - tax_rate)
                
                # Add back depreciation
                depreciation = self.data.get('Depreciation', pd.Series([0]*len(self.data)))
                
                # CapEx (approximate from change in fixed assets)
                # This is simplified - uses depreciation as proxy
                capex = depreciation * 1.2  # Assumption
                
                # Change in Working Capital (approximate)
                change_wc = pd.Series([0]*len(self.data))  # Simplified
                
                fcf = nopat + depreciation - capex - change_wc
                return fcf
            
            except:
                return None
    
    def calculate_growth_rates(self, years=5):
        """
        Calculate historical growth rates.
        Returns: (revenue_growth, fcf_growth, overall_growth)
        """
        sales = self.data['Sales']
        fcf = self.calculate_historical_fcf()
        
        if fcf is None or len(sales) < 2:
            return 0.08, 0.08, 0.08  # Default 8%
        
        # Calculate CAGR
        def calc_cagr(series, periods=5):
            if len(series) < periods + 1 or series.iloc[0] <= 0:
                return series.pct_change().mean()
            
            start = series.iloc[-periods-1]
            end = series.iloc[-1]
            return ((end / start) ** (1/periods) - 1) if start > 0 else 0.08
        
        rev_growth = calc_cagr(sales, years)
        fcf_growth = calc_cagr(fcf, years)
        
        # Use average or conservative estimate
        overall = (rev_growth + fcf_growth) / 2
        overall = min(0.15, max(0.02, overall))  # Clip to 2-15%
        
        return rev_growth, fcf_growth, overall
    
    # ========== PROJECTION & ASSUMPTION SETTING ==========
    
    def create_projections(self, 
                          revenue_growth=None,
                          terminal_growth=0.025,
                          ebit_margin=None,
                          tax_rate=None,
                          capex_pct_sales=0.035,
                          wc_change_pct_sales=0.005,
                          projection_years=5,
                          wacc=0.10):
        """
        Create 5-year FCF projections.
        
        Parameters:
        - revenue_growth: Annual revenue growth % (if None, uses historical)
        - terminal_growth: Perpetual growth rate (typically 2-3%)
        - ebit_margin: Operating margin % (if None, uses historical average)
        - tax_rate: Tax rate % (if None, calculates from data)
        - capex_pct_sales: CapEx as % of sales
        - wc_change_pct_sales: Working capital change as % of sales
        - projection_years: Years to project (default 5)
        - wacc: Discount rate for DCF
        """
        
        # Get historical data
        latest_sales = self.data['Sales'].iloc[-1]
        latest_fcf = self.calculate_historical_fcf().iloc[-1] if self.calculate_historical_fcf() is not None else latest_sales * 0.15
        
        # Set defaults if not provided
        if revenue_growth is None:
            _, _, revenue_growth = self.calculate_growth_rates()
        
        if ebit_margin is None:
            ebit = self.data['Profit before tax'] + self.data['Interest']
            ebit_margin = (ebit / self.data['Sales']).mean()
        
        if tax_rate is None:
            tax_rate = (self.data['Tax'] / (self.data['Profit before tax'] + 0.1)).mean()
            tax_rate = max(0, min(0.50, tax_rate))
        
        # Create projection DataFrame
        years = np.arange(1, projection_years + 1)
        projections = pd.DataFrame(index=years)
        
        # Project revenue
        projections['Revenue'] = latest_sales * ((1 + revenue_growth) ** years)
        
        # Project EBIT
        projections['EBIT'] = projections['Revenue'] * ebit_margin
        
        # Project NOPAT
        projections['NOPAT'] = projections['EBIT'] * (1 - tax_rate)
        
        # Add back depreciation (approximate as % of sales)
        depreciation_pct = (self.data['Depreciation'] / self.data['Sales']).mean()
        projections['Depreciation'] = projections['Revenue'] * depreciation_pct
        
        # CapEx
        projections['CapEx'] = projections['Revenue'] * capex_pct_sales
        
        # Change in Working Capital
        projections['Change in WC'] = projections['Revenue'] * wc_change_pct_sales
        
        # Free Cash Flow = NOPAT + D&A - CapEx - Change in WC
        projections['FCF'] = (projections['NOPAT'] + 
                            projections['Depreciation'] - 
                            projections['CapEx'] - 
                            projections['Change in WC'])
        
        # Discount factors
        projections['Discount Factor'] = 1 / ((1 + wacc) ** years)
        
        # Present Value of FCF
        projections['PV of FCF'] = projections['FCF'] * projections['Discount Factor']
        
        self.projections = projections
        self.wacc = wacc
        self.terminal_growth = terminal_growth
        self.tax_rate = tax_rate
        
        return projections
    
    # ========== VALUATION CALCULATIONS ==========
    
    def calculate_terminal_value(self):
        """
        Calculate Terminal Value using Gordon Growth Model.
        TV = FCF_Year5 × (1 + g) / (WACC - g)
        
        Where g = perpetual growth rate (typically 2-3%)
        """
        if self.projections is None:
            return None
        
        fcf_terminal = self.projections['FCF'].iloc[-1]
        
        if self.wacc <= self.terminal_growth:
            # Prevent division by zero
            return fcf_terminal * 30  # Simplified approximation
        
        terminal_value = (fcf_terminal * (1 + self.terminal_growth)) / (self.wacc - self.terminal_growth)
        
        return terminal_value
    
    def calculate_enterprise_value(self):
        """
        Calculate Enterprise Value.
        EV = PV of FCF (projection period) + PV of Terminal Value
        """
        if self.projections is None:
            return None, None, None
        
        # PV of explicit projection period
        pv_fcf = self.projections['PV of FCF'].sum()
        
        # Terminal Value and its PV
        tv = self.calculate_terminal_value()
        discount_factor_tv = 1 / ((1 + self.wacc) ** len(self.projections))
        pv_tv = tv * discount_factor_tv
        
        # Enterprise Value
        ev = pv_fcf + pv_tv
        
        return ev, pv_fcf, pv_tv
    
    def calculate_equity_value(self, total_debt, cash_and_equivalents):
        """
        Calculate Equity Value.
        Equity Value = Enterprise Value - Net Debt
        Net Debt = Total Debt - Cash & Equivalents
        """
        ev, _, _ = self.calculate_enterprise_value()
        
        if ev is None:
            return None
        
        net_debt = total_debt - cash_and_equivalents
        equity_value = ev - net_debt
        
        return equity_value
    
    def calculate_fair_value_per_share(self, shares_outstanding, total_debt, cash_and_equivalents):
        """
        Calculate Fair Value Per Share.
        Fair Value = Equity Value / Shares Outstanding
        """
        equity_value = self.calculate_equity_value(total_debt, cash_and_equivalents)
        
        if equity_value is None or equity_value <= 0:
            return None
        
        fair_value = equity_value / shares_outstanding
        
        return fair_value
    
    def calculate_upside_downside(self, current_price, fair_value):
        """
        Calculate Upside/Downside vs Current Price.
        Returns: (upside_pct, assessment)
        """
        if fair_value is None or current_price <= 0:
            return None, "N/A"
        
        upside = ((fair_value - current_price) / current_price) * 100
        
        if upside > 20:
            assessment = "🟢 Strong Buy (>20% upside)"
        elif upside > 10:
            assessment = "🟢 Buy (10-20% upside)"
        elif upside > 0:
            assessment = "🟡 Hold (0-10% upside)"
        elif upside > -10:
            assessment = "🟡 Sell (-10-0% downside)"
        else:
            assessment = "🔴 Strong Sell (<-10% downside)"
        
        return upside, assessment
    
    # ========== SENSITIVITY ANALYSIS ==========
    
    def sensitivity_analysis(self, 
                            wacc_range=(0.08, 0.12, 0.01),
                            growth_range=(0.020, 0.035, 0.005)):
        """
        Create sensitivity table for fair value.
        Varies WACC and Terminal Growth Rate.
        
        Returns: sensitivity_matrix
        """
        wacc_values = np.arange(wacc_range[0], wacc_range[1] + wacc_range[2], wacc_range[2])
        growth_values = np.arange(growth_range[0], growth_range[1] + growth_range[2], growth_range[2])
        
        sensitivity = pd.DataFrame(index=wacc_values, columns=growth_values)
        
        # Store original parameters
        orig_wacc = self.wacc
        orig_growth = self.terminal_growth
        
        for wacc in wacc_values:
            for growth in growth_values:
                try:
                    # Recalculate projections with different assumptions
                    self.create_projections(
                        wacc=wacc,
                        terminal_growth=growth,
                        projection_years=5
                    )
                    
                    # Get fair value (needs company-specific data)
                    ev, _, _ = self.calculate_enterprise_value()
                    sensitivity.loc[wacc, growth] = ev if ev else np.nan
                
                except:
                    sensitivity.loc[wacc, growth] = np.nan
        
        # Restore original parameters
        self.wacc = orig_wacc
        self.terminal_growth = orig_growth
        
        return sensitivity.astype(float)
    
    # ========== SCENARIO ANALYSIS ==========
    
    def scenario_analysis(self, scenarios_dict):
        """
        Analyze multiple scenarios with different assumptions.
        
        scenarios_dict: {
            'Bull': {'revenue_growth': 0.12, 'ebit_margin': 0.22, 'wacc': 0.09},
            'Base': {'revenue_growth': 0.08, 'ebit_margin': 0.20, 'wacc': 0.10},
            'Bear': {'revenue_growth': 0.04, 'ebit_margin': 0.18, 'wacc': 0.11}
        }
        """
        scenario_results = {}
        
        for scenario_name, assumptions in scenarios_dict.items():
            try:
                self.create_projections(
                    revenue_growth=assumptions.get('revenue_growth'),
                    ebit_margin=assumptions.get('ebit_margin'),
                    wacc=assumptions.get('wacc'),
                    terminal_growth=assumptions.get('terminal_growth', 0.025)
                )
                
                ev, pv_fcf, pv_tv = self.calculate_enterprise_value()
                
                scenario_results[scenario_name] = {
                    'Enterprise Value': ev,
                    'PV of FCF': pv_fcf,
                    'PV of Terminal Value': pv_tv,
                    'Assumptions': assumptions
                }
            
            except Exception as e:
                scenario_results[scenario_name] = {'Error': str(e)}
        
        return scenario_results
    
    # ========== SUMMARY & REPORTING ==========
    
    def get_dcf_summary(self, shares_outstanding, current_price, total_debt, cash):
        """Get comprehensive DCF summary"""
        ev, pv_fcf, pv_tv = self.calculate_enterprise_value()
        equity_value = self.calculate_equity_value(total_debt, cash)
        fair_value = self.calculate_fair_value_per_share(shares_outstanding, total_debt, cash)
        upside, assessment = self.calculate_upside_downside(current_price, fair_value)
        
        summary = {
            'Enterprise Value (Rs. Cr)': f"{ev:,.0f}",
            'PV of FCF (5Y)': f"{pv_fcf:,.0f}",
            'PV of Terminal Value': f"{pv_tv:,.0f}",
            'Less: Net Debt': f"{total_debt - cash:,.0f}",
            'Equity Value (Rs. Cr)': f"{equity_value:,.0f}",
            'Shares Outstanding (Cr)': f"{shares_outstanding:.2f}",
            'Fair Value Per Share (Rs.)': f"{fair_value:.2f}",
            'Current Price (Rs.)': f"{current_price:.2f}",
            'Upside/(Downside) %': f"{upside:.1f}%",
            'Investment Verdict': assessment,
            'WACC Used': f"{self.wacc*100:.1f}%",
            'Terminal Growth': f"{self.terminal_growth*100:.1f}%"
        }
        
        return summary


# Convenience function
def get_dcf_analyzer(annual_data, quarterly_data=None):
    """Factory function to create DCF analyst"""
    return DCFValuation(annual_data, quarterly_data)
