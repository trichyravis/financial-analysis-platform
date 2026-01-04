
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        """
        Robust initialization to handle complex Pandas objects from Excel.
        """
        # Ensure we are working with a clean copy
        self.df = df.copy()
        
        # 1. Standardize the Index
        if 'Report Date' in self.df.columns:
            self.df = self.df.set_index('Report Date')
            
        # 2. Force conversion to 1-D numeric Series for every column
        for col in self.df.columns:
            # Squeeze handles any nested dimensions; ravel ensures it is a flat array
            raw_data = np.array(self.df[col]).ravel() 
            self.df[col] = pd.to_numeric(pd.Series(raw_data), errors='coerce').fillna(0).values

    def get_profitability_metrics(self):
        """Calculates core profitability ratios with alignment safety."""
        metrics = pd.DataFrame(index=self.df.index)
        
        pat = self.df.get('Net Profit', 0)
        sales = self.df.get('Sales', 0)
        # Equity = Share Capital + Reserves
        equity = self.df.get('Equity Share Capital', 0) + self.df.get('Reserves', 0)
        
        metrics['ROE %'] = (pat / equity.replace(0, np.nan)) * 100
        metrics['Net Margin %'] = (pat / sales.replace(0, np.nan)) * 100
        metrics['Year'] = self.df.index.astype(str)
        
        return metrics.fillna(0)

    def get_solvency_metrics(self):
        """Calculates Debt-to-Equity ratios."""
        metrics = pd.DataFrame(index=self.df.index)
        borrowings = self.df.get('Borrowings', 0)
        equity = self.df.get('Equity Share Capital', 0) + self.df.get('Reserves', 0)
        
        metrics['Debt-to-Equity'] = borrowings / equity.replace(0, np.nan)
        metrics['Year'] = self.df.index.astype(str)
        return metrics.fillna(0)
