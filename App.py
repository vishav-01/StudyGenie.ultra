import streamlit as st
import requests
import json
import random

# =====================================================
# PAGE SETUP + SOFT GRADIENT + CUTE GEN Z FONT
# =====================================================
st.set_page_config(page_title="StudyGenie Ultra 💖", layout="wide")

custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(170deg, #dff3ff, #f5dfff, #ffe6f2);
    background-size: cover !important;
    background-attachment: fixed !important;
    font-family: 'Poppins', sans-serif !important;
    color: #333;
}

.section {
    background: rgba(255, 255, 255, 0.45);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.4);
    margin-top: 20px;
    backdrop-filter: blur(10px);
}

h1, h2, h3 {
    font-weight: 700;
    font-style: italic;
}

.genie-bubble {
    background: #ffffffa8;
    padding: 16px;
    margin: 12px 0;
    border-radius: 14px;
    border-left: 4px solid #a88bff;
    animation: fadeIn 0.4s ease-in-out;
}

.question-box {
    padding: 20px;
    background: #ffffff;
    border-radius: 18px;
    font-size: 19px;
    border: 2px solid #ffffff55;
}

@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.98); }
    to { opacity: 1; transform: scale(1); }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;color:#4a3b8f;'>✨ StudyGenie Ultra – Your AI Study Bestie 💕</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:#5f569b;font-size:18px;'>Always here for your doubts, dreams, and glow-up ✨</p>",
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR — MAIN MENU + THEME (for future theme changes)
# =====================================================
tool = st.sidebar.radio(
    "✨ Choose your tool",
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
# CHAT HISTORY
# =====================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =====================================================
# BACKEND AI CALL
# =====================================================
def ask_ai(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"
    }
    payload = {
        "model": "gpt-4.1-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000,
        "temperature": 0.65
    }
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
                          headers=headers, data=json.dumps(payload), timeout=20)
        data = r.json()
        if "choices" not in data:
            return "⚠️ Bestie the AI fainted 😭"
        reply = data["choices"][0]["message"]["content"]
        st.session_state.chat_history.append({"you": prompt, "ai": reply})
        return reply
    except Exception as e:
        return "❌ Error: " + str(e)

# =====================================================
# NORMAL TOOLS (except IQ game)
# =====================================================
if tool != "Mini IQ Test Game 🧠":
    st.markdown(f"<h2 style='text-align:center;'>✨ {tool} ✨</h2>", unsafe_allow_html=True)

    for chat in st.session_state.chat_history:
        st.markdown(f"<div class='genie-bubble'><b>You:</b> {chat['you']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='genie-bubble'><b>Genie:</b> {chat['ai']}</div>", unsafe_allow_html=True)

    prompt = st.text_area("Type your message 💬")
    if st.button("Send"):
        if prompt.strip() != "":
            response = ask_ai(f"{tool}: {prompt}")
            st.markdown(f"<div class='genie-bubble'><b>Genie:</b> {response}</div>", unsafe_allow_html=True)

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# =====================================================
# MINI IQ TEST GAME 🧠
# =====================================================
if tool == "Mini IQ Test Game 🧠":
    st.markdown("<h2 style='text-align:center;'>🧠 Mini IQ Test (MCQ Edition)</h2>", unsafe_allow_html=True)

    iq_mcq = [
        ("What number comes next? 2, 6, 12, 20, 30, __",
         ["36", "40", "42", "44"], "42"),
        ("Which one is different?", ["Cat", "Dog", "Lion", "Wolf"], "Cat"),
        ("Missing letter? A, D, G, J, M, __", ["O", "P", "N", "Q"], "P"),
        ("Odd number: 27,64,125,144,216", ["27", "144", "125", "216"], "144"),
        ("What's bigger: 3/7 or 4/9?", ["3/7", "4/9"], "4/9"),
        ("Solve: (3×4)² ÷ 6", ["12", "24", "36", "48"], "24"),
        ("Sun : Day :: Moon : __", ["Light", "Sky", "Night", "Dark"], "Night"),
        ("Which weighs more?", ["1 kg iron", "1 kg cotton", "Both same"], "Both same"),
        ("45% of 200 =", ["70", "80", "90", "100"], "90")
    ]

    if "current_q" not in st.session_state:
        st.session_state.current_q = random.choice(iq_mcq)

    question, options, answer = st.session_state.current_q
    st.markdown(f"<div class='question-box'>{question}</div>", unsafe_allow_html=True)
    user_choice = st.radio("Choose option:", options)

    if st.button("Submit Answer"):
        if user_choice == answer:
            st.success("🔥 Correct bestie!! Genius brain unlocked 💙💖")
        else:
            st.error(f"😭 Wrong babe… the correct answer was **{answer}** 💗")

    if st.button("Next Question"):
        st.session_state.current_q = random.choice(iq_mcq)
        st.rerun()