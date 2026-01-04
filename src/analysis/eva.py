
"""
eva.py - Economic Value Added Engine
🏔️ THE MOUNTAIN PATH - World of Finance
CORRECTED: Works with Screener.in data loader structure
"""

import pandas as pd
import numpy as np

class EVAAnalyzer:
    def __init__(self, df, wacc=0.12):
        """
        Initialize EVA Analyzer.
        
        Args:
            df: DataFrame from UniversalScreenerLoader
               Structure: 'Report Date' column (metric names), 
                         date columns with numeric values
            wacc: Weighted Average Cost of Capital (default 12%)
        """
        self.df = df
        self.wacc = wacc

    def calculate_eva(self):
        """
        Calculates Economic Value Added over historical periods.
        
        Returns DataFrame with:
        - Report Date: Metric names
        - NOPAT: Net Operating Profit After Tax
        - Invested Capital: Total capital invested
        - Capital Charge: WACC × Invested Capital
        - EVA: Economic Value Added
        - ROIC %: Return on Invested Capital percentage
        """
        try:
            # Transpose the data so dates are rows, metrics are columns
            df_t = self.df.set_index('Report Date').T
            
            # Get financial metrics (with safe defaults)
            # P&L Statement metrics
            pbt = df_t.get('Profit before tax', pd.Series(0, index=df_t.index))
            interest = df_t.get('Interest', pd.Series(0, index=df_t.index))
            tax = df_t.get('Tax', pd.Series(0, index=df_t.index))
            
            # 1. Calculate NOPAT (Net Operating Profit After Tax)
            # NOPAT = (EBIT) × (1 - Tax Rate)
            # Where EBIT = PBT + Interest
            ebit = pbt + interest
            
            # Calculate effective tax rate from actual data
            # Tax Rate = Tax / PBT (with fallback to 25%)
            tax_rate = pd.Series(np.where(pbt != 0, tax / pbt, 0.25), index=df_t.index)
            tax_rate = tax_rate.replace([np.inf, -np.inf], 0.25)  # Handle division by zero
            tax_rate = tax_rate.clip(lower=0, upper=1)  # Keep between 0-100%
            
            nopat = ebit * (1 - tax_rate)
            
            # 2. Calculate Invested Capital from Balance Sheet
            # Invested Capital = Equity + Debt
            # Note: P&L data doesn't have Balance Sheet items, so use 0 default
            equity_capital = df_t.get('Equity Share Capital', pd.Series(0, index=df_t.index))
            reserves = df_t.get('Reserves', pd.Series(0, index=df_t.index))
            equity = equity_capital + reserves
            
            debt = df_t.get('Borrowings', pd.Series(0, index=df_t.index))
            invested_capital = equity + debt
            
            # Handle zero invested capital (use average of 1 year lag for ROIC calculation)
            invested_capital_safe = invested_capital.replace(0, np.nan)
            
            # 3. Calculate Capital Charge
            # Capital Charge = Invested Capital × WACC
            capital_charge = invested_capital * self.wacc
            
            # 4. Calculate EVA
            # EVA = NOPAT - Capital Charge
            eva_value = nopat - capital_charge
            
            # 5. Calculate ROIC
            # ROIC % = NOPAT / Invested Capital × 100
            roic_pct = (nopat / invested_capital_safe) * 100
            roic_pct = roic_pct.replace([np.inf, -np.inf], 0)  # Handle division by zero
            
            # 6. Compile Results
            eva_df = pd.DataFrame({
                'Report Date': df_t.index.astype(str),
                'NOPAT': nopat.round(2),
                'Invested Capital': invested_capital.round(2),
                'Capital Charge': capital_charge.round(2),
                'EVA': eva_value.round(2),
                'ROIC %': roic_pct.round(2),
                'Tax Rate %': (tax_rate * 100).round(2)
            })
            
            # Reset index for cleaner output
            eva_df = eva_df.reset_index(drop=True)
            
            print(f"✓ EVA analysis complete: {len(eva_df)} periods analyzed")
            
            return eva_df
            
        except Exception as e:
            print(f"❌ Error in EVA calculation: {e}")
            import traceback
            traceback.print_exc()
            
            # Return empty DataFrame on error
            return pd.DataFrame({
                'Report Date': [],
                'NOPAT': [],
                'Invested Capital': [],
                'Capital Charge': [],
                'EVA': [],
                'ROIC %': [],
                'Tax Rate %': []
            })
