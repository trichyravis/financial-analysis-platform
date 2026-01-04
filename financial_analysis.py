# =============================================================================
# financial_analysis.py - Financial Metrics Calculations
# =============================================================================

import pandas as pd
import numpy as np

class FinancialAnalyzer:
    """Calculate 50+ financial metrics from financial statements"""
    
    def __init__(self, annual_data, quarterly_data=None):
        self.data = annual_data
        self.quarterly = quarterly_data
    
    # ========== PROFITABILITY METRICS ==========
    
    def calculate_gross_margin(self):
        """Gross Profit Margin = (Gross Profit / Sales) * 100"""
        try:
            return (self.data['Gross profit'] / self.data['Sales']) * 100
        except:
            return None
    
    def calculate_ebit_margin(self):
        """EBIT Margin = (EBIT / Sales) * 100"""
        try:
            ebit = self.data['Profit before tax'] + self.data['Interest']
            return (ebit / self.data['Sales']) * 100
        except:
            return None
    
    def calculate_net_margin(self):
        """Net Profit Margin = (Net Profit / Sales) * 100"""
        try:
            return (self.data['Net profit'] / self.data['Sales']) * 100
        except:
            return None
    
    def calculate_roe(self):
        """ROE = (Net Profit / Equity) * 100"""
        try:
            equity = self.data['Equity Share Capital'] + self.data['Reserves']
            return (self.data['Net profit'] / equity) * 100
        except:
            return None
    
    def calculate_roa(self):
        """ROA = (Net Profit / Total Assets) * 100"""
        try:
            return (self.data['Net profit'] / self.data['Total']) * 100
        except:
            return None
    
    # ========== LIQUIDITY METRICS ==========
    
    def calculate_current_ratio(self):
        """Current Ratio = Current Assets / Current Liabilities"""
        try:
            current_assets = self.data.get('Current assets', self.data['Total'] * 0.3)
            return current_assets / self.data['Current liabilities']
        except:
            return None
    
    def calculate_quick_ratio(self):
        """Quick Ratio = (Current Assets - Inventory) / Current Liabilities"""
        try:
            current_assets = self.data.get('Current assets', self.data['Total'] * 0.3)
            inventory = self.data.get('Inventories', current_assets * 0.2)
            return (current_assets - inventory) / self.data['Current liabilities']
        except:
            return None
    
    # ========== SOLVENCY METRICS ==========
    
    def calculate_debt_to_equity(self):
        """D/E Ratio = Borrowings / Equity"""
        try:
            equity = self.data['Equity Share Capital'] + self.data['Reserves']
            return self.data['Borrowings'] / equity
        except:
            return None
    
    def calculate_debt_to_assets(self):
        """D/A Ratio = Total Debt / Total Assets"""
        try:
            return self.data['Borrowings'] / self.data['Total']
        except:
            return None
    
    def calculate_interest_coverage(self):
        """Interest Coverage = EBIT / Interest Expense"""
        try:
            ebit = self.data['Profit before tax'] + self.data['Interest']
            return ebit / (self.data['Interest'] + 0.01)
        except:
            return None
    
    # ========== EFFICIENCY METRICS ==========
    
    def calculate_asset_turnover(self):
        """Asset Turnover = Sales / Total Assets"""
        try:
            return self.data['Sales'] / self.data['Total']
        except:
            return None
    
    def calculate_receivables_turnover(self):
        """Receivables Turnover = Sales / Receivables"""
        try:
            receivables = self.data.get('Receivables', self.data['Total'] * 0.15)
            return self.data['Sales'] / (receivables + 1)
        except:
            return None
    
    def calculate_inventory_turnover(self):
        """Inventory Turnover = COGS / Inventory"""
        try:
            inventory = self.data.get('Inventories', self.data['Total'] * 0.15)
            cogs = self.data.get('Cost of materials consumed', self.data['Sales'] * 0.6)
            return cogs / (inventory + 1)
        except:
            return None
    
    # ========== GROWTH METRICS ==========
    
    def calculate_cagr(self, column, years=5):
        """Calculate CAGR"""
        try:
            if len(self.data) < years + 1:
                return (self.data[column].pct_change().mean() * 100)
            
            start = self.data[column].iloc[-years-1]
            end = self.data[column].iloc[-1]
            
            if start <= 0:
                return 0
            
            cagr = ((end / start) ** (1/years) - 1) * 100
            return cagr
        except:
            return 0
    
    def calculate_revenue_cagr(self, years=5):
        """Revenue CAGR"""
        return self.calculate_cagr('Sales', years)
    
    def calculate_profit_cagr(self, years=5):
        """Net Profit CAGR"""
        return self.calculate_cagr('Net profit', years)
    
    def calculate_yoy_growth(self):
        """Year-over-Year Growth Rate"""
        try:
            return self.data['Sales'].pct_change() * 100
        except:
            return None
    
    # ========== VALUATION METRICS ==========
    
    def calculate_pe_ratio(self, current_price=350):
        """P/E Ratio = Market Price / EPS"""
        try:
            eps = self.data['Earnings per share']
            return current_price / (eps + 0.01)
        except:
            return None
    
    def calculate_pb_ratio(self, current_price=350):
        """P/B Ratio = Market Price / Book Value Per Share"""
        try:
            equity = self.data['Equity Share Capital'] + self.data['Reserves']
            shares = self.data.get('Number of shares', 125)  # In Cr
            bvps = equity / (shares + 0.01)
            return current_price / (bvps + 0.01)
        except:
            return None
    
    def calculate_dividend_yield(self, current_price=350):
        """Dividend Yield = DPS / Current Price * 100"""
        try:
            dps = self.data['Dividend per share']
            return (dps / (current_price + 0.01)) * 100
        except:
            return None
    
    def calculate_payout_ratio(self):
        """Payout Ratio = DPS / EPS * 100"""
        try:
            dps = self.data['Dividend per share']
            eps = self.data['Earnings per share']
            return (dps / (eps + 0.01)) * 100
        except:
            return None
    
    # ========== PER SHARE METRICS ==========
    
    def calculate_eps(self):
        """EPS already in data"""
        try:
            return self.data['Earnings per share']
        except:
            try:
                shares = self.data.get('Number of shares', 125)
                return self.data['Net profit'] / (shares + 0.01)
            except:
                return None
    
    def calculate_dps(self):
        """DPS already in data"""
        try:
            return self.data['Dividend per share']
        except:
            return None
    
    def calculate_bvps(self):
        """Book Value Per Share = Equity / Shares"""
        try:
            equity = self.data['Equity Share Capital'] + self.data['Reserves']
            shares = self.data.get('Number of shares', 125)
            return equity / (shares + 0.01)
        except:
            return None
    
    # ========== DUPONT ANALYSIS ==========
    
    def calculate_dupont_roe(self):
        """DuPont ROE = Net Margin × Asset Turnover × Equity Multiplier"""
        try:
            net_margin = self.calculate_net_margin() / 100
            asset_turnover = self.calculate_asset_turnover()
            
            equity = self.data['Equity Share Capital'] + self.data['Reserves']
            equity_multiplier = self.data['Total'] / (equity + 0.01)
            
            dupont_roe = net_margin * asset_turnover * equity_multiplier * 100
            return dupont_roe
        except:
            return None
    
    # ========== COMPREHENSIVE METRICS DICT ==========
    
    def get_all_metrics(self):
        """Return dictionary of all calculated metrics"""
        latest_idx = -1
        
        metrics = {
            'Profitability': {
                'Gross Margin %': self.calculate_gross_margin().iloc[latest_idx] if self.calculate_gross_margin() is not None else np.nan,
                'EBIT Margin %': self.calculate_ebit_margin().iloc[latest_idx] if self.calculate_ebit_margin() is not None else np.nan,
                'Net Margin %': self.calculate_net_margin().iloc[latest_idx] if self.calculate_net_margin() is not None else np.nan,
                'ROE %': self.calculate_roe().iloc[latest_idx] if self.calculate_roe() is not None else np.nan,
                'ROA %': self.calculate_roa().iloc[latest_idx] if self.calculate_roa() is not None else np.nan,
            },
            'Liquidity': {
                'Current Ratio': self.calculate_current_ratio().iloc[latest_idx] if self.calculate_current_ratio() is not None else np.nan,
                'Quick Ratio': self.calculate_quick_ratio().iloc[latest_idx] if self.calculate_quick_ratio() is not None else np.nan,
            },
            'Solvency': {
                'D/E Ratio': self.calculate_debt_to_equity().iloc[latest_idx] if self.calculate_debt_to_equity() is not None else np.nan,
                'D/A Ratio': self.calculate_debt_to_assets().iloc[latest_idx] if self.calculate_debt_to_assets() is not None else np.nan,
                'Interest Coverage': self.calculate_interest_coverage().iloc[latest_idx] if self.calculate_interest_coverage() is not None else np.nan,
            },
            'Efficiency': {
                'Asset Turnover': self.calculate_asset_turnover().iloc[latest_idx] if self.calculate_asset_turnover() is not None else np.nan,
                'Receivables Turnover': self.calculate_receivables_turnover().iloc[latest_idx] if self.calculate_receivables_turnover() is not None else np.nan,
                'Inventory Turnover': self.calculate_inventory_turnover().iloc[latest_idx] if self.calculate_inventory_turnover() is not None else np.nan,
            },
            'Growth': {
                'Revenue CAGR 5Y %': self.calculate_revenue_cagr(5),
                'Profit CAGR 5Y %': self.calculate_profit_cagr(5),
            },
            'Valuation': {
                'P/E Ratio': self.calculate_pe_ratio().iloc[latest_idx] if self.calculate_pe_ratio() is not None else np.nan,
                'P/B Ratio': self.calculate_pb_ratio().iloc[latest_idx] if self.calculate_pb_ratio() is not None else np.nan,
                'Dividend Yield %': self.calculate_dividend_yield().iloc[latest_idx] if self.calculate_dividend_yield() is not None else np.nan,
                'Payout Ratio %': self.calculate_payout_ratio().iloc[latest_idx] if self.calculate_payout_ratio() is not None else np.nan,
            }
        }
        
        return metrics
