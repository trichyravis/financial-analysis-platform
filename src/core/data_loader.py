
def get_processed_data(self):
        try:
            pl_data = self.extract_section("PROFIT & LOSS")
            bs_data = self.extract_section("BALANCE SHEET")
            
            combined = pd.concat([pl_data, bs_data], axis=1)
            # Standardize column names to Title Case and remove extra spaces
            combined.columns = [str(col).strip().title() for col in combined.columns]
            
            # CRITICAL FIX: Ensure 'Net Profit' exists regardless of Screener's casing
            if 'Net Profit' not in combined.columns:
                # Look for common variations if the standard isn't found
                for alt in ['Net profit', 'Profit after tax', 'Pat']:
                    if alt in combined.columns:
                        combined['Net Profit'] = combined[alt]
            
            combined.index.name = "Report Date"
            return combined.reset_index()
        except Exception as e:
            st.error(f"Data Parsing Error: {e}")
            return None
