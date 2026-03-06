import streamlit as st
from utils.auth import logout
from utils.language import t, is_urdu

def render_dashboard():
    user = st.session_state.user

    # RTL support for Urdu
    if is_urdu():
        st.markdown("""
        <style>
        .stApp { direction: rtl; }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* ── Sidebar base ── */
    section[data-testid="stSidebar"] {
        background: white !important;
        width: 260px !important;
        min-width: 260px !important;
        padding: 0 !important;
        transition: all 0.3s ease !important;
    }

    /* Sidebar inner content */
    section[data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem !important;
        background: white !important;
        height: 100vh !important;
        overflow-y: auto !important;
    }

    /* Collapse toggle arrow button — always visible */
    button[data-testid="baseButton-headerNoPadding"],
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
        color: #2563EB !important;
    }

    /* Main content area */
    .main .block-container {
        padding-top: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Hide streamlit default nav */
    div[data-testid="stSidebarNav"] { display: none !important; }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.65rem 1rem !important;
        min-height: 44px !important;
        margin-bottom: 0.4rem !important;
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        transform: none !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
    }

    /* Quick action cards */
    .qa-card {
        border-radius: 16px;
        padding: 1.4rem 1rem;
        text-align: center;
        color: white;
        margin-bottom: 0.75rem;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .qa-icon { font-size: 2.6rem; margin-bottom: 0.4rem; }
    .qa-title { font-weight: 700; font-size: 1.05rem; line-height: 1.3; }
    .qa-sub   { font-size: 0.9rem; opacity: 0.9; }

    /* Subject cards */
    .subj-card {
        background: #F8FAFC;
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        border: 2px solid #E2E8F0;
        margin-bottom: 0.75rem;
    }
    .subj-icon  { font-size: 3rem; margin-bottom: 0.4rem; }
    .subj-title { color: #1E3A5F; font-weight: 700; font-size: 1.15rem; }
    .subj-grade { color: #64748B; font-size: 0.95rem; }

    /* Rewards card */
    .rewards-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        text-align: center;
    }
    .rewards-title  { color: #1E3A5F; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.75rem; }
    .rewards-stars  { font-size: 2.6rem; color: #F59E0B; font-weight: 800; line-height: 1; }
    .rewards-label  { color: #64748B; font-size: 1rem; margin-top: 0.3rem; }
    .rewards-badges { font-size: 2rem; margin-top: 1rem; letter-spacing: 0.3rem; }
    .rewards-footer { color: #64748B; font-size: 0.9rem; margin-top: 0.75rem; }

    /* Subjects section wrapper */
    .subjects-wrapper {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .section-title { color: #1E3A5F; font-weight: 700; font-size: 1.25rem; margin-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

    # ── SIDEBAR ──────────────────────────────────────────────
    with st.sidebar:
        first_letter = user.get("name", "S")[0].upper()

        st.markdown(f"""
        <div style="text-align:center; padding-bottom:1rem; border-bottom:1px solid #E2E8F0; margin-bottom:1rem;">
            <div style="width:72px;height:72px;border-radius:50%;
                background:linear-gradient(135deg,#2563EB 0%,#1D4ED8 100%);
                display:flex;align-items:center;justify-content:center;
                margin:0 auto 0.75rem;color:white;font-size:1.8rem;font-weight:700;">
                {first_letter}
            </div>
            <div style="color:#1E3A5F;font-weight:700;font-size:1.1rem;">{user.get('name','Student')}</div>
            <div style="color:#2563EB;font-size:0.95rem;">{t('grade')} {user.get('grade',4)}</div>
            <div style="background:linear-gradient(135deg,#FCD34D 0%,#F59E0B 100%);
                color:white;padding:0.4rem 1rem;border-radius:20px;
                display:inline-block;font-weight:700;font-size:0.95rem;margin-top:0.75rem;">
                ⭐ {user.get('stars',0)} {t('stars_earned')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"🤖 {t('ai_tutor')}",          key="nav_ai_tutor",   use_container_width=True):
            st.session_state.navigate("ai_tutor")
        if st.button(f"📝 {t('practice_quiz')}",      key="nav_practice",   use_container_width=True):
            st.info(t("coming_soon"))
        if st.button(f"📊 {t('learning_analytics')}", key="nav_analytics",  use_container_width=True):
            st.info(t("coming_soon"))
        if st.button(f"🏆 {t('earn_rewards')}",       key="nav_rewards",    use_container_width=True):
            st.info(t("coming_soon"))
        if st.button(f"⚙️ Settings",                  key="nav_settings",   use_container_width=True):
            st.info(t("coming_soon"))

        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

        if st.button(f"🚪 {t('logout')}", key="nav_logout", use_container_width=True):
            logout()
            st.session_state.navigate("landing")

    # ── MAIN CONTENT ─────────────────────────────────────────
    st.markdown(f"""
    <h1 style="color:#1E3A5F;font-weight:800;margin-bottom:1.5rem;">
        {t('welcome_back_name')}, {user.get('name','Student')}! 👋
    </h1>
    """, unsafe_allow_html=True)

    # Quick Actions
    st.markdown(f'<div class="section-title">{t("quick_actions")}</div>', unsafe_allow_html=True)

    qa_col1, qa_col2, qa_col3, qa_col4 = st.columns(4)

    qa_items = [
        (qa_col1, "#3B82F6",  "#60A5FA", "🤖", t("chat_with_tutor"), t("ask_any_question"), t("start_chat"),     "quick_chat",     "ai_tutor"),
        (qa_col2, "#059669",  "#10B981", "📝", t("practice_quiz"),   t("test_knowledge"),  t("start_practice"), "quick_practice", None),
        (qa_col3, "#7C3AED",  "#8B5CF6", "📊", t("learning_analytics"), t("track_progress"), t("view_progress"), "quick_analytics", None),
        (qa_col4, "#D97706",  "#F59E0B", "🏆", t("earn_rewards"),    t("collect_badges"),  t("view_rewards"),   "quick_rewards",  None),
    ]

    for col, c1, c2, icon, title, sub, btn_label, btn_key, nav_target in qa_items:
        with col:
            st.markdown(f"""
            <div class="qa-card" style="background:linear-gradient(135deg,{c2} 0%,{c1} 100%);">
                <div class="qa-icon">{icon}</div>
                <div class="qa-title">{title}</div>
                <div class="qa-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(btn_label, key=btn_key, use_container_width=True):
                if nav_target:
                    st.session_state.navigate(nav_target)
                else:
                    st.info(t("coming_soon"))

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # Your Subjects + Your Rewards
    col_main, col_side = st.columns([2, 1])

    grade   = user.get("grade", 4)
    GRADE_SUBJECTS = {
        4: ["Maths", "General Science"],
        5: ["Maths", "General Science"],
        6: ["Maths", "General Science", "Computer"],
        7: ["Maths", "General Science", "Computer"],
    }
    subjects = GRADE_SUBJECTS.get(grade, ["Maths", "General Science"])
    subject_icons = {"Maths": "🔢", "General Science": "🔬", "Computer": "💻"}
    subject_translations = {
        "Maths":           t("maths"),
        "General Science": t("general_science"),
        "Computer":        t("computer"),
    }

    with col_main:
        st.markdown(f"""
        <div class="subjects-wrapper">
            <div class="section-title">{t('your_subjects')}</div>
        </div>
        """, unsafe_allow_html=True)

        sub_cols = st.columns(len(subjects))
        for scol, subject in zip(sub_cols, subjects):
            with scol:
                icon             = subject_icons.get(subject, "📚")
                translated_subj  = subject_translations.get(subject, subject)
                st.markdown(f"""
                <div class="subj-card">
                    <div class="subj-icon">{icon}</div>
                    <div class="subj-title">{translated_subj}</div>
                    <div class="subj-grade">{t('grade')} {grade}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"{t('study')} {translated_subj}", key=f"study_{subject}", use_container_width=True):
                    st.session_state.selected_grade   = grade
                    st.session_state.selected_subject = subject
                    st.session_state.navigate("chat")

    with col_side:
        stars = user.get("stars", 0)
        st.markdown(f"""
        <div class="rewards-card">
            <div class="rewards-title">{t('your_rewards')}</div>
            <div class="rewards-stars">{stars} ⭐</div>
            <div class="rewards-label">{t('stars_earned')}</div>
            <div class="rewards-badges">🏅 🎯 ⭐ 🌟</div>
            <div class="rewards-footer">{t('keep_learning')}</div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:1rem;border-top:1px solid #E2E8F0;color:#94A3B8;font-size:0.95rem;">
        By using our services, you agree to our
        <a href="#" style="color:#2563EB;">Privacy Policy</a> and
        <a href="#" style="color:#2563EB;">Terms of Service</a>.
    </div>
    """, unsafe_allow_html=True)
