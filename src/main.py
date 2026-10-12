# Import the ollama library so Python can talk to the Ollama server
import ollama

# sends my message to the model and waits for the reply (ollama needs to be open or this crashes, learned that the hard way)
response = ollama.chat(
    model="llama3.2",        # the model I pulled earlier
    messages=[
        {"role": "user", "content": "Hello! Introduce yourself in one sentence."} # role = who's talking, content = what they say
    ],
)

print(response["message"]["content"]) # the reply is nested: response -> message -> content