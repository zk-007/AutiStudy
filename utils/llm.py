import os
import re
import json
import base64
import uuid
from typing import List, Dict, Optional, Any

import streamlit as st
from openai import OpenAI

from utils.rag import query_knowledge_base, format_context_for_prompt


# =========================================================
# OPENAI KEY SETTINGS
# =========================================================
# Put your OpenAI key file path here if you are storing the key in a text file.
# Example:
# OPENAI_API_KEY_FILE = r"D:\AutoStudy\openai_api_key.txt"
OPENAI_API_KEY_FILE = r"PASTE_YOUR_OPENAI_KEY_FILE_PATH_HERE"


def _read_api_key_from_file(file_path: str) -> str:
    """Read API key from a text file."""
    try:
        if (
            file_path
            and file_path != "PASTE_YOUR_OPENAI_KEY_FILE_PATH_HERE"
            and os.path.exists(file_path)
        ):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception as e:
        print(f"Error reading API key file: {e}")
    return ""


def get_openai_client():
    """Get OpenAI client from env, Streamlit secrets, or local key file."""
    api_key = (
        os.getenv("OPENAI_API_KEY")
        or st.secrets.get("OPENAI_API_KEY", "")
        or _read_api_key_from_file(OPENAI_API_KEY_FILE)
    )

    if not api_key:
        return None

    return OpenAI(api_key=api_key)


# =========================================================
# TEXT TUTOR PROMPT
# =========================================================
SYSTEM_PROMPT_EN = """You are AutiStudy AI Tutor, a friendly and patient educational assistant designed specifically for students with autism in grades 4-7 in Pakistan.

Your teaching style:
- Use simple, clear language appropriate for the student's grade level
- Break down complex concepts into smaller, manageable steps
- Be patient, encouraging, and supportive
- Use examples from everyday life when possible
- Provide visual descriptions when helpful
- Repeat important points when needed
- Celebrate small achievements
- Avoid overwhelming the student with too much information at once

Current Context:
- Student Grade: {grade}
- Subject: {subject}

When answering questions:
1. First acknowledge the student's question
2. Provide a clear, step-by-step explanation
3. Use relevant examples
4. Check understanding with a simple follow-up question
5. Encourage the student

If you have reference material provided, use it to give accurate answers about the Pakistan curriculum.
If you don't have specific information, be honest but helpful.

Remember: Your goal is to make learning enjoyable and accessible!
"""

SYSTEM_PROMPT_UR = """آپ آٹی اسٹڈی AI ٹیوٹر ہیں، ایک دوستانہ اور صبر کرنے والے تعلیمی معاون جو خاص طور پر پاکستان میں جماعت 4-7 کے آٹزم والے طلباء کے لیے ڈیزائن کیا گیا ہے۔

آپ کا تدریسی انداز:
- طالب علم کی جماعت کی سطح کے مطابق آسان، واضح زبان استعمال کریں
- پیچیدہ تصورات کو چھوٹے، قابل انتظام مراحل میں تقسیم کریں
- صبر کریں، حوصلہ افزائی کریں، اور معاون بنیں
- جب ممکن ہو روزمرہ زندگی کی مثالیں استعمال کریں
- جب مددگار ہو تو بصری وضاحت فراہم کریں
- اہم نکات کو ضرورت کے مطابق دہرائیں
- چھوٹی کامیابیوں کا جشن منائیں
- ایک وقت میں بہت زیادہ معلومات سے طالب علم کو مغلوب نہ کریں

موجودہ سیاق و سباق:
- طالب علم کی جماعت: {grade}
- مضمون: {subject}

سوالات کا جواب دیتے وقت:
1. پہلے طالب علم کے سوال کو تسلیم کریں
2. واضح، قدم بہ قدم وضاحت فراہم کریں
3. متعلقہ مثالیں استعمال کریں
4. سمجھ کی جانچ کے لیے ایک سادہ فالو اپ سوال پوچھیں
5. طالب علم کی حوصلہ افزائی کریں

اگر آپ کے پاس حوالہ مواد فراہم کیا گیا ہے، تو اسے پاکستانی نصاب کے بارے میں درست جوابات دینے کے لیے استعمال کریں۔
اگر آپ کے پاس مخصوص معلومات نہیں ہیں، تو ایماندار مگر مددگار بنیں۔

یاد رکھیں: آپ کا مقصد سیکھنے کو خوشگوار اور قابل رسائی بنانا ہے!

اہم: آپ کو ہمیشہ اردو میں جواب دینا ہے۔ تمام وضاحتیں، مثالیں اور جوابات اردو میں ہونے چاہئیں۔
"""


def get_system_prompt(language: str = "en") -> str:
    """Get the system prompt based on selected language"""
    if language == "ur":
        return SYSTEM_PROMPT_UR
    return SYSTEM_PROMPT_EN


