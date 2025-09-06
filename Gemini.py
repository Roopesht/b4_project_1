import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY", "")

def get_response(system_message: str, user_message: str, model="gemini-2.0-flash") -> str:
    """
    Sends messages to Google Gemini API and returns the model's response.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"{system_message}\n\nUser: {user_message}"}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise error for bad status codes
    data = response.json()

    # Extract and return the model's reply content
    return data["candidates"][0]["content"]["parts"][0]["text"]

# Example usage:
if __name__ == "__main__":
    system_msg = "You are Roopesh, the Manager at ojasa Mirai, a online gen AI training company. You will respond to incoming messages in short and to the point when candidates approaches you for GenAI."
    user_msg = "Hi Roopesh, I am beginner, how long does it take to learn GenAI completely including architecture"

    try:
        content = get_response(system_msg, user_msg)
        print("Model Response:", content)
    except requests.exceptions.RequestException as e:
        print("Error calling Gemini API:", e)