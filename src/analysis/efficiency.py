
def calculate_efficiency(data):
    efficiency = pd.DataFrame(index=data['Report Date'])
    
    # 1. Asset Turnover Ratio
    efficiency['Asset Turnover'] = data['Sales'] / data['Total Assets']
    
    # 2. Inventory Turnover (if Inventory exists)
    if 'Inventory' in data.columns:
        efficiency['Inventory Turnover'] = data['Sales'] / data['Inventory']
    
    # 3. Debtor Days (Working Capital Cycle Component)
    if 'Trade Receivables' in data.columns:
        efficiency['Debtor Days'] = (data['Trade Receivables'] / data['Sales']) * 365
        
    return efficiency
