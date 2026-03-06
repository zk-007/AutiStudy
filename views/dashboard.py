import streamlit as st
from utils.auth import logout
from utils.language import t, is_urdu

def render_dashboard():
    user = st.session_state.user

    # Initialize sidebar state
    if "sidebar_visible" not in st.session_state:
        st.session_state.sidebar_visible = True

    # RTL support for Urdu
    if is_urdu():
        st.markdown("""
        <style>
        .stApp { direction: rtl; }
        </style>
        """, unsafe_allow_html=True)

    # ── Global styles ──────────────────────────────────────────────────────────
    st.markdown("""
    <style>

    /* Hide Streamlit's native sidebar completely */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Main layout */
    .main .block-container {
        padding-top: 1.2rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    /* =============================================
       UNIFIED SIDEBAR PANEL STYLING
       Multiple sections styled to look like ONE panel
    ============================================= */
    
    /* Profile section - top of sidebar panel */
    .sidebar-profile {
        background: white;
        border-radius: 20px 20px 0 0;
        padding: 1.25rem 1rem 1rem 1rem;
        border: 1px solid #E2E8F0;
        border-bottom: none;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.03);
    }

    /* Nav buttons section - middle of sidebar panel */
    .sidebar-nav {
        background: white;
        padding: 0.5rem 0.6rem;
        border-left: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
    }

    /* Logout section - bottom of sidebar panel */
    .sidebar-logout {
        background: white;
        border-radius: 0 0 20px 20px;
        padding: 0.5rem 0.6rem 1rem 0.6rem;
        border: 1px solid #E2E8F0;
        border-top: none;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }

    /* Style all buttons in sidebar column to look unified */
    [data-testid="column"]:first-child .stButton > button {
        background: #f8f9fc !important;
        color: #1E3A5F !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="column"]:first-child .stButton > button:hover {
        background: #EFF6FF !important;
        border-color: #2563EB !important;
    }

    /* Main page headings */
    .main-heading {
        color: #1E3A5F;
        font-weight: 800;
        font-size: 2.2rem;
        margin-top: 0.5rem;
        margin-bottom: 1.4rem;
    }

    .section-heading {
        color: #1E3A5F;
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 1rem;
    }

    /* Dashboard cards */
    .dashboard-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e8e8e8;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        height: 100%;
    }

    /* Quick-action cards */
    .qa-card {
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        color: white;
        margin-bottom: 0.8rem;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* Subject cards */
    .subj-card {
        background: #F8FAFC;
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        border: 2px solid #E2E8F0;
        margin-bottom: 0.75rem;
    }

    /* Subjects wrapper */
    .subjects-wrap {
        background: white;
        border-radius: 20px;
        padding: 1.5rem 1.5rem 0.5rem 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }

    /* Fix overflow */
    html, body {
        overflow-x: hidden;
    }

    /* Toggle button styling */
    .toggle-button-container button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1.3rem !important;
        min-height: 42px !important;
        padding: 0.4rem 0.8rem !important;
    }
    .toggle-button-container button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
    }
    .toggle-button-container button p,
    .toggle-button-container button span {
        color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)

    # ── Toggle button callback ─────────────────────────────────────────────────
    def toggle_sidebar():
        st.session_state.sidebar_visible = not st.session_state.sidebar_visible

    # ── LAYOUT ─────────────────────────────────────────────────────────────────
    
    # Toggle button row - narrow column to keep it in corner
    top_left, top_rest = st.columns([0.6, 9.4])
    with top_left:
        st.markdown('<div class="toggle-button-container">', unsafe_allow_html=True)
        if st.button("☰", key="toggle_sidebar", help="Toggle sidebar"):
            toggle_sidebar()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Main layout with or without sidebar
    if st.session_state.sidebar_visible:
        sidebar_col, main_col = st.columns([1.05, 3.15], gap="large")
    else:
        sidebar_col, main_col = None, st.container()

    # ── CUSTOM SIDEBAR ─────────────────────────────────────────────────────────
    if st.session_state.sidebar_visible and sidebar_col is not None:
        with sidebar_col:
            first_letter = user.get("name", "S")[0].upper()
            name = user.get("name", "Student")
            grade_num = user.get("grade", 4)
            stars = user.get("stars", 0)

            # SECTION 1: Profile card (top of unified panel)
            st.markdown(f"""
            <div class="sidebar-profile">
                <div style="text-align:center; padding-bottom:1rem;
                     border-bottom:1px solid #E2E8F0; margin-bottom:1rem;">
                    <div style="width:72px;height:72px;border-radius:50%;
                        background:linear-gradient(135deg,#2563EB 0%,#1D4ED8 100%);
                        display:flex;align-items:center;justify-content:center;
                        margin:0 auto 0.6rem;color:white;font-size:1.8rem;font-weight:700;">
                        {first_letter}
                    </div>
                    <div style="color:#1E3A5F;font-weight:700;font-size:1.1rem;">{name}</div>
                    <div style="color:#2563EB;font-size:0.95rem;">{t('grade')} {grade_num}</div>
                </div>
                <div style="text-align:center;">
                    <span style="background:linear-gradient(135deg,#FCD34D 0%,#F59E0B 100%);
                        color:white;padding:0.4rem 1.2rem;border-radius:20px;
                        font-weight:700;font-size:0.95rem;display:inline-block;">
                        ⭐ {stars} {t('stars_earned')}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # SECTION 2: Nav buttons (middle of unified panel)
            st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
            if st.button(f"🤖 {t('ai_tutor')}", key="nav_ai_tutor", use_container_width=True):
                st.session_state.navigate("ai_tutor")
            if st.button(f"📝 {t('practice_quiz')}", key="nav_practice", use_container_width=True):
                st.info(t("coming_soon"))
            if st.button(f"📊 {t('learning_analytics')}", key="nav_analytics", use_container_width=True):
                st.info(t("coming_soon"))
            if st.button(f"🏆 {t('earn_rewards')}", key="nav_rewards", use_container_width=True):
                st.info(t("coming_soon"))
            if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
                st.info(t("coming_soon"))
            st.markdown('</div>', unsafe_allow_html=True)

            # SECTION 3: Logout (bottom of unified panel)
            st.markdown('<div class="sidebar-logout">', unsafe_allow_html=True)
            if st.button(f"🚪 {t('logout')}", key="nav_logout", use_container_width=True):
                logout()
                st.session_state.navigate("landing")
            st.markdown('</div>', unsafe_allow_html=True)

    # ── MAIN CONTENT ───────────────────────────────────────────────────────────
    with main_col:
        # Welcome heading
        st.markdown(f'<div class="main-heading">{t("welcome_back_name")}, {user.get("name","Student")}! 👋</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-heading">{t("quick_actions")}</div>', unsafe_allow_html=True)

        # ── Quick Actions ──────────────────────────────────────────────────────
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="qa-card" style="background:linear-gradient(135deg,#60A5FA 0%,#3B82F6 100%);">
                <div style="font-size:2.8rem;margin-bottom:0.4rem;">🤖</div>
                <div style="font-weight:700;font-size:1.1rem;">{t('chat_with_tutor')}</div>
                <div style="font-size:0.95rem;opacity:0.9;">{t('ask_any_question')}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(t("start_chat"), key="quick_chat", use_container_width=True):
                st.session_state.navigate("ai_tutor")

        with col2:
            st.markdown(f"""
            <div class="qa-card" style="background:linear-gradient(135deg,#10B981 0%,#059669 100%);">
                <div style="font-size:2.8rem;margin-bottom:0.4rem;">📝</div>
                <div style="font-weight:700;font-size:1.1rem;">{t('practice_quiz')}</div>
                <div style="font-size:0.95rem;opacity:0.9;">{t('test_knowledge')}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(t("start_practice"), key="quick_practice", use_container_width=True):
                st.info(t("coming_soon"))

        with col3:
            st.markdown(f"""
            <div class="qa-card" style="background:linear-gradient(135deg,#8B5CF6 0%,#7C3AED 100%);">
                <div style="font-size:2.8rem;margin-bottom:0.4rem;">📊</div>
                <div style="font-weight:700;font-size:1.1rem;">{t('learning_analytics')}</div>
                <div style="font-size:0.95rem;opacity:0.9;">{t('track_progress')}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(t("view_progress"), key="quick_analytics", use_container_width=True):
                st.info(t("coming_soon"))

        with col4:
            st.markdown(f"""
            <div class="qa-card" style="background:linear-gradient(135deg,#F59E0B 0%,#D97706 100%);">
                <div style="font-size:2.8rem;margin-bottom:0.4rem;">🏆</div>
                <div style="font-weight:700;font-size:1.1rem;">{t('earn_rewards')}</div>
                <div style="font-size:0.95rem;opacity:0.9;">{t('collect_badges')}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(t("view_rewards"), key="quick_rewards", use_container_width=True):
                st.info(t("coming_soon"))

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

        # ── Your Subjects + Your Rewards ───────────────────────────────────────
        col_main, col_side = st.columns([2, 1])

        grade = user.get("grade", 4)
        GRADE_SUBJECTS = {
            4: ["Maths", "General Science"],
            5: ["Maths", "General Science"],
            6: ["Maths", "General Science", "Computer"],
            7: ["Maths", "General Science", "Computer"],
        }
        subjects = GRADE_SUBJECTS.get(grade, ["Maths", "General Science"])
        subject_icons = {"Maths": "🔢", "General Science": "🔬", "Computer": "💻"}
        subject_translations = {
            "Maths": t("maths"),
            "General Science": t("general_science"),
            "Computer": t("computer"),
        }

        with col_main:
            st.markdown(f"""
            <div class="subjects-wrap">
                <h3 style="color:#1E3A5F;font-weight:700;margin:0 0 1rem 0;">{t('your_subjects')}</h3>
            </div>
            """, unsafe_allow_html=True)

            sub_cols = st.columns(len(subjects))
            for scol, subject in zip(sub_cols, subjects):
                with scol:
                    icon = subject_icons.get(subject, "📚")
                    translated_subj = subject_translations.get(subject, subject)
                    st.markdown(f"""
                    <div class="subj-card">
                        <div style="font-size:3.2rem;margin-bottom:0.4rem;">{icon}</div>
                        <div style="color:#1E3A5F;font-weight:700;font-size:1.2rem;">{translated_subj}</div>
                        <div style="color:#64748B;font-size:0.95rem;">{t('grade')} {grade}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"{t('study')} {translated_subj}",
                                 key=f"study_{subject}", use_container_width=True):
                        st.session_state.selected_grade = grade
                        st.session_state.selected_subject = subject
                        st.session_state.navigate("chat")

        with col_side:
            stars = user.get("stars", 0)
            rewards_title = t('your_rewards')
            stars_label = t('stars_earned')
            keep_learning = t('keep_learning')

            st.markdown(f"""
            <div class="dashboard-card" style="text-align: center; min-height: 300px;">
                <h3 style="color:#1E3A5F;font-weight:700;margin-bottom:1.5rem;text-align:left;">{rewards_title}</h3>
                <div style="display:flex;align-items:center;justify-content:center;gap:0.5rem;margin-bottom:0.4rem;">
                    <span style="font-size:3.5rem;color:#F59E0B;font-weight:800;">{stars}</span>
                    <span style="font-size:3rem;">⭐</span>
                </div>
                <p style="color:#64748B;font-size:1.1rem;margin:0.3rem 0 1.5rem 0;">{stars_label}</p>
                <div style="display:flex;justify-content:center;gap:1rem;margin-bottom:1.5rem;font-size:2.4rem;">
                    <span>🏅</span><span>🎯</span><span>⭐</span><span>🌟</span>
                </div>
                <p style="color:#64748B;font-size:1rem;">{keep_learning}</p>
            </div>
            """, unsafe_allow_html=True)

        # ── Footer ─────────────────────────────────────────────────────────────
        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;padding:1rem;border-top:1px solid #E2E8F0;
             color:#94A3B8;font-size:0.9rem;">
            By using our services, you agree to our
            <a href="#" style="color:#2563EB;">Privacy Policy</a> and
            <a href="#" style="color:#2563EB;">Terms of Service</a>.
        </div>
        """, unsafe_allow_html=True)
