import streamlit as st
from utils.language import t, is_urdu


def render_about():
    """Render the About page"""
    
    # RTL support for Urdu
    direction = "rtl" if is_urdu() else "ltr"
    text_align = "right" if is_urdu() else "left"
    
    # Inject CSS
    st.markdown(f"""
    <style>
    body {{ font-family: 'Nunito', sans-serif; }}
    a {{ text-decoration: none !important; }}
    
    .about-header {{
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
        cursor: pointer;
    }}
    
    .nav-btn:hover {{
        color: #1F3C88;
    }}
    
    .about-links {{
        display: flex;
        gap: 14px;
        background: #EEF4FF;
        padding: 8px 20px;
        border-radius: 30px;
    }}
    
    .small-btn {{
        font-size: 15px;
        font-weight: 600;
        color: #5A78C8;
        cursor: pointer;
    }}
    
    .small-btn:hover {{
        color: #1F3C88;
    }}
    
    .separator {{
        color: #B5C3EA;
    }}
    
    .about-hero {{
        max-width: 1100px;
        margin: 40px auto 0;
        text-align: center;
    }}
    
    .about-title {{
        font-size: 52px;
        font-weight: 800;
        color: #1F3C88;
        margin-bottom: 20px;
    }}
    
    .about-subtitle {{
        font-size: 20px;
        color: #3B4F7D;
        max-width: 700px;
        margin: 0 auto 40px;
        line-height: 1.6;
    }}
    
    .accordion-wrapper {{
        max-width: 900px;
        margin: 40px auto 80px;
        display: flex;
        flex-direction: column;
        gap: 18px;
        direction: {direction};
    }}
    
    details {{
        background: linear-gradient(135deg, #EEF3FF, #F7F9FF);
        border-radius: 18px;
        padding: 18px 22px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }}
    
    summary {{
        list-style: none;
        font-size: 18px;
        font-weight: 700;
        color: #1F3C88;
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
    }}
    
    summary::-webkit-details-marker {{
        display: none;
    }}
    
    summary::after {{
        content: "⌄";
        font-size: 22px;
        transition: transform 0.3s ease;
    }}
    
    details[open] summary::after {{
        transform: rotate(180deg);
    }}
    
    details p, details ul {{
        margin-top: 14px;
        color: #3B4F7D;
        line-height: 1.8;
        font-size: 15px;
        text-align: {text_align};
    }}
    
    details ul {{
        padding-left: 20px;
    }}
    
    details li {{
        margin-bottom: 8px;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back to Home", key="about_back"):
            st.session_state.navigate("landing")
    
    with col3:
        if st.button("FAQs →", key="about_to_faq"):
            st.session_state.navigate("faq")
    
    # Hero Section
    st.markdown("""
    <div class="about-hero">
        <h1 class="about-title">📚 About AutiStudy</h1>
        <p class="about-subtitle">
            An AI-powered learning companion designed specifically for autistic students 
            in Grades 4-7, making education accessible, engaging, and personalized.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Accordion Sections
    st.markdown("""
    <div class="accordion-wrapper">
        
        <details open>
            <summary>🎯 About the System</summary>
            <ul>
                <li>This chatbot is a smart learning helper made especially for autistic students.</li>
                <li>It helps students from Grade 4 to Grade 7 in Pakistan.</li>
                <li>It can explain Math, Science, and Computer subjects.</li>
                <li>It gives answers in simple and clear language (English & Urdu).</li>
                <li>It can show text, pictures, and even speak out loud.</li>
                <li>It remembers your learning preferences.</li>
                <li>It adjusts explanations based on how you learn best.</li>
                <li>It is designed to make learning calm, safe, and comfortable.</li>
            </ul>
        </details>
        
        <details>
            <summary>⚙️ How It Works</summary>
            <ul>
                <li>You type or speak your question to the chatbot.</li>
                <li>The system understands what you are asking.</li>
                <li>It searches your grade textbooks for correct information (RAG technology).</li>
                <li>It chooses the best way to explain — text, image, or voice.</li>
                <li>If you like pictures more, it shows images.</li>
                <li>If you prefer listening, it gives voice answers.</li>
                <li>It remembers where you stopped learning.</li>
                <li>You can continue anytime from the same place.</li>
            </ul>
        </details>
        
        <details>
            <summary>🛡️ Safety & Ethics</summary>
            <ul>
                <li>The chatbot gives answers only from trusted Pakistan curriculum textbooks.</li>
                <li>It does not guess or make up information.</li>
                <li>It avoids harmful or unsafe content.</li>
                <li>It protects your personal information.</li>
                <li>Your data is stored safely and securely.</li>
                <li>It does not replace doctors or therapists.</li>
                <li>Parents and teachers can monitor progress.</li>
                <li>The system is built to support and protect students.</li>
            </ul>
        </details>
        
        <details>
            <summary>📖 Coverage</summary>
            <ul>
                <li>The chatbot supports Grade 4 to Grade 7 students.</li>
                <li>It covers Math, General Science, and Computer subjects.</li>
                <li>It explains topics step by step.</li>
                <li>It supports text, pictures, and voice learning.</li>
                <li>It remembers your learning progress.</li>
                <li>It helps with homework and practice questions.</li>
                <li>It provides simple study feedback.</li>
                <li>It works online anytime you need help.</li>
            </ul>
        </details>
        
        <details>
            <summary>🌟 Special Features</summary>
            <ul>
                <li>Bilingual support: English and Urdu.</li>
                <li>AI-generated images to explain concepts visually.</li>
                <li>Text-to-speech for audio learning.</li>
                <li>Personalized learning based on student preferences.</li>
                <li>Progress tracking and rewards system.</li>
                <li>Clean, calm interface designed for neurodivergent learners.</li>
                <li>Automatic explanations for "how" questions.</li>
                <li>Chat memory to continue conversations naturally.</li>
            </ul>
        </details>
        
        <details>
            <summary>👥 Who Made This?</summary>
            <p>
                AutiStudy was developed as a Final Year Project to help autistic students 
                in Pakistan access quality education through AI technology. The system 
                combines modern AI (GPT-4, RAG, embeddings) with autism-friendly design 
                principles to create a supportive learning environment.
            </p>
        </details>
        
    </div>
    """, unsafe_allow_html=True)
