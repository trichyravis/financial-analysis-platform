
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        """
        Robust initialization that strictly matches data length to the index
        to prevent ValueError during metadata extraction.
        """
        # Create a deep copy to avoid modifying the original dataframe
        self.df = df.copy()
        
        # 1. Standardize the Index
        # We use 'Report Date' as the anchor for all time-series data
        if 'Report Date' in self.df.columns:
            self.df = self.df.set_index('Report Date')
            
        # 2. Get the target length (Total number of valid years/columns)
        # This prevents 'ghost' rows from Excel from crashing the app
        target_length = len(self.df.index)
            
        # 3. Clean each column and force-match the length exactly
        for col in self.df.columns:
            # Flatten to 1D array and slice to the exact length of the index
            raw_array = np.array(self.df[col]).ravel()[:target_length]
            
            # Convert to numeric, handle errors (commas/symbols), and fill blanks with 0
            self.df[col] = pd.to_numeric(pd.Series(raw_array), errors='coerce').fillna(0).values

    def get_profitability_metrics(self):
        """
        Calculates ROE and Net Profit Margin with alignment safety.
        """
        metrics = pd.DataFrame(index=self.df.index)
        
        # Extract components safely
        pat = self.df.get('Net Profit', 0)
        sales = self.df.get('Sales', 0)
        
        # Equity = Share Capital + Reserves
        equity = self.df.get('Equity Share Capital', 0) + self.df.get('Reserves', 0)
        
        # Calculate Ratios (Replace 0 with NaN to avoid division by zero errors)
        metrics['ROE %'] = (pat / equity.replace(0, np.nan)) * 100
        metrics['Net Margin %'] = (pat / sales.replace(0, np.nan)) * 100
        
        # Convert index (Dates) to strings for clean UI rendering
        metrics['Year'] = self.df.index.astype(str)
        
        return metrics.fillna(0)

    def get_solvency_metrics(self):
        """
        Calculates balance sheet strength and leverage ratios.
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
        Calculates how effectively the company uses its assets.
        """
        metrics = pd.DataFrame(index=self.df.index)
        
        sales = self.df.get('Sales', 0)
        total_assets = self.df.get('Total Assets', 0)
        
        metrics['Asset Turnover'] = sales / total_assets.replace(0, np.nan)
        metrics['Year'] = self.df.index.astype(str)
        
        return metrics.fillna(0)
