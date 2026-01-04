
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        """
        Robust initialization that re-aligns the DataFrame to prevent length mismatches.
        """
        # 1. Standardize the Index first
        if 'Report Date' in df.columns:
            df = df.set_index('Report Date')
        
        cleaned_data = {}
        # 2. Process each column and store in a dictionary
        for col in df.columns:
            # Flatten to 1D and convert to numeric
            raw_array = np.array(df[col]).ravel()
            # Ensure we only take as many values as there are rows in the original index
            numeric_series = pd.to_numeric(pd.Series(raw_array), errors='coerce').fillna(0)
            cleaned_data[col] = numeric_series.iloc[:len(df)].values
        
        # 3. Create a brand new DataFrame to ensure perfect alignment
        self.df = pd.DataFrame(cleaned_data, index=df.index)

    def get_profitability_metrics(self):
        metrics = pd.DataFrame(index=self.df.index)
        pat = self.df.get('Net Profit', 0)
        sales = self.df.get('Sales', 0)
        equity = self.df.get('Equity Share Capital', 0) + self.df.get('Reserves', 0)
        
        metrics['ROE %'] = (pat / equity.replace(0, np.nan)) * 100
        metrics['Net Margin %'] = (pat / sales.replace(0, np.nan)) * 100
        metrics['Year'] = self.df.index.astype(str)
        return metrics.fillna(0)
