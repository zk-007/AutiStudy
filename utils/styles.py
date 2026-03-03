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
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        h1, h2, h3 {
            line-height: 1.3;
        }
        
        /* ===== CRITICAL: Prevent horizontal overflow globally ===== */
        html, body {
            overflow-x: hidden !important;
            max-width: 100vw !important;
        }
        
        .stApp {
            background: linear-gradient(135deg, #E8F0FE 0%, #F5F8FF 100%);
            overflow-x: hidden !important;
            max-width: 100% !important;
        }
        
        /* Main container - responsive padding */
        .block-container {
            padding-top: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
            overflow-x: hidden !important;
        }
        
        /* Ensure all horizontal blocks don't overflow */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
            max-width: 100% !important;
            overflow-x: hidden !important;
        }
        
        /* Ensure columns fit properly */
        [data-testid="column"] {
            min-width: 0 !important;
            overflow: hidden !important;
        }
        
        /* Dashboard cards - ensure text doesn't overflow */
        [data-testid="column"] > div {
            overflow: hidden !important;
        }
        
        /* ===== FORCE SIDEBAR TO ALWAYS SHOW ===== */
        /* Critical for Streamlit Cloud deployment */
        [data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            min-width: 280px !important;
            width: 300px !important;
            transform: none !important;
            position: relative !important;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%);
            width: 100% !important;
            min-width: 280px !important;
        }
        
        [data-testid="stSidebarContent"] {
            display: block !important;
            visibility: visible !important;
        }
        
        /* Hide the collapse button since we force it open */
        [data-testid="stSidebar"] button[kind="header"] {
            display: none !important;
        }
        
        div[data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Adjust main content to account for sidebar */
        [data-testid="stAppViewContainer"] > section:first-child {
            margin-left: 0 !important;
        }
        
        /* ===== Form styling - Remove all backgrounds ===== */
        .stForm {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            box-shadow: none !important;
        }
        
        .stForm > div {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        
        /* Hide form instructions */
        [data-testid="InputInstructions"] {
            display: none !important;
        }
        
        /* ===== Text Input - Clean pill style ===== */
        .stTextInput > div {
            background: transparent !important;
        }
        
        .stTextInput > div > div {
            background: transparent !important;
            border: none !important;
        }
        
        .stTextInput input {
            border-radius: 30px !important;
            border: 2px solid #E2E8F0 !important;
            padding: 0.875rem 1.25rem !important;
            font-size: 1rem !important;
            background: white !important;
            min-height: 50px !important;
        }
        
        .stTextInput input:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        }
        
        .stTextInput input::placeholder {
            color: #94A3B8 !important;
            font-size: 0.95rem !important;
        }
        
        /* ===== Button styling ===== */
        .stButton > button {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: white !important;
            border-radius: 25px !important;
            padding: 0.75rem 1.25rem !important;
            border: none !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            min-height: 48px !important;
            transition: all 0.2s ease !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
            background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        }
        
        .stButton > button:focus,
        .stButton > button:active {
            color: white !important;
            background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
            outline: none !important;
        }
        
        .stButton > button p,
        .stButton > button span,
        .stButton > button div {
            color: white !important;
        }
        
        /* Primary button (larger) */
        [data-testid="stButton"] button[kind="primary"] {
            min-width: 140px !important;
            padding: 0.875rem 1.5rem !important;
        }
        
        /* ===== Other UI elements ===== */
        .main-header {
            background: white;
            padding: 1rem 1.5rem;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
        }
        
        .logo-text {
            color: #2563EB;
            font-size: 2.4rem;
            font-weight: 800;
        }
        
        .hero-section {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin: 1.5rem 0;
        }
        
        .hero-title {
            color: #1E3A5F;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        
        .hero-subtitle {
            color: #64748B;
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
        }
        
        .card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        .grade-card {
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-radius: 16px;
            padding: 1.25rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 3px solid transparent;
        }
        
        .grade-card:hover {
            transform: scale(1.03);
            border-color: #2563EB;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.2);
        }
        
        .grade-number {
            font-size: 2.5rem;
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
            padding: 1.25rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 3px solid #E2E8F0;
        }
        
        .subject-card:hover {
            border-color: #2563EB;
            transform: translateY(-2px);
        }
        
        .subject-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .subject-name {
            color: #1E3A5F;
            font-weight: 700;
            font-size: 1.1rem;
        }
        
        .sidebar-card {
            background: white;
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }
        
        .user-avatar {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 0.75rem;
            color: white;
            font-size: 1.75rem;
            font-weight: 700;
        }
        
        .user-name {
            text-align: center;
            color: #1E3A5F;
            font-weight: 700;
            font-size: 1.2rem;
        }
        
        .user-grade {
            text-align: center;
            color: #2563EB;
            font-size: 1rem;
        }
        
        .stars-badge {
            background: linear-gradient(135deg, #FCD34D 0%, #F59E0B 100%);
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            margin-top: 0.75rem;
        }
        
        .chat-container {
            background: white;
            border-radius: 16px;
            padding: 1.25rem;
            max-height: 500px;
            overflow-y: auto;
        }
        
        .chat-message {
            margin-bottom: 0.75rem;
            padding: 0.875rem;
            border-radius: 14px;
        }
        
        .user-message {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: white;
            margin-left: 15%;
        }
        
        .bot-message {
            background: #F1F5F9;
            color: #1E3A5F;
            margin-right: 15%;
        }
        
        /* Hide Streamlit branding */
        header[data-testid="stHeader"] {
            background: transparent;
            height: 0;
        }
        
        .stApp > header {
            background-color: transparent;
        }
        
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
        
        /* Login form styling */
        .login-card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
            max-width: 400px;
            margin: 1.5rem auto;
        }
        
        .login-title {
            color: #1E3A5F;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 1.5rem;
        }
        
        .form-label {
            color: #1E3A5F;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.4rem;
        }
        
        .footer {
            text-align: center;
            padding: 1.5rem;
            color: #64748B;
            font-size: 0.9rem;
        }
        
        .footer a {
            color: #2563EB;
            text-decoration: none;
        }
    </style>
    """, unsafe_allow_html=True)
