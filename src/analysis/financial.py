import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        self.df = df

    def safe_get(self, col_name):
        """Helper to get column or return series of zeros to prevent KeyError."""
        if col_name in self.df.columns:
            return self.df[col_name]
        return pd.Series(0, index=self.df.index)

    def get_profitability_metrics(self):
        metrics = pd.DataFrame(index=self.df.index)
        metrics['Year'] = self.df['Report Date']
        
        sales = self.safe_get('Sales')
        net_profit = self.safe_get('Net Profit')
        
        # Calculate with safety check to avoid division by zero
        metrics['Net Margin %'] = (net_profit / sales.replace(0, np.nan)) * 100
        return metrics
