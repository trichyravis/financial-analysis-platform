
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        # Safety check: if df is a tuple (data, meta), take only the data
        if isinstance(df, tuple):
            self.df = df[0]
        else:
            self.df = df
            
        # Ensure the index is valid
        if self.df is None or self.df.empty:
            raise ValueError("Analyzer received empty or invalid DataFrame")

    def safe_get(self, col_name):
        """Returns column data or zeros if column is missing."""
        if col_name in self.df.columns:
            return self.df[col_name]
        return pd.Series(0, index=self.df.index)

    def get_profitability_metrics(self):
        metrics = pd.DataFrame(index=self.df.index)
        metrics['Year'] = self.df.get('Report Date', self.df.index)
        
        sales = self.safe_get('Sales')
        net_profit = self.safe_get('Net Profit')
        
        # Calculate Margin
        metrics['Net Margin %'] = (net_profit / sales.replace(0, np.nan)) * 100
        
        # ROE = Net Profit / (Equity + Reserves)
        equity = self.safe_get('Equity Share Capital') + self.safe_get('Reserves')
        metrics['ROE %'] = (net_profit / equity.replace(0, np.nan)) * 100
        return metrics

    def get_solvency_metrics(self):
        """The missing method causing your AttributeError."""
        solvency = pd.DataFrame(index=self.df.index)
        
        equity = self.safe_get('Equity Share Capital') + self.safe_get('Reserves')
        borrowings = self.safe_get('Borrowings')
        pbt = self.safe_get('Profit Before Tax')
        interest = self.safe_get('Interest')

        solvency['Debt-to-Equity'] = borrowings / equity.replace(0, np.nan)
        solvency['Interest Coverage'] = (pbt + interest) / interest.replace(0, np.nan)
        
        return solvency
