# Import the ollama library so Python can talk to the Ollama server
import ollama

print("chat started, type 'quit' to exit")

while True:  # loops forever until break
    user_input = input("You: ")  # waits for me to type something

    # stop if i type quit (lower() so QUIT or Quit work too)
    if user_input.lower() == "quit":
        print("bye!")
        break
    
    # sends my message to the model and waits for the reply (ollama needs to be open or this crashes, learned that the hard way)
    response = ollama.chat(
        model="llama3.2",    # the model I pulled earlier
        messages=[{"role": "user", "content": user_input}], # role = who's talking, content = what they say
    )

    print("Bot:", response["message"]["content"])   # the reply is nested: response -> message -> content
