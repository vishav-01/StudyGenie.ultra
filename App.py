import streamlit as st
import requests, json, random

# ================= PAGE =================
st.set_page_config(page_title="StudyGenie", layout="wide")

# ================= THEME =================
theme = st.sidebar.selectbox("🎨 Theme", ["Doraemon","Sky","Pink","Lavender"])
themes = {
    "Doraemon":("#5EC2FF","#0089E0"),
    "Sky":("#d2eaff","#8cc8ff"),
    "Pink":("#ffd6e8","#ffa4c8"),
    "Lavender":("#e7d9ff","#c7a4ff")
}
bg1,bg2 = themes[theme]

# ================= CSS =================
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg,{bg1},{bg2});
    font-family:Poppins,sans-serif;
}}
.card {{
    background:rgba(255,255,255,0.9);
    padding:20px;
    border-radius:16px;
}}
.user {{
    background:#fff;
    padding:12px;
    border-radius:16px 16px 0 16px;
    max-width:70%;
    margin:8px 0 8px auto;
}}
.ai {{
    background:#eaf3ff;
    padding:12px;
    border-radius:16px 16px 16px 0;
    max-width:70%;
    margin:8px auto 8px 0;
}}
</style>
""",unsafe_allow_html=True)

# ================= TOOLS =================
tools = [
 "AI Doubt Solver","Notes Generator","Summary Maker","Timetable Builder",
 "Motivation Booster","Flashcards","Brain-Dump Cleaner","Answer Checker",
 "AI Planner","Mindset Reset","Study Routine Designer",
 "Exam Strategy Maker","Personal Study Coach","Mini IQ Test Game 🧠"
]
tool = st.sidebar.radio("✨ Tools", tools)

# ================= MEMORY =================
if "memory" not in st.session_state:
    st.session_state.memory = {t:[] for t in tools}

# ================= MOOD =================
def mood(txt):
    t=txt.lower()
    if any(w in t for w in ["sad","low","cry","alone"]): return "sad"
    if any(w in t for w in ["stress","exam","panic"]): return "stressed"
    if any(w in t for w in ["happy","excited","love"]): return "happy"
    return "neutral"

# ================= AI =================
def ask_ai(msg,tool):
    context=""
    for m in st.session_state.memory[tool][-4:]:
        context+=f"User:{m['u']}\nAI:{m['a']}\n"

    prompt=f"""
You are StudyGenie, a friendly Gen-Z AI study assistant.
User mood: {mood(msg)}

Context:
{context}

Task: {tool}
User: {msg}
"""

    headers={
      "Authorization":f"Bearer {st.secrets['OPENAI_API_KEY']}",
      "Content-Type":"application/json"
    }
    payload={
      "model":"gpt-4.1-mini",
      "messages":[{"role":"user","content":prompt}],
      "temperature":0.6,
      "max_tokens":1200
    }

    r=requests.post(
      "https://api.openai.com/v1/chat/completions",
      headers=headers,
      data=json.dumps(payload),
      timeout=20
    )
    reply=r.json()["choices"][0]["message"]["content"]
    st.session_state.memory[tool].append({"u":msg,"a":reply})
    return reply

# ================= CHAT FEATURES =================
if tool!="Mini IQ Test Game 🧠":
    st.markdown("<div class='card'>",unsafe_allow_html=True)

    for m in st.session_state.memory[tool]:
        st.markdown(f"<div class='user'>{m['u']}</div>",unsafe_allow_html=True)
        st.markdown(f"<div class='ai'>{m['a']}</div>",unsafe_allow_html=True)

    msg=st.text_area("Type here…",height=80)

    if st.button("Send"):
        if msg.strip():
            ask_ai(msg,tool)
            st.rerun()

    st.markdown("</div>",unsafe_allow_html=True)

# ================= IQ GAME =================
if tool=="Mini IQ Test Game 🧠":

    def iq_bank():
        q=[]
        for _ in range(120):
            n=random.randint(3,15)
            q.append((
              f"What is {n}² + {n}³ ?",
              [str(n*n),str(n**3),str(n*n+n**3),str(n**3-n)],
              str(n*n+n**3)
            ))
        return q

    if "iq" not in st.session_state:
        st.session_state.iq=iq_bank()
        st.session_state.q=random.choice(st.session_state.iq)

    ques,opts,ans=st.session_state.q

    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.markdown(f"🧠 **{ques}**")
    c=st.radio("Choose:",opts)

    if st.button("Submit"):
        st.success("Correct 🔥" if c==ans else f"Wrong ❌ Answer: {ans}")

    if st.button("Next"):
        st.session_state.q=random.choice(st.session_state.iq)
        st.rerun()

    st.markdown("</div>",unsafe_allow_html=True)