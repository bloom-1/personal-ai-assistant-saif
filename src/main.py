from alfred import save_history, start_messages, ask_alfred

messages = start_messages() #start the conversation

print("Type 'quit' to exit")    #inform the user on how to quit the conversation 

while True:
    user_input = input("You: ") # wait for my message

    if user_input.lower() == "quit":   #check if the user wants to quit the conversation
        print("Bye !")
        break

    messages.append({"role":"user", "content":user_input})  #add the user's message into 'messages'

    reply = ask_alfred(messages)    # get alfred's reply

    messages.append({"role":"assistant", "content":reply})  #add his reply into 'messages'
    save_history(messages)  #save the interaction / conversation
    print(f"Alfred: {reply}")   #print the answer