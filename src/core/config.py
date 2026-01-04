
"""
config.py - Centralized Configuration for The Mountain Path
🏔️ THE MOUNTAIN PATH - World of Finance
"""

# =============================================================================
# BRANDING & IDENTITY
# =============================================================================
COMPANY_NAME = "The Mountain Path"
TAGLINE = "World of Finance"
AUTHOR = "Prof. V. Ravichandran"
AUTHOR_CREDENTIALS = "28+ Years Corporate Finance & Banking | 10+ Years Academic Excellence"

# =============================================================================
# UI COLOR PALETTE (Institutional Theme)
# =============================================================================
COLORS = {
    "primary_dark": "#002147",      # Deep Navy for Sidebar/Header
    "primary_light": "#004b8d",     # Lighter Blue for gradients
    "accent_gold": "#FFD700",       # Gold for accents and borders
    "background": "#F5F5F5",
    "text": "#333333",
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545"
}

# =============================================================================
# FINANCIAL CONSTANTS (Default Assumptions)
# =============================================================================
FINANCIAL_DEFAULTS = {
    "risk_free_rate": 0.07,          # 7.0% (India 10Y G-Sec average)
    "market_return": 0.12,           # 12.0% (Nifty 50 long-term avg)
    "terminal_growth": 0.04,         # 4.0% (Long-term inflation target)
    "tax_rate": 0.25,                # Standard Corporate Tax
    "wacc_default": 12.0             # Default WACC percentage for EVA/DCF
}

# =============================================================================
# NAVIGATION (Expanded to 12 Specific Tabs)
# =============================================================================
TABS = [
    "📊 Dashboard",      # Tab 0
    "📋 Financials",     # Tab 1
    "📈 Profitability",  # Tab 2
    "🎯 DCF Valuation",  # Tab 3
    "💎 EVA Analysis",   # Tab 4
    "⚖️ Solvency",       # Tab 5
    "⚡ Efficiency",     # Tab 6
    "🚀 Growth",         # Tab 7
    "🏦 Shareholding",   # Tab 8
    "🛡️ Risk Metrics",   # Tab 9
    "💹 Peers",          # Tab 10
    "📝 Thesis"          # Tab 11
]

# =============================================================================
# DATA MAPPING (Screener.in Column Normalization)
# =============================================================================
# This helps the analyzer handle variations in export files
COLUMN_MAPPING = {
    "Net Profit": ["Net Profit", "Profit After Tax", "Pat"],
    "Sales": ["Sales", "Revenue", "Interest Earned"],
    "Borrowings": ["Borrowings", "Total Debt", "Long Term Borrowings"],
    "Equity": ["Equity Share Capital", "Share Capital"],
    "Interest": ["Interest", "Finance Costs"]
}
