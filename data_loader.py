
# screener_data_loader.py
# Universal data loader for standard Screener.in Excel format
# Automatically parses ANY stock downloaded from Screener.in
# No manual column renaming needed!

import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st

class ScreenerDataLoader:
    """
    Loads and parses standard Screener.in Excel format automatically.
    Handles the fixed structure used by all Screener.in exports.
    """
    
    # Standard row positions in Screener.in format
    COMPANY_NAME_ROW = 0
    METADATA_START = 4
    REPORT_DATE_ROW = 15  # Dates are in row 15
    PL_SECTION_START = 14  # PROFIT & LOSS section
    BS_SECTION_START = 54  # BALANCE SHEET section
    
    # Financial metric row mappings (relative to PL_SECTION_START)
    PL_METRICS = {
        'Sales': 16,
        'Revenue': 16,  # Alias for Sales
        'Raw Material Cost': 17,
        'Power and Fuel': 19,
        'Employee Cost': 21,
        'Selling and Admin': 22,
        'Other Expenses': 23,
        'Other Income': 24,
        'Depreciation': 25,
        'Interest': 26,
        'Profit Before Tax': 27,
        'EBIT': 27,  # Alias for PBT
        'Tax': 28,
        'Net Profit': 29,
        'Net Income': 29,  # Alias for Net Profit
        'Dividend Amount': 30,
    }
    
    # Balance Sheet metrics - these vary by position, search by label
    BS_METRICS = [
        'Total Assets',
        'Current Assets',
        'Current Liabilities',
        'Total Liabilities',
        'Cash & Bank',
        'Cash',
        'Inventory',
        'Receivables',
        'Equity',
        'Book Value',
    ]
    
    def __init__(self, file_path):
        """Initialize loader with Excel file path"""
        self.file_path = file_path
        self.raw_df = None
        self.company_name = None
        self.years = None
        self.data = None
        self.load_and_parse()
    
    def load_and_parse(self):
        """Load Excel file and parse standard Screener.in format"""
        try:
            # Load the raw data without headers
            self.raw_df = pd.read_excel(
                self.file_path,
                sheet_name='Data Sheet',
                header=None
            )
            
            # Extract metadata
            self._extract_metadata()
            
            # Extract financial data
            self._extract_financial_data()
            
            st.success("✅ File parsed successfully!")
            
        except Exception as e:
            st.error(f"❌ Error parsing file: {str(e)}")
            raise
    
    def _extract_metadata(self):
        """Extract company name and years from file"""
        # Get company name from first row
        self.company_name = str(self.raw_df.iloc[0, 1])
        
        # Extract years from Report Date row
        report_dates = self.raw_df.iloc[self.REPORT_DATE_ROW, 1:]
        report_dates = report_dates.dropna()
        
        # Convert dates to years
        self.years = []
        for date in report_dates:
            try:
                year = int(pd.Timestamp(date).year)
                self.years.append(year)
            except:
                pass
        
        if not self.years:
            raise ValueError("Could not extract years from file")
        
        st.info(f"Company: {self.company_name} | Years: {len(self.years)} ({self.years[0]}-{self.years[-1]})")
    
    def _extract_financial_data(self):
        """Extract all financial metrics from standard structure"""
        data = {'Year': self.years}
        
        # Extract PROFIT & LOSS metrics
        for metric_name, row_idx in self.PL_METRICS.items():
            try:
                values = self.raw_df.iloc[row_idx, 1:len(self.years)+1].values
                # Clean values - convert to numeric
                values = pd.to_numeric(values, errors='coerce').tolist()
                
                # Use primary name only (avoid duplicates)
                if metric_name == 'Revenue':  # Alias
                    continue
                if metric_name == 'EBIT':  # Alias
                    continue
                if metric_name == 'Net Income':  # Alias
                    continue
                
                data[metric_name] = values
            except:
                pass
        
        # Extract BALANCE SHEET metrics by searching for labels
        self._extract_balance_sheet_metrics(data)
        
        # Create DataFrame
        self.data = pd.DataFrame(data)
        
        # Rename columns for consistency with app
        self.data = self._standardize_column_names(self.data)
    
    def _extract_balance_sheet_metrics(self, data):
        """Extract balance sheet metrics by searching for labels"""
        # Search through rows starting from BS section
        for row_idx in range(self.BS_SECTION_START, min(self.BS_SECTION_START + 100, len(self.raw_df))):
            metric_label = str(self.raw_df.iloc[row_idx, 0]).strip()
            
            # Check if this row contains a metric we want
            for bs_metric in self.BS_METRICS:
                if bs_metric.lower() in metric_label.lower():
                    try:
                        values = self.raw_df.iloc[row_idx, 1:len(self.years)+1].values
                        values = pd.to_numeric(values, errors='coerce').tolist()
                        
                        if not all(pd.isna(v) for v in values):  # Only if has data
                            # Use the actual label from the file
                            clean_label = metric_label.replace('₹', '').strip()
                            if clean_label not in data:  # Don't duplicate
                                data[clean_label] = values
                    except:
                        pass
    
    def _standardize_column_names(self, df):
        """Standardize column names to match app expectations"""
        # Mapping of various name formats to standard names
        name_mapping = {
            'Sales': 'Revenue',
            'Profit Before Tax': 'EBIT',
            'Net Profit': 'Net Income',
            'Total': 'Total Assets',
            'Current': 'Current Assets',
            'Receivables': 'Receivables',
            'Inventory': 'Inventory',
            'Cash & Bank': 'Cash',
            'Equity': 'Equity',
            'Employee Cost': 'Employee Cost',
            'Depreciation': 'Depreciation',
            'Interest': 'Interest',
            'Tax': 'Tax',
            'Dividend Amount': 'Dividend',
        }
        
        # Rename columns that have exact matches
        df = df.rename(columns=name_mapping)
        
        return df
    
    def get_data(self):
        """Return the processed DataFrame"""
        return self.data.copy()
    
    def get_company_name(self):
        """Return company name"""
        return self.company_name
    
    def get_years(self):
        """Return list of years"""
        return self.years.copy()
    
    def get_summary(self):
        """Return data summary"""
        return {
            'company': self.company_name,
            'rows': len(self.data),
            'columns': len(self.data.columns),
            'years': f"{self.years[0]} to {self.years[-1]}",
            'columns_list': self.data.columns.tolist(),
        }


def load_screener_file(uploaded_file):
    """
    Streamlit helper function to load Screener.in Excel file.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        DataFrame with financial data
    """
    import tempfile
    
    try:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name
        
        # Load using ScreenerDataLoader
        loader = ScreenerDataLoader(tmp_path)
        data = loader.get_data()
        
        # Display summary
        summary = loader.get_summary()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Company", summary['company'][:20])
        with col2:
            st.metric("Rows", summary['rows'])
        with col3:
            st.metric("Columns", summary['columns'])
        with col4:
            st.metric("Years", summary['years'])
        
        # Show available columns
        with st.expander("📊 Available Columns"):
            st.write(summary['columns_list'])
        
        return data
        
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        st.info("Make sure you downloaded the file from Screener.in using the standard format.")
        return None
