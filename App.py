import streamlit as st
import requests

st.set_page_config(page_title="Simple AI Test")

st.title("🤖 Simple AI Test")

# Input box
prompt = st.text_input("Ask something:")

def ask_ai(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        return response.text

    return response.json()["choices"][0]["message"]["content"]

# Button
if st.button("Send"):
    if prompt:
        reply = ask_ai(prompt)
        st.write("AI:", reply)