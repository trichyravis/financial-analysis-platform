# =============================================================================
# EVA Analysis Module - Economic Value Added & Value Creation Analysis
# =============================================================================

import pandas as pd
import numpy as np
from scipy import stats

class EVAAnalyzer:
    """
    Complete EVA (Economic Value Added) analysis.
    Calculates value creation, ROIC, WACC, and related metrics.
    """
    
    def __init__(self, annual_data, quarterly_data=None):
        """
        Initialize with annual financial data.
        
        Required columns in annual_data:
        - Sales
        - Profit before tax (or EBIT)
        - Tax
        - Total (assets)
        - Equity Share Capital
        - Reserves
        - Borrowings
        - Interest (expense)
        - Depreciation
        """
        self.data = annual_data
        self.quarterly = quarterly_data
        
    # ========== CORE EVA CALCULATIONS ==========
    
    def calculate_nopat(self, tax_rate=None):
        """
        Calculate NOPAT (Net Operating Profit After Tax)
        NOPAT = EBIT × (1 - Tax Rate)
        
        If tax_rate not provided, calculates from data: Tax / PBT
        """
        # Calculate EBIT from PBT + Interest
        ebit = self.data['Profit before tax'] + self.data['Interest']
        
        # Calculate tax rate if not provided
        if tax_rate is None:
            # Historical tax rate = Tax / PBT
            tax_rate = (self.data['Tax'] / (self.data['Profit before tax'] + 0.1)).clip(0, 0.50)
            tax_rate_avg = tax_rate.mean()
        else:
            tax_rate_avg = tax_rate
        
        nopat = ebit * (1 - tax_rate_avg)
        return nopat, tax_rate_avg
    
    def calculate_invested_capital(self):
        """
        Calculate Invested Capital (IC)
        IC = Total Assets - Current Liabilities
        Or: IC = Equity + Net Debt
        
        Using first method (more robust)
        """
        # Simple approximation: Equity + Debt
        equity = self.data['Equity Share Capital'] + self.data['Reserves']
        debt = self.data['Borrowings']
        
        invested_capital = equity + debt
        return invested_capital
    
    def calculate_roic(self):
        """
        Calculate ROIC (Return on Invested Capital)
        ROIC = NOPAT / Invested Capital
        """
        nopat, _ = self.calculate_nopat()
        ic = self.calculate_invested_capital()
        
        roic = (nopat / ic) * 100  # As percentage
        return roic, nopat, ic
    
    def calculate_wacc(self, risk_free_rate=0.06, market_return=0.12, tax_rate=None):
        """
        Calculate WACC (Weighted Average Cost of Capital)
        WACC = (E/V × Re) + (D/V × Rd × (1 - Tc))
        
        Where:
        E/V = Equity as % of total capital
        D/V = Debt as % of total capital
        Re = Cost of Equity (CAPM)
        Rd = Cost of Debt (Interest Expense / Total Debt)
        Tc = Corporate tax rate
        """
        try:
            # Get latest year data
            equity_latest = (self.data['Equity Share Capital'] + self.data['Reserves']).iloc[-1]
            debt_latest = self.data['Borrowings'].iloc[-1]
            
            # Avoid division by zero
            if debt_latest < 10:  # Very low debt - treat as unlevered company
                debt_latest = 0
            
            total_capital = equity_latest + debt_latest
            
            if total_capital <= 0:
                return 10.0, 10.0, 5.0  # Default WACC
            
            # Weight ratios
            e_v = equity_latest / total_capital
            d_v = debt_latest / total_capital
            
            # Cost of Equity (CAPM)
            # Re = Rf + Beta × (Rm - Rf)
            # For simplicity, use market return as proxy
            beta = 1.0  # Market average
            cost_of_equity = risk_free_rate + beta * (market_return - risk_free_rate)
            
            # Cost of Debt
            if debt_latest > 0:
                cost_of_debt = (self.data['Interest'].iloc[-1] / debt_latest)
            else:
                cost_of_debt = risk_free_rate * 0.8
            
            # Tax rate
            if tax_rate is None:
                tax_rate = (self.data['Tax'] / (self.data['Profit before tax'] + 0.1)).iloc[-1]
                tax_rate = max(0, min(0.50, tax_rate))  # Clip to reasonable range
            
            # WACC
            wacc = (e_v * cost_of_equity) + (d_v * cost_of_debt * (1 - tax_rate))
            
            return wacc * 100, cost_of_equity * 100, cost_of_debt * 100
        
        except Exception as e:
            print(f"Error calculating WACC: {e}")
            return 10.0, 10.0, 5.0  # Default values
    
    def calculate_eva(self, tax_rate=None, risk_free_rate=0.06, market_return=0.12):
        """
        Calculate EVA (Economic Value Added)
        EVA = NOPAT - (Invested Capital × WACC)
        
        Returns: EVA series, capital charge, components
        """
        nopat, calc_tax_rate = self.calculate_nopat(tax_rate)
        ic = self.calculate_invested_capital()
        wacc, _, _ = self.calculate_wacc(risk_free_rate, market_return, calc_tax_rate)
        
        wacc_decimal = wacc / 100
        capital_charge = ic * wacc_decimal
        eva = nopat - capital_charge
        
        return eva, capital_charge, nopat, ic, wacc_decimal
    
    def calculate_eva_margin(self):
        """Calculate EVA Margin = EVA / Sales"""
        eva, _, _, _, _ = self.calculate_eva()
        sales = self.data['Sales']
        
        eva_margin = (eva / sales) * 100
        return eva_margin
    
    def calculate_spread(self):
        """
        Calculate ROIC - WACC Spread
        This is the value creation spread.
        Positive = Creating value
        Negative = Destroying value
        """
        roic, _, _ = self.calculate_roic()
        _, _, _ = self.calculate_wacc()
        wacc, _, _ = self.calculate_wacc()
        
        spread = roic - wacc
        return spread, roic, wacc
    
    def calculate_mva(self, market_cap, shares_outstanding=None):
        """
        Calculate MVA (Market Value Added)
        MVA = Market Capitalization - Invested Capital
        
        This shows how much value management has created above capital invested.
        """
        ic = self.calculate_invested_capital().iloc[-1]
        
        # If shares outstanding provided, calculate market cap
        if shares_outstanding and len(self.data.columns) > 0:
            if 'Current Price' in self.data.columns:
                price = self.data['Current Price'].iloc[-1]
                market_cap = (shares_outstanding / 10000000) * price  # shares in Cr
        
        mva = market_cap - ic
        mva_percentage = (mva / ic) * 100 if ic > 0 else 0
        
        return mva, mva_percentage
    
    # ========== ANALYSIS & TRENDS ==========
    
    def get_eva_trend(self):
        """Get EVA trend over years"""
        eva, capital_charge, nopat, ic, wacc = self.calculate_eva()
        
        trend_df = pd.DataFrame({
            'NOPAT': nopat,
            'Capital Charge': capital_charge,
            'EVA': eva,
            'Invested Capital': ic,
            'WACC %': wacc * 100
        })
        
        return trend_df
    
    def get_roic_trend(self):
        """Get ROIC trend over years"""
        roic, _, _ = self.calculate_roic()
        
        return roic
    
    def get_spread_trend(self):
        """Get ROIC - WACC spread over years"""
        roic, _, _ = self.calculate_roic()
        _, _, wacc_values = self.calculate_wacc()
        
        # Create WACC series for each year
        wacc_series = pd.Series(
            [self.calculate_wacc()[0]] * len(roic),  # Use latest WACC for all years
            index=roic.index
        )
        
        spread = roic - wacc_series
        
        return spread, roic, wacc_series
    
    def get_eva_drivers(self):
        """
        Identify EVA drivers and decompose value creation.
        
        EVA = NOPAT - Capital Charge
        
        Drivers:
        1. Revenue growth (increases NOPAT)
        2. Margin improvement (increases NOPAT)
        3. Capital efficiency (reduces IC or WACC)
        """
        nopat, _ = self.calculate_nopat()
        
        # Calculate year-over-year changes
        nopat_growth = nopat.pct_change() * 100
        sales_growth = self.data['Sales'].pct_change() * 100
        
        # Margin
        margins = (nopat / self.data['Sales']) * 100
        margin_change = margins.diff()
        
        # Capital efficiency
        ic = self.calculate_invested_capital()
        ic_change = ic.pct_change() * 100
        
        drivers = pd.DataFrame({
            'Sales Growth %': sales_growth,
            'NOPAT Growth %': nopat_growth,
            'Margin Change bps': margin_change * 100,
            'IC Change %': ic_change
        })
        
        return drivers
    
    def get_value_creation_ranking(self, other_analyzers_dict=None):
        """
        Rank companies by value creation metrics.
        
        other_analyzers_dict: {'Company B': analyzer_b, 'Company C': analyzer_c}
        """
        # Current company metrics
        spread, roic, wacc = self.calculate_spread()
        latest_spread = spread.iloc[-1]
        latest_roic = roic.iloc[-1]
        latest_eva, _, _, _, _ = self.calculate_eva()
        latest_eva_val = latest_eva.iloc[-1]
        
        ranking = {
            'This Company': {
                'ROIC': latest_roic,
                'WACC': wacc,
                'Spread': latest_spread,
                'EVA': latest_eva_val
            }
        }
        
        # Add other companies if provided
        if other_analyzers_dict:
            for company_name, analyzer in other_analyzers_dict.items():
                try:
                    sp, ro, wa = analyzer.calculate_spread()
                    ev, _, _, _, _ = analyzer.calculate_eva()
                    
                    ranking[company_name] = {
                        'ROIC': ro.iloc[-1],
                        'WACC': wa,
                        'Spread': sp.iloc[-1],
                        'EVA': ev.iloc[-1]
                    }
                except:
                    pass
        
        return ranking
    
    # ========== SUMMARY & INTERPRETATION ==========
    
    def get_eva_summary(self):
        """Get comprehensive EVA summary"""
        eva, capital_charge, nopat, ic, wacc = self.calculate_eva()
        roic, _, _ = self.calculate_roic()
        spread, _, _ = self.calculate_spread()
        eva_margin = self.calculate_eva_margin()
        
        latest_idx = -1
        
        summary = {
            'NOPAT (Rs. Cr)': f"{nopat.iloc[latest_idx]:.0f}",
            'Invested Capital (Rs. Cr)': f"{ic.iloc[latest_idx]:.0f}",
            'WACC (%)': f"{wacc*100:.2f}",
            'Capital Charge (Rs. Cr)': f"{capital_charge.iloc[latest_idx]:.0f}",
            'EVA (Rs. Cr)': f"{eva.iloc[latest_idx]:.0f}",
            'EVA Margin (%)': f"{eva_margin.iloc[latest_idx]:.2f}",
            'ROIC (%)': f"{roic.iloc[latest_idx]:.2f}",
            'Spread ROIC-WACC (%)': f"{spread.iloc[latest_idx]:.2f}"
        }
        
        # Value creation assessment
        if eva.iloc[latest_idx] > 0:
            assessment = "✅ Creating Value"
        else:
            assessment = "❌ Destroying Value"
        
        if roic.iloc[latest_idx] > wacc*100:
            efficiency = "✅ Return exceeds cost"
        else:
            efficiency = "❌ Return below cost"
        
        return summary, assessment, efficiency
    
    def get_interpretation(self):
        """Get EVA interpretation and insights"""
        eva, _, nopat, ic, wacc = self.calculate_eva()
        roic, _, _ = self.calculate_roic()
        spread, _, _ = self.calculate_spread()
        
        latest_eva = eva.iloc[-1]
        latest_roic = roic.iloc[-1]
        latest_wacc = wacc * 100
        latest_spread = spread.iloc[-1]
        
        insights = []
        
        # EVA assessment
        if latest_eva > 0:
            insights.append(f"✅ Creating Rs. {latest_eva:.0f} Cr of economic value")
        else:
            insights.append(f"❌ Destroying Rs. {abs(latest_eva):.0f} Cr of economic value")
        
        # ROIC assessment
        insights.append(f"📊 ROIC of {latest_roic:.1f}% vs WACC of {latest_wacc:.1f}%")
        
        # Spread assessment
        if latest_spread > 5:
            insights.append(f"⭐ Strong spread of {latest_spread:.1f}% - excellent value creation")
        elif latest_spread > 2:
            insights.append(f"✅ Moderate spread of {latest_spread:.1f}% - good value creation")
        elif latest_spread > 0:
            insights.append(f"⚠️ Weak spread of {latest_spread:.1f}% - minimal value creation")
        else:
            insights.append(f"❌ Negative spread of {latest_spread:.1f}% - value destruction")
        
        # Trend assessment
        if len(eva) > 1:
            eva_trend = eva.iloc[-1] - eva.iloc[-2]
            if eva_trend > 0:
                insights.append(f"📈 EVA improving (↑ Rs. {eva_trend:.0f} Cr YoY)")
            else:
                insights.append(f"📉 EVA declining (↓ Rs. {abs(eva_trend):.0f} Cr YoY)")
        
        return insights


# Convenience function
def get_eva_analyzer(annual_data, quarterly_data=None):
    """Factory function to create EVAAnalyzer"""
    return EVAAnalyzer(annual_data, quarterly_data)
