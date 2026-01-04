
import streamlit as st

def format_indian_currency(number):
    """Formats large numbers into Indian format (Crores)."""
    if number >= 10000000:
        return f"₹{number/10000000:.2f} Cr"
    elif number >= 100000:
        return f"₹{number/100000:.2f} L"
    else:
        return f"₹{number:,.2f}"

def apply_custom_sidebar():
    """Applies your specific sidebar design with Mountain Path colors."""
    st.markdown(f"""
        <style>
            [data-testid="stSidebar"] {{
                background-color: #002147;
                color: white;
            }}
            [data-testid="stSidebar"] * {{
                color: white !important;
            }}
            .stButton>button {{
                background-color: #FFD700 !important;
                color: #002147 !important;
                font-weight: bold;
            }}
        </style>
    """, unsafe_allow_html=True)

def calculate_cagr(start_val, end_val, periods):
    """Calculates Compound Annual Growth Rate."""
    if start_val <= 0 or end_val <= 0 or periods <= 0:
        return 0
    return (pow(end_val / start_val, 1/periods) - 1) * 100
