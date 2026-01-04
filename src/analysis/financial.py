
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        # Unpack tuple if data_loader returned (df, meta)
        if isinstance(df, tuple):
            self.df = df[0]
        else:
            self.df = df
            
        if self.df is None or self.df.empty:
            raise ValueError("Analyzer received empty or invalid DataFrame")

    def safe_get(self, col_name):
        """Standardizes metric retrieval across different company types."""
        # Mapping common variations in Screener.in names
        aliases = {
            'Sales': ['Sales', 'Revenue', 'Interest Earned', 'Turnover'],
            'Net Profit': ['Net Profit', 'Profit After Tax', 'Pat'],
            'Borrowings': ['Borrowings', 'Total Debt', 'Long Term Borrowings'],
            'Equity': ['Equity Share Capital', 'Share Capital'],
            'Raw Materials': ['Raw Material Cost', 'Cost Of Materials Consumed', 'Purchases Of Stock-In-Trade'],
            'Total Assets': ['Total Assets', 'Total Liabilities'],
            'Inventory': ['Inventory', 'Inventories'],
            'Trade Receivables': ['Trade Receivables', 'Receivables']
        }
        
        # Check for aliases if exact name isn't found
        if col_name not in self.df.columns and col_name in aliases:
            for alias in aliases[col_name]:
                if alias in self.df.columns:
                    return self.df[alias]
        
        if col_name in self.df.columns:
            return self.df[col_name]
        return pd.Series(0, index=self.df.index)

    def get_profitability_metrics(self):
        """Calculates margins and return ratios for Tab 3."""
        metrics = pd.DataFrame(index=self.df.index)
        metrics['Year'] = self.df['Report Date'] if 'Report Date' in self.df.columns else self.df.index
        
        sales = self.safe_get('Sales')
        net_profit = self.safe_get('Net Profit')
        depreciation = self.safe_get('Depreciation')
        interest = self.safe_get('Interest')
        pbt = self.safe_get('Profit Before Tax')
        
        # 1. Gross Margin Calculation
        gross_profit = self.safe_get('Gross Profit')
        if (gross_profit == 0).all():
            rm_costs = self.safe_get('Raw Materials')
            gross_profit = sales - rm_costs
            
        metrics['Gross Margin %'] = (gross_profit / sales.replace(0, np.nan)) * 100
        
        # 2. EBITDA Margin
        ebitda = pbt + depreciation + interest
        metrics['EBITDA Margin %'] = (ebitda / sales.replace(0, np.nan)) * 100
        metrics['Net Margin %'] = (net_profit / sales.replace(0, np.nan)) * 100
        
        # 3. ROE Calculation
        equity_base = self.safe_get('Equity Share Capital') + self.safe_get('Reserves')
        metrics['ROE %'] = (net_profit / equity_base.replace(0, np.nan)) * 100
        
        return metrics

    def get_solvency_metrics(self):
        """Calculates Debt-to-Equity and Interest Coverage for Tab 6."""
        solvency = pd.DataFrame(index=self.df.index)
        solvency['Year'] = self.df['Report Date'] if 'Report Date' in self.df.columns else self.df.index
        
        equity_base = self.safe_get('Equity Share Capital') + self.safe_get('Reserves')
        borrowings = self.safe_get('Borrowings')
        pbt = self.safe_get('Profit Before Tax')
        interest = self.safe_get('Interest')

        solvency['Debt-to-Equity'] = borrowings / equity_base.replace(0, np.nan)
        solvency['Interest Coverage'] = (pbt + interest) / interest.replace(0, np.nan).fillna(999)
        
        return solvency

    def get_efficiency_metrics(self):
        """Calculates Asset Turnover and Working Capital Cycles for Tab 7."""
        eff = pd.DataFrame(index=self.df.index)
        eff['Year'] = self.df['Report Date'] if 'Report Date' in self.df.columns else self.df.index
        
        sales = self.safe_get('Sales')
        assets = self.safe_get('Total Assets')
        inventory = self.safe_get('Inventory')
        debtors = self.safe_get('Trade Receivables')
        
        # Calculation with zero-division protection
        eff['Asset Turnover'] = sales / assets.replace(0, np.nan)
        eff['Inventory Turnover'] = sales / inventory.replace(0, np.nan)
        eff['Debtor Days'] = (debtors / sales.replace(0, np.nan)) * 365
        
        return eff
