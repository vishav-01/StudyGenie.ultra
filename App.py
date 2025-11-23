import streamlit as st
import requests
import json
import random

# ---------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------
st.set_page_config(page_title="StudyGenie AI : Your Study Babe 😘", layout="wide")

# ---------------------------------------------------
# THEME SELECTOR (FROM APP 1)
# ---------------------------------------------------
theme = st.sidebar.selectbox(
    "🌈 Choose Theme",
    ["Pink Pastel", "Sky Blue", "Lavender", "Doraemon"]
)

theme_colors = {
    "Pink Pastel": "#ffd1dc",
    "Sky Blue": "#cfe8ff",
    "Lavender": "#e6d7ff",
    "Doraemon": "#44a8ff",
}

bg_color = theme_colors[theme]

# ---------------------------------------------------
# GLOBAL CSS MERGED (APP1 + APP2)
# ---------------------------------------------------
css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

.stApp {{
    background-color: {bg_color} !important;
}}

html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
    font-family: 'Poppins', sans-serif !important;
    background: linear-gradient(170deg, {bg_color}AA, #ffffffEE);
    background-attachment: fixed !important;
}}

section[data-testid="stSidebar"] {{
    background-color: {bg_color}33 !important;
}}

.section {{
    background: rgba(255, 255, 255, 0.45);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.4);
    margin-top: 20px;
    backdrop-filter: blur(10px);
}}

.genie-bubble {{
    background: #ffffffa8;
    padding: 16px;
    margin: 12px 0;
    border-radius: 14px;
    border-left: 4px solid #a88bff;
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown(
    "<h1 style='text-align:center;color:#4a3b8f;'>✨ "StudyGenie AI - Your Study Babe 💕</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:#6b57cc;'>Your Study Bestie, always here 💜</p>",
    unsafe_allow_html=True
)

# ---------------------------------------------------
# AI CALL
# ---------------------------------------------------
def ask_ai(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [{
            "role": "user",
            "content": (
                "Soft Gen-Z tone. Short, helpful.\n\n" + prompt
            )
        }],
        "max_tokens": 350,
        "temperature": 0.65
    }

    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=20
        )
        data = r.json()

        if "choices" not in data:
            return "⚠️ Genie fainted for a sec bestie 😭."

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return "❌ Error: " + str(e)


# ---------------------------------------------------
# SIDEBAR TOOL SELECTOR (MERGED BOTH APPS)
# ---------------------------------------------------
tool = st.sidebar.radio(
    "✨ Choose a Tool",
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
    ]
)

# ---------------------------------------------------
# TOOL ENGINE — MERGED FROM BOTH APPS
# ---------------------------------------------------

# 1 — AI DOUBT SOLVER
if tool == "AI Doubt Solver":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("💡 Ask your doubt")

    q = st.text_area("Your question bestie:")
    if st.button("Solve it 💜"):
        if q.strip():
            ans = ask_ai(q)
            st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 2 — NOTES GENERATOR
elif tool == "Notes Generator":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📘 Aesthetic Notes")

    topic = st.text_input("Topic:")
    if st.button("Generate Notes ✨"):
        if topic.strip():
            ans = ask_ai(f"Make crisp cute notes on: {topic}")
            st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 3 — SUMMARY MAKER
elif tool == "Summary Maker":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📄 Ultra Summary")
    txt = st.text_area("Paste text to summarize:")
    if st.button("Summarize ✨"):
        if txt.strip():
            ans = ask_ai("Summarize this short & clear:\n" + txt)
            st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)

# 4 — TIMETABLE BUILDER
elif tool == "Timetable Builder":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📅 Cute Timetable")
    subjects = st.text_input("Subjects (comma separated):")
    hours = st.slider("Total hours / day:", 1, 12, 5)
    if st.button("Create ✨"):
        if subjects.strip():
            subs = [s.strip() for s in subjects.split(",")]
            each = round(hours / len(subs), 2)
            out = ""
            for s in subs:
                out += f"📘 {s}: **{each} hrs**\n"
            st.markdown(f"<div class='genie-bubble'>{out}</div>", unsafe_allow_html=True)

# 5 — MOTIVATION BOOSTER
elif tool == "Motivation Booster":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🔥 Motivation Shot")
    quotes = [
        "You’re growing silently. I’m proud of you.",
        "Future you is already smiling at your effort.",
        "Slow progress is still progress babe."
    ]
    if st.button("Boost Me ✨"):
        st.markdown(
            f"<div class='genie-bubble'>{random.choice(quotes)}</div>",
            unsafe_allow_html=True
        )

# 6 — FLASHCARDS
elif tool == "Flashcards":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🃏 Flashcards")
    topic = st.text_input("Topic:")
    if st.button("Generate Flashcards ✨"):
        if topic.strip():
            ans = ask_ai(f"Make 6 simple flashcards for: {topic}")
            st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)

# 7 — BRAIN-DUMP CLEANER
elif tool == "Brain-Dump Cleaner":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🧠 Clean up your thoughts")
    dump = st.text_area("Write your messy thoughts:")
    if st.button("Organize ✨"):
        ans = ask_ai("Organize this neatly:\n" + dump)
        st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)

# 8 — ANSWER CHECKER
elif tool == "Answer Checker":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("✔️ Answer Checker")
    your = st.text_area("Your answer:")
    correct = st.text_area("Correct answer:")
    if st.button("Check ✨"):
        ans = ask_ai(
            f"Compare student answer with correct answer. Short: {your} || Correct: {correct}"
        )
        st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)

# 9 — AI PLANNER
elif tool == "AI Planner":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📆 Daily Planner")
    goal = st.text_input("Your goal:")
    if st.button("Make Plan ✨"):
        ans = ask_ai(f"Make a simple clean daily plan for this goal: {goal}")
        st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)

# 10 — MINDSET RESET
elif tool == "Mindset Reset":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🌸 Mindset Reset")
    if st.button("Reset Me ✨"):
        ans = ask_ai("Give a mindset reset. Soft tone.")
        st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)

# 11 — STUDY ROUTINE DESIGNER
elif tool == "Study Routine Designer":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📚 Study Routine Designer")
    hours = st.slider("Hours you can study:", 1, 10, 4)
    if st.button("Design ✨"):
        ans = ask_ai(f"Create a daily study routine for {hours} hours.")
        st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)

# 12 — EXAM STRATEGY MAKER
elif tool == "Exam Strategy Maker":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🎯 Exam Strategy")
    exam = st.text_input("Exam:")
    if st.button("Build Strategy ✨"):
        ans = ask_ai(f"Make a high-impact exam strategy for: {exam}")
        st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)

# 13 — PERSONAL STUDY COACH
elif tool == "Personal Study Coach":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("💞 Personal Study Coach")
    msg = st.text_area("Tell me what you’re struggling with:")
    if st.button("Coach Me ✨"):
        ans = ask_ai(f"You are their soft study coach. Respond: {msg}")
        st.markdown(f"<div class='genie-bubble'>{ans}</div>", unsafe_allow_html=True)
