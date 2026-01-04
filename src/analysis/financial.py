
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        """
        Institutional Grade Analyzer: Handles Screener.in's non-unique indexes.
        """
        # Create a deep copy and reset index immediately to prevent 'non-unique' errors
        self.df = df.copy().reset_index(drop=True)
        
        # Standardize all columns to numeric safely
        for col in self.df.columns:
            if col != 'Report Date':
                # Convert to numeric, force 1D array
                vals = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
                self.df[col] = vals.values

    def _get_clean_series(self, keyword):
        """Hunts for a column and ensures it is a single 1D Series."""
        for col in self.df.columns:
            if keyword.lower() in str(col).lower():
                series = self.df[col]
                # If duplicate columns exist, take the first one
                if isinstance(series, pd.DataFrame):
                    series = series.iloc[:, 0]
                return series.reset_index(drop=True)
        return pd.Series(0.0, index=self.df.index)

    def get_profitability_metrics(self):
        """Calculates ROE and Margin with calculation guardrails."""
        # Use a fresh dataframe to avoid index pollution
        metrics = pd.DataFrame()
        
        pat = self._get_clean_series('Net Profit')
        sales = self._get_clean_series('Sales')
        # Equity = Share Capital + Reserves
        equity = self._get_clean_series('Equity Share Capital') + self._get_clean_series('Reserves')
        
        # Perform math on raw numpy values to bypass Pandas index alignment issues
        with np.errstate(divide='ignore', invalid='ignore'):
            metrics['ROE %'] = (pat.values / np.where(equity.values == 0, np.nan, equity.values)) * 100
            metrics['Net Margin %'] = (pat.values / np.where(sales.values == 0, np.nan, sales.values)) * 100
        
        # Add back the Date for display
        date_col = self._get_clean_series('Report Date')
        metrics['Year'] = date_col.astype(str)
        
        return metrics.fillna(0)

    def get_solvency_metrics(self):
        metrics = pd.DataFrame()
        debt = self._get_clean_series('Borrowings')
        equity = self._get_clean_series('Equity Share Capital') + self._get_clean_series('Reserves')
        
        metrics['Debt-to-Equity'] = debt.values / np.where(equity.values == 0, np.nan, equity.values)
        metrics['Year'] = self._get_clean_series('Report Date').astype(str)
        return metrics.fillna(0)
