import streamlit as st
import hashlib
import json
import os
from utils.session import create_session, delete_session, clear_session_cookie, set_session_cookie

USERS_FILE = "data/users.json"

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "selected_grade" not in st.session_state:
        st.session_state.selected_grade = None
    if "selected_subject" not in st.session_state:
        st.session_state.selected_subject = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = {}
    if "session_token" not in st.session_state:
        st.session_state.session_token = None
    if "language" not in st.session_state:
        st.session_state.language = "en"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def register_user(name, email, password, role, grade):
    users = load_users()
    if email in users:
        return False, "Email already registered"
    
    users[email] = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": role,
        "grade": grade,
        "stars": 0,
        "badges": [],
        "progress": {}
    }
    save_users(users)
    return True, "Registration successful"

def authenticate_user(email, password):
    users = load_users()
    if email in users:
        if users[email]["password"] == hash_password(password):
            user_data = users[email]
            # Get current language
            current_language = st.session_state.get("language", "en")
            # Create persistent session with current language
            token = create_session(email, user_data, current_page="dashboard", language=current_language)
            st.session_state.session_token = token
            # Set cookie in browser
            set_session_cookie(token)
            return True, user_data
    return False, None

def check_authentication():
    return st.session_state.get("authenticated", False)

def logout():
    # Clear persistent session
    if "session_token" in st.session_state and st.session_state.session_token:
        delete_session(st.session_state.session_token)
    clear_session_cookie()
    
    # Clear session state
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.selected_grade = None
    st.session_state.selected_subject = None
    st.session_state.chat_history = []
    st.session_state.current_chat_id = None
    st.session_state.generated_images = {}
    st.session_state.session_token = None
