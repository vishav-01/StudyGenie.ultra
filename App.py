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