
import streamlit as st
from src.core.config import COMPANY_NAME, TAGLINE, AUTHOR, AUTHOR_CREDENTIALS

class UIComponents:
    @staticmethod
    def header(title):
        """Renders the branded Mountain Path Hero Header."""
        st.markdown(f"""
            <div class="hero-header">
                <h1 style="color: white; margin: 0; font-size: 2.5rem;">🏔️ {COMPANY_NAME}</h1>
                <p style="color: #FFD700; font-size: 1.2rem; margin: 5px 0;">{TAGLINE} | {title}</p>
                <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.2);">
                <p style="font-size: 0.9rem; opacity: 0.9;">{AUTHOR} • {AUTHOR_CREDENTIALS}</p>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def footer():
        """Renders the institutional footer."""
        st.divider()
        st.markdown(f"""
            <div style="text-align: center; padding: 20px; color: #666;">
                <p><b>{COMPANY_NAME} - World of Finance</b></p>
                <p>Bridging Academic Theory with Institutional Practice</p>
                <p style="font-size: 0.8rem;">© 2026 {AUTHOR}. All rights reserved.</p>
                <p style="font-size: 0.7rem; font-style: italic;">
                    Disclaimer: This tool is for educational purposes only. Financial analysis should not be 
                    interpreted as investment advice.
                </p>
            </div>
        """, unsafe_allow_html=True)
