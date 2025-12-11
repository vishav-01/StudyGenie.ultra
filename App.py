import streamlit as st
import requests
import json
import random

# =====================================================
# PAGE SETTINGS
# =====================================================
st.set_page_config(page_title="StudyGenie — K•Apple Fusion", layout="wide")

# =====================================================
# GLOBAL BACKGROUND (DORAEMON BLUE)
# =====================================================
BG = "#44a8ff"  # Doraemon Sky Blue

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {BG} !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {BG}33 !important;
        }}
        html, body, [class*="css"] {{
            font-family: 'Poppins', sans-serif !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.title("💙 StudyGenie — Your AI Study Bestie 😚")

    tool = st.radio(
        "Choose a Tool ✨",
        [
            "AI Doubt Solver",
            "Notes Generator",
            "Summary Maker",
            "Timetable Builder",
            "Motivation Booster",
            "Flashcards",
            "Brain-Dump Cleaner",
            "Answer Checker",
            "AI Planner",
            "Mindset Reset",
            "Study Routine Designer",
            "Exam Strategy Maker",
            "Personal Study Coach",
            "Mini IQ Test Game 🧠"
        ]
    )

# =====================================================
# AI FUNCTION
# =====================================================
def ask_ai(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500,
        "temperature": 0.65
    }

    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
                          headers=headers, data=json.dumps(payload), timeout=20)
        data = r.json()

        if "choices" not in data:
            return "⚠️ Bestie, your AI fainted 😭."

        reply = data["choices"][0]["message"]["content"]
        st.session_state.chat_history.append({"you": prompt, "ai": reply})

        st.session_state["clear_input"] = True
        return reply

    except Exception as e:
        return "❌ Error: " + str(e)

# Chat initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# =====================================================
# NON-IQ TEST TOOLS
# =====================================================
if tool != "Mini IQ Test Game 🧠":
    st.markdown(f"<h1 style='text-align:center;'>✨ {tool} ✨</h1>", unsafe_allow_html=True)

    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['you']}")
        st.markdown(f"**Genie:** {chat['ai']}")

    prompt = st.text_area("Type your message 💬")

    if st.button("Send"):
        if prompt.strip() != "":
            response = ask_ai(f"{tool}: {prompt}")
            st.markdown(f"**Genie:** {response}")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()


# =====================================================
# 🧠 MINI IQ TEST (MCQ VERSION)
# =====================================================
if tool == "Mini IQ Test Game 🧠":

    st.markdown("<h1 style='text-align:center;'>🧠 Mini IQ Test — Doraemon Edition</h1>", unsafe_allow_html=True)

    # MCQ bank
    iq_mcq = [
        {
            "q": "What number comes next? 2, 6, 12, 20, 30, __",
            "options": ["A) 36", "B) 40", "C) 42", "D) 48"],
            "answer": "C"
        },
        {
            "q": "Which one is different?",
            "options": ["A) Dog", "B) Lion", "C) Wolf", "D) Cat"],
            "answer": "D"
        },
        {
            "q": "If ALL roses are flowers, which is true?",
            "options": [
                "A) Some roses aren't flowers",
                "B) All roses are flowers",
                "C) No roses are flowers",
                "D) Flowers aren’t roses"
            ],
            "answer": "B"
        },
        {
            "q": "Missing letter? A, D, G, J, M, __",
            "options": ["A) O", "B) P", "C) R", "D) S"],
            "answer": "B"
        },
        {
            "q": "Find odd number:",
            "options": ["A) 27", "B) 64", "C) 125", "D) 144"],
            "answer": "D"
        },
        {
            "q": "Sun