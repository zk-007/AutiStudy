import streamlit as st
from utils.auth import logout
from utils.language import t, is_urdu

def render_dashboard():
    user = st.session_state.user

    st.markdown("""
    <style>
    .stApp {
        background: #EEF3FB;
    }

    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }

    [data-testid="stSidebarContent"] {
        background: #FFFFFF !important;
        padding-top: 0.5rem;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border: none;
        border-radius: 22px;
        min-height: 58px;
        font-size: 1rem;
        font-weight: 600;
        color: white;
        background: linear-gradient(135deg, #2F6CF6 0%, #244FD1 100%);
        box-shadow: none;
        margin-bottom: 0.55rem;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        color: white;
        background: linear-gradient(135deg, #3A78FF 0%, #2A58E0 100%);
    }

    .stButton > button {
        border: none;
        border-radius: 22px;
        min-height: 54px;
        font-size: 1rem;
        font-weight: 600;
        color: white;
        background: linear-gradient(135deg, #2F6CF6 0%, #244FD1 100%);
        box-shadow: none;
    }

    .stButton > button:hover {
        color: white;
        background: linear-gradient(135deg, #3A78FF 0%, #2A58E0 100%);
    }

    .dashboard-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        line-height: 1.25;
        margin-bottom: 0.35rem;
        white-space: normal;
        word-break: break-word;
        text-align: center;
    }

    .dashboard-card-subtitle {
        font-size: 0.95rem;
        opacity: 0.95;
        line-height: 1.35;
        white-space: normal;
        word-break: break-word;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    if is_urdu():
        st.markdown("""
        <style>
        .stApp { direction: rtl; }
        </style>
        """, unsafe_allow_html=True)

    with st.sidebar:
        first_letter = user.get("name", "S")[0].upper()

        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 24px;
            padding: 1rem 0.4rem 0.7rem 0.4rem;
            text-align: center;
            margin-bottom: 1rem;
        ">
            <div style="
                width: 88px;
                height: 88px;
                border-radius: 50%;
                background: linear-gradient(135deg, #2F6CF6 0%, #244FD1 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1rem auto;
                color: white;
                font-size: 2.2rem;
                font-weight: 700;
            ">{first_letter}</div>

            <div style="color: #1E3A5F; font-size: 1.05rem; font-weight: 700; margin-bottom: 0.25rem;">
                {user.get('name', 'Student')}
            </div>

            <div style="color: #2563EB; font-size: 0.95rem; margin-bottom: 1rem;">
                {t('grade')} {user.get('grade', 4)}
            </div>

            <div style="
                background: linear-gradient(135deg, #F7C53A 0%, #F2A40A 100%);
                color: white;
                border-radius: 22px;
                padding: 0.9rem 1rem;
                font-weight: 700;
                font-size: 1rem;
                text-align: center;
                margin-bottom: 0.5rem;
            ">
                ⭐ {user.get('stars', 0)} {t('stars_earned')}
            </div>
        </div>
        """, unsafe_allow_html=True)

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

        if st.button(f"🚪 {t('logout')}", key="nav_logout", use_container_width=True):
            logout()
            st.session_state.navigate("landing")

    st.markdown(f"""
    <h1 style="
        color: #1E3A5F;
        font-weight: 800;
        font-size: 3rem;
        line-height: 1.1;
        margin-bottom: 2rem;
    ">
        {t('welcome_back_name')}, {user.get('name', 'Student')}! 👋
    </h1>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <h2 style="
        color: #1E3A5F;
        font-weight: 800;
        font-size: 2rem;
        margin-bottom: 1rem;
    ">
        {t('quick_actions')}
    </h2>
    """, unsafe_allow_html=True)

    q1, q2, q3, q4 = st.columns(4, gap="large")
    card_height = "230px"

    with q1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #67A7F8 0%, #4A86E8 100%);
            border-radius: 20px;
            height: {card_height};
            padding: 1.6rem 1.2rem;
            text-align: center;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-bottom: 0.8rem;
        ">
            <div style="font-size: 3.2rem; margin-bottom: 0.8rem;">🤖</div>
            <div class="dashboard-card-title">{t('chat_with_tutor')}</div>
            <div class="dashboard-card-subtitle">{t('ask_any_question')}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(t("start_chat"), key="quick_chat", use_container_width=True):
            st.session_state.navigate("ai_tutor")

    with q2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1FC48D 0%, #12A974 100%);
            border-radius: 20px;
            height: {card_height};
            padding: 1.6rem 1.2rem;
            text-align: center;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-bottom: 0.8rem;
        ">
            <div style="font-size: 3.2rem; margin-bottom: 0.8rem;">📝</div>
            <div class="dashboard-card-title">{t('practice_quiz')}</div>
            <div class="dashboard-card-subtitle">{t('test_knowledge')}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(t("start_practice"), key="quick_practice", use_container_width=True):
            st.info(t("coming_soon"))

    with q3:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #9860F6 0%, #7B42E8 100%);
            border-radius: 20px;
            height: {card_height};
            padding: 1.6rem 1.2rem;
            text-align: center;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-bottom: 0.8rem;
        ">
            <div style="font-size: 3.2rem; margin-bottom: 0.8rem;">📊</div>
            <div class="dashboard-card-title">{t('learning_analytics')}</div>
            <div class="dashboard-card-subtitle">{t('track_progress')}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(t("view_progress"), key="quick_analytics", use_container_width=True):
            st.info(t("coming_soon"))

    with q4:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #F5A105 0%, #E58D00 100%);
            border-radius: 20px;
            height: {card_height};
            padding: 1.6rem 1.2rem;
            text-align: center;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-bottom: 0.8rem;
        ">
            <div style="font-size: 3.2rem; margin-bottom: 0.8rem;">🏆</div>
            <div class="dashboard-card-title">{t('earn_rewards')}</div>
            <div class="dashboard-card-subtitle">{t('collect_badges')}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(t("view_rewards"), key="quick_rewards", use_container_width=True):
            st.info(t("coming_soon"))

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2.2, 1], gap="large")

    with col_main:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 24px;
            padding: 1.6rem;
            min-height: 145px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
            margin-bottom: 1rem;
        ">
            <h3 style="
                color: #1E3A5F;
                font-weight: 800;
                font-size: 1.9rem;
                margin: 0;
            ">
                {t('your_subjects')}
            </h3>
        </div>
        """, unsafe_allow_html=True)

        grade = user.get("grade", 4)

        GRADE_SUBJECTS = {
            4: ["Maths", "General Science"],
            5: ["Maths", "General Science"],
            6: ["Maths", "General Science", "Computer"],
            7: ["Maths", "General Science", "Computer"]
        }
        subjects = GRADE_SUBJECTS.get(grade, ["Maths", "General Science"])

        subject_icons = {
            "Maths": "🔢",
            "General Science": "🔬",
            "Computer": "💻"
        }

        subject_translations = {
            "Maths": t("maths"),
            "General Science": t("general_science"),
            "Computer": t("computer")
        }

        sub_cols = st.columns(len(subjects), gap="large")

        for col, subject in zip(sub_cols, subjects):
            with col:
                icon = subject_icons.get(subject, "📚")
                translated_subject = subject_translations.get(subject, subject)

                st.markdown(f"""
                <div style="
                    background: #F8FAFC;
                    border-radius: 20px;
                    padding: 1.7rem 1rem;
                    min-height: 285px;
                    text-align: center;
                    border: 1.5px solid #E2E8F0;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    margin-bottom: 0.8rem;
                ">
                    <div style="font-size: 4rem; margin-bottom: 0.9rem;">{icon}</div>
                    <div style="
                        color: #1E3A5F;
                        font-weight: 800;
                        font-size: 1.3rem;
                        line-height: 1.25;
                        margin-bottom: 0.35rem;
                        text-align: center;
                    ">
                        {translated_subject}
                    </div>
                    <div style="
                        color: #64748B;
                        font-size: 1rem;
                        line-height: 1.3;
                    ">
                        {t('grade')} {grade}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"{t('study')} {translated_subject}", key=f"study_{subject}", use_container_width=True):
                    st.session_state.selected_grade = grade
                    st.session_state.selected_subject = subject
                    st.session_state.navigate("chat")

    with col_side:
        stars = user.get("stars", 0)

        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 24px;
            padding: 1.8rem 1.6rem;
            min-height: 465px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
            text-align: center;
        ">
            <h3 style="
                color: #1E3A5F;
                font-weight: 800;
                font-size: 1.8rem;
                margin-top: 0;
                margin-bottom: 1.8rem;
                text-align: left;
            ">
                {t('your_rewards')}
            </h3>

            <div style="
                font-size: 3.8rem;
                font-weight: 800;
                color: #F59E0B;
                line-height: 1;
                margin-bottom: 0.5rem;
            ">
                {stars} ⭐
            </div>

            <div style="
                color: #64748B;
                font-size: 1.05rem;
                line-height: 1.4;
                margin-bottom: 1.4rem;
            ">
                {t('stars_earned')}
            </div>

            <div style="font-size: 2.8rem; margin-bottom: 1.4rem;">
                🏅 🎯 ⭐ 🌟
            </div>

            <div style="
                color: #64748B;
                font-size: 1rem;
                line-height: 1.7;
            ">
                {t('keep_learning')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
        text-align: center;
        padding: 1.2rem 0 0.5rem 0;
        border-top: 1px solid #E2E8F0;
        color: #94A3B8;
        font-size: 1rem;
    ">
        By using our services, you agree to our
        <a href="#" style="color: #2563EB;">Privacy Policy</a>
        and
        <a href="#" style="color: #2563EB;">Terms of Service</a>.
    </div>
    """, unsafe_allow_html=True)