
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        """
        Robust initialization to handle complex Pandas objects from Excel.
        """
        self.df = df.copy()
        
        # 1. Standardize the Index
        # We ensure 'Report Date' is the index for all time-series calculations
        if 'Report Date' in self.df.columns:
            self.df = self.df.set_index('Report Date')
            
        # 2. Convert all columns to numeric safely
        # We flatten the values into a 1-D array to prevent TypeError: arg must be a list, tuple...
        for col in self.df.columns:
            # Extract raw values, flatten them, and convert to numeric Series
            raw_values = self.df[col].values.flatten()
            self.df[col] = pd.to_numeric(pd.Series(raw_values), errors='coerce').fillna(0).values

    def get_profitability_metrics(self):
        """
        Calculates core profitability ratios with index alignment safety.
        Returns a DataFrame with ROE and Net Margin.
        """
        # Initialize metrics DataFrame with the exact same index as source data
        metrics = pd.DataFrame(index=self.df.index)
        
        # Data Extraction
        pat = self.df.get('Net Profit', 0)
        sales = self.df.get('Sales', 0)
        # Equity = Share Capital + Reserves
        equity = self.df.get('Equity Share Capital', 0) + self.df.get('Reserves', 0)
        
        # Calculations (replace 0 with NaN to avoid division errors)
        metrics['ROE %'] = (pat / equity.replace(0, np.nan)) * 100
        metrics['Net Margin %'] = (pat / sales.replace(0, np.nan)) * 100
        
        # Add a string version of the Year for UI display
        metrics['Year'] = self.df.index.astype(str)
        
        return metrics.fillna(0)

    def get_solvency_metrics(self):
        """
        Calculates balance sheet strength (Debt-to-Equity).
        """
        metrics = pd.DataFrame(index=self.df.index)
        
        borrowings = self.df.get('Borrowings', 0)
        equity = self.df.get('Equity Share Capital', 0) + self.df.get('Reserves', 0)
        total_assets = self.df.get('Total Assets', 0)
        
        metrics['Debt-to-Equity'] = borrowings / equity.replace(0, np.nan)
        metrics['Equity Multiplier'] = total_assets / equity.replace(0, np.nan)
        metrics['Year'] = self.df.index.astype(str)
        
        return metrics.fillna(0)

    def get_efficiency_metrics(self):
        """
        Calculates Asset Turnover and Working Capital efficiency.
        """
        metrics = pd.DataFrame(index=self.df.index)
        
        sales = self.df.get('Sales', 0)
        total_assets = self.df.get('Total Assets', 0)
        
        metrics['Asset Turnover'] = sales / total_assets.replace(0, np.nan)
        metrics['Year'] = self.df.index.astype(str)
        
        return metrics.fillna(0)
