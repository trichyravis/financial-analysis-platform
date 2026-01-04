
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    """Calculates professional financial metrics from Screener.in data."""
    
    def __init__(self, df):
        self.df = df

    def get_profitability_metrics(self):
        """Returns a dataframe of margin and return ratios."""
        metrics = pd.DataFrame(index=self.df.index)
        metrics['Year'] = self.df['Report Date']
        
        # Margins
        metrics['Gross Margin %'] = (self.df['Sales'] - self.df['Raw Material Cost']) / self.df['Sales'] * 100
        metrics['EBITDA Margin %'] = (self.df['Profit before tax'] + self.df['Depreciation'] + self.df['Interest']) / self.df['Sales'] * 100
        metrics['Net Margin %'] = self.df['Net Profit'] / self.df['Sales'] * 100
        
        # Returns
        equity = self.df['Equity Share Capital'] + self.df['Reserves']
        metrics['ROE %'] = (self.df['Net Profit'] / equity) * 100
        metrics['ROCE %'] = (self.df['Profit before tax'] + self.df['Interest']) / (equity + self.df['Borrowings']) * 100
        
        return metrics

    def get_solvency_metrics(self):
        """Returns debt and coverage ratios."""
        solvency = pd.DataFrame(index=self.df.index)
        solvency['Year'] = self.df['Report Date']
        equity = self.df['Equity Share Capital'] + self.df['Reserves']
        
        solvency['Debt-to-Equity'] = self.df['Borrowings'] / equity
        solvency['Interest Coverage'] = (self.df['Profit before tax'] + self.df['Interest']) / self.df['Interest']
        return solvency
