import json  # to save and load the convo as a file
import os  # to check if the file exists
import ollama  # lets my code talk to the ollama app
from datetime import datetime


# alfred's personality (no personal info in here because this file is public)
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

HISTORY_FILE = "data/history.json"  # where the convo gets saved (git ignores it)

MODEL = "llama3.1:8b" 


def load_history():
    # to load a saved convo from before (if there's one)
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)  # turns json text into python list
            except json.decoder.JSONDecodeError:
                print("History file is broken, starting with an empty history")
                return []
        print(f"Loaded {len(history)} old messages")  
        return history  
    else:
        return []  # no history yet (first time convo)



def save_history(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages[1:], f, ensure_ascii=False, indent=2)


def start_messages():
    with open("data/about_me.txt", "r", encoding="utf-8") as f:
        about_me = f.read()  # the whole file as one string

    full_prompt = SYSTEM_PROMPT + "\nAbout me:\n" + about_me

    history = load_history()

    messages = [{"role": "system", "content": full_prompt}] + history
    
    date_now = datetime.now()
    full_date = date_now.strftime("%d/%m/%Y %H:%M") 

    if len(history) != 0:
        messages.append({"role": "system", "content": f"A new session has started : {full_date}"})

    print(f"A new session has started : {full_date}")  # so i know it started

    return messages

def ask_alfred(messages):
    # send everything to the model
    response = ollama.chat(model=MODEL, messages=messages)

    # get just the text of the answer
    reply = response["message"]["content"]

    return reply