def generate_response(
    user_message: str,
    grade: int,
    subject: str,
    chat_history: List[Dict],
    use_rag: bool = True,
    language: str = None,
) -> str:
    """Generate a response using GPT-4o-mini with optional RAG."""
    
    # Get language from session state if not provided
    if language is None:
        language = st.session_state.get("language", "en")

    client = get_openai_client()
    if not client:
        if language == "ur":
            return "معذرت، لیکن میں ابھی صحیح طریقے سے ترتیب نہیں ہوں۔ براہ کرم اپنے استاد سے OpenAI API کلید سیٹ اپ کرنے کو کہیں۔"
        return (
            "I'm sorry, but I'm not properly configured yet. "
            "Please ask your teacher to set up the OpenAI API key."
        )

    context = ""
    is_from_textbook = True
    query_related_to_subject = True
    
    if use_rag:
        try:
            rag_result = query_knowledge_base(user_message, grade, subject)
            documents = rag_result.get("documents", [])
            is_from_textbook = rag_result.get("is_relevant", False)
            relevance_score = rag_result.get("relevance_score", 0)
            query_related_to_subject = rag_result.get("query_related_to_subject", True)
            
            if documents and is_from_textbook:
                context = format_context_for_prompt(documents)
                print(f"Retrieved {len(documents)} documents for query: {user_message[:50]}...")
            else:
                print(f"Topic NOT in textbook (relevance: {relevance_score:.3f}, related: {query_related_to_subject}): {user_message[:50]}...")
        except Exception as e:
            print(f"RAG retrieval error: {e}")
            context = ""
            is_from_textbook = False

    # Get language-specific system prompt
    system_prompt = get_system_prompt(language).format(grade=grade, subject=subject)

    # Add context or not-in-textbook instruction
    if context and is_from_textbook:
        if language == "ur":
            system_prompt += f"\n\nمتعلقہ تعلیمی مواد:\n{context}"
        else:
            system_prompt += f"\n\nRelevant learning material:\n{context}"
    elif not is_from_textbook:
        # Determine if it's a wrong subject question or just out of textbook
        if not query_related_to_subject:
            # Question is about a different subject entirely
            if language == "ur":
                system_prompt += f"""

اہم: یہ سوال {subject} کا نہیں لگتا۔ براہ کرم:
1. طالب علم کو بتائیں کہ "یہ سوال {subject} سے متعلق نہیں لگتا۔"
2. انہیں بتائیں کہ وہ صحیح مضمون منتخب کریں (مثلاً سائنس، کمپیوٹر وغیرہ)
3. ایک بہت مختصر وضاحت دیں (2-3 جملے) صرف مدد کے لیے
4. انہیں {subject} کے سوالات پوچھنے کی حوصلہ افزائی کریں
"""
            else:
                system_prompt += f"""

IMPORTANT: This question does NOT seem to be about {subject}. Please:
1. Tell the student: "This question doesn't seem to be about {subject}."
2. Suggest they select the correct subject (like Science, Computer, etc.)
3. Give a VERY brief explanation (2-3 sentences only) just to help
4. Encourage them to ask {subject} questions instead

Example response: "This looks like a Science question, not {subject}! But briefly, [very short answer]. For more Science help, go back and select the Science subject. Meanwhile, I'm here to help you with {subject}!"
"""
        else:
            # Question seems related to subject but not in textbook
            if language == "ur":
                system_prompt += f"""

اہم: یہ موضوع طالب علم کی جماعت {grade} کی {subject} کتاب میں نہیں ہے۔ براہ کرم:
1. پہلے طالب علم کو بتائیں کہ یہ موضوع ان کی نصابی کتاب میں نہیں ہے
2. پھر ایک مختصر، آسان وضاحت دیں
3. طالب علم کو یاد دلائیں کہ وہ اپنی نصابی کتاب سے متعلق سوالات پوچھیں
"""
            else:
                system_prompt += f"""

IMPORTANT: This topic is NOT covered in the student's Grade {grade} {subject} textbook. Please:
1. First, kindly inform the student that this topic is not in their textbook
2. Then, provide a brief, simple explanation
3. Encourage the student to ask questions from their textbook topics
"""

    messages = [{"role": "system", "content": system_prompt}]

    for msg in chat_history[-10:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        if language == "ur":
            return f"مجھے ابھی سوچنے میں مشکل ہو رہی ہے۔ دوبارہ کوشش کرتے ہیں! (خرابی: {str(e)})"
        return f"I'm having trouble thinking right now. Let's try again! (Error: {str(e)})"


# =========================================================
# "HOW" QUESTION DETECTION AND CONTEXT EXTRACTION
# =========================================================

HOW_QUESTION_PATTERNS = [
    r"^how\??$",
    r"^how is that\??$",
    r"^how does that work\??$",
    r"^how do you do that\??$",
    r"^show me how\??$",
    r"^can you show me\??$",
    r"^explain how\??$",
    r"^how did you get that\??$",
    r"^how does it work\??$",
    r"^why\??$",
    r"^why is that\??$",
]


def is_followup_how_question(user_message: str) -> bool:
    """
    Detect if the user is asking a short follow-up "how" question
    that refers to the previous conversation.
    """
    msg = user_message.strip().lower()
    
    # Check against patterns
    for pattern in HOW_QUESTION_PATTERNS:
        if re.match(pattern, msg):
            return True
    
    # Short "how" questions (less than 5 words starting with how/why/show)
    words = msg.split()
    if len(words) <= 5 and words[0] in ["how", "why", "show", "explain"]:
        return True
    
    return False


def get_context_from_history(chat_history: List[Dict], user_message: str) -> str:
    """
    For follow-up "how" questions, extract the relevant context 
    from the previous conversation to understand what the user is asking about.
    """
    if not chat_history:
        return user_message
    
    # Get the last few exchanges
    relevant_messages = []
    for msg in chat_history[-4:]:  # Last 2 Q&A pairs
        if msg.get("role") == "user":
            relevant_messages.append(f"Student asked: {msg.get('content', '')}")
        elif msg.get("role") == "assistant":
            # Get first 200 chars of assistant response
            content = msg.get("content", "")[:200]
            relevant_messages.append(f"Tutor explained: {content}")
    
    context = "\n".join(relevant_messages)
    return f"Previous conversation:\n{context}\n\nStudent now asks: {user_message}"


def should_auto_generate_image(user_message: str, subject: str, chat_history: List[Dict]) -> bool:
    """
    Determine if we should automatically generate an image for this question.
    Returns True for:
    - Math questions asking "how" 
    - Follow-up "how" questions about previous topics
    - Questions with visual keywords
    """
    msg = user_message.strip().lower()
    subj = subject.lower()
    
    # Always generate for explicit visual requests
    visual_keywords = ["show me", "draw", "picture", "image", "visual", "diagram", "illustrate"]
    if any(kw in msg for kw in visual_keywords):
        return True
    
    # For Math subject
    if subj in ["maths", "math"]:
        # "How" questions in math benefit from visuals
        if msg.startswith("how") or "how do" in msg or "how does" in msg:
            return True
        
        # Follow-up "how" questions
        if is_followup_how_question(msg) and chat_history:
            return True
        
        # Direct math expressions benefit from step-by-step visuals
        if re.search(r"\d+\s*[-+x×*/÷]\s*\d+", msg):
            return True
    
    # For Computer subject - "how does X work" questions
    if subj == "computer":
        if "how" in msg and ("work" in msg or "does" in msg or "process" in msg):
            return True
    
    # For Science - process/how questions
    if subj in ["science", "general science"]:
        if "how" in msg and ("work" in msg or "happen" in msg or "process" in msg):
            return True
    
    return False


def get_image_context(user_message: str, chat_history: List[Dict], subject: str) -> str:
    """
    Get the full context for image generation, especially for follow-up questions.
    """
    # If it's a follow-up "how" question, include the previous topic
    if is_followup_how_question(user_message) and chat_history:
        # Find the last user question that was substantive
        for msg in reversed(chat_history[:-1]):  # Exclude current message
            if msg.get("role") == "user":
                prev_question = msg.get("content", "")
                if len(prev_question) > 10:  # Substantive question
                    return f"{prev_question} - explain how this works visually"
        
    return user_message


# =========================================================
# IMAGE PROMPT BUILDER
# =========================================================
IMAGE_BUILDER_SYSTEM_PROMPT = """You are VisualPromptBuilder for an autism-friendly learning app.

Your job:
Convert the student's question into a SIMPLE, LOW-CLUTTER educational image plan.

The final image must be:
- beginner-friendly
- visually calm
- white background
- simple flat vector style
- clearly colorful, but soft and not harsh
- easy to understand in one look

STRICT RULES:
1. Use ONLY 3 to 6 relevant visual elements. Never more than 6.
2. No decorative/confetti shapes. No random symbols. No extra stickers.
3. No long paragraphs inside the image.
4. Only minimal text:
   - one short title
   - very short labels only
   - for math, short solution lines are allowed
5. If the question is:
   - "what is" / "what are" -> use template "definition"
   - "how" / "how does" / "process" -> use template "workflow"
   - "difference between" / "vs" / "compare" -> use template "comparison"
   - a direct arithmetic equation -> use template "math_steps"
   - a math concept like multiplication, division, fraction, area, perimeter, etc. -> use template "math_concept"
6. For comparison: use two clean columns.
7. For workflow: use 3 to 5 steps with arrows.
8. For math_steps:
   - show the equation
   - show 2 to 3 clean solution steps
   - show the final answer clearly
9. For math_concept:
   - show the concept name simply
   - show one small solved example
   - make the example easier than the student's topic if needed
10. Use 4 to 6 soft educational colors. Never make the image monochrome or black-and-white unless the topic truly requires it.
11. Never ask for a busy infographic.
12. Do not use too many icons. Only the icons that directly explain the question.

Return JSON ONLY in this exact schema:
{
  "template": "definition|workflow|comparison|math_steps|math_concept",
  "title": "SHORT TITLE",
  "icons": ["icon1", "icon2", "icon3"],
  "labels": ["label1", "label2", "label3"],
  "layout": "one short sentence",
  "arrows": true,
  "aspect_ratio": "1:1|4:3|16:9|3:4",
  "prompt": "complete final prompt for the image model"
}

Important:
- The prompt must clearly say where icons go, where arrows go, what labels are allowed, and that only relevant icons should appear.
- The prompt must explicitly say: no clutter, no decorations, no extra icons.
- For math concept questions, the image should explain the idea by solving one simple example.
- The JSON must be valid.
- Output JSON only.
"""


DEFAULT_NEGATIVE_TEXT = (
    "No clutter. No decoration. No confetti. No stickers. No random symbols. "
    "No busy infographic. No paragraphs. No long text. No dark background. "
    "No neon colors. No extra icons. Keep it simple, calm, and easy for a child to understand."
)


MATH_CONCEPT_KEYWORDS = [
    "addition",
    "subtraction",
    "multiplication",
    "division",
    "fraction",
    "fractions",
    "decimal",
    "decimals",
    "percentage",
    "percentages",
    "perimeter",
    "area",
    "volume",
    "ratio",
    "ratios",
    "algebra",
    "angle",
    "angles",
    "mean",
    "median",
    "mode",
    "average",
    "pemdas",
    "bodmas",
    "order of operations",
    "place value",
    "lcm",
    "hcf",
    "gcf",
    "multiple",
    "factor",
    "factors",
    "equation",
]


def _extract_json(text: str) -> Dict[str, Any]:
    """Extract JSON object from model response."""
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise json.JSONDecodeError("Could not extract valid JSON", cleaned, 0)


def _sanitize_list(items: Any, fallback: List[str], max_items: int = 6) -> List[str]:
    """Normalize icon/label lists."""
    if not isinstance(items, list):
        return fallback[:max_items]

    cleaned = []
    for item in items:
        text = str(item).strip()
        if text and text not in cleaned:
            cleaned.append(text)
        if len(cleaned) >= max_items:
            break

    return cleaned if cleaned else fallback[:max_items]


def _looks_like_math_expression(question: str) -> bool:
    """Check if question looks like a direct arithmetic expression."""
    q = question.strip().lower()

    if re.search(r"\d+\s*[-+x×*/÷]\s*\d+", q):
        return True

    simple_patterns = [
        r"what\s+is\s+\d+\s*[-+x×*/÷]\s*\d+",
        r"solve\s+\d+\s*[-+x×*/÷]\s*\d+",
    ]
    return any(re.search(pattern, q) for pattern in simple_patterns)


def _is_math_concept_question(question: str, subject: str) -> bool:
    """Check if question is asking about a math concept/theory."""
    q = question.lower().strip()
    subj = subject.lower().strip()

    if subj != "maths" and subj != "math":
        return False

    if _looks_like_math_expression(q):
        return False

    trigger_phrases = [
        "what is",
        "what are",
        "tell me about",
        "explain",
        "define",
        "difference between",
        "compare",
        "how do",
        "how does",
    ]

    has_trigger = any(phrase in q for phrase in trigger_phrases)
    has_math_keyword = any(keyword in q for keyword in MATH_CONCEPT_KEYWORDS)

    return has_trigger and has_math_keyword


def _extract_math_concept_name(question: str) -> str:
    """Best-effort extraction of the main math concept from the question."""
    q = question.lower()

    for keyword in MATH_CONCEPT_KEYWORDS:
        if keyword in q:
            return keyword.title()

    return "Math Concept"


def _math_concept_example_instruction(concept_name: str) -> str:
    """Return example instruction for a math concept."""
    concept = concept_name.lower()

    if "multiplication" in concept:
        return (
            "Show one simple solved example such as 3 × 2 = 6. "
            "Also show that multiplication means repeated addition: 2 + 2 + 2 = 6."
        )

    if "division" in concept:
        return (
            "Show one simple solved example such as 6 ÷ 2 = 3. "
            "Also show division as equal sharing into groups."
        )

    if "addition" in concept:
        return "Show one simple solved example such as 2 + 3 = 5 using a clear step."

    if "subtraction" in concept:
        return "Show one simple solved example such as 7 - 2 = 5 using a clear step."

    if "fraction" in concept:
        return (
            "Show one simple example such as 1/2 of a shape or 1/4 of a pizza. "
            "Make the parts clear and large."
        )

    if "decimal" in concept:
        return "Show one simple example such as 0.5 = one half."

    if "percentage" in concept:
        return "Show one simple example such as 50% = half."

    if "perimeter" in concept:
        return (
            "Show a simple rectangle with side lengths and add all sides to find perimeter."
        )

    if "area" in concept:
        return (
            "Show a simple rectangle with rows and columns or length × width."
        )

    if "angle" in concept:
        return "Show one simple angle example and label it clearly as an angle."

    if "average" in concept or "mean" in concept:
        return "Show a tiny example of adding a few numbers and dividing by how many numbers there are."

    if "pemdas" in concept or "bodmas" in concept or "order of operations" in concept:
        return "Show one simple equation and solve it in the correct order step by step."

    return "Show one simple solved example that explains the concept in an easy way."


def _heuristic_visual_plan(question: str, grade: int, subject: str) -> Dict[str, Any]:
    """Fallback visual plan when GPT prompt building fails."""
    q = question.strip()
    q_lower = q.lower()

    if _looks_like_math_expression(q):
        title = "Solve Step by Step"
        icons = ["equation", "step line", "answer box"]
        labels = ["equation", "steps", "answer"]
        layout = "Top: equation. Middle: 2 to 3 simple steps. Bottom: final answer in a clear answer box."
        aspect_ratio = "3:4"
        prompt = (
            f"Create a simple autism-friendly math learning image for: {q}. "
            "White background, flat vector style, 4 to 6 soft educational colors, lots of empty space. "
            "Do not make it black-and-white. "
            "Top section: show the full equation clearly. "
            "Middle section: show 2 to 3 simple solution steps in large readable math text. "
            "Bottom section: show the final answer clearly in a highlighted answer box. "
            "Use clean written calculation steps. Supporting blocks are optional, but the written solution is more important. "
            "No decoration, no extra icons, no clutter, no long paragraphs. "
            f"{DEFAULT_NEGATIVE_TEXT}"
        )
        return {
            "template": "math_steps",
            "title": title,
            "icons": icons,
            "labels": labels,
            "layout": layout,
            "arrows": True,
            "aspect_ratio": aspect_ratio,
            "prompt": prompt,
        }

    if _is_math_concept_question(q, subject):
        concept_name = _extract_math_concept_name(q)
        title = concept_name
        icons = ["concept box", "example box", "result box"]
        labels = ["concept", "example", "result"]
        layout = "Top: concept title. Middle: one simple solved example. Bottom: short takeaway or result."
        aspect_ratio = "3:4"
        prompt = (
            f"Create a simple autism-friendly maths concept image about: {concept_name}. "
            f"The original student question is: {q}. "
            "White background, flat vector style, 4 to 6 soft educational colors, lots of empty space. "
            "Do not make it black-and-white. "
            "Top section: show the concept name clearly. "
            "Middle section: show one small solved example in large readable math text. "
            "Bottom section: show the final result or key idea clearly. "
            f"{_math_concept_example_instruction(concept_name)} "
            "Make the image basic, clear, and child-friendly. "
            "No decoration, no extra icons, no clutter, no busy infographic. "
            f"{DEFAULT_NEGATIVE_TEXT}"
        )
        return {
            "template": "math_concept",
            "title": title,
            "icons": icons,
            "labels": labels,
            "layout": layout,
            "arrows": True,
            "aspect_ratio": aspect_ratio,
            "prompt": prompt,
        }

    if "difference between" in q_lower or " vs " in q_lower or q_lower.startswith("compare"):
        title = "Compare"
        icons = ["left concept", "right concept", "column divider"]
        labels = ["left", "right"]
        layout = "Two clean columns with only relevant icons on each side."
        aspect_ratio = "16:9"
        prompt = (
            f"Create a simple autism-friendly comparison image for: {q}. "
            "White background, flat vector style, 4 to 6 soft educational colors, lots of spacing. "
            "Title at the top. Two clean columns. "
            "Use only 2 to 3 relevant icons on the left and 2 to 3 relevant icons on the right. "
            "Use very short labels only. No paragraphs. "
            "No decoration, no extra objects, no clutter. "
            f"{DEFAULT_NEGATIVE_TEXT}"
        )
        return {
            "template": "comparison",
            "title": title,
            "icons": icons,
            "labels": labels,
            "layout": layout,
            "arrows": False,
            "aspect_ratio": aspect_ratio,
            "prompt": prompt,
        }

    if q_lower.startswith("how") or "how does" in q_lower or "process" in q_lower or "work" in q_lower:
        title = q[:36].strip().rstrip("?")
        icons = ["step 1", "step 2", "step 3", "step 4"]
        labels = ["step 1", "step 2", "step 3", "step 4"]
        layout = "Short title at top. Below it, 3 to 5 simple steps connected by arrows."
        aspect_ratio = "16:9"
        prompt = (
            f"Create a simple autism-friendly workflow image for: {q}. "
            "White background, flat vector style, 4 to 6 soft educational colors, high contrast, lots of empty space. "
            "Use only the most relevant visual elements needed to explain the process. "
            "Show 3 to 5 large steps with clear arrows in order. "
            "Use tiny labels only. No paragraphs, no decoration, no clutter, no extra icons. "
            f"{DEFAULT_NEGATIVE_TEXT}"
        )
        return {
            "template": "workflow",
            "title": title,
            "icons": icons,
            "labels": labels,
            "layout": layout,
            "arrows": True,
            "aspect_ratio": aspect_ratio,
            "prompt": prompt,
        }

    title = q[:36].strip().rstrip("?") or subject.title()
    icons = ["main concept", "example 1", "example 2", "example 3"]
    labels = ["main", "example", "example", "example"]
    layout = "Title at top, then 3 to 5 large relevant icons in one simple row or grid."
    aspect_ratio = "4:3"
    prompt = (
        f"Create a simple autism-friendly educational image for: {q}. "
        f"Subject: {subject}. Grade: {grade}. "
        "White background, flat vector style, calm colorful icons, lots of spacing. "
        "Use only relevant icons that directly explain the topic. "
        "Use very short labels only. No decoration, no confetti, no extra symbols, no clutter, no long text. "
        f"{DEFAULT_NEGATIVE_TEXT}"
    )
    return {
        "template": "definition",
        "title": title,
        "icons": icons,
        "labels": labels,
        "layout": layout,
        "arrows": False,
        "aspect_ratio": aspect_ratio,
        "prompt": prompt,
    }


def _build_final_image_prompt(plan: Dict[str, Any], question: str, grade: int, subject: str) -> str:
    """Build the final strict prompt for the image model."""
    title = plan["title"]
    icons = plan["icons"]
    labels = plan["labels"]
    icon_count = len(icons)

    icon_text = ", ".join(icons[:icon_count])
    label_text = ", ".join(labels[:icon_count])

    base = [
        f"Create a simple autism-friendly educational image for Grade {grade} {subject} students about: {question}.",
        "Style: flat vector, white background, 4 to 6 soft educational colors, high contrast, lots of empty space.",
        "Do not make it monochrome or black-and-white.",
        f"Use EXACTLY {icon_count} relevant visual elements only: {icon_text}.",
        f"Allowed labels only: {label_text}.",
        f"Title: {title}.",
        f"Layout: {plan['layout']}",
        "No decoration, no confetti, no extra icons, no random symbols, no busy infographic style.",
        "Keep everything clean, basic, calm, and easy for a child to understand.",
    ]

    template = plan["template"]

    if template == "comparison":
        base.append(
            "Use two clean columns. Left side explains the first concept. Right side explains the second concept."
        )

    elif template == "workflow":
        base.append(
            "Connect the steps with clear arrows in the correct order."
        )

    elif template == "math_steps":
        base.append(
            "Show the full equation clearly at the top, then show 2 to 3 simple solution steps in order, then show the final answer clearly at the bottom. "
            "Use large readable math text and symbols. "
            "A few supporting blocks or shapes are allowed, but the written solution steps are more important."
        )

    elif template == "math_concept":
        base.append(
            "Explain the maths idea using one simple solved example. "
            "Top: concept title. Middle: easy example solved clearly. Bottom: short key idea or result. "
            "Use readable math text and symbols. The solved example is more important than decorative visuals."
        )

    else:
        base.append(
            "Arrange the icons in one simple row or grid so the student can understand the topic at a glance."
        )

    base.append(DEFAULT_NEGATIVE_TEXT)

    return " ".join(base)


def _normalize_visual_plan(plan: Dict[str, Any], question: str, grade: int, subject: str) -> Dict[str, Any]:
    """Validate and normalize a visual plan."""
    fallback = _heuristic_visual_plan(question, grade, subject)

    template = str(plan.get("template", fallback["template"])).strip().lower()
    if template not in {"definition", "workflow", "comparison", "math_steps", "math_concept"}:
        template = fallback["template"]

    title = str(plan.get("title", fallback["title"])).strip() or fallback["title"]

    aspect_ratio = str(plan.get("aspect_ratio", fallback["aspect_ratio"])).strip()
    if aspect_ratio not in {"1:1", "4:3", "16:9", "3:4"}:
        aspect_ratio = fallback["aspect_ratio"]

    icons = _sanitize_list(plan.get("icons"), fallback["icons"])
    labels = _sanitize_list(plan.get("labels"), fallback["labels"], max_items=len(icons))
    if len(labels) < len(icons):
        labels += [icon[:18] for icon in icons[len(labels):]]

    layout = str(plan.get("layout", fallback["layout"])).strip() or fallback["layout"]
    arrows = bool(plan.get("arrows", fallback["arrows"]))

    prompt = str(plan.get("prompt", "")).strip()
    if not prompt:
        prompt = _build_final_image_prompt(
            {
                "template": template,
                "title": title,
                "icons": icons,
                "labels": labels,
                "layout": layout,
                "arrows": arrows,
                "aspect_ratio": aspect_ratio,
            },
            question=question,
            grade=grade,
            subject=subject,
        )

    return {
        "template": template,
        "title": title,
        "icons": icons,
        "labels": labels,
        "layout": layout,
        "arrows": arrows,
        "aspect_ratio": aspect_ratio,
        "prompt": prompt,
    }


def enhance_image_prompt(question: str, grade: int, subject: str) -> Dict[str, Any]:
    """Use GPT-4o-mini to create a strict visual plan."""
    client = get_openai_client()
    if not client:
        fallback = _heuristic_visual_plan(question, grade, subject)
        return _normalize_visual_plan(fallback, question, grade, subject)

    user_prompt = (
        f"Question: {question}\n"
        f"Grade: {grade}\n"
        f"Subject: {subject}\n\n"
        "Build the image plan now."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": IMAGE_BUILDER_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=900,
            response_format={"type": "json_object"},
        )

        response_text = response.choices[0].message.content.strip()
        prompt_data = _extract_json(response_text)
        plan = _normalize_visual_plan(prompt_data, question, grade, subject)

        print(f"Visual prompt template: {plan['template']}")
        print(f"Visual prompt icons: {plan['icons']}")
        print(f"Visual prompt title: {plan['title']}")
        return plan

    except Exception as e:
        print(f"Error enhancing prompt: {e}")
        fallback = _heuristic_visual_plan(question, grade, subject)
        return _normalize_visual_plan(fallback, question, grade, subject)


# =========================================================
# IMAGE GENERATION
# =========================================================
def _aspect_ratio_to_size(aspect_ratio: str) -> str:
    """Map aspect ratio to supported image sizes."""
    if aspect_ratio == "16:9":
        return "1536x1024"
    if aspect_ratio == "3:4":
        return "1024x1536"
    if aspect_ratio == "4:3":
        return "1536x1024"
    return "1024x1024"


def _save_b64_image_to_temp(b64_string: str) -> Optional[str]:
    """Save base64 image to a temporary local file and return file path."""
    try:
        image_bytes = base64.b64decode(b64_string)
        temp_dir = os.path.join(os.getcwd(), "temp_generated_images")
        os.makedirs(temp_dir, exist_ok=True)

        file_name = f"generated_{uuid.uuid4().hex}.png"
        file_path = os.path.join(temp_dir, file_name)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        return file_path
    except Exception as e:
        print(f"Error saving base64 image: {e}")
        return None


def generate_image(
    question: str, 
    grade: int, 
    subject: str,
    chat_history: List[Dict] = None
) -> Optional[str]:
    """Generate an educational image using OpenAI image generation."""
    client = get_openai_client()
    if not client:
        print("OpenAI client not found")
        return None

    # Get full context for image generation (handles follow-up questions)
    image_question = get_image_context(question, chat_history or [], subject)
    
    print(f"Building image prompt for: {image_question[:100]}...")
    prompt_data = enhance_image_prompt(image_question, grade, subject)

    image_prompt = prompt_data.get("prompt", "")
    aspect_ratio = prompt_data.get("aspect_ratio", "4:3")
    template = prompt_data.get("template", "definition")
    size = _aspect_ratio_to_size(aspect_ratio)

    print(f"Image template: {template}")
    print(f"Aspect ratio: {aspect_ratio}")
    print(f"OpenAI image size: {size}")
    print(f"Generated image prompt: {image_prompt[:300]}...")

    # Main attempt: GPT Image 1.5
    try:
        response = client.images.generate(
            model="gpt-image-1.5",
            prompt=image_prompt,
            size=size,
            quality="high",
            n=1,
        )

        if response.data and len(response.data) > 0:
            first_item = response.data[0]

            if getattr(first_item, "b64_json", None):
                print("GPT Image 1.5 generated successfully.")
                saved_path = _save_b64_image_to_temp(first_item.b64_json)
                if saved_path:
                    return saved_path

            if getattr(first_item, "url", None):
                print("GPT Image 1.5 generated successfully with URL output.")
                return first_item.url

        print("GPT Image 1.5 returned no usable image data.")

    except Exception as e:
        print(f"GPT Image 1.5 generation error: {e}")

    # Fallback 1: GPT Image 1
    try:
        print("Falling back to gpt-image-1...")
        response = client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size=size,
            quality="high",
            n=1,
        )

        if response.data and len(response.data) > 0:
            first_item = response.data[0]

            if getattr(first_item, "b64_json", None):
                print("GPT Image 1 generated successfully.")
                saved_path = _save_b64_image_to_temp(first_item.b64_json)
                if saved_path:
                    return saved_path

            if getattr(first_item, "url", None):
                print("GPT Image 1 generated successfully with URL output.")
                return first_item.url

    except Exception as e:
        print(f"GPT Image 1 fallback error: {e}")

    # Fallback 2: DALL-E 3
    try:
        print("Falling back to DALL-E 3...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        if response.data and len(response.data) > 0:
            first_item = response.data[0]

            if getattr(first_item, "url", None):
                print("DALL-E 3 generated successfully.")
                return first_item.url

            if getattr(first_item, "b64_json", None):
                saved_path = _save_b64_image_to_temp(first_item.b64_json)
                if saved_path:
                    return saved_path

    except Exception as e:
        print(f"DALL-E 3 fallback error: {e}")

    print("All image generation methods failed.")
    return None


# =========================================================
# TEXT-TO-SPEECH (TTS) using OpenAI
# =========================================================
def generate_speech(text: str, language: str = "en") -> Optional[bytes]:
    """
    Generate speech audio from text using OpenAI TTS model.
    
    Args:
        text: The text to convert to speech
        language: Language code ("en" for English, "ur" for Urdu)
    
    Returns:
        Audio bytes (MP3 format) or None if failed
    """
    client = get_openai_client()
    if not client:
        print("OpenAI client not available for TTS")
        return None
    
    try:
        # Use alloy voice for English, nova for Urdu (both work well)
        # Available voices: alloy, echo, fable, onyx, nova, shimmer
        voice = "nova" if language == "ur" else "alloy"
        
        # Truncate text if too long (TTS has limits)
        max_chars = 4000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        response = client.audio.speech.create(
            model="tts-1",  # or "tts-1-hd" for higher quality
            voice=voice,
            input=text,
            response_format="mp3"
        )
        
        # Get audio bytes
        audio_bytes = response.content
        print(f"TTS generated: {len(audio_bytes)} bytes")
        return audio_bytes
        
    except Exception as e:
        print(f"TTS generation error: {e}")
        return None


def text_to_speech_base64(text: str, language: str = "en") -> Optional[str]:
    """
    Generate speech and return as base64-encoded string for HTML audio playback.
    
    Args:
        text: The text to convert to speech
        language: Language code ("en" for English, "ur" for Urdu)
    
    Returns:
        Base64-encoded audio string or None if failed
    """
    audio_bytes = generate_speech(text, language)
    if audio_bytes:
        return base64.b64encode(audio_bytes).decode("utf-8")
    return None


# =========================================================
# COMBINED RESPONSE WITH AUTO-IMAGE
# =========================================================
def generate_response_with_auto_image(
    user_message: str,
    grade: int,
    subject: str,
    chat_history: List[Dict],
    use_rag: bool = True,
    language: str = None,
) -> Dict[str, Any]:
    """
    Generate a text response and automatically generate an image
    if the question is a "how" question or would benefit from visuals.
    
    Returns:
        Dict with keys:
        - text_response: The text answer
        - image_url: URL/path to generated image (or None)
        - auto_image_generated: Whether image was auto-generated
    """
    # Generate text response first
    text_response = generate_response(
        user_message, grade, subject, chat_history, use_rag, language
    )
    
    result = {
        "text_response": text_response,
        "image_url": None,
        "auto_image_generated": False
    }
    
    # Check if we should auto-generate an image
    if should_auto_generate_image(user_message, subject, chat_history):
        print(f"Auto-generating image for: {user_message[:50]}...")
        try:
            image_url = generate_image(user_message, grade, subject, chat_history)
            if image_url:
                result["image_url"] = image_url
                result["auto_image_generated"] = True
                print("Auto-image generated successfully!")
        except Exception as e:
            print(f"Auto-image generation failed: {e}")
    
    return result


# =========================================================
# QUIZ GENERATION
# =========================================================
def generate_quiz_question(
    grade: int,
    subject: str,
    topic: Optional[str] = None
) -> Dict:
    """Generate a quiz question for practice."""

    client = get_openai_client()
    if not client:
        return None

    prompt = f"""Generate a simple multiple-choice quiz question for a Grade {grade} student studying {subject}.
{"Topic: " + topic if topic else ""}

Format your response as:
Question: [Your question here]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct: [A/B/C/D]
Explanation: [Brief, encouraging explanation]
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly quiz master for students with autism. Keep questions simple and clear.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=500,
        )

        content = response.choices[0].message.content
        return {"raw": content}

    except Exception:
        return None