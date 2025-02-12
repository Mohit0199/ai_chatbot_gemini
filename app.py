import streamlit as st
import google.generativeai as ai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

ai.configure(api_key=API_KEY)

# Initialize Model
model = ai.GenerativeModel("gemini-pro")

# Streamlit UI
st.title("💬 AI Chatbot using Gemini-Pro")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores messages for display
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Stores conversation context

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message to UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Append user input to chat history in Gemini’s format
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": user_input}]})

    # Generate AI response with full chat history
    response = model.generate_content(st.session_state.chat_history)

    # Extract response text
    ai_response = response.text

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)

    # Store AI response in session state
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": ai_response}]})
