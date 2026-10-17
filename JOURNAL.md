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

### problems
- nothing broke in the code itself, it ran first try
- the "problem" was my prediction, i thought it'd remember my name and it didn't. explained in the result part

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

### problems
- added the debug print but couldn't see it when running. it has to be inside the loop, right under `print("Bot:", reply)` with the exact same indentation, otherwise it doesn't run every turn. moved it and the count showed up
- learned to look at the vertical lines in vs code to see which block a line belongs to

## Stage 4: giving it a personality (12/10/2026)

goal: give my bot a name, a way of talking and some rules. there's a 3rd role called "system", it's a hidden message at the start of the convo that tells the model how to act

### my prediction
i think it's gonna work really well, especially when i gave it more info, rules and told it how to behave with me. 

### my system prompt
"""
You're Alfred, my personal assistant. Think classy British butler: polite, calm, loyal.

How you talk:
- call me "sir" sometimes, not every message
- you can be a bit sarcastic/witty but don't overdo it
- if I'm about to do something dumb, tell me (politely)

Rules:
- short answers, 3 sentences max unless I ask for more
- answer in the language I use (french or english)
- if you don't know something just say it, don't invent stuff
- answer the question first, jokes after

About me:
- I'm Saif, engineering student
- I like straight answers, no long speeches
"""


