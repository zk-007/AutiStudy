import streamlit as st
from utils.llm import generate_response, generate_image, text_to_speech_base64
from utils.auth import logout
from utils.chat_db import get_user_chats, create_chat_session, save_message, get_chat_session, save_media_to_message
from utils.language import t, is_urdu, get_language


def render_chat():
    user = st.session_state.user
    grade = st.session_state.selected_grade or user.get("grade", 4)
    subject = st.session_state.selected_subject or "Maths"
    user_email = user.get("email", "guest")

    # Get current language
    current_language = get_language()
    
    # Initialize chat session if not exists
    if "current_chat_id" not in st.session_state or not st.session_state.current_chat_id:
        st.session_state.current_chat_id = create_chat_session(user_email, grade, subject, current_language)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "generated_images" not in st.session_state:
        st.session_state.generated_images = {}

    if "generated_audio" not in st.session_state:
        st.session_state.generated_audio = {}

    # ===== CRITICAL CSS FIXES =====
    # This CSS is carefully designed to work on both localhost AND Streamlit Cloud
    st.markdown("""
    <style>
    /* ===== PREVENT HORIZONTAL SCROLL ===== */
    html, body, .stApp, .main, section.main, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
        max-width: 100% !important;
    }
    
    .block-container {
        max-width: 100% !important;
        padding: 1rem 1rem 2rem 1rem !important;
        overflow-x: hidden !important;
    }
    
    /* Ensure columns don't overflow */
    [data-testid="stHorizontalBlock"] {
        max-width: 100% !important;
        overflow-x: hidden !important;
        flex-wrap: wrap !important;
    }
    
    [data-testid="column"] {
        max-width: 100% !important;
        overflow: hidden !important;
    }
    
    /* ===== FORM STYLING - Remove white box ===== */
    .stForm {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    
    .stForm > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        gap: 0.5rem !important;
    }
    
    .stForm [data-testid="stFormSubmitButton"] {
        margin-top: 0 !important;
    }
    
    /* Hide form instructions completely */
    [data-testid="InputInstructions"],
    .stForm [data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* ===== TEXT INPUT - Clean pill style only ===== */
    .stTextInput {
        background: transparent !important;
    }
    
    .stTextInput > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .stTextInput > div > div {
        background: transparent !important;
        border: none !important;
    }
    
    .stTextInput input {
        border-radius: 25px !important;
        border: 2px solid #CBD5E1 !important;
        padding: 0.75rem 1.25rem !important;
        font-size: 1rem !important;
        background: white !important;
        min-height: 48px !important;
        width: 100% !important;
    }
    
    .stTextInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
        outline: none !important;
    }
    
    .stTextInput input::placeholder {
        color: #94A3B8 !important;
        font-size: 0.9rem !important;
    }
    
    /* ===== QUICK QUESTION BUTTONS ===== */
    .quick-btn-container {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.5rem !important;
        margin-top: 0.5rem !important;
    }
    
    .quick-btn-container .stButton {
        flex: 1 1 auto !important;
        min-width: 120px !important;
        max-width: 200px !important;
    }
    
    .quick-btn-container .stButton > button {
        font-size: 0.85rem !important;
        padding: 0.5rem 0.75rem !important;
        min-height: 42px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.3 !important;
    }
    
    /* ===== PREVIOUS CHATS SIDEBAR ===== */
    .previous-chats-col {
        background: linear-gradient(180deg, #E9D5FF 0%, #DDD6FE 100%) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        min-height: 200px !important;
    }
    
    .previous-chats-title {
        color: #1E3A8A !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-align: center !important;
        margin-bottom: 0.75rem !important;
        white-space: nowrap !important;
    }
    
    .previous-chats-empty {
        background: rgba(255, 255, 255, 0.5) !important;
        border: 1px dashed rgba(99, 102, 241, 0.4) !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        text-align: center !important;
        color: #475569 !important;
        font-size: 0.85rem !important;
    }
    
    /* Previous chat buttons */
    .prev-chat-btn .stButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        font-size: 0.8rem !important;
        padding: 0.6rem 0.5rem !important;
        min-height: 56px !important;
        border-radius: 12px !important;
        white-space: normal !important;
        line-height: 1.25 !important;
        margin-bottom: 0.4rem !important;
    }
    
    .prev-chat-btn .stButton > button:hover {
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    }
    
    /* ===== RTL SUPPORT ===== */
    .rtl-mode {
        direction: rtl !important;
    }
    
    .rtl-mode [data-testid="stChatMessage"] {
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # RTL support for Urdu
    if is_urdu():
        st.markdown('<div class="rtl-mode">', unsafe_allow_html=True)

    # ===== LEFT SIDEBAR =====
    with st.sidebar:
        st.markdown(
            """
            <div style="background: white; border-radius: 16px; padding: 1.25rem; margin-bottom: 1rem; text-align: center;">
            """,
            unsafe_allow_html=True,
        )

        first_letter = user.get("name", "S")[0].upper()
        st.markdown(
            f"""
            <div style="width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
                display: flex; align-items: center; justify-content: center; margin: 0 auto 0.75rem; color: white; font-size: 1.75rem; font-weight: 700;">
                {first_letter}
            </div>
            <h3 style="color: #1E3A5F; margin: 0; font-weight: 700; font-size: 1.1rem;">{user.get('name', 'Student')}</h3>
            <p style="color: #2563EB; margin: 0.25rem 0; font-size: 0.9rem;">Grade {grade} - {subject}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(f"🏠 {t('dashboard')}", key="nav_dashboard", use_container_width=True):
            st.session_state.navigate("dashboard")

        if st.button(f"🤖 {t('change_subject')}", key="nav_ai_tutor", use_container_width=True):
            st.session_state.current_chat_id = None
            st.session_state.chat_history = []
            st.session_state.navigate("ai_tutor")

        if st.button(f"➕ {t('new_chat')}", key="new_chat", use_container_width=True):
            st.session_state.current_chat_id = create_chat_session(user_email, grade, subject, current_language)
            st.session_state.chat_history = []
            st.session_state.generated_images = {}
            st.session_state.generated_audio = {}
            st.rerun()

        if st.button(f"🗑️ {t('clear_chat')}", key="clear_chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.generated_images = {}
            st.rerun()

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        if st.button(f"🚪 {t('logout')}", key="nav_logout", use_container_width=True):
            logout()
            st.session_state.navigate("landing")

        # Current Session Info
        st.markdown(
            f"""
            <div style="background: #EFF6FF; border-radius: 12px; padding: 0.875rem; margin-top: 0.75rem;">
                <p style="color: #1E3A5F; font-weight: 600; margin: 0 0 0.4rem 0; font-size: 0.9rem;">{t('current_session')}</p>
                <p style="color: #64748B; font-size: 0.8rem; margin: 0;">{t('grade')}: {grade}</p>
                <p style="color: #64748B; font-size: 0.8rem; margin: 0;">{t('subject')}: {subject}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ===== MAIN LAYOUT - Use 3:1 ratio for better fit =====
    main_col, right_col = st.columns([3, 1], gap="medium")

    with main_col:
        # Header
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-right: 0.75rem;">🤖</div>
                <div>
                    <h2 style="color: #1E3A5F; font-weight: 800; margin: 0; font-size: 1.4rem;">{t('ai_tutor_title')}</h2>
                    <p style="color: #64748B; margin: 0; font-size: 0.9rem;">{t('grade')} {grade} - {subject}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Instructions box (only show if no chat history)
        if not st.session_state.chat_history:
            tutor_intro = t('tutor_intro').format(subject=subject, grade=grade)
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #DBEAFE 0%, #E0E7FF 50%, #EDE9FE 100%); border-radius: 14px; padding: 1.25rem; margin-bottom: 1rem; border-left: 4px solid #2563EB;">
                    <div style="display: flex; align-items: flex-start;">
                        <div style="font-size: 1.5rem; margin-right: 0.75rem;">💡</div>
                        <div>
                            <p style="color: #1E3A5F; font-weight: 700; margin: 0 0 0.4rem 0; font-size: 1.1rem;">{t('how_to_ask')}</p>
                            <p style="color: #475569; margin: 0; font-size: 0.95rem;">
                                {tutor_intro} 😊
                            </p>
                            <p style="color: #64748B; font-size: 0.85rem; margin: 0.4rem 0 0 0;">
                                <em>{t('example_questions')}</em>
                            </p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Initial input area
            render_input_area(grade, subject, user_email, "initial")

            # Quick Questions
            render_quick_questions(grade, subject, user_email)

        else:
            # Display conversation with input after each response
            display_conversation_with_inputs(grade, subject, user_email)

    with right_col:
        # Previous chats column with styling
        st.markdown('<div class="previous-chats-col">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="previous-chats-title">📂 {t("previous_chats")}</div>',
            unsafe_allow_html=True,
        )

        # Get previous chats (filtered by current language)
        previous_chats = get_user_chats(user_email, current_language)

        if previous_chats:
            st.markdown('<div class="prev-chat-btn">', unsafe_allow_html=True)
            for idx, chat in enumerate(previous_chats[:8]):  # Show last 8 chats
                chat_title = chat.get("title", "Untitled")
                chat_id = chat.get("id", "")

                if len(chat_title) > 22:
                    chat_title = chat_title[:22] + "..."

                is_current = chat_id == st.session_state.current_chat_id
                button_label = f"{'⭐ ' if is_current else '💬 '}{chat_title}"

                if st.button(
                    button_label,
                    key=f"chat_{chat_id}_{idx}",
                    use_container_width=True,
                ):
                    # Load this chat
                    session = get_chat_session(user_email, chat_id)
                    if session:
                        st.session_state.current_chat_id = chat_id
                        st.session_state.selected_grade = session.get("grade", grade)
                        st.session_state.selected_subject = session.get("subject", subject)
                        st.session_state.chat_history = session.get("messages", [])
                        
                        # Restore stored images and audio from messages
                        st.session_state.generated_images = {}
                        st.session_state.generated_audio = {}
                        messages = session.get("messages", [])
                        pair_idx = 0
                        for i, msg in enumerate(messages):
                            if msg["role"] == "assistant":
                                if msg.get("image_url"):
                                    st.session_state.generated_images[pair_idx] = msg["image_url"]
                                if msg.get("audio_base64"):
                                    st.session_state.generated_audio[pair_idx] = msg["audio_base64"]
                                pair_idx += 1
                        
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="previous-chats-empty">{t("no_previous_chats")}</div>',
                unsafe_allow_html=True,
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Close RTL div if needed
    if is_urdu():
        st.markdown('</div>', unsafe_allow_html=True)


def render_input_area(grade, subject, user_email, key_suffix):
    """Render the input area for asking questions"""
    st.markdown(
        f'<p style="color: #1E3A5F; font-weight: 600; font-size: 1rem; margin-bottom: 0.4rem;">{t("ask_question")}</p>',
        unsafe_allow_html=True,
    )

    with st.form(key=f"chat_form_{key_suffix}", clear_on_submit=True):
        col1, col2 = st.columns([4, 1], gap="small")

        with col1:
            user_input = st.text_input(
                t('type_question'),
                key=f"user_input_{key_suffix}",
                placeholder=t('type_question'),
                label_visibility="collapsed",
            )

        with col2:
            send_button = st.form_submit_button(f"{t('send')} 📤", use_container_width=True, type="primary")

        if send_button and user_input:
            process_user_input(user_input, grade, subject, user_email)


def render_quick_questions(grade, subject, user_email):
    """Render quick question buttons with responsive flex layout"""
    st.markdown(
        f'<p style="color: #64748B; font-size: 0.9rem; margin: 0.5rem 0 0.25rem 0;">{t("quick_question")}</p>',
        unsafe_allow_html=True,
    )

    quick_questions = {
        "Maths": [
            t("what_is_addition"),
            t("help_multiplication"),
            t("explain_fractions"),
            t("even_odd_numbers"),
        ],
        "General Science": [
            t("parts_of_plant"),
            t("solar_system"),
            t("states_of_matter"),
            t("how_magnets_work"),
        ],
        "Computer": [
            t("what_is_computer"),
            t("input_devices"),
            t("tell_about_internet"),
            t("what_is_software"),
        ],
    }

    questions = quick_questions.get(subject, quick_questions["Maths"])

    # Use 2 columns for better responsiveness (2 buttons per row)
    col1, col2 = st.columns(2, gap="small")
    
    for idx, question in enumerate(questions):
        with col1 if idx % 2 == 0 else col2:
            if st.button(question, key=f"quick_{idx}_{question}", use_container_width=True):
                process_user_input(question, grade, subject, user_email)


def process_user_input(user_input, grade, subject, user_email):
    """Process user input and generate response"""
    from utils.llm import generate_response

    # Add user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
    })

    # Save to database
    save_message(user_email, st.session_state.current_chat_id, "user", user_input)

    # Generate response
    with st.spinner("Thinking... 🤔"):
        response = generate_response(
            user_input,
            grade,
            subject,
            st.session_state.chat_history,
        )

    # Add assistant message
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response,
    })

    # Save to database
    save_message(user_email, st.session_state.current_chat_id, "assistant", response)

    st.rerun()


def display_conversation_with_inputs(grade, subject, user_email):
    """Display conversation with input fields after each response"""

    messages = st.session_state.chat_history

    # Group messages into Q&A pairs
    i = 0
    pair_idx = 0

    while i < len(messages):
        msg = messages[i]

        if msg["role"] == "user":
            # Display user message
            with st.chat_message("user", avatar="👤"):
                st.write(msg["content"])

            # Check if there's a response
            if i + 1 < len(messages) and messages[i + 1]["role"] == "assistant":
                assistant_msg = messages[i + 1]

                # Display assistant message
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(assistant_msg["content"])

                    # ImageAid and VoiceAid buttons
                    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])

                    # Get stored image/audio from message if available
                    stored_image = assistant_msg.get("image_url")
                    stored_audio = assistant_msg.get("audio_base64")
                    
                    # Message index for saving to database (assistant message index)
                    assistant_msg_idx = i + 1

                    with btn_col1:
                        if st.button(f"🖼️ {t('image_aid')}", key=f"imageaid_{pair_idx}", use_container_width=True):
                            with st.spinner(f"{t('generating_image')} 🎨"):
                                image_url = generate_image(msg["content"], grade, subject)
                                if image_url:
                                    st.session_state.generated_images[pair_idx] = image_url
                                    save_media_to_message(user_email, st.session_state.current_chat_id, assistant_msg_idx, image_url=image_url)
                                    st.rerun()
                                else:
                                    st.error(f"❌ {t('image_failed')}")

                    with btn_col2:
                        if st.button(f"🔊 {t('voice_aid')}", key=f"voiceaid_{pair_idx}", use_container_width=True):
                            with st.spinner(f"🔊 {t('generating_voice')}..."):
                                language = get_language()
                                audio_base64 = text_to_speech_base64(assistant_msg["content"], language)
                                if audio_base64:
                                    st.session_state.generated_audio[pair_idx] = audio_base64
                                    save_media_to_message(user_email, st.session_state.current_chat_id, assistant_msg_idx, audio_base64=audio_base64)
                                    st.rerun()
                                else:
                                    st.error(f"❌ {t('voice_failed')}")

                    # Display generated image (from session state or stored in DB)
                    display_image = st.session_state.generated_images.get(pair_idx) or stored_image
                    if display_image:
                        st.markdown(
                            f'<p style="color: #2563EB; font-weight: 600; font-size: 0.9rem; margin-top: 0.75rem;">🖼️ {t("generated_image")}</p>',
                            unsafe_allow_html=True,
                        )
                        st.image(display_image, use_container_width=True)

                    # Display generated audio (from session state or stored in DB)
                    display_audio = st.session_state.generated_audio.get(pair_idx) or stored_audio
                    if display_audio:
                        st.markdown(
                            f'<p style="color: #10B981; font-weight: 600; font-size: 0.9rem; margin-top: 0.75rem;">🔊 {t("listen_response")}</p>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"""
                            <audio controls style="width: 100%; border-radius: 8px;">
                                <source src="data:audio/mp3;base64,{display_audio}" type="audio/mp3">
                            </audio>
                            """,
                            unsafe_allow_html=True,
                        )

                i += 2  # Move past both user and assistant messages
                pair_idx += 1
            else:
                i += 1
        else:
            # Orphan assistant message (shouldn't happen normally)
            with st.chat_message("assistant", avatar="🤖"):
                st.write(msg["content"])
            i += 1

    # Divider
    st.markdown("<hr style='margin: 1rem 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    # Input area at the bottom for next question
    render_input_area(grade, subject, user_email, f"bottom_{len(messages)}")

    # Quick questions
    render_quick_questions(grade, subject, user_email)
