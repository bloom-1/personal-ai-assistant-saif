# Alfred

My own AI assistant, running fully on my Mac. He's a butler called Alfred, he remembers our conversations, and I can talk to him in the terminal or in a chat page in my browser.

![Alfred chat page](docs/screenshots/alfred-chat.png)

## What it does

- Runs a local AI model with Ollama: free, and my conversations never leave my computer
- Has a personality (a calm, polite British butler) set with a system prompt
- Knows some info about me from a private file that stays off GitHub
- Remembers past conversations, even after closing the app, and knows when each session started
- Works in two ways: a terminal version and a web chat page
- Has a "clear conversation" button to start fresh
- Doesn't crash if the history file is broken or a file is missing

## Tech stack

- Python 3.14
- Ollama with the llama3.1:8b model that runs locally
- Streamlit for the chat page

## How it works

The model has no memory on its own: every time I send a message, it only knows what's in the list it receives. So the app keeps the whole conversation in a list and sends all of it each time.

That list starts with a system message (Alfred's personality + info about me), then the saved history, then a marker with the date of the current session. After every answer, the conversation is saved to a JSON file and loaded back on the next start.

All of Alfred's logic lives in `src/alfred.py`. The terminal version (`main.py`) and the web version (`app.py`) both use it, so there's only one "brain" to maintain.

## Getting started

### 1. Install Ollama and the model

Download Ollama from [ollama.com](https://ollama.com), open it, then:

```bash
ollama pull llama3.1:8b
```

### 2. Clone the project and set up Python

Needs **Python 3.14** (3.15 is too new for one of Streamlit's dependencies right now, so I chose to go with 3.14).

```bash
git clone https://github.com/bloom-1/personal-ai-assistant-saif.git
cd personal-ai-assistant-saif
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Add your info (optional)

```bash
cp data/about_me.example.txt data/about_me.txt
```

Then edit `data/about_me.txt` with whatever you want Alfred to know about you. If you skip this, Alfred still works, he just won't know anything about you, so it's better to edit it if you want a more personalized experience.

### 4. Run it

Make sure the Ollama app is open, then either:

```bash
python src/main.py          # terminal version
streamlit run src/app.py    # web version
```

## Project structure

```
personal-ai-assistant-saif/
├── src/
│   ├── alfred.py        # all of Alfred's logic (prompt, history, talking to the model)
│   ├── main.py          # terminal version
│   └── app.py           # web chat version (Streamlit)
├── data/
│   └── about_me.example.txt   # example of the private info file
├── .streamlit/
│   └── config.toml      # theme + only allow connections from this computer
├── docs/screenshots/    # screenshots used in the journal
├── JOURNAL.md           # step by step build journal
├── requirements.txt
└── LICENSE
```

## Privacy

- Everything runs locally, nothing is sent to an online AI service, so nothing leaves your computer
- `data/about_me.txt` and `data/history.json` are in `.gitignore`, so personal info and chats never go on GitHub
- The web app only accepts connections from the same computer (not from other devices on the Wi-Fi)

## What I learned

I'm an engineering student and I wanted to understand how AI apps actually work instead of just using them. I built Alfred step by step: talking to a local model, figuring out why it forgets everything, saving conversations, organizing the code into functions, and a lot of debugging. Everything I did, including my mistakes and how I fixed them, is in the [build journal](JOURNAL.md).

## Next steps

- Answers appearing word by word (streaming)
- Choosing the model from the sidebar
- Summarizing old conversations when the history gets too long
- Letting Alfred use tools (time, weather, calculations)
- Answering questions from my course PDFs
- A FastAPI + HTML version
