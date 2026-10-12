import ollama  # lets my code talk to the ollama app

# alfred's personality, caps because it's a constant (never changes)
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

About me:
- I'm Saif, engineering student
- I like straight answers, no long speeches
"""

# the convo starts with the system message already in it
# so the model reads the personality before anything else
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("chat started, type 'quit' to exit")  # so i know it started

while True:  # loops forever until i type quit
    user_input = input("You: ")  # waits for me to type

    if user_input.lower() == "quit":  # lower() so QUIT works too
        print("bye!")
        break  # exits the loop

    # add my message to the convo
    messages.append({"role": "user", "content": user_input})

    # send everything (personality + whole convo) to the model
    response = ollama.chat(model="llama3.2", messages=messages)

    # dig into the answer to get just the text
    reply = response["message"]["content"]

    # save alfred's answer so he remembers what he said
    messages.append({"role": "assistant", "content": reply})

    print("Alfred:", reply)  # show the answer