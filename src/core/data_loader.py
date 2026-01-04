
import pandas as pd
import streamlit as st

class UniversalScreenerLoader:
    """Universal parser for Screener.in Excel files using keyword detection."""
    
    def __init__(self, file):
        # Read the 'Data Sheet' specifically
        self.raw_df = pd.read_excel(file, sheet_name='Data Sheet', header=None)
        
    def find_row_by_keyword(self, keyword):
        """Finds the index of the row containing the keyword."""
        for idx, row in self.raw_df.iterrows():
            if keyword in str(row.iloc[0]):
                return idx
        return None

    def extract_section(self, start_keyword, num_rows=15):
        """Extracts a financial block starting from a keyword."""
        start_idx = self.find_row_by_keyword(start_keyword)
        if start_idx is None:
            return pd.DataFrame()
            
        # Get dates (usually first row after section title)
        dates = self.raw_df.iloc[start_idx + 1, 1:].values
        
        # Get data rows
        data_block = self.raw_df.iloc[start_idx + 2 : start_idx + num_rows, :]
        data_block.columns = ['Metric'] + list(dates)
        
        return data_block.set_index('Metric').transpose()

    def get_processed_data(self):
        """Combines P&L and Balance Sheet into one clean DataFrame."""
        try:
            pl_data = self.extract_section("PROFIT & LOSS")
            bs_data = self.extract_section("BALANCE SHEET")
            
            # Clean column names (strip whitespace)
            combined = pd.concat([pl_data, bs_data], axis=1)
            combined.columns = [str(col).strip() for col in combined.columns]
            combined.index.name = "Report Date"
            
            return combined.reset_index()
        except Exception as e:
            st.error(f"Data Parsing Error: {e}")
            return None
