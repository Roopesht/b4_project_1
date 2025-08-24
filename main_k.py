import os
from dotenv import load_dotenv
import json

#Load env file
load_dotenv()

# Read environment variables
JSON_FILE = os.getenv("JSON_FILE", "data.json")  # default = data.json
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
API_KEY = os.getenv("API_KEY")

# Load JSON file
with open("JSON_FILE", "r") as f:
    data = json.load(f)

# Function to display all contacts
def show_contacts():
    print("\n--- Contacts ---")
    for contact in data["contacts"]:
        print(f"Name: {contact['name']}, Tags: {', '.join(contact['tags'])}")

# Function to show conversation with a contact
def show_conversation(contact_name):
    conversations = data["conversations"].get(contact_name, [])
    if not conversations:
        print(f"\nNo conversation found with {contact_name}.")
        return
    
    print(f"\n--- Chat with {contact_name} ---\n")
    for msg in conversations:
        print(f"[{msg['datetime']}] {msg['sender']}: {msg['text']}")

# Function to add a new message
def add_message(contact_name, sender, text):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_message = {
        "datetime": timestamp,
        "sender": sender,
        "text": text
    }
    
    if contact_name in data["conversations"]:
        data["conversations"][contact_name].append(new_message)
    else:
        data["conversations"][contact_name] = [new_message]

    # Save to JSON
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Message added successfully!")

# adding conv
if __name__ == "__main__":
    show_contacts()
    show_conversation("Ramesh")
    add_message("Ramesh", "me", "Looking forward to our meeting!")
    show_conversation("Ramesh")