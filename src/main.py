import ollama  # lets my code talk to the ollama app

# the whole conversation lives in this list
# created once before the loop so it doesn't get wiped every turn
messages = []

print("chat started, type 'quit' to exit")  # just so i know it started

while True:  # loops forever until i type quit
    user_input = input("You: ")  # shows "You: " and waits for me to type

    if user_input.lower() == "quit":  # lower() so QUIT or Quit also work
        print("bye!")  
        break  

    # add my message at the end of the conversation
    # role "user" = me talking
    messages.append({"role": "user", "content": user_input})

    # send the whole conversation to the model, not just my last message
    # it waits here until the model is done answering
    response = ollama.chat(model="llama3.2", messages=messages)

    # the answer is nested: response -> message -> content
    # i put it in a variable because i need it twice below
    reply = response["message"]["content"]

    # add the bot's answer to the conversation too
    # role "assistant" = the bot, otherwise it won't know what it said before
    messages.append({"role": "assistant", "content": reply})

    print("Bot:", reply)  # show the answer in the terminal
