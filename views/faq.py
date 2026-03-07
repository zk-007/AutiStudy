import streamlit as st
from utils.language import t, is_urdu, get_language, set_language


def _inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #EAF2FF 0%, #F4F8FF 45%, #EDEBFF 100%);
        }

        section.main > div.block-container {
            max-width: 1000px;
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
            background: rgba(255,255,255,0.65);
            border: 1px solid rgba(148,163,184,0.18);
            border-radius: 22px;
            box-shadow: 0 12px 35px rgba(15,23,42,0.07);
            backdrop-filter: blur(10px);
        }

        .block-container {
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }

        footer, #MainMenu {
            visibility: hidden;
        }

        .faq-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .faq-title {
            color: #0F2D4A;
            font-size: 2.8rem;
            font-weight: 900;
            margin: 0 0 0.5rem 0;
        }

        .faq-subtitle {
            color: #64748B;
            font-size: 1.2rem;
            font-weight: 500;
            margin: 0;
        }

        .faq-category {
            color: #2563EB;
            font-size: 1.5rem;
            font-weight: 800;
            margin: 2rem 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .faq-item {
            background: white;
            border: 1px solid rgba(148,163,184,0.22);
            border-radius: 16px;
            margin-bottom: 1rem;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(15,23,42,0.04);
        }

        .faq-question {
            background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
            padding: 1.2rem 1.5rem;
            color: #0F2D4A;
            font-size: 1.15rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.8rem;
            border-bottom: 1px solid rgba(148,163,184,0.15);
        }

        .faq-question-icon {
            color: #2563EB;
            font-size: 1.3rem;
            flex-shrink: 0;
        }

        .faq-answer {
            padding: 1.2rem 1.5rem;
            color: #475569;
            font-size: 1.05rem;
            line-height: 1.8;
        }

        .faq-answer strong {
            color: #1E3A5F;
        }

        .faq-answer ul {
            margin: 0.5rem 0;
            padding-left: 1.5rem;
        }

        .faq-answer li {
            margin-bottom: 0.4rem;
        }

        .highlight-tip {
            background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
            border-left: 4px solid #10B981;
            border-radius: 8px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
            font-size: 1rem;
        }

        .contact-box {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            text-align: center;
            color: white;
        }

        .contact-title {
            font-size: 1.6rem;
            font-weight: 800;
            margin: 0 0 0.8rem 0;
        }

        .contact-text {
            font-size: 1.1rem;
            opacity: 0.95;
            margin: 0;
        }

        .rtl-text {
            direction: rtl;
            text-align: right;
        }

        @media (max-width: 768px) {
            .faq-title {
                font-size: 2.2rem;
            }
            .faq-question {
                font-size: 1.05rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# FAQ Data - English
FAQ_DATA_EN = {
    "General": [
        {
            "q": "What is AutiStudy?",
            "a": """AutiStudy is an <strong>AI-powered adaptive learning platform</strong> specifically designed for students with autism in grades 4-7 in Pakistan. It provides personalized tutoring in Mathematics, General Science, and Computer Science, aligned with Pakistan's national curriculum."""
        },
        {
            "q": "Who is AutiStudy designed for?",
            "a": """AutiStudy is designed for:
            <ul>
                <li><strong>Students on the autism spectrum</strong> in grades 4, 5, 6, and 7</li>
                <li><strong>Students in Pakistan</strong> following the national curriculum</li>
                <li>Children who benefit from <strong>patient, step-by-step learning</strong></li>
                <li>Learners who prefer <strong>visual and multi-modal</strong> explanations</li>
            </ul>"""
        },
        {
            "q": "Is AutiStudy free to use?",
            "a": """Yes! AutiStudy is currently free to use. Our mission is to make quality education accessible to all students, especially those with special learning needs."""
        },
        {
            "q": "What languages does AutiStudy support?",
            "a": """AutiStudy is fully <strong>bilingual</strong>, supporting both:
            <ul>
                <li><strong>English</strong> - Full interface and AI responses</li>
                <li><strong>اردو (Urdu)</strong> - Complete interface and AI responses in Urdu</li>
            </ul>
            You can switch between languages anytime using the language toggle."""
        }
    ],
    "Learning & Subjects": [
        {
            "q": "What subjects can I study?",
            "a": """AutiStudy covers three main subjects:
            <ul>
                <li><strong>🔢 Mathematics</strong> - Grades 4-7: Arithmetic, algebra, geometry, fractions, and more</li>
                <li><strong>🔬 General Science</strong> - Grades 4-7: Biology, physics, chemistry basics</li>
                <li><strong>💻 Computer Science</strong> - Grades 6-7: Computer basics, software, internet</li>
            </ul>
            All content is aligned with Pakistan's national curriculum textbooks."""
        },
        {
            "q": "How does the AI tutor work?",
            "a": """The AI tutor uses <strong>GPT-4o-mini</strong> combined with a <strong>RAG (Retrieval-Augmented Generation)</strong> system:
            <ul>
                <li>It searches your textbook content to find relevant information</li>
                <li>It provides accurate, curriculum-based answers</li>
                <li>It explains concepts step-by-step in simple language</li>
                <li>It's patient and encouraging, never rushing you</li>
            </ul>"""
        },
        {
            "q": "Can the AI generate images to explain concepts?",
            "a": """Yes! AutiStudy <strong>automatically generates visual aids</strong> when you ask "how" questions or request explanations. For example:
            <ul>
                <li>Ask "What is 2+4?" and then "How?" → Get a visual showing 2 apples + 4 apples = 6 apples</li>
                <li>Ask "How does multiplication work?" → Get a step-by-step visual explanation</li>
            </ul>
            You can also manually request images using the "Image Aid" button."""
        },
        {
            "q": "Does the AI remember my previous questions?",
            "a": """Yes! The AI has <strong>chat memory</strong>. It remembers the last several questions and answers in your conversation. So if you ask "What is addition?" and then follow up with "How?", the AI knows you're asking about addition."""
        }
    ],
    "Technical Questions": [
        {
            "q": "What if my question is not from the textbook?",
            "a": """AutiStudy will:
            <ul>
                <li><strong>Inform you</strong> that the topic is not in your grade's textbook</li>
                <li><strong>Provide a brief explanation</strong> to help you understand</li>
                <li><strong>Encourage you</strong> to ask questions from your textbook topics</li>
            </ul>
            If your question is about a completely different subject, it will suggest you switch to the correct subject."""
        },
        {
            "q": "Can I listen to the AI's explanations?",
            "a": """Yes! AutiStudy has <strong>Text-to-Speech</strong> capability. After the AI answers your question, click the "🔊 Voice Aid" button to hear the explanation read aloud. This is helpful for audio learners."""
        },
        {
            "q": "How do I create an account?",
            "a": """Creating an account is simple:
            <ul>
                <li>Click "Get Started" on the landing page</li>
                <li>Enter your name, email, and choose a password</li>
                <li>Select your grade (4, 5, 6, or 7)</li>
                <li>Start learning!</li>
            </ul>"""
        },
        {
            "q": "What browsers work best with AutiStudy?",
            "a": """AutiStudy works best on modern browsers:
            <ul>
                <li><strong>Google Chrome</strong> (recommended)</li>
                <li><strong>Microsoft Edge</strong></li>
                <li><strong>Firefox</strong></li>
                <li><strong>Safari</strong> (on Mac/iOS)</li>
            </ul>
            Make sure your browser is updated to the latest version."""
        }
    ],
    "Autism-Friendly Features": [
        {
            "q": "How is AutiStudy autism-friendly?",
            "a": """AutiStudy is designed with autism spectrum needs in mind:
            <ul>
                <li><strong>Clear, simple language</strong> - No complex jargon</li>
                <li><strong>Step-by-step explanations</strong> - Concepts broken into small pieces</li>
                <li><strong>Visual learning</strong> - Auto-generated images and diagrams</li>
                <li><strong>Patience</strong> - The AI never rushes, always supportive</li>
                <li><strong>Predictable interface</strong> - Calm, consistent design</li>
                <li><strong>Multi-modal learning</strong> - Text, images, and audio options</li>
            </ul>"""
        },
        {
            "q": "Is the interface designed to be calm and not overwhelming?",
            "a": """Yes! The AutiStudy interface uses:
            <ul>
                <li><strong>Soft, calming colors</strong> - Blues and whites</li>
                <li><strong>Clean layout</strong> - No cluttered elements</li>
                <li><strong>Consistent design</strong> - Same layout across all pages</li>
                <li><strong>Large, readable text</strong> - Easy on the eyes</li>
                <li><strong>Simple navigation</strong> - Easy to find what you need</li>
            </ul>"""
        },
        {
            "q": "Can parents/teachers monitor progress?",
            "a": """Currently, students can track their own progress through:
            <ul>
                <li><strong>Stars earned</strong> - Rewards for learning</li>
                <li><strong>Chat history</strong> - Review previous conversations</li>
                <li><strong>Subject progress</strong> - See what topics you've studied</li>
            </ul>
            Parent/teacher dashboards are coming soon!"""
        }
    ]
}

# FAQ Data - Urdu
FAQ_DATA_UR = {
    "عمومی سوالات": [
        {
            "q": "آٹی اسٹڈی کیا ہے؟",
            "a": """آٹی اسٹڈی ایک <strong>AI پر مبنی موافقت پذیر سیکھنے کا پلیٹ فارم</strong> ہے جو خاص طور پر پاکستان میں جماعت 4-7 کے آٹزم والے طلباء کے لیے ڈیزائن کیا گیا ہے۔ یہ ریاضی، جنرل سائنس اور کمپیوٹر سائنس میں ذاتی نوعیت کی تعلیم فراہم کرتا ہے۔"""
        },
        {
            "q": "آٹی اسٹڈی کس کے لیے ہے؟",
            "a": """آٹی اسٹڈی ان کے لیے ڈیزائن کیا گیا ہے:
            <ul>
                <li>جماعت 4، 5، 6 اور 7 کے <strong>آٹزم سپیکٹرم</strong> کے طلباء</li>
                <li>پاکستانی نصاب پڑھنے والے طلباء</li>
                <li>جو بچے <strong>صبر اور قدم بہ قدم سیکھنے</strong> سے فائدہ اٹھاتے ہیں</li>
            </ul>"""
        },
        {
            "q": "کیا آٹی اسٹڈی مفت ہے؟",
            "a": """جی ہاں! آٹی اسٹڈی فی الحال مفت ہے۔ ہمارا مشن معیاری تعلیم کو تمام طلباء کے لیے قابل رسائی بنانا ہے۔"""
        },
        {
            "q": "کون سی زبانیں دستیاب ہیں؟",
            "a": """آٹی اسٹڈی مکمل طور پر <strong>دو زبانوں</strong> میں دستیاب ہے:
            <ul>
                <li><strong>انگریزی</strong> - مکمل انٹرفیس اور AI جوابات</li>
                <li><strong>اردو</strong> - مکمل انٹرفیس اور AI جوابات</li>
            </ul>"""
        }
    ],
    "سیکھنے کے سوالات": [
        {
            "q": "کون سے مضامین پڑھ سکتے ہیں؟",
            "a": """آٹی اسٹڈی تین مضامین پڑھاتا ہے:
            <ul>
                <li><strong>🔢 ریاضی</strong> - جماعت 4-7</li>
                <li><strong>🔬 جنرل سائنس</strong> - جماعت 4-7</li>
                <li><strong>💻 کمپیوٹر سائنس</strong> - جماعت 6-7</li>
            </ul>"""
        },
        {
            "q": "AI ٹیوٹر کیسے کام کرتا ہے؟",
            "a": """AI ٹیوٹر <strong>GPT-4o-mini</strong> اور <strong>RAG سسٹم</strong> استعمال کرتا ہے:
            <ul>
                <li>یہ آپ کی نصابی کتاب سے متعلقہ معلومات تلاش کرتا ہے</li>
                <li>یہ درست، نصاب پر مبنی جوابات فراہم کرتا ہے</li>
                <li>یہ آسان زبان میں قدم بہ قدم وضاحت کرتا ہے</li>
            </ul>"""
        },
        {
            "q": "کیا AI تصاویر بنا سکتا ہے؟",
            "a": """جی ہاں! جب آپ "کیسے" کا سوال پوچھتے ہیں، آٹی اسٹڈی <strong>خودکار طور پر تصویری وضاحت</strong> بناتا ہے۔ مثال کے طور پر، "2+4 کیسے؟" پوچھیں اور 2 سیب + 4 سیب = 6 سیب کی تصویر دیکھیں۔"""
        }
    ]
}


def render_faq():
    _inject_css()

    urdu = is_urdu()
    text_dir = "rtl-text" if urdu else ""

    # Header with back button
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("← Back", key="back_home", use_container_width=True):
            st.session_state.navigate("landing")
    with col3:
        # Language toggle
        current_lang = get_language()
        new_lang = "ur" if current_lang == "en" else "en"
        lang_label = "اردو" if current_lang == "en" else "English"
        if st.button(lang_label, key="toggle_lang", use_container_width=True):
            set_language(new_lang)
            st.rerun()

    # Page Header
    if urdu:
        st.markdown(
            """
            <div class="faq-header rtl-text">
                <h1 class="faq-title">اکثر پوچھے گئے سوالات</h1>
                <p class="faq-subtitle">آٹی اسٹڈی کے بارے میں عام سوالات کے جوابات</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        faq_data = FAQ_DATA_UR
    else:
        st.markdown(
            """
            <div class="faq-header">
                <h1 class="faq-title">Frequently Asked Questions</h1>
                <p class="faq-subtitle">Find answers to common questions about AutiStudy</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        faq_data = FAQ_DATA_EN

    # Render FAQ categories and questions
    category_icons = {
        "General": "📋",
        "Learning & Subjects": "📚",
        "Technical Questions": "⚙️",
        "Autism-Friendly Features": "💙",
        "عمومی سوالات": "📋",
        "سیکھنے کے سوالات": "📚",
    }

    for category, questions in faq_data.items():
        icon = category_icons.get(category, "📌")
        st.markdown(
            f'<div class="faq-category {text_dir}">{icon} {category}</div>',
            unsafe_allow_html=True,
        )

        for item in questions:
            st.markdown(
                f"""
                <div class="faq-item">
                    <div class="faq-question {text_dir}">
                        <span class="faq-question-icon">❓</span>
                        {item["q"]}
                    </div>
                    <div class="faq-answer {text_dir}">
                        {item["a"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Still have questions? Contact section
    if urdu:
        st.markdown(
            """
            <div class="contact-box rtl-text">
                <h2 class="contact-title">🤔 ابھی بھی سوالات ہیں؟</h2>
                <p class="contact-text">
                    ہم یہاں مدد کے لیے ہیں! اپنے سوالات کے ساتھ ہم سے رابطہ کریں۔
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="contact-box">
                <h2 class="contact-title">🤔 Still Have Questions?</h2>
                <p class="contact-text">
                    We're here to help! If you couldn't find the answer you were looking for, 
                    feel free to reach out to us. Start learning today and let AutiStudy guide you!
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Quick tip
    st.markdown(
        """
        <div class="highlight-tip">
            <strong>💡 Quick Tip:</strong> You can ask the AI tutor any question about your subjects! 
            Just select your grade and subject, then type your question. The AI will help you understand 
            step by step.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Footer
    st.markdown(
        """
        <div style="text-align:center; margin-top:2rem; padding-top:1.5rem; border-top:1px solid rgba(148,163,184,0.3);">
            <div style="color:#2563EB; font-weight:800; font-size:1.3rem;">AutiStudy</div>
            <div style="color:#64748B; margin-top:0.3rem; font-size:0.95rem;">Made with ❤️ for students in Pakistan</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
