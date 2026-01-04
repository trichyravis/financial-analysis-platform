
"""
Corrected Universal Screener Loader for Screener.in Financial Data
Properly handles Screener.in Excel export format with robust error handling
"""

import pandas as pd
import numpy as np
from datetime import datetime


class UniversalScreenerLoader:
    """
    Robust loader for Screener.in Excel exports with proper metadata and financial data extraction.
    
    Structure Expected:
    - Rows 0-8: Metadata (Company Name, Shares, Current Price, Market Cap)
    - Rows 15-29: P&L Annual Data with datetime headers
    - Rows 55-70: Balance Sheet Data
    - Rows 80-84: Cash Flow Data
    """
    
    def __init__(self, uploaded_file):
        self.file = uploaded_file
        self.raw_data = None
        self.metadata = {
            'market_cap': 0.0,
            'current_price': 0.0,
            'total_shares': 0.0,
            'company_name': "Unknown Entity"
        }
        self.excel_data = None
        
    def get_processed_data(self):
        """Main entry point to load and clean the Excel data."""
        try:
            # Load the 'Data Sheet' from Screener Excel
            self.excel_data = pd.read_excel(self.file, sheet_name='Data Sheet', header=None)
            
            # 1. Extract Metadata (Company, Market Cap, Price, Shares)
            self._extract_metadata_fixed()
            
            # 2. Extract P&L Financial Table (Annual data)
            processed_df = self._extract_financial_table_robust()
            
            # 3. Validation checks
            if not self._validate_data(processed_df):
                return None, None
            
            return processed_df, self.metadata
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            import traceback
            traceback.print_exc()
            return None, None

    def _extract_metadata_fixed(self):
        """
        Extract metadata from FIXED row positions in Screener.in format.
        
        Row 0, Col 1: Company Name
        Row 5, Col 1: Number of Shares (in Crores)
        Row 7, Col 1: Current Price
        Row 8, Col 1: Market Capitalization (in Crores)
        """
        try:
            df = self.excel_data
            
            # Company Name (Row 0, Col 1)
            company_name = str(df.iloc[0, 1]).strip() if pd.notnull(df.iloc[0, 1]) else "Unknown"
            self.metadata['company_name'] = company_name
            
            # Number of Shares in Crores (Row 5, Col 1)
            shares = self._safe_float(df.iloc[5, 1])
            self.metadata['total_shares'] = shares
            
            # Current Price (Row 7, Col 1)
            current_price = self._safe_float(df.iloc[7, 1])
            self.metadata['current_price'] = current_price
            
            # Market Capitalization in Crores (Row 8, Col 1)
            market_cap = self._safe_float(df.iloc[8, 1])
            self.metadata['market_cap'] = market_cap
            
            # Validation: Verify consistency
            if market_cap > 0 and current_price > 0:
                calculated_shares = market_cap / current_price
                if abs(calculated_shares - shares) / shares > 0.05:
                    print(f"⚠️  Warning: Share count mismatch. Excel: {shares:.2f}Cr, Calculated: {calculated_shares:.2f}Cr")
            
            print(f"✓ Metadata extracted:")
            print(f"  Company: {self.metadata['company_name']}")
            print(f"  Current Price: ₹{self.metadata['current_price']:.2f}")
            print(f"  Market Cap: ₹{self.metadata['market_cap']:.2f} Cr")
            print(f"  Total Shares: {self.metadata['total_shares']:.2f} Cr")
            
        except Exception as e:
            print(f"⚠️  Error extracting metadata: {e}")

    def _extract_financial_table_robust(self):
        """
        Extract P&L financial data from Screener.in format.
        
        Structure:
        - Row 14: Section header "PROFIT & LOSS"
        - Row 15: Headers with datetime objects (2016-03-31, 2017-03-31, ...)
        - Rows 16+: Financial line items with numerical data
        
        Returns DataFrame with:
        - Index: Financial metric names (Sales, Profit, etc.)
        - Columns: Report dates formatted as 'YYYY-MM-DD'
        """
        try:
            df = self.excel_data
            
            # Find P&L section (Row 14 contains "PROFIT & LOSS")
            pl_section_row = 14
            if not isinstance(df.iloc[pl_section_row, 0], str) or 'PROFIT' not in str(df.iloc[pl_section_row, 0]):
                for i in range(len(df)):
                    if pd.notnull(df.iloc[i, 0]) and 'PROFIT' in str(df.iloc[i, 0]).upper():
                        pl_section_row = i
                        break
            
            # Row with headers (next row after section header)
            header_row = pl_section_row + 1
            
            # Extract headers (dates) from columns 1 onwards
            headers = df.iloc[header_row, 1:].tolist()
            
            # Convert datetime objects to string format 'YYYY-MM-DD'
            headers = [self._format_date(h) for h in headers]
            
            # Extract data rows (starting from header_row + 1)
            data_rows = []
            for row_idx in range(header_row + 1, len(df)):
                metric_name = df.iloc[row_idx, 0]
                
                # Stop if we hit the next section
                if pd.notnull(metric_name) and isinstance(metric_name, str):
                    if any(keyword in metric_name.upper() for keyword in ['QUARTERS', 'BALANCE', 'CASH FLOW']):
                        break
                
                # Extract numeric values for this metric
                if pd.notnull(metric_name) and metric_name.strip():
                    values = []
                    for col_idx in range(1, 1 + len(headers)):
                        val = self._safe_float(df.iloc[row_idx, col_idx])
                        values.append(val)
                    
                    data_rows.append({
                        'Metric': str(metric_name).strip(),
                        'values': values
                    })
            
            # Create DataFrame
            if not data_rows:
                print("❌ No financial data found in P&L section")
                return None
            
            # Build the final dataframe
            final_data = []
            for row in data_rows:
                row_dict = {'Report Date': row['Metric']}
                for col_idx, date_str in enumerate(headers):
                    row_dict[date_str] = row['values'][col_idx]
                final_data.append(row_dict)
            
            result_df = pd.DataFrame(final_data)
            
            # Clean numeric columns
            for col in result_df.columns:
                if col != 'Report Date':
                    result_df[col] = pd.to_numeric(result_df[col], errors='coerce').fillna(0)
            
            print(f"✓ Financial data extracted: {len(result_df)} metrics × {len(headers)} periods")
            print(f"  Date range: {headers[0]} to {headers[-1]}")
            print(f"  Metrics: {', '.join(result_df['Report Date'].head(5).tolist())}...")
            
            return result_df
            
        except Exception as e:
            print(f"❌ Error extracting financial table: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _safe_float(self, value):
        """Safely convert value to float, handling various data types."""
        if pd.isna(value):
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def _format_date(self, date_obj):
        """
        Convert various date formats to 'YYYY-MM-DD' string.
        Handles datetime objects, strings, and NaT values.
        """
        if pd.isna(date_obj):
            return None
        
        try:
            if hasattr(date_obj, 'strftime'):
                return date_obj.strftime('%Y-%m-%d')
            
            if isinstance(date_obj, str):
                parsed = pd.to_datetime(date_obj)
                return parsed.strftime('%Y-%m-%d')
            
            parsed = pd.to_datetime(date_obj)
            return parsed.strftime('%Y-%m-%d')
            
        except Exception as e:
            print(f"⚠️  Could not format date: {date_obj}")
            return None

    def _validate_data(self, df):
        """Validate that extracted data is reasonable."""
        if df is None or df.empty:
            print("❌ Validation failed: Empty dataframe")
            return False
        
        if 'Report Date' not in df.columns:
            print("❌ Validation failed: 'Report Date' column missing")
            return False
        
        if len(df) < 5:
            print(f"⚠️  Warning: Only {len(df)} metrics found (expected at least 5)")
            return False
        
        if len(df.columns) < 4:
            print(f"⚠️  Warning: Only {len(df.columns) - 1} years of data (expected at least 3)")
            return False
        
        print("✓ Data validation passed")
        return True


class ScreenerDataAnalyzer:
    """
    Utility class to analyze and inspect Screener.in Excel structure
    Useful for debugging data format issues
    """
    
    @staticmethod
    def inspect_excel(file_path):
        """Print detailed information about Excel file structure."""
        try:
            df = pd.read_excel(file_path, sheet_name='Data Sheet', header=None)
            
            print("\n" + "="*80)
            print("SCREENER.IN EXCEL STRUCTURE INSPECTION")
            print("="*80)
            
            print(f"\nFile shape: {df.shape}")
            print("\nSheet names available: ['Data Sheet']")
            
            print("\n" + "-"*80)
            print("METADATA SECTION (Rows 0-10)")
            print("-"*80)
            for i in range(10):
                print(f"Row {i}: {df.iloc[i, 0]} | {df.iloc[i, 1]}")
            
            print("\n" + "-"*80)
            print("SECTION IDENTIFIERS")
            print("-"*80)
            for idx, row in df[0].items():
                if pd.notnull(row) and isinstance(row, str) and row.strip():
                    if any(keyword in row.upper() for keyword in ['PROFIT', 'BALANCE', 'CASH', 'QUARTERS', 'META']):
                        print(f"Row {idx}: {row}")
            
            return df
            
        except Exception as e:
            print(f"❌ Error inspecting Excel: {e}")
            return None
