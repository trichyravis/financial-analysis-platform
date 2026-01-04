
"""
data_loader.py - Universal Screener.in Excel Parser
🏔️ THE MOUNTAIN PATH - World of Finance
"""

import pandas as pd
import numpy as np
import streamlit as st

class UniversalScreenerLoader:
    def __init__(self, uploaded_file):
        try:
            # Screener.in data is always in 'Data Sheet'
            self.raw_df = pd.read_excel(uploaded_file, sheet_name='Data Sheet', header=None)
        except Exception as e:
            st.error(f"Error reading Excel: {e}")
            self.raw_df = None

    def find_row_index(self, keywords):
        if self.raw_df is None: return None
        for i, row in self.raw_df.iterrows():
            val = str(row.iloc[0]).upper().strip()
            if any(k.upper() in val for k in keywords):
                return i
        return None

    def get_metadata(self):
        """Extracts key company info from the top section."""
        meta = {}
        # MCAP and Price are usually in the first 15 rows
        mcap_idx = self.find_row_index(["Market Capitalization"])
        price_idx = self.find_row_index(["Current Price"])
        
        if mcap_idx is not None: meta['Market Cap'] = self.raw_df.iloc[mcap_idx, 1]
        if price_idx is not None: meta['Current Price'] = self.raw_df.iloc[price_idx, 1]
        return meta

    def parse_section(self, start_keywords, rows_to_read=25):
        start_idx = self.find_row_index(start_keywords)
        if start_idx is None: return pd.DataFrame()
        
        date_row = self.raw_df.iloc[start_idx + 1]
        dates = date_row[1:].values
        data_block = self.raw_df.iloc[start_idx + 2 : start_idx + 2 + rows_to_read, :]
        data_block.columns = ['Metric'] + list(dates)
        
        # Clean and Transpose
        df = data_block.dropna(subset=['Metric']).set_index('Metric').transpose()
        # Convert index to string to avoid datetime mismatch during merge
        df.index = df.index.astype(str)
        return df

    def get_processed_data(self):
        if self.raw_df is None: return None, {}
        try:
            # 1. Parse individual sections
            pl = self.parse_section(["PROFIT & LOSS", "P&L"])
            bs = self.parse_section(["BALANCE SHEET"])
            cf = self.parse_section(["CASH FLOW"])
            
            # 2. Combine sections
            combined = pd.concat([pl, bs, cf], axis=1)
            
            # 3. Clean duplicate columns and standardize names
            combined = combined.loc[:, ~combined.columns.duplicated()]
            combined.columns = [str(col).strip().title() for col in combined.columns]
            
            # 4. FIX FOR "Processing Error: cannot insert Report Date"
            # If "Report Date" already exists as a column, drop it before reset_index
            if "Report Date" in combined.columns:
                combined = combined.drop(columns=["Report Date"])
            
            # 5. Map essential columns for calculations
            mappings = {
                'Net Profit': ['Net Profit', 'Profit After Tax', 'Pat'],
                'Sales': ['Sales', 'Revenue', 'Turnover'],
                'Interest': ['Interest', 'Finance Costs']
            }
            
            for target, aliases in mappings.items():
                if target not in combined.columns:
                    for alias in aliases:
                        if alias.title() in combined.columns:
                            combined[target] = combined[alias.title()]
                            break
            
            # 6. Clean numeric data (handle '--' or empty strings)
            for col in combined.columns:
                combined[col] = pd.to_numeric(combined[col], errors='coerce').fillna(0)
            
            processed_df = combined.reset_index().rename(columns={'index': 'Report Date'})
            return processed_df, self.get_metadata()
            
        except Exception as e:
            st.error(f"Processing Error: {e}")
            return None, {}
