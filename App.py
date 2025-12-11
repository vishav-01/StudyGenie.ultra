import streamlit as st
import requests
import json
import random

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(page_title="StudyGenie — Ultra K•Apple Edition", layout="wide")

# ============================================
# THEMES
# ============================================
theme = st.sidebar.selectbox(
    "🌈 Choose Theme",
    ["Doraemon", "Sky Blue", "Pink Pastel", "Lavender"],
    index=0
)

theme_colors = {
    "Doraemon": ("#5EC2FF", "#0089E0"),
    "Sky Blue": ("#d2eaff", "#8cc8ff"),
    "Pink Pastel": ("#ffd6e8", "#ffa4c8"),
    "Lavender": ("#e7d9ff", "#c7a4ff")
}

grad_start, grad_end = theme_colors[theme]

# ============================================
# CSS APPLY
# ============================================
st.markdown(
    f"""
    <style>
        .stApp {{
            background: linear-gradient(135deg, {grad_start}, {grad_end}) !important;
        }}
        section[data-testid="stSidebar"] {{
            background: rgba(255,255,255,0.3) !important;
            backdrop-filter: blur(7px);
        }}
        html, body {{
            font-family: 'Poppins', sans-serif !important;
        }}
        .genie-box {{
            background: rgba(255,255,255,0.6);
            padding: 20px;
            border-radius: 16px;
            border: 1.5px solid rgba(255,255,255,0.4);
            margin-bottom: 18px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================
# SIDEBAR MENU
# ============================================
with st.sidebar:
    st.title("✨ StudyGenie — K•Apple Edition")

    tool = st.radio(
        "Choose a Tool 💙",
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

# ============================================
# SESSION STATE
# ============================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# ============================================
# OPENAI CALLER
# ============================================
def ask_ai(prompt):
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.7
    }

    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
                          headers=headers,
                          data=json.dumps(payload),
                          timeout=25)
        data = r.json()

        if "choices" not in data:
            return "⚠️ Genie fainted for a sec 😭 Try again."

        reply = data["choices"][0]["message"]["content"]
        st.session_state.chat_history.append({"you": prompt, "ai": reply})
        st.session_state.clear_input = True
        return reply

    except Exception as e:
        return "❌ Error: " + str(e)

# ============================================
# NORMAL AI TOOLS
# ============================================
if tool != "Mini IQ Test Game 🧠":

    st.markdown(f"<h1 style='text-align:center;'>✨ {tool} ✨</h1>", unsafe_allow_html=True)

    # show chat history
    for chat in st.session_state.chat_history:
        st.markdown(f"<div class='genie-box'><b>You:</b> {chat['you']}<br><b>Genie:</b> {chat['ai']}</div>",
                    unsafe_allow_html=True)

    # user input
    prompt = st.text_area("Tell me, bestie 💬", value="" if st.session_state.clear_input else st.session_state.get("last_prompt", ""))
    st.session_state.last_prompt = prompt

    # send
    if st.button("Send 💙"):
        if prompt.strip():
            response = ask_ai(f"{tool}: {prompt}")
            st.markdown(f"<div class='genie-box'><b>Genie:</b> {response}</div>", unsafe_allow_html=True)
            st.session_state.last_prompt = ""

    # clear history
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.last_prompt = ""
        st.rerun()

# ============================================
# MINI IQ GAME
# ============================================
else:
    st.markdown("<h1 style='text-align:center;'>🧠 Mini IQ Test Game</h1>", unsafe_allow_html=True)

    questions = [
        ("What number comes next? 2, 6, 12, 20, 30, __", ["36", "40", "42", "44"], "42"),
        ("Which one is different?", ["Cat", "Dog", "Lion", "Wolf"], "Cat"),
        ("If ALL roses are flowers & SOME flowers fade quickly, what follows?",
         ["All roses fade quickly", "Some roses fade quickly", "No conclusion", "All flowers fade suddenly"],
         "No conclusion")
    ]

    for i, (q, options, ans) in enumerate(questions):
        st.write(f"### {i+1}. {q}")
        choice = st.radio("", options, key=f"q{i}")
        if st.button(f"Check Q{i+1}"):
            if choice == ans:
                st.success("Correct bestie 😭💙🧠")
            else:
                st.error(f"Wrong 😭 Correct answer: {ans}")