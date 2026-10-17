import streamlit as st
from alfred import save_history, start_messages, ask_alfred, clear_history

AVATARS = {"user":"🦇", "assistant":"🤵"}
MODELS = ["llama3.1:8b", "llama3.2"]
st.title("Alfred")

with st.sidebar:
    ai_model = st.selectbox("Model", MODELS)
    if st.button("Clear conversation"):
        clear_history()
        st.session_state["messages"] = start_messages()   #loads alfred's personality + my info + no history
        st.rerun()

if "messages" not in st.session_state:
    st.session_state["messages"] = start_messages()   #loads alfred's personality + my info + history

for msg in st.session_state["messages"]:    #for every message in the session_state
    if msg["role"] != "system":
        with st.chat_message(msg["role"], avatar=AVATARS[msg["role"]]):      # draw a bubble for this message
            st.write(msg["content"])            # show the content of the person's message


user_input = st.chat_input("Message Alfred... ")

if user_input:
    st.session_state["messages"].append({"role":"user", "content":user_input}) #saving my message in the list
    with st.chat_message("user", avatar=AVATARS["user"]):      # draw a bubble for this message
        st.write(user_input)  

    with st.spinner("Alfred is thinking..."):
        reply = ask_alfred(st.session_state["messages"], model=ai_model)    #put the reply in a variable

    st.session_state["messages"].append({"role":"assistant", "content":reply})   #add it to the list
    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        st.write(reply)     # show alfred's reply
    save_history(st.session_state["messages"])



