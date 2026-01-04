# =============================================================================
# Generic Data Loader - Works with Screener.in Excel Format for ANY Company
# =============================================================================

import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import os

class ScreenerDataLoader:
    """
    Auto-detects and loads financial data from Screener.in Excel exports.
    Works with ANY company - no manual setup required!
    """
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.company_name = None
        self.annual_data = None
        self.quarterly_data = None
        self.meta_data = {}
        self.validation_status = {}
        
    def load_and_detect(self):
        """
        Load Excel file and auto-detect Screener.in structure.
        Returns: (success: bool, company_name: str, status_dict: dict)
        """
        try:
            df = pd.read_excel(self.file_path, sheet_name='Data Sheet')
            
            # Extract company name
            self.company_name = self._extract_company_name(df)
            self.validation_status['company_name'] = f"✅ {self.company_name}"
            
            # Extract meta data
            self._extract_meta(df)
            self.validation_status['meta'] = "✅ Meta data found"
            
            # Extract annual data
            self.annual_data = self._extract_annual_data(df)
            self.validation_status['annual_data'] = f"✅ {len(self.annual_data)} years"
            
            # Extract quarterly data
            self.quarterly_data = self._extract_quarterly_data(df)
            if self.quarterly_data is not None:
                self.validation_status['quarterly_data'] = f"✅ Quarterly data found"
            
            return True, self.company_name, self.validation_status
            
        except Exception as e:
            return False, None, {'error': str(e)}
    
    def _extract_company_name(self, df):
        """Extract company name from header"""
        # Usually in row 0, column 1
        if df.iloc[0, 1] and df.iloc[0, 1] != 'nan':
            name = str(df.iloc[0, 1]).strip()
            if name and name.upper() != 'NAN':
                return name
        
        # Fallback: Try to find from file name
        file_name = os.path.basename(self.file_path)
        return file_name.split('_')[0].replace('.xlsx', '').strip()
    
    def _extract_meta(self, df):
        """Extract meta information (shares, price, market cap)"""
        meta_row_start = None
        
        # Find META section
        for idx, row in df.iterrows():
            if 'META' in str(row.iloc[0]).upper():
                meta_row_start = idx
                break
        
        if meta_row_start:
            meta_section = df.iloc[meta_row_start:meta_row_start+10]
            
            for idx, row in meta_section.iterrows():
                label = str(row.iloc[0]).strip()
                try:
                    value = float(row.iloc[1])
                except:
                    continue
                
                if 'shares' in label.lower():
                    self.meta_data['shares'] = value
                elif 'price' in label.lower():
                    self.meta_data['current_price'] = value
                elif 'market cap' in label.lower():
                    self.meta_data['market_cap'] = value
                elif 'face value' in label.lower():
                    self.meta_data['face_value'] = value
    
    def _extract_annual_data(self, df):
        """Extract annual P&L, Balance Sheet, Cash Flow data"""
        try:
            # Find P&L section header (row with "Report Date")
            pl_header_idx = None
            for idx, row in df.iterrows():
                if 'Report Date' in str(row.iloc[0]) and idx > 10 and idx < 30:
                    pl_header_idx = idx
                    break
            
            if pl_header_idx is None:
                return None
            
            # Get dates from header row
            dates_row = df.iloc[pl_header_idx]
            years = []
            for col_idx in range(1, len(dates_row)):
                try:
                    date = pd.to_datetime(dates_row.iloc[col_idx])
                    years.append(date)
                except:
                    pass
            
            if not years:
                return None
            
            # Extract P&L, BS, CF sections
            data_dict = {}
            current_section = None
            
            for idx in range(pl_header_idx + 1, len(df)):
                row = df.iloc[idx]
                label = str(row.iloc[0]).strip()
                
                # Skip empty rows
                if not label or label.upper() == 'NAN':
                    continue
                
                # Detect section headers
                if 'BALANCE SHEET' in label.upper():
                    current_section = 'bs'
                    continue
                elif 'CASH FLOW' in label.upper():
                    current_section = 'cf'
                    continue
                elif 'PROFIT & LOSS' in label.upper():
                    current_section = 'pl'
                    continue
                
                # Extract row data
                try:
                    values = []
                    for col_idx in range(1, len(years) + 1):
                        try:
                            val = float(row.iloc[col_idx])
                            values.append(val)
                        except:
                            values.append(np.nan)
                    
                    if any(~np.isnan(values)):
                        # Create unique key for this metric
                        key = f"{current_section}_{label}" if current_section else label
                        data_dict[label] = values
                
                except Exception as e:
                    continue
            
            # Create DataFrame with years as index
            annual_df = pd.DataFrame(data_dict, index=years)
            annual_df.index.name = 'Year'
            
            return annual_df.sort_index()
        
        except Exception as e:
            st.warning(f"Could not extract annual data: {e}")
            return None
    
    def _extract_quarterly_data(self, df):
        """Extract quarterly P&L data if available"""
        try:
            # Find quarterly section
            q_section_idx = None
            for idx, row in df.iterrows():
                if 'Quarter' in str(row.iloc[0]):
                    q_section_idx = idx + 1
                    break
            
            if q_section_idx is None:
                return None
            
            # Similar extraction logic for quarterly
            q_dates = []
            dates_row = df.iloc[q_section_idx]
            
            for col_idx in range(1, len(dates_row)):
                try:
                    date = pd.to_datetime(dates_row.iloc[col_idx])
                    q_dates.append(date)
                except:
                    pass
            
            if not q_dates:
                return None
            
            # Extract quarterly data
            q_data = {}
            for idx in range(q_section_idx + 1, min(q_section_idx + 15, len(df))):
                row = df.iloc[idx]
                label = str(row.iloc[0]).strip()
                
                if not label or label.upper() == 'NAN':
                    continue
                
                try:
                    values = []
                    for col_idx in range(1, len(q_dates) + 1):
                        try:
                            val = float(row.iloc[col_idx])
                            values.append(val)
                        except:
                            values.append(np.nan)
                    
                    if any(~np.isnan(values)):
                        q_data[label] = values
                
                except:
                    continue
            
            if q_data:
                q_df = pd.DataFrame(q_data, index=q_dates)
                q_df.index.name = 'Quarter'
                return q_df.sort_index()
        
        except:
            pass
        
        return None
    
    def get_company_name(self):
        """Get detected company name"""
        return self.company_name
    
    def get_annual_data(self):
        """Get annual financial data"""
        return self.annual_data
    
    def get_quarterly_data(self):
        """Get quarterly financial data"""
        return self.quarterly_data
    
    def get_meta_data(self):
        """Get meta information"""
        return self.meta_data
    
    def get_validation_status(self):
        """Get data validation status"""
        return self.validation_status
    
    def validate_data_completeness(self):
        """
        Validate that all required data sections are present.
        Returns: (is_valid: bool, missing_sections: list, message: str)
        """
        missing = []
        
        if self.annual_data is None:
            missing.append("Annual Financial Data")
        elif len(self.annual_data) < 3:
            missing.append(f"Insufficient years ({len(self.annual_data)} years, need 5+)")
        
        required_metrics = ['Sales', 'Net profit', 'Total', 'Borrowings']
        
        if self.annual_data is not None:
            available_cols = self.annual_data.columns
            for metric in required_metrics:
                found = any(metric in col for col in available_cols)
                if not found:
                    missing.append(f"Missing metric: {metric}")
        
        if missing:
            return False, missing, f"⚠️ Data validation issues:\n• " + "\n• ".join(missing)
        
        return True, [], "✅ All data validated successfully!"
    
    def get_data_summary(self):
        """Get summary of loaded data"""
        summary = {
            'company_name': self.company_name,
            'years_available': len(self.annual_data) if self.annual_data is not None else 0,
            'year_range': f"{self.annual_data.index.min().year}-{self.annual_data.index.max().year}" 
                         if self.annual_data is not None else "N/A",
            'has_quarterly': self.quarterly_data is not None,
            'meta_data': self.meta_data,
            'metrics_count': len(self.annual_data.columns) if self.annual_data is not None else 0
        }
        return summary


