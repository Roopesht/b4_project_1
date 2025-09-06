from datetime import datetime
from gemini import get_response


data = {
    "contacts": [
        {"name": "Ramesh", "tags": ["Student", "BTech"]},
        {"name": "Roshini", "tags": ["Software Engineer", "Highly ambitious"]}
    ],
    "conversations": {
        "Ramesh": [
            {"datetime": "2025-08-01 10:00:00", "sender": "Ramesh", "text": "Hi Roopesh, I want to know more on GenAI"},
            {"datetime": "2025-08-01 10:01:00", "sender": "me", "text": "Hi Ramesh, I will send you the brochure"}
        ]
    }
}


system_msg = "You are Roopesh, the Manager at ojasa Mirai, an online GenAI training company. You respond shortly and to the point when candidates approach you for GenAI."

def show_conversations(data):
    for contact in data["contacts"]:
        name=contact["name"]
        print("Conversation with ",name)
        if name in data["conversations"]:
            messages=data["conversations"][name]  
            
        else:
            print("no messages")
            continue 
        for msg in messages:
            if msg["sender"]=="me":
                sender="Roopesh"
            else:
                sender=msg["sender"]
            print(sender + " at " + msg["datetime"] + ": " + msg["text"])       




def add_conversation(data):
    name = input("Enter the sender of this message's name: ")
    message = input("Enter the message to be sent: ")


 
    present = False

    for contact in data["contacts"]:
        if contact["name"] == name:
            present = True
            break

    if not present:
        print("Contact not present in the existing data")
        return

    
    new_msg = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender": name,
        "text": message
    }

  
    if name in data["conversations"]:
        data["conversations"][name].append(new_msg)
    else:
        data["conversations"][name] = [new_msg]

    print("Message added")





def respond_to_users(data):
    for contact in data["contacts"]:
        name = contact["name"]

       
        if name in data["conversations"]:
            conversation = data["conversations"][name]
        else:
            continue 

        if not conversation:
            continue  

        last_msg = conversation[-1]

      
        if last_msg["sender"] == "me":
            continue

        
        user_msg = last_msg["text"]

        reply = get_response(system_msg, user_msg)

        print("Replying to", name + ":", reply)

       
        new_msg = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender": "me",
            "text": reply
        }

        data["conversations"][name].append(new_msg)



if __name__ == "__main__":
    while True:
        print("Ojasa Mirai Conversation System ")
        print("1. View existing conversations")
        print("2. Add a conversation")
        print("3. Respond to all conversations (if applicable)")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            show_conversations(data)
        elif choice == "2":
            add_conversation(data)
        elif choice == "3":
            respond_to_users(data)
        elif choice == "4":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid Choice; re-enter a valid one")
