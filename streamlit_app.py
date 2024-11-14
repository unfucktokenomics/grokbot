import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from a .env file if present (useful for local development)
load_dotenv()

# Retrieve the API key securely from the environment
api_key = os.getenv("XAI_API_KEY")

# Function to get response from XAI API
def get_xai_response(api_key, user_input):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are a test assistant."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, json=data, verify=True)  # Use verify=True for production security
        response.raise_for_status()  # Raise error if HTTP status is 4xx or 5xx
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
    except requests.exceptions.HTTPError as http_error:
        st.error(f"HTTP Error: {http_error} - Check the endpoint URL and request format.")
        print(f"Full Response Content: {response.content}")  # For debugging
        return None
    except requests.exceptions.RequestException as req_error:
        st.error("Failed to connect to the API.")
        print(f"Request Error: {req_error}")
        return None

# Streamlit app main section
user_input = st.text_input("Ask the bot:", "Testing. Just say hi and hello world and nothing else.")

if api_key is None:
    st.error("API key not found. Please set the XAI_API_KEY environment variable.")
elif user_input:
    bot_response = get_xai_response(api_key, user_input)
    if bot_response:
        st.write(bot_response)
    else:
        st.write("No response from the bot.")
