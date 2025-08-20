import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key  = os.getenv("PERPLEXITY_API_KEY", "")

def get_perplexity_response(system_message: str, user_message: str) -> str:

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise error for bad status codes
    data = response.json()

    # Extract and return the model's reply content
    return data["choices"][0]["message"]["content"]

# Example usage:
if __name__ == "__main__":
    system_msg = "You are Roopesh, the Manager at ojasa Mirai, a online gen AI training company. You will respond to incoming messages in short and to the point when candidates approaches you for GenAI."
    user_msg = " Hi Roopesh, I am beginner, how long does it take to learn GenAI completely including architecture"

    try:
        content = get_perplexity_response(system_msg, user_msg)
        print("Model Response:", content)
    except requests.exceptions.RequestException as e:
        print("Error calling Perplexity API:", e)
