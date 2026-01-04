
import streamlit as st
from src.core.config import COMPANY_NAME, TAGLINE, AUTHOR, AUTHOR_CREDENTIALS

class UIComponents:
    @staticmethod
    def header(title):
        """Renders the branded Mountain Path Hero Header using CSS classes."""
        st.markdown(f"""
            <div class="main-header">
                <h1>🏔️ {COMPANY_NAME}</h1>
                <p style="color: #FFD700; font-size: 1.2rem; margin: 5px 0; font-weight: bold;">
                    {TAGLINE} | {title}
                </p>
                <div style="height: 1px; background-color: rgba(255,255,255,0.2); margin: 10px 0;"></div>
                <p style="font-size: 0.9rem; color: white; opacity: 0.9; margin: 0;">
                    {AUTHOR}
                </p>
                <p style="font-size: 0.8rem; color: white; opacity: 0.7; margin: 0;">
                    {AUTHOR_CREDENTIALS}
                </p>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def footer():
        """Renders the institutional sticky footer with gold accent."""
        st.markdown(f"""
            <div class="footer">
                <div style="margin-bottom: 5px;">
                    <b>{COMPANY_NAME} - {TAGLINE}</b>
                </div>
                <div style="font-size: 0.8rem; opacity: 0.8;">
                    Bridging Academic Theory with Institutional Practice | © 2026 {AUTHOR}
                </div>
                <div style="font-size: 0.7rem; font-style: italic; margin-top: 5px; opacity: 0.6;">
                    Disclaimer: Educational purposes only. Not investment advice.
                </div>
            </div>
        """, unsafe_allow_html=True)
