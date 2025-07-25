
# Define a function to handle user input
def chatbot_response(user_input):
    # Convert input to lowercase for consistency
    user_input = user_input.lower()

    # Rule-based responses
    if "hello" in user_input or "hi" in user_input:
        return "Hi there! 👋 How can I assist you today?"

    elif "how are you" in user_input:
        return "I'm just a bunch of code, but I'm running smoothly. Thanks for asking!"

    elif "what is your name" in user_input or "your name" in user_input:
        return "I'm ChatBot, your friendly rule-based assistant."

    elif "bye" in user_input or "goodbye" in user_input:
        return "See you later! Have a great day! 😊"

    else:
        return "Hmm... I didn’t quite get that. Could you try saying it differently?"

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "exit", "quit"]:
        print("ChatBot: Goodbye!")
        break
    response = chatbot_response(user_input)
    print("ChatBot:", response)
