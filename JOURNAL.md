# Build Journal

## Stage 0: Setup (12/10/2026)

### What I wanted to do
Get everything ready before writing any code: editor, Python, repo, venv.

### What I did
- Picked Python over C. I practice C more than Python but for AI stuff Python is way easier (official Claude library, no malloc/pointers to deal with, web interface later with Streamlit, makes my life way easier)
- Created the repo on GitHub with a README, the Python .gitignore and an MIT license, then cloned it
- Made a ~/Projects folder in my home folder and moved the repo there. Didn't use Desktop because of iCloud sync and the venv has thousands of files
- Upgraded Python (had 3.10.6, which is basically end of life) to 3.15
- Created the venv and activated it
- Set up the folders and a VS Code setting so screenshots I paste go straight into docs/screenshots

### Screenshots
![setup0](docs/screenshots/image.png)
![ollama-implementation](docs/screenshots/image-1.png)

### Problems I ran into
**Cloned in the wrong place**
I forgot to cd before cloning so the repo ended up in my home folder. Used `pwd` and `ls` to figure out where I was, then moved it with `mv` to my new folder/directory : Projects.

**Python version**
3.10.6 still works but it's getting dropped. I upgraded before creating the venv because the venv is stuck with the Python version that made it, so doing it later would've meant redoing the venv.

**`code .` not working**
Got "command not found". The `code` command isn't installed by default on Mac, you have to do Cmd+Shift+P > "Shell Command: Install 'code' command in PATH" in VS Code.

**Where to put folders**
Wasn't sure if docs/ and .vscode/ go inside .venv or not. Answer: outside, at the root. .venv is just for libraries and it's ignored by git anyway.

### Stuff I learned
- venv = a separate box of libraries for each project so they don't mess with each other
- .gitignore keeps the venv and later my API key (.env) off GitHub
- Every new terminal starts in ~ with the venv off, so I need `cd` + `source .venv/bin/activate` each time
- When a command fails: check where I am (`pwd`), what's there (`ls`), and actually read the error


## Stage 1: first message to the AI (12/10/2026)

goal: get my python script to send one message to an AI and print the answer. no chat yet just checking it works

### why ollama and not claude
was going to use the claude API but you have to pay for it so no. went with ollama instead, it's free and the model runs directly on my mac so nothing leaves my computer. it's less smart than claude but whatever, for learning it's fine. it asked me to log in, skipped it, don't need an account for local stuff

### what i did
- installed ollama (v0.40.3)
- `ollama pull llama3.2` to download the model, like 2gb
- tested it in the terminal with `ollama run llama3.2` before coding anything. that way if my code breaks i know it's my code and not the model
- `pip install ollama` then `pip freeze > requirements.txt`
- wrote src/main.py, it sends one message and prints the reply
- added comments so i don't forget what stuff does

### how i understand it
the ollama app = a server on my mac, it's what actually runs the model
the ollama python library = just sends my message to that server and gets the answer back
same name, two different things, confused me at first

### screenshots
![ollama-installation-requirements](docs/screenshots/image-2.png)
![main-first-test](docs/screenshots/image-3.png)
![testing with ollama off](docs/screenshots/image-4.png)

### problems
- typed `ollama --version` and `ollama pull` on the same line, didn't work obviously. one command per line
- typed just `ollama` and got some weird menu with claude code and other stuff. esc to get out. it needs `pull` or `run` after
- after `ollama run` i typed `python src/main.py` and it sent it to the AI as a message lol. i was still in the chat (the `>>>` thing). `/bye` to get out. now i look at the prompt before typing
- i thought my script would work even without the ollama app since i was using the library. and it did work... but only because the server was still running in the background even after closing the app. checked with `curl http://localhost:11434` and it said "Ollama is running". killed it with `pkill ollama` and then the script crashed with a ConnectionError. so i was wrong, no server = nothing to talk to

### what i learned
- test each part alone before putting them together
- the library talks, the app does the work
- closing a window doesn't mean the program stopped
- python errors: read the last line first, then look for the lines with my files
- if something weird happens, check instead of guessing


## Stage 2: chat loop (12/10/2026)

goal: being able to chat back and forth in the terminal instead of sending just one message. it should keep going until i type quit

### my prediction before testing
if i tell it my name and then ask what my name is, i think it'll remember since it's the same conversation

### what i did 
- replaced the code with a `while True` loop 
- `input("You: ")` waits for me to type
- if i type quit it prints bye and `break` gets out of the loop
- `.lower()` so it works even if i type QUIT

### screenshots
![ollama new code test](docs/screenshots/image-5.png)
![name test](docs/screenshots/image-6.png)
![quit test](docs/screenshots/image-7.png)

### result
nope, didn't remember my name. so i was wrong

### why
turns out the model has zero memory. every loop i'm creating a new `messages` list with just what i typed, so when i asked "what's my name?" that's literally the only thing it got. it never saw the first message

so chatgpt and claude don't really "remember" either, the app just sends the whole conversation again every time. gonna do that next

## Stage 3: giving it memory (12/10/2026)

goal: make it remember the conversation. idea is to keep one list with every message (mine and the bot's) and send the whole thing each time

### my prediction
should remember my name now since it'll see the whole conversation every time


### screenshots
![main code](docs/screenshots/image-8.png)
![ollama with memory](docs/screenshots/image-9.png)
![number of messages in memory](docs/screenshots/image-10.png)


### what i changed
- moved `messages = []` before the loop so it's created once and doesn't get wiped every turn
- `append` my message, send the whole list, then `append` the bot's answer too
- role "assistant" is the bot's messages, so it knows who said what

### result
it remembers now. asked my name and the first thing i said and it got both

added a debug print with `len(messages)` to see the list grow, goes up by 2 every turn (my message + its answer). removed it after

### PS
the list just keeps growing so long chats which means there's more to send every time, probably gets slower. also everything is gone when i close the program