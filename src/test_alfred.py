from alfred import ask_alfred

test_messages = [
    {"role":"system", "content":"You are a test bot. Answer in 4 words max."},
    {"role":"user", "content":"Say hello"}
]

print(ask_alfred(test_messages))