
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
            'Sales': ['Sales', 'Revenue', 'Interest Earned'],
            'Net Profit': ['Net Profit', 'Profit After Tax', 'Pat'],
            'Borrowings': ['Borrowings', 'Total Debt'],
            'Equity': ['Equity Share Capital', 'Share Capital']
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
        """Amended to include EBITDA and Operating Margins."""
        metrics = pd.DataFrame(index=self.df.index)
        metrics['Year'] = self.df.get('Report Date', self.df.index)
        
        sales = self.safe_get('Sales')
        net_profit = self.safe_get('Net Profit')
        depreciation = self.safe_get('Depreciation')
        interest = self.safe_get('Interest')
        pbt = self.safe_get('Profit Before Tax')
        
        # EBITDA Calculation (PBT + Depreciation + Interest)
        ebitda = pbt + depreciation + interest
        metrics['EBITDA Margin %'] = (ebitda / sales.replace(0, np.nan)) * 100
        metrics['Net Margin %'] = (net_profit / sales.replace(0, np.nan)) * 100
        
        # ROE Calculation
        equity = self.safe_get('Equity Share Capital') + self.safe_get('Reserves')
        metrics['ROE %'] = (net_profit / equity.replace(0, np.nan)) * 100
        
        return metrics

    def get_solvency_metrics(self):
        """Calculates Debt-to-Equity and Interest Coverage."""
        solvency = pd.DataFrame(index=self.df.index)
        
        equity = self.safe_get('Equity Share Capital') + self.safe_get('Reserves')
        borrowings = self.safe_get('Borrowings')
        pbt = self.safe_get('Profit Before Tax')
        interest = self.safe_get('Interest')

        solvency['Debt-to-Equity'] = borrowings / equity.replace(0, np.nan)
        # 999 is an institutional shorthand for 'Infinity' (Debt Free)
        solvency['Interest Coverage'] = (pbt + interest) / interest.replace(0, np.nan).fillna(999)
        
        return solvency

    def get_efficiency_metrics(self):
        """Added Efficiency logic for Tab 7."""
        efficiency = pd.DataFrame(index=self.df.index)
        
        sales = self.safe_get('Sales')
        total_assets = self.safe_get('Total Assets')
        receivables = self.safe_get('Trade Receivables')
        
        efficiency['Asset Turnover'] = sales / total_assets.replace(0, np.nan)
        
        # Debtor Days: (Receivables / Sales) * 365
        efficiency['Debtor Days'] = (receivables / sales.replace(0, np.nan)) * 365
        
        return efficiency
