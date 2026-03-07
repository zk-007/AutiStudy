import streamlit as st
from utils.language import t, is_urdu


def render_faq():
    """Render the FAQ page"""
    
    # RTL support for Urdu
    direction = "rtl" if is_urdu() else "ltr"
    text_align = "right" if is_urdu() else "left"
    
    # FAQ Data
    faqs = [
        ("1️⃣ What is this AI chatbot for?",
         "This AI chatbot is designed to help autistic students in Grades 4–7 understand school subjects more easily. It provides personalized, patient, and clear explanations."),
        
        ("2️⃣ How does the chatbot answer questions?",
         "It uses Retrieval-Augmented Generation (RAG), searching approved Pakistan curriculum textbooks before generating answers. This ensures accurate, curriculum-aligned responses."),
        
        ("3️⃣ What subjects are supported?",
         "Mathematics, General Science (Biology, Physics, Chemistry), and Computer Studies for Grades 4-7."),
        
        ("4️⃣ Is the chatbot safe for children?",
         "Yes. It filters harmful content and only uses trusted educational material from approved textbooks."),
        
        ("5️⃣ Does it replace teachers?",
         "No. It supports learning but does not replace teachers, parents, or educational professionals. It's a learning companion."),
        
        ("6️⃣ How does personalization work?",
         "It remembers your grade level, subject preferences, and learning progress. It can also adapt explanations based on how you prefer to learn (text, images, or voice)."),
        
        ("7️⃣ Can parents monitor progress?",
         "Yes. Parents can view learning summaries and chat history to track their child's progress."),
        
        ("8️⃣ How are difficult topics handled?",
         "It breaks complex topics into smaller, manageable steps and provides simple examples. For visual learners, it can generate helpful images."),
        
        ("9️⃣ What technology powers it?",
         "AI (GPT-4), Natural Language Processing (NLP), Retrieval-Augmented Generation (RAG), vector search (ChromaDB), embeddings, and text-to-speech."),
        
        ("🔟 Does it store personal data?",
         "Only necessary learning data is stored securely. Personal information is protected and not shared with third parties."),
        
        ("1️⃣1️⃣ Can it work on mobile?",
         "Yes. It runs on laptops, tablets, and phones through any modern web browser."),
        
        ("1️⃣2️⃣ What if it doesn't understand my question?",
         "It will ask you to clarify or rephrase your question. You can also try asking in a different way."),
        
        ("1️⃣3️⃣ Can it remember our conversation?",
         "Yes. It saves chat history and can continue from where you left off. It remembers context within a conversation."),
        
        ("1️⃣4️⃣ Does it require internet?",
         "Yes. The AI features require an active internet connection to work."),
        
        ("1️⃣5️⃣ What if I face technical problems?",
         "Try refreshing the page or checking your internet connection. If problems persist, contact your teacher or administrator."),
        
        ("1️⃣6️⃣ Can I use it in Urdu?",
         "Yes! AutiStudy supports both English and Urdu. You can switch languages from your profile settings."),
        
        ("1️⃣7️⃣ How do I earn stars and rewards?",
         "You earn stars by asking questions, completing learning sessions, and engaging with the chatbot regularly."),
        
        ("1️⃣8️⃣ Can I get images to help me understand?",
         "Yes! Click the 'Image Aid' button after any answer, or ask 'how' questions - the system will automatically generate helpful visuals."),
        
        ("1️⃣9️⃣ Can I listen to answers?",
         "Yes! Click the 'Voice Aid' button to hear any answer read aloud. This helps with audio learning."),
        
        ("2️⃣0️⃣ What grades does it support?",
         "Currently, AutiStudy supports Grade 4, 5, 6, and 7 students following the Pakistan national curriculum.")
    ]
    
    # Session state for visible FAQs
    if "faq_visible" not in st.session_state:
        st.session_state.faq_visible = 8
    
    visible_count = st.session_state.faq_visible
    
    # Inject CSS
    st.markdown(f"""
    <style>
    body {{ font-family: 'Nunito', sans-serif; }}
    a {{ text-decoration: none !important; }}
    
    .page-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(235, 243, 255, 0.85);
        padding: 14px 24px;
        border-radius: 22px;
        margin: 20px auto;
        max-width: 1000px;
    }}
    
    .nav-btn {{
        font-size: 16px;
        font-weight: 600;
        color: #5A78C8;
    }}
    
    .page-hero {{
        max-width: 1100px;
        margin: 40px auto 0;
        text-align: center;
    }}
    
    .page-title {{
        font-size: 48px;
        font-weight: 800;
        color: #1F3C88;
        margin-bottom: 15px;
    }}
    
    .page-subtitle {{
        margin-top: 12px;
        font-size: 18px;
        color: #3B4F7D;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }}
    
    .faq-section {{
        max-width: 900px;
        margin: 50px auto 80px;
        direction: {direction};
    }}
    
    .faq-question {{
        background: linear-gradient(135deg, #DCE8FF, #E8F0FF);
        padding: 16px 22px;
        border-radius: 14px;
        margin-bottom: 8px;
        font-weight: 700;
        font-size: 16px;
        color: #1F3C88;
        text-align: {text_align};
    }}
    
    .faq-answer {{
        background: white;
        padding: 16px 22px;
        border-radius: 14px;
        margin-bottom: 22px;
        color: #3B4F7D;
        font-size: 15px;
        line-height: 1.7;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
        text-align: {text_align};
    }}
    
    .view-more-btn {{
        text-align: center;
        margin: 30px 0;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back to Home", key="faq_back"):
            st.session_state.navigate("landing")
    
    with col3:
        if st.button("About →", key="faq_to_about"):
            st.session_state.navigate("about")
    
    # Hero Section
    st.markdown("""
    <div class="page-hero">
        <h1 class="page-title">❓ Frequently Asked Questions</h1>
        <p class="page-subtitle">
            Answers to common questions about our adaptive AI chatbot for autistic students.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ Section
    st.markdown('<div class="faq-section">', unsafe_allow_html=True)
    
    for i in range(min(visible_count, len(faqs))):
        question, answer = faqs[i]
        st.markdown(f'<div class="faq-question">{question}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="faq-answer">{answer}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # View More Button
    if visible_count < len(faqs):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📋 View More FAQs", key="view_more_faqs", use_container_width=True):
                if visible_count == 8:
                    st.session_state.faq_visible = 15
                else:
                    st.session_state.faq_visible = len(faqs)
                st.rerun()
    elif visible_count >= len(faqs):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📋 Show Less", key="show_less_faqs", use_container_width=True):
                st.session_state.faq_visible = 8
                st.rerun()
