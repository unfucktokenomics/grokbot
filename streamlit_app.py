import streamlit as st
import openai
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Chatbot with Grok API",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto",
)

# Grok API endpoint and Streamlit secrets for secure API management
API_KEY = st.secrets["xai_api_key"]
BASE_URL = "https://api.x.ai/v1"

# Set default chatbot messages
DEFAULT_RESPONSES = {
    "greeting": "Hello! How can I assist you today?",
    "farewell": "Goodbye! Have a great day ahead!",
    "basic_questions": "I'm here to answer your questions to the best of my ability."
}

# Chat function that communicates with the Grok API
def get_grok_response(user_message):
    try:
        # Set up the OpenAI client
        client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)
        
        # Construct the request payload
        messages = [
            {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhiker's Guide to the Galaxy."},
            {"role": "user", "content": user_message}
        ]
        
        completion = client.chat.completions.create(
            model="grok-beta",
            messages=messages
        )

        # Return the response from Grok
        return completion.choices[0].message['content'] if completion.choices else "I'm not sure how to respond to that."
    except Exception as e:
        logging.error(f"Error communicating with Grok API: {e}")
        return "Sorry, I am currently experiencing connectivity issues."

# Streamlit UI elements for the chatbot application
def main():
    st.title("Streamlit Chatbot with Grok API")
    st.write("Welcome! Feel free to ask me anything. 🚀")

    # Store conversation history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Input for user message
    user_message = st.text_input("You:", key="user_message")

    # Handle user input
    if user_message:
        # Add user message to history
        st.session_state.history.append({"user": user_message})

        # Get response from Grok API
        bot_response = get_grok_response(user_message)

        # Add bot response to history
        st.session_state.history.append({"bot": bot_response})

    # Display conversation history with unique keys for each element
    for idx, message in enumerate(st.session_state.history):
        if "user" in message:
            st.text_area("User:", message["user"], key=f"user_{idx}", disabled=True)
        elif "bot" in message:
            st.text_area("Bot:", message["bot"], key=f"bot_{idx}", disabled=True)

# Entry point for the Streamlit application
if __name__ == "__main__":
    main()