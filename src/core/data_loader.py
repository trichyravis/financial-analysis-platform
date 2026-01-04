
"""
data_loader.py - Universal Screener.in Excel Parser
🏔️ THE MOUNTAIN PATH - World of Finance
"""

import pandas as pd
import numpy as np
import streamlit as st
import io

class UniversalScreenerLoader:
    """
    Reworked parser that dynamically finds financial sections using keywords.
    Avoids 'Fixed Row' errors common in Screener.in exports.
    """
    
    def __init__(self, uploaded_file):
        """Initialize with a Streamlit UploadedFile object."""
        try:
            # Read the 'Data Sheet' which contains the raw financial values
            self.raw_df = pd.read_excel(uploaded_file, sheet_name='Data Sheet', header=None)
        except Exception as e:
            st.error(f"Error reading Excel: {e}")
            self.raw_df = None

    def find_row_index(self, keywords):
        """Finds the row index where any of the keywords appear in the first column."""
        if self.raw_df is None: return None
        for i, row in self.raw_df.iterrows():
            cell_value = str(row.iloc[0]).upper().strip()
            if any(key.upper() in cell_value for key in keywords):
                return i
        return None

    def parse_section(self, start_keywords, rows_to_read=20):
        """Extracts a section (like P&L) and returns a cleaned DataFrame."""
        start_idx = self.find_row_index(start_keywords)
        if start_idx is None:
            return pd.DataFrame()

        # Step 1: Identify dates (usually the row immediately after the section header)
        date_row = self.raw_df.iloc[start_idx + 1]
        dates = date_row[1:].values
        
        # Step 2: Extract data rows (next 20 rows or until next empty/metadata section)
        data_block = self.raw_df.iloc[start_idx + 2 : start_idx + 2 + rows_to_read, :]
        
        # Step 3: Set columns and clean
        data_block.columns = ['Metric'] + list(dates)
        data_block = data_block.dropna(subset=['Metric'])
        
        # Step 4: Transpose so 'Report Date' becomes the index
        section_df = data_block.set_index('Metric').transpose()
        section_df.index.name = 'Report Date'
        
        return section_df

    def get_processed_data(self):
        """Combines all sections into one clean master DataFrame."""
        if self.raw_df is None:
            return None
            
        try:
            # Parse main sections
            pl = self.parse_section(["PROFIT & LOSS", "P&L"])
            bs = self.parse_section(["BALANCE SHEET"])
            
            # Combine P&L and Balance Sheet on the Date index
            combined = pd.concat([pl, bs], axis=1)
            
            # Clean duplicate columns and standardize names to Title Case
            combined = combined.loc[:, ~combined.columns.duplicated()]
            combined.columns = [str(col).strip().title() for col in combined.columns]
            
            # Critical Column Mapping: Ensure standard names exist for the analyzer
            # Screener sometimes uses 'Net profit' vs 'Net Profit'
            mapping = {
                'Net Profit': ['Net Profit', 'Profit After Tax', 'Pat'],
                'Sales': ['Sales', 'Revenue', 'Turnover'],
                'Borrowings': ['Borrowings', 'Total Debt', 'Debt'],
                'Reserves': ['Reserves', 'Retained Earnings']
            }
            
            for standard, aliases in mapping.items():
                if standard not in combined.columns:
                    for alias in aliases:
                        if alias.title() in combined.columns:
                            combined[standard] = combined[alias.title()]
                            break

            # Convert all numeric data, forcing errors to 0 (to avoid crashes on '--' values)
            for col in combined.columns:
                combined[col] = pd.to_numeric(combined[col], errors='coerce').fillna(0)

            return combined.reset_index()
            
        except Exception as e:
            st.error(f"Failed to process financial data: {e}")
            return None

def load_screener_file(uploaded_file):
    """Entry point for the Streamlit app to load and return data."""
    loader = UniversalScreenerLoader(uploaded_file)
    return loader.get_processed_data()