# =============================================================================
# Streamlit Upload Interface & Multi-Company Management
# =============================================================================

class CompanyDataManager:
    """Manages multiple company data uploads and selections"""
    
    def __init__(self):
        if 'companies' not in st.session_state:
            st.session_state.companies = {}
        if 'selected_company' not in st.session_state:
            st.session_state.selected_company = None
    
    def upload_file(self, uploaded_file):
        """
        Upload and process a file.
        Returns: (success: bool, company_name: str, message: str)
        """
        try:
            # Save temp file
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name
            
            # Load with ScreenerDataLoader
            loader = ScreenerDataLoader(tmp_path)
            success, company_name, status = loader.load_and_detect()
            
            if success:
                # Validate completeness
                is_valid, missing, msg = loader.validate_data_completeness()
                
                if not is_valid:
                    return False, None, f"⚠️ {msg}"
                
                # Store in session
                st.session_state.companies[company_name] = {
                    'loader': loader,
                    'annual_data': loader.get_annual_data(),
                    'quarterly_data': loader.get_quarterly_data(),
                    'meta_data': loader.get_meta_data(),
                    'summary': loader.get_data_summary(),
                    'upload_time': datetime.now()
                }
                
                # Auto-select first company
                if st.session_state.selected_company is None:
                    st.session_state.selected_company = company_name
                
                return True, company_name, f"✅ {company_name} uploaded successfully!"
            else:
                return False, None, f"❌ Could not process file: {status.get('error', 'Unknown error')}"
        
        except Exception as e:
            return False, None, f"❌ Error: {str(e)}"
    
    def get_companies(self):
        """Get list of uploaded companies"""
        return list(st.session_state.companies.keys())
    
    def select_company(self, company_name):
        """Select active company"""
        if company_name in st.session_state.companies:
            st.session_state.selected_company = company_name
            return True
        return False
    
    def get_selected_company(self):
        """Get currently selected company"""
        return st.session_state.selected_company
    
    def get_company_data(self, company_name=None):
        """Get data for a specific company"""
        if company_name is None:
            company_name = st.session_state.selected_company
        
        if company_name and company_name in st.session_state.companies:
            return st.session_state.companies[company_name]
        return None
    
    def remove_company(self, company_name):
        """Remove a company from analysis"""
        if company_name in st.session_state.companies:
            del st.session_state.companies[company_name]
            
            if st.session_state.selected_company == company_name:
                remaining = self.get_companies()
                st.session_state.selected_company = remaining[0] if remaining else None
            
            return True
        return False
    
    def get_all_data_summary(self):
        """Get summary of all uploaded companies"""
        summary = {}
        for company_name, data in st.session_state.companies.items():
            summary[company_name] = data['summary']
        return summary


# Utility function to get or create manager
def get_company_manager():
    """Get or create CompanyDataManager instance"""
    if 'company_manager' not in st.session_state:
        st.session_state.company_manager = CompanyDataManager()
    return st.session_state.company_manager
