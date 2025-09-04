import requests
import json
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

api_key  = os.getenv("my_api", "")

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


def last_message(data,contact_name):
    conversations = data.get('conversations', {})
    contact_conversations = conversations.get(contact_name, [])
    if not contact_conversations:
        return None
    last_message = contact_conversations[-1]
    return last_message.get('text')

def last_message_sent(data,contact_name):
    conversations = data.get('conversations', {})
    contact_conversations = conversations.get(contact_name,[])
    if not contact_conversations:
        return None
    last_message_sent = contact_conversations[-1]
    return last_message_sent.get('sender')

with open('data.json', 'r') as file:
    data = json.load(file)
    
def read_conversations():
    with open('data.json', 'r') as file:
        reader = json.load(file)
        conversations = reader.get('conversations', {})
        print("================================================================")
        for contact,messages in conversations.items():
            print(f"Conversation with {contact}: ")
            for msg in messages:
                sender = msg.get('sender', '')
                text = msg.get('text', '')
                dt = msg.get('datetime', '')
                print(f"{dt}:\t{sender}\t:{text}")
            print("\n")
    print("================================================================")

def add_conversations(contact_name):
    with open('data.json', 'r') as f:
        reader = json.load(f)
        contacts = reader.get('contacts', [])
        conversations = reader.get('conversations', {})
        contact_names = [c['name'] for c in contacts]
        if contact_name not in contact_names:
            print(f"Contact '{contact_name}' not found in contacts.")
            return
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = input("Enter the message: ")
        new_msg = {"datetime": dt, "sender": contact_name, "text": message}
        if contact_name in conversations:
            conversations[contact_name].append(new_msg)
        else:
            conversations[contact_name] = [new_msg] 
        reader["conversations"] = conversations
        
    with open('data.json', 'w') as file:
        json.dump(reader, file, indent=4)
    print(f"Message added to {contact_name}'s conversation successfully.")

        
def respond_to_last_message():
    if __name__ == "__main__":
        contact_name = input("Enter the contact name (Ramesh/Roshini/Bharath): ").capitalize()
        system_msg = ""
        user_msg = last_message(data, contact_name)
        if last_message_sent(data, contact_name) == "Roopesh":
            print(f"No new message from {contact_name}.")
            exit()
        if contact_name == "Ramesh":
            system_msg = "You are Roopesh, the Manager at ojasa Mirai, a online gen AI training company. You will respond in short and to the point when candidates approaches you for GenAI."
        elif contact_name == "Roshini":
            system_msg = "You are Roopesh, The colleague of Roshini who is Software Engineer at ojasa Mirai. You will respond appropriately."
        elif contact_name == "Bharath":
            system_msg = "You are Roopesh, a dear friend of Bharath since high school. You respond as a close friend."
        else:
            system_msg = "You are Roopesh, a software Engineer. Respond appropriately to unknown contacts."

        try:
            content = get_perplexity_response(system_msg, user_msg)
            print("Model Response:", content)
        except requests.exceptions.RequestException as e:
            print("Error calling Perplexity API:", e)


print("======================Auto_Response function========================")
quit = True
while quit:
    print("Enter your Choice: \n1.View Existing Conversations\n2.Add New Conversation\n3.Respond to Last Message\n4.Quit")
    choice = input("Choice: ")
    if choice == '1':
        read_conversations()
    elif choice == '2':
        contact_name = input("Enter the contact name (Ramesh/Roshini/Bharath): ").capitalize()
        add_conversations(contact_name)
    elif choice == '3':
        respond_to_last_message()
    elif choice == '4':
        quit = False
        print("======================Exiting the program. Goodbye!========================")
    else:
        print("Invalid choice. Please try again.")

