import os
import time
import streamlit as st
import google import genai
from google.genai import types, errors


def main() -> None:
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print('Run: export GEMINI_API_KEY="your-api-key-here"')
        sys.exit(1)

    client = genai.Client()

    chat = client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are CHABO AI, a helpful, clear, and friendly AI assistant "
                "that can answer questions on any topic."
            ),
            temperature=0.7,
        ),
    )

    print("=========================================")
    print("  CHABO AI is online! Ask anything.")
    print("  Type 'exit' or 'quit' to end the chat.")
    print("=========================================\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nCHABO AI: Goodbye! See you next time.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("CHABO AI: Goodbye! See you next time.")
            break

        try:
            response = chat.send_message(user_input)
            print(f"\nCHABO AI: {response.text}\n")
        except Exception as exc:
            print(f"\n[Error communicating with CHABO AI: {exc}]\n")


if __name__ == "__main__":
    main()
