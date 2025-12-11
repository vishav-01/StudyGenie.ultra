import streamlit as st
import requests
import json
import random

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="StudyGenie — K•Apple UI", layout="wide")

# =====================================================
# THEME SYSTEM (Default: Doraemon Blue Gradient)
# =====================================================
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

# =====================================================
# APPLY CSS + GRADIENT + POPPINS FONT
# =====================================================
st.markdown(
    f"""
    <style>
        /* Background Gradient */
        .stApp {{
            background: linear-gradient(135deg, {grad_start}, {grad_end}) !important;
            color: #000000;
        }}

        /* Frosted Sidebar */
        section[data-testid="stSidebar"] {{
            background: rgba(255,255,255,0.35) !important;
            backdrop-filter: blur(6px);
        }}

        /* Global Font */
        html, body, [class*="css"] {{
            font-family: 'Poppins', sans-serif !important;
        }}

        /* Question Box */
        .question-box {{
            padding: 22px;
            background: #ffffff;
            border-radius: 16px;
            border: 2px solid #ffffff55;
            font-size: 19px;
            margin-bottom: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR — MAIN MENU
# =====================================================
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

# =====================================================
# SESSION STATE SETUP
# =====================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# =====================================================
# OPENAI BACKEND CALL
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
        st.session_state["clear_input"] = True
        return reply

    except Exception as e:
        return "❌ Error: " + str(e)

# =====================================================
# NORMAL TOOLS UI
# =====================================================
if tool != "Mini IQ Test Game 🧠":

    st.markdown(
        f"<h1 style='text-align:center;'>✨ {tool} ✨</h1>",
        unsafe_allow_html=True
    )

    # Show chat history
    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['you']}")
        st.markdown(f"**Genie:** {chat['ai']}")

    # Input field
    default_text = "" if st.session_state.clear_input else st.session_state.get("last_prompt", "")
    prompt = st.text_area("Ask me anything 💬", value=default_text)
    st.session_state.last_prompt = prompt

    # SEND BUTTON
    if st.button("Send"):
        if prompt.strip():
            st.session_state.clear_input = True
            response = ask_ai(f"{tool}: {prompt}")
            st.markdown(f"**Genie:** {response}")
            st.session_state.last_prompt = ""

    # CLEAR CHAT
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.last_prompt = ""
        st.rerun()

# =====================================================
# MINI IQ TEST GAME 🧠
# =====================================================
else:
    st.markdown("<h1 style='text-align:center;'>🧠 Mini IQ Test (MCQ Edition)</h1>", unsafe_allow_html=True)

    # IQ QUESTIONS LIST
    iq_mcq = [
        ("What number comes next? 2, 6, 12, 20, 30, __", ["36", "40", "42", "44"], "42"),
        ("Which one is different?", ["Cat", "Dog", "Lion", "Wolf"], "Cat"),
        ("Conclusion? If ALL roses are flowers and SOME flowers fade quickly…",
         ["All roses fade quickly", "Some roses may fade quickly", "No roses fade quickly"],
         "Some roses may fade quickly"),
        ("Missing letter? A, D, G, J, M, __", ["O", "P", "N", "Q"], "P"),
        ("Odd number: 27,64,125,144,216", ["27", "144", "125", "216"], "144"),
        ("What's bigger: 3/7 or 4/9?", ["3/7", "4/9"], "4/9"),
        ("Solve: (3×4)² ÷ 6", ["12", "24", "36", "48"], "24"),
        ("Sun : Day :: Moon : __", ["Light", "Sky", "Night", "Dark"], "Night"),
        ("Which weighs more?", ["1 kg iron", "1 kg cotton", "Both same"], "Both same"),
        ("45% of 200 =", ["70", "80", "90", "100"], "90")
    ]

    # Load or generate question
    if "current_q" not in st.session_state:
        st.session_state.current_q = random.choice(iq_mcq)

    question, options, answer = st.session_state.current_q

    st.markdown(f"<div class='question-box'>{question}</div>", unsafe_allow_html=True)

    user_choice = st.radio("Choose option:", options)

    # Submit Answer
    if st.button("Submit Answer"):
        if user_choice == answer:
            st.success("🔥 Correct bestie!! Genius brain unlocked 💙💖")
        else:
            st.error(f"😭 Wrong babe… the correct answer was **{answer}** 💗")

    # Next Question
    if st.button("Next Question"):
        st.session_state.current_q = random.choice(iq_mcq)
        st.rerun()