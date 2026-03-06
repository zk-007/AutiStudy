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

        p, li, span, div {
            line-height: 1.5;
        }

        h1, h2, h3 {
            line-height: 1.2;
        }

        .stApp {
            background: #EEF3FB;
        }

        div[data-testid="stSidebarNav"] {
            display: none;
        }

        /* Keep Streamlit sidebar behavior natural */
        section[data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid #E2E8F0;
        }

        [data-testid="stSidebarContent"] {
            background: #FFFFFF !important;
            padding-top: 0.5rem;
        }

        /* Main page spacing */
        .block-container {
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-bottom: 2rem;
            max-width: 100%;
        }

        /* Hide extra Streamlit chrome only */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        .stDeployButton {
            display: none;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        header[data-testid="stHeader"] {
            background: transparent;
            height: 0;
        }

        .stApp > header {
            background: transparent;
        }

        /* Global buttons: cleaner default, no giant forced sizing */
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
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        .stButton > button:hover {
            color: white !important;
            background: linear-gradient(135deg, #3A78FF 0%, #2A58E0 100%) !important;
            transform: translateY(-1px);
            box-shadow: none;
        }

        .stButton > button:focus,
        .stButton > button:active {
            color: white !important;
            background: linear-gradient(135deg, #244FD1 0%, #1E40AF 100%) !important;
            box-shadow: none !important;
        }

        .stButton > button p,
        .stButton > button span,
        .stButton > button div {
            color: white !important;
            text-align: center !important;
        }

        /* Inputs */
        .stTextInput > div > div > input {
            border-radius: 18px;
            border: 2px solid #E2E8F0;
            padding: 0.9rem 1.2rem;
            font-size: 1rem;
            min-height: 52px;
        }

        .stTextInput > div > div > input:focus {
            border-color: #2563EB;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.10);
        }

        /* Reusable cards */
        .main-header {
            background: white;
            padding: 1rem 2rem;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
        }

        .logo-text {
            color: #2563EB;
            font-size: 2.4rem;
            font-weight: 800;
        }

        .hero-section {
            background: white;
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin: 2rem 0;
        }

        .hero-title {
            color: #1E3A5F;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        .hero-subtitle {
            color: #64748B;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }

        .feature-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: transform 0.2s;
            border: 2px solid transparent;
        }

        .feature-card:hover {
            transform: translateY(-4px);
            border-color: #2563EB;
        }

        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .feature-title {
            color: #1E3A5F;
            font-weight: 700;
            font-size: 1.1rem;
        }

        .card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }

        .grade-card {
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 3px solid transparent;
        }

        .grade-card:hover {
            transform: scale(1.03);
            border-color: #2563EB;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.15);
        }

        .grade-card.selected {
            border-color: #2563EB;
            background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        }

        .grade-number {
            font-size: 2.6rem;
            font-weight: 800;
            color: #2563EB;
        }

        .grade-label {
            color: #1E3A5F;
            font-weight: 600;
        }

        .subject-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid #E2E8F0;
        }

        .subject-card:hover {
            border-color: #2563EB;
            transform: translateY(-3px);
        }

        .subject-icon {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }

        .subject-name {
            color: #1E3A5F;
            font-weight: 700;
            font-size: 1.2rem;
        }

        .sidebar-card {
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }

        .user-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            color: white;
            font-size: 2rem;
            font-weight: 700;
        }

        .user-name {
            text-align: center;
            color: #1E3A5F;
            font-weight: 700;
            font-size: 1.3rem;
        }

        .user-grade {
            text-align: center;
            color: #2563EB;
            font-size: 1rem;
        }

        .stars-badge {
            background: linear-gradient(135deg, #FCD34D 0%, #F59E0B 100%);
            color: white;
            padding: 0.7rem 1rem;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            margin-top: 1rem;
        }

        .nav-item {
            display: flex;
            align-items: center;
            padding: 0.8rem 1rem;
            border-radius: 12px;
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.2s;
            color: #64748B;
            font-weight: 600;
        }

        .nav-item:hover {
            background: #EFF6FF;
            color: #2563EB;
        }

        .nav-item.active {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: white;
        }

        .nav-icon {
            margin-right: 0.75rem;
            font-size: 1.2rem;
        }

        .chat-container {
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            height: 500px;
            overflow-y: auto;
        }

        .chat-message {
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 16px;
        }

        .user-message {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: white;
            margin-left: 20%;
        }

        .bot-message {
            background: #F1F5F9;
            color: #1E3A5F;
            margin-right: 20%;
        }

        .input-container {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }

        .login-card {
            background: white;
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
            max-width: 400px;
            margin: 2rem auto;
        }

        .login-title {
            color: #1E3A5F;
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 2rem;
        }

        .form-label {
            color: #1E3A5F;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }

        .footer {
            text-align: center;
            padding: 2rem;
            color: #64748B;
            font-size: 1rem;
        }

        .footer a {
            color: #2563EB;
            text-decoration: none;
        }

        .how-it-works {
            text-align: center;
            padding: 2rem 0;
        }

        .how-it-works-title {
            color: #1E3A5F;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 2rem;
        }

        .step-item {
            display: inline-flex;
            align-items: center;
            margin: 0 1rem;
        }

        .step-icon {
            background: #EFF6FF;
            padding: 0.8rem;
            border-radius: 12px;
            margin-right: 0.5rem;
        }

        .step-text {
            color: #1E3A5F;
            font-weight: 600;
        }

        .step-arrow {
            color: #CBD5E1;
            margin: 0 1rem;
            font-size: 1.5rem;
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