### screenshots
![alfred's frist day](docs/screenshots/image-11.png)

### what i changed
- added a SYSTEM_PROMPT at the top with alfred's personality and rules
- the messages list now starts with the system message in it instead of being empty, so the model reads the personality first every time
- changed "Bot:" to "Alfred:" in the print

### result
(keep what's true, delete the rest)
- he says who he is and calls me sir, works
- kept it short and went longer when i asked, works
- answered in french when i wrote in french
- made something up about what i ate
- told me not to skip school

about the debug count: list starts with 1 thing now (the system message) so it would go 3, 5, 7 instead of 2, 4, 6

### what i noticed
llama3.2 is small so it doesn't follow every rule perfectly. the more precise the rule the better it follows it

### hallucination
asked "what did i eat today" and he just made something up even though my rule says don't invent stuff. that's called a hallucination, the model predicts words that sound right, it doesn't actually know that it doesn't know changed the rule to be more specific: told him he only knows what i say in the chat and to say he doesn't know if i never told him after the change he said he didn't know.

### problems
- first version of the system prompt was too clean and didn't sound like me, rewrote it my way but kept the precise rules like "3 sentences max"
- asked "what did i eat today" and he made something up even though the rules said not to (more in the hallucination part)


## Stage 5: private info file (12/10/2026)

goal: give alfred personal info about me without putting it on github. the "about me" part is in main.py right now and my repo is public so anyone can read it. moving it to a separate file that git ignores


### screenshots
![new data folder](docs/screenshots/image-12.png)
![protected info](docs/screenshots/image-13.png)
![code with my protected info](docs/screenshots/image-14.png)
![testing main](docs/screenshots/image-15.png)
![error message](docs/screenshots/image-16.png)

### what i did
- moved the "about me" part out of main.py into data/about_me.txt
- added data/about_me.txt to .gitignore so it stays on my mac
- made about_me.example.txt with fake info, that one goes on github so people know what the file should look like
- the code reads the file at the start with `open()` and sticks it at the end of the system prompt

### result
alfred knows the stuff from my file now, and source control doesn't show about_me.txt so it's not going on github, renamed the file to see what happens if it's missing: FileNotFoundError: [Errno 2] No such file or directory: 'data/about_me_of.txt'. makes sense, the code tries to open a file that's not there

### stuff i learned
- public code, private data. same idea as .env for api keys

### problems
- nothing broke this time



## Stage 5b: saving conversations (13/10/2026)

goal: alfred forgets everything when i close the program because the messages list only exists while it runs. going to save the convo in a file after every answer and load it back when it starts

### my prediction
the first time it will tell me that there are 0 or X old messages, i will test it with a question about what i ate or something, close the program, and ask it what i ate. I think it will work. 


### screenshots

![p1 of main ](docs/screenshots/image-17.png)
![p2 of main](docs/screenshots/image-18.png)
![big error](docs/screenshots/image-19.png)
![empty file](docs/screenshots/image-20.png)
![non-existant history file](docs/screenshots/image-21.png)
![working code using a functional history file](docs/screenshots/image-22.png)
![memory testing](docs/screenshots/image-23.png)
![mission failed successfully](docs/screenshots/image-24.png)
![testing memory again](docs/screenshots/image-25.png)
![ollama 3.1:8b test](docs/screenshots/image-26.png)
![history with date](docs/screenshots/image-27.png)
![new date update](docs/screenshots/image-28.png)
![ollama test with new updates](docs/screenshots/image-29.png)

### problems
- got a JSONDecodeError on startup. history.json existed but was empty, and an empty file isn't valid json. my code only checked if the file existed, not if what's inside was ok
- could happen for real: "w" mode empties the file as soon as it opens, so if the program stops right while saving you get an empty file
- fixed it with try/except around json.load only. first version caught every error with a bare `except:`, bad idea because it would hide other bugs, now it only catches JSONDecodeError
- also forgot the else at first so if the file didn't exist `history` was never created
- after the fix it said "loaded 4 old messages" but alfred acted like he didn't remember anything. printed len(messages) before the loop and got 9 (system + 8 old ones) so the code was fine, he was getting the history
- opened history.json: the burger message was there but also his answers saying "i don't remember anything". so after every restart he was rereading himself saying that and kept going with it. my questions were also super vague ("what was our last conversation?") which makes small models give the default "i don't keep memories" answer
- deleted the file, told him what i ate, restarted and asked "what did i have for lunch?" and he got it
- also he said my burger was "a bit of a rushed affair" which i never said, hallucination++
- after fixing the prompt: "what did i eat?" works but "what was our last conversation about?" and he made up something about my daily schedule. finding one fact is easy for him but summarizing is harder so he guesses
- also realized history.json is just one long list with no dates, so he can't even tell where the last conversation starts. he doesn't know when anything was said
- history.json was one long list with no dates so alfred couldn't tell where the last convo started. now when the program starts and there's old history, it adds a system message with the date and time like "A new session has started : 13/10/2026 12:37"
- typed `message` instead of `messages` so it was appending to a list that doesn't exist
- put `print(...)` inside the content. print shows text but returns None, so the content would've been None. an f-string on its own is already text, no need for print
- first date format had commas everywhere, looked like a list of numbers. switched to `%d/%m/%Y %H:%M`

### result
- told him what i ate, quit, restarted and he remembered. the file is just my convo saved as json
- the date comes up at the start of every session, and is shown in the history.json file

### stuff i learned
- json = text format to save lists and dictionaries
- save after every answer, not just on quit, otherwise a crash loses everything
- try/except only around the line that can fail, and catch the specific error, not everything
- when the code is right but the bot acts weird, check what it actually receives (print it) and what's in the data
- change one thing at a time when testing, otherwise you don't know what fixed it

### bigger model test
- tried llama3.1:8b (8 billion parameters) instead of llama3.2 (3 billion). with 16gb of ram my mac handles it fine, answers come in like 3 seconds max changed only the model, same test as before so it's a fair comparison. the 8b one is just better overall, follows the rules and the convo better. keeping it also put the model name in a constant at the top OLLA so switching models is one line now



## Stage 6: chat interface in the browser (13/10/2026)

goal: chat with alfred in a real web page instead of the terminal. using streamlit, it turns a python script into a web page so no html/css needed. keeping main.py for the terminal version and making a new app.py for the web one

picked streamlit because it's pure python and has chat stuff built in. other options were gradio, flask/fastapi with html/js (more control but takes time to code) or a telegram bot. might do a fastapi version later

#### problems (setup)
- `pip install streamlit` crashed on pyarrow. in the log: `pyarrow!=25.0.0,<26` from streamlit, so streamlit only accepts pyarrow below 26. but only pyarrow 26 has a pre-built version for python 3.15. pip took 25.0.1, which only exists as source code (.tar.gz instead of .whl) for 3.15, tried to compile it and failed
- fixed it by switching the project to python 3.14: committed first to be safe, deleted .venv, made a new one with python3.14, reinstalled everything with `pip install -r requirements.txt`. my code didn't change at all
- lesson: newest python isn't always the best choice, libraries need time to catch up. and read the dependency lines in the log, the answer wasn't in the big error at the bottom
- after that alfred took ~5s instead of 3 for the first answer. not python's fault, ollama unloads the model from ram when it's not used for a while, so it has to load it again

### 6.1 first page (14/10/2026)
made src/app.py, 2 lines: import streamlit and a title. you run it with `streamlit run` instead of `python`, it opens a page in the browser at localhost:8501. the terminal stays busy while the app runs, ctrl+c to stop it

#### screenshots
![Alfred on the screen](docs/screenshots/image-30.png)
![alfred code](docs/screenshots/image-31.png)

#### problems
- `streamlit: command not found`, the venv wasn't active (new terminal, new day). `source .venv/bin/activate` fixed it
- a weird `DeltaGenerator(...)` line showed up in the terminal. i had a print around st.title, same mistake as the print inside content in 5B. st.title already shows the title on the page, no print needed
- the terminal shows a "Network URL" = anyone on the same wifi can open my app. fine for now but i'll need to lock it to my mac only before connecting alfred

### 6.2 the counter test (14/10/2026)
streamlit reruns the whole script every time i click something. made a counter with a button to see what that does

#### prediction
i think the counter will work and add up normally

#### screenshots
![four clicks and display it](docs/screenshots/image-32.png)

#### problems
- added `clicked = False` at the end to "reset" the button, but it did nothing. the variable isn't used after and gets a new value on the next rerun anyway, so deleted it
- first try with session_state was a mess: i read `st.session_state["count"]` before creating it, checked `"count" not in count` instead of in session_state, and wrote `["count":0]` instead of `["count"] = 0`
- also did `count += 1` on a copy, so the value in session_state never changed

#### result
stuck at 1 with a normal variable. every click reruns the whole file so `count = 0` runs again every time

fix: st.session_state, a dictionary streamlit keeps alive between reruns. only set it to 0 if it's not in there yet, then add 1 directly to the value in session_state. a normal variable would just be a copy

### 6.3 chat page, no ai yet (15/10/2026)
made the chat interface with an echo bot that just repeats what i type, so if something breaks i know it's the interface and not ollama

- st.chat_input = the input box at the bottom, gives back what i typed or None
- st.chat_message("user" / "assistant") = a bubble
- messages saved in st.session_state as a list, same format as alfred's (role + content)
- a for loop redraws every old message on each rerun, otherwise they'd disappear

#### screenshots
![chat interface echo](docs/screenshots/image-33.png)

#### problems
- typed `st.session_State` with a capital S, python is case sensitive
- tried to get the role straight from the whole list (`st.session_state["messages"]["role"]`). a list doesn't have a role, each message inside it does. that's what the for loop is for, it gives me one message at a time
- wrote `msg["role"]["content"]` like content was inside role, but they're two separate fields of the same message
- for the new message i used `msg` but it only exists inside the loop. the new text is in the variable from chat_input
- used `NULL` like in c, in python it's `None`. and `if user_inp:` is enough since None counts as false
- appended `["user"]` instead of a full dictionary with role and content

#### prediction (refresh)
the messages won't be there because they are not stored anywhere

#### result
the messages dissapeared 



### 6.4 locking the app to my mac
the terminal showed a network url, so anyone on the same wifi (like at school) could open alfred and read my stuff once he's connected. made .streamlit/config.toml with a [server] section and address = "localhost". the log went from `started on :::8501` (every network) to `started on localhost:8501` (only my mac) and the network url is gone

#### problems
- didn't get the toml format at first, wrote `key = "value"` literally then `dark = "dark"`. a section in [ ], then the setting name = the value
- streamlit detected the config change by itself and said to restart it
- first refresh test said "site cannot be reached", the app wasn't running (i had stopped it with ctrl+c). the browser page is just a client, it needs the streamlit server running in the terminal

### screenshots
![only local show](docs/screenshots/image-34.png)
![testing history number of messages](docs/screenshots/image-37.png)



### 6.5 moving alfred's logic into its own file (15/10/2026)
goal: make src/alfred.py with all of alfred's logic in functions, so main.py and app.py both use the same code instead of each having a copy. if i change the prompt in one file and forget the other, the two alfreds would act differently

a function = a named block of code i can call whenever. `def` to create it, what goes in the () is its input, `return` is what it gives back. without return it gives back None (same as print)

4 functions:
- `load_history()` loads history.json and returns the list
- `save_history(messages)` saves the convo to history.json
- `start_messages()` builds the full messages list (system prompt + about me + history + session marker)
- `ask_alfred(messages)` sends everything to ollama and returns the reply

did them one at a time and tested each one alone with a temporary test file (src/test_alfred.py)

#### load_history()
moved my loading block into a function. at first i wrote `return json.load(f)` directly, but then the "loaded X old messages" print after it never ran because return ends the function right away. it also used a `history` variable that didn't exist anymore. fixed it by storing the list in a variable first, then printing, then returning it

#### save_history(messages)
moved my saving block into a function that takes the messages list as input. no return needed, it just writes the file

tested it: loaded the history (26 messages), added a test message, saved it with a fake system message in front, loaded it again → 27. the fake system message got skipped by `[1:]` like it should

#### start_messages()
moved the about_me reading and full_prompt inside the function, now nothing runs outside functions in alfred.py except constants. it calls load_history() instead of copying the code, builds the messages list, adds the session marker and returns everything

tested it: 29 items = 1 system + 27 history + 1 marker. 27 because the test message from the save_history test was still in there, removed it after

#### ask_alfred(messages)
sends the messages to ollama and returns just the reply text. one job only: no append, no saving, the caller decides what to do with the answer. tested it with fake messages so my real history wasn't touched

### screenshots 
![testing the alfred functions load_history](docs/screenshots/image-35.png)
![test message](docs/screenshots/image-36.png)
![alfred code ](docs/screenshots/image-38.png)
![start messages test](docs/screenshots/image-39.png)
![hello to you](docs/screenshots/image-40.png)
![new main code](docs/screenshots/image-41.png)
![new main test](docs/screenshots/image-42.png)

#### problems
- typed `python run src/test_alfred.py` out of habit from streamlit. python takes the file directly, only streamlit needs `run`. the error said it couldn't find a file called run
- `save_history() takes 0 positional arguments but 1 was given`: forgot `messages` in the parentheses of the def, so the function didn't accept any input
- `object of type 'function' has no len()`: wrote `load_history` without the (). without () you get the function itself, with () you run it and get what it returns
- code at the top of alfred.py (outside functions) runs as soon as another file imports it. had `full_prompt = ... + about_me` up there after moving the about_me reading into the function, so about_me didn't exist anymore. moved it inside start_messages()
- in start_messages i called `load_history()` without storing the result so `history` didn't exist, used `full_date` before creating it (python runs top to bottom), and forgot `return messages` so it would've given back None
- had comments like "FIXED: ..." in the code. comments should say what the code does, the history of changes is what git commits are for. removed them
- ask_alfred test crashed with a ValidationError inside ollama. it said the `role` field was missing and showed my message with `roles` in it. typo in the test file, not in the function. the crash showed up in alfred.py but the mistake was in the data i passed in

#### switching main.py to alfred.py
main.py went from ~80 lines to 18. it only does the terminal stuff now (input, quit, print) and calls the functions from alfred.py for everything else. the appends stay in main.py because ask_alfred only returns the reply, main.py decides what to do with it

#### problems (main.py switch)
- imported load_history but main.py never uses it, start_messages already calls it. removed it
- wrote the message with [ ] instead of { }. [ ] = list, { } = dictionary, a message is a dictionary
- had "me" in quotes so it would've saved the word "me" every time instead of what i typed. variables go without quotes
- called ask_alfred(messages) without storing the result, the reply just disappeared. same mistake as load_history in start_messages

#### result
alfred did remember our last conversation and the count went up



### Stage 6.6 : connect Alfred to the chat page.(16/10/2026)
replaced the echo bot with the real alfred using the same functions as main.py: start_messages() for the starting list, ask_alfred() for the reply, save_history() after each answer

#### prediction
the history will be saved and we will continue where we left off

#### problems
- first version passed my text (user_inp) to ask_alfred and save_history instead of the whole messages list. ask_alfred would've sent a sentence instead of a convo, and save_history would've replaced my whole history.json with a piece of text. made a backup before testing just in case
- was saving twice per exchange, once is enough, after alfred's reply is in the list
- had the save inside the assistant bubble block, works but makes no sense, moved it out
- the backup file wasn't in .gitignore so it would've gone on github.added it to .gitignore


#### result
- works. after cmd+r all the messages come back, even the ones from right before the refresh. session_state still resets on refresh, but start_messages() reloads history.json, and since i save after every answer the file is always up to date. 
- checked the numbers: 29 loaded at first, +1 session marker, +4 for 2 exchanges = 34 after the refresh
- the "loaded X old messages" shows in the terminal, not the page. print() always goes to the terminal where the streamlit server runs, only st.something draws on the page



### screenshots
![alfred answering in the browser](docs/screenshots/image-43.png)
![terminal after refresh](docs/screenshots/image-44.png)



### 6.7 making it look like mine (16/10/2026)
wanted a darker black and blue look instead of the default red and orange

- avatars: 🦇 for me and 🤵 for alfred. made an AVATARS dictionary at the top of app.py that maps each role to its emoji, so in the loop i just do `AVATARS[msg["role"]]`. if i want to change an emoji later it's one line
- colors: added primaryColor, backgroundColor, secondaryBackgroundColor and textColor under [theme] in config.toml, with hex codes for dark navy and blue

#### screenshots
![more personalized streamlit version](docs/screenshots/image-45.png)
![config.toml new](docs/screenshots/image-46.png)

#### problems
- added the avatars only to the 2 bubbles drawn after sending a message, but everything on screen still had the default red/orange icons. on every rerun the loop redraws all the bubbles, and the loop had no avatar. had to add it in all 3 places
- passed the emoji without a name like `st.chat_message("user", "🦇")`. better to write `avatar="🦇"`, some inputs have to be named (keyword arguments)
- the red border around the input box comes from primaryColor, changing it to blue fixed it



## Stage 7: finishing (16/10/2026)

### 7.1 docstrings
added a docstring to each function in alfred.py: what it does, what it takes, what it returns. it's a triple-quoted string right at the start of the function. vs code shows it when i hover over the function somewhere else, and help() prints it

#### problems
- first versions didn't match what the code actually does: said start_messages returns a welcome message (it returns the messages list), said ask_alfred sends the last message (it sends the whole convo), called messages a dictionary (it's a list of dictionaries), and said save_history skips a "welcome message" (it skips the system message)
- lesson: a wrong docstring is worse than none, someone would trust it. had to read my own code again line by line to describe it right

### screenshots
![fct info](docs/screenshots/image-47.png)


### 7.2 clear conversation button
added a sidebar with a "clear conversation" button. when clicked: clear_history() empties history.json, start_messages() rebuilds a fresh list (personality + my info, no history), and st.rerun() redraws the page right away so the old bubbles disappear

made a new function clear_history() in alfred.py instead of hacking save_history. it's the same as save_history but writes an empty list and takes no input

the order matters: empty the file first, then rebuild. start_messages() loads the history file, so rebuilding first would load the old convo again

#### problems
- clear_history had `messages` in its parentheses even though it doesn't use it and app.py calls it with nothing, would've crashed with "missing 1 required positional argument"
- first tried `load_history(st.session_state["messages"])` to rebuild. wrong function (only gives the history, not alfred's personality), wrong input (it takes nothing) and the result wasn't stored. start_messages() does the full job
- the "no history" note had a hidden bug: save_history saves everything except item 0, so the note got saved too. next session alfred would've read in his own history that there's no history. changed it to "the very first conversation started on [date]. nothing was said before this point", it stays true forever wherever it ends up
- lesson: anything that gets saved has to still make sense when it's reloaded later

#### result
[what alfred said after clearing]

### screenshots
![sidebar with clear conversation](docs/screenshots/image-48.png)
![new sidebar with clear conversation](docs/screenshots/image-49.png)
![history cleared](docs/screenshots/image-50.png)
![halucination fix](docs/screenshots/image-51.png)
![history fix](docs/screenshots/image-52.png)


### 7.3 cleanup
- fixed comments that didn't match the code anymore (bubbles, "save" used for things that don't save)
- cleaned the system prompt: there was a line i pasted by mistake ("keep the anti-hallucination part") and the same rule written 3 times
- renamed user_inp to user_input so app.py and main.py match
- fixed typos and spacing (no space before `:`, 2 blank lines between functions)
- made start_messages() handle a missing about_me.txt: if the file isn't there it prints a warning and uses an empty string instead of crashing. same if/else shape as load_history. also put the path in a constant ABOUT_ME_FILE like HISTORY_FILE
- restored about_me.example.txt with `git checkout HEAD -- data/about_me.example.txt`, git can bring back any file from a commit

#### problems
- deleted about_me.example.txt thinking it was useless, but about_me.txt is gitignored so anyone cloning the repo would crash on start with no idea what the file should contain

### screenshots
![about me fix](docs/screenshots/image-53.png)