import json #to save and load the convo as a file
import os   #to check if the file exists 
import ollama  # lets my code talk to the ollama app
from datetime import datetime

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
- the messages before the current one include our earlier conversations, saved from before
- when I ask what we talked about, use those messages to answer
- keep the anti-hallucination part, for anything not in the conversation (what I did today, where I am...), say you don't know, say it, don't make anything up
- if i am asking you to give me an information that you don't have, just say you don't have it instead of making things up 
"""

# read my private info from a file that git ignores
HISTORY_FILE = "data/history.json"

OLLA = "llama3.1:8b"

# "r" = read mode, utf-8 so french accents don't break
# "with" closes the file automatically when done
with open("data/about_me.txt", "r", encoding="utf-8") as f:
    about_me = f.read()  # the whole file as one string

# glue the personality and my info together into one system message

full_prompt = SYSTEM_PROMPT + "\nAbout me:\n" + about_me

#to load a saved convo from before ( if there's one )
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f :
        try:
            history = json.load(f)  #turns the json text back into a python list
        except json.decoder.JSONDecodeError :
            print("History file is broken, an empty list is created")
            history = []
    print(f"Loaded {len(history)} old messages")    #to check if it worked
else :
    history = []    #if there's no history ( first time convo )


#the system message first, then the old convo after it
messages = [{"role": "system", "content": full_prompt}] + history

date_now = datetime.now()
full_date = date_now.strftime("%d/%m/%Y %H:%M")

print(f"A new session has started, type 'quit' to exit : {full_date}")  # so i know it started


if len(history) != 0:
    messages.append({"role": "system", "content": f"A new session has started : {full_date}"})

while True:  # loops until i type quit
    user_input = input("You: ")  # waits for me to type

    if user_input.lower() == "quit":  # lower() so QUIT works too
        print("bye!")
        break  # exits the loop

    # add my message to the convo
    messages.append({"role": "user", "content": user_input})

    # send everything to the model
    response = ollama.chat(model=OLLA, messages=messages)

    # get just the text of the answer
    reply = response["message"]["content"]

    # save alfred's answer so he remembers it
    messages.append({"role": "assistant", "content": reply})

    # save the convo after every answer
    # "w" = write mode, replaces the old file with the new version
    # messages[1:] = everything except the first item (the system message)
    # ensure_ascii=False keeps accents readable, indent=2 makes the file easy to read
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages[1:], f, ensure_ascii=False, indent=2)

    print("Alfred:", reply)  # show the answer