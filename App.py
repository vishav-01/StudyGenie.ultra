import streamlit as st
import requests
import json
import random

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="StudyGenie — AI Study Bestie", layout="wide")

# =====================================================
# THEME SYSTEM (Default: Doraemon Blue Gradient)
# =====================================================
theme = st.sidebar.selectbox(
    "🌈 Choose Theme",
    ["Doraemon", "Sky Blue", "Pink Pastel", "Lavender"],
    index=0  # Default
)

theme_colors = {
    "Doraemon": ("#5EC2FF", "#0089E0"),  # Gradient
    "Sky Blue": ("#d2eaff", "#8cc8ff"),
    "Pink Pastel": ("#ffd6e8", "#ffa4c8"),
    "Lavender": ("#e7d9ff", "#c7a4ff")
}

grad_start, grad_end = theme_colors[theme]

# =====================================================
# APPLY CSS GRADIENT
# =====================================================
st.markdown(
    f"""
    <style>
        .stApp {{
            background: linear-gradient(135deg, {grad_start}, {grad_end}) !important;
            color: #000000;
        }}
        section[data-testid="stSidebar"] {{
            background: rgba(255,255,255,0.3) !important;
            backdrop-filter: blur(4px);
        }}
        html, body, [class*="css"] {{
            font-family: 'Poppins', sans-serif !important;
        }}
        .question-box {{
            padding: 20px;
            background: #ffffff;
            border-radius: 18px;
            font-size: 19px;
            border: 2px solid #ffffff55;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR — MAIN MENU
# =====================================================
with st.sidebar:
    st.title("😘 StudyGenie — Your AI Bestie 💖")

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
# CHAT HISTORY SETUP
# =====================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

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
        st.session_state["clear_input"] = True
        return reply

    except Exception as e:
        return "❌ Error: " + str(e)

# =====================================================
# NORMAL TOOLS (Everything except IQ Game)
# =====================================================
if tool != "Mini IQ Test Game 🧠":
    st.markdown(f"<h1 style='text-align:center;'>✨ {tool} ✨</h1>", unsafe_allow_html=True)

    # Display chat history
    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['you']}")
        st.markdown(f"**Genie:** {chat['ai']}")

    default_text = "" if st.session_state.clear_input else st.session_state.get("last_prompt", "")
    prompt = st.text_area("Type your message 💬", value=default_text)
    st.session_state.last_prompt = prompt

    if st.button("Send"):
        if prompt.strip() != "":
            st.session_state.clear_input = True
            response = ask_ai(f"{tool}: {prompt}")
            st.markdown(f"**Genie:** {response}")
            st.session_state.last_prompt = ""

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.last_prompt = ""
        st.session_state.clear_input = True
        st.rerun()
# ================= AI PLANNER =================
if tool == "AI Planner":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📆 Daily Study Planner")

    goal = st.text_input("Your goal:")

    if st.button("Make Plan ✨"):
        res = ask_ai(f"Create a simple daily study plan for: {goal}")
        st.markdown(f"<div class='genie'>{res}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= MINDSET RESET =================
elif tool == "Mindset Reset":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🌸 Mindset Reset")

    if st.button("Reset My Mind ✨"):
        res = ask_ai("Give a calm, motivating mindset reset.")
        st.markdown(f"<div class='genie'>{res}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STUDY ROUTINE =================
elif tool == "Study Routine Designer":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📚 Study Routine Designer")

    hrs = st.slider("How many hours can you study daily?", 1, 10, 4)

    if st.button("Design Routine ✨"):
        res = ask_ai(f"Design a clean study routine for {hrs} hours.")
        st.markdown(f"<div class='genie'>{res}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= EXAM STRATEGY =================
elif tool == "Exam Strategy Maker":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🎯 Exam Strategy")

    exam = st.text_input("Your exam:")

    if st.button("Build Strategy ✨"):
        res = ask_ai(f"Create a high-impact exam strategy for {exam}")
        st.markdown(f"<div class='genie'>{res}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STUDY COACH =================
elif tool == "Personal Study Coach":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("💞 Personal Study Coach")

    prob = st.text_area("Tell me what you're struggling with:")

    if st.button("Coach Me ✨"):
        res = ask_ai(f"You are a kind personal study coach. Help with: {prob}")
        st.markdown(f"<div class='genie'>{res}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
# =====================================================
# MINI IQ TEST GAME 🧠
# =====================================================
if tool == "Mini IQ Test Game 🧠":

    st.markdown("<h1 style='text-align:center;'>🧠 Mini IQ Test (MCQ Edition)</h1>", unsafe_allow_html=True)

    # -------------- IQ QUESTIONS --------------
    iq_mcq = [
        ("What number comes next? 2, 6, 12, 20, 30, __",
         ["36", "40", "42", "44"], "42"),

        ("Which one is different?",
         ["Cat", "Dog", "Lion", "Wolf"], "Cat"),

        ("Conclusion? If ALL roses are flowers and SOME flowers fade quickly…",
         ["All roses fade quickly", "Some roses may fade quickly", "No roses fade quickly"], "Some roses may fade quickly"),

        ("Missing letter? A, D, G, J, M, __",
         ["O", "P", "N", "Q"], "P"),

        ("Odd number: 27,64,125,144,216",
         ["27", "144", "125", "216"], "144"),

        ("What's bigger: 3/7 or 4/9?",
         ["3/7", "4/9"], "4/9"),

        ("Solve: (3×4)² ÷ 6",
         ["12", "24", "36", "48"], "24"),

        ("Sun : Day :: Moon : __",
         ["Light", "Sky", "Night", "Dark"], "Night"),

        ("Which weighs more?",
         ["1 kg iron", "1 kg cotton", "Both same"], "Both same"),

        ("45% of 200 =",
         ["70", "80", "90", "100"], "90")
    ]

    # Pick question
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