
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        self.df = df.copy()
        if 'Report Date' in self.df.columns:
            self.df = self.df.set_index('Report Date')
        
        # Standardize columns to numeric
        for col in self.df.columns:
            raw_array = np.array(self.df[col]).ravel()[:len(self.df)]
            self.df[col] = pd.to_numeric(pd.Series(raw_array), errors='coerce').fillna(0).values

    def _get_fuzzy_col(self, keyword):
        """Hunts for a column that contains the keyword (e.g., 'Sales')"""
        for col in self.df.columns:
            if keyword.lower() in str(col).lower():
                return self.df[col]
        return pd.Series(0, index=self.df.index)

    def get_profitability_metrics(self):
        metrics = pd.DataFrame(index=self.df.index)
        
        # Use fuzzy matching to find Sales and Net Profit
        pat = self._get_fuzzy_col('Net Profit')
        sales = self._get_fuzzy_col('Sales')
        equity = self._get_fuzzy_col('Equity Share Capital') + self._get_fuzzy_col('Reserves')
        
        metrics['ROE %'] = (pat / equity.replace(0, np.nan)) * 100
        metrics['Net Margin %'] = (pat / sales.replace(0, np.nan)) * 100
        metrics['Year'] = self.df.index.astype(str)
        
        return metrics.fillna(0)
