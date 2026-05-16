import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Your API Key
API_KEY = "AIzaSyBLPxYMjLY3MDtMuf9j7w6PzGKkZfeQYa4"

# Configure Gemini
genai.configure(api_key=API_KEY)

# Page settings
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 My Personal AI Chatbot")
st.caption("Powered by Google Gemini 2.5")

# System prompt with today's date
today = datetime.now().strftime("%A, %B %d, %Y")
SYSTEM_PROMPT = f"""You are a helpful, honest and friendly AI assistant. 
Today's date is {today}.
Always give accurate and concise answers.
If you don't know something, say so honestly instead of guessing."""

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Build full conversation with system prompt
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            history = SYSTEM_PROMPT + "\n\n"
            history += "\n".join([
                f"{m['role']}: {m['content']}"
                for m in st.session_state.messages
            ])
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(history)
            reply = response.text
            st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })