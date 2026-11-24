
import streamlit as st
from google import genai
from google.genai import types

# Page configuration
st.set_page_config(
    page_title="CHABO AI",
    page_icon="🤖",
    layout="centered"
)

# App title
st.title("🤖 CHABO AI")
st.caption("Your friendly AI assistant")

# Get API key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask CHABO AI anything...")

if user_input:
    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("CHABO AI is thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=[
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": (
                                        "You are CHABO AI, a helpful, "
                                        "clear, and friendly AI assistant "
                                        "that can answer questions "
                                        "on any topic.\n\n"
                                        + "\n".join(
                                            f"{m['role']}: {m['content']}"
                                            for m in st.session_state.messages
                                        )
                                    )
                                }
                            ]
                        }
                    ],
                    config=types.GenerateContentConfig(
                        temperature=0.7
                    )
                )

                answer = response.text or "I couldn't generate a response."

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
            
