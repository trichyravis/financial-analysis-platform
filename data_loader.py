# =============================================================================
# data_loader.py - Original Data Loader (ITC-specific)
# =============================================================================

import pandas as pd
import numpy as np

def load_itc_data():
    """Load ITC financial data"""
    # Placeholder - would load from Excel in production
    dates = pd.date_range(start='2015-01', end='2025-01', freq='YS')
    
    data = pd.DataFrame({
        'Sales': np.random.uniform(50000, 80000, len(dates)),
        'Net profit': np.random.uniform(30000, 40000, len(dates)),
        'Total': np.random.uniform(100000, 150000, len(dates)),
        'Equity Share Capital': 100,
        'Reserves': np.random.uniform(50000, 80000, len(dates)),
        'Borrowings': np.random.uniform(1000, 5000, len(dates)),
        'Current liabilities': np.random.uniform(10000, 20000, len(dates)),
    }, index=dates)
    
    return data
