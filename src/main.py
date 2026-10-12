import ollama  # lets my code talk to the ollama app

# alfred's personality (no personal info in here anymore because this file is public)
SYSTEM_PROMPT = """
You're Alfred, my personal assistant / butler : polite, calm, loyal.

How you talk:
- call me "sir" sometimes, not every message
- you can be a bit sarcastic but don't overdo it
- if I'm about to do something dumb, tell me (politely)

Rules:
- short answers, 3 sentences max unless I ask for more
- answer in the language I use (french or english)
- you only know what I tell you in this chat. you have no idea what I did today, where I am, what I ate, etc.
- if I ask about something I never told you, say you don't know, don't guess
- answer the question first 
"""

# read my private info from a file that git ignores
# "r" = read mode, utf-8 so french accents don't break
# "with" closes the file automatically when done
with open("data/about_me.txt", "r", encoding="utf-8") as f:
    about_me = f.read()  # the whole file as one string

# glue the personality and my info together into one system message

full_prompt = SYSTEM_PROMPT + "\nAbout me:\n" + about_me

# the convo starts with the system message
messages = [{"role": "system", "content": full_prompt}]

print("chat started, type 'quit' to exit")  # so i know it started

while True:  # loops until i type quit
    user_input = input("You: ")  # waits for me to type

    if user_input.lower() == "quit":  # lower() so QUIT works too
        print("bye!")
        break  # exits the loop

    # add my message to the convo
    messages.append({"role": "user", "content": user_input})

    # send everything to the model
    response = ollama.chat(model="llama3.2", messages=messages)

    # get just the text of the answer
    reply = response["message"]["content"]

    # save alfred's answer so he remembers it
    messages.append({"role": "assistant", "content": reply})

    print("Alfred:", reply)  # show the answer