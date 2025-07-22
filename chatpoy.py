import streamlit as st
import google.generativeai as genai

# Streamlit App Setup
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Gemini AI Chatbot")
st.caption("Chat with Google's Gemini using Streamlit")

# API Key setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize the Model
model = genai.GenerativeModel('gemini-pro')

# Chat History Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
user_input = st.chat_input("Say something...")

if user_input:
    # Save User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get Gemini Response
    response = model.generate_content(user_input)

    bot_reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

