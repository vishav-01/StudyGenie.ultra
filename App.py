import streamlit as st
import requests
import json
import random

# ================= HARD RESET ON REFRESH =================
st.session_state.clear()

# ================= PAGE CONFIG =================
st.set_page_config(page_title="StudyGenie", layout="wide")

# ================= THEME SYSTEM =================
theme = st.sidebar.selectbox(
    "🌈 Theme",
    ["Doraemon", "Sky Blue", "Pink Pastel", "Lavender"],
)

themes = {
    "Doraemon": ("#5EC2FF", "#0089E0"),
    "Sky Blue": ("#d2eaff", "#8cc8ff"),
    "Pink Pastel": ("#ffd6e8", "#ffa4c8"),
    "Lavender": ("#e7d9ff", "#c7a4ff"),
}

g1, g2 = themes[theme]

# ================= CSS =================
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, {g1}, {g2});
    font-family: 'Poppins', sans-serif;
}}

.sidebar .sidebar-content {{
    background: rgba(255,255,255,0.3);
}}

.chat-user {{
    background: #ffffff;
    padding: 12px 16px;
    border-radius: 18px 18px 0 18px;
    max-width: 70%;
    margin: 10px 0 10px auto;
}}

.chat-ai {{
    background: #eaf4ff;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 0;
    max-width: 70%;
    margin: 10px auto 10px 0;
}}

.card {{
    background: rgba(255,255,255,0.85);
    padding: 20px;
    border-radius: 18px;
}}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
tool = st.sidebar.radio(
    "✨ Tools",
    [
        "AI Planner",
        "Mindset Reset",
        "Study Routine Designer",
        "Exam Strategy Maker",
        "Personal Study Coach",
        "Mini IQ Test 🧠"
    ]
)

# ================= MEMORY =================
if "memory" not in st.session_state:
    st.session_state.memory = {t: [] for t in [
        "AI Planner", "Mindset Reset", "Study Routine Designer",
        "Exam Strategy Maker", "Personal Study Coach"
    ]}

# ================= MOOD DETECTION =================
def detect_mood(text):
    t = text.lower()
    if any(w in t for w in ["sad","tired","cry","low","alone"]):
        return "sad 😔"
    if any(w in t for w in ["stress","exam","panic","pressure"]):
        return "stressed 😵‍💫"
    if any(w in t for w in ["happy","excited","love","confident"]):
        return "happy 😊"
    return "neutral 🙂"

# ================= AI CALL =================
def ask_ai(user_input, tool):
    mood = detect_mood(user_input)
    memory_text = "\n".join(
        [f"User: {m['u']}\nAI: {m['a']}" for m in st.session_state.memory[tool][-4:]]
    )

    prompt = f"""
You are StudyGenie, a warm Gen-Z AI study bestie.
User mood: {mood}

Memory:
{memory_text}

User message:
{user_input}
"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
        "max_tokens": 1200
    }

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=json.dumps(payload),
        timeout=20
    )

    data = r.json()
    reply = data["choices"][0]["message"]["content"]

    st.session_state.memory[tool].append({"u": user_input, "a": reply})
    return reply

# ================= CHAT UI =================
if tool != "Mini IQ Test 🧠":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    for m in st.session_state.memory[tool]:
        st.markdown(f"<div class='chat-user'>{m['u']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-ai'>{m['a']}</div>", unsafe_allow_html=True)

    msg = st.text_area("Type here…", height=80)

    if st.button("Send ✨") and msg.strip():
        reply = ask_ai(msg, tool)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================= IQ GAME =================
if tool == "Mini IQ Test 🧠":

    def generate_iq():
        q = []
        for _ in range(50):
            a = random.randint(3, 10)
            q.append((
                f"What comes next? {a}, {a*2}, {a*3}, {a*4}, ?",
                [str(a*5), str(a*6), str(a*4), str(a*7)],
                str(a*5)
            ))
        for _ in range(30):
            n = random.randint(4, 12)
            q.append((
                f"What is {n}² + {n}³?",
                [str(n*n), str(n**3), str(n*n+n**3), str(n**3-n)],
                str(n*n+n**3)
            ))
        for _ in range(30):
            x,y = random.randint(10,99), random.randint(10,99)
            q.append((
                f"Which is larger? {x}/{y} or {y}/{x}",
                [f"{x}/{y}", f"{y}/{x}"],
                f"{y}/{x}" if (y/x) > (x/y) else f"{x}/{y}"
            ))
        return q

    if "iq" not in st.session_state:
        st.session_state.iq = generate_iq()
        st.session_state.q = random.choice(st.session_state.iq)

    ques, opts, ans = st.session_state.q

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"**🧠 {ques}**")
    choice = st.radio("Choose:", opts)

    if st.button("Submit"):
        st.success("🔥 Correct!" if choice == ans else f"❌ Wrong. Answer: {ans}")

    if st.button("Next Question"):
        st.session_state.q = random.choice(st.session_state.iq)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)