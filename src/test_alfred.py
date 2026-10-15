from alfred import load_history, save_history

history = load_history()
print("Before: ", len(history))

history.append({"role":"user", "content":"test message"})
save_history([{"role":"system", "content":"fake system"}] + history)

print("after: ", len(load_history()))