
import pandas as pd
import numpy as np

class UniversalScreenerLoader:
    def __init__(self, uploaded_file):
        self.file = uploaded_file
        self.raw_data = None
        self.metadata = {
            'market_cap': 0.0,
            'current_price': 0.0,
            'total_shares': 0.0,
            'company_name': "Unknown Entity"
        }

    def get_processed_data(self):
        """Main entry point to load and clean the Excel data."""
        try:
            # Load the 'Data Sheet' specifically from Screener Excel
            df = pd.read_excel(self.file, sheet_name='Data Sheet', header=None)
            self.raw_data = df

            # 1. Extract Metadata (Market Cap, Price, Shares)
            self._extract_metadata(df)

            # 2. Extract Time-Series Financials
            processed_df = self._extract_financial_table(df)

            return processed_df, self.metadata

        except Exception as e:
            print(f"Error loading data: {e}")
            return None, None

    def _find_value_by_label(self, df, label):
        """Hunts for a specific value next to a label in the entire sheet."""
        for row_idx in range(len(df)):
            row_content = str(df.iloc[row_idx, 0])
            if label.lower() in row_content.lower():
                # Usually, the value is in the next column or two
                for col_idx in range(1, 4):
                    val = df.iloc[row_idx, col_idx]
                    if pd.notnull(val) and isinstance(val, (int, float)):
                        return float(val)
        return 0.0

    def _extract_metadata(self, df):
        """Extracts institutional context from the top of the sheet."""
        self.metadata['market_cap'] = self._find_value_by_label(df, "Market Capitalization")
        self.metadata['current_price'] = self._find_value_by_label(df, "Current Price")
        
        # Calculate Total Shares in Crores
        # Formula: Market Cap / Current Price
        if self.metadata['current_price'] > 0:
            self.metadata['total_shares'] = self.metadata['market_cap'] / self.metadata['current_price']
        
        # Extract Company Name (Usually in Row 0 or 1)
        self.metadata['company_name'] = str(df.iloc[0, 0]).split('\n')[0]

    def _extract_financial_table(self, df):
        """Locates the Profit & Loss or Balance Sheet block and formats it."""
        # Find the row where the 'Report Date' or years start (Usually contains 'Mar-')
        start_row = 0
        for i, row in df.iterrows():
            if any(str(cell).startswith('Mar ') or 'Mar-' in str(cell) for cell in row):
                start_row = i
                break
        
        # Capture the headers (Years)
        headers = df.iloc[start_row].tolist()
        headers[0] = "Report Date"
        
        # Slice data from the headers downward
        data_block = df.iloc[start_row + 1:].copy()
        data_block.columns = headers
        
        # Keep only rows that have a label in the first column and numeric data
        data_block = data_block[data_block['Report Date'].notnull()]
        
        # Pivot the data so 'Report Date' (Years) are the Index
        # This makes it compatible with our analysis engines
        final_df = data_block.set_index('Report Date').T
        
        # Clean numeric data: remove commas, handle NaNs
        final_df = final_df.apply(pd.to_numeric, errors='coerce').fillna(0)
        
        # Reset index to bring 'Report Date' back as a column
        final_df = final_df.reset_index().rename(columns={'index': 'Report Date'})
        
        return final_df
