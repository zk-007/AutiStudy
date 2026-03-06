import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

        * {
            font-family: 'Nunito', sans-serif;
            box-sizing: border-box;
        }

        html, body, [class*="css"] {
            font-size: 18px;
        }

        .stApp {
            background: #EEF3FB;
        }

        div[data-testid="stSidebarNav"] {
            display: none;
        }

        section[data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid #E2E8F0;
        }

        [data-testid="stSidebarContent"] {
            background: #FFFFFF !important;
            padding-top: 0.5rem;
        }

        .block-container {
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-bottom: 2rem;
            max-width: 100%;
        }

        #MainMenu, footer, .stDeployButton, [data-testid="stToolbar"] {
            display: none !important;
        }

        /* IMPORTANT: do NOT hide the header, otherwise the sidebar arrow disappears */
        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        .stApp > header {
            background: transparent !important;
        }

        .stButton > button {
            width: 100%;
            border: none;
            border-radius: 22px;
            min-height: 54px;
            padding: 0.8rem 1.2rem;
            font-size: 1rem;
            font-weight: 700;
            color: white !important;
            background: linear-gradient(135deg, #2F6CF6 0%, #244FD1 100%) !important;
            transition: all 0.2s ease;
            box-shadow: none;
            white-space: normal !important;
            line-height: 1.25;
            text-align: center;
        }

        .stButton > button:hover {
            color: white !important;
            background: linear-gradient(135deg, #3A78FF 0%, #2A58E0 100%) !important;
            transform: translateY(-1px);
        }

        .stButton > button:focus,
        .stButton > button:active {
            color: white !important;
            box-shadow: none !important;
        }

        .stTextInput > div > div > input {
            border-radius: 18px;
            border: 2px solid #E2E8F0;
            padding: 0.9rem 1.2rem;
            font-size: 1rem;
            min-height: 52px;
        }

        @media (max-width: 1200px) {
            .block-container {
                padding-left: 1.2rem;
                padding-right: 1.2rem;
            }

            html, body, [class*="css"] {
                font-size: 16px;
            }
        }
    </style>
    """, unsafe_allow_html=